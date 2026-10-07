#!/usr/bin/env bash
# =====================================================================
# BUILD A MODULE
#
#   ./build.sh 1.2 --check    check module.yaml for problems (seconds)
#   ./build.sh 1.2 --slides   slides PDF only, to review quickly (seconds)
#   ./build.sh 1.2 --draft    full video with a FREE voice (a few minutes)
#   ./build.sh 1.2            FINAL video with your ElevenLabs voice
#
# Results go to: modules/<module folder>/build/publish/
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"

if [ $# -lt 1 ]; then
  sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi
if [ ! -x .venv/bin/python ]; then
  echo "The tools are not installed yet. Run:  ./setup.sh"
  exit 1
fi
# Load secrets from .env (only values that are filled in, so an empty line
# never hides a key that is already set, e.g. a GitHub Actions secret).
if [ -f .env ]; then
  while IFS='=' read -r key value; do
    [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]] || continue
    value="${value%\"}"; value="${value#\"}"; value="${value%\'}"; value="${value#\'}"
    [ -n "$value" ] && export "$key=$value"
  done < .env
fi

.venv/bin/python engine/build.py "$@"

# On Windows (WSL), show how to open the results folder in File Explorer.
if grep -qi microsoft /proc/version 2>/dev/null && [[ " $* " != *" --check "* ]]; then
  dir=$(ls -d modules/module-"$1"-*/build/publish 2>/dev/null | head -1 || true)
  [ -n "$dir" ] && echo -e "\nOpen the folder in Windows:   explorer.exe $dir"
fi
