---
name: stock-analysis
description: >
  Generate a full equity-research report (HTML + optional PDF) for a listed stock
  from a plain-English query. Scrapes Screener.in fundamentals deterministically,
  pulls shareholding/qualitative news + index context via web search, then
  synthesizes a 10-section analyst report with target price and BUY/HOLD/SELL
  call. Indian-market aware (NSE/BSE, Indian FY). Use when the user asks to
  "analyze <stock>", "research <ticker>", "is <stock> a buy", "fundamental
  analysis of <company>", "stock report", "equity research on <symbol>", or
  pastes a stock symbol/company wanting investment analysis. Input here, output
  here — no Telegram, no n8n.
---

# Stock Analysis

Standalone rebuild of an n8n "Stock_Analysis_parent" workflow (50 nodes →
Claude + 2 scripts). The LLM agents in the original (Market Router, financial
parser, Architect synthesizer) are **you** — run them inline. Screener scraping
and PDF rendering are deterministic scripts. News is WebSearch. No API keys,
no external services beyond web fetch/search.

**Base dir:** `~/.claude/skills/stock-analysis`

## Pipeline

### 1. Route the query (Market Router)
From the user's query identify: **SYMBOL** (Screener slug — usually the NSE/BSE
ticker), **EXCHANGE** (default NSE for Indian stocks), **ACTION**, **DAY**.

- If the symbol is **missing or ambiguous** → ask the user to clarify. Stop.
- Determine market status vs `now` in the exchange's timezone (NSE/BSE: Asia/
  Kolkata, 09:15–15:30 IST, Mon–Fri, minus holidays):
  - **FETCH** — market open (intraday).
  - **VERIFY** — market closed (after-hours / weekend / holiday). Same report;
    note in the header that figures are from the last close.
- Map symbol → Screener slug. Indian names: NTPC, TCS, RELIANCE, INFY, HDFCBANK…
  US/other: use the Screener slug if listed, else say Screener covers Indian
  equities and offer to proceed with web-search-only fundamentals.

### 2. Cache check (optional, replaces Supabase T3/T4/T5)
Reports cache to `~/.claude/skills/stock-analysis/.cache/<SYMBOL>_<YYYY-MM-DD>.html`.
Freshness rule from the source workflow:
- Market **open**: reuse if cached < 60 min ago.
- Market **closed**: reuse any same-day cache written after 15:30 IST.
- Holiday/weekend: reuse any same-day cache.
On hit → skip to step 6 with the cached HTML.

### 3. Fetch fundamentals (deterministic)
```bash
python3 ~/.claude/skills/stock-analysis/scripts/fetch_screener.py <SYMBOL> --out /tmp/<SYMBOL>.json
```
Returns overview ratios, pros/cons, quarterly/P&L/balance-sheet/cash-flow/ratios/
shareholding/peers tables, document links. Schema:
`references/scraper-output-schema.md`. This single script replaces the original's
HTTP→Markdown→financial-parser-LLM chain.

### 4. News + qualitative + index context (WebSearch)
Run 2–3 web searches (no Tavily key needed):
- `"<COMPANY> <SYMBOL>" shareholding pattern promoter FII DII quarterly latest`
- `"<COMPANY>" management business model growth strategy recent results`
- `<INDEX e.g. NIFTY 50 / sector index> news performance this week` (index context)
Extract shareholding trend, recent developments, analyst sentiment, index direction.

### 5. Synthesize the report (Architect)
Read `references/architect-report-spec.md` and produce ONE self-contained HTML
document (10 sections, Inter font, navy/accent theme, target price, BUY/HOLD/SELL).
Write it to `/tmp/<SYMBOL>_report.html` (and cache it per step 2).

### 6. Deliver
- Always: give the user the HTML file path + an on-screen executive summary
  (recommendation, CMP, target, upside, 3–4 key points).
- PDF (offer or on request):
  ```bash
  python3 ~/.claude/skills/stock-analysis/scripts/render_pdf.py /tmp/<SYMBOL>_report.html
  ```
  Uses headless Chrome → playwright → wkhtmltopdf, whichever is present. If none,
  the HTML opens in any browser and prints to PDF.

## Notes
- The source workflow labeled fundamentals "FMP" — it is actually Screener.in
  scraping. `fyersSymbol` (`NSE:SYM-EQ`) existed but was unused; dropped.
- Never fabricate numbers. Missing data → "Data unavailable". Always end the
  report with the not-investment-advice disclaimer.
- Strip `₹ , % Cr.` before any math on Screener strings (Indian number format).

## Field notes (verified 2026-08-14, BOSCHLTD + SOLARINDS)

**Scope boundary — this skill does NOT do price prediction.** It is a
fundamentals/valuation report generator. Requests for *intraday range*, *today's
price band*, *volatility forecast*, or *"predict the price"* need a separate
quant path (below); do not try to answer them from Screener data.

**Free OHLCV for NSE without any API key** — Yahoo chart API works and is
survey-verified against Trendlyne/Value Research:
`https://query1.finance.yahoo.com/v8/finance/chart/<SYM>.NS?range=5y&interval=1d`
(send a browser `User-Agent` or it 403s). Gotchas found in the wild:
- `interval=15m` with `range=3mo` → **HTTP 422**. 15m/30m cap at 60d; 5m caps at 1mo.
- `meta.chartPreviousClose` is the close *before the requested range starts*, NOT
  yesterday's close. Do not use it as prev-close.
- Daily bars can lag the latest session by a day on thin counters (Bosch). Rebuild
  the missing session by aggregating the 5m series — verified accurate to ₹10
  (0.02%) on a ₹46,750 stock. Low-liquidity names may have no 5m prints after
  ~15:10 even though NSE closes 15:30.
- Indices: `^NSEI` (Nifty 50), `^CNXAUTO`. Index *daily* series can go stale for
  weeks while the 5m series stays fresh — check before using.

**macOS: `timeout` is not installed.** `timeout 180 python3 …` fails with
`command not found`. Use the Bash tool's own `timeout` parameter instead.

**If asked for an intraday band, the calibrated recipe that worked:**
filtered historical simulation — forecast σ, standardise `U=H/C₋₁−1` and
`D=L/C₋₁−1` by it (this puts overnight gap risk *inside* the target), then take
empirical quantiles of the standardised series. Model rule
`σ = MAX(median-ensemble, GARCH(1,1))`. Critically: **test conditional coverage,
not just average coverage** — the plain ensemble hit 79-80% on all days but only
71.6% on post-shock days, i.e. it silently under-covers exactly when it matters.
Always report the realised hit-rate for the state the stock is in *today*, with a
binomial standard error. Never tune the band to hit a target number.
