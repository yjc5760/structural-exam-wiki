#!/usr/bin/env python3
"""gen_lecture_RC-U2-1_figs.py — RC-U2-1 觀念講義的 9 張向量圖解。

所有幾何由公式與題目數值算出（莫爾圓、桁架、STM、RC-2020-2 剪力圖…），可重跑、可審核。
用法：python3 gen_lecture_RC-U2-1_figs.py <lecture-RC-U2-1.html>
      → 依序替換 HTML 中第 1..9 個 <div class="fig"> 內的 <svg>…</svg>。
      之後再跑會找 <!--FIG:name--> 標記替換（第一次執行會加上標記）。
"""
import math, re, sys

# ───────────────────────── 基本繪圖工具 ─────────────────────────
C = dict(ink="#263238", mut="#607d8b", grid="#cfd8dc", beam="#f5f7f8", edge="#546e7a",
         red="#c62828", red2="#ffebee", grn="#2e7d32", grn2="#e8f5e9", blu="#1565c0",
         blu2="#e3f2fd", org="#ef6c00", org2="#fff3e0", pur="#6a1b9a", pur2="#f3e5f5",
         dblu="#0d47a1", sup="#90a4ae")

def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")

class Svg:
    def __init__(s, w, h):
        s.w, s.h, s.o = w, h, []
    def add(s, t): s.o.append(t)
    def line(s, x1, y1, x2, y2, c=C["edge"], w=1.5, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}"{d}{extra}/>')
    def pl(s, pts, c=C["edge"], w=1.5, fill="none", dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        s.add(f'<polyline points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d} stroke-linejoin="round"{extra}/>')
    def poly(s, pts, fill, c="none", w=1.2, extra=""):
        p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        s.add(f'<polygon points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}"{extra}/>')
    def rect(s, x, y, w, h, fill=C["beam"], c=C["edge"], sw=1.6, rx=0, extra=""):
        s.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{extra}/>')
    def circ(s, x, y, r, fill="none", c=C["edge"], w=1.5):
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>')
    def text(s, x, y, t, size=12, c=C["ink"], anchor="start", bold=False, extra=""):
        b = ' font-weight="700"' if bold else ""
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        s.add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}"{a} fill="{c}"{b}{extra}>{t}</text>')
    def arrow(s, x1, y1, x2, y2, c=C["edge"], w=1.6, head=8, both=False, dash=None):
        """直線箭頭，箭頭頭部以三角形計算（不用 marker，PDF 也穩）。"""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        hw = head * 0.45
        def headat(xe, ye, ux, uy):
            bx, by = xe - ux * head, ye - uy * head
            s.poly([(xe, ye), (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)], fill=c)
        xs, ys = (x1 + ux * head * 0.8, y1 + uy * head * 0.8) if both else (x1, y1)
        s.line(xs, ys, x2 - ux * head * 0.8, y2 - uy * head * 0.8, c, w, dash)
        headat(x2, y2, ux, uy)
        if both: headat(x1, y1, -ux, -uy)
    def dim_h(s, x1, x2, y, label, c=C["ink"], size=12, tick=6, above=False):
        s.line(x1, y, x2, y, c, 1.1)
        s.line(x1, y - tick, x1, y + tick, c, 1.1); s.line(x2, y - tick, x2, y + tick, c, 1.1)
        s.text((x1 + x2) / 2, y - 6 if above else y + size + 4, label, size, c, "middle", True)
    def dim_v(s, x, y1, y2, label, c=C["ink"], size=12, tick=6, left=True):
        s.line(x, y1, x, y2, c, 1.1)
        s.line(x - tick, y1, x + tick, y1, c, 1.1); s.line(x - tick, y2, x + tick, y2, c, 1.1)
        s.text(x - 6 if left else x + 6, (y1 + y2) / 2 + size * 0.35, label, size, c, "end" if left else "start", True)
    def pin(s, x, y, c=C["edge"]):
        s.poly([(x, y), (x - 9, y + 14), (x + 9, y + 14)], fill=c)
    def roller(s, x, y, c=C["edge"]):
        s.circ(x, y + 7, 7, "none", c, 1.6)
    def svg(s, label):
        body = "\n  ".join(s.o)
        return (f'<svg viewBox="0 0 {s.w} {s.h}" xmlns="http://www.w3.org/2000/svg" role="img" '
                f'aria-label="{label}">\n  {body}\n</svg>')

