#!/usr/bin/env python3
"""Extract page-aware text and large embedded figure candidates from a paper PDF."""

import argparse
import io
import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def extract(pdf_path: Path, out_dir: Path, min_size: int = 220, crop=None) -> dict:
    reader = PdfReader(str(pdf_path))
    out_dir.mkdir(parents=True, exist_ok=True)
    image_dir = out_dir / "figures"
    image_dir.mkdir(exist_ok=True)
    pages, figures = [], []
    seen = set()
    for page_number, page in enumerate(reader.pages, 1):
        pages.append({"page": page_number, "text": page.extract_text() or ""})
        for image_number, source_image in enumerate(page.images, 1):
            try:
                with Image.open(io.BytesIO(source_image.data)) as picture:
                    width, height = picture.size
                    if min(width, height) < min_size:
                        continue
                    picture = picture.convert("RGB")
                    fingerprint = hash(picture.tobytes())
                    if fingerprint in seen:
                        continue
                    seen.add(fingerprint)
                    name = f"page-{page_number}-image-{image_number}.png"
                    picture.save(image_dir / name)
                figures.append({"path": f"figures/{name}", "page": page_number, "source": "pdf-embedded", "width": width, "height": height, "original_name": source_image.name})
            except Exception as exc:
                figures.append({"page": page_number, "source": "pdf-embedded", "original_name": source_image.name, "error": str(exc)})
    if crop:
        from pdf2image import convert_from_path
        page_number, x0, y0, x1, y1 = crop
        page_number = int(page_number)
        if not 1 <= page_number <= len(reader.pages):
            raise ValueError("Crop page is outside PDF")
        x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
        page = reader.pages[page_number - 1]
        page_w, page_h = float(page.mediabox.width), float(page.mediabox.height)
        if not (0 <= x0 < x1 <= page_w and 0 <= y0 < y1 <= page_h):
            raise ValueError("Crop coordinates must be inside page, in points from top-left")
        rendered = convert_from_path(str(pdf_path), dpi=220, first_page=page_number, last_page=page_number)[0]
        sx, sy = rendered.width / page_w, rendered.height / page_h
        cropped = rendered.crop((round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy)))
        name = f"page-{page_number}-crop-{len(figures) + 1}.png"
        cropped.save(image_dir / name)
        figures.append({"path": f"figures/{name}", "page": page_number, "source": "pdf-page-crop", "width": cropped.width, "height": cropped.height, "region_points": [x0, y0, x1, y1]})
    (out_dir / "paper_pages.json").write_text(json.dumps({"pdf": str(pdf_path.resolve()), "pages": pages}, ensure_ascii=False, indent=2), encoding="utf-8")
    (image_dir / "index.json").write_text(json.dumps({"pdf": str(pdf_path.resolve()), "figures": figures}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"pages": len(pages), "figure_candidates": len([f for f in figures if f.get("path")]), "text": str(out_dir / "paper_pages.json"), "figure_index": str(image_dir / "index.json")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--min-size", type=int, default=220, help="Minimum width and height of embedded image candidates")
    parser.add_argument("--crop", nargs=5, metavar=("PAGE", "X0", "Y0", "X1", "Y1"), help="Crop one figure region in PDF points from top-left")
    args = parser.parse_args()
    print(json.dumps(extract(args.pdf, args.out, args.min_size, args.crop), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
