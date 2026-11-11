# -*- coding: utf-8 -*-
"""SM-2023-1 圖解（名詞解釋題）。
本題未給任何數值，故兩張圖的示範數據為自訂（圖上已明標），
但所有判準（C_u、C_c 的界限、A 線與 U 線公式）皆為 USCS／ASTM D2487 之規範值；
圖上標示的 D_10／D_30／D_{60} 與 C_u／C_c 一律由所繪曲線本身反算，不是手打。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px, seg, curve, dot, hmonotone

OUT = "/tmp/sd/out/SM-2023-1"
os.makedirs(OUT, exist_ok=True)

# ── 自訂示範級配（非考題數據）──────────────────────────
WELL = [(0.05, 2), (0.15, 10), (0.30, 22), (0.45, 30), (0.90, 60),
        (2.0, 84), (5.0, 97), (10.0, 100)]
GAP  = [(0.06, 4), (0.15, 10), (0.25, 13), (0.50, 16), (1.00, 20),
        (1.50, 40), (2.00, 60), (4.00, 90), (8.00, 99), (12.0, 100)]

def sample(ctrl, n=600):
    return hmonotone([(math.log10(d), p) for d, p in ctrl], n)

def d_at(pts, pct):
    """由所繪曲線反查通過百分率 pct 對應的粒徑（線性內插於 log d）。"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 <= pct <= y1:
            t = (pct - y0) / (y1 - y0) if y1 != y0 else 0
            return 10 ** (x0 + t * (x1 - x0))
    return None

SW, GP = sample(WELL), sample(GAP)
D = {}
for nm, pts in (("SW", SW), ("GP", GP)):
    d10, d30, d60 = (d_at(pts, p) for p in (10, 30, 60))
    D[nm] = (d10, d30, d60, d60 / d10, d30 ** 2 / (d10 * d60))

# ══════ fig-1：粒徑分布曲線與 D_{10} / D_{30} / D_{60} 的讀法 ══════
W_, H_ = 1020, 760
ML, MR, MT_, MB = 160, 130, 92, 262
cv = Canvas(W_, H_, bg="#FFFFFF")
XL, XR = math.log10(0.02), math.log10(20.0)
PX = lambda ld: ML + (ld - XL) / (XR - XL) * (W_ - ML - MR)
PY = lambda p: H_ - MB - p / 100.0 * (H_ - MT_ - MB)
for dec in (0.01, 0.1, 1.0, 10.0):
    for k in range(1, 10):
        d = dec * k
        if 0.02 <= d <= 20:
            x = PX(math.log10(d))
            seg(cv, (x, PY(0)), (x, PY(100)), C["border"], 1.0 if k > 1 else 1.6)
            if k == 1 or d in (0.02, 2.0, 20.0):
                cv.text_px(x, PY(0) + 19, ("%g" % d), 12.5, C["muted"])
for p in range(0, 101, 20):
    seg(cv, (PX(XL), PY(p)), (PX(XR), PY(p)), C["border"], 1.1)
    cv.text_px(PX(XL) - 12, PY(p), "%d" % p, 12.5, C["muted"], anchor="end")
seg(cv, (PX(XL), PY(0)), (PX(XR), PY(0)), C["muted"], 1.9)
seg(cv, (PX(XL), PY(0)), (PX(XL), PY(100)), C["muted"], 1.9)
cv.text_px((PX(XL) + PX(XR)) / 2, PY(0) + 44, "粒徑 D（mm，對數刻度，向右變粗）", 13.5, C["text"])
cv.text_px(PX(XL) - 82, (PY(0) + PY(100)) / 2, "通過百分率（%）", 13.5, C["text"])

curve(cv, [(PX(x), PY(y)) for x, y in SW], C["bmd"], 3.4)
curve(cv, [(PX(x), PY(y)) for x, y in GP], C["load"], 3.0, "9 5")
d10, d30, d60, cu, cc = D["SW"]
for pct, dv, lab, dyp in ((10, d10, "D_{10}", -16), (30, d30, "D_{30}", -44),
                          (60, d60, "D_{60}", -72)):
    x = PX(math.log10(dv))
    seg(cv, (PX(XL), PY(pct)), (x, PY(pct)), C["accent"], 1.8, "5 4")
    seg(cv, (x, PY(pct)), (x, PY(0)), C["accent"], 1.8, "5 4")
    dot(cv, x, PY(pct), 6.4, C["accent"])
    tag_px(cv, x, PY(0) + dyp, "{} = {:.3f} mm".format(lab, dv), 12.5, C["accent"])
tag_px(cv, PX(math.log10(0.28)), PY(78), "良好級配（示範）", 13, C["bmd"])
tag_px(cv, PX(math.log10(3.6)), PY(30), "跳躍級配（示範）", 13, C["load"])

