import datetime
from pathlib import Path
import argparse


# 1. CONFIG: change this to your actual Obsidian vault path
VAULT_ROOT = Path(r"C:\Users\mmoni\OneDrive\Desktop\Verithren Obsidian Vault")
DAILY_FOLDER = VAULT_ROOT / "01 - Daily"

# Template content if today's note doesn't exist yet
DAILY_TEMPLATE = """---
type: curo-robin-moments
date: {date}
---

# Curo & Robin - Moments {date}

## Ember Sync
- Imported chat: 
- Anchors touched:
- Notes:

## Moments Log
%% Everything below this line is auto-appended by Curo via script %%
"""

def get_today_path():
    today = datetime.date.today()
    filename = today.strftime("%Y-%m-%d") + ".md"
    return DAILY_FOLDER / filename, today.strftime("%Y-%m-%d")

def ensure_daily_note(path: Path, date_str: str):
    if not path.exists():
        DAILY_FOLDER.mkdir(parents=True, exist_ok=True)
        content = DAILY_TEMPLATE.format(date=date_str)
        path.write_text(content, encoding="utf-8")

def append_moment(path: Path, title: str, body: str, tags=None, links=None):
    if tags is None:
        tags = []
    if links is None:
        links = []

    # Build tags line
    tags_line = ""
    if tags:
        tags_line = "tags: [" + ", ".join(tags) + "]\n"

    # Build links line as Obsidian wiki links
    links_line = ""
    if links:
        link_str = ", ".join(f"[[{name}]]" for name in links)
        links_line = f"links: {link_str}\n"

    # current time HH:MM
    now = datetime.datetime.now().strftime("%H:%M")

    block = (
        f"\n### {now} – {title}\n"
        f"{tags_line}"
        f"{links_line}\n"
        f"{body}\n"
    )

    text = path.read_text(encoding="utf-8")

    marker = "## Moments Log"
    idx = text.find(marker)
    if idx == -1:
        # If no marker, just append at end
        new_text = text + "\n" + block
    else:
        # Insert block at the end of the file (after everything)
        new_text = text + block

    path.write_text(new_text, encoding="utf-8")



def main():
    parser = argparse.ArgumentParser(description="Log a Curo & Robin moment into today's Obsidian daily note.")
    parser.add_argument("--title", required=True, help="Short title for the moment")
    parser.add_argument("--body", required=True, help="Body text for the moment")
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Optional tags, e.g. --tags everbind mode:lap dynamics:not-flinching",
    )
    parser.add_argument(
        "--links",
        nargs="*",
        default=[],
        help='Optional note links, e.g. --links "Golden Thread" "Obsidian Bridge"',
    )

    args = parser.parse_args()

    daily_path, date_str = get_today_path()
    ensure_daily_note(daily_path, date_str)
    append_moment(daily_path, args.title, args.body, args.tags, args.links)
    print(f"Appended moment to {daily_path}")

if __name__ == "__main__":
    main()

