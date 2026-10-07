[🏠 Home](../README.md) · **Step 0 of 9** · [Next ➡ Step 1: Install WSL + Ubuntu](01-install-wsl-ubuntu.md)

# Step 0: Tools to install (the full list)

This page lists **everything** the project uses, so nothing surprises you later.
You do **not** install anything on this page. The next steps walk you through each one.

---

## A. On your Windows PC (steps 1-2)

| # | Tool | What it does for you | Cost | Link | Installed in |
|---|------|----------------------|------|------|--------------|
| 1 | **WSL 2 + Ubuntu 24.04** | Runs Linux inside Windows. Every build command runs here. | Free | [Microsoft guide](https://learn.microsoft.com/windows/wsl/install) | [Step 1](01-install-wsl-ubuntu.md) |
| 2 | **Windows Terminal** | A nicer window for Ubuntu (already on Windows 11) | Free | [Microsoft Store](https://aka.ms/terminal) | [Step 1](01-install-wsl-ubuntu.md) |
| 3 | **VS Code** + **WSL extension** | Open and edit `module.yaml`, read these docs | Free | [VS Code](https://code.visualstudio.com/) · [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) | [Step 1](01-install-wsl-ubuntu.md) |
| 4 | **GitHub CLI (`gh`)** | Lets Ubuntu download and save this project to your GitHub | Free | [cli.github.com](https://cli.github.com/) | [Step 2](02-install-the-tools.md) |

## B. Inside Ubuntu: installed for you by `./setup.sh` (step 2)

You run **one command** and all of these are installed and tested automatically:

| Tool | What it does |
|------|--------------|
| **VHS** (by Charm) + **ttyd** | Records the terminal demos as video from a script (no screen recording, no typos) |
| **Chromium** | Used by VHS in the background (VHS downloads it on first use) |
| **FFmpeg** | Joins the terminal clips and the voice into the final video |
| **Python 3** + ReportLab, PyYAML, Requests, Pillow | Makes the slides and talks to ElevenLabs |
| **Piper** + voice `en_US-lessac-medium` | Free, natural-sounding voice for **draft** videos |
| **espeak-ng** | Backup free voice (robotic) if Piper is missing |
| **poppler-utils** | Turns the slides PDF into images for the video |
| **dig, nslookup, ping, jq, tree** | Linux tools used in the terminal demos |
| **DejaVu + Liberation fonts** | Fonts for the slides (so arrows like `──>` display correctly) |

## C. Online accounts (step 3 and step 8)

| # | Account | What it is for | Cost | Link | Needed by |
|---|---------|----------------|------|------|-----------|
| 1 | **GitHub** | Stores this project (you already have `sagidi/linux-course`) | Free | [github.com](https://github.com) | Step 2 |
| 2 | **AI chat**: Gemini, Claude or ChatGPT | Writes each module from the master prompt | Free tier works. Paid tiers write longer, better answers | [Gemini](https://gemini.google.com) · [Claude](https://claude.ai) · [ChatGPT](https://chatgpt.com) | Step 5 |
| 3 | **ElevenLabs** | The studio voice for **final** videos | Paid plan needed for a course you sell (commercial use) | [Pricing](https://elevenlabs.io/pricing) | Step 7 |
| 4 | **Killercoda** (creator) | Free browser Linux terminal for the hands-on labs | Free | [killercoda.com/creators](https://killercoda.com/creators) | Step 8 |
| 5 | **LMS**: LearnWorlds or Thinkific | Hosts your course: videos, PDFs, quizzes, students | Paid (free trials) | [LearnWorlds](https://www.learnworlds.com) · [Thinkific](https://www.thinkific.com) | Step 8 |

> **Cost of one module with ElevenLabs:** about 4,000 characters of narration
> (around 4,000 credits with the default voice model). Draft builds are free.
> You only pay again for the scenes you change.

## D. Optional (only if you want them)

| Tool | Why you might want it | Link |
|------|----------------------|------|
| **Claude Code** in Ubuntu | Lets Claude run `./build.sh` and fix problems on your PC for you | [Working with Claude](reference/working-with-claude.md) |
| **CapCut Desktop** or **Descript** | Hand-edit a video (the build already does this automatically) | [Manual editing](reference/manual-editing-capcut.md) |
| **Your photo** (square, `.png`) | Shown as a round badge in the corner of every video | Save it as `assets/instructor.png` |

---

## ✅ Done when

You know what will be installed and which accounts you will create. Nothing to install yet.

[🏠 Home](../README.md) · **Step 0 of 9** · [Next ➡ Step 1: Install WSL + Ubuntu](01-install-wsl-ubuntu.md)
