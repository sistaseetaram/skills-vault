# doc-ingest Converter Reference

## Install

```bash
# Already installed in anaconda env:
/opt/homebrew/anaconda3/bin/pip install "markitdown[docx,xlsx,pptx,epub,youtube-transcription]" ebooklib
```

Verify:
```bash
/opt/homebrew/anaconda3/bin/python3 -c "from markitdown import MarkItDown; print('OK')"
```

## Converter → Dependency Map

| Converter | Extra | Key Package | Notes |
|-----------|-------|------------|-------|
| DocxConverter | [docx] | mammoth | Preserves bold, italic, tables, headings |
| XlsxConverter | [xlsx] | openpyxl | Multiple sheets = multiple Markdown tables |
| XlsConverter | [xls] | xlrd | Legacy .xls only; prefer .xlsx |
| PptxConverter | [pptx] | python-pptx | Slide title → H2, content → bullets |
| EpubConverter | [epub] | ebooklib | Chapter nav preserved |
| IpynbConverter | built-in | — | Code cells, output, markdown cells |
| PlainTextConverter | built-in | — | .txt, .md, .csv, .tsv |
| HtmlConverter | built-in | beautifulsoup4 | → use web-ingest for URLs |

## Python API Examples

### XLSX with multiple sheets
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("data.xlsx")
# result.text_content has all sheets as Markdown tables
with open("data.md", "w") as f:
    f.write(result.text_content)
```

### PPTX slide deck
```python
result = md.convert("deck.pptx")
# Output: ## Slide 1: Title\ncontent bullets...
```

### Batch conversion
```python
import glob, os
md = MarkItDown()
for path in glob.glob("drop/*.docx"):
    result = md.convert(path)
    out = os.path.splitext(path)[0] + ".md"
    with open(out, "w") as f:
        f.write(result.text_content)
```

## CLI Reference

```bash
markitdown [file]            # stdout
markitdown [file] -o [out]   # write to file
markitdown --help            # all options
```

Full path if needed: `/opt/homebrew/anaconda3/bin/markitdown`
