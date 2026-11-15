#!/usr/bin/env python3
"""Package the 19 ArtCraft skill directories into Claude-ready .zip archives.

Claude (claude.ai / Claude Desktop) requires uploaded skill archives to contain
`<skill>/SKILL.md` at the archive root with a YAML `description` of at most
1,024 characters and no angle brackets (`<` or `>`). Because 16 of the source
`SKILL.md` files carry longer trigger descriptions (up to 1,528 chars) and one
uses a multiline block scalar (`>-`), this script stages each skill cleanly
without modifying the source folders, trims only the packaged frontmatter
`description` to <= 1,024 chars while preserving the full trigger text at the
top of the packaged `SKILL.md` body, strips `.DS_Store`/`.mimosa` noise, and
writes deterministic `.zip` files under `claude-zips/`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
FIXED_ZIP_TIME = (2026, 11, 15, 0, 0, 0)

SKILLS = (
    "anicraft",
    "cadcraft",
    "craft-anything",
    "deckcraft",
    "designcraft",
    "effectcraft",
    "figcraft",
    "filmcraft",
    "gridcraft",
    "lightcraft",
    "mailcraft",
    "materialcraft",
    "pdfcraft",
    "photocraft",
    "solidcraft",
    "soundcraft",
    "texturecraft",
    "vectorcraft",
    "wordcraft",
)

IGNORED_NAMES = {".DS_Store", ".mimosa", "__MACOSX"}

CONDENSED_DESCRIPTIONS: dict[str, str] = {
    "cadcraft": (
        "CADCraft is an open-source, clean-room AutoCAD-style 2D CAD and drafting app "
        "(pure Rust, egui) for macOS, Windows, Linux, FreeBSD and the web, with DXF/DWG "
        "support, clipped block/xref references (XCLIP), raster image attach "
        "(PNG/JPEG/BMP/TIFF), SHX fonts, proxy-preserving DWG saves, editable "
        "MTEXT/multileaders, and control via MCP, JSON control channel, window.cadcraft "
        'and cadcraft-cli. Trigger whenever the user mentions CADCraft (or "the CAD app"), '
        "asks what it can or cannot do, which formats or shortcuts it supports, wants to "
        "draw, edit, dimension, hatch, block, xref, clip, plot, export, convert/round-trip "
        "DXF or DWG, script drafting (AutoLISP, .scr, .pgp, MCP, CLI), prepare assets or "
        'troubleshoot — or describes the job without naming it ("draw a floor plan", '
        '"edit this DXF", "convert DWG to PDF/PNG", "dimension this drawing").'
    ),
    "craft-anything": (
        "Craft Anything is ArtCraft's open-source, pure-Rust reverse-engineering and "
        "rebuilding workbench: it inspects a website, desktop/phone app, game or file "
        "(disassembler, decompiler, archives, browsers, databases, packet captures), has "
        "a coding agent rebuild it in your chosen stack, compares against the original at "
        "three widths or via self-tests, and refines until it matches. Trigger whenever "
        "the user mentions Craft Anything, craft-anything-cli, craft.json, .cany, its "
        "303-tool engine, MCP server, Clean room vs Deep mode, per-project builder approvals "
        'or project layout — or describes the job ("rebuild this website/app/game", '
        '"how does X work under the hood", "figure out how this site is built", "make a '
        'clone of this app", "disassemble this binary"). Do not assume IDA Pro or Ghidra '
        "behaviour; read this first."
    ),
    "deckcraft": (
        "DeckCraft is ArtCraft's open-source, clean-room PowerPoint-compatible presentation "
        "app (macOS, Windows, Linux, FreeBSD, web): slides, masters/layouts, shapes, 3-D, "
        "text, tables, charts, SmartArt, media, transitions, animations, and .deckcraft, "
        ".pptx/.potx/.ppsx, outline, Markdown, .rtf, PDF/PNG/JPEG/GIF files — driven by "
        "329 commands, a 12-subcommand CLI, JSON control channel, 25-tool MCP server and "
        "window.deckcraft. Trigger whenever the user mentions DeckCraft, .deckcraft, "
        "deckcraft-cli, asks what it supports, wants to build, edit, inspect, convert, "
        "render, export, verify or troubleshoot a deck, prepare assets, or automate "
        'presentations — even unnamed ("make a deck", "turn this outline into slides", '
        '"export slides to PDF", "why did my PPTX lose animations?"). Not for Microsoft '
        "PowerPoint itself."
    ),
    "designcraft": (
        "DesignCraft is ArtCraft's clean-room, open-source InDesign-class page-layout app "
        "(pure Rust; .designcraft format; IDML/INDD/INDT import; PDF/X-4, PDF/X-1a, "
        "PDF/A-2b, EPUB with Split Document, editable PPTX, HTML, PNG and JPEG export; "
        "batch export of layouts/versions; preflight; CLI, MCP server and JSON control "
        "channel). Trigger whenever the user mentions DesignCraft or .designcraft, .idml, "
        ".indd, .indt, .dcbook, .dclib, .ase or command scripts; asks what it supports, "
        "how to automate it, prepare assets, place PDFs/layers, thread text, target tables "
        'by id, check links or troubleshoot — or describes the job ("lay out a magazine", '
        '"thread text across columns", "baseline grid", "export PDF/X-4 or PDF/X-1a", '
        '"split EPUB into chapters", "batch-export pages", "import InDesign shortcuts", '
        '"white object vanished on press"). Do not guess from InDesign knowledge.'
    ),
    "effectcraft": (
        "EffectCraft is an open-source, pure-Rust motion-graphics, compositing and VFX app "
        "(macOS, Windows, Linux, web) — a clean-room After Effects-shaped studio with "
        "compositions, layers, keyframes, 308 effects, expressions, Classic/Advanced 3D, "
        "tracking, roto, .aep/.aepx subset interchange, render queue, Lottie, repro scripts "
        "and WASM ABI 1/2 plug-ins, driven by effectcraft-cli, MCP server, JSON control "
        "channel and JS scripting. Trigger whenever the user mentions EffectCraft, "
        ".ecproj/.ecprojx/.ectemplate/.ecpreset, effectcraft-cli, its MCP/control surfaces, "
        'or describes the job ("make a title card", "animate this logo", "key this green '
        'screen", "render ProRes", "export Lottie", "open this .aep"), or when choosing '
        "between EffectCraft and FilmCraft or verifying/preparing assets. Expect subset "
        "reports for .aep, not AE-identical renders."
    ),
    "figcraft": (
        "FigCraft is an open-source, pure-Rust, offline interface-design, prototyping and "
        "whiteboard app (clean-room Figma Design workflow): frames, auto layout, "
        "components, styles, variables, vector networks, prototyping, Developer Mode, mind "
        "maps and board files on macOS, Windows, Linux, FreeBSD and the web. Trigger "
        "whenever the user mentions FigCraft or .figcraft, asks what it can do, which "
        "formats it opens/writes, how to automate it (figcraft-cli, MCP, JSON control "
        "channel), prepare assets, or verify/repair/troubleshoot output — or describes the "
        'job ("make a mockup", "design a screen/landing page/dashboard", "build a design '
        'system", "export frames to PNG/PDF/SVG", "open .fig or Figma JSON", "convert '
        'Sketch or Penpot", "prototype this flow", "hand off to a developer", "make a '
        'retro board or mind map"). FigCraft is not Figma and runs no Figma plugins.'
    ),
    "filmcraft": (
        "FilmCraft is an open-source, pure-Rust non-linear video editor (editing, "
        "multicam, colour grading, effects, titles, captions, audio mixing, export) "
        "mirroring Premiere Pro's workflow for macOS/Windows/Linux and the web. Trigger "
        "whenever the user mentions FilmCraft, .fcproj, filmcraft-cli, its control channel "
        "or MCP server, window.filmcraft, or .prfpset presets; asks what it supports, how "
        "to script/automate it, prepare/convert media, verify/repair exports or project "
        'files, or troubleshoot it — or describes the job ("cut this footage", "make a '
        'rough cut", "export H.264 MP4", "grade this clip", "bake grade to LUT", "add '
        'captions", "hand EDL/AAF to an editor", "drive a video editor from an agent"). '
        "Prefer over generic NLE advice; do not assume Premiere-only features (.prproj, "
        "plugins, uploads) exist."
    ),
    "gridcraft": (
        "GridCraft is an open-source, clean-room Rust Excel reimplementation (macOS, "
        "Windows, Linux, BSD, web) that reads/writes real .xlsx files and runs headlessly "
        "via gridcraft-cli, an MCP server, a JSON control channel, recorded scripts and "
        "window.gridcraft. Trigger whenever the user mentions GridCraft, asks what it "
        "supports (formats, shortcuts, commands, functions), wants to create, edit, "
        "calculate, print or export spreadsheets, automate it, prepare/convert inputs "
        "(.xlsx, CSV, TSV, JSON, .xls/.xlsb/.ods/.slk), verify/round-trip output "
        "(gridcraft-cli check), run sandbox-check, or troubleshoot symptoms — or describes "
        'Excel work ("make an Excel file", "add a formula column", "sort/filter", "pivot '
        'this data", "export workbook to PDF", "read spreadsheet values", "make Arabic '
        'sheet RTL"). Do not assume Excel parity without checking.'
    ),
    "lightcraft": (
        "LightCraft is a pure-Rust photo library and non-destructive raw developer "
        "(clean-room Lightroom Classic) with desktop, lightcraft-cli and WASM builds. "
        "Trigger whenever the user mentions LightCraft, .lcpreset, .lcprint, a library "
        "folder (catalog.snap/catalog.log), lightcraft-cli or its control/MCP server; asks "
        "about RAW/export formats (DNG/CR2/CR3/ARW/NEF/RAF/RW2/ORF/PEF/SRW/MRW/SR2; "
        "JPEG/PNG/TIFF/WebP/AVIF/JXL/PSD/DNG), shortcuts, automation (CLI "
        "run/render/snapshot/merge/calibrate/denoise-serve, JSON control, MCP, "
        "print.*/slideshow.*), migrating Lightroom catalogs (incl. backup .zip), camera "
        "profiles, lensfun, XMP verification or troubleshooting — or describes the job "
        '("cull this shoot", "develop this RAW", "apply preset and export JPEGs", "import '
        'Lightroom catalog", "why won\'t CR3 open", "lens-blur background").'
    ),
    "mailcraft": (
        "MailCraft is an open-source, clean-room Outlook-shaped mail, calendar, contacts "
        "and tasks app in Rust (public beta, v0.13.0): IMAP/SMTP with IDLE push, Microsoft "
        "365/Outlook.com via Graph OAuth, Exchange Web Services, JMAP in web, .mailcraft "
        "mailbox, .eml/.mbox/.ics/.vcf interchange, Outlook .pst import, 343 engine "
        "commands, 89 window commands, 20-tool MCP server, 20-method JSON control channel "
        "and 14-subcommand mailcraft-cli. Trigger whenever the user mentions MailCraft, "
        ".mailcraft, mailcraft-cli, its MCP/control channel or control-key file, asks what "
        "it supports or how to script/troubleshoot it, or describes desktop mail work "
        '("organise this mailbox", "import Outlook .pst", "check calendar", "send mail '
        'from a script"). Not for Outlook itself, mail-server admin, or installed by the '
        "macOS launcher."
    ),
    "materialcraft": (
        "MaterialCraft is ArtCraft's open-source, pure-Rust node-based procedural material "
        "designer: build tileable PBR materials from native primitives, functions and a "
        "171-function SBS library, preview in 2D and displaced 3D, and export texture "
        "maps. Native documents are SBS XML (.sbs) and MaterialCraft Project archives "
        "(.mcraft); portable .mcmat files share materials with TextureCraft. Trigger "
        "whenever the user mentions MaterialCraft or .sbs/.mcraft/.mcmat files, asks what "
        "it supports, how to drive it (materialcraft-cli, MCP, JSON control channel), "
        "build/export PBR materials, import SBS graphs, verify maps/archives or "
        'troubleshoot — or describes the job ("tileable brick material", "export base '
        'color/normal/roughness maps", "material node graph", "open SBS file", "package '
        'project"). Don\'t guess node ids/params; read this first.'
    ),
    "photocraft": (
        "PhotoCraft is ArtCraft's clean-room, pure-Rust Photoshop reimplementation — "
        "layers, masks, adjustment layers, layer styles, live type, vectors, smart "
        "objects, real PSD read/write and PDF-page import — with every action exposed as an "
        "engine command for the UI, photocraft-cli, JSON control channel and 26-tool MCP "
        "server. Trigger whenever the user mentions PhotoCraft, asks what it supports "
        "(formats, shortcuts), how to script/automate/batch it, prepare assets, "
        "inspect/verify/repair a .pcraft, PSD, XCF, PDF or .ora it produced, or "
        'troubleshoot it — or describes the job ("edit this photo", "open this PSD", "PDF '
        'pages to layered artboards", "make transparent PNG", "batch-resize images", '
        '"remove background", "convert HEIC/NEF/PCX", "inspect layered file"). Early alpha: '
        "prefer CLI/MCP over GUI, and do not promise Photoshop-grade PSD fidelity or "
        "generative AI."
    ),
    "solidcraft": (
        "SolidCraft is an open-source parametric 3D CAD app in pure Rust (by Tangency "
        "Labs, clean-room): constrained sketches, parametric feature timeline (extrude, "
        "revolve, sweep, loft, fillet, chamfer, shell, draft, holes, threads, patterns, "
        "mirror, split, combine, cell grids), sheet metal, enclosures, assemblies with "
        "joints/motion, physical materials/mass, sandboxed WASM command plugins, "
        "GnuPG/COSE-signed designs, and STEP/IGES/3MF/STL/OBJ/GLB/URDF/DXF plus KiCad "
        "PCB import. Desktop, browser, solidcraft-cli and 22-tool MCP server share the "
        "647-command registry. Trigger whenever the user mentions SolidCraft, .sc, "
        "solidcraft-cli, SolidCraft MCP, port 27878 or plugins, or describes parametric "
        'CAD ("model a case for this board", "sketch, constrain and extrude", "export STEP '
        'of this bracket"). Don\'t assume Fusion/SolidWorks behaviour.'
    ),
    "texturecraft": (
        "TextureCraft is ArtCraft's open-source, pure-Rust 3D texture painter (clean-room "
        "Substance 3D Painter workflow): paint PBR materials onto 3D models with layers, "
        "masks and generators, bake mesh maps with live streaming preview, drive smart "
        "materials and export texture sets for glTF, Unreal, Unity, Blender, Godot and "
        "OpenPBR. Trigger whenever the user mentions TextureCraft or .tcraft/.tcmat files, "
        "asks what it supports, which mesh formats it opens, how to bake "
        "AO/curvature/normal maps, how to automate it (texturecraft-cli, MCP, JSON control "
        "channel), paint/export engine textures, verify baked maps or troubleshoot — or "
        'describes the job ("paint rust onto this model", "bake AO map", "export glTF PBR '
        'textures", "make a smart material", "reimport mesh without losing paint"). '
        "Don't guess from Substance Painter knowledge; read this first."
    ),
    "vectorcraft": (
        "VectorCraft is a free, open-source, pure-Rust vector illustration app "
        "(clean-room Illustrator for macOS, Windows, Linux, FreeBSD and WASM) with a "
        "33-tool MCP server, 30-method JSON control channel, 11-call browser JS API, "
        "7-subcommand CLI and in-process JS scripting (script.run). Trigger whenever the "
        'user mentions VectorCraft (or "the vector app", .vectorcraft, .drawcraft, '
        ".vctemplate), asks what it supports (formats, CLI flags, MCP/control tools, "
        "shortcuts), wants to create, edit, script, batch-convert or export vector art, "
        "prepare assets (SVG/PDF/EPS/DXF/PSD/HEIC/rasters/fonts/.wasm plug-ins), "
        "verify/repair output or troubleshoot — or describes Illustrator-style work "
        '("draw a logo", "make an SVG", "edit this .ai", "trace bitmap", "convert DXF"). '
        "Not for Adobe Illustrator itself."
    ),
    "wordcraft": (
        "WordCraft is an open-source, clean-room Rust reimplementation of Microsoft Word "
        "(alpha, v0.18.1): reads/writes .docx (incl. password/AES-encrypted), opens "
        ".doc/.mht/.mhtml, reads/writes .odt/.ott/.fodt, exports PDF/PNG (with strict "
        "completeness check), supports multiple docs/windows, wordcraft-cli, 18-tool MCP "
        "server, JSON control channel and headless screenshots. Trigger whenever the user "
        "mentions WordCraft, wordcraft-cli, its MCP/control channel, templates, mail merge, "
        "macros, track changes, or .docx/.doc/.odt/.rtf/.html/.md/.tex in WordCraft, asks "
        "what it supports or how to automate/verify/repair/troubleshoot it — or describes "
        'word-processor work ("write a .docx", "convert .doc to PDF", "decrypt .docx", '
        '"track changes", "mail-merge a letter", "report from Markdown"). Not for '
        "Microsoft Word itself."
    ),
}


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body_text) from a SKILL.md string."""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    if not match:
        raise ValueError("Missing or malformed YAML frontmatter delimiters")
    return match.group(1), match.group(2)


