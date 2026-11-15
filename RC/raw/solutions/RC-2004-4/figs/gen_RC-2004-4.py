#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2004-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2004-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2004-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-3 批 2＋U1-3＋U2-3 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2004-4"

# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


def _hoop(cv, c, B, H, w=2.0, r=None):
    cv.poly([(c, c), (B - c, c), (B - c, H - c), (c, H - c), (c, c)], C["member"], w)


def _ring_bars(cv, B, H, e, n, r):
    """每面 n 根（含角筋）沿周邊等距排列，回傳座標"""
    pts = set()
    for i in range(n):
        t = e + (B - 2 * e) * i / (n - 1)
        u = e + (H - 2 * e) * i / (n - 1)
        for p in ((t, e), (t, H - e), (e, u), (B - e, u)):
            pts.add((round(p[0], 6), round(p[1], 6)))
    for p in pts:
        _bar(cv, p, r)
    return pts


# ── 題目附圖重繪（題目正本 RC-2004-4-problem.md §4）──
P_CX, P_CY = 70.0, 50.0   # #1 柱：X 向 70、Y 向 50
P_BB, P_BH = 35.0, 70.0   # #8 貳樓梁 35 寬 × 70 深，四面各一支、中心對齊
P_HS = 600.0              # 題文壹樓高度 600
P_LU = P_HS - P_BH        # #4 淨長 530（判讀）
PW, PH = 560, 500


def panel_plan():
    cv = Canvas(PW, PH, sx=1.6, ox=280, oy=262)
    a, b = P_CX / 2, P_CY / 2
    Lb = 85.0
    _rect(cv, a, -P_BB / 2, a + Lb, P_BB / 2)                     # X 向梁（右）
    _rect(cv, -a - Lb, -P_BB / 2, -a, P_BB / 2)                   # X 向梁（左）
    _rect(cv, -P_BB / 2, b, P_BB / 2, b + Lb)                     # Y 向梁（上）
    _rect(cv, -P_BB / 2, -b - Lb, P_BB / 2, -b)                   # Y 向梁（下）
    _rect(cv, -a, -b, a, b, fill="#C9D1DC")
    cv.text((0, 0), "柱", 15, weight="700")
    cv.dim((-a, -b - Lb), (a, -b - Lb), "70", off=44, label_off=13)
    cv.dim((-P_BB / 2, -b - Lb), (P_BB / 2, -b - Lb), "35", off=14, label_off=13)
    cv.dim((a + Lb, b), (a + Lb, -b), "50", off=-34, label_off=-18)
    cv.dim((-a - Lb, P_BB / 2), (-a - Lb, -P_BB / 2), "35", off=14, label_off=16)
    cv.axes((-a - Lb, -b - Lb - 20), 32, 32, labels=("X", "Y"))
    cv.text((0, b + Lb + 18), "平面（單位 cm）：柱 X 向 70、Y 向 50", 13, color=C["muted"])
    cv.text((0, -b - Lb - 50), "X 軸彎矩＝繞 X 軸（深度取 Y 向 50）", 12.5, color=C["accent"])
    return cv


def panel_elev():
    cv = Canvas(PW, PH, sx=0.62, ox=200, oy=70)
    _rect(cv, 0, 0, P_CY, P_HS - P_BH)                            # 柱（示 Y 向 50 的立面）
    _rect(cv, -160, P_HS - P_BH, P_CY + 160, P_HS)                # 貳樓梁
    cv.line((-170, 0), (P_CY + 170, 0), C["member"], 2.4)          # 基礎面
    cv.dim((-160, 0), (-160, P_HS), "600", off=-30, label_off=-24)
    cv.dim((0, 0), (0, P_LU), "530", off=-34, label_off=-24)
    cv.text((P_CY / 2, P_HS + 30), "貳樓梁深 70", 12.5, color=C["muted"])
    cv.text((P_CY + 30, P_LU * 0.55), "柱頂：X 軸 +8(D)／+9(L)", 12.5, anchor="start")
    cv.text((P_CY + 30, P_LU * 0.55 - 36), "　　　Y 軸 +10(D)／+12(L)", 12.5, anchor="start")
    cv.text((P_CY + 30, P_LU * 0.3), "柱底：X 軸 −12(D)／−8(L)", 12.5, anchor="start")
    cv.text((P_CY + 30, P_LU * 0.3 - 36), "　　　Y 軸 −10(D)／−6(L)", 12.5, anchor="start")
    cv.text((P_CY + 30, P_LU * 0.12), "（t-m；正＝順時鐘）", 12, color=C["muted"], anchor="start")
    cv.text((P_CY / 2, -45), "立面示意：樓層高 600 扣梁深 70 → ℓu＝530（判讀 #4）", 12.5, color=C["muted"])
    cv.text((P_CY / 2, -80), "兩端轉向相反 → 單曲率（判讀 #3）；P_D＝200、P_L＝100 t", 12.5, color=C["accent"])
    return cv


