# CLAUDE.md - how to work in this repository

> **Read this first.** The real, current course is NOT built from this repo. It lives on the owner's computer at
> `~/Courses/Linux-networking-course` (GitHub: `agidilogic/linux-networking-course`, a different account) and is
> published on Thinkific with labs at https://labs.agidilogic.com. Its own `CLAUDE.md`, `COURSE_OUTLINE.md` and
> `linux_course_prompt_template_v2_5.md` describe every step. Connect to the owner's device (folder access, or a
> Remote Control session for builds, deploys and Thinkific) and follow those files. This repo is an older
> module.yaml/Killercoda setup kept for reference.

This repo builds a Linux/SRE video course. Each module is ONE file, `modules/module-X.Y-<slug>/module.yaml`;
`./build.sh` turns it into slides, VHS terminal demos, voiceover, a synced video, captions, quiz and a Killercoda lab.
The owner is new to this. Keep answers short and give copy-paste commands.

## Commands
- `./setup.sh`: one-time install + self-test (Ubuntu/WSL)
- `./new-module.sh X.Y`: creates the module folder and `prompt.md` (title from `course.yaml` → `outline`)
- `./paste-module.sh X.Y [--file f]`: saves an AI answer as `module.yaml` and validates it
- `./build.sh X.Y --check | --slides | --draft` and `./build.sh X.Y` (final, ElevenLabs)

## Writing or editing a module
- Follow `prompts/module_prompt.md` exactly (12 scenes, size limits, plain-English narration, safe demo commands).
- Use `modules/module-1.2-dns-ttl-caching/module.yaml` as the style reference. Its slide text is approved: do not change it unless asked.
- Always finish with `./build.sh X.Y --check` (fast) and `--slides` to confirm the slides fit.
- Never put API keys in files other than `.env` (gitignored). Never commit `build/` output.

## Code
- `engine/`: Python. `build.py` orchestrates: `validate.py` → `slides.py` → `tapes.py` → `voice.py` → `video.py` → `extras.py`.
- Shared settings live in `course.yaml`. Secrets in `.env`.
- Docs are numbered steps in `docs/` (00-09) with prev/next links. Keep them in sync when behaviour changes.
