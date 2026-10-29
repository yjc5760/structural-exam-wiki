# -*- coding: utf-8 -*-
"""
gen_lecture-SS-U1-2_figs.py
為 study/lecture-SS-U1-2.html 產生向量圖解（inline SVG）。
所有幾何與曲線皆由斷面性質與講義手算範例的數值算出，不手描。

  範例 ① 單軸對稱 H：上翼 20×1.0、腹 40×1.0、下翼 20×2.0（cm），Fy = 2.5 tf/cm²
  範例 ② 熱軋 H400×200×8×13，Fy = 2.5、Fr = 0.7、E = 2040、G = 800 tf/cm²，Lb = 4.0 m，Cb = 1.14

用法：python gen_lecture-SS-U1-2_figs.py <src.html> <dst.html>（可原地：src = dst）
      → 依 <!--FIG:id--> 標記置換 .fig 內的 <svg>，並印出驗算表。
"""
import math, re, sys

PI = math.pi
# ---------------------------------------------------------------- palette
C_COMP, C_COMP2 = "#c62828", "#ef9a9a"
C_TENS, C_TENS2 = "#2e7d32", "#a5d6a7"
C_BLUE, C_BLUE2 = "#1565c0", "#bbdefb"
C_WARN, C_WARN2 = "#ef6c00", "#ffe0b2"
C_KEY, C_KEY2 = "#6a1b9a", "#e1bee7"
C_INK, C_MUT, C_GRID = "#263238", "#607d8b", "#cfd8dc"
C_STEEL = "#eceff1"


# ---------------------------------------------------------------- helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(s, fs):
    """mini markup → tspans:  X_{ab} 下標、X^{2} 上標、**粗體**"""
    out, i = [], 0
    sub = f'font-size="{fs*0.72:.1f}"'
    pat = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}|\*\*([^*]*)\*\*")
    for m in pat.finditer(s):
        out.append(esc(s[i:m.start()]))
        if m.group(1) is not None:
            out.append(f'<tspan {sub} baseline-shift="sub">{esc(m.group(1))}</tspan>')
        elif m.group(2) is not None:
            out.append(f'<tspan {sub} baseline-shift="super">{esc(m.group(2))}</tspan>')
        else:
            out.append(f'<tspan font-weight="bold">{rich(m.group(3), fs)}</tspan>')
        i = m.end()
    out.append(esc(s[i:]))
    return "".join(out)


def T(x, y, s, fs=11.5, fill=C_INK, anchor="start", bold=False, extra=""):
    b = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{fill}" '
            f'text-anchor="{anchor}"{b} {extra}>{rich(s, fs)}</text>')


def L(x1, y1, x2, y2, c=C_INK, w=1.4, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} {extra}/>'


def R(x, y, w, h, fill="none", stroke=C_INK, sw=1.2, rx=0, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def P(pts, fill="none", stroke=C_INK, sw=1.4, close=False, dash=None, extra=""):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da} {extra}/>'


def arrow(x1, y1, x2, y2, c=C_INK, w=1.6, head=7, dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang) * head * 0.45, math.cos(ang) * head * 0.45
    return (L(x1, y1, bx, by, c, w, dash) +
            P([(x2, y2), (bx + px, by + py), (bx - px, by - py)], fill=c, stroke=c, sw=0.5, close=True))


def dim_v(x, y1, y2, label, c=C_MUT, side=1, fs=10.5):
    """垂直尺寸線（兩端箭頭）"""
    s = arrow(x, (y1 + y2) / 2, x, y1, c, 1, 5) + arrow(x, (y1 + y2) / 2, x, y2, c, 1, 5)
    s += T(x + 5 * side, (y1 + y2) / 2 + 4, label, fs, c, "start" if side > 0 else "end")
    return s


def svg(w, h, body, title):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="sans-serif" role="img" aria-label="{esc(title)}">\n' + body + "\n</svg>")


# ---------------------------------------------------------------- section data
class ExA:  # 範例 ①
    bt, tt, hw, tw, bb, tb = 20.0, 1.0, 40.0, 1.0, 20.0, 2.0
    Fy = 2.5
    d = tt + hw + tb
    A = bt * tt + hw * tw + bb * tb
    ybar = (bt * tt * (tb + hw + tt / 2) + hw * tw * (tb + hw / 2) + bb * tb * tb / 2) / A
    ypna = tb + (A / 2 - bb * tb) / tw
    Ix = (bt * tt ** 3 / 12 + bt * tt * (tb + hw + tt / 2 - ybar) ** 2 +
          tw * hw ** 3 / 12 + hw * tw * (tb + hw / 2 - ybar) ** 2 +
          bb * tb ** 3 / 12 + bb * tb * (ybar - tb / 2) ** 2)
    Zx = (bt * tt * (tb + hw + tt / 2 - ypna) + tw * (tb + hw - ypna) ** 2 / 2 +
          tw * (ypna - tb) ** 2 / 2 + bb * tb * (ypna - tb / 2))
    ctop, cbot = d - ybar, ybar
    Smin = Ix / max(ctop, cbot)
    My = Fy * Smin / 100
    Mp = Fy * Zx / 100


class ExB:  # 範例 ② H400×200×8×13
    d, bf, tw, tf = 40.0, 20.0, 0.8, 1.3
    E, G, Fy, Fr = 2040.0, 800.0, 2.5, 0.7
    Lb, Cb = 400.0, 1.14
    h = d - 2 * tf
    A = 2 * bf * tf + h * tw
    Ix = bf * d ** 3 / 12 - (bf - tw) * h ** 3 / 12
    Sx = Ix / (d / 2)
    Zx = bf * tf * (d - tf) + tw * h * h / 4
    Iy = 2 * tf * bf ** 3 / 12 + h * tw ** 3 / 12
    ry = math.sqrt(Iy / A)
    J = (2 * bf * tf ** 3 + h * tw ** 3) / 3
    h0 = d - tf
    Cw = Iy * h0 ** 2 / 4
    Mp = Fy * Zx
    Mr = (Fy - Fr) * Sx
    Lp = 1.76 * ry * math.sqrt(E / Fy)
    X1 = PI / Sx * math.sqrt(E * G * J * A / 2)
    X2 = 4 * Cw / Iy * (Sx / (G * J)) ** 2
    FL = Fy - Fr
    Lr = ry * X1 / FL * math.sqrt(1 + math.sqrt(1 + X2 * FL ** 2))

    @classmethod
    def Mcr(cls, Lb):  # Cb = 1，精確式
        return PI / Lb * math.sqrt(cls.E * cls.Iy * cls.G * cls.J + (PI * cls.E / Lb) ** 2 * cls.Iy * cls.Cw)

    @classmethod
    def Mcr_GJ(cls, Lb):
        return PI / Lb * math.sqrt(cls.E * cls.Iy * cls.G * cls.J)

    @classmethod
    def Mcr_W(cls, Lb):
        return PI ** 2 * cls.E / Lb ** 2 * math.sqrt(cls.Iy * cls.Cw)

    @classmethod
    def Mn1(cls, Lb):  # Cb = 1 三段式
        if Lb <= cls.Lp:
            return cls.Mp
        if Lb <= cls.Lr:
            return cls.Mp - (cls.Mp - cls.Mr) * (Lb - cls.Lp) / (cls.Lr - cls.Lp)
        return cls.Mcr(Lb)

    @classmethod
    def Mn(cls, Lb, Cb):
        if Lb <= cls.Lp:
            return cls.Mp
        return min(Cb * cls.Mn1(Lb), cls.Mp)

    @classmethod
    def M_of_phi(cls, k, n=4000):
        """彈性-完全塑性，k = φ/φy（φy 對應最外緣 d/2 剛好降伏）。回傳 M (tf·cm) 與降伏深度 ye"""
        c = cls.d / 2
        ye = c / k
        M = 0.0
        dy = c / n
        for i in range(n):
            y = (i + 0.5) * dy
            b = cls.bf if y > cls.h / 2 else cls.tw
            s = cls.Fy * min(1.0, y / ye)
            M += 2 * s * b * y * dy
        return M, ye


