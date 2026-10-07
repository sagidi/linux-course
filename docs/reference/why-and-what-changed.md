[🏠 Home](../../README.md) · Reference

# Why it is built this way, and what changed

This page keeps every decision from the original planning chat and handbook, and lists what was fixed.

## The tool stack

| Task | Tool | Output |
|------|------|--------|
| Lesson content, narration, demo commands, quiz, lab | Master prompt v3 + any AI chat | `module.yaml` |
| Slides | ReportLab (Python) | `.pdf` + `.png` per slide |
| Terminal demos | VHS by Charm (in WSL) | `.mp4` clips, 1920×1080 |
| Voiceover | ElevenLabs API (final), Piper (free draft) | `.mp3` / `.wav` per scene |
| Video assembly + sync | FFmpeg | final `.mp4` |
| Captions | generated from the narration | `.srt` + `.vtt` |
| Course hosting | LearnWorlds or Thinkific | online course |
| Hands-on labs | Killercoda | browser terminal |
| Optional manual editing | CapCut Desktop / Descript | hand-edited `.mp4` |

## Why VHS by Charm for terminal demos

1. **Code-as-video:** a demo is a short text script. If a command changes, edit one line and re-record in a minute. No re-filming.
2. **Zero typos, steady pace:** commands are typed at a fixed speed (`150ms` per key) with fixed pauses (`5s`) so learners can read every output.
3. **Pixel-perfect:** rendered by a real browser engine, so the text is sharp with no compression smudges.

## Why the Catppuccin Macchiato terminal theme

1. **High contrast without eye strain:** a deep slate background (`#24273A`) instead of pure black, with soft pastel text.
2. **Professional look:** widely used by SRE/DevOps teams and modern terminals (Warp, Alacritty).
3. **Colours pop:** commands, IPs and output stand out clearly. (Alternative in `course.yaml`: `"Dracula"`.)

The **slides** use the light style of the approved Module 1.2 PDF (white page, navy text). The dark theme is
for the terminal.

## Why one complete module at a time

| Approach | Quality | Workflow | Verdict |
|----------|---------|----------|---------|
| **One module at a time, all its sub-topics** | 🟢 Best: slides, demos, voice and quiz stay in sync | Clean batch per module | **Recommended** |
| One sub-topic at a time | 🟡 Good, but slow | Constant context switching | Over-fragmented |
| All modules in one go | 🔴 AI drops details and code to fit | Long answers get cut | High risk of errors |

## Why one `module.yaml` per module (new)

Before, every module needed new Python code: the slide text lived inside `generate_slides.py`, and the narration
inside `generate_audio.py`. Now the AI writes **data** (one YAML file) and the same tested code builds every
module. You review one readable file instead of three programs, and a mistake cannot break the build code.

## What was fixed compared with the old handbook (v2)

| # | Old handbook | Problem | Now |
|---|--------------|---------|-----|
| 1 | FFmpeg merged the terminal clip with the whole narration (`-shortest`) | The ~30 s clip cut the ~4 min narration short, and **slides never appeared in the video** | Scene-by-scene assembly: every slide and clip is shown exactly while its narration plays |
| 2 | `.tape` file had no `Output` line | VHS writes no video file without it, so the build stopped at the FFmpeg step | Tapes are generated with `Output` always set |
| 3 | "Open PowerShell as Administrator" then `sudo apt ...` | `apt` commands do not work in PowerShell | PowerShell only installs WSL. Everything else runs in Ubuntu ([step 1](../01-install-wsl-ubuntu.md)) |
| 4 | `pip3 install reportlab requests` | Blocked on Ubuntu 24.04 (`externally-managed-environment`) | Private Python folder `.venv`, made by `./setup.sh` |
| 5 | Package list | `dig` (`dnsutils`) was missing. Library names differ between Ubuntu 22.04 and 24.04 | `./setup.sh` installs `dnsutils` and picks the right names |
| 6 | `apt install ttyd` | Ubuntu 22.04's ttyd is too old for VHS (needs 1.7.2+) | `./setup.sh` checks the version and downloads a newer one if needed |
| 7 | ElevenLabs model `eleven_monolingual_v1` | Deprecated by ElevenLabs | `eleven_multilingual_v2` (change in `course.yaml`) |
| 8 | "4K recording" | The tape was 1280×720 | Everything is 1920×1080 (1080p) |
| 9 | `start dns_v2_cache.mp4` | Does not work inside WSL | `explorer.exe <folder>` |
| 10 | Slides used basic PDF fonts | Arrows (`──>`) and emoji showed as empty boxes in the PDF | Real fonts (DejaVu/Liberation). Unsupported symbols are removed |
| 11 | Slides were US-letter size | Black bars in a 16:9 video | 16:9 slides that fill the frame |
| 12 | Prompt v2.2 had DNS details written into it | Had to be rewritten for every topic | Prompt v3 works for any topic. The module number and title are filled in automatically |
| 13 | Narration was a separate prompt | Narration and slides could drift apart | One prompt writes slides and narration together, scene by scene |
| 14 | Video editing in CapCut was a manual step | Slow, and timing was done by hand | Automatic. CapCut is optional ([manual method](manual-editing-capcut.md)) |
| 15 | Captions, instructor photo overlay | Manual in CapCut | Automatic (`.srt`/`.vtt`. Photo from `assets/instructor.png`) |
| 16 | 1-question quiz on the slide, "3-question quiz" in the LMS | Inconsistent | 3 questions in `module.yaml`. Question 1 is on the slide |
| 17 | Killercoda lab described in words only | You had to build the lab by hand | Lab files (steps, click-to-run commands, auto-check scripts) are generated |
| 18 | Every rebuild re-generated all audio | Paid for the same sentences again | Audio and recordings are cached per scene |
| 19 | No checks before building | AI mistakes only showed up as broken videos | `--check` catches them first, before spending credits |

## Module 1.2 notes

- The approved PDF is kept unchanged: `modules/module-1.2-dns-ttl-caching/Linux_DNS_and_TTL_Caching_Architecture.pdf`.
- `module.yaml` reproduces its slides word for word, in 16:9.
- **Voice:** the approved ElevenLabs script is used **word for word** (saved in `narration_approved.txt`;
  the build refuses to run if the narration differs). It is split across the slides it talks about; the quiz
  slide is not in the video (the quiz lives in the LMS) because the script has no quiz part.
- **Video = terminal + voice only.** Slides are the student PDF. Every part of the script plays over its own short
  terminal demo (marked `# NEW`); scenes 8-9 are the approved `dns_v2_cache.tape` commands.
- **Terminal demos:** the approved `dns_v2_cache.tape` commands, recorded at 1920×1080 (font 32) instead of
  1280×720 (font 22) so the video is full HD. Same look, sharper.
- Additions (slides/quiz only, never spoken), marked `# NEW`: the "Fix:" commands in the outage table (asked
  for by prompt v2.2) and two extra quiz questions.
- The approved slides use some technical names (`getaddrinfo()`, `glibc`, NSS). Prompt v3 allows precise
  terms **on slides** if they are explained, and keeps **narration** 100% plain English. If you want
  slides fully plain too, change rule 1 in [`prompts/module_prompt.md`](../../prompts/module_prompt.md).

[🏠 Home](../../README.md)
