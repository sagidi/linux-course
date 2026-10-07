[⬅ Step 5](05-create-a-module-with-ai.md) · [🏠 Home](../README.md) · **Step 6 of 9** · [Next ➡ Step 7: Build the final video](07-build-the-final-video.md)

# Step 6: Review the module

**Goal:** you are happy with the facts, the slides and the free draft video **before** paying for the final voice.
**Time:** 30-60 minutes.
**Why this matters:** AI can be confidently wrong. You are the expert, and this step is your quality gate.

Open the module file in VS Code (keep it open for this whole step):

```bash
cd ~/linux-course
code modules/module-1.3-*/module.yaml
```

---

## 1. Read the content (15 minutes)

Go through `module.yaml` top to bottom with this checklist:

- [ ] **Facts:** every statement is correct. No made-up file paths, flags or numbers.
- [ ] **Plain English:** a beginner understands each narration sentence on the first listen.
- [ ] **Real-world link:** it connects to Splunk / ClickHouse log pipelines where it makes sense.
- [ ] **Outage table:** each row has Why Required, If NOT Done, and a real **Fix:** command.
- [ ] **Quiz:** 3 questions, one clearly correct answer each, explanations make sense.
- [ ] **Lab:** steps are doable in a fresh Ubuntu terminal, and `verify` lines check the right thing.

## 2. Try the demo commands yourself (5 minutes)

Every `run:` line under `demo:` is typed for real during the recording. Paste each one into Ubuntu:

- It works and finishes by itself within a few seconds.
- The output is short and matches what the slide shows.

If a command needs a demo file, the `setup:` lines create it. Run those first.

## 3. Check the slides (seconds per try)

```bash
./build.sh 1.3 --slides
explorer.exe modules/module-1.3-*/build/publish
```

Open `Module_1_3_Slides.pdf`. Look for text that is too long or unclear. Edit `module.yaml`, save,
run the command again, then reopen the PDF. Repeat until it looks right.

| To get this on a slide | Write this in module.yaml |
|------------------------|---------------------------|
| **bold** | `**bold**` |
| `code` style | `` `cat /etc/hosts` `` |
| red / orange / green / blue text | `[red]Pipeline Stopped:[/red]` |
| a line break | a new line inside a `\|` block, or `\n` inside quotes |

## 4. Watch the free draft video (10 minutes)

```bash
./build.sh 1.3 --draft
```

Open `Module_1_3_DRAFT.mp4` and watch it **all the way through**:

- [ ] Each slide matches what the voice is saying.
- [ ] The terminal demos show the right commands and real output.
- [ ] Pacing feels right, not rushed, not too slow.
- [ ] Words are pronounced well (see below).

**Fixing pronunciation:** if a word sounds wrong (e.g. `journalctl`), add it to `pronounce:` in
`course.yaml`. It changes only the audio, not the slides or captions:

```yaml
pronounce:
  "journalctl": "journal control"
  "nginx": "engine x"
```

**Changing pacing:**

| To change | Edit |
|-----------|------|
| Pause after each scene | `course.yaml` → `video.scene_gap` (seconds) |
| Typing speed in the terminal | `course.yaml` → `terminal.typing_speed` |
| How long output stays on screen | the `wait:` value of that command in `module.yaml` |

Rebuilding is fast: **only what you changed is redone** (unchanged terminal recordings and audio are reused).

---

## ✅ Done when

You watched the whole draft and would be proud to show it to a student.

[⬅ Step 5](05-create-a-module-with-ai.md) · [🏠 Home](../README.md) · **Step 6 of 9** · [Next ➡ Step 7: Build the final video](07-build-the-final-video.md)
