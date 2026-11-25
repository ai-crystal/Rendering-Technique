#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据各册的 structure.json / book.json 生成侧栏、各册首页与系列首页。

运行：python books/build/make_sidebar.py
输出：
    books/<册名>/_sidebar.md
    books/<册名>/README.md
    _sidebar.md
    README.md
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"


def first_heading(path):
    for ln in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^#\s+\S", ln):
            return re.sub(r"^#\s+", "", ln).strip()
    return path.stem


def load_books():
    out = []
    for p in sorted(BOOKS.iterdir()):
        cfgp = p / "book.json"
        stp = p / "structure.json"
        if not (cfgp.exists() and stp.exists()):
            continue
        if not list((p / "chapters").glob("ch*.md")):
            continue
        cfg = json.loads(cfgp.read_text(encoding="utf-8"))
        st = json.loads(stp.read_text(encoding="utf-8"))
        cfg["_dir"] = p
        cfg["_st"] = st
        pdf = ROOT / "output" / cfg.get("pdf", "")
        if pdf.exists():
            try:
                import pymupdf
                with pymupdf.open(pdf) as doc:
                    cfg["pages"] = doc.page_count
            except Exception:
                pass
        out.append(cfg)
    out.sort(key=lambda c: str(c.get("volume_no", "99")))
    return out


def chapters_of(cfg):
    """返回 [(part_title, [(title, path)])]，path 为仓库相对路径。"""
    book = cfg["name"]
    groups, cur = [], None
    for b in cfg["_st"].get("body", []):
        rel = b["file"]
        p = cfg["_dir"] / rel
        if not p.exists():
            continue
        title = first_heading(p)
        if b["type"] == "part":
            cur = (title, [])
            groups.append(cur)
        else:
            if cur is None:
                cur = ("", [])
                groups.append(cur)
            cur[1].append((title, f"books/{book}/{rel}"))
    return groups


