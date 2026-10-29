#!/usr/bin/env python3
"""
SS-2023-3 非對稱 I 型斷面之降伏彎矩與塑性彎矩 — 解題圖解產生腳本

用法：
    python3 gen_SS-2023-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2023-3.md 哪一節
  2. ENA 由一次矩、PNA 由等面積法、I_x 由平行軸定理現算；
     改一個翼板寬度，兩條中性軸與應力分布會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2023-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2023-3.md，勿手動改動）
# ══════════════════════════════════════════════════════════
FY = 2.5                     # tf/cm^2（§1）
# §4 一：三塊子斷面（寬, 厚, 底緣高度）
PARTS = [("底翼板", 30.0, 5.0, 0.0),
         ("腹板",   2.0, 100.0, 5.0),
         ("頂翼板", 50.0, 5.0, 105.0)]
H_TOT = 110.0

AREAS = [b * t for _, b, t, _ in PARTS]
YBARS = [y0 + t / 2 for _, _, t, y0 in PARTS]
A_TOT = sum(AREAS)                                   # 600 cm^2
# §4 二：彈性中性軸＝形心
ENA = sum(a * y for a, y in zip(AREAS, YBARS)) / A_TOT       # 63.75 cm
C_BOT, C_TOP = ENA, H_TOT - ENA                              # 63.75 / 46.25
# §4 三：平行軸定理
IX = sum(b * t ** 3 / 12 + (b * t) * (y0 + t / 2 - ENA) ** 2
         for _, b, t, y0 in PARTS)                            # 1,224,062.5 cm^4
# §4 四
S_BOT, S_TOP = IX / C_BOT, IX / C_TOP                        # 19,201 / 26,466
def _r(x): return math.floor(x + 0.5)          # 半數進位（Python round 為銀行家進位）
MY = _r(FY * _r(min(S_BOT, S_TOP)))                          # 48,003 tf·cm（同 .md 取法）
SIG_TOP_AT_MY = FY * C_TOP / C_BOT                           # 1.814 tf/cm^2（頂緣尚未降伏）
# §4 五：等面積法求 PNA
_half = A_TOT / 2                                            # 300 cm^2
_acc, PNA = 0.0, None
for _, b, t, y0 in PARTS:                                    # 由底往上累加
    if _acc + b * t >= _half:
        PNA = y0 + (_half - _acc) / b
        break
    _acc += b * t
H_WEB_LO = PNA - PARTS[1][3]                                 # 腹板下段 75 cm
H_WEB_HI = (PARTS[1][3] + PARTS[1][2]) - PNA                 # 腹板上段 25 cm
# §4 六：Z 的四項組成（面積, 形心至 PNA 距離, 名稱）
Z_ITEMS = [("底翼板", 150.0, PNA - 2.5),
           (f"腹板下段（{H_WEB_LO:.0f}×2）", 2 * H_WEB_LO, PNA - (5 + H_WEB_LO / 2)),
           (f"腹板上段（{H_WEB_HI:.0f}×2）", 2 * H_WEB_HI, (PNA + H_WEB_HI / 2) - PNA),
           ("頂翼板", 250.0, 107.5 - PNA)]
Z = sum(a * d for _, a, d in Z_ITEMS)                        # 24,750 cm^3
MP = FY * Z                                                  # 61,875 tf·cm
SHAPE = MP / MY                                              # 1.289

# 繪圖用比例
SXX, PW, PH = 3.4, 380, 560
OXX, OYY = 190.0, 100.0
K_SIG = 8.0                  # 1 tf/cm^2 對應 8 個模型單位（與斷面寬度可比）


def _panel(title, sub):
    cv = Canvas(PW, PH, sx=SXX, ox=OXX, oy=OYY)
    cv.panel(title, sub)
    return cv


def _rect(cv, x0, x1, y0, y1, fill, stroke="none", w=1.4):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w)


def _section(cv, fill=C["fill_c"], stroke=C["member"], w=1.8):
    for _, b, t, y0 in PARTS:
        _rect(cv, -b / 2, b / 2, y0, y0 + t, fill, stroke, w)


def _axis(cv, y, col, lab, sub=None, half=30.0):
    cv.line((-half, y), (half, y), col, 2.4, dash="7 4")
    cv.text_px(cv.X(half) + 6, cv.Y(y) - (8 if sub else 0), lab, 12.5, col,
               "start", weight="700")
    if sub:
        cv.text_px(cv.X(half) + 6, cv.Y(y) + 11, sub, 11.5, col, "start")


# ══════════════════════════════════════════════════════════
def fig2_stress():
    """斷面／彈性應力／塑性應力：三格共用同一縱向比例，兩條中性軸的高低一目了然"""
    # ── ① 斷面與兩條中性軸 ──
    a = _panel("① 斷面與兩條中性軸", "縱向比例三格共用，可直接比高低")
    _section(a)
    a.dim((-25, 0), (-25, H_TOT), f"{H_TOT:.0f}", off=-40, label_off=-16)   # 總高：左側外
    a.dim((-25, 105), (25, 105), "50", off=22, label_off=12)               # 頂翼板寬：標在其下
    a.dim((-15, 5), (15, 5), "30", off=-22, label_off=-12)                 # 底翼板寬：標在其上
    a.dim((1, 5), (1, 105), "100", off=30, label_off=14)                   # 腹板高：腹板右側
    for _, b, t, y0 in PARTS:
        if t == 5.0:
            a.dim((b / 2, y0), (b / 2, y0 + t), "5", off=0, label_off=16)
    a.text_px(a.X(1) + 74, a.Y(20), "t_w = 2", 11.5, C["muted"], "start")
    _axis(a, ENA, C["bmd"], "ENA", f"{ENA:.2f} cm")
    _axis(a, PNA, C["accent"], "PNA", f"{PNA:.0f} cm")
    a.text_px(PW / 2, PH - 76, "ENA：一次矩為零（形心軸）", 12, C["bmd"], weight="700")
    a.text_px(PW / 2, PH - 54, "PNA：上下面積各半（等面積軸）", 12, C["accent"], weight="700")
    a.math_px(PW / 2, PH - 28, f"I_x = {IX:,.0f} cm^{{4}}", 13.5, C["muted"], weight="700")

    # ── ② 彈性應力分布 ──
    b = _panel("② 彈性：M = M_y", "應力線性，繞 ENA 旋轉")
    _section(b, "#FFFFFF", C["ghost"], 1.2)
    b.line((-30, ENA), (30, ENA), C["bmd"], 2.0, dash="7 4")
    top_x = -SIG_TOP_AT_MY * K_SIG
    bot_x = FY * K_SIG
    b.polygon([(0, ENA), (top_x, H_TOT), (0, H_TOT)], C["fill_c"], C["compr"], 2.0)
    b.polygon([(0, ENA), (bot_x, 0), (0, 0)], C["fill_t"], C["tension"], 2.0)
    b.line((0, 0), (0, H_TOT), C["muted"], 1.4)
    b.math_px(b.X(top_x) - 6, b.Y(H_TOT), f"{SIG_TOP_AT_MY:.3f}", 12.5, C["compr"],
              "end", weight="700")
    b.text_px(b.X(top_x) - 6, b.Y(H_TOT) + 16, "壓（未降伏）", 11.5, C["compr"], "end")
    b.math_px(b.X(bot_x) + 6, b.Y(0), f"F_y = {FY}", 12.5, C["tension"], "start", weight="700")
    b.text_px(b.X(bot_x) + 6, b.Y(0) - 16, "拉（先降伏）", 11.5, C["tension"], "start",
              weight="700")
    b.text_px(PW / 2, PH - 76,
              f"c_{{bot}} = {C_BOT:.2f} 大於 c_{{top}} = {C_TOP:.2f} ⇒ 底緣先到 F_y",
              12, C["muted"])
    b.math_px(PW / 2, PH - 52,
              f"S_{{bot}} = {S_BOT:,.0f} 小於 S_{{top}} = {S_TOP:,.0f} cm^{{3}}", 12.5,
              C["muted"], weight="700")
    b.math_px(PW / 2, PH - 26, f"M_y = F_y S_{{bot}} = {MY:,.0f} tf·cm", 14,
              C["tension"], weight="700")

    # ── ③ 塑性應力分布 ──
    c = _panel("③ 塑性：M = M_p", "全斷面降伏，繞 PNA 分界")
    _section(c, "#FFFFFF", C["ghost"], 1.2)
    c.line((-30, PNA), (30, PNA), C["accent"], 2.4, dash="7 4")
    sx_ = FY * K_SIG
    _rect(c, -sx_, 0, PNA, H_TOT, C["fill_c"], C["compr"], 2.0)
    _rect(c, 0, sx_, 0, PNA, C["fill_t"], C["tension"], 2.0)
    c.line((0, 0), (0, H_TOT), C["muted"], 1.4)
    c.math_px(c.X(-sx_) - 6, c.Y((PNA + H_TOT) / 2), f"F_y = {FY}", 12.5, C["compr"],
              "end", weight="700")
    c.text_px(c.X(-sx_) - 6, c.Y((PNA + H_TOT) / 2) + 16, "全部受壓", 11.5, C["compr"], "end")
    c.math_px(c.X(sx_) + 6, c.Y(PNA / 2), f"F_y = {FY}", 12.5, C["tension"], "start",
              weight="700")
    c.text_px(c.X(sx_) + 6, c.Y(PNA / 2) + 16, "全部受拉", 11.5, C["tension"], "start")
    c.text_px(PW / 2, PH - 76,
              f"PNA 上下各 {A_TOT/2:.0f} cm² ⇒ 合力自動平衡", 12, C["muted"])
    c.math_px(PW / 2, PH - 52, f"Z = Σ A_i d_i = {Z:,.0f} cm^{{3}}", 12.5, C["muted"],
              weight="700")
    c.math_px(PW / 2, PH - 26, f"M_p = F_y Z = {MP:,.0f} tf·cm", 14, C["accent"],
              weight="700")

    compose([a, b, c], cols=3,
            title="彈性中性軸與塑性中性軸不是同一條——本題差了 16.25 cm",
            sub="ENA 由一次矩定（形心軸），PNA 由等面積定；頂翼板較寬 ⇒ 形心偏上、"
                "等面積軸更偏上",
            note=f"形狀因子 = 塑性彎矩／降伏彎矩 = {MP:,.0f}／{MY:,.0f} = {SHAPE:.3f}"
                 f"（介於對稱 I 型的約 1.12 與矩形的 1.50 之間）",
            path=f"{OUT}/{TAG}-fig-2-ena-pna.svg")
    return f"{OUT}/{TAG}-fig-2-ena-pna.svg"


# ══════════════════════════════════════════════════════════
def fig3_equal_area():
    """等面積法定 PNA，以及 Z 的四項組成——腹板一定要拆成上下兩段"""
    PW3, PH3 = 470, 560

    # ── ① 等面積法 ──
    a = Canvas(PW3, PH3, sx=SXX, ox=200.0, oy=OYY)
    a.panel("① 等面積法：由底往上累加到 A/2", "腹板必須在 PNA 處切開")
    for _, b, t, y0 in PARTS:
        if y0 + t <= PNA or y0 >= PNA:
            fill = C["fill_t"] if y0 + t <= PNA else C["fill_c"]
            _rect(a, -b / 2, b / 2, y0, y0 + t, fill, C["member"], 1.8)
        else:                                   # 腹板：在 PNA 處切成上下兩段
            _rect(a, -b / 2, b / 2, y0, PNA, C["fill_t"], C["member"], 1.8)
            _rect(a, -b / 2, b / 2, PNA, y0 + t, C["fill_c"], C["member"], 1.8)
    a.line((-30, PNA), (34, PNA), C["accent"], 2.6, dash="7 4")
    a.text_px(a.X(34) + 6, a.Y(PNA) - 8, "PNA", 12.5, C["accent"], "start", weight="700")
    a.text_px(a.X(34) + 6, a.Y(PNA) + 11, f"距底緣 {PNA:.0f} cm", 11.5, C["accent"], "start")
    a.line((-30, ENA), (34, ENA), C["bmd"], 1.8, dash="4 4")
    a.text_px(a.X(34) + 6, a.Y(ENA), f"ENA {ENA:.2f}", 11.5, C["bmd"], "start", weight="700")
    for lab, ar, yy, col in (("底翼板 150", 150, 2.5, C["tension"]),
                             (f"腹板下段 {2*H_WEB_LO:.0f}", 2 * H_WEB_LO, 5 + H_WEB_LO / 2,
                              C["tension"]),
                             (f"腹板上段 {2*H_WEB_HI:.0f}", 2 * H_WEB_HI, PNA + H_WEB_HI / 2,
                              C["compr"]),
                             ("頂翼板 250", 250, 107.5, C["compr"])):
        a.text_px(a.X(-26) - 6, a.Y(yy), lab, 11.5, col, "end", weight="700")
    a.dim((13, 5), (13, PNA), f"{H_WEB_LO:.0f}", off=20, label_off=14)
    a.text_px(PW3 / 2, PH3 - 76,
              f"以下：150 + {2*H_WEB_LO:.0f} = {A_TOT/2:.0f} cm²", 12.5, C["tension"],
              weight="700")
    a.text_px(PW3 / 2, PH3 - 52,
              f"以上：{2*H_WEB_HI:.0f} + 250 = {A_TOT/2:.0f} cm²", 12.5, C["compr"],
              weight="700")
    a.text_px(PW3 / 2, PH3 - 26, f"PNA 距底緣 = 5 + {H_WEB_LO:.0f} = {PNA:.0f} cm",
              13.5, C["accent"], weight="700")

    # ── ② Z 的四項組成 ──
    b = Canvas(PW3, PH3, sx=1.0, ox=0.0, oy=0.0)
    b.panel("② Z 的四項組成", "Z = Σ A_i × |形心至 PNA 的距離|")
    x0, bw = 214.0, 176.0
    peak = max(ar * d for _, ar, d in Z_ITEMS)
    for i, (nm, ar, d) in enumerate(Z_ITEMS):
        y = 116 + i * 62
        col = C["compr"] if i >= 2 else C["tension"]
        b.text_px(28, y - 9, nm, 12.5, C["text"], "start", weight="700")
        b.text_px(28, y + 12, f"A = {ar:.0f} cm²　d = {d:.1f} cm", 11.5, C["muted"], "start")
        b.rect_px(x0, y - 15, bw, 30, "#EDF1F6", 6)
        b.rect_px(x0, y - 15, bw * ar * d / peak, 30, col, 6)
        b.math_px(x0 + bw + 12, y, f"{ar*d:,.0f}", 13, col, "start", weight="700")
    b.text_px(28, 116 + 4 * 62 - 6, "合計", 13, C["accent"], "start", weight="700")
    b.math_px(PW3 - 16, 116 + 4 * 62 - 6, f"{Z:,.0f} cm^{{3}}", 14, C["accent"],
              "end", weight="700")
    b.text_px(PW3 / 2, PH3 - 76, "Z 不是 I_x / c —— 那是彈性的 S", 12.5, C["muted"])
    b.math_px(PW3 / 2, PH3 - 52, f"M_p = F_y Z = {FY} × {Z:,.0f} = {MP:,.0f} tf·cm",
              13, C["accent"], weight="700")
    b.text_px(PW3 / 2, PH3 - 26, f"＝ {MP/100:,.2f} tf·m", 13, C["accent"], weight="700")

    compose([a, b],
            title="腹板一定要在 PNA 處拆成兩段——這是 Z 算錯的頭號原因",
            sub=f"由底往上累加：底翼板 150 cm² 不足 {A_TOT/2:.0f}，"
                f"還差 {A_TOT/2-150:.0f} cm² ⇒ 進入腹板 {A_TOT/2-150:.0f}/2 = "
                f"{H_WEB_LO:.0f} cm，PNA 落在腹板內",
            note=f"四項乘積一律取正值（都是「離開 PNA 的距離」），"
                 f"上下各自加總後相加即得 Z = {Z:,.0f} cm³",
            path=f"{OUT}/{TAG}-fig-3-equal-area.svg")
    return f"{OUT}/{TAG}-fig-3-equal-area.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_stress, "§4 二～六·§5",
     "把 ENA 當成 PNA（或反過來）；以及誤以為頂緣先降伏"),
    (fig3_equal_area, "§4 五～六·§3 陷阱3",
     "算 Z 時沒把腹板在 PNA 處拆成上下兩段"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ref = [("A", A_TOT, 600), ("ENA", ENA, 63.75), ("I_x", IX, 1224062),
           ("S_top", S_TOP, 26466), ("S_bot", S_BOT, 19201), ("M_y", MY, 48003),
           ("PNA", PNA, 80), ("腹板下段", H_WEB_LO, 75), ("腹板上段", H_WEB_HI, 25),
           ("Z", Z, 24750), ("M_p", MP, 61875), ("形狀因子", SHAPE, 1.289),
           ("σ_top@M_y", SIG_TOP_AT_MY, 1.814)]
    print("現算值 vs SS-2023-3.md 表列值：")
    for nm, got, want in ref:
        ok = "OK " if abs(got - want) <= max(abs(want) * 0.002, 0.02) else "!! "
        print(f"  {ok}{nm:<10} {got:>12,.4g}   （.md: {want:,}）")
    print("  Z 四項：" + "、".join(f"{a*d:,.0f}" for _, a, d in Z_ITEMS)
          + "（.md: 11,625、5,625、625、6,875）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<40} {section:<20} 攔：{catches}")
