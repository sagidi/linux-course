#!/usr/bin/env bash
# =====================================================================
# SAVE THE AI's ANSWER AS module.yaml
#
#   1. In the AI chat, click "Copy" on the answer (the YAML block).
#   2. Run:   ./paste-module.sh 1.3
#
# Reads your clipboard, keeps only the YAML, saves it as
# modules/<folder>/module.yaml (old version is backed up) and checks it.
# No clipboard access? Save the answer to a file and run:
#   ./paste-module.sh 1.3 --file answer.txt
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"
if [ $# -lt 1 ]; then sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 1; fi
[ -x .venv/bin/python ] || { echo "Run ./setup.sh first."; exit 1; }
.venv/bin/python engine/paste_module.py "$@"
