# -*- coding: utf-8 -*-
"""SM-2025-1 圖解。所有數值取自 SM-2025-1.md §4。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *

OUT = "/tmp/sd/out/SM-2025-1"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2025-1 §4 解得 ────────────────────────────────
H_LAB     = 2.54                                     # cm（25.4 mm）
HDR_LAB   = H_LAB / 2                                # 1.27 cm，雙面排水
T_LAB     = 3.0                                      # min
TV50      = math.pi / 4 * 0.50 ** 2                  # 0.19635
CV        = TV50 * HDR_LAB ** 2 / T_LAB              # 0.105564 cm²/min
H_FIELD   = 1000.0                                   # cm（10 m）
HDR_FIELD = H_FIELD                                  # 單面排水
TV90      = -0.933 * math.log10(1 - 0.90) - 0.085    # 0.848
TV45      = math.pi / 4 * 0.45 ** 2                  # 0.159043
T90       = TV90 * HDR_FIELD ** 2 / CV
T45       = TV45 * HDR_FIELD ** 2 / CV
T90_WRONG = TV90 * (HDR_FIELD / 2) ** 2 / CV         # 誤取雙面排水
TV90_WRONGBRANCH = math.pi / 4 * 0.9 ** 2            # 誤用 U≤0.6 那條式子
YR        = 60 * 24 * 365
RATIO     = (HDR_FIELD / HDR_LAB) ** 2

PW, PH = 580, 440
XA, XB, YB, YT = 0.05, 0.60, 0.20, 0.74
YM = (YB + YT) / 2


def _box(cv):
    soil_fill(cv, XA, XB, YB, YT, "rgba(63,74,90,0.10)")
    cv.polygon([(XA, YB), (XB, YB), (XB, YT), (XA, YT)], "none", C["member"], 2.4)


def panel_lab():
    cv = Canvas(PW, PH, **fit(PW, PH, (0, 1), (0, 1), 125, 155, 96, 78))
    cv.panel("實驗室試體：可雙向排水", "H = 25.4 mm，t = 3 min 達 U = 50%")
    _box(cv)
    for y in (YT, YB):
        cv.line((XA, y), (XB, y), C["deform"], 4.6)
    cv.text_px(cv.X((XA + XB) / 2), cv.Y(YT) - 16, "透水石", 12.5, C["deform"])
    cv.text_px(cv.X((XA + XB) / 2), cv.Y(YB) + 18, "透水石", 12.5, C["deform"])
    for x in (0.17, 0.325, 0.48):
        cv.arrow((x, YM + 0.03), (x, YT + 0.05), C["deform"], 2.4, 8)
        cv.arrow((x, YM - 0.03), (x, YB - 0.05), C["deform"], 2.4, 8)
    cv.line((XA, YM), (XB, YM), C["accent"], 2.0, dash="7 5")
    cv.text_px(cv.X((XA + XB) / 2), cv.Y(YM) - 13, "不排水中央面", 11.5, C["accent"])
    cv.dim((XA - 0.13, YB), (XA - 0.13, YT), "H = 25.4 mm", 0, C["dim"], 13.5, label_off=-44)
    cv.dim((XB + 0.10, YM), (XB + 0.10, YT), "H_{dr} = 12.7 mm", 0, C["accent"], 14, label_off=74)
    cv.text_px(PW / 2, PH - 48, "水往上下兩邊跑，只需走一半層厚", 13.5, C["text"])
    cv.math_px(PW / 2, PH - 26, "H_{dr} = H/2 = 1.27 cm", 14, C["muted"])
    return cv


def panel_field():
    cv = Canvas(PW, PH, **fit(PW, PH, (0, 1), (0, 1), 125, 155, 96, 78))
    cv.panel("現場黏土層：僅可單向排水", "H = 10 m，題問 U = 90% 與 U = 45%")
    _box(cv)
    cv.line((XA, YT), (XB, YT), C["deform"], 4.6)
    cv.text_px(cv.X((XA + XB) / 2), cv.Y(YT) - 16, "透水層（唯一排水面）", 12.5, C["deform"])
    hatch_band(cv, XA, XB, YB - 0.05, YB, C["member2"], 18, 1.3)
    cv.line((XA, YB), (XB, YB), C["member"], 3.6)
    cv.text_px(cv.X((XA + XB) / 2), cv.Y(YB) + 36, "不透水底：水出不去", 12.5, C["muted"])
    for x in (0.17, 0.325, 0.48):
        cv.arrow((x, YB + 0.055), (x, YT + 0.05), C["deform"], 2.4, 8)
    cv.dim((XA - 0.13, YB), (XA - 0.13, YT), "H = 10 m", 0, C["dim"], 13.5, label_off=-44)
    cv.dim((XB + 0.10, YB), (XB + 0.10, YT), "H_{dr} = 10 m", 0, C["accent"], 14, label_off=70)
    cv.text_px(PW / 2, PH - 48, "水只能往上跑，整層厚度都要走", 13.5, C["text"])
    cv.math_px(PW / 2, PH - 26, "H_{dr} = H = 1000 cm", 14, C["muted"])
    return cv


compose([panel_lab(), panel_field()],
        title="圖 1　排水路徑 H_dr 怎麼判：兩邊都通取一半，只通一邊取全厚",
        sub="時間與 H_dr 的平方成正比，故 (1000 / 1.27) 的平方 ≈ 62 萬倍",
        note="攔錯用：若把現場也當成雙面排水（H_dr = 5 m），t90 只剩 %.2f 年；"
             "正解為 %.2f 年，整整差 4 倍。" % (T90_WRONG / YR, T90 / YR),
        path=OUT + "/SM-2025-1-fig-1-drainage-path.svg")

# ══════ fig-2：U–Tv 兩段參考公式 ══════
W, H = 960, 620
cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1), (0, 1), 168, 132, 84, 176))
MX = lambda tv: tv
MY = lambda u: u / 100.0

xt = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
yt = [0, 20, 40, 60, 80, 100]
for t in xt: cv.line((MX(t), 0), (MX(t), 1), C["border"], 1.1)
for t in yt: cv.line((0, MY(t)), (1, MY(t)), C["border"], 1.1)
cv.line((0, 0), (1, 0), C["muted"], 1.9)
cv.line((0, 0), (0, 1), C["muted"], 1.9)
for t in xt: cv.text_px(cv.X(t), cv.Y(0) + 19, "%g" % t, 12.5, C["muted"])
for t in yt: cv.text_px(cv.X(0) - 11, cv.Y(MY(t)), "%g" % t, 12.5, C["muted"], anchor="end")
cv.math_px((cv.X(0) + cv.X(1)) / 2, cv.Y(0) + 48, "T_{v} = c_{v} t / H_{dr}^{2}", 15, C["text"])
cv.text_px(cv.X(0) - 78, (cv.Y(0) + cv.Y(1)) / 2, "平均壓密度 U（%）", 13.5, C["text"])

N = 300
seg1 = [(math.pi / 4 * (u / 100) ** 2, u) for u in [i * 60.0 / N for i in range(N + 1)]]
seg2 = [(-0.933 * math.log10(1 - u / 100) - 0.085, u)
        for u in [60 + i * 39.5 / N for i in range(N + 1)]]
cv.poly([(MX(t), MY(u)) for t, u in seg1 if t <= 1.0], C["bmd"], 3.6)
cv.poly([(MX(t), MY(u)) for t, u in seg2 if t <= 1.0], C["sfd"], 3.6)

TV60 = math.pi / 4 * 0.6 ** 2
cv.line((MX(TV60), 0), (MX(TV60), MY(60)), C["accent"], 2.0, dash="6 5")
cv.line((0, MY(60)), (MX(TV60), MY(60)), C["accent"], 2.0, dash="6 5")
cv.text_px(cv.X(MX(TV60)) - 10, cv.Y(MY(68)), "U = 60% 換式分界", 13, C["accent"],
           anchor="end", weight="700")

# 三個工作點：標籤一律拉到不與曲線／虛線相交的空白區，並以細引線連回點
for tv, u, lab, col, lx, ly, ax in [
        (TV45, 45, "本題(二)  U = 45% → T_v = 0.159", C["bmd"], 0.315, 40, "start"),
        (TV50, 50, "實驗室    U = 50% → T_v = 0.196", C["bmd"], 0.315, 52, "start"),
        (TV90, 90, "本題(一)  U = 90% → T_v = 0.848", C["sfd"], 0.830, 96, "end")]:
    cv.line((MX(tv), 0), (MX(tv), MY(u)), col, 1.4, dash="3 4")
    cv.line((MX(tv), MY(u)), (MX(lx), MY(ly)), col, 1.1, dash="2 3")
    cv.dot((MX(tv), MY(u)), 6.4, fill="#FFFFFF", stroke=col, w=3.0)
    cv.text_px(cv.X(MX(lx)) + (8 if ax == "start" else -8), cv.Y(MY(ly)),
               lab, 13, col, anchor=ax, weight="700")

cv.text_px(W / 2, 32, "圖 2　考卷給的兩條參考公式，各自負責哪一段", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 56, "縱軸 U 向上遞增（考卷圖為倒置座標，此處採一般數學慣例）", 12.5, C["muted"])
cv.text_px(W / 2, H - 100, "T_v = π/4 · U²                 （U ≤ 60%）", 14.5,
           C["bmd"], weight="700")
cv.text_px(W / 2, H - 74, "T_v = −0.933 · log(1−U) − 0.085   （U > 60%）", 14.5,
           C["sfd"], weight="700")
cv.text_px(W / 2, H - 50, "兩式皆由考卷提供，不必自己背；要自己判的是 H_{dr}", 12.5, C["muted"])
cv.text_px(W / 2, H - 26,
           "攔錯用：三個工作點分屬兩段。若一律用 π/4·U² 去算 U = 90%，"
           "得 T_v = {:.3f} 而非 {:.3f}，t90 會少估 25%。".format(TV90_WRONGBRANCH, TV90),
           13, C["muted"])
cv.save(OUT + "/SM-2025-1-fig-2-u-tv-branches.svg")

print("cv=%.6f  t90=%.0f min (%.1f d, %.2f yr)  t45=%.0f min (%.1f d, %.2f yr)"
      % (CV, T90, T90 / 1440, T90 / YR, T45, T45 / 1440, T45 / YR))
print("Hdr ratio^2 = %.3e ; t90_wrong=%.2f yr ; Tv90 wrong branch=%.4f"
      % (RATIO, T90_WRONG / YR, TV90_WRONGBRANCH))
