#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2004-3 特殊抗彎構架柱・圍束箍筋間距 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2004-3.md §1 給定的原始資料（保護層為明示的假設）；
     h_c、A_ch、A_sh、s1、s2、h_x、s_x 全部現算，檔尾對 §4 公佈值 assert。
  2. 改斷面尺寸或保護層重跑，兩張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2004-3"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B      = 50.0     # 柱斷面邊長 (cm，方形)
FC     = 280.0    # f'c (kgf/cm^2)
FYH    = 2800.0   # 橫向鋼筋 fyh (kgf/cm^2)
AB_TIE = 1.29     # D13 單根面積 (cm^2)  ← 本卷「資料」欄給定值，非 CNS 1.267
DB_TIE = 1.27     # D13 標稱直徑 (cm)
DB_MAIN = 2.54    # D25 標稱直徑 (cm)
N_LEG  = 3        # 每方向有效腿數：外箍 2 腿 + 該方向繫筋 1 支
COVER  = 4.0      # ⚠ 保護層：題目未給，依規範假設淨保護層 4 cm（量至箍筋外緣）

# ── 由上列推得 ──────────────────────────────────────────
AG   = B * B
HC   = B - 2 * COVER              # 核心尺寸，量到箍筋外緣（現行規範的 b_c）
ACH  = HC * HC                    # 同一基準，故可直接平方
ASH  = N_LEG * AB_TIE
RATIO = AG / ACH - 1

S1 = ASH / (0.3 * HC * (FC / FYH) * RATIO)          # 公式一（含 Ag/Ach 項）
S2 = ASH / (0.09 * HC * (FC / FYH))                 # 公式二
# 主筋中心到中心（角筋）→ 每面 3 根，相鄰支承點水平間距
HX = (B - 2 * (COVER + DB_TIE + DB_MAIN / 2)) / 2
SX = min(15.0, max(10.0, 10 + (35 - HX) / 3))
S_CODE = min(B / 4, 6 * DB_MAIN, SX)
S_CTRL = min(S1, S2, S_CODE)
S_USE = math.floor(S_CTRL)                          # 無條件捨去


