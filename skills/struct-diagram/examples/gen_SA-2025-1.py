#!/usr/bin/env python3
"""
SA-2025-1 門型剛構架側向勁度 — 解題圖解產生腳本（完整範例）

用法：
    python3 gen_SA-2025-1.py [輸出目錄]

本檔示範 SKILL.md 三條鐵則的具體寫法：
  1. 常數區的每個數字都標明來自解題檔哪一節
  2. 反曲點位置由彎矩內插算出（XI_INFL），不是寫死 0.571
  3. 每張圖在 FIGURES 表裡都寫明「攔什麼錯」
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from structdraw import Canvas, C, FONT_M, compose, column_shape, beam_shape
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SA-2025-1"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SA-2025-1.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §4.3 勁度矩陣（符號約定：轉角與彎矩順時針為正，Δ 與水平力向右為正）
K11, K12, K13, K33 = "8EI/L", "2EI/L", "−6EI/L^{2}", "24EI/L^{3}"

# §4.5–4.6
THETA_RATIO = 3 / 5          # θ = 3Δ/(5L)，順時針為正
K_LATERAL   = 84 / 5         # k = 84EI/(5L³)

# §5.1 端點彎矩（以 PL 為單位）
M_BASE = 2 / 7               # |M_AB| = 2PL/7
M_TOP  = 3 / 14              # |M_BA| = 3PL/14

# 由彎矩線性內插算出的反曲點位置——這是鐵則 2 的落實：算式，不是常數
XI_INFL = M_BASE / (M_BASE + M_TOP)          # = 4/7

# §5.2 側向勁度上下界
K_RIGID_BEAM = 24.0          # 梁無限剛：兩根固端柱
K_NO_BEAM    = 6.0           # 梁無勁度：兩根獨立懸臂柱

# 繪圖用的位移量（純視覺放大，不影響上列任何物理量）
D_DRAW  = 0.185
TH_DRAW = -THETA_RATIO * D_DRAW              # 轉為逆時針正，供 column_shape 使用
MW = 7.0


def frame(cv, color=C["member"], w=MW, dash=None):
    """未變形之門型構架 A(0,0) B(0,1) C(1,1) D(1,0)"""
    for s, e in (((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))):
        cv.line(s, e, color, w, dash=dash, cap="butt")


def ghost(cv):
    frame(cv, C["ghost"], 3.0, dash="6 5")


# ══════════════════════════════════════════════════════════
def fig1_frame():
    """題目重繪：取代低解析度截圖，把節點命名固定下來"""
    cv = Canvas(540, 430, sx=190, ox=155, oy=125, bg="#FFFFFF")
    frame(cv)
    cv.fixed_support((0, 0)); cv.fixed_support((1, 0))
    cv.arrow((1, 1), (1.40, 1), C["load"], 3.6, 12)
    cv.math((1.40, 1), "P", 20, C["load"], "start", dx=10, weight="700")
    for p, lab, ax, ay in ((0, 0), "A", -20, 22), ((0, 1), "B", -18, -15), \
                          ((1, 1), "C", 17, -15), ((1, 0), "D", 20, 22):
        cv.dot(p, 5.5); cv.text(p, lab, 17, C["text"], weight="700", dx=ax, dy=ay)
    cv.math((0.5, 1), "EI", 17, C["muted"], dy=-17)
    cv.math((0, 0.55), "EI", 17, C["muted"], "end", dx=-13)
    cv.math((1, 0.55), "EI", 17, C["muted"], "start", dx=13)
    cv.dim((0, 0), (1, 0), "L", off=58, label_off=16)
    cv.dim((0, 0), (0, 1), "L", off=-62, label_off=-15)
    cv.text_px(270, 400, "所有桿件 EI、L 相同；柱底 A、D 固定；B、C 為剛接；忽略軸向變形",
               13.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-frame.svg")


def fig2_dof():
    """自由度辨識：把「忽略軸向變形」翻譯成看得見的約束"""
    cv = Canvas(770, 410, sx=185, ox=140, oy=108, bg="#FFFFFF")
    frame(cv, "#9AA4B2")
    cv.fixed_support((0, 0)); cv.fixed_support((1, 0))
    cv.arrow((1.07, 1), (1.42, 1), C["deform"], 3.4, 12)
    cv.math((1.42, 1), "Δ", 20, C["deform"], "start", dx=9, weight="700")

    for p, lx, ly, nm in ((0, 1), -46, -10, "θ_{B}"), ((1, 1), 40, 24, "θ_{C}"):
        cv.moment_arrow(p, r=28, ccw=False, color=C["accent"], w=2.8, span=235, start=205)
        cv.text_px(cv.X(p[0]) + lx, cv.Y(p[1]) + ly, nm, 19, C["accent"],
                   weight="700", italic=True, font=FONT_M)

    def cross(px, py, s=8, col="#C0392B"):
        cv.parts.append(f'<line x1="{px-s}" y1="{py-s}" x2="{px+s}" y2="{py+s}" '
                        f'stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')
        cv.parts.append(f'<line x1="{px-s}" y1="{py+s}" x2="{px+s}" y2="{py-s}" '
                        f'stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')

    for bx in (0, 1):
        cv.arrow((bx, 1.12), (bx, 1.30), "#D6AEA6", 2.4, 8)
        cross(cv.X(bx) + 17, cv.Y(1.21))
    for p, lab, ax, ay in ((0, 0), "A", -20, 22), ((0, 1), "B", 20, 20), \
                          ((1, 1), "C", -20, 20), ((1, 0), "D", 20, 22):
        cv.dot(p, 5.5, fill="#4A5568")
        cv.text(p, lab, 16, C["text"], weight="700", dx=ax, dy=ay)

    cv.rect_px(478, 92, 274, 74, "#EEF4FF", 12, "#C7D9F5", 1.3)
    cv.text_px(615, 116, "有效自由度只剩 3 個", 14.5, "#1D4ED8", weight="700")
    cv.text_px(615, 144, "{ θ_{B} ,  θ_{C} ,  Δ }", 19, "#1D4ED8", italic=True, font=FONT_M)
    cv.rect_px(478, 196, 274, 106, "#FFF6F1", 12, "#F0C9B8", 1.3)
    cv.text_px(496, 222, "被消去的自由度", 13.5, "#9A3412", "start", weight="700")
    for i, t in enumerate(["柱不縮短 → B、C 垂直位移 = 0",
                           "梁不伸縮 → B、C 水平位移相同",
                           "柱底全固定 → 不貢獻自由度"]):
        cross(504, 248 + i*22, 6)
        cv.text_px(518, 248 + i*22, t, 12.5, "#9A3412", "start")
    cv.text_px(385, 386, "自由度數目 = 勁度矩陣階數。這一步錯，後面整個矩陣都白算。",
               13.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-dof.svg")


def _unit_panel(tB, tC, dl, title, sub, mB, mB_cw, mC, mC_cw, hlab, hsgn, PW=362, PH=372):
    """單一單位位移狀態。tB/tC 為順時針正之轉角（與解題檔一致）"""
    cv = Canvas(PW, PH, sx=150, ox=95, oy=92)
    cv.panel(title, sub)
    ghost(cv)
    b, c = -tB, -tC                      # 轉為逆時針正
    cv.poly(column_shape((0, 0), 1.0, dl, b), C["deform"], 5.0)
    cv.poly(column_shape((1, 0), 1.0, dl, c), C["deform"], 5.0)
    cv.poly(beam_shape((dl, 1), 1.0, b, c), C["deform"], 5.0)
    cv.fixed_support((0, 0), size=17); cv.fixed_support((1, 0), size=17)
    cv.dot((dl, 1), 4.5, fill=C["deform"]); cv.dot((1 + dl, 1), 4.5, fill=C["deform"])
    cv.moment_arrow((dl, 1), r=26, ccw=not mB_cw, color=C["load"], w=2.8, span=235, start=205)
    cv.math_px(cv.X(dl) - 48, cv.Y(1) - 38, mB, 14, C["load"], weight="700")
    cv.moment_arrow((1 + dl, 1), r=26, ccw=not mC_cw, color=C["load"], w=2.8, span=235, start=205)
    cv.math_px(cv.X(1 + dl) + 6, cv.Y(1) - 42, mC, 14, C["load"], "start", weight="700")
    x0 = 1 + dl
    a, b2 = ((x0 + 0.10, x0 + 0.44) if hsgn > 0 else (x0 + 0.44, x0 + 0.10))
    cv.arrow((a, 1), (b2, 1), C["load"], 3.2, 11)
    cv.math_px(cv.X(x0 + 0.27), cv.Y(1) + 24, hlab, 14, C["load"], weight="700")
    return cv


def fig3_unit_states():
    """勁度矩陣三行的物理意義：耦合項正負號的唯一直覺檢核"""
    panels = [
        _unit_panel(1, 0, 0.0,  "狀態 ①：θ_B = 1（其餘鎖住）", "→ 勁度矩陣第 1 行",
                    K11, True, K12, True, K13, -1),
        _unit_panel(0, 1, 0.0,  "狀態 ②：θ_C = 1（其餘鎖住）", "→ 勁度矩陣第 2 行",
                    K12, True, K11, True, K13, -1),
        _unit_panel(0, 0, 0.16, "狀態 ③：Δ = 1（B、C 不轉動）", "→ 勁度矩陣第 3 行",
                    K13, False, K13, False, K33, +1),
    ]
    compose(panels,
            title="勁度矩陣的每一行 ＝ 令該自由度產生單位位移、其餘全部鎖住時，必須施加的節點力",
            sub="符號約定：轉角與彎矩以順時針為正，Δ 與水平力以向右為正（與傾角變位法一致）",
            note="把三個狀態的節點力依序填成三行即為 [K]。灰虛線＝原結構，藍實線＝該狀態之變形，紅色＝所需施加的力",
            path=f"{OUT}/{TAG}-fig-3-unit-states.svg")
    return f"{OUT}/{TAG}-fig-3-unit-states.svg"


def fig4_deflected_bmd():
    """變形形狀與彎矩圖：兩個與矩陣運算完全獨立的檢核"""
    PW, PH = 440, 410

    a = Canvas(PW, PH, sx=172, ox=126, oy=96)
    a.panel("變形形狀（側移模式）", "柱：雙曲率　梁：反對稱雙曲率")
    ghost(a)
    a.poly(column_shape((0, 0), 1.0, D_DRAW, TH_DRAW), C["deform"], 5.4)
    a.poly(column_shape((1, 0), 1.0, D_DRAW, TH_DRAW), C["deform"], 5.4)
    a.poly(beam_shape((D_DRAW, 1), 1.0, TH_DRAW, TH_DRAW), C["deform"], 5.4)
    a.fixed_support((0, 0), size=18); a.fixed_support((1, 0), size=18)
    u = D_DRAW * (2.4 * XI_INFL**2 - 1.4 * XI_INFL**3)
    for bx in (0, 1):
        a.dot((bx + u, XI_INFL), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    a.dot((D_DRAW + 0.5, 1), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    a.math_px(a.X(u) + 16, a.Y(XI_INFL), "4L/7", 13, C["accent"], "start", weight="700")
    a.math_px(a.X(D_DRAW + 0.5), a.Y(1) + 24, "L/2", 13, C["accent"], weight="700")
    a.arrow((1 + D_DRAW, 1), (1 + D_DRAW + 0.30, 1), C["load"], 3.4, 12)
    a.math((1 + D_DRAW + 0.30, 1), "P", 18, C["load"], "start", dx=8, weight="700")
    a.text_px(PW/2, 352, "○ ＝ 反曲點（M = 0）", 13, C["accent"], weight="700")
    a.math_px(PW/2, 382, "Δ = 5PL^{3}/84EI 　 θ_{B} = θ_{C} = PL^{2}/28EI", 14.5,
              C["deform"], weight="700")

    b = Canvas(PW, PH, sx=172, ox=126, oy=96)
    b.panel("彎矩圖（繪於受拉側）", "節點彎矩平衡與樓層剪力檢核")
    ms = 0.60
    Mb, Mt = M_BASE * ms, M_TOP * ms
    for bx in (0, 1):                                   # 兩柱變形相同 → 受拉側相同
        b.polygon([(bx, 0), (bx - Mb, 0), (bx, XI_INFL)], C["fill_m"], C["bmd"], 2)
        b.polygon([(bx, XI_INFL), (bx + Mt, 1), (bx, 1)], C["fill_m"], C["bmd"], 2)
    b.polygon([(0, 1), (0, 1 - Mt), (0.5, 1)], C["fill_m"], C["bmd"], 2)
    b.polygon([(0.5, 1), (1, 1 + Mt), (1, 1)], C["fill_m"], C["bmd"], 2)
    frame(b, "#4A5568", 3.4)
    b.fixed_support((0, 0), size=18); b.fixed_support((1, 0), size=18)
    b.dot((0.5, 1), 4.6, fill="#FFFFFF", stroke=C["bmd"], w=2.6)
    b.math_px(b.X(-Mb) - 6, b.Y(0.02), "2PL/7", 13, C["bmd"], "end", weight="700")
    b.math_px(b.X(1 + Mt) + 6, b.Y(0.97), "3PL/14", 13, C["bmd"], "start", weight="700")
    b.text_px(b.X(0.5), b.Y(1 + Mt) - 16, "梁中點 M = 0", 12.5, C["bmd"], weight="700")
    b.math_px(PW/2, 352, "M_{BA} + M_{BC} = 0 ✓", 13, C["bmd"], weight="700")
    b.text_px(PW/2, 382, "每柱剪力 = (2PL/7 + 3PL/14)/L = P/2 → 兩柱合計 = P ✓",
              13.5, C["bmd"], weight="700")

    compose([a, b], title="解出 Δ 之後：用幾何與平衡回頭檢核答案",
            path=f"{OUT}/{TAG}-fig-4-deflected-bmd.svg")
    return f"{OUT}/{TAG}-fig-4-deflected-bmd.svg"


def fig5_spectrum():
    """側向勁度光譜：把靜態凝縮扣掉的那一項變成可理解的物理量"""
    def sketch(mini, i):
        D = 0.30
        th = (0.0, -THETA_RATIO * D, -1.5 * D)[i]
        col = ("#1D4ED8", "#B45309", "#94A3B8")[i]
        for s, e in (((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))):
            mini.line(s, e, C["ghost"], 2.2, dash="4 4", cap="butt")
        mini.poly(column_shape((0, 0), 1.0, D, th), col, 3.2)
        mini.poly(column_shape((1, 0), 1.0, D, th), col, 3.2)
        mini.poly(beam_shape((D, 1), 1.0, th, th), col, 3.2)

    bar_compare(
        [("梁無限剛　EI_{b} → ∞", "θ_{B} = θ_{C} = 0", K_RIGID_BEAM, "24EI/L^{3}", "#1D4ED8"),
         ("本題　梁柱同 EI/L", "θ = 3Δ/5L", K_LATERAL,
          f"84EI/5L^{{3}} = {K_LATERAL:.1f}EI/L^{{3}}", "#B45309"),
         ("梁無勁度　EI_{b} → 0", "兩根獨立懸臂柱", K_NO_BEAM, "6EI/L^{3}", "#94A3B8")],
        title="靜態凝縮做了什麼？——梁的束縛能力決定側向勁度折減多少",
        sub="旋轉自由度被凝縮掉，代價就是 K_{33} 被扣掉一項；梁越軟，扣得越多",
        note=f"答案必落在 {K_NO_BEAM:g}EI/L^{{3}} 與 {K_RIGID_BEAM:g}EI/L^{{3}} 之間，"
             f"否則量級就錯了", sketch=sketch,
        path=f"{OUT}/{TAG}-fig-5-stiffness-spectrum.svg")
    return f"{OUT}/{TAG}-fig-5-stiffness-spectrum.svg"


# ══════════════════════════════════════════════════════════
# 每張圖攔下什麼錯 —— 寫不出來的就不該畫
# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig1_frame,          "§1",   "作答時 B、C 標反 → 矩陣行列對應錯亂"),
    (fig2_dof,            "§4.1", "誤把 B、C 水平位移當兩個自由度 → 寫出 4×4 矩陣"),
    (fig3_unit_states,    "§4.3", "K₁₃ 正負號寫反"),
    (fig4_deflected_bmd,  "§5.1", "反曲點不在 4L/7 或梁中點彎矩不為零 → 前面必有錯"),
    (fig5_spectrum,       "§5.2", "答案量級落在物理上下界之外"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<6} 攔：{catches}")
    print(f"\n完成。接著執行： python3 ../scripts/render.py {OUT}")