# ======================================================================== FIG 0-1
def fig0_1():
    W, H = 720, 350
    b = [T(16, 22, "梁的斷面拆開看：受壓翼板想跑、受拉翼板不肯跑，斷面只好又移又轉", 13.5, C_INK, bold=True)]
    # ---- panel A：斷面分解
    x0, ytop = 30, 70
    fw, ft, hw, wt = 150, 14, 110, 9
    b.append(R(x0, ytop, fw, ft, C_COMP2, C_COMP, 1.4))
    b.append(R(x0 + fw / 2 - wt / 2, ytop + ft, wt, hw, C_STEEL, "#78909c", 1))
    b.append(R(x0, ytop + ft + hw, fw, ft, C_TENS2, C_TENS, 1.4))
    b.append(L(x0 - 8, ytop + ft + hw / 2, x0 + fw + 8, ytop + ft + hw / 2, C_MUT, 1, "4 3"))
    b.append(T(x0 + fw + 10, ytop + ft + hw / 2 + 4, "中性軸", 10, C_MUT))
    b.append(T(x0, ytop - 10, "受壓翼板 ＝ 一根壓桿", 12, C_COMP, bold=True))
    b.append(T(x0, ytop + 2 * ft + hw + 22, "受拉翼板 ＝ 一根拉桿", 12, C_TENS, bold=True))
    b.append(T(x0 + fw / 2 + 10, ytop + ft + 30, "腹板", 10.5, C_MUT))
    b.append(T(x0, ytop + 2 * ft + hw + 44, "腹板把兩者綁在一起，", 11, C_MUT))
    b.append(T(x0, ytop + 2 * ft + hw + 62, "不准它們各走各的。", 11, C_MUT))
    b.append(L(232, 46, 232, 330, C_GRID, 1.2))

    # ---- panel B：俯視圖（兩側撐間）
    bx0, bx1 = 262, 452
    yt, yb = 118, 218  # 上、下翼板在俯視圖中的基準線位置（示意，分開畫）
    b.append(T(bx0 - 8, 62, "俯視圖：兩個側撐點之間", 12, C_INK, bold=True))
    ut, ub = 34.0, 9.0   # 跨中側移（px），上翼 > 下翼
    for yy, amp, col, lab in [(yt, ut, C_COMP, "受壓翼板"), (yb, ub, C_TENS, "受拉翼板")]:
        b.append(L(bx0, yy, bx1, yy, col, 1, "3 3", 'opacity="0.55"'))
        pts = [(bx0 + (bx1 - bx0) * t / 40, yy + amp * math.sin(PI * t / 40)) for t in range(41)]
        b.append(P(pts, stroke=col, sw=3.2))
        b.append(arrow((bx0 + bx1) / 2, yy, (bx0 + bx1) / 2, yy + amp, col, 1.2, 5))
        b.append(T(bx0 + 8, yy - 9, lab, 10.5, col, bold=True))
    b.append(T((bx0 + bx1) / 2 + 6, yt + ut / 2 + 4, "u_{上}", 11, C_COMP))
    b.append(T((bx0 + bx1) / 2 + 6, yb + ub / 2 + 10, "u_{下}", 11, C_TENS))
    for xx in (bx0, bx1):  # 側撐符號
        for yy in (yt, yb):
            b.append(P([(xx - 5, yy - 5), (xx + 5, yy + 5)], stroke=C_INK, sw=2))
            b.append(P([(xx - 5, yy + 5), (xx + 5, yy - 5)], stroke=C_INK, sw=2))
    b.append(L(bx0, 250, bx1, 250, C_MUT, 1))
    b.append(L(bx0, 245, bx0, 255, C_MUT, 1) + L(bx1, 245, bx1, 255, C_MUT, 1))
    b.append(T((bx0 + bx1) / 2, 266, "L_{b}（側撐間距）", 11, C_INK, "middle", True))
    b.append(T(bx0 - 8, 292, "× ＝側撐點（不准側移）", 10.5, C_MUT))
    b.append(T(bx0 - 8, 310, "受壓翼板像壓桿一樣往側面拱，", 10.5, C_COMP))
    b.append(T(bx0 - 8, 327, "受拉翼板被拉直，幾乎不動。", 10.5, C_TENS))
    b.append(L(478, 46, 478, 330, C_GRID, 1.2))

    # ---- panel C：跨中斷面（正視），剛體 平移 u ＋ 轉角 φ
    cx, cy = 600, 168
    s = 2.6  # px/cm，斷面以 40×20 cm 繪
    hh, bf, tf_, tw_ = 40.0, 20.0, 1.6, 1.0
    b.append(T(498, 62, "跨中斷面：平移 u ＋ 轉角 φ", 12, C_KEY, bold=True))

    def sect(dx, phi):
        polys = []
        for (x1, y1, x2, y2) in [(-bf / 2, hh / 2 - tf_, bf / 2, hh / 2),
                                 (-tw_ / 2, -hh / 2 + tf_, tw_ / 2, hh / 2 - tf_),
                                 (-bf / 2, -hh / 2, bf / 2, -hh / 2 + tf_)]:
            pts = []
            for (x, y) in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]:
                xr = x * math.cos(phi) + y * math.sin(phi) + dx
                yr = -x * math.sin(phi) + y * math.cos(phi)
                pts.append((cx + xr * s, cy - yr * s))
            polys.append(pts)
        return polys

    for pts in sect(0, 0):
        b.append(P(pts, fill="none", stroke="#90a4ae", sw=1, close=True, dash="4 3"))
    u_cm, phi = 6.5, math.radians(13)
    cols = [(C_COMP2, C_COMP), (C_STEEL, "#78909c"), (C_TENS2, C_TENS)]
    for pts, (f, st) in zip(sect(u_cm, phi), cols):
        b.append(P(pts, fill=f, stroke=st, sw=1.3, close=True))
    # 剪力中心
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#90a4ae"/>')
    b.append(f'<circle cx="{cx + u_cm * s:.1f}" cy="{cy:.1f}" r="3.2" fill="{C_KEY}"/>')
    b.append(arrow(cx, cy, cx + u_cm * s, cy, C_KEY, 1.4, 6))
    b.append(T(cx + u_cm * s / 2, cy - 6, "u", 11, C_KEY, "middle", True))
    # 上、下翼板中點位移
    yt_c = (hh - tf_) / 2
    xt = (yt_c * math.sin(phi) + u_cm)
    xb = (-yt_c * math.sin(phi) + u_cm)
    ytop_px, ybot_px = cy - yt_c * s - 20, cy + yt_c * s + 22
    b.append(arrow(cx, ytop_px, cx + xt * s, ytop_px, C_COMP, 1.3, 5))
    b.append(T(cx + xt * s + 4, ytop_px + 4, "u_{上}＝u＋φh_{0}/2", 10.5, C_COMP))
    b.append(arrow(cx, ybot_px, cx + xb * s, ybot_px, C_TENS, 1.3, 5))
    b.append(T(cx + xb * s + 6, ybot_px + 4, "u_{下}＝u－φh_{0}/2", 10.5, C_TENS))
    # 轉角弧
    r_ = 26
    a0, a1 = -PI / 2, -PI / 2 + phi
    sx_, sy_ = cx + u_cm * s, cy
    arc = (f'<path d="M{sx_ + r_ * math.cos(a0):.1f} {sy_ + r_ * math.sin(a0):.1f} '
           f'A{r_} {r_} 0 0 1 {sx_ + r_ * math.cos(a1):.1f} {sy_ + r_ * math.sin(a1):.1f}" '
           f'fill="none" stroke="{C_KEY}" stroke-width="1.3"/>')
    b.append(arc + L(sx_, sy_, sx_, sy_ - r_ - 6, C_KEY, 0.8, "2 2"))
    b.append(T(sx_ + 6, sy_ - r_ - 4, "φ", 12, C_KEY, bold=True))
    b.append(T(498, 300, "灰虛線＝原位置；● ＝剪力中心", 10.5, C_MUT))
    b.append(T(498, 320, "**側移 u ＋ 扭轉 φ ＝ LTB**", 12, C_KEY))
    b.append(T(498, 338, "控制參數：r_{y}（或 r_{T}）、L_{b}、C_{b}", 10.5, C_MUT))
    return svg(W, H, "\n".join(b), "LTB 機制：俯視側移與斷面平移加轉角")


