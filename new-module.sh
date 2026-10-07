#!/usr/bin/env bash
# =====================================================================
# START A NEW MODULE
#
#   ./new-module.sh 1.3
#   ./new-module.sh 1.3 "Linux System Logging (/var/log & journalctl)"
#
# Creates the module folder, fills in the master prompt for this module
# and copies it to your clipboard, ready to paste into the AI chat.
# (The title is optional when the module is listed in course.yaml -> outline.)
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"
if [ $# -lt 1 ]; then sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 1; fi
[ -x .venv/bin/python ] || { echo "Run ./setup.sh first."; exit 1; }
.venv/bin/python engine/new_module.py "$@"
