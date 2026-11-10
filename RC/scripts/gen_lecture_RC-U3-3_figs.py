# -*- coding: utf-8 -*-
"""
gen_lecture_RC-U3-3_figs.py
重繪 study/lecture-RC-U3-3.html 的 8 張向量圖解。
所有幾何由題目數值計算（RC-2025-2、RC-2022-4、RC-2013-2），可重跑、可審核。

用法（於 repo 根目錄）：python scripts/gen_lecture_RC-U3-3_figs.py <原始講義.html> study/lecture-RC-U3-3.html
注意：輸入須為「重繪前」版本（腳本依 .fig 順序整段替換 svg 與圖說，對已處理過的檔案重跑也安全，流程圖修正會自動跳過）。
腳本依 <div class="fig"> 出現順序（0~7）替換其中的 <svg> 與 .cap。
"""
import math, re, sys

C = dict(ink="#263238", mut="#607d8b", line="#455a64", grid="#cfd8dc", bd="#90a4ae",
         blue="#1565c0", blue2="#bbdefb", blue3="#e3f2fd", red="#c62828", red2="#ffcdd2",
         red3="#ffebee", green="#2e7d32", green2="#c8e6c9", orange="#ef6c00", orange2="#ffe0b2",
         purple="#6a1b9a", concrete="#eceff1", concrete2="#cfd8dc", steel="#37474f")


def f(x, n=1):
    return f"{x:.{n}f}"


