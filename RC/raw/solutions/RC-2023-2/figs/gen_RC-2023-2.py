#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2023-2 T 形雙筋梁・壓力鋼筋未降伏 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2023-2.md §1 給定的原始資料；y1、y2、d、c、a、f'_s、Mn
     一律由下方函式現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字（b_w、b_e、h_f、根數、f'_c）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-section       斷面配筋與淨間距檢核  攔：算完 d 沒回頭驗每排放不放得下
  fig-2-strain-stress 應變／應力三聯        攔：拿 c（而非 a）去和 h_f 比、壓筋逕自假設降伏
  fig-3-layout        4+4 vs 3+3+2 對照     攔：以為換排列會改中性軸
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2023-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定（RC-2023-2.md §1 表格與「幾何假設」方塊）
# ══════════════════════════════════════════════════════════
BW      = 30.0     # 梁腹寬 (cm)
BE      = 90.0     # 有效翼緣寬 (cm)
HF      = 15.0     # 翼緣厚 (cm)
H       = 70.0     # 梁深 (cm)
N_BAR   = 8        # D32 根數
AB      = 8.14     # D32 單根面積 (cm^2)
DB      = 3.22     # D32 標稱直徑 (cm)
ASP     = 18.0     # 壓力鋼筋量 (cm^2)
DP      = 6.0      # 壓力鋼筋深度（依最小覆蓋估算）
COVER   = 4.0      # 最小淨保護層（至箍筋外面）
D_STIR  = 1.0      # D10 箍筋直徑（取 1.0 簡化）
S_LAYER = 2.5      # 雙排層間淨距（規範下限）
FC      = 280.0
FY      = 4200.0
ES      = 2.04e6
EPS_CU  = 0.003

# ── 由上列推得（不得手打） ────────────────────────────────
B1   = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
EPSY = FY / ES
AS   = N_BAR * AB
T    = AS * FY
INNER = BW - 2 * COVER - 2 * D_STIR          # 箍筋內淨寬 = 20 cm


def row_y(k):
    """第 k 排（k=0 為底排）鋼筋形心距梁底 (cm)。"""
    return COVER + D_STIR + DB / 2 + k * (DB + S_LAYER)


def s_clear(n):
    """每排 n 根 D32 的淨間距 (cm)。"""
    return (INNER - n * DB) / (n - 1)


def d_of(counts):
    """給定各排根數（由底排起算），回傳有效深度 d。"""
    tot = sum(counts)
    ybar = sum(c * row_y(k) for k, c in enumerate(counts)) / tot
    return H - ybar, ybar


D_44,    YB_44    = d_of([4, 4])
D_332,   YB_332   = d_of([3, 3, 2])
S_MIN_REQ = max(DB, 2.5)                     # 規範最小淨間距

# ── 中性軸：由力平衡解出（與 d 無關，這正是圖 3 要說的事） ──
QA = 0.85 * FC * BE * B1
QB = ASP * (ES * EPS_CU - 0.85 * FC) - T
QC = -ASP * ES * EPS_CU * DP
CU = (-QB + math.sqrt(QB * QB - 4 * QA * QC)) / (2 * QA)
A_BLK = B1 * CU
FSP   = ES * EPS_CU * (CU - DP) / CU
CC    = 0.85 * FC * BE * A_BLK
CSN   = ASP * (FSP - 0.85 * FC)

# 試算階段（先假設壓筋降伏）
A_TRIAL = (T - ASP * (FY - 0.85 * FC)) / (0.85 * FC * BE)
C_TRIAL = A_TRIAL / B1
EPS_SP_TRIAL = EPS_CU * (C_TRIAL - DP) / C_TRIAL


def Mn_of(d):
    return CC * (d - A_BLK / 2) + CSN * (d - DP)


def phi_of(et):
    if et >= 0.005: return 0.90
    if et <= EPSY:  return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


ET_44  = EPS_CU * (D_44 - CU) / CU
PHI    = phi_of(ET_44)
MN_44  = Mn_of(D_44)
MN_332 = Mn_of(D_332)

