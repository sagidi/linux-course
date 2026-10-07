[🏠 Home](../../README.md) · Reference

# Troubleshooting

**First thing to try, always:** run `./setup.sh` again. It re-installs anything missing and tests every tool.
Then re-run the command that failed. Error messages from the build start with `ERROR:` and say what to do.

---

## Step 1: WSL

| Problem | Fix |
|---------|-----|
| `virtualization` / `Virtual Machine Platform` error | Enable **Virtualization (VT-x / AMD-V / SVM)** in your PC's BIOS/UEFI, restart, run `wsl --install -d Ubuntu-24.04` again |
| `wsl` is not recognised | Update Windows (Settings → Windows Update) |
| Ubuntu closes immediately | PowerShell (admin): `wsl --update`, then `wsl --shutdown`, then reopen Ubuntu |
| Forgot the Ubuntu password | PowerShell: `wsl -u root`, then `passwd yourusername` |
| Everything is slow | Make sure you work in `~/linux-course`, **not** `/mnt/c/...` |

## Step 2: setup

| Problem | Fix |
|---------|-----|
| `Permission denied` running a `.sh` file | `chmod +x *.sh` |
| `bash\r: No such file or directory` | A file was saved with Windows line endings. Fix: `sed -i 's/\r$//' *.sh`. In VS Code, click `CRLF` (bottom-right) → choose `LF` → save |
| `E: Unable to locate package ...` | `sudo apt update`, then `./setup.sh` again |
| `ttyd version (...) is out of date` | `./setup.sh` installs a newer ttyd automatically |
| `externally-managed-environment` (pip) | Do not use `pip install` yourself. `./setup.sh` installs Python packages into `.venv` |
| Piper voice download failed | Drafts still work with the robotic espeak voice. Run `./setup.sh` again later |

## VHS (terminal recording)

| Problem | Fix |
|---------|-----|
| `FAIL VHS could not record a test video` | Read the log: `cat /tmp/vhs-selftest.log`, then match the message below |
| `error while loading shared libraries: libnss3.so` (or another `.so`) | Browser libraries missing: `./setup.sh` (installs them) |
| `could not launch browser` / `no sandbox` | Only when running as `root`: `export VHS_NO_SANDBOX=1` and run again. As your normal user this does not happen |
| `Require: ... not found` (e.g. `dig`) | The demo uses a tool that is not installed: `sudo apt install -y dnsutils` (for `dig`) or the right package |
| Recording never finishes | A demo command is waiting for input. Check `run:` lines (no `less`, `nano`, `top`, `ping` without `-c`) |
| Terminal shows WSL notices or messy output | Create a clean sample file in the demo's `setup:` and show that file (see Module 1.2 demo 1) |
| Re-record a demo without changing it | Delete its clip: `rm modules/module-1.2-*/build/work/demos/<scene-id>.mp4` |

## Slides

| Problem | Fix |
|---------|-----|
| `slide for scene 'x' has too much text` | Shorten that slide's text in `module.yaml` (or ask the AI to) |
| `note: ... shrunk slightly to fit` | Only a note. The slide fits but the text is a bit smaller. Shorten it if you like |
| Arrows/lines show as boxes | Fonts missing: `sudo apt install -y fonts-dejavu-core fonts-liberation` |
| `is not valid YAML` | Usually a colon `:` inside text without quotes. Put the whole value in double quotes. The message shows the line |

## Voice

| Problem | Fix |
|---------|-----|
| `ELEVENLABS_API_KEY is not set` | Add the key to `.env` ([step 3A](../03-create-accounts-and-keys.md#a-elevenlabs-final-voice)), or use `--draft` |
| ElevenLabs `401` / `402` / `404` / `422` | See [step 7](../07-build-the-final-video.md#-if-something-goes-wrong) |
| A word is pronounced wrong | Add it to `pronounce:` in `course.yaml`, then rebuild ([step 6](../06-review-the-module.md#4-watch-the-free-draft-video-10-minutes)) |
| Draft voice sounds robotic | Piper is not installed and espeak is used. Run `./setup.sh` again |

## Video

| Problem | Fix |
|---------|-----|
| A demo appears too early or late | It follows the narration. Move the sentence to the right scene in `module.yaml` |
| `every scene with narration needs a 'demo'` | Add a short `demo:` to that scene (the video is terminal-only) |
| Too fast / too slow overall | `course.yaml`: `video.scene_gap`, `terminal.typing_speed`, `terminal.playback_speed` |
| No photo in the corner | Check that `assets/instructor.png` exists and `course.yaml` → `video.avatar` points to it |
| Want subtitles always visible | `course.yaml` → `video.burn_captions: true` |
| Start completely fresh | `rm -r modules/module-1.2-*/build` and build again |

## Clipboard (new-module / paste-module)

| Problem | Fix |
|---------|-----|
| `Could not copy to the clipboard` | Open `modules/<module>/prompt.md` in VS Code, **Ctrl+A**, **Ctrl+C** |
| `Cannot read the clipboard` / `clipboard is empty` | Save the AI answer as `answer.txt`, then `./paste-module.sh 1.3 --file answer.txt` |
| `does not look like a module.yaml` | You copied the wrong thing. Use the **Copy** button on the AI's YAML box |

## Still stuck?

Ask Claude with the **exact error text** and the command you ran. See [Working with Claude](working-with-claude.md).

[🏠 Home](../../README.md)
