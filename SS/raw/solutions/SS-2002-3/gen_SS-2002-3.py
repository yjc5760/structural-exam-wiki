#!/usr/bin/env python3
"""
SS-2002-3 中間有弱軸側撐之固接－鉸接柱 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2002-3.py [輸出目錄]

重繪依據：題目正本 SS-2002-3-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪柱立面與斷面方位；考卷所附「設計 K 值表」屬設計圖表，不重繪。
柱高依比例；斷面僅示意方位（W14×53 尺寸考卷未畫）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2002-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2002-3-problem.md §4，已確認）；單位 m
# ══════════════════════════════════════════════════════════
H = 10.0              # #1 柱長 10 m（兩個面皆是）
#                       #2 底部固接；#3 頂端鉸接（側向束制、不可平移）
BR_TOP = 4.0          # #4 中間側撐距頂 4.0 m、距底 6.0 m，只在 X-Z 面
BR_BOT = H - BR_TOP
#                       #5 X-Z 面＝繞弱軸 Y；Y-Z 面＝繞強軸 X，無中間側撐

PW, PH = 330, 520


def _elev(title, sub, brace):
    sx = (PH - 170) / H
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2 + (45 if brace else 0), oy=70)
    cv.panel(title, sub)
    cv.line((0, 0), (0, H), C["member"], 4.5, cap="butt")
    cv.support((0, 0), "fixed", 0, size=22)
    cv.support((0, H), "pin", 90, size=14)            # 側向鉸支（三角形朝右）
    if brace:
        cv.support((0, BR_BOT), "pin", 90, size=14)
        cv.text((0, BR_BOT), "中間側撐", 12.5, C["accent"], "start", dx=34, weight="700")
        cv.dim((0, BR_BOT), (0, H), f"{BR_TOP:.1f} m", off=-62, label_off=-26)
        cv.dim((0, 0), (0, BR_BOT), f"{BR_BOT:.1f} m", off=-62, label_off=-26)
        cv.dim((0, 0), (0, H), f"{H:.1f} m", off=-112, label_off=-28)
    else:
        cv.dim((0, 0), (0, H), f"{H:.1f} m", off=-62, label_off=-28)
    return cv


def _section():
    cv = Canvas(PW, PH, sx=7.0, ox=PW / 2, oy=PH / 2 - 30)
    cv.panel("斷面方位", "W14×53（示意，未依比例）")
    bf, d, tf, tw = 20.0, 30.0, 2.0, 1.2
    for x0, x1, y0, y1 in ((-bf / 2, bf / 2, d / 2 - tf, d / 2),
                           (-bf / 2, bf / 2, -d / 2, -d / 2 + tf),
                           (-tw / 2, tw / 2, -d / 2 + tf, d / 2 - tf)):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.8)
    cv.line((0, -d / 2 - 4), (0, d / 2 + 6), C["muted"], 1.4, dash="6 4")
    cv.line((-bf / 2 - 4, 0), (bf / 2 + 6, 0), C["muted"], 1.4, dash="6 4")
    cv.math((0, d / 2 + 8), "Y", 16, C["text"], weight="700")
    cv.math((bf / 2 + 8, 0), "X", 16, C["text"], weight="700")
    cv.text_px(PW / 2, PH - 70, "腹板沿 Y 軸、翼板水平", 12.5, C["muted"])
    cv.text_px(PW / 2, PH - 50, "X-Z 面彎曲＝繞弱軸 Y", 12.5, C["muted"])
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([_elev("X-Z 面", "繞弱軸 Y 挫屈", True),
             _elev("Y-Z 面", "繞強軸 X 挫屈", False),
             _section()], cols=3,
            title="SS-2002-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；設計 K 值表為設計圖表，不重繪",
            note="底部固接、頂端側向鉸支；中間側撐只在 X-Z 面（距頂 4.0 m、距底 6.0 m）",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """與解析相同的加法：各項先四捨五入到 nd 位再相加"""
    return round(sum(round(t, nd) for t in terms), nd)


def _stack_row(cv, x0, y, scale, terms, colors, name, total_color, h=34, fmt="{:.3f}"):
    """水平堆疊長條：互制比 1.0 對應 scale 像素"""
    cv.text_px(x0 - 14, y, name, 14, C["text"], "end", weight="700")
    xx = x0
    for t, col in zip(terms, colors):
        w = scale * t
        cv.rect_px(xx, y - h/2, w, h, col, 0)
        if w > 44:
            cv.text_px(xx + w/2, y, fmt.format(t), 12.5, "#FFFFFF", weight="700")
        xx += w
    tot = rsum(terms)
    cv.text_px(xx + 12, y, "= " + fmt.format(tot), 15, total_color, "start", weight="700")
    return tot


# ══════════════════════════════════════════════════════════════
# 柱強度曲線（ASD Fa 與 LRFD φcFcr，舊版 LRFD φc = 0.85）
# ══════════════════════════════════════════════════════════════
import math


def q_fa(klr, fy, e):
    cc = math.sqrt(2 * math.pi ** 2 * e / fy)
    if klr <= cc:
        r = klr / cc
        return (1 - r * r / 2) * fy / (5 / 3 + 3 * r / 8 - r ** 3 / 8)
    return 12 * math.pi ** 2 * e / (23 * klr ** 2)


def q_phifcr(klr, fy, e, phi=0.85):
    lam = klr / math.pi * math.sqrt(fy / e)
    f = math.exp(-0.419 * lam ** 2) * fy if lam <= 1.5 else 0.877 / lam ** 2 * fy
    return phi * f


def q_curve_panel(W1, H1, title, sub, fy, e, marks, kmax=200.0, fmax=None):
    """marks: [(klr, '標籤', 是否控制)]；縱軸應力 tf/cm²"""
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    X0, X1, YB, YT = 90, W1 - 40, H1 - 110, 110
    fmax = fmax or fy
    PX = lambda k: X0 + (X1 - X0) * k / kmax
    PY = lambda f: YB - (YB - YT) * f / fmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT - 10, C["muted"], 1.5)
    for k in range(0, int(kmax) + 1, 50):
        cv.text_px(PX(k), YB + 18, f"{k}", 11.5, C["muted"])
    for f in [fmax * i / 4 for i in range(5)]:
        cv.text_px(X0 - 8, PY(f), f"{f:.2f}", 11, C["muted"], "end")
    cv.text_px((X0 + X1) / 2, YB + 42, "KL/r", 13, C["text"], weight="700")
    cv.text_px(X0 - 6, YT - 22, "tf/cm²", 12, C["text"], "start", weight="700")
    ks = [kmax * i / 300 for i in range(1, 301)]
    cv.poly([(PX(k), H1 - PY(min(q_phifcr(k, fy, e), fmax))) for k in ks], C["bmd"], 2.6)
    cv.poly([(PX(k), H1 - PY(min(q_fa(k, fy, e), fmax))) for k in ks], C["compr"], 2.6, dash="8 5")
    cc = math.sqrt(2 * math.pi ** 2 * e / fy)
    _hl(cv, H1, PX(cc), YB, PX(cc), YT, C["ghost"], 1.2, dash="3 4")
    cv.text_px(PX(cc) + 4, YT + 4, f"Cc = {cc:.1f}", 11.5, C["muted"], "start")
    for k, lab, ctrl in marks:
        col = C["load"] if ctrl else C["muted"]
        _hl(cv, H1, PX(k), YB, PX(k), PY(q_phifcr(k, fy, e)) - 4, col, 1.4 if ctrl else 1.0, dash="4 3")
        cv.dot((PX(k), H1 - PY(q_phifcr(k, fy, e))), 5.5 if ctrl else 4, fill=C["bmd"])
        cv.dot((PX(k), H1 - PY(q_fa(k, fy, e))), 5.5 if ctrl else 4, fill=C["compr"])
        cv.text_px(PX(k) + 4, YB - 10, lab, 11.5, col, "start", weight="700" if ctrl else "400")
    cv.legend(X1 - 200, YT + 10, [(C["bmd"], "LRFD φc·Fcr（φc = 0.85）"), (C["compr"], "ASD Fa")], size=12, gap=19)
    return cv

# ── SS-2002-3 解題圖解（2026-11-03 補繪）：數值取自 §1／§4 ──
Q_RX, Q_RY, Q_A = 14.96, 4.88, 100.64                 # W14×53                §1
Q_FY, Q_E = 2.5, 2100.0                                # t/cm²                 §1
Q_KF, Q_KP = 0.80, 1.0                                 # 考卷附表設計值：固-鉸、鉸-鉸   §4 步驟 1
Q_SEGS = [("強軸（Y-Z 面）全長", Q_KF * H * 100, Q_RX),
          ("弱軸下段（固-鉸 6 m）", Q_KF * BR_BOT * 100, Q_RY),
          ("弱軸上段（鉸-鉸 4 m）", Q_KP * BR_TOP * 100, Q_RY)]
Q_KLR = [kl / r for _, kl, r in Q_SEGS]
Q_CTRL = max(range(3), key=lambda i: Q_KLR[i])
Q_PA = q_fa(Q_KLR[Q_CTRL], Q_FY, Q_E) * Q_A
Q_PU = q_phifcr(Q_KLR[Q_CTRL], Q_FY, Q_E) * Q_A


def _fixed_pinned(n=60):
    """固-鉸柱第一模態：y = −sin(kx)/(kL) + cos(kx) + x/L − 1，kL = 4.4934"""
    kl = 4.4934
    ys = [(-math.sin(kl * t) / kl + math.cos(kl * t) + t - 1) for t in [i / n for i in range(n + 1)]]
    m = max(abs(v) for v in ys)
    return [v / m for v in ys]


def fig1_modes():
    W1, H1 = 420, 600
    panels = []
    for title, sub, segs in (("① 強軸（Y-Z 面）", "底固接、頂側向鉸支，無中間側撐", [(0.0, H, "fp", 0)]),
                             ("② 弱軸（X-Z 面）", "中間側撐距底 6 m、距頂 4 m", [(0.0, BR_BOT, "fp", 1), (BR_BOT, H, "pp", 2)])):
        sx = 40.0
        cv = Canvas(W1, H1, sx=sx, ox=150, oy=110)
        cv.panel(title, sub)
        cv.line((0, 0), (0, H), C["ghost"], 2.0, dash="6 5")
        cv.support((0, 0), "fixed", 0, size=20)
        cv.support((0, H), "pin", 90, size=13)
        amp = 1.3
        for y0, y1, kind, i in segs:
            n = 60
            ys = _fixed_pinned(n) if kind == "fp" else [math.sin(math.pi * j / n) for j in range(n + 1)]
            pts = [(amp * ys[j], y0 + (y1 - y0) * j / n) for j in range(n + 1)]
            ctrl = i == Q_CTRL
            cv.poly(pts, C["load"] if ctrl else C["deform"], 4.0)
            _, kl, r = Q_SEGS[i]
            cv.text_px(cv.X(amp) + 18, cv.Y((y0 + y1) / 2) - 10, f"KL = {kl:.0f} cm", 12.5,
                       C["load"] if ctrl else C["deform"], "start", weight="700")
            cv.text_px(cv.X(amp) + 18, cv.Y((y0 + y1) / 2) + 10, f"KL/r = {kl / r:.1f}" + ("（控制）" if ctrl else ""),
                       12.5, C["load"] if ctrl else C["deform"], "start", weight="700")
        if len(segs) == 2:
            cv.support((0, BR_BOT), "pin", 90, size=13)
            cv.dim((0, 0), (0, BR_BOT), f"{BR_BOT:g} m", off=-40, label_off=-24, size=12.5)
            cv.dim((0, BR_BOT), (0, H), f"{BR_TOP:g} m", off=-40, label_off=-24, size=12.5)
        else:
            cv.dim((0, 0), (0, H), f"{H:g} m", off=-40, label_off=-24, size=12.5)
        panels.append(cv)
    panels[0].text_px(W1 / 2, H1 - 30, f"K = {Q_KF}（表 (b) 固-鉸設計值）", 12.5, C["muted"])
    panels[1].text_px(W1 / 2, H1 - 30, f"下段 K = {Q_KF}、上段 K = {Q_KP}", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-modes.svg")
    compose(panels, cols=2,
            title=f"圖 1　兩個平面各自挫屈：弱軸下段 KL/r = {Q_KLR[Q_CTRL]:.1f} 控制",
            sub=f"rx = {Q_RX}、ry = {Q_RY} cm；K 取考卷附表設計值（非理論值 0.7）",
            note="側撐只擋弱軸、且不在中點：下段 6 m 固-鉸（480）比上段 4 m 鉸-鉸（400）長，控制的是下段",
            path=path)
    return path


def fig2_curve():
    cv = q_curve_panel(1000, 520, "柱強度曲線與三段細長比", f"Fy = {Q_FY}、E = {Q_E:g} t/cm²",
                       Q_FY, Q_E, [(Q_KLR[0], f"{Q_KLR[0]:.1f}", False), (Q_KLR[2], f"{Q_KLR[2]:.1f}", False),
                                   (Q_KLR[1], f"{Q_KLR[1]:.1f}（控制）", True)])
    k = Q_KLR[Q_CTRL]
    cv.text_px(560, 200, f"ASD：Fa = {q_fa(k, Q_FY, Q_E):.3f} ⇒ Pa = {Q_PA:.1f} t", 14, C["compr"], "start", weight="700")
    cv.text_px(560, 230, f"LRFD：φcFcr = {q_phifcr(k, Q_FY, Q_E):.3f} ⇒ φcPn = {Q_PU:.1f} t", 14, C["bmd"], "start", weight="700")
    cv.text_px(560, 260, f"A = {Q_A} cm²；λc = {k / math.pi * math.sqrt(Q_FY / Q_E):.3f}（非彈性）", 12.5, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-curve.svg")
    compose([cv], cols=1,
            title=f"圖 2　KL/r = {k:.1f}：Pa = {Q_PA:.1f} t、φcPn = {Q_PU:.1f} t",
            sub="同一個細長比代入兩套規範；兩條曲線都在 Cc 左側（非彈性段）",
            note="三段中細長比最大者控制；把側撐當成中點（上下段各 5 m）會改由 KL = 500 的上段控制，答案變成另一個數",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把側撐放到強軸方向；側撐位置上下顛倒（4.0／6.0 m）"),
    (fig1_modes, "§4 步驟 1–2",
     "側撐當成在中點、配到強軸平面；K 用理論值 0.7"),
    (fig2_curve, "§4 步驟 3",
     "取錯控制段；ASD／LRFD 公式區段（Cc、λc = 1.5）判斷錯"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert BR_BOT == 6.0
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