# ══════════════════════════════════════════════════════════
# 共用：T 形斷面繪製
# ══════════════════════════════════════════════════════════
OUTLINE = [((BE - BW) / 2, 0), ((BE + BW) / 2, 0), ((BE + BW) / 2, H - HF),
           (BE, H - HF), (BE, H), (0, H), (0, H - HF), ((BE - BW) / 2, H - HF)]


def bar_xs(n):
    """一排 n 根 D32 的中心 x 座標（沿腹板內淨寬均分）。"""
    x_lo = (BE - BW) / 2 + COVER + D_STIR + DB / 2
    if n == 1: return [BE / 2]
    step = (INNER - DB) / (n - 1)
    return [x_lo + i * step for i in range(n)]


def draw_section(cv, counts, show_comp=True, bar_r=6.2):
    cv.polygon(OUTLINE + [OUTLINE[0]], "#EDF1F6", C["member"], 2.6)
    # 箍筋（腹板內框）
    cv.poly([((BE - BW) / 2 + COVER, COVER), ((BE + BW) / 2 - COVER, COVER),
             ((BE + BW) / 2 - COVER, H - COVER), ((BE - BW) / 2 + COVER, H - COVER),
             ((BE - BW) / 2 + COVER, COVER)], C["member2"], 1.6, dash="5 4")
    for k, n in enumerate(counts):
        for x in bar_xs(n):
            cv.dot((x, row_y(k)), bar_r, fill=C["tension"], stroke="#FFFFFF", w=1.5)
    if show_comp:
        for x in bar_xs(3):
            cv.dot((x, H - DP), bar_r * 0.85, fill=C["compr"], stroke="#FFFFFF", w=1.5)


# ══════════════════════════════════════════════════════════
# 圖 1　斷面配筋與淨間距檢核
# ══════════════════════════════════════════════════════════
PW, PH = 460, 560
sc = min((PW - 175) / BE, (PH - 235) / H)
p1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - BE * sc / 2, oy=136)
p1.panel("斷面與配筋（依原卷文字 4+4）", f"b_e×h_f = {BE:.0f}×{HF:.0f}，b_w = {BW:.0f}")
draw_section(p1, [4, 4])
p1.line((0, H - HF), (BE, H - HF), C["member2"], 1.4, dash="4 4")
p1.dim((0, H), (BE, H), f"b_{{e}}={BE:.0f}", off=-46, label_off=-14)
p1.dim(((BE - BW) / 2, 0), ((BE + BW) / 2, 0), f"b_{{w}}={BW:.0f}", off=32, label_off=14)
p1.dim((BE, H), (BE, H - HF), f"h_{{f}}={HF:.0f}", off=-38, label_off=-13)
p1.dim(((BE + BW) / 2, H), ((BE + BW) / 2, 0), f"h={H:.0f}", off=-84, label_off=-13)
p1.dim((0, H), (0, H - D_44), f"d={D_44:.2f}", off=42, label_off=13)
p1.line((0, H - D_44), (BE, H - D_44), C["tension"], 1.4, dash="6 4")
p1.math_px(p1.X(0) + 8, p1.Y(H - DP) - 2, f"A'_{{s}}={ASP:.0f} cm^{{2}}", 12.5,
           C["compr"], "start", weight="700")
p1.text_px(PW / 2, PH - 48, f"A_{{s}} = {N_BAR}-D32 = {AS:.2f} cm^{{2}}（4+4 雙排）",
           13.5, C["tension"], weight="700")
p1.text_px(PW / 2, PH - 26, f"y_{{1}}={row_y(0):.2f}　y_{{2}}={row_y(1):.2f}　"
                            f"鋼筋形心 {YB_44:.2f} cm（距梁底）", 12, C["muted"])

# --- 放大：底排淨間距 ---
p2 = Canvas(PW, PH, sx=sc, ox=PW / 2 - BE * sc / 2, oy=136)
p2.panel("底排淨間距檢核（放大）", "每排 4 根 D32 排得下嗎？")
zx = 3.2                                         # 放大倍率
zsc = sc * zx
p2b = Canvas(PW, PH, sx=zsc, ox=PW / 2 - (BE / 2) * zsc, oy=PH * 0.50 - row_y(0) * zsc)
p2b.parts = p2.parts
for x, col, dsh in (((BE - BW) / 2, C["member"], None), ((BE + BW) / 2, C["member"], None),
                    ((BE - BW) / 2 + COVER, C["member2"], "5 4"),
                    ((BE + BW) / 2 - COVER, C["member2"], "5 4")):
    p2b.line((x, row_y(0) - 3.6), (x, row_y(0) + 3.6), col, 2.4, dash=dsh)
