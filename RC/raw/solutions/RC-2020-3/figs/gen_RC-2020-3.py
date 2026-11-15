#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2020-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2020-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2020-3.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-1／U3-2 題目正本推廣・批 1）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2020-3"
PW, PH = 560, 560          # 各子圖畫布尺寸（px，compose 要求相同）


def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


# ── 判讀清單數值（題目正本 §4）──
LX, LY = 800.0, 900.0            # #1 柱距：X 向 800、Y 向 900（柱中心距）
CW = 100.0                       # #3 柱 100×100
SW = 100.0                       # #4 剪力筋帶寬 100（＝柱寬）
H_SLAB = 40.0                    # #5 版全深 40


def _hatched_col(cv, cx, cy, a, label=None):
    _rect(cv, cx - a / 2, cy - a / 2, cx + a / 2, cy + a / 2, fill="#C9D1DC", w=1.8)
    for k in range(1, 4):
        t = k / 4 * a
        cv.line((cx - a / 2 + t, cy - a / 2), (cx - a / 2, cy - a / 2 + t), C["member"], 1)
        cv.line((cx + a / 2, cy - a / 2 + t), (cx - a / 2 + t, cy + a / 2), C["member"], 1)


def _strip(cv, x0, y0, x1, y1, horiz, n):
    _rect(cv, x0, y0, x1, y1, fill="#FFFFFF", w=1.4)
    for k in range(1, n):
        if horiz:
            x = x0 + (x1 - x0) * k / n
            cv.line((x, y0), (x, y1), C["member"], 1)
        else:
            y = y0 + (y1 - y0) * k / n
            cv.line((x0, y), (x1, y), C["member"], 1)


def panel_plan():
    cv = Canvas(PW, PH, sx=0.22, ox=PW / 2 - 10, oy=PH / 2 + 2)
    a = CW
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            _hatched_col(cv, i * LX, j * LY, a)
    # #4 剪力筋帶：由柱 A 四面沿 ±X、±Y（長度依考卷附圖畫到鄰柱，示意）
    _strip(cv, a / 2, -SW / 2, LX - a / 2, SW / 2, True, 18)
    _strip(cv, -LX + a / 2, -SW / 2, -a / 2, SW / 2, True, 18)
    _strip(cv, -SW / 2, a / 2, SW / 2, LY - a / 2, False, 20)
    _strip(cv, -SW / 2, -LY + a / 2, SW / 2, -a / 2, False, 20)
    _hatched_col(cv, 0, 0, a)
    cv.dim((-LX, LY), (0, LY), "800", off=-36, label_off=-14)
    cv.dim((0, LY), (LX, LY), "800", off=-36, label_off=-14)
    cv.dim((LX, LY), (LX, 0), "900", off=-40, label_off=-22)
    cv.dim((LX, 0), (LX, -LY), "900", off=-40, label_off=-22)
    yA = a / 2 + 75                                         # #3 柱寬 100（照考卷「100→ ←」畫法）
    cv.line((-a / 2, a / 2 + 10), (-a / 2, yA + 18), C["dim"], 1)
    cv.line((a / 2, a / 2 + 10), (a / 2, yA + 18), C["dim"], 1)
    cv.arrow((-a / 2 - 120, yA), (-a / 2, yA), C["dim"], 1.2, 7)
    cv.arrow((a / 2 + 120, yA), (a / 2, yA), C["dim"], 1.2, 7)
    cv.math((-a / 2 - 175, yA), "100", 14, color=C["dim"])
    xS = LX * 0.62                                          # #4 剪力筋帶寬 100
    cv.line((xS - 30, SW / 2), (xS + 30, SW / 2), C["dim"], 1)
    cv.line((xS - 30, -SW / 2), (xS + 30, -SW / 2), C["dim"], 1)
    cv.arrow((xS, SW / 2 + 130), (xS, SW / 2), C["dim"], 1.2, 7)
    cv.arrow((xS, -SW / 2 - 130), (xS, -SW / 2), C["dim"], 1.2, 7)
    cv.math((xS, SW / 2 + 175), "100", 14, color=C["dim"])
    sp = (LX - a) / 18                                      # 剪力筋間距 s（示意）
    x1 = a / 2 + 16 * sp
    cv.dim((x1, -SW / 2), (x1 + sp, -SW / 2), "s", off=16, label_off=14)
    cv.text((-170, -160), "柱 A（內柱）", 13, anchor="end")
    cv.line((-160, -140), (-55, -55), C["muted"], 1.2)
    cv.text((LX * 0.34, -SW / 2 - 120), "剪力筋（雙肢）", 12, color=C["muted"])
    cv.axes((LX + 250, -LY - 130), lx=110, ly=110, labels=("X", "Y"))
    cv.text((0, -LY - 175), "平面圖（單位 cm）", 13, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=1.05, ox=PW / 2, oy=PH / 2 - 20)
    a, t = CW, H_SLAB
    W = 200
    _rect(cv, -W, 0, W, t, fill="#EDF1F6", w=2.2)                  # 無梁版
    _rect(cv, -a / 2, t, a / 2, t + 110, fill="#C9D1DC", w=2.0)    # 上柱
    _rect(cv, -a / 2, -110, a / 2, 0, fill="#C9D1DC", w=2.0)       # 下柱
    for x0, x1 in ((a / 2, W), (-W, -a / 2)):                      # 剪力筋（示意間距）
        n = 12
        for k in range(1, n + 1):
            x = x0 + (x1 - x0) * (k - 0.5) / n
            cv.line((x, 6), (x, t - 6), C["member"], 1.2)
    cv.dim((-a / 2, t + 110), (a / 2, t + 110), "100", off=-24, label_off=-13)
    cv.dim((W, t), (W, 0), "40", off=-26, label_off=-20)
    xs = a / 2 + (W - a / 2) * 0.5 / 12
    cv.dim((xs, t), (xs + (W - a / 2) / 12, t), "s", off=-20, label_off=-13)
    cv.text((W - 10, t + 26), "無梁版", 13, anchor="end")
    cv.text((0, -60), "柱", 14)
    cv.text((-W + 70, -26), "剪力筋由柱面往外", 12, color=C["muted"])
    cv.text((0, -150), "斷面圖（單位 cm）", 13, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_plan(), panel_sec()], title=f"{TAG} 題目附圖（平面圖＋斷面圖重繪）",
                   sub="依題目正本判讀清單 #1–#5；剪力筋帶長度與剪力筋間距為示意",
                   note="柱距 X 向 800、Y 向 900（兩向不同）；柱 A 為內柱 100×100")


