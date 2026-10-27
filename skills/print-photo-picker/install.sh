#!/usr/bin/env bash
# macOS arm64 / Python 3.11 — HANDOFF §6–§8
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${HOME}/.qwenworkcn/skills/print-photo-picker"
PY="${PYTHON:-python3.11}"

echo "Installing print-photo-picker to ${TARGET}"
mkdir -p "${HOME}/.qwenworkcn/skills"
if [ ! -e "${TARGET}" ] || [ "${SKILL_DIR}" != "$(cd "${TARGET}" 2>/dev/null && pwd)" ]; then
  mkdir -p "$(dirname "${TARGET}")"
  rsync -a --delete "${SKILL_DIR}/" "${TARGET}/" 2>/dev/null || cp -a "${SKILL_DIR}/." "${TARGET}/"
fi

"${PY}" -m pip install -U pip
"${PY}" -m pip install -r "${TARGET}/requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple

MODEL_DIR="${HOME}/.insightface/models/buffalo_l"
if [ ! -d "${MODEL_DIR}" ]; then
  echo "Preparing InsightFace buffalo_l model..."
  mkdir -p "${HOME}/.insightface/models"
  ZIP="${HOME}/.insightface/models/buffalo_l.zip"
  if [ ! -f "${ZIP}" ]; then
    curl -L --retry 3 -o "${ZIP}" \
      "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip" \
      || curl -L --retry 3 -o "${ZIP}" \
      "https://hf-mirror.com/deepinsight/insightface/resolve/main/models/buffalo_l.zip"
  fi
  unzip -o "${ZIP}" -d "${HOME}/.insightface/models/"
fi

echo "Done. Run:"
echo "  cd ${TARGET} && ${PY} -m src.cli run --help"