xs4 = bar_xs(4)
for x in xs4:
    p2b.circle((x, row_y(0)), DB / 2, fill="rgba(192,57,43,0.18)", stroke=C["tension"], w=2.2)
p2b.dim((xs4[0] + DB / 2, row_y(0)), (xs4[1] - DB / 2, row_y(0)),
        f"s={s_clear(4):.2f}", off=-52, label_off=-14, color=C["load"])
p2b.dim((xs4[2] - DB / 2, row_y(0)), (xs4[2] + DB / 2, row_y(0)),
        f"d_{{b}}={DB:.2f}", off=46, label_off=14)
p2b.dim(((BE - BW) / 2 + COVER, row_y(0)), ((BE + BW) / 2 - COVER, row_y(0)),
        f"箍筋內淨寬 {INNER:.0f} cm", off=92, label_off=17)
p2b.text_px(PW / 2, PH - 132,
            f"s = {s_clear(4):.2f} cm  小於  max(d_b, 2.5) = {S_MIN_REQ:.2f} cm", 14,
            C["load"], weight="700")
p2b.text_px(PW / 2, PH - 108, "× 不符規範", 13, C["load"], weight="700")
p2b.text_px(PW / 2, PH - 84, "原卷「雙排排列」與「間距依規範最小值」無法並存",
            12.5, C["load"])
p2b.text_px(PW / 2, PH - 50,
            f"改每排 3 根：s = {s_clear(3):.2f} cm  大於  {S_MIN_REQ:.2f} cm ✓", 12.5,
            C["bmd"], weight="700")

compose([p1, p2b],
        title=f"{TAG}　T 形雙筋梁斷面與鋼筋淨間距檢核",
        note=(f"算完 d 順手驗一次每排淨間距 —— 本題正是靠這一步才看得出原卷條件矛盾"),
        path=f"{OUT}/{TAG}-fig-1-section.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　應變／應力三聯（含翼板判斷）
# ══════════════════════════════════════════════════════════
PW, PH = 470, 580
sc = min((PH - 245) / H, (PW - 155) / BE)
M = 92 / sc                                      # 圖形最大水平半寬（模型單位）
EPS_SP = EPS_CU * (CU - DP) / CU                 # 最終狀態的壓力鋼筋應變

# (a) 斷面
q1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - BE * sc / 2, oy=140)
q1.panel("斷面", f"d = {D_44:.2f} cm，d' = {DP:.0f} cm")
draw_section(q1, [4, 4], bar_r=5.0)
q1.line((0, H - HF), (BE, H - HF), C["accent"], 1.8, dash="6 4")
q1.math_px(q1.X(0) - 8, q1.Y(H - HF), f"h_{{f}}={HF:.0f}", 12.5, C["accent"], "end", weight="700")
q1.text_px(PW / 2, PH - 46, "紅＝拉力鋼筋 8-D32　藍＝壓力鋼筋 A's", 12, C["muted"])

# (b) 應變
q2 = Canvas(PW, PH, sx=sc, ox=PW * 0.46, oy=140)
q2.panel("應變分佈", "平面保持平面")
wt = M
wc = M * CU / (D_44 - CU)
wsp = wc * (CU - DP) / CU
q2.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
q2.polygon([(0, H), (wc, H), (0, H - CU)], C["fill_c"], C["compr"], 2.4)
q2.polygon([(0, H - CU), (-wt, H - D_44), (0, H - D_44)], C["fill_t"], C["tension"], 2.4)
q2.line((-M * 1.15, H - CU), (M * 1.15, H - CU), C["accent"], 1.8, dash="6 4")
q2.text_px(q2.X(M * 1.15) + 4, q2.Y(H - CU), "N.A.", 12, C["accent"], "start", weight="700")
q2.math_px(q2.X(wc) + 6, q2.Y(H) - 14, "ε_{cu}=0.003", 12.5, C["compr"], "start", weight="700")
q2.math_px(q2.X(-wt) - 6, q2.Y(H - D_44), f"ε_{{t}}={ET_44:.4f}", 12.5, C["tension"], "end",
           weight="700")