cv.text_px(W_ / 2, 32, "圖 1　D_{10} / D_{30} / D_{60} 怎麼讀，C_u 與 C_c 怎麼算", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 58, "⚠ 兩條曲線為自訂示範級配，非考題數據；圖上的 D 值與係數皆由曲線本身反算",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 196,
           "有效粒徑 D_{{10}} = {:.3f} mm　（10% 重量比它細；Hazen：k ≈ c·D_{{10}}²）".format(d10),
           13.5, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 166,
           "均勻係數 C_u = D_{{60}}/D_{{10}} = {:.3f}/{:.3f} = {:.2f}　　"
           "曲率係數 C_c = D_{{30}}²/(D_{{10}}·D_{{60}}) = {:.3f}²/({:.3f}×{:.3f}) = {:.2f}"
           .format(d60, d10, cu, d30, d10, d60, cc), 13.5, C["bmd"], weight="700")
cv.text_px(W_ / 2, H_ - 138,
           "判為 SW（優良級配砂）：砂需 C_u ≥ 6 且 1 ≤ C_c ≤ 3——本例 {:.2f} 與 {:.2f}，兩項皆過。"
           .format(cu, cc), 13, C["bmd"], weight="700")
g10, g30, g60, gcu, gcc = D["GP"]
cv.text_px(W_ / 2, H_ - 108,
           "對照虛線的跳躍級配：C_u = {:.2f}（夠大）但 C_c = {:.2f} 已跳出 1～3，故判為不良級配。"
           .format(gcu, gcc), 13, C["load"], weight="700")
cv.text_px(W_ / 2, H_ - 76,
           "攔錯用：C_u 大只代表「粒徑範圍寬」，不代表級配好；中間有沒有缺料要靠 C_c。",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 50,
           "兩條曲線的 D_{10} 與 C_u 都不小，但虛線在 0.25～1.0 mm 之間幾乎水平（缺料），C_c 就爆掉了。",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 24,
           "另注意：礫石的門檻是 C_u ≥ 4，砂是 C_u ≥ 6；C_c 的 1～3 兩者相同。", 12.5, C["muted"])
cv.save(OUT + "/SM-2023-1-fig-1-gradation.svg")

# ══════ fig-2：Atterberg 界限 ＋ USCS 塑性圖 ══════
SL, PL, LL = 15.0, 22.0, 45.0          # 自訂示範值
PI = LL - PL                            # 23
A_LINE = lambda ll: 0.73 * (ll - 20)    # ASTM D2487
U_LINE = lambda ll: 0.90 * (ll - 8)
W_, H_ = 1040, 860
cv = Canvas(W_, H_, bg="#FFFFFF")
# ── 上半：含水量軸 ──
AY = 190
AX0, AX1 = 150, 890
wmax = 60.0
WX = lambda w: AX0 + w / wmax * (AX1 - AX0)
seg(cv, (AX0, AY), (AX1, AY), C["member"], 3.0)
cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                % (AX1 + 16, AY, AX1, AY - 7, AX1, AY + 7, C["member"]))
cv.text_px(AX1 + 26, AY, "含水量 ω 增加 →", 12.5, C["member"], anchor="start")
BANDS = [(0, SL, "固態", "rgba(63,74,90,0.16)"), (SL, PL, "半固態", "rgba(180,83,9,0.16)"),
         (PL, LL, "塑性狀態", "rgba(29,78,216,0.18)"), (LL, wmax, "液態", "rgba(46,125,111,0.16)")]
for w0, w1, lab, col in BANDS:
    cv.rect_px(WX(w0), AY - 34, WX(w1) - WX(w0), 34, col, 0, "rgba(0,0,0,0.10)", 1)
    cv.text_px((WX(w0) + WX(w1)) / 2, AY - 17, lab, 13, C["text"], weight="700")
for w, lab, col in ((SL, "SL 縮限", C["accent"]), (PL, "PL 塑限", C["deform"]),
                    (LL, "LL 液限", C["bmd"])):
    seg(cv, (WX(w), AY - 40), (WX(w), AY + 16), col, 2.4)
    cv.text_px(WX(w), AY + 32, "%s = %g%%" % (lab, w), 12.5, col, weight="700")
seg(cv, (WX(PL), AY + 56), (WX(LL), AY + 56), C["load"], 2.6)
for xx, dx in ((WX(PL), 1), (WX(LL), -1)):
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (xx, AY + 56, xx + 9 * dx, AY + 51, xx + 9 * dx, AY + 61, C["load"]))
tag_px(cv, (WX(PL) + WX(LL)) / 2, AY + 56, "PI = LL − PL = %g" % PI, 13.5, C["load"])
cv.text_px(W_ / 2, 96, "（一）塑性指數：土壤還「捏得動」的含水量區間有多寬", 15, C["text"], weight="700")

