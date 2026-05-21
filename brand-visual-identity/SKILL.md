---
name: brand-visual-identity
description: "Brand Phase 2 — design wordmark, color palette, typography, brand guidelines HTML page, and exported PNG image"
allowed-tools:
  - Read
  - Write
  - Bash
  - Agent
---

<objective>
Produces all visual identity artifacts through iterative HTML rendering with user feedback at each step.

Visual-first rule: always render HTML and show it before reporting anything as done.
Never deliver a text spec as the primary output — the rendered visual IS the output.

Steps: Wordmark → Color Palette → Typography → Brand Guidelines HTML → Brand Guidelines PNG

Tool selection rule (apply without asking):
  - Wordmark, swatches, type specimens, guidelines page → HTML rendered via browser/Puppeteer
  - Multi-page strategy document → Gamma
  - Export-ready production files (cards, social posts, print) → Canva (offer AFTER HTML shown)

Invoked by: brand-identity-process (Phase 2)
Followed by: brand-collateral (Phase 3)
</objective>

<process>

## 0. Load context

Find repo: `ls -d *-brand/ 2>/dev/null | head -1` → REPO
If not found: stop and say "Run /brand-identity-process setup first."

Read `<REPO>/01-foundation/brand-brief.md` — extract name, values, tone, and visual direction.
This brief informs every design decision below.

## Step 2a — Wordmark

Generate 2–3 distinct direction options as self-contained HTML files.
Each option must differ meaningfully in concept (e.g., typographic only, symbolic + text, script-based).
Render all options in a single HTML page for side-by-side comparison.

Show light AND dark background variations for each option.
Do NOT describe the options in text — render them and present the visual.

Wait for user feedback. Iterate until one direction is locked.
Save locked wordmark as `<REPO>/02-visual-identity/wordmark.html` (both variations in one file).

## Step 2b — Color Palette

Generate a color exploration HTML page: render swatches in context (not just hex squares).
Show each color applied to backgrounds, text, and accent uses so the mood is clear.
Include labels: Primary, Secondary, Accent, Neutral, Dark, etc.

Iterate until palette is locked.
Save as `<REPO>/02-visual-identity/color-palette.html`.

## Step 2c — Typography

Generate 2 type pairing options as HTML specimens.
Each specimen must show: heading (H1, H2), body paragraph, caption/small text — set in that font pair.
Use real brand-relevant copy (not Lorem Ipsum) drawn from the brand brief.

Iterate until pair is locked.
Save as `<REPO>/02-visual-identity/typography.html`.

## Step 2d — Brand Guidelines Page

Combine all locked decisions (wordmark, palette, typography, usage rules) into a single comprehensive HTML page.
Sections: Logo & Wordmark, Color System, Typography System, Usage Do's and Don'ts.
This is the reference document for all future design work on this brand.

Save as `<REPO>/02-visual-identity/brand-guidelines.html`.

## Step 2e — Brand Guidelines Image (PNG export)

Export the guidelines HTML page to a full-page PNG using Chrome headless / Puppeteer:

```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  const path = require('path');
  const file = path.resolve('<REPO>/02-visual-identity/brand-guidelines.html');
  await page.goto('file://' + file);
  await page.waitForTimeout(500);
  await page.screenshot({ path: '<REPO>/02-visual-identity/brand-guidelines.png', fullPage: true });
  await browser.close();
  console.log('Exported.');
})();
"
```

If Puppeteer is not available, try Chrome headless:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu \
  --screenshot=<REPO>/02-visual-identity/brand-guidelines.png \
  --window-size=1440,900 \
  "file://$(pwd)/<REPO>/02-visual-identity/brand-guidelines.html"
```

Confirm the PNG was created: `ls -lh <REPO>/02-visual-identity/brand-guidelines.png`

## Step 2f — Commit locked visual identity

Update `<REPO>/README.md` — fill in the Visual Identity section with: wordmark description, primary colors (hex), and font pair.

```bash
cd <REPO>
git add 02-visual-identity/ README.md
git commit -m "Lock Phase 2 — wordmark, palette, typography, brand guidelines"
```

## Step 2g — Hand off

Print:
  "Visual identity locked and committed.
   Artifacts in <REPO>/02-visual-identity/ — including brand-guidelines.png for sharing.
   Run /brand-identity-process collateral to begin Phase 3."

</process>
