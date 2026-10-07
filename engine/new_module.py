"""./new-module.sh 1.3 ["Title"] -> module folder + filled-in prompt on the clipboard."""
import re
import sys

import clipboard
from common import MODULES_DIR, REPO_ROOT, fail, load_course, say

EXAMPLE_MODULE = MODULES_DIR / "module-1.2-dns-ttl-caching" / "module.yaml"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40].strip("-")


def example_yaml():
    """Approved Module 1.2 file without the review notes and the header box."""
    lines = EXAMPLE_MODULE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("module:"))
    keep = [ln for ln in lines[start:] if not re.match(r"\s*# (NEW|CHANGED)\b", ln)]
    return "\n".join(keep).rstrip() + "\n"


def main():
    if len(sys.argv) < 2:
        fail('Usage: ./new-module.sh 1.3 ["Module title"] ["notes for the AI"]')
    number = sys.argv[1].strip()
    if not re.fullmatch(r"\d+(\.\d+)*", number):
        fail(f"'{number}' is not a module number like 1.3")
    course = load_course()
    outline = course.get("outline") or []
    by_num = {str(o["number"]): o["title"] for o in outline}
    given = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    title = given or by_num.get(number)
    if not title:
        fail(f"Module {number} is not in course.yaml -> outline. Either add it there, or give the title:\n"
             f'  ./new-module.sh {number} "Your module title"')
    notes = sys.argv[3] if len(sys.argv) > 3 else "(none)"

    nums = [str(o["number"]) for o in outline]
    prev_txt = next_txt = "(none - this is the first/last module)"
    if number in nums:
        i = nums.index(number)
        if i > 0:
            prev_txt = f"Module {nums[i - 1]} - {by_num[nums[i - 1]]}"
        if i + 1 < len(nums):
            next_txt = f"Module {nums[i + 1]} - {by_num[nums[i + 1]]}"

    existing = sorted(MODULES_DIR.glob(f"module-{number}-*"))
    folder = existing[0] if existing else MODULES_DIR / f"module-{number}-{slugify(title)}"
    folder.mkdir(parents=True, exist_ok=True)

    c = course.get("course", {})
    prompt = (REPO_ROOT / "prompts" / "module_prompt.md").read_text(encoding="utf-8")
    prompt = prompt.split("\n---\n", 1)[1].lstrip()          # drop the "how to use" box
    values = {"COURSE_TITLE": c.get("title", ""), "AUDIENCE": c.get("audience", ""),
              "CONTEXT": c.get("context", ""), "NUMBER": number, "TITLE": title,
              "PREVIOUS": prev_txt, "NEXT": next_txt, "NOTES": notes,
              "EXAMPLE": example_yaml().rstrip("\n")}
    for k, v in values.items():
        prompt = prompt.replace("{{" + k + "}}", str(v))
    (folder / "prompt.md").write_text(prompt, encoding="utf-8")
    rel = folder.relative_to(REPO_ROOT)

    if not (folder / "module.yaml").exists():
        (folder / "module.yaml").write_text(
            "# Paste the AI's YAML answer here, or run: ./paste-module.sh " + number + "\n",
            encoding="utf-8")

    copied = clipboard.copy(prompt)
    say(f"\nModule {number}: {title}")
    say(f"Folder ready:  {rel}/")
    say(f"Prompt saved:  {rel}/prompt.md")
    if copied:
        say("\nThe prompt is on your clipboard. Next:")
        say("  1. Open your AI chat (Gemini / Claude / ChatGPT), start a NEW chat, press Ctrl+V, send.")
    else:
        say("\nCould not copy to the clipboard automatically. Next:")
        say(f"  1. Open {rel}/prompt.md, select all, copy, paste into a NEW AI chat and send.")
    say("  2. When the answer is finished, click its Copy button.")
    say(f"  3. Run:  ./paste-module.sh {number}")


if __name__ == "__main__":
    main()
