#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把某一册的 Markdown 编译成 output/<pdf>.pdf。

用法：
    python books/build/build.py --book beginner
    python books/build/build.py --book cloth --no-opt      # 跳过图片压缩
    python books/build/build.py --book hair --no-pdf       # 只出 HTML，便于预览
    python books/build/build.py --check-only --book sss    # 只体检

流程：体检 -> 保护公式 -> Markdown 转 HTML -> 拼封面/目录/正文
      -> KaTeX 渲染 -> Chrome 无头打印 -> 补页码与书签 -> 压缩
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
import pymupdf

HERE = Path(__file__).resolve().parent          # books/build
BOOKS = HERE.parent                             # books
ROOT = BOOKS.parent                             # 仓库根
OUT = ROOT / "output"
ASSETS = HERE / "assets"
TMP = HERE / "_out"

CSS = r"""
@page { size: A4; margin: 17mm 15mm 15mm 15mm; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Source Han Serif SC", "Noto Serif SC", "Songti SC", "SimSun", serif;
  font-size: 9.9pt; line-height: 1.58; color: #1a1a1a; margin: 0;
  text-align: left;
}
p { margin: 0 0 0.35em 0; text-indent: 2em; }
li p, td p, blockquote p { text-indent: 0; }
h1, h2, h3, h4 {
  font-family: "Source Han Sans SC", "Microsoft YaHei", "SimHei", sans-serif;
  color: #111; line-height: 1.35; page-break-after: avoid;
}
h1 { font-size: 19pt; margin: 0 0 0.9em 0; padding-bottom: 0.32em;
     border-bottom: 2pt solid #23262b; page-break-before: always; }
h2 { font-size: 13pt; margin: 1.0em 0 0.35em 0; padding-left: 0.5em;
     border-left: 4pt solid ACCENT; }
h3 { font-size: 11.2pt; margin: 0.95em 0 0.3em 0; color: #202a36; }
h4 { font-size: 10.2pt; margin: 0.8em 0 0.25em 0; color: #33404f; }
strong { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif; }
em { font-style: normal; text-emphasis: dot; text-emphasis-position: under right; }

.katex { font-size: 1.08em; }
.katex-display { margin: 0.5em 0; }

pre { background: #f6f7f8; border: 0.6pt solid #dcdfe3; border-radius: 2pt;
      padding: 0.5em 0.65em; font-size: 8.1pt; line-height: 1.42;
      page-break-inside: avoid; text-align: left; }
code { font-family: "Cascadia Mono", "Consolas", monospace; font-size: 0.88em;
       background: #f2f3f5; padding: 0 0.16em; }
pre code { background: none; padding: 0; font-size: 1em; }

table { border-collapse: collapse; width: 100%; margin: 0.65em 0;
        font-size: 9.1pt; line-height: 1.48; page-break-inside: avoid; }
th, td { border: 0.5pt solid #c9ccd1; padding: 0.26em 0.44em;
         text-align: left; vertical-align: top; }
th { background: #eef1f5; font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif; }

blockquote { margin: 0.7em 0; padding: 0.4em 0.85em; border-left: 3pt solid #9aa7b4;
             background: #f7f8fa; font-size: 0.97em; }
blockquote p { text-indent: 0; }

figure { margin: 0.75em 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; }
figcaption { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
             font-size: 8.7pt; color: #333; margin-top: 0.55em; text-indent: 0;
             line-height: 1.45; }
img { max-width: 100%; }

ul, ol { margin: 0.3em 0 0.65em 0; padding-left: 1.55em; }
li { margin-bottom: 0.2em; }
hr { border: none; border-top: 0.6pt solid #d6d9dd; margin: 1.3em 0; }
a { color: #2b4f81; text-decoration: none; }

/* 封面 */
.cover { page-break-after: always; position: relative; width: 100%; margin: 0; }
.cover img.bg { display: block; width: 100%; height: auto; }

/* 扉页、版权页 */
.titlepage { page-break-after: always; text-align: center; padding-top: 52mm; }
.titlepage .series { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-size: 10pt; letter-spacing: 5pt; color: #6d7885; }
.titlepage .vol { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-size: 11pt; letter-spacing: 3pt; color: ACCENT; margin-top: 8mm; }
.titlepage .t { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-size: 25pt; font-weight: 700; margin-top: 6mm; }
.titlepage .s { font-size: 13pt; color: #3a3a3a; margin-top: 6mm; }
.titlepage .rule { width: 40mm; border-top: 2pt solid ACCENT; margin: 12mm auto 0 auto; }
.titlepage .a { font-size: 11.5pt; margin-top: 34mm; }
.titlepage .m { font-size: 9.5pt; color: #666; margin-top: 6mm; }
.copyright { page-break-after: always; font-size: 9.4pt; color: #333; padding-top: 150mm; }
.copyright p { text-indent: 0; margin-bottom: 0.4em; }

/* 分部页 */
.part { page-break-before: always; page-break-after: always; padding-top: 78mm; }
.part .n { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-size: 10.5pt; letter-spacing: 6pt; color: #6d7885; }
.part .t { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-size: 26pt; font-weight: 700; margin-top: 4mm; letter-spacing: 1.5pt; }
.part .r { width: 42mm; border-top: 2pt solid ACCENT; margin: 6mm 0 7mm 0; }
.part p { font-size: 10.2pt; color: #2b3540; }

/* 封底 */
.backcover { page-break-before: always; position: relative; width: 100%; margin: 0; }
.backcover img.bg { display: block; width: 100%; height: auto; }

/* 目录 */
.toc { page-break-after: always; }
.toc h1 { page-break-before: avoid; }
.toc .l0 { font-family: "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  font-weight: 700; font-size: 10.4pt; margin: 0.5em 0 0.1em 0; }
.toc .l1 { font-size: 9.5pt; margin-left: 0; }
.toc .l2 { font-size: 9.1pt; margin-left: 1.7em; color: #333; }
.toc .row { display: flex; align-items: baseline; line-height: 1.30; }
.toc .dots { flex: 1; border-bottom: 0.5pt dotted #b8bcc2; margin: 0 0.35em;
  transform: translateY(-0.18em); }
.toc .pg { font-variant-numeric: tabular-nums; }
.toc a { color: inherit; }
.pmark { font-size: 0.5pt; color: #ffffff; }
"""


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------- 配置

