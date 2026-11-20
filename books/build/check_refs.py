#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查各册正文里有没有指向其他分册的引用。

用法：
    python books/build/check_refs.py            # 全部检查
    python books/build/check_refs.py cloth      # 只查一册

每本书要能单独出版，正文里不能出现“另一册”“入门篇第 3 章”这类指路。
封面、扉页、版权页上的分册标签（专题三、入门篇）不算，那是这本书自己的标识。
"""
import re
import sys
from pathlib import Path

BOOKS = Path(__file__).resolve().parents[1]

PATTERNS = [
    (r"那一册", "指向另一本"),
    (r"另一册", "指向另一本"),
    (r"这本册", "分册说法"),
    (r"每册", "分册说法"),
    (r"各册", "分册说法"),
    (r"分册", "分册说法"),
    (r"专题册", "分册说法"),
    (r"入门篇", "指向入门册"),
    (r"本系列", "系列说法"),
    (r"这套书", "系列说法"),
    (r"后面[八九]册", "指向后续分册"),
    (r"其余[七八]个专题", "列举其他分册"),
    (r"《[^》]*渲染》", "引用另一本的书名"),
]

SKIP = ("titlepage.md", "copyright.md")


def check_book(book):
    problems = []
    files = []
    for sub in ("chapters", "front", "appendix"):
        d = book / sub
        if d.exists():
            files += sorted(d.glob("*.md"))
    for f in files:
        if f.name in SKIP:
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for pat, why in PATTERNS:
                m = re.search(pat, line)
                if m:
                    problems.append((f.relative_to(BOOKS.parent), i, m.group(0), why, line.strip()[:60]))
    return problems


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    books = [b for b in sorted(BOOKS.iterdir()) if (b / "book.json").exists()]
    if only:
        books = [b for b in books if b.name == only]
    total = 0
    for b in books:
        probs = check_book(b)
        total += len(probs)
        if probs:
            print(f"== {b.name}")
            for f, i, word, why, ctx in probs:
                print(f"  {f}:{i}  [{word}] {why} —— {ctx}")
    print("未发现跨册引用" if total == 0 else f"共 {total} 处")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
