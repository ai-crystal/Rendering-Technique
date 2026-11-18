#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按清单下载各册参考的论文 PDF 到 paper/<册名>/。

用法：python books/common/fetch_papers.py [--book 册名] [--list]
清单在 paper/manifest.txt，每行：册名<TAB>文件名<TAB>URL
支持断点续传，失败会重试；文件必须是完整 PDF 才保留。
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
MANIFEST = PAPER / "manifest.txt"


def looks_like_pdf(path):
    try:
        with open(path, "rb") as f:
            head = f.read(5)
            if head != b"%PDF-":
                return False
            f.seek(-2048, 2)
            tail = f.read()
        return b"%%EOF" in tail
    except OSError:
        return False


def fetch(url, dest, tries=4):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and looks_like_pdf(dest):
        return "skip"
    for i in range(tries):
        cmd = ["curl", "-sL", "-C", "-", "--max-time", "300",
               "--retry", "3", "--retry-all-errors", "-o", str(dest), url]
        subprocess.run(cmd)
        if dest.exists() and looks_like_pdf(dest):
            return "ok"
    if dest.exists():
        dest.unlink()
    return "fail"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if not MANIFEST.exists():
        print("没有 paper/manifest.txt")
        return 1
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        rows.append(parts)
    if args.list:
        for b, name, url in rows:
            print(f"{b:12s} {name}")
        return 0
    ok = fail = skip = 0
    for b, name, url in rows:
        if args.book and b != args.book:
            continue
        dest = PAPER / b / name
        r = fetch(url, dest)
        print(f"[{r}] {b}/{name}")
        ok += r == "ok"
        skip += r == "skip"
        fail += r == "fail"
    print(f"完成：新增 {ok}，已存在 {skip}，失败 {fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