def load_book(name):
    book = BOOKS / name
    cfg_path = book / "book.json"
    if not cfg_path.exists():
        raise SystemExit(f"找不到 {cfg_path}")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["dir"] = book
    cfg["name"] = name
    st_path = book / "structure.json"
    if st_path.exists():
        cfg["structure"] = json.loads(st_path.read_text(encoding="utf-8"))
    else:
        cfg["structure"] = {"front": [], "body": [], "back": []}
    cfg.setdefault("author", "Dr. Dezeming")
    cfg.setdefault("year", "2026")
    cfg.setdefault("accent", "#b5651d")
    cfg.setdefault("toc_sections", True)
    cfg.setdefault("series_title", "专业级渲染技术")
    return cfg


# ---------------------------------------------------------------- 体检

BAD_HEADING = re.compile(r"[\\${}%^~&|<>#\[\]]")


def preflight(cfg):
    book = cfg["dir"]
    errs, warns = [], []
    st = cfg["structure"]
    files = list(st.get("front", [])) + [b["file"] for b in st.get("body", [])] + list(st.get("back", []))
    if not files:
        errs.append("structure.json 里没有任何文件")
    for rel in files:
        p = book / rel
        if not p.exists():
            errs.append(f"缺文件 {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        # 代码围栏配对
        fences = len(re.findall(r"(?m)^\s*```", text))
        if fences % 2:
            errs.append(f"{rel} 代码围栏数量为奇数（{fences}），可能有一个代码块没闭合")
        # 必须有一个一级标题
        if not re.search(r"(?m)^#\s+\S", text):
            warns.append(f"{rel} 没有一级标题")
        for ln in text.split("\n"):
            if re.match(r"^#{1,6}\s", ln):
                title = re.sub(r"^#+\s*", "", ln)
                if BAD_HEADING.search(title):
                    errs.append(f"{rel} 标题含特殊字符，可能编译出错：{title[:40]}")
        # 图片引用
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
            src = m.group(1).split()[0]
            if src.startswith("http"):
                warns.append(f"{rel} 引用远程图片 {src}")
                continue
            ip = (book / "chapters" / src).resolve()
            if not ip.exists():
                errs.append(f"{rel} 图片不存在：{src}")
        # 图号与章号一致性
        cm = re.search(r"ch(\d+)\.md$", rel)
        if cm:
            chno = int(cm.group(1))
            for m in re.finditer(r"!\[图\s*(\d+)-", text):
                if int(m.group(1)) != chno:
                    warns.append(f"{rel} 图号前缀 {m.group(1)} 与章号 {chno} 不一致")
    return errs, warns


# ---------------------------------------------------------------- Markdown

def protect_math(text):
    store = []

    def blk(m):
        store.append((True, m.group(1)))
        return f"\ue000{len(store)-1}\ue001"

    def inl(m):
        store.append((False, m.group(1)))
        return f"\ue000{len(store)-1}\ue001"

    text = re.sub(r"\$\$(.+?)\$\$", blk, text, flags=re.S)
    text = re.sub(r"(?<!\\)\$(?!\s)([^\n$]+?)(?<!\s)\$(?!\d)", inl, text)
    return text, store


def restore_math(html_text, store):
    def rep(m):
        idx = int(m.group(1))
        display, body = store[idx]
        body = html.escape(body, quote=False)
        if display:
            return f'<div class="displaymath">$${body}$$</div>'
        return f"${body}$"

    return re.sub(r"\ue000(\d+)\ue001", rep, html_text)


def md2html(text, md):
    text, store = protect_math(text)
    out = md.convert(text)
    return restore_math(out, store)


TOC_SKIP = ("本章小结", "延伸阅读", "小结", "本章要点")


def headings(text, with_sections=True):
    out, fence = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,2})\s+(.*\S)\s*$", ln)
        if m:
            lvl, title = len(m.group(1)), m.group(2).strip()
            title = re.sub(r"[`*]", "", title)
            if title in TOC_SKIP:
                continue
            if lvl == 2 and not with_sections:
                continue
            out.append((lvl, title))
    return out


