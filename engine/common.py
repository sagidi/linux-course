"""Shared helpers for the course build engine.

Every other engine file imports from here: paths, config loading,
running shell commands, measuring media duration, and the small
text markup used inside module.yaml.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"


# --------------------------------------------------------------------------
# Friendly console output
# --------------------------------------------------------------------------
def say(msg):
    print(msg, flush=True)


def step(n, total, msg):
    say(f"\n[{n}/{total}] {msg}")


def fail(msg):
    """Stop the build with a clear message (no Python stack trace)."""
    print(f"\nERROR: {msg}\n", file=sys.stderr, flush=True)
    sys.exit(1)


# --------------------------------------------------------------------------
# Config + module loading
# --------------------------------------------------------------------------
def load_yaml(path):
    path = Path(path)
    if not path.exists():
        fail(f"File not found: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(f"{path} is not valid YAML.\n{e}\n\nTip: text that contains a colon "
             f"(:) must be inside quotes, or use a block with '|'.")
    if not isinstance(data, dict):
        fail(f"{path} is empty or not a YAML mapping.")
    return data


def load_course():
    return load_yaml(REPO_ROOT / "course.yaml")


def find_module_dir(arg):
    """Accept '1.2', 'module-1.2-dns-ttl-caching' or a path."""
    p = Path(arg)
    if p.is_dir() and (p / "module.yaml").exists():
        return p.resolve()
    if (MODULES_DIR / arg).is_dir():
        return (MODULES_DIR / arg).resolve()
    matches = sorted(MODULES_DIR.glob(f"module-{arg}-*"))
    if len(matches) == 1:
        return matches[0].resolve()
    if len(matches) > 1:
        fail(f"More than one folder matches module {arg}: "
             + ", ".join(m.name for m in matches))
    fail(f"Cannot find module '{arg}'. Folders in modules/: "
         + ", ".join(sorted(d.name for d in MODULES_DIR.iterdir() if d.is_dir())))


def output_name(module):
    """'1.2' -> 'Module_1_2'"""
    return "Module_" + str(module["module"]["number"]).replace(".", "_")


# --------------------------------------------------------------------------
# Running tools
# --------------------------------------------------------------------------
def need(tool, hint):
    if shutil.which(tool) is None:
        fail(f"'{tool}' is not installed. {hint}")


def run(cmd, cwd=None, env=None, quiet=True):
    """Run a command; on failure show its output and stop."""
    res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=quiet, text=True)
    if res.returncode != 0:
        out = ((res.stdout or "") + (res.stderr or "")).strip()
        fail(f"Command failed: {' '.join(str(c) for c in cmd)}\n{out[-3000:]}")
    return res


def media_duration(path):
    res = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "json", str(path)])
    return float(json.loads(res.stdout)["format"]["duration"])


def sha(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------
# Text markup used in module.yaml
#   **bold**   `code`   [red]text[/red]  (red, orange, green, blue, muted)
#   A new line in the YAML text becomes a line break on the slide.
# --------------------------------------------------------------------------
COLORS = {
    "navy": "#0F172A",
    "module": "#0369A1",
    "blue": "#38BDF8",
    "red": "#F43F5E",
    "orange": "#F59E0B",
    "green": "#10B981",
    "text": "#334155",
    "muted": "#64748B",
    "bg": "#F8FAFC",
    "code_bg": "#020617",
    "border": "#CBD5E1",
    "lavender_bg": "#EEF2FF",
    "lavender": "#818CF8",
    "mint_bg": "#ECFDF5",
    "white": "#FFFFFF",
}
TAG_COLORS = ["red", "orange", "green", "blue", "muted"]
_TAG_RE = re.compile(r"\[(/?)(" + "|".join(TAG_COLORS) + r")\]")


def strip_markup(text):
    """Plain text version (for narration checks, captions, quiz.md)."""
    text = _TAG_RE.sub("", str(text))
    return text.replace("**", "").replace("`", "")


def to_markdown(text):
    """module.yaml markup -> GitHub markdown (drops colour tags)."""
    return _TAG_RE.sub("", str(text))
