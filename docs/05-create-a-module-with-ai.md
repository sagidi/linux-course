[⬅ Step 4](04-first-test-build.md) · [🏠 Home](../README.md) · **Step 5 of 9** · [Next ➡ Step 6: Review the module](06-review-the-module.md)

# Step 5: Create a module with AI

**Goal:** a new `module.yaml` with all the content for one module, written by AI from the master prompt.
**Time:** 10-15 minutes.
**Strategy:** build **one complete module at a time** (all its sub-topics), lock it, then start the next.
Asking the AI for several modules at once makes it cut corners and drop details.

The example below makes **Module 1.3**. For another module, change the number.

---

## 1. Add the module to the course outline (once per module)

Open `course.yaml`:

```bash
cd ~/linux-course
code course.yaml
```

Under `outline:` make sure the module is listed **in teaching order**, for example:

```yaml
outline:
  - number: "1.2"
    title: "Linux DNS & TTL Caching Architecture"
  - number: "1.3"
    title: "Linux System Logging (/var/log & journalctl)"
```

Save (**Ctrl+S**). The prompt uses this list to tell the AI what came before and what comes next.

## 2. Make the module folder + prompt

```bash
./new-module.sh 1.3
```

Want to steer the AI? Add your notes in quotes as a third value:

```bash
./new-module.sh 1.3 "" "Focus on journalctl filters. Use Splunk forwarder logs as the example."
```

(The empty `""` keeps the title from `course.yaml`.)

It prints:

```
Folder ready:  modules/module-1.3-linux-system-logging-var-log-journalctl/
Prompt saved:  modules/module-1.3-.../prompt.md
The prompt is on your clipboard.
```

The prompt is the [master prompt](../prompts/module_prompt.md) with this module's details filled in, plus
the approved Module 1.2 as an example to copy the style from.

## 3. Paste it into the AI

1. Open your AI chat ([Gemini](https://gemini.google.com), [Claude](https://claude.ai) or [ChatGPT](https://chatgpt.com)). Pick the **most capable model** in the menu, because the answer is long (about 300 lines).
2. Start a **new chat** (old chats confuse it).
3. Press **Ctrl+V**, then **Enter**.
4. Wait until it has finished writing. The answer is one grey box that starts with `yaml`.

> **Answer stopped halfway?** Do **not** ask it to "continue" (that splits the file in two).
> Instead type: *"Your answer was cut off. Send the complete module.yaml again in ONE yaml block."*

## 4. Save the answer

1. Click the **Copy** button on the answer's grey box (top-right of the box).
2. In Ubuntu:

   ```bash
   ./paste-module.sh 1.3
   ```

It reads your clipboard, keeps only the YAML, saves it as `module.yaml`, and checks it:

- `module.yaml: OK`: go to the next step.
- `PROBLEM ...` lines: go to part 5.

> **Paste does not work?** Save the AI answer in a text file instead (VS Code → **File → New File** →
> paste → save as `answer.txt` in `~/linux-course`), then run `./paste-module.sh 1.3 --file answer.txt`.

## 5. If the check finds problems

The check catches things like text too long for a slide, a demo command that would freeze the
recording, or a missing quiz answer. Let the AI fix them:

1. Select all the `PROBLEM` lines in Ubuntu and copy them.
2. In the **same** AI chat, type: *"Fix these problems and send the complete corrected module.yaml:"* then paste the lines.
3. Copy the new answer → run `./paste-module.sh 1.3` again. (Each paste backs up the old file as `module.yaml.bak-...`.)

You can also fix small things yourself: `code modules/module-1.3-*/module.yaml`.
Field-by-field help: [module.yaml reference](reference/module-yaml-reference.md).

---

## ✅ Done when

`./paste-module.sh 1.3` (or `./build.sh 1.3 --check`) prints `module.yaml: OK`.

[⬅ Step 4](04-first-test-build.md) · [🏠 Home](../README.md) · **Step 5 of 9** · [Next ➡ Step 6: Review the module](06-review-the-module.md)
