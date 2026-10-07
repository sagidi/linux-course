"""Slides + terminal clips + narration -> one finished lesson video + captions.

How sync works (no manual editing):
  every scene = one picture (slide image or terminal clip) + its narration.
  The scene lasts as long as its narration (plus a short pause).
  - slide scene:    the slide is shown for exactly that long
  - terminal scene: the clip plays; if the voice is longer, the last frame
                    is held; if the clip is longer, the voice is followed by silence
Scenes are then joined in order.
"""
import re
from pathlib import Path

from common import media_duration, run, say, strip_markup


def _fmt(t, sep):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def make_avatar(src, dst, size):
    """Square photo -> round badge with a white ring (PNG with transparency)."""
    from PIL import Image, ImageDraw, ImageOps
    img = ImageOps.fit(Image.open(src).convert("RGBA"), (size, size))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    ring = 6
    out = Image.new("RGBA", (size + 2 * ring, size + 2 * ring), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse((0, 0, size + 2 * ring - 1, size + 2 * ring - 1),
                                fill=(255, 255, 255, 255))
    out.paste(img, (ring, ring), mask)
    out.save(dst)
    return dst


def encode_segment(visual, audio, duration, clip_len, vcfg, avatar, out):
    W, H, fps = int(vcfg.get("width", 1920)), int(vcfg.get("height", 1080)), int(vcfg.get("fps", 30))
    kind, path = visual
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if kind == "image":
        cmd += ["-loop", "1", "-framerate", str(fps), "-i", str(path)]
        pad_color = "white"
        hold = ""
    else:
        cmd += ["-i", str(path)]
        pad_color = "0x24273A"
        extra = max(0.0, duration - clip_len)
        hold = f",tpad=stop_mode=clone:stop_duration={extra:.3f}" if extra > 0 else ""
    if audio:
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    if avatar:
        cmd += ["-i", str(avatar)]

    v = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,"
         f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={pad_color},fps={fps},setsar=1{hold}")
    if avatar:
        margin = 36
        pos = {"bottom-right": f"W-w-{margin}:H-h-{margin}", "top-right": f"W-w-{margin}:{margin}",
               "bottom-left": f"{margin}:H-h-{margin}", "top-left": f"{margin}:{margin}"
               }.get(vcfg.get("avatar_position", "bottom-right"), f"W-w-{margin}:H-h-{margin}")
        v += f"[base];[base][2:v]overlay={pos}"
    v += ",format=yuv420p[v]"
    a = "[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
    cmd += ["-filter_complex", f"{v};{a}", "-map", "[v]", "-map", "[a]",
            "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-preset", vcfg.get("preset", "medium"), "-crf", str(vcfg.get("crf", 18)),
            "-r", str(fps), "-g", str(fps * 2), "-video_track_timescale", "90000",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            str(out)]
    if kind == "image":
        cmd.insert(cmd.index("-c:v"), "-tune")
        cmd.insert(cmd.index("-c:v"), "stillimage")
    run(cmd)


def split_captions(text, max_len=84):
    """Narration -> short caption chunks (sentence first, then by words)."""
    text = " ".join(strip_markup(text).split())
    chunks = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words, cur = sentence.split(), ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > max_len:
                chunks.append(cur)
                cur = w
            else:
                cur = f"{cur} {w}".strip()
        if cur:
            chunks.append(cur)
    return chunks


def two_lines(chunk, width=42):
    if len(chunk) <= width:
        return chunk
    words, best = chunk.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = abs(len(a) - len(b))
        if best is None or score < best[0]:
            best = (score, a, b)
    return f"{best[1]}\n{best[2]}"


def write_captions(cues, srt_path, vtt_path):
    srt, vtt = [], ["WEBVTT", ""]
    for i, (start, end, text) in enumerate(cues, 1):
        srt += [str(i), f"{_fmt(start, ',')} --> {_fmt(end, ',')}", text, ""]
        vtt += [f"{_fmt(start, '.')} --> {_fmt(end, '.')}", text, ""]
    Path(srt_path).write_text("\n".join(srt), encoding="utf-8")
    Path(vtt_path).write_text("\n".join(vtt), encoding="utf-8")


def assemble(scenes, visuals, audios, vcfg, work_dir, out_video, srt_path, vtt_path, avatar_src):
    seg_dir = work_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    for old in seg_dir.glob("*.mp4"):
        old.unlink()

    avatar = None
    if avatar_src and Path(avatar_src).exists():
        avatar = make_avatar(avatar_src, work_dir / "avatar_round.png", int(vcfg.get("avatar_size", 200)))
        say("  instructor photo found - adding it in the corner")

    gap = float(vcfg.get("scene_gap", 0.8))
    t, cues, segs = 0.0, [], []
    for i, sc in enumerate(scenes):
        audio = audios.get(sc["id"])
        a_len = media_duration(audio) if audio else 0.0
        kind, path = visuals[sc["id"]]
        clip_len = media_duration(path) if kind == "clip" else 0.0
        duration = max(a_len + gap, clip_len, float(sc.get("hold", 0) or 0), 1.0)
        seg = seg_dir / f"{i + 1:02d}-{sc['id']}.mp4"
        say(f"  [{i + 1}/{len(scenes)}] {sc['id']}: {duration:5.1f}s "
            f"({'terminal demo' if kind == 'clip' else 'slide'})")
        encode_segment((kind, path), audio, duration, clip_len, vcfg, avatar, seg)
        segs.append(seg)

        chunks = split_captions(sc.get("narration") or "")
        total_chars = sum(len(c) for c in chunks) or 1
        c_t = t
        for c in chunks:
            d = a_len * len(c) / total_chars
            cues.append((c_t, c_t + d, two_lines(c)))
            c_t += d
        t += media_duration(seg)

    lst = work_dir / "segments.txt"
    lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs), encoding="utf-8")
    joined = work_dir / "joined.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", "-movflags", "+faststart", str(joined)])
    write_captions(cues, srt_path, vtt_path)

    if vcfg.get("burn_captions"):
        say("  burning captions into the video...")
        style = "FontName=DejaVu Sans,FontSize=20,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=4,MarginV=40"
        srt_esc = str(Path(srt_path).resolve()).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(joined),
             "-vf", f"subtitles='{srt_esc}':force_style='{style}'",
             "-c:v", "libx264", "-crf", str(vcfg.get("crf", 18)), "-preset", vcfg.get("preset", "medium"),
             "-c:a", "copy", "-movflags", "+faststart", str(out_video)])
        joined.unlink()
    else:
        joined.replace(out_video)
    return t
