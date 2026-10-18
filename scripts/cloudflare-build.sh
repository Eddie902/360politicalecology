#!/usr/bin/env bash
set -euo pipefail
if ! command -v quarto >/dev/null 2>&1; then
  VERSION="1.6.43"
  echo "Installing Quarto ${VERSION} for Cloudflare Pages build (linux amd64)"
  curl -fsSL "https://github.com/quarto-dev/quarto-cli/releases/download/v${VERSION}/quarto-${VERSION}-linux-amd64.tar.gz" -o /tmp/quarto.tar.gz
  mkdir -p /tmp/quarto-bin
  tar -xzf /tmp/quarto.tar.gz -C /tmp/quarto-bin
  export PATH="/tmp/quarto-bin/quarto-${VERSION}/bin:${PATH}"
fi
quarto --version
python3 -m pip install --quiet PyYAML
python3 scripts/build_media.py
quarto render
