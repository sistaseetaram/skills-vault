#!/usr/bin/env python3
"""
render_pdf.py — convert a self-contained HTML report to PDF.

Replaces the n8n PDFBolt node. No API key. Tries, in order:
  1. headless Chrome / Chromium (best fidelity for the styled report)
  2. playwright (if installed)
  3. wkhtmltopdf
If none available, prints guidance and exits non-zero (HTML is still usable).

Usage:
    python3 render_pdf.py report.html              # -> report.pdf
    python3 render_pdf.py report.html out.pdf
"""
import sys, os, shutil, subprocess, pathlib

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome"), shutil.which("chromium"),
    shutil.which("chromium-browser"), shutil.which("chrome"),
]


def via_chrome(src, dst):
    binp = next((c for c in CHROME_CANDIDATES if c and os.path.exists(c)), None)
    if not binp:
        return False
    uri = pathlib.Path(src).resolve().as_uri()
    cmd = [binp, "--headless", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", f"--print-to-pdf={dst}", uri]
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    return os.path.exists(dst) and os.path.getsize(dst) > 0


def via_playwright(src, dst):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    uri = pathlib.Path(src).resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(uri, wait_until="networkidle")
        pg.pdf(path=dst, format="A4", print_background=True)
        b.close()
    return os.path.exists(dst)


def via_wkhtmltopdf(src, dst):
    if not shutil.which("wkhtmltopdf"):
        return False
    subprocess.run(["wkhtmltopdf", "--enable-local-file-access", src, dst],
                   capture_output=True, timeout=120)
    return os.path.exists(dst)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: render_pdf.py report.html [out.pdf]")
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".pdf"
    for fn in (via_chrome, via_playwright, via_wkhtmltopdf):
        try:
            if fn(src, dst):
                print(f"PDF written: {dst}")
                return
        except Exception as e:
            print(f"{fn.__name__} failed: {e}", file=sys.stderr)
    sys.exit("No PDF engine available. Install Chrome, or `pip install playwright "
             "&& playwright install chromium`. The HTML report is still valid — "
             "open it in a browser and Print > Save as PDF.")


if __name__ == "__main__":
    main()
