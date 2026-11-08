#!/usr/bin/env python3
"""
SS-2003-3 雙角鋼－WT－柱 斜向受拉接合 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2003-3.py [輸出目錄]

重繪依據：題目正本 SS-2003-3-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西：拉力斜率 3:4、作用線通過 WT 翼板螺栓群、WT 翼板 2 列 × 4 顆螺栓
與 40／3@75／40 mm 配置。角鋼上的螺栓顆數為㈠所求，圖上不畫顆數。
WT 外形、角鋼長度與螺栓橫向間距考卷未標，僅示意。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2003-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2003-3-problem.md §4，已確認）；單位 mm
# ══════════════════════════════════════════════════════════
RISE, RUN = 3.0, 4.0            # #3 拉力斜率 垂直 3：水平 4，作用線通過 WT 翼板螺栓群
TW_WT, TF_WT = 12.4, 18.9       # #4 WT13.5x470，t_w = 12.4 mm、t_f = 18.9 mm
N_ROW, N_COL = 4, 2             # #5 8 顆 = 2 列 × 4 顆
EDGE, PITCH = 40.0, 75.0        # #5 上下端距 40 mm、垂直間距 3@75 = 225 mm
H_PL = 2 * EDGE + (N_ROW - 1) * PITCH          # WT 翼板高（推得值 305 mm）
YS = [H_PL / 2 - EDGE - k * PITCH for k in range(N_ROW)]
GAGE_SKETCH = 110.0             # 兩列螺栓橫向間距（考卷未標，示意）

PW, PH = 520, 520

_L = (RISE ** 2 + RUN ** 2) ** 0.5
UX, UY = RUN / _L, RISE / _L     # 拉力方向單位向量
NX, NY = -UY, UX


def _along(s, t=0.0):
    return (s * UX + t * NX, s * UY + t * NY)


def side_panel():
    W, H, sx = PW, PH, 0.7
    cv = Canvas(W, H, sx=sx, ox=100, oy=180)
    cv.panel("側視", "雙角鋼長肢背對背夾住 WT 腹板（外形示意）")
    # 柱翼板（斷開線示意）
    cv.polygon([(-30, -200), (0, -200), (0, 200), (-30, 200)], C["border"], C["member"], 1.6)
    cv.text((-15, 200), "W10 柱", 13, C["text"], "middle", dy=-14, weight="700")
    # WT 翼板
    cv.polygon([(0, -H_PL / 2), (TF_WT, -H_PL / 2), (TF_WT, H_PL / 2), (0, H_PL / 2)],
               C["fill_c"], C["member"], 1.6)
    for y in YS:
        cv.line((-8, y), (TF_WT + 8, y), C["member"], 3.4, cap="butt")
    # WT 腹板（外形示意）
    stem = [(TF_WT, H_PL / 2 - 20), _along(330, 55), _along(330, -55), (TF_WT, -H_PL / 2 + 20)]
    cv.polygon(stem, C["fill_c"], C["member"], 1.6)
    # 雙角鋼
    ang = [_along(150, 38), _along(470, 38), _along(470, -38), _along(150, -38)]
    cv.polygon(ang, C["border"], C["member"], 1.8)
    # 作用線（通過翼板螺栓群中心）與水平中心線
    cv.line(_along(0), _along(470), C["load"], 1.4, dash="10 4 2 4")
    cv.line((-60, 0), (260, 0), C["muted"], 1.2, dash="10 4 2 4")
    cv.arrow(_along(470), _along(560), C["load"], 3.0, 11)
    # 斜率三角形
    p0 = _along(530, -60)
    cv.poly([p0, (p0[0] + 80, p0[1]), (p0[0] + 80, p0[1] + 60)], C["text"], 1.4)
    cv.text((p0[0] + 40, p0[1]), "4", 13, C["text"], dy=12)
    cv.text((p0[0] + 80, p0[1] + 30), "3", 13, C["text"], "start", dx=6)
    cv.text(_along(330, -80), "角鋼螺栓一列（顆數為㈠所求）", 12, C["accent"], "start", weight="700")
    cv.text_px(W - 24, H - 74, "WT13.5x470", 13, C["text"], "end", weight="700")
    cv.math_px(W - 24, H - 52, f"t_{{w}} = {TW_WT} mm, t_{{f}} = {TF_WT} mm", 13, C["text"], "end")
    cv.text_px(W - 24, H - 30, "19 mm A325X 螺栓", 12.5, C["muted"], "end")
    return cv


def front_panel():
    W, H, sx = PW, PH, 0.95
    cv = Canvas(W, H, sx=sx, ox=W / 2 - 70, oy=H / 2 - 30)
    cv.panel("WT 翼板與柱接合（正視）", "2 列 × 4 顆；橫向間距示意")
    bw = GAGE_SKETCH + 2 * EDGE
    cv.line((-bw / 2 - 25, -200), (-bw / 2 - 25, 200), C["member"], 1.6)
    cv.line((bw / 2 + 25, -200), (bw / 2 + 25, 200), C["member"], 1.6)
    cv.polygon([(-bw / 2, -H_PL / 2), (bw / 2, -H_PL / 2), (bw / 2, H_PL / 2), (-bw / 2, H_PL / 2)],
               C["fill_c"], C["member"], 1.8)
    cv.line((-TW_WT / 2, -H_PL / 2), (-TW_WT / 2, H_PL / 2), C["member"], 1.4)
    cv.line((TW_WT / 2, -H_PL / 2), (TW_WT / 2, H_PL / 2), C["member"], 1.4)
    for y in YS:
        for x in (-GAGE_SKETCH / 2, GAGE_SKETCH / 2):
            cv.circle((x, y), 9.5, fill="#FFFFFF", stroke=C["member"], w=1.8)
    xr = bw / 2
    cv.dim((xr, YS[0]), (xr, H_PL / 2), f"{EDGE:.0f}mm", off=48, label_off=34)
    cv.dim((xr, YS[-1]), (xr, YS[0]), f"3@{PITCH:.0f}mm={3 * PITCH:.0f}mm", off=48, label_off=72)
    cv.dim((xr, -H_PL / 2), (xr, YS[-1]), f"{EDGE:.0f}mm", off=48, label_off=34)
    cv.text((0, -H_PL / 2), "W10 柱", 13, C["text"], dy=36, weight="700")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    a, b = side_panel(), front_panel()
    compose([a, b], cols=2,
            title="SS-2003-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#3–#5；只畫考卷所給條件",
            note="拉力斜率 3:4，作用線通過 WT 翼板 8 顆螺栓的中心",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2003-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_FU, Q_AG, Q_TA = 2.5, 4.1, 34.45, 0.95       # 雙角鋼 Ag、肢厚 cm      §1
Q_DH, Q_U = 2.2, 0.85                                # 扣除孔徑、U             §4.1
Q_PY = 0.9 * Q_FY * Q_AG
Q_AN = Q_AG - 2 * Q_DH * Q_TA
Q_PR = 0.75 * Q_FU * Q_U * Q_AN
Q_P  = min(Q_PY, Q_PR)                               # 77.51 t（降伏控制）
Q_AB, Q_FV, Q_D = 2.85, 4.2, 1.9                     # 螺栓 cm²、t/cm²、cm      §1
Q_RV2 = 0.75 * Q_FV * Q_AB * 2                       # 雙剪 17.96               §4.2
Q_RP  = 0.75 * 2.4 * Q_D * (2 * Q_TA) * Q_FU         # 承壓 26.64
Q_RB  = min(Q_RV2, Q_RP)
Q_N   = math.ceil(Q_P / Q_RB)                        # 5
Q_T, Q_V = RUN / _L * Q_P, RISE / _L * Q_P           # 62.01、46.51             §4.3
Q_NB = N_ROW * N_COL
Q_TU, Q_VU = Q_T / Q_NB, Q_V / Q_NB
Q_FVS = Q_VU / Q_AB                                  # 2.04
Q_FT = lambda fv: min(8.2 - 1.9 * fv, 6.3)           # 考卷背面表
Q_FTS = Q_TU / Q_AB
Q_P_ALT = Q_N * Q_RB                                 # 誤取設計力 89.8


def fig1_force():
    W1, H1 = 560, 560
    cv = Canvas(W1, H1, sx=0.95, ox=150, oy=290)
    cv.panel("① WT 翼板—柱：構材拉力沿 3:4 方向", "作用線通過 8 顆螺栓群中心（mm，示意）")
    cv.polygon([(-60, -190), (0, -190), (0, 190), (-60, 190)], "rgba(63,74,90,0.15)", C["member"], 1.4)
    cv.text_px(cv.X(-30), cv.Y(190) - 10, "柱翼板", 12, C["muted"])
    cv.polygon([(0, -H_PL / 2), (TF_WT, -H_PL / 2), (TF_WT, H_PL / 2), (0, H_PL / 2)], C["fill_c"], C["member"], 1.6)
    for y in YS:
        cv.line((-20, y), (TF_WT + 14, y), C["member"], 3.4, cap="butt")
    L = 210
    cv.arrow((TF_WT, 0), (TF_WT + L * UX, L * UY), C["load"], 3.4, 12)
    cv.text_px(cv.X(TF_WT + L * UX) + 8, cv.Y(L * UY), f"P = {Q_P:.2f} t", 13.5, C["load"], "start", weight="700")
    cv.arrow((TF_WT, 0), (TF_WT + L * UX, 0), C["compr"], 2.4, 10, dash="6 4")
    cv.arrow((TF_WT + L * UX, 0), (TF_WT + L * UX, L * UY), C["sfd"], 2.4, 10, dash="6 4")
    cv.text_px(cv.X(TF_WT + L * UX / 2), cv.Y(0) + 20, f"T = 4/5·P = {Q_T:.2f}（拉）", 12.5, C["compr"], weight="700")
    cv.text_px(cv.X(TF_WT + L * UX) + 8, cv.Y(L * UY / 2) + 18, f"V = 3/5·P = {Q_V:.2f}", 12.5, C["sfd"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"每顆：tu = {Q_TU:.2f} t（拉）、vu = {Q_VU:.2f} t（剪）", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"P 取構材設計強度 φtPn = min({Q_PY:.2f}, {Q_PR:.2f})", 12.5, C["muted"])
    p1 = cv
    cv = Canvas(W1, H1, sx=1)
    cv.panel("②（一）雙角鋼—WT 腹板螺栓數", f"雙剪 φRv = {Q_RV2:.2f} t/顆（承壓 {Q_RP:.2f}，不控制）")
    x0, sc = 170, 3.6
    _hl(cv, H1, x0 + sc * Q_P, 110, x0 + sc * Q_P, 380, C["load"], 1.8, dash="6 4")
    cv.text_px(x0 + sc * Q_P, 398, f"需求 {Q_P:.2f}", 12.5, C["load"], weight="700")
    for i, n in enumerate((Q_N - 1, Q_N)):
        y = 170 + i * 100
        v = n * Q_RB
        ok = v >= Q_P
        cv.text_px(x0 - 12, y, f"{n} 顆", 15, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 17, sc * v, 34, C["bmd"] if ok else C["ghost"], 4)
        if ok:
            cv.text_px(x0 + sc * v + 8, y, f"{v:.1f} ✓", 13.5, C["bmd"], "start", weight="700")
        else:
            cv.text_px(x0 + sc * v - 10, y, f"{v:.1f}（不足）", 13.5, C["load"], "end", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"n = {Q_P:.2f} / {Q_RB:.2f} = {Q_P / Q_RB:.2f} → {Q_N} 顆（一列）", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "角鋼／WT 腹板／角鋼 ⇒ 兩個剪力面", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-force.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　設計力 P = {Q_P:.2f} t：（一）{Q_N} 顆雙剪螺栓；（二）分解為拉 {Q_T:.2f}、剪 {Q_V:.2f}",
            sub="構材是長肢背對背的雙角鋼，WT 只是接頭板",
            note="斜向拉力的「垂直柱面」分量才是螺栓拉力；3:4 斜率中 4 在水平向（垂直柱面）",
            path=path)
    return path


def fig2_interact():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("（二）WT 翼板—柱 8 顆螺栓：拉剪互制（應力，t/cm²）", "容許拉應力 φFt' = 0.75(8.2 − 1.9fv) ≤ 0.75 × 6.3；剪應力 fv ≤ φFv")
    X0, X1, YB, YT = 120, 640, 470, 110
    fvm, ftm = 4.0, 5.5
    PX = lambda v: X0 + (X1 - X0) * v / fvm
    PY = lambda t: YB - (YB - YT) * t / ftm
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 5):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for t in range(0, 6):
        cv.text_px(X0 - 8, PY(t), f"{t}", 11.5, C["muted"], "end")
    cv.text_px((X0 + X1) / 2, YB + 42, "fv = vu / Ab", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 16, "ft = tu / Ab", 13, C["text"], "start", weight="700")
    fvcap = 0.75 * Q_FV
    pts = [(PX(v), H1 - PY(0.75 * Q_FT(v))) for v in [fvcap * i / 100 for i in range(101)]]
    cv.polygon([(PX(0), H1 - PY(0))] + pts + [(PX(fvcap), H1 - PY(0))], C["fill_m"], C["bmd"], 2.4)
    cv.text_px(PX(fvcap) + 6, PY(0.5), f"φFv = {fvcap:.2f}", 12, C["bmd"], "start")
    cv.dot((PX(Q_FVS), H1 - PY(Q_FTS)), 7, fill=C["load"])
    cv.text_px(PX(Q_FVS) - 10, PY(Q_FTS) + 22, f"需求 ({Q_FVS:.2f}, {Q_FTS:.2f})", 12.5, C["load"], "end", weight="700")
    cap = 0.75 * Q_FT(Q_FVS)
    _hl(cv, H1, PX(Q_FVS), PY(Q_FTS), PX(Q_FVS), PY(cap), C["accent"], 1.6, dash="4 3")
    cv.dot((PX(Q_FVS), H1 - PY(cap)), 5, fill=C["accent"])
    fv2, ft2 = Q_P_ALT * RISE / _L / Q_NB / Q_AB, Q_P_ALT * RUN / _L / Q_NB / Q_AB
    cv.dot((PX(fv2), H1 - PY(ft2)), 6, fill=C["ghost"])
    cv.text_px(PX(fv2) + 10, PY(ft2) - 8, f"誤取 P = {Q_P_ALT:.1f}：超出", 12, C["muted"], "start")
    xt = 680
    rows = [(f"fv = {Q_VU:.2f}/{Q_AB} = {Q_FVS:.2f} ≤ {fvcap:.2f} ✓", C["text"]),
            (f"Ft' = 8.2 − 1.9 × {Q_FVS:.2f} = {Q_FT(Q_FVS):.2f}", C["text"]),
            (f"φRt' = 0.75 × {Q_FT(Q_FVS):.2f} × {Q_AB} = {0.75 * Q_FT(Q_FVS) * Q_AB:.2f} t", C["bmd"]),
            (f"≥ tu = {Q_TU:.2f} t ✓（使用率 {Q_TU / (0.75 * Q_FT(Q_FVS) * Q_AB):.2f}）", C["bmd"]),
            ("", C["text"]),
            ("設計力要取構材的設計強度", C["muted"]),
            (f"φtPn = {Q_P:.2f}，不是螺栓群強度", C["muted"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight="700" if col == C["bmd"] else "400")
    path = os.path.join(OUT, f"{TAG}-fig-2-interact.svg")
    compose([cv], cols=1,
            title=f"圖 2　拉剪互制：需求點在容許區內（拉力使用率 {Q_TU / (0.75 * Q_FT(Q_FVS) * Q_AB):.2f}）",
            sub="考卷背面表的承壓型 A325 互制式（照考卷作答）",
            note="剪力越大、容許拉力越小：只單獨檢核拉力或剪力，會漏掉兩者同時作用的折減",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "拉力斜率讀反（4:3）；WT 翼板螺栓配置與端距讀錯"),
    (fig1_force, "§4.1–4.3",
     "把 WT 當構材；單剪；3:4 分量對調（拉剪互換）；自行假設設計載重"),
    (fig2_interact, "§4.3",
     "拉力與剪力分開檢核、漏了互制折減；以螺栓群強度 89.8 t 當設計力"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert H_PL == 305
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
