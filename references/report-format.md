# Report data contract

Save UTF-8 JSON. `render_report.py` validates required fields and local figure paths.

```json
{
  "report_title": "论文组会汇报",
  "paper": {
    "title": "Paper title",
    "authors": ["First Author¹", "Second Author¹²", "Third Author²"],
    "affiliations": ["¹ University A", "² Institute B"],
    "venue": "Venue/year",
    "pdf": "paper.pdf"
  },
  "application_context": "智能运维可视化",
  "speaker_script": {
    "target_minutes": 10,
    "opening": "今天我想用十分钟介绍这篇工作。我们先看它解决什么问题，再看它怎样用知识图谱让回答更可靠。",
    "sections": [
      {"title": "方法概览", "duration_seconds": 60, "script": "这一页先不要急着记模块名。可以把它理解为：模型先提出可能的答案方向，再回到知识图谱里找证据，最后只保留真正有帮助的信息。"}
    ],
    "qa": [
      {"question": "它和普通 RAG 的主要区别是什么？", "answer": "普通 RAG 多从原始问题直接检索；这里先让模型补出可能相关的线索，再用图谱关系检查这些线索是否站得住脚。"}
    ]
  },
  "language": "zh",
  "duration_minutes": 20,
  "sections": [
    {
      "type": "paper",
      "title": "方法概览",
      "takeaway": "一句话讲清方法思想",
      "takeaway_source": "p. 4, Fig. 2",
      "points": [
        {"text": "关键设计及其作用", "source": "p. 4, §3.1"}
      ],
      "figure": {"path": "figures/page-4-image-1.png", "caption": "原论文 Fig. 2", "source": "p. 4, Fig. 2"},
      "speaker_notes": "先解释直觉，再指向图中的两个关键模块。"
    },
    {
      "type": "analysis",
      "title": "局限与讨论",
      "takeaway": "实验覆盖可能不足",
      "points": [{"text": "缺少跨领域验证；这是基于实验设置的判断。", "source": "p. 7, Table 3"}],
      "speaker_notes": "明确说明这不是作者直接给出的结论。"
    }
  ]
}
```

`type` is `paper`, `analysis`, or `question`. `paper.authors` accepts a full string or a list of author strings; use every author printed on the first page, never “et al.”. `paper.affiliations` is optional and accepts a string or list of affiliation strings; include it only when it is legible in the source PDF. The title header/page renders both fields. For `paper`, every nonempty takeaway requires `takeaway_source`, and every point requires `source`. Analysis and questions may cite evidence, but their type label must remain visible in HTML only. Figure paths are relative to the JSON file (or absolute). Figure source and caption are required. The renderer refuses missing figures and malformed data. Use concise strings; no Markdown or HTML in fields. `paper.pdf` is provenance metadata and is not embedded in output.

`application_context` is optional. When present, include a final analysis/reflection section that gives grounded transfer ideas and deployment caveats for that context; do not present these as results established by the paper. `speaker_script` is required whenever PPTX is requested: set `target_minutes` to 10 unless the user specifies otherwise; provide a short `opening`, one ordered entry for every report section, and at least three `qa` entries. Each passage should explain what the audience should notice, use short everyday sentences, expand or explain a necessary acronym on first use, and avoid merely repeating the slide text. For manual mode, the JSON is an editable handoff. Show the user the narrative, section order, takeaways, evidence, figure plan, speaker-note intent, and script plan before rendering. After approval, update this same file and render.

For an ordinary 20-minute report, plan enough material to explain one key method diagram and one key-evidence experiment section, with time reserved for critique and questions. The key-evidence section should show only the most decision-relevant comparison and, when needed, one ablation that explains the claimed mechanism. Keep detailed benchmark matrices, secondary metrics, hyperparameter sweeps, and routine setup descriptions out of the main flow unless they change the central conclusion; put them in speaker notes instead. Merge or omit sections according to paper complexity. Do not fill pages with generic background or copy long paper passages.

Output conventions: HTML is a self-contained `report.html` with inline styles and embedded local images. Its opening header shows the paper title, complete authors, and provided affiliations, followed by all sections in normal, continuous page flow; it has no table of contents, slide controls, card-like page containers, speaker-note/disclosure blocks, citations/source text, type labels, page numbers, footer metadata, or duration. PPTX is `report.pptx`, 16:9, with the same complete title metadata, one section per slide, and notes in the notes pane; its visible surface follows the same clean rule. When PPTX is generated, write a sibling `speaker-script.md` containing the opening, slide-by-slide script with timings, and a final “可能的提问与回答” section. HTML and PPTX section ordering, point text, and figure assignments must match; speaker notes are deliberately PPTX-only.

For readable PPTX pages, use at most five concise points per section. The renderer rejects a point or takeaway over 120 characters; split dense sections before rendering.
