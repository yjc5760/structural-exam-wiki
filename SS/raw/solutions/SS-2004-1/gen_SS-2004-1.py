#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2004-1 圖解產生腳本（高強度螺栓施工三情境）

三張圖的數字全部來自「鋼構造建築物鋼結構施工規範」第五章原文（門檻 1 mm、鐵鎚 2.5 kg、
擴孔 +2 mm、預拉力 0.7F_u），孔徑與拉力–伸長曲線由這些值算出。
執行：python3 gen_SS-2004-1.py   →   figs/*.svg
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
# 由 SS-2004-1 §4 之規範原文取得
# ══════════════════════════════════════════════════════════════
GAP_LIMIT   = 1.0     # mm  §5.2 板厚差 < 1 mm 不必處理，≧ 1 mm 加墊片
HAMMER_MAX  = 2.5     # kg  §5.3.1 不得使用 2.5 kg 以上之鐵鎚
REAM_EXTRA  = 2.0     # mm  §5.3.1 擴孔後孔徑不得大於設計孔徑 2 mm
STD_HOLE_EX = 1.5     # mm  國內摩阻型高強度螺栓標準孔徑 ≈ d + 1.5 mm
DB          = 22.0    # mm  數值示例用之螺栓標稱直徑
PRELOAD_K   = 0.70    # §5.3.1 T_b = 0.7 F_u^b A_t
TORQUE_TOL  = 10.0    # %   §5.4.1 扭矩法容許誤差 ±10%
TURN_LO, TURN_HI = 1/3, 2/3      # §5.4.2 轉角法 1/3～2/3 迴轉

# F10T 之材料值（§4 (三) 之推導）
FU_B   = 1000.0                  # MPa
YR     = 0.90                    # 降伏比（約）
FY_B   = YR*FU_B                 # 900 MPa
SIG_PL = PRELOAD_K*FU_B          # 700 MPa 之預拉應力水準

STD_HOLE = DB + STD_HOLE_EX      # 23.5
REAM_MAX = STD_HOLE + REAM_EXTRA # 25.5


# ══════════════════════════════════════════════════════════════
def fig1_faying_gap():
    """圖 1：板面不密接時夾緊力去了哪裡"""
    PWD, PH = 500, 460
    XL, XR, YL, YH = -13.0, 13.0, -5.5, 7.5
    Lm, Tm, Bm = 40, 112, 116
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx
    T = 1.6                       # 板厚（繪圖單位）；間隙亦取 T，與格 2 之墊片同厚

    def bolt(cv, ytop, ybot):
        cv.polygon([(-0.95, ybot), (0.95, ybot), (0.95, ytop), (-0.95, ytop)],
                   "#FFFFFF", C["member"], 1.8)
        cv.polygon([(-2.1, ytop), (2.1, ytop), (2.1, ytop+0.85), (-2.1, ytop+0.85)],
                   "#C9D3E0", C["member"], 1.8)
        cv.polygon([(-2.1, ybot-0.85), (2.1, ybot-0.85), (2.1, ybot), (-2.1, ybot)],
                   "#C9D3E0", C["member"], 1.8)

    def lower(cv):
        cv.polygon([(-11.0, -T/2 - T), (11.0, -T/2 - T), (11.0, -T/2), (-11.0, -T/2)],
                   "#DCE3EC", C["member"], 2.0)

    # ── 格 1：有間隙，上板被夾緊力壓彎 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel(f"板面有間隙（板厚差 ≧ {GAP_LIMIT:g} mm）", "夾緊力先被拿去壓彎板件")
    XS = [-11.0 + 22.0*i/120 for i in range(121)]
    yb = lambda x: -T/2 + T*min(1.0, (abs(x)/8.5)**1.8)   # 螺栓處貼合，往外張開
    lower(p1)
    p1.polygon([(x, yb(x)) for x in XS] + [(x, yb(x) + T) for x in reversed(XS)],
               "#DCE3EC", C["member"], 2.0)
    bolt(p1, T/2, -T/2 - T)
    # 間隙標註
    p1.arrow((7.6, T/2 - 0.05), (7.6, -T/2 + 0.05), C["load"], 2.0, 7)
    p1.arrow((7.6, -T/2 + 0.05), (7.6, T/2 - 0.05), C["load"], 2.0, 7)
    p1.text_px(p1.X(7.6) + 10, p1.Y(0), "間隙", 11.5, C["load"], "start", weight="700")
    p1.arrow((0, 6.2), (0, T/2 + 1.0), C["load"], 2.8, 9)
    p1.math_px(p1.X(0) + 12, p1.Y(5.1), "T_{b}", 15, C["load"], "start", weight="700")
    p1.text_px(PWD/2, PH - 62, "夾緊力做功把板壓彎", 13, C["load"], weight="700")
    p1.text_px(PWD/2, PH - 40, "真正壓在接觸面上的正向力大幅下降", 12, C["muted"])
    p1.math_px(PWD/2 - 40, PH - 16, "R_{n} = μ·T_{b}·n_{s}", 13, C["muted"])
    p1.text_px(PWD/2 + 6, PH - 16, "失去依據", 12, C["muted"], "start")

    # ── 格 2：加墊片填平 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("加墊片填平後鎖緊", "墊片須與母材同等表面處理")
    lower(p2)
    p2.polygon([(-11.0, T/2), (11.0, T/2), (11.0, T/2 + T), (-11.0, T/2 + T)],
               "#DCE3EC", C["member"], 2.0)
    p2.polygon([(-8.5, -T/2), (8.5, -T/2), (8.5, T/2), (-8.5, T/2)],
               C["fill_m"], C["bmd"], 2.0)
    p2.text_px(p2.X(-8.5) - 8, p2.Y(0), "墊片", 11.5, C["bmd"], "end", weight="700")
    bolt(p2, T/2 + T, -T/2 - T)
    p2.arrow((0, 6.2), (0, T/2 + T + 1.0), C["bmd"], 2.8, 9)
    p2.math_px(p2.X(0) + 12, p2.Y(5.1), "T_{b}", 15, C["bmd"], "start", weight="700")
    for x in (-5.6, 5.6):
        p2.arrow((x, T/2 + 1.3), (x, T/2 + 0.1), C["bmd"], 2.2, 8)
        p2.arrow((x, -T/2 - 1.3), (x, -T/2 - 0.1), C["bmd"], 2.2, 8)
    p2.text_px(PWD/2, PH - 62, "夾緊力完整作用在接觸面上", 13, C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 40, "墊片若未做表面處理，等於夾入一片低摩擦介面", 12, C["load"])
    p2.text_px(PWD/2, PH - 16, "——這是最常見的實務錯誤", 12, C["load"])

    compose([p1, p2], cols=2,
            title=f"圖 1　板面不密接：規範門檻只有一個數字 —— {GAP_LIMIT:g} mm",
            sub=f"§5.2：板厚差小於 {GAP_LIMIT:g} mm 不必處理（由板件彈性變形吸收）；"
                f"達 {GAP_LIMIT:g} mm 以上加墊片填平",
            note="鎖螺栓前並應將鐵銹、鱗片、黑皮、污泥、油垢及孔緣毛邊徹底清除；"
                 "不要自行發明「2 mm／6 mm」三段式門檻",
            path=os.path.join(OUT, "SS-2004-1-fig-1-faying-gap.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_hole_correction():
    """圖 2：孔位校正的三層順序與兩個上限"""
    W, H = 980, 500
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")

    # ── 左：孔徑的三個尺度 ──
    x0, bw = 290, 300
    peak = REAM_MAX*1.06
    rows = ((f"螺栓標稱直徑 d", f"本例 d = {DB:g} mm", DB, C["muted"]),
            (f"標準孔徑 d + {STD_HOLE_EX:g}", "國內摩阻型高強度螺栓", STD_HOLE, C["bmd"]),
            (f"鉸孔上限 標準孔 + {REAM_EXTRA:g}", "§5.3.1「不得大於設計孔徑 2 mm」",
             REAM_MAX, C["load"]))
    for i, (nm, note, v, col) in enumerate(rows):
        y = 158 + i*62
        cv.text_px(x0 - 14, y - 9, nm, 12.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11, C["muted"], "end")
        cv.rect_px(x0, y-16, bw, 32, "#EDF1F6", 7)
        cv.rect_px(x0, y-16, bw*v/peak, 32, col, 7)
        cv.text_px(x0 + bw*v/peak - 12, y, f"{v:.1f} mm", 12.5, "#FFFFFF", "end",
                   weight="700")
    xr = x0 + bw*REAM_MAX/peak
    cv.parts.append(f'<line x1="{xr}" y1="128" x2="{xr}" y2="{158+2*62+24}" '
                    f'stroke="{C["load"]}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    cv.text_px(xr, 120, "超過即不得使用", 12, C["load"], weight="700")

    # ── 左下：三項絕對禁止 ──
    cv.text_px(x0 - 14, 372, "絕對禁止：", 12.5, C["load"], "end", weight="700")
    for i, t in enumerate(("以氣體切割（氣割）擴孔",
                           "以重鎚強行敲入螺栓",
                           "以螺栓本身充當沖梢")):
        y = 372 + i*24
        cv.text_px(x0, y, "×", 14, C["load"], "start", weight="700")
        cv.text_px(x0 + 20, y, t, 12, C["load"], "start")

    # ── 右：三層順序 ──
    sx0 = 640
    steps = (("① 沖梢（drift pin）校正", f"不得使用 {HAMMER_MAX:g} kg 以上之鐵鎚",
              C["bmd"]),
             ("② 鉸孔（reaming）擴孔", f"擴孔後孔徑 ≤ 設計孔徑 + {REAM_EXTRA:g} mm",
              C["accent"]),
             ("③ 超出上限", "該孔不得使用，須檢討補救並重新驗算", C["load"]))
    for i, (nm, note, col) in enumerate(steps):
        y = 158 + i*86
        cv.rect_px(sx0, y-25, 300, 52, "#F5F7FA", 10, col, 1.8)
        cv.text_px(sx0 + 14, y - 8, nm, 12.5, col, "start", weight="700")
        cv.text_px(sx0 + 14, y + 13, note, 11, C["muted"], "start")
        if i < len(steps) - 1:
            cv.parts.append(f'<line x1="{sx0+150}" y1="{y+27}" x2="{sx0+150}" y2="{y+53}" '
                            f'stroke="{C["muted"]}" stroke-width="2"/>')
            cv.parts.append(f'<polygon points="{sx0+150},{y+58} {sx0+145},{y+49} '
                            f'{sx0+155},{y+49}" fill="{C["muted"]}"/>')
    cv.text_px(sx0, 372, "順序不可顛倒：先以沖梢對正，", 12, C["muted"], "start")
    cv.text_px(sx0, 394, "確認確實無法穿入後才鉸孔；", 12, C["muted"], "start")
    cv.text_px(sx0, 416, "鉸孔須疊合後一次施作、鐵屑清除，", 12, C["muted"], "start")
    cv.text_px(sx0, 438, "並重新驗算構件與接合板之淨斷面。", 12, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 2　螺栓無法徒手穿入時的校正：先沖梢、後鉸孔", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "兩個數字是本小題的得分點：鐵鎚重量上限與擴孔孔徑上限",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"只寫「用鉸孔擴大」而漏掉沖梢與 {REAM_EXTRA:g} mm 上限，等於漏掉一半配分",
               12.5, C["accent"])
    cv.save(os.path.join(OUT, "SS-2004-1-fig-2-hole-correction.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_reuse():
    """圖 3：為什麼拆卸後不得再用——拉力–伸長曲線上的兩種鎖緊法"""
    W, H = 1020, 620
    Lm, Rm, Tm, Bm = 90, 330, 150, 120
    XMAX = 1.0                          # 正規化伸長量
    YMAX = FU_B*1.22
    sxx = (W-Lm-Rm)/XMAX
    syy = (H-Tm-Bm)/YMAX
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda e: Lm + e*sxx
    Y = lambda v: H - Bm - v*syy

    E1, E2 = 0.26, 0.84                 # 降伏點、極限點之正規化伸長
    def curve(e):
        if e <= E1:
            return FY_B*e/E1
        if e <= E2:
            return FY_B + (FU_B - FY_B)*((e-E1)/(E2-E1))**0.6
        return FU_B
    SLOPE = FY_B/E1                     # 彈性段斜率（卸載線與之平行）

    # 轉角法之目標區：規範以「自密貼再轉 1/3～2/3 圈」控制，落在降伏之後
    EP_LO, EP_HI = E1 + (E2-E1)*0.18, E1 + (E2-E1)*0.55
    cv.rect_px(X(EP_LO), Y(YMAX), X(EP_HI)-X(EP_LO), Y(0)-Y(YMAX),
               "rgba(180,83,9,0.09)", 0)

    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{X(XMAX)+14}" y2="{Y(0)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{Lm}" y2="{Y(YMAX)-6}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.text_px(X(XMAX/2), Y(0) + 40, "螺栓伸長量 →", 13, C["muted"])
    cv.text_px(Lm + 6, Tm - 14, "螺栓拉應力（MPa）", 13, C["muted"], "start")

    pts = " ".join(f"{X(XMAX*i/240):.2f},{Y(curve(XMAX*i/240)):.2f}" for i in range(241))
    cv.parts.append(f'<polyline points="{pts}" fill="none" stroke="{C["compr"]}" '
                    f'stroke-width="3.4" stroke-linejoin="round"/>')

    for v, col, lab in ((FU_B, C["muted"], f"極限 F_u = {FU_B:.0f}"),
                        (FY_B, C["accent"], f"降伏 F_y ≈ {FY_B:.0f}"),
                        (SIG_PL, C["bmd"], f"0.7F_u = {SIG_PL:.0f}")):
        cv.parts.append(f'<line x1="{Lm}" y1="{Y(v)}" x2="{X(XMAX)}" y2="{Y(v)}" '
                        f'stroke="{col}" stroke-width="1.6" stroke-dasharray="6 4"/>')
        cv.text_px(X(XMAX) + 12, Y(v), lab, 12, col, "start", weight="700")

    # A：扭矩法之目標（0.7F_u，仍在彈性段）
    EA = SIG_PL/SLOPE
    cv.parts.append(f'<circle cx="{X(EA):.2f}" cy="{Y(SIG_PL):.2f}" r="6.2" '
                    f'fill="{C["bmd"]}" stroke="#FFFFFF" stroke-width="2"/>')
    cv.text_px(X(EA) - 12, Y(SIG_PL) - 16, "A 扭矩法目標", 12.5, C["bmd"], "end",
               weight="700")

    # B：轉角法刻意進入塑性區 → 卸載後留下永久伸長
    EB = (EP_LO + EP_HI)/2
    SB = curve(EB)
    cv.parts.append(f'<circle cx="{X(EB):.2f}" cy="{Y(SB):.2f}" r="6.6" '
                    f'fill="{C["load"]}" stroke="#FFFFFF" stroke-width="2"/>')
    cv.text_px(X(EB) + 16, Y(SB) + 22, "B 轉角法目標區（塑性）", 12.5, C["load"],
               "start", weight="700")
    e_res = EB - SB/SLOPE
    cv.parts.append(f'<line x1="{X(EB):.2f}" y1="{Y(SB):.2f}" x2="{X(e_res):.2f}" '
                    f'y2="{Y(0):.2f}" stroke="{C["load"]}" stroke-width="2.2" '
                    f'stroke-dasharray="7 4"/>')
    cv.text_px(X(e_res) + 30, Y(0) - 104, "卸載", 11.5, C["load"], "end")
    cv.parts.append(f'<line x1="{X(0):.2f}" y1="{Y(0)+16:.2f}" x2="{X(e_res):.2f}" '
                    f'y2="{Y(0)+16:.2f}" stroke="{C["load"]}" stroke-width="3.6"/>')
    cv.text_px(X(e_res) + 10, Y(0) + 16, "拆卸後留下的永久伸長", 12, C["load"],
               "start", weight="700")

    # 剩餘延性
    ybr = Y(YMAX) + 34
    cv.parts.append(f'<line x1="{X(EB):.2f}" y1="{ybr:.2f}" x2="{X(E2):.2f}" '
                    f'y2="{ybr:.2f}" stroke="{C["accent"]}" stroke-width="2.4"/>')
    for xx in (X(EB), X(E2)):
        cv.parts.append(f'<line x1="{xx:.2f}" y1="{ybr-6:.2f}" x2="{xx:.2f}" '
                        f'y2="{ybr+6:.2f}" stroke="{C["accent"]}" stroke-width="2.4"/>')
    cv.text_px((X(EB)+X(E2))/2, ybr - 18, "再鎖時只剩這段延性餘裕", 12, C["accent"],
               weight="700")

    bx = W - Rm + 24
    cv.text_px(bx, 344, "規範 §5.3.1：", 12.5, C["text"], "start", weight="700")
    cv.text_px(bx, 366, "「已使用過之螺栓或帶有", 12, C["muted"], "start")
    cv.text_px(bx, 386, "傷痕銹蝕者，不得再使用」", 12, C["muted"], "start")
    cv.text_px(bx, 418, "主因（規範解說）：", 12.5, C["load"], "start", weight="700")
    cv.text_px(bx, 440, "預拉力已超過降伏拉力，", 12, C["load"], "start")
    cv.text_px(bx, 460, "拆卸後已產生永久變形", 12, C["load"], "start")
    cv.text_px(bx, 492, "次因：", 12.5, C["muted"], "start", weight="700")
    cv.text_px(bx, 514, f"K 值偏移 ⇒ 扭矩法失準（±{TORQUE_TOL:g}%）", 12, C["muted"], "start")
    cv.text_px(bx, 534, "密貼起算點失真 ⇒ 轉角法失準", 12, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 3　鎖緊本身就是刻意讓螺栓進入降伏之後", 17.5, C["text"],
               weight="700")
    cv.text_px(W/2, 58,
               f"以 F10T 為例：F_u = {FU_B:.0f}、降伏比約 {YR:g} ⇒ F_y ≈ {FY_B:.0f} MPa",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"0.7F_u = {SIG_PL:.0f} MPa 本身仍在彈性段（為 F_y 的 {100*SIG_PL/FY_B:.0f}%）；",
               12.5, C["accent"])
    cv.text_px(W/2, 106,
               "是「轉角法再轉 1/3～2/3 圈」把螺栓推過降伏，規範解說所稱「已超過降伏拉力」即指此",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "這是單調靜力造成的塑性耗損，不是疲勞——把理由寫成「疲勞」是本小題最常見的錯",
               13, C["load"])
    cv.save(os.path.join(OUT, "SS-2004-1-fig-3-reuse.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_faying_gap(); fig2_hole_correction(); fig3_reuse()
    print(f"門檻：板厚差 {GAP_LIMIT:g} mm；鐵鎚 {HAMMER_MAX:g} kg；擴孔 +{REAM_EXTRA:g} mm")
    print(f"孔徑（d = {DB:g}）：標準孔 {STD_HOLE:g}、鉸孔上限 {REAM_MAX:g} mm")
    print(f"F10T：F_u = {FU_B:.0f}、F_y ≈ {FY_B:.0f}、0.7F_u = {SIG_PL:.0f} MPa"
          f"（F_y 的 {100*SIG_PL/FY_B:.0f}%，仍在彈性段）")
    print("越過降伏的是『轉角法再轉 1/3～2/3 圈』，非 0.7F_u 本身——圖 3 已據此區分 A、B 兩點")
    print("done ->", OUT)
