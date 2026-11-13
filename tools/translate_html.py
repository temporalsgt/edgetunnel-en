#!/usr/bin/env python3
"""Translate the visible text of the edgetunnel panel HTML files.

Only user-visible text nodes and a small set of visible attributes are touched.
<script>/<style> contents, ids, classes and internal config keys are left alone.
Translations are cached in tools/panel_translations.json.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "panel" / "public"
CACHE = ROOT / "tools" / "panel_translations.json"
CJK = re.compile(r"[\u3400-\u9fff]")
ATTRS = ("title", "placeholder", "aria-label", "alt", "value")
EMAIL = "edgetunnel.en@gmail.com"
API = "https://api.mymemory.translated.net/get"

# Strings that are internal keys/values and must never be translated.
PROTECTED = {
    "协议类型", "传输协议", "启用0RTT", "跳过证书验证", "TLS分片", "随机路径",
    "连接复用", "优选订阅生成", "本地IP库", "随机数量", "指定端口",
    "订阅名称", "订阅转换", "节点协议", "加密方式", "代理协议",
    "gRPC模式", "gRPCUserAgent", "ECHConfig", "SS", "CF", "TG",
}

cache: dict[str, str] = {}
if CACHE.exists():
    cache = json.loads(CACHE.read_text(encoding="utf-8"))


def translate_batch(items: list[str]) -> list[str]:
    """Translate strings while preserving one output line per input line."""
    if not items:
        return []
    q = "\n".join(items)
    params = urllib.parse.urlencode({"q": q, "langpair": "zh-CN|en", "de": EMAIL})
    url = f"{API}?{params}"
    proc = subprocess.run(
        ["curl", "-sS", "--max-time", "25", "-A", "edgetunnel-en/1.0", url],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl exit {proc.returncode}: {proc.stderr.strip()[:200]}")
    data = json.loads(proc.stdout)
    text = (data.get("responseData") or {}).get("translatedText") or ""
    lines = text.split("\n")
    if len(lines) != len(items):
        raise RuntimeError(f"line count mismatch: sent {len(items)}, got {len(lines)}")
    return [x.strip() for x in lines]


def translate_missing(strings: set[str]) -> None:
    todo = [s for s in strings if s not in cache and s.strip()]
    if not todo:
        return
    # Keep requests comfortably below URL limits. Chinese text expands to
    # roughly 9 bytes per character once URL-encoded, so stay small.
    batch: list[str] = []
    size = 0
    batches: list[list[str]] = []
    for s in todo:
        if len(s) > 260:
            batches.append([s])
            continue
        if batch and (size + len(s) + 1 > 280 or len(batch) >= 20):
            batches.append(batch)
            batch, size = [], 0
        batch.append(s)
        size += len(s) + 1
    if batch:
        batches.append(batch)

    for i, b in enumerate(batches, 1):
        preview = " | ".join(x.replace("\n", " ")[:40] for x in b[:2])
        print(f"  requesting batch {i}/{len(batches)} ({len(b)} strings): {preview}", flush=True)
        ok = False
        for attempt in range(2):
            try:
                translated = translate_batch(b)
                for src, dst in zip(b, translated):
                    if dst and dst != src:
                        cache[src] = dst
                print(f"  batch {i}/{len(batches)}: {len(b)} strings", flush=True)
                ok = True
                break
            except Exception as e:  # noqa: BLE001
                print(f"  batch {i} attempt {attempt + 1} failed: {e}", file=sys.stderr, flush=True)
                time.sleep(1.0 + attempt)
        if not ok:
            # MyMemory sometimes collapses multi-line input into one line.
            # Fall back to one request per string, caching after each success.
            print(f"  batch {i}: falling back to one-by-one", file=sys.stderr, flush=True)
            for src in b:
                if src in cache:
                    continue
                for attempt in range(2):
                    try:
                        dst = translate_batch([src])[0]
                        if dst and dst != src:
                            cache[src] = dst
                        break
                    except Exception as e:  # noqa: BLE001
                        print(f"    single failed ({attempt + 1}): {e}", file=sys.stderr, flush=True)
                        time.sleep(0.8)
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
                time.sleep(0.15)
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        time.sleep(0.2)


def collect_and_translate(path: Path) -> None:
    raw = path.read_text(encoding="utf-8-sig")
    soup = BeautifulSoup(raw, "html.parser")

    text_nodes: list[NavigableString] = []
    attr_nodes: list[tuple[Tag, str, str]] = []
    strings: set[str] = set()

    for node in soup.find_all(string=True):
        if isinstance(node, Comment):
            continue
        parent = node.parent
        if parent and parent.name in ("script", "style"):
            continue
        text = str(node)
        if not CJK.search(text):
            continue
        stripped = text.strip()
        if not stripped or stripped in PROTECTED:
            continue
        strings.add(stripped)
        text_nodes.append(node)

    for tag in soup.find_all(True):
        for attr in ATTRS:
            val = tag.get(attr)
            if not isinstance(val, str) or not CJK.search(val):
                continue
            stripped = val.strip()
            if not stripped or stripped in PROTECTED:
                continue
            strings.add(stripped)
            attr_nodes.append((tag, attr, val))

    print(f"{path.relative_to(ROOT)}: {len(text_nodes)} text nodes, {len(attr_nodes)} attrs, {len(strings)} unique", flush=True)
    translate_missing(strings)

    changed = 0
    for node in text_nodes:
        text = str(node)
        m = re.match(r"^(\s*)(.*?)(\s*)$", text, re.S)
        if not m:
            continue
        lead, core, trail = m.groups()
        if core in cache:
            node.replace_with(NavigableString(lead + cache[core] + trail))
            changed += 1

    for tag, attr, old in attr_nodes:
        core = old.strip()
        if core in cache:
            tag[attr] = old.replace(core, cache[core], 1)
            changed += 1

    out = str(soup)
    if not out.startswith("<!DOCTYPE"):
        out = "<!DOCTYPE html>\n" + out
    path.write_text(out, encoding="utf-8")
    print(f"  applied {changed} translations -> {path.relative_to(ROOT)}")


def main() -> None:
    files = [
        PUBLIC / "admin" / "index.html",
        PUBLIC / "login" / "index.html",
        PUBLIC / "noADMIN" / "index.html",
        PUBLIC / "noKV" / "index.html",
        PUBLIC / "index.html",
    ]
    for path in files:
        collect_and_translate(path)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(f"cache: {len(cache)} entries -> {CACHE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
