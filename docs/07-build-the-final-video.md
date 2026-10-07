[⬅ Step 6](06-review-the-module.md) · [🏠 Home](../README.md) · **Step 7 of 9** · [Next ➡ Step 8: Publish the module](08-publish-the-module.md)

# Step 7: Build the final video

**Goal:** the finished lesson video with your ElevenLabs studio voice.
**Time:** 5 minutes.
**You need:** your ElevenLabs key in `.env` ([step 3A](03-create-accounts-and-keys.md#a-elevenlabs-final-voice)) and a reviewed module ([step 6](06-review-the-module.md)).
**Cost:** about 4,000 ElevenLabs credits per module (first time). Later changes only cost the changed scenes.

---

## 1. Run the final build

```bash
cd ~/linux-course
./build.sh 1.3
```

At the voiceover stage it shows what it will spend:

```
[4/6] Making the voiceover
  voice: ElevenLabs (final voice)
  characters to send to ElevenLabs now: 3,998 (cached scenes are free)
```

## 2. Watch it

```bash
explorer.exe modules/module-1.3-*/build/publish
```

Open **`Module_1_3_Final.mp4`**. It is the same as the draft, but with the ElevenLabs voice.
Listen for pronunciation: fix it in `course.yaml` → `pronounce:` and run `./build.sh 1.3` again
(only the scenes with that word are re-generated).

## 3. Changed something after the final build?

Just run `./build.sh 1.3` again. Only changed scenes are sent to ElevenLabs. Everything else is reused.

---

## ✅ Done when

`Module_1_3_Final.mp4` plays with the studio voice and you are happy with it.

## ❌ If something goes wrong

| Message | Meaning / fix |
|---------|---------------|
| `ELEVENLABS_API_KEY is not set` | Key missing in `.env`. See [step 3A](03-create-accounts-and-keys.md#a-elevenlabs-final-voice) |
| `ElevenLabs error 401` | Key is wrong or was deleted. Make a new key and update `.env` |
| `ElevenLabs error 402` | Out of credits, or your plan does not include API use. Check [your subscription](https://elevenlabs.io/app/subscription) |
| `ElevenLabs error 404` | The `voice_id` in `course.yaml` is not in your account. Add the voice to **My Voices** first |
| `ElevenLabs error 422` | `model_id` or voice settings in `course.yaml` were rejected. Use `eleven_multilingual_v2` |

[⬅ Step 6](06-review-the-module.md) · [🏠 Home](../README.md) · **Step 7 of 9** · [Next ➡ Step 8: Publish the module](08-publish-the-module.md)
