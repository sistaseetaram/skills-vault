#!/usr/bin/env python3
"""
fetch_screener.py — deterministic Screener.in scraper.

Collapses the n8n parent's [HTTP Request -> Markdown -> AI Agent1 financial
parser] chain into one stdlib-only script. No API key, no LLM, no deps.

Fetches a company's Screener.in page and emits clean structured JSON:
overview ratios, pros/cons, and every financial table (quarters, P&L,
balance sheet, cash flow, ratios, shareholding) plus document links.

Usage:
    python3 fetch_screener.py NTPC                 # consolidated (default)
    python3 fetch_screener.py NTPC --standalone    # standalone view
    python3 fetch_screener.py TCS --out tcs.json   # write to file

Symbol = the Screener.in slug (usually the NSE/BSE ticker, e.g. NTPC, TCS,
RELIANCE, INFY). Exchange is NOT part of the URL on Screener.
"""
import sys, json, re, html, argparse, urllib.request, urllib.error

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(symbol, consolidated=True):
    base = f"https://www.screener.in/company/{symbol}/"
    url = base + ("consolidated/" if consolidated else "")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        # consolidated may not exist -> fall back to standalone
        if consolidated and e.code in (404, 302):
            return fetch(symbol, consolidated=False)
        raise
    return url, raw


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parse_table(tbl):
    """Return {'headers':[...], 'rows':[[...]]} for one <table> blob."""
    head = []
    mh = re.search(r"<thead.*?</thead>", tbl, re.S)
    if mh:
        head = [clean(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", mh.group(0), re.S)]
    body = re.search(r"<tbody.*?</tbody>", tbl, re.S)
    rows = []
    src = body.group(0) if body else tbl
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", src, re.S):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)
        row = [clean(c) for c in cells]
        if any(row):
            rows.append(row)
    return {"headers": head, "rows": rows}


def section_table(htmltext, section_id):
    m = re.search(rf'id="{section_id}".*?(<table.*?</table>)', htmltext, re.S)
    return parse_table(m.group(1)) if m else None


def parse(url, h):
    out = {"source_url": url}

    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    out["company"] = clean(m.group(1)) if m else None

    # top ratios -> overview dict
    overview = {}
    mt = re.search(r'id="top-ratios".*?</ul>', h, re.S)
    if mt:
        for li in re.findall(r"<li[^>]*>(.*?)</li>", mt.group(0), re.S):
            t = clean(li)
            # split "Label value" on first run of digits/₹
            mm = re.match(r"(.+?)\s+(₹.*|[\d][\d,.\-/%].*)$", t)
            if mm:
                overview[mm.group(1).strip()] = mm.group(2).strip()
    out["overview"] = overview

    # pros / cons
    def bullets(klass):
        mb = re.search(rf'class="{klass}".*?<ul[^>]*>(.*?)</ul>', h, re.S)
        return [clean(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", mb.group(1), re.S)] if mb else []
    out["pros"] = bullets("pros")
    out["cons"] = bullets("cons")

    # financial sections
    for key, sid in [("quarterly_results", "quarters"),
                     ("profit_and_loss", "profit-loss"),
                     ("balance_sheet", "balance-sheet"),
                     ("cash_flow", "cash-flow"),
                     ("ratios", "ratios"),
                     ("shareholding", "shareholding"),
                     ("peers", "peers")]:
        t = section_table(h, sid)
        if t:
            out[key] = t

    # document / external links
    links = []
    md = re.search(r'id="documents".*?</section>', h, re.S)
    if md:
        for href, txt in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', md.group(0), re.S):
            label = clean(txt)
            if label and href.startswith("http"):
                links.append({"label": label, "url": href})
    out["document_links"] = links[:40]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("--standalone", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    url, raw = fetch(a.symbol.upper(), consolidated=not a.standalone)
    data = parse(url, raw)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"wrote {a.out}  ({len(text)} bytes, company={data.get('company')})")
    else:
        print(text)


if __name__ == "__main__":
    main()