def write_book_sidebar(cfg):
    book = cfg["name"]
    lines = []
    front = cfg["_st"].get("front", [])
    for rel in front:
        if rel.endswith("cover.md"):
            continue
        p = cfg["_dir"] / rel
        if p.exists():
            lines.append(f"- [{first_heading(p)}](books/{book}/{rel})")
    lines.append("")

    groups = chapters_of(cfg)
    app = []
    for title, chs in groups:
        if not chs:
            continue
        if title:
            lines.append(f"- **{title}**")
            for t, path in chs:
                lines.append(f"  - [{t}]({path})")
        else:
            for t, path in chs:
                lines.append(f"- [{t}]({path})")
        lines.append("")

    for f in cfg["_st"].get("appendix", []):
        p = cfg["_dir"] / f
        if p.exists():
            app.append((first_heading(p), f"books/{book}/{f}"))
    if app:
        lines.append("- **附录**")
        for t, path in app:
            lines.append(f"  - [{t}]({path})")
        lines.append("")

    for rel in cfg["_st"].get("back", []):
        if rel.endswith("backcover.md"):
            continue
        p = cfg["_dir"] / rel
        if p.exists():
            lines.append(f"- [{first_heading(p)}](books/{book}/{rel})")
    lines.append(f"- [下载 PDF](output/{cfg['pdf']} ':ignore')")
    (cfg["_dir"] / "_sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_book_readme(cfg):
    book = cfg["name"]
    lines = [f"# {cfg['title']}", ""]
    lines.append(f"**{cfg.get('series_title', '专业级渲染技术')} · {cfg.get('volume', '')}**　·　"
                 f"{cfg.get('subtitle', '')}")
    lines.append("")
    lines.append(f"作者：{cfg['author']}　　在线阅读 <https://ai-crystal.github.io/Rendering-Technique/>"
                 f"　　下载：[整本 PDF](../../output/{cfg['pdf']})")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(cfg.get("blurb", "").strip())
    lines.append("")
    lines.append("## 目录")
    lines.append("")
    for title, chs in chapters_of(cfg):
        if not chs:
            continue
        if title:
            lines.append(f"**{title}**")
            lines.append("")
        for t, path in chs:
            lines.append(f"- [{t}](#/{path[:-3].replace('books/', 'books/')})")
        lines.append("")
    lines.append("## 重新生成")
    lines.append("")
    lines.append(f"双击仓库根目录的 `build-{book}.bat`，或运行：")
    lines.append("")
    lines.append("```text")
    lines.append(f"python books/build/build.py --book {book}")
    lines.append("```")
    lines.append("")
    lines.append("## 关于插图")
    lines.append("")
    lines.append("所有插图由 `books/code/` 下对应章节的脚本绘制，没有外部图片，也没有 AI 生成的图。"
                 "性能与对比类曲线由书中给出的公式直接算出，不使用估算数据。")
    lines.append("")
    (cfg["_dir"] / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_root_sidebar(books):
    lines = ["- [首页](/)"]
    lines.append("")
    for cfg in books:
        tag = f"{cfg.get('volume_no', '')}　{cfg.get('volume', '')}"
        lines.append(f"- **{tag} · {cfg['title']}**")
        lines.append(f"  - [本册目录](books/{cfg['name']}/README.md)")
        lines.append(f"  - [下载 PDF](output/{cfg['pdf']} ':ignore')")
        lines.append("")
    lines.append("- [系列说明](SERIES.md)")
    (ROOT / "_sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_root_readme(books):
    L = ["# 专业级渲染技术", ""]
    L.append("**一套写给渲染实现者的材质专题书**　·　Dr. Dezeming")
    L.append("")
    L.append("在线阅读：<https://ai-crystal.github.io/Rendering-Technique/>")
    L.append("")
    L.append("---")
    L.append("")
    L.append("这套书假设你已经写过一个能跑的光线追踪器，知道射线求交、着色和蒙特卡洛积分怎么工作，"
             "也见过 BRDF 和渲染方程。它不打算再教一遍怎么打第一条光线，而是集中在“材质”这一层"
             "最容易含糊的地方：一个材质为什么长成那个公式，公式里的每一项在物理上对应什么，"
             "换到另一种材料上哪些假设会碎掉。")
    L.append("")
    L.append("入门篇把后面几册共用的骨架搭起来：Fresnel、微表面三段式、能量补偿、分层、采样与验证。"
             "各专题册再各自深入一种材料或一种光学现象，彼此独立，可以从任意一本读起。")
    L.append("")
    L.append("光谱那一册从普朗克讲起，把量子描述、相干性、辐亮度、光谱渲染、RGB 看成层层收紧的近似；"
             "蓄水池那一册从 MIS 与带权蓄水池讲起，前半本是可以独立读的采样理论。")
    L.append("")
    L.append("## 分册")
    L.append("")
    L.append("| 册 | 书名 | 一句话 | 页数 | 阅读 | PDF |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for cfg in books:
        pages = cfg.get("pages", "")
        L.append(f"| {cfg.get('volume_no', '')} | {cfg['title']} | {cfg.get('oneline', '')} | "
                 f"{pages} | [阅读](books/{cfg['name']}/README.md) | "
                 f"[下载](output/{cfg['pdf']}) |")
    L.append("")
    L.append("## 怎么读")
    L.append("")
    L.append("入门篇建议按顺序读完，它是后面所有册的公共语言。专题册之间没有依赖，"
             "做布料就读布料那一册，做毛发就读毛发那一册，需要的微表面结论在入门篇第 4 到第 7 章。")
    L.append("")
    L.append("系列内的符号、参数名和代码约定保持一致：$\u03c3_t$ 始终表示消光系数，"
             "$\u03b1$ 始终是粗糙度，$f_r$ 始终是 BSDF，不随分册换写法。")
    L.append("")
    L.append("## 仓库结构")
    L.append("")
    L.append("```text")
    L.append("books/")
    L.append("  build/          构建脚本，全系列共用")
    L.append("  code/           插图脚本，按册、按章分目录")
    L.append("  common/         共用样式与封面生成")
    L.append("  <册名>/")
    L.append("    book.json     这一册的元数据")
    L.append("    structure.json  章节顺序")
    L.append("    chapters/     正文")
    L.append("    front/        封面、扉页、前言、篇首、后记")
    L.append("    images/       插图，按章分目录")
    L.append("output/           各册 PDF")
    L.append("```")
    L.append("")
    L.append("## 重新生成")
    L.append("")
    L.append("双击 `build-<册名>.bat` 只编那一册；`build.bat` 编译全部；"
             "`build.bat figures` 只重画插图。")
    L.append("")
    L.append("## 关于插图")
    L.append("")
    L.append("所有插图由 `books/code/` 下的脚本绘制，没有外部图片，也没有 AI 生成的图。"
             "性能与对比曲线一律由书中给出的公式算出。")
    L.append("")
    (ROOT / "README.md").write_text("\n".join(L), encoding="utf-8")


def main():
    books = load_books()
    for cfg in books:
        write_book_sidebar(cfg)
        write_book_readme(cfg)
        print("侧栏与首页:", cfg["name"])
    write_root_sidebar(books)
    write_root_readme(books)
    print("系列首页与根侧栏完成，共", len(books), "册")


if __name__ == "__main__":
    main()
