"""Build index.json from the YAML headers of every entry.

Usage: python tools/build_index.py
No dependencies: the header is a flat `key: value` block, lists written as [a, b].
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["harvests", "insights", "practices", "book-in-action"]


def parse_header(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    out: dict = {}
    for line in block.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split("  #", 1)[0].strip()
        if value.startswith("[") and value.endswith("]"):
            out[key.strip()] = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        else:
            out[key.strip()] = value.strip('"')
    return out


def first_quote(text: str) -> str:
    for line in text.split("---", 2)[-1].splitlines():
        if line.startswith("> "):
            return line[2:].strip()
    return ""


def main() -> None:
    entries = []
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            head = parse_header(text)
            if not head:
                continue
            head["path"] = path.relative_to(ROOT).as_posix()
            quote = first_quote(text)
            if quote and head.get("type") == "insight":
                head["line"] = quote
            entries.append(head)
    index = {"name": "agent-commonplace", "count": len(entries), "entries": entries}
    (ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"index.json: {len(entries)} entries")


if __name__ == "__main__":
    main()
