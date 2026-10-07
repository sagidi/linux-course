"""Check a module.yaml before building.

Catches the common problems in AI-generated files *before* any time or
ElevenLabs credits are spent: missing fields, text too long to fit on a
slide, demo commands that would hang the terminal recorder, and quiz
answers that do not exist.

Run on its own:  ./build.sh 1.2 --check
"""
import re
import sys

from common import strip_markup

SLIDE_TYPES = {"title", "two_columns", "table", "diagram", "panel",
               "terminal", "quiz", "lab"}

# Commands that wait for a key press or never exit -> the recording hangs.
HANGING = [
    (r"^\s*(vi|vim|nano|less|more|man|top|htop|watch)\b", "opens an interactive screen"),
    (r"\bping\b(?!.*\s-c\s*\d)", "ping runs forever - add -c 3"),
    (r"\btail\s+(-\w*f|--follow)", "tail -f never exits"),
    (r"\bjournalctl\b.*\s(-f|--follow)\b", "journalctl -f never exits"),
    (r"\bjournalctl\b(?!.*(--no-pager|\|))", "add --no-pager (or pipe to head) so it does not wait for a key"),
    (r"\bsystemctl\s+status\b(?!.*(--no-pager|\|))", "add --no-pager so it does not wait for a key"),
]
DANGEROUS = [
    (r"\brm\s+-\w*r\w*f?\s+/(\s|$)", "deletes the whole filesystem"),
    (r"\bmkfs\b|\bdd\s+if=", "can destroy a disk"),
    (r"\bsudo\b", "needs a password - the recorder cannot type it (use files in /tmp instead)"),
    (r"\breboot\b|\bshutdown\b", "restarts the machine"),
]


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def _text(r, where, value, max_len, required=True):
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            r.err(where, "is missing or empty")
        return
    if not isinstance(value, (str, int, float)):
        r.err(where, f"must be text, got {type(value).__name__}")
        return
    plain = strip_markup(value)
    if len(plain) > max_len:
        r.err(where, f"is {len(plain)} characters - keep it under {max_len} so it fits on the slide")
    if any(ord(ch) > 0xFFFF for ch in plain):
        r.warn(where, "contains emoji - slides cannot show them, they will be removed")


def _list(r, where, value, lo, hi, required=True):
    if value is None:
        if required:
            r.err(where, "is missing")
        return []
    if not isinstance(value, list):
        r.err(where, "must be a list (lines starting with '- ')")
        return []
    if not lo <= len(value) <= hi:
        r.err(where, f"has {len(value)} items - use {lo} to {hi}")
    return value


def _lines(value):
    if isinstance(value, list):
        return [str(v) for v in value]
    return str(value or "").rstrip("\n").split("\n")


