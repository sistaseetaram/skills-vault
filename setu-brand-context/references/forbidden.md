# Setu — Hard NO List

Mirrors `MyPersonalBrand/CLAUDE.md`. Anything here is non-negotiable.

## Color

- ❌ New hex values not in the 11-token locked table (`references/palette.md`)
- ❌ "Close to terracotta" / "slightly darker forest" — no derivations
- ❌ New accent colors of any kind — contrast comes from surface, not accents
- ❌ Extending the grandfathered exceptions list (it is CLOSED)
- ❌ Deriving tints with a new hex — use locked-fg + opacity instead

## Visual Effects

- ❌ Gradients — any direction, any palette, any opacity
- ❌ Glows, neon, drop-shadows beyond minimal UI affordance
- ❌ "AI-brain" motifs, circuit-board imagery, futuristic chrome
- ❌ Generic SaaS visual language (purple gradients, isometric illustrations, etc.)

## Typography

- ❌ New fonts beyond Cormorant Garamond / Inter / Noto Sans Devanagari
- ❌ Font substitutions "just for this one section"
- ❌ All-caps headings (10px label spec is the only uppercase use)

## Voice

- ❌ Hype words: revolutionary, game-changing, cutting-edge, next-gen
- ❌ Abstractions: transformation, synergy, paradigm, unlock
- ❌ Proof claims before they exist (no fake metrics, no unauthorised "trusted by")
- ❌ Selling tone — invitation, not pitch

## Process

- ❌ Long-lived feature branches — `main` only
- ❌ Editing locked LinkedIn assets without founder sign-off
- ❌ Moving founder photo back to `public/` (breaks Astro WebP pipeline)

## Pre-Edit Check

Before any CSS / copy / asset edit:
1. Diff for non-locked hex → fail-fast if found outside grandfathered list
2. Diff for new font-family declaration → fail
3. Diff for `linear-gradient` / `radial-gradient` / `box-shadow` (beyond minimal) → flag
4. Copy: scan for any DON'T word above → rewrite
