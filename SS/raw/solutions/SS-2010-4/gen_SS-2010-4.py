#!/usr/bin/env python3
"""
SS-2010-4 樓版支撐鋼梁之斷面選擇與撓度檢核 — 解題圖解產生腳本

用法：
    python3 gen_SS-2010-4.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2010-4.md 哪一節
  2. 五組候選斷面的兩個使用率全部由載重與斷面性質現算（含自重迭代），
     改一個載重或跨距，五個點會一起移動
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2010-4"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2010-4.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 題目給定
L_M = 6.0                # m　跨距
S_M = 3.0                # m　梁間距＝集水寬
T_SLAB = 0.15            # m　RC 版厚
GAMMA_C = 2.4            # tf/m^3
Q_TILE = 0.030           # tf/m^2　大理石面磚
Q_LIVE = 0.400           # tf/m^2　活載重
FY, ES = 3.52, 2040.0    # tf/cm^2
PHI = 0.9
DEF_LIMIT = 360.0        # L/360
# §4 一 Step 1：線載重（集水寬 = 梁間距）
Q_RC = T_SLAB * GAMMA_C                      # 0.360 tf/m^2
WD0 = (Q_RC + Q_TILE) * S_M                  # 1.170 tf/m（不含自重）
WL = Q_LIVE * S_M                            # 1.200 tf/m
WU0 = 1.2 * WD0 + 1.6 * WL                   # 3.324 tf/m
MU0 = WU0 * L_M ** 2 / 8 * 100               # 1,495.8 tf·cm
Z_REQ = MU0 / (PHI * FY)                     # 472.2 cm^3
# §1 題目給定之五組候選（名稱, S_x, Z_x, I_x, r_y, 單位重 kg/m）
CANDS = [("RH175×175", 331.0, 370.0, 2900.0, 4.37, 40.4),
         ("RH298×149", 424.0, 475.0, 6320.0, 3.29, 32.0),
         ("RH200×200", 472.0, 525.0, 4720.0, 5.02, 49.9),
         ("RH244×175", 495.0, 550.0, 6040.0, 4.21, 43.6),
         ("RH200×204", 498.0, 565.0, 4980.0, 4.88, 56.2)]
PICK = "RH244×175"       # §4 一 Step 4 之主答
D_ALLOW = L_M * 100 / DEF_LIMIT              # 1.667 cm


def mu_with_self(w_kgm):
    """含自重之設計彎矩（tf·cm）"""
    wu = 1.2 * (WD0 + w_kgm / 1000.0) + 1.6 * WL
    return wu * L_M ** 2 / 8 * 100


def delta_live(ix):
    """服務（未因數化）活載重撓度（cm）——§4 二 Step 6"""
    return 5 * (WL / 100.0) * (L_M * 100) ** 4 / (384 * ES * ix)


ROWS = []
for nm, sx, zx, ix, ry, wt in CANDS:
    mu = mu_with_self(wt)
    phimp = PHI * FY * zx
    d = delta_live(ix)
    ROWS.append(dict(name=nm, Sx=sx, Zx=zx, Ix=ix, ry=ry, wt=wt, Mu=mu, phiMp=phimp,
                     um=mu / phimp, dl=d, ud=d / D_ALLOW))

# §5.5 RH298×149 的翼板局部挫屈（FLB）獨立佐證
BF_298, TF_298 = 14.9, 0.8            # cm（＝ H-298×149×5.5×8）
FR = 0.703                            # tf/cm^2（10 ksi）
LAM_F = BF_298 / (2 * TF_298)                       # 9.313
LAM_P = 17 / math.sqrt(FY)                          # 9.061
LAM_R = 37.39 / math.sqrt(FY - FR)                  # 22.28
MP_298 = FY * 475.0                                 # 1,672 tf·cm
MR_298 = (FY - FR) * 424.0                          # 1,194 tf·cm
MN_FLB = MP_298 - (MP_298 - MR_298) * (LAM_F - LAM_P) / (LAM_R - LAM_P)   # 1,663
PHI_MN_FLB = PHI * MN_FLB                           # 1,497 tf·cm


# ══════════════════════════════════════════════════════════
# 圖 2：集水寬與兩種載重（強度用因數化、撓度用服務載重）
# ══════════════════════════════════════════════════════════
def fig2_load_path():
    PW2, PH2 = 540, 470
    KY = 4.0                    # 縱向比例放大倍數（橫向 1:1）

    def _box(cv, x0, x1, y0, y1, fill, stroke="none", w=1.2):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w)

    # ── ① 橫斷面：集水寬 ──
    a = Canvas(PW2, PH2, sx=48.0, ox=270.0, oy=190.0)
    a.panel("① 橫斷面：集水寬 ＝ 梁間距", f"縱向比例放大 {KY:.0f} 倍（橫向 1:1）")
    ys, yt = 0.0, T_SLAB * KY
    _box(a, -4.6, 4.6, ys, yt, C["fill_m"], C["member"], 1.6)
    _box(a, -S_M / 2, S_M / 2, ys, yt, "rgba(180,83,9,0.18)")
    bf, tf_, tw = 0.175, 0.011 * KY, 0.0055 * 6      # 翼板寬 1:1；板厚放大以便辨識
    for bx in (-S_M, 0.0, S_M):
        top = yt - 0.05 * KY                          # 上翼版埋在版內
        bot = top - 0.244 * KY
        col = C["member"] if bx == 0 else C["member2"]
        _box(a, bx - bf / 2, bx + bf / 2, top - tf_, top, col)          # 上翼板
        _box(a, bx - tw / 2, bx + tw / 2, bot + tf_, top - tf_, col)    # 腹板
        _box(a, bx - bf / 2, bx + bf / 2, bot, bot + tf_, col)          # 下翼板
    a.udl((-S_M / 2, yt), (S_M / 2, yt), 0.26 * KY, n=9, color=C["load"], w=1.8)
    a.dim((-S_M / 2, yt + 0.30 * KY), (S_M / 2, yt + 0.30 * KY),
          f"集水寬 {S_M:.1f} m", off=-14, label_off=-12)
    a.dim((-S_M, -1.10), (0.0, -1.10), f"{S_M:.1f} m", off=18, label_off=12)
    a.dim((0.0, -1.10), (S_M, -1.10), f"{S_M:.1f} m", off=18, label_off=12)
    a.text_px(a.X(-4.6) + 6, a.Y(yt) - 12, f"RC 版 {T_SLAB*100:.0f} cm", 11.5,
              C["bmd"], "start")     # 放在版上方左端，避開最左側鋼梁
    a.text_px(a.X(0), a.Y(-0.82), "上翼版埋入版內 ⇒ 全側撐、無 LTB", 12, C["accent"],
              weight="700")
    a.text_px(PW2 / 2, PH2 - 84,
              f"RC {Q_RC:.3f} ＋ 面磚 {Q_TILE:.3f} ＝ {Q_RC+Q_TILE:.3f} tf/m²", 12, C["muted"])
    a.text_px(PW2 / 2, PH2 - 58,
              f"w_D = {Q_RC+Q_TILE:.3f} × {S_M:.1f} = {WD0:.3f} tf/m（不含自重）", 12.5,
              C["muted"], weight="700")
    a.text_px(PW2 / 2, PH2 - 30,
              f"w_L = {Q_LIVE:.3f} × {S_M:.1f} = {WL:.3f} tf/m", 12.5, C["tension"],
              weight="700")

    # ── ② 縱向：兩種載重各有各的用途 ──
    b = Canvas(PW2, PH2, sx=68.0, ox=100.0, oy=250.0)
    b.panel("② 縱向：強度與撓度用不同的載重", "同一根梁，兩套載重不可混用")
    pick = next(r for r in ROWS if r["name"] == PICK)
    wu = 1.2 * (WD0 + pick["wt"] / 1000) + 1.6 * WL
    b.line((0, 0), (L_M, 0), C["member"], 6.0, cap="butt")
    b.pin_support((0, 0), size=13)
    b.roller_support((L_M, 0), size=13)
    b.udl((0, 0), (L_M, 0), 0.60, n=13, color=C["load"], w=1.8)
    b.text_px(b.X(L_M / 2), b.Y(0.60) - 16,
              f"強度：w_u = 1.2(w_D + 自重) + 1.6w_L = {wu:.3f} tf/m", 12, C["load"],
              weight="700")
    b.dim((0, -0.42), (L_M, -0.42), f"L = {L_M:.1f} m", off=18, label_off=12)
    amp = 0.46
    b.line((0, -1.02), (L_M, -1.02), C["ghost"], 1.6, dash="5 4")
    b.poly([(L_M * i / 60, -1.02 - amp * math.sin(math.pi * i / 60))
            for i in range(61)], C["deform"], 3.6)
    b.text_px(b.X(L_M / 2), b.Y(-1.02 - amp) + 22,
              f"撓度：w_L = {WL:.3f} tf/m（服務載重，不乘 1.6）", 12.5, C["tension"],
              weight="700")
    b.text_px(PW2 / 2, PH2 - 84,
              f"M_u = w_u L²/8 = {pick['Mu']:,.0f} tf·cm", 12.5, C["load"], weight="700")
    b.text_px(PW2 / 2, PH2 - 58,
              f"δ_L = 5w_L L⁴/(384EI_x) = {pick['dl']:.3f} cm", 12.5, C["tension"],
              weight="700")
    b.text_px(PW2 / 2, PH2 - 30,
              f"δ 容許 = L/360 = {D_ALLOW:.3f} cm　⇒　通過（{100*pick['ud']:.1f}%）",
              12.5, C["muted"], weight="700")

    compose([a, b],
            title="集水寬就是梁間距，而強度與撓度用的是兩套不同的載重",
            sub="每根梁承擔左右各 1.5 m、合計 3.0 m 寬的樓版載重；"
                "撓度是使用性檢核，一律用未因數化的活載重",
            note="上翼版埋入混凝土 ⇒ 壓力翼版全程側撐、無側扭挫屈 ⇒ "
                 "標稱彎矩直接取塑性彎矩，不必計算彎矩修正係數與側撐長度界限",
            path=f"{OUT}/{TAG}-fig-2-load-path.svg")
    return f"{OUT}/{TAG}-fig-2-load-path.svg"


# ══════════════════════════════════════════════════════════
# 圖 3：五組候選的雙準則篩選
# ══════════════════════════════════════════════════════════
def fig3_screen():
    """五組候選的雙準則篩選：兩個使用率並排，100% 線一眼看穿"""
    W, HH = 980, 600
    X0, BW = 286.0, 560.0
    SCALE = 2.10                      # 長條滿格代表 210%
    ROW_H, BAR_H = 88, 22
    TOP = 116
    x100 = X0 + BW / SCALE            # 100% 的位置

    cv = Canvas(W, HH, sx=1.0, ox=0.0, oy=0.0, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "兩個準則要同時過——五組候選只有一組兩根長條都在 100% 線內",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "上排＝含自重之彎矩使用率 M_u／φ_b M_p　下排＝服務活載重之撓度使用率 δ_L／(L/360)",
               13, C["muted"])

    order = ["RH298×149", "RH175×175", "RH244×175", "RH200×200", "RH200×204"]
    rows = [next(r for r in ROWS if r["name"] == n) for n in order]

    for i, r in enumerate(rows):
        y = TOP + i * ROW_H
        ok = r["um"] <= 1.0 and r["ud"] <= 1.0
        if ok:
            cv.rect_px(14, y - 34, W - 28, ROW_H - 6, "rgba(46,125,111,0.10)", 10)
        cv.text_px(28, y - 20, r["name"], 14, C["text"] if ok else C["muted"], "start",
                   weight="700")
        cv.text_px(28, y + 3, f"{r['wt']:.1f} kg/m", 12, C["muted"], "start")
        cv.text_px(28, y + 24, f"Z_x = {r['Zx']:.0f}　I_x = {r['Ix']:,.0f}", 11.5,
                   C["muted"], "start")
        for j, (val, lab, col) in enumerate(
                ((r["um"], "彎矩", C["load"]), (r["ud"], "撓度", C["tension"]))):
            by = y - 26 + j * (BAR_H + 8)
            good = val <= 1.0
            cv.rect_px(X0, by, BW, BAR_H, "#EDF1F6", 5)
            cv.rect_px(X0, by, min(BW * val / SCALE, BW), BAR_H,
                       C["bmd"] if good else col, 5)
            cv.text_px(X0 - 10, by + BAR_H / 2, lab, 11.5, C["muted"], "end")
            lx = min(X0 + BW * val / SCALE, BW + X0) + 10
            if lx < x100 and lx + 56 > x100:        # 會被 100% 虛線劃過 → 推到線右側
                lx = x100 + 10
            cv.text_px(lx, by + BAR_H / 2, f"{100*val:.1f}%", 12.5,
                       C["bmd"] if good else col, "start", weight="700")

    # 100% 限值線貫穿五列
    y_top, y_bot = TOP - 30, TOP + 4 * ROW_H + 26
    cv.parts.append(f'<line x1="{x100:.2f}" y1="{y_top}" x2="{x100:.2f}" y2="{y_bot}" '
                    f'stroke="{C["load"]}" stroke-width="2.6" stroke-dasharray="6 4"/>')
    cv.text_px(x100, y_top - 10, "上限 100%", 13, C["load"], weight="700")

    pick = next(r for r in ROWS if r["name"] == PICK)
    cv.text_px(W / 2, HH - 42,
               f"最輕的 RH298×149（32.0 kg/m）撓度只用 94.2%，卻在彎矩超出 0.55%；"
               f"Z_x 更大的 200×200 與 200×204 則因梁深僅 20 cm、I_x 偏小而撓度不合格",
               13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               f"⇒ 選 {PICK}（{pick['wt']} kg/m）：彎矩 {100*pick['um']:.1f}%、"
               f"撓度 {100*pick['ud']:.1f}% —— 撓度才是真正的控制項", 12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-3-screen.svg")
    return f"{OUT}/{TAG}-fig-3-screen.svg"


# ══════════════════════════════════════════════════════════
# 圖 4：RH298×149 的 0.55%
# ══════════════════════════════════════════════════════════
def fig4_298_debate():
    W, HH = 900, 520
    cv = Canvas(W, HH, sx=1.0, ox=0.0, oy=0.0, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "被淘汰的 RH298×149：又輕又剛，但彎矩確定超出",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "0.55% 不是誤差——自重 32.0 kg/m 是斷面表給的確定值；"
               "而翼板非結實的 FLB 檢核又獨立確認了同一個結論", 13, C["muted"])

    items = [("需求　M_u（不含自重）", MU0, C["muted"], "初估用"),
             ("需求　M_u（含自重 32.0 kg/m）", ROWS[1]["Mu"], C["load"], "實際需求"),
             ("容量　φ_b M_p（誤設結實）", ROWS[1]["phiMp"], C["compr"], "差 0.55%"),
             ("容量　φ_b M_n（FLB 修正後）", PHI_MN_FLB, C["accent"], "差 1.1%")]
    # 四個值只差 1% 上下，自零起畫會完全看不出差距 → 橫軸自 1,450 起（截斷刻度，圖上明示）
    x0, bw = 320, 380
    BASE, TOPV = 1450.0, 1530.0

    def bar_len(v): return bw * (v - BASE) / (TOPV - BASE)

    for i, (nm, v, col, note) in enumerate(items):
        y = 118 + i * 68
        cv.text_px(28, y - 9, nm, 13, C["text"], "start", weight="700")
        cv.text_px(28, y + 13, note, 11.5, C["muted"], "start")
        cv.rect_px(x0, y - 16, bw, 32, "#EDF1F6", 6)
        cv.rect_px(x0, y - 16, bar_len(v), 32, col, 6)
        cv.math_px(x0 + bw + 14, y, f"{v:,.0f} tf·cm", 13, col, "start", weight="700")
    # 截斷刻度的刻度線與說明
    ytick = 118 + 3 * 68 + 30
    cv.parts.append(f'<line x1="{x0}" y1="{ytick}" x2="{x0 + bw}" y2="{ytick}" '
                    f'stroke="{C["muted"]}" stroke-width="1.4"/>')
    for tv in (1450, 1470, 1490, 1510, 1530):
        tx = x0 + bar_len(tv)
        cv.parts.append(f'<line x1="{tx:.1f}" y1="{ytick}" x2="{tx:.1f}" y2="{ytick + 6}" '
                        f'stroke="{C["muted"]}" stroke-width="1.4"/>')
        cv.math_px(tx, ytick + 20, f"{tv:,}", 11, C["muted"])
    cv.text_px(28, ytick + 14, "橫軸自 1,450 起（非自零）", 11.5, C["muted"], "start")

    cv.text_px(W / 2, HH - 92,
               f"翼板細長比 λ_f = {BF_298:.1f}/(2×{TF_298}) = {LAM_F:.3f} "
               f"大於 λ_p = 17/√F_y = {LAM_P:.3f} ⇒ 非結實，M_n 不得取 M_p",
               12.5, C["accent"], weight="700")
    cv.text_px(W / 2, HH - 68,
               f"FLB 內插：M_n = {MP_298:,.0f} − ({MP_298:,.0f} − {MR_298:,.0f}) × "
               f"({LAM_F:.3f} − {LAM_P:.3f})／({LAM_R:.2f} − {LAM_P:.3f}) = {MN_FLB:,.0f} tf·cm",
               12, C["muted"])
    cv.text_px(W / 2, HH - 40,
               f"φ_b M_n = {PHI_MN_FLB:,.0f} tf·cm，連不含自重的 {MU0:,.0f} 都只剩 "
               f"{100*(PHI_MN_FLB/MU0-1):.2f}% 餘裕", 13, C["accent"], weight="700")
    cv.text_px(W / 2, HH - 16,
               "從 φ_b M_n 借用額外餘裕，等於私自把 φ_b 由 0.9 調升為 0.905——無規範依據",
               12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-4-298-debate.svg")
    return f"{OUT}/{TAG}-fig-4-298-debate.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_load_path, "§4 一 Step 1·§4 二·§3 陷阱❶❸❹",
     "集水寬取錯，或撓度誤用因數化載重（1.6w_L）"),
    (fig3_screen, "§4 一 Step 4 附表",
     "只看強度（或只看重量）就選斷面，漏掉撓度這個真正的控制項"),
    (fig4_298_debate, "§4 一 Step 4·§5.5",
     "忘記自重迭代就放行最輕斷面；或忽略翼板結實性檢核"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"w_D0 = {WD0:.3f}　w_L = {WL:.3f} tf/m　M_u0 = {MU0:,.1f} tf·cm　"
          f"Z_req = {Z_REQ:.1f} cm³　δ 容許 = {D_ALLOW:.3f} cm")
    print(f"{'斷面':<12}{'kg/m':>7}{'M_u':>10}{'φbMp':>10}{'彎矩%':>9}{'δ_L':>8}{'撓度%':>9}")
    for r in ROWS:
        print(f"{r['name']:<12}{r['wt']:>7.1f}{r['Mu']:>10,.1f}{r['phiMp']:>10,.1f}"
              f"{100*r['um']:>9.2f}{r['dl']:>8.3f}{100*r['ud']:>9.1f}")
    print(f"\nFLB：λ_f = {LAM_F:.3f}　λ_p = {LAM_P:.3f}　λ_r = {LAM_R:.2f}　"
          f"M_n = {MN_FLB:,.0f}　φ_b M_n = {PHI_MN_FLB:,.0f} tf·cm（.md: 1,663／1,497）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<38} {section:<28} 攔：{catches}")