# ======================================================================== FIG 0-2（僅修正框寬）
def patch_fig0_2(s):
    s = s.replace('<rect x="185" y="132" width="337" height="58"', '<rect x="150" y="132" width="420" height="58"')
    s = s.replace('<text x="200" y="153"', '<text x="166" y="153"').replace('<text x="200" y="173"', '<text x="166" y="173"')
    return s


# ======================================================================== FIG 1-1
def fig1_1():
    B = ExB
    W, H = 720, 510
    b = [T(16, 22, "H400×200×8×13 被彎到底：應力分佈（上）與彎矩—曲率曲線（下），全部依斷面算出", 13, C_INK, bold=True)]
    My = B.Fy * B.Sx
    Mp = B.Mp
    sc = 4.0                 # px / cm（斷面深度方向）
    y_mid = 140
    ytop, ybot = y_mid - B.d / 2 * sc, y_mid + B.d / 2 * sc
    # 斷面
    sx0 = 30
    sw = B.bf * sc * 0.75   # 翼寬略縮（僅為了版面，深度方向真比例）
    b.append(R(sx0, ytop, sw, B.tf * sc, C_STEEL, "#78909c", 1))
    b.append(R(sx0, ybot - B.tf * sc, sw, B.tf * sc, C_STEEL, "#78909c", 1))
    b.append(R(sx0 + sw / 2 - B.tw * sc / 2, ytop + B.tf * sc, B.tw * sc, B.h * sc, C_STEEL, "#78909c", 1))
    b.append(T(sx0 + sw / 2, ybot + 18, "斷面（深度真比例）", 10, C_MUT, "middle"))

    stages = [  # (k=φ/φy, 標題, 色)
        (0.6, "① 全彈性", C_BLUE),
        (1.0, "② 初始降伏", C_BLUE),
        (2.0, "③ 部分塑化", C_WARN),
        (60.0, "④ 全斷面塑化", C_COMP),
    ]
    sw_ = 46   # Fy 對應的水平長度(px)
    pts_k = []
    for i, (k, title, col) in enumerate(stages):
        ax = 190 + i * 132
        if k >= 50:
            M, ye = Mp, 0.0
        else:
            M, ye = B.M_of_phi(k)
        pts_k.append((k, M))
        # 應力剖面：壓（上，往右）拉（下，往左）
        prof = []
        N = 80
        for j in range(N + 1):
            y = B.d / 2 - B.d * j / N
            if k >= 50:
                sig = 0.0 if abs(y) < 1e-9 else (B.Fy if y > 0 else -B.Fy)
            elif k < 1:
                sig = B.Fy * k * y / (B.d / 2)
            else:
                sig = B.Fy * max(-1.0, min(1.0, y / ye))
            prof.append((ax + sig / B.Fy * sw_, y_mid - y * sc))
        top = [(ax, ytop)] + [p for p in prof if p[1] <= y_mid] + [(ax, y_mid)]
        bot = [(ax, y_mid)] + [p for p in prof if p[1] >= y_mid] + [(ax, ybot)]
        if k >= 50:
            top = [(ax, ytop), (ax + sw_, ytop), (ax + sw_, y_mid), (ax, y_mid)]
            bot = [(ax, y_mid), (ax - sw_, y_mid), (ax - sw_, ybot), (ax, ybot)]
        b.append(P(top, fill=C_COMP2 if k > 1 else C_BLUE2, stroke=C_COMP if k > 1 else C_BLUE, sw=1.2, close=True))
        b.append(P(bot, fill=C_TENS2 if k > 1 else C_BLUE2, stroke=C_TENS if k > 1 else C_BLUE, sw=1.2, close=True))
        b.append(L(ax, ytop - 6, ax, ybot + 6, C_INK, 1))
        # Fy 參考虛線
        b.append(L(ax + sw_, ytop - 4, ax + sw_, y_mid, C_MUT, 0.8, "3 3"))
        b.append(L(ax - sw_, y_mid, ax - sw_, ybot + 4, C_MUT, 0.8, "3 3"))
        if i == 0:
            b.append(T(ax + sw_, ytop - 8, "+F_{y}", 9.5, C_MUT, "middle"))
            b.append(T(ax - sw_, ybot + 16, "－F_{y}", 9.5, C_MUT, "middle"))
        if 1 < k < 50:   # 標彈性核
            yy = ye * sc
            b.append(L(ax - sw_ - 4, y_mid - yy, ax + sw_ + 8, y_mid - yy, C_WARN, 0.9, "2 2"))
            b.append(L(ax - sw_ - 8, y_mid + yy, ax + sw_ + 4, y_mid + yy, C_WARN, 0.9, "2 2"))
            b.append(T(ax + sw_ + 10, y_mid - yy + 4, f"y_{{e}}={ye:.0f} cm", 9.5, C_WARN))
        if k == 1.0:
            b.append(f'<circle cx="{ax + sw_:.1f}" cy="{ytop:.1f}" r="3.2" fill="{C_COMP}"/>')
            b.append(f'<circle cx="{ax - sw_:.1f}" cy="{ybot:.1f}" r="3.2" fill="{C_COMP}"/>')
        b.append(T(ax - 50, ybot + 34, title, 12, col, bold=True))
        b.append(T(ax - 50, ybot + 52, f"M/M_{{y}} = {M / My:.2f}", 11, C_INK))
    b.append(T(30, ybot + 74, "＊③ 只多轉 φ/φ_{y} = 2 倍，M 就已達 M_{p} 的 "
               f"{pts_k[2][1] / Mp * 100:.0f}% ——H 型鋼的材料集中在翼板，翼板一降伏，剩下的潛力只有腹板。", 10.5, C_MUT))

    # ---- M-φ 曲線
    gx0, gx1, gy0, gy1 = 70, 670, 488, 330
    kmax, mmax = 6.0, 1.2
    X = lambda k: gx0 + (gx1 - gx0) * k / kmax
    Y = lambda m: gy0 - (gy0 - gy1) * m / mmax
    b.append(L(gx0, gy0, gx1 + 8, gy0, C_INK, 1.4) + L(gx0, gy0, gx0, gy1 - 10, C_INK, 1.4))
    for kk in range(0, 7):
        b.append(L(X(kk), gy0, X(kk), gy0 + 4, C_INK, 1) + T(X(kk), gy0 + 15, str(kk), 9.5, C_MUT, "middle"))
    b.append(T(gx1 + 10, gy0 + 4, "φ/φ_{y}", 11, C_INK))
    for mm in (0.5, 1.0):
        b.append(L(gx0 - 4, Y(mm), gx0, Y(mm), C_INK, 1) + T(gx0 - 7, Y(mm) + 4, f"{mm:.1f}", 9.5, C_MUT, "end"))
    b.append(T(gx0 - 8, gy1 - 14, "M/M_{y}", 11, C_INK, "end"))
    b.append(L(gx0, Y(Mp / My), gx1, Y(Mp / My), C_COMP, 1, "5 4"))
    b.append(T(gx1, Y(Mp / My) - 5, f"M_{{p}}/M_{{y}} = Z_{{x}}/S_{{x}} = {Mp / My:.3f}", 10.5, C_COMP, "end", True))
    b.append(L(gx0, Y(1), gx1, Y(1), C_BLUE, 0.8, "3 4"))
    curve = [(X(0), Y(0))]
    for i in range(1, 121):
        k = kmax * i / 120
        if k <= 1:
            m = k
        else:
            m = B.M_of_phi(k, 1500)[0] / My
        curve.append((X(k), Y(m)))
    b.append(P(curve, stroke=C_INK, sw=2.2))
    # 翼板全降伏點
    kf = (B.d / 2) / (B.h / 2)
    Mf = B.M_of_phi(kf)[0] / My
    b.append(f'<circle cx="{X(kf):.1f}" cy="{Y(Mf):.1f}" r="3" fill="{C_WARN}"/>')
    b.append(T(X(kf) + 14, Y(Mf) + 44, f"翼板全部降伏：φ/φ_{{y}} = {kf:.2f}，M/M_{{y}} = {Mf:.2f}", 10, C_WARN))
    for (k, M), (_, title, col) in zip(pts_k, stages):
        if k >= 50:
            continue
        b.append(f'<circle cx="{X(k):.1f}" cy="{Y(M / My):.1f}" r="4" fill="{col}" stroke="#fff" stroke-width="1"/>')
        b.append(T(X(k) + (8 if k > 1.5 else -6), Y(M / My) + (22 if k > 1.5 else -8), title[0], 11, col, "start" if k > 1.5 else "end", True))
    b.append(T(X(4.2), Y(Mp / My) - 6, "④ 漸近 M_{p}（形成塑性鉸）", 10.5, C_COMP, "middle", True))
    return svg(W, H, "\n".join(b), "應力分佈四階段與彎矩曲率曲線")


