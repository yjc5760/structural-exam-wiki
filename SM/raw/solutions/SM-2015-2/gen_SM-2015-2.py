# -*- coding: utf-8 -*-
"""SM-2015-2 圖解。數值全部由本檔依 SM-2015-2.md §3.5 的 L1 重算。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）──────────────────────────────────────────────
H, HC = 8.0, 4.0            # 牆高、黏土層厚（＝地下水位深度）
G1, C1, PHI1 = 17.5, 20.0, 20.0      # 黏土（水位以上，γ_dry）
G2S, PHI2 = 18.5, 30.0               # 砂土（水位以下，γ_sat）
GC, BTOP, BBOT, DTOE = 23.0, 1.0, 3.0, 1.0   # 混凝土、頂寬、底寬、前趾覆土
GW = 9.81

# ── L2（§4）───────────────────────────────────────────────
KA1 = math.tan(R(45 - PHI1/2))**2          # 0.49029
KA2 = math.tan(R(45 - PHI2/2))**2          # 1/3
KP2 = math.tan(R(45 + PHI2/2))**2          # 3.0
GP2 = G2S - GW                             # 8.69
ZC  = 2*C1/(G1*math.sqrt(KA1))             # 3.2643 張力裂縫深度
SV4 = G1*HC                                # 70.00
SA1 = SV4*KA1 - 2*C1*math.sqrt(KA1)        # 6.312  黏土層底
SA2T= SV4*KA2                              # 23.333 砂層頂
SV8 = SV4 + GP2*(H-HC)                     # 104.76
SA2B= SV8*KA2                              # 34.920 砂層底
UB  = GW*(H-HC)                            # 39.24

BLK = [("P_1 黏土三角（z_c–4 m）", 0.5*SA1*(HC-ZC),          (H-HC) + (HC-ZC)/3.0),
       ("P_2 砂土矩形（4–8 m）",   SA2T*(H-HC),              (H-HC)/2.0),
       ("P_3 砂土三角（4–8 m）",   0.5*(SA2B-SA2T)*(H-HC),   (H-HC)/3.0),
       ("P_w 水壓三角（4–8 m）",   0.5*UB*(H-HC),            (H-HC)/3.0)]
PTOT = sum(b[1] for b in BLK)
MTOT = sum(b[1]*b[2] for b in BLK)
YBAR = MTOT/PTOT
PA_EFF = sum(b[1] for b in BLK[:3])

# 抗滑動
AW  = (BTOP + BBOT)/2.0*H
W   = AW*GC                                # 368.0
U1, U2 = GW*(H-HC), GW*DTOE                # 牆踵 39.24、牆趾 9.81
UU  = (U1+U2)/2.0*BBOT                     # 73.575 揚水壓合力
WP  = W - UU                               # 294.43
DL  = 2.0/3.0*PHI2                         # 20°
FR  = WP*math.tan(R(DL))                   # 107.16
PP  = 0.5*KP2*GP2*DTOE**2                  # 13.035
PWP = 0.5*GW*DTOE**2                       # 4.905
FRT = FR + PP + PWP
FS  = FRT/PTOT
# 其他假設情境
FR_NOU = W*math.tan(R(DL)); FS_NOU = (FR_NOU+PP+PWP)/PTOT
FR_D30 = W*math.tan(R(PHI2)); FS_D30 = (FR_D30+PP+PWP)/PTOT
PWC = 0.5*GW*ZC**2                         # 裂縫充水
YWC = H - ZC + ZC/3.0
FS_CRACK = FRT/(PTOT+PWC)

PSC = 0.085                                 # 1 kPa = 0.085 繪圖公尺
P  = lambda q: q*PSC
Yz = lambda z: H - z


# ══════════════════════════════════════════════════════════
# fig-1　牆背壓力分布（含張力裂縫零壓區）
# ══════════════════════════════════════════════════════════
def fig1():
    W1, H1 = 940, 700
    xmin, xmax, ymin, ymax = -1.9, 11.6, -1.4, 10.0
    L, Rm, T, Bm = 44, 44, 66, 132
    sx = min((W1-L-Rm)/(xmax-xmin), (H1-T-Bm)/(ymax-ymin))
    cv = Canvas(W1, H1, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="SM-2015-2 (一)　牆背土壓力＋水壓力分布與合力",
             sub="上段 %.3f m 是張力裂縫，土壓力歸零；水壓力只從地下水位（z = 4 m）起算" % ZC)
    cv.line((0, Yz(H)), (0, Yz(0)), C["member"], 3.4)
    for z in range(0, 9, 2):
        cv.line((0, Yz(z)), (-0.16, Yz(z)), C["muted"], 1.3)
        cv.text_px(cv.X(-0.26), cv.Y(Yz(z)), "%d" % z, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-1.35), cv.Y(Yz(4.0)), "深度", 12.5, C["muted"])
    cv.text_px(cv.X(-1.35), cv.Y(Yz(4.0))+19, "z (m)", 12.5, C["muted"])
    cv.line((0, Yz(0)), (P(80), Yz(0)), C["muted"], 1.6)
    for q in (0, 20, 40, 60, 80):
        cv.line((P(q), Yz(0)), (P(q), Yz(0)+0.14), C["muted"], 1.3)
        cv.text_px(cv.X(P(q)), cv.Y(Yz(0))-17, "%g" % q, 12, C["muted"])
    cv.text_px(cv.X(P(40)), cv.Y(Yz(0))-39, "側向壓力 (kN/m²)", 12.5, C["muted"],
               weight="700")
    # 張力裂縫段
    cv.line((0, Yz(ZC)), (P(70), Yz(ZC)), C["load"], 1.6, dash="7 5")
    cv.polygon([(0, Yz(0)), (P(6.0), Yz(0)), (P(6.0), Yz(ZC)), (0, Yz(ZC))],
               "rgba(220,38,38,0.10)", "none")
    cv.text_px(cv.X(P(11.0)), cv.Y(Yz(ZC/2.0)), "張力裂縫區", 12.5, C["load"],
               anchor="start", weight="700")
    cv.text_px(cv.X(P(11.0)), cv.Y(Yz(ZC/2.0))+19, "σ_a ＜ 0，土壓力歸零", 11.5,
               C["load"], anchor="start")
    cv.text_px(cv.X(P(11.0)), cv.Y(Yz(ZC))-14, "z_c = 2c/(γ√K_a) = %.3f m" % ZC, 12,
               C["load"], anchor="start", weight="700")
    # 黏土三角（zc→4 m）
    cv.polygon([(0, Yz(ZC)), (P(SA1), Yz(HC)), (0, Yz(HC))],
               "rgba(180,83,9,0.28)", C["accent"], 2.2)
    cv.text_px(cv.X(P(SA1))+8, cv.Y(Yz(HC))+16, "%.2f（黏土層底）" % SA1, 11.5,
               C["accent"], anchor="start")
    # 砂土有效土壓（4→8 m）
    cv.polygon([(0, Yz(HC)), (P(SA2T), Yz(HC)), (P(SA2B), Yz(H)), (0, Yz(H))],
               "rgba(180,83,9,0.20)", C["accent"], 2.4)
    # 水壓（4→8 m，疊在右側）
    cv.polygon([(P(SA2T), Yz(HC)), (P(SA2B), Yz(H)), (P(SA2B+UB), Yz(H))],
               "rgba(29,78,216,0.26)", C["deform"], 2.4)
    cv.text_px(cv.X(P(SA2T))+8, cv.Y(Yz(HC))+37, "%.2f（土層交界跳躍）" % SA2T, 11.5,
               C["accent"], anchor="start")
    cv.text_px(cv.X(P(SA2B))+2, cv.Y(Yz(H))+18, "%.2f" % SA2B, 11.5, C["accent"],
               anchor="middle")
    cv.text_px(cv.X(P(SA2B+UB))+7, cv.Y(Yz(H)), "%.2f ＝ %.2f + %.2f"
               % (SA2B+UB, SA2B, UB), 12, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(P(SA2T*0.5)), cv.Y(Yz(7.3)), "砂土有效土壓", 12, C["accent"],
               weight="700")
    cv.text_px(cv.X(P(SA2B+UB*0.42)), cv.Y(Yz(7.1)), "水壓力", 12, C["deform"],
               weight="700")
    # 合力
    cv.arrow((P(76), Yz(H-YBAR)), (P(SA2B+UB)*0.42, Yz(H-YBAR)), C["load"], 4.0, 12)
    cv.line((0, Yz(H-YBAR)), (P(76), Yz(H-YBAR)), C["load"], 1.2, dash="4 4")
    cv.text_px(cv.X(P(77)), cv.Y(Yz(H-YBAR))-15, "P_{total} = %.2f kN/m" % PTOT, 13.5,
               C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(P(77)), cv.Y(Yz(H-YBAR))+7, "作用點距牆底 %.3f m" % YBAR, 12,
               C["muted"], anchor="start")
    x0 = 60; ytab = H1 - 116
    cv.rect_px(x0-12, ytab-24, 820, 28, "#ECEFF1", 6)
    for j, hcell in enumerate(["分塊", "P_i (kN/m)", "y_i (m)", "力矩 (kN·m/m)"]):
        cv.text_px(x0 + (0, 300, 400, 520)[j], ytab-10, hcell, 12, C["text"],
                   anchor="start" if j == 0 else "end", weight="700")
    for i, (name, pi, yi) in enumerate(BLK):
        yy = ytab + 14 + i*21
        cv.text_px(x0, yy, name, 11.5, C["muted"], anchor="start")
        cv.text_px(x0+300, yy, "%.2f" % pi, 11.5, C["text"], anchor="end")
        cv.text_px(x0+400, yy, "%.3f" % yi, 11.5, C["text"], anchor="end")
        cv.text_px(x0+520, yy, "%.2f" % (pi*yi), 11.5, C["text"], anchor="end")
    cv.text_px(x0+620, ytab+35, "有效土壓合力 %.2f kN/m" % PA_EFF, 12, C["accent"],
               anchor="start", weight="700")
    cv.text_px(x0+620, ytab+56, "水壓合力 %.2f kN/m" % BLK[3][1], 12, C["deform"],
               anchor="start", weight="700")
    cv.text_px(W1/2, H1-22, "ΣP = %.2f kN/m　　ΣM = %.2f kN·m/m　　作用點 = %.3f m（距牆底）"
               % (PTOT, MTOT, YBAR), 13.5, C["load"], weight="700")
    cv.save(os.path.join(OUT, "SM-2015-2-fig-1-pressure.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　抗滑動自由體圖 ＋ 四種假設的 FS
# ══════════════════════════════════════════════════════════
PW2, PH2 = 740, 700


def panel_fbd():
    xmin, xmax, ymin, ymax = -6.4, 8.2, -3.4, 9.6
    L, Rm, T, Bm = 34, 34, 62, 92
    sx = min((PW2-L-Rm)/(xmax-xmin), (PH2-T-Bm)/(ymax-ymin))
    cv = Canvas(PW2, PH2, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="(二) 抗滑動自由體圖", sub="驅動＝土壓＋水壓；抵抗＝底面摩擦＋被動側")
    wall = [(-BBOT, 0), (0, 0), (0, H), (-BTOP, H)]
    cv.polygon([(0, 0), (7.9, 0), (7.9, H), (0, H)], "rgba(180,83,9,0.10)")
    cv.polygon([(0, 0), (7.9, 0), (7.9, Yz(HC)), (0, Yz(HC))], "rgba(29,78,216,0.10)")
    cv.line((0, Yz(HC)), (7.9, Yz(HC)), C["deform"], 1.6, dash="7 5")
    cv.text_px(cv.X(7.7), cv.Y(Yz(HC))-13, "G.W.T. (z = 4 m)", 12, C["deform"],
               anchor="end", weight="700")
    cv.polygon([(-6.2, DTOE), (-BBOT, DTOE), (-BBOT, 0), (-6.2, 0)],
               "rgba(63,74,90,0.16)")
    cv.line((-6.2, DTOE), (-BBOT, DTOE), C["muted"], 1.8)
    cv.line((-6.2, 0), (7.9, 0), C["muted"], 2.2)
    cv.text_px(cv.X(-4.6), cv.Y(DTOE+0.62), "前趾覆土 %g m" % DTOE, 11.5, C["muted"])
    cv.polygon(wall, "rgba(148,163,184,0.32)", C["member"], 2.6)
    cv.arrow((-BBOT/2.0-0.30, H*0.62), (-BBOT/2.0-0.30, H*0.62-1.7), C["muted"], 3.0, 10)
    cv.text_px(cv.X(-BBOT/2.0-0.55), cv.Y(H*0.62-0.85), "W = %.1f kN/m" % W, 12.5,
               C["muted"], anchor="end", weight="700")
    # 驅動
    cv.arrow((3.4, YBAR), (0.15, YBAR), C["load"], 4.2, 13)
    cv.text_px(cv.X(3.6), cv.Y(YBAR)-15, "ΣF_D = %.2f kN/m" % PTOT, 13,
               C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(3.6), cv.Y(YBAR)+6, "（有效土壓 %.1f ＋ 水壓 %.1f）" % (PA_EFF, BLK[3][1]),
               11.5, C["muted"], anchor="start")
    # 揚水壓（梯形，向上）
    us = 0.9/U1
    cv.polygon([(-BBOT, 0), (0, 0), (0, -U1*us), (-BBOT, -U2*us)],
               "rgba(29,78,216,0.22)", C["deform"], 1.8)
    for k in range(6):
        x = -BBOT + k*BBOT/5.0
        h = (U2 + (U1-U2)*(x+BBOT)/BBOT)*us
        cv.arrow((x, -h), (x, -0.06), C["deform"], 1.6, 6)
    cv.text_px(cv.X(1.05), cv.Y(-U1*us*0.55), "U = %.2f kN/m（揚水壓）" % UU, 12,
               C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(1.05), cv.Y(-U1*us*0.55)+19, "牆趾 %.2f → 牆踵 %.2f kN/m²" % (U2, U1),
               11.5, C["muted"], anchor="start")
    # 抵抗
    cv.arrow((-BBOT-0.2, -2.15), (0.0, -2.15), C["member"], 4.0, 12)
    cv.text_px(cv.X(-BBOT/2.0-0.1), cv.Y(-2.15)+20, "F_r = (W − U)·tanδ = %.2f" % FR,
               12.5, C["member"], weight="700")
    cv.text_px(cv.X(-BBOT/2.0-0.1), cv.Y(-2.15)+39, "δ = (2/3)·φ(砂土) = %g°" % DL,
               11.5, C["muted"])
    cv.arrow((-5.15, DTOE/2.0), (-BBOT-0.1, DTOE/2.0), C["member"], 3.0, 10)
    cv.text_px(cv.X(-5.3), cv.Y(DTOE/2.0)-15, "P_p + P_wp", 12, C["member"],
               anchor="end", weight="700")
    cv.text_px(cv.X(-5.3), cv.Y(DTOE/2.0)+6, "%.2f + %.2f" % (PP, PWP), 11.5,
               C["muted"], anchor="end")
    cv.text_px(PW2/2, PH2-56, "FS = (%.2f + %.2f + %.2f) / %.2f = %.3f"
               % (FR, PP, PWP, PTOT, FS), 15, C["text"], weight="700")
    cv.text_px(PW2/2, PH2-31, "＜ 1.5 ⇒ 抗滑動不恰當", 13, C["load"], weight="700")
    return cv


def panel_bars():
    cv = Canvas(PW2, PH2, sx=1, bg="#FFFFFF")
    cv.panel(title="四種假設下的 FS", sub="不管怎麼假設都遠低於 1.5，結論穩固")
    cases = [("計揚水壓、δ = (2/3)φ = 20°（本解主答）", FRT, PTOT, FS, C["member"]),
             ("不計揚水壓、δ = 20°", FR_NOU+PP+PWP, PTOT, FS_NOU, C["muted"]),
             ("不計揚水壓、δ = φ = 30°（最寬鬆）", FR_D30+PP+PWP, PTOT, FS_D30, C["muted"]),
             ("計揚水壓、且張力裂縫積水（最不利）", FRT, PTOT+PWC, FS_CRACK, C["load"])]
    peak = max(max(c[1], c[2]) for c in cases)
    x0, bw = 300, 330
    for i, (name, res, drv, fs, col) in enumerate(cases):
        y0 = 118 + i*136
        cv.text_px(34, y0, name, 13, col, anchor="start", weight="700")
        for j, (lab, val, cc) in enumerate((("抵抗 ΣF_R", res, C["member"]),
                                            ("驅動 ΣF_D", drv, C["load"]))):
            y = y0 + 32 + j*34
            cv.text_px(34, y, lab, 12, C["muted"], anchor="start")
            cv.rect_px(x0, y-14, bw, 28, "#EDF1F6", 7)
            cv.rect_px(x0, y-14, bw*val/peak, 28, cc, 7)
            cv.text_px(x0 + bw*val/peak - 10, y, "%.1f" % val, 12.5, "#FFFFFF",
                       anchor="end", weight="700")
        cv.text_px(34, y0+102, "FS = %.3f" % fs, 17, col, anchor="start", weight="700")
        cv.text_px(150, y0+104, "（規範需 ≥ 1.5）", 12, C["muted"], anchor="start")
    cv.text_px(PW2/2, PH2-40, "張力裂縫一旦積水，多出 P_w,crack = %.2f kN/m，"
               "FS 再掉到 %.2f" % (PWC, FS_CRACK), 12.5, C["load"], weight="700")
    return cv


def fig2():
    compose([panel_fbd(), panel_bars()], cols=2,
            title="SM-2015-2 (二)　抗滑動檢核與四種假設的敏感度",
            note="牆底揚水壓與牆面摩擦角 δ 都是「題目沒給、必須自己假設」的量；"
                 "把假設寫清楚比選哪個值更重要。",
            path=os.path.join(OUT, "SM-2015-2-fig-2-sliding.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print("Ka1=%.5f Ka2=%.5f zc=%.4f σa1(4)=%.3f σa2(4)=%.3f σa2(8)=%.3f u=%.2f"
          % (KA1, KA2, ZC, SA1, SA2T, SA2B, UB))
    for n, p_, y_ in BLK: print("  %-24s P=%8.3f y=%.3f M=%9.3f" % (n, p_, y_, p_*y_))
    print("ΣP=%.3f ΣM=%.3f ȳ=%.4f 有效土壓=%.3f" % (PTOT, MTOT, YBAR, PA_EFF))
    print("W=%.1f U=%.3f W'=%.3f Fr=%.3f Pp=%.3f Pwp=%.3f ΣFR=%.3f FS=%.4f"
          % (W, UU, WP, FR, PP, PWP, FRT, FS))
    print("FS(不計U)=%.4f  FS(δ=30°,不計U)=%.4f  Pw,crack=%.3f FS(裂縫積水)=%.4f"
          % (FS_NOU, FS_D30, PWC, FS_CRACK))
