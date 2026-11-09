#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
pkg install -y python ffmpeg
if [ ! -x .venv/bin/python ]; then python -m venv .venv; fi
.venv/bin/python -m pip install 'edge-tts==7.3.1'
.venv/bin/python gerar.py --diagnostico
.venv/bin/python gerar.py --login
exec .venv/bin/python gerar.py
