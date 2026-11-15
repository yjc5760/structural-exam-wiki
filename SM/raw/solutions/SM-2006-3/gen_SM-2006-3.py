# -*- coding: utf-8 -*-
"""SM-2006-3 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2006-3-problem.md §4 判讀清單（#2–#11），不含任何解題結果。
用法：python gen_SM-2006-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單（高程以黏土層頂為 0）──────────
L_SLOPE = 20.0     # #2 坡趾→坡肩水平距
Z_ORIG  = 12.0     # #3 原地表面高於黏土層頂
Z_EXC   = 2.0      # #4 開挖面高於黏土層頂
H_SLOPE = Z_ORIG - Z_EXC   # #5 坡高 10 m（1：2）
T_CLAY  = 0.10     # #7 黏土薄層厚約 10 cm（圖上放大示意）
X_TOE   = 0.0
X_CREST = X_TOE + L_SLOPE

def fig_problem():
    W, H = 980, 430
    XL, XR = -14.0, 34.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 3.0, XR + 9.0), (-6.0, Z_ORIG + 4.0), 30, 30, 40, 40))
    TB = 0.45                                   # 黏土帶繪圖厚度（示意，實際 10 cm）
    ground = [(XL, Z_EXC), (X_TOE, Z_EXC), (X_CREST, Z_ORIG), (XR, Z_ORIG)]
    cv.polygon(ground + [(XR, 0), (XL, 0)], "rgba(180,83,9,0.13)")
    cv.polygon([(XL, -TB), (XR, -TB), (XR, -5.0), (XL, -5.0)], "rgba(180,83,9,0.13)")
    cv.polygon([(XL, 0), (XR, 0), (XR, -TB), (XL, -TB)], "rgba(63,74,90,0.45)", C["member"], 1.2)
    hatch_band(cv, XL, XR, 0, -TB, C["member"], n=120, w=0.8, op=0.6)
    cv.poly(ground, C["member"], 2.6)
    # 常時水位：黏土層頂（#8）
    wt(cv, -4.0, 0.0, 0.35)
    cv.text_px(cv.X(-5.2), cv.Y(0.9), "GWL（常時）", 12.5, C["deform"], anchor="end", weight="700")
    # 文字
    cv.text_px(cv.X(-8.0), cv.Y(Z_EXC + 1.2), "開挖面", 13, C["text"], weight="700")
    cv.text_px(cv.X(27.0), cv.Y(Z_ORIG + 1.2), "原地表面", 13, C["text"], weight="700")
    cv.text_px(cv.X(14.5), cv.Y(6.2), "砂質土層", 13, C["text"], weight="700", anchor="start")
    cv.text_px(cv.X(14.5), cv.Y(4.7), "γ = 20 kN/m³（常時、飽和同）", 12, C["text"], anchor="start")
    cv.text_px(cv.X(14.5), cv.Y(3.3), "c' = 10 kN/m²，φ' = 30°", 12, C["text"], anchor="start")
    cv.text_px(cv.X(-6.0), cv.Y(-2.4), "砂質土層  γ = 20 kN/m³，c' = 10 kN/m²，φ' = 30°", 12, C["text"], anchor="start")
    cv.text_px(cv.X(XR) + 6, cv.Y(-TB / 2), "軟弱黏土薄層（厚約 10 cm）", 12, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(XR) + 6, cv.Y(-TB / 2) + 20, "s_{u} = 12 kN/m^{2}", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(5.0), cv.Y(Z_EXC + 5.6), "V：H = 1：2", 12.5, C["muted"])
    # 尺寸線
    cv.dim((X_TOE, Z_ORIG + 2.2), (X_CREST, Z_ORIG + 2.2), "20 m", 0, C["dim"], 12.5, label_off=-14)
    for x in (X_TOE, X_CREST):
        cv.line((x, Z_ORIG + 2.6), (x, Z_EXC if x == X_TOE else Z_ORIG), C["dim"], 0.9, dash="2 3")
    xd = XR - 2.0
    cv.dim((xd, 0), (xd, Z_ORIG), "12 m", 0, C["dim"], 12.5, label_off=22)
    xd2 = XL + 2.0
    cv.dim((xd2, 0), (xd2, Z_EXC), "2 m", 0, C["dim"], 12.5, label_off=-16)
    return cv

compose([fig_problem()],
        title="SM-2006-3 題目附圖重繪",
        sub="依題目正本判讀清單；坡高 10 m、坡趾到坡肩水平 20 m，黏土薄層在開挖面下 2 m（圖上加厚示意）",
        note="攔錯用：12 m 量到黏土層頂（不是坡高）；坡高 = 12 − 2 = 10 m；常時水位在黏土層頂。",
        path=os.path.join(OUT, "SM-2006-3-fig-1-problem.svg"))


# ═══ fig-2-blocks：解題圖解（階段 E，2026-11-15）══════════════════════
# 數值取自解析 §4 Step 1–3（盲解一致，2026-11-15）。滑動塊體：坡肩後鉛直面（主動，H1 = 12 m）、
# 坡趾鉛直面（被動，H2 = 2 m）、底面沿黏土層 L = 20 m。
H1, H2, LB = Z_ORIG, Z_EXC, L_SLOPE
CASES = [
    dict(tag="㈠ 常時（水位在黏土層頂）", zc=1.732, sa=68.453, pp0=34.641, pp1=154.641,
         Pa=351.44, Pp=189.28, PwA=0.0, PwP=0.0, T=240.0, FS=1.22),
    dict(tag="㈡ 豪雨（水位與地表輪廓重合）", zc=3.40, sa=29.217, pp0=34.641, pp1=95.781,
         Pa=125.63, Pp=130.42, PwA=706.32, PwP=19.62, T=240.0, FS=0.47),
]
GW = 9.81
def fig_block(cs):
    W, H = 640, 400
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-11.0, 35.0), (-4.0, 14.5), 20, 20, 70, 85))
    cv.panel(cs["tag"])
    ground = [(-9.0, H2), (0, H2), (LB, H1), (33.0, H1)]
    cv.polygon([(0, 0), (0, H2), (LB, H1), (LB, 0)], "rgba(180,83,9,0.16)")
    cv.poly(ground, C["member"], 2.4)
    cv.line((-9.0, 0), (33.0, 0), C["member"], 3.2)
    cv.line((0, 0), (0, H2), C["member"], 1.6, dash="5 4")
    cv.line((LB, 0), (LB, H1), C["member"], 1.6, dash="5 4")
    cv.text_px(cv.X(32.8), cv.Y(0) + 34, "黏土薄層 s_{u} = 12 kPa", 11, C["text"], anchor="end")
    if cs["PwA"] > 0:
        cv.poly([(-9.0, H2 + 0.15), (0, H2 + 0.15), (LB, H1 + 0.15), (33.0, H1 + 0.15)], C["deform"], 2.0, dash="7 4")
    # 主動土壓分布（右面，向左）：0 於 zc，sa 於底
    k = 6.0 / 160.0          # 繪圖比例：kPa → m
    zc_y = H1 - cs["zc"]
    cv.polygon([(LB, zc_y), (LB, 0), (LB + cs["sa"] * k, 0)], "rgba(192,57,43,0.18)", C["load"], 1.2)
    cv.text_px(cv.X(LB + cs["sa"] * k) + 4, cv.Y(0) + 12, "%.1f kPa" % cs["sa"], 10.5, C["load"], anchor="start")
    cv.text_px(cv.X(LB) + 6, cv.Y(zc_y), "z_{c} = %.2f m" % cs["zc"], 10.5, C["load"], anchor="start")
    # 被動分布（左面，向右）
    cv.polygon([(0, H2), (0, 0), (-cs["pp1"] * k, 0), (-cs["pp0"] * k, H2)], "rgba(46,125,111,0.18)", C["bmd"], 1.2)
    # 力箭頭
    ya = (H1 - cs["zc"]) / 3
    cv.arrow((LB + 7.5, ya + 1.2), (LB + 0.3, ya + 1.2), C["load"], 3.0)
    cv.text_px(cv.X(LB + 7.6), cv.Y(ya + 1.2) - 13, "P_{a}' = %.1f" % cs["Pa"] if cs["PwA"] else "P_{a} = %.1f" % cs["Pa"], 11.5, C["load"], anchor="end", weight="700")
    cv.arrow((-7.5, H2 / 2 + 2.6), (-0.3, H2 / 2 + 2.6), C["bmd"], 3.0)
    cv.text_px(cv.X(-7.6), cv.Y(H2 / 2 + 2.6) - 13, "P_{p}' = %.1f" % cs["Pp"] if cs["PwA"] else "P_{p} = %.1f" % cs["Pp"], 11.5, C["bmd"], anchor="start", weight="700")
    cv.arrow((LB * 0.30, -1.2), (LB * 0.70, -1.2), C["bmd"], 3.0)
    cv.text_px(cv.X(LB * 0.50), cv.Y(-1.2) + 17, "T = s_{u}L = %.0f（水位不影響）" % cs["T"], 11.5, C["bmd"], weight="700")
    if cs["PwA"] > 0:
        cv.polygon([(LB, H1), (LB, 0), (LB + GW * H1 * k, 0)], "rgba(29,78,216,0.10)", C["deform"], 1.0)
        cv.arrow((LB + 9.5, H1 / 3 + 3.6), (LB + 0.3, H1 / 3 + 3.6), C["deform"], 3.0)
        cv.text_px(cv.X(LB + 9.6), cv.Y(H1 / 3 + 3.6) - 13, "P_{wA} = %.1f" % cs["PwA"], 11.5, C["deform"], anchor="end", weight="700")
        cv.arrow((-7.5, -0.6), (-0.3, -0.6), C["deform"], 2.4)
        cv.text_px(cv.X(-7.6), cv.Y(-0.9) + 16, "P_{wP} = %.1f" % cs["PwP"], 11, C["deform"], anchor="start", weight="700")
        num = "%.1f + %.1f + %.1f" % (cs["T"], cs["Pp"], cs["PwP"]); den = "%.1f + %.1f" % (cs["Pa"], cs["PwA"])
    else:
        num = "%.1f + %.1f" % (cs["T"], cs["Pp"]); den = "%.1f" % cs["Pa"]
    cv.text_px(W / 2, H - 42, "FS = (%s) / (%s) = %.2f" % (num, den, cs["FS"]), 13, C["text"], weight="700")
    cv.text_px(W / 2, H - 20, "單位 kN/m；主動側張力區不計", 11, C["muted"])
    return cv

compose([fig_block(c_) for c_ in CASES],
        title="SM-2006-3 沿黏土薄層側向滑動：三塊體法自由體",
        sub="坡肩後鉛直面主動土壓（H1 = 12 m）、坡趾鉛直面被動土壓（H2 = 2 m）、底面不排水強度 su·L",
        note="攔錯用：豪雨時 su 不變（不可改用有效應力）；張力裂縫積水，坡肩後靜水推力 ½γw·12² = 706 kN/m 佔驅動力八成以上。",
        path=os.path.join(OUT, "SM-2006-3-fig-2-blocks.svg"))
