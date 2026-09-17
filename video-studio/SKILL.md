---
name: video-studio
description: Executive orchestrator for the local video editing studio. Use for ANY video editing or motion-graphics task from ANY project — editing raw footage, removing filler words (umm/uh/false starts), cutting silences/dead air, cutting spoken mistakes (stutters, repeats, retakes), color grading, burning subtitles/captions, building animated overlays, title cards, lower thirds, transitions, kinetic captions, data-in-motion charts, TTS narration, narrative/visual storytelling passes, reels and YouTube Shorts, or full raw-footage-to-final.mp4 pipelines. Triggers on "edit this video", "remove filler words", "cut silences", "trim pauses", "remove dead air", "cut my mistakes", "fix stutters", "keep the best take", "add captions", "add motion graphics", "make a YouTube edit", "make a Short", "make a reel", "cut this Loom", "animate this", "turn this into a video". Routes to project-local video-use + HyperFrames + student-kit skills and orchestrates the full pipeline from the main thread.
---

# Video Studio — Executive Orchestrator

Thin global router. Owns NO editing logic itself. Knows the toolset, the paths, the pipeline, and orchestrates. All heavy skills live project-local and are READ on demand — zero global session cost until this skill fires.

## Why this exists

One global skill instead of 11. Loads the full toolset only when a video task actually appears. Runs in the **main thread** (not as a subagent) so it CAN spawn parallel subagents for animation rendering (video-use Hard Rule #10).

## Studio root (hardcoded — project-local skills do not auto-discover from other CWDs)

```
STUDIO=/Users/sistaseetaram/Desktop/Claude/claude_projects/VideoEditorHyperframes
```

- video-use repo + helpers: `$STUDIO/video-use/`  (helpers at `$STUDIO/video-use/helpers/`)
- video-use `.env` (ElevenLabs key): `$STUDIO/video-use/.env`  — never write keys to the footage dir
- HyperFrames skills: `$STUDIO/hyperframes/skills/<name>/`  ← **ours, a superset — keep using these for `hyperframes`**
- Student kit: `$STUDIO/student-kit/`  (sparse clone of `nateherkai/hyperframes-student-kit`, MIT)
  - **Canonical kit skills: `$STUDIO/student-kit/.claude/skills/<name>/SKILL.md`**
  - `$STUDIO/student-kit/.agents/skills/` is the generated Codex mirror — byte-identical except script
    paths rewritten to `.agents/…`. Never edit it; it regenerates via `npm run sync:skills`.
- Project-local skill symlinks: `$STUDIO/.claude/skills/`  (kit skills are **not** symlinked here — read them
  by absolute path per the rule below)

When orchestrating, **Read the relevant skill's SKILL.md by absolute path before acting on it.** Do not rely on auto-trigger from a foreign CWD.

## Tool catalog

### Cutting / grading / captions / concat → `video-use`
Read `$STUDIO/video-use/SKILL.md` first. Helpers (invoke as `python $STUDIO/video-use/helpers/<name>.py`, run via `uv run` from the video-use repo so the venv is active):
- **`transcribe_local.py <video|dir>` — DEFAULT transcriber.** mlx-whisper, Apple-Silicon native, free, offline, word-level, cached. No API key. Single-speaker (speaker_0); model `mlx-community/whisper-large-v3-turbo`. Outputs Scribe-compatible JSON so the rest of the pipeline is unchanged. Handles a single file or a whole directory (batch).
- `transcribe.py <video>` / `transcribe_batch.py <dir>` — **fallback only**: ElevenLabs Scribe (cloud, paid). Use ONLY when the job needs speaker diarization (multi-speaker) or audio-event tags `(laughter)/(applause)`. Needs `ELEVENLABS_API_KEY` in `$STUDIO/video-use/.env`. For multi-speaker WITHOUT paying, WhisperX is the local diarizing alternative.
- `pack_transcripts.py --edit-dir <dir>` — JSON → `takes_packed.md` (primary reading view).
- `timeline_view.py <video> <start> <end>` — filmstrip + waveform PNG at decision points.
- `grade.py <in> -o <out>` — ffmpeg color grade (presets or `--filter`).
- `render.py <edl.json> -o <out>` — per-segment extract → concat → overlays (PTS-shifted) → subtitles LAST. `--preview` for 720p, `--build-subtitles` for inline SRT.

### Talking-head cleanup / storytelling / short-form → `student-kit`

Read the chosen skill's SKILL.md by absolute path: `$STUDIO/student-kit/.claude/skills/<name>/SKILL.md`.

| Need | Kit skill |
|---|---|
| Full raw talking-head edit (umbrella — coordinates the rest) | `edit-video` |
| Silence / dead-air / pause removal | `cut-silences` |
| Stutters, repeats, false starts, retakes ("keep the best take") | `cut-mistakes` |
| Narrative arc, persistent world, visual callbacks (fixes an edit that "looks AI-made") | `video-storytelling` |
| Overlay beats, paper takeovers, glass lower-thirds, retention graphics | `hyperframes-video-beats` |
| Reels / YouTube Shorts / short ads | `short-form-edit` |
| Legacy May-Shorts example maintenance ONLY | `short-form-video` |
| New motion-graphics video from a brief (one-pass beginner interview) | `make-a-video` |
| Choose / extend motion-graphics card styles + templates | `style-library` |

**Zero-install scripts** — pure `node:` builtins + ffmpeg shell-out, no `npm install` needed (verified):

```bash
KIT=$STUDIO/student-kit

# Agent 1 — cut silences. Accepts our video-use transcripts directly (see note below).
node $KIT/.claude/skills/cut-silences/scripts/cut-silences.mjs <transcript.json> \
  [--video in.mp4] [--out-dir dir] [--gap 0.55] [--head-pad 0.22] [--tail-pad 0.34] [--apply]
# → <stem>.silence-edl.json · <stem>.silence-transcript.json (RE-TIMED) · <stem>.silence-decisions.md

# Agent 2 — find mistakes (review-gated). Feed it the RE-TIMED transcript + cut video from Agent 1.
node $KIT/.claude/skills/cut-mistakes/scripts/find-cut-candidates.mjs <transcript.json> [--out-dir dir]

# Agent 2b — apply only the cuts a human approved.
node $KIT/.claude/skills/cut-mistakes/scripts/apply-cuts.mjs <transcript.json> --cuts <approved.json> \
  [--video in.mp4] [--output out.mp4] [--out-dir dir] [--apply]
```

**Order is load-bearing:** silences first, then mistakes — using Agent 1's *edited video AND re-timed
transcript*. Never mix original timestamps with edited footage. Review every proposed mistake in context;
intentional repetition is not a mistake. If nothing needs cutting, pass an empty cuts list.

**Needs `npm install` (only these two):** `hyperframes/scripts/contrast-report.mjs` (`sharp`) and
`hyperframes/scripts/animation-map.mjs` (`@hyperframes/producer`). Everything above runs with zero installs.

Kit npm scripts (run from `$KIT`): `npm run preflight -- <project>` · `npm run validate-beats -- <project>`
· `npm run new-video -- <slug>` · `npm run catalog` · `npm run sync:skills` (regenerates the `.agents/` mirror).

`style-library`: 410 cards across 2 packs + a blueprint —
`$KIT/style-library/{01-vox-explainer,02-kallaway,_blueprint}/`, indexed by `style-library/registry.json`,
each style carrying a DESIGN.md, CSS tokens and named text slots. Guide: `$KIT/style-library/GUIDE.md`.

⚠️ **Version gap, unresolved:** our hyperframes fork is `0.6.61`; the kit pins `0.7.109` (devDep); npm
latest is `0.8.41`. Do not silently upgrade — breaking changes not yet evaluated.

### Motion graphics / overlays / title cards / captions-as-HTML → HyperFrames
Read `$STUDIO/hyperframes/skills/hyperframes/SKILL.md` for authoring. Engines + helpers:
- `hyperframes-cli` — `npx hyperframes init|lint|inspect|preview|render`. Lint+inspect BEFORE render.
- `hyperframes-media` — TTS (Kokoro), Whisper transcribe, background removal for transparent overlays.
- `hyperframes-registry` — install pre-built blocks: lower-thirds, caption styles, transitions, VFX. `npx hyperframes add`.
- `gsap` — primary motion engine (timelines, easing, stagger). Default for custom animation.
- `tailwind` — styling for compositions (`init --tailwind`, v4 browser runtime).
- `lottie` — embed After Effects JSON / .lottie exports.
- `css-animations` / `waapi` — lightweight native motion (gsap covers most; use when simpler).
- `website-to-hyperframes` — turn a web page into a video explainer.

Read each engine's SKILL.md by absolute path only when that engine is chosen.

## The pipeline (raw footage → final.mp4)

1. **Verify env** (cold start only): `ffmpeg`/`ffprobe` on PATH; deps synced; Node >=22 if HyperFrames slot needed. Local transcription needs NO API key. Only if falling back to Scribe (multi-speaker/audio-events): `grep -c ELEVENLABS_API_KEY $STUDIO/video-use/.env`; if missing, ask user to paste — write to `$STUDIO/video-use/.env`, never echo, never to footage dir.
2. **Inventory** — `ffprobe` sources; `uv run python helpers/transcribe_local.py <dir>` (DEFAULT, local mlx-whisper) — or Scribe fallback only if diarization/audio-events needed; `pack_transcripts.py`; sample 1-2 `timeline_view`s.
   **Transcription is ALWAYS ours, never the kit's.** `transcribe_local.py` emits
   `{"type":"word","text","start","end"}` — exactly the shape the kit's `cut-silences.mjs` accepts (it
   filters `type === "word"` and reads `w.text`), so its output feeds the kit cutters **directly, with no
   adapter**. Ignore the kit's `scripts/transcribe-elevenlabs.mjs` (ElevenLabs-only, paid, cloud).
