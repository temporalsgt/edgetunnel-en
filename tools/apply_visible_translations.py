#!/usr/bin/env python3
"""Apply tools/visible_translations.merged.json to the visible text of the panel HTML."""
from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "panel" / "public"
MAP_PATH = ROOT / "tools" / "visible_translations.merged.json"
CJK = re.compile(r"[\u3400-\u9fff]")
ATTRS = ("title", "placeholder", "aria-label", "alt", "value")

mapping: dict[str, str] = json.loads(MAP_PATH.read_text(encoding="utf-8"))
missing: set[str] = set()


def apply(path: Path) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8-sig"), "html.parser")

    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment):
            continue
        if node.parent and node.parent.name in ("script", "style"):
            continue
        text = str(node)
        if not CJK.search(text):
            continue
        m = re.match(r"^(\s*)(.*?)(\s*)$", text, re.S)
        if not m:
            continue
        lead, core, trail = m.groups()
        if core in mapping:
            node.replace_with(NavigableString(lead + mapping[core] + trail))
        else:
            missing.add(core)

    for tag in soup.find_all(True):
        for attr in ATTRS:
            val = tag.get(attr)
            if not isinstance(val, str) or not CJK.search(val):
                continue
            core = val.strip()
            if core in mapping:
                tag[attr] = val.replace(core, mapping[core], 1)
            else:
                missing.add(core)

    out = str(soup)
    if not out.startswith("<!DOCTYPE"):
        out = "<!DOCTYPE html>\n" + out
    path.write_text(out, encoding="utf-8")
    print(f"applied -> {path.relative_to(ROOT)}")


def main() -> None:
    for rel in [
        "admin/index.html",
        "login/index.html",
        "noADMIN/index.html",
        "noKV/index.html",
        "index.html",
    ]:
        apply(PUBLIC / rel)
    if missing:
        out = ROOT / "tools" / "visible_missing.json"
        out.write_text(json.dumps(sorted(missing), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"missing {len(missing)} strings -> {out.relative_to(ROOT)}")
    else:
        print("no missing visible strings")


if __name__ == "__main__":
    main()
