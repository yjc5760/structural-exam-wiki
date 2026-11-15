# -*- coding: utf-8 -*-
"""SM-2018-1 圖解。
fig-1-settlement-time：由 200 天 30% 推得的沉陷—時間曲線，標出 1～4 年沉陷，並對照「全程用 √t 外推」的錯誤。
數值只取自解析 §4 步驟 1–6（U ≤ 60% 拋物線式、U > 60% 對數式，一年 365 天）。
用法：python gen_SM-2018-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目給定與解析 §4 ────────────────────────────────
T0, S0, U0 = 200.0, 234.0, 0.30          # 200 天沉陷 234 mm，U = 30%
S_ULT = S0 / U0                          # 780 mm（步驟 1）
K = math.pi / 4 * U0 ** 2 / T0           # Tv/t（步驟 2）
TV60 = math.pi / 4 * 0.6 ** 2            # 0.2827

def U_of_Tv(Tv):                         # 步驟 3–6 用的兩段近似式
    if Tv <= TV60:
        return math.sqrt(4 * Tv / math.pi)
    return (100 - 10 ** ((1.781 - Tv) / 0.933)) / 100

S = lambda t: S_ULT * U_of_Tv(K * t)
T_60 = TV60 / K                          # U = 60% 的時間（約 800 天）
YEARS = [(365, "1 年"), (730, "2 年"), (1095, "3 年"), (1460, "4 年")]
S_SQRT = lambda t: S0 * math.sqrt(t / T0)  # 錯誤外推：U ∝ √t 用到 U > 60%

def fig():
    W, H = 920, 560
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R, T, B = 100, 210, 30, 470
    TA, TB, SA, SB = 0, 1600, 0, 900
    X = lambda t: L + (t - TA) / (TB - TA) * (W - L - R)
    Y = lambda s: B - (s - SA) / (SB - SA) * (B - T)
    for t in range(0, 1601, 200):
        seg(cv, (X(t), T), (X(t), B), C["border"], 1.0)
        cv.text_px(X(t), B + 18, "%d" % t, 12.5, C["muted"])
    for s in range(0, 901, 100):
        seg(cv, (X(TA), Y(s)), (X(TB), Y(s)), C["border"], 1.0)
        cv.text_px(X(TA) - 9, Y(s), "%d" % s, 12.5, C["muted"], anchor="end")
    seg(cv, (X(TA), B), (X(TB), B), C["muted"], 1.9)
    seg(cv, (X(TA), B), (X(TA), T), C["muted"], 1.9)
    cv.text_px((X(TA) + X(TB)) / 2, B + 44, "時間 t（天）", 13.5, C["text"])
    cv.text_px(X(TA) - 40, T - 14, "沉陷 S（mm）", 13, C["text"])
    # 最終沉陷
    seg(cv, (X(TA), Y(S_ULT)), (X(TB), Y(S_ULT)), C["muted"], 1.5, dash="8 5")
    cv.text_px(X(TB) + 8, Y(S_ULT), "S∞ = %.0f mm" % S_ULT, 12.5, C["muted"], anchor="start", weight="700")
    # U = 60% 分界
    seg(cv, (X(T_60), T + 20), (X(T_60), B), C["accent"], 1.2, dash="3 4")
    cv.text_px(X(T_60) + 6, T + 22, "U = 60%%（t = %.0f 天）" % T_60, 12, C["accent"], anchor="start", weight="700")
    # 錯誤外推
    pts = [(X(t), Y(S_SQRT(t))) for t in [T_60 + (TB - T_60) * j / 80 for j in range(81)] if S_SQRT(t) <= SB]
    curve(cv, pts, C["load"], 2.0, dash="7 5")
    # 正確曲線
    curve(cv, [(X(t), Y(S(t))) for t in [TB * j / 400 for j in range(401)]], C["deform"], 3.0)
    dot(cv, X(T0), Y(S0), 6, C["text"])
    tag_px(cv, X(T0) + 10, Y(S0) + 20, "已知 200 天 234 mm（U = 30%）", 12, C["text"], anchor="start", weight="400")
    for t, lab in YEARS:
        s = S(t)
        dot(cv, X(t), Y(s), 6, C["deform"])
        tag_px(cv, X(t) - 6, Y(s) + (-22 if t < 1000 else 28), "%s %.1f" % (lab, s), 12.5, C["deform"], anchor="middle")
    for t, lab in YEARS[2:]:
        s = S_SQRT(t)
        dot(cv, X(t), Y(s), 4.5, C["load"])
        cv.text_px(X(t) - 8, Y(s) - 14, "錯 %.0f" % s, 11.5, C["load"], anchor="end", weight="700")
    cv.legend(W - R + 18, 300, [(C["deform"], "兩段近似式（本解）"), (C["load"], "錯：U ∝ √t 外推")], size=12)
    return cv

compose([fig()],
        title="圖 1　沉陷—時間曲線：U 超過 60% 後要換對數式",
        sub="S∞ = 234/0.30 = 780 mm；Tv 與 t 成正比（cv、Hdr 不變），U ≤ 60% 時 S ∝ √t",
        note="攔錯用：3、4 年已超過 U = 60%，若續用 S ∝ √t 會高估（紅虛線）；也攔下把 200 天的 234 mm 當成最終沉陷。",
        path=os.path.join(OUT, "SM-2018-1-fig-1-settlement-time.svg"))
print("S_ULT", S_ULT, "T60 %.1f" % T_60, ["%.1f" % S(t) for t, _ in YEARS], ["%.1f" % S_SQRT(t) for t, _ in YEARS])