FIGURES = [("1-problem", fig1_problem, "把兩向柱距都讀成 800（Y 向為 900）")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-B1；數值由常數現算，檔尾對 §4 assert）══
FC, FYT, D_EFF, WU, AB = 280.0, 4200.0, 35.0, 4.6, 1.267
LAM_S = math.sqrt(2 / (1 + 0.04 * D_EFF))
C_D = CW + D_EFF                                  # 臨界方塊邊長 135
BO = 4 * C_D
VU = WU * (LX * LY - C_D ** 2) / 1e4              # tf
PHI_VC = 0.75 * 1.06 * LAM_S * math.sqrt(FC) * BO * D_EFF / 1000
VCW = 0.53 * LAM_S * math.sqrt(FC) * BO * D_EFF / 1000
VS = VU / 0.75 - VCW
NLEG = 4 * 2; AV = NLEG * AB
S_REQ = AV * FYT * D_EFF / (VS * 1000)
PHI_VNMAX = 0.75 * 1.59 * math.sqrt(FC) * BO * D_EFF / 1000


def panel_trib():
    cv = Canvas(PW, PH, sx=0.235, ox=PW / 2, oy=PH / 2 - 40)
    cv.panel("從屬面積 8 m × 9 m", "邊界在鄰柱中心距之半；扣臨界方塊")
    for i in (-1, 0, 1):                                  # 柱格（中央為柱 A，鄰柱在外）
        for j in (-1, 0, 1):
            if i or j:
                _hatched_col(cv, i * LX, j * LY, CW)
    _rect(cv, -LX / 2, -LY / 2, LX / 2, LY / 2, fill="rgba(124,58,237,0.14)", stroke=C["sfd"], w=1.8, dash="7 5")
    for k in (-1, 1):                                     # 柱線
        cv.line((k * LX, -LY - 60), (k * LX, LY + 60), C["dim"], 1, dash="2 4")
        cv.line((-LX - 60, k * LY), (LX + 60, k * LY), C["dim"], 1, dash="2 4")
    _rect(cv, -C_D / 2, -C_D / 2, C_D / 2, C_D / 2, fill="#FFFFFF", stroke=C["accent"], w=2)
    _hatched_col(cv, 0, 0, CW)
    cv.dim((-LX / 2, -LY / 2), (LX / 2, -LY / 2), "800", off=20, label_off=13)
    cv.dim((LX / 2, -LY / 2), (LX / 2, LY / 2), "900", off=20, label_off=20)
    cv.text((0, LY / 2 - 110), f"V_{{u}}＝4.6×(8×9−1.35^{{2}})", 13, C["sfd"], weight="700")
    cv.text((0, LY / 2 - 210), f"＝{VU:.2f} tf", 13, C["sfd"], weight="700")
    cv.text((0, -C_D / 2 - 90), "柱 A", 12, C["muted"])
    return cv


def panel_perim():
    cv = Canvas(PW, PH, sx=1.35, ox=PW / 2, oy=PH / 2 - 18)
    cv.panel("臨界周長與剪力筋肢數", f"距柱面 d/2＝{D_EFF/2:.1f}，b_{{o}}＝4×{C_D:.0f}＝{BO:.0f} cm")
    a = CW; e = 150
    for sgn in (1, -1):
        _strip(cv, a / 2, -SW / 2, e, SW / 2, True, 1) if sgn == 1 else _strip(cv, -e, -SW / 2, -a / 2, SW / 2, True, 1)
        _strip(cv, -SW / 2, a / 2, SW / 2, e, False, 1) if sgn == 1 else _strip(cv, -SW / 2, -e, SW / 2, -a / 2, False, 1)
    _hatched_col(cv, 0, 0, a)
    _rect(cv, -C_D / 2, -C_D / 2, C_D / 2, C_D / 2, fill=None, stroke=C["accent"], w=2.4, dash="8 5")
    # 一條周線（距柱面 s 處，示意）上的 8 肢
    r = C_D / 2
    legs = []
    for x in (-SW / 2 + 12, SW / 2 - 12):
        legs += [(x, r), (x, -r)]
    for y in (-SW / 2 + 12, SW / 2 - 12):
        legs += [(r, y), (-r, y)]
    for p in legs:
        cv.dot(p, 6.5, C["tension"])
    cv.text((0, r + 22), "每條帶雙肢（紅點）", 12, C["tension"])
    cv.text((e - 4, -r - 26), "臨界周線", 12.5, C["accent"], anchor="end")
    cv.text((0, -e - 14), f"A_{{v}}＝4 帶×2 肢×1.267＝{AV:.3f} cm^{{2}}", 13, C["text"], weight="700")
    return cv


def panel_result():
    cv = Canvas(PW, PH, sx=1, ox=0, oy=0)
    cv.panel("由 V_{s} 求 s", "V_{s}＝A_{v} f_{yt} d / s（長度用 d，不是 b_{o}）")
    rows = [(f"λ_{{s}}＝√(2/(1+0.04×35))＝{LAM_S:.4f}", C["text"]),
            (f"㈠ φV_{{c}}＝0.75×1.06λ_{{s}}√f'c b_{{o}}d＝{PHI_VC:.2f} tf", C["text"]),
            (f"     ＜ V_{{u}}＝{VU:.2f} tf → 需剪力筋", C["load"]),
            (f"㈡ V_{{c}}＝0.53λ_{{s}}√f'c b_{{o}}d＝{VCW:.2f} tf", C["text"]),
            (f"     V_{{s}}＝V_{{u}}/0.75−V_{{c}}＝{VS:.2f} tf", C["text"]),
            (f"     s＝{AV:.3f}×4200×35/V_{{s}}＝{S_REQ:.2f} cm → 取 5 cm", C["bmd"]),
            (f"上限：φV_{{n,max}}＝{PHI_VNMAX:.1f} tf ≥ V_{{u}}；s ≤ d/2＝17.5", C["text"]),
            ("", C["text"]),
            ("舊解：A_{v} 只算一組雙肢、式中以 b_{o} 代 d，", C["load"]),
            ("得 s 由 d/2＝17.5 控制 → φV_{n} 僅 178.6 tf", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(34, 112 + i * 38, s, 13.5, col, "start", weight="700" if col == C["bmd"] else "400")
    return cv


def fig2_punching():
    return compose([panel_trib(), panel_perim(), panel_result()],
                   title=f"{TAG} 圖 2　穿孔剪力：從屬面積、臨界周長與剪力筋肢數",
                   sub="數值取自解析 §4（現行規範，樓版乘 λs）",
                   note="攔：Y 向柱距讀成 800；A_v 只算一組雙肢；V_s 以 b_o 代 d")


def check_solution():
    for name, got, want, tol in [("Vu", VU, 322.82, 0.01), ("phiVc", PHI_VC, 229.52, 0.02), ("Vcw", VCW, 153.01, 0.02),
                                 ("Vs", VS, 277.41, 0.03), ("Av", AV, 10.136, 1e-6), ("s", S_REQ, 5.37, 0.006),
                                 ("phiVnmax", PHI_VNMAX, 377.1, 0.06), ("bo", BO, 540, 0)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-punching", fig2_punching, "從屬面積 8×9、8 肢、V_s 長度用 d"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