# ───────────────────── 圖 0：§0 三種軸力的莫爾圓 ─────────────────────
def fig0():
    s = Svg(900, 450)
    k = 46.0                      # 莫爾圓：1 ft = 46 px
    cases = [("無軸力（純剪）", 0.0, C["dblu"]),
             ("加軸壓  σx = −1.0 ft", -1.0, C["grn"]),
             ("加軸拉  σx = +0.5 ft", +0.5, C["red"])]
    for i, (title, sx, tc) in enumerate(cases):
        cx = 150 + 300 * i
        if i: s.line(300 * i, 14, 300 * i, 440, C["grid"], 1.5, "6 5")
        # 開裂瞬間：σ1 = ft → τcr = ft·√(1 − σx/ft)
        tau = math.sqrt(1 - sx)
        th_p = 0.5 * math.degrees(math.atan2(2 * tau, sx))   # σ1 方向（自梁軸逆時針）
        beta = 90 - th_p                                     # 裂縫與梁軸夾角
        s.text(cx, 26, title, 14.5, tc, "middle", True)
        # 微元素
        a, ey = 78, 104
        x0, y0 = cx - a / 2, ey - a / 2
        cid = f"clip0{i}"
        s.add(f'<clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0)}" width="{a}" height="{a}"/></clipPath>')
        s.rect(x0, y0, a, a, "#fafbfc", C["edge"], 1.6)
        # 裂縫：垂直於 σ1，畫三條平行線並裁切在元素內
        # 裂縫方向：自水平量 beta，向右下（與 σ1 = 向右上 θp 垂直）
        dx, dy = math.cos(math.radians(-beta)), -math.sin(math.radians(-beta))
        nx, ny = math.cos(math.radians(th_p)), -math.sin(math.radians(th_p))
        g = [f'<g clip-path="url(#{cid})" stroke="{C["red"]}" stroke-width="2.4">']
        for off in (-22, 0, 22):
            px, py = cx + nx * off, ey + ny * off
            g.append(f'<line x1="{f(px - dx*80)}" y1="{f(py - dy*80)}" x2="{f(px + dx*80)}" y2="{f(py + dy*80)}"/>')
        g.append("</g>"); s.add("".join(g))
        # τ 箭頭（正剪力：右面向上、左面向下、上面向右、下面向左）
        tl = 18 + 10 * (tau - 0.7)
        s.arrow(x0 + a + 7, ey + tl, x0 + a + 7, ey - tl, C["blu"], 1.8, 7)
        s.arrow(x0 - 7, ey - tl, x0 - 7, ey + tl, C["blu"], 1.8, 7)
        s.arrow(cx - tl, y0 - 7, cx + tl, y0 - 7, C["blu"], 1.8, 7)
        s.arrow(cx + tl, y0 + a + 7, cx - tl, y0 + a + 7, C["blu"], 1.8, 7)
        s.text(x0 + a + 13, ey - tl + 4, f"τ = {tau:.2f} ft" if sx else "τ = 1.00 ft", 11, C["blu"], bold=True)
        # σx 箭頭
        if sx < 0:
            s.arrow(x0 - 46, ey, x0 - 16, ey, C["grn"], 2.4, 9)
            s.arrow(x0 + a + 46, ey, x0 + a + 16, ey, C["grn"], 2.4, 9)
        elif sx > 0:
            s.arrow(x0 - 16, ey, x0 - 42, ey, C["red"], 2.4, 9)
            s.arrow(x0 + a + 16, ey, x0 + a + 42, ey, C["red"], 2.4, 9)
        if sx:
            s.text(x0 - 30, ey - 10, "σx", 11, tc, "middle", True)
        # σ1 方向（虛線雙箭頭）
        r1 = 54
        s.arrow(cx - nx * r1, ey - ny * r1, cx + nx * r1, ey + ny * r1, C["org"], 1.4, 7, both=True, dash="4 3")
        s.text(cx + nx * r1 + 4, ey + ny * r1 - 3, "σ1", 11, C["org"], bold=True)
        # 莫爾圓
        my, O = 292, cx + 10            # σ 軸高度、原點 x
        s.line(cx - 138, my, cx + 138, my, C["mut"], 1.1)
        s.line(O, my - 76, O, my + 76, C["mut"], 1.1)
        s.text(cx + 136, my - 5, "σ", 11, C["mut"], "end")
        s.text(O + 4, my - 66, "τ", 11, C["mut"])
        xf = O + k
        s.line(xf, my - 80, xf, my + 80, C["red"], 1.2, "5 4")
        s.text(xf + 3, my + 92 - 4, "ft", 11, C["red"], bold=True)
        c0, R = sx / 2, math.sqrt((sx / 2) ** 2 + tau ** 2)
        s.circ(O + c0 * k, my, R * k, "none", tc, 2.2)
        X = (O + sx * k, my - tau * k)
        Y = (O, my + tau * k)
        s.line(X[0], X[1], Y[0], Y[1], tc, 1.1, "3 3")
        s.circ(*X, 3.6, tc, tc, 1)
        s.circ(xf, my, 4.2, C["red"], C["red"], 1)
        s.text(X[0] - 4 if sx < 0 else X[0] + 6, X[1] - 6, "(σx, τ)", 10.5, tc, "end" if sx < 0 else "start")
        # 結論
        s.text(cx, 398, f"開裂所需 τcr = {tau:.2f} ft", 13, tc, "middle", True)
        tilt = "45°（標準）" if abs(beta - 45) < .1 else (f"{beta:.0f}°（較平）" if beta < 45 else f"{beta:.0f}°（較陡）")
        s.text(cx, 418, f"裂縫與梁軸夾角 {tilt}", 12, C["ink"], "middle")
        verdict = ["Vc 基準值", "Vc 提高、裂縫較窄", "Vc 降低、裂縫較寬"][i]
        s.text(cx, 437, verdict, 12, C["mut"], "middle")
    return s.svg("三種軸力狀態下的微元素與莫爾圓")