# ======================================================================== FIG 1-2（新）範例 ①
def fig1_2():
    A = ExA
    W, H = 760, 370
    b = [T(16, 22, "範例 ① 依比例：ENA 管 S_{x}（彈性），PNA 管 Z_{x}（塑性）——兩條軸差 "
           f"{A.ybar - A.ypna:.2f} cm", 13, C_INK, bold=True)]
    sc = 6.0
    yb = 334
    Yc = lambda y: yb - y * sc       # y 自底部量起（cm）
    x0 = 110
    cxs = x0 + A.bb * sc / 2
    b.append(R(x0, Yc(A.d), A.bt * sc, A.tt * sc, C_COMP2, C_COMP, 1.2))
    b.append(R(cxs - A.tw * sc / 2, Yc(A.tb + A.hw), A.tw * sc, A.hw * sc, C_STEEL, "#78909c", 1))
    b.append(R(x0, Yc(A.tb), A.bb * sc, A.tb * sc, C_TENS2, C_TENS, 1.2))
    b.append(T(x0 + A.bt * sc + 6, Yc(A.d) + 4, "上翼 20×1.0", 10, C_COMP))
    b.append(T(x0 + A.bb * sc + 6, Yc(A.tb / 2) + 4, "下翼 20×2.0", 10, C_TENS))
    b.append(T(cxs + 6, Yc(30) , "腹板 40×1.0", 10, C_MUT))
    # ENA / PNA
    for y, col, lab in [(A.ybar, C_BLUE, f"ENA  ȳ = {A.ybar:.2f}"), (A.ypna, C_KEY, f"PNA  y = {A.ypna:.2f}")]:
        b.append(L(x0 - 6, Yc(y), x0 + A.bb * sc + 14, Yc(y), col, 1.4, "6 3"))
        b.append(T(x0 + A.bb * sc + 18, Yc(y) + 4, lab, 10.5, col, "start", True))
    b.append(dim_v(x0 - 16, Yc(A.d), Yc(A.ybar), f"c_{{上}}={A.ctop:.2f}", C_BLUE, -1, 10))
    b.append(dim_v(x0 - 16, Yc(A.ybar), Yc(0), f"c_{{下}}={A.cbot:.2f}", C_BLUE, -1, 10))
    b.append(T(x0 + A.bb * sc / 2, yb + 20, "（cm，自底部量起）", 10, C_MUT, "middle"))

    # 彈性應力（繞 ENA）
    ax = 440
    sf = 34 / A.Fy
    st_top = A.Fy
    st_bot = A.Fy * A.cbot / A.ctop
    b.append(T(ax, 50, "彈性（繞 ENA）", 11.5, C_BLUE, "middle", True))
    b.append(T(ax, 66, "上緣先到 F_{y}", 10.5, C_BLUE, "middle"))
    b.append(P([(ax, Yc(A.d)), (ax + st_top * sf, Yc(A.d)), (ax, Yc(A.ybar))], fill=C_COMP2, stroke=C_COMP, sw=1.2, close=True))
    b.append(P([(ax, Yc(A.ybar)), (ax - st_bot * sf, Yc(0)), (ax, Yc(0))], fill=C_TENS2, stroke=C_TENS, sw=1.2, close=True))
    b.append(L(ax, Yc(A.d) - 6, ax, Yc(0) + 6, C_INK, 1))
    b.append(L(ax - 44, Yc(A.ybar), ax + 44, Yc(A.ybar), C_BLUE, 1, "6 3"))
    b.append(T(ax + st_top * sf + 4, Yc(A.d) + 4, "F_{y}=2.50", 10, C_COMP))
    b.append(T(ax - st_bot * sf - 4, Yc(0) + 4, f"{st_bot:.2f}", 10, C_TENS, "end"))
    b.append(T(ax, yb + 20, f"S_{{x,min}} = I_{{x}}/c_{{上}} = {A.Smin:.1f} cm³", 10.5, C_BLUE, "middle"))

    # 塑性應力（繞 PNA）
    px = 600
    b.append(T(px, 50, "塑性（繞 PNA）", 11.5, C_KEY, "middle", True))
    b.append(T(px, 66, "上下面積各 50 cm²", 10.5, C_KEY, "middle"))
    b.append(R(px, Yc(A.d), 34, (A.d - A.ypna) * sc, C_COMP2, C_COMP, 1.2))
    b.append(R(px - 34, Yc(A.ypna), 34, A.ypna * sc, C_TENS2, C_TENS, 1.2))
    b.append(L(px, Yc(A.d) - 6, px, Yc(0) + 6, C_INK, 1))
    b.append(L(px - 44, Yc(A.ypna), px + 44, Yc(A.ypna), C_KEY, 1, "6 3"))
    b.append(T(px + 40, Yc(A.d - 3), "壓 125 tf", 10, C_COMP))
    b.append(T(px - 40, Yc(A.ypna / 2) + 4, "拉 125 tf", 10, C_TENS, "end"))
    b.append(T(px, yb + 20, f"Z_{{x}} = Σ A·ȳ = {A.Zx:.0f} cm³", 10.5, C_KEY, "middle"))
    # 結果
    b.append(R(650, 220, 104, 78, "#fafafa", C_GRID, 1, 6))
    b.append(T(658, 240, f"M_{{y}} = {A.My:.1f} tf·m", 10.5, C_BLUE))
    b.append(T(658, 260, f"M_{{p}} = {A.Mp:.1f} tf·m", 10.5, C_KEY))
    b.append(T(658, 282, f"f = {A.Zx / A.Smin:.2f}", 11.5, C_INK, bold=True))
    return svg(W, H, "\n".join(b), "範例一斷面 ENA 與 PNA 依比例")


