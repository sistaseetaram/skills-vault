---
name: brand-collateral
description: "Brand Phase 3 — produce brand collateral: website wireframe, LinkedIn strategy, pitch deck, or print/digital assets"
allowed-tools:
  - Read
  - Write
  - Bash
  - Agent
  - AskUserQuestion
---

<objective>
Produces one or more brand collateral deliverables using the locked visual identity as the source of truth.

Always reads the brand brief and brand guidelines before starting any deliverable.
Applies the tool selection rule without asking:
  - Website wireframe, LinkedIn templates, social post designs → HTML
  - Pitch deck, strategy document → Gamma
  - Business card, email signature, print/export-ready assets → Canva

Invoked by: brand-identity-process (Phase 3)
</objective>

<process>

## 0. Load context

Find repo: `ls -d *-brand/ 2>/dev/null | head -1` → REPO
If not found: stop and say "Run /brand-identity-process setup first."

Read both:
- `<REPO>/01-foundation/brand-brief.md`
- `<REPO>/02-visual-identity/brand-guidelines.html` (skim for palette and type pair)

## 1. Select collateral type(s)

Ask (single AskUserQuestion call, multi-select):
"Which collateral would you like to produce?"
Options:
  a) Website — copy framework + page structure + HTML wireframe mockup
  b) LinkedIn — profile optimization + content strategy + post templates
  c) Pitch deck — outline + Gamma presentation
  d) Print/digital assets — business card, email signature, social post templates (Canva)

## 2. Route to the right output for each selection

### Website
- Produce a page-by-page copy outline (Home, About, Services, Contact) grounded in the brand brief
- Write each page's structure as an HTML wireframe mockup with placeholder copy
- Save each page as `<REPO>/03-collateral/website/<page>.html`
- Render and show before reporting done

### LinkedIn
- Write optimized headline, about section, and featured section copy
- Produce a 30-day content calendar (themes, not full posts)
- Generate 3 sample post templates as HTML cards styled in brand colors and type
- Save to `<REPO>/03-collateral/linkedin/`

### Pitch Deck
- Produce a structured outline (10–12 slides: problem, solution, audience, differentiators, proof, ask)
- Generate via Gamma (multi-page structured narrative — Gamma is the right tool here)
- Save the Gamma link / exported file to `<REPO>/03-collateral/pitch-deck/`

### Print/Digital Assets
- Produce via Canva (export-ready production files)
- Assets: business card (front + back), email signature (HTML + image), social post template (1:1 and 16:9)
- Save exported files to `<REPO>/03-collateral/assets/`
- After showing HTML previews, ask: "Want me to push these to Canva for export?"

## 3. Commit each deliverable as it's completed

```bash
cd <REPO>
git add 03-collateral/
git commit -m "Add Phase 3 collateral — <type>"
```

Update `<REPO>/README.md` Collateral section with a one-line summary of what was produced.

## 4. Hand off

After all selected collateral is done:
Print a summary of what was created and where the files live in the repo.

</process>
