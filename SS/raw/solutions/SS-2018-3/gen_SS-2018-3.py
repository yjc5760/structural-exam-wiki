#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2018-3 圖解產生腳本（箱型柱–H 梁接頭之填角銲檢核）

銲道幾何、應力與所需銲腳尺寸全部由下方常數區重算；改銲腳尺寸重跑，判定跟著變。
執行：python3 gen_SS-2018-3.py   →   figs/*.svg
附加 fig1_problem：題目附圖重繪（重繪依據：題目正本 -problem.md §4 判讀清單，待確認）；
輸出目錄可由參數指定：python3 gen_<id>.py [輸出目錄]（預設 figs/）。
"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

# ══════════════════════════════════════════════════════════════
# L1：題目給定（§1，單位 mm、N）
# ══════════════════════════════════════════════════════════════
MF   = 124.5e6      # N·mm 梁翼負擔彎矩
MWB  = 25.5e6       # N·mm 梁腹負擔彎矩
Q    = 100e3        # N    設計剪力
FA   = 90.5         # N/mm^2 銲道容許應力（日本 AIJ：F/(1.5√3)，F = 235）
FY   = 235.0        # N/mm^2 SN400B
D_   = 500.0        # mm 梁總高
BF   = 200.0        # mm 翼板寬
TFL  = 16.0         # mm 翼板厚
TWB  = 9.0          # mm 腹板厚
SCALLOP = 40.0      # mm 腹板端部扇形開孔
W0   = 6.0          # mm 圖示銲腳尺寸

# ── 腹板銲道幾何 ──
LW   = D_ - 2*(TFL + SCALLOP)                 # 388
THR  = lambda w: w/math.sqrt(2)               # 有效喉厚 0.707w
SW   = lambda w: 2*THR(w)*LW**2/6             # 斷面模數（雙面）
AW   = lambda w: 2*THR(w)*LW                  # 面積（雙面）

# ── 腹板應力（6 mm）──
TAU1 = MWB/SW(W0)                             # 119.8 彎矩（水平）
TAU2 = Q/AW(W0)                               # 30.4  剪力（垂直）
TAU  = math.hypot(TAU1, TAU2)                 # 123.6 合成
W_WEB_REQ = W0*TAU/FA                          # 8.19 → 9 mm
W_WEB_USE = 9      # §4 Step 6：8.19 → 9 mm
TAU_CHK = math.hypot(MWB/SW(W_WEB_USE), Q/AW(W_WEB_USE))   # 82.4

# ── 翼板銲道（力偶臂 d − t_f，銲道沿上下表面各一道）──
ARM  = D_ - TFL                               # 484
FF   = MF/ARM                                 # 257,231 N
LF   = 2*BF                                   # 400（保守取法）
LF_ALT = 2*BF + 2*TFL                         # 432（較寬鬆取法）
AWF  = lambda w, L=LF: THR(w)*L
TAUF = FF/AWF(W0)                             # 151.6
TAUF_ALT = FF/AWF(W0, LF_ALT)                 # 140.3
W_FL_REQ = W0*TAUF/FA                          # 10.05
W_FL_USE = 11     # §4 翼板 Step 4：10.05 → 進位 11 mm（2026-11-01；10 mm 時 τ=91.0>90.5）
SIG_BASE = FF/(BF*TFL)                        # 80.4 母材
SIG_ALLOW_BASE = 0.6*FY                       # 141
W_FL_MAX = TFL - 2                            # 沿板緣上限 14 mm

# ── 三套規範之容許應力（§5 爭議三、§6.1）──
FEXX = 70*6.895                               # 482.6 N/mm^2（E70）
FA_TW = 0.3*FEXX                              # 144.8（台灣 ASD ＝ AISC ASD）
def k_dir(theta_deg):
    return 1.0 + 0.5*math.sin(math.radians(theta_deg))**1.5
TH_WEB = math.degrees(math.atan2(TAU1, TAU2))       # 75.8°（合力與銲軸夾角）
TH_FL  = 90.0
FA_AISC_WEB = FA_TW*k_dir(TH_WEB)                   # 213.9
FA_AISC_FL  = FA_TW*k_dir(TH_FL)                    # 217.2


# ══════════════════════════════════════════════════════════════
def fig1_joint():
    """圖 1：接頭重繪——三處皆為 6 mm 填角銲"""
    W, H = 900, 780
    XL, XR = -230.0, 344.0
    YL, YH = -84.0, 590.0
    Lm, Rm, Tm, Bm = 56, 56, 118, 96
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    ox = (W - (XR-XL)*sx)/2 - XL*sx
    cv = Canvas(W, H, sx=sx, ox=ox, oy=Bm - YL*sx, bg="#FFFFFF")

    yb, yt = 0.0, D_                           # 梁下、上緣
    YC = (yb + yt)/2                           # 梁中心高
    # 箱型柱
    cv.polygon([(-200, -60), (0, -60), (0, 560), (-200, 560)], "#DCE3EC", C["member"], 2.4)
    cv.text_px(cv.X(-100), cv.Y(560) - 16, "SN400B 箱型柱", 12.5, C["muted"], weight="700")
    # 內橫隔板（於梁翼板高度）
    for y in (yb + TFL/2, yt - TFL/2):
        cv.line((-200, y), (0, y), C["member2"], 3.0, dash="8 5")
    cv.text_px(cv.X(-190), cv.Y(yt - TFL/2) - 18, "內橫隔板（虛線）", 11.5, C["muted"], "start")

    XB = 300.0
    cv.polygon([(0, yb), (XB, yb), (XB, yb+TFL), (0, yb+TFL)], "#EDF1F6", C["member"], 2.0)
    cv.polygon([(0, yt-TFL), (XB, yt-TFL), (XB, yt), (0, yt)], "#EDF1F6", C["member"], 2.0)
    cv.polygon([(0, yb+TFL), (XB, yb+TFL), (XB, yt-TFL), (0, yt-TFL)],
               "#F7F9FB", C["member2"], 1.6)

    # 三處填角銲（皆 6 mm）
    welds = ((yt - TFL/2, "上翼板"), (YC, "腹板"), (yb + TFL/2, "下翼板"))
    for y, nm in welds:
        cv.polygon([(0, y-13), (26, y-13), (0, y+13)], C["fill_t"], C["load"], 2.4)
        cv.text_px(cv.X(34), cv.Y(y), f"{nm}　{W0:g} mm 填角銲", 12, C["load"], "start",
                   weight="700")

    # 腹板有效銲長與扇形開孔
    cv.line((-6, yb + TFL + SCALLOP), (-6, yt - TFL - SCALLOP), C["bmd"], 5.0, cap="butt")
    cv.dim((-6, yb + TFL + SCALLOP), (-6, yt - TFL - SCALLOP),
           f"l_{{w}} = {LW:g}", off=-52, label_off=-15, color=C["bmd"])
    for y0 in (yb + TFL, yt - TFL - SCALLOP):
        cv.dim((-6, y0), (-6, y0 + SCALLOP), f"{SCALLOP:g}", off=-138, label_off=-14,
               color=C["accent"])
    cv.text_px(cv.X(-6) - 150, cv.Y(YC) - 6, "扇形開孔（scallop）", 11.5, C["accent"],
               "middle", weight="700")

    # 梁尺寸
    cv.dim((XB, yb), (XB, yt), f"d = {D_:g}", off=40, label_off=13)
    cv.dim((XB, yt-TFL), (XB, yt), f"t_{{f}} = {TFL:g}", off=118, label_off=14)

    # 作用力
    cv.arrow((250, yt + 60), (250, yt + 12), C["load"], 3.4, 11)
    cv.math_px(cv.X(250) + 12, cv.Y(yt + 40), f"Q = {Q/1000:g} kN", 13, C["load"],
               "start", weight="700")
    cv.moment_arrow((190, YC), r=26, ccw=False, color=C["load"], w=2.8, span=250, start=120)
    cv.math_px(cv.X(190), cv.Y(YC) - 58,
               f"M = {(MF+MWB)/1e6:g} kN·m", 13, C["load"], weight="700")

    cv.text_px(W/2, 34, "圖 1　梁柱接頭重繪：三處銲接符號皆為 6 mm 填角銲", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"腹板有效銲長 l_w = d − 2(t_f + 扇形開孔) = {D_:g} − 2({TFL:g} + {SCALLOP:g}) = {LW:g} mm",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "舊版把梁翼判為 CJP 而以母材 0.6F_y 驗算得 OK；依圖面應以銲道喉面積檢核 ⇒ NG",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"l_w 與題目所給 S_w 公式中的 {LW:g}² 完全一致，可作為圖面判讀的交叉驗核",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2018-3-fig-1-joint.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_web_stress():
    """圖 2：腹板銲道之應力向量合成"""
    PWD, PH = 500, 440

    # ── 格 1：向量合成（範圍以合成向量的外接框置中）──
    XL, XR, YL, YH = -55.0, 175.0, -81.0, 44.0
    Lm, Tm, Bm = 44, 112, 104
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    p1 = Canvas(PWD, PH, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx)
    p1.panel("① 兩個分量正交", "彎矩水平、剪力垂直")
    VS = 150.0 / TAU        # 合成向量 → 150 繪圖單位
    p1.arrow((0, 0), (TAU1*VS, 0), C["accent"], 3.2, 11)
    p1.arrow((0, 0), (0, -TAU2*VS), C["compr"], 3.2, 11)
    p1.arrow((0, 0), (TAU1*VS, -TAU2*VS), C["load"], 4.0, 13)
    p1.line((TAU1*VS, 0), (TAU1*VS, -TAU2*VS), C["ghost"], 1.4, dash="4 3")
    p1.line((0, -TAU2*VS), (TAU1*VS, -TAU2*VS), C["ghost"], 1.4, dash="4 3")
    p1.math_px(p1.X(TAU1*VS/2), p1.Y(0) - 16, f"τ_{{w1}} = {TAU1:.1f}", 13, C["accent"],
               weight="700")
    p1.math_px(p1.X(0) - 10, p1.Y(-TAU2*VS/2), f"τ_{{w2}} = {TAU2:.1f}", 13, C["compr"],
               "end", weight="700")
    p1.math_px(p1.X(TAU1*VS) + 10, p1.Y(-TAU2*VS) + 16, f"τ = {TAU:.1f}", 15, C["load"],
               "end", weight="700")
    p1.text_px(PWD/2, PH - 62, f"τ = {TAU:.1f} 大於 f_a = {FA:g} N/mm²", 13.5, C["load"],
               weight="700")
    p1.text_px(PWD/2, PH - 38, f"⇒ 6 mm 腹板填角銲 NG（超出 {100*(TAU/FA-1):.0f}%）",
               13, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 16, "只比 τ_w1 就下結論，會漏掉剪力貢獻", 12, C["muted"])

    # ── 格 2：所需銲腳尺寸 ──
    p2 = Canvas(PWD, PH, sx=1)
    p2.panel("② 反算所需銲腳尺寸", "應力與 w 成反比")
    x0, bw = 150, 250
    rows = ((f"{W0:g} mm（圖示）", TAU, C["load"]),
            (f"{W_WEB_REQ:.2f} mm（恰好）", FA, C["accent"]),
            (f"{W_WEB_USE:g} mm（採用）", TAU_CHK, C["bmd"]))
    peak = TAU*1.14
    for i, (nm, v, col) in enumerate(rows):
        y = 142 + i*58
        p2.text_px(x0 - 12, y, nm, 12.5, C["text"], "end", weight="700")
        p2.rect_px(x0, y-15, bw, 30, "#EDF1F6", 6)
        p2.rect_px(x0, y-15, bw*v/peak, 30, col, 6)
        p2.text_px(x0 + bw*v/peak + 17, y, f"{v:.1f}", 12, col, "start", weight="700")
    xa = x0 + bw*FA/peak
    p2.parts.append(f'<line x1="{xa}" y1="116" x2="{xa}" y2="{142+2*58+22}" '
                    f'stroke="{C["accent"]}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    p2.text_px(xa, 108, f"f_a = {FA:g}", 12, C["accent"], weight="700")
    p2.math_px(PWD/2, PH - 62, f"τ(w) = {W0*TAU:.0f}/w", 14, C["text"], weight="700")
    p2.text_px(PWD/2, PH - 38, f"令 τ = f_a ⇒ w ≥ {W_WEB_REQ:.2f} mm，採用 {W_WEB_USE:g} mm",
               13, C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 16, f"{W_WEB_USE:g} mm 驗算：τ = {TAU_CHK:.1f} 小於 {FA:g} ✓",
               12, C["muted"])

    compose([p1, p2], cols=2,
            title="圖 2　腹板填角銲：彎矩與剪力必須向量合成",
            sub=f"腹板銲道為兩條鉛垂線；M_w 使力沿梁軸（橫向 θ = 90°）、Q 使力鉛垂（縱向 θ = 0°），兩者正交",
            note=f"題目已給 τ_w1 = {TAU1:.1f}，核心就是補上 τ_w2 = Q/A_w = {TAU2:.1f} 再合成——1 分鐘可完成",
            path=os.path.join(OUT, "SS-2018-3-fig-2-web-stress.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_code_compare():
    """圖 3：同一組銲道，三套規範三種結論"""
    W, H = 980, 430
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 316, 400
    peak = max(FA_AISC_FL, TAUF) * 1.12

    rows = (("日本 AIJ（本題給定）", f"F/(1.5√3)，F = {FY:g}", FA, C["load"]),
            ("台灣 2010 ASD 表 10.2-5", f"0.3F_EXX = 0.3 × {FEXX:.1f}", FA_TW, C["bmd"]),
            ("AISC 360-16 ＋方向性（腹板）", f"×(1+0.5·sin^{{1.5}}θ) ，θ = {TH_WEB:.1f}° ⇒ ×{k_dir(TH_WEB):.3f}",
             FA_AISC_WEB, C["compr"]),
            ("AISC 360-16 ＋方向性（翼板）", f"×(1+0.5·sin^{{1.5}}θ) ，θ = 90° ⇒ ×{k_dir(90):.3f}",
             FA_AISC_FL, C["accent"]))
    for i, (nm, note, v, col) in enumerate(rows):
        y = 132 + i*56
        cv.text_px(x0 - 14, y - 8, nm, 12.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11, C["muted"], "end")
        cv.rect_px(x0, y-15, bw, 30, "#EDF1F6", 6)
        cv.rect_px(x0, y-15, bw*v/peak, 30, col, 6)
        cv.text_px(x0 + bw*v/peak + 10, y, f"{v:.1f}", 12.5, col, "start", weight="700")

    # 兩個實際應力的位置
    for v, col, lab in ((TAU, C["sfd"], f"腹板實際 {TAU:.1f}"),
                        (TAUF, C["tension"], f"翼板實際 {TAUF:.1f}")):
        xv = x0 + bw*v/peak
        cv.parts.append(f'<line x1="{xv}" y1="108" x2="{xv}" y2="{132+3*56+24}" '
                        f'stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>')
        cv.text_px(xv, 100 if v == TAU else 82, lab, 12, col, weight="700")

    cv.text_px(W/2, 34, "圖 3　同一組 6 mm 銲道，三套規範得到三種結論", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"容許應力由 {FA:g} 到 {FA_AISC_FL:.1f} N/mm²，差 {FA_AISC_FL/FA:.1f} 倍",
               13, C["muted"])
    cv.text_px(W/2, H - 74,
               f"日本 AIJ：腹板 NG（需 {W_WEB_USE:g} mm）、翼板 NG（需 {W_FL_USE:g} mm）　←　本題主答案",
               13, C["load"], weight="700")
    cv.text_px(W/2, H - 50,
               f"台灣 2010 ASD（{FA_TW:.1f}）：腹板 OK、翼板 NG（僅超 {100*(TAUF/FA_TW-1):.0f}%）",
               12.5, C["bmd"])
    cv.text_px(W/2, H - 26,
               "AISC 360-16 加方向性強度：兩處皆 OK——「銲道夠不夠」在很大程度上是規範體系的問題",
               12.5, C["accent"])
    cv.save(os.path.join(OUT, "SS-2018-3-fig-3-code-compare.svg"))


# ══════════════════════════════════════════════════════════════
# 圖 1：題目附圖重繪（依題目正本 SS-2018-3-problem.md §4 判讀清單，待確認）
# 只畫考卷給的東西，與上方解題常數分開；不含銲長、應力、所需銲腳等任何解題結果。
# ══════════════════════════════════════════════════════════════
Q_D, Q_BF, Q_TF, Q_TW = 500.0, 200.0, 16.0, 9.0   # 圖面 梁斷面 500／200／16／9（mm）
Q_SC  = 40.0      # 圖面 扇形開孔至翼板內側 40 mm（#3）
Q_W   = "6"       # #1 三處皆 6 mm 填角銲；#2 箭頭與基線交點有圓圈（全周銲，待確認）
Q_M, Q_Q = "M=150kN-m", "Q=100kN"   # 圖面 梁端作用力（#4、#5）
# 示意（考卷未標）：箱型柱寬、柱壁厚、柱與梁畫出長度、斷面圖位置
Q_BC, Q_TC = 380.0, 16.0
Q_HC = 180.0
Q_LB = 640.0
Q_XS = 1000.0     # 斷面圖中心 x（排版用）


def _q_rect(cv, x0, x1, y0, y1, fill="#FFFFFF", w=1.6):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def _q_zig(cv, x0, x1, y):
    xm = (x0 + x1) / 2
    cv.poly([(x0, y), (xm - 10, y), (xm - 3, y + 18), (xm + 3, y - 18), (xm + 10, y), (x1, y)], C["member"], 1.6)


def _q_pinch(cv, p0, p1, label, orient, label_end=1, L=30):
    """小尺寸：兩支箭頭由外側指向兩端（同考卷 16、9 的標法），標字放在 label_end 那一側外面。"""
    (x0, y0), (x1, y1) = cv.P(p0), cv.P(p1)
    d = C["dim"]
    if orient == "v":
        lo, hi = (p0, p1) if y0 > y1 else (p1, p0)        # lo：畫面下方端
        (xl, yl), (xh, yh) = cv.P(lo), cv.P(hi)
        cv.parts.append(f'<line x1="{xl - 8:.1f}" y1="{yl:.1f}" x2="{xl + 22:.1f}" y2="{yl:.1f}" stroke="{d}" stroke-width="1" stroke-dasharray="3 3"/>')
        cv.parts.append(f'<line x1="{xh - 8:.1f}" y1="{yh:.1f}" x2="{xh + 22:.1f}" y2="{yh:.1f}" stroke="{d}" stroke-width="1" stroke-dasharray="3 3"/>')
        cv.arrow(_q_inv(cv, xl, yl + L), lo, d, 1.3, 8)
        cv.arrow(_q_inv(cv, xh, yh - L), hi, d, 1.3, 8)
        ty = (yl + L + 12) if label_end == 0 else (yh - L - 12)
        cv.math_px(xl + 2, ty, label, 15, C["text"])
    else:
        lo, hi = (p0, p1) if x0 < x1 else (p1, p0)
        (xl, yl), (xh, yh) = cv.P(lo), cv.P(hi)
        cv.arrow(_q_inv(cv, xl - L, yl), lo, d, 1.3, 8)
        cv.arrow(_q_inv(cv, xh + L, yh), hi, d, 1.3, 8)
        cv.math_px(xh + L + 4, yh + 16, label, 15, C["text"], "start")


def _q_inv(cv, x, y):
    return ((x - cv.ox) / cv.sx, (cv.h - y - cv.oy) / cv.sx)


def _q_weld_sym(cv, tip, dx=48, dy=-80):
    m = C["text"]
    tx, ty = cv.P(tip)
    cx, cy = tx + dx, ty + dy
    ang = math.atan2(ty - cy, tx - cx)
    cv.parts.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{m}" stroke-width="1.5"/>')
    hl, hw = 11, 4
    pts = [(tx, ty), (tx - hl * math.cos(ang) + hw * math.sin(ang), ty - hl * math.sin(ang) - hw * math.cos(ang)),
           (tx - hl * math.cos(ang) - hw * math.sin(ang), ty - hl * math.sin(ang) + hw * math.cos(ang))]
    cv.parts.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{m}"/>')
    cv.parts.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + 95:.1f}" y2="{cy:.1f}" stroke="{m}" stroke-width="1.5"/>')
    cv.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="#FFFFFF" stroke="{m}" stroke-width="1.6"/>')
    x0 = cx + 40
    cv.parts.append(f'<polygon points="{x0:.1f},{cy - 12:.1f} {x0:.1f},{cy + 12:.1f} {x0 + 16:.1f},{cy:.1f}" '
                    f'fill="#FFFFFF" stroke="{m}" stroke-width="1.5"/>')
    cv.text_px(x0 - 6, cy - 14, Q_W, 17, m, "end", weight="700")


def fig1_problem():
    path = os.path.join(OUT, "SS-2018-3-fig-1-problem.svg")
    cv = Canvas(1200, 740, sx=0.64, ox=330, oy=210)
    cv.panel("箱型柱–H 梁接頭立面與梁斷面", "單位：mm")
    top, bot = Q_D + Q_HC, -Q_HC
    # 箱型柱：兩側柱壁（雙線）＋梁翼高度之橫隔板
    for x0 in (-Q_BC, -Q_TC):
        _q_rect(cv, x0, x0 + Q_TC, bot, top)
    for y0 in (0.0, Q_D - Q_TF):
        _q_rect(cv, -Q_BC + Q_TC, -Q_TC, y0, y0 + Q_TF)
    _q_zig(cv, -Q_BC - 10, 10, top)
    _q_zig(cv, -Q_BC - 10, 10, bot)
    cv.text((-Q_BC / 2, top + 50), "柱 SN 400 B", 16, C["text"], weight="700")
    # H 梁立面
    for y0 in (0.0, Q_D - Q_TF):
        _q_rect(cv, 0, Q_LB, y0, y0 + Q_TF)
    ym = Q_D / 2
    cv.poly([(Q_LB, Q_TF), (Q_LB, ym - 12), (Q_LB + 8, ym - 4), (Q_LB - 8, ym + 4), (Q_LB, ym + 12),
             (Q_LB, Q_D - Q_TF)], C["member"], 1.6)
    cv.text((Q_LB * 0.62, Q_D + 60), "梁 SN 400 B", 16, C["text"], weight="700")
    # 扇形開孔（腹板上下端、靠柱面）與 40
    for yc, sg in ((Q_D - Q_TF, -1), (Q_TF, 1)):
        pts = [(Q_SC * math.sin(t * math.pi / 40), yc + sg * Q_SC * math.cos(t * math.pi / 40)) for t in range(21)]
        cv.poly(pts, C["member"], 1.4)
    xs = Q_SC + 70
    cv.line((Q_SC, Q_D - Q_TF), (xs + 10, Q_D - Q_TF), C["dim"], 1, dash="3 3")
    cv.line((0, Q_D - Q_TF - Q_SC), (xs + 10, Q_D - Q_TF - Q_SC), C["dim"], 1, dash="3 3")
    cv.dim((xs, Q_D - Q_TF), (xs, Q_D - Q_TF - Q_SC), f"{Q_SC:.0f}", label_off=-20, size=15)
    # 銲接符號三處（上翼板、腹板、下翼板）
    _q_weld_sym(cv, (0, Q_D - Q_TF / 2))
    _q_weld_sym(cv, (0, Q_D * 0.42), dx=48, dy=70)
    _q_weld_sym(cv, (0, Q_TF / 2), dx=48, dy=70)
    # 梁端作用力
    xq = 230.0
    cv.arrow((xq, Q_D * 0.70), (xq, Q_D * 0.44), C["load"], 4.0, 14)
    cv.moment_arrow((xq + 110, Q_D * 0.60), r=28, ccw=False, color=C["load"], w=3.4, span=250, start=150)
    cv.text((xq + 165, Q_D * 0.70), Q_M, 16, C["load"], "start", weight="700")
    cv.text((xq + 20, Q_D * 0.28), Q_Q, 16, C["load"], "start", weight="700")
    # 投影線（立面翼板延伸至斷面）
    for yy in (0.0, Q_D):
        cv.line((Q_LB + 40, yy), (Q_XS - Q_BF / 2 - 40, yy), C["member"], 1.2)
    # 梁斷面
    xa, xb = Q_XS - Q_BF / 2, Q_XS + Q_BF / 2
    _q_rect(cv, xa, xb, 0, Q_TF, C["fill_c"])
    _q_rect(cv, xa, xb, Q_D - Q_TF, Q_D, C["fill_c"])
    _q_rect(cv, Q_XS - Q_TW / 2, Q_XS + Q_TW / 2, Q_TF, Q_D - Q_TF, C["fill_c"])
    cv.dim((xa, Q_D), (xb, Q_D), f"{Q_BF:.0f}", off=-28, label_off=-15, size=15)
    xr = xb + 115
    for yy in (0.0, Q_D):
        cv.line((xb + 20, yy), (xr + 12, yy), C["dim"], 1, dash="3 3")
    cv.dim((xr, Q_D), (xr, 0), f"{Q_D:.0f}", label_off=-22, size=15)
    xt = xb + 55
    for yy in (Q_TF, Q_D - Q_TF):
        cv.line((xb, yy), (xt + 10, yy), C["dim"], 1, dash="3 3")
    _q_pinch(cv, (xt, Q_D - Q_TF), (xt, Q_D), f"{Q_TF:.0f}", "v", label_end=1)
    _q_pinch(cv, (xt, 0), (xt, Q_TF), f"{Q_TF:.0f}", "v", label_end=0)
    _q_pinch(cv, (Q_XS - Q_TW / 2, Q_D * 0.55), (Q_XS + Q_TW / 2, Q_D * 0.55), f"{Q_TW:.0f}", "h", label_end=1)
    compose([cv], cols=1,
            title="SS-2018-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；梁斷面與 40 依比例，柱寬、柱壁厚與構材長度為示意",
            note="三個銲接符號都是 6 mm 填角銲（不是全滲透），箭頭與基線交點的圓圈為全周銲記號",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 6 mm 填角銲讀成全滲透開槽銲；漏看全周銲圓圈；腹板銲長忘扣扇形開孔 40"),
]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
    fig1_joint(); fig2_web_stress(); fig3_code_compare()
    print(f"l_w={LW:g}  S_w(6)={SW(W0):,.0f} mm³  A_w(6)={AW(W0):,.0f} mm²")
    print(f"τw1={TAU1:.1f} τw2={TAU2:.1f} τ={TAU:.1f} > fa={FA} -> w≥{W_WEB_REQ:.2f}"
          f" 採 {W_WEB_USE}mm（驗算 τ={TAU_CHK:.1f}）")
    print(f"力偶臂={ARM:g} Ff={FF:,.0f} N  A_wf={AWF(W0):,.0f} mm²  τf={TAUF:.1f}"
          f" -> w≥{W_FL_REQ:.2f} 採 {W_FL_USE}mm（另一取法 {TAUF_ALT:.1f}）")
    print(f"母材 σ={SIG_BASE:.1f} 小於 0.6Fy={SIG_ALLOW_BASE:.0f} OK；最大銲腳 {W_FL_MAX:g}mm")
    print(f"三套容許應力：AIJ {FA} ／台灣 {FA_TW:.1f} ／AISC 腹板 {FA_AISC_WEB:.1f}"
          f"、翼板 {FA_AISC_FL:.1f}（θ_web={TH_WEB:.1f}°）")
    print("done ->", OUT)
