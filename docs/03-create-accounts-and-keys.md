[⬅ Step 2](02-install-the-tools.md) · [🏠 Home](../README.md) · **Step 3 of 9** · [Next ➡ Step 4: First test build](04-first-test-build.md)

# Step 3: Create accounts & keys

**Goal:** the accounts the course needs exist, and your ElevenLabs key is saved safely.
**Time:** 20 minutes.

| Part | Needed for | Do it |
|------|-----------|-------|
| [A. ElevenLabs key](#a-elevenlabs-final-voice) | Final videos (step 7) | Now, or skip until step 7. Drafts are free without it |
| [B. Your photo](#b-optional-your-photo-in-the-video-corner) | Optional round photo in the video | Any time |
| [C. Killercoda](#c-killercoda-hands-on-labs) | Labs (step 8) | Now or at step 8 |
| [D. Course platform (LMS)](#d-course-platform-lms) | Publishing (step 8) | Now or at step 8 |
| [E. GitHub secret](#e-later-github-secret-for-cloud-builds) | Cloud builds (optional) | Later |

> 🔒 **Secret keys never go in chats, screenshots or GitHub.** They go only in the `.env`
> file, which is set up so it is never uploaded.

---

## A. ElevenLabs (final voice)

1. **Create an account:** [elevenlabs.io/app/sign-up](https://elevenlabs.io/app/sign-up).
2. **Choose a plan:** [elevenlabs.io/pricing](https://elevenlabs.io/pricing). For a course you sell, use a **paid plan (Starter or higher)**, because the free plan is not for commercial use. One module uses about **4,000 credits**.
3. **Create an API key:** open [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) → **Create API Key** → name it `linux-course` → if it shows permissions, allow **Text to Speech** (and **Voices: read**) → **Create** → **copy the key**.
4. **Save the key in `.env`** (in Ubuntu):

   ```bash
   cd ~/linux-course
   nano .env
   ```

   Put your key between the quotes, like `ELEVENLABS_API_KEY="sk_abc123..."`.
   Save: **Ctrl+O**, **Enter**. Exit: **Ctrl+X**.

5. **Test the key** (uses about 30 credits):

   ```bash
   cd ~/linux-course && source .env && curl -s -o ~/voice-test.mp3 -w "HTTP %{http_code}\n" \
     -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
     -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
     -d '{"text":"Hello! This is the voice of my Linux course.","model_id":"eleven_multilingual_v2"}'
   ```

   - `HTTP 200` means it works. Listen: run `explorer.exe ~` and double-click `voice-test.mp3`.
   - `HTTP 401` means the key is wrong: repeat parts 3-4.

6. **(Optional) Choose a different voice:** browse [elevenlabs.io/app/voice-library](https://elevenlabs.io/app/voice-library) → **Add to my voices** → in **My Voices** click the voice → copy its **Voice ID** → open `course.yaml` (`code course.yaml`) and replace the value of `voice_id:`. The default is "Rachel" (`21m00Tcm4TlvDq8ikWAM`). Calm, clear voices work best for teaching.

## B. (Optional) Your photo in the video corner

Save a **square** photo of yourself (at least 400×400 pixels) as `assets/instructor.png`:

```bash
explorer.exe ~/linux-course/assets
```

Drag your photo into that folder and rename it `instructor.png`. Every video built from now on shows it
as a round badge in the bottom-right corner. Change the corner in `course.yaml` → `avatar_position`.
No photo means no badge (that is fine).

## C. Killercoda (hands-on labs)

1. Sign up (free) at [killercoda.com](https://killercoda.com) (log in with GitHub is easiest).
2. Open the creator area: [killercoda.com/creators](https://killercoda.com/creators).
3. Connecting your labs to GitHub is done once, in [step 8](08-publish-the-module.md#b-killercoda-lab).

## D. Course platform (LMS)

Pick one and start the free trial. Both do videos, PDFs, quizzes and embedded labs:

- [LearnWorlds](https://www.learnworlds.com) (strong interactive video + quizzes)
- [Thinkific](https://www.thinkific.com) (simple, popular)

What to upload where is in [step 8](08-publish-the-module.md).

## E. (Later) GitHub secret for cloud builds

Only if you want GitHub to build videos for you without your PC. Skip for now. Steps:
[Cloud builds with GitHub Actions](reference/cloud-build-github-actions.md).

---

## ✅ Done when

- `.env` contains your ElevenLabs key and the test printed `HTTP 200` (or you chose to do this at step 7).
- You have a Killercoda account and an LMS trial (or you will create them at step 8).

[⬅ Step 2](02-install-the-tools.md) · [🏠 Home](../README.md) · **Step 3 of 9** · [Next ➡ Step 4: First test build](04-first-test-build.md)
