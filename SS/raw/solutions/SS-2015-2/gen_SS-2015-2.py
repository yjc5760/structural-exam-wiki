#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2015-2 圖解產生腳本（雙槽鋼拉力桿：GSY／NSF／BSR ＋ 填角銲反算）

破壞塊幾何與所有面積、強度值皆由下方常數區算出，改一個間距重跑即改變圖形。
執行：python3 gen_SS-2015-2.py   →   figs/*.svg
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
AG   = 29.9      # cm^2 單根 C200x75（取自同卷第三題）
CY   = 2.49      # cm   形心至腹板外面
HCH  = 20.0      # cm   槽鋼深（腹板高）
TW   = 0.6       # cm   腹板厚
DB   = 2.5       # cm   螺栓直徑
E1   = 5.0       # cm   槽鋼自由端 → 第一排螺栓
S    = 10.0      # cm   縱向螺栓間距（＝接合長度 L）
E2   = 7.0       # cm   第二排螺栓 → 連接板邊緣（虛線，非槽鋼端緣）
G    = 10.0      # cm   橫向螺栓間距 gauge
LW   = 35.0      # cm   連接板單側有效銲長
TP   = 1.6       # cm   連接板厚
FY, FU, FEXX = 3.5, 4.6, 4.9      # tf/cm^2
PHI_T, PHI_R = 0.90, 0.75

# ── Step 1：幾何 ──
DH   = DB + 0.3                    # 2.8 標準孔
LJ   = S                           # 接合長度 10 cm
LSH  = E1 + S                      # 剪力面長度 15 cm（自自由端至最遠一排）

# ── Step 2：GSY ──
GSY  = PHI_T * FY * (2*AG)                         # 188.4

# ── Step 3：NSF ──
AN   = AG - 2*DH*TW                                # 26.54（橫斷面切 2 孔）
U_TB = 0.75                                        # 試卷／台灣規範表列（每線 2 螺栓）
U_FM = 1 - CY/LJ                                   # AISC 公式法 0.751
AE   = U_TB*AN
NSF  = PHI_R * FU * (2*AE)                         # 137.3

# ── Step 4：BSR（破壞塊：2 條縱向剪力面 + 1 條橫向拉力面）──
AGV  = 2*LSH*TW                                    # 18.0
ANV  = 2*(LSH - 1.5*DH)*TW                         # 12.96（1 整孔 + 1 半孔）
AGT  = G*TW                                        # 6.0
ANT  = (G - DH)*TW                                 # 4.32
T_RUP = FU*ANT                                     # 19.87
V_RUP = 0.6*FU*ANV                                 # 35.77
BSR_EQ2 = V_RUP + FY*AGT                           # 56.77（剪力斷裂 + 張力降伏）
BSR_CAP = V_RUP + T_RUP                            # 55.64（上限）
BSR_RN  = min(BSR_EQ2, BSR_CAP)
BSR  = 2 * PHI_R * BSR_RN                          # 83.5

# ── Step 5：設計強度與填角銲 ──
PHI_PN = min(GSY, NSF, BSR)
Q_UNIT = PHI_R * 0.6 * FEXX * 0.707 * (2*LW)       # 109.13 tf/cm(銲腳)
W_REQ  = PHI_PN / Q_UNIT * 10                      # mm
W_MIN  = 6.0                                       # 表 10.2-4：12 < t ≤ 19 mm
W_USE  = math.ceil(max(W_REQ, W_MIN))              # 8 mm
THETA  = math.degrees(math.atan2(4, 3))            # T 與鉛垂銲軸夾角 53.13°
K_DIR  = 1.0 + 0.5*math.sin(math.radians(THETA))**1.5   # AISC 方向性 1.358
W_AISC = PHI_PN / (Q_UNIT*K_DIR) * 10              # 5.63 mm
W_MAX  = TP*10 - 2                                 # 沿板緣上限 14 mm

# ── 補充檢核（§4 接合端）──
CHK_BOLT_N, CHK_BOLT_X, CHK_BEAR = 99.0, 123.8, 85.5     # tf


# ══════════════════════════════════════════════════════════════
def fig1_connection():
    """圖 1：接合詳圖重繪（螺栓 2×2、7 cm 量至連接板邊緣虛線）"""
    W, H = 980, 620
    XL, XR = -22.0, 40.0
    YL, YH = -20.0, 20.0
    Lm, Rm, Tm, Bm = 128, 60, 118, 92
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    cv = Canvas(W, H, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx, bg="#FFFFFF")

    XCOL, XPL = -14.0, E1 + S + E2          # 柱面 x、連接板邊緣 x = 22
    XEND = 34.0                             # 槽鋼折斷處

    # 柱翼板（左）與填角銲
    cv.polygon([(XCOL-4.5, -19), (XCOL, -19), (XCOL, 19), (XCOL-4.5, 19)],
               "#DCE3EC", C["member"], 2.2)
    cv.line((XCOL, -LW/2), (XCOL, LW/2), C["load"], 6.0, cap="butt")
    cv.dim((XCOL-4.5, -LW/2), (XCOL-4.5, LW/2), f"L_{{w}} = {LW:g}", off=-32, label_off=-13,
           color=C["load"])

    # 連接板（gusset）：柱面 → x = 22
    cv.polygon([(XCOL, -17), (XPL, -17), (XPL, 17), (XCOL, 17)],
               "#EDF1F6", C["member2"], 2.0)
    cv.line((XPL, -17), (XPL, 17), C["accent"], 2.4, dash="7 5")
    cv.text_px(cv.X(XPL), cv.Y(17) - 14, "連接板邊緣（虛線）", 12, C["accent"], weight="700")
    cv.math_px(cv.X(XCOL) + 10, cv.Y(13.6), f"t = {TP:g} cm", 13, C["muted"], "start")

    # 槽鋼腹板：自由端 x = 0 → 折斷 x = XEND
    cv.polygon([(0, -HCH/2), (XEND, -HCH/2), (XEND, HCH/2), (0, HCH/2)],
               "none", C["member"], 3.0)
    cv.line((0, -HCH/2), (0, HCH/2), C["bmd"], 4.4, cap="butt")
    cv.text_px(cv.X(0) - 6, cv.Y(-HCH/2) + 24, "槽鋼自由端", 12.5, C["bmd"], "end", weight="700")
    # 折斷符號
    for yy in (-HCH/2, HCH/2):
        cv.poly([(XEND-1.2, yy), (XEND-0.4, yy+0.9), (XEND+0.4, yy-0.9), (XEND+1.2, yy)],
                C["member"], 2.0)

    # 螺栓（2 縱排 × 2 橫列）
    for x in (E1, E1+S):
        for y in (-G/2, G/2):
            cv.circle((x, y), DH/2, "#FFFFFF", C["member"], 2.0)
            cv.dot((x, y), 3.2, fill=C["member"])

    # 尺寸線
    cv.dim((0, HCH/2), (E1, HCH/2), f"{E1:g}", off=-30, label_off=-12)
    cv.dim((E1, HCH/2), (E1+S, HCH/2), f"s = {S:g}", off=-30, label_off=-12)
    cv.dim((E1+S, HCH/2), (XPL, HCH/2), f"{E2:g}", off=-30, label_off=-12, color=C["accent"])
    cv.dim((E1, -G/2), (E1, G/2), f"g = {G:g}", off=-40, label_off=-15)

    # 拉力 T：與鉛垂銲軸夾 53.13°（3:4）
    tx, ty = 4/5, 3/5
    cv.arrow((XEND-2, 0), (XEND-2 + 9*tx, 9*ty), C["load"], 3.6, 12)
    cv.math_px(cv.X(XEND-2 + 9*tx) + 8, cv.Y(9*ty) - 8, "T", 18, C["load"], "start", weight="700")
    cv.text_px(cv.X(XEND-2) + 10, cv.Y(0) + 26, "3:4（與銲軸夾 53.13°）", 11.5, C["load"], "start")

    cv.text_px(cv.X(XCOL) + 6, cv.Y(LW/2) + 18, "填角銲（兩側各一道）", 12, C["load"],
               "start", weight="700")

    cv.text_px(W/2, 34, "圖 1　接合詳圖重繪（平面，單位 cm）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "雙槽鋼背靠背夾住連接板，螺栓只貫穿腹板；腹板上為 2 縱排 × 2 橫列共 4 孔",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"「{E2:g} cm」量到的是連接板邊緣的虛線，不是槽鋼端緣——槽鋼的自由端在左側（{E1:g} cm 那側）",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"接合長度 L = 縱向螺栓間距 = {S:g} cm；U 值與破壞塊幾何都由這個 L 與 g 決定",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2015-2-fig-1-connection.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_block_shear():
    """圖 2：BSR 破壞塊幾何（正解 vs 舊版誤讀）"""
    PWD, PH = 500, 470
    XL, XR = -3.0, 26.0
    YL, YH = -13.0, 13.0
    Lm, Tm, Bm = 40, 112, 96
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    def base(cv):
        cv.polygon([(0, -HCH/2), (24, -HCH/2), (24, HCH/2), (0, HCH/2)],
                   "none", C["member"], 2.4)
        cv.line((0, -HCH/2), (0, HCH/2), C["bmd"], 4.0, cap="butt")
        for x in (E1, E1+S):
            for y in (-G/2, G/2):
                cv.circle((x, y), DH/2, "#FFFFFF", C["member"], 1.8)
        # 螺栓對腹板的承壓力方向（向左）
        cv.arrow((E1+S+7.6, 8.0), (E1+S+2.0, 8.0), C["load"], 3.0, 10)
        cv.text_px(cv.X(E1+S+4.8), cv.Y(8.0) - 14, "螺栓推腹板向左", 11.5, C["load"], weight="700")

    # ── 正解 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("正解：拉力面在最遠一排螺栓", f"剪力面自自由端量 {E1+S:g} cm")
    p1.polygon([(0, -G/2), (E1+S, -G/2), (E1+S, G/2), (0, G/2)], C["fill_t"], "none")
    base(p1)
    for y in (-G/2, G/2):
        p1.line((0, y), (E1+S, y), C["sfd"], 4.0)
    p1.line((E1+S, -G/2), (E1+S, G/2), C["tension"], 4.4)
    p1.dim((0, -G/2), (E1+S, -G/2), f"{E1+S:g}", off=34, label_off=13, color=C["sfd"])
    p1.text_px(p1.X(2.0), p1.Y(G/2) - 16, "剪力面 ×2", 12, C["sfd"], "start", weight="700")
    p1.text_px(p1.X(E1+S) + 10, p1.Y(-9.0), f"拉力面 寬 g = {G:g}", 12, C["tension"],
               "start", weight="700")
    p1.math_px(PWD/2, PH - 66, f"A_{{nv}} = {ANV:.2f} cm^{{2}}", 14, C["sfd"], weight="700")
    p1.math_px(PWD/2, PH - 44, f"A_{{nt}} = {ANT:.2f}   A_{{gt}} = {AGT:.2f} cm^{{2}}",
               14, C["tension"], weight="700")
    p1.text_px(PWD/2, PH - 20, "剪力面切 1 整孔 + 1 半孔 ⇒ 扣 1.5 個孔徑", 12, C["muted"])

    # ── 舊版誤讀 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("舊版誤讀：拉力面放在 7 cm 側", "把連接板邊緣當成槽鋼端緣")
    XW = E1 + S + E2
    p2.polygon([(0, -G/2), (XW, -G/2), (XW, G/2), (0, G/2)], "rgba(192,57,43,0.10)", "none")
    base(p2)
    for y in (-G/2, G/2):
        p2.line((0, y), (E1+S, y), C["sfd"], 4.0, dash="7 5")
    p2.line((XW, -G/2), (XW, G/2), C["load"], 4.4, dash="6 4")
    p2.text_px(p2.X(XW) + 6, p2.Y(-9.0), "拉力面（誤）", 12, C["load"], "start", weight="700")
    p2.dim((E1+S, -G/2), (XW, -G/2), f"{E2:g}", off=34, label_off=13, color=C["load"])
    p2.math_px(PWD/2 - 26, PH - 66, f"A_{{nv}} = 14.64 cm^{{2}}", 14, C["load"], weight="700")
    p2.text_px(PWD/2 + 74, PH - 66, "（只扣 1 孔）", 12, C["load"], "start", weight="700")
    p2.math_px(PWD/2, PH - 44, f"A_{{nt}} = 3.36   A_{{gt}} = 4.20 cm^{{2}}", 14, C["load"],
               weight="700")
    p2.text_px(PWD/2, PH - 20, "完全沒用到橫向間距 g，破壞機構的物理圖像錯誤", 12, C["load"])

    compose([p1, p2], cols=2,
            title="圖 2　塊狀剪力破壞塊的幾何（自由端在哪一側決定一切）",
            sub=f"T 把槽鋼往右拉 ⇒ 螺栓推腹板向左 ⇒ 破壞塊往左側自由端擠出",
            note=f"兩處幾何誤差恰好部分相消，BSR 只差 1.0%（82.7 → {BSR:.1f} tf）；"
                 f"但若題目改變 g 或 e1，舊版會給出嚴重錯誤的答案",
            path=os.path.join(OUT, "SS-2015-2-fig-2-block-shear.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_limit_states():
    """圖 3：三種極限狀態 + BSR 內部的上限控制"""
    PWD, PH = 560, 420

    p1 = Canvas(PWD, PH, sx=1)
    p1.panel("① 三種極限狀態取最小", "另列接合端補充檢核")
    x0, bw = 176, 250
    rows = (("GSY 全斷面降伏", GSY, C["muted"]),
            ("NSF 淨斷面斷裂", NSF, C["compr"]),
            ("BSR 塊狀剪力", BSR, C["load"]),
            ("螺栓雙剪（N）", CHK_BOLT_N, C["border"]),
            ("腹板孔壁承壓", CHK_BEAR, C["border"]))
    peak = max(v for _, v, _ in rows)
    for i, (nm, v, col) in enumerate(rows):
        y = 118 + i*50
        ctrl = abs(v - BSR) < 1e-9
        p1.text_px(x0 - 12, y, nm, 12.5, C["text"] if ctrl else C["muted"], "end",
                   weight="700" if ctrl else "400")
        p1.rect_px(x0, y-15, bw, 30, "#EDF1F6", 6)
        p1.rect_px(x0, y-15, bw*v/peak, 30, col, 6)
        p1.text_px(x0 + bw*v/peak + 10, y, f"{v:.1f} tf", 13,
                   col if col != C["border"] else C["muted"], "start", weight="700")
        if ctrl:
            p1.text_px(x0 + bw*v/peak - 12, y, "控制", 12, "#FFFFFF", "end", weight="700")
    p1.parts.append(f'<line x1="{x0 + bw*BSR/peak}" y1="96" x2="{x0 + bw*BSR/peak}" '
                    f'y2="{118+4*50+20}" stroke="{C["load"]}" stroke-width="1.8" '
                    f'stroke-dasharray="6 4"/>')
    p1.text_px(PWD/2, PH - 44,
               f"設計強度 = {PHI_PN:.1f} tf（BSR 控制）", 15, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 20,
               f"承壓僅高出 BSR {100*(CHK_BEAR/BSR-1):.1f}%，屬同一量級，實務應一併列出",
               12, C["muted"])

    p2 = Canvas(PWD, PH, sx=1)
    p2.panel("② BSR 內部：兩條件式都要再與上限取小", "本題由上限控制")
    x0b, bwb = 150, 260
    peak2 = max(BSR_EQ2, BSR_CAP) * 1.06
    rows2 = ((f"式二（剪斷+張降）", BSR_EQ2, C["muted"],
              f"0.6F_uA_nv + F_yA_gt"),
             (f"上限（剪斷+張斷）", BSR_CAP, C["load"],
              f"0.6F_uA_nv + F_uA_nt"))
    for i, (nm, v, col, expr) in enumerate(rows2):
        y = 150 + i*74
        p2.text_px(x0b - 12, y - 9, nm, 12.5, C["text"], "end", weight="700")
        p2.text_px(x0b - 12, y + 12, expr, 11.5, C["muted"], "end")
        p2.rect_px(x0b, y-16, bwb, 32, "#EDF1F6", 6)
        p2.rect_px(x0b, y-16, bwb*v/peak2, 32, col, 6)
        p2.text_px(x0b + bwb*v/peak2 + 10, y, f"{v:.2f} tf", 13, col, "start", weight="700")
    p2.text_px(PWD/2, 300, f"取小 ⇒ R_n = {BSR_RN:.2f} tf/根", 14, C["load"], weight="700")
    p2.math_px(PWD/2, 326, f"φR_{{n}} = 0.75 × {BSR_RN:.2f} × 2 = {BSR:.1f} tf", 14,
               C["load"], weight="700")
    p2.text_px(PWD/2, PH - 44,
               "物理意義：張力面用降伏×全面積算得的貢獻", 12, C["muted"])
    p2.text_px(PWD/2, PH - 22,
               f"（{FY*AGT:.2f}）已超過它的斷裂能力（{T_RUP:.2f}），不合理 ⇒ 以斷裂值封頂",
               12, C["muted"])

    compose([p1, p2], cols=2,
            title=f"圖 3　拉力桿三種極限狀態：設計強度 {PHI_PN:.1f} tf 由塊狀剪力控制",
            sub=f"BSR 遠低於 NSF（{BSR:.1f} vs {NSF:.1f} tf），因為 BSR 只用到腹板的局部面積",
            note="提高強度最有效的途徑是改善接合詳圖（拉長剪力面／加寬拉力面），而不是換更強的鋼材",
            path=os.path.join(OUT, "SS-2015-2-fig-3-limit-states.svg"))


# ══════════════════════════════════════════════════════════════
def fig4_weld():
    """圖 4：填角銲腳尺寸的三個門檻"""
    W, H = 900, 400
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 292, 380
    rows = ((f"強度需求（台灣 2010）", "由設計強度反算，本題控制", W_REQ, C["load"]),
            (f"規範最小銲腳", f"表 10.2-4：12 &lt; t ≤ 19 mm ⇒ {W_MIN:g} mm", W_MIN, C["bmd"]),
            (f"強度需求（AISC 方向性）", f"θ = {THETA:.1f}°，係數 {K_DIR:.3f}", W_AISC, C["compr"]),
            (f"選用值", f"進位取整；沿板緣上限 {W_MAX:g} mm", float(W_USE), C["accent"]))
    peak = max(v for *_, v, _ in rows) * 1.10
    for i, (nm, note, v, col) in enumerate(rows):
        y = 130 + i*62
        cv.text_px(x0 - 14, y - 9, nm, 13, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11.5, C["muted"], "end")
        cv.rect_px(x0, y-16, bw, 32, "#EDF1F6", 6)
        cv.rect_px(x0, y-16, bw*v/peak, 32, col, 6)
        cv.text_px(x0 + bw*v/peak + 12, y, f"{v:.2f} mm", 13.5, col, "start", weight="700")
    # 最小銲腳門檻線
    cv.parts.append(f'<line x1="{x0 + bw*W_MIN/peak}" y1="104" x2="{x0 + bw*W_MIN/peak}" '
                    f'y2="{130+3*62+22}" stroke="{C["bmd"]}" stroke-width="1.6" '
                    f'stroke-dasharray="6 4"/>')

    cv.text_px(W/2, 34, "圖 4　填角銲腳尺寸：需求、規範最小值與選用值", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"φR_n = 0.75 × 0.6F_EXX × 0.707w × 2L_w = {Q_UNIT:.2f}·w（w 以 cm 計）",
               13, C["muted"])
    cv.text_px(W/2, 82,
               f"本題強度需求 {W_REQ:.2f} mm 大於最小值 {W_MIN:g} mm ⇒ 由「強度」控制，不是由「規範最小值」控制",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"AISC 360-16 的方向性強度使需求降到 {W_AISC:.2f} mm，改由最小銲腳 {W_MIN:g} mm 控制"
               f"（銲料約省 {100*(1-(W_MIN/W_USE)**2):.0f}%）",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2015-2-fig-4-weld.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_connection(); fig2_block_shear(); fig3_limit_states(); fig4_weld()
    print(f"dh={DH:.1f} An={AN:.2f} U={U_TB} (公式 {U_FM:.3f}) Ae={AE:.3f}")
    print(f"GSY={GSY:.1f} NSF={NSF:.1f}")
    print(f"Agv={AGV:.1f} Anv={ANV:.2f} Agt={AGT:.1f} Ant={ANT:.2f}")
    print(f"FuAnt={T_RUP:.2f} 0.6FuAnv={V_RUP:.2f} 式二={BSR_EQ2:.2f} 上限={BSR_CAP:.2f}"
          f" -> Rn={BSR_RN:.2f} BSR={BSR:.1f}")
    print(f"設計強度={PHI_PN:.1f}  q={Q_UNIT:.2f}  w_req={W_REQ:.2f}mm  w_aisc={W_AISC:.2f}mm"
          f"  選用={W_USE}mm")
    print("done ->", OUT)