3. **Pre-scan** — one pass over `takes_packed.md` for slips/mis-speaks.
4. **Converse** — describe material in plain English, ask material-shaped questions (type, length, aspect, brand/aesthetic, pacing, must-keep/must-cut, animation + grade prefs, caption style).
5. **Propose strategy** — 4-8 sentences. **WAIT for confirmation. Never cut before user approves the plain-English plan** (video-use Hard Rule #11).
6. **Execute** — build `edl.json` (spawn editor subagent for multi-take selection); grade per-segment; spawn **parallel** subagents for HyperFrames animations (one per animation, never sequential); compose via `render.py` with subtitles LAST.
   - For a **talking-head cleanup** pass, route through the kit instead of hand-rolling cuts:
     `cut-silences` → review → `cut-mistakes` (Agent 1's re-timed transcript + cut video as input).
   - **Feeding HyperFrames beat-sync (Gate 0):** once a video-use `edl.json` exists, generate a word-level
     transcript re-timed onto the **edited** timeline with
     `node $STUDIO/student-kit/scripts/video-use-to-hyperframes-transcript.mjs <edl.json>` — it reads
     `<edl_dir>/transcripts/<source>.json` for each EDL source and writes `<edl_dir>/transcript.json`.
     This is a **post-cut** adapter for `validate-beat-sync.mjs`; it is NOT the path from our transcriber
     into the cutters (that needs no adapter — see step 2). Anchored beats need `data-anchor` with an exact
     transcript phrase, entering 0.2s after and 1.8s before that word.
7. **Preview** — `render.py --preview`.
8. **Self-eval before showing user** — `timeline_view` on the RENDERED output at every cut boundary (±1.5s): check flash/jump, audio pop past 30ms fade, subtitle hidden behind overlay, overlay misalignment. Sample first/last 2s + midpoints. `ffprobe` duration vs EDL. Fix→re-render→re-eval, cap 3 passes.
9. **Iterate + persist** — natural-language feedback; never re-transcribe; final render on confirmation; append to `project.md`. All outputs in `<footage_dir>/edit/`.

## Hard rules (inherit from video-use — non-negotiable, silent-failure if broken)

1. Subtitles applied LAST in filter chain (after every overlay).
2. Per-segment extract → lossless `-c copy` concat (not single-pass filtergraph).
3. 30ms audio fades at every cut boundary.
4. Overlays use `setpts=PTS-STARTPTS+T/TB`.
5. Master SRT uses output-timeline offsets.
6. Never cut inside a word — snap to word boundary.
7. Pad cut edges 30-200ms.
8. Word-level verbatim ASR only (never SRT/phrase mode, never normalized fillers).
9. Cache transcripts per source — never re-transcribe unchanged source.
10. Parallel subagents for multiple animations — never sequential.
11. Strategy confirmation before execution.
12. All session outputs in `<footage_dir>/edit/` — never inside the studio repo.

## ContentGenerator handoff

YouTube/long-form scripts originate in the ContentGenerator project (`/Users/sistaseetaram/Desktop/Claude/claude_projects/ContentGenerator`). That pipeline drafts; THIS studio renders+edits. When a footage dir carries a ContentGenerator script/brief, read it for narrative intent before step 4. See `ContentGenerator/workflows/youtube-edit-handoff.md`.
