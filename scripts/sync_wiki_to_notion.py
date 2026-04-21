#!/usr/bin/env python3
"""
Sync GitHub Wiki -> Notion

Spiegelt den Inhalt des unraid-nas-docs.wiki Repos auf eine Notion-Seite.

Strategie:
  1. Wiki wird vor dem Aufruf durch die Action bereits geklont (siehe Workflow).
  2. Home.md wird zum Content der HOMELAB-Parent-Seite.
  3. Alle anderen .md-Dateien werden Unterseiten.
  4. Alte Unterseiten werden vor dem Sync archiviert (Notion = "delete"),
     damit gelöschte/umbenannte Wiki-Seiten nicht als Zombies übrig bleiben.

Environment Variables (Required):
  NOTION_TOKEN          - Notion Integration Token (secret_...)
  NOTION_PARENT_PAGE_ID - ID der HOMELAB-Seite in Notion
  WIKI_DIR              - Pfad zum geklonten Wiki-Repo (default: ./wiki)
"""

import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# --- Konfiguration ---

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
PARENT_PAGE_ID = os.environ.get("NOTION_PARENT_PAGE_ID")
WIKI_DIR = Path(os.environ.get("WIKI_DIR", "./wiki"))

if not NOTION_TOKEN or not PARENT_PAGE_ID:
    print("ERROR: NOTION_TOKEN und NOTION_PARENT_PAGE_ID müssen gesetzt sein.",
          file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

# Notion limitiert rich_text auf 2000 Zeichen pro Block.
MAX_TEXT_LENGTH = 1900


# --- Notion API Helpers ---

def notion_request(method: str, path: str, **kwargs) -> dict:
    """Kleiner Wrapper mit Retry bei Rate-Limits."""
    url = f"{NOTION_API}{path}"
    for attempt in range(5):
        resp = requests.request(method, url, headers=HEADERS, timeout=30, **kwargs)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", "2"))
            print(f"  Rate-limited, warte {wait}s...")
            time.sleep(wait)
            continue
        if not resp.ok:
            print(f"  Notion API Fehler {resp.status_code}: {resp.text}",
                  file=sys.stderr)
            resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Zu viele Retries gegen Notion API")


def get_child_pages(parent_id: str) -> list[dict]:
    """Liste alle direkten Child-Pages einer Seite."""
    children = []
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = notion_request("GET", f"/blocks/{parent_id}/children", params=params)
        for block in data.get("results", []):
            if block.get("type") == "child_page":
                children.append(block)
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return children


def archive_page(page_id: str) -> None:
    """Seite löschen (= archivieren in Notion)."""
    notion_request("PATCH", f"/pages/{page_id}",
                   json={"archived": True})


def create_page(parent_id: str, title: str, blocks: list[dict]) -> str:
    """Neue Unterseite mit Inhalt anlegen. Returns page_id."""
    # Notion erlaubt max. 100 Blocks pro API-Call. Rest hängen wir nach.
    first_batch = blocks[:100]
    rest = blocks[100:]

    body = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "children": first_batch,
    }
    result = notion_request("POST", "/pages", json=body)
    page_id = result["id"]

    # Rest-Blocks in 100er-Chunks anhängen
    for i in range(0, len(rest), 100):
        chunk = rest[i:i + 100]
        notion_request("PATCH", f"/blocks/{page_id}/children",
                       json={"children": chunk})

    return page_id


def replace_page_content(page_id: str, blocks: list[dict]) -> None:
    """Ersetze den Inhalt einer bestehenden Seite."""
    # Alle existierenden Kinder (die KEINE Child-Pages sind) löschen
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = notion_request("GET", f"/blocks/{page_id}/children", params=params)
        for block in data.get("results", []):
            if block.get("type") != "child_page":
                try:
                    notion_request("DELETE", f"/blocks/{block['id']}")
                except Exception as e:
                    print(f"  Konnte Block nicht löschen: {e}")
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    # Neue Blöcke in 100er-Chunks anhängen
    for i in range(0, len(blocks), 100):
        chunk = blocks[i:i + 100]
        notion_request("PATCH", f"/blocks/{page_id}/children",
                       json={"children": chunk})


# --- Markdown -> Notion Blocks ---
#
# Bewusst simpel gehalten. Deckt ab was im Wiki vorkommt:
# - Headings (#, ##, ###)
# - Paragraphs
# - Bulleted / numbered lists
# - Task-Lists (- [ ] / - [x])
# - Code blocks (``` lang)
# - Blockquotes (>)
# - Horizontal rules (---)
# - Tables -> werden als Notion-Tabellen ausgegeben
# - Inline: bold, italic, code, links
# - GitHub Wiki-Links: [[Page]] und [[Page|Label]]