# ======================================================================== FIG 3-1
def fig3_1():
    B = ExB
    W, H = 720, 400
    b = [T(16, 22, "抵抗 LTB 的兩種扭轉勁度：短梁靠翹曲（E·C_{w}），長梁靠純扭轉（G·J）", 13.5, C_INK, bold=True)]
    # ---- 左上：純扭轉
    b.append(R(14, 38, 300, 160, "#f5f9ff", "#90caf9", 1, 8))
    b.append(T(26, 58, "① 純扭轉 G·J（St. Venant）", 12, C_BLUE, bold=True))
    b.append(T(26, 76, "每片板各自在厚度內繞一圈剪應力", 10.5, C_MUT))
    cx, cy = 92, 136
    fw, ft, hw, tw = 76, 7, 62, 5
    for (x, y, w, h) in [(cx - fw / 2, cy - hw / 2 - ft, fw, ft), (cx - tw / 2, cy - hw / 2, tw, hw), (cx - fw / 2, cy + hw / 2, fw, ft)]:
        b.append(R(x, y, w, h, C_BLUE2, C_BLUE, 1))
    # 每片板內的剪流小迴圈（示意方向）
    for (x1, x2, y) in [(cx - fw / 2 + 4, cx + fw / 2 - 4, cy - hw / 2 - ft / 2), (cx - fw / 2 + 4, cx + fw / 2 - 4, cy + hw / 2 + ft / 2)]:
        b.append(arrow(x1, y - 1.6, x2, y - 1.6, C_BLUE, 0.8, 4) + arrow(x2, y + 1.6, x1, y + 1.6, C_BLUE, 0.8, 4))
    b.append(arrow(cx - 1.4, cy + hw / 2 - 4, cx - 1.4, cy - hw / 2 + 4, C_BLUE, 0.8, 4) +
             arrow(cx + 1.4, cy - hw / 2 + 4, cx + 1.4, cy + hw / 2 - 4, C_BLUE, 0.8, 4))
    r_ = 50
    b.append(f'<path d="M{cx + r_ * math.cos(-0.5):.1f} {cy + r_ * math.sin(-0.5):.1f} A{r_} {r_} 0 0 1 '
             f'{cx + r_ * math.cos(0.5):.1f} {cy + r_ * math.sin(0.5):.1f}" fill="none" stroke="{C_INK}" stroke-width="1.4"/>')
    b.append(arrow(cx + r_ * math.cos(0.42), cy + r_ * math.sin(0.42), cx + r_ * math.cos(0.5), cy + r_ * math.sin(0.5), C_INK, 1.4, 7))
    b.append(T(cx + 58, cy + 4, "T", 12, C_INK, bold=True))
    b.append(T(170, 108, "J = Σ b·t^{3} / 3", 11.5, C_BLUE, bold=True))
    b.append(T(170, 128, "t 的三次方 → 薄板幾乎沒貢獻", 10.3, C_BLUE))
    b.append(T(170, 148, f"本例 J = {B.J:.1f} cm⁴", 10.3, C_INK))
    b.append(T(170, 168, "單獨提供：M_{cr} ∝ 1/L_{b}", 10.8, C_BLUE, bold=True))
    b.append(T(170, 186, "（長梁主導）", 10.3, C_MUT))

    # ---- 左下：翹曲（俯視上、下翼板反向彎）
    b.append(R(14, 208, 300, 180, "#fbf5fd", "#ce93d8", 1, 8))
    b.append(T(26, 228, "② 翹曲 E·C_{w}（兩片翼板反向側彎）", 12, C_KEY, bold=True))
    b.append(T(26, 246, "俯視：轉 φ 時上翼往右、下翼往左彎（短梁主導）", 10.5, C_MUT))
    x0, x1 = 34, 200
    for yy, sgn, col, lab in [(286, 1, C_COMP, "上翼"), (346, -1, C_TENS, "下翼")]:
        b.append(L(x0, yy, x1, yy, col, 1, "3 3", 'opacity="0.5"'))
        pts = [(x0 + (x1 - x0) * t / 30, yy - sgn * 16 * math.sin(PI * t / 30)) for t in range(31)]
        b.append(P(pts, stroke=col, sw=3))
        b.append(T(x1 + 6, yy + 4, lab, 10, col, bold=True))
    b.append(dim_v(x1 + 40, 286, 346, "h_{0}", C_KEY, 1, 10.5))
    b.append(T(26, 375, "C_{w} = I_{y}h_{0}^{2}/4　單獨提供：M_{cr} ∝ 1/L_{b}^{2}", 10.8, C_KEY, bold=True))

    # ---- 右：依比例的三條曲線
    gx0, gx1, gy0, gy1 = 380, 700, 350, 84
    Lmin, Lmax, Mmax = 100.0, 1000.0, 80.0
    X = lambda Lb: gx0 + (gx1 - gx0) * (Lb - Lmin) / (Lmax - Lmin)
    Y = lambda M: gy0 - (gy0 - gy1) * min(M, Mmax) / Mmax
    b.append(T(gx0 - 20, 52, "H400×200×8×13 實算（C_{b}=1）", 11.5, C_INK, bold=True))
    b.append(L(gx0, gy0, gx1, gy0, C_INK, 1.3) + L(gx0, gy0, gx0, gy1, C_INK, 1.3))
    for Lm in range(1, 11):
        b.append(L(X(Lm * 100), gy0, X(Lm * 100), gy0 + 4, C_INK, 1) + T(X(Lm * 100), gy0 + 15, str(Lm), 9.5, C_MUT, "middle"))
    b.append(T(gx1, gy0 + 30, "L_{b} (m)", 10.5, C_INK, "end"))
    for Mm in range(0, 81, 20):
        b.append(L(gx0 - 4, Y(Mm), gx0, Y(Mm), C_INK, 1) + T(gx0 - 7, Y(Mm) + 4, str(Mm), 9.5, C_MUT, "end"))
        if Mm:
            b.append(L(gx0, Y(Mm), gx1, Y(Mm), "#eceff1", 0.8))
    b.append(T(gx0 + 6, gy1 - 6, "M_{cr} (tf·m)", 10.5, C_INK))

    def curve(f, col, sw, dash=None):
        pts = []
        for i in range(0, 301):
            Lb = Lmin + (Lmax - Lmin) * i / 300
            M = f(Lb) / 100
            if M > Mmax:
                continue
            pts.append((X(Lb), Y(M)))
        return P(pts, stroke=col, sw=sw, dash=dash)

    b.append(curve(B.Mcr_GJ, C_BLUE, 2))
    b.append(curve(B.Mcr_W, C_KEY, 2))
    b.append(curve(B.Mcr, C_INK, 2.6))
    b.append(L(gx0, Y(B.Mp / 100), gx1, Y(B.Mp / 100), C_COMP, 1, "5 4"))
    b.append(T(gx1, Y(B.Mp / 100) - 5, f"M_{{p}} = {B.Mp / 100:.1f}", 10, C_COMP, "end"))
    Ls = PI * math.sqrt(B.E * B.Cw / (B.G * B.J))
    Ms = B.Mcr_GJ(Ls) / 100
    b.append(L(X(Ls), gy0, X(Ls), Y(Ms) - 4, C_MUT, 1, "3 3"))
    b.append(f'<circle cx="{X(Ls):.1f}" cy="{Y(Ms):.1f}" r="3.5" fill="{C_WARN}"/>')
    b.append(T(X(Ls) - 6, Y(7), "兩項相等：", 10, C_WARN, "end", True))
    b.append(T(X(Ls) - 6, Y(2.5), f"L_{{b}}* = π√(EC_{{w}}/GJ) = {Ls / 100:.2f} m", 10, C_WARN, "end", True))
    # labels
    b.append(T(X(470) + 6, Y(B.Mcr(470) / 100) - 6, "合計 M_{cr}", 10.5, C_INK, bold=True))
    b.append(T(X(150), Y(B.Mcr_GJ(150) / 100) + 26, "純扭轉項", 10.5, C_BLUE, bold=True))
    b.append(T(X(300) - 8, Y(B.Mcr_W(300) / 100) + 4, "翹曲項", 10.5, C_KEY, "end", True))
    b.append(T(gx0 + 10, 378, "M_{cr}^{2} = (純扭轉項)^{2} ＋ (翹曲項)^{2}；比 L_{b}* 短由翹曲主導", 10.3, C_MUT))
    return svg(W, H, "\n".join(b), "純扭轉與翹曲勁度，以及 H400x200 的 Mcr 分解")