MARKERS = []


def slug(s):
    return re.sub(r"[^\w\u4e00-\u9fff]+", "-", s)[:40]


def find_chrome():
    for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]:
        if Path(c).exists():
            return c
    raise RuntimeError("找不到 Chrome / Edge")


def print_pdf(html_path, pdf_path):
    chrome = find_chrome()
    profile = tempfile.mkdtemp(prefix="pdf-")
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--user-data-dir={profile}", "--no-pdf-header-footer",
           "--virtual-time-budget=180000", "--run-all-compositor-stages-before-draw",
           f"--print-to-pdf={pdf_path}", html_path.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=3600)
    shutil.rmtree(profile, ignore_errors=True)
    if not pdf_path.exists():
        log(r.stdout[-2000:])
        log(r.stderr[-2000:])
        raise RuntimeError("PDF 生成失败")


def prepare_images(cfg, do_opt=True):
    """把 PNG 转成 JPEG，控制 PDF 体积。"""
    from PIL import Image
    book = cfg["dir"]
    out_dir = TMP / cfg["name"] / "img"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    mapping = {}
    for p in sorted((book / "images").glob("*/*.png")):
        dst = out_dir / p.parent.name
        dst.mkdir(exist_ok=True)
        jpg = dst / (p.stem + ".jpg")
        im = Image.open(p).convert("RGB")
        if do_opt and im.width > 1000:
            im = im.resize((1000, int(im.height * 1000 / im.width)), Image.LANCZOS)
        im.save(jpg, "JPEG", quality=82 if do_opt else 95, optimize=True, progressive=True)
        mapping[p] = jpg
    return mapping


def build_document(cfg, front, toc, page_map, body_pages, html_path):
    toc_html = ['<div class="toc"><h1 style="page-break-before:avoid">目 录</h1><span class="pmark">§S§</span>']
    for lvl, title, anchor in toc:
        cls = {0: "l0", 1: "l1", 2: "l2", 3: "l2"}[lvl]
        pg = page_map.get(anchor, "")
        toc_html.append(
            f'<div class="{cls}"><div class="row"><span><a href="#{anchor}">{html.escape(title)}</a></span>'
            f'<span class="dots"></span><span class="pg">{pg}</span></div></div>')
    toc_html.append('<span class="pmark">§E§</span></div>')

    front_html = "\n".join(front)
    body = "\n".join(body_pages)
    css = CSS.replace("ACCENT", cfg["accent"])
    doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{html.escape(cfg['title'])}</title>