# ══════════════════════════════════════════════════════════
# 圖 1：斷面重繪（外箍 + 兩支繫筋，標 h_c / A_ch / h_x / 有效腿數）
# ══════════════════════════════════════════════════════════
def fig1_section():
    W, H = 780, 620
    L, Rm, T, Bm = 78, 250, 92, 112
    sx = min((W - L - Rm) / B, (H - T - Bm) / B)
    cv = Canvas(W, H, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")

    # 全斷面
    cv.polygon([(0, 0), (B, 0), (B, B), (0, B)], C["fill_m"], C["member"], 2.6)
    # 核心（箍筋外緣圍成）
    c0, c1 = COVER, B - COVER
    cv.polygon([(c0, c0), (c1, c0), (c1, c1), (c0, c1)],
               C["fill_c"], C["compr"], 2.8)

    # 主筋 8-D25：4 角 + 各面中點
    bar_lo = COVER + DB_TIE + DB_MAIN / 2
    bar_hi = B - bar_lo
    bar_mid = B / 2
    pos = [(bar_lo, bar_lo), (bar_mid, bar_lo), (bar_hi, bar_lo),
           (bar_lo, bar_mid),                    (bar_hi, bar_mid),
           (bar_lo, bar_hi), (bar_mid, bar_hi), (bar_hi, bar_hi)]
    for p in pos:
        cv.dot(p, 6.0, fill=C["member"], stroke="#FFFFFF", w=1.8)

    # 繫筋：水平 1 支（連左右面中點）、垂直 1 支（連上下面中點）
    cv.line((bar_lo, bar_mid), (bar_hi, bar_mid), C["load"], 3.0)
    cv.line((bar_mid, bar_lo), (bar_mid, bar_hi), C["accent"], 3.0)

    # 尺寸
    cv.dim((0, 0), (B, 0), f"b = {B:.0f} cm", off=82, color=C["dim"])
    cv.dim((c0, c1), (c1, c1), f"h_c = {HC:.0f} cm", off=-30, color=C["compr"])
    cv.dim((bar_lo, bar_lo), (bar_mid, bar_lo), f"h_x = {HX:.2f}", off=36,
           color=C["accent"])

    # 右側說明
    x = W - Rm + 10
    y = 118
    blocks = [
        (C["compr"], f"h_c = b − 2c = {HC:.0f} cm", "量到箍筋外緣"),
        (C["compr"], f"A_{{ch}} = h_c^{{2}} = {ACH:,.0f} cm^{{2}}", "同基準，才可直接平方"),
        (C["member"], f"A_g / A_{{ch}} = {AG/ACH:.3f}", f"> 1.3 → 公式一控制"),
        (C["load"], f"A_{{sh}} = {N_LEG}×{AB_TIE} = {ASH:.2f} cm^{{2}}", "每方向只算 3 腿"),
        (C["accent"], f"h_x = {HX:.2f} cm ≤ 35", "繫筋水平間距"),
    ]
    for col, expr, desc in blocks:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 13.5, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12, C["muted"], "start")
        y += 54

    y += 6
    cv.text_px(x, y, "有效腿數怎麼數", 13.5, C["text"], "start", weight="700")
    cv.text_px(x, y + 22, "檢核 X 向 → 只算 Y 向的腿：", 12.2, C["muted"], "start")
    cv.text_px(x, y + 42, "外箍 2 腿 ＋ Y 向繫筋 1 支 = 3", 12.2, C["muted"], "start")
    cv.text_px(x, y + 66, "斷面共 6 腿，但每方向只能", 12.2, C["load"], "start")
    cv.text_px(x, y + 86, "算 3 腿——全部加總是常見錯", 12.2, C["load"], "start")

    cv.legend(L, H - 46,
              [(C["load"], "X 向檢核用的繫筋"), (C["accent"], "Y 向檢核用的繫筋")],
              size=12.5)

    cv.text_px(W / 2, 34, "圖 1　柱斷面與圍束幾何（向量重繪）", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"保護層 {COVER:.0f} cm 為假設值（題目未給），但它直接決定 A_{{ch}} 與最終間距",
               12.8, C["load"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2：四個間距上限與最終控制值
# ══════════════════════════════════════════════════════════
def fig2_spacing():
    W, H = 900, 580
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    x0, bw = 300, 470
    peak = 16.0                    # 橫軸滿格 16 cm
    rows = [
        ("公式一（含 A_g/A_{ch}−1）", "0.3·s·h_c·(f'_c/f_{yh})(A_g/A_{ch}−1) ≤ A_{sh}",
         S1, C["load"], True),
        ("公式二（0.09 式）", "0.09·s·h_c·(f'_c/f_{yh}) ≤ A_{sh}", S2, C["compr"], False),
        ("規範　b / 4", f"{B:.0f} / 4", B / 4, C["member"], False),
        ("規範　6 d_b", f"6 × {DB_MAIN} (D25)", 6 * DB_MAIN, C["member"], False),
        ("規範　s_x", f"10 + (35 − {HX:.2f})/3 = {10+(35-HX)/3:.2f} → 取上限 15", SX,
         C["member"], False),
    ]
    y = 128
    for name, expr, val, col, ctrl in rows:
        cv.text_px(x0 - 16, y - 8, name, 14, C["text"], "end",
                   weight="700" if ctrl else "400")
        cv.text_px(x0 - 16, y + 13, expr, 11.5, C["muted"], "end")
        cv.rect_px(x0, y - 16, bw, 32, "#EDF1F6", 7)
        cv.rect_px(x0, y - 16, bw * val / peak, 32, col, 7)
        cv.text_px(x0 + bw * val / peak - 12, y, f"{val:.2f}", 13.5, "#FFFFFF",
                   "end", weight="700")
        if ctrl:
            cv.text_px(x0 + bw * val / peak + 14, y, "← 控制", 13.5, col,
                       "start", weight="700")
        y += 62

    # 控制線與越線示範
    xc = x0 + bw * S_CTRL / peak
    cv.parts.append(
        f'<line x1="{xc:.1f}" y1="102" x2="{xc:.1f}" y2="{y+96:.1f}" '
        f'stroke="{C["load"]}" stroke-width="2" stroke-dasharray="7 5"/>')
    cv.text_px(xc, 92, f"s ≤ {S_CTRL:.2f} cm", 14, C["load"], weight="700")

    yv = y + 16
    cv.rect_px(46, yv - 22, W - 92, 104, "#FFF6E8", 10, C["load"], 1.4)
    cv.text_px(W / 2, yv, "間距上限只能無條件捨去，不可四捨五入", 14.5,
               C["load"], weight="700")
    for i, (lab, val, ok) in enumerate([
            (f"寫 7.4 cm", 7.4, False),
            (f"取 7.5 cm", 7.5, False),
            (f"取 {S_USE:.0f} cm", float(S_USE), True)]):
        xx = W / 2 - 250 + i * 250
        col = C["bmd"] if ok else C["load"]
        cv.text_px(xx, yv + 30, lab, 13.5, col, weight="700")
        cv.text_px(xx, yv + 52,
                   "合格" if ok else f"超過 {S_CTRL:.2f}", 12.5, col)
        cv.text_px(xx, yv + 72,
                   "" if ok else "已經不滿足公式一", 11.8, C["muted"])

    cv.text_px(W / 2, 34, "圖 2　五個間距上限與最終控制值", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "五個條件全部要算，取最小；本題由公式一控制", 12.8, C["muted"])
    cv.text_px(W / 2, H - 18,
               f"加密區 s = {S_USE:.0f} cm；加密區外 s ≤ min(6d_b, 15) = "
               f"{min(6*DB_MAIN,15):.0f} cm", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section", fig1_section,
     "h_c 誤用箍筋中心距（與量到外緣的 A_ch 混用兩套基準）；把 6 腿全部算給同一方向"),
    ("2-spacing", fig2_spacing,
     "只算兩條 A_sh 公式而漏掉 s_x；把 7.36 進位成 7.4 或取 7.5（已違規）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("A_g",     AG,     2500.0, 0.1),
        ("h_c",     HC,     42.0,   0.01),
        ("A_ch",    ACH,    1764.0, 0.1),
        ("A_sh",    ASH,    3.87,   0.005),
        ("A_g/A_ch-1", RATIO, 0.417, 0.001),
        ("s1",      S1,     7.36,   0.01),
        ("s2",      S2,     10.24,  0.01),
        ("h_x",     HX,     18.46,  0.01),
        ("s_x",     SX,     15.0,   0.01),
        ("s_code",  S_CODE, 12.5,   0.01),
        ("s_ctrl",  S_CTRL, 7.36,   0.01),
        ("s_use",   S_USE,  7.0,    0.001),
    ]
    print("── 與 RC-2004-3.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<12} 算得 {got:>10.4f}   .md {want:>8}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
