"""Build one course module from its module.yaml.

Usually started through ./build.sh:
    ./build.sh 1.2 --check     only check module.yaml for problems
    ./build.sh 1.2 --slides    only make the slides PDF (fast, for reviewing)
    ./build.sh 1.2 --draft     full video with a FREE voice (for reviewing)
    ./build.sh 1.2             full video with the ElevenLabs voice (final)
"""
import argparse
import shutil
import time
from pathlib import Path

from common import (REPO_ROOT, fail, find_module_dir, load_course, load_yaml,
                    output_name, say, step)
from validate import check_module, print_report


def check_approved_narration(mdir, module):
    """If narration_approved.txt exists, the voice text must match it word for word."""
    approved_file = mdir / "narration_approved.txt"
    if not approved_file.exists():
        return
    approved = approved_file.read_text(encoding="utf-8").split()
    spoken = " ".join(str(sc.get("narration") or "") for sc in module["scenes"]).split()
    if spoken == approved:
        say("  narration matches narration_approved.txt word for word")
        return
    i = next((k for k, (a, b) in enumerate(zip(spoken, approved)) if a != b),
             min(len(spoken), len(approved)))
    fail("The narration in module.yaml is different from narration_approved.txt\n"
         f"  approved: ...{' '.join(approved[max(0, i - 6):i + 8])}...\n"
         f"  in yaml:  ...{' '.join(spoken[max(0, i - 6):i + 8])}...\n"
         "Fix module.yaml, or update narration_approved.txt if you approved a new script.")


def main():
    ap = argparse.ArgumentParser(description="Build one course module.")
    ap.add_argument("module", help="module number (e.g. 1.2) or folder name")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="only check module.yaml")
    g.add_argument("--slides", action="store_true", help="only build the slides PDF")
    g.add_argument("--draft", action="store_true", help="full build with a free voice")
    args = ap.parse_args()

    started = time.time()
    mdir = find_module_dir(args.module)
    module = load_yaml(mdir / "module.yaml")
    course = load_course()
    module["_author"] = course.get("course", {}).get("instructor", "")
    name = output_name(module)
    build = mdir / "build"
    work, publish = build / "work", build / "publish"
    total = 1 if args.check else 2 if args.slides else 6

    say(f"=== Building Module {module['module']['number']}: {module['module']['title']} ===")
    step(1, total, "Checking module.yaml")
    if not print_report(check_module(module), "module.yaml"):
        fail("Fix the problems above, then run the build again.")
    check_approved_narration(mdir, module)
    if args.check:
        return

    import slides
    scenes = module["scenes"]
    slide_scenes = [sc for sc in scenes if sc.get("slide")]
    publish.mkdir(parents=True, exist_ok=True)
    pdf = publish / f"{name}_Slides.pdf"

    step(2, total, f"Making {len(slide_scenes)} slides")
    pngs = slides.build_slides(module, pdf, None if args.slides else work / "slides", slide_scenes)
    say(f"  saved {pdf.relative_to(REPO_ROOT)}")
    if args.slides:
        say(f"\nDone in {time.time() - started:.0f}s. Open the PDF to review the slides.")
        return

    import extras
    import tapes
    import video
    import voice

    step(3, total, "Recording terminal demos with VHS")
    clips = tapes.record_demos(scenes, course.get("terminal", {}), work / "demos")
    if not clips:
        say("  (this module has no terminal demos)")

    visuals, png_iter = {}, iter(pngs)
    for sc in scenes:
        png = next(png_iter) if sc.get("slide") else None
        visuals[sc["id"]] = ("clip", clips[sc["id"]]) if sc["id"] in clips else ("image", png)

    step(4, total, "Making the voiceover")
    pronounce = dict(course.get("pronounce") or {})
    pronounce.update(module.get("pronounce") or {})
    audios, provider = voice.make_voiceover(scenes, course.get("voice", {}), pronounce,
                                            work / "audio", args.draft)

    step(5, total, "Putting the video together")
    suffix = "DRAFT" if args.draft else "Final"
    out_video = publish / f"{name}_{suffix}.mp4"
    srt, vtt = publish / f"{name}_Captions.srt", publish / f"{name}_Captions.vtt"
    vcfg = course.get("video", {})
    avatar = vcfg.get("avatar")
    length = video.assemble(scenes, visuals, audios, vcfg, work, out_video, srt, vtt,
                            REPO_ROOT / avatar if avatar else None)

    step(6, total, "Writing quiz, narration script and Killercoda lab")
    quiz = publish / f"{name}_Quiz.md"
    script = publish / f"{name}_Narration.txt"
    extras.write_quiz(module, quiz)
    extras.write_script(module, script)
    kc_dir = publish / "killercoda"
    if kc_dir.exists():
        shutil.rmtree(kc_dir)
    lab_dir = extras.write_killercoda(module, kc_dir)
    files = [("lesson video (LMS)", out_video), ("student download (LMS)", pdf),
             ("subtitles (LMS / YouTube)", srt), ("subtitles, web format", vtt),
             ("quiz questions (LMS quiz builder)", quiz),
             ("script you can read along", script),
             ("Killercoda lab folder (GitHub)", lab_dir)]
    extras.write_publish_readme(module, publish / "README.txt", files, provider)

    mins, secs = divmod(int(length), 60)
    say(f"\n=== DONE in {time.time() - started:.0f}s - video length {mins}m{secs:02d}s ===")
    say(f"Your files are in: {publish.relative_to(REPO_ROOT)}/")
    for _, f in files:
        say(f"  - {f.name}")
    if args.draft:
        say(f"\nThis is a DRAFT with a free voice. When you are happy, run:  ./build.sh {module['module']['number']}")


if __name__ == "__main__":
    main()
