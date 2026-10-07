"""./paste-module.sh 1.3 [--file answer.txt] -> saves the AI answer as module.yaml and checks it."""
import re
import sys
import time

import yaml

import clipboard
from common import MODULES_DIR, REPO_ROOT, fail, say
from validate import check_module, print_report


def extract_yaml(text):
    """Keep only the YAML: the ```yaml block if there is one, else everything."""
    blocks = re.findall(r"```(?:ya?ml)?[ \t]*\n(.*?)\n```", text, flags=re.S)
    if blocks:
        return max(blocks, key=len).strip() + "\n"
    return text.strip() + "\n"


def main():
    args = sys.argv[1:]
    if not args:
        fail("Usage: ./paste-module.sh 1.3   (or: ./paste-module.sh 1.3 --file answer.txt)")
    number = args[0]
    folders = sorted(MODULES_DIR.glob(f"module-{number}-*"))
    if not folders:
        fail(f"No folder for module {number}. Run ./new-module.sh {number} first.")
    folder = folders[0]

    if "--file" in args:
        i = args.index("--file")
        if i + 1 >= len(args):
            fail("Give the file name after --file")
        text = open(args[i + 1], encoding="utf-8").read()
    else:
        text = clipboard.paste()
        if text is None:
            fail("Cannot read the clipboard here. Save the AI answer to a file and run:\n"
                 f"  ./paste-module.sh {number} --file answer.txt")
    if not text.strip():
        fail("The clipboard is empty. In the AI chat, click Copy on the answer, then run this again.")

    content = extract_yaml(text)
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        fail(f"The AI answer is not valid YAML:\n{e}\n\n"
             "Ask the AI: 'Your YAML has a syntax error at the line above. Send the full corrected file.'")
    if not isinstance(data, dict) or "scenes" not in data:
        fail("That does not look like a module.yaml (no 'scenes' section). Did you copy the right answer?")

    target = folder / "module.yaml"
    if target.exists() and "scenes:" in target.read_text(encoding="utf-8"):
        backup = folder / f"module.yaml.bak-{time.strftime('%Y%m%d-%H%M%S')}"
        backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        say(f"Old version backed up as {backup.name}")
    target.write_text(content, encoding="utf-8")
    say(f"Saved {target.relative_to(REPO_ROOT)}\n")

    ok = print_report(check_module(data), "module.yaml")
    if ok:
        say(f"\nNext: review it (docs/06-review-the-module.md), then:  ./build.sh {number} --slides")
    else:
        say("\nTip: copy the PROBLEM lines above into the same AI chat and ask it to send the full corrected file,")
        say(f"then run ./paste-module.sh {number} again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
