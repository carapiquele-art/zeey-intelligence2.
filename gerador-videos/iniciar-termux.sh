#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v pkg >/dev/null; then echo 'Execute este arquivo no Termux.'; exit 1; fi
pkg install -y python python-pillow ffmpeg
if [ ! -x .venv/bin/python ]; then python -m venv --system-site-packages .venv; fi
.venv/bin/python -m pip install 'edge-tts==7.3.1'
.venv/bin/python -c 'from PIL import Image; import edge_tts; print("Dependências disponíveis.")'
exec .venv/bin/python agente.py --inicio 1 --limite 10000 --vigiar
