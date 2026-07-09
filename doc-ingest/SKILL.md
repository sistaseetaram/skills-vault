---
name: doc-ingest
description: Use when converting a local document file (Word, Excel, PowerPoint, EPUB, Jupyter notebook) to Markdown before ingesting into a wiki or LLM workflow. Triggers on: "ingest this DOCX", "convert this Word doc", "turn this Excel into markdown", "parse this PPTX", "ingest this notebook", "raw document into wiki", file dropped with .docx/.xlsx/.xls/.pptx/.epub/.ipynb extension.
---

# doc-ingest

**Purpose**: Convert local non-text documents to clean Markdown, then chain into `llm-wiki-ingest` or any LLM workflow. Front door for raw files entering any wiki.

**Python env**: `/opt/homebrew/anaconda3/bin/markitdown` (use full path if `markitdown` not found in shell)

---

## Format Gate

```
Incoming file → What extension?
  .md / .txt        → skip conversion, go straight to llm-wiki-ingest
  .docx             → markitdown → .md → llm-wiki-ingest
  .xlsx / .xls      → markitdown → .md → llm-wiki-ingest
  .pptx             → markitdown → .md → llm-wiki-ingest
  .epub             → markitdown → .md → llm-wiki-ingest
  .ipynb            → markitdown → .md → llm-wiki-ingest
  .pdf              → /pdf skill → llm-wiki-ingest
  .mp3/.wav/.m4a/.mp4 → hyperframes-media transcribe (Whisper) → llm-wiki-ingest
  URL               → web-ingest skill
```

---

## Commands

### Single file
```bash
markitdown /path/to/file.docx > /path/to/raw/sources/output.md
# or
markitdown /path/to/file.docx -o /path/to/raw/sources/output.md
```

### Batch (directory)
```bash
for f in /path/to/drop/*.docx; do
  name=$(basename "$f" .docx)
  markitdown "$f" -o "/path/to/raw/sources/${name}.md"
done
```

### Python (when more control needed)
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("file.xlsx")
print(result.text_content)
```

---

## Chain to Wiki Ingest

After conversion, the `.md` output lands in `raw/sources/`. Then invoke `llm-wiki-ingest` on that file — it proceeds with its normal 10-step workflow.

---

## Quick Reference

| Format | Dep installed | Notes |
|--------|--------------|-------|
| .docx | mammoth ✅ | Tables, headings preserved |
| .xlsx | openpyxl ✅ | Each sheet → Markdown table |
| .xls | xlrd (if needed) | Legacy Excel |
| .pptx | python-pptx ✅ | Slides → headings + bullets |
| .epub | ebooklib ✅ | Chapter structure preserved |
| .ipynb | built-in ✅ | Code cells + output included |

---

## Rules

- Never modify `raw/`. Output to `raw/sources/`, then ingest from there.
- If conversion produces empty output, check file is not password-protected.
- For scanned PDFs (image-only), use `/pdf` skill with OCR, not markitdown.
- Batch only if user explicitly asks.
