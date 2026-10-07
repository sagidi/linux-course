#!/usr/bin/env bash
# =====================================================================
# ONE-TIME SETUP - installs every tool the course builder needs.
#
#   Run inside Ubuntu (WSL) from the project folder:   ./setup.sh
#
# Safe to run again at any time: it skips what is already installed and
# finishes with a self-test that tells you if anything is missing.
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"

TTYD_VERSION="1.7.7"                     # VHS needs ttyd 1.7.2 or newer
PIPER_VOICE="en_US-lessac-medium"        # free draft voice
PIPER_DIR="${PIPER_VOICES_DIR:-$HOME/.local/share/piper-voices}"

say()  { printf "\n\033[1;36m==> %s\033[0m\n" "$*"; }
ok()   { printf "    \033[32mOK\033[0m   %s\n" "$*"; }
bad()  { printf "    \033[31mFAIL\033[0m %s\n" "$*"; }

if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi
. /etc/os-release
if [ "${ID:-}" != "ubuntu" ]; then
  echo "This script is made for Ubuntu (you have: ${PRETTY_NAME:-unknown}). Continuing anyway..."
fi

# Ubuntu 24.04 renamed some libraries (libasound2 -> libasound2t64, ...)
pkg() { if apt-cache show "${1}t64" >/dev/null 2>&1; then echo "${1}t64"; else echo "$1"; fi; }

# ---------------------------------------------------------------------
say "1/6  System packages (Ubuntu may ask for your password)"
$SUDO apt-get update -y
$SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git curl ca-certificates gnupg \
  python3 python3-venv python3-pip \
  ffmpeg poppler-utils espeak-ng fonts-dejavu-core fonts-liberation \
  dnsutils iputils-ping jq tree \
  libnss3 "$(pkg libatk1.0-0)" "$(pkg libatk-bridge2.0-0)" "$(pkg libcups2)" libdrm2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
  "$(pkg libasound2)" libpango-1.0-0 libcairo2
ok "system packages"

# ---------------------------------------------------------------------
say "2/6  ttyd (the terminal VHS records)"
need_ttyd=1
if command -v ttyd >/dev/null; then
  have=$(ttyd --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  if [ -n "$have" ] && [ "$(printf '%s\n1.7.2\n' "$have" | sort -V | head -1)" = "1.7.2" ]; then
    need_ttyd=0; ok "ttyd $have"
  fi
fi
if [ $need_ttyd -eq 1 ]; then
  $SUDO apt-get install -y ttyd >/dev/null 2>&1 || true
  have=$(ttyd --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
  if [ -z "$have" ] || [ "$(printf '%s\n1.7.2\n' "$have" | sort -V | head -1)" != "1.7.2" ]; then
    arch=$(uname -m)   # x86_64 or aarch64
    curl -fsSL -o /tmp/ttyd "https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.${arch}"
    $SUDO install -m 0755 /tmp/ttyd /usr/local/bin/ttyd
  fi
  ok "ttyd $(ttyd --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
fi

# ---------------------------------------------------------------------
say "3/6  VHS by Charm (records terminal demos as video)"
if ! command -v vhs >/dev/null; then
  $SUDO mkdir -p /etc/apt/keyrings
  curl -fsSL https://repo.charm.sh/apt/gpg.key | $SUDO gpg --dearmor --yes -o /etc/apt/keyrings/charm.gpg
  echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" \
    | $SUDO tee /etc/apt/sources.list.d/charm.list >/dev/null
  $SUDO apt-get update -y
  $SUDO apt-get install -y vhs
fi
ok "$(vhs --version)"

# ---------------------------------------------------------------------
say "4/6  Python tools (in a private folder: .venv)"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -r engine/requirements.txt
ok "python packages"

# ---------------------------------------------------------------------
say "5/6  Free draft voice (Piper: $PIPER_VOICE)"
mkdir -p "$PIPER_DIR"
if [ ! -f "$PIPER_DIR/$PIPER_VOICE.onnx" ]; then
  .venv/bin/python -m piper.download_voices --download-dir "$PIPER_DIR" "$PIPER_VOICE" \
    || echo "    (Piper voice download failed - drafts will use the robotic espeak voice instead)"
fi
[ -f "$PIPER_DIR/$PIPER_VOICE.onnx" ] && ok "Piper voice"

# ---------------------------------------------------------------------
say "6/6  Project files"
chmod +x setup.sh build.sh new-module.sh paste-module.sh
if [ ! -f .env ]; then
  cp .env.example .env
  ok "created .env (put your ElevenLabs key in it later - see docs/03)"
else
  ok ".env already exists"
fi

# ---------------------------------------------------------------------
say "Self-test"
fails=0
for t in python3 ffmpeg ffprobe pdftoppm ttyd vhs espeak-ng dig git; do
  if command -v "$t" >/dev/null; then ok "$t"; else bad "$t is missing"; fails=$((fails+1)); fi
done
.venv/bin/python -c "import reportlab, yaml, requests, PIL" && ok "python packages import" \
  || { bad "python packages"; fails=$((fails+1)); }

# Record a 1-second test clip. The first run downloads the browser VHS uses.
printf 'Output "/tmp/vhs-selftest.mp4"\nSet Width 640\nSet Height 360\nType "echo hello"\nEnter\nSleep 500ms\n' > /tmp/vhs-selftest.tape
if vhs /tmp/vhs-selftest.tape >/tmp/vhs-selftest.log 2>&1 && [ -s /tmp/vhs-selftest.mp4 ]; then
  ok "VHS can record video"
else
  bad "VHS could not record a test video - see /tmp/vhs-selftest.log and docs/reference/troubleshooting.md"
  fails=$((fails+1))
fi

echo
if [ $fails -eq 0 ]; then
  printf "\033[1;32mAll set!\033[0m Next step: docs/04-first-test-build.md   (run:  ./build.sh 1.2 --draft)\n"
else
  printf "\033[1;31m%d problem(s) above.\033[0m Fix them (docs/reference/troubleshooting.md) and run ./setup.sh again.\n" $fails
  exit 1
fi
