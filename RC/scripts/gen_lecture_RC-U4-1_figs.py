#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lecture-RC-U4-1 觀念講義 —— 精準 SVG 圖解產生器

原則：所有幾何由題目給定值與現算結果決定（不手畫比例）。
  RC-2014-4  → 圖 0、圖 1、圖 2、圖 6b（兩階段、三項疊加、C 線、偏心區間）
  RC-2011-5  → 圖 4（三斷面形心與 ep）
  RC-2004-5  → 圖 7（M–φ 三門檻）
  其餘（圖 6a、圖 8）為通用幾何，但曲線形狀用正確函數（拋物線、(L−x)²）。
輸出：figs/<name>.svg（每張一檔，供注入 HTML）
"""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
os.makedirs(OUT, exist_ok=True)

INK, MUT, AX = "#263238", "#607d8b", "#455a64"
BLUE, BLUE2 = "#1565c0", "#0d47a1"
RED, RED2 = "#c62828", "#ffcdd2"
GRN, GRN2 = "#2e7d32", "#c8e6c9"
ORG, ORG2 = "#ef6c00", "#fff3e0"
PUR = "#6a1b9a"
GREY, GREY2 = "#546e7a", "#eceff1"


# ───────────────────────── 基本元件 ─────────────────────────
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=12, anchor="start", fill=INK, bold=False, italic=False):
    w = ' font-weight="700"' if bold else ""
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}"{w}{it}>{esc(s)}</text>')


def L(x1, y1, x2, y2, stroke=AX, w=1.4, dash=None, marker=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    o = f' opacity="{op}"' if op else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{w}"{d}{m}{o}/>')


def P(pts, fill="none", stroke=AX, w=1.5, dash=None, op=None, close=True):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    tag = "polygon" if close else "polyline"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<{tag} points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{da}{o}/>'


def R(x, y, w, h, fill=GREY2, stroke=GREY, sw=1.5, rx=0, dash=None, op=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{o}/>')


def C(x, y, r, fill=INK, stroke="none", sw=1.4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def defs(*colors):
    out = ["<defs>"]
    for name, col in colors:
        out.append(f'<marker id="{name}" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
                   f'orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{col}"/></marker>')
    out.append("</defs>")
    return "".join(out)


def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{esc(label)}">\n' + "\n".join(body) + "\n</svg>")


def stress(x0, yt, yb, ft, fb, k):
    """線性應力圖：壓（+）畫右、紅；拉（−）畫左、綠。回傳 SVG 片段 list。"""
    out = []
    xt, xb = x0 + ft * k, x0 + fb * k
    if ft * fb >= 0:
        sgn = ft + fb
        fill, st = (RED2, RED) if sgn >= 0 else (GRN2, GRN)
        out.append(P([(x0, yt), (xt, yt), (xb, yb), (x0, yb)], fill, st, 1.6))
    else:
        yz = yt + (yb - yt) * ft / (ft - fb)
        f1, s1 = (RED2, RED) if ft > 0 else (GRN2, GRN)
        f2, s2 = (RED2, RED) if fb > 0 else (GRN2, GRN)
        out.append(P([(x0, yt), (xt, yt), (x0, yz)], f1, s1, 1.6))
        out.append(P([(x0, yz), (xb, yb), (x0, yb)], f2, s2, 1.6))
    out.append(L(x0, yt - 8, x0, yb + 8, "#90a4ae", 1.3))
    return out


def col(f):
    return RED if f > 0 else GRN


# ═════════════════════ RC-2014-4 給定與現算 ═════════════════════
L14 = 1200.0                     # cm
A14, I14, c14, e14 = 1100.0, 469_000.0, 30.0, 19.8
S14 = I14 / c14                  # 15,633
r2_14 = I14 / A14                # 426.4
k14 = r2_14 / c14                # 核心距 14.21（對稱，上下相同）
wd, wl = 0.264e3 / 100, 1.1e3 / 100   # kgf/cm
Pi14, Pe14 = 70_000.0, 60_000.0
fci, fc = 300.0, 420.0
Md = wd * L14**2 / 8
MT = (wd + wl) * L14**2 / 8


def terms(Pf, M):
    r = lambda v: round(v, 2)      # 與講義逐項取兩位小數一致
    return dict(ax=r(Pf / A14), ecc=r(Pf * e14 / S14), mom=r(M / S14))


T1, T2 = terms(Pi14, Md), terms(Pe14, MT)
f1t = T1["ax"] - T1["ecc"] + T1["mom"]
f1b = T1["ax"] + T1["ecc"] - T1["mom"]
f2t = T2["ax"] - T2["ecc"] + T2["mom"]
f2b = T2["ax"] + T2["ecc"] - T2["mom"]
assert abs(f1t - 5.38) < 0.006 and abs(f1b - 121.90) < 0.02
assert abs(f2t - 135.61) < 0.006 and abs(f2b + 26.51) < 0.006
lim = dict(ci_c=0.60 * fci, ci_t=-0.80 * math.sqrt(fci),
           c_c=0.45 * fc, c_t16=-1.6 * math.sqrt(fc), c_t10=-1.0 * math.sqrt(fc))

# ═════════════════ 圖 0：兩階段（RC-2014-4 實際應力，同一比例）══════════════
def fig0():
    b = [defs(("a0", ORG))]
    b.append(L(450, 30, 450, 345, "#cfd8dc", 2, "6 5"))
    k = 1.10
    for ox, stage in ((0, 1), (450, 2)):
        cx = ox + 225
        if stage == 1:
            b += [T(cx, 24, "傳遞階段：預力大、載重小", 15, "middle", BLUE2, True),
                  T(cx, 44, "Pi = 70 tf（未損失）　M = 僅自重 Md = 4.75 tf·m", 12.5, "middle", MUT)]
            ft, fb, ac, at = f1t, f1b, lim["ci_c"], lim["ci_t"]
        else:
            b += [T(cx, 24, "使用階段：預力小、載重大", 15, "middle", BLUE2, True),
                  T(cx, 44, "Pe = 60 tf（已損失）　M = Md + Ml = 24.55 tf·m", 12.5, "middle", MUT)]
            ft, fb, ac, at = f2t, f2b, lim["c_c"], lim["c_t16"]
        # 對稱 I 形斷面（示意外形；深度 60 cm、形心、腱位依比例 3 px/cm）
        s = 3.0
        yt, yb = 74, 74 + 60 * s
        yc = yt + c14 * s
        xs = ox + 40
        b.append(P([(xs, yt), (xs + 56, yt), (xs + 56, yt + 18), (xs + 34, yt + 18), (xs + 34, yb - 18),
                    (xs + 56, yb - 18), (xs + 56, yb), (xs, yb), (xs, yb - 18), (xs + 22, yb - 18),
                    (xs + 22, yt + 18), (xs, yt + 18)], GREY2, GREY, 1.5))
        yp = yc + e14 * s
        b.append(L(xs - 6, yc, ox + 440, yc, "#b0bec5", 1, "5 4"))
        b.append(C(xs + 28, yp, 5))
        b.append(L(xs + 66, yc, xs + 66, yp, ORG, 1.2))
        b.append(T(xs + 70, (yc + yp) / 2 + 4, "e=19.8", 11, "start", ORG))
        b.append(T(xs - 4, yc - 4, "形心", 10.5, "end", MUT))
        x0 = ox + 175
        # 容許值線
        for fa, lab, colr in ((ac, f"容許壓 {ac:.0f}", RED), (at, f"容許拉 {at:.1f}", GRN)):
            xa = x0 + fa * k
            b.append(L(xa, yt - 6, xa, yb + 6, colr, 1.2, "4 3"))
            b.append(T(xa + (0 if fa > 0 else -3), yb + 20, lab, 10.5, "middle" if fa > 0 else "end", colr))
        if stage == 2:
            xa = x0 + lim["c_t10"] * k
            b.append(L(xa, yt + 40, xa, yb + 6, "#8d6e63", 1.1, "2 3"))
            b.append(T(xa + 2, yb + 36, "1.0√f'c = −20.5（該題解析採用）", 10.5, "start", "#8d6e63"))
        b += stress(x0, yt, yb, ft, fb, k)
        b.append(T(x0 + ft * k + 6, yt - 6, f"{ft:+.2f}", 12, "start", col(ft), True))
        b.append(T(x0 + fb * k + (6 if fb > 0 else -6), yb - 4, f"{fb:+.2f}",
                   12, "start" if fb > 0 else "end", col(fb), True))
        if stage == 1:
            b.append(L(x0 + 70, yt + 34, x0 + 12, yt + 6, ORG, 1.4, marker="a0"))
            b.append(T(x0 + 74, yt + 40, "頂緣只剩 +5.4，e 再加大就翻成拉", 11.5, "start", ORG, True))
            b += [T(cx, 318, "危險在頂纖維：偏心把它往拉的方向推", 13.5, "middle", GRN, True),
                  T(cx, 338, "容許值用 f'ci = 300（混凝土還嫩，限值小）", 12, "middle", MUT)]
        else:
            b.append(L(x0 + 64, yb - 34, x0 - 8, yb - 8, ORG, 1.4, marker="a0"))
            b.append(T(x0 + 68, yb - 30, "底緣已受拉（未超 32.8，但超過 20.5）", 11.5, "start", ORG, True))
            b += [T(cx, 318, "危險在底纖維：活載重把它拉過零點", 13.5, "middle", GRN, True),
                  T(cx, 338, "容許值用 f'c = 420（強度已足，但載重也最大）", 12, "middle", MUT)]
    return svg(900, 352, b, "RC-2014-4 傳遞與使用階段應力分布對照")


# ═════════════════ 圖 1：三項疊加（兩階段 × 四格，同一比例）═════════════════
def fig1():
    b = []
    k = 0.50
    heads = ["① 軸壓 P/A", "② 偏心 P·e/S", "③ 外力 M/S", "④ 合成 f"]
    subs = ["全斷面同號", "頂拉、底壓", "頂壓、底拉", "代數相加"]
    cxs = [215, 405, 595, 785]
    for cx, h, s_ in zip(cxs, heads, subs):
        b.append(T(cx, 24, h, 14, "middle", BLUE2, True))
        b.append(T(cx, 42, s_, 11.5, "middle", MUT))
    for xo, op in zip((310, 500, 690), ("+", "+", "=")):
        for yy in (150, 350):
            b.append(T(xo, yy, op, 22, "middle", AX))
    rows = [(70, 210, "傳遞階段", "Pi = 70 tf", "M = Md", T1, f1t, f1b),
            (270, 410, "使用階段", "Pe = 60 tf", "M = Md + Ml", T2, f2t, f2b)]
    for yt, yb, n1, n2, n3, TT, ft4, fb4 in rows:
        ym = (yt + yb) / 2
        b += [T(14, ym - 14, n1, 13.5, "start", INK, True), T(14, ym + 6, n2, 12, "start", MUT),
              T(14, ym + 24, n3, 12, "start", MUT)]
        vals = [(TT["ax"], TT["ax"]), (-TT["ecc"], TT["ecc"]), (TT["mom"], -TT["mom"]), (ft4, fb4)]
        for cx, (ft, fb) in zip(cxs, vals):
            b += stress(cx, yt, yb, ft, fb, k)
            b.append(T(cx + ft * k, yt - 12, f"{ft:+.1f}", 11.5, "middle", col(ft), True))
            b.append(T(cx + fb * k, yb + 22, f"{fb:+.1f}", 11.5, "middle", col(fb), True))
    b.append(T(785 - 118, 262, "", 1))
    b.append(T(450, 456, "單位 kgf/cm²，壓為正；八格共用同一水平比例，長度可直接比較", 12, "middle", MUT))
    return svg(900, 466, b, "RC-2014-4 三項應力疊加，傳遞與使用兩階段")


# ═════════════════ 圖 2：C 線沿跨度（RC-2014-4，含核心帶）═════════════════
def fig2():
    b = [defs(("a2", ORG), ("a2b", BLUE))]
    X0, X1 = 90, 810
    sx = (X1 - X0) / L14
    YT, YC = 70, 175
    sy = (YC - YT) / c14          # 3.333 px/cm
    YB = YC + c14 * sy
    X = lambda x: X0 + x * sx
    Y = lambda z: YC + z * sy     # z：形心以下為正（cm）
    b.append(R(X0, YT, X1 - X0, YB - YT, "#f5f7f8", GREY, 1.6))
    b.append(R(X0, Y(-k14), X1 - X0, 2 * k14 * sy, "#e3f2fd", "none", 0, op=0.9))
    b.append(L(X0, Y(-k14), X1, Y(-k14), "#64b5f6", 1, "3 3"))
    b.append(L(X0, Y(k14), X1, Y(k14), "#64b5f6", 1, "3 3"))
    b.append(L(X0, YC, X1, YC, "#90a4ae", 1.2, "7 5"))
    b.append(T(X1 + 6, YC + 4, "形心", 11.5, "start", MUT))
    b.append(T(X1 + 6, Y(-k14) + 4, "上核心點", 11, "start", "#1e88e5"))
    b.append(T(X1 + 6, Y(-k14) + 18, "kt = r²/yb", 10.5, "start", "#1e88e5"))
    b.append(T(X1 + 6, Y(k14) + 4, "下核心點", 11, "start", "#1e88e5"))
    b.append(T(X1 + 6, Y(k14) + 18, "kb = r²/yt", 10.5, "start", "#1e88e5"))
    # 支承
    for xx in (X0, X1):
        b.append(P([(xx, YB), (xx - 9, YB + 15), (xx + 9, YB + 15)], GREY, GREY, 1))
    # 鋼腱（直線、全長 e = 19.8）
    b.append(L(X0, Y(e14), X1, Y(e14), INK, 2.6))
    b.append(T(X0 + 10, Y(e14) + 18, "c.g.s. 鋼腱（直線腱，全長 e = 19.8 cm）", 12, "start", INK, True))
    N = 120
    def cline(Pf, w):
        pts = []
        for i in range(N + 1):
            x = L14 * i / N
            M = w * x * (L14 - x) / 2
            pts.append((X(x), Y(e14 - M / Pf)))
        return pts
    b.append(P(cline(Pi14, wd), "none", BLUE, 2.4, "9 4", close=False))
    b.append(P(cline(Pe14, wd + wl), "none", RED, 2.6, close=False))
    sh1, sh2 = Md / Pi14, MT / Pe14
    xm = X(L14 / 2)
    b.append(T(X(250), Y(e14 - (wd * 250 * (L14 - 250) / 2) / Pi14) - 8, "C 線・傳遞（Md/Pi）", 12, "middle", BLUE, True))
    b.append(T(X(215), Y(e14 - ((wd + wl) * 215 * (L14 - 215) / 2) / Pe14) - 8, "C 線・使用（MT/Pe）", 12, "middle", RED, True))
    # 跨中位移箭頭
    b.append(L(xm + 26, Y(e14), xm + 26, Y(e14 - sh2) + 3, ORG, 1.8, marker="a2"))
    b.append(T(xm + 32, Y(e14 - sh2 / 2), f"MT/Pe = {sh2:.1f} cm", 12, "start", ORG, True))
    b.append(T(xm + 32, Y(e14 - sh2 / 2) + 16, f"→ C 在形心上 {sh2 - e14:.1f} cm > kt", 11.5, "start", ORG))
    b.append(L(xm - 22, Y(e14), xm - 22, Y(e14 - sh1) + 2, BLUE, 1.6, marker="a2b"))
    b.append(T(X1 - 10, Y(e14) + 16, f"傳遞：上移 Md/Pi = {sh1:.1f} cm，C 在形心下 {e14 - sh1:.1f} cm", 11.5, "end", BLUE, True))
    b.append(T(X1 - 10, Y(e14) + 30, f"< kb = {k14:.1f} → 仍在核心帶內，頂緣 +5.4（受壓）", 11, "end", BLUE))
    # 底緣受拉區：MT(x) > Pe(e + kt) = Mdec
    Mdec = Pe14 * (e14 + k14)
    wT = wd + wl
    disc = L14**2 - 8 * Mdec / wT
    xa = (L14 - math.sqrt(disc)) / 2
    xb = L14 - xa
    b.append(R(X(xa), YB + 2, X(xb) - X(xa), 7, GRN2, GRN, 1.2))
    b.append(T(xm, YB + 26, f"使用階段底緣受拉區 x = {xa/100:.2f} ～ {xb/100:.2f} m（C 線越過上核心點之處；"
               f"該點彎矩恰為 Mdec = Pe(e + kt) = {Mdec/1e5:.1f} tf·m）", 11.5, "middle", GRN, True))
    b.append(T(X0, 22, f"RC-2014-4：L = 12 m、h = 60 cm、r² = {r2_14:.1f} cm²；淺藍帶＝核心 ±{k14:.1f} cm；垂直比例放大 {sy/sx:.1f} 倍", 12, "start", MUT))
    b.append(T(X0, 42, "C 線上移量 = M/P：同一條鋼腱，兩個階段的壓力合力走在不同高度", 12.5, "start", INK, True))
    return svg(900, 326, b, "RC-2014-4 壓力線沿跨度位置與核心帶")


# ═════════════════ 圖 6b（新）：四控制條件夾出 e 區間 ═════════════════
def fig6b():
    """RC-2014-4 跨中，P 固定，四式各解出 e 的界限。"""
    # 傳遞頂：P/A − P e/S + Md/S ≥ ci_t
    e_tt = (T1["ax"] + T1["mom"] - lim["ci_t"]) * S14 / Pi14
    # 傳遞底：P/A + P e/S − Md/S ≤ ci_c
    e_tb = (lim["ci_c"] - T1["ax"] + T1["mom"]) * S14 / Pi14
    # 使用底：P/A + P e/S − MT/S ≥ c_t
    e_sb16 = (T2["mom"] - T2["ax"] + lim["c_t16"]) * S14 / Pe14
    e_sb10 = (T2["mom"] - T2["ax"] + lim["c_t10"]) * S14 / Pe14
    # 使用頂：P/A − P e/S + MT/S ≤ c_c
    e_st = (T2["ax"] + T2["mom"] - lim["c_c"]) * S14 / Pe14
    global E_LIMITS
    E_LIMITS = dict(e_tt=e_tt, e_tb=e_tb, e_sb16=e_sb16, e_sb10=e_sb10, e_st=e_st)
    b = []
    X0, X1, EM = 230, 860, 36.0
    sx = (X1 - X0) / EM
    X = lambda e: X0 + e * sx
    rows = [
        ("傳遞・頂緣（拉）", f"e ≤ {e_tt:.2f}", 0, e_tt, GRN, True, None),
        ("傳遞・底緣（壓）", f"e ≤ {e_tb:.2f}", 0, e_tb, "#90a4ae", False, None),
        ("使用・底緣（拉 1.6√f'c）", f"e ≥ {e_sb16:.2f}", e_sb16, EM, RED, True, None),
        ("使用・頂緣（壓）", f"e ≥ {e_st:.2f}", e_st, EM, "#90a4ae", False, None),
        ("使用・底緣（拉 1.0√f'c）", f"e ≥ {e_sb10:.2f}", e_sb10, EM, "#8d6e63", True, "5 3"),
    ]
    y = 62
    for name, rel, a, z, colr, ctrl, dash in rows:
        b.append(T(X0 - 12, y + 12, name, 12.5, "end", INK if ctrl else MUT, ctrl))
        b.append(R(X(a), y, X(z) - X(a), 16, colr, colr, 1, rx=3, dash=dash, op=0.28 if ctrl else 0.18))
        edge = X(z) if z < EM else X(a)
        b.append(L(edge, y - 4, edge, y + 20, colr, 2.6))
        b.append(T(edge + (6 if z < EM else -6), y + 12, rel, 12, "start" if z < EM else "end", colr, True))
        y += 34
    yf = y + 10
    b.append(T(X0 - 12, yf + 12, "可行區間（1.6√f'c）", 12.5, "end", BLUE, True))
    b.append(R(X(e_sb16), yf, X(e_tt) - X(e_sb16), 16, "#bbdefb", BLUE, 1.6, rx=3))
    b.append(T(X(e_tt) + 8, yf + 12, f"{e_sb16:.2f} ≤ e ≤ {e_tt:.2f} → 19.8 ✓", 12, "start", BLUE, True))
    yf2 = yf + 32
    b.append(T(X0 - 12, yf2 + 12, "可行區間（1.0√f'c）", 12.5, "end", "#8d6e63", True))
    b.append(R(X(e_sb10), yf2, X(e_tt) - X(e_sb10), 16, "#efebe9", "#8d6e63", 1.4, rx=3, dash="5 3"))
    b.append(T(X(e_tt) + 8, yf2 + 12, f"{e_sb10:.2f} ≤ e ≤ {e_tt:.2f} → 19.8 ✗", 12, "start", "#8d6e63", True))
    ya = yf2 + 46
    b.append(L(X0, ya, X1, ya, AX, 1.6))
    for e in range(0, 36, 5):
        b.append(L(X(e), ya, X(e), ya + 6, AX, 1.2))
        b.append(T(X(e), ya + 20, str(e), 11.5, "middle", AX))
    b.append(T(X1, ya + 36, "偏心距 e（cm，形心下方）", 12, "end", AX))
    xe = X(e14)
    b.append(L(xe, 44, xe, ya, ORG, 1.8, "6 4"))
    b.append(T(xe, 38, "題給 e = 19.8", 12.5, "middle", ORG, True))
    b.append(T(14, 22, "RC-2014-4 跨中：Pi = 70、Pe = 60 tf 固定，把四個容許值當等式各解一次", 13, "start", BLUE2, True))
    return svg(900, ya + 46, b, "RC-2014-4 四控制條件夾出偏心距區間")


# ═════════════════ 圖 4：三斷面（RC-2011-5 題給性質反算）═════════════════
NET = dict(A=2500.0, Zt=40_000.0, Zb=39_000.0, I=1_800_000.0, e=25.0)
TRAN = dict(A=2800.0, Zt=41_000.0, Zb=43_000.0, I=1_900_000.0, e=24.0)
COMP = dict(A=3900.0, Zt=137_000.0, Zb=74_000.0, I=4_300_000.0, e=39.0)
for S_ in (NET, TRAN, COMP):
    S_["yt"], S_["yb"] = S_["I"] / S_["Zt"], S_["I"] / S_["Zb"]


def fig4():
    b = [defs(("a4", AX))]
    s, YBOT = 2.0, 270
    panels = [(150, NET, "① 淨斷面 (net)", "後拉法張拉瞬間：導管是空洞", "net"),
              (450, TRAN, "② 變換斷面 (transformed)", "灌漿後：鋼腱以 n 倍計入", "tran"),
              (750, COMP, "③ 合成斷面 (composite)", "現場版硬化後：梁＋版共同作用", "comp")]
    hbeam = TRAN["yt"] + TRAN["yb"]
    for cx, S_, t1, t2, kind in panels:
        b.append(T(cx, 22, t1, 14, "middle", BLUE2, True))
        b.append(T(cx, 40, t2, 12, "middle", MUT))
        h = (S_["yt"] + S_["yb"]) if kind != "comp" else hbeam
        top = YBOT - h * s
        if kind == "comp":
            b.append(R(cx - 82, top - 15 * s, 164, 15 * s, "#cfd8dc", GREY, 1.6))
            b.append(T(cx + 86, top - 10, "現場版", 11, "start", MUT))
        b.append(R(cx - 40, top, 80, h * s, GREY2, GREY, 1.6))
        yc = YBOT - S_["yb"] * s
        yp = YBOT - (S_["yb"] - S_["e"]) * s
        b.append(L(cx - 58, yc, cx + 58, yc, BLUE, 1.4, "6 4"))
        b.append(T(cx - 62, yc + 4, f"形心 yb={S_['yb']:.1f}", 11, "end", BLUE))
        if kind == "comp":
            yc0 = YBOT - TRAN["yb"] * s
            b.append(L(cx - 40, yc0, cx + 40, yc0, "#90a4ae", 1, "2 3"))
            b.append(T(cx - 62, yc0 + 14, f"（②形心 {TRAN['yb']:.1f}）", 10.5, "end", MUT))
            b.append(L(cx - 26, yc0, cx - 26, yc + 3, ORG, 1.4, marker="a4"))
            b.append(T(cx - 22, (yc + yc0) / 2 + 5, f"+{S_['yb'] - TRAN['yb']:.1f}", 11, "start", ORG, True))
        for dx in (-13, 13):
            if kind == "net":
                b.append(C(cx + dx, yp, 7, "#fff", RED, 1.6))
            else:
                b.append(C(cx + dx, yp, 7, "#bbdefb", BLUE, 1.6))
        b.append(L(cx + 52, yc, cx + 52, yp, ORG, 1.6))
        b.append(L(cx + 47, yc, cx + 57, yc, ORG, 1.6))
        b.append(L(cx + 47, yp, cx + 57, yp, ORG, 1.6))
        b.append(T(cx + 60, (yc + yp) / 2 + 5, f"ep = {S_['e']:.0f}", 12.5, "start", ORG, True))
        load = {"net": "承受：Fi ＋ 梁自重 MG", "tran": "承受：F0 ＋ MG ＋ 版重 MS",
                "comp": "承受：活載重 ML（只有 ML！）"}[kind]
        b.append(T(cx, 296, load, 12.5, "middle", INK, True))
        b.append(T(cx, 316, f"A = {S_['A']:.0f}、Zt = {S_['Zt']/1e3:.0f}k、Zb = {S_['Zb']/1e3:.0f}k cm³", 11.5, "middle", MUT))
    for xx in (300, 600):
        b.append(T(xx, 170, "→", 22, "middle", AX))
    return svg(900, 330, b, "RC-2011-5 淨、變換、合成三斷面形心與偏心距")


# ═════════════════ 圖 6a：偏心方向跟著彎矩圖（形狀精確）═════════════════
def fig6a():
    b = [defs(("a6", GREY))]
    b.append(L(450, 20, 450, 345, "#cfd8dc", 2, "6 5"))
    N = 60
    # 簡支梁
    b.append(T(225, 22, "簡支梁（均布載重）：底部受拉", 15, "middle", BLUE2, True))
    for i in range(9):
        xx = 55 + i * 42.5
        b.append(L(xx, 32, xx, 48, GREY, 1.2, marker="a6"))
    b.append(L(45, 32, 405, 32, GREY, 1.2))
    b.append(R(45, 52, 360, 66, "#f5f7f8", GREY, 1.6))
    yc = 85
    b.append(L(45, yc, 405, yc, "#90a4ae", 1.2, "6 4"))
    pts = [(45 + 360 * i / N, yc + 24 * 4 * (i / N) * (1 - i / N)) for i in range(N + 1)]
    b.append(P(pts, "none", RED, 2.6, close=False))
    b.append(T(225, 136, "c.g.s.：e(x) ∝ x(L−x)，跨中最大、支承處為 0", 12, "middle", RED, True))
    b.append(P([(45, 118), (36, 132), (54, 132)], GREY, GREY, 1))
    b.append(C(405, 125, 7, "none", GREY, 1.6))
    base = 168
    mpts = [(45 + 360 * i / N, base + 64 * 4 * (i / N) * (1 - i / N)) for i in range(N + 1)]
    b.append(P(mpts, "#bbdefb", BLUE, 1.8))
    b.append(L(45, base, 405, base, AX, 1.4))
    b.append(T(225, 210, "M(x) = w x(L−x)/2（畫在受拉側）", 12.5, "middle", BLUE2, True))
    b += [T(225, 270, "同一條拋物線：鋼腱形狀＝彎矩圖形狀", 13, "middle", AX),
          T(225, 292, "支承處 M = 0 → 偏心也應為 0", 13, "middle", AX),
          T(225, 316, "端部若仍有大偏心 → 傳遞階段頂纖維開裂", 12, "middle", ORG)]
    # 懸臂梁
    b.append(T(675, 22, "懸臂梁（均布載重）：頂部受拉", 15, "middle", BLUE2, True))
    for i in range(9):
        xx = 505 + i * 42.5
        b.append(L(xx, 32, xx, 48, GREY, 1.2, marker="a6"))
    b.append(L(495, 32, 855, 32, GREY, 1.2))
    b.append(R(495, 52, 360, 66, "#f5f7f8", GREY, 1.6))
    b.append(R(483, 40, 12, 90, "#78909c", "#546e7a", 1))
    b.append(L(495, yc, 855, yc, "#90a4ae", 1.2, "6 4"))
    pts = [(495 + 360 * i / N, yc - 24 * (1 - i / N) ** 2) for i in range(N + 1)]
    b.append(P(pts, "none", RED, 2.6, close=False))
    b.append(L(495, yc - 24, 855, yc - 24, PUR, 1.6, "6 3"))
    b.append(T(850, yc - 10, "全長固定偏心（RC-2012-1）", 11, "end", PUR, True))
    b.append(T(675, 136, "c.g.s.：e(x) ∝ (L−x)²，固定端最大、自由端為 0", 12, "middle", RED, True))
    base = 232
    mpts = [(495 + 360 * i / N, base - 64 * (1 - i / N) ** 2) for i in range(N + 1)]
    b.append(P(mpts + [(855, base), (495, base)], RED2, RED, 1.8))
    b.append(L(495, base, 855, base, AX, 1.4))
    b.append(T(700, 190, "M(x) = −w(L−x)²/2（畫在受拉側）", 12.5, "middle", RED, True))
    b.append(T(860, 250, "自由端 M=0、斜率也為 0", 11, "end", MUT))
    b += [T(675, 270, "最大彎矩在固定端 → 偏心在固定端最大", 13, "middle", AX),
          T(675, 292, "若全長固定偏心（紫虛線）：自由端沒有 M 抵銷", 13, "middle", AX),
          T(675, 316, "→ 自由端底緣拉應力最大，才是控制斷面", 12, "middle", ORG)]
    return svg(900, 330, b, "簡支梁與懸臂梁的偏心方向與彎矩圖")


# ═════════════════ 圖 7：M–φ 三門檻（RC-2004-5 實算）═════════════════
def fig7():
    A, I, Sb, e, dp = 3600.0, 2_430_000.0, 54_000.0, 35.0, 80.0
    Pe = 6.16 * 9900
    fcp = 350.0
    Ec = 15000 * math.sqrt(fcp)
    EI = Ec * I
    fr = 2.0 * math.sqrt(fcp)
    Mbal = Pe * e
    Mdec = Pe * (Sb / A + e)
    Mcr = Mdec + fr * Sb
    Mn, phiMn = 73.67e5, 66.30e5
    cdep = 10.19
    phiu = 0.003 / cdep
    assert abs(Mcr / 1e5 - 50.7) < 0.1
    phi = lambda M: (M - Mbal) / EI
    b = [defs(("a7", AX))]
    # 座標：M 軸
    Y0, sy = 350, 3.8
    Y = lambda m: Y0 - m / 1e5 * sy
    # φ 軸：A 段線性 −4e-6~8e-6 → 150~510；B 段 8e-6~3.2e-4 → 540~860（線性）
    def X(p):
        if p <= 8e-6:
            return 150 + (p + 4e-6) / 12e-6 * 360
        return 540 + (p - 8e-6) / (3.2e-4 - 8e-6) * 320
    b.append(L(150, Y0, 515, Y0, AX, 1.8))
    b.append(L(535, Y0, 868, Y0, AX, 1.8, marker="a7"))
    for xx in (515, 535):
        b.append(L(xx - 4, Y0 + 7, xx + 4, Y0 - 7, AX, 1.6))
    b.append(L(150, Y0, 150, 30, AX, 1.8, marker="a7"))
    b.append(T(868, Y0 + 36, "曲率 φ（1/cm）", 12.5, "end", AX))
    b.append(T(144, 26, "彎矩 M（tf·m）", 12.5, "end", AX))
    for p, lab in ((-2e-6, "−2"), (0, "0"), (2e-6, "2"), (4e-6, "4"), (6e-6, "6")):
        b.append(L(X(p), Y0, X(p), Y0 + 6, AX, 1.2))
        b.append(T(X(p), Y0 + 20, lab, 11, "middle", AX))
    b.append(T(X(1e-6), Y0 + 36, "×10⁻⁶（未開裂段，實比例）", 11, "middle", MUT))
    for p, lab in ((1e-4, "1×10⁻⁴"), (2e-4, "2×10⁻⁴"), (3e-4, "3×10⁻⁴")):
        b.append(L(X(p), Y0, X(p), Y0 + 6, AX, 1.2))
        b.append(T(X(p), Y0 + 20, lab, 11, "middle", AX))
    b.append(L(X(0), Y0, X(0), 40, "#b0bec5", 1, "3 3"))
    b.append(T(X(0) + 4, 50, "φ = 0", 11, "start", MUT))
    # 水平參考線
    refs = [(Mn, f"Mn = {Mn/1e5:.1f}", GRN), (phiMn, f"φMn = {phiMn/1e5:.1f}", GRN),
            (1.2 * Mcr, f"1.2Mcr = {1.2*Mcr/1e5:.1f}", ORG), (Mcr, f"Mcr = {Mcr/1e5:.1f}", RED),
            (Mdec, f"Mdec = {Mdec/1e5:.1f}", BLUE), (Mbal, f"Pe·e = {Mbal/1e5:.1f}", MUT)]
    for m, lab, colr in refs:
        b.append(L(150, Y(m), 860, Y(m), colr, 1.1, "5 4" if colr != ORG else "3 3", op=0.85))
        b.append(T(144, Y(m) + 4, lab, 11.5, "end", colr, True))
    # 未開裂直線（實算）
    b.append(L(X(phi(0)), Y0, X(phi(Mcr)), Y(Mcr), BLUE, 3))
    # 開裂後（端點實算，中段示意）
    # 開裂後：端點實算，中間以顯示座標下的平滑凹曲線示意
    xa_, xb_ = X(phi(Mcr)), X(phiu)
    seg = []
    for j in range(81):
        t = j / 80
        seg.append((xa_ + (xb_ - xa_) * t, Y(Mcr + (Mn - Mcr) * (1 - (1 - t) ** 2.6))))
    b.append(P(seg, "none", RED, 3, close=False))
    b.append(L(X(phiu), Y(Mn), X(phiu), Y0, GRN, 1, "2 3"))
    b.append(T(X(phiu), Y0 - 8, f"φu = 0.003/c = 0.003/{cdep}", 11, "end", GRN))
    for p, m, colr in ((phi(0), 0, BLUE), (0, Mbal, MUT), (phi(Mdec), Mdec, BLUE),
                       (phi(Mcr), Mcr, RED), (phiu, Mn, GRN)):
        b.append(C(X(p), Y(m), 5.5, colr))
    b.append(T(X(phi(0)) + 24, Y0 - 8, "M = 0：預力造成反拱（負曲率）", 11, "start", BLUE))
    b.append(T(X(0) + 10, Y(Mbal) + 16, "M = Pe·e：全斷面均勻受壓、曲率歸零", 11, "start", MUT))
    b.append(T(X(phi(Mdec)) + 12, Y(Mdec) + 16, "① 去壓：底緣應力 = 0", 12, "start", BLUE, True))
    b.append(T(X(phi(Mcr)) - 10, Y(Mcr) - 10, "② 開裂：底緣 = −fr", 12, "end", RED, True))
    b.append(T(X(phiu) - 6, Y(Mn) - 10, "③ 極限：混凝土壓碎 εcu = 0.003", 12, "end", GRN, True))
    b.append(T(560, Y(1.2 * Mcr) + 30, f"φMn / 1.2Mcr = {phiMn/(1.2*Mcr):.2f} → 餘裕僅 9%", 12, "start", ORG, True))
    b.append(T(560, Y(1.2 * Mcr) + 48, "開裂後曲線形狀為示意；所有水平線與端點皆為實算", 11, "start", MUT))
    b.append(T(300, 22, "RC-2004-5（40×90 矩形先拉梁）：Mdec、Mcr、Mn 依實算值定位", 13, "start", BLUE2, True))
    return svg(900, 400, b, "RC-2004-5 彎矩-曲率曲線三門檻")


# ═════════════════ 圖 8：腱應變增量分布（等面積）═════════════════
def fig8():
    b = []
    b.append(L(450, 20, 450, 330, "#cfd8dc", 2, "6 5"))
    N = 60
    for ox, kind in ((0, "b"), (450, "u")):
        cx = ox + 225
        x0, x1 = ox + 45, ox + 405
        b.append(T(cx, 24, "有黏結腱（bonded）" if kind == "b" else "無握裹腱（unbonded）", 15, "middle", BLUE2, True))
        b.append(R(x0, 46, 360, 56, "#f5f7f8", GREY, 1.6))
        b.append(L(x0, 88, x1, 88, RED, 2.6))
        if kind == "b":
            for i in range(8):
                xx = x0 + 30 + i * 43
                b.append(L(xx, 81, xx, 95, INK, 1.4))
            b.append(T(cx, 122, "每一點都被握裹住，不能滑動", 12, "middle", AX))
        else:
            b.append(L(x0, 82, x1, 82, "#90a4ae", 1, "4 3"))
            b.append(L(x0, 94, x1, 94, "#90a4ae", 1, "4 3"))
            b.append(R(x0 - 6, 78, 6, 20, "#78909c", "#546e7a", 1))
            b.append(R(x1, 78, 6, 20, "#78909c", "#546e7a", 1))
            b.append(T(cx, 122, "套管內自由滑動（僅兩端錨定）", 12, "middle", AX))
        base, peak = 230, 78
        par = [(x0 + 360 * i / N, base - peak * 4 * (i / N) * (1 - i / N)) for i in range(N + 1)]
        b.append(L(x0, base, x1, base, "#90a4ae", 1.2))
        b.append(T(x0 - 4, base - peak + 4, "Δε", 11.5, "end", MUT))
        if kind == "b":
            b.append(P(par + [(x1, base)], RED2, RED, 2.4, op=0.7))
            b.append(T(cx, base - peak - 8, "峰值 Δεmax（跨中）", 11.5, "middle", RED, True))
            b.append(T(cx, 252, "腱應變增量跟著彎矩：Δε(x) ∝ M(x)", 12.5, "middle", RED, True))
            b += [T(cx, 276, "跨中腱應變＝該斷面混凝土應變", 12.5, "middle", AX),
                  T(cx, 298, "→ 可用應變相容求 fps（或 ACI 近似式）", 12.5, "middle", AX),
                  T(cx, 322, "fps 高，常可達 0.9～0.95 fpu", 13, "middle", GRN, True)]
        else:
            avg = base - peak * 2 / 3
            b.append(P(par, "none", RED, 1.4, "5 4", close=False))
            b.append(P([(x0, base), (x0, avg), (x1, avg), (x1, base)], ORG2, ORG, 2.4))
            b.append(T(x1 - 4, base - peak - 4, "虛線＝同撓度的有黏結分布", 11, "end", RED))
            b.append(T(cx, avg + 20, "平均值 = 2/3 Δεmax", 12, "middle", ORG, True))
            b.append(T(cx, 252, "兩者面積相同（＝腱的總伸長量相同）", 12.5, "middle", ORG, True))
            b += [T(cx, 276, "應變 = 全長伸長量 ÷ 腱長，被攤平", 12.5, "middle", AX),
                  T(cx, 298, "→ 不能用斷面應變相容，只能用經驗式", 12.5, "middle", AX),
                  T(cx, 322, "fps 低，僅 fse 加上有限增量", 13, "middle", ORG, True)]
    return svg(900, 334, b, "有黏結與無握裹鋼腱應變增量分布對照")


FIGS = dict(fig0=fig0, fig1=fig1, fig2=fig2, fig4=fig4, fig6a=fig6a, fig6b=fig6b, fig7=fig7, fig8=fig8)
for name, fn in FIGS.items():
    s = fn()
    open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8").write(s)
    print("OK", name, len(s))
print("e-limits:", {k: round(v, 2) for k, v in E_LIMITS.items()})
print(f"RC-2014-4: S={S14:.0f}, r2={r2_14:.1f}, k={k14:.2f}, Md/Pi={Md/Pi14:.2f}, MT/Pe={MT/Pe14:.2f}")
