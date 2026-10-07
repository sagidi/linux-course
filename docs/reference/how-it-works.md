[🏠 Home](../../README.md) · Reference

# How it works

You do not need this page to make a course. Read it when you are curious, or when something
behaves in a way you do not expect.

## The big idea: one file per module

Everything about a module lives in **one file**: `modules/<module>/module.yaml`.
The AI writes it, you review it, and `./build.sh` turns it into every course asset.
To change anything, edit that file and rebuild. Never edit the generated files.

```
                              module.yaml
                                   │
     ┌──────────────┬──────────────┼───────────────┬──────────────┐
     ▼              ▼              ▼               ▼              ▼
  slides         demos          narration        quiz           lab
     │              │              │               │              │
  ReportLab      VHS (.tape)    ElevenLabs /      Quiz.md       Killercoda
  PDF + PNG      → .mp4 clips   Piper → audio                   folder
     └──────────────┴──────┬───────┘
                           ▼
                FFmpeg: one segment per scene, joined in order
                           ▼
              Module_X_Y_Final.mp4  +  Captions.srt/.vtt
```

## Scenes: how sync works without editing

A module is a list of **scenes** (12 by default). Each scene has:

- a **picture**: a slide, or a terminal demo (`demo:`), or both (the slide goes in the PDF, the demo in the video);
- its **narration**: the words spoken while that picture is on screen.

The build measures each scene's narration and shows the picture for **exactly that long** (plus a short
pause, `video.scene_gap`). For a terminal demo, the recording plays while the voice talks: if the voice is
longer, the last frame is held; if the recording is longer, the voice is followed by silence.
The scenes are then joined. That is why the slides, terminal and voice always line up, with no timeline
editing. It does automatically what you would otherwise do by hand in CapCut ([manual method](manual-editing-capcut.md)).

## What `./build.sh` does, stage by stage

| Stage | What happens | Code |
|-------|--------------|------|
| 1. Check | Checks `module.yaml`: required fields, text lengths, unsafe or freezing demo commands, quiz answers | `engine/validate.py` |
| 2. Slides | Draws each slide (16:9, same look as the approved Module 1.2 PDF), checks the text fits, saves the PDF and one 1920×1080 PNG per slide | `engine/slides.py` |
| 3. Demos | Writes a `.tape` file per demo with the standard look from `course.yaml`, and VHS records it | `engine/tapes.py` |
| 4. Voice | One audio file per scene: ElevenLabs (final) or Piper/espeak (draft). Uses the previous/next scene text so the voice flows naturally | `engine/voice.py` |
| 5. Video | Turns each scene into a video segment of the right length, adds your photo if present, joins them, writes captions | `engine/video.py` |
| 6. Extras | Quiz file, narration script, Killercoda lab folder, `README.txt` | `engine/extras.py` |

## Caching: why rebuilds are fast and cheap

- **Terminal recordings** are reused unless the demo's commands or the terminal settings changed.
- **Audio** is reused per scene unless that scene's text or the voice settings changed.
  This is why changing one sentence costs only that scene's ElevenLabs credits.
- Slides and the final video are always rebuilt (that takes seconds).

To force everything to be redone, delete the module's `build` folder:
`rm -r modules/module-1.3-*/build` (it is safe: it only contains generated files).

## Where things are

| Path | What | Saved to GitHub? |
|------|------|:---:|
| `modules/<m>/module.yaml` | The module's content (source of truth) | ✅ |
| `modules/<m>/prompt.md` | The exact prompt sent to the AI (for your records) | ✅ |
| `modules/<m>/build/work/` | Intermediate files: slide PNGs, `.tape` files, clips, audio, segments | ❌ |
| `modules/<m>/build/publish/` | Finished files to upload | ❌ |
| `course.yaml` | Settings shared by all modules | ✅ |
| `.env` | Your secret API key | ❌ never |

## Draft vs final

| | `--draft` | final (no flag) |
|-|-----------|-----------------|
| Voice | Piper (free, offline). espeak-ng if Piper is missing | `voice.provider` in `course.yaml` (ElevenLabs) |
| Video file | `Module_X_Y_DRAFT.mp4` | `Module_X_Y_Final.mp4` |
| Cost | Free | ElevenLabs credits for new/changed scenes |

[🏠 Home](../../README.md)
