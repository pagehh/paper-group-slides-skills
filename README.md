# Paper Group Slides

Turn one AI/ML paper PDF into a clean group-meeting presentation.

`paper-group-slides` produces a restrained PPTX deck, a continuous HTML report, and—when PPTX is requested—a plain-language Markdown speaker script. It uses the source PDF as the authority and does not invent paper claims.

## Deliverables

- `report.pptx` — editable, clean academic slides.
- `report.html` — a self-contained, continuously scrollable HTML report.
- `speaker-script.md` — a roughly ten-minute, slide-by-slide script with speaking times and a final Q&A section.
- `report.json` and extracted figures — working artifacts that preserve source mapping.

The visible PPTX and HTML show the paper title, complete author list, affiliations when legible, concise content, and original figures. They intentionally omit citations, type labels, page numbers, time labels, and presenter notes.

## Requirements

- Python 3.10+.
- Python packages: `pypdf`, `pdfplumber`, `Pillow`, and `python-pptx`.
- `pdf2image` plus Poppler are optional but recommended for cropping vector figures from PDF pages.
- Microsoft PowerPoint is optional and only needed for PowerPoint-based visual inspection or export.

The skill runs local scripts. Review `scripts/` before installation and only use PDFs and skill packages you trust.

## Use it

After installation, give the agent a local PDF path and a clear request:

```text
Use paper-group-slides to turn /path/to/paper.pdf into a Chinese, 20-minute group-meeting report.
Use auto mode. Generate both HTML and PPTX. Add a reflection for intelligent operations visualization.
```

- `manual`: first review an editable outline, figure plan, and script plan.
- `auto`: complete extraction, writing, rendering, and checks in one run.
- Output: `html`, `pptx`, or `both`.

For PPTX output, the report must include a `speaker_script`: a short opening, one spoken passage per content slide, and at least three likely questions with concise answers. The renderer writes it as `speaker-script.md` next to `report.pptx`.

## Install from this repository

```bash
git clone https://github.com/pagehh/paper-group-slides-skills.git
```

Keep the entire directory together. `SKILL.md` references `scripts/` and `references/`, so copying only `SKILL.md` will not work.

### Codex

Personal scope:

```text
~/.codex/skills/paper-group-slides/
```

Codex Desktop project scope:

```text
<your-project>/.agents/skills/paper-group-slides/
```

Open a new Codex session after copying, then invoke `$paper-group-slides` or ask Codex to prepare a group-meeting paper report. See [OpenAI Skills](https://openai.com/academy/skills/) and [Codex app skills](https://openai.com/index/introducing-the-codex-app/).

### Claude Code and Claude Agent SDK

Project scope:

```text
<your-project>/.claude/skills/paper-group-slides/
```

Personal scope:

```text
~/.claude/skills/paper-group-slides/
```

Start a new Claude Code session and ask Claude to use `paper-group-slides` with your PDF. See the [Claude Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [Claude Code/SDK skills guide](https://code.claude.com/docs/en/agent-sdk/skills).

### Claude.ai

Zip the *contents* of this repository so `SKILL.md` is at the ZIP root, then upload it in Claude's Skills settings. Code execution and file creation need to be available; feature availability and upload permissions depend on your Claude plan and workspace. See [Creating custom skills for Claude](https://claude.com/docs/skills/how-to).

### ChatGPT

Create a ZIP with `SKILL.md` at the ZIP root and include `scripts/` and `references/`. In an eligible workspace, open **Skills** → **Create** → **Upload from your computer**. Availability and upload permissions vary by plan and workspace. See [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

### GitHub Copilot

Project scope:

```text
<your-project>/.github/skills/paper-group-slides/
```

Compatible project alternative: `<your-project>/.agents/skills/paper-group-slides/`.

Personal scope: `~/.copilot/skills/paper-group-slides/`. Copilot supports skills in the cloud agent, CLI, app, and supported IDE agent modes. See [GitHub's agent-skill guide](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

### Gemini CLI

Project scope:

```text
<your-project>/.gemini/skills/paper-group-slides/
```

Personal scope: `~/.gemini/skills/paper-group-slides/`. Mark the workspace as trusted if prompted, start a new session, and run `/skills list` to confirm discovery. See the [Gemini CLI skills tutorial](https://geminicli.com/docs/cli/tutorials/skills-getting-started/).

### Other Agent Skills-compatible clients

The package follows the portable `SKILL.md` convention: YAML frontmatter with `name` and `description`, plus scripts and references. For clients such as Cursor, Windsurf, OpenCode, or a custom runtime, copy the entire directory to the client’s documented skills directory or register it as a custom skill directory. Confirm discovery in that client before relying on it; paths and support levels vary by product and version.

## Quality rules

- Keep the PDF authoritative; do not invent methods, metrics, baselines, or figure meanings.
- Preserve complete authors and affiliations when legible; never replace authors with “et al.”.
- Show decisive evidence rather than a dense experiment dump.
- Keep the speaker script conversational: explain a necessary abbreviation once, use short sentences, and do not read slide bullets word for word.
- Label application reflections as analysis, not as conclusions proven by the paper.

## Repository layout

```text
SKILL.md                    Main workflow and constraints
agents/openai.yaml          Codex-facing metadata
scripts/inspect_pdf.py      Page-aware text and figure inspection
scripts/render_report.py    HTML, PPTX, and speaker-script renderer
references/report-format.md Report JSON and speaker-script contract
tests/test_workflow.py      Workflow tests
```

## Verify a local checkout

```bash
python -B -m unittest discover -s tests -v
```

Review generated HTML, PPTX, figures, and `speaker-script.md` before presenting. Refer to the repository-level license when distributing the skill.
