[⬅ Step 7](07-build-the-final-video.md) · [🏠 Home](../README.md) · **Step 8 of 9** · [Next ➡ Step 9: Finish & next module](09-finish-and-next-module.md)

# Step 8: Publish the module

**Goal:** students can watch the lesson, download the slides, take the quiz and do the lab.
**Time:** 20 minutes (the first time, another 20 for the one-time lab setup).
**Your files:** `explorer.exe modules/module-1.3-*/build/publish` (the folder also has a `README.txt` listing them).

| File | Goes to |
|------|---------|
| `Module_1_3_Final.mp4` | LMS: lesson video |
| `Module_1_3_Captions.vtt` (or `.srt`) | LMS: subtitles of that video |
| `Module_1_3_Slides.pdf` | LMS: downloadable resource |
| `Module_1_3_Quiz.md` | LMS: quiz (copy the questions in) |
| `killercoda/<lab folder>` | Your Killercoda labs repository on GitHub |

---

## A. Course platform (LMS)

Button names differ a little between LearnWorlds and Thinkific, but the steps are the same:

1. **Create the lesson:** in your course, add a section (e.g. *Section 1: Linux Networking & Logging*) and a lesson named **Module 1.3: <title>**.
2. **Video:** add a **Video** item → upload `Module_1_3_Final.mp4`.
3. **Subtitles:** in that video's settings find **Subtitles / Captions** → upload `Module_1_3_Captions.vtt` (use the `.srt` if `.vtt` is not accepted) → language **English**.
4. **Slides:** add a **PDF / Download** item → upload `Module_1_3_Slides.pdf` → title *Lesson slides*.
5. **Quiz:** add a **Quiz / Assessment** item. Open `Module_1_3_Quiz.md` in VS Code. For each of the 3 questions, copy the question and options, mark the correct option, and paste the **Feedback** text into the explanation/feedback box.
6. **Lab:** add an **Embed / Web page / Link** item for the Killercoda lab (part B gives you the link).
7. Preview the lesson as a student, then **Publish**.

## B. Killercoda lab

### B1. One-time setup: a labs repository

Killercoda reads labs from a GitHub repository. Keep labs in their own small repository:

1. Create it: [github.com/new](https://github.com/new) → name `linux-course-labs` → **Public** → tick **Add a README file** → **Create repository**.
2. Download it next to the course project (in Ubuntu):

   ```bash
   cd ~ && gh repo clone sagidi/linux-course-labs
   ```

3. Connect it in Killercoda: open [killercoda.com/creators](https://killercoda.com/creators) → choose to add/connect a **GitHub repository** → enter `sagidi/linux-course-labs` → follow Killercoda's on-screen steps. It gives you a **deploy key** and a **webhook** to add in GitHub:
   - Deploy key goes in: [linux-course-labs → Settings → Deploy keys](https://github.com/sagidi/linux-course-labs/settings/keys) → **Add deploy key** → paste → **Add key**.
   - Webhook goes in: [linux-course-labs → Settings → Webhooks](https://github.com/sagidi/linux-course-labs/settings/hooks) → **Add webhook** → paste the URL (and secret, if shown) → **Add webhook**.

   After this, every push to the repository updates your labs on Killercoda automatically.

### B2. Every module: publish its lab

```bash
cp -r ~/linux-course/modules/module-1.3-*/build/publish/killercoda/* ~/linux-course-labs/
cd ~/linux-course-labs
git add . && git commit -m "Add lab for module 1.3" && git push
cd ~/linux-course
```

After a minute the lab appears in your Killercoda creator profile. Open it, **do the whole lab once yourself**
(including the **Check** buttons), then copy its URL into the LMS lab item from part A.

> The lab folder contains `index.json` (title + step list), `intro.md`, `step1/text.md`… and `verify.sh`
> scripts that check the student's work. To change a lab, edit the `lab:` section of `module.yaml`,
> rebuild, and copy it again.

---

## ✅ Done when

You opened the lesson **as a student** and the video, subtitles, slides, quiz and lab all work.

[⬅ Step 7](07-build-the-final-video.md) · [🏠 Home](../README.md) · **Step 8 of 9** · [Next ➡ Step 9: Finish & next module](09-finish-and-next-module.md)
