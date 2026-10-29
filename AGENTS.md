# AGENTS.md — ArtCraft Skills archive

You are a coding agent. This folder is the persistence archive of the
[artcraft-skills](https://github.com/midasmatterhorn/artcraft-skills) project: 13
evidence-verified skills for the ArtCraft desktop apps. If the user asks you to
install, update, or verify these skills, do it for the agent **you** are running as.

## Install (pick your target)

From the packaged release in this folder — the 13 skill folders sit at the zip root
(pick the newest `artcraft-skills-v*.zip`):

```sh
ZIP="$(ls -t releases/artcraft-skills-v*.zip | head -1)"

# Default: OpenAI Codex, ChatGPT desktop, ZCode, Devin, CommandCode, Gemini CLI (~/.agents/skills)
unzip -o "$ZIP" -d ~/.agents/skills/

# Claude Code
unzip -o "$ZIP" -d ~/.claude/skills/

# OpenCode
unzip -o "$ZIP" -d ~/.config/opencode/skills/

# Gemini CLI
unzip -o "$ZIP" -d ~/.gemini/skills/

# Google Antigravity
unzip -o "$ZIP" -d ~/.gemini/config/skills/
```

Windows PowerShell:

```powershell
$zip = Get-ChildItem releases\artcraft-skills-v*.zip | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Expand-Archive $zip -DestinationPath $HOME\.agents\skills   # or .claude\skills / .config\opencode\skills / .gemini\skills / .gemini\config\skills
```

Or from source (latest state):

```sh
git clone https://github.com/midasmatterhorn/artcraft-skills.git && cd artcraft-skills
bash install.sh              # default → ~/.agents/skills/  (add --claude, --opencode, --gemini or --antigravity to retarget)
.\install.ps1                # Windows; -Claude / -OpenCode / -Gemini / -Antigravity switches, -Force to overwrite
```

## Verify

All 13 skill directories must exist under the chosen target — `cadcraft`, `deckcraft`,
`designcraft`, `effectcraft`, `figcraft`, `filmcraft`, `gridcraft`, `lightcraft`,
`pdfcraft`, `photocraft`, `soundcraft`, `vectorcraft`, `wordcraft` — each containing
`SKILL.md` and `agents/openai.yaml`. Print the target directory you used, then tell the
user to restart their agent session so the skills are discovered.

## Windows: driving the GUI apps live

Agents on Windows often spawn processes in a non-interactive window station
(`CREATE_NO_WINDOW`); the ArtCraft GUI apps (egui/DirectX) can exit immediately with code 0
and no window when launched that way. An app that dies before its first frame may also
record the display adapter as bad and leave it out on later starts — VectorCraft writes
`%APPDATA%\VectorCraft\logs\graphics-start.json`, FilmCraft keeps a similar start record —
so the GPU can look "disabled" until that memory is cleared.

**Try the direct launch first.** `CREATE_NO_WINDOW` only hides a console; it does not move
the process to another window station. An agent running in the user's logged-on session (a
terminal, an IDE, a desktop app) can start the GUI itself. The launcher installs apps
per-user by default (`%LOCALAPPDATA%\Programs\ArtCraft\<App>`); apps installed for all
users live at `C:\Program Files\ArtCraft\<App>`:

```cmd
cmd.exe /c start "" "%LOCALAPPDATA%\Programs\ArtCraft\<App>\<app>.exe" --control <port>
```

If no window appears, the agent is in a non-interactive session — a Windows service /
session 0, or a runner that sandboxed its window station. Nothing started from that session
can paint on the user's desktop: use the headless CLI/MCP surface instead, or ask the
**user** to launch the app interactively. As a last resort, an agent that *is* running as
the logged-in user can have Task Scheduler launch the app interactively:

```cmd
schtasks /create /tn "ArtCraft-<App>-<port>" /tr "\"%LOCALAPPDATA%\Programs\ArtCraft\<App>\<app>.exe\" --control <port>" /sc once /st <future-time> /it /f
schtasks /run /tn "ArtCraft-<App>-<port>"
schtasks /delete /tn "ArtCraft-<App>-<port>" /f
```

- `/it` has no effect for tasks run as SYSTEM, and the System account has no interactive
  desktop; from a service, the interactive user has to launch the app.
- `/sc once` refuses a start time already in the past, so `<future-time>` must be later
  today (or create the task with `/sc onlogon` and `/run` it immediately).
- This creates a real scheduled task — an auditable artifact and a known execution
  primitive. Use a unique task name, keep the default limited run level (never
  `/rl highest`), delete the task right after it runs, and if endpoint policy blocks
  `schtasks`, ask the user instead of retrying.
- The app needs its control channel enabled at launch, with its own authentication (below).

If an earlier background launch did mark the adapter, reset the choice before blaming the
GPU: close the app, change Preferences › Performance › Graphics Processor (or set
`WGPU_ADAPTER_NAME` / `WGPU_BACKEND` for one start), or — only when you know the GPU is
healthy — delete `%APPDATA%\<App>\logs\graphics-start.json` so the next start tries it
again. Not every app writes that file.

Then connect a TCP socket to `127.0.0.1:<port>` and send one JSON request per line.
Authentication differs per app — check the app's SKILL.md before connecting:

- **PhotoCraft**: pass `--control-token <64-hex>` (or `--control-token-file <path>`) at launch.
- **WordCraft**: read the key from `%APPDATA%\<App>\control-key.local-<port>` (mode 0600, deleted on exit).
- **PdfCraft**: launch with `--control FILE` — the file holds the loopback port and per-launch token.
- **CADCraft**: every request needs `"token": "<session token>"`, read from `cadcraft-control-<port>.token` (`%LOCALAPPDATA%` on Windows; `$XDG_RUNTIME_DIR`, else `~/.cache` elsewhere) — the app prints the path at startup.
- **FilmCraft**: the listener only opens when `FILMCRAFT_CONTROL_TOKEN` holds 64 hex characters at launch; every request carries the same `"token"`.
- **GridCraft**: the first line of a connection must authenticate with the app's token — pass `--control-token <token>` or `GRIDCRAFT_CONTROL_TOKEN` at launch, or read the auto-generated token file whose path the app prints to stderr (`gridcraft-cli` reads it automatically); a connection that does not authenticate, or later sends a bad line, is closed.
- **All other apps**: loopback-only, unauthenticated — enable only while in use.

Send UTF-8 **without a BOM**: the control servers treat a BOM-prefixed first line as
malformed JSON and close the connection. Windows PowerShell 5.1 pipes add a BOM — use raw
sockets, `pwsh` (`utf8NoBOM`), or set `[Console]::OutputEncoding` explicitly. On macOS and
Linux the apps launch normally; this note is Windows-specific.