q2.line((0, H - DP), (wsp, H - DP), C["compr"], 2.0)
q2.dot((wsp, H - DP), 4.6, fill=C["compr"], stroke="#FFFFFF", w=1.4)
q2.line((wsp, H - DP), (M * 1.05, H - DP + 4.0), C["compr"], 1.2, dash="3 3")
q2.math_px(q2.X(M * 1.05) + 4, q2.Y(H - DP + 4.0), f"ε'_{{s}}={EPS_SP:.6f}", 12,
           C["compr"], "start", weight="700")
q2.dim((0, H), (0, H - CU), f"c={CU:.2f}", off=34, label_off=12)
q2.text_px(PW / 2, PH - 68, f"ε'_{{s}} = {EPS_SP:.6f}  小於  ε_{{y}} = {EPSY:.6f}",
           13, C["load"], weight="700")
q2.text_px(PW / 2, PH - 46, f"→ 壓力鋼筋未降伏，f'_{{s}} = {FSP:.0f} kgf/cm^{{2}}",
           12.5, C["load"])

# (c) 應力
q3 = Canvas(PW, PH, sx=sc, ox=PW * 0.42, oy=140)
q3.panel("等值應力塊", f"a = β1 × c = {A_BLK:.2f} cm")
q3.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
q3.polygon([(0, H), (M, H), (M, H - A_BLK), (0, H - A_BLK)], C["fill_c"], C["compr"], 2.4)
q3.line((-M * 1.15, H - HF), (M * 1.45, H - HF), C["accent"], 2.0, dash="6 4")
q3.math_px(q3.X(M * 1.45) + 5, q3.Y(H - HF), f"h_{{f}}={HF:.0f}", 12.5, C["accent"], "start",
           weight="700")
q3.math_px(q3.X(0) - 8, q3.Y(H) - 13, f"0.85f'_{{c}}={0.85*FC:.0f}", 12.5, C["compr"], "end",
           weight="700")
q3.arrow((M * 0.45, H - A_BLK / 2), (M * 1.40, H - A_BLK / 2), C["compr"], 3.2, 10)
q3.arrow((0.0, H - D_44), (-M * 0.95, H - D_44), C["tension"], 3.2, 10)
q3.dim((0, H), (0, H - A_BLK), f"a={A_BLK:.2f}", off=30, label_off=11)
q3.text_px(PW / 2, PH - 128, f"a = {A_BLK:.2f} cm  小於  h_{{f}} = {HF:.0f} cm ✓",
           13.5, C["bmd"], weight="700")
q3.text_px(PW / 2, PH - 106, f"壓縮區全在翼板內，可用 b_{{e}} = {BE:.0f} cm", 12, C["muted"])
q3.text_px(PW / 2, PH - 74, f"C_{{c}} = {CC/1000:.1f}k　作用於 a/2 = {A_BLK/2:.2f} cm 處",
           12.5, C["compr"], weight="700")
q3.text_px(PW / 2, PH - 54, f"C_{{s,net}} = {CSN/1000:.1f}k　作用於 d' = {DP:.0f} cm 處",
           12.5, C["compr"], weight="700")
q3.text_px(PW / 2, PH - 34, f"T = {T/1000:.1f}k　作用於 d = {D_44:.2f} cm 處",
           12.5, C["tension"], weight="700")

