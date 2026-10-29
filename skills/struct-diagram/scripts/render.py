#!/usr/bin/env python3
"""
render.py — 產圖後的驗證與輸出
================================
用法：
    python3 render.py <資料夾或 .svg 檔> [--scale 2.0] [--no-png]

做三件事：
  1. XML 合法性檢查（缺 & 跳脫、標籤沒關會在這裡被抓到）
  2. 溢出檢查：座標超出 viewBox 代表版面爆掉（最常見的失敗）
  3. 輸出同名 PNG（給 pptx／影片管線用；HTML wiki 直接用 SVG）

溢出檢查是必要的：SVG 不會自動裁切，圖跑出畫布時檔案依然「合法」，
只有在瀏覽器裡才看得出來。這支腳本讓你不必開瀏覽器就知道。
"""
import sys, os, re, xml.dom.minidom

NUM = re.compile(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?")


def check_overflow(path, tol=2.0):
    dom = xml.dom.minidom.parse(path)
    svg = dom.documentElement
    vb = svg.getAttribute("viewBox").split()
    if len(vb) != 4:
        return []
    x0, y0, W, H = map(float, vb)
    bad = []

    def flag(tag, x, y, extra=""):
        if x < x0 - tol or x > x0 + W + tol or y < y0 - tol or y > y0 + H + tol:
            bad.append(f"    {tag} @ ({x:.0f}, {y:.0f}) {extra}")

    for el in dom.getElementsByTagName("*"):
        t = el.tagName
        if t in ("line",):
            flag(t, float(el.getAttribute("x1") or 0), float(el.getAttribute("y1") or 0))
            flag(t, float(el.getAttribute("x2") or 0), float(el.getAttribute("y2") or 0))
        elif t == "circle":
            cx, cy, r = (float(el.getAttribute(a) or 0) for a in ("cx", "cy", "r"))
            flag(t, cx - r, cy); flag(t, cx + r, cy); flag(t, cx, cy - r); flag(t, cx, cy + r)
        elif t in ("polygon", "polyline"):
            pts = [tuple(map(float, p.split(","))) for p in el.getAttribute("points").split() if "," in p]
            for x, y in pts:
                flag(t, x, y)
        elif t == "text":
            x, y = float(el.getAttribute("x") or 0), float(el.getAttribute("y") or 0)
            txt = "".join(n.data for n in el.childNodes if n.nodeType == n.TEXT_NODE)[:18]
            flag(t, x, y, f'"{txt}"')
        elif t == "rect":
            x, y = float(el.getAttribute("x") or 0), float(el.getAttribute("y") or 0)
            w, h = float(el.getAttribute("width") or 0), float(el.getAttribute("height") or 0)
            flag(t, x, y); flag(t, x + w, y + h)
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scale = 2.0
    for a in sys.argv[1:]:
        if a.startswith("--scale"):
            scale = float(a.split("=")[1]) if "=" in a else 2.0
    make_png = "--no-png" not in sys.argv
    target = args[0] if args else "."

    files = ([target] if target.endswith(".svg")
             else sorted(os.path.join(target, f) for f in os.listdir(target) if f.endswith(".svg")))
    if not files:
        print("找不到 .svg"); return 1

    fails = 0
    for f in files:
        name = os.path.basename(f)
        try:
            xml.dom.minidom.parse(f)
        except Exception as e:
            print(f"[XML 錯誤] {name}: {e}"); fails += 1; continue
        bad = check_overflow(f)
        status = "OK" if not bad else f"溢出 {len(bad)} 處"
        print(f"{name:<46} {os.path.getsize(f):>7,d} B  {status}")
        for b in bad[:6]:
            print(b)
        if len(bad) > 6:
            print(f"    …另有 {len(bad)-6} 處")
        if bad:
            fails += 1
        if make_png:
            try:
                import cairosvg
                cairosvg.svg2png(url=f, write_to=f[:-4] + ".png", scale=scale)
            except ImportError:
                make_png = False
                print("  （未安裝 cairosvg，略過 PNG 輸出：pip install cairosvg --break-system-packages）")
    print(f"\n{len(files)} 個檔案，{fails} 個需要修正。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
