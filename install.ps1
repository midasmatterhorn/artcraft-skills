# Install the ArtCraft agent skills into an agent skills directory.
# Usage: .\install.ps1 [-Force] [-Claude] [-OpenCode] [-Gemini] [-Antigravity]
#   default target $HOME\.agents\skills\ — scanned natively by OpenAI Codex,
#   ChatGPT desktop, ZCode, Devin, CommandCode, Gemini CLI on Windows; -Claude
#   targets $HOME\.claude\skills\ for Claude Code; -OpenCode targets
#   $HOME\.config\opencode\skills\ for OpenCode; -Gemini targets
#   $HOME\.gemini\skills\ for Gemini CLI; -Antigravity targets
#   $HOME\.gemini\config\skills\ for Google Antigravity. PowerShell 5.1+, no modules.
param([switch]$Force, [switch]$Claude, [switch]$OpenCode, [switch]$Gemini, [switch]$Antigravity)

$ErrorActionPreference = 'Stop'
$dest = Join-Path $HOME '.agents\skills'
if ($Claude)     { $dest = Join-Path $HOME '.claude\skills' }
if ($OpenCode)   { $dest = Join-Path $HOME '.config\opencode\skills' }
if ($Gemini)     { $dest = Join-Path $HOME '.gemini\skills' }
if ($Antigravity){ $dest = Join-Path $HOME '.gemini\config\skills' }
$skills = 'artcraft-studio photocraft lightcraft vectorcraft figcraft designcraft wordcraft deckcraft gridcraft pdfcraft effectcraft filmcraft anicraft soundcraft cadcraft craft-anything solidcraft texturecraft materialcraft mailcraft' -split ' '

New-Item -ItemType Directory -Force -Path $dest | Out-Null
$installed = 0; $skipped = 0
foreach ($s in $skills) {
    if ($s -notmatch '^[a-z][a-z-]*$') { [Console]::Error.WriteLine("refusing bad skill name: $s"); exit 1 }
    $target = Join-Path $dest $s
    if ((Test-Path $target) -and -not $Force) {
        Write-Host "skip  $s (already installed — use -Force to overwrite)"
        $skipped++
    } else {
        Remove-Item -Recurse -Force -Path $target -ErrorAction SilentlyContinue
        Copy-Item -Recurse -Force -Path (Join-Path $PSScriptRoot $s) -Destination $target
        Write-Host "install  $s -> $target"
        $installed++
    }
}
Write-Host "done: $installed installed, $skipped skipped. Restart your agent session to pick them up."