class SVG:
    def __init__(self, w, h, pid):
        self.w, self.h, self.pid, self.o, self.used = w, h, pid, [], set()

    def add(self, s):
        self.o.append(s)

    def mk(self, color):
        key = color.lstrip("#")
        self.used.add(color)
        return f"url(#{self.pid}{key})"

    def line(self, x1, y1, x2, y2, color=C["line"], w=2, dash=None, arrow=False, arrow0=False, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="{self.mk(color)}"' if arrow else ""
        m0 = f' marker-start="{self.mk(color)}"' if arrow0 else ""
        self.add(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{color}" stroke-width="{w}"{d}{m}{m0}{extra}/>')

    def poly(self, pts, color=C["line"], w=2, fill="none", dash=None, close=False, arrow=False, op=None):
        p = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="{self.mk(color)}"' if arrow else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        self.add(f'<{tag} points="{p}" fill="{fill}"{o} stroke="{color}" stroke-width="{w}" stroke-linejoin="round"{d}{m}/>')

    def rect(self, x, y, w, h, fill=C["concrete"], stroke=C["line"], sw=1.8, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        self.add(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, x, y, r, fill=C["steel"], stroke="none", sw=1):
        self.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=12.5, color=C["ink"], anchor="middle", bold=False, italic=False):
        b = ' font-weight="700"' if bold else ""
        it = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" fill="{color}"{b}{it}>{s}</text>')

    def path(self, d, color=C["line"], w=2, fill="none", arrow=False, dash=None, op=None):
        m = f' marker-end="{self.mk(color)}"' if arrow else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        self.add(f'<path d="{d}" fill="{fill}"{o} stroke="{color}" stroke-width="{w}"{m}{da}/>')

    def moment(self, cx, cy, r, a0, a1, color, w=2.4):
        """彎矩弧形箭頭。角度採數學慣例（逆時針為正、y 向上）；a1>a0 → 逆時針。"""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 0 if a1 > a0 else 1
        self.path(f"M{f(x0)},{f(y0)} A{r},{r} 0 {large} {sweep} {f(x1)},{f(y1)}", color, w, arrow=True)

    def hinge(self, x, y, color, r=5.5):
        self.circle(x, y, r, fill="#fff", stroke=color, sw=2.6)

    def render(self):
        defs = "".join(
            f'<marker id="{self.pid}{c.lstrip("#")}" markerWidth="10" markerHeight="10" refX="8" refY="5" '
            f'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for c in sorted(self.used))
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg">\n'
                f'<defs>{defs}</defs>\n' + "\n".join(self.o) + "\n</svg>")


# ════════════════════════════════════════════════════════════════════
# 題目數值（全部由原題資料算出，不手打結果）
# ════════════════════════════════════════════════════════════════════
# RC-2025-2 耐震梁
ln, bw, h, dprime, wu, fc, fy = 9.0, 60.0, 76.0, 9.0, 2.0, 280.0, 4200.0
Ab32 = 8.14
d = h - dprime
As_top, As_bot = 8 * Ab32, 6 * Ab32


def Mcap(As, fs):
    a = As * fs / (0.85 * fc * bw)
    return As * fs * (d - a / 2) / 1e5, a  # tf·m


Mpr_neg, a_pr_top = Mcap(As_top, 1.25 * fy)
Mpr_pos, _ = Mcap(As_bot, 1.25 * fy)
Mn_neg, a_n_top = Mcap(As_top, fy)
c_n = a_n_top / 0.85
eps_t = 0.003 * (d - c_n) / c_n
phi_flex = 0.90 if eps_t >= 0.005 else None
phiMn_neg = phi_flex * Mn_neg
V_seis = (Mpr_neg + Mpr_pos) / ln
V_grav = wu * ln / 2
Ve_L, Ve_R = V_seis + V_grav, V_seis - V_grav

# RC-2022-4 韌性
lu, phi_y, My, phi_u, Mu, db, fy22 = 6.4, 0.005, 220.0, 0.020, 245.0, 0.0322, 4200.0
L = lu / 2
Lp = max(0.08 * L + 0.0022 * db * fy22, 0.0044 * db * fy22)
dy = phi_y * L ** 2 / 3
theta_p = (phi_u - phi_y) * Lp
du = Mu / My * dy + theta_p * (L - Lp / 2)
mu_phi, mu = phi_u / phi_y, du / dy

# RC-2013-2 柱圍束
B, cov, dh, dbl = 50.0, 4.0, 1.27, 3.22
bar_c = cov + dh + dbl / 2                      # 主筋心至柱面
bar_sp = (B - 2 * bar_c) / 4                    # 每面 5 根，4 個間距

print(f"[RC-2025-2] Mpr-={Mpr_neg:.2f} Mpr+={Mpr_pos:.2f} Mn-={Mn_neg:.2f} phiMn-={phiMn_neg:.2f} "
      f"eps_t={eps_t:.4f} Vseis={V_seis:.2f} VeL={Ve_L:.2f} VeR={Ve_R:.2f}")
print(f"[RC-2022-4] L={L} Lp={Lp:.4f} dy={dy:.5f} du={du:.5f} mu_phi={mu_phi:.2f} mu={mu:.3f}")
print(f"[RC-2013-2] bar_c={bar_c:.2f} bar_sp={bar_sp:.2f} span={B-2*bar_c:.2f}")


# ════════════════════════════════════════════════════════════════════
# 圖 0：層崩塌 vs 梁式機構（含變形形狀）
# ════════════════════════════════════════════════════════════════════
def fig0():
    s = SVG(900, 400, "g0")
    s.line(450, 18, 450, 385, C["grid"], 2, dash="6 5")
    ground, hs, bay = 318, 70, 140
    levels = [ground - i * hs for i in range(4)]

    def frame(x0, drift, color, hinges, title, sub, title_c):
        cx = x0 + bay
        s.text(cx, 26, title, 15, title_c, bold=True)
        s.text(cx, 46, sub, 12.5, C["mut"])
        s.line(x0 - 40, ground, x0 + 2 * bay + 40, ground, "#546e7a", 2.4)
        for i in range(9):
            xx = x0 - 30 + i * 37
            s.line(xx, ground, xx - 9, ground + 10, "#90a4ae", 1.4)
        cols = [x0 + j * bay for j in range(3)]
        # 原始位置（淡虛線）
        for x in cols:
            s.line(x, ground, x, levels[3], C["grid"], 1.6, dash="4 4")
        for y in levels[1:]:
            s.line(cols[0], y, cols[2], y, C["grid"], 1.6, dash="4 4")
        # 變形後
        for x in cols:
            s.poly([(x + drift[i], levels[i]) for i in range(4)], C["line"], 2.4)
        for i in range(1, 4):
            s.line(cols[0] + drift[i], levels[i], cols[2] + drift[i], levels[i], C["line"], 2.4)
        for hx, hy in hinges(cols):
            s.hinge(hx, hy, color)
        # 側力
        yT = levels[3] - 22
        s.line(cols[0] - 6, yT, cols[0] + 70, yT, color, 2.6, arrow=True)
        s.text(cols[0] + 76, yT + 4, "地震側力", 11.5, color, anchor="start")
        # 層間位移標註
        return cols

    # 左：軟層（只有一樓變形）
    D = 30
    drL = [0, D, D, D]

    def hingesL(cols):
        out = []
        for x in cols:
            t0, t1 = 9 / hs, 1 - 9 / hs
            out += [(x + D * t0, ground - hs * t0), (x + D * t1, ground - hs * t1)]
        return out

    colsL = frame(45, drL, C["red"], hingesL, "脆性先到：層崩塌機構", "柱端先出鉸（或柱剪力先破壞）", C["red"])
    xr = colsL[2] + D + 20
    s.line(xr, levels[1], xr, ground, C["red"], 1.2, dash="3 3")
    s.text(xr + 6, (levels[1] + ground) / 2 - 2, "整棟的側位移", 11, C["red"], anchor="start", bold=True)
    s.text(xr + 6, (levels[1] + ground) / 2 + 13, "全擠在一樓", 11, C["red"], anchor="start", bold=True)
    s.text(185, 348, "柱上下端各 1 鉸 × 3 柱 = <tspan font-weight=\"700\">6 個塑鉸</tspan> 即成機構", 12.5, C["line"])
    s.text(185, 370, "耗能少、無預警、整棟倒", 13, C["red"], bold=True)

    # 右：梁式機構（每層均勻層間位移）
    d1 = 12
    drR = [0, d1, 2 * d1, 3 * d1]
    off = 15

    def hingesR(cols):
        out = []
        for i in (1, 2, 3):
            y = levels[i]
            for j in range(2):
                xa, xb = cols[j] + drR[i], cols[j + 1] + drR[i]
                out += [(xa + off, y), (xb - off, y)]
        for x in cols:
            t = 9 / hs
            out.append((x + d1 * t, ground - hs * t))
        return out

    colsR = frame(520, drR, C["green"], hingesR, "延性先到：梁式機構", "梁端先出鉸，柱保持彈性（柱底除外）", C["green"])
    s.text(660, 348, "梁端 12 鉸 + 柱底 3 鉸 = <tspan font-weight=\"700\">15 個塑鉸</tspan> 才成機構", 12.5, C["line"])
    s.text(660, 370, "耗能多、變形分散到每一層、不易倒", 13, C["green"], bold=True)
    # 圖例
    s.hinge(400, 88, C["line"], 5)
    s.text(410, 92, "塑鉸", 11, C["mut"], anchor="start")
    s.line(380, 106, 404, 106, C["grid"], 1.6, dash="4 4")
    s.text(410, 110, "原位置", 11, C["mut"], anchor="start")
    cap = ("兩張圖是同一棟建築的兩種命運，差別只在「哪裡先出鉸」（變形已放大示意）。"
           "左圖側位移全集中在一樓，6 個鉸就成機構；右圖每層都分擔變形，要 15 個鉸 —— 這就是「強柱弱梁」值得用 6/5 去買的東西（§5）。"
           "注意右圖<b>柱底仍然出鉸</b>：強柱弱梁救不了柱底，所以柱底一定要有密箍（§4）。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 1：φMn / Mn / Mpr（RC-2025-2 頂筋實際數值，比例尺正確）
# ════════════════════════════════════════════════════════════════════
def fig1():
    s = SVG(900, 330, "g1")
    x0, sc = 250, 2.25  # px per tf·m
    s.text(40, 34, f"RC-2025-2 柱面負彎矩斷面（頂筋 8-D32，b = {bw:.0f}、d = {d:.0f} cm）的三個「彎矩強度」：", 13, C["line"], anchor="start")
    rows = [
        ("設計時承諾的 φM<tspan baseline-shift=\"sub\" font-size=\"9\">n</tspan>", phiMn_neg, C["blue2"], C["blue"],
         f"φ = 0.90（ε<tspan baseline-shift=\"sub\" font-size=\"9\">t</tspan> = {eps_t:.4f} ≥ 0.005）、f<tspan baseline-shift=\"sub\" font-size=\"9\">y</tspan>"),
        ("標稱彎矩強度 M<tspan baseline-shift=\"sub\" font-size=\"9\">n</tspan>", Mn_neg, C["concrete"], C["line"],
         f"φ = 1.0、f<tspan baseline-shift=\"sub\" font-size=\"9\">y</tspan>，a = {a_n_top:.2f} cm"),
        ("地震時可能發揮的 M<tspan baseline-shift=\"sub\" font-size=\"9\">pr</tspan>", Mpr_neg, C["red2"], C["red"],
         f"φ = 1.0、1.25f<tspan baseline-shift=\"sub\" font-size=\"9\">y</tspan>，a = {a_pr_top:.2f} cm"),
    ]
    ys = [62, 122, 182]
    for (lab, val, fill, stc, note), y in zip(rows, ys):
        s.text(x0 - 12, y + 26, lab, 13, stc, anchor="end", bold=True)
        s.rect(x0, y, val * sc, 38, fill, stc, 1.8)
        s.text(x0 + val * sc + 10, y + 18, f"{val:.1f} tf·m", 13.5, stc, anchor="start", bold=True)
        s.text(x0 + val * sc + 10, y + 34, note, 11, C["mut"], anchor="start")
    s.line(x0, 50, x0, 232, C["mut"], 1.4)
    # 刻度
    for v in range(0, 201, 50):
        X = x0 + v * sc
        s.line(X, 232, X, 238, C["mut"], 1.2)
        s.text(X, 252, str(v), 10.5, C["mut"])
    s.text(x0 + 200 * sc + 18, 252, "tf·m", 10.5, C["mut"], anchor="start")
    # 比值帶
    xa, xb = x0 + phiMn_neg * sc, x0 + Mpr_neg * sc
    s.line(xa, 100, xa, 270, C["blue"], 1.2, dash="4 3")
    s.line(xb, 220, xb, 270, C["red"], 1.2, dash="4 3")
    s.line(xa + 2, 268, xb - 2, 268, C["orange"], 2, arrow=True, arrow0=True)
    s.text((xa + xb) / 2, 290, f"M<tspan baseline-shift=\"sub\" font-size=\"9\">pr</tspan> / φM<tspan baseline-shift=\"sub\" font-size=\"9\">n</tspan> = {Mpr_neg/phiMn_neg:.2f}", 13.5, C["orange"], bold=True)
    s.text((xa + xb) / 2, 308, f"M<tspan baseline-shift=\"sub\" font-size=\"9\">pr</tspan> / M<tspan baseline-shift=\"sub\" font-size=\"9\">n</tspan> = {Mpr_neg/Mn_neg:.2f}（不是 1.25）", 11.5, C["mut"])
    cap = (f"\\(\\phi M_n\\) 是「我保證至少有這麼強」（下限）；\\(M_{{pr}}\\) 是「它最多可能有這麼強」（上限）。"
           f"剪力設計要問的是「塑鉸能把多大的力送進來」—— 那是<b>上限</b>問題，所以必須用 \\(M_{{pr}}\\)，而且不能再折減。"
           f"本例若拿 \\(\\phi M_n={phiMn_neg:.1f}\\) 去推剪力，地震項只有真實值的 {phiMn_neg/Mpr_neg*100:.0f}%。"
           f"另注意 \\(M_{{pr}}/M_n={Mpr_neg/Mn_neg:.2f}\\) 而非 1.25：鋼筋力放大 1.25 倍時壓力區深度 \\(a\\) 也跟著變大（{a_n_top:.1f} → {a_pr_top:.1f} cm），力臂變短。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 2：韌性三層次（RC-2022-4，M-φ 與曲率分佈皆依比例）
# ════════════════════════════════════════════════════════════════════
def fig2():
    s = SVG(900, 420, "g2")
    s.line(392, 20, 392, 400, C["grid"], 2, dash="6 5")
    # ── 左：M-φ ──
    s.text(205, 28, "斷面層次：雙線性 M-φ（RC-2022-4 內插後）", 14, C["blue"], bold=True)
    ox, oy, sx, sy = 70, 330, 14000, 0.95   # px/(1/m), px/(tf·m)
    s.line(ox, oy, ox + 0.022 * sx + 10, oy, C["line"], 1.8, arrow=True)
    s.line(ox, oy, ox, oy - 270 * sy, C["line"], 1.8, arrow=True)
    s.text(ox + 0.022 * sx + 8, oy - 8, "φ (1/m)", 11.5, C["mut"], anchor="end")
    s.text(ox - 8, oy - 270 * sy + 4, "M (tf·m)", 11.5, C["mut"], anchor="end")
    for v in (0.005, 0.010, 0.015, 0.020):
        X = ox + v * sx
        s.line(X, oy, X, oy + 5, C["mut"], 1.2)
        s.text(X, oy + 18, f"{v:.3f}", 10, C["mut"])
    for v in (100, 200):
        Y = oy - v * sy
        s.line(ox - 5, Y, ox, Y, C["mut"], 1.2)
        s.text(ox - 8, Y + 4, str(v), 10, C["mut"], anchor="end")
    P1 = (ox + phi_y * sx, oy - My * sy)
    P2 = (ox + phi_u * sx, oy - Mu * sy)
    s.line(ox, P1[1], P1[0], P1[1], C["blue"], 1, dash="4 3")
    s.line(ox, P2[1], P2[0], P2[1], C["red"], 1, dash="4 3")
    s.line(P1[0], P1[1], P1[0], oy, C["blue"], 1, dash="4 3")
    s.line(P2[0], P2[1], P2[0], oy, C["red"], 1, dash="4 3")
    s.poly([(ox, oy), P1, P2], C["blue"], 3)
    s.circle(*P1, 5, C["blue"]); s.circle(*P2, 5, C["red"])
    s.text(P1[0] + 8, P1[1] + 18, f"(φy, My) = ({phi_y}, {My:.0f})", 11, C["blue"], anchor="start", bold=True)
    s.text(P2[0] + 2, P2[1] - 12, f"(φu, Mu) = ({phi_u}, {Mu:.0f})", 11, C["red"], anchor="end", bold=True)
    s.text((P1[0] + P2[0]) / 2 + 10, P1[1] + 70, "降伏後強度只增 11%，曲率卻增 4 倍", 11, C["mut"])
    # μφ bracket
    yb = oy + 36
    s.line(ox, yb, P1[0], yb, C["blue"], 1.6, arrow=True, arrow0=True)
    s.line(ox, yb + 14, P2[0], yb + 14, C["red"], 1.6, arrow=True, arrow0=True)
    s.text(ox + 0.021 * sx, yb + 18, f"μφ = φu/φy = {mu_phi:.1f}", 12.5, C["blue"], anchor="start", bold=True)
    # ── 右：構件層次 ──
    s.text(650, 28, f"構件層次：塑性曲率只在 Lp 內（L = {L} m 依比例）", 14, C["blue"], bold=True)
    base, top = 352, 118
    pxm = (base - top) / L
    cx0, cw = 520, 34
    # 柱（未變形）
    s.rect(cx0, top, cw, base - top, C["concrete"], C["line"], 1.6)
    yLp = base - Lp * pxm
    s.rect(cx0, yLp, cw, base - yLp, C["orange2"], C["orange"], 1.6)
    s.line(cx0 - 40, base, cx0 + cw + 40, base, "#546e7a", 2.4)
    for i in range(6):
        xx = cx0 - 34 + i * 20
        s.line(xx, base, xx - 8, base + 9, "#90a4ae", 1.3)
    s.text(cx0 + cw / 2, top - 8, "反曲點", 11, C["mut"])
    # L 尺寸
    s.line(cx0 - 22, top, cx0 - 22, base, C["mut"], 1.2, arrow=True, arrow0=True)
    s.text(cx0 - 28, (top + base) / 2, f"L = {L} m", 11.5, C["mut"], anchor="end")
    s.text(cx0 - 28, (top + base) / 2 + 16, "(= lu/2)", 10.5, C["mut"], anchor="end")
    s.text(cx0 - 28, yLp + (base - yLp) / 2 + 4, f"Lp = {Lp:.3f} m", 11.5, C["orange"], anchor="end", bold=True)
    s.line(cx0 - 22, yLp, cx0 - 4, yLp, C["orange"], 1, dash="3 2")
    # 撓度形狀（放大）：彈性 φ(z)=φ0(1-z/L) 積分 + θp 集中於 Lp/2
    amp = 62 / du
    def yel(z, phi0):
        return phi0 * (z ** 2 / 2 - z ** 3 / (6 * L))
    xc = cx0 + cw / 2
    ptsY, ptsU = [], []
    for k in range(41):
        z = L * k / 40
        ptsY.append((xc + amp * yel(z, phi_y), base - z * pxm))
        yu = yel(z, phi_y * Mu / My) + (theta_p * (z - Lp / 2) if z > Lp / 2 else 0)
        ptsU.append((xc + amp * yu, base - z * pxm))
    s.poly(ptsY, C["blue"], 2, dash="5 4")
    s.poly(ptsU, C["red"], 2.6)
    s.line(xc, top - 22, xc + amp * dy, top - 22, C["blue"], 1.6, arrow=True)
    s.line(xc, top - 40, xc + amp * du, top - 40, C["red"], 1.8, arrow=True)
    s.text(xc + amp * dy + 6, top - 18, f"δy = {dy*100:.2f} cm", 11, C["blue"], anchor="start", bold=True)
    s.text(xc + amp * du + 6, top - 36, f"δu = {du*100:.2f} cm", 11, C["red"], anchor="start", bold=True)
    # 曲率分佈圖
    gx = 680
    s.text(gx + 60, top + 8, "極限狀態的曲率分佈", 11.5, C["line"], bold=True)
    psc = 2200 * 2.2  # px per 1/m
    s.line(gx, top + 20, gx, base, C["line"], 1.4)
    s.line(gx, base, gx + phi_u * psc + 20, base, C["line"], 1.4)
    # 彈性三角形（基部 φy·Mu/My）
    pe = phi_y * Mu / My
    s.poly([(gx, top + 20), (gx + pe * psc, base), (gx, base)], C["blue"], 1.6, fill=C["blue2"], close=True, op=0.8)
    s.rect(gx + pe * psc, yLp, (phi_u - pe) * psc, base - yLp, C["orange2"], C["orange"], 1.6)
    s.text(gx + pe * psc / 2 + 4, base - 70, "彈性", 11, C["blue"], bold=True)
    s.text(gx + pe * psc + (phi_u - pe) * psc / 2, yLp - 8, "塑性 φu − φy", 11, C["orange"], bold=True)
    s.text(gx + pe * psc, base + 16, "≈φy", 10.5, C["blue"])
    s.text(gx + phi_u * psc, base + 16, "φu", 10.5, C["red"])
    s.text(gx - 10, base + 36, f"θp = (φu−φy)·Lp = {theta_p:.5f} rad", 11.5, C["orange"], anchor="start", bold=True)
    s.text(gx - 10, base + 54, f"μ = δu/δy = {mu:.2f}  ≪  μφ = {mu_phi:.1f}", 12, C["blue"], anchor="start", bold=True)
    cap = (f"左圖依 RC-2022-4 內插值按比例繪出：\\(\\mu_\\phi={mu_phi:.1f}\\) 是<b>斷面</b>能提供的曲率放大倍數。"
           f"右圖把同一根柱的曲率分佈也按比例畫出：橘色塑性區只占柱長 {Lp:.3f}/{L} ≈ {Lp/L*100:.0f}%，其餘部分仍是彈性的，"
           f"所以頂點位移只放大 \\(\\mu={mu:.2f}\\) 倍（撓度已放大示意，但 \\(\\delta_u/\\delta_y\\) 比例正確）。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 3：耐震梁自由體 + 剪力圖 + 彎矩圖（RC-2025-2）
# ════════════════════════════════════════════════════════════════════
def fig3():
    s = SVG(900, 640, "g3")
    xL, xR = 160, 740
    sx = (xR - xL) / ln
    yb, hb = 120, 40
    s.text(450, 26, "梁自由體：側移向左（←），兩端塑鉸同時發展", 14.5, C["blue"], bold=True)
    s.line(520, 46, 400, 46, C["red"], 2.8, arrow=True)
    s.text(530, 51, "地震側移", 12, C["red"], anchor="start", bold=True)
    # 柱與梁
    s.rect(xL - 40, yb - 34, 40, hb + 68, C["concrete2"], C["line"], 1.8)
    s.rect(xR, yb - 34, 40, hb + 68, C["concrete2"], C["line"], 1.8)
    s.rect(xL, yb, xR - xL, hb, C["concrete"], C["line"], 1.8)
    # 均佈載重
    for i in range(11):
        X = xL + 15 + i * (xR - xL - 30) / 10
        s.line(X, yb - 34, X, yb - 3, C["line"], 1.6, arrow=True)
    s.line(xL + 15, yb - 34, xR - 15, yb - 34, C["line"], 1.4)
    s.text(xR - 15, yb - 42, f"wu = {wu:.0f} tf/m", 12, C["line"], anchor="end", bold=True)
    # 塑鉸
    s.hinge(xL + 14, yb + hb / 2, C["green"], 6)
    s.hinge(xR - 14, yb + hb / 2, C["green"], 6)
    # 端彎矩（作用於梁上，均為逆時針）
    s.moment(xL + 2, yb + hb / 2, 34, -70, 70, C["red"])
    s.moment(xR - 2, yb + hb / 2, 34, 110, 250, C["red"])
    # 受拉側標示
    s.line(xL + 4, yb + 5, xL + 70, yb + 5, C["red"], 3)
    s.line(xR - 70, yb + hb - 5, xR - 4, yb + hb - 5, C["red"], 3)
    s.text(xL + 46, yb + hb + 56, f"Mpr⁻ = {Mpr_neg:.1f} tf·m（頂筋受拉，逆時針）", 12, C["red"], anchor="start", bold=True)
    s.text(xR - 46, yb + hb + 56, f"Mpr⁺ = {Mpr_pos:.1f} tf·m（底筋受拉，逆時針）", 12, C["red"], anchor="end", bold=True)
    # 端剪力（柱給梁的力）
    s.line(xL + 6, yb + hb + 46, xL + 6, yb + hb + 2, C["blue"], 2.6, arrow=True)
    s.text(xL - 46, yb + hb + 64, f"{Ve_L:.2f} tf ↑", 12, C["blue"], anchor="start", bold=True)
    s.line(xR - 6, yb + hb + 2, xR - 6, yb + hb + 46, C["blue"], 2.6, arrow=True)
    s.text(xR + 46, yb + hb + 64, f"{Ve_R:.2f} tf ↓", 12, C["blue"], anchor="end", bold=True)
    # ln
    yl = 238
    s.line(xL, yl, xR, yl, C["mut"], 1.2, arrow=True, arrow0=True)
    s.text(450, yl - 6, f"ln = {ln:.0f} m（柱面到柱面）", 11.5, C["mut"])
    # 剪力圖
    y0v, sv = 362, 1.25
    s.text(450, 274, "剪力圖 V(x)（單位 tf，依比例）", 13, C["blue"], bold=True)
    s.line(xL, y0v, xR, y0v, C["line"], 1.4)
    s.poly([(xL, y0v), (xL, y0v - Ve_L * sv), (xR, y0v - Ve_R * sv), (xR, y0v)], C["blue"], 2, fill=C["blue2"], close=True, op=0.7)
    s.line(xL, y0v - V_seis * sv, xR, y0v - V_seis * sv, C["orange"], 1.6, dash="6 4")
    s.text(xL - 6, y0v - Ve_L * sv + 4, f"{Ve_L:.2f}", 13, C["blue"], anchor="end", bold=True)
    s.text(xR + 6, y0v - Ve_R * sv + 4, f"{Ve_R:.2f}", 13, C["blue"], anchor="start", bold=True)
    s.text(450, y0v - V_seis * sv + 20, f"地震項 (Mpr⁻+Mpr⁺)/ln = {V_seis:.2f}（全跨定值）", 11.5, C["orange"], bold=True)
    s.text(450, y0v + 18, f"重力項 ±wu·ln/2 = ±{V_grav:.2f}（線性）→ 左端兩項同號 = 控制端", 11.5, C["mut"])
    # 彎矩圖（正彎矩向下畫，即畫在受拉側）
    y0m, sm = 510, 0.38
    s.text(450, 412, "彎矩圖 M(x)（tf·m，畫在受拉側；依比例）", 13, C["blue"], bold=True)
    s.line(xL, y0m, xR, y0m, C["line"], 1.4)
    pts = []
    for k in range(61):
        x = ln * k / 60
        M = -Mpr_neg + Ve_L * x - wu * x ** 2 / 2
        pts.append((xL + x * sx, y0m + M * sm))
    s.poly([(xL, y0m)] + pts + [(xR, y0m)], C["purple"], 2.2, fill="#e1bee7", close=True, op=0.6)
    s.line(xL, y0m - Mpr_neg * sm, xR, y0m + Mpr_pos * sm, C["orange"], 1.6, dash="6 4")
    x0 = (Ve_L - math.sqrt(Ve_L ** 2 - 2 * wu * Mpr_neg)) / wu
    s.circle(xL + x0 * sx, y0m, 3.5, C["purple"])
    s.text(xL + x0 * sx + 6, y0m - 8, f"M = 0 @ x = {x0:.2f} m", 11, C["purple"], anchor="start")
    s.text(xL - 6, y0m - Mpr_neg * sm + 4, f"−{Mpr_neg:.1f}", 12.5, C["purple"], anchor="end", bold=True)
    s.text(xR + 6, y0m + Mpr_pos * sm + 4, f"+{Mpr_pos:.1f}", 12.5, C["purple"], anchor="start", bold=True)
    s.text(xL + 40, y0m - Mpr_neg * sm + 6, "頂受拉", 11, C["mut"], anchor="start")
    s.text(xR - 40, y0m + Mpr_pos * sm - 2, "底受拉", 11, C["mut"], anchor="end")
    s.text(450, 624, "橘虛線 = 只有地震項（直線 → 斜率定值）；紫色 = 加上重力（拋物線 → 斜率線性變化）", 11.5, C["mut"])
    cap = (f"側移向左時，兩端塑鉸彎矩作用在梁上<b>同為逆時針</b>：左端頂筋受拉（\\(M_{{pr}}^-\\)）、右端底筋受拉（\\(M_{{pr}}^+\\)）。"
           f"地震項 \\(\\left(M_{{pr}}^-+M_{{pr}}^+\\right)/l_n\\) 是彎矩圖橘色直線的斜率 → 全跨定值；重力項 \\(\\pm w_u l_n/2\\) 是拋物線的斜率 → 線性。"
           f"兩者<b>同號的那一端</b>（本圖為左端，{Ve_L:.2f} tf）就是控制端（這就是公式裡 \\(\\pm\\) 的意思）；側移反向時右端改為頂筋受拉，控制端也跟著換邊，數值相同。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 4：柱圍束（RC-2013-2，50×50 依比例）
# ════════════════════════════════════════════════════════════════════
def fig4():
    s = SVG(900, 420, "g4")
    s.line(450, 18, 450, 400, C["grid"], 2, dash="6 5")
    sc = 5.2  # px/cm

    def section(X0, Y0, ties, title, title_c):
        s.text(X0 + B * sc / 2, 28, title, 14.5, title_c, bold=True)
        s.rect(X0, Y0, B * sc, B * sc, "#f5f7f8", C["bd"], 1.6)
        hc = cov + dh / 2
        # 主筋位置
        pos = [bar_c + i * bar_sp for i in range(5)]
        bars = [(x, y) for x in pos for y in pos if x in (pos[0], pos[-1]) or y in (pos[0], pos[-1])]
        P = lambda u, v: (X0 + u * sc, Y0 + v * sc)
        color = C["red"] if not ties else C["green"]
        # 受撐主筋
        sup = [(pos[0], pos[0]), (pos[0], pos[-1]), (pos[-1], pos[0]), (pos[-1], pos[-1])]
        if ties:
            sup = bars
        # 失效區（拱）
        def arch(p, q, inward):
            (u1, v1), (u2, v2) = p, q
            span = math.hypot(u2 - u1, v2 - v1)
            rise = span / 4
            mx, my = (u1 + u2) / 2 + inward[0] * rise * 2, (v1 + v2) / 2 + inward[1] * rise * 2
            a, b, c2 = P(u1, v1), P(mx, my), P(u2, v2)
            return a, b, c2
        sides = [((0, 1), lambda t: (t, pos[0])), ((0, -1), lambda t: (t, pos[-1])),
                 ((1, 0), lambda t: (pos[0], t)), ((-1, 0), lambda t: (pos[-1], t))]
        for inward, g in sides:
            pts_side = sorted({p for p in sup if (g(0)[1] == p[1] if inward[1] else g(0)[0] == p[0])})
            for p, q in zip(pts_side, pts_side[1:]):
                a, b, c2 = arch(p, q, inward)
                d_ = f"M{f(a[0])},{f(a[1])} Q{f(b[0])},{f(b[1])} {f(c2[0])},{f(c2[1])} Z"
                s.path(d_, color, 1.4, fill=C["red2"] if not ties else C["green2"], dash="4 3", op=0.75)
        # 外箍（中心線）
        s.rect(X0 + hc * sc, Y0 + hc * sc, (B - 2 * hc) * sc, (B - 2 * hc) * sc, "none", color, 3.2, rx=6)
        # 135° 彎鉤（外箍角部）
        hx_, hy_ = P(hc, hc)
        s.line(hx_ + 4, hy_ + 2, hx_ + 20, hy_ + 18, color, 2.6)
        s.line(hx_ + 2, hy_ + 4, hx_ + 18, hy_ + 20, color, 2.6)
        # 繫筋
        if ties:
            for i, u in enumerate(pos[1:4]):
                # 垂直繫筋（勾住上下主筋），兩端 135° / 90° 交替
                xa, ya = P(u, pos[0] - dbl / 2 - dh / 2)
                xb, yb = P(u, pos[-1] + dbl / 2 + dh / 2)
                s.line(xa, ya, xb, yb, color, 2.4)
                if i % 2 == 0:
                    s.line(xa, ya, xa + 12, ya + 12, color, 2.4)   # 135°
                    s.line(xb, yb, xb + 14, yb, color, 2.4)        # 90°
                else:
                    s.line(xa, ya, xa + 14, ya, color, 2.4)
                    s.line(xb, yb, xb + 12, yb - 12, color, 2.4)
                # 水平繫筋
                xa, ya = P(pos[0] - dbl / 2 - dh / 2, u)
                xb, yb = P(pos[-1] + dbl / 2 + dh / 2, u)
                s.line(xa, ya, xb, yb, color, 2.4)
                if i % 2 == 1:
                    s.line(xa, ya, xa + 12, ya - 12, color, 2.4)
                    s.line(xb, yb, xb, yb + 14, color, 2.4)
                else:
                    s.line(xa, ya, xa, ya + 14, color, 2.4)
                    s.line(xb, yb, xb - 12, yb - 12, color, 2.4)
        for (u, v) in bars:
            x, y = P(u, v)
            supported = (u, v) in sup
            s.circle(x, y, dbl / 2 * sc, C["steel"] if supported else "#fff", stroke=C["steel"], sw=2.2)
        # 切面 a-a（數 Ash 腳數）
        ycut = Y0 + (pos[1] + pos[2]) / 2 * sc
        s.line(X0 - 14, ycut, X0 + B * sc + 14, ycut, C["orange"], 1.4, dash="7 3")
        s.text(X0 - 18, ycut + 4, "a", 12, C["orange"], anchor="end", bold=True)
        s.text(X0 + B * sc + 18, ycut + 4, "a", 12, C["orange"], anchor="start", bold=True)
        legs = [hc, B - hc] + ([] if not ties else pos[1:4])
        for u in legs:
            x = X0 + u * sc
            s.circle(x, ycut, 4.2, C["orange"])
        return P, pos

    Y0 = 52
    X1, X2 = 95, 545
    P1, pos = section(X1, Y0, False, "只有外箍：只有 4 根角筋被撐住", C["red"])
    P2, _ = section(X2, Y0, True, "外箍 + 每向 3 道繫筋：每根主筋都被撐住", C["green"])
    yt = Y0 + B * sc + 26
    # 左註
    s.text(X1 + B * sc / 2, yt, f"拱跨 = 角筋間距 ≈ {pos[-1]-pos[0]:.1f} cm → 拱高 ≈ 跨距/4", 12, C["red"], bold=True)
    s.text(X1 + B * sc / 2, yt + 20, "白色主筋無側向支撐 → 易挫屈；且違反構造規定", 11.5, C["line"])
    s.text(X1 + B * sc / 2, yt + 40, "切面 a–a 只穿過 <tspan font-weight=\"700\" fill=\"#ef6c00\">2 腳</tspan>", 12, C["line"])
    # 右註
    s.text(X2 + B * sc / 2, yt, f"拱跨 = 相鄰主筋間距 ≈ {bar_sp:.1f} cm → 失效區大幅縮小", 12, C["green"], bold=True)
    s.text(X2 + B * sc / 2, yt + 20, "hx 變小 → so 放寬；繫筋兩端 135°／90° 鉤交替", 11.5, C["line"])
    s.text(X2 + B * sc / 2, yt + 40, "切面 a–a 穿過 <tspan font-weight=\"700\" fill=\"#ef6c00\">2 + 3 = 5 腳</tspan>（RC-2013-2）", 12, C["line"])
    cap = ("50×50 cm、16-D32、保護層 4 cm 依比例繪製；淡色區＝外拱以外、圍束到不了的混凝土（拱高取跨距 1/4 示意）。"
           "繫筋一個動作帶來三個好處：①增加 \\(A_{sh}\\) 的腳數（切面 a–a 從 2 腳變 5 腳）、"
           "②縮短外拱跨距（讓圍束真正到得了核心中央）、③把 \\(h_x\\) 變小，使 \\(s_o = 10 + (35-h_x)/3\\) 放寬。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 5：強柱弱梁節點彎矩平衡（側移向右）
# ════════════════════════════════════════════════════════════════════
def fig5():
    s = SVG(900, 440, "g5")
    jx, jy, jw, jh = 390, 170, 120, 100
    s.text(450, 26, "節點自由體：側移向右（→）時，各構件作用在接頭上的彎矩", 14, C["blue"], bold=True)
    s.line(680, 62, 790, 62, C["red"], 2.6, arrow=True)
    s.text(735, 52, "地震側移", 12, C["red"], bold=True)
    # 構件
    s.rect(jx + 10, 50, jw - 20, jy - 50, C["concrete"], C["line"], 1.8)
    s.rect(jx + 10, jy + jh, jw - 20, 120, C["concrete"], C["line"], 1.8)
    s.rect(140, jy + 10, jx - 140, jh - 30, C["concrete"], C["line"], 1.8)
    s.rect(jx + jw, jy + 10, 250, jh - 30, C["concrete"], C["line"], 1.8)
    s.rect(jx, jy, jw, jh, C["blue3"], C["blue"], 2)
    s.text(jx + jw / 2, jy + jh / 2 + 5, "接頭", 13, "#0d47a1", bold=True)
    s.text(jx + jw / 2, 44, "上柱", 11.5, C["mut"])
    s.text(jx + jw / 2, jy + jh + 138, "下柱", 11.5, C["mut"])
    s.text(150, jy + 2, "左梁", 11.5, C["mut"], anchor="start")
    s.text(jx + jw + 240, jy + 2, "右梁", 11.5, C["mut"], anchor="end")
    # 受拉側
    s.line(150, jy + 15, jx - 2, jy + 15, C["red"], 3)
    s.line(jx + jw + 2, jy + jh - 25, jx + jw + 240, jy + jh - 25, C["red"], 3)
    s.text(260, jy + jh - 8, "頂筋受拉 → Mnb⁻", 11.5, C["red"], bold=True)
    s.text(jx + jw + 125, jy + 4, "底筋受拉 → Mnb⁺", 11.5, C["red"], bold=True)
    # 梁彎矩（作用於接頭，逆時針）
    s.moment(jx - 8, jy + jh / 2 - 10, 30, 110, 250, C["red"], 2.6)
    s.moment(jx + jw + 8, jy + jh / 2 - 10, 30, -70, 70, C["red"], 2.6)
    s.text(jx - 46, jy + jh / 2 - 6, "Mnb,左", 12.5, C["red"], anchor="end", bold=True)
    s.text(jx + jw + 46, jy + jh / 2 - 6, "Mnb,右", 12.5, C["red"], anchor="start", bold=True)
    # 柱彎矩（作用於接頭，順時針）
    s.moment(jx + jw / 2, jy - 8, 30, 160, 20, C["blue"], 2.6)
    s.moment(jx + jw / 2, jy + jh + 8, 30, -20, -160, C["blue"], 2.6)
    s.text(jx + jw / 2 + 48, jy - 28, "Mnc,上", 12.5, C["blue"], anchor="start", bold=True)
    s.text(jx + jw / 2 + 48, jy + jh + 40, "Mnc,下", 12.5, C["blue"], anchor="start", bold=True)
    # 圖例
    s.text(690, 300, "紅：梁給接頭的彎矩（同為逆時針）", 11.5, C["red"], anchor="start")
    s.text(690, 320, "藍：柱給接頭的彎矩（同為順時針）", 11.5, C["blue"], anchor="start")
    s.text(690, 340, "兩組必須互相平衡", 11.5, C["mut"], anchor="start")
    s.rect(150, 392, 600, 36, "#fff", C["blue"], 1.6, rx=8)
    s.text(450, 416, "Mnc,上 + Mnc,下  ≥  (6/5) × (Mnb,左 + Mnb,右)", 14.5, "#0d47a1", bold=True)
    cap = ("節點是一個自由體：兩根梁送進來的彎矩（同向）必須由上下兩根柱（反向）承接。所以問題不是「這根柱比這根梁強嗎」，"
           "而是「<b>柱能提供的總容量</b>是否超過<b>梁能送進來的總需求</b>」。"
           "注意同一個節點左梁是頂筋受拉、右梁是底筋受拉；地震方向反轉時兩者互換 → \\(\\sum M_{nb}\\) 要<b>兩個方向各算一次</b>取大。")
    return s.render(), cap


# ════════════════════════════════════════════════════════════════════
# 圖 6：內接頭水平力自由體（側移向右）
# ════════════════════════════════════════════════════════════════════
def fig6():
    s = SVG(900, 470, "g6")
    jx, jy, jw, jh = 380, 150, 140, 150
    ym = jy + jh / 2
    s.text(450, 26, "內接頭自由體：側移向右（→），沿接頭中高切開，取上半部", 14, C["blue"], bold=True)
    s.line(700, 58, 800, 58, C["red"], 2.6, arrow=True)
    s.text(750, 48, "地震側移", 12, C["red"], bold=True)
    # 構件
    s.rect(jx + 15, 50, jw - 30, jy - 50, C["concrete"], C["line"], 1.6)
    s.rect(jx + 15, jy + jh, jw - 30, 90, C["concrete"], C["line"], 1.6)
    s.rect(120, jy + 10, jx - 120, jh - 20, C["concrete"], C["line"], 1.6)
    s.rect(jx + jw, jy + 10, 260, jh - 20, C["concrete"], C["line"], 1.6)
    s.rect(jx, jy, jw, jh, "#f5f7f8", C["blue"], 2)
    s.rect(jx, jy, jw, jh / 2, C["blue3"], C["blue"], 0, op=0.9)
    s.line(jx - 30, ym, jx + jw + 30, ym, C["orange"], 1.8, dash="7 4")
    s.text(jx + jw + 34, ym + 4, "切面", 11.5, C["orange"], anchor="start", bold=True)
    # 鋼筋線
    yt, ybt = jy + 22, jy + jh - 22
    s.line(130, yt, jx + jw - 12, yt, C["steel"], 2)
    s.line(jx + 12, ybt, jx + jw + 250, ybt, C["steel"], 2)
    s.line(jx + 12, yt, jx + jw + 250, yt, C["steel"], 1.2, dash="3 3")
    s.line(130, ybt, jx + jw - 12, ybt, C["steel"], 1.2, dash="3 3")
    # 上半部力（作用在接頭上）
    s.line(jx - 2, yt, jx - 110, yt, C["red"], 3, arrow=True)
    s.text(jx - 8, jy - 2, "T_top = 1.25fy·As,左頂", 12, C["red"], anchor="end", bold=True)
    s.text(jx - 8, yt + 28, "左梁頂筋把接頭往左拉", 11, C["mut"], anchor="end")
    s.line(jx + jw + 110, yt + 8, jx + jw + 2, yt + 8, C["red"], 3, arrow=True)
    s.text(jx + jw + 8, jy - 2, "C_bot：右梁頂部壓力", 12, C["red"], anchor="start", bold=True)
    s.text(jx + jw + 8, yt + 28, "＝右梁底筋拉力 1.25fy·As,右底", 11, C["mut"], anchor="start")
    s.line(jx + jw / 2 - 50, 80, jx + jw / 2 + 50, 80, C["blue"], 3, arrow=True)
    s.text(jx + jw / 2 + 58, 85, "Vcol（上柱剪力，反向）", 12, C["blue"], anchor="start", bold=True)
    s.line(jx + jw / 2 - 58, ym - 10, jx + jw / 2 + 58, ym - 10, C["green"], 3.4, arrow=True)
    s.text(jx + jw / 2, ym - 18, "Vjh", 13, C["green"], bold=True)
    # 下半部力（淡色，供對照）
    s.line(jx - 110, ybt, jx - 2, ybt, "#ef9a9a", 2.4, arrow=True)
    s.text(jx - 8, ybt + 32, "左梁底部壓力（作用於下半部）", 11, "#c48b8b", anchor="end")
    s.line(jx + jw + 2, ybt, jx + jw + 110, ybt, "#ef9a9a", 2.4, arrow=True)
    s.text(jx + jw + 8, ybt + 32, "右梁底筋拉力（作用於下半部）", 11, "#c48b8b", anchor="start")
    s.line(jx + jw / 2 + 50, jy + jh + 60, jx + jw / 2 - 50, jy + jh + 60, "#90caf9", 2.4, arrow=True)
    # 公式
    s.rect(160, 400, 580, 58, "#fff", C["blue"], 1.6, rx=8)
    s.text(450, 424, "上半部 ΣFx = 0：Vjh = T_top + C_bot − Vcol", 14.5, "#0d47a1", bold=True)
    s.text(450, 446, "外接頭／角接頭只有一側有梁 → Vjh = T_top − Vcol", 12, C["mut"])
    cap = ("切面以上：左梁頂筋拉力 \\(T_{top}\\) 把接頭往左拉，右梁頂部壓力 \\(C_{bot}\\)（大小等於右梁<b>底筋</b>拉力，故以 bot 標記）把接頭往左推 —— "
           "<b>兩者同向，所以相加</b>；上柱剪力 \\(V_{col}\\) 方向相反，所以相減。"
           "搞錯這個符號會讓答案差兩倍以上 —— 而且是最常見的錯誤。")
    return s.render(), cap


FIGS = [fig0, fig1, fig2, fig3, fig4, fig5, fig6]

# 流程圖（圖 7）：沿用版面，只修內容與重疊
FLOW_FIX = [
    ('<text x="644" y="199" font-size="11.5" fill="#546e7a">是</text>',
     '<text x="626" y="201" font-size="11.5" fill="#546e7a">是</text>'),
    ('<text x="644" y="102" font-size="11.5" fill="#546e7a">是</text>',
     '<text x="626" y="104" font-size="11.5" fill="#546e7a">是</text>'),
    ('Vjh = T_top + T_bot − Vcol', 'Vjh = T_top + C_bot − Vcol'),
    ('外／角接頭：只有 T_top', 'C_bot ＝ 另側梁底筋拉力；外／角接頭只有 T_top'),
    ('bj = min(bc, bw + 0.5hc)', 'bj = min(bw + hc, bw + 2x) ≤ bc'),
    ('γ = 5.3 / 4.0 / 3.2（kgf/cm²）', 'γ = 5.3 / 3.9 / 3.2（kgf/cm²）'),
    ('MPa 制為 1.7 / 1.25 / 1.0', 'MPa 制為 1.7 / 1.2 / 1.0'),
    ('密箍區長 = 2h；第一支 ≤ s/2', '密箍區長 = 2h；第一支距柱面 ≤ 5 cm'),
    ('<text x="160" y="550" font-size="11" text-anchor="middle" fill="#e65100" font-weight="700">Vc 可以計入嗎？</text>',
     '<text x="160" y="543" font-size="10.5" text-anchor="middle" fill="#e65100" font-weight="700">地震剪力 ≥ ½Ve ？</text>'
     '<text x="160" y="559" font-size="9.5" text-anchor="middle" fill="#e65100">（且 Nu &lt; Agf\'c/20，梁幾乎必成立）</text>'),
    ('<text x="100" y="584" font-size="10.5" text-anchor="middle" fill="#546e7a">不可</text>',
     '<text x="100" y="584" font-size="10.5" text-anchor="middle" fill="#546e7a">是</text>'),
    ('<text x="222" y="584" font-size="10.5" text-anchor="middle" fill="#546e7a">可</text>',
     '<text x="222" y="584" font-size="10.5" text-anchor="middle" fill="#546e7a">否</text>'),
    ('<text x="460" y="550" font-size="11" text-anchor="middle" fill="#e65100" font-weight="700">Nu &lt; Ag f\'c /20 ？</text>',
     '<text x="460" y="543" font-size="10.5" text-anchor="middle" fill="#e65100" font-weight="700">Nu &lt; Ag f\'c /20 ？</text>'
     '<text x="460" y="559" font-size="9.5" text-anchor="middle" fill="#e65100">（且地震剪力 ≥ ½，柱幾乎必成立）</text>'),
]
FLOW_CAP = ("五個判斷菱形。\\(V_c=0\\) 的兩個條件（地震剪力 ≥ 最大剪力的一半，<b>且</b> \\(N_u &lt; A_g f'_c/20\\)）對梁與柱<b>完全相同</b>，"
            "差別只在哪一個是臨界：梁幾乎沒有軸力，所以看剪力比；柱的設計剪力本來就幾乎全由梁的 \\(M_{pr}\\) 而來，所以看軸壓"
            "（常常是臨界，必須把 \\(A_g f'_c/20\\) 算出來）。")

# 內文同步修正（與新圖一致）
TEXT_FIX = [
    ("6/5 = 1.2 只是<b>降低機率</b>而非絕對保證（見 §5.2）", "6/5 = 1.2 只是<b>降低機率</b>而非絕對保證（見 §5.1）"),
    ("關鍵在於 \\(T_{top}\\) 與 \\(C_{bot}\\) 方向相同（一個往左拉、一個往右推，對切面而言是同向的水平推力），",
     "關鍵在於 \\(T_{top}\\) 與 \\(C_{bot}\\) 方向相同（左梁頂筋往左拉、右梁頂部壓力往左推，作用在切面以上是同向的水平力），"),
]


def main(src, dst):
    html = open(src, encoding="utf-8").read()
    blocks = list(re.finditer(r'<div class="fig">\s*(<svg.*?</svg>)\s*<div class="cap">(.*?)</div>', html, flags=re.S))
    assert len(blocks) == 8, len(blocks)
    out, last = [], 0
    for i, m in enumerate(blocks):
        out.append(html[last:m.start(1)])
        if i < 7:
            svg, cap = FIGS[i]()
        else:
            svg = m.group(1)
            for a, b in FLOW_FIX:
                if a in svg:
                    svg = svg.replace(a, b)
                else:
                    assert b in svg, a
            cap = FLOW_CAP
        out.append(svg + '\n<div class="cap">\n' + cap + '\n')
        last = m.end(2)
    out.append(html[last:])
    html = "".join(out)
    for a, b in TEXT_FIX:
        if a in html:
            html = html.replace(a, b)
    open(dst, "w", encoding="utf-8", newline="").write(html)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
