#!/usr/bin/env bash
# Atlas Desk — installation de l'agent en une ligne.
#   curl -fsSL https://atlasnexus.tech/atlas-desk/install.sh | bash
# Telecharge le binaire adapte, l'installe dans ~/.local/bin, cree un service
# utilisateur systemd (demarrage automatique a l'ouverture de session) et
# affiche l'identifiant a 9 chiffres de la machine.
set -euo pipefail

VERSION="v0.10.0"
BASE="https://github.com/AtlasNexusTech/atlas-desk/releases/download/${VERSION}"
BIN_DIR="${HOME}/.local/bin"
BIN="${BIN_DIR}/atlas-desk-agent"
SIGNAL="wss://signal.atlasnexus.tech/ws"

say() { printf '\033[1;34m◆\033[0m %s\n' "$1"; }
die() { printf '\033[1;31m✗\033[0m %s\n' "$1" >&2; exit 1; }

case "$(uname -s)" in
  Linux) ;;
  *) die "Ce script cible Linux. Sous Windows, telechargez l'archive depuis atlasnexus.tech/atlas-desk/" ;;
esac
case "$(uname -m)" in
  x86_64|amd64) ASSET="atlas-desk-agent-linux-amd64.tar.gz" ;;
  aarch64|arm64) ASSET="atlas-desk-agent-linux-arm64.tar.gz" ;;
  *) die "Architecture non prise en charge : $(uname -m)" ;;
esac

say "Telechargement de l'agent (${VERSION}, $(uname -m))"
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
curl -fsSL "${BASE}/${ASSET}" -o "${TMP}/agent.tar.gz" || die "Telechargement impossible"
tar xzf "${TMP}/agent.tar.gz" -C "${TMP}"

FOUND="$(find "${TMP}" -type f -name '*agent*' ! -name '*.tar.gz' | head -1)"
[ -n "${FOUND}" ] || die "Binaire introuvable dans l'archive"
mkdir -p "${BIN_DIR}"
install -m 755 "${FOUND}" "${BIN}"
say "Agent installe : ${BIN}"

# Service utilisateur : l'agent redemarre seul et se lance a l'ouverture de session.
if command -v systemctl >/dev/null 2>&1 && systemctl --user show-environment >/dev/null 2>&1; then
  UNIT_DIR="${HOME}/.config/systemd/user"
  mkdir -p "${UNIT_DIR}"
  cat > "${UNIT_DIR}/atlas-desk-agent.service" <<EOF
[Unit]
Description=Atlas Desk — agent de prise en main a distance
After=network.target

[Service]
ExecStart=${BIN} -signal ${SIGNAL}
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
  systemctl --user daemon-reload
  systemctl --user enable --now atlas-desk-agent.service
  say "Service actif (demarrage automatique a l'ouverture de session)"
  sleep 2
  echo
  say "Votre identifiant Atlas Desk :"
  journalctl --user -u atlas-desk-agent.service -n 40 --no-pager 2>/dev/null \
    | grep -Eo '[0-9]{3}[ -]?[0-9]{3}[ -]?[0-9]{3}' | tail -1 \
    || echo "  (consultez : journalctl --user -u atlas-desk-agent -f)"
else
  say "systemd indisponible : lancez l'agent manuellement"
  echo "  ${BIN} -signal ${SIGNAL}"
fi

echo
say "Connectez-vous depuis un navigateur : https://atlasnexus.tech/atlas-desk/client/"
