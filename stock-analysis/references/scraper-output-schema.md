# `fetch_screener.py` output schema

JSON object (UTF-8). Tables are emitted as `{headers:[...], rows:[[...]]}` exactly
as they appear on Screener.in — first header cell is usually empty (row-label
column). Map them yourself; do not assume fixed column counts (years vary by stock).

```jsonc
{
  "source_url": "https://www.screener.in/company/NTPC/consolidated/",
  "company": "NTPC Ltd",
  "overview": {                 // top ratio strip — string values with ₹ / %
    "Market Cap": "₹ 3,54,704 Cr.",
    "Current Price": "₹ 366",
    "High / Low": "₹ 414 / 316",
    "Stock P/E": "13.1",
    "Book Value": "₹ 210",
    "Dividend Yield": "2.28 %",
    "ROCE": "8.33 %",
    "ROE": "14.0 %",
    "Face Value": "₹ 10.0"
  },
  "pros": ["..."],              // Screener's auto pros
  "cons": ["..."],              // Screener's auto cons
  "quarterly_results": {"headers": ["", "Mar 2023", ...], "rows": [["Sales", "..."], ...]},
  "profit_and_loss":   {"headers": ["", "Mar 2015", ...], "rows": [...]},   // annual
  "balance_sheet":     {"headers": [...], "rows": [...]},
  "cash_flow":         {"headers": [...], "rows": [...]},
  "ratios":            {"headers": [...], "rows": [...]},  // debtor days, CCC, ROCE%
  "shareholding":      {"headers": ["", "Jun 2023", ...], "rows": [["Promoters", "..."], ...]},
  "peers":             {"headers": [...], "rows": [...]},
  "document_links":    [{"label": "Annual Report 2024", "url": "https://..."}, ...]
}
```

## Notes / gotchas

- **Symbol = Screener slug**, normally the NSE/BSE ticker (NTPC, TCS, RELIANCE,
  INFY). No exchange in the URL.
- Script auto-falls back consolidated → standalone on 404.
- P&L / balance sheet show ~10–12 fiscal years; quarterly shows ~12 quarters.
  Use the most recent columns for current figures, earliest→latest for CAGR.
- `shareholding` rows = Promoters / FIIs / DIIs / Government / Public + No. of
  shareholders. Use for the shareholding-pattern section.
- All numbers are strings with Indian formatting (commas as `3,54,704`). Strip
  `₹`, `,`, `%`, `Cr.` before any arithmetic.