INLINE_PATTERN = re.compile(
    r"(\*\*([^*]+)\*\*|"   # bold
    r"\*([^*]+)\*|"         # italic
    r"`([^`]+)`|"           # inline code
    r"\[([^\]]+)\]\(([^)]+)\))"  # link
)

# GitHub Wiki-Link: [[Seitenname]] oder [[Seitenname|Anzeigetext]]
# Heuristik: Das Segment mit Bindestrich/Gross-Kleinschreibung ist vermutlich
# der Seitenname (z.B. "Disaster-Recovery"), das andere der Anzeigetext.
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

# Basis-URL für Wiki-Links (wird in main() bei Bedarf überschrieben)
WIKI_BASE_URL = os.environ.get(
    "WIKI_BASE_URL",
    "https://github.com/Bolmir/unraid-nas-docs/wiki"
)


def _looks_like_page_name(s: str) -> bool:
    """Heuristik: Enthält Bindestrich oder beginnt gross → vermutlich Seitenname."""
    return "-" in s or (s[:1].isupper() and " " not in s)


def convert_wiki_links(text: str) -> str:
    """Konvertiert [[Page]] und [[A|B]] zu normalen Markdown-Links."""
    def replace(m: re.Match) -> str:
        first, second = m.group(1), m.group(2)
        if second is None:
            # [[Seitenname]]
            page = first
            label = first.replace("-", " ")
        else:
            # [[A|B]] — welcher ist der Seitenname?
            if _looks_like_page_name(first) and not _looks_like_page_name(second):
                page, label = first, second
            elif _looks_like_page_name(second) and not _looks_like_page_name(first):
                page, label = second, first
            else:
                # Default GitHub-Verhalten: erstes = Seite, zweites = Label
                page, label = first, second
        # Seitenname für URL: Leerzeichen werden zu Bindestrichen
        page_url = page.strip().replace(" ", "-")
        return f"[{label}]({WIKI_BASE_URL}/{page_url})"
    return WIKI_LINK_PATTERN.sub(replace, text)


def truncate(text: str) -> str:
    if len(text) > MAX_TEXT_LENGTH:
        return text[:MAX_TEXT_LENGTH - 3] + "..."
    return text


def parse_inline(text: str) -> list[dict]:
    """Inline-Markdown zu Notion rich_text Array."""
    text = text.strip()
    if not text:
        return [{"type": "text", "text": {"content": ""}}]

    result = []
    pos = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > pos:
            result.append({
                "type": "text",
                "text": {"content": truncate(text[pos:match.start()])},
            })

        bold, italic, code, link_text, link_url = (
            match.group(2), match.group(3), match.group(4),
            match.group(5), match.group(6)
        )

        if bold:
            result.append({
                "type": "text",
                "text": {"content": truncate(bold)},
                "annotations": {"bold": True},
            })
        elif italic:
            result.append({
                "type": "text",
                "text": {"content": truncate(italic)},
                "annotations": {"italic": True},
            })
        elif code:
            result.append({
                "type": "text",
                "text": {"content": truncate(code)},
                "annotations": {"code": True},
            })
        elif link_text:
            result.append({
                "type": "text",
                "text": {"content": truncate(link_text), "link": {"url": link_url}},
            })
        pos = match.end()

    if pos < len(text):
        result.append({
            "type": "text",
            "text": {"content": truncate(text[pos:])},
        })

    return result if result else [{"type": "text", "text": {"content": ""}}]


def parse_table(lines: list[str]) -> dict | None:
    """Markdown-Tabelle -> Notion table block."""
    # Mindestens Header + Separator + 1 Zeile
    if len(lines) < 2:
        return None

    def split_row(row: str) -> list[str]:
        cells = row.strip().strip("|").split("|")
        return [c.strip() for c in cells]

    header_cells = split_row(lines[0])
    # Zeile 2 ist Separator (---|---), überspringen
    body_rows = [split_row(l) for l in lines[2:]]
    width = len(header_cells)

    def row_to_block(cells: list[str]) -> dict:
        # Auf gleiche Breite padden
        while len(cells) < width:
            cells.append("")
        return {
            "type": "table_row",
            "table_row": {"cells": [parse_inline(c) for c in cells[:width]]},
        }

    children = [row_to_block(header_cells)] + [row_to_block(r) for r in body_rows]

    return {
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": children,
        },
    }