# ── 下半：塑性圖 ──
ML, MR = 170, 150
PT, PB = 330, 212
XLL, XRR = 0.0, 100.0
YLO, YHI = 0.0, 60.0
QX = lambda ll: ML + (ll - XLL) / (XRR - XLL) * (W_ - ML - MR)
QY = lambda pi: H_ - PB - (pi - YLO) / (YHI - YLO) * (H_ - PT - PB)
for ll in range(0, 101, 20):
    seg(cv, (QX(ll), QY(0)), (QX(ll), QY(60)), C["border"], 1.1)
    cv.text_px(QX(ll), QY(0) + 19, str(ll), 12.5, C["muted"])
for pi in range(0, 61, 10):
    seg(cv, (QX(0), QY(pi)), (QX(100), QY(pi)), C["border"], 1.1)
    cv.text_px(QX(0) - 12, QY(pi), str(pi), 12.5, C["muted"], anchor="end")
seg(cv, (QX(0), QY(0)), (QX(100), QY(0)), C["muted"], 1.9)
seg(cv, (QX(0), QY(0)), (QX(0), QY(60)), C["muted"], 1.9)
cv.text_px((QX(0) + QX(100)) / 2, QY(0) + 44, "液限 LL（%）", 13.5, C["text"])
cv.text_px(QX(0) - 78, (QY(0) + QY(60)) / 2, "塑性指數 PI", 13.5, C["text"])
curve(cv, [(QX(ll), QY(A_LINE(ll))) for ll in [l / 2 for l in range(40, 201)]
           if 0 <= A_LINE(ll) <= 60], C["load"], 3.0)
curve(cv, [(QX(ll), QY(U_LINE(ll))) for ll in [l / 2 for l in range(16, 201)]
           if 0 <= U_LINE(ll) <= 60], C["member"], 2.4, "8 5")
seg(cv, (QX(50), QY(0)), (QX(50), QY(60)), C["muted"], 2.0, "6 5")
cv.text_px(QX(50), QY(58) - 4, "LL = 50", 12, C["muted"], weight="700")
for pi in (4, 7):
    seg(cv, (QX(0), QY(pi)), (QX(A_LINE and (pi / 0.73 + 20)), QY(pi)), C["muted"], 1.4, "3 4")
cv.text_px(QX(29), QY(5.5), "CL-ML", 11.5, C["muted"], weight="700")
tag_px(cv, QX(72), QY(A_LINE(72)) + 26, "A 線　PI = 0.73(LL − 20)", 13, C["load"])
tag_px(cv, QX(40), QY(U_LINE(40)) - 22, "U 線　PI = 0.9(LL − 8)（上界）", 12.5, C["member"])
for ll_, pi_, lab in ((33, 13, "CL"), (74, 44, "CH"), (42, 4.5, "ML"), (74, 16, "MH")):
    cv.text_px(QX(ll_), QY(pi_), lab, 15, C["muted"], weight="700")
dot(cv, QX(LL), QY(PI), 7.4, C["deform"])
tag_px(cv, QX(LL) + 16, QY(PI), "示範點 (LL = %g, PI = %g) ⇒ CL" % (LL, PI), 13,
       C["deform"], anchor="start")

cv.text_px(W_ / 2, 34, "圖 2　塑性指數是「一條軸上的一段」，塑性圖是它的分類用途", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 60, "⚠ SL / PL / LL 為自訂示範值；A 線與 U 線為 USCS（ASTM D2487）規範式",
           12.5, C["muted"])
cv.text_px(W_ / 2, 296, "（三）～（四）塑性圖：同一個 PI，落在 A 線上下代表完全不同的土", 15,
           C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 148,
           "示範點 (LL = 45, PI = 23)：A 線在此為 0.73×(45−20) = 18.25，點在其上；"
           "又 LL ＜ 50 ⇒ 判為 CL（低塑性黏土）。", 13, C["deform"], weight="700")
cv.text_px(W_ / 2, H_ - 122,
           "攔錯用：PI 只有一個數字，講不出是黏土還是粉土——一定要配 LL 一起看。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 96,
           "A 線之上為黏土（C），之下為粉土（M）；LL = 50 分低塑性（L）與高塑性（H）。",
           13, C["text"])
cv.text_px(W_ / 2, H_ - 68,
           "U 線是經驗上界：任何試驗點落在 U 線之上，代表試驗有誤，應重做。", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 42,
           "（五）壓縮指數 C_c 與本圖的曲率係數 C_c 同符號但意義完全不同——"
           "前者是 e–log p′ 的斜率，", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 18,
           "圖解見 SM-2003-2 圖 3；作答時可把曲率係數寫成 C_z 以免混淆。", 12.5, C["muted"])
cv.save(OUT + "/SM-2023-1-fig-2-plasticity.svg")

for nm in ("SW", "GP"):
    d10, d30, d60, cu, cc = D[nm]
    print("%s: D10=%.4f D30=%.4f D60=%.4f Cu=%.3f Cc=%.3f" % (nm, d10, d30, d60, cu, cc))
print("A線(45)=%.2f U線(45)=%.2f 示範點 PI=%.0f" % (A_LINE(45), U_LINE(45), PI))
