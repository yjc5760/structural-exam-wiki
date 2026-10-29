#!/usr/bin/env python3
"""
SS-2005-1 單角鋼螺栓接合之設計拉力強度 — 解題圖解產生腳本

用法：
    python3 gen_SS-2005-1.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個尺寸、面積、強度都標明來自 SS-2005-1.md 哪一節
  2. 三條塊狀剪力路徑的破壞面由螺栓座標算出（PATHS 由 Y_ROW1/Y_ROW2 推得），
     改一個邊距，破壞塊與 A_nt 會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2005-1"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2005-1.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 幾何（cm）
W_LEG  = 20.0           # 連接肢寬（L200×200×20）
T      = 2.0            # 肢厚
D_H    = 2.35           # 螺栓孔徑
D_B    = 2.2            # 螺栓直徑
E_END  = 5.0            # 端距（自角鋼端至第 1 列）
S_LONG = 7.5            # 列距（沿載重方向）
G1     = 7.5            # 肢背 → 第 1 行
G2     = 7.5            # 第 1 行 → 第 2 行
G3     = W_LEG - G1 - G2  # 第 2 行 → 肢趾 = 5.0
# §1 材料
FY, FU = 2.5, 4.1       # tf/cm^2
FNV    = 4.2            # tf/cm^2（螺紋不在剪力平面）
# §4.5 剪力面
L_SH   = E_END + 2 * S_LONG                 # 20 cm
A_GV1  = L_SH * T                           # 40.0 cm^2（每面）
A_NV1  = (L_SH - 2.5 * D_H) * T             # 28.25 cm^2（扣 2.5 孔）
# §4.8 五個極限狀態
P_GSY  = 171.0
P_NSF  = 174.1
P_BSR_A, P_BSR_B, P_BSR_C = 68.5, 83.9, 121.7
P_BOLT = 71.8
P_BRG  = 194.8
P_ANS  = 68.5
# §5.2 若螺紋改在剪力平面
P_BOLT_N = 57.5

# ── 繪圖座標：x 沿載重方向（角鋼端在 x=0），y 由肢趾(0) 至肢背(W_LEG) ──
Y_HEEL = W_LEG                  # 肢背（外伸肢所在）
Y_ROW1 = W_LEG - G1             # 12.5（第 1 行，距肢背 7.5）
Y_ROW2 = W_LEG - G1 - G2        # 5.0 （第 2 行，距肢趾 5.0）
Y_TOE  = 0.0
X_COLS = [E_END, E_END + S_LONG, E_END + 2 * S_LONG]   # 5, 12.5, 20
X_END_BOLT = X_COLS[-1]
X_FAR  = 30.0                   # 角鋼往載重方向延伸至此（截斷）


def _ant(width):
    """拉力破壞面淨面積：扣半個孔（§4.5）"""
    return (width - 0.5 * D_H) * T


# PATHS：(代號, 說明, 剪力面 y 座標串, 拉力面 y0, 拉力面 y1, 剪力面數, A_nt, R_n, 上限, phiRn, 備註)
PATHS = [
    ("A", "沿第 2 行剪出 ＋ 拉裂至肢趾",
     [Y_ROW2], Y_TOE, Y_ROW2, 1, _ant(G3), 100.9, 91.4, P_BSR_A, "← 全題控制"),
    ("B", "沿第 1 行剪出 ＋ 拉裂至肢背",
     [Y_ROW1], Y_ROW1, Y_HEEL, 1, _ant(G1), 121.4, 111.9, P_BSR_B, "須連帶剪斷外伸肢，實務不發生"),
    ("C", "兩行同時剪出 ＋ 拉裂行間",
     [Y_ROW2, Y_ROW1], Y_ROW2, Y_ROW1, 2, (G2 - D_H) * T, 181.2, 162.2, P_BSR_C, ""),
]

PW, PH = 460, 470
SXX, OXX, OYY = 10.67, 95, 100


def new_panel(title, sub):
    cv = Canvas(PW, PH, sx=SXX, ox=OXX, oy=OYY)
    cv.panel(title, sub)
    return cv


def draw_leg(cv, holes=True, faint=False):
    """連接肢俯視圖：外輪廓、外伸肢、螺栓孔、拉力方向"""
    col = C["member2"] if faint else C["member"]
    cv.poly([(0, Y_TOE), (X_FAR, Y_TOE)], col, 2.6)
    cv.poly([(0, Y_HEEL), (X_FAR, Y_HEEL)], col, 2.6)
    cv.line((0, Y_TOE), (0, Y_HEEL), col, 2.6, cap="butt")          # 角鋼端
    # 未連接之外伸肢（垂直於紙面，以雙線示意）
    cv.line((0, Y_HEEL + 1.15), (X_FAR, Y_HEEL + 1.15), col, 2.0)
    for i in range(13):
        x = 0.6 + i * (X_FAR - 1.2) / 12
        cv.line((x, Y_HEEL), (x - 0.55, Y_HEEL + 1.15), C["member2"], 1.1)
    # 截斷符號
    cv.line((X_FAR, Y_TOE), (X_FAR, Y_HEEL), C["muted"], 1.6, dash="5 4", cap="butt")
    if holes:
        for x in X_COLS:
            for y in (Y_ROW1, Y_ROW2):
                cv.circle((x, y), D_H / 2, "#FFFFFF", col, 1.9)
                cv.dot((x, y), 1.8, fill=col, stroke=col)
    cv.arrow((X_FAR + 0.4, W_LEG / 2), (X_FAR + 3.4, W_LEG / 2), C["load"], 3.4, 11)
    cv.math_px(cv.X(X_FAR + 3.4) + 8, cv.Y(W_LEG / 2), "P", 17, C["load"], "start", weight="700")


# ══════════════════════════════════════════════════════════
def _panel_geom():
    cv = new_panel("接合幾何（連接肢俯視）",
                   f"L200×200×20，t = {T} cm｜孔徑 {D_H} cm｜6 顆（2 行 × 3 列）")
    draw_leg(cv)
    cv.text_px(cv.X(X_FAR / 2), cv.Y(Y_HEEL + 1.15) - 13, "未連接之外伸肢（垂直於紙面）",
               11.5, C["muted"])
    cv.dim((0, Y_HEEL), (0, Y_ROW1), f"{G1:.1f} cm", off=44, label_off=14)
    cv.dim((0, Y_ROW1), (0, Y_ROW2), f"{G2:.1f} cm", off=44, label_off=14)
    cv.dim((0, Y_ROW2), (0, Y_TOE), f"{G3:.1f} cm", off=44, label_off=14)
    cv.dim((0, Y_TOE), (X_COLS[0], Y_TOE), f"{E_END:.0f}", off=40, label_off=13)
    cv.dim((X_COLS[0], Y_TOE), (X_COLS[1], Y_TOE), f"{S_LONG:.1f}", off=40, label_off=13)
    cv.dim((X_COLS[1], Y_TOE), (X_COLS[2], Y_TOE), f"{S_LONG:.1f}", off=40, label_off=13)
    cv.text_px(cv.X(X_FAR / 2), cv.Y(Y_TOE) + 68, "端距 e ＋ 2s ＝ 剪力面長度 20 cm",
               12, C["muted"])
    cv.text_px(cv.X(0) - 8, cv.Y(Y_HEEL), "肢背", 12, C["muted"], "end")
    cv.text_px(cv.X(0) - 8, cv.Y(Y_TOE), "肢趾", 12, C["accent"], "end", weight="700")
    cv.text_px(cv.X(X_END_BOLT + 1.6), cv.Y(Y_ROW1), "第 1 行", 11.5, C["muted"], "start")
    cv.text_px(cv.X(X_END_BOLT + 1.6), cv.Y(Y_ROW2), "第 2 行", 11.5, C["muted"], "start")
    return cv


def _panel_path(code, desc, ys, yt0, yt1, nsh, ant, rn, cap, phirn, note):
    cv = new_panel(f"③ 塊狀剪力　路徑 {code}" + ("（控制）" if code == "A" else ""), desc)
    draw_leg(cv, faint=True)
    # 破壞塊（介於剪力面之間、自角鋼端至最遠螺栓）
    yb0 = min([yt0] + ys) if code != "C" else Y_ROW2
    yb1 = max([yt1] + ys) if code != "C" else Y_ROW1
    cv.polygon([(0, yb0), (X_END_BOLT, yb0), (X_END_BOLT, yb1), (0, yb1)],
               C["fill_s"], "none")
    for y in ys:                                    # 剪力面（縱向）
        cv.line((0, y), (X_END_BOLT, y), C["sfd"], 4.4)
    cv.line((X_END_BOLT, yt0), (X_END_BOLT, yt1), C["tension"], 4.4)   # 拉力面（橫向）
    for x in X_COLS:
        for y in (Y_ROW1, Y_ROW2):
            cv.circle((x, y), D_H / 2, "none", C["member"], 1.6)
    for y in ys:
        cv.text_px(cv.X(0) - 10, cv.Y(y), "剪力面", 12, C["sfd"], "end", weight="700")
    cv.text_px(cv.X(X_END_BOLT) + 10, cv.Y(0.5 * (yt0 + yt1)), "拉力面",
               12, C["tension"], "start", weight="700")
    agv = nsh * A_GV1
    anv = nsh * A_NV1
    cv.text_px(PW / 2, PH - 88,
               f"A_{{gv}} = {agv:.1f}　A_{{nv}} = {anv:.2f}　A_{{nt}} = {ant:.2f} cm^{{2}}"
               f"（{nsh} 個剪力面）", 12.5, C["muted"])
    cv.text_px(PW / 2, PH - 64,
               f"R_n = {rn:.1f} tf　　上限式 = {cap:.1f} tf", 12.5, C["muted"])
    col = C["accent"] if code == "A" else C["muted"]
    cv.text_px(PW / 2, PH - 38,
               f"φR_n = 0.75 × {cap:.1f} = {phirn:.1f} tf　{note}", 13.5, col, weight="700")
    return cv


def fig2_block_shear():
    """接合幾何 ＋ 三條塊狀剪力路徑：哪一條控制是幾何決定的"""
    panels = [_panel_geom()] + [_panel_path(*p) for p in PATHS]
    compose(panels, cols=2,
            title="塊狀剪力有三條可能的破壞路徑——只算一條就會漏掉控制項",
            sub="剪力面（紫，縱向）自角鋼端延伸至最遠螺栓；拉力面（紅，橫向）位於最遠螺栓處；"
                "紫色網底為被推出的破壞塊",
            note=f"肢趾側只剩 {G3:.0f} cm、肢背側有 {G1:.1f} cm ⇒ 拉力面積最小的路徑 A 控制"
                 f"（{P_BSR_A} tf）；三條路徑的標稱強度都由上限式（剪力面降伏）控制",
            path=f"{OUT}/{TAG}-fig-2-block-shear.svg")
    return f"{OUT}/{TAG}-fig-2-block-shear.svg"


# ══════════════════════════════════════════════════════════
def fig3_limit_states():
    """五個極限狀態並排：第 ④ 項只比控制值高 4.8%"""
    bar_compare(
        [("① 全斷面降伏 GSY", "用 A_g，與 U 無關",
          P_GSY, f"0.9 F_y A_g = {P_GSY:.1f} tf", C["muted"]),
         ("② 淨斷面斷裂 NSF", "考卷表格 U = 0.85",
          P_NSF, f"0.75 F_u A_e = {P_NSF:.1f} tf", C["muted"]),
         ("③ 塊狀剪力 路徑 A", "肢趾側邊距僅 5 cm",
          P_BSR_A, f"0.75(91.4) = {P_BSR_A:.1f} tf", C["accent"]),
         ("④ 螺栓剪力（單剪）", "螺紋不在剪力面",
          P_BOLT, f"0.75 F_{{nv}} A_b (6) = {P_BOLT:.1f} tf", C["load"]),
         ("⑤ 螺栓孔承壓", "R_n = 2.4 d t F_u",
          P_BRG, f"0.75(2.4 d t F_u)(6) = {P_BRG:.1f} tf", C["muted"])],
        title="五個極限狀態全部算完才知道誰控制——第 ④ 項只比控制值高 4.8%",
        sub="題目特地交代「F_{nv} = 4.2 tf/cm^{2}」與「螺紋不在剪力平面上」，"
            "就是為了設下「漏算螺栓剪力」這道關卡",
        note=f"φP_n = {P_ANS} tf（塊狀剪力路徑 A 控制）；若螺紋改在剪力平面，"
             f"F_{{nv}} 降至 3.36 ⇒ 螺栓剪力 {P_BOLT_N} tf，控制項立刻翻轉",
        W=1180,
        path=f"{OUT}/{TAG}-fig-3-limit-states.svg")
    return f"{OUT}/{TAG}-fig-3-limit-states.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_block_shear,  "§4.5",
     "只算一條塊狀剪力路徑（或選錯邊）→ 漏掉肢趾側控制路徑"),
    (fig3_limit_states, "§4.8·§5.2",
     "漏算螺栓剪力這個極限狀態（71.8 tf，與控制值僅差 4.8%）"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"A_gv(每面) = {A_GV1:.1f}　A_nv(每面) = {A_NV1:.2f} cm^2")
    for code, desc, ys, yt0, yt1, nsh, ant, rn, cap, phirn, note in PATHS:
        print(f"  路徑 {code}: A_nt = {ant:.2f} cm^2  → φR_n = {phirn} tf")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<12} 攔：{catches}")
