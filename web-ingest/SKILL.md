---
name: web-ingest
description: Use when converting web content (URLs, YouTube videos, RSS feeds, Wikipedia pages) to clean Markdown before ingesting into a wiki or LLM workflow. Triggers on: "get YouTube transcript", "scrape this page", "fetch this article to markdown", "ingest this URL into wiki", "clip this web page", "pull this RSS feed", any http/https URL given as ingest source.
---

# web-ingest

**Purpose**: Fetch and convert web content to clean Markdown, then chain into `llm-wiki-ingest` or any LLM workflow. Replaces the manual Obsidian Web Clipper step.

**Python env**: `/opt/homebrew/anaconda3/bin/markitdown`

---

## URL Type Gate

```
URL given → What type?
  youtube.com / youtu.be   → YouTubeConverter (transcript, no local model)
  wikipedia.org            → WikipediaConverter (structured Markdown)
  RSS feed URL             → RssConverter (article list)
  any other URL            → HtmlConverter (strips nav/ads, clean body)
```

---

## Commands

### Any URL (auto-detected)
```bash
markitdown "https://example.com/article"
markitdown "https://www.youtube.com/watch?v=VIDEO_ID"
markitdown "https://en.wikipedia.org/wiki/Topic"
```

### Save to raw/sources/
```bash
markitdown "https://..." -o raw/sources/article-slug.md
```

### Python
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)  # Full transcript as Markdown
```

---

## Chain to Wiki Ingest

Output lands in `raw/sources/`. Invoke `llm-wiki-ingest` on that file normally.

---

## Quick Reference

| Source | Converter | Notes |
|--------|-----------|-------|
| YouTube URL | YouTubeConverter | No Whisper needed — pulls existing transcript via API |
| Wikipedia URL | WikipediaConverter | Structured with sections |
| RSS feed URL | RssConverter | Article titles + summaries |
| Any URL | HtmlConverter | Strips nav/footer/ads, body only |

---

## Rules

- YouTube: works only if video has captions (auto-generated or manual). No captions = no transcript. Fall back to hyperframes-media transcribe if needed.
- HTML: some paywalled sites return little content — check output before ingesting.
- Never feed raw URL into llm-wiki-ingest; always convert first so raw/ has a proper .md file.
- Output file slug = URL-derived lowercase-hyphenated name.
