#!/usr/bin/env bash
# Comprueba lo que necesita /aplicacion: Mac, Xcode con el plugin oficial de Apple para Claude, Claude Code y Python 3.
# Solo lee: no instala ni cambia nada.
ok(){ printf '  ✓ %s\n' "$1"; }; ko(){ printf '  ✗ %s\n' "$1"; }; av(){ printf '  · %s\n' "$1"; }
echo "Comprobando el ordenador…"

if [ "$(uname)" = "Darwin" ]; then ok "macOS $(sw_vers -productVersion)"; else ko "Esto no es un Mac: para apps de iPhone hace falta un Mac con Xcode"; fi

if command -v xcodebuild >/dev/null 2>&1 && xcodebuild -version >/dev/null 2>&1; then
  ok "$(xcodebuild -version | head -1)"
else
  ko "Xcode no está instalado (o no está seleccionado). Instálalo gratis desde la Mac App Store y ábrelo una vez"
fi

if xcrun agent plugin path --plugin-format claude >/dev/null 2>&1; then
  ok "Tu Xcode trae el plugin para Claude: $(xcrun agent plugin path --plugin-format claude 2>/dev/null)"
else
  ko "Tu Xcode no trae el plugin para Claude (xcrun agent). Actualiza Xcode a la última versión"
fi

if command -v claude >/dev/null 2>&1; then ok "Claude Code $(claude --version 2>/dev/null | head -1)"; else ko "Claude Code no está instalado (claude.com/claude-code)"; fi
if command -v python3 >/dev/null 2>&1; then ok "$(python3 --version)"; else ko "Python 3 no está (xcode-select --install)"; fi
if command -v node >/dev/null 2>&1; then ok "Node $(node -v) (opcional: para app-store-scraper)"; else av "Node no está (opcional)"; fi

if xcrun simctl list devices available 2>/dev/null | grep -q "iPhone"; then
  ok "Hay simuladores de iPhone instalados"
else
  av "No veo simuladores de iPhone: en Xcode → Settings → Components, descarga la plataforma iOS"
fi