# ───────────────────── 圖 1：§1.1 三個階段 ─────────────────────
def fig1():
    s = Svg(900, 300)
    # ① 未開裂：矩形斷面＋拋物線剪應力
    s.text(150, 24, "① 未開裂", 13.5, C["dblu"], "middle", True)
    bx, by, bw, bh = 70, 46, 46, 150
    s.rect(bx, by, bw, bh)
    s.text(bx + bw / 2, by + bh + 16, "b", 11, C["mut"], "middle")
    s.dim_v(bx - 10, by, by + bh, "h", C["mut"], 11)
    x0, tmax = bx + bw + 16, 70
    pts = []
    for j in range(41):
        y = by + bh * j / 40
        eta = 2 * (y - (by + bh / 2)) / bh
        pts.append((x0 + tmax * (1 - eta ** 2), y))
    s.poly([(x0, by)] + pts + [(x0, by + bh)], C["blu2"], C["blu"], 1.6)
    s.line(x0, by, x0, by + bh, C["blu"], 1.2)
    for j in range(1, 8):
        y = by + bh * j / 8
        eta = 2 * (y - (by + bh / 2)) / bh
        L = tmax * (1 - eta ** 2)
        if L > 10: s.arrow(x0, y, x0 + L, y, C["blu"], 1, 5)
    s.text(x0 + tmax + 6, by + bh / 2 + 4, "τmax", 11.5, C["blu"], bold=True)
    s.text(x0 + tmax + 6, by + bh / 2 + 20, "= 1.5V/(bh)", 10.5, C["blu"])
    s.text(150, 232, "全斷面均質彈性，箍筋幾乎不受力", 11.5, C["ink"], "middle")
    s.text(150, 256, "V 由整個斷面以拋物線分布承擔", 12, C["grn"], "middle", True)

    # ② 斜裂縫：左側自由體的四個 Vc 來源（皆為垂直剪力分量）
    def beam_with_crack(x0, title, stirrups=False):
        s.text(x0 + 135, 24, title, 13.5, C["dblu"], "middle", True)
        y0, H, L = 50, 120, 250
        ys, ycz = y0 + H - 12, y0 + 34       # 主筋高度、壓力區底
        crack = [(x0 + 66, y0 + H), (x0 + 74, y0 + H - 26), (x0 + 74 + (y0 + H - 26 - ycz), ycz)]
        free = [(x0, y0), (crack[2][0], y0), crack[2], crack[1], crack[0], (x0, y0 + H)]
        s.rect(x0, y0, L, H, "#fbfcfd")
        s.poly(free, "#e3f2fd", "none")
        s.line(x0, ycz, x0 + L, ycz, C["sup"], 1, "4 3")
        s.text(x0 + L - 4, ycz - 5, "壓力區", 10, C["mut"], "end")
        s.line(x0, ys, x0 + L, ys, C["ink"], 2.6)
        if stirrups:
            sp = 30
            for xs in [x0 + 45 + sp * j for j in range(7)]:
                hit = crack[1][0] < xs < crack[2][0]
                s.line(xs, y0 + 5, xs, y0 + H - 5, C["grn"] if hit else "#a5d6a7", 2.6 if hit else 1.8)
                if hit:
                    yc = crack[1][1] - (xs - crack[1][0])
                    s.arrow(xs + 6, yc - 26, xs + 6, yc - 3, C["grn"], 1.6, 7)
            s.text(x0 + 135, y0 + H + 22, "跨越裂縫的箍筋降伏：每支 Av·fyt", 11.5, C["grn"], "middle", True)
        s.pl(crack, C["red"], 2.8)
        return y0, H, ys, ycz, crack
    x2 = 320
    y0, H, ys, ycz, crack = beam_with_crack(x2, "② 斜裂縫出現：Vc 的四個來源")
    xc = crack[2][0]
    s.arrow(xc - 12, y0 + 4, xc - 12, ycz - 2, C["blu"], 2, 8)   # 作用在自由體上：向下
    s.text(xc - 18, y0 + 18, "① Vcz", 10.5, C["blu"], "end", True)
    mx, my = (crack[1][0] + crack[2][0]) / 2, (crack[1][1] + crack[2][1]) / 2
    s.arrow(mx + 6, my - 20, mx - 18, my + 4, C["blu"], 2, 8)
    s.text(mx + 12, my + 6, "② Va 骨材互鎖", 10.5, C["blu"], bold=True)
    s.arrow(crack[0][0] + 2, ys - 24, crack[0][0] + 2, ys - 3, C["blu"], 2, 8)
    s.text(crack[0][0] - 6, ys - 12, "③ Vd 銷栓", 10.5, C["blu"], "end", True)
    s.text(x2 + 135, y0 + H + 22, "④ 拱作用：短跨才顯著（§5）", 11, C["blu"], "middle")
    s.text(x2 + 135, 232, "四者無法個別量化 → 規範以 √f'c 迴歸", 11.5, C["ink"], "middle")
    s.text(x2 + 135, 256, "Vc = 開裂瞬間 ①＋②＋③（＋④）", 12, C["grn"], "middle", True)
    # ③ 箍筋接手
    x3 = 625
    beam_with_crack(x3, "③ 箍筋接手", stirrups=True)
    s.text(x3 + 135, 232, "裂縫張開後 ②③ 衰退，箍筋縫住裂縫", 11.5, C["ink"], "middle")
    s.text(x3 + 135, 256, "Vs = 跨越裂縫箍筋的降伏力總和", 12, C["grn"], "middle", True)
    s.text(450, 288, "藍底＝裂縫左側自由體；箭頭＝切面上作用於自由體的剪力分量（向下，與支承反力平衡）", 11, C["mut"], "middle")
    return s.svg("RC 梁剪力傳遞的三個階段")

# ───────────────────── 圖 2：§1.2 數箍筋 ─────────────────────
def fig2():
    s = Svg(900, 300)
    xl, xr, yt, yb = 70, 830, 70, 210
    d = yb - yt                 # 140 px：上下弦間距（≈ d）
    sp = d / 4                  # s = d/4 → 一條 45° 裂縫跨 4 支
    s.rect(xl, yt - 14, xr - xl, d + 28, "#f7f9fb", C["grid"], 1.2)
    xs = [xl + 20 + sp * j for j in range(int((xr - xl - 30) / sp) + 1)]
    # 斜壓桿（每隔一支畫一條，45°）
    for x in xs[::2]:
        if x + d <= xr - 5:
            s.line(x, yb, x + d, yt, "#ef9a9a", 2, "7 5")
    for x in xs:
        s.line(x, yt, x, yb, C["grn"], 2.4)
    s.line(xl, yt, xr, yt, C["red"], 4)
    s.line(xl, yb, xr, yb, C["grn"], 4)
    s.text(xr + 6, yt + 4, "上弦（壓）", 11.5, C["red"], bold=True)
    s.text(xr + 6, yb + 4, "下弦（拉）", 11.5, C["grn"], bold=True)
    # 裂縫：起點在兩支箍筋正中間
    c0 = xs[5] + sp / 2
    s.line(c0, yb, c0 + d, yt, C["org"], 4)
    s.text(c0 + d + 8, yt - 20, "一條 45° 斜裂縫（水平投影 = d）", 12, C["org"], bold=True)
    hits = [x for x in xs if c0 < x < c0 + d]
    for n, x in enumerate(hits, 1):
        yc = yb - (x - c0)
        s.circ(x, yc, 5, C["org"], "#fff", 1.5)
        s.arrow(x + 9, yc + 18, x + 9, yc - 16, C["grn"], 1.8, 7)
        s.text(x + 13, yc + 14, str(n), 11, C["grn"], bold=True)
    s.text(xs[1] + d / 2 + 4, (yt + yb) / 2 + 30, "斜壓桿", 11, C["red"])
    s.dim_h(c0, c0 + d, yb + 24, "d")
    s.dim_h(xs[1], xs[2], yb + 24, "s", C["mut"], 11)
    s.dim_v(xl - 8, yt, yb, "d", C["ink"], 12)
    s.text(450, 284, f"跨越 n = d / s = {len(hits)} 支，每支降伏力 Av·fyt   →   Vs = n·Av·fyt = Av·fyt·d / s",
           13, C["dblu"], "middle", True)
    return s.svg("45 度斜裂縫跨越箍筋數 n = d/s")

