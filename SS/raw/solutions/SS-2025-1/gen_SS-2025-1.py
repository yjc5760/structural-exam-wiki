#!/usr/bin/env python3
"""
SS-2025-1 銲接 H 型鋼梁 φbMnx — 解題圖解產生腳本

用法：
    python3 gen_SS-2025-1.py [輸出目錄]

畫兩張圖：
  1. 斷面重繪＋寬厚比判定（取代低解析度截圖 fig-1.png）
     攔：翼板寬厚比分母算成 t_f 而非 2t_f；結實/非結實斷面判斷錯
  2. 彈性（Sx）vs 塑性（Zx）應力分布對照
     攔：結實斷面＋完全支撐時誤用 Sx 而非 Zx；Zx 漏算腹板貢獻
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".claude", "skills",
                                 "struct-diagram", "scripts"))
# 上面路徑供備援；若在本機環境直接用 skill 目錄的絕對路徑亦可
SKILL_SCRIPTS = "/sessions/brave-elegant-hypatia/mnt/.claude/skills/struct-diagram/scripts"
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2025-1"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2025-1.md §1／§4，勿手動改動）
# ══════════════════════════════════════════════════════════
BF, TF = 30.0, 1.5      # §1 翼板寬、翼板厚 (cm)
HW, TW = 42.0, 1.5      # §1 腹板淨高、腹板厚 (cm)
FY = 2.5                # §1 降伏強度 (tf/cm²)
D = HW + 2 * TF          # 全深

# §4 Step2：寬厚比判定（公式，非手打數值）
LAM_F  = BF / (2 * TF)          # 翼板寬厚比：懸臂長 bf/2 除以 tf
LAM_PF = 17 / math.sqrt(FY)
LAM_W  = HW / TW
LAM_PW = 170 / math.sqrt(FY)
FLANGE_COMPACT = LAM_F < LAM_PF
WEB_COMPACT    = LAM_W < LAM_PW

# §4 Step4：塑性斷面模數分解（公式，非手打數值）
ARM_FLANGE = HW / 2 + TF / 2                       # 翼板形心到中性軸距離 = 21.75
ARM_WEB    = HW / 4                                # 半腹板形心到中性軸距離 = 10.5
Z_FLANGE   = 2 * BF * TF * ARM_FLANGE              # = 1957.5
Z_WEB      = 2 * (HW / 2) * TW * ARM_WEB           # = 661.5
ZX         = Z_FLANGE + Z_WEB                      # = 2619
MP         = FY * ZX                               # = 6547.5
PHI_B      = 0.9
PHI_MN     = PHI_B * MP                             # = 5892.75


def section_outline(dx=0.0, dy=0.0):
    """I 形斷面外框座標（逆時針），可整體平移 dx,dy"""
    hw2, tw2, bf2 = HW / 2, TW / 2, BF / 2
    pts = [(-bf2, hw2 + TF), (bf2, hw2 + TF), (bf2, hw2), (tw2, hw2),
           (tw2, -hw2), (bf2, -hw2), (bf2, -hw2 - TF), (-bf2, -hw2 - TF),
           (-bf2, -hw2), (-tw2, -hw2), (-tw2, hw2), (-bf2, hw2)]
    return [(x + dx, y + dy) for x, y in pts]


def weld_fillets(cv, dx=0.0, dy=0.0, leg=1.35, color="#3F4A5A"):
    """四個翼板/腹板交角的填角銲三角形"""
    tw2 = TW / 2
    corners = [(tw2, HW / 2, +1, -1), (-tw2, HW / 2, -1, -1),
               (tw2, -HW / 2, +1, +1), (-tw2, -HW / 2, -1, +1)]
    for cx, cy, sx_, sy_ in corners:
        p0 = (cx + dx, cy + dy)
        p1 = (cx + sx_ * leg + dx, cy + dy)
        p2 = (cx + dx, cy + sy_ * leg + dy)
        cv.polygon([p0, p1, p2], color, "none")


# ══════════════════════════════════════════════════════════
def fig1_section_compact():
    """題目重繪＋寬厚比判定：取代截圖，並把 λ 計算過程畫成看得見的懸臂長"""
    W, H = 930, 680
    L, R, T, B = 160, 380, 112, 96
    x_min, x_max = -20, 26
    y_min, y_max = -30, 42
    sx = min((W - L - R) / (x_max - x_min), (H - T - B) / (y_max - y_min))
    cv = Canvas(W, H, sx=sx, ox=L - x_min * sx, oy=B - y_min * sx, bg="#FFFFFF")

    cv.text_px(W / 2, 34, "銲接 H 型鋼斷面重繪與寬厚比判定", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "λ = b/(2t)，分母是 2t_f，因翼板從腹板兩側懸出，懸臂長 = b_f/2", 12.5, C["muted"])

    # 斷面
    outline = section_outline()
    cv.polygon(outline, "#EEF1F5", C["member"], 2.6)
    weld_fillets(cv)

    # 中性軸：只畫在斷面寬度內＋右側延伸到標籤，避開左側 h_w 標註區（在斷面外側更左邊）
    cv.line((-BF / 2, 0), (19, 0), C["dim"], 1.2, dash="5 4")
    cv.text_px(cv.X(19) + 6, cv.Y(0), "N.A.（中性軸）", 12, C["muted"], "start")

    # 尺寸線：b_f（上方，緊貼翼板頂）
    cv.dim((-BF / 2, HW / 2 + TF), (BF / 2, HW / 2 + TF), f"b_f = {BF:g}", off=-30, label_off=-15)
    # 尺寸線：h_w（左側，量測翼板內緣間距）。垂直尺寸線的 label_off 與 off 同方向，
    # 若差距太小，較寬的文字會整個蓋在尺寸線上；這裡刻意拉大差距，並加大 L 邊界留白配合
    cv.dim((-BF / 2, -HW / 2), (-BF / 2, HW / 2), f"h_w = {HW:g}", off=-50, label_off=-85)
    # t_f、t_w 皆遠小於整體尺度，正規雙箭頭 dim() 會擠成一團，改用簡單引線＋文字
    cv.line((BF / 2, HW / 2 + TF / 2), (BF / 2 + 9, HW / 2 + TF / 2), C["dim"], 1.1, dash="3 3")
    cv.text_px(cv.X(BF / 2 + 9) + 6, cv.Y(HW / 2 + TF / 2), f"t_f = {TF:g}", 13, C["dim"], "start")
    cv.line((TW / 2, 14), (8.5, 14), C["dim"], 1.1, dash="3 3")
    cv.text_px(cv.X(8.5) + 6, cv.Y(14), f"t_w = {TW:g}", 13, C["dim"], "start")

    # 翼板懸臂長 b_f/2（λ_f 分母的由來）：改用色塊標示右半翼板＋單一引線，
    # 不用縱向輔助線貫穿整個標註帶（之前的畫法會與 b_f 尺寸標籤在垂直方向打架）
    cant_x0, cant_x1 = TW / 2, BF / 2
    cant_y0, cant_y1 = HW / 2, HW / 2 + TF
    cv.polygon([(cant_x0, cant_y0), (cant_x1, cant_y0), (cant_x1, cant_y1), (cant_x0, cant_y1)],
               "rgba(180,83,9,0.22)")
    lx, ly = (cant_x0 + cant_x1) / 2, cant_y1
    cv.line((lx, ly), (lx + 4, 33), C["accent"], 1.1, dash="3 3")
    cv.text_px(cv.X(lx + 4) + 5, cv.Y(33), f"懸臂長 b_f/2 = {BF/2:g}（λ_f 分母）", 12, C["accent"], "start", weight="700")

    cv.text_px(cv.X(0), cv.Y(-HW / 2 - TF) + 26, f"全深 d = h_w + 2t_f = {D:g} cm", 13, C["muted"])

    # 判定面板
    px, py, pw = W - R + 20, T - 16, R - 46
    cv.rect_px(px, py, pw, 232, "#EEF4FF", 12, "#C7D9F5", 1.3)
    cv.text_px(px + pw / 2, py + 28, "翼板（懸臂板）寬厚比", 14.5, "#1D4ED8", weight="700")
    cv.math_px(px + 18, py + 58, f"λ_f = b_f/(2t_f) = {BF:g}/{2*TF:g} = {LAM_F:.2f}", 13.5, C["text"], "start")
    cv.math_px(px + 18, py + 82, f"λ_{{pf}} = 17/F_y^{{1/2}} = 17/{FY:g}^{{1/2}} = {LAM_PF:.2f}", 13.5, C["text"], "start")
    ok1 = "✓ 結實（compact）" if FLANGE_COMPACT else "× 非結實"
    rel1 = "＜" if FLANGE_COMPACT else "≥"
    cv.text_px(px + 18, py + 110, f"λ_f {rel1} λ_pf → {ok1}", 14,
               "#15803D" if FLANGE_COMPACT else C["load"], "start", weight="700")

    cv.text_px(px + pw / 2, py + 148, "腹板（加勁元素）寬厚比", 14.5, "#1D4ED8", weight="700")
    cv.math_px(px + 18, py + 178, f"λ_w = h_w/t_w = {HW:g}/{TW:g} = {LAM_W:.2f}", 13.5, C["text"], "start")
    cv.math_px(px + 18, py + 202, f"λ_{{pw}} = 170/F_y^{{1/2}} = 170/{FY:g}^{{1/2}} = {LAM_PW:.2f}", 13.5, C["text"], "start")
    ok2 = "✓ 結實（compact）" if WEB_COMPACT else "× 非結實"
    rel2 = "＜" if WEB_COMPACT else "≥"
    cv.text_px(px + 18, py + 230, f"λ_w {rel2} λ_pw → {ok2}", 14,
               "#15803D" if WEB_COMPACT else C["load"], "start", weight="700")

    cv.rect_px(px, py + 250, pw, 92, "#FFF6F1", 12, "#F0C9B8", 1.3)
    cv.text_px(px + 18, py + 274, "翼板、腹板皆結實 → 全斷面結實", 13, "#9A3412", "start", weight="700")
    cv.text_px(px + 18, py + 296, "＋完全側向支撐（L_b = 0 ＜ L_p）", 13, "#9A3412", "start", weight="700")
    cv.text_px(px + 18, py + 318, "→ M_n = M_p（見圖 2）", 13, "#9A3412", "start", weight="700")

    return cv.save(f"{OUT}/{TAG}-fig-1-section-compact.svg")


# ══════════════════════════════════════════════════════════
def _stress_panel(mode, title, tag_text, tag_color):
    """mode: 'elastic' 或 'plastic'。回傳一格 Canvas。
    版面：左側斷面 + 中間應力分布，右側固定像素寬的文字溝（GUTTER）放標註，
    溝寬用像素而非模型座標決定，避免長中文標籤把畫布撐爆。
    壓／拉應力用頂端圖例標示（固定位置），避免與 z_f／z_w 引線標籤在同一高度打架。"""
    PW, PH = 560, 580
    GUTTER = 210             # 右側文字溝寬度（像素）
    SEC_DX = -18.0           # 斷面整體左移，中間留給應力分布
    x_min, x_max = -40, 16
    y_min, y_max = -30, 30
    L, T, B = 10, 118, 74
    R_model = PW - GUTTER    # 應力/斷面繪圖區右邊界（像素）
    sx = min((R_model - L) / (x_max - x_min), (PH - T - B) / (y_max - y_min))
    ox = L - x_min * sx
    cv = Canvas(PW, PH, sx=sx, ox=ox, oy=B - y_min * sx, bg="#FFFFFF")
    cv.panel(title, None, pad=6, radius=14)
    cv.text_px(PW / 2, 58, tag_text, 12.5, tag_color, weight="700")
    peak_lab = "邊緣峰值 = F_y（中性軸為 0）" if mode == "elastic" else "全斷面 = F_y（均勻）"
    cv.legend(PW / 2 - 108, 82, [(C["compr"], f"壓應力，{peak_lab}"), (C["tension"], "拉應力，同上")],
              size=11.5, gap=17, swatch=18)

    outline = section_outline(dx=SEC_DX)
    fill = "#EEF1F5" if mode == "elastic" else "none"
    cv.polygon(outline, fill, C["member"], 2.4)
    weld_fillets(cv, dx=SEC_DX, leg=1.1)

    STRESS_W = 13.0          # 應力軸比例尺（模型單位＝Fy 之全幅）；兩張圖共用同一比例尺
    x0 = 3.0                 # 應力零線位置
    GX = R_model + 16        # 文字溝左緣（像素，固定不隨模型座標變動）

    # 零應力線與中性軸
    cv.line((SEC_DX - BF / 2 - 2, 0), (x0 + STRESS_W, 0), C["dim"], 1.1, dash="5 4")
    cv.text_px(cv.X(SEC_DX - BF / 2 - 2) - 6, cv.Y(0), "N.A.", 11.5, C["muted"], "end")
    cv.line((x0, -26), (x0, 26), C["dim"], 1.2)

    y_top, y_bot = HW / 2 + TF, -(HW / 2 + TF)

    if mode == "elastic":
        # 三角形分布：頂端 +Fy（壓）、底端 -Fy（拉），中性軸為 0
        cv.polygon([(x0, 0), (x0 + STRESS_W, y_top), (x0, y_top)], C["fill_c"], C["compr"], 1.8)
        cv.polygon([(x0, 0), (x0 + STRESS_W, y_bot), (x0, y_bot)], C["fill_t"], C["tension"], 1.8)
        cv.line((x0, 0), (x0 + STRESS_W, y_top), C["compr"], 2.2)
        cv.line((x0, 0), (x0 + STRESS_W, y_bot), C["tension"], 2.2)
        cv.math_px(PW / 2, PH - 46, "M_y = F_y · S_x", 15.5, C["text"], weight="700")
        cv.text_px(PW / 2, PH - 22, "腹板大部分仍在彈性範圍，未充分利用強度", 11.5, C["muted"])
    else:
        # 矩形分布：全斷面達 Fy（壓／拉），並標出翼板與半腹板兩個分區的形心臂距
        cv.polygon([(x0, 0), (x0 + STRESS_W, 0), (x0 + STRESS_W, y_top), (x0, y_top)], C["fill_c"], C["compr"], 1.8)
        cv.polygon([(x0, 0), (x0 + STRESS_W, 0), (x0 + STRESS_W, y_bot), (x0, y_bot)], C["fill_t"], C["tension"], 1.8)

        # 形心臂距標註：從應力塊高度水平引線指到文字溝，文字用固定像素 GX 起排版
        for arm, lab in ((ARM_FLANGE, f"z_f = h_w/2+t_f/2 = {ARM_FLANGE:g}"),
                          (ARM_WEB, f"z_w = h_w/4 = {ARM_WEB:g}")):
            cv.line((x0, arm), (x0 + STRESS_W + 5, arm), C["accent"], 1.1, dash="3 3")
            cv.dot((x0, arm), 3.6, fill=C["accent"])
            cv.text_px(GX, cv.Y(arm), lab, 11, C["accent"], "start", weight="700")

        cv.math_px(PW / 2, PH - 68, "M_p = F_y · Z_x", 15.5, C["text"], weight="700")
        cv.text_px(PW / 2, PH - 46,
                   f"Z_x = 2b_ft_f·z_f + 2(h_w/2)t_w·z_w", 11, C["muted"])
        cv.text_px(PW / 2, PH - 26,
                   f"= {Z_FLANGE:g} + {Z_WEB:g} = {ZX:g} cm³", 11.5, C["muted"], weight="700")
        cv.text_px(PW / 2, PH - 6, "翼板貢獻與腹板貢獻分開計算，兩者都要算", 11.5, C["accent"], weight="700")
    return cv


def fig2_elastic_vs_plastic():
    """彈性 Sx vs 塑性 Zx 應力分布對照：本題結實斷面＋完全支撐，正確作法用右圖"""
    a = _stress_panel("elastic", "彈性分布（首達降伏）", "× 本題不適用（結實斷面＋完全支撐已達全塑性）", C["load"])
    b = _stress_panel("plastic", "塑性分布（全斷面降伏）", "✓ 本題適用：M_n = M_p", "#15803D")
    compose([a, b],
            title="陷阱1：結實斷面＋完全側向支撐時，設計強度用 Z_x（塑性）而非 S_x（彈性）",
            sub=f"F_y = {FY:g} tf/cm² 兩圖同一應力比例尺；矩形分布的寬度差異＝翼板／腹板貢獻各自獨立計算",
            note=f"φ_bM_n = 0.9 × F_y × Z_x = 0.9 × {FY:g} × {ZX:g} = {PHI_MN:,.2f} tf·cm ≈ {PHI_MN/100:.1f} tf·m",
            path=f"{OUT}/{TAG}-fig-2-elastic-vs-plastic.svg")
    return f"{OUT}/{TAG}-fig-2-elastic-vs-plastic.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig1_section_compact,      "§4 Step2", "翼板寬厚比分母誤用 t_f 而非 2t_f → 結實斷面誤判"),
    (fig2_elastic_vs_plastic,   "§4 Step4-5", "結實斷面＋完全支撐仍誤用 S_x；Z_x 漏算腹板貢獻"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<46} {section:<10} 攔：{catches}")
    print(f"\n完成。接著執行： python3 <skill>/scripts/render.py {OUT}")