def parse_frontmatter(fm_text: str) -> tuple[str, str, bool]:
    """Parse `name` and `description` from SKILL.md frontmatter without external deps."""
    lines = fm_text.splitlines()
    name: str | None = None
    description: str | None = None
    multiline_scalar = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line or line[0].isspace():
            raise ValueError(f"Unexpected YAML frontmatter line: {line!r}")

        key, raw_val = line.split(":", 1)
        key = key.strip()
        val = raw_val.strip()

        if val in (">-", ">", "|", "|-"):
            multiline_scalar = True
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i][:1].isspace() or lines[i].strip() == ""):
                block.append(lines[i].strip())
                i += 1
            parsed_val = " ".join(part for part in block if part) if val.startswith(">") else "\n".join(block).strip()
        else:
            if val.startswith('"') and val.endswith('"') and len(val) >= 2:
                try:
                    parsed_val = json.loads(val)
                except json.JSONDecodeError:
                    parsed_val = val[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            elif val.startswith("'") and val.endswith("'") and len(val) >= 2:
                parsed_val = val[1:-1].replace("''", "'")
            else:
                parsed_val = val
            i += 1

        if key == "name":
            name = parsed_val
        elif key == "description":
            description = parsed_val
        else:
            raise ValueError(f"Unexpected frontmatter key: {key!r}")

    if not name or not description:
        raise ValueError("Frontmatter must include both 'name' and 'description'")
    return name, description, multiline_scalar


def fallback_trim(description: str) -> str:
    """Trim any unforeseen description > 1024 chars cleanly on sentence/word boundaries."""
    if len(description) <= MAX_DESC_LEN:
        return description
    cutoff = description[: MAX_DESC_LEN - 3]
    for sep in (". ", "; ", " — ", ", ", " "):
        idx = cutoff.rfind(sep)
        if idx > MAX_DESC_LEN // 2:
            return cutoff[:idx].rstrip(" ,;—") + "..."
    return cutoff.rstrip() + "..."


def validate_frontmatter(skill: str, name: str, description: str) -> None:
    if name != skill:
        raise ValueError(f"{skill}: frontmatter name {name!r} != directory name")
    if len(name) > MAX_NAME_LEN or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        raise ValueError(f"{skill}: invalid name {name!r}")
    if not description.strip():
        raise ValueError(f"{skill}: description is empty")
    if "<" in description or ">" in description:
        raise ValueError(f"{skill}: description contains angle brackets")
    if len(description) > MAX_DESC_LEN:
        raise ValueError(f"{skill}: description length {len(description)} > {MAX_DESC_LEN}")


def transform_skill_md(skill: str, raw_text: str) -> str:
    """Return Claude-compatible SKILL.md text without altering the repo source file."""
    fm_text, body = split_frontmatter(raw_text)
    name, orig_desc, is_multiline = parse_frontmatter(fm_text)

    if len(orig_desc) > MAX_DESC_LEN:
        new_desc = CONDENSED_DESCRIPTIONS.get(skill) or fallback_trim(orig_desc)
        validate_frontmatter(skill, name, new_desc)
        new_fm = f"name: {name}\ndescription: {json.dumps(new_desc, ensure_ascii=False)}"
        trigger_note = f"> **Full trigger scope:** {orig_desc}\n\n"
        heading_match = re.match(r"\A(\s*# [^\n]+\r?\n+)(.*)\Z", body, re.DOTALL)
        if heading_match:
            new_body = f"{heading_match.group(1)}{trigger_note}{heading_match.group(2).lstrip()}"
        else:
            new_body = f"\n{trigger_note}{body.lstrip()}"
        return f"---\n{new_fm}\n---\n{new_body}"

    if is_multiline:
        validate_frontmatter(skill, name, orig_desc)
        new_fm = f"name: {name}\ndescription: {json.dumps(orig_desc, ensure_ascii=False)}"
        return f"---\n{new_fm}\n---\n{body}"

    validate_frontmatter(skill, name, orig_desc)
    return raw_text


def collect_skill_files(skill_dir: Path) -> list[Path]:
    """Return sorted regular files inside a skill folder, excluding local noise."""
    files: list[Path] = []
    for path in sorted(skill_dir.rglob("*")):
        rel_parts = path.relative_to(skill_dir).parts
        if any(part in IGNORED_NAMES or part.startswith(".") for part in rel_parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Refusing symlink inside skill directory: {path}")
        if path.is_file():
            files.append(path)
    return files


def build_zip_bytes(repo_root: Path, skill: str, out_path: Path) -> tuple[int, int]:
    """Write `<skill>.zip` deterministically and return (file_count, desc_len)."""
    skill_dir = repo_root / skill
    files = collect_skill_files(skill_dir)
    if not (skill_dir / "SKILL.md").is_file():
        raise FileNotFoundError(f"Missing {skill_dir / 'SKILL.md'}")

    desc_len = 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file_path in files:
            rel = file_path.relative_to(repo_root).as_posix()
            if file_path.name == "SKILL.md" and file_path.parent == skill_dir:
                raw_text = file_path.read_text(encoding="utf-8")
                data_text = transform_skill_md(skill, raw_text)
                fm_text, _ = split_frontmatter(data_text)
                _, desc, _ = parse_frontmatter(fm_text)
                desc_len = len(desc)
                payload = data_text.encode("utf-8")
            else:
                payload = file_path.read_bytes()

            info = zipfile.ZipInfo(filename=rel, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, payload)

    return len(files), desc_len


def verify_zip(zip_path: Path, skill: str) -> tuple[int, int]:
    """Verify an existing archive's integrity, layout, and SKILL.md frontmatter."""
    with zipfile.ZipFile(zip_path, mode="r") as zf:
        bad_member = zf.testzip()
        if bad_member is not None:
            raise ValueError(f"{zip_path}: CRC error on {bad_member}")

        names = [info.filename for info in zf.infolist() if not info.is_dir()]
        if not names:
            raise ValueError(f"{zip_path}: archive is empty")
        for member in names:
            parts = Path(member).parts
            if parts[0] != skill:
                raise ValueError(f"{zip_path}: member {member!r} does not sit under '{skill}/'")
            if any(part in IGNORED_NAMES or part.startswith(".") for part in parts):
                raise ValueError(f"{zip_path}: unexpected hidden/junk entry {member!r}")

        skill_md_member = f"{skill}/SKILL.md"
        if skill_md_member not in names:
            raise ValueError(f"{zip_path}: missing {skill_md_member}")

        content = zf.read(skill_md_member).decode("utf-8")
        fm_text, _ = split_frontmatter(content)
        name, desc, is_multiline = parse_frontmatter(fm_text)
        if is_multiline:
            raise ValueError(f"{zip_path}: multiline scalar in packaged SKILL.md frontmatter")
        validate_frontmatter(skill, name, desc)
        return len(names), len(desc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default="claude-zips",
        help="Output directory relative to repo root (default: claude-zips)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing zip archives without rewriting them",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = (repo_root / args.out_dir).resolve()

    for skill in SKILLS:
        zip_path = out_dir / f"{skill}.zip"
        if args.verify:
            if not zip_path.is_file():
                print(f"MISSING {zip_path}", file=sys.stderr)
                return 1
            count, desc_len = verify_zip(zip_path, skill)
            print(f"OK      {skill:16s} files={count:2d} desc={desc_len:4d}")
        else:
            count, desc_len = build_zip_bytes(repo_root, skill, zip_path)
            verify_zip(zip_path, skill)
            print(f"BUILT   {skill:16s} files={count:2d} desc={desc_len:4d} size={zip_path.stat().st_size:6d}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
