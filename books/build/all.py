#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按顺序构建所有已成稿的分册，然后刷新首页与侧栏。

用法：
    python books/build/all.py            # 体检 + 构建 + 刷新导航
    python books/build/all.py --check    # 只体检
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
BOOKS = HERE.parent
ROOT = BOOKS.parent
PY = sys.executable


def load_books():
    out = []
    for p in BOOKS.iterdir():
        if not (p / "book.json").exists() or not (p / "structure.json").exists():
            continue
        if not list((p / "chapters").glob("ch*.md")):
            continue
        cfg = json.loads((p / "book.json").read_text(encoding="utf-8"))
        cfg["_dir"] = p
        out.append(cfg)
    out.sort(key=lambda c: str(c.get("volume_no", "99")))
    return out


def run(cmd):
    return subprocess.run([PY] + cmd, cwd=ROOT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    books = load_books()
    rows = []
    for cfg in books:
        name = cfg["name"]
        print(f"===== {name} =====", flush=True)
        if args.check:
            rc = run(["books/build/build.py", "--book", name, "--check-only"])
        else:
            rc = run(["books/build/build.py", "--book", name, "--passes", "3"])
        pdf = ROOT / "output" / cfg.get("pdf", "")
        pages = 0
        size = 0.0
        if pdf.exists():
            with pymupdf.open(pdf) as doc:
                pages = doc.page_count
            size = pdf.stat().st_size / 1e6
            cfg["pages"] = pages
            (cfg["_dir"] / "book.json").write_text(
                json.dumps({k: v for k, v in cfg.items() if not k.startswith("_")},
                           ensure_ascii=False, indent=2), encoding="utf-8")
        rows.append((cfg.get("volume_no", ""), cfg["title"], pages, size, "OK" if rc == 0 else "FAIL"))

    print("\n===== 汇总 =====")
    for no, title, pages, size, st in rows:
        print(f"{no}  {title:12s}  {pages:3d} 页  {size:5.1f} MB  {st}")
    if not args.check:
        run(["books/build/make_sidebar.py"])


if __name__ == "__main__":
    main()
