#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2020-4 圖解產生腳本（四鈑續接：腹板鈑之螺栓尺寸與鈑厚）

斷面性質、三項作用力、螺栓群向量與鈑厚全部由下方常數區重算；改螺栓排數重跑，圖跟著變。
執行：python3 gen_SS-2020-4.py   →   figs/*.svg
"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = os.path.join(_HERE, "figs")

# ══════════════════════════════════════════════════════════════
# L1：題目給定（§1）
# ══════════════════════════════════════════════════════════════
D_, BF, TW, TF = 70.0, 30.0, 1.4, 2.5     # cm  H700x300x14x25
FY   = 2.5        # tf/cm^2
FVA  = 2.8        # tf/cm^2  A490-X 承壓型（題給）
MW   = 60.0       # tf·m 工作彎矩
VW   = 70.0       # tf   工作剪力
NB   = 6          # 每側螺栓數（2 縱列 × 6 橫排，每列負責一端）
SP   = 8.0        # cm 沿梁高之螺栓間距
EDGE = 4.0        # cm 邊距
ECC  = 5.0        # cm 螺栓列至續接中心線
NS   = 2          # 雙剪（腹板兩側各一片鈑）
COL_GAP = 10.0    # cm 兩縱列間距

# ── Step 1：斷面性質 ──
HW   = D_ - 2*TF                                    # 65
IX   = (BF*D_**3 - (BF-TW)*HW**3)/12                # 202,977
SX   = IX/(D_/2)                                    # 5,799
IW   = TW*HW**3/12                                  # 32,040
RATIO_W = IW/IX                                     # 0.1578

# ── Step 2：最小接合強度規定（M、V 雙向）──
MA   = 0.66*FY*SX                                   # 9,569 tf·cm
VA   = 0.4*FY*D_*TW                                 # 98 tf
M_DES = max(MW*100, 0.5*MA)                         # tf·cm
V_DES = max(VW, 0.5*VA)                             # tf

# ── Step 3～4：腹板鈑所受之作用力 ──
H_PL = 2*EDGE + (NB-1)*SP                           # 48 鈑高
W_PL = 2*EDGE + COL_GAP                             # 18 鈑寬
YS   = [(-(NB-1)/2 + i)*SP for i in range(NB)]      # ±4, ±12, ±20
SUM_Y2 = sum(y*y for y in YS)                       # 1,120
M_WEB = M_DES*RATIO_W                               # 947
M_ECC = V_DES*ECC                                   # 350
M_BOLT = M_WEB + M_ECC                              # 1,297

# ── Step 5：最不利螺栓 ──
FV_B = V_DES/NB                                     # 11.67（鉛垂，均勻）
YMAX = max(YS)                                      # 20
FH_B = M_BOLT*YMAX/SUM_Y2                           # 23.16（水平，線性）
RMAX = math.hypot(FV_B, FH_B)                       # 25.93
AB_REQ = RMAX/(NS*FVA)                              # 4.631 cm^2
DB_REQ = math.sqrt(4*AB_REQ/math.pi)                # 2.428 cm
DB_USE = 2.5                                        # D25
AB_USE = math.pi*DB_USE**2/4                        # 4.909
CAP_USE = NS*AB_USE*FVA                             # 27.49

# 三種假設（§5 爭議一）
def rmax_of(m_bolt):
    return math.hypot(FV_B, m_bolt*YMAX/SUM_Y2)
CASE_A = rmax_of(0.0)                               # 11.67 舊版
CASE_B = rmax_of(M_ECC)                             # 13.24
CASE_C = RMAX                                       # 25.93

# ── Step 6：鈑厚（兩片）──
T_SHEAR = V_DES/(2*H_PL*0.4*FY)                     # 0.729
S_PL    = 2*H_PL**2/6                               # 768 t
T_BEND  = M_BOLT/(S_PL*0.6*FY)                      # 1.126
T_REQ   = max(T_SHEAR, T_BEND)
T_USE   = 1.2                                       # 12 mm
FB_USE  = M_BOLT/(S_PL*T_USE)
FVV_USE = V_DES/(2*H_PL*T_USE)


# ══════════════════════════════════════════════════════════════
def fig1_splice():
    """圖 1：續接立面重繪（每側 6 支、偏心 5 cm）"""
    W, H = 900, 620
    XL, XR = -19.0, 19.0
    YL, YH = -32.0, 32.0
    Lm, Rm, Tm, Bm = 60, 60, 118, 96
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    ox = (W - (XR-XL)*sx)/2 - XL*sx
    cv = Canvas(W, H, sx=sx, ox=ox, oy=Bm - YL*sx, bg="#FFFFFF")

    # 梁腹板（背景）與翼板
    cv.polygon([(-18, -HW/2), (18, -HW/2), (18, HW/2), (-18, HW/2)],
               "#F3F6F9", C["member2"], 1.6)
    for sgn in (1, -1):
        y0 = sgn*HW/2
        cv.polygon([(-18, min(y0, y0+sgn*TF)), (18, min(y0, y0+sgn*TF)),
                    (18, max(y0, y0+sgn*TF)), (-18, max(y0, y0+sgn*TF))],
                   "#DCE3EC", C["member"], 1.8)
        cv.text_px(cv.X(-15), cv.Y(y0 + sgn*TF/2), "翼板續接鈑", 11, C["muted"], "start")

    # 腹板續接鈑
    cv.polygon([(-W_PL/2, -H_PL/2), (W_PL/2, -H_PL/2), (W_PL/2, H_PL/2), (-W_PL/2, H_PL/2)],
               "#EDF1F6", C["member"], 2.6)
    # 續接中心線
    cv.line((0, -H_PL/2 - 5), (0, H_PL/2 + 5), C["accent"], 1.8, dash="7 4")
    cv.text_px(cv.X(0), cv.Y(H_PL/2 + 5) - 16, "續接中心線", 11.5, C["accent"], weight="700")

    # 螺栓（左列接左段梁、右列接右段梁）
    for sgnx, lab, col in ((-1, "左列 6 支\n接左段梁", C["compr"]),
                           (1, "右列 6 支\n接右段梁", C["load"])):
        x = sgnx*COL_GAP/2
        for y in YS:
            cv.circle((x, y), DB_USE/2, "#FFFFFF", col, 2.0)
            cv.dot((x, y), 3.0, fill=col)
    for sgnx, lab, col in ((-1, f"左列 {NB} 支（接左段梁）", C["compr"]),
                           (1, f"右列 {NB} 支（接右段梁）", C["load"])):
        yl = YS[3]
        cv.line((sgnx*COL_GAP/2, yl), (sgnx*(W_PL/2 + 1.4), yl), col, 1.3, dash="4 3")
        cv.text_px(cv.X(sgnx*(W_PL/2 + 1.8)), cv.Y(yl), lab, 11.5, col,
                   "end" if sgnx < 0 else "start", weight="700")

    # 尺寸
    cv.dim((COL_GAP/2, YS[0]), (COL_GAP/2, YS[1]), f"{SP:g}", off=46, label_off=13)
    cv.dim((COL_GAP/2, YS[0]), (COL_GAP/2, YS[-1]),
           f"{NB-1}@{SP:g} = {(NB-1)*SP:g}", off=96, label_off=14)
    cv.dim((-W_PL/2, -H_PL/2), (W_PL/2, -H_PL/2), f"{W_PL:g}", off=34, label_off=13)
    cv.dim((-W_PL/2, -H_PL/2), (-W_PL/2, H_PL/2), f"h = {H_PL:g}", off=-40, label_off=-14)
    cv.dim((0, YS[0] - 4), (COL_GAP/2, YS[0] - 4), f"e = {ECC:g}", off=20, label_off=12,
           color=C["accent"])

    cv.text_px(W/2, 34, "圖 1　梁腹板續接的螺栓配置（正視）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"鈑上共 {2*NB} 支（2 縱列 × {NB} 橫排），但**每一縱列**的 {NB} 支只負責一端梁"
               .replace("**", ""),
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"故設計螺栓數 n = {NB}（不是 2 列 × 3 排）；且該列距續接中心線 e = {ECC:g} cm，"
               f"會產生 V·e 的附加彎矩",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"腹板兩側各一片鈑（雙剪）＋上下兩片翼板鈑 = 四鈑接合；"
               f"Σy² = {SUM_Y2:,.0f} cm²",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-4-fig-1-splice.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_moment_share():
    """圖 2：腹板鈑承受哪些作用力"""
    W, H = 940, 470
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 336, 400
    rows = ((f"腹板依剛度分擔之彎矩", f"M × I_w/I_x = {M_DES:,.0f} × {RATIO_W:.4f}",
             M_WEB, C["load"]),
            (f"螺栓列偏心彎矩", f"V × e = {V_DES:g} × {ECC:g}", M_ECC, C["accent"]),
            (f"螺栓群總彎矩", "兩者相加", M_BOLT, C["bmd"]))
    peak = M_BOLT * 1.12
    for i, (nm, note, v, col) in enumerate(rows):
        y = 142 + i*72
        cv.text_px(x0 - 14, y - 9, nm, 13.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11.5, C["muted"], "end")
        cv.rect_px(x0, y-17, bw, 34, "#EDF1F6", 7)
        cv.rect_px(x0, y-17, bw*v/peak, 34, col, 7)
        cv.text_px(x0 + bw*v/peak + 12, y, f"{v:,.0f} tf·cm", 13.5, col, "start", weight="700")

    cv.text_px(W/2, 34, "圖 2　腹板續接鈑到底承受哪些作用力", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"四鈑續接：翼板鈑承擔 M(1 − I_w/I_x)，腹板鈑承擔 M·I_w/I_x ＋ 全部 V ＋ V·e",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"腹板分擔彎矩是偏心彎矩的 {M_WEB/M_ECC:.1f} 倍——舊版兩項全漏，只用 V/n",
               12.5, C["accent"])
    cv.text_px(W/2, H - 48,
               f"深梁的 I_w/I_x 佔比小（本題僅 {RATIO_W*100:.1f}%），但乘上 M 之後仍是螺栓群最大的彎矩來源",
               13, C["muted"])
    cv.text_px(W/2, H - 24,
               f"另有全部剪力 V = {V_DES:g} tf 由腹板鈑承擔（不分給翼板鈑）",
               12.5, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-4-fig-2-moment-share.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_bolt_force():
    """圖 3：偏心螺栓群的向量分佈與最不利螺栓"""
    W, H = 940, 620
    XL, XR = -30.0, 30.0
    YL, YH = -28.0, 28.0
    Lm, Rm, Tm, Bm = 60, 300, 118, 96
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    cv = Canvas(W, H, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx, bg="#FFFFFF")

    VS = 10.5 / RMAX          # 向量比例：最大合力 → 10.5 cm（不讓箭頭連成一條線）

    cv.line((0, -H_PL/2), (0, H_PL/2), C["ghost"], 2.0, dash="6 4")
    cv.polygon([(-6, -H_PL/2), (6, -H_PL/2), (6, H_PL/2), (-6, H_PL/2)],
               "#F3F6F9", C["member2"], 1.6)

    for y in YS:
        fh = M_BOLT*y/SUM_Y2                    # 水平分量（線性隨 y）
        r  = math.hypot(FV_B, fh)
        crit = abs(abs(y) - YMAX) < 1e-9
        col = C["load"] if crit else C["muted"]
        cv.circle((0, y), DB_USE/2, "#FFFFFF", C["member"], 1.8)
        cv.arrow((0, y), (0, y - FV_B*VS), C["compr"], 2.4, 8)          # 直接剪力（向下）
        cv.arrow((0, y), (fh*VS, y), C["accent"], 2.4, 8)               # 彎矩剪力（水平）
        cv.arrow((0, y), (fh*VS, y - FV_B*VS), col, 3.4 if crit else 2.2, 10)
        cv.math_px(cv.X(fh*VS) + (14 if fh >= 0 else -14), cv.Y(y - FV_B*VS) + 12,
                   f"{r:.2f}", 12, col, "start" if fh >= 0 else "end",
                   weight="700" if crit else "400")

    cv.text_px(cv.X(0) - 16, cv.Y(YMAX) - 26, "最不利螺栓（最外排）", 12, C["load"], "end", weight="700")

    cv.legend(W - Rm + 12, 168,
              [(C["compr"], f"直接剪力 V/n = {FV_B:.2f} tf"),
               (C["accent"], "彎矩剪力 M y/Σy²"),
               (C["load"], "合力（最不利）")], size=12, gap=22)
    cv.math_px(W - Rm + 12, 258, f"f_{{v}} = {V_DES:g}/{NB} = {FV_B:.2f} tf", 13,
               C["compr"], "start", weight="700")
    cv.math_px(W - Rm + 12, 282,
               f"f_{{h}} = {M_BOLT:,.0f}×{YMAX:g}/{SUM_Y2:,.0f} = {FH_B:.2f} tf", 13,
               C["accent"], "start", weight="700")
    cv.math_px(W - Rm + 12, 306, f"R_{{max}} = {RMAX:.2f} tf", 14, C["load"], "start",
               weight="700")
    cv.text_px(W - Rm + 12, 344, "三種假設的差距：", 12.5, C["text"], "start", weight="700")
    for i, (nm, v) in enumerate((("A 只有 V（舊版）", CASE_A),
                                 ("B ＋偏心 V·e", CASE_B),
                                 ("C ＋腹板分擔彎矩", CASE_C))):
        cv.text_px(W - Rm + 12, 368 + i*21, f"{nm}：{v:.2f} tf", 11.5,
                   C["load"] if v == CASE_C else C["muted"], "start",
                   weight="700" if v == CASE_C else "400")
    cv.math_px(W - Rm + 12, 448,
               f"A_{{b}} ≥ {RMAX:.2f}/(2×{FVA:g}) = {AB_REQ:.3f} cm^{{2}}", 12.5,
               C["text"], "start", weight="700")
    cv.math_px(W - Rm + 12, 472, f"d_{{b}} ≥ {DB_REQ:.3f} cm", 12.5,
               C["text"], "start", weight="700")
    cv.text_px(W - Rm + 108, 472, "⇒ 選 D25", 12.5, C["text"], "start", weight="700")
    cv.text_px(W - Rm + 12, 498,
               f"容量 2×{AB_USE:.3f}×{FVA:g} = {CAP_USE:.2f} tf（使用率 {RMAX/CAP_USE*100:.1f}%）",
               11.5, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 3　偏心螺栓群：直接剪力均勻、彎矩剪力線性", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "ASD 是「逐支」檢核最不利螺栓，不是把總力除以螺栓數",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"只用 V/n 會得 {CASE_A:.2f} tf（低估 {100*(1-CASE_A/CASE_C):.0f}%），螺栓由 D25 誤選為 M20",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "彎矩剪力隨 y 線性變化 ⇒ 最外排最大；與均勻的直接剪力正交疊加",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-4-fig-3-bolt-force.svg"))


# ══════════════════════════════════════════════════════════════
def fig4_plate():
    """圖 4：鈑厚由剪力還是彎矩控制"""
    W, H = 900, 400
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 300, 400
    rows = (("剪力控制", f"V/(2·h·0.4F_y) = {V_DES:g}/(2×{H_PL:g}×{0.4*FY:g})",
             T_SHEAR, C["compr"]),
            ("彎矩控制", f"M/(2h²/6 · 0.6F_y) = {M_BOLT:,.0f}/({S_PL:.0f}×{0.6*FY:g})",
             T_BEND, C["load"]),
            ("選用鈑厚", f"12 mm；f_b = {FB_USE:.3f}、f_v = {FVV_USE:.3f} tf/cm²",
             T_USE, C["accent"]))
    peak = max(v for *_, v, _ in rows) * 1.12
    for i, (nm, note, v, col) in enumerate(rows):
        y = 136 + i*66
        cv.text_px(x0 - 14, y - 9, nm, 13.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11, C["muted"], "end")
        cv.rect_px(x0, y-17, bw, 34, "#EDF1F6", 7)
        cv.rect_px(x0, y-17, bw*v/peak, 34, col, 7)
        cv.text_px(x0 + bw*v/peak + 12, y, f"{v:.3f} cm", 13.5, col, "start", weight="700")
    cv.parts.append(f'<line x1="{x0 + bw*T_BEND/peak}" y1="110" x2="{x0 + bw*T_BEND/peak}" '
                    f'y2="{136+2*66+24}" stroke="{C["load"]}" stroke-width="1.6" '
                    f'stroke-dasharray="6 4"/>')

    cv.text_px(W/2, 34, "圖 4　腹板續接鈑厚度：剪力與彎矩雙重控制", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"兩片鈑，高 {H_PL:g} cm；剪力用 0.4F_y = {0.4*FY:g}，彎矩用 0.6F_y = {0.6*FY:g} tf/cm²",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"彎矩控制（{T_BEND:.3f} cm）比剪力控制（{T_SHEAR:.3f} cm）大 "
               f"{100*(T_BEND/T_SHEAR-1):.0f}%——只算剪力會選成 8 mm",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "鈑件不符「結實斷面」之肢材定義，故彎曲用 0.6F_y 而非 0.66F_y",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-4-fig-4-plate.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_splice(); fig2_moment_share(); fig3_bolt_force(); fig4_plate()
    print(f"Ix={IX:,.0f} Sx={SX:,.0f} Iw={IW:,.0f} Iw/Ix={RATIO_W:.4f}")
    print(f"Ma={MA:,.0f} tf·cm (0.5Ma={0.5*MA/100:.1f} tf·m)  Va={VA:g} (0.5Va={0.5*VA:g})")
    print(f"M_des={M_DES:,.0f} tf·cm  V_des={V_DES:g} tf")
    print(f"h_pl={H_PL:g} w_pl={W_PL:g} Σy²={SUM_Y2:,.0f}")
    print(f"M_web={M_WEB:,.0f} M_ecc={M_ECC:,.0f} M_bolt={M_BOLT:,.0f}（比 {M_WEB/M_ECC:.1f} 倍）")
    print(f"fv={FV_B:.2f} fh={FH_B:.2f} Rmax={RMAX:.2f} Ab≥{AB_REQ:.3f} db≥{DB_REQ:.3f}"
          f" 選 D25 容量 {CAP_USE:.2f}")
    print(f"A={CASE_A:.2f} B={CASE_B:.2f} C={CASE_C:.2f}")
    print(f"t_shear={T_SHEAR:.3f} t_bend={T_BEND:.3f} -> 選 {T_USE:g} cm"
          f"（fb={FB_USE:.3f} fv={FVV_USE:.3f}）")
    print("done ->", OUT)