def check_slide(r, where, s, module):
    t = s.get("type")
    if t not in SLIDE_TYPES:
        r.err(where, f"type '{t}' is unknown - use one of: {', '.join(sorted(SLIDE_TYPES))}")
        return
    if t != "title":
        _text(r, f"{where}.number", s.get("number"), 12)
        _text(r, f"{where}.title", s.get("title"), 80)
        _text(r, f"{where}.subtitle", s.get("subtitle"), 150)

    if t == "two_columns":
        for side in ("left", "right"):
            p = s.get(side)
            w = f"{where}.{side}"
            if not isinstance(p, dict):
                r.err(w, "is missing")
                continue
            _text(r, f"{w}.heading", p.get("heading"), 50)
            _text(r, f"{w}.text", p.get("text"), 260, required=False)
            _text(r, f"{w}.example", p.get("example"), 50, required=False)
            for i, b in enumerate(_list(r, f"{w}.bullets", p.get("bullets"), 1, 5, required=False)):
                _text(r, f"{w}.bullets[{i + 1}]", b, 140)
            for i, ln in enumerate(_lines(p.get("code")) if p.get("code") else []):
                if len(strip_markup(ln)) > 46:
                    r.err(f"{w}.code line {i + 1}", "is longer than 46 characters")
            if not (p.get("text") or p.get("bullets") or p.get("code")):
                r.err(w, "needs at least one of: text, bullets, code")

    elif t == "table":
        cols = _list(r, f"{where}.columns", s.get("columns"), 2, 4)
        widths = s.get("widths")
        if widths is not None and (not isinstance(widths, list) or len(widths) != len(cols)):
            r.err(f"{where}.widths", "must have one number per column")
        for i, row in enumerate(_list(r, f"{where}.rows", s.get("rows"), 1, 6)):
            if not isinstance(row, list) or len(row) != len(cols):
                r.err(f"{where}.rows[{i + 1}]", f"must have exactly {len(cols)} cells")
                continue
            for j, cell in enumerate(row):
                _text(r, f"{where}.rows[{i + 1}][{j + 1}]", cell, 200)

    elif t == "diagram":
        _text(r, f"{where}.heading", s.get("heading"), 80, required=False)
        for i, ln in enumerate(_list(r, f"{where}.lines", _lines(s.get("lines")) if s.get("lines") else None, 1, 9)):
            if len(strip_markup(ln)) > 92:
                r.err(f"{where}.lines[{i + 1}]", "is longer than 92 characters")
        for i, b in enumerate(_list(r, f"{where}.takeaways", s.get("takeaways"), 0, 3, required=False)):
            _text(r, f"{where}.takeaways[{i + 1}]", b, 170)

    elif t == "panel":
        _text(r, f"{where}.heading", s.get("heading"), 70)
        _text(r, f"{where}.text", s.get("text"), 420, required=False)
        _text(r, f"{where}.subheading", s.get("subheading"), 70, required=False)
        for i, b in enumerate(_list(r, f"{where}.bullets", s.get("bullets"), 0, 5, required=False)):
            _text(r, f"{where}.bullets[{i + 1}]", b, 170)

    elif t == "terminal":
        panels = _list(r, f"{where}.panels", s.get("panels"), 1, 2)
        max_line = 92 if len(panels) == 1 else 44
        for i, p in enumerate(panels):
            w = f"{where}.panels[{i + 1}]"
            if not isinstance(p, dict):
                r.err(w, "must have heading and lines")
                continue
            _text(r, f"{w}.heading", p.get("heading"), 60)
            lines = _lines(p.get("lines"))
            if not 1 <= len(lines) <= 11:
                r.err(f"{w}.lines", f"has {len(lines)} lines - use 1 to 11")
            for k, ln in enumerate(lines):
                if len(strip_markup(ln)) > max_line:
                    r.err(f"{w}.lines line {k + 1}", f"is longer than {max_line} characters")
        for i, b in enumerate(_list(r, f"{where}.takeaways", s.get("takeaways"), 0, 3, required=False)):
            _text(r, f"{where}.takeaways[{i + 1}]", b, 170)
        _text(r, f"{where}.note", s.get("note"), 260, required=False)

    elif t == "quiz":
        idx = s.get("question", 1)
        if not isinstance(idx, int) or not 1 <= idx <= len(module.get("quiz") or []):
            r.err(f"{where}.question", "must point to a question number in the quiz section")

    elif t == "lab":
        for i, b in enumerate(_list(r, f"{where}.steps", s.get("steps"), 0, 6, required=False)):
            _text(r, f"{where}.steps[{i + 1}]", b, 150)
        _text(r, f"{where}.next_text", s.get("next_text"), 300, required=False)


def check_demo(r, where, d):
    if not isinstance(d, dict):
        r.err(where, "must have a 'commands' list")
        return
    for i, c in enumerate(_list(r, f"{where}.commands", d.get("commands"), 1, 6)):
        w = f"{where}.commands[{i + 1}]"
        if not isinstance(c, dict) or not str(c.get("run", "")).strip():
            r.err(w, "needs a 'run' command")
            continue
        for field in ("comment", "run"):
            val = str(c.get(field) or "")
            if val and all(q in val for q in ('"', "'", "`")):
                r.err(f"{w}.{field}", "uses \", ' and ` together - the recorder can only type text that avoids one of them")
        if c.get("comment") and not str(c["comment"]).startswith("#"):
            r.err(f"{w}.comment", "must start with '#'")
        cmd = str(c["run"])
        for pat, why in HANGING:
            if re.search(pat, cmd):
                r.err(w, f"'{cmd}' {why}")
        for pat, why in DANGEROUS:
            if re.search(pat, cmd):
                r.err(w, f"'{cmd}' {why}")
        wait = c.get("wait", 5)
        if not isinstance(wait, (int, float)) or not 1 <= wait <= 20:
            r.err(f"{w}.wait", "must be a number of seconds between 1 and 20")
    for ln in _lines(d.get("setup")) if d.get("setup") else []:
        for pat, why in DANGEROUS:
            if re.search(pat, ln):
                r.err(f"{where}.setup", f"'{ln}' {why}")