# ───────────────────── 圖 3：§2.3 軸力修正 ─────────────────────
def fig3():
    s = Svg(900, 340)
    X0, X1, Y0 = 110, 840, 286        # Nu/Ag = -35 → X0；+140 → X1
    kx = (X1 - X0) / 175.0
    ky = 105.0                        # Vc/Vc0 = 1 → 105 px
    X = lambda n: X0 + (n + 35) * kx
    Y = lambda r: Y0 - r * ky
    s.rect(X0, Y(2.1), X(0) - X0, Y0 - Y(2.1), C["red2"], "none", 0)
    s.rect(X(0), Y(2.1), X1 - X(0), Y0 - Y(2.1), C["grn2"], "none", 0)
    for r in (0.5, 1.0, 1.5, 2.0):
        s.line(X0, Y(r), X1, Y(r), "#b0bec5", 0.8, "3 4")
        s.text(X0 - 8, Y(r) + 4, f"{r:.1f}", 11, C["mut"], "end")
    for n in (-35, 0, 35, 70, 105, 140):
        s.line(X(n), Y0, X(n), Y0 + 5, C["ink"], 1.2)
        s.text(X(n), Y0 + 19, f"{n:+d}" if n else "0", 11, C["red"] if n < 0 else (C["grn"] if n > 0 else C["ink"]), "middle")
    s.text(X0 - 8, Y0 + 4, "0", 11, C["mut"], "end")
    s.line(X0, Y0, X1 + 14, Y0, C["ink"], 1.6)
    s.line(X(0), Y0 + 8, X(0), Y(2.1) - 8, C["ink"], 1.6)
    s.text(X1, Y0 + 38, "Nu / Ag（kgf/cm²，壓為正）", 12, C["ink"], "end")
    s.text(X(0) - 8, Y(2.1) - 12, "Vc / Vc0", 12, C["ink"], "end")
    s.text((X0 + X(0)) / 2, Y(1.9), "軸拉區", 12.5, C["red"], "middle", True)
    s.text((X(0) + X1) / 2, Y(1.9) + 4, "軸壓區", 12.5, C["grn"], "middle", True)
    s.line(X(-35), Y(0), X(0), Y(1), C["red"], 3.2)
    s.line(X(0), Y(1), X(140), Y(2), C["grn"], 3.2)
    s.text(X(-34), Y(1.45), "1 + Nu/(35Ag)", 11.5, C["red"], bold=True)
    s.text(X(70), Y(1.5) - 12, "1 + Nu/(140Ag)", 11.5, C["grn"], "middle", True)
    for n, col, anc, dx, dy in ((-12.5, C["red"], "start", 8, 22), (12.5, C["grn"], "start", 10, 22)):
        r = 1 + n / (35 if n < 0 else 140)
        s.circ(X(n), Y(r), 5.5, col, "#fff", 1.5)
        s.text(X(n) + dx, Y(r) + dy, f"RC-2010-3：{n:+.1f} → {r:.3f}", 11, col, anc, True)
    s.text(X(70), Y(0.62), "斜率比 = (1/35) ÷ (1/140) = 4", 13, C["dblu"], "middle", True)
    s.text(X(70), Y(0.62) + 21, "同樣大小的 N/Ag，軸拉的傷害是軸壓幫助的 4 倍", 12, C["ink"], "middle")
    s.text(X(70), Y(0.62) + 41, "N/Ag = −35 時 Vc 歸零；再拉也取 Vc = 0", 12, C["red"], "middle")
    return s.svg("軸力對 Vc 的修正係數")

# ───────────────────── 圖 4：§3.1 三個區間＋間距示意 ─────────────────────
def fig4():
    s = Svg(900, 396)
    X0, k = 80, 150.0                 # Vs/Vc：1 → 150 px
    X = lambda r: X0 + r * k
    zones = [(0, 2, C["grn2"], C["grn"], "smax = min(d/2, 60 cm)", "裂縫還不密，箍筋跨得到"),
             (2, 4, C["org2"], C["org"], "smax = min(d/4, 30 cm)", "裂縫變密 → 間距減半"),
             (4, 5.1, C["red2"], C["red"], "斷面不足，必須加大", "斜壓桿壓碎，加箍筋沒用")]
    for a, b, fc, sc, t1, t2 in zones:
        s.rect(X(a), 70, X(b) - X(a), 36, fc, sc, 1.6)
        s.text((X(a) + X(b)) / 2, 93, t1, 12.5, sc, "middle", True)
        s.text((X(a) + X(b)) / 2, 58, t2, 11.5, C["ink"], "middle")
    s.arrow(X0, 124, X(5.4), 124, C["ink"], 1.6, 9)
    s.text(X(5.4), 116, "Vs / Vc", 12, C["ink"], "end")
    for r in range(6):
        s.line(X(r), 118, X(r), 130, C["ink"], 1.3)
        s.text(X(r), 146, str(r), 11.5, C["ink"], "middle")
    s.text(X(2), 164, "2Vc = 1.06√f'c bw d", 11, C["org"], "middle", True)
    s.text(X(4), 164, "4Vc = 2.12√f'c bw d", 11, C["red"], "middle", True)
    r20 = 37.13 / 26.07
    s.poly([(X(r20), 118), (X(r20) - 6, 108), (X(r20) + 6, 108)], C["blu"])
    s.text(X(r20), 184, f"RC-2020-2：Vs = {r20:.2f} Vc", 11, C["blu"], "middle", True)
    s.line(X(r20), 130, X(r20), 172, C["blu"], 1, "3 3")
    # 下方：兩種間距下，一條 45° 裂縫跨幾支（同比例）
    d = 104
    for j, (div, col, lab) in enumerate(((2, C["grn"], "s = d/2 → 跨 2 支"), (4, C["org"], "s = d/4 → 跨 4 支"))):
        x0, yt = 110 + j * 400, 222
        yb, sp = yt + d, d / div
        s.rect(x0, yt, 300, d, "#fafbfc", C["edge"], 1.4)
        xs = [x0 + 14 + sp * i for i in range(int(286 / sp) + 1)]
        c0 = x0 + 14 + sp * 1.5 if div == 2 else x0 + 14 + sp * 2.5
        for x in xs:
            hit = c0 < x < c0 + d
            s.line(x, yt + 4, x, yb - 4, col if hit else "#b0bec5", 2.6 if hit else 1.6)
            if hit: s.circ(x, yb - (x - c0), 4.5, col, "#fff", 1.4)
        s.line(c0, yb, c0 + d, yt, C["red"], 3)
        s.dim_h(c0, c0 + d, yb + 14, "d", C["ink"], 11, 5)
        s.text(x0 + 150, yt - 8, lab, 12.5, col, "middle", True)
    s.text(450, 384, "推論：Vu,max = φ(Vc + 4Vc) = 5φVc（RC-2020-2：5 × 0.75 × 26.07 = 97.8 tf）",
           12.5, C["dblu"], "middle", True)
    return s.svg("Vs 的三個區間與箍筋間距")

