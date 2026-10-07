[🏠 Home](../../README.md) · Reference · Optional, set up later

# Cloud builds with GitHub Actions

GitHub can build a module **on its own computers**: same result as `./build.sh`, but your PC can be off.
Useful when your PC is busy or slow. The workflow file is already in the project:
[`.github/workflows/build-module.yml`](../../.github/workflows/build-module.yml). It only runs when **you** start it.

> The **Run workflow** button only appears once this file is on the `main` branch.

## One-time: give GitHub your ElevenLabs key (only needed for `final` builds)

1. Open [sagidi/linux-course → Settings → Secrets and variables → Actions → New repository secret](https://github.com/sagidi/linux-course/settings/secrets/actions/new).
2. **Name:** `ELEVENLABS_API_KEY` (exactly like this).
3. **Secret:** paste your ElevenLabs key → **Add secret**.

GitHub keeps it encrypted. Nobody, including you, can read it back, and it never appears in logs.

## Every time: build a module

1. Make sure the module's `module.yaml` is pushed to GitHub ([step 9, part 2](../09-finish-and-next-module.md#2-save-your-work-to-github)).
2. Open [Actions → Build a module](https://github.com/sagidi/linux-course/actions/workflows/build-module.yml).
3. Click **Run workflow** (right side) → type the module number (e.g. `1.3`) → choose `draft` or `final` → **Run workflow**.
4. Wait about 15-20 minutes (it installs the tools first). A green tick means done.
5. Click the finished run → scroll to **Artifacts** → download `module-1.3-final` (a zip with everything from `build/publish/`).

## Cost

Free for public repositories. For private repositories, GitHub's free plan includes a monthly allowance of
Actions minutes (see [GitHub billing](https://github.com/settings/billing)). One build uses about 20 minutes.

[🏠 Home](../../README.md)
