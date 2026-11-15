# -*- coding: utf-8 -*-
"""SM-2020-2 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2020-2-problem.md §4 判讀清單，不含任何解題結果。
用法：python gen_SM-2020-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
SAND, SAND2, CLAY = "rgba(180,83,9,0.12)", "rgba(180,83,9,0.24)", "rgba(63,74,90,0.20)"


def ground(cv, x0, x1, y, n=4, s=0.35):
    """地面剖線（短斜線）。"""
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        cv.line((x, y), (x - s, y - s), C["member"], 1.3)


def wall(cv, x, y0, y1, t=0.18, fill="#3F4A5A"):
    cv.polygon([(x - t / 2, y0), (x + t / 2, y0), (x + t / 2, y1), (x - t / 2, y1)], fill)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
Z_WT  = 0.5    # 背側地下水位
H_EXC = 4.0    # 開挖深度＝Sand 1 / Sand 2 層界（開挖側水位同高）
L_PL  = 10.0   # 懸臂版樁長，底端 O


def fig_problem():
    Wd, Ht = 820, 680
    XL, XR = -4.0, 7.0
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 0.3, XR + 1.4), (-(L_PL + 1.0), 0.8), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, 0, XR, Y(Z_WT), Y(0), SAND)
    soil_fill(cv, 0, XR, Y(H_EXC), Y(Z_WT), SAND2)
    soil_fill(cv, XL, XR, Y(L_PL + 0.6), Y(H_EXC), "rgba(180,83,9,0.34)")
    cv.line((0, Y(0)), (XR, Y(0)), C["member"], 2.4)
    cv.line((0, Y(Z_WT)), (XR, Y(Z_WT)), C["deform"], 1.4, dash="7 4")
    wt_symbol(cv, 3.0, Y(Z_WT), C["deform"], 0.1)
    cv.line((XL, Y(H_EXC)), (XR, Y(H_EXC)), C["member"], 2.0)
    wt_symbol(cv, -2.4, Y(H_EXC), C["deform"], 0.1)
    wall(cv, 0, Y(0), Y(L_PL), 0.22)
    cv.text_px(cv.X(0), cv.Y(Y(L_PL)) + 18, "O", 15, C["text"], weight="700")
    cv.text_px(cv.X(3.0), cv.Y(Y(1.4)), "Sand 1", 14, C["text"], anchor="start", weight="700")
    for i, s in enumerate(["γ = 16.0 kN/m^{3}", "γ_{sat} = 18.8 kN/m^{3}", "φ' = 26°"]):
        cv.math_px(cv.X(3.0), cv.Y(Y(2.0 + 0.6 * i)), s, 13.5, C["text"], anchor="start")
    cv.text_px(cv.X(3.0), cv.Y(Y(6.6)), "Sand 2", 14, C["text"], anchor="start", weight="700")
    for i, s in enumerate(["γ_{sat} = 19.6 kN/m^{3}", "φ' = 30°"]):
        cv.math_px(cv.X(3.0), cv.Y(Y(7.2 + 0.6 * i)), s, 13.5, C["text"], anchor="start")
    cv.text_px(cv.X(-2.0), cv.Y(Y(2.2)), "開挖側", 13, C["muted"])
    xd = 1.2
    cv.dim((xd, Y(Z_WT)), (xd, Y(0)), "0.5 m", 0, C["dim"], 12, label_off=26)
    cv.dim((xd, Y(H_EXC)), (xd, Y(Z_WT)), "3.5 m", 0, C["dim"], 12.5, label_off=26)
    cv.dim((xd, Y(L_PL)), (xd, Y(H_EXC)), "6.0 m", 0, C["dim"], 12.5, label_off=26)
    cv.line((0.15, Y(L_PL)), (xd + 0.2, Y(L_PL)), C["dim"], 0.9, dash="2 3")
    return cv


compose([fig_problem()],
        title="SM-2020-2 題目附圖重繪",
        sub="依題目正本判讀清單；懸臂版樁長 10 m，兩側水位差 3.5 m",
        note="攔錯用：0.5 m 是地表到背側水位、開挖面在 4 m（＝兩砂層界面），坑內水位在開挖面；版樁底 O 在開挖面下 6 m。",
        path=os.path.join(OUT, "SM-2020-2-fig-1-problem.svg"))


# ══════ fig-2-pressure：解題圖解（2026-11-15 補解題圖解；數值依 SM-2020-2.md §4 重算）══════
# 簡化滲流：i = ΔH/(H_wA + 2D)，主動側 γ' + iγw、被動側 γ' − iγw；淨水壓在開挖面最大、O 點為 0。
GW = 9.81
DH, D = 3.5, 6.0
I = DH / (DH + 2 * D)                              # 0.2258
KA1 = round(math.tan(math.radians(45 - 13)) ** 2, 3)  # φ 26°，0.390（與 §4 同取三位）
KA2, KP2 = 1 / 3, 3.0
GA1 = 18.8 - GW + I * GW; GA2 = 19.6 - GW + I * GW; GP2 = 19.6 - GW - I * GW
s05 = 16.0 * 0.5; s4 = s05 + 3.5 * GA1; s10 = s4 + 6.0 * GA2
PA = [(0, 0), (0.5, KA1 * s05), (4.0, KA1 * s4), (4.0, KA2 * s4), (10.0, KA2 * s10)]
PP10 = KP2 * 6.0 * GP2
UN4 = GW * 3.5 * (1 - I)
# 對 O 點力矩（解析：分段梯形）
def mom(pts):
    F = M = 0.0
    for (z0, p0), (z1, p1) in zip(pts[:-1], pts[1:]):
        h = z1 - z0
        if h <= 0: continue
        f = (p0 + p1) / 2 * h
        zc = z0 + h * (p0 + 2 * p1) / (3 * (p0 + p1)) if p0 + p1 else z0
        F += f; M += f * (10 - zc)
    return F, M
MO = mom(PA)[1] + mom([(0.5, 0), (4.0, UN4), (10.0, 0)])[1]
MR = mom([(4.0, 0), (10.0, PP10)])[1]
FSW = MR / MO


def fig_pressure():
    W2, H2 = 640, 700
    out = []
    for kind in ("earth", "water"):
        sx = 50.0
        cv = Canvas(W2, H2, sx=sx, ox=(300 if kind == "earth" else 400), oy=80, bg=C["panel"])
        Yz = lambda z: 10.4 - z
        if kind == "earth":
            cv.panel("(a) 土壓力圖（有效應力 × K）", sub="主動畫在牆左、被動畫在牆右；水壓另畫")
            S = 3.6 / PP10 * 1.0        # kPa → m（被動 136 kPa 約 3.6 m）
            S = 3.8 / 136.35
            cv.polygon([(-p * S * 4, Yz(z)) for z, p in PA] + [(0, Yz(10)), (0, Yz(0))],
                       "rgba(220,38,38,0.20)", C["load"], 2.2)
            cv.polygon([(0, Yz(4)), (PP10 * S, Yz(10)), (0, Yz(10))], "rgba(37,99,235,0.18)", C["deform"], 2.2)
            for z, p, dy in ((0.5, PA[1][1], -2), (4.0, PA[2][1], -8), (4.0, PA[3][1], 14), (10.0, PA[4][1], 4)):
                cv.text_px(cv.X(-p * S * 4) - 6, cv.Y(Yz(z)) + dy, "%.2f" % p, 11.5, C["load"], anchor="end", weight="700")
            cv.text_px(cv.X(PP10 * S) + 6, cv.Y(Yz(10)) + 4, "%.2f" % PP10, 11.5, C["deform"], anchor="start", weight="700")
            cv.text_px(cv.X(-1.9), cv.Y(Yz(2.2)), "主動（×4 放大）", 12, C["load"], anchor="middle", weight="700")
            cv.text_px(cv.X(1.3), cv.Y(Yz(8.4)), "被動", 12, C["deform"], anchor="middle", weight="700")
            cv.text_px(cv.X(1.3), cv.Y(Yz(8.4)) + 17, "γ' − iγw = %.3f" % GP2, 11, C["muted"], anchor="middle")
        else:
            cv.panel("(b) 淨水壓力圖（u_A − u_P）", sub="沿壁線性水頭損失：開挖面最大、版樁底 O 為 0")
            S = 3.2 / UN4
            cv.polygon([(0, Yz(0.5)), (-UN4 * S, Yz(4)), (0, Yz(10))], "rgba(14,116,144,0.20)", C["deform"], 2.2)
            cv.text_px(cv.X(-UN4 * S) - 6, cv.Y(Yz(4)) + 4, "%.2f kPa" % UN4, 12, C["deform"], anchor="end", weight="700")
            cv.text_px(cv.X(-2.5), cv.Y(Yz(8.7)), "i = ΔH/(H_w + 2D)", 11.5, C["muted"], anchor="middle")
            cv.text_px(cv.X(-2.5), cv.Y(Yz(8.7)) + 17, "= 3.5/15.5 = %.4f" % I, 11.5, C["muted"], anchor="middle")
        # 牆、地面、水位
        cv.line((0, Yz(0)), (0, Yz(10)), C["member"], 4.5)
        cv.line((-4.4, Yz(0)), (0, Yz(0)), C["member"], 1.4)
        cv.line((0, Yz(4)), (4.4 if kind == "earth" else 1.8, Yz(4)), C["member"], 1.4)
        cv.line((-4.4, Yz(0.5)), (0, Yz(0.5)), C["deform"], 1.2, dash="6 4")
        cv.text_px(cv.X(-4.3), cv.Y(Yz(0.5)) - 6, "背側水位 0.5 m", 10.5, C["deform"], anchor="start")
        cv.text_px(cv.X(0.2), cv.Y(Yz(4)) - 6, "開挖面＝坑內水位 4 m", 10.5, C["muted"], anchor="start")
        cv.dot((0, Yz(10)), 5, fill=C["member"])
        cv.text_px(cv.X(0) + 8, cv.Y(Yz(10)) + 18, "O（z = 10 m）", 11.5, C["member"], anchor="start", weight="700")
        out.append(cv)
    return out


compose(fig_pressure(),
        title="SM-2020-2　土壓力與淨水壓力分開畫 → 對 O 點取矩",
        sub="傾覆力矩 ≈ %.0f、抵抗力矩 ≈ %.0f kN·m/m ⇒ FS = %.2f（淨水壓計入傾覆力矩）" % (MO, MR, FSW),
        note="土壓用有效應力乘 K，水壓全額另畫；淨水壓佔傾覆力矩約一半，漏掉它 FS 會從 0.60 跳到 1 以上。",
        path=os.path.join(OUT, "SM-2020-2-fig-2-pressure.svg"))
print("i=%.4f pa=%s pp10=%.2f un4=%.2f MO=%.2f MR=%.2f FS=%.3f" % (I, [round(p, 2) for _, p in PA], PP10, UN4, MO, MR, FSW))
