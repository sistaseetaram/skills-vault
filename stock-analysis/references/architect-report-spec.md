# Architect Report Spec

This is the "Architect AI Agent" role from the source workflow — YOU (Claude) play
it directly. Synthesize the provided data into ONE self-contained HTML document.
Output the HTML to a file; output nothing else around it (no markdown, no fences).

## Inputs you will have

1. **Fundamentals JSON** — from `fetch_screener.py` (overview ratios, pros/cons,
   quarterly results, P&L, balance sheet, cash flow, ratios, shareholding, peers,
   document links). This is the primary quantitative source (Screener.in — the
   source workflow mislabels it "FMP"; it is Screener scraping).
2. **News / qualitative** — from your WebSearch on shareholding pattern, promoter /
   FII / DII holdings, management, business model, recent developments.
3. **Index / market context** — optional: news + direction of the indices the stock
   belongs to (NIFTY 50, sector index). From WebSearch.

## Synthesis rules

- Use ONLY data provided/fetched. Never fabricate numbers. If a point is missing,
  write "Data unavailable" and continue. Always produce a complete document.
- **Target Price:** derive from the data — P/E mean reversion, EV/EBITDA, or SOTP.
  Show the method and the math.
- **Recommendation band:** BUY if upside > 15% | HOLD if -10% to +15% | SELL if
  downside > 10%.
- **Indian FY** runs Apr 1 → Mar 31. Label years FY20…FY24 correctly.
- State the date of the most recent data point in the header.
- Tone: objective, professional. No hype.
- Trend colors: green `#16a34a` positive, red `#dc2626` negative, orange `#d97706`
  neutral.

## HTML requirements

- Single complete document `<!DOCTYPE html> … </html>`. No markdown fences.
- All CSS inline or in one `<style>` block. Google Font **Inter**.
- Color scheme: dark navy header `#0f172a`, white body, accent `#2563eb`.
- `page-break-inside: avoid` on section blocks; `page-break-before` at major
  section boundaries (so the PDF paginates cleanly).
- Tables for all numeric data.

## Sections (in order)

1. **Header block** — Company name + Ticker + Exchange; Recommendation pill
   (BUY green / HOLD orange / SELL red); 4 KPI boxes: CMP | Target Price |
   Upside % | Investment Horizon; "Data as of" date.
2. **Company Overview** — 120–150 words.
3. **Quantitative Analysis** — subsections, each with a table:
   (a) Market Valuation (Mkt cap, P/E, P/B, div yield)
   (b) Profitability (ROCE, ROE, OPM trend)
   (c) Growth (sales & profit CAGR from P&L)
   (d) Balance Sheet (borrowings, reserves, D/E)
   (e) Cash Flow (operating / investing / financing / FCF)
   (f) Dividend
   (g) Efficiency (debtor days, cash conversion cycle)
   (h) Peer Comparison (from peers table)
4. **Qualitative Analysis** — Business Model, Management, Growth Strategy.
5. **Shareholding Pattern** — Promoter / FII / DII / Public quarterly table + trend
   commentary.
6. **Investment Thesis** — Key Drivers, Catalysts, Industry Positioning.
7. **Valuation & Recommendation** — derivation method, recommendation box, rationale
   bullets.
8. **Conclusion** — two paragraphs.
9. **Market Context** — index direction & news.
10. **Footer** — "For educational/informational purposes only. Not investment
    advice." + data sources + generated date.
