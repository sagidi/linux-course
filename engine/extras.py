"""Copy-paste-ready files for publishing: quiz, narration script, Killercoda lab."""
import json
import re
import shutil

from common import strip_markup, to_markdown

LETTERS = "ABCDE"


def write_quiz(module, path):
    m = module["module"]
    out = [f"# Quiz - Module {m['number']}: {m['title']}", "",
           "Copy each question into your course platform's quiz builder.",
           "Paste the **Feedback** text into the 'explanation' / 'feedback' box.", ""]
    for i, q in enumerate(module["quiz"], 1):
        ans = str(q["answer"]).strip().upper()
        out += [f"## Question {i}" + (f" - {to_markdown(q['topic'])}" if q.get("topic") else ""), "",
                to_markdown(q["question"]), ""]
        for j, o in enumerate(q["options"]):
            mark = "  <-- correct" if LETTERS[j] == ans else ""
            out.append(f"- {LETTERS[j]}) {to_markdown(o)}{mark}")
        out += ["", f"**Correct answer:** {ans}", "",
                f"**Feedback:** {to_markdown(q['explanation'])}"]
        if q.get("tip"):
            out += ["", f"**Pro-tip:** {to_markdown(q['tip'])}"]
        out += ["", "---", ""]
    path.write_text("\n".join(out), encoding="utf-8")


def write_script(module, path):
    m = module["module"]
    out = [f"MODULE {m['number']}: {m['title']} - NARRATION SCRIPT", "=" * 60, ""]
    words = 0
    for i, sc in enumerate(module["scenes"], 1):
        text = " ".join(str(sc.get("narration") or "").split())
        words += len(text.split())
        out += [f"[Scene {i}: {sc['id']}]", text or "(silent)", ""]
    out += [f"Total: {words} words, about {words / 150:.1f} minutes of speech."]
    path.write_text("\n".join(out), encoding="utf-8")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def write_killercoda(module, out_dir):
    """Creates a Killercoda scenario folder (index.json + markdown + scripts)."""
    lab = module["lab"]
    m = module["module"]
    name = f"module-{m['number'].replace('.', '-')}-{slug(lab['title'])}"
    root = out_dir / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)

    (root / "intro.md").write_text(to_markdown(lab["intro"]).strip() + "\n", encoding="utf-8")
    (root / "finish.md").write_text(to_markdown(lab["finish"]).strip() + "\n", encoding="utf-8")
    setup = lab.get("setup") or ""
    (root / "setup.sh").write_text("#!/bin/bash\n# Runs in the background when the lab starts.\n"
                                   + setup.strip() + "\n", encoding="utf-8")

    steps = []
    for i, st in enumerate(lab["steps"], 1):
        d = root / f"step{i}"
        d.mkdir()
        body = [f"### {to_markdown(st['title'])}", "", to_markdown(st["text"]).strip(), ""]
        for c in st.get("commands") or []:
            body += ["```plain", str(c), "```{{exec}}", ""]
        if st.get("verify"):
            body += ["When you are done, click **Check**."]
        (d / "text.md").write_text("\n".join(body) + "\n", encoding="utf-8")
        entry = {"title": strip_markup(st["title"]), "text": f"step{i}/text.md"}
        if st.get("verify"):
            (d / "verify.sh").write_text("#!/bin/bash\nset -e\n" + str(st["verify"]).strip()
                                         + "\necho done\n", encoding="utf-8")
            entry["verify"] = f"step{i}/verify.sh"
        steps.append(entry)

    index = {
        "title": f"Module {m['number']}: {strip_markup(lab['title'])}",
        "description": strip_markup(m["subtitle"]),
        "details": {
            "intro": {"text": "intro.md", "background": "setup.sh"},
            "steps": steps,
            "finish": {"text": "finish.md"},
        },
        "backend": {"imageid": lab.get("image", "ubuntu")},
    }
    (root / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return root


def write_publish_readme(module, path, files, provider):
    m = module["module"]
    draft = provider != "elevenlabs"
    out = [f"MODULE {m['number']}: {m['title']}", "=" * 60, ""]
    if draft:
        out += ["THIS IS A DRAFT (free voice). Review it, then run the final build:",
                f"    ./build.sh {m['number']}", ""]
    out += ["What to upload where (full guide: docs/08-publish-the-module.md):", ""]
    for label, f in files:
        out.append(f"  {f.name:<38} -> {label}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
