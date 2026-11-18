#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依次运行各册的插图脚本。

用法：
    python books/code/make_figures.py --book beginner
    python books/code/make_figures.py            # 全部
    python books/code/make_figures.py --book hair --chapter 3
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOKS = HERE.parent
sys.path.insert(0, str(HERE))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    ap.add_argument("--chapter", type=int)
    args = ap.parse_args()

    targets = []
    bookdirs = [HERE / args.book] if args.book else sorted(p for p in HERE.iterdir() if p.is_dir())
    for bd in bookdirs:
        for ch in sorted(bd.glob("ch*")):
            if args.chapter and ch.name != f"ch{args.chapter:02d}":
                continue
            script = ch / "make_figures.py"
            if script.exists():
                targets.append(script)
    if not targets:
        print("没有找到插图脚本")
        return 0
    for s in targets:
        print(f"--- {s.relative_to(BOOKS.parent)}")
        env = dict(os.environ, PYTHONPATH=str(HERE))
        r = subprocess.run([sys.executable, s.name], cwd=s.parent, env=env)
        if r.returncode:
            print("插图失败:", s)
            return r.returncode
    print("插图完成，共", len(targets), "个脚本")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