# ======================================================================== FIG 3-2
def fig3_2():
    B = ExB
    W, H = 720, 440
    b = [T(16, 22, "LTB 強度曲線（依比例）：範例 ② H400×200×8×13，F_{y}=2.5、F_{r}=0.7 tf/cm²", 13.5, C_INK, bold=True)]
    gx0, gx1, gy0, gy1 = 52, 628, 350, 50
    Lmax, Mmax = 1000.0, 40.0
    X = lambda Lb: gx0 + (gx1 - gx0) * Lb / Lmax
    Y = lambda M: gy0 - (gy0 - gy1) * M / Mmax
    Lp, Lr, Mp, Mr = B.Lp, B.Lr, B.Mp / 100, B.Mr / 100
    # 分區底色
    b.append(R(gx0, gy1, X(Lp) - gx0, gy0 - gy1, "#e8f5e9", "none", 0, extra='opacity="0.7"'))
    b.append(R(X(Lp), gy1, X(Lr) - X(Lp), gy0 - gy1, "#fff3e0", "none", 0, extra='opacity="0.7"'))
    b.append(R(X(Lr), gy1, gx1 - X(Lr), gy0 - gy1, "#e3f2fd", "none", 0, extra='opacity="0.7"'))
    b.append(T((gx0 + X(Lp)) / 2, gy0 - 10, "① 塑性", 11.5, C_TENS, "middle", True))
    b.append(T((X(Lp) + X(Lr)) / 2, gy0 - 10, "② 非彈性 LTB", 11.5, C_WARN, "middle", True))
    b.append(T((X(Lr) + gx1) / 2, gy0 - 10, "③ 彈性 LTB", 11.5, C_BLUE, "middle", True))
    # axes & ticks
    b.append(L(gx0, gy0, gx1 + 6, gy0, C_INK, 1.4) + L(gx0, gy0, gx0, gy1 - 6, C_INK, 1.4))
    for Lm in range(0, 11):
        b.append(L(X(Lm * 100), gy0, X(Lm * 100), gy0 + 4, C_INK, 1) + T(X(Lm * 100), gy0 + 16, str(Lm), 9.5, C_MUT, "middle"))
    b.append(T(gx1 + 10, gy0 + 4, "L_{b} (m)", 11, C_INK, "start", True))
    for Mm in range(0, 41, 10):
        b.append(L(gx0 - 4, Y(Mm), gx0, Y(Mm), C_INK, 1) + T(gx0 - 7, Y(Mm) + 4, str(Mm), 9.5, C_MUT, "end"))
    b.append(T(gx0 - 6, gy1 - 12, "M_{n} (tf·m)", 11, C_INK, "start", True))
    # ref lines
    b.append(L(gx0, Y(Mp), gx1, Y(Mp), C_COMP, 0.9, "5 4"))
    b.append(T(gx1 + 6, Y(Mp) + 4, f"M_{{p}} = {Mp:.2f}", 10.5, C_COMP, "start", True))
    b.append(L(gx0, Y(Mr), gx1, Y(Mr), C_WARN, 0.9, "5 4"))
    b.append(T(gx1 + 6, Y(Mr) + 4, f"M_{{r}} = {Mr:.2f}", 10.5, C_WARN, "start", True))
    b.append(T(gx1 + 6, Y(Mr) + 18, "＝(F_{y}－F_{r})S_{x}", 9.5, C_WARN, "start"))
    for Lx, lab in [(Lp, f"L_{{p}}={Lp / 100:.2f}"), (Lr, f"L_{{r}}={Lr / 100:.2f}")]:
        b.append(L(X(Lx), gy0, X(Lx), gy1, C_MUT, 0.9, "3 3"))
        b.append(T(X(Lx), gy0 + 32, lab, 10, C_INK, "middle", True))
    # 理論彈性曲線（全域，裁切到圖框）
    pts = []
    for i in range(1, 501):
        Lb = Lmax * i / 500
        M = B.Mcr(Lb) / 100
        if M <= Mmax:
            pts.append((X(Lb), Y(M)))
    b.append(P(pts, stroke="#78909c", sw=1.6, dash="6 4"))
    # 理論高估的區域（Lp~Lr 間 Mcr 與直線之間），只畫到 Mmax
    poly = []
    for i in range(0, 101):
        Lb = Lp + (Lr - Lp) * i / 100
        poly.append((X(Lb), Y(min(B.Mcr(Lb) / 100, min(Mp, Mmax)))))
    for i in range(100, -1, -1):
        Lb = Lp + (Lr - Lp) * i / 100
        poly.append((X(Lb), Y(B.Mn1(Lb) / 100)))
    b.append(P(poly, fill="#90a4ae", stroke="none", sw=0, close=True, extra='opacity="0.22"'))
    # Cb = 1.14 曲線
    pts = [(X(Lmax * i / 500), Y(B.Mn(Lmax * i / 500 + 1e-9, B.Cb) / 100)) for i in range(0, 501)]
    b.append(P(pts, stroke=C_KEY, sw=1.6, dash="2 3"))
    # Cb = 1 三段式（主曲線）
    seg1 = [(X(0), Y(Mp)), (X(Lp), Y(Mp))]
    seg2 = [(X(Lp), Y(Mp)), (X(Lr), Y(Mr))]
    seg3 = [(X(Lr + (Lmax - Lr) * i / 200), Y(B.Mcr(Lr + (Lmax - Lr) * i / 200) / 100)) for i in range(201)]
    b.append(P(seg1, stroke=C_TENS, sw=3.4) + P(seg2, stroke=C_WARN, sw=3.4) + P(seg3, stroke=C_BLUE, sw=3.4))
    b.append(f'<circle cx="{X(Lr):.1f}" cy="{Y(Mr):.1f}" r="3.5" fill="{C_INK}"/>')
    # 範例點
    M1 = B.Mn1(B.Lb) / 100
    Mc = B.Mn(B.Lb, B.Cb) / 100
    b.append(L(X(B.Lb), gy0, X(B.Lb), Y(Mc), C_KEY, 1, "2 2"))
    b.append(f'<circle cx="{X(B.Lb):.1f}" cy="{Y(M1):.1f}" r="4.5" fill="{C_WARN}" stroke="#fff" stroke-width="1.2"/>')
    b.append(f'<circle cx="{X(B.Lb):.1f}" cy="{Y(Mc):.1f}" r="4.5" fill="{C_KEY}" stroke="#fff" stroke-width="1.2"/>')
    b.append(T(X(B.Lb) - 8, Y(M1) + 18, f"C_{{b}}=1：{M1:.2f}", 10.5, C_WARN, "end", True))
    b.append(T(X(B.Lb) - 8, Y(Mc) - 13, f"×1.14 → {Mc:.2f} ≤ M_{{p}}", 10.5, C_KEY, "end", True))
    b.append(T(X(B.Lb), gy0 + 32, "L_{b}=4.00", 10, C_KEY, "middle", True))
    Mcr4 = B.Mcr(B.Lb) / 100
    b.append(T(X(712), Y(9.0), "灰陰影＝理論解高估區", 10, "#546e7a", "start", True))
    b.append(T(X(712), Y(9.0) + 15, f"L_{{b}}=4 m：理論 M_{{cr}} = {Mcr4:.1f}", 10, "#546e7a"))
    b.append(T(X(712), Y(9.0) + 30, f"規範直線只給 {M1:.2f}（{M1 / Mcr4 * 100:.0f}%）", 10, "#546e7a"))
    b.append(T(X(Lr) - 8, Y(Mr) + 16, "L_{r} 處 M_{cr} = M_{r}", 10, C_INK, "end"))
    # legend
    ly = 426
    for i, (col, dash, lab) in enumerate([(C_INK, None, "規範三段式（C_{b}=1）"), ("#78909c", "6 4", "理論彈性 M_{cr}"),
                                          (C_KEY, "2 3", "C_{b}=1.14")]):
        x = 60 + i * 170
        b.append(L(x, ly - 4, x + 28, ly - 4, col, 2.4 if not dash else 1.6, dash))
        b.append(T(x + 34, ly, lab, 10.5, C_INK))
    b.append(R(570, ly - 10, 18, 10, "#90a4ae", "none", 0, 'opacity="0.35"') + T(592, ly, "理論高估區", 10.5, C_INK))
    return svg(W, H, "\n".join(b), "LTB 三區段強度曲線依比例繪製")


