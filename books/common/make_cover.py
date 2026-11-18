#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 book.json 的参数生成各册的封面与封底。

运行：python books/common/make_cover.py [册名]
输出：books/<册名>/images/cover/cover_front.jpg、cover_front_plain.jpg、cover_back.jpg
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"
LOGO = ROOT.parent / "0-logo"

W, H = 2100, 2970
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_REG = "C:/Windows/Fonts/msyh.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


def hex_rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def crop_to(page_ratio, im):
    w, h = im.size
    if w / h > page_ratio:
        nw = int(h * page_ratio)
        box = ((w - nw) // 2, 0, (w + nw) // 2, h)
    else:
        nh = int(w / page_ratio)
        box = (0, (h - nh) // 2, w, (h + nh) // 2)
    return im.crop(box).resize((W, H), Image.LANCZOS)


def veil(im, stops):
    layer = Image.new("L", (1, H))
    px = layer.load()
    for y in range(H):
        t = y / (H - 1)
        a = stops[0][1]
        for i in range(len(stops) - 1):
            p0, a0 = stops[i]
            p1, a1 = stops[i + 1]
            if p0 <= t <= p1:
                k = (t - p0) / max(p1 - p0, 1e-6)
                a = a0 + (a1 - a0) * k
                break
        px[0, y] = int(a * 255)
    mask = layer.resize((W, H))
    base = Image.new("RGB", (W, H), (4, 8, 16))
    return Image.composite(base, im, mask)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if draw.textlength(cur + ch, font=fnt) <= max_w:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def grade(im, tint=(12, 20, 36), amount=0.45):
    """把不同来源的背景图压成同一冷色调，整套书看起来像一个系列。"""
    g = ImageOps.grayscale(im).convert("RGB")
    tinted = Image.blend(g, Image.new("RGB", im.size, tint), 0.42)
    return Image.blend(im, tinted, amount)


def base_image(cfg, key="image"):
    path = LOGO / cfg["cover"][key]
    im = Image.open(path).convert("RGB")
    im = crop_to(W / H, im)
    return grade(im)


def front(cfg, out_dir):
    accent = hex_rgb(cfg.get("accent", "#b5651d"))
    im = base_image(cfg)
    im = ImageEnhance.Brightness(im).enhance(0.86)
    im = veil(im, [(0.0, 0.80), (0.34, 0.42), (0.66, 0.34), (1.0, 0.78)])
    d = ImageDraw.Draw(im)

    x = 200
    # 系列名
    d.text((x, 470), cfg.get("series_title", "专业级渲染技术"), font=font(FONT_REG, 46),
           fill=(208, 218, 230))
    # 书名
    y = 580
    f_title = font(FONT_BOLD, 132)
    for line in cfg["cover"].get("title_lines") or wrap(d, cfg["title"], f_title, W - 400):
        d.text((x, y), line, font=f_title, fill=(255, 255, 255))
        y += 158
    y += 46
    # 分册名
    vol = cfg.get("volume", "")
    if vol:
        d.text((x, y), vol, font=font(FONT_BOLD, 54), fill=accent)
        y += 96
    # 副标题
    f_sub = font(FONT_REG, 54)
    for line in wrap(d, cfg.get("subtitle", ""), f_sub, W - 400):
        d.text((x, y), line, font=f_sub, fill=(224, 231, 240))
        y += 72
    # 作者
    y = max(y + 60, 1560)
    d.rectangle([x, y, x + 300, y + 6], fill=accent)
    d.text((x, y + 48), cfg.get("author", "Dr. Dezeming"), font=font(FONT_REG, 56),
           fill=(238, 243, 250))

    foot = cfg["cover"].get("footer", "")
    if foot:
        f = font(FONT_REG, 38)
        fy = H - 230
        for line in wrap(d, foot, f, W - 400):
            d.text((x, fy), line, font=f, fill=(188, 198, 212))
            fy += 54

    im.save(out_dir / "cover_front.jpg", "JPEG", quality=90, optimize=True, progressive=True)
    return im


def front_plain(cfg, out_dir):
    im = base_image(cfg)
    im = ImageEnhance.Brightness(im).enhance(0.80)
    im = veil(im, [(0.0, 0.72), (0.45, 0.42), (1.0, 0.66)])
    im.save(out_dir / "cover_front_plain.jpg", "JPEG", quality=88, optimize=True, progressive=True)


def back(cfg, out_dir, back_image=None):
    accent = hex_rgb(cfg.get("accent", "#b5651d"))
    im = base_image(cfg, "back_image") if back_image else base_image(cfg)
    im = ImageEnhance.Brightness(im).enhance(0.9)
    im = veil(im, [(0.0, 0.55), (0.42, 0.46), (1.0, 0.82)])
    d = ImageDraw.Draw(im)

    x, maxw = 200, W - 400
    y = 1080
    quote = cfg["cover"].get("back_quote", "")
    if quote:
        fq = font(FONT_BOLD, 70)
        for line in wrap(d, quote, fq, maxw):
            d.text((x, y), line, font=fq, fill=(255, 255, 255))
            y += 96
        y += 46

    f = font(FONT_REG, 46)
    for para in cfg["cover"].get("back_paras", []):
        for line in wrap(d, para, f, maxw):
            d.text((x, y), line, font=f, fill=(222, 229, 238))
            y += 70
        y += 34

    d.rectangle([x, H - 520, x + 240, H - 514], fill=accent)
    d.text((x, H - 470), cfg.get("author", "Dr. Dezeming"), font=font(FONT_REG, 54),
           fill=(240, 244, 250))
    im.save(out_dir / "cover_back.jpg", "JPEG", quality=90, optimize=True, progressive=True)


def main():
    names = sys.argv[1:]
    targets = [BOOKS / n for n in names] if names else \
        [p for p in sorted(BOOKS.iterdir()) if (p / "book.json").exists()]
    for book in targets:
        cfg = json.loads((book / "book.json").read_text(encoding="utf-8"))
        if "cover" not in cfg:
            print("跳过（无封面参数）:", book.name)
            continue
        out_dir = book / "images" / "cover"
        out_dir.mkdir(parents=True, exist_ok=True)
        front(cfg, out_dir)
        front_plain(cfg, out_dir)
        back(cfg, out_dir)
        print("封面完成:", book.name)


if __name__ == "__main__":
    main()
