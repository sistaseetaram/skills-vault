---
name: brand-setup
description: "Brand Phase 0 — create project repository structure and initialize git for a new brand project"
argument-hint: "[brand-name]"
allowed-tools:
  - Bash
  - Write
  - AskUserQuestion
---

<objective>
Sets up a clean, organized repository for a brand project before any creative work begins.

Creates the canonical directory structure, initializes git, and writes a README that tracks
phase progress and locked decisions throughout the project.

Invoked by: brand-identity-process (Phase 0)
Followed by: brand-foundation (Phase 1)
</objective>

<process>

## 1. Confirm brand name

If $ARGUMENTS contains a name, use it as the slug (lowercase, hyphenated, e.g. "setu").
Otherwise, ask:
  "What is the brand name? (used to name the project folder)"

Derive slug: lowercase, spaces → hyphens, strip special characters.
REPO = "<slug>-brand"

## 2. Create repository structure

```bash
mkdir -p <REPO>/01-foundation
mkdir -p <REPO>/02-visual-identity
mkdir -p <REPO>/03-collateral/website
mkdir -p <REPO>/03-collateral/linkedin
mkdir -p <REPO>/03-collateral/pitch-deck
mkdir -p <REPO>/03-collateral/assets
```

## 3. Write README.md

Write `<REPO>/README.md` with:

```markdown
# <Brand Name> — Brand Project

## Current Phase
Phase 0 complete — repository initialized

## Locked Decisions
### Foundation
(empty — run /brand-identity-process foundation)

### Visual Identity
(empty — run /brand-identity-process visual-identity)

### Collateral
(empty — run /brand-identity-process collateral)

## Structure
01-foundation/     — brand brief (name, audience, values, tone)
02-visual-identity/ — wordmark, palette, typography, guidelines
03-collateral/     — website, linkedin, pitch-deck, assets
```

## 4. Initialize git and commit

```bash
cd <REPO>
git init
git add README.md
git commit -m "Initialize <Brand Name> brand project"
```

## 5. Confirm and hand off

Print:
  "Repository created at ./<REPO>/ and initialized with git.
   Run /brand-identity-process foundation to begin Phase 1."

</process>
