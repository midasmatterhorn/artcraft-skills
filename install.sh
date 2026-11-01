#!/usr/bin/env bash
# Install the ArtCraft agent skills into an agent skills directory.
# Usage: ./install.sh [--force] [--claude] [--opencode] [--gemini] [--antigravity]
#   default target ~/.agents/skills/ — scanned natively by OpenAI Codex,
#   ChatGPT desktop, ZCode, Devin, CommandCode, Gemini CLI and other
#   agentskills.io-standard agents
#   --claude targets ~/.claude/skills/ for Claude Code
#   --opencode targets ~/.config/opencode/skills/ for OpenCode
#   --gemini targets ~/.gemini/skills/ for Gemini CLI
#   --antigravity targets ~/.gemini/config/skills/ for Google Antigravity
set -euo pipefail
cd "$(dirname "$0")"

dest="${HOME}/.agents/skills"
skills="photocraft lightcraft vectorcraft figcraft designcraft wordcraft deckcraft gridcraft pdfcraft effectcraft filmcraft soundcraft cadcraft craft-anything solidcraft"
force=false
for arg in "$@"; do
  case "$arg" in
    --force)    force=true ;;
    --claude)     dest="${HOME}/.claude/skills" ;;
    --opencode)   dest="${HOME}/.config/opencode/skills" ;;
    --gemini)     dest="${HOME}/.gemini/skills" ;;
    --antigravity) dest="${HOME}/.gemini/config/skills" ;;
    *) echo "unknown flag: $arg (usage: $0 [--force] [--claude] [--opencode] [--gemini] [--antigravity])" >&2; exit 1 ;;
  esac
done

mkdir -p "$dest"
installed=0; skipped=0
for s in $skills; do
  case "$s" in ''|*[!a-z]*) echo "refusing bad skill name: $s" >&2; exit 1;; esac
  if [ -e "$dest/$s" ] && [ "$force" = false ]; then
    echo "skip  $s (already installed — use --force to overwrite)"
    skipped=$((skipped+1))
  else
    rm -rf "$dest/$s"
    cp -R "$s" "$dest/$s"
    echo "install  $s -> $dest/$s"
    installed=$((installed+1))
  fi
done
echo "done: $installed installed, $skipped skipped. Restart your agent session to pick them up."