def markdown_to_blocks(md: str) -> list[dict]:
    """Konvertiert Markdown in eine Liste von Notion-Block-Dicts."""
    # Wiki-Links ([[Page|Label]]) vorab zu normalen Markdown-Links umschreiben
    md = convert_wiki_links(md)

    blocks: list[dict] = []
    lines = md.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Leerzeile
        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$|^\*{3,}$|^_{3,}$", stripped):
            blocks.append({"type": "divider", "divider": {}})
            i += 1
            continue

        # Code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # closing ```
            code_content = "\n".join(code_lines)
            # Notion unterstützt nur bestimmte Sprachen
            valid_langs = {
                "bash", "shell", "python", "javascript", "typescript", "json",
                "yaml", "html", "css", "sql", "markdown", "docker", "dockerfile",
                "go", "rust", "java", "c", "c++", "c#", "php", "ruby",
                "plain text",
            }
            lang_norm = lang.lower()
            if lang_norm == "sh":
                lang_norm = "shell"
            if lang_norm not in valid_langs:
                lang_norm = "plain text"
            blocks.append({
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text",
                                   "text": {"content": truncate(code_content)}}],
                    "language": lang_norm,
                },
            })
            continue

        # Heading
        heading_match = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            blocks.append({
                "type": f"heading_{level}",
                f"heading_{level}": {"rich_text": parse_inline(text)},
            })
            i += 1
            continue

        # Blockquote
        if stripped.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append({
                "type": "quote",
                "quote": {"rich_text": parse_inline(" ".join(quote_lines))},
            })
            continue

        # Task-List (GitHub-Style: "- [ ] foo" oder "- [x] foo")
        task_match = re.match(r"^[-*+]\s+\[([ xX])\]\s+(.+)$", stripped)
        if task_match:
            checked = task_match.group(1).lower() == "x"
            text = task_match.group(2)
            blocks.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": parse_inline(text),
                    "checked": checked,
                },
            })
            i += 1
            continue

        # Bulleted list
        if re.match(r"^[-*+]\s+", stripped):
            text = re.sub(r"^[-*+]\s+", "", stripped)
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_inline(text)},
            })
            i += 1
            continue

        # Numbered list
        if re.match(r"^\d+\.\s+", stripped):
            text = re.sub(r"^\d+\.\s+", "", stripped)
            blocks.append({
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": parse_inline(text)},
            })
            i += 1
            continue

        # Table (Header-Zeile mit | erkannt)
        if "|" in stripped and stripped.count("|") >= 2:
            # Prüfen ob nächste Zeile eine Separator-Zeile ist
            if i + 1 < len(lines) and re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$",
                                                lines[i + 1].strip()):
                table_lines = [lines[i], lines[i + 1]]
                j = i + 2
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    table_lines.append(lines[j])
                    j += 1
                table_block = parse_table(table_lines)
                if table_block:
                    blocks.append(table_block)
                    i = j
                    continue

        # Default: Paragraph
        blocks.append({
            "type": "paragraph",
            "paragraph": {"rich_text": parse_inline(stripped)},
        })
        i += 1

    return blocks


# --- Main ---

def slug_to_title(name: str) -> str:
    """'Docker-Container.md' -> 'Docker Container'"""
    return name.replace(".md", "").replace("-", " ").replace("_", " ")


def main() -> int:
    if not WIKI_DIR.exists():
        print(f"ERROR: Wiki-Verzeichnis {WIKI_DIR} nicht gefunden.", file=sys.stderr)
        return 1

    md_files = sorted(WIKI_DIR.glob("*.md"))
    print(f"Gefunden: {len(md_files)} Markdown-Dateien im Wiki")

    # 1. Existierende Child-Pages archivieren (clean slate)
    print("\nArchiviere alte Unterseiten...")
    existing = get_child_pages(PARENT_PAGE_ID)
    for page in existing:
        title = page.get("child_page", {}).get("title", "?")
        print(f"  - Archiviere: {title}")
        archive_page(page["id"])

    # 2. Home.md als Inhalt der Parent-Seite (falls vorhanden)
    home_file = WIKI_DIR / "Home.md"
    if home_file.exists():
        print(f"\nAktualisiere Parent-Seite mit Home.md...")
        home_md = home_file.read_text(encoding="utf-8")
        # Sync-Timestamp voranstellen
        timestamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
        intro = (f"> **Automatisch gespiegelt** aus dem GitHub Wiki.\n"
                 f"> Letzter Sync: {timestamp}\n"
                 f"> Quelle: https://github.com/Bolmir/unraid-nas-docs/wiki\n\n")
        home_blocks = markdown_to_blocks(intro + home_md)
        replace_page_content(PARENT_PAGE_ID, home_blocks)

    # 3. Alle anderen .md-Dateien als Unterseiten anlegen
    print(f"\nErstelle Unterseiten...")
    for md_file in md_files:
        if md_file.name == "Home.md":
            continue
        if md_file.name.startswith("_"):  # _Sidebar.md, _Footer.md
            continue

        title = slug_to_title(md_file.name)
        print(f"  - Erstelle: {title}")
        md = md_file.read_text(encoding="utf-8")
        blocks = markdown_to_blocks(md)
        try:
            create_page(PARENT_PAGE_ID, title, blocks)
        except Exception as e:
            print(f"    FEHLER beim Anlegen von {title}: {e}", file=sys.stderr)

    print("\n✓ Sync abgeschlossen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
