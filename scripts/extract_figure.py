#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_figure.py — 從考卷 PDF 擷取題目附圖（取代手動截圖）

兩個子指令（在知識庫根目錄執行）：

  1) preview：把某頁轉成帶座標格線的預覽圖，用來目視找出附圖的範圍（單位：PDF point）
     python scripts/extract_figure.py preview SS/raw/exams/SS-2013_鋼結構設計.pdf --page 2
       → 產生 .work/exam-preview/page-2-grid.png（.work/ 不進版控）；同時列出該 PDF 每頁嵌入圖片的數量與 ppi
       ※ 在使用者電腦上產生的新檔，Google Drive 同步完成前可能暫時無法 stage 到雲端檢視，稍候重試即可

  2) crop：依 bbox 擷取附圖
     python scripts/extract_figure.py crop SS/raw/exams/SS-2013_鋼結構設計.pdf --page 2 \
         --bbox 255 755 474 865 --name SS-2013-4-fig-1 --out SS/raw/solutions/SS-2013-4
       → <name>.png         點陣擷取（預設 500 dpi），即證據圖
       → <name>-vector.svg  向量抽取（該頁附圖為向量線條時才有意義；點陣嵌入圖則只是包了一張圖）

bbox 格式：x0 y0 x1 y1（point，原點在頁面左上角，與 preview 格線一致）。
依賴：poppler-utils（pdftoppm、pdftocairo、pdfimages、pdfinfo）、Pillow。
"""
import argparse, os, re, subprocess, sys, tempfile


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def page_size(pdf, page):
    out = run(["pdfinfo", "-f", str(page), "-l", str(page), pdf])
    m = re.search(r"Page\s+%d size:\s+([\d.]+) x ([\d.]+)" % page, out) or re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", out)
    return float(m.group(1)), float(m.group(2))


def preview(a):
    from PIL import Image, ImageDraw
    os.makedirs(a.out, exist_ok=True)
    dpi = 100
    W, H = page_size(a.pdf, a.page)
    with tempfile.TemporaryDirectory() as td:
        run(["pdftoppm", "-r", str(dpi), "-f", str(a.page), "-l", str(a.page), "-png", "-singlefile", a.pdf, os.path.join(td, "p")])
        im = Image.open(os.path.join(td, "p.png")).convert("RGB")
    s = dpi / 72
    d = ImageDraw.Draw(im)
    for v in range(0, int(max(W, H)) + 1, 25):
        col = (220, 60, 60) if v % 100 == 0 else (200, 200, 230)
        if v <= W:
            d.line([(v * s, 0), (v * s, im.height)], fill=col, width=1)
            if v % 100 == 0: d.text((v * s + 2, 2), str(v), fill=(200, 0, 0))
        if v <= H:
            d.line([(0, v * s), (im.width, v * s)], fill=col, width=1)
            if v % 100 == 0: d.text((2, v * s + 2), str(v), fill=(200, 0, 0))
    p = os.path.join(a.out, f"page-{a.page}-grid.png")
    im.save(p)
    print(f"頁面 {a.page}：{W:.0f} × {H:.0f} pt；預覽 {p}（紅線每 100 pt、淡線每 25 pt）")
    lst = run(["pdfimages", "-list", a.pdf]).splitlines()[2:]
    per = {}
    for ln in lst:
        f = ln.split()
        per.setdefault(int(f[0]), []).append(f[12])
    for pg in sorted(per):
        print(f"  第 {pg} 頁：嵌入圖片 {len(per[pg])} 張，ppi {sorted(set(per[pg]))}")
    if a.page not in per:
        print(f"  第 {a.page} 頁沒有嵌入圖片 → 附圖若存在即為向量線條，可用 crop 產生無損 -vector.svg")


def crop(a):
    x0, y0, x1, y1 = a.bbox
    os.makedirs(a.out, exist_ok=True)
    s = a.dpi / 72
    png = os.path.join(a.out, a.name + ".png")
    base = png[:-4]
    run(["pdftoppm", "-r", str(a.dpi), "-f", str(a.page), "-l", str(a.page), "-png", "-singlefile",
         "-x", str(int(x0 * s)), "-y", str(int(y0 * s)), "-W", str(int((x1 - x0) * s)), "-H", str(int((y1 - y0) * s)),
         a.pdf, base])
    print(f"點陣擷取：{png}（{a.dpi} dpi）")
    if a.no_vector:
        return
    with tempfile.TemporaryDirectory() as td:
        full = os.path.join(td, "full.svg")
        run(["pdftocairo", "-svg", "-f", str(a.page), "-l", str(a.page), a.pdf, full])
        svg = open(full, encoding="utf-8").read()
    w, h = x1 - x0, y1 - y0
    svg = re.sub(r'width="[\d.]+(pt)?" height="[\d.]+(pt)?" viewBox="[^"]+"',
                 f'width="{w*3:.0f}" height="{h*3:.0f}" viewBox="{x0} {y0} {w} {h}"', svg, count=1)
    vp = os.path.join(a.out, a.name + "-vector.svg")
    open(vp, "w", encoding="utf-8").write(svg)
    print(f"向量抽取：{vp}（整頁向量內容，以 viewBox 裁到附圖範圍）")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preview"); p.add_argument("pdf"); p.add_argument("--page", type=int, required=True)
    p.add_argument("--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".work", "exam-preview"))
    c = sub.add_parser("crop"); c.add_argument("pdf"); c.add_argument("--page", type=int, required=True)
    c.add_argument("--bbox", type=float, nargs=4, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    c.add_argument("--name", required=True); c.add_argument("--out", required=True)
    c.add_argument("--dpi", type=int, default=500); c.add_argument("--no-vector", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    preview(a) if a.cmd == "preview" else crop(a)


if __name__ == "__main__":
    main()
