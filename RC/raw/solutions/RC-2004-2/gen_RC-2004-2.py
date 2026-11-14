#!/usr/bin/env python3
"""
RC-2004-2 外伸梁 — 題目附圖重繪腳本

用法：python3 gen_RC-2004-2.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2004-2-problem.md §4 判讀清單（已確認）。
只畫考卷給的東西（支承、跨度、均佈載重範圍、D 點），不含任何解題結果。
FIGURES
  fig-1-problem  題目附圖重繪  攔：B 讀成鉸支、D 取全梁中點 5 m、外伸段漏掉載重
  fig-2-vm       剪力／彎矩圖  攔：D 點 Mu 取成無外伸簡支梁 wL²/8＝8wu、或取全梁中點；忽略 B 處負彎矩
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2004-2"

# ── 判讀清單（RC-2004-2-problem.md §4，已確認）──
L_AB, L_BC = 8.0, 2.0      # #4 AB 簡支跨 8 m、BC 外伸 2 m
X_D = L_AB / 2             # #7 D 在 AB 跨中（距 A 4 m）
#                            #1 A 鉸支、#2 B 滾支、#3 C 自由端、#5 W 作用全長 10 m


def fig1_problem():
    W, Hc = 900, 380
    L = L_AB + L_BC
    s = (W - 200) / L
    cv = Canvas(W, Hc, sx=s, ox=100, oy=150)
    cv.panel("梁立面（重繪）", "依題目正本判讀清單 #1–#7")
    cv.line((0, 0), (L, 0), C["member"], 6, cap="butt")
    cv.support((0, 0), "pin", 0, size=16)
    cv.support((L_AB, 0), "roller", 0, size=16)
    cv.udl((0, 0.12), (L, 0.12), 1.1, n=21, color=C["load"], w=1.6)
    cv.text((L / 2, 1.25), "W（自重＋WD 5 t/m＋WL 2 t/m，全長）", 13, C["load"], dy=-14)
    cv.text((0, 0), "A", 17, C["text"], "end", dx=-24, dy=-4, weight="700")
    cv.text((L_AB, 0), "B", 17, C["text"], "start", dx=30, dy=18, weight="700")
    cv.text((L, 0), "C", 17, C["text"], "start", dx=10, dy=-4, weight="700")
    cv.text((X_D, 0), "×", 20, C["accent"], weight="700", dy=-1)
    cv.text((X_D, 0), "D", 16, C["accent"], dy=24, weight="700")
    cv.dim((0, 0), (L_AB, 0), f"{L_AB:.0f} m", off=78, label_off=16)
    cv.dim((L_AB, 0), (L, 0), f"{L_BC:.0f} m", off=78, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（重繪）",
            sub="A 鉸支、B 滾支、C 自由端；均佈載重作用 A 到 C 全長；D 在 AB 跨中",
            note="D 距 A 4 m（AB 跨中），不是全梁 10 m 的中點；外伸段 BC 同樣承受 W",
            path=path)
    return path



# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-13 補繪）：由題給量現算，檔尾對 §4 公佈值 assert
# ══════════════════════════════════════════════════════════
from recipes import plot_function
B_, H_ = 0.40, 0.70                    # 斷面 m（題目正本 §1）
WD, WL = 5.0, 2.0                      # t/m
GAMMA = 2.4                            # t/m³（§4 假設）
WSW = B_ * H_ * GAMMA
WU = 1.4 * (WD + WSW) + 1.7 * WL       # §4 ① 1.4D + 1.7L
L = L_AB + L_BC
RB = WU * L * (L / 2) / L_AB
RA = WU * L - RB


def V(x):
    return RA - WU * x + (RB if x > L_AB else 0.0)


def M(x):
    return RA * x - WU * x * x / 2 + (RB * (x - L_AB) if x > L_AB else 0.0)


X_MAX = RA / WU                        # 剪力為零 → 正彎矩極值
X_INF = 2 * RA / WU                    # 正彎矩段的反曲點


def fig2_vm():
    W, PH = 900, 230
    sx = (W - 220) / L
    pad = 110
    xs = [L * i / 400 for i in range(401)]
    xs = sorted(set(xs + [L_AB - 1e-9, L_AB + 1e-9]))
    top = Canvas(W, PH, sx=sx, ox=pad, oy=PH * 0.34)
    top.panel("載重與支承", f"wu = 1.4(5 + {WSW:.3f}) + 1.7 × 2 = {WU:.2f} t/m（全長 10 m）")
    top.line((0, 0), (L, 0), C["member"], 6, cap="butt")
    top.support((0, 0), "pin"); top.support((L_AB, 0), "roller")
    top.udl((0, 0), (L, 0), 0.085 * L, n=13)
    top.text((0, 0), "A", 14, C["text"], dx=-16, dy=-14, weight="700")
    top.text((L_AB, 0), "B", 14, C["text"], dx=18, dy=-14, weight="700")
    top.text((L, 0), "C", 14, C["text"], dx=14, dy=0, weight="700")
    top.dot((X_D, 0), 5, fill=C["accent"])
    top.text((X_D, 0), "D", 14, C["accent"], dy=24, weight="700")
    top.dim((0, 0), (L_AB, 0), "8 m", off=46, label_off=14)
    top.dim((L_AB, 0), (L, 0), "2 m", off=46, label_off=14)
    top.text_px(24, PH - 22, f"RA = {RA:.1f} t　RB = {RB:.1f} t", 12.5, C["muted"], "start")

    def strip(vals, color, fill, name, unit, keys):
        top_px, bot_px = 74, 36
        vmax, vmin = max(max(vals), 0.0), min(min(vals), 0.0)
        px_per = (PH - top_px - bot_px) / (vmax - vmin)
        cv = Canvas(W, PH, sx=sx, ox=pad, oy=PH - (top_px + vmax * px_per))
        cv.panel(name, None)
        plot_function(cv, xs, vals, px_per / sx, 0.0, 0.0, color, fill, marks=keys)
        cv.text_px(pad - 14, cv.Y(0), "0", 12, C["muted"], "end")
        cv.text_px(W - 22, 32, unit, 12, C["muted"], "end")
        return cv

    mid = strip([V(x) for x in xs], C["sfd"], C["fill_s"], "剪力圖 SFD", "t",
                [(0, f"+{RA:.1f}", -12),
                 (L_AB - 0.01, f"{V(L_AB - 0.01):.1f}", 16), (L_AB + 0.01, f"+{V(L_AB + 0.01):.1f}", -12)])
    Ms = [M(x) for x in xs]
    bot = strip(Ms, C["bmd"], C["fill_m"], "彎矩圖 BMD（正彎矩畫在上方）", "t·m",
                [(X_D, f"M_{{D}} = 7w_{{u}} = {M(X_D):.1f}", -16), 
                 (L_AB + 0.6, f"M_{{B}} = {M(L_AB):.1f}", 18)])
    mid.dot((X_MAX, 0), 4.6, fill=C["accent"])
    mid.math_px(mid.X(X_MAX) - 8, mid.Y(0) + 20, f"V = 0, x = {X_MAX:.2f} m", 12.5, C["accent"], "end", weight="700")
    bot.dot((X_INF, 0), 4.6, fill=C["accent"])
    bot.math_px(bot.X(X_INF) - 8, bot.Y(0) + 20, f"M = 0, x = {X_INF:.1f} m", 12.5, C["accent"], "end", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-vm.svg")
    compose([top, mid, bot], cols=1,
            title=f"{TAG}　外伸段讓 D 點彎矩由 8wu 降為 7wu",
            sub=f"D 在 AB 跨中 x = 4 m：Mu = {M(X_D):.1f} t·m；正彎矩最大在 x = {X_MAX:.2f} m（{M(X_MAX):.2f}，差 0.4%）",
            note=f"不計外伸段時 wL²/8 = {WU*64/8:.1f} t·m（高估 14%）；B 處負彎矩 {M(L_AB):.1f} t·m 需另配上層筋",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "B 讀成鉸支；D 取全梁中點；外伸段漏載重"),
           (fig2_vm, "§4 ②③", "D 點 Mu 取 8wu 或取全梁中點；忽略 B 處負彎矩")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2004-2.md §4 公佈值核對
    assert round(WU, 2) == 11.34 and round(RB, 1) == 70.9 and round(RA, 1) == 42.5
    assert round(M(X_D), 1) == 79.4 and abs(M(X_D) - 7 * WU) < 1e-9
    print("assert OK")