# ======================================================================== FIG 4-1
def fig4_1():
    W, H = 720, 490
    b = [T(16, 22, "C_{b} 四分點公式：同樣的 M_{max}、同樣的 L_{b}，彎矩圖越「尖」紅利越大", 13.5, C_INK, bold=True)]
    cases = [
        ("均勻彎矩", lambda t: 1.0, C_COMP),
        ("一端為零（線性）", lambda t: t, C_TENS),
        ("簡支＋均佈（拋物線）", lambda t: 4 * t * (1 - t), C_TENS),
        ("簡支＋跨中集中力", lambda t: 2 * t if t <= .5 else 2 * (1 - t), C_TENS),
        ("反曲率（等端彎矩）", lambda t: 1 - 2 * t, C_TENS),
    ]
    pw, ph = 216, 206
    for idx, (title, f, col) in enumerate(cases):
        r, c = divmod(idx, 3)
        ox, oy = 18 + c * 232, 40 + r * 222
        b.append(R(ox, oy, pw, ph, "#fff", C_GRID, 1, 8))
        MA, MB, MC = abs(f(.25)), abs(f(.5)), abs(f(.75))
        Mmax = max(abs(f(i / 200)) for i in range(201))
        Cb = 12.5 * Mmax / (2.5 * Mmax + 3 * MA + 4 * MB + 3 * MC)
        good = abs(Cb - 1) > 1e-6
        b.append(T(ox + 10, oy + 20, title, 11.5, C_INK, bold=True))
        b.append(T(ox + pw - 10, oy + 20, f"C_{{b}} = {Cb:.2f}", 12, (C_TENS if good else C_COMP), "end", True))
        x0, x1 = ox + 16, ox + pw - 16
        ybase = oy + 98
        sc = 40
        # beam & braces
        b.append(L(x0, ybase, x1, ybase, C_INK, 2))
        for xx in (x0, x1):
            b.append(P([(xx - 4, ybase - 4), (xx + 4, ybase + 4)], stroke=C_INK, sw=1.8) +
                     P([(xx - 4, ybase + 4), (xx + 4, ybase - 4)], stroke=C_INK, sw=1.8))
        pts = [(x0, ybase)] + [(x0 + (x1 - x0) * i / 100, ybase + sc * f(i / 100)) for i in range(101)] + [(x1, ybase)]
        fill = C_COMP2 if not good else C_TENS2
        b.append(P(pts, fill=fill, stroke=(C_COMP if not good else C_TENS), sw=1.3, close=True, extra='fill-opacity="0.8"'))
        for t, lab, v in [(.25, "A", MA), (.5, "B", MB), (.75, "C", MC)]:
            xx = x0 + (x1 - x0) * t
            yy = ybase + sc * f(t)
            b.append(L(xx, oy + 46, xx, yy, C_INK, 0.8, "2 2"))
            b.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="2.8" fill="{C_INK}"/>')
            b.append(T(xx, oy + 42, lab, 10, C_INK, "middle", True))
        b.append(T(ox + 10, oy + ph - 42, f"|M_{{A}}|,|M_{{B}}|,|M_{{C}}| = {MA:.2f}, {MB:.2f}, {MC:.2f}", 10.3, C_INK))
        den = 2.5 * Mmax + 3 * MA + 4 * MB + 3 * MC
        b.append(T(ox + 10, oy + ph - 22, f"12.5 / ({2.5 * Mmax:.1f}+{3 * MA:.2f}+{4 * MB:.2f}+{3 * MC:.2f})", 10, C_MUT))
        b.append(T(ox + 10, oy + ph - 7, f"= 12.5 / {den:.2f}  （M 以 M_{{max}}=1 計）", 10, C_MUT))
    # 第 6 格：說明
    ox, oy = 18 + 2 * 232, 40 + 222
    b.append(R(ox, oy, pw, ph, "#fbf5fd", "#ce93d8", 1, 8))
    lines = [("**為什麼均勻彎矩最不利？**", C_KEY), ("整段 L_{b} 每個斷面都在 M_{max}，", C_INK),
             ("沒有任何一段「有餘力」拉住", C_INK), ("別人 → 臨界彎矩最低。", C_INK), ("", C_INK),
             ("**C_{b} = 1.0 是「最保守」**", C_COMP), ("不是「最好」。", C_COMP), ("", C_INK),
             ("中點 B 權重 4 最高：挫屈波形", C_INK), ("在 L_{b} 中央振幅最大。", C_INK)]
    for i, (s, col) in enumerate(lines):
        b.append(T(ox + 12, oy + 24 + i * 16, s, 10.6, col))
    return svg(W, H, "\n".join(b), "五種彎矩圖的 Cb 四分點計算")


