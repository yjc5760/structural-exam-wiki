#!/usr/bin/env python3
"""
SS-2005-1 單角鋼螺栓接合之設計拉力強度 — 解題圖解產生腳本

用法：
    python3 gen_SS-2005-1.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個尺寸、面積、強度都標明來自 SS-2005-1.md 哪一節
  2. 四條塊狀剪力路徑的破壞面由螺栓座標算出（PATHS 由 Y_ROW1/Y_ROW2 推得），
     A_nt、選式、塊內螺栓數與受力分擔都由 block_shear_tw() 算出，改一個邊距會一起變
     （2026-11-03 勘誤：改用台灣二式，主算 6 栓撕出塊；單行路徑按 P/2 換算等效總力）
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
# 輸入（全部來自 SS-2005-1.md；強度一律由下方算式算出，勿手填）
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
PHI_BS = 0.75
N_BOLT = 6
A_G    = (2 * W_LEG - T) * T                # 76.0 cm^2
A_B    = math.pi * D_B ** 2 / 4             # 3.801 cm^2
# §4.3／4.4／4.6／4.7 其餘四個極限狀態（由算式算出，勿手填）
P_GSY  = 0.9 * FY * A_G                                   # 171.0
P_NSF  = 0.75 * FU * 0.85 * (A_G - 2 * D_H * T)           # 174.1
P_BOLT = 0.75 * FNV * A_B * N_BOLT                        # 71.8
P_BRG  = 0.75 * 2.4 * D_B * T * FU * N_BOLT               # 194.8
# §5.2 若螺紋改在剪力平面（F_nv ≈ 0.8 × 4.2）
P_BOLT_N = 0.75 * 0.8 * FNV * A_B * N_BOLT                # 57.5

# ── 繪圖座標：x 沿載重方向（角鋼端在 x=0），y 由肢趾(0) 至肢背(W_LEG) ──
Y_HEEL = W_LEG                  # 肢背（外伸肢所在）
Y_ROW1 = W_LEG - G1             # 12.5（第 1 行，距肢背 7.5）
Y_ROW2 = W_LEG - G1 - G2        # 5.0 （第 2 行，距肢趾 5.0）
Y_TOE  = 0.0
ROWS   = (Y_ROW1, Y_ROW2)
X_COLS = [E_END, E_END + S_LONG, E_END + 2 * S_LONG]   # 5, 12.5, 20
X_END_BOLT = X_COLS[-1]
X_FAR  = 30.0                   # 角鋼往載重方向延伸至此（截斷）


def block_shear_tw(ys, yt0, yt1):
    """台灣規範（極限設計法）塊狀剪力二式，φ = 0.75（§4.5）。
    ys：剪力面所在 y（每面長 L_SH、扣 2.5 孔）；拉力面自 yt0 至 yt1（位於最遠螺栓處）。
    拉力面扣孔：落在剪力面上的那一行扣半孔，夾在拉力面內部的行扣整孔。
    回傳 dict：面積、選式、R_n、上限、φR_n、塊內螺栓數、受力分擔、等效總力。"""
    nsh = len(ys)
    agv, anv = nsh * A_GV1, nsh * A_NV1
    holes = sum(0.5 if y in ys else 1.0 for y in ROWS if yt0 <= y <= yt1)
    agt = (yt1 - yt0) * T
    ant = (yt1 - yt0 - holes * D_H) * T
    if FU * ant >= 0.6 * FU * anv:
        case, rn = "I", 0.6 * FY * agv + FU * ant
        parts = (0.6 * FY * agv, FU * ant)
    else:
        case, rn = "II", 0.6 * FU * anv + FY * agt
        parts = (0.6 * FU * anv, FY * agt)
    cap = 0.6 * FU * anv + FU * ant
    phirn = PHI_BS * min(rn, cap)
    yb0, yb1 = min([yt0] + ys), max([yt1] + ys)
    nb = sum(len(X_COLS) for y in ROWS if yb0 <= y <= yb1)
    share = nb / N_BOLT
    # 雙路徑檢核：AISC 360-05 起之單式
    aisc = PHI_BS * (min(0.6 * FU * anv, 0.6 * FY * agv) + FU * ant)
    return dict(nsh=nsh, agv=agv, anv=anv, agt=agt, ant=ant, holes=holes, case=case,
                rn=rn, parts=parts, cap=cap, phirn=phirn, nb=nb, share=share,
                equiv=phirn / share, aisc=aisc, aisc_equiv=aisc / share,
                yb0=yb0, yb1=yb1)


# PATHS：(代號, 標題, 說明, 剪力面 y 座標串, 拉力面 y0, 拉力面 y1)
PATHS = [
    ("6 栓塊", "③ 塊狀剪力　主算：6 栓撕出塊", "沿第 1 行剪出 ＋ 經第 2 行拉裂至肢趾",
     [Y_ROW1], Y_TOE, Y_ROW1),
    ("A", "路徑 A（說明用）", "只沿第 2 行剪出 ＋ 拉裂至肢趾",
     [Y_ROW2], Y_TOE, Y_ROW2),
    ("B", "路徑 B（說明用）", "只沿第 1 行剪出 ＋ 拉裂至肢背",
     [Y_ROW1], Y_ROW1, Y_HEEL),
    ("C", "路徑 C（說明用）", "兩行同時剪出 ＋ 拉裂行間",
     [Y_ROW2, Y_ROW1], Y_ROW2, Y_ROW1),
]
BS = {code: block_shear_tw(ys, y0, y1) for code, _, _, ys, y0, y1 in PATHS}
P_BSR = BS["6 栓塊"]["phirn"]                                   # 100.2
LIMITS = [("④ 螺栓剪力", P_BOLT), ("③ 塊狀剪力（6 栓塊）", P_BSR),
          ("① 全斷面降伏", P_GSY), ("② 淨斷面斷裂", P_NSF), ("⑤ 承壓", P_BRG)]
P_ANS  = min(v for _, v in LIMITS)                               # 71.8（螺栓剪力）
# 單行路徑換算後的等效總力須不低於螺栓剪力，否則控制模式改變
assert P_ANS == P_BOLT
assert all(BS[c]["equiv"] > P_ANS for c in BS)

PW, PH = 460, 530
SXX, OXX, OYY = 10.67, 95, 160


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
            for y in ROWS:
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
    cv.dim((0, Y_HEEL), (0, Y_ROW1), f"{G1:.1f}", off=44, label_off=16)
    cv.dim((0, Y_ROW1), (0, Y_ROW2), f"{G2:.1f}", off=44, label_off=16)
    cv.dim((0, Y_ROW2), (0, Y_TOE), f"{G3:.1f}", off=44, label_off=16)
    cv.dim((0, Y_TOE), (X_COLS[0], Y_TOE), f"{E_END:.0f}", off=40, label_off=13)
    cv.dim((X_COLS[0], Y_TOE), (X_COLS[1], Y_TOE), f"{S_LONG:.1f}", off=40, label_off=13)
    cv.dim((X_COLS[1], Y_TOE), (X_COLS[2], Y_TOE), f"{S_LONG:.1f}", off=40, label_off=13)
    cv.text_px(cv.X(X_FAR / 2), cv.Y(Y_TOE) + 68, "端距 e ＋ 2s ＝ 剪力面長度 20 cm（尺寸單位 cm）",
               12, C["muted"])
    cv.text_px(cv.X(X_FAR / 2), cv.Y(Y_TOE) + 92, "兩行各 3 栓，各承總拉力的一半（P/2）",
               12, C["accent"], weight="700")
    cv.text_px(cv.X(X_FAR) + 6, cv.Y(Y_HEEL), "肢背", 12, C["muted"], "start")
    cv.text_px(cv.X(X_FAR) + 6, cv.Y(Y_TOE), "肢趾", 12, C["muted"], "start")
    cv.text_px(cv.X(X_END_BOLT + 1.6), cv.Y(Y_ROW1), "第 1 行", 11.5, C["muted"], "start")
    cv.text_px(cv.X(X_END_BOLT + 1.6), cv.Y(Y_ROW2), "第 2 行", 11.5, C["muted"], "start")
    return cv


def _panel_path(code, title, desc, ys, yt0, yt1):
    r = BS[code]
    main = r["share"] == 1.0 and code != "C"
    cv = new_panel(title, desc)
    draw_leg(cv, faint=True)
    # 破壞塊（介於剪力面／自由邊之間、自角鋼端至最遠螺栓）
    yb0, yb1 = r["yb0"], r["yb1"]
    cv.polygon([(0, yb0), (X_END_BOLT, yb0), (X_END_BOLT, yb1), (0, yb1)],
               C["fill_s"], "none")
    for y in ys:                                    # 剪力面（縱向）
        cv.line((0, y), (X_END_BOLT, y), C["sfd"], 4.4)
    cv.line((X_END_BOLT, yt0), (X_END_BOLT, yt1), C["tension"], 4.4)   # 拉力面（橫向）
    for x in X_COLS:
        for y in ROWS:
            inside = yb0 <= y <= yb1
            cv.circle((x, y), D_H / 2, C["accent"] if inside else "none",
                      C["accent"] if inside else C["member2"], 1.6)
    for y in ys:
        cv.text_px(cv.X(0) - 10, cv.Y(y), "剪力面", 12, C["sfd"], "end", weight="700")
    cv.text_px(cv.X(X_END_BOLT) + 10, cv.Y(0.5 * (yt0 + yt1)), "拉力面",
               12, C["tension"], "start", weight="700")
    cv.text_px(PW / 2, PH - 130,
               f"A_{{gv}} = {r['agv']:.1f}　A_{{nv}} = {r['anv']:.2f}　"
               f"A_{{gt}} = {r['agt']:.1f}　A_{{nt}} = {r['ant']:.2f} cm^{{2}}", 12, C["muted"])
    if r["case"] == "I":
        sel = (f"F_uA_{{nt}} = {FU*r['ant']:.1f} ≥ 0.6F_uA_{{nv}} = {0.6*FU*r['anv']:.1f}"
               f" ⇒ 0.6F_yA_{{gv}} + F_uA_{{nt}}")
    else:
        sel = (f"0.6F_uA_{{nv}} = {0.6*FU*r['anv']:.1f} > F_uA_{{nt}} = {FU*r['ant']:.1f}"
               f" ⇒ 0.6F_uA_{{nv}} + F_yA_{{gt}}")
    cv.text_px(PW / 2, PH - 107, sel, 12, C["muted"])
    cv.text_px(PW / 2, PH - 84,
               f"R_n = {r['parts'][0]:.1f} + {r['parts'][1]:.1f} = {r['rn']:.1f} tf"
               f"（上限 {r['cap']:.1f}）⇒ φR_n = {r['phirn']:.1f} tf", 12.5, C["text"])
    if r["share"] < 1.0:
        l1 = f"塊內只含 {r['nb']} 栓、只承 P/2"
        l2 = f"等效總力 = {r['phirn']:.1f} ÷ 0.5 = {r['equiv']:.1f} tf　不控制"
        col = C["muted"]
    elif main:
        l1 = "塊內含全部 6 栓、承全部 P"
        l2 = f"φR_n = {r['phirn']:.1f} tf ＞ 螺栓剪力 {P_BOLT:.1f} tf　不控制"
        col = C["sfd"]
    else:
        l1 = "兩個剪力面；保守以全部 P 比較"
        l2 = f"φR_n = {r['phirn']:.1f} tf　不控制"
        col = C["muted"]
    cv.text_px(PW / 2, PH - 60, l1, 13, col, weight="700")
    cv.text_px(PW / 2, PH - 36, l2, 13, col, weight="700")
    return cv


def _panel_equiv():
    """換算成總拉力 P 後，各路徑與螺栓剪力並排"""
    cv = new_panel("換算成總拉力 P 後比較", "部分撕出塊 ÷ 受力分擔比 ＝ 等效總力（tf）")
    rows = [("④ 螺栓剪力（6 顆單剪）", P_BOLT, C["accent"])]
    rows += [((f"③ 6 栓撕出塊" if c == "6 栓塊" else f"路徑 {c}") +
              (f"（{BS[c]['nb']} 栓，÷0.5）" if BS[c]["share"] < 1 else ""),
              BS[c]["equiv"], C["sfd"] if c == "6 栓塊" else C["member2"])
             for c in ("6 栓塊", "C", "A", "B")]
    peak = max(v for _, v, _ in rows)
    x0, bw, y = 40, 300, 100
    for name, v, col in rows:
        cv.text_px(x0, y, name, 12.5, C["text"], "start", weight="700")
        cv.rect_px(x0, y + 12, bw, 22, "#EDF1F6", 6)
        cv.rect_px(x0, y + 12, bw * v / peak, 22, col, 6)
        cv.text_px(x0 + bw * v / peak + 8, y + 23, f"{v:.1f}", 13, col, "start", weight="700")
        y += 66
    cv.text_px(PW / 2, PH - 60, f"最小者為螺栓剪力 {P_ANS:.1f} tf ⇒ 全題控制", 13.5,
               C["accent"], weight="700")
    cv.text_px(PW / 2, PH - 36, f"單行窄條直接比總力（單式誤得 {BS['A']['aisc']:.1f} tf）是本題易犯錯誤", 12,
               C["muted"])
    return cv


def fig2_block_shear():
    """接合幾何 ＋ 6 栓撕出塊 ＋ 三條說明路徑 ＋ 等效總力比較"""
    panels = ([_panel_geom()] + [_panel_path(*p) for p in PATHS] + [_panel_equiv()])
    r = BS["6 栓塊"]
    compose(panels, cols=3,
            title="塊狀剪力：撕出塊要對應它承擔的力——只含 3 栓的單行窄條只承 P/2",
            sub="剪力面（紫，縱向）自角鋼端延伸至最遠螺栓；拉力面（紅，橫向）位於最遠螺栓處；"
                "紫色網底為撕出塊，橘色實心孔為塊內螺栓",
            note=f"台灣二式、φ = 0.75：主算 6 栓撕出塊 {r['phirn']:.1f} tf；"
                 f"單行路徑 A、B 換算等效總力 {BS['A']['equiv']:.1f}、{BS['B']['equiv']:.1f} tf；"
                 f"行間路徑 C {BS['C']['phirn']:.1f} tf——全部大於螺栓剪力 {P_BOLT:.1f} tf，塊狀剪力不控制",
            path=f"{OUT}/{TAG}-fig-2-block-shear.svg")
    return f"{OUT}/{TAG}-fig-2-block-shear.svg"


# ══════════════════════════════════════════════════════════
def fig3_limit_states():
    """五個極限狀態並排：螺栓剪力控制，塊狀剪力（6 栓塊）次之"""
    r = BS["6 栓塊"]
    bar_compare(
        [("④ 螺栓剪力（單剪）", "螺紋不在剪力面｜控制",
          P_BOLT, f"0.75 F_{{nv}} A_b (6) = {P_BOLT:.1f} tf", C["accent"]),
         ("③ 塊狀剪力（6 栓塊）", "沿第 1 行剪、拉至肢趾",
          P_BSR, f"0.75({r['rn']:.1f}) = {P_BSR:.1f} tf", C["sfd"]),
         ("① 全斷面降伏 GSY", "用 A_g，與 U 無關",
          P_GSY, f"0.9 F_y A_g = {P_GSY:.1f} tf", C["muted"]),
         ("② 淨斷面斷裂 NSF", "考卷表格 U = 0.85",
          P_NSF, f"0.75 F_u A_e = {P_NSF:.1f} tf", C["muted"]),
         ("⑤ 螺栓孔承壓", "R_n = 2.4 d t F_u",
          P_BRG, f"0.75(2.4 d t F_u)(6) = {P_BRG:.1f} tf", C["muted"])],
        title=f"五個極限狀態全部算完：螺栓剪力 {P_BOLT:.1f} tf 控制，塊狀剪力 {P_BSR:.1f} tf 次之",
        sub="題目特地交代「F_{nv} = 4.2 tf/cm^{2}」與「螺紋不在剪力平面上」，"
            "就是要考生算出這個控制值",
        note=f"φP_n = {P_ANS:.1f} tf（螺栓剪力控制）；若螺紋改在剪力平面，"
             f"F_{{nv}} 降至 3.36 ⇒ 螺栓剪力 {P_BOLT_N:.1f} tf，仍由螺栓剪力控制",
        W=1180,
        path=f"{OUT}/{TAG}-fig-3-limit-states.svg")
    return f"{OUT}/{TAG}-fig-3-limit-states.svg"


# ══════════════════════════════════════════════════════════
# 圖 1：題目附圖重繪（依題目正本 SS-2005-1-problem.md §4 判讀清單，2026-11-02 已確認）
# 只用考卷給的尺寸，與上方解題常數分開；不含任何解題結果。接合板外形為示意。
# ══════════════════════════════════════════════════════════
Q_LEG = 20.0                  # §1 題文 L200×200×20：肢寬 20 cm
Q_G1, Q_G2 = 7.5, 7.5         # #2 自角鋼背量 7.5 cm 至第 1 排、再 7.5 cm 至第 2 排
Q_E1 = 5.0                    # #3 角鋼端部至第 1 顆 5 cm
Q_N, Q_S = 3, 7.5             # #1 每排 3 顆；#3 間距 2@7.5 cm = 15 cm
Q_E2 = 5.0                    # #3 末顆至接合板邊緣 5 cm
Q_TOE = Q_LEG - Q_G1 - Q_G2   # 第 2 排至肢趾（推得值 5 cm）
Q_XB = [Q_E1 + k * Q_S for k in range(Q_N)]          # 0 = 角鋼端部
Q_YB = [Q_LEG - Q_G1, Q_LEG - Q_G1 - Q_G2]           # 0 = 肢趾，Q_LEG = 角鋼背
Q_XP = Q_XB[-1] + Q_E2                               # 接合板邊緣


def fig1_problem():
    W1, H1, sx = 760, 470, 6.5
    cv = Canvas(W1, H1, sx=sx, ox=250, oy=170)
    cv.panel("平面", "接合板外形示意；角鋼與螺栓位置依比例")
    plate = [(-14, -10), (8, -10), (Q_XP, -2), (Q_XP, Q_LEG + 2), (8, Q_LEG + 10), (-14, Q_LEG + 10)]
    cv.polygon(plate, C["border"], C["member"], 1.8)
    cv.polygon([(0, 0), (52, 0), (52, Q_LEG), (0, Q_LEG)], C["fill_c"], C["member"], 1.8)
    cv.line((0, Q_LEG - 0.8), (52, Q_LEG - 0.8), C["member"], 1.2)      # 外伸肢（背側雙線）
    for x in Q_XB:
        for y in Q_YB:
            cv.circle((x, y), 1.1, fill="#FFFFFF", stroke=C["member"], w=1.8)
    cv.arrow((54, Q_LEG / 2), (64, Q_LEG / 2), C["load"], 3.4, 12)
    cv.text((-14, Q_LEG + 10), "接合板", 13, C["text"], "start", dy=-14, weight="700")
    cv.text((52, Q_LEG), "L200×200×20", 13, C["text"], "end", dy=-14, weight="700")
    xl = -(14 * sx) - 34                                   # 縱向尺寸線放在接合板外側
    cv.dim((0, Q_YB[0]), (0, Q_LEG), f"{Q_G1} cm", off=xl, label_off=-34)
    cv.dim((0, Q_YB[1]), (0, Q_YB[0]), f"{Q_G2} cm", off=xl, label_off=-34)
    cv.dim((0, 0), (Q_XB[0], 0), "", off=95)
    cv.dim((Q_XB[0], 0), (Q_XB[-1], 0), f"2@{Q_S} cm={Q_S * (Q_N - 1):g} cm", off=95, label_off=36)
    cv.dim((Q_XB[-1], 0), (Q_XP, 0), "", off=95)
    yb = cv.Y(0) + 95
    cv.math_px(cv.X(0) - 8, yb, f"{Q_E1:g} cm", 14, C["dim"], "end")
    cv.math_px(cv.X(Q_XP) + 8, yb, f"{Q_E2:g} cm", 14, C["dim"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2005-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；只畫考卷所給條件",
            note="7.5 cm 自角鋼背量起；末顆螺栓至接合板邊緣 5 cm；第 2 排至肢趾 5 cm 為推得值",
            path=path)
    return path


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "7.5 cm 量測基準讀錯（自肢趾量起）；末顆至接合板邊緣 5 cm 誤當角鋼端距"),
    (fig2_block_shear,  "§4.5",
     "把只含 3 栓、只承 P/2 的單行撕出塊直接與總拉力比較（誤得 68.5 tf 控制），"
     "並漏算含全部 6 栓的撕出塊"),
    (fig3_limit_states, "§4.8·§5.1",
     "把單行撕出塊誤判為控制項；正確為螺栓剪力 71.8 tf 控制"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert Q_TOE == 5.0
    print(f"A_gv(每面) = {A_GV1:.1f}　A_nv(每面) = {A_NV1:.2f} cm^2")
    for code, *_ in PATHS:
        r = BS[code]
        print(f"  {code}: 式{r['case']} A_gt={r['agt']:.2f} A_nt={r['ant']:.2f} "
              f"R_n={r['rn']:.2f} 上限={r['cap']:.2f} φR_n={r['phirn']:.2f} "
              f"(單式 {r['aisc']:.2f}) 栓數={r['nb']} 等效={r['equiv']:.2f} (單式 {r['aisc_equiv']:.2f})")
    print(f"GSY={P_GSY:.2f} NSF={P_NSF:.2f} 螺栓剪力={P_BOLT:.2f} 承壓={P_BRG:.2f} "
          f"N 型={P_BOLT_N:.2f} ⇒ φP_n={P_ANS:.2f}")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<12} 攔：{catches}")
