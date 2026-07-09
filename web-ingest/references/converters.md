# web-ingest Converter Reference

## Install

```bash
# Already installed:
/opt/homebrew/anaconda3/bin/pip install "markitdown[youtube-transcription]"
# Core HtmlConverter is in base markitdown install
```

## Converter Map

| URL Pattern | Converter | Package | Notes |
|-------------|-----------|---------|-------|
| youtube.com, youtu.be | YouTubeConverter | youtube-transcript-api ✅ | Existing captions only, no local model |
| en.wikipedia.org | WikipediaConverter | requests ✅ | Structured sections |
| RSS feed URL | RssConverter | built-in | Items as Markdown list |
| Any other URL | HtmlConverter | beautifulsoup4 ✅ | Body extraction, strips nav/ads |

## CLI Examples

```bash
# YouTube
markitdown "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o raw/sources/video-title.md

# Wikipedia
markitdown "https://en.wikipedia.org/wiki/Zettelkasten" -o raw/sources/zettelkasten.md

# Article
markitdown "https://example.com/great-article" -o raw/sources/great-article.md

# RSS
markitdown "https://example.com/feed.xml" -o raw/sources/feed-snapshot.md
```

## Python Examples

```python
from markitdown import MarkItDown
md = MarkItDown()

# YouTube transcript
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
# Returns: full transcript with timestamps (if available)

# Clean article
result = md.convert("https://example.com/article")
# Returns: main body content as Markdown
```

## YouTube Transcript Notes

- Uses `youtube-transcript-api` — pulls existing CC/auto-generated captions
- No Whisper / no local model needed
- Falls back to `hyperframes-media transcribe` if video has no captions at all
- For private/unavailable videos → error; use hyperframes-media with downloaded audio

## Paywall / Rate Limit Handling

- Paywalled articles return minimal content (title + meta only) — check output before ingesting
- Some sites block scrapers — if content empty, use Obsidian Web Clipper manually instead
- Wikipedia and YouTube work reliably
