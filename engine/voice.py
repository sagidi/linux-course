"""Narration text -> one audio file per scene.

Voices:
  elevenlabs  final studio voice (needs ELEVENLABS_API_KEY, costs credits)
  piper       free, natural-sounding offline voice (used for drafts)
  espeak      free robotic voice (last-resort draft fallback)

Every audio file is cached by its text + voice settings, so changing one
scene only re-generates that one scene. You never pay twice for the same
sentence.
"""
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from common import fail, run, say, sha

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
PIPER_DIR = Path(os.environ.get("PIPER_VOICES_DIR", Path.home() / ".local/share/piper-voices"))


def spoken_text(text, pronounce):
    t = " ".join(str(text).split())
    for written, spoken in (pronounce or {}).items():
        t = re.sub(re.escape(str(written)), str(spoken), t)
    return t


def piper_ready(voice):
    try:
        import piper  # noqa: F401
    except ImportError:
        return False
    return (PIPER_DIR / f"{voice}.onnx").exists()


def pick_provider(cfg, draft):
    if draft:
        voice = cfg.get("piper", {}).get("voice", "en_US-lessac-medium")
        if piper_ready(voice):
            return "piper"
        if shutil.which("espeak-ng"):
            say("  note: Piper voice not found - using the robotic espeak-ng draft voice "
                "(run ./setup.sh to install Piper)")
            return "espeak"
        fail("No free draft voice installed. Run ./setup.sh")
    provider = cfg.get("provider", "elevenlabs")
    if provider == "elevenlabs" and not os.environ.get("ELEVENLABS_API_KEY"):
        fail("ELEVENLABS_API_KEY is not set, so the final voice cannot be made.\n"
             "  - Add your key to the .env file (see docs/03-create-accounts-and-keys.md), or\n"
             "  - build a free draft instead:  ./build.sh <module> --draft")
    return provider


def settings_fingerprint(provider, cfg):
    if provider == "elevenlabs":
        e = cfg.get("elevenlabs", {})
        return (provider, e.get("voice_id"), e.get("model_id"), e.get("stability"),
                e.get("similarity_boost"), e.get("style"), e.get("speed"))
    if provider == "piper":
        p = cfg.get("piper", {})
        return (provider, p.get("voice"), p.get("length_scale"))
    return (provider, cfg.get("espeak", {}).get("voice"), cfg.get("espeak", {}).get("speed"))


# --------------------------------------------------------------------------
def eleven(text, prev_text, next_text, cfg, out_path):
    import requests
    e = cfg.get("elevenlabs", {})
    body = {
        "text": text,
        "model_id": e.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": {k: e[k] for k in ("stability", "similarity_boost", "style", "speed")
                           if e.get(k) is not None},
    }
    if prev_text:
        body["previous_text"] = prev_text[-1000:]
    if next_text:
        body["next_text"] = next_text[:1000]
    headers = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
               "Content-Type": "application/json", "Accept": "audio/mpeg"}
    url = ELEVEN_URL.format(voice_id=e.get("voice_id", "21m00Tcm4TlvDq8ikWAM"))
    for attempt in range(4):
        try:
            r = requests.post(url, params={"output_format": "mp3_44100_128"},
                              json=body, headers=headers, timeout=180)
        except requests.RequestException as ex:
            if attempt == 3:
                fail(f"Could not reach ElevenLabs: {ex}")
            time.sleep(2 ** (attempt + 1))
            continue
        if r.status_code == 200:
            out_path.write_bytes(r.content)
            return
        if r.status_code in (429, 500, 502, 503) and attempt < 3:
            time.sleep(2 ** (attempt + 2))
            continue
        hint = {401: "Your API key is wrong or expired - check the .env file.",
                402: "Your ElevenLabs plan is out of credits or does not allow API use.",
                404: "The voice_id in course.yaml was not found in your ElevenLabs account.",
                422: "ElevenLabs rejected the request (check model_id / voice settings in course.yaml)."
                }.get(r.status_code, "")
        fail(f"ElevenLabs error {r.status_code}. {hint}\n{r.text[:500]}")


def piper(text, cfg, out_path, tmp_dir):
    p = cfg.get("piper", {})
    txt = tmp_dir / "piper_input.txt"
    txt.write_text(text, encoding="utf-8")
    cmd = [sys.executable, "-m", "piper", "-m", p.get("voice", "en_US-lessac-medium"),
           "--data-dir", str(PIPER_DIR), "-i", str(txt), "-f", str(out_path),
           "--sentence-silence", str(p.get("sentence_silence", 0.35))]
    if p.get("length_scale"):
        cmd += ["--length-scale", str(p["length_scale"])]
    run(cmd)


def espeak(text, cfg, out_path):
    e = cfg.get("espeak", {})
    run(["espeak-ng", "-v", e.get("voice", "en-us"), "-s", str(e.get("speed", 160)),
         "-w", str(out_path), text])


# --------------------------------------------------------------------------
def make_voiceover(scenes, voice_cfg, pronounce, audio_dir, draft):
    """Returns ({scene_id: audio_path_or_None}, provider)."""
    audio_dir.mkdir(parents=True, exist_ok=True)
    provider = pick_provider(voice_cfg, draft)
    fp = settings_fingerprint(provider, voice_cfg)
    texts = [spoken_text(sc.get("narration") or "", pronounce) for sc in scenes]
    ext = "mp3" if provider == "elevenlabs" else "wav"

    plan, chars = [], 0
    for i, sc in enumerate(scenes):
        if not texts[i]:
            plan.append((sc, None, False))
            continue
        path = audio_dir / f"{sc['id']}-{sha(fp, texts[i])}.{ext}"
        cached = path.exists() and path.stat().st_size > 0
        if not cached:
            chars += len(texts[i])
        plan.append((sc, path, cached))

    label = {"elevenlabs": "ElevenLabs (final voice)", "piper": "Piper (free draft voice)",
             "espeak": "espeak-ng (free robotic draft voice)"}[provider]
    say(f"  voice: {label}")
    if provider == "elevenlabs":
        say(f"  characters to send to ElevenLabs now: {chars:,} "
            f"(cached scenes are free)")

    result = {}
    for i, (sc, path, cached) in enumerate(plan):
        if path is None:
            result[sc["id"]] = None
            continue
        if cached:
            say(f"  [{i + 1}/{len(plan)}] {sc['id']}: unchanged, reusing audio")
        else:
            say(f"  [{i + 1}/{len(plan)}] {sc['id']}: generating...")
            for old in audio_dir.glob(f"{sc['id']}-*.{ext}"):
                old.unlink()
            tmp = path.with_suffix(".part." + ext)
            if provider == "elevenlabs":
                prev_t = texts[i - 1] if i > 0 else ""
                next_t = texts[i + 1] if i + 1 < len(texts) else ""
                eleven(texts[i], prev_t, next_t, voice_cfg, tmp)
            elif provider == "piper":
                piper(texts[i], voice_cfg, tmp, audio_dir)
            else:
                espeak(texts[i], voice_cfg, tmp)
            tmp.rename(path)
        result[sc["id"]] = path
    return result, provider
