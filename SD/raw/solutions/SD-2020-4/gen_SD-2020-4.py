#!/usr/bin/env python3
"""SD-2020-4 圖解產生器 — 三水準地震：需求 vs 設計力、V*/V 與 VM/V 隨 R、設計反應譜、韌性額度
圖上每個數字由 R 與規範關係式算出；改 R 重跑，四張圖同時更新。
2026-11-16 勘誤：刪除 SaM = 1.5 SaD（ASCE 7 的 SDS = 2/3 SMS，不是我國規範）。
我國規範 S_S^D、S_1^D 與 S_S^M、S_1^M 依鄉鎮市區分別查表，比值不固定；
VM/V 改以 S_aM/S_aD 的示意值 RHO_LO～RHO_HI 畫帶狀範圍，並標出兩平條件 S_aM/S_aD = R/Ra。
"""
import sys, os, math
SKILL = os.environ.get("STRUCTDRAW",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ── 規範關係（建築物耐震設計規範及解說，111 年版）──────────────────
RATIO_D_OVER_SMALL = 3.0      # 一般工址：4.2 = 1.4 × 3
RHO_LO, RHO_HI     = 1.2, 1.5 # S_aM/S_aD 示意值（實際依工址查表 2-1，非規範固定值）
R_MAIN, R_ALT      = 4.8, 2.4


def ra_of(R):
    return 1 + (R - 1) / 1.5


def fu_long(R):
    return ra_of(R)


def fu_mid(R):
    return math.sqrt(2 * ra_of(R) - 1)


def vstar_over_v(R, seg="long"):
    return (fu_long(R) if seg == "long" else fu_mid(R)) / RATIO_D_OVER_SMALL


def vm_over_v(R, rho):
    """長週期、(·)_m 第一段：VM/V = (SaM/SaD) × Ra/R"""
    return rho * ra_of(R) / R


def breakeven(R):
    """VM = V 時的 SaM/SaD = R/Ra"""
    return R / ra_of(R)


# ══════════════════════════════════════════════════════════
# 圖 1：地震需求差很多，設計力卻差不多，次序可翻轉
# ══════════════════════════════════════════════════════════
def fig1():
    W, HH = 1120, 580
    cv = Canvas(W, HH, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "圖 1　三水準地震：需求相差數倍，設計檢核力卻接近，次序可以翻轉",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"以 R = {R_MAIN}（特殊抗彎矩構架）、長週期段為例；設計地震力 V 取為 1.00；"
               f"SaM/SaD 取 {RHO_LO}～{RHO_HI} 為示意（實際依工址查表）",
               13, C["muted"])
    vm_lo, vm_hi = vm_over_v(R_MAIN, RHO_LO), vm_over_v(R_MAIN, RHO_HI)
    rows = [
        ("中小度地震", "回歸期約 30 年 ｜ 50 年超越機率約 80%", "小震不壞（結構體保持彈性）",
         (1 / RATIO_D_OVER_SMALL,) * 2, (vstar_over_v(R_MAIN),) * 2, "V*", C["sfd"]),
        ("設計地震", "回歸期 475 年 ｜ 50 年超越機率約 10%", "中震可修（韌性需求 ≤ Ra）",
         (1.0, 1.0), (1.0, 1.0), "V", C["bmd"]),
        ("最大考量地震", "回歸期 2500 年 ｜ 50 年超越機率約 2%", "大震不倒（韌性可用滿 R）",
         (RHO_LO, RHO_HI), (vm_lo, vm_hi), "VM", C["load"]),
    ]
    dpeak, fpeak = RHO_HI, max(vstar_over_v(R_MAIN), vm_hi)
    xd, xf, bw = 360, 730, 230
    cv.text_px(xd + bw / 2, 100, "地震需求（譜加速度相對 SaD）", 13.5, C["text"], weight="700")
    cv.text_px(xf + bw / 2, 100, "設計檢核力（相對 V）", 13.5, C["text"], weight="700")
    for i, (name, prob, perf, dem, frc, sym, col) in enumerate(rows):
        y = 152 + i * 116
        cv.text_px(28, y - 12, name, 15, C["text"], "start", weight="700")
        cv.text_px(28, y + 10, prob, 11.8, C["muted"], "start")
        cv.text_px(28, y + 30, perf, 11.8, col, "start", weight="700")
        for x0, (a, b), peak, kind in ((xd, dem, dpeak, "d"), (xf, frc, fpeak, "f")):
            if kind == "d":
                lab = f"{a:.2f}" if a == b else f"{a:.1f}～{b:.1f}"
            else:
                lab = f"{sym} = {a:.3f}" if a == b else f"{sym} = {a:.3f}～{b:.3f}"
            cv.rect_px(x0, y - 17, bw, 34, "#EDF1F6", 8)
            cv.rect_px(x0, y - 17, bw * b / peak, 34, col, 8)
            if a != b:   # 範圍段畫淡色
                cv.parts.append(f'<rect x="{x0 + bw*a/peak:.1f}" y="{y-17}" width="{bw*(b-a)/peak:.1f}" '
                                f'height="34" fill="#FFFFFF" opacity="0.55"/>')
            cv.text_px(x0 + bw + 12, y, lab, 13.5, col, "start", weight="700")
    xv = xf + bw * 1.0 / fpeak
    cv.parts.append(f'<line x1="{xv:.1f}" y1="125" x2="{xv:.1f}" y2="{152+2*116+24}" stroke="{C["bmd"]}" '
                    f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    cv.text_px(xv, 120, "V = 1", 11.5, C["bmd"])
    cv.text_px(W / 2, 500,
               f"V* ({vstar_over_v(R_MAIN):.3f}) ＞ V；VM 在 {vm_lo:.3f}～{vm_hi:.3f}，"
               f"SaM/SaD ＜ R/Ra = {breakeven(R_MAIN):.3f} 時 VM ＜ V",
               14, C["text"], weight="700")
    cv.text_px(W / 2, HH - 26,
               "攔錯：以為 VM ＞ V ＞ V* 恆成立，或把 SaM/SaD 背成固定 1.5（那是 ASCE 7 的 SDS = 2/3 SMS）",
               13.5, C["muted"])
    cv.save(f"{OUT}/SD-2020-4-fig-1-three-levels.svg")


# ══════════════════════════════════════════════════════════
# 圖 2：V*/V 與 VM/V 隨韌性容量 R 的變化
# ══════════════════════════════════════════════════════════
def fig2():
    W, HH = 960, 610
    R0, R1 = 1.0, 5.2
    ymax = 1.65
    L, R_, T_, B = 96, 238, 100, 130
    sx = (HH - T_ - B) / ymax
    XSC = (W - L - R_) / (sx * (R1 - R0))
    cv = Canvas(W, HH, sx=sx, ox=L, oy=B)
    XM = lambda r: (r - R0) * XSC

    cv.text_px(W / 2, 34, "圖 2　三個檢核力的相對大小隨韌性容量 R 變化（長週期段）", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"縱軸為與設計地震力 V 的比值（V ≡ 1.00）；VM/V 以 SaM/SaD = {RHO_LO}～{RHO_HI} 示意",
               13, C["muted"])
    cv.axes((0, 0), XM(R1) * 0.99, ymax * 0.99, ("R", "V_i/V"), C["muted"], 1.8)

    rs = [R0 + i * (R1 - R0) / 400 for i in range(401)]
    lo = [(XM(r), vm_over_v(r, RHO_LO)) for r in rs]
    hi = [(XM(r), vm_over_v(r, RHO_HI)) for r in rs]
    cv.polygon(hi + lo[::-1], "rgba(192,57,43,0.12)", "none")
    cv.line((0, 1.0), (XM(R1) * 0.99, 1.0), C["bmd"], 3.0)
    cv.math_px(cv.X(XM(R1) * 0.99) + 10, cv.Y(1.0), "V = 1.00（基準）", 13.5, C["bmd"], "start", weight="700")
    curves = [
        ([(XM(r), vstar_over_v(r, "long")) for r in rs], C["sfd"], 4.2, None, "V*/V ＝ Fu/3（長週期）"),
        ([(XM(r), vstar_over_v(r, "mid")) for r in rs], C["sfd"], 2.8, "9 6", "V*/V（中週期，參考）"),
        (hi, C["load"], 3.4, None, f"VM/V，SaM/SaD = {RHO_HI}"),
        (lo, C["load"], 3.4, "9 6", f"VM/V，SaM/SaD = {RHO_LO}"),
    ]
    for pts, col, wdt, dsh, _ in curves:
        cv.poly(pts, col, wdt, dash=dsh)
    cv.text_px(cv.X(XM(R1)) + 8, cv.Y(vm_over_v(R1, RHO_HI)) - 2, f"{RHO_HI}", 12, C["load"], "start", weight="700")
    cv.text_px(cv.X(XM(R1)) + 8, cv.Y(vm_over_v(R1, RHO_LO)) + 10, f"{RHO_LO}", 12, C["load"], "start", weight="700")

    RC = 4.0
    cv.line((XM(RC), 0), (XM(RC), 1.16), C["accent"], 2.0, dash="6 5")
    cv.dot((XM(RC), 1.0), 5.6, C["accent"])
    cv.text_px(cv.X(XM(RC)), cv.Y(1.22), f"R = {RC}", 13, C["accent"], weight="700")
    cv.text_px(cv.X(XM(RC)), cv.Y(1.30), "V* = V 的臨界", 11.8, C["accent"])

    for R in (R_MAIN, R_ALT):
        cv.dot((XM(R), vstar_over_v(R, "long")), 5.2, C["sfd"])
        cv.dot((XM(R), vm_over_v(R, RHO_LO)), 4.6, C["load"])
        cv.dot((XM(R), vm_over_v(R, RHO_HI)), 4.6, C["load"])
        cv.text_px(cv.X(XM(R)), cv.Y(0) + 42, f"R = {R}", 12.5, C["text"], weight="700")
    for r in (1, 2, 3, 4, 5):
        cv.line((XM(r), -0.018), (XM(r), 0.018), C["muted"], 1.2)
        cv.text_px(cv.X(XM(r)), cv.Y(0) + 22, str(r), 11.5, C["muted"])
    for yv in (0.5, 1.0, 1.5):
        cv.line((-0.02 * XSC, yv), (0.02 * XSC, yv), C["muted"], 1.2)
        cv.text_px(cv.X(0) - 12, cv.Y(yv), f"{yv:.1f}", 11.5, C["muted"], "end")
    cv.text_px(cv.X(XM(4.55)), cv.Y(1.32), "V* ＞ V", 13, C["sfd"], weight="700")
    cv.text_px(cv.X(XM(4.6)), cv.Y(0.62), "V* ＜ V", 13, C["sfd"], weight="700")
    cv.legend(cv.X(XM(2.45)), cv.Y(0.42), [(c[1], c[4]) for c in curves] + [(C["bmd"], "V（設計地震，基準）")])
    cv.text_px(W / 2, HH - 40,
               "紅色帶跨過 1.0：VM 可大於也可小於 V（長週期 VM ＞ V ⇔ SaM/SaD ＞ R/Ra）",
               13.5, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               "攔錯：直接拿表列的 R 當 Fu（R = 4.8 的 Fu 是 3.53 或 2.46）；把 VM ＞ V 當成恆成立",
               13, C["muted"])
    cv.save(f"{OUT}/SD-2020-4-fig-2-ratio-curve.svg")


# ══════════════════════════════════════════════════════════
# 圖 3：設計反應譜 SaD(T) 的四段式
# ══════════════════════════════════════════════════════════
def fig3():
    W, HH = 940, 540
    XR, ymax = 3.4, 1.32
    L, R_, T_, B = 96, 176, 100, 104
    sx = (HH - T_ - B) / ymax
    XSC = (W - L - R_) / (sx * XR)
    cv = Canvas(W, HH, sx=sx, ox=L, oy=B)
    XM = lambda x: x * XSC

    def sa(x):                       # SaD / SDS，x = T/T0D
        if x < 0.2:
            return 0.4 + 3 * x
        if x <= 1.0:
            return 1.0
        if x <= 2.5:
            return 1.0 / x
        return 0.4

    cv.text_px(W / 2, 34, "圖 3　設計反應譜 SaD(T) 的四段式", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "縱軸為 SaD/SDS，橫軸為 T/T0D；T0D = SD1/SDS（地盤愈軟，T0D 愈大）",
               13, C["muted"])
    cv.axes((0, 0), XM(XR) * 0.99, ymax * 0.82, ("T/T0D", "S_{aD}/S_{DS}"), C["muted"], 1.8)

    xs = [i * XR / 600 for i in range(601)]
    pts = [(XM(x), sa(x)) for x in xs]
    cv.polygon([(0, 0)] + pts + [(XM(XR), 0)], C["fill_m"], "none")
    cv.poly(pts, C["bmd"], 4.2)

    segs = [(0.0, 0.2, "上升段", "S_{DS}(0.4+3T/T0D)"),
            (0.2, 1.0, "等加速度平台", "S_{DS}"),
            (1.0, 2.5, "等速度段", "S_{D1}/T"),
            (2.5, XR, "長週期下限", "0.4S_{DS}")]
    for x0, x1, name, expr in segs:
        if x0 > 0:
            cv.line((XM(x0), 0), (XM(x0), sa(x0) + 0.10), C["border"], 1.6, dash="6 5")
        cv.text_px(cv.X(XM((x0 + x1) / 2)), cv.Y(ymax * 0.96), name, 12.5, C["text"], weight="700")
        cv.math_px(cv.X(XM((x0 + x1) / 2)), cv.Y(ymax * 0.88), expr, 12.5, C["bmd"])

    for xb, lab in ((0.2, "0.2 T0D"), (1.0, "T0D"), (2.5, "2.5 T0D")):
        cv.text_px(cv.X(XM(xb)), cv.Y(0) + 22, lab, 12.5, C["muted"])
    for yv, lab in ((0.4, "0.4"), (1.0, "1.0")):
        cv.line((-0.02 * XSC, yv), (0.02 * XSC, yv), C["muted"], 1.2)
        cv.text_px(cv.X(0) - 12, cv.Y(yv), lab, 11.5, C["muted"], "end")
        cv.line((0, yv), (XM(XR) * 0.99, yv), C["border"], 1.2, dash="4 4")

    # 因子進入點
    cv.rect_px(W - 168, 132, 150, 118, C["panel"], 12, C["border"], 1.2)
    cv.text_px(W - 158, 156, "因子進入點", 12.8, C["text"], "start", weight="700")
    for k, (s_, col) in enumerate([("震區 → SSD, S1D", C["muted"]),
                                   ("地盤 → Fa, Fv", C["muted"]),
                                   ("近斷層 → NA, NV", C["muted"]),
                                   ("週期 → 落在哪段", C["accent"])]):
        cv.text_px(W - 158, 180 + k * 20, s_, 11.5, col, "start")

    cv.text_px(W / 2, HH - 26,
               "攔錯：把譜形背成三段、或把分界寫成固定秒數。分界永遠相對於 T0D = SD1/SDS",
               13.5, C["muted"])
    cv.save(f"{OUT}/SD-2020-4-fig-3-design-spectrum.svg")


# ══════════════════════════════════════════════════════════
# 圖 4：韌性額度的 2/3 : 1/3 分配，與 VM/V 的兩平條件
# ══════════════════════════════════════════════════════════
def fig4():
    W, HH = 960, 480
    cv = Canvas(W, HH, sx=1, bg="#FFFFFF")
    R = R_MAIN
    RA = ra_of(R)
    cv.text_px(W / 2, 34, "圖 4　Ra：設計地震只准用掉非彈性變形額度的 2/3",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"R = {R} → Ra = 1 + (R−1)/1.5 = {RA:.3f}（臺北盆地分母 2.0）", 13, C["muted"])

    x0, bw, y = 140, 680, 168
    unit = bw / (R - 1)
    cv.rect_px(x0, y - 26, bw, 52, "#EDF1F6", 10)
    cv.rect_px(x0, y - 26, unit * (RA - 1), 52, C["bmd"], 10)
    cv.text_px(x0 + unit * (RA - 1) / 2, y, f"設計地震可用 {RA-1:.3f}（= 2/3）", 13.5, "#FFFFFF", weight="700")
    cv.text_px(x0 + unit * (RA - 1) + (bw - unit * (RA - 1)) / 2, y,
               f"留給最大考量地震 {R - RA:.3f}（= 1/3）", 13.5, C["text"], weight="700")
    cv.text_px(x0 - 14, y, "韌性額度", 13.5, C["text"], "end", weight="700")
    cv.text_px(x0 - 14, y + 20, f"R − 1 = {R-1:.1f}", 12, C["muted"], "end")
    cv.text_px(x0 + bw + 12, y, f"R = {R}", 13.5, C["load"], "start", weight="700")

    # 下排：VM/V 的兩平條件（長週期）
    y2 = 300
    be = breakeven(R)
    smax = 1.6
    sc = bw / smax
    cv.rect_px(x0, y2 - 22, bw, 44, "#EDF1F6", 10)
    cv.rect_px(x0, y2 - 22, sc * be, 44, C["sfd"], 10)
    cv.text_px(x0 + sc * be / 2, y2, f"SaM/SaD ＜ R/Ra = {be:.3f} → VM ＜ V", 13.5, "#FFFFFF", weight="700")
    cv.text_px(x0 + sc * be + (bw - sc * be) / 2, y2, "VM ＞ V", 13.5, C["text"], weight="700")
    cv.text_px(x0 - 14, y2, "SaM/SaD", 13.5, C["text"], "end", weight="700")
    cv.text_px(x0 - 14, y2 + 20, "（依工址查表）", 12, C["muted"], "end")
    for v in (0.0, 0.5, 1.0, 1.2, 1.4, 1.6):
        xx = x0 + sc * v
        cv.parts.append(f'<line x1="{xx:.1f}" y1="{y2+24}" x2="{xx:.1f}" y2="{y2+30}" stroke="{C["muted"]}" stroke-width="1.2"/>')
        cv.text_px(xx, y2 + 42, f"{v:.1f}", 11.5, C["muted"])
    cv.text_px(W / 2, 240, "多准用的 1/3 韌性（FuM 以 R 計、Fu 以 Ra 計）抵銷了最大考量地震多出的需求",
               13.5, C["accent"], weight="700")
    cv.text_px(W / 2, 384, f"長週期：VM/V = (SaM/SaD) × Ra/R；R = {R} 時兩平比值 {be:.3f}",
               13.5, C["text"], weight="700")
    cv.text_px(W / 2, HH - 26,
               "攔錯：在設計地震就把 R 用滿；或把 SaM/SaD 背成固定 1.5，推出「VM ＞ V 恆成立」",
               13.5, C["muted"])
    cv.save(f"{OUT}/SD-2020-4-fig-4-ductility-budget.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2(); fig3(); fig4()
    for R in (R_MAIN, 4.0, 3.2, R_ALT, 2.0):
        print(f"R={R}: Ra={ra_of(R):.4f} Fu_L={fu_long(R):.3f} Fu_M={fu_mid(R):.3f} "
              f"V*/V(L)={vstar_over_v(R):.3f} V*/V(M)={vstar_over_v(R,'mid'):.3f} "
              f"VM/V(rho={RHO_LO})={vm_over_v(R,RHO_LO):.3f} VM/V(rho={RHO_HI})={vm_over_v(R,RHO_HI):.3f} R/Ra={breakeven(R):.4f}")