# ───────────────────── 圖 5：§4 臨界斷面（RC-2020-2 實際比例） ─────────────────────
def fig5():
    s = Svg(900, 420)
    s.line(450, 14, 450, 408, C["grid"], 2, "6 5")
    s.text(225, 26, "可以用 d 偏移（RC-2020-2 實際比例）", 14, C["grn"], "middle", True)
    km = 75.0                         # 1 m = 75 px
    xf, yt = 70, 92                   # 支承面 x、梁頂 y
    h, d, Lh, wu = 0.90, 0.84, 4.0, 15.0
    yb, ys = yt + h * km, yt + d * km
    xm = xf + Lh * km
    s.rect(xf - 0.30 * km, yb, 0.30 * km, 18, C["sup"], "none")
    s.rect(xf - 0.30 * km, yt, xm - xf + 0.30 * km, h * km)
    s.line(xf - 0.3 * km, ys, xm, ys, C["ink"], 2)
    for j in range(9):
        x = xf + 6 + j * (xm - xf - 12) / 8
        s.arrow(x, yt - 24, x, yt - 2, C["edge"], 1.3, 6)
    s.line(xf + 6, yt - 24, xm - 6, yt - 24, C["edge"], 1.3)
    s.text(xm, yt - 30, "wu = 15 tf/m（作用於梁頂）", 11, C["mut"], "end")
    s.text(xm + 4, yt + h * km / 2 + 4, "≈ 跨中", 10, C["mut"])
    xd = xf + d * km
    s.line(xf, ys, xd, yt, C["red"], 3)
    s.text(xd + 6, yt + 16, "45° 斜裂縫", 11.5, C["red"], bold=True)
    s.line(xd, yt - 4, xd, 330, C["blu"], 1.5, "6 4")
    s.text(xd + 5, 326, "臨界斷面", 11, C["blu"], bold=True)
    s.dim_v(xf - 0.3 * km - 6, yt, ys, "d", C["ink"], 11, 5)
    s.dim_h(xf, xd, yb + 30, "d = 0.84 m", C["ink"], 11, 5)
    # 剪力圖（1 tf = 1 px）
    y0, kv = 312, 1.0
    V = lambda x_m: wu * (Lh - x_m)
    pts = [(xf, y0)] + [(xf + x * km, y0 - V(x) * kv) for x in (0, Lh)]
    s.poly(pts, "#eceff1", C["edge"], 1.4)
    s.poly([(xf, y0), (xf, y0 - V(0) * kv), (xd, y0 - V(d) * kv), (xd, y0)], "#bbdefb", C["blu"], 1.2)
    s.line(xf, y0, xm + 10, y0, C["ink"], 1.2)
    s.text(xf - 4, y0 - V(0) * kv + 4, "60", 11, C["ink"], "end", True)
    s.text(xd + 6, y0 - V(d) * kv - 2, f"Vu,d = 60 − 15×0.84 = {V(d):.1f} tf", 11, C["blu"], bold=True)
    s.text(xm - 4, y0 + 15, "V（tf）", 10.5, C["mut"], "end")
    s.text(225, 360, "支承反力向上壓住端區；d 以內的剪力沿斜壓桿直入支承", 11.5, C["ink"], "middle")
    s.text(225, 382, "藍色那段不必以 60 tf 設計 → 以 47.4 tf 設計（省 21%）", 12, C["grn"], "middle", True)
    s.text(225, 402, "三條件 (a)(b)(c) 同時成立才可用（§4.1）", 11, C["mut"], "middle")

    s.text(672, 26, "以下情況不可用（取支承面）", 14, C["red"], "middle", True)
    tx = 668
    # (a) 端部由拉力構件吊掛
    s.rect(484, 44, 90, 12, C["sup"], "none")
    s.line(500, 56, 500, 124, C["ink"], 3)
    s.rect(492, 124, 16, 5, C["ink"], "none")
    s.rect(492, 88, 150, 34)
    s.arrow(522, 112, 522, 70, C["red"], 1.8, 7)
    s.text(526, 80, "T", 11, C["red"], bold=True)
    s.text(tx, 70, "(a) 端部由拉力構件支承（吊掛）", 12, C["red"], bold=True)
    s.text(tx, 88, "反力不在端區產生壓力", 11, C["mut"])
    s.text(tx, 105, "條件 (a) 不成立 → 取支承面", 11, C["mut"])
    # (b) 倒 T 梁，載重作用在下翼
    wx0, wx1, ty, fy0, fy1 = 548, 584, 160, 226, 250
    s.poly([(wx0, ty), (wx1, ty), (wx1, fy0), (622, fy0), (622, fy1), (510, fy1), (510, fy0), (wx0, fy0)],
           C["beam"], C["edge"], 1.6)
    for xa in (522, 610):
        s.arrow(xa, 190, xa, fy0 - 1, C["red"], 2, 8)
    s.text(516, 186, "P", 11, C["red"], "end", True)
    s.pl([(wx0 + 6, fy1 - 6), (wx0 + 6, ty + 6), (wx1 - 6, ty + 6), (wx1 - 6, fy1 - 6), (wx0 + 6, fy1 - 6)], C["grn"], 2)
    s.arrow(566, 238, 566, 176, C["grn"], 1.6, 7, dash="4 3")
    s.text(tx, 182, "(b) 載重作用在下翼（倒 T 梁托承）", 12, C["red"], bold=True)
    s.text(tx, 200, "力要靠吊筋（綠）吊回腹板上方", 11, C["mut"])
    s.text(tx, 217, "條件 (b) 不成立；RC-2020-2 載重在頂面 ✓", 11, C["mut"])
    # (c) 集中載重在 d 以內
    bx0, by0, H, dd = 506, 300, 52, 46
    s.rect(486, by0 + H, 20, 14, C["sup"], "none")
    s.rect(bx0, by0, 136, H)
    xp = bx0 + 0.65 * dd
    s.arrow(xp, by0 - 28, xp, by0 - 1, C["red"], 2.2, 8)
    s.text(xp + 5, by0 - 12, "P", 11, C["red"], bold=True)
    s.line(xp, by0 + 3, bx0 + 3, by0 + H - 3, C["red"], 2, "5 3")
    s.line(bx0 + dd, by0 - 4, bx0 + dd, by0 + H + 4, C["blu"], 1.2, "4 3")
    s.dim_h(bx0, xp, by0 + H + 22, "< d", C["ink"], 10.5, 4)
    s.text(tx, 312, "(c) 支承面與 d 處之間有集中載重", 12, C["red"], bold=True)
    s.text(tx, 330, "力經斜壓桿直入支承（紅虛線）", 11, C["mut"])
    s.text(tx, 347, "不可折減，必要時改用 STM（§5）", 11, C["mut"])
    return s.svg("臨界斷面可否取距支承面 d 處")

