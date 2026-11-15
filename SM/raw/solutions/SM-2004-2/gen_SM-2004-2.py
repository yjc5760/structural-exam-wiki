# -*- coding: utf-8 -*-
"""SM-2004-2 圖解。
fig-1-problem：題目附圖重繪，幾何與應力只取自題目正本 SM-2004-2-problem.md §4 判讀清單（#1–#8），不含任何解題結果。
fig-2-mohr：解題圖解（2026-11-15 階段 E），Mohr 圓，數值取自解析 §4。
用法：python gen_SM-2004-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, tag_px
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
A_L, A_R = 20.0, 51.0          # #2、#3 左／右斜面與水平面夾角（度）
SN_L, ST_L = 2.0, 2.0          # #4、#5 左斜面：正應力（壓）、剪應力（朝頂點）kPa
SN_R, ST_R = 5.0, 3.0          # #6、#7 右斜面：正應力（壓）、剪應力（朝頂點）kPa
LB = 10.0                      # 底邊長（示意尺度，不影響角度）
tl, tr = math.tan(math.radians(A_L)), math.tan(math.radians(A_R))
XP = LB * tr / (tl + tr); YP = XP * tl          # 頂點
P0, P1, PT = (0.0, 0.0), (LB, 0.0), (XP, YP)

def unit(a): return (math.cos(math.radians(a)), math.sin(math.radians(a)))

def arc(cv, c, r, a0, a1, col):
    pts = [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / 30)),
            c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / 30))) for k in range(31)]
    cv.poly(pts, col, 1.6)

def fig_problem():
    W, H = 900, 440
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-1.0, LB + 3.2), (-2.2, YP + 2.4), 30, 30, 10, 10))
    cv.polygon([P0, P1, PT], "rgba(180,83,9,0.12)", C["member"], 2.6)
    cv.line((LB + 0.3, 0), (LB + 2.8, 0), C["member"], 2.0)
    cv.text((LB + 1.6, 0.35), "水平面", 14, C["text"], weight="700")
    # 角度
    arc(cv, P0, 1.6, 0, A_L, C["muted"]); cv.text((1.95, 0.33), "%g°" % A_L, 13.5, C["text"])
    arc(cv, P1, 1.0, 180 - A_R, 180, C["muted"]); cv.text((LB - 1.45, 0.45), "%g°" % A_R, 13.5, C["text"])
    arc(cv, PT, 0.8, 180 + A_L, 360 - A_R, C["muted"]); cv.text((XP, YP - 1.15), "%g°" % (180 - A_L - A_R), 13.5, C["text"])
    # 左斜面：法向（外法線 nL）、切向（朝頂點 uL）
    uL = unit(A_L); nL = (-uL[1], uL[0])
    mL = (XP * 0.55, YP * 0.55)
    s = (mL[0] + nL[0] * 2.2, mL[1] + nL[1] * 2.2); e = (mL[0] + nL[0] * 0.25, mL[1] + nL[1] * 0.25)
    cv.arrow(s, e, C["load"], 2.6, 10)
    cv.text((s[0] - 0.2, s[1] + 0.35), "%g kPa（壓）" % SN_L, 13.5, C["load"], weight="700")
    o = 0.45
    a0 = (mL[0] - uL[0] * 1.2 + nL[0] * o, mL[1] - uL[1] * 1.2 + nL[1] * o)
    a1 = (mL[0] + uL[0] * 1.2 + nL[0] * o, mL[1] + uL[1] * 1.2 + nL[1] * o)
    cv.arrow(a0, a1, C["deform"], 2.6, 10)
    cv.text((a1[0] + 0.25, a1[1] + 0.45), "%g kPa" % ST_L, 13.5, C["deform"], weight="700")
    # 右斜面：方向由右下角指向頂點
    uR = unit(180 - A_R); nR = (uR[1], -uR[0])     # 外法線指向右上
    mR = ((XP + LB) / 2, YP / 2)
    s = (mR[0] + nR[0] * 2.2, mR[1] + nR[1] * 2.2); e = (mR[0] + nR[0] * 0.25, mR[1] + nR[1] * 0.25)
    cv.arrow(s, e, C["load"], 2.6, 10)
    cv.text((s[0] + 0.3, s[1] + 0.35), "%g kPa（壓）" % SN_R, 13.5, C["load"], weight="700")
    a0 = (mR[0] - uR[0] * 0.9 + nR[0] * o, mR[1] - uR[1] * 0.9 + nR[1] * o)
    a1 = (mR[0] + uR[0] * 0.9 + nR[0] * o, mR[1] + uR[1] * 0.9 + nR[1] * o)
    cv.arrow(a0, a1, C["deform"], 2.6, 10)
    cv.text((a1[0] + 0.55, a1[1] + 0.25), "%g kPa" % ST_R, 13.5, C["deform"], weight="700")
    # 水平面：未知 σh（向上指向底面）、τh（向右）
    xm = LB * 0.45
    cv.arrow((xm, -2.0), (xm, -0.2), C["muted"], 2.4, 10)
    cv.math((xm + 0.3, -1.3), "σ_{h}", 15, C["muted"], anchor="start")
    cv.arrow((xm - 2.6, -0.4), (xm - 0.6, -0.4), C["muted"], 2.4, 10)
    cv.math((xm - 1.6, -0.9), "τ_{h}", 15, C["muted"])
    cv.text((xm + 1.4, -1.3), "（水平面上的所求量）", 12.5, C["muted"], anchor="start")
    return cv

compose([fig_problem()],
        title="SM-2004-2 題目附圖重繪",
        sub="依題目正本判讀清單；紅＝正應力（壓，指向面內）、藍＝剪應力（兩斜面都指向頂點）",
        note="攔錯用：兩斜面的剪應力都沿斜面指向頂點（對單元的旋轉方向相反），正負號不可取成相同。",
        path=os.path.join(OUT, "SM-2004-2-fig-1-problem.svg"))


# ══════ fig-2：Mohr 圓（解題圖解，2026-11-15 階段 E）══════
# ── 由 SM-2004-2 §4 Step 1–5 解得（壓為正；剪應力使單元逆時針轉為正）──
PA = (SN_L, -ST_L)                       # 左斜面 (2, −2)：剪應力對單元順時針
PB = (SN_R, +ST_R)                       # 右斜面 (5, +3)
CC = ((PA[0]**2 + PA[1]**2) - (PB[0]**2 + PB[1]**2)) / (2 * (PA[0] - PB[0]))   # 13/3
RR = math.hypot(PA[0] - CC, PA[1])                                              # 3.073
S1, S3 = CC + RR, CC - RR

def fig_mohr():
    W, H = 900, 620
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-0.8, 9.6), (-4.2, 4.4), 60, 60, 30, 40))
    cv.line((-0.5, 0), (9.0, 0), C["muted"], 1.8); cv.line((0, -3.9), (0, 3.9), C["muted"], 1.8)
    cv.text((9.1, 0), "σ（kPa，壓為正）", 12.5, C["text"], anchor="start")
    cv.text((0.15, 4.1), "τ（逆時針為正）", 12.5, C["text"], anchor="start")
    for v in range(1, 9):
        cv.line((v, -0.08), (v, 0.08), C["muted"], 1.2); cv.text((v, -0.35), "%d" % v, 11.5, C["muted"])
    cv.circle((CC, 0), RR, stroke=C["bmd"], w=2.6)
    cv.dot((CC, 0), 4.5, fill=C["bmd"])
    cv.line((CC, 0), PA, C["member2"], 1.3, dash="4 3"); cv.line((CC, 0), PB, C["member2"], 1.3, dash="4 3")
    for p, lab, anc, dx in ((PA, "左斜面 (2, −2)", "end", -0.25), (PB, "右斜面 (5, +3)", "start", 0.25)):
        cv.dot(p, 6, fill=C["load"]); cv.text((p[0] + dx, p[1]), lab, 12.5, C["load"], anchor=anc, weight="700")
    cv.dot((S3, 0), 6, fill=C["deform"]); cv.dot((S1, 0), 6, fill=C["deform"])
    tag_px(cv, cv.X(S3) - 8, cv.Y(0) - 26, "σ3 = %.2f＝水平面（τh = 0）" % S3, 12, C["deform"], anchor="end")
    tag_px(cv, cv.X(S1) + 8, cv.Y(0) - 26, "σ1 = %.2f（鉛直面）" % S1, 12, C["deform"], anchor="start")
    cv.dot((CC, RR), 5, fill=C["accent"]); cv.dot((CC, -RR), 5, fill=C["accent"])
    tag_px(cv, cv.X(CC) + 10, cv.Y(RR) - 14, "τmax = +%.2f：面與水平 −45°（135°）" % RR, 12, C["accent"], anchor="start")
    tag_px(cv, cv.X(CC) + 10, cv.Y(-RR) + 14, "τmin = −%.2f：面與水平 +45°" % RR, 12, C["accent"], anchor="start")
    cv.text((CC + 0.12, -0.75), "C = %.3f" % CC, 11.5, C["bmd"], anchor="start")
    cv.text((CC - RR / 2 - 0.2, 0.5), "R = %.3f" % RR, 11.5, C["bmd"])
    return cv

compose([fig_mohr()],
        title="圖 2　Mohr 圓：兩斜面的點一上一下，圓心在 σ 軸上",
        sub="左斜面剪應力對單元順時針（取 −2）、右斜面逆時針（+3）；水平面落在最左端 σ3，τh ≈ 0",
        note="攔錯用：兩面剪應力若取同號，圓心與半徑全錯；τmax／τmin 面的方向隨剪應力正負約定互換，作答須寫明約定。",
        path=os.path.join(OUT, "SM-2004-2-fig-2-mohr.svg"))
