# Linux Course Builder

Turn **one prompt** into a **finished video lesson**: slides, live terminal demos,
voiceover, captions, quiz and a hands-on lab, with almost no manual work.

```
 ┌──────────────┐   ┌──────────────┐   ┌─────────────────────────────────────────┐   ┌─────────────┐
 │ 1. PROMPT    │──>│ 2. AI ANSWER │──>│ 3. ./build.sh  (automatic)              │──>│ 4. PUBLISH  │
 │ new-module.sh│   │ module.yaml  │   │ slides + terminal video + voice + sync  │   │ LMS + lab   │
 └──────────────┘   └──────────────┘   └─────────────────────────────────────────┘   └─────────────┘
       you             you review                    computer does it                    you upload
```

---

## Start here: follow the steps in order

Each page ends with a **Next ➡** link, so you can click through from start to finish.

### Part A: one-time setup (do once, about 1 hour)

| Step | Page | What you do |
|:---:|------|-------------|
| 0 | [Tools to install](docs/00-tools-to-install.md) | See the full list of tools and accounts (what, why, cost) |
| 1 | [Install WSL + Ubuntu](docs/01-install-wsl-ubuntu.md) | Get Linux running on your Windows PC |
| 2 | [Install the tools](docs/02-install-the-tools.md) | Download this project, run `./setup.sh` |
| 3 | [Create accounts & keys](docs/03-create-accounts-and-keys.md) | ElevenLabs key, (later) GitHub secret, Killercoda, LMS |
| 4 | [First test build](docs/04-first-test-build.md) | Build Module 1.2 to prove everything works |

### Part B: for every module (repeat, about 1-2 hours each)

| Step | Page | What you do |
|:---:|------|-------------|
| 5 | [Create a module with AI](docs/05-create-a-module-with-ai.md) | `./new-module.sh` → paste into AI → `./paste-module.sh` |
| 6 | [Review the module](docs/06-review-the-module.md) | Check facts, slides and the free draft video |
| 7 | [Build the final video](docs/07-build-the-final-video.md) | `./build.sh 1.3` with your ElevenLabs voice |
| 8 | [Publish the module](docs/08-publish-the-module.md) | Upload to your LMS, publish the lab |
| 9 | [Finish & next module](docs/09-finish-and-next-module.md) | Checklist, save to GitHub, start the next one |

### Reference (read when you need it)

- [How it works](docs/reference/how-it-works.md): what happens inside `./build.sh`
- [module.yaml reference](docs/reference/module-yaml-reference.md): every field and slide type
- [Troubleshooting](docs/reference/troubleshooting.md): problems and fixes, by step
- [Cloud builds with GitHub Actions](docs/reference/cloud-build-github-actions.md): build without your PC (optional, later)
- [Manual editing with CapCut/Descript](docs/reference/manual-editing-capcut.md): only if you want to hand-edit a video
- [Working with Claude](docs/reference/working-with-claude.md): let Claude run the steps for you, cheaply
- [Why it is built this way & what changed](docs/reference/why-and-what-changed.md): tool choices and fixes to the old handbook

---

## The 4 commands you will use

Run them inside Ubuntu, in the project folder (`cd ~/linux-course`):

| Command | When | What it does |
|---------|------|--------------|
| `./setup.sh` | once | Installs every tool and tests it |
| `./new-module.sh 1.3` | start of a module | Makes the module folder, copies the AI prompt to your clipboard |
| `./paste-module.sh 1.3` | after the AI answers | Saves the AI answer as `module.yaml` and checks it |
| `./build.sh 1.3 --draft` / `./build.sh 1.3` | review / final | Builds everything: free voice (draft) or ElevenLabs voice (final) |

More build options: `--check` (check the file only) and `--slides` (slides PDF only, in seconds).

---

## What is automatic and what you do

| Part | Who | How |
|------|-----|-----|
| Lesson content, slides text, narration, demo commands, quiz, lab | **AI** writes, **you** review | [Master prompt](prompts/module_prompt.md) → `module.yaml` |
| Slides PDF + slide images | automatic | ReportLab (same look as the approved Module 1.2 PDF) |
| Terminal demo videos | automatic | VHS by Charm, Catppuccin Macchiato theme |
| Voiceover | automatic | ElevenLabs API (final) or Piper (free draft) |
| Syncing slides, terminal and voice into one video | automatic | FFmpeg: each scene lasts exactly as long as its narration |
| Captions (.srt/.vtt), quiz file, narration script | automatic | from `module.yaml` |
| Killercoda lab files | automatic | from `module.yaml` |
| Upload to the LMS + Killercoda | **you** | [Step 8](docs/08-publish-the-module.md) (about 15 minutes) |

---

## Project map

```
linux-course/
├── README.md                ← you are here
├── docs/                    ← the step-by-step guide (00 → 09) + reference/
├── setup.sh                 ← one-time installer
├── new-module.sh            ← start a module (prompt → clipboard)
├── paste-module.sh          ← save the AI answer as module.yaml
├── build.sh                 ← build a module
├── course.yaml              ← course settings: outline, voice, terminal look, video
├── .env.example             ← template for your secret API key (copy to .env)
├── prompts/
│   └── module_prompt.md     ← THE master prompt (v3)
├── modules/
│   └── module-1.2-dns-ttl-caching/
│       ├── module.yaml      ← everything about this module (the only file you edit)
│       ├── Linux_DNS_and_TTL_Caching_Architecture.pdf   ← approved original slides
│       └── build/publish/   ← results appear here (not uploaded to GitHub)
├── engine/                  ← the Python code behind build.sh (no need to touch)
├── assets/                  ← put instructor.png here (optional photo in the video corner)
├── archive/                 ← the original documents (old versions, kept for reference)
└── .github/workflows/       ← optional cloud build
```

## Modules

| Module | Title | Status |
|--------|-------|--------|
| 1.2 | [Linux DNS & TTL Caching Architecture](modules/module-1.2-dns-ttl-caching/module.yaml) | Content approved. Draft build tested. Final voice: waiting for ElevenLabs key |
| 1.3 | Linux System Logging (/var/log & journalctl) | Next. Start with [step 5](docs/05-create-a-module-with-ai.md) |