# ───────────────────── 圖 6：§5 a/d 與 STM（計算曲線） ─────────────────────
def fig6():
    s = Svg(900, 380)
    fc, fy, rho, zr, lr = 280.0, 4200.0, 0.015, 0.85, 0.20
    bs, bn = 0.60, 0.80
    Vc = 0.53 * math.sqrt(fc)
    X0, X1, Y0, Y1 = 100, 820, 300, 50
    amax, vmax = 3.0, 45.0
    X = lambda a: X0 + a * (X1 - X0) / amax
    Y = lambda v: Y0 - v * (Y0 - Y1) / vmax
    a25 = zr / math.tan(math.radians(25))
    def comps(a):
        th = math.atan(zr / a)
        ws = lr * math.sin(th) + lr * math.cos(th)
        return (0.85 * bs * fc * ws * math.sin(th),       # 壓桿（瓶形，無腹筋）
                0.85 * bn * fc * lr,                       # CCT 支承節點承壓
                rho * fy * zr / a)                         # 拉桿降伏
    s.rect(X(a25), Y1, X1 - X(a25), Y0 - Y1, C["grn2"], "none", 0)
    s.rect(X0, Y1, X(a25) - X0, Y0 - Y1, C["org2"], "none", 0)
    for v in range(0, 46, 10):
        s.line(X0, Y(v), X1, Y(v), "#cfd8dc", 0.8, "3 4") if v else None
        s.text(X0 - 8, Y(v) + 4, str(v), 11, C["mut"], "end")
    for a in (0, 0.5, 1, 1.5, 2, 2.5, 3):
        s.line(X(a), Y0, X(a), Y0 + 5, C["ink"], 1.2)
        s.text(X(a), Y0 + 19, f"{a:g}", 11, C["mut"], "middle")
    s.line(X0, Y0, X1 + 10, Y0, C["ink"], 1.6)
    s.line(X0, Y0 + 6, X0, Y1 - 8, C["ink"], 1.6)
    s.text(X1, Y0 + 38, "剪力跨深比 a / d", 12, C["ink"], "end")
    s.text(X0 + 6, Y1 - 12, "V / (b d)　kgf/cm²", 12, C["ink"])
    cid = "clip6"
    s.add(f'<clipPath id="{cid}"><rect x="{X0}" y="{Y1}" width="{X1-X0}" height="{Y0-Y1}"/></clipPath>')
    names = [("壓桿 βs=0.60", "#7986cb"), ("CCT 節點", "#9575cd"), ("拉桿 ρ=1.5%", "#4db6ac")]
    A = [0.3 + j * (a25 - 0.3) / 80 for j in range(81)]
    cv = [comps(a) for a in A]
    for m, (nm, col) in enumerate(names):
        s.pl([(X(a), Y(c[m])) for a, c in zip(A, cv)], col, 1.5, dash="6 4", extra=f' clip-path="url(#{cid})"')
    s.pl([(X(a), Y(min(c))) for a, c in zip(A, cv)], C["blu"], 3.4, extra=f' clip-path="url(#{cid})"')
    s.text(X(1.32) + 6, Y(comps(1.32)[2]) - 4, "拉桿降伏", 11, "#00897b", bold=True)
    s.text(X(0.3), Y(comps(0.3)[1]) - 6, "CCT 節點承壓", 11, "#7e57c2", bold=True)
    s.text(X(1.25), Y(comps(1.25)[0]) - 10, "直接壓桿（STM）強度", 12, C["blu"], bold=True)
    # 一般梁 Vc
    s.line(X0, Y(Vc), X1, Y(Vc), C["grn"], 3)
    s.text(X1 - 4, Y(Vc) - 8, f"桁架類比 Vc = 0.53√f'c = {Vc:.2f}", 11.5, C["grn"], "end", True)
    # θ = 25° 界線
    s.line(X(a25), Y1, X(a25), Y0, C["org"], 2, "6 4")
    s.text(X(a25), Y1 - 4, f"θ = 25° → a/d = {a25:.2f}", 11.5, C["org"], "middle", True)
    s.text(X(a25) + 8, Y(30), "θ < 25°：STM 不合法", 11, C["mut"])
    s.text(X(a25) + 8, Y(30) + 16, "→ B 區，用 Vc + Vs", 11, C["grn"], bold=True)
    s.text((X0 + X(a25)) / 2, Y(42), "D 區：拱作用（直接壓桿）", 12.5, C["org"], "middle", True)
    for a in (0.5, 1.0, 1.5):
        v = min(comps(a))
        s.circ(X(a), Y(v), 4, C["blu"], "#fff", 1.4)
        s.text(X(a) - 4, Y(v) + 20, f"{v / Vc:.1f}×Vc", 11, C["blu"], "middle", True)
    s.text(450, 362, f"計算條件：f'c=280、fy=4200 kgf/cm²，z=0.85d，承壓板寬＝節點高＝0.2d，βs=0.60、βn=0.80，標稱值（未乘 φ）",
           10.5, C["mut"], "middle")
    return s.svg("a/d 與直接壓桿強度、Vc 的比較")

