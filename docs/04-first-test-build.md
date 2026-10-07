[⬅ Step 3](03-create-accounts-and-keys.md) · [🏠 Home](../README.md) · **Step 4 of 9** · [Next ➡ Step 5: Create a module with AI](05-create-a-module-with-ai.md)

# Step 4: First test build (Module 1.2: DNS)

**Goal:** prove the whole pipeline works on your PC by building the finished Module 1.2.
**Time:** 10 minutes (the build runs by itself for about 5).
**Cost:** free. The draft uses the free Piper voice.

Module 1.2 is already written: [`modules/module-1.2-dns-ttl-caching/module.yaml`](../modules/module-1.2-dns-ttl-caching/module.yaml).
Its slides are your approved PDF, and its narration is your approved script.

---

## 1. Check the module file (seconds)

```bash
cd ~/linux-course
./build.sh 1.2 --check
```

Expected: `module.yaml: OK (0 warning(s)).`

## 2. Build only the slides (seconds)

```bash
./build.sh 1.2 --slides
explorer.exe modules/module-1.2-dns-ttl-caching/build/publish
```

A Windows folder opens. Double-click **`Module_1_2_Slides.pdf`**: 12 slides in 16:9 with the same look as your approved PDF.

## 3. Build the full draft video (about 5 minutes)

```bash
./build.sh 1.2 --draft
```

You will see it work through 6 stages:

```
[1/6] Checking module.yaml
[2/6] Making 12 slides
[3/6] Recording terminal demos with VHS        <- types the commands for real, about 1 min each
[4/6] Making the voiceover                     <- free Piper voice
[5/6] Putting the video together               <- one line per scene, with its length
[6/6] Writing quiz, narration script and Killercoda lab
=== DONE - video length 4m50s ===
```

## 4. Watch the result

```bash
explorer.exe modules/module-1.2-dns-ttl-caching/build/publish
```

| File | What it is |
|------|-----------|
| `Module_1_2_DRAFT.mp4` | The full lesson: slides + live terminal + voice, all in sync |
| `Module_1_2_Slides.pdf` | Student download |
| `Module_1_2_Captions.srt` / `.vtt` | Subtitles |
| `Module_1_2_Quiz.md` | 3 quiz questions with answers + feedback |
| `Module_1_2_Narration.txt` | The full script, scene by scene |
| `killercoda/` | The ready-made hands-on lab |
| `README.txt` | What to upload where |

Watch `Module_1_2_DRAFT.mp4` from start to finish. Check that:

- [ ] Each slide stays on screen while the voice talks about it, then moves on.
- [ ] Scenes 8 and 9 show the **dark terminal** typing `cat` and `dig` commands with real output.
- [ ] The voice is clear (Piper is a good free voice. The final ElevenLabs voice is better).

## 5. (Optional) Build the final version now

If you saved your ElevenLabs key in [step 3](03-create-accounts-and-keys.md#a-elevenlabs-final-voice):

```bash
./build.sh 1.2
```

It prints how many characters it sends to ElevenLabs (about 4,000) and creates `Module_1_2_Final.mp4`.
Slides and terminal recordings are reused, so this is quicker.

> **Module 1.2's voice = your approved script, word for word.** It is saved in
> `modules/module-1.2-dns-ttl-caching/narration_approved.txt`, and the build stops if the narration in
> `module.yaml` is ever different. The only additions are on the slides and quiz (not spoken):
> "Fix:" commands on the outage slide and 2 extra quiz questions, marked `# NEW`.

---

## ✅ Done when

`Module_1_2_DRAFT.mp4` plays with slides, terminal demos and voice in sync. **Your pipeline works.**
From now on, every module is made the same way.

## ❌ If something goes wrong

| What you see | Fix |
|--------------|-----|
| `The tools are not installed yet` | Run `./setup.sh` ([step 2](02-install-the-tools.md)) |
| Stops at `[3/6] Recording terminal demos` | [Troubleshooting → VHS](reference/troubleshooting.md#vhs-terminal-recording) |
| `note: Piper voice not found - using espeak` | Draft still works (robotic voice). Run `./setup.sh` again to install Piper |
| `ERROR: ELEVENLABS_API_KEY is not set` | You ran the final build without a key. Add `--draft`, or do [step 3A](03-create-accounts-and-keys.md#a-elevenlabs-final-voice) |

[⬅ Step 3](03-create-accounts-and-keys.md) · [🏠 Home](../README.md) · **Step 4 of 9** · [Next ➡ Step 5: Create a module with AI](05-create-a-module-with-ai.md)
