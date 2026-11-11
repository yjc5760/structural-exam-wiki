# -*- coding: utf-8 -*-
"""SM-2015-3 圖解。數值全部由本檔依 SM-2015-3.md §3.5 的 L1 重算。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）──────────────────────────────────────────────
H, HS, HC = 8.0, 3.0, 5.0
GS, PHIS = 16.5, 32.0
GC, CU = 17.5, 30.0
BW, LW = 6.0, 15.0
KS = 1.0
# ── L2（§4）───────────────────────────────────────────────
GBAR = (GS*HS + GC*HC)/H                       # 17.125
GH   = GBAR*H                                  # 137.0
CUS  = 0.5*GS*HS*KS*math.tan(R(PHIS))          # 15.4655
CBAR = (CUS*HS + CU*HC)/H                      # 24.5496
NST  = GH/CBAR                                 # 5.5805
PA1  = GH - 4*CBAR                             # 38.802
PA2  = 0.3*GH                                  # 41.100
PA   = max(PA1, PA2)                           # 41.100
ZT   = 0.25*H                                  # 2.0
# 正確（軟弱至中度）包絡線
P_TRI  = 0.5*ZT*PA
P_RECT = PA*(H-ZT)
P_TOT  = P_TRI + P_RECT                        # 287.70
ZBAR   = (P_TRI*(2.0/3*ZT) + P_RECT*(ZT+(H-ZT)/2))/P_TOT   # 4.476
# 誤用（堅硬有裂縫黏土）包絡線
P_BAD  = 0.5*ZT*PA + PA*(0.5*H) + 0.5*ZT*PA    # 246.60
# 抗隆起
NC   = 5*(1+0.2*BW/LW)*(1+0.2*H/BW)            # 6.84
NCAP = 7.5*(1+0.2*BW/LW)
FS   = NC*CU/GH                                # 1.4978
# 對照
CBAR_DAS = (GS*KS*HS**2*math.tan(R(PHIS)) + (H-HS)*0.75*2*CU)/H
N_DAS    = GH/CBAR_DAS
PA_M04   = GH - 0.4*4*CBAR

PSC = 0.085                 # 1 kPa = 0.085 繪圖公尺
P = lambda q: q*PSC
Yz = lambda z: H - z


# ══════════════════════════════════════════════════════════
# fig-1　視土壓力包絡線：正確形狀 vs 誤用堅硬黏土形狀
# ══════════════════════════════════════════════════════════
def fig1():
    W1, H1 = 980, 700
    xmin, xmax, ymin, ymax = -1.9, 9.6, -1.5, 10.1
    L, Rm, T, Bm = 44, 44, 66, 128
    sx = min((W1-L-Rm)/(xmax-xmin), (H1-T-Bm)/(ymax-ymin))
    cv = Canvas(W1, H1, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="SM-2015-3 (一)　Peck 視土壓力包絡線：形狀由分類決定",
             sub="N = γ_{av}H/C_{av} = %.2f ＞ 4 ⇒ 軟弱至中度黏土 ⇒ 0.25H 之後維持 p_a 到坑底，不遞減" % NST)
    cv.line((0, Yz(H)), (0, Yz(0)), C["member"], 3.4)
    for z in range(0, 9, 2):
        cv.line((0, Yz(z)), (-0.16, Yz(z)), C["muted"], 1.3)
        cv.text_px(cv.X(-0.26), cv.Y(Yz(z)), "%d" % z, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-1.3), cv.Y(Yz(4)), "深度", 12.5, C["muted"])
    cv.text_px(cv.X(-1.3), cv.Y(Yz(4))+19, "z (m)", 12.5, C["muted"])
    cv.line((0, Yz(0)), (P(60), Yz(0)), C["muted"], 1.6)
    for q in (0, 20, 40, 60):
        cv.line((P(q), Yz(0)), (P(q), Yz(0)+0.16), C["muted"], 1.3)
        cv.text_px(cv.X(P(q)), cv.Y(Yz(0))-17, "%g" % q, 12, C["muted"])
    cv.text_px(cv.X(P(30)), cv.Y(Yz(0))-39, "視土壓力 (kN/m²)", 12.5, C["muted"], weight="700")
    # 土層分界
    cv.line((0, Yz(HS)), (P(58), Yz(HS)), C["accent"], 1.4, dash="6 4")
    cv.text_px(cv.X(P(58))+7, cv.Y(Yz(HS)), "砂／黏土交界 z = %g m" % HS, 11.5,
               C["accent"], anchor="start")
    # 正確包絡線（實心）
    cv.polygon([(0, Yz(0)), (P(PA), Yz(ZT)), (P(PA), Yz(H)), (0, Yz(H))],
               "rgba(220,38,38,0.22)", C["load"], 3.0)
    # 誤用形狀（虛線）
    cv.poly([(P(PA), Yz(0.75*H)), (0, Yz(H))], C["muted"], 2.4, dash="8 5")
    cv.dot((P(PA), Yz(0.75*H)), 4.4, fill=C["muted"])
    cv.line((P(PA*0.5), Yz(7.2)), (P(46), Yz(7.2)), C["muted"], 1.1, dash="3 3")
    cv.text_px(cv.X(P(47)), cv.Y(Yz(7.05)), "誤用堅硬有裂縫黏土的形狀", 12,
               C["muted"], anchor="start")
    cv.text_px(cv.X(P(47)), cv.Y(Yz(7.05))+18, "（0.75H 之後遞減回零）", 11.5,
               C["muted"], anchor="start")
    cv.dot((P(PA), Yz(ZT)), 5.2, fill=C["load"])
    cv.dot((P(PA), Yz(H)), 5.2, fill=C["load"])
    cv.text_px(cv.X(P(PA))+9, cv.Y(Yz(ZT)), "p_a = %.1f kN/m²" % PA, 12.5, C["load"],
               anchor="start", weight="700")
    cv.text_px(cv.X(P(PA))+9, cv.Y(Yz(ZT))+18, "z = 0.25H = %g m" % ZT, 11.5, C["muted"],
               anchor="start")
    cv.text_px(cv.X(P(PA))+9, cv.Y(Yz(H)), "坑底仍為 %.1f" % PA, 12.5, C["load"],
               anchor="start", weight="700")
    # 合力
    cv.arrow((P(58), Yz(ZBAR)), (P(PA)*0.55, Yz(ZBAR)), C["accent"], 4.0, 12)
    cv.line((0, Yz(ZBAR)), (P(58), Yz(ZBAR)), C["accent"], 1.2, dash="4 4")
    cv.text_px(cv.X(P(58))+8, cv.Y(Yz(ZBAR))-15, "P = %.2f kN/m" % P_TOT, 13.5,
               C["accent"], anchor="start", weight="700")
    cv.text_px(cv.X(P(58))+8, cv.Y(Yz(ZBAR))+7, "形心 z_c = %.3f m" % ZBAR, 12,
               C["muted"], anchor="start")
    rows = [("正確（軟弱至中度）", P_TOT, ZBAR, C["load"]),
            ("誤用（堅硬有裂縫）", P_BAD, 4.0, C["muted"])]
    x0, ytab = 62, H1-104
    cv.rect_px(x0-12, ytab-24, 620, 28, "#ECEFF1", 6)
    for j, hcell in enumerate(["包絡線形狀", "總側向推力 (kN/m)", "形心距地表 (m)", "差異"]):
        cv.text_px(x0 + (0, 250, 400, 530)[j], ytab-10, hcell, 12, C["text"],
                   anchor="start" if j == 0 else "end", weight="700")
    for i, (nm, pv, zv, col) in enumerate(rows):
        yy = ytab + 16 + i*24
        cv.text_px(x0, yy, nm, 12, col, anchor="start", weight="700")
        cv.text_px(x0+250, yy, "%.2f" % pv, 12, col, anchor="end")
        cv.text_px(x0+400, yy, "%.3f" % zv, 12, col, anchor="end")
        cv.text_px(x0+530, yy, "—" if i == 0 else "低估 %.1f%%" % (100*(P_TOT-P_BAD)/P_TOT),
                   12, col, anchor="end")
    cv.text_px(W1/2, H1-24, "誤用形狀會把最下一層支撐的荷重嚴重低估——那正是開挖工程最危險的一根",
               13, C["load"], weight="700")
    cv.save(os.path.join(OUT, "SM-2015-3-fig-1-apparent-pressure.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　等值參數的來源 ＋ 抗隆起（Bjerrum & Eide）
# ══════════════════════════════════════════════════════════
PW2, PH2 = 720, 660


def panel_profile():
    xmin, xmax, ymin, ymax = -2.6, 10.4, -4.6, 9.6
    L, Rm, T, Bm = 34, 34, 62, 96
    sx = min((PW2-L-Rm)/(xmax-xmin), (PH2-T-Bm)/(ymax-ymin))
    cv = Canvas(PW2, PH2, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="等值參數怎麼來的", sub="砂土的摩擦抗力先換算成等值凝聚力，再與黏土加權")
    cv.polygon([(0, Yz(HS)), (9.9, Yz(HS)), (9.9, Yz(0)), (0, Yz(0))], "rgba(180,83,9,0.16)")
    cv.polygon([(0, Yz(13.0)), (9.9, Yz(13.0)), (9.9, Yz(HS)), (0, Yz(HS))], "rgba(63,74,90,0.14)")
    cv.line((0, Yz(HS)), (9.9, Yz(HS)), C["muted"], 1.8)
    cv.line((0, Yz(H)), (9.9, Yz(H)), C["member"], 3.0)
    cv.line((0, Yz(0)), (0, Yz(13.0)), C["member"], 3.4)
    cv.text_px(cv.X(5.0), cv.Y(Yz(1.4)), "砂土　H_s = %g m、γ_s = %g、φ_s = %g°"
               % (HS, GS, PHIS), 12.5, C["accent"], weight="700")
    cv.text_px(cv.X(5.0), cv.Y(Yz(2.2)),
               "C_us = ½γ_s·H_s·K_s·tanφ_s = %.2f kN/m²" % CUS, 12, C["muted"])
    cv.text_px(cv.X(5.0), cv.Y(Yz(5.4)), "黏土　γ_c = %g、C_u = %g kN/m²" % (GC, CU),
               12.5, C["member"], weight="700")
    cv.text_px(cv.X(5.0), cv.Y(Yz(9.6)), "開挖面 z = %g m（下方仍為黏土）" % H, 12,
               C["load"], weight="700")
    cv.dim((-1.55, Yz(H)), (-1.55, Yz(0)), "H = 8 m", off=0, color=C["dim"], size=12.5,
           label_off=-14)
    cv.dim((-0.7, Yz(HS)), (-0.7, Yz(0)), "3 m", off=0, color=C["dim"], size=11.5,
           label_off=-12)
    rows = ["γ_{av} = (%g×%g + %g×%g)/8 = %.3f kN/m³　⇒　γ_{av}H = %.1f kN/m²"
            % (GS, HS, GC, HC, GBAR, GH),
            "C_{av} = (%.2f×%g + %g×%g)/8 = %.2f kN/m²" % (CUS, HS, CU, HC, CBAR),
            "N = γ_{av}H / C_{av} = %.1f / %.2f = %.2f ＞ 4 ⇒ 軟弱至中度黏土" % (GH, CBAR, NST),
            "p_a = max(γ_{av}H − 4C_{av}, 0.3γ_{av}H) = max(%.1f, %.1f) = %.1f kN/m²" % (PA1, PA2, PA)]
    for i, t in enumerate(rows):
        cv.text_px(PW2/2, PH2-116+i*24, t, 12.5,
                   C["load"] if i >= 2 else C["muted"], weight="700" if i >= 2 else "400")
    cv.text_px(PW2/2, PH2-18, "（若改用 Das 的 Peck 原式，C_{av} = %.2f、N = %.2f ≤ 4 會判成堅硬黏土，見 §5）"
               % (CBAR_DAS, N_DAS), 11.5, C["muted"])
    return cv


def panel_heave():
    cv = Canvas(PW2, PH2, sx=1, bg="#FFFFFF")
    cv.panel(title="抗隆起：Bjerrum–Eide 法（三維修正）", sub="題目給了 B 與 L，就是要你用形狀修正")
    rows = [("Skempton N_c 的兩個修正", "", C["text"]),
            ("形狀修正　1 + 0.2 B/L = 1 + 0.2×%g/%g" % (BW, LW), "= %.3f" % (1+0.2*BW/LW), C["muted"]),
            ("深度修正　1 + 0.2 D/B = 1 + 0.2×%g/%g" % (H, BW), "= %.4f" % (1+0.2*H/BW), C["muted"]),
            ("N_c = 5 × %.3f × %.4f" % (1+0.2*BW/LW, 1+0.2*H/BW), "= %.3f" % NC, C["deform"]),
            ("上限檢核　7.5(1+0.2B/L)", "= %.3f ✓ 未超過" % NCAP, C["muted"])]
    for i, (a, b, col) in enumerate(rows):
        y = 116 + i*30
        cv.text_px(40, y, a, 13 if i == 0 else 12.5, col, anchor="start",
                   weight="700" if i in (0, 3) else "400")
        if b: cv.text_px(PW2-46, y, b, 12.5, col, anchor="end", weight="700" if i == 3 else "400")
    # FS 條
    y0 = 300
    cv.text_px(40, y0, "FS = N_c·C_u / (γ_{av}H) = %.3f × %g / %.1f" % (NC, CU, GH), 13.5,
               C["text"], anchor="start", weight="700")
    bw, x0 = 380, 250
    for i, (lab, val, col) in enumerate((("抵抗　N_c·C_u", NC*CU, C["deform"]),
                                         ("驅動　γ_{av}H", GH, C["load"]))):
        y = y0 + 44 + i*44
        cv.text_px(40, y, lab, 12.5, C["muted"], anchor="start")
        peak = max(NC*CU, GH)
        cv.rect_px(x0, y-16, bw, 32, "#EDF1F6", 8)
        cv.rect_px(x0, y-16, bw*val/peak, 32, col, 8)
        cv.text_px(x0+bw*val/peak-12, y, "%.1f" % val, 13, "#FFFFFF", anchor="end", weight="700")
        cv.text_px(x0+bw+14, y, "kN/m²", 11.5, C["muted"], anchor="start")
    cv.text_px(40, y0+152, "FS = %.3f" % FS, 20, C["deform"], anchor="start", weight="700")
    cv.text_px(190, y0+154, "（≥ 1.5，坑底不會隆起）", 12.5, C["muted"], anchor="start")
    note = ["這個 FS 反過來鎖定第一部分的 m 係數：",
            "Peck 的 m = 0.4 只用在「坑底軟弱正常壓密黏土、深厚、抗隆起偏低」的情況。",
            "本題 FS = %.2f ≥ 1.5，不屬該情形，故 m = 1.0。" % FS,
            "若誤取 m = 0.4：p_a = %.1f − 0.4×%.1f = %.1f kN/m²，是本解的 %.2f 倍。"
            % (GH, 4*CBAR, PA_M04, PA_M04/PA)]
    for i, t in enumerate(note):
        cv.text_px(40, PH2-124+i*24, t, 12.5,
                   C["load"] if i == 3 else C["muted"], anchor="start",
                   weight="700" if i in (0, 3) else "400")
    return cv


def fig2():
    compose([panel_profile(), panel_heave()], cols=2,
            title="SM-2015-3 (二)　等值參數與抗隆起，以及兩個子題的連動",
            note="先算抗隆起、再回頭確認 m 係數，是本題最容易被忽略的一條線。",
            path=os.path.join(OUT, "SM-2015-3-fig-2-heave.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print("γ_{av}=%.4f γ_{av}H=%.2f C_us=%.4f C_{av}=%.4f N=%.4f" % (GBAR, GH, CUS, CBAR, NST))
    print("p_a1=%.3f p_a2=%.3f p_a=%.3f" % (PA1, PA2, PA))
    print("正確合力=%.2f 形心=%.4f ／ 誤用合力=%.2f（低估 %.2f%%）"
          % (P_TOT, ZBAR, P_BAD, 100*(P_TOT-P_BAD)/P_TOT))
    print("Nc=%.4f（上限 %.3f） FS=%.4f" % (NC, NCAP, FS))
    print("Das 原式 C_{av}=%.3f N=%.3f ／ m=0.4 時 p_a=%.2f" % (CBAR_DAS, N_DAS, PA_M04))
