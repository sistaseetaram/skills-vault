---
name: video-studio
description: Executive orchestrator for the local video editing studio. Use for ANY video editing or motion-graphics task from ANY project — editing raw footage, removing filler words (umm/uh/false starts), cutting dead space, color grading, burning subtitles/captions, building animated overlays, title cards, lower thirds, transitions, kinetic captions, data-in-motion charts, TTS narration, or full raw-footage-to-final.mp4 pipelines. Triggers on "edit this video", "remove filler words", "add captions", "add motion graphics", "make a YouTube edit", "cut this Loom", "animate this", "turn this into a video". Routes to project-local video-use + HyperFrames skills and orchestrates the full pipeline from the main thread.
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
- HyperFrames skills: `$STUDIO/hyperframes/skills/<name>/`
- Project-local skill symlinks: `$STUDIO/.claude/skills/`

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
3. **Pre-scan** — one pass over `takes_packed.md` for slips/mis-speaks.
4. **Converse** — describe material in plain English, ask material-shaped questions (type, length, aspect, brand/aesthetic, pacing, must-keep/must-cut, animation + grade prefs, caption style).
5. **Propose strategy** — 4-8 sentences. **WAIT for confirmation. Never cut before user approves the plain-English plan** (video-use Hard Rule #11).
6. **Execute** — build `edl.json` (spawn editor subagent for multi-take selection); grade per-segment; spawn **parallel** subagents for HyperFrames animations (one per animation, never sequential); compose via `render.py` with subtitles LAST.
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