# ───────────────────── 圖 7：§6 剪力摩擦（張開 w = δ·tanα） ─────────────────────
def fig7():
    s = Svg(900, 320)
    s.line(450, 14, 450, 306, C["grid"], 2, "6 5")
    P, A = 60.0, 15.0                  # 齒距、齒高 → tanα = A/(P/2) = 0.5
    tana = A / (P / 2)
    delta = 24.0
    w = delta * tana
    def teeth(x0, x1, y, dx=0.0, dy=0.0):
        pts, x, j = [], x0, 0
        while x <= x1 + 1e-6:
            pts.append((x + dx, y + dy - (A if j % 2 else 0)))
            x += P / 2; j += 1
        return pts
    for side, (x0, title) in enumerate(((60, "滑動前：介面閉合"), (510, "滑動 δ 後：被迫張開 w = δ·tanα"))):
        cx = x0 + 165
        s.text(cx, 28, title, 14, C["dblu"], "middle", True)
        x1 = x0 + 330
        yi = 150
        dx, dy = (delta, -w) if side else (0, 0)
        top = teeth(x0, x1, yi, dx, dy)
        bot = teeth(x0, x1, yi)
        s.poly([(x0 + dx, 60 + dy)] + top + [(x1 + dx, 60 + dy)], "#eceff1", C["edge"], 1.8)
        s.poly([(x0, 240)] + bot + [(x1, 240)], "#cfd8dc", C["edge"], 1.8)
        xb = x0 + 165 - 8
        if not side:
            s.line(xb, 72, xb, 228, C["grn"], 3.4)
            s.text(xb + 8, 222, "植筋 Avf（兩側錨定）", 11.5, C["grn"], bold=True)
            s.line(x0 + P, yi, x0 + P + 34, yi, C["org"], 1.2, "3 2")
            s.text(x0 + P + 22, yi - 3, "α", 12, C["org"], bold=True)
            s.text(cx, 266, f"齒高 / 半齒距 = tanα = {tana:.2f}（粗糙面 ≥ 6 mm 凹凸）", 11.5, C["ink"], "middle")
            s.text(cx, 288, "鋼筋尚未受力", 11.5, C["mut"], "middle")
        else:
            # 鋼筋：上段隨上塊位移，跨介面處被拉長（S 形）
            s.pl([(xb + dx, 72 + dy), (xb + dx, yi - A + dy - 4), (xb, yi + 6), (xb, 228)], C["grn"], 3.4)
            s.arrow(x0 + 40, 74, x0 + 40 + 44, 74, C["red"], 2.4, 9)
            s.text(x0 + 90, 78, "Vu", 12, C["red"], bold=True)
            s.arrow(x1 - 60, 238, x1 - 104, 238, C["red"], 2.4, 9)
            # 張開量標註
            xt = x0 + 2 * P + delta
            s.dim_v(x0 + 300, yi + dy - A, yi - A, f"w = {w:.0f}", C["org"], 10.5, 4, left=False)
            s.dim_h(x0 + P, x0 + P + delta, yi + 22, f"δ = {delta:.0f}", C["org"], 10.5, 4)
            # 夾緊力：鋼筋拉力 → 對混凝土的反作用壓力
            s.arrow(xb + 22, 100, xb + 22, 128, C["grn"], 2, 8)
            s.arrow(xb + 22, 200, xb + 22, 172, C["grn"], 2, 8)
            s.text(xb + 30, 108, "夾緊力", 11.5, C["grn"], bold=True)
            s.text(xb + 30, 194, "= Avf·fy", 11.5, C["grn"], bold=True)
            s.text(cx, 266, "Vn = μ × (Avf · fy)", 13, C["dblu"], "middle", True)
            s.text(cx, 288, "夾緊力是張開的「副產品」，不是外加的", 11.5, C["mut"], "middle")
    return s.svg("剪力摩擦：滑動引起張開，鋼筋受拉產生夾緊力")