def fig1_problem():
    return compose([panel_plan(), panel_elev()], title=f"{TAG} 題目附圖（梁柱平面重繪＋立面示意）",
                   sub="依題目正本判讀清單 #1–#4、#8；梁伸出長度、基礎面為示意",
                   note="柱斷面方向以附圖為準：70 cm 沿 X、50 cm 沿 Y；k 考卷未給（無側移取 1.0）")


FIGURES = [("1-problem", fig1_problem, "柱 70 cm 讀成 Y 向；單曲率讀成雙曲率；ℓu 用層高 600")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2；數值由常數現算，檔尾對 §4 assert）══
from structdraw import Canvas as _Cv
EC4 = 15000 * math.sqrt(280.0)
PD4, PL4 = 200.0, 100.0
PU4 = 1.2 * PD4 + 1.6 * PL4                       # §4 ①
BD4 = 1.2 * PD4 / PU4                             # βdns（軸力比）
MXT, MXB = 1.2 * 8 + 1.6 * 9, 1.2 * 12 + 1.6 * 8  # M_ux 頂（順）、底（逆）
MYT, MYB = 1.2 * 10 + 1.6 * 12, 1.2 * 10 + 1.6 * 6


def _slender(Mt, Mb, h, b, lu):
    M2, M1 = max(Mt, Mb), min(Mt, Mb)
    rat = -M1 / M2                                # 單曲率：現行慣例為負
    kl_r, lim = lu / (0.3 * h), min(40.0, 34 + 12 * rat)
    EI = 0.4 * EC4 * (b * h ** 3 / 12) / (1 + BD4)
    Pc = math.pi ** 2 * EI / lu ** 2 / 1000
    Cm = 0.6 - 0.4 * rat
    d = max(1.0, Cm / (1 - PU4 / (0.75 * Pc)))
    return dict(M2=M2, M1=M1, rat=rat, klr=kl_r, lim=lim, Pc=Pc, Cm=Cm, d=d,
                slender=kl_r > lim, Mc=(d * max(M2, PU4 * (1.5 + 0.03 * h) / 100)) if kl_r > lim else M2)


SX4 = _slender(MXT, MXB, P_CY, P_CX, P_LU)        # 繞 X 軸：深 50
SY4 = _slender(MYT, MYB, P_CX, P_CY, P_LU)        # 繞 Y 軸：深 70
SY6 = dict(_slender(MYT, MYB, P_CX, P_CY, P_HS))  # ℓu＝600 對照（§5 ②）
SY6["Mc"] = SY6["d"] * SY6["M2"]
QW, QH = 400, 500


def panel_q_section():
    cv = _Cv(QW, QH, sx=3.0, ox=200, oy=330)
    cv.panel("① 斷面方向與細長比")
    a, b = P_CX / 2, P_CY / 2
    _rect(cv, -a, -b, a, b, fill="#C9D1DC")
    cv.dim((-a, -b), (a, -b), "70", off=18, label_off=13)
    cv.dim((a, -b), (a, b), "50", off=18, label_off=16)
    cv.text_px(200, 296, "X 向", 12.5, color=C["muted"])
    cv.text_px(358, 196, "Y 向", 12.5, color=C["muted"], anchor="start")
    cv.text_px(200, 170, "柱 70×50", 14, weight="700")
    cv.text_px(200, 324, f"繞 X 軸（M_ux）：深 50 → r_x＝{0.3*P_CY:.0f} cm", 13, color=C["text"])
    cv.text_px(200, 347, f"kℓu/r＝{SX4['klr']:.2f} ＞ 限值 {SX4['lim']:.2f} → 細長", 13, color=C["load"], weight="700")
    cv.text_px(200, 380, f"繞 Y 軸（M_uy）：深 70 → r_y＝{0.3*P_CX:.0f} cm", 13, color=C["text"])
    cv.text_px(200, 403, f"kℓu/r＝{SY4['klr']:.2f} ≤ 限值 {SY4['lim']:.2f} → 不放大", 13, color=C["deform"], weight="700")
    cv.text_px(200, 425, f"（Y 向餘裕僅 {(SY4['lim']-SY4['klr'])/SY4['lim']*100:.1f}%）", 12.5, color=C["muted"])
    cv.text_px(200, 452, "限值＝34＋12 M_1/M_2（單曲率 M_1/M_2 取負）", 12, color=C["muted"])
    cv.text_px(200, 472, f"X：M_1/M_2＝{SX4['rat']:.3f}　Y：{SY4['rat']:.3f}", 12, color=C["muted"])
    return cv


def _col_panel(title, S, top_is_M2, extra=None):
    k = 6.0                                        # 每 tf·m 的模型長度
    cv = _Cv(QW, QH, sx=0.62, ox=150, oy=78)
    cv.panel(title)
    H = P_LU
    # 單曲率變形示意（左側小柱）
    xs = -150
    cv.line((xs, 0), (xs, H), C["ghost"], 2, dash="6 5")
    cv.poly([(xs - 34 * math.sin(math.pi * i / 40), H * i / 40) for i in range(41)], C["deform"], 3.2)
    cv.text((xs, -30), "單曲率（弓形）", 12, color=C["deform"])
    # 一階彎矩圖（兩端同側＝單曲率）
    Mb, Mt = (S["M2"], S["M1"]) if not top_is_M2 else (S["M1"], S["M2"])
    pts = [(0, 0), (Mb * k, 0), (Mt * k, H), (0, H)]
    cv.polygon(pts, C["fill_m"]); cv.poly(pts + [(0, 0)], C["bmd"], 2.4)
    cv.line((0, -10), (0, H + 10), C["member"], 4, cap="butt")
    cv.text((Mt * k + 8, H + 26), f"柱頂 {Mt:.1f}", 13, color=C["bmd"], anchor="start", weight="700")
    cv.text((Mb * k + 8, -26), f"柱底 {Mb:.1f}", 13, color=C["bmd"], anchor="start", weight="700")
    cv.text((S["M2"] * k * 0.45, H * 0.5), "一階 M_u", 12.5, color=C["bmd"])
    if S["slender"]:
        x = S["Mc"] * k
        cv.line((x, 0), (x, H), C["load"], 2.6, dash="8 6")
        cv.text((x + 7, H * 0.66), "δns·M_2", 13, color=C["load"], anchor="start", weight="700")
        cv.text((x + 7, H * 0.58), f"＝{S['d']:.3f}", 12, color=C["load"], anchor="start")
        cv.text((x + 7, H * 0.52), f"　×{S['M2']:.1f}", 12, color=C["load"], anchor="start")
        cv.text((x + 7, H * 0.44), f"＝{S['Mc']:.1f}", 13, color=C["load"], anchor="start", weight="700")
        cv.text_px(200, 470, f"C_m＝{S['Cm']:.3f}　P_c＝{S['Pc']:.1f} tf　δns＝{S['d']:.3f}", 12.5, color=C["muted"])
    if extra:
        x = extra["Mc"] * k
        cv.line((x, 0), (x, H), C["muted"], 1.8, dash="3 5")
        cv.text((x + 4, H * 0.30), "ℓu＝600 時", 11.5, color=C["muted"], anchor="start")
        cv.text((x + 4, H * 0.24), f"轉細長 {extra['Mc']:.1f}", 11.5, color=C["muted"], anchor="start")
        cv.text_px(200, 470, f"不放大：M_uy＝M_2＝{S['M2']:.1f}（柱頂）", 12.5, color=C["deform"], weight="700")
    cv.dim((-60, 0), (-60, H), f"ℓu＝{H:.0f}", off=-14, label_off=-30)
    return cv


def fig2_moments():
    return compose([panel_q_section(),
                    _col_panel("② X 向（繞 X 軸）：細長，放大", SX4, top_is_M2=False),
                    _col_panel("③ Y 向（繞 Y 軸）：不放大", SY4, top_is_M2=True, extra=SY6)],
                   title=f"{TAG} 圖 2　斷面方向、單曲率彎矩圖與放大前後",
                   sub=f"1.2D＋1.6L：Pu＝{PU4:.0f} tf；k＝1.0、ℓu＝530 cm；現行慣例單曲率 M₁/M₂＜0",
                   note=f"設計值：Pu＝{PU4:.0f} tf、Mux＝{SX4['Mc']:.1f}、Muy＝{SY4['Mc']:.1f} tf·m（柱頂斷面不放大讀法 24.0／31.2 見 §5）")


def check_solution():
    for name, got, want, tol in [("Pu", PU4, 400, 1e-9), ("Mxb", MXB, 27.2, 1e-9), ("Myt", MYT, 31.2, 1e-9),
                                 ("klx", SX4["klr"], 35.33, 0.005), ("limx", SX4["lim"], 23.41, 0.005),
                                 ("kly", SY4["klr"], 25.24, 0.005), ("limy", SY4["lim"], 25.69, 0.005),
                                 ("Pcx", SX4["Pc"], 1607.6, 0.05), ("Cmx", SX4["Cm"], 0.953, 5e-4), ("dx", SX4["d"], 1.426, 5e-4),
                                 ("Mux", SX4["Mc"], 38.8, 0.05), ("Muy", SY4["Mc"], 31.2, 1e-9), ("Y600", SY6["Mc"], 34.9, 0.05)]:
        assert abs(got - want) <= tol, (name, got, want)
    assert SX4["slender"] and not SY4["slender"] and SY6["slender"]
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-moments", fig2_moments, "斷面方向弄反；單曲率畫成雙曲率；放大前後混用"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