compose([q1, q2, q3],
        title=f"{TAG}　中性軸與應力塊：翼板夠不夠是拿 a 去比，不是 c",
        sub=(f"試算階段先假設壓筋降伏得 c = {C_TRIAL:.2f} cm，"
             f"該處 εs' = {EPS_SP_TRIAL:.6f} 已低於 εy → 必須改走應變相容"),
        note=(f"單位 k = 1000 kgf；Cc + Cs,net = {(CC+CSN)/1000:.1f}k = T ✓　"
              f"力平衡定出 c，與 d 無關"),
        path=f"{OUT}/{TAG}-fig-2-strain-stress.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　4+4 vs 3+3+2：中性軸不變，只有力臂變
# ══════════════════════════════════════════════════════════
PW, PH = 430, 500
sc = min((PW - 190) / BE, (PH - 200) / H)


def layout_panel(counts, tag, d, mn):
    cv = Canvas(PW, PH, sx=sc, ox=PW / 2 - BE * sc / 2, oy=122)
    cv.panel(tag, f"每排淨間距 s = {s_clear(counts[0]):.2f} cm")
    draw_section(cv, counts, bar_r=5.4)
    cv.line((0, H - CU), (BE, H - CU), C["accent"], 2.2, dash="7 4")
    cv.math_px(cv.X(BE) + 6, cv.Y(H - CU), f"c={CU:.2f}", 12.5, C["accent"], "start", weight="700")
    cv.line((0, H - d), (BE, H - d), C["tension"], 1.6, dash="5 4")
    cv.dim((0, H), (0, H - d), f"d={d:.2f}", off=40, label_off=13)
    ok = s_clear(counts[0]) >= S_MIN_REQ
    cv.text_px(PW / 2, PH - 88,
               ("每排間距 " + ("✓ 合規" if ok else "× 不合規")), 13,
               C["bmd"] if ok else C["load"], weight="700")
    cv.text_px(PW / 2, PH - 62, f"M_{{n}} = {mn/1e5:.1f} tf·m", 14, C["text"], weight="700")
    cv.text_px(PW / 2, PH - 36, f"φM_{{n}} = {PHI*mn/1e5:.1f} tf·m", 15, C["bmd"], weight="700")
    return cv


compose([layout_panel([4, 4], "4+4（本解，依原卷文字）", D_44, MN_44),
         layout_panel([3, 3, 2], "3+3+2（嚴守間距）", D_332, MN_332)],
        title=f"{TAG}　換排列只改力臂，不改中性軸",
        sub=(f"兩圖的 c、a、fs' 完全相同：c = {CU:.2f} cm、a = {A_BLK:.2f} cm、"
             f"fs' = {FSP:.0f} kgf/cm²"),
        note=(f"c 由力平衡 Cc + Cs,net = As·fy 決定，與 d 無關；d 只進到力臂，"
              f"故 φMn 只差 {100*(MN_44-MN_332)/MN_44:.1f}%"),
        path=f"{OUT}/{TAG}-fig-3-layout.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4／§5 公佈值 assert
# ══════════════════════════════════════════════════════════
assert abs(row_y(0) - 6.61) < 0.005,        row_y(0)
assert abs(row_y(1) - 12.33) < 0.005,       row_y(1)
assert abs(D_44 - 60.53) < 0.005,           D_44
assert abs(D_332 - 58.38) < 0.01,           D_332
assert abs(s_clear(4) - 2.37) < 0.005,      s_clear(4)
assert abs(s_clear(3) - 5.17) < 0.005,      s_clear(3)
assert abs(C_TRIAL - 11.11) < 0.02,         C_TRIAL
assert abs(EPS_SP_TRIAL - 0.001380) < 5e-6, EPS_SP_TRIAL
assert abs(CU - 12.19) < 0.01,              CU
assert abs(A_BLK - 10.36) < 0.01,           A_BLK
assert abs(FSP - 3108) < 2,                 FSP
assert abs(CC - 221911) < 200,              CC
assert abs(CSN - 51660) < 200,              CSN
assert abs(ET_44 - 0.01189) < 5e-5,         ET_44
assert abs(PHI - 0.90) < 1e-9,              PHI
assert abs(MN_44 / 1e5 - 151.0) < 0.15,     MN_44 / 1e5
assert abs(MN_332 / 1e5 - 145.1) < 0.15,    MN_332 / 1e5
assert abs(PHI * MN_44 / 1e5 - 136) < 0.3,  PHI * MN_44 / 1e5
assert abs(PHI * MN_332 / 1e5 - 130.6) < 0.2, PHI * MN_332 / 1e5
print(f"{TAG}: 3 圖 OK　d(4+4)={D_44:.2f} d(3+3+2)={D_332:.2f} c={CU:.2f} a={A_BLK:.2f} "
      f"f's={FSP:.0f} s4={s_clear(4):.2f} s3={s_clear(3):.2f} "
      f"φMn={PHI*MN_44/1e5:.1f} / {PHI*MN_332/1e5:.1f} tf·m")