# ───────────────────── 圖 8：§8 解題流程 ─────────────────────
def fig8():
    s = Svg(900, 860)
    def box(cx, cy, w, h, lines, fill, stroke, tc):
        s.rect(cx - w / 2, cy - h / 2, w, h, fill, stroke, 1.7, 7)
        n = len(lines); y = cy - (n - 1) * 9.5 + 4
        for j, (t, b) in enumerate(lines):
            s.text(cx, y + j * 19, t, 11.5 if b else 10.5, tc, "middle", b)
    def dia(cx, cy, hw, hh, t):
        s.poly([(cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)], C["org2"], C["org"], 1.7)
        lines = t.split("\n"); y = cy - (len(lines) - 1) * 8 + 4
        for j, l in enumerate(lines):
            s.text(cx, y + j * 16, l, 11.5, "#e65100", "middle", True)
    A = lambda *p: s.arrow(*p, c=C["edge"], w=1.6, head=8)
    lab = lambda x, y, t, a="start": s.text(x, y, t, 11.5, C["edge"], a, True)
    M = 330                                              # 主幹 x
    box(M, 40, 360, 40, [("讀題：認出構件、載重路徑、單位制", True)], C["blu2"], C["blu"], C["dblu"])
    A(M, 60, M, 82)
    dia(M, 122, 200, 40, "是新舊混凝土介面／\n既有裂縫面嗎？")
    box(745, 122, 260, 84, [("摩擦剪力法（§6）", True), ("Vu = 介面必須傳遞的力", False),
                           ("Vn = μ·Avf·fy，φ = 0.75", False), ("μ = 1.4／1.0／0.6", False)], C["grn2"], C["grn"], "#1b5e20")
    A(M + 200, 122, 615, 122); lab(M + 210, 114, "是")
    A(M, 162, M, 190); lab(M + 8, 182, "否")
    dia(M, 232, 200, 42, "集中載重距支承 ≤ 2h\n或淨跨 ln ≤ 4h？")
    box(745, 232, 260, 104, [("D 區 → 壓拉桿模式 STM（§5）", True), ("建壓桿・拉桿・節點；驗 θ ≥ 25°", False),
                            ("βs = 1.0／0.75／0.60", False), ("βn = 1.0（CCC）／0.80（CCT）", False),
                            ("各項取最小 → 判破壞模式", True)], C["grn2"], C["grn"], "#1b5e20")
    A(M + 200, 232, 615, 232); lab(M + 210, 224, "是")
    A(M, 274, M, 302); lab(M + 8, 294, "否")
    dia(M, 346, 180, 44, "臨界斷面可取距支承面 d 處？\n（(a)(b)(c) 三條件，§4）")
    L, R = 125, 535
    s.pl([(M - 180, 346), (L, 346)], C["edge"], 1.6); A(L, 346, L, 410)
    s.pl([(M + 180, 346), (R, 346)], C["edge"], 1.6); A(R, 346, R, 410)
    lab(L + 8, 388, "三者皆成立"); lab(R - 8, 388, "任一不成立", "end")
    box(L, 434, 230, 48, [("Vu 取距支承面 d 處", True), ("反力壓住端區＋載重在頂面", False)], C["blu2"], C["blu"], C["dblu"])
    box(R, 434, 250, 48, [("Vu 取支承面", True), ("吊掛／下翼載重／d 內集中載重", False)], C["blu2"], C["blu"], C["dblu"])
    s.pl([(L, 458), (L, 476), (R, 476), (R, 458)], C["edge"], 1.6); A(M, 476, M, 494)
    box(M, 540, 470, 92, [("算 Vc（四張臉擇一，§2）", True), ("簡化 0.53√f'c bw d ｜ 詳細式（上限 0.93√f'c bw d）", False),
                         ("軸壓 ×(1 + Nu/140Ag)；軸拉 ×(1 + Nu/35Ag)", False), ("耐震塑鉸區 → Vc = 0", True)],
        C["blu2"], C["blu"], C["dblu"])
    A(M, 586, M, 606)
    box(M, 626, 300, 40, [("Vs = Vu/φ − Vc", True)], C["blu2"], C["blu"], C["dblu"])
    D1, D2, D3 = 150, 440, 745
    s.pl([(M, 646), (M, 660), (D1, 660)], C["edge"], 1.6); A(D1, 660, D1, 674)
    dia(D1, 704, 120, 30, "Vs ≤ 2Vc ？")
    dia(D2, 704, 120, 30, "Vs ≤ 4Vc ？")
    A(D1 + 120, 704, D2 - 120, 704); lab(D1 + 128, 696, "否")
    s.pl([(D2 + 120, 704), (D3, 704)], C["edge"], 1.6); A(D3, 704, D3, 744); lab(D2 + 128, 696, "否")
    A(D1, 734, D1, 744); lab(D1 - 10, 744, "是", "end")
    A(D2, 734, D2, 744); lab(D2 - 10, 744, "是", "end")
    box(D1, 768, 250, 48, [("smax = min(d/2, 60 cm)", True), ("裂縫還不密", False)], C["grn2"], C["grn"], "#1b5e20")
    box(D2, 768, 250, 48, [("smax = min(d/4, 30 cm)", True), ("裂縫變密 → 間距減半", False)], C["org2"], C["org"], "#e65100")
    box(D3, 768, 250, 48, [("斷面不足 → 加大斷面", True), ("斜壓桿要壓碎，加箍筋無用", False)], C["red2"], C["red"], "#b71c1c")
    s.pl([(D1, 792), (D1, 806)], C["edge"], 1.6); s.pl([(D2, 792), (D2, 806)], C["edge"], 1.6)
    s.pl([(D1, 806), (D2, 806)], C["edge"], 1.6); A(295, 806, 295, 818)
    box(295, 838, 560, 40, [("三道關卡取最小 s：① 強度 s = Av·fyt·d/Vs　② smax　③ Av,min（Vu > 0.5φVc 時）", True)],
        C["pur2"], C["pur"], "#4a148c")
    return s.svg("RC 剪力題解題決策流程")

FIGS = [("mohr", fig0), ("stages", fig1), ("truss", fig2), ("axial", fig3), ("zones", fig4),
        ("critical", fig5), ("stm-ad", fig6), ("friction", fig7), ("flow", fig8)]

def main(path):
    html = open(path, encoding="utf-8").read()
    if "<!--FIG:" in html:
        for name, fn in FIGS:
            html, n = re.subn(rf"<!--FIG:{name}-->.*?<!--/FIG:{name}-->",
                              lambda m: f"<!--FIG:{name}-->\n{fn()}\n<!--/FIG:{name}-->", html, flags=re.S)
            assert n == 1, name
    else:
        parts = re.split(r'(<div class="fig">\s*<svg\b.*?</svg>)', html, flags=re.S)
        idx = 0
        for i in range(1, len(parts), 2):
            name, fn = FIGS[idx]; idx += 1
            parts[i] = f'<div class="fig">\n<!--FIG:{name}-->\n{fn()}\n<!--/FIG:{name}-->'
        assert idx == len(FIGS), idx
        html = "".join(parts)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    print("ok", len(FIGS), "figs")

if __name__ == "__main__":
    main(sys.argv[1])
