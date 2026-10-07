[⬅ Step 8](08-publish-the-module.md) · [🏠 Home](../README.md) · **Step 9 of 9** · [Back to Step 5 for the next module ↩](05-create-a-module-with-ai.md)

# Step 9: Finish the module & start the next one

**Goal:** the module is saved to GitHub, marked done, and you are ready for the next one.
**Time:** 5 minutes.

---

## 1. Module checklist

Copy this list into your notes for each module and tick it off:

- [ ] `./new-module.sh X.Y` → prompt pasted into a new AI chat ([step 5](05-create-a-module-with-ai.md))
- [ ] `./paste-module.sh X.Y` → `module.yaml: OK`
- [ ] Facts, commands, quiz and lab reviewed ([step 6](06-review-the-module.md))
- [ ] Slides PDF looks right (`--slides`)
- [ ] Draft video watched start to finish (`--draft`)
- [ ] Final video built with ElevenLabs ([step 7](07-build-the-final-video.md))
- [ ] Video + subtitles + slides + quiz uploaded to the LMS ([step 8A](08-publish-the-module.md#a-course-platform-lms))
- [ ] Lab pushed to `linux-course-labs` and tested on Killercoda ([step 8B](08-publish-the-module.md#b-killercoda-lab))
- [ ] Lesson previewed as a student and published
- [ ] Changes saved to GitHub (part 2 below)

## 2. Save your work to GitHub

The **source** (`module.yaml`, `course.yaml`) is what you save. The videos are not uploaded (they are big,
and `./build.sh` can rebuild them at any time).

```bash
cd ~/linux-course
git add .
git commit -m "Module 1.3 done"
git push
```

> Your `.env` (API key) and the `build/` folders are never uploaded. `.gitignore` blocks them.

## 3. Mark it done

Open `README.md` (`code README.md`), find the **Modules** table at the bottom, and update the status, e.g.
`Published`. Add the next module to `course.yaml` → `outline:` if it is not there yet.
Save, then repeat part 2 to push.

## 4. Next module

Go back to **[Step 5: Create a module with AI](05-create-a-module-with-ai.md)** with the next number.

---

## Tips that save time

- **Improve the prompt, not each answer.** If the AI makes the same mistake in every module, add a line to
  [`prompts/module_prompt.md`](../prompts/module_prompt.md). Every future module gets the fix.
- **Change the look for all modules at once** in `course.yaml` (voice, terminal theme, font size, pauses).
- **Rebuild old modules** after changing `course.yaml`: `./build.sh 1.2 --draft` (only affected parts are redone).
- **Ask Claude to help** with the steps, cheaply: [Working with Claude](reference/working-with-claude.md).

[⬅ Step 8](08-publish-the-module.md) · [🏠 Home](../README.md) · **Step 9 of 9** · [Back to Step 5 for the next module ↩](05-create-a-module-with-ai.md)