def check_module(m):
    r = Report()
    info = m.get("module")
    if not isinstance(info, dict):
        r.err("module", "section is missing")
        return r
    num = str(info.get("number", ""))
    if not re.fullmatch(r"\d+(\.\d+)*", num):
        r.err("module.number", f"'{num}' must look like 1.2 (and be in quotes)")
    _text(r, "module.label", info.get("label"), 60)
    _text(r, "module.title", info.get("title"), 60)
    _text(r, "module.subtitle", info.get("subtitle"), 170)
    for i, box in enumerate(_list(r, "module.info", info.get("info"), 1, 3)):
        if not isinstance(box, dict):
            r.err(f"module.info[{i + 1}]", "needs heading and text")
            continue
        _text(r, f"module.info[{i + 1}].heading", box.get("heading"), 30)
        _text(r, f"module.info[{i + 1}].text", box.get("text"), 90)
    nxt = info.get("next")
    if nxt is not None and not (isinstance(nxt, dict) and nxt.get("number") and nxt.get("title")):
        r.err("module.next", "needs number and title")

    scenes = _list(r, "scenes", m.get("scenes"), 3, 20)
    ids, total_words = set(), 0
    for i, sc in enumerate(scenes):
        where = f"scene {i + 1}"
        if not isinstance(sc, dict):
            r.err(where, "must be a mapping with id, slide/demo and narration")
            continue
        sid = sc.get("id")
        if not sid or not re.fullmatch(r"[a-z0-9-]+", str(sid)):
            r.err(f"{where}.id", "must be lowercase letters, numbers and dashes")
        elif sid in ids:
            r.err(f"{where}.id", f"'{sid}' is used twice")
        ids.add(sid)
        where = f"scene '{sid or i + 1}'"
        if not sc.get("slide") and not sc.get("demo"):
            r.err(where, "needs a slide, a demo, or both")
        if sc.get("slide"):
            check_slide(r, f"{where}.slide", sc["slide"], m)
        if sc.get("demo"):
            check_demo(r, f"{where}.demo", sc["demo"])
        narr = str(sc.get("narration") or "").strip()
        words = len(narr.split())
        total_words += words
        if not narr and not sc.get("hold"):
            r.err(f"{where}.narration", "is missing (or set 'hold: 5' for a silent scene)")
        if words > 220:
            r.warn(f"{where}.narration", f"is {words} words (~{words // 150 + 1} min) - consider splitting the scene")
        if re.search(r"[<>]|\*\*|`|\[/?(red|orange|green|blue|muted)\]", narr):
            r.err(f"{where}.narration", "must be plain spoken text - remove markup, backticks and < > tags")

    minutes = total_words / 150
    if total_words and not 2 <= minutes <= 8:
        r.warn("narration", f"totals {total_words} words (~{minutes:.1f} min). Target is 3-5 minutes.")

    letters = "ABCDE"
    for i, q in enumerate(_list(r, "quiz", m.get("quiz"), 1, 5)):
        w = f"quiz[{i + 1}]"
        if not isinstance(q, dict):
            r.err(w, "needs question, options, answer, explanation")
            continue
        _text(r, f"{w}.question", q.get("question"), 200)
        opts = _list(r, f"{w}.options", q.get("options"), 2, 5)
        ans = str(q.get("answer", "")).strip().upper()
        if ans not in letters[:len(opts)]:
            r.err(f"{w}.answer", f"'{ans}' must be one of {', '.join(letters[:len(opts)])}")
        _text(r, f"{w}.explanation", q.get("explanation"), 320)
        _text(r, f"{w}.tip", q.get("tip"), 220, required=False)

    lab = m.get("lab")
    if not isinstance(lab, dict):
        r.err("lab", "section is missing")
    else:
        _text(r, "lab.title", lab.get("title"), 80)
        _text(r, "lab.intro", lab.get("intro"), 600)
        for i, st in enumerate(_list(r, "lab.steps", lab.get("steps"), 1, 8)):
            w = f"lab.steps[{i + 1}]"
            if not isinstance(st, dict):
                r.err(w, "needs title and text")
                continue
            _text(r, f"{w}.title", st.get("title"), 80)
            _text(r, f"{w}.text", st.get("text"), 800)
            if st.get("commands") is not None and not isinstance(st.get("commands"), list):
                r.err(f"{w}.commands", "must be a list")
        _text(r, "lab.finish", lab.get("finish"), 600)
    return r


def print_report(r, name):
    for w in r.warnings:
        print(f"  WARNING  {w}")
    for e in r.errors:
        print(f"  PROBLEM  {e}")
    if r.errors:
        print(f"\n{name}: {len(r.errors)} problem(s) to fix, {len(r.warnings)} warning(s).")
        print("Fix them in module.yaml (or ask the AI to fix them), then run the check again.")
    else:
        print(f"{name}: OK ({len(r.warnings)} warning(s)).")
    return not r.errors


if __name__ == "__main__":
    from common import find_module_dir, load_yaml
    d = find_module_dir(sys.argv[1])
    ok = print_report(check_module(load_yaml(d / "module.yaml")), d.name)
    sys.exit(0 if ok else 1)