# ======================================================================== FIG 10-1
def fig10_1():
    W, H = 740, 760
    b = []

    def box(x, y, w, h, fill, st, l1, l2=None, c1=None, c2=None, rx=7):
        s = R(x, y, w, h, fill, st, 1.5, rx)
        s += T(x + w / 2, y + (19 if l2 else h / 2 + 4.5), l1, 11.6, c1 or st, "middle", True)
        if l2:
            for k, ln in enumerate(l2 if isinstance(l2, list) else [l2]):
                s += T(x + w / 2, y + 37 + 16 * k, ln, 10.6, c2 or st, "middle")
        return s

    def dia(cx, cy, w, h, fill, st, l1, l2):
        s = P([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], fill, st, 1.6, True)
        s += T(cx, cy - 4, l1, 11.6, st, "middle", True) + T(cx, cy + 14, l2, 10.4, st, "middle")
        return s

    cx = 370
    b.append(R(cx - 90, 10, 180, 32, C_INK, "none", 0, 16) + T(cx, 31, "拿到梁桿件題目", 12.5, "#fff", "middle", True))
    b.append(arrow(cx, 42, cx, 60, "#455a64"))
    b.append(box(cx - 140, 60, 280, 46, "#e3f2fd", C_BLUE, "① 整理斷面性質", "Z_{x}, S_{x}, I_{y}, r_{y}, J, C_{w}（非對稱：ENA≠PNA）", "#0d47a1", "#0d47a1"))
    b.append(arrow(cx, 106, cx, 124, "#455a64"))
    b.append(dia(cx, 172, 360, 96, "#fff3e0", C_WARN, "關卡一：寬厚比分類（翼板、腹板）", "λ ≤ λ_{p}？　λ ≤ λ_{r}？"))
    # 三個結果並排
    yk = 246
    b.append(arrow(cx - 180, 172, cx - 270, 172, C_TENS) + arrow(cx - 270, 172, cx - 270, yk, C_TENS))
    b.append(T(cx - 222, 165, "結實", 10.8, C_TENS, "middle", True))
    b.append(box(cx - 350, yk, 160, 52, "#e8f5e9", C_TENS, "M_{n,FLB} = M_{p}", "局部挫屈不控制", "#1b5e20", "#1b5e20"))
    b.append(arrow(cx, 220, cx, yk, C_WARN))
    b.append(T(cx + 8, 238, "非結實", 10.8, C_WARN, "start", True))
    b.append(box(cx - 90, yk, 180, 52, "#fff3e0", C_WARN, "M_{n,FLB}：M_{p}→M_{r} 內插", "依 λ 在 λ_{p}～λ_{r} 間的比例", "#e65100", "#e65100"))
    b.append(arrow(cx + 180, 172, cx + 270, 172, C_COMP) + arrow(cx + 270, 172, cx + 270, yk, C_COMP))
    b.append(T(cx + 222, 165, "細長", 10.8, C_COMP, "middle", True))
    b.append(box(cx + 190, yk, 160, 52, "#ffebee", C_COMP, "M_{n,FLB} < M_{r}", "板梁另有公式（§9.3）", "#b71c1c", "#b71c1c"))
    # 匯流
    ym = 326
    for xx in (cx - 270, cx, cx + 270):
        b.append(L(xx, yk + 52, xx, ym, "#455a64", 1.6))
    b.append(L(cx - 270, ym, cx + 270, ym, "#455a64", 1.6))
    b.append(T(cx + 280, ym + 14, "三條都要繼續走 LTB ↓", 10.3, C_COMP, "end", True))
    b.append(arrow(cx, ym, cx, ym + 20, "#455a64"))
    b.append(box(cx - 160, ym + 20, 320, 46, "#f3e5f5", C_KEY, "② 圈出所有側向支撐點，切段", "每段各自有 L_{b}、C_{b}、M_{u}", "#4a148c", "#4a148c"))
    b.append(arrow(cx, ym + 66, cx, ym + 84, "#455a64"))
    yd2 = ym + 130
    b.append(dia(cx, yd2, 340, 92, "#e8f5e9", C_TENS, "L_{b} ≤ L_{p}？", "埋入 RC 版／剪力釘連續連接 ＝ 完全側撐"))
    b.append(arrow(cx + 170, yd2, cx + 270, yd2, C_TENS) + arrow(cx + 270, yd2, cx + 270, yd2 + 74, C_TENS))
    b.append(T(cx + 220, yd2 - 7, "是", 11, C_TENS, "middle", True))
    b.append(box(cx + 190, yd2 + 74, 160, 50, "#e8f5e9", C_TENS, "M_{n,LTB} = M_{p}", "不必算 L_{r}、C_{b}", "#1b5e20", "#1b5e20"))
    b.append(arrow(cx, yd2 + 46, cx, yd2 + 70, "#455a64"))
    b.append(T(cx + 8, yd2 + 62, "否", 11, C_COMP, "start", True))
    b.append(box(cx - 160, yd2 + 70, 320, 46, "#ffebee", C_COMP, "③ 算 M_{r}、L_{r}（X_{1}、X_{2}）、C_{b}",
                 "M_{r} = (F_{y}－F_{r})S_{x}；F_{r}：熱軋 0.7、銲接 1.16", "#b71c1c", "#b71c1c"))
    b.append(arrow(cx, yd2 + 116, cx, yd2 + 134, "#455a64"))
    yd3 = yd2 + 176
    b.append(dia(cx, yd3, 300, 84, "#e3f2fd", C_BLUE, "L_{b} ≤ L_{r}？", "每段各自判斷"))
    b.append(arrow(cx - 150, yd3, cx - 270, yd3, C_WARN) + arrow(cx - 270, yd3, cx - 270, yd3 + 56, C_WARN))
    b.append(T(cx - 210, yd3 - 7, "是（非彈性）", 10.6, C_WARN, "middle", True))
    b.append(box(cx - 350, yd3 + 56, 160, 50, "#fff3e0", C_WARN, "M_{n,LTB} = C_{b}[直線內插]", "≤ M_{p}", "#e65100", "#e65100"))
    b.append(arrow(cx + 150, yd3, cx + 270, yd3, C_BLUE) + arrow(cx + 270, yd3, cx + 270, yd3 + 56, C_BLUE))
    b.append(T(cx + 210, yd3 - 7, "否（彈性）", 10.6, C_BLUE, "middle", True))
    b.append(box(cx + 190, yd3 + 56, 160, 50, "#e3f2fd", C_BLUE, "M_{n,LTB} = C_{b}M_{cr} ≤ M_{p}", "M_{cr} 取 C_{b}=1 之值", "#0d47a1", "#0d47a1"))
    # 收尾
    yf = yd3 + 140
    b.append(L(cx - 270, yd3 + 106, cx - 270, yf - 14, "#455a64", 1.6) + L(cx + 270, yd3 + 106, cx + 270, yf - 14, "#455a64", 1.6))
    b.append(L(cx + 350, yd2 + 99, cx + 362, yd2 + 99, "#455a64", 1.6) + L(cx + 362, yd2 + 99, cx + 362, yf - 14, "#455a64", 1.6) +
             L(cx + 270, yf - 14, cx + 362, yf - 14, "#455a64", 1.6))
    b.append(L(cx - 270, yf - 14, cx + 270, yf - 14, "#455a64", 1.6))
    b.append(arrow(cx, yf - 14, cx, yf, "#455a64"))
    b.append(R(cx - 230, yf, 460, 62, C_INK, "none", 0, 8))
    b.append(T(cx, yf + 21, "④ 收尾（少一個就扣分）", 12, "#fff", "middle", True))
    b.append(T(cx, yf + 40, "M_{n} = min(M_{n,FLB}, M_{n,LTB}, M_{p})　→　φ_{b}M_{n}（φ_{b}=0.90）≥ M_{u}", 11, "#eceff1", "middle"))
    b.append(T(cx, yf + 56, "→　另檢核剪力（§6）與服務載重撓度（§7）", 10.6, "#b0bec5", "middle"))
    return svg(W, yf + 72, "\n".join(b), "梁桿件解題決策樹")


FIGS = {"0-1": fig0_1, "1-1": fig1_1, "1-2": fig1_2, "3-1": fig3_1, "3-2": fig3_2, "4-1": fig4_1, "10-1": fig10_1}


def report():
    A, B = ExA, ExB
    print("範例①  ybar=%.2f  ypna=%.2f  Ix=%.0f  Smin=%.1f  Zx=%.0f  My=%.2f  Mp=%.2f  f=%.3f" %
          (A.ybar, A.ypna, A.Ix, A.Smin, A.Zx, A.My, A.Mp, A.Zx / A.Smin))
    print("範例②  A=%.2f Ix=%.0f Sx=%.0f Zx=%.0f Iy=%.0f ry=%.2f J=%.2f Cw=%.3e" % (B.A, B.Ix, B.Sx, B.Zx, B.Iy, B.ry, B.J, B.Cw))
    print("        Mp=%.0f Mr=%.0f Lp=%.1f Lr=%.1f X1=%.1f X2=%.3f" % (B.Mp, B.Mr, B.Lp, B.Lr, B.X1, B.X2))
    print("        Mn1(4m)=%.0f  Mn(Cb)=%.0f  phiMn=%.0f   Mcr(Lr)=%.1f vs Mr=%.1f" %
          (B.Mn1(400), B.Mn(400, 1.14), .9 * B.Mn(400, 1.14), B.Mcr(B.Lr), B.Mr))
    print("        Mp/My=%.3f  Lb*=%.1f cm" % (B.Zx / B.Sx, PI * math.sqrt(B.E * B.Cw / (B.G * B.J))))


if __name__ == "__main__":
    report()
    if len(sys.argv) > 2:
        src, dst = sys.argv[1], sys.argv[2]
        html = open(src, encoding="utf-8").read()
        for k, f in FIGS.items():
            pat = re.compile(r"(<!--FIG:%s-->\s*)<svg.*?</svg>" % re.escape(k), re.S)
            html, n = pat.subn(lambda m: m.group(1) + f(), html)
            print("FIG", k, "replaced" if n == 1 else f"!! matches={n}")
        html = re.sub(r'(<svg viewBox="0 0 730 250".*?</svg>)', lambda m: patch_fig0_2(m.group(1)), html, flags=re.S)
        open(dst, "w", encoding="utf-8").write(html)
