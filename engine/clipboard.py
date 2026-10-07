"""Copy/paste between WSL (or Linux/Mac) and the system clipboard."""
import os
import shutil
import subprocess
import tempfile


def _is_wsl():
    try:
        return "microsoft" in open("/proc/version").read().lower()
    except OSError:
        return False


def copy(text):
    """Returns True if the text is now on the clipboard."""
    try:
        if _is_wsl() and shutil.which("powershell.exe"):
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write(text)
            win = subprocess.run(["wslpath", "-w", f.name], capture_output=True, text=True).stdout.strip()
            r = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                                f"Set-Clipboard -Value (Get-Content -Raw -Encoding UTF8 '{win}')"],
                               capture_output=True)
            os.unlink(f.name)
            return r.returncode == 0
        for cmd in (["pbcopy"], ["wl-copy"], ["xclip", "-selection", "clipboard"]):
            if shutil.which(cmd[0]):
                return subprocess.run(cmd, input=text.encode("utf-8")).returncode == 0
    except OSError:
        pass
    return False


def paste():
    """Returns the clipboard text, or None if it cannot be read."""
    try:
        if _is_wsl() and shutil.which("powershell.exe"):
            r = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                                "[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-Clipboard -Raw"],
                               capture_output=True)
            if r.returncode == 0:
                return r.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
        for cmd in (["pbpaste"], ["wl-paste"], ["xclip", "-selection", "clipboard", "-o"]):
            if shutil.which(cmd[0]):
                r = subprocess.run(cmd, capture_output=True)
                if r.returncode == 0:
                    return r.stdout.decode("utf-8", "replace")
    except OSError:
        pass
    return None