<link rel="stylesheet" href="{(ASSETS/'katex.min.css').as_uri()}">
<script src="{(ASSETS/'katex.min.js').as_uri()}"></script>
<script src="{(ASSETS/'auto-render.min.js').as_uri()}"></script>
<style>{css}</style></head><body>
{front_html}{''.join(toc_html)}{body}
<script>
renderMathInElement(document.body, {{
  delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}],
  throwOnError: false,
  ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
  onError: function (msg) {{ console.error(msg); }}
}});
document.querySelectorAll('.katex-mathml').forEach(function (e) {{ e.remove(); }});
</script>
</body></html>"""
    html_path.write_text(doc, encoding="utf-8")


def measure(pdf_path):
    doc = pymupdf.open(pdf_path)
    idx_page, toc_end, toc_start = {}, None, None
    for page in doc:
        try:
            txt = page.get_text("text")
        except Exception:
            continue
        for idx in re.findall(r"§\s*(\d+)\s*§", txt):
            idx_page.setdefault(int(idx), page.number + 1)
        if toc_start is None and "§S§" in txt:
            toc_start = page.number + 1
        if "§E§" in txt:
            toc_end = page.number + 1
    doc.close()
    return ({MARKERS[i]: pg for i, pg in idx_page.items() if i < len(MARKERS)},
            toc_start, toc_end)


def finalize(pdf_path, toc, page_map, toc_start, toc_end):
    doc = pymupdf.open(pdf_path)
    start = (toc_end or 4) + 1
    for i in range(start, doc.page_count - 1):
        r = doc[i].rect
        doc[i].insert_text(pymupdf.Point(r.width / 2 - 8, r.height - 26), str(i + 1),
                           fontname="helv", fontsize=9, color=(0.3, 0.3, 0.3))
    outline = [[1, "封面", 1], [1, "扉页", 2], [1, "目录", toc_start or 3]]
    for lvl, title, anchor in toc:
        if anchor in page_map:
            outline.append([max(1, min(lvl, 3)), title, page_map[anchor]])
    doc.set_toc(outline)
    try:
        n = doc.subset_fonts()
        log(f"  字体子集: {n}")
    except Exception as e:
        log(f"  subset_fonts skipped: {e}")
    doc.saveIncr()
    doc.close()

    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc = pymupdf.open(pdf_path)
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    tmp.replace(pdf_path)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--no-opt", action="store_true")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--passes", type=int, default=3)
    args = ap.parse_args()

    cfg = load_book(args.book)
    book = cfg["dir"]
    log(f"===== {cfg.get('volume', '')} {cfg['title']} =====")

    errs, warns = preflight(cfg)
    for w in warns:
        log("  [警告] " + w)
    if errs:
        for e in errs:
            log("  [错误] " + e)
        raise SystemExit(f"体检未通过，共 {len(errs)} 项错误")
    log("体检通过")
    if args.check_only:
        return

    st = cfg["structure"]
    output_name = cfg.get("pdf") or f"{cfg['name']}.pdf"
    OUT.mkdir(exist_ok=True)
    (TMP / cfg["name"]).mkdir(parents=True, exist_ok=True)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "attr_list", "md_in_html"])
    imgs = prepare_images(cfg, do_opt=not args.no_opt)

    pages, front, toc = [], [], []
    MARKERS.clear()
    kinds = {f: "front" for f in st.get("front", [])}
    for b in st.get("body", []):
        kinds[b["file"]] = b["type"]
    for f in st.get("back", []):
        kinds[f] = "back"

    order = [(f, "front") for f in st.get("front", [])]
    for b in st.get("body", []):
        order.append((b["file"], b["type"]))
    for f in st.get("back", []):
        order.append((f, "back"))

    for rel, kind in order:
        path = book / rel
        raw = path.read_text(encoding="utf-8")
        anchor = "doc-" + slug(rel.replace("/", "-"))
        basename = path.name

        if basename in ("cover.md", "backcover.md"):
            body = re.sub(r'src="\.\./images/([^"]+)"',
                          lambda m: f'src="{(book / "images" / m.group(1)).as_uri()}"', raw)
            cls = "cover" if basename == "cover.md" else "backcover"
            frag = f'<section class="{cls}" id="{anchor}">{body}</section>'
            if basename == "cover.md":
                front.append(frag)
            else:
                pages.append(frag)
            continue

        if basename in ("titlepage.md", "copyright.md"):
            body = md2html(raw, md)
            front.append(f'<section class="{kind}" id="{anchor}">{body}</section>')
            continue

        if kind == "part":
            body = md2html(raw, md)
            head = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)
            MARKERS.append(anchor)
            mark = f'<span class="pmark">§{len(MARKERS)-1}§</span>'
            if head:
                title = re.sub(r"<[^>]+>", "", head.group(1)).strip()
                seg = re.split(r"[\u3000\s]+", title, maxsplit=1)
                number = seg[0]
                name = seg[1] if len(seg) > 1 else ""
                block = (f'<div class="n">{number}</div>'
                         f'<div class="t">{name}</div><div class="r"></div>')
                body = body.replace(head.group(0), block + mark)
            pages.append(f'<section class="part" id="{anchor}">{body}</section>')
            toc.append((0, raw.split("\n")[0].lstrip("# ").strip(), anchor))
            continue

        heads = headings(raw, with_sections=cfg.get("toc_sections", True))
        local = []
        rest = heads
        if heads and heads[0][0] == 1:
            local.append((1, anchor))
            toc.append((1 if kind == "part" else 2, heads[0][1], anchor))
            rest = heads[1:]
        for lvl, title in rest:
            a = f"{anchor}-{slug(title)}"
            local.append((2 if lvl == 2 else 1, a))
            toc.append((3 if lvl == 2 else 2, title, a))

        body = md2html(raw, md)
        it = iter([a for lv, a in local])

        def mark(aid):
            MARKERS.append(aid)
            return f'<span class="pmark">§{len(MARKERS)-1}§</span>'

        def add_id(m):
            lvl, attrs, inner = m.group(1), m.group(2), m.group(3)
            try:
                aid = next(it)
            except StopIteration:
                return m.group(0)
            return f'<h{lvl}{attrs} id="{aid}">{inner}{mark(aid)}</h{lvl}>'

        body = re.sub(r"<h([12])([^>]*)>(.*?)</h\1>", add_id, body, flags=re.S)

        def fix_img(m):
            alt, src = m.group(1), m.group(2)
            p = (path.parent / src).resolve()
            jpg = imgs.get(p, p)
            return (f'<figure><img src="{jpg.as_uri()}" alt="{alt}">'
                    f'<figcaption>{alt}</figcaption></figure>')

        body = re.sub(r'<p>\s*<img\s+alt="([^"]*)"\s+src="([^"]+)"\s*/?>\s*</p>', fix_img, body, flags=re.S)
        body = re.sub(r'<img\s+alt="([^"]*)"\s+src="([^"]+)"\s*/?>', fix_img, body)

        def rel_link(m):
            href = m.group(1)
            target = (path.parent / href).resolve()
            try:
                relp = target.relative_to(book).as_posix()
            except ValueError:
                return m.group(0)
            return f'href="#doc-{slug(relp.replace("/", "-"))}"'

        body = re.sub(r'href="([^"#]+\.md)"', rel_link, body)
        pages.append(f'<section id="{anchor}">{body}</section>')

    html_path = TMP / cfg["name"] / "book.html"
    if args.no_pdf:
        build_document(cfg, front, toc, {}, pages, html_path)
        log(f"HTML: {html_path}")
        return

    page_map, toc_start, toc_end = {}, None, None
    pdf_path = OUT / output_name
    for it in range(args.passes):
        build_document(cfg, front, toc, page_map, pages, html_path)
        if pdf_path.exists():
            pdf_path.unlink()
        log(f"[{it+1}/{args.passes}] 打印 PDF ...")
        print_pdf(html_path, pdf_path)
        new_map, toc_start, toc_end = measure(pdf_path)
        changed = sum(1 for k, v in new_map.items() if page_map.get(k) != v)
        n_page = pymupdf.open(pdf_path).page_count
        log(f"    页数 {n_page}，页码定位 {len(new_map)}，变动 {changed}")
        page_map = new_map
        if changed == 0:
            break

    log(f"打印完成: {pdf_path.stat().st_size/1e6:.1f} MB")
    finalize(pdf_path, toc, page_map, toc_start, toc_end)
    size_mb = pdf_path.stat().st_size / 1e6
    doc = pymupdf.open(pdf_path)
    log(f"完成：{pdf_path}   {doc.page_count} 页   {size_mb:.1f} MB")
    doc.close()


if __name__ == "__main__":
    main()
