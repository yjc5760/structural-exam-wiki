#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2009-4 圖解產生腳本（開槽銲型式、螺栓中心距、預拉力）

三張圖的每個數字都來自規範原文或 AISC 表 J3.1（以 3/4 in A325 之 28 kips 驗核）。
執行：python3 gen_SS-2009-4.py   →   figs/*.svg
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
# 由 SS-2009-4 §4 之規範原文取得
# ══════════════════════════════════════════════════════════════
S_MIN_K   = 8/3          # 一般強制下限（§10.3.9）           §4 四
S_PREF_K  = 3.0          # 沿力方向且 F_p 依式(10.3-1a/b) 時   §4 四
DB_EX     = 25.0         # mm 數值示例用之螺栓標稱直徑         §4 四
PRELOAD_K = 0.70         # T_0 = 0.70 F_u A_t                 §4 五
# 3/4 in A325 之驗核（AISC 表 J3.1 列 28 kips）                §4 五
FU_A325   = 120.0        # ksi
AT_34     = 0.334        # in^2 螺紋處有效抗拉面積
AB_34     = 0.442        # in^2 全斷面積
T_AT      = PRELOAD_K*FU_A325*AT_34      # 28.1 kips ✓
T_AB      = PRELOAD_K*FU_A325*AB_34      # 37.1 kips ✗
T_TABLE   = 28.0         # kips  AISC 表 J3.1
# 開槽角度（AWS A2.4 常用值）                                   §4 一
BEVEL_DEG = 35.0


# ══════════════════════════════════════════════════════════════
def fig1_groove():
    """圖 1：Single V 與 Single Bevel 的開槽幾何"""
    PWD, PH = 500, 470
    XL, XR, YL, YH = -30.0, 30.0, -16.0, 34.0
    Lm, Tm, Bm = 40, 112, 104
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    TP  = 20.0                                        # 母材厚（繪圖單位）
    RF  = 1.6                                         # 根部間隙之半
    DX  = TP*math.tan(math.radians(BEVEL_DEG))        # 斜面之水平投影

    # ── Single V：對接接頭，兩側母材各開斜角，槽口向上敞開 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("Single V（V 形開槽）", "對接接頭 Butt Joint")
    p1.polygon([(-28, 0), (-RF, 0), (-RF - DX, TP), (-28, TP)], "#DCE3EC", C["member"], 2.2)
    p1.polygon([(28, 0), (RF, 0), (RF + DX, TP), (28, TP)], "#DCE3EC", C["member"], 2.2)
    p1.polygon([(-RF, 0), (RF, 0), (RF + DX, TP), (-RF - DX, TP)],
               C["fill_t"], C["load"], 2.4)
    p1.text_px(p1.X(0), p1.Y(TP) - 18, "兩側母材均開斜角", 12.5, C["load"], weight="700")
    p1.line((-RF, 0), (RF, 0), C["accent"], 3.0)
    p1.text_px(p1.X(0), p1.Y(0) + 22, "根部間隙", 11.5, C["accent"], weight="700")
    p1.math_px(p1.X(-RF - DX*0.45), p1.Y(TP*0.55), f"{BEVEL_DEG:g}°", 13, C["accent"],
               "end", weight="700")
    p1.math_px(p1.X(RF + DX*0.45), p1.Y(TP*0.55), f"{BEVEL_DEG:g}°", 13, C["accent"],
               "start", weight="700")
    p1.text_px(PWD/2, PH - 62, "截面對稱，槽口向上敞開", 13.5, C["text"], weight="700")
    p1.text_px(PWD/2, PH - 38, "加工量較多；對稱填充，較易完全熔透", 12, C["muted"])
    p1.text_px(PWD/2, PH - 16, "常用於柱／梁翼板之全滲透對接銲（CJP）", 12, C["muted"])

    # ── Single Bevel：T 形接頭，僅立板端部單側開斜角 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("Single Bevel（單斜面開槽）", "T 形接頭 T-Joint")
    TV = 9.0                                          # 立板厚
    HB = TV                                           # 45° 斜切，端部抬高 HB
    p2.polygon([(-28, -12), (28, -12), (28, 0), (-28, 0)], "#DCE3EC", C["member"], 2.2)
    p2.polygon([(0, 0), (TV, HB), (TV, TP), (0, TP)], "#DCE3EC", C["member"], 2.2)
    p2.polygon([(0, 0), (TV, HB), (TV, 0)], C["fill_t"], C["load"], 2.4)
    p2.text_px(p2.X(TV) + 10, p2.Y(HB*0.45), "僅立板端部單側開斜角", 12, C["load"],
               "start", weight="700")
    p2.line((0, TP), (0, 0), C["accent"], 2.0, dash="5 4")
    p2.text_px(p2.X(0) - 10, p2.Y(TP*0.62), "另一側維持方形邊", 11.5, C["muted"], "end")
    p2.text_px(PWD/2, PH - 62, "截面不對稱（半 V）", 13.5, C["text"], weight="700")
    p2.text_px(PWD/2, PH - 38, "加工量較少（只需開一側）", 12, C["muted"])
    p2.text_px(PWD/2, PH - 16, "非對稱填充，根部熔透較難掌握", 12, C["muted"])

    compose([p1, p2], cols=2,
            title="圖 1　Single V 與 Single Bevel 的差別在「幾片母材開斜角」",
            sub="AWS A2.4 命名邏輯：前綴 Single／Double 指單面／雙面開槽；"
                "字根 V／Bevel 指兩側／單側母材開斜角",
            note="接頭型式決定開槽選擇：對接兩側都磨得到 ⇒ V；T 形只有一側磨得到 ⇒ Bevel",
            path=os.path.join(OUT, "SS-2009-4-fig-1-groove.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_bolt_spacing():
    """圖 2：螺栓中心距的三個層次"""
    W, H = 940, 520
    XL, XR = -1.4, 5.2                      # 以「倍螺栓直徑」為單位
    YL, YH = -1.9, 2.0
    Lm, Rm, Tm, Bm = 60, 300, 118, 100
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    cv = Canvas(W, H, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx, bg="#FFFFFF")

    # 鋼板與兩個螺栓孔（間距畫在 3d，並標出 8/3 d 的位置）
    cv.polygon([(-1.2, -1.3), (5.0, -1.3), (5.0, 1.3), (-1.2, 1.3)],
               "#EDF1F6", C["member"], 2.2)
    for x in (0.0, S_PREF_K):
        cv.circle((x, 0), 0.5, "#FFFFFF", C["member"], 2.2)
        cv.dot((x, 0), 3.4, fill=C["member"])
    cv.arrow((-1.1, 0), (-0.7, 0), C["load"], 3.0, 10)
    cv.arrow((4.9, 0), (4.5, 0), C["load"], 3.0, 10)

    # 三層規定
    cv.dim((0, -0.55), (S_MIN_K, -0.55), f"8/3 d ≈ 2.67 d", off=52, label_off=14,
           color=C["bmd"])
    cv.dim((0, 0.55), (S_PREF_K, 0.55), f"3 d", off=-40, label_off=-14, color=C["accent"])
    cv.line((S_MIN_K, -1.3), (S_MIN_K, 1.3), C["bmd"], 1.6, dash="5 4")
    cv.line((S_PREF_K, -1.3), (S_PREF_K, 1.3), C["accent"], 1.6, dash="5 4")

    cv.legend(W - Rm + 12, 168,
              [(C["bmd"], "① 一般強制下限"), (C["accent"], "② 沿力方向之加嚴")],
              size=12, gap=22)
    cv.text_px(W - Rm + 12, 226, "① 所有孔型、所有方向", 12.5, C["bmd"], "start", weight="700")
    cv.math_px(W - Rm + 12, 248, f"s ≥ (8/3) d_{{b}}", 13, C["bmd"], "start", weight="700")
    cv.text_px(W - Rm + 12, 268, "← 本題所問的答案", 11.5, C["bmd"], "start")
    cv.text_px(W - Rm + 12, 302, "② 當 F_p 依式(10.3-1a)/(10.3-1b)", 12, C["accent"],
               "start", weight="700")
    cv.text_px(W - Rm + 12, 322, "　 取用時，沿力量傳遞方向", 12, C["accent"], "start")
    cv.math_px(W - Rm + 12, 344, f"s ≥ 3 d_{{b}}", 13, C["accent"], "start", weight="700")
    cv.text_px(W - Rm + 12, 378, "③ 承壓需求（式 10.3-2）", 12, C["muted"], "start",
               weight="700")
    cv.math_px(W - Rm + 12, 400, "s ≥ P/(F_{u}t) + d/2", 12.5, C["muted"], "start")
    cv.text_px(W - Rm + 12, 434, f"數值示例（d_b = {DB_EX:g} mm）：", 12, C["text"], "start",
               weight="700")
    cv.text_px(W - Rm + 12, 456, f"① {S_MIN_K*DB_EX:.1f} mm　② {S_PREF_K*DB_EX:.0f} mm",
               12.5, C["text"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 2　螺栓中心距的三個層次（層次別搞反）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               "台灣規範 §10.3.9 強制的一般下限是 8/3 d；3d 是「有條件」的加嚴，不是一般規定",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "舊版與許多考生記成「規範規定 3d、絕對下限 2又2/3 d」——把兩者的層次顛倒了",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "AISC 360-16 §J3.3 把 3d 明寫為「preferred（建議值）」，強制下限同為 8/3 d",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2009-4-fig-2-bolt-spacing.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_preload():
    """圖 3：預拉力要乘哪一個面積"""
    W, H = 940, 440
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 330, 380
    rows = ((f"乘 A_t（螺紋處有效抗拉面積）", f"0.70 × {FU_A325:g} × {AT_34:g}",
             T_AT, C["bmd"], "✓ 與 AISC 表 J3.1 之 28 kips 相符"),
            (f"乘 A_b（全斷面積，誤用）", f"0.70 × {FU_A325:g} × {AB_34:g}",
             T_AB, C["load"], f"✗ 高估 {100*(T_AB/T_AT-1):.0f}%"))
    peak = max(T_AT, T_AB) * 1.16
    for i, (nm, expr, v, col, verdict) in enumerate(rows):
        y = 150 + i*84
        cv.text_px(x0 - 14, y - 10, nm, 13, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, expr, 11.5, C["muted"], "end")
        cv.rect_px(x0, y-17, bw, 34, "#EDF1F6", 7)
        cv.rect_px(x0, y-17, bw*v/peak, 34, col, 7)
        cv.text_px(x0 + bw*v/peak + 12, y - 9, f"{v:.1f} kips", 13.5, col, "start",
                   weight="700")
        cv.text_px(x0 + bw*v/peak + 12, y + 12, verdict, 11.5, col, "start")
    # 表列值基準線
    xt = x0 + bw*T_TABLE/peak
    cv.parts.append(f'<line x1="{xt}" y1="118" x2="{xt}" y2="{150+84+26}" '
                    f'stroke="{C["accent"]}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    cv.text_px(xt, 110, f"AISC 表 J3.1：{T_TABLE:g} kips", 12, C["accent"], weight="700")

    cv.text_px(W/2, 34, "圖 3　最小預拉力：0.7 倍抗拉強度，但要乘哪一個面積？", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"規範原文：「等於最小抗拉強度之 {PRELOAD_K} 倍」；以 3/4 in A325 反向驗核",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"寫成 0.7F_u A_b 而把 A_b 理解為全斷面積，會高估三成"
               f"（以實際表值 {AB_34:g}/{AT_34:g} 得 {100*(T_AB/T_AT-1):.0f}%；"
               f"以名目 A_t ≈ 0.75A_b 概算則為 33%）",
               12, C["accent"])
    cv.text_px(W/2, H - 48,
               "題目問「多少倍」⇒ 答 0.7 倍即符合題意；面積取法是實際計算時的關鍵",
               13, C["muted"])
    cv.text_px(W/2, H - 24,
               "0.7 這個係數自 AISC LRFD 1993 至 360-22 從未改變；螺栓標準已改為 ASTM F3125",
               12.5, C["muted"])
    cv.save(os.path.join(OUT, "SS-2009-4-fig-3-preload.svg"))


# ══════════════════════════════════════════════════════════════
# 圖 1：題目附圖重繪（依題目正本 SS-2009-4-problem.md §4 判讀清單，待確認）
# 只畫考卷給的東西：情境示意（箱型柱貫通、四向 H 梁、翼板與腹板續接板＋螺栓）；
# 考卷無任何尺寸（#1 附圖只作情境示意），下列尺寸全部為示意，與上方解題常數無關。
# ══════════════════════════════════════════════════════════════
Q_BC   = 56.0     # 箱型柱寬（示意）
Q_HC   = 105.0    # 柱自梁中心上下各畫出長度（示意）
Q_D, Q_BF, Q_TF, Q_TW = 46.0, 22.0, 2.2, 1.4   # 梁深、翼寬、翼厚、腹厚（示意）
Q_LB   = 86.0     # 梁自柱面伸出長度（示意）
Q_SPL  = 46.0     # 續接位置距柱面（示意）
Q_LPF, Q_LPW, Q_HPW, Q_TP = 34.0, 20.0, 30.0, 1.2   # 翼續接板長、腹續接板長、高、板厚（示意）
Q_C30, Q_S30 = math.cos(math.radians(30)), 0.5


def _q_iso(p):
    x, y, z = p
    return ((x - y) * Q_C30, z - (x + y) * Q_S30)


def _q_poly(cv, pts3, fill="#FFFFFF", w=1.5):
    cv.polygon([_q_iso(p) for p in pts3], fill, C["member"], w)


def _q_beam(cv, e, n):
    """e：梁軸向單位向量（±x 或 ±y）；n：朝觀者的水平側向（+x 或 +y）。"""
    a = Q_BC / 2
    h = Q_D / 2

    def P(u, v, z):
        return (e[0] * u + n[0] * v, e[1] * u + n[1] * v, z)

    def quad_uv(u0, u1, v0, v1, z):
        return [P(u0, v0, z), P(u1, v0, z), P(u1, v1, z), P(u0, v1, z)]

    def quad_uz(u0, u1, v, z0, z1):
        return [P(u0, v, z0), P(u1, v, z0), P(u1, v, z1), P(u0, v, z1)]

    u0, u1, s = a, a + Q_LB, a + Q_SPL
    pf0, pf1 = s - Q_LPF / 2, s + Q_LPF / 2
    pw0, pw1 = s - Q_LPW / 2, s + Q_LPW / 2
    fill_pl = "rgba(29,78,216,0.16)"
    # 下翼板（上表面可見半邊、前緣）＋下翼續接板前緣
    _q_poly(cv, quad_uz(pf0, pf1, Q_BF / 2, -h - Q_TP, -h), fill_pl, 1.2)
    _q_poly(cv, quad_uz(u0, u1, Q_BF / 2, -h, -h + Q_TF))
    _q_poly(cv, quad_uv(u0, u1, Q_TW / 2, Q_BF / 2, -h + Q_TF))
    _q_poly(cv, quad_uv(pf0, pf1, Q_TW / 2 + 1.5, Q_BF / 2, -h + Q_TF + 0.01), fill_pl, 1.2)
    for uu in (pf0 + 4, pf0 + 9, pf0 + 14, pf1 - 14, pf1 - 9, pf1 - 4):
        cv.circle(_q_iso(P(uu, Q_BF * 0.33, -h + Q_TF)), 1.5, "#FFFFFF", C["member"], 1.0)
    # 腹板可見面＋續接縫＋腹續接板與螺栓
    _q_poly(cv, quad_uz(u0, u1, Q_TW / 2, -h + Q_TF, h - Q_TF))
    cv.line(_q_iso(P(s, Q_TW / 2, -h + Q_TF)), _q_iso(P(s, Q_TW / 2, h - Q_TF)), C["member"], 1.2)
    _q_poly(cv, quad_uz(pw0, pw1, Q_TW / 2 + Q_TP, -Q_HPW / 2, Q_HPW / 2), fill_pl, 1.4)
    for uu in (pw0 + 3.5, pw0 + 7, pw1 - 7, pw1 - 3.5):
        for k in range(6):
            zz = -Q_HPW / 2 + 3.5 + k * (Q_HPW - 7) / 5
            cv.circle(_q_iso(P(uu, Q_TW / 2 + Q_TP, zz)), 1.5, "#FFFFFF", C["member"], 1.0)
    # 上翼板（前緣、上表面）＋上翼續接板與螺栓
    _q_poly(cv, quad_uz(u0, u1, Q_BF / 2, h - Q_TF, h))
    _q_poly(cv, quad_uv(u0, u1, -Q_BF / 2, Q_BF / 2, h))
    cv.line(_q_iso(P(s, -Q_BF / 2, h)), _q_iso(P(s, Q_BF / 2, h)), C["member"], 1.0)
    _q_poly(cv, quad_uz(pf0, pf1, Q_BF / 2, h, h + Q_TP), fill_pl, 1.2)
    _q_poly(cv, quad_uv(pf0, pf1, -Q_BF / 2, Q_BF / 2, h + Q_TP), fill_pl, 1.4)
    for uu in (pf0 + 4, pf0 + 9, pf0 + 14, pf1 - 14, pf1 - 9, pf1 - 4):
        for vv in (-Q_BF * 0.27, Q_BF * 0.27):
            cv.circle(_q_iso(P(uu, vv, h + Q_TP)), 1.5, "#FFFFFF", C["member"], 1.0)
    # 梁端斷面（僅朝觀者的 +x、+y 梁可見）
    if e[0] + e[1] > 0:
        f, w = Q_BF / 2, Q_TW / 2
        prof = [(-f, -h), (f, -h), (f, -h + Q_TF), (w, -h + Q_TF), (w, h - Q_TF), (f, h - Q_TF), (f, h),
                (-f, h), (-f, h - Q_TF), (-w, h - Q_TF), (-w, -h + Q_TF), (-f, -h + Q_TF)]
        _q_poly(cv, [P(u1, v, z) for v, z in prof], "#FFFFFF", 1.5)


def _q_column(cv):
    a = Q_BC / 2
    t = 1.6
    _q_poly(cv, [(a, -a, -Q_HC), (a, a, -Q_HC), (a, a, Q_HC), (a, -a, Q_HC)])     # +x 面
    _q_poly(cv, [(-a, a, -Q_HC), (a, a, -Q_HC), (a, a, Q_HC), (-a, a, Q_HC)])     # +y 面
    _q_poly(cv, [(-a, -a, Q_HC), (a, -a, Q_HC), (a, a, Q_HC), (-a, a, Q_HC)], "#FFFFFF", 2.2)
    b = a - t
    _q_poly(cv, [(-b, -b, Q_HC), (b, -b, Q_HC), (b, b, Q_HC), (-b, b, Q_HC)], "#FFFFFF", 1.4)
    cv.line(_q_iso((a, a, -Q_HC)), _q_iso((a, a, Q_HC)), C["member"], 2.2)


def fig1_problem():
    path = os.path.join(OUT, "SS-2009-4-fig-1-problem.svg")
    cv = Canvas(760, 720, sx=2.0, ox=380, oy=335)
    cv.panel("梁柱接頭示意（等角圖）", "箱型柱貫通，四向 H 型梁；翼板、腹板皆以續接板＋螺栓接合")
    _q_beam(cv, (-1, 0), (0, 1))     # 左後
    _q_beam(cv, (0, -1), (1, 0))     # 右後
    _q_column(cv)
    _q_beam(cv, (0, 1), (1, 0))      # 左前
    _q_beam(cv, (1, 0), (0, 1))      # 右前
    compose([cv], cols=1,
            title="SS-2009-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1；考卷無尺寸，全圖為情境示意",
            note="附圖只是情境示意，五個小題都不必從圖上讀數值",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "誤以為要從附圖讀尺寸或螺栓間距作答"),
]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
    fig1_groove(); fig2_bolt_spacing(); fig3_preload()
    print(f"中心距：一般 {S_MIN_K:.4f}d（d={DB_EX:g}mm → {S_MIN_K*DB_EX:.1f}mm）；"
          f"沿力方向 {S_PREF_K:g}d → {S_PREF_K*DB_EX:g}mm")
    print(f"預拉力：0.7×{FU_A325:g}×A_t({AT_34:g}) = {T_AT:.1f} kips（表列 {T_TABLE:g} ✓）")
    print(f"        0.7×{FU_A325:g}×A_b({AB_34:g}) = {T_AB:.1f} kips（高估 "
          f"{100*(T_AB/T_AT-1):.0f}%）")
    print("done ->", OUT)
