# -*- coding: utf-8 -*-
"""SM-2010-2 圖解。數值全部由本檔依 SM-2010-2.md §3.5 的 L1 重算。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
Rad = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）──────────────────────────────────────────────
H      = 8.0     # 擋土牆高
HS     = 4.0     # 砂土層厚
GDS    = 17.0    # 砂 γdry
GSS    = 18.0    # 砂 γsat
PHIS   = 30.0    # 砂 φ
GSC    = 17.5    # 黏土 γsat
CU     = 30.0    # 黏土 c
ZW     = 2.0     # 地下水位深度
GW     = 9.81

# ── L2（§4）───────────────────────────────────────────────
KA1 = math.tan(Rad(45 - PHIS/2))**2      # 1/3
KA2 = 1.0                                # φu = 0
GPS = GSS - GW                           # 8.19
S2  = GDS*ZW                             # 34.00   z=2 之 σv'
SA2 = S2*KA1                             # 11.333
S4  = S2 + GPS*(HS-ZW)                   # 50.38   z=4 之 σv'
SA4 = S4*KA1                             # 16.793
U4  = GW*(HS-ZW)                         # 19.62
TOT4= SA4 + U4                           # 36.413  砂層底總側壓
SV4 = GDS*ZW + GSS*(HS-ZW)               # 70.00   z=4 總垂直應力
CA4 = SV4*KA2 - 2*CU*math.sqrt(KA2)      # 10.00   黏土頂總側壓
SV8 = SV4 + GSC*(H-HS)                   # 140.00
CA8 = SV8*KA2 - 2*CU*math.sqrt(KA2)      # 80.00

# 六個壓力區塊（面積 kN/m、力臂自牆底 m）
BLK = [("P_1 砂 0–2 m 三角", 0.5*(ZW)*SA2,           (H-ZW) + ZW/3.0),
       ("P_2 砂 2–4 m 矩形", (HS-ZW)*SA2,            (H-HS) + (HS-ZW)/2.0),
       ("P_3 砂 2–4 m 三角", 0.5*(HS-ZW)*(SA4-SA2),  (H-HS) + (HS-ZW)/3.0),
       ("P_4 砂 2–4 m 水壓", 0.5*(HS-ZW)*U4,         (H-HS) + (HS-ZW)/3.0),
       ("P_5 黏土 4–8 m 矩形", (H-HS)*CA4,           (H-HS)/2.0),
       ("P_6 黏土 4–8 m 三角", 0.5*(H-HS)*(CA8-CA4), (H-HS)/3.0)]
PA_TOT = sum(b[1] for b in BLK)
M_TOT  = sum(b[1]*b[2] for b in BLK)
YBAR   = M_TOT/PA_TOT

# 黏土段「總側壓 vs 靜水壓」的交會深度
def sa_clay(z): return CA4 + GSC*(z-HS)
def u_of(z):    return GW*(z-ZW)
ZX = (2*CU + GW*ZW - (SV4 - GSC*HS))/(GSC - GW)   # 由 sa_clay(z)=u_of(z) 解出
ZX = (CA4 - GSC*HS - (-GW*ZW))/(GW - GSC)          # 同式整理
ZX = (CA4 - GSC*HS + GW*ZW)/(GW - GSC)
UX = u_of(ZX)

PW_, PH_ = 720, 680
PSC = 0.075     # 繪圖用：1 kPa = 0.075 繪圖公尺（兩軸單位不同，必須換算）
P = lambda q: q*PSC
Yz = lambda z: H - z        # 深度 → 繪圖高度（牆底為 0）


def layers(cv, x0, x1, with_labels=True):
    cv.polygon([(x0, Yz(HS)), (x1, Yz(HS)), (x1, Yz(0)), (x0, Yz(0))],
               "rgba(180,83,9,0.14)")
    cv.polygon([(x0, Yz(10.0)), (x1, Yz(10.0)), (x1, Yz(HS)), (x0, Yz(HS))],
               "rgba(63,74,90,0.13)")
    cv.line((x0, Yz(HS)), (x1, Yz(HS)), C["muted"], 2.0)
    cv.line((x0, Yz(0)), (x1, Yz(0)), C["muted"], 2.0)
    cv.line((x0, Yz(ZW)), (x1, Yz(ZW)), C["deform"], 1.8, dash="8 5")


# ══════════════════════════════════════════════════════════
# fig-1　剖面與各深度的應力狀態
# ══════════════════════════════════════════════════════════
def fig1():
    xmin, xmax, ymin, ymax = -2.9, 10.2, -2.3, 9.4
    L, R, T, Bm = 40, 40, 64, 262
    sx = min((PW_-L-R)/(xmax-xmin), (PH_-T-Bm)/(ymax-ymin))
    cv = Canvas(PW_, PH_, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="題目剖面（本題考卷無附圖）：兩層土、一個水位、兩種分析法",
             sub="砂土用有效應力法（另加水壓），黏土用 φ_u = 0 總應力法（水壓已含在內）")
    layers(cv, 0.0, 9.9)
    cv.polygon([(-2.2, Yz(H)), (0, Yz(H)), (0, Yz(0)), (-1.3, Yz(0))],
               "rgba(148,163,184,0.30)", C["member"], 2.4)
    cv.line((-2.4, Yz(0)), (0, Yz(0)), C["muted"], 2.0)
    cv.polygon([(7.9, Yz(ZW)), (8.5, Yz(ZW)), (8.2, Yz(ZW)-0.42)], "none", C["deform"], 2.0)
    cv.line((7.95, Yz(ZW)-0.56), (8.45, Yz(ZW)-0.56), C["deform"], 1.8)
    cv.text_px(cv.X(8.7), cv.Y(Yz(ZW))-13, "G.W.T. (−2 m)", 12.5, C["deform"],
               anchor="start", weight="700")
    cv.text_px(cv.X(4.9), cv.Y(Yz(0.9)), "砂土層　厚 %g m" % HS, 13, C["accent"], weight="700")
    cv.text_px(cv.X(4.9), cv.Y(Yz(1.5)), "γ_dry = %g、γ_sat = %g、φ = %g°、c = 0"
               % (GDS, GSS, PHIS), 12, C["muted"])
    cv.text_px(cv.X(4.9), cv.Y(Yz(2.6)), "水位以下 γ' = %g − %g = %.2f" % (GSS, GW, GPS),
               12, C["deform"])
    cv.text_px(cv.X(4.9), cv.Y(Yz(5.2)), "黏土層　厚 10 m（牆體入土 %g m）" % (H-HS),
               13, C["member"], weight="700")
    cv.text_px(cv.X(4.9), cv.Y(Yz(5.8)), "γ_sat = %g、c = %g kN/m²、未給 φ ⇒ φ_u = 0"
               % (GSC, CU), 12, C["muted"])
    cv.dim((-2.55, Yz(H)), (-2.55, Yz(0)), "8 m", off=0, color=C["dim"], size=13,
           label_off=-14)
    cv.line((0, Yz(H)), (-2.55, Yz(H)), C["dim"], 1.0, dash="3 3")
    for z, lab, dy in ((0, "z = 0", -13), (ZW, "z = 2", -13), (HS, "z = 4", -13),
                       (H, "z = 8", 14)):
        cv.dot((0, Yz(z)), 5.0, fill=C["load"])
        cv.text_px(cv.X(0.22), cv.Y(Yz(z))+dy, lab, 11.5, C["load"], anchor="start",
                   weight="700")
    hdr = ["深度 z", "γ 選用", "σ_v 總", "u", "σ_v' 有效", "牆背側壓 σ_a"]
    rows = [["0 m", "—", "0", "0", "0", "0"],
            ["2 m", "γ_dry = %g" % GDS, "%.2f" % (GDS*ZW), "0", "%.2f" % S2,
             "%.2f（K_a=1/3）" % SA2],
            ["4 m 砂底", "γ_sat = %g" % GSS, "%.2f" % SV4, "%.2f" % U4, "%.2f" % S4,
             "%.2f ＝ %.2f + %.2f" % (TOT4, SA4, U4)],
            ["4 m 黏頂", "總應力", "%.2f" % SV4, "（已含）", "—",
             "%.2f ＝ σ_v − 2c" % CA4],
            ["8 m 牆底", "γ_sat = %g" % GSC, "%.2f" % SV8, "（已含）", "—",
             "%.2f ＝ σ_v − 2c" % CA8]]
    x0, colw = 44, [86, 104, 92, 78, 92, 190]
    ytab = PH_ - 208
    xs = [x0]
    for w in colw: xs.append(xs[-1] + w)
    cv.rect_px(x0-10, ytab-24, sum(colw)+20, 30, "#ECEFF1", 6)
    for j, hcell in enumerate(hdr):
        cv.text_px(xs[j], ytab-9, hcell, 12, C["text"], anchor="start", weight="700")
    for i, r in enumerate(rows):
        yy = ytab + 18 + i*30
        col = C["accent"] if i <= 2 else C["member"]
        for j, cell in enumerate(r):
            cv.text_px(xs[j], yy, cell, 12, col if j else C["text"], anchor="start",
                       weight="700" if j == 0 else "400")
    cv.text_px(PW_/2, PH_-24,
               "z = 4 m 有兩列：砂土交出「有效土壓＋水壓」，黏土接手「總側壓」，兩者不可相加",
               12.5, C["load"], weight="700")
    cv.save(os.path.join(OUT, "SM-2010-2-fig-1-profile.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　牆背壓力分布圖與六個分塊（題目明文要求）
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2 = 980, 700
    xmin, xmax, ymin, ymax = -1.7, 12.4, -1.5, 9.9
    L, R, T, Bm = 44, 44, 66, 126
    sx = min((W2-L-R)/(xmax-xmin), (H2-T-Bm)/(ymax-ymin))
    cv = Canvas(W2, H2, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="SM-2010-2　牆背各項壓力分布圖與合力",
             sub="題目明文要求「繪出牆背所受各項壓力分佈圖並計算所有合力及作用位置」")
    cv.line((0, Yz(H)), (0, Yz(0)), C["member"], 3.4)
    for z in range(0, 9, 2):
        cv.line((0, Yz(z)), (-0.16, Yz(z)), C["muted"], 1.3)
        cv.text_px(cv.X(-0.26), cv.Y(Yz(z)), "%d" % z, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-1.25), cv.Y(Yz(4.0)), "深度", 12.5, C["muted"])
    cv.text_px(cv.X(-1.25), cv.Y(Yz(4.0))+19, "z (m)", 12.5, C["muted"])
    cv.line((0, Yz(0)), (P(84), Yz(0)), C["muted"], 1.6)
    for q in (0, 20, 40, 60, 80):
        cv.line((P(q), Yz(0)), (P(q), Yz(0)+0.16), C["muted"], 1.3)
        cv.text_px(cv.X(P(q)), cv.Y(Yz(0))-17, "%g" % q, 12, C["muted"])
    cv.text_px(cv.X(P(42)), cv.Y(Yz(0))-39, "側向壓力 (kN/m²)", 12.5, C["muted"],
               weight="700")
    # 砂層有效土壓（0–4 m）
    cv.polygon([(0, Yz(0)), (P(SA2), Yz(ZW)), (P(SA4), Yz(HS)), (0, Yz(HS))],
               "rgba(180,83,9,0.26)", C["accent"], 2.4)
    # 砂層水壓（2–4 m，疊在有效土壓右側）
    cv.polygon([(P(SA2), Yz(ZW)), (P(TOT4), Yz(HS)), (P(SA4), Yz(HS))],
               "rgba(29,78,216,0.26)", C["deform"], 2.4)
    # 黏土層總側壓（4–8 m）
    cv.polygon([(0, Yz(HS)), (P(CA4), Yz(HS)), (P(CA8), Yz(H)), (0, Yz(H))],
               "rgba(63,74,90,0.22)", C["member"], 2.4)
    cv.line((0, Yz(HS)), (P(TOT4)+0.35, Yz(HS)), C["load"], 1.8, dash="6 4")
    cv.text_px(cv.X(P(TOT4))+10, cv.Y(Yz(HS))-13, "z = 4 m　壓力突降 %.2f → %.2f"
               % (TOT4, CA4), 12, C["load"], anchor="start", weight="700")
    for q, z, lab in ((SA2, ZW, "%.2f" % SA2), (TOT4, HS, "%.2f" % TOT4),
                      (CA4, HS, "%.2f" % CA4), (CA8, H, "%.2f" % CA8)):
        cv.dot((P(q), Yz(z)), 4.6, fill=C["text"])
    cv.text_px(cv.X(P(SA2))+7, cv.Y(Yz(ZW))+3, "%.2f" % SA2, 11.5, C["accent"], anchor="start")
    cv.text_px(cv.X(P(CA4))+7, cv.Y(Yz(HS))+16, "%.2f" % CA4, 11.5, C["member"], anchor="start")
    cv.text_px(cv.X(P(CA8))+8, cv.Y(Yz(H)), "%.2f" % CA8, 12, C["member"],
               anchor="start", weight="700")
    cv.text_px(cv.X(P(SA4)*0.42), cv.Y(Yz(2.6)), "砂：有效土壓", 12, C["accent"], weight="700")
    cv.text_px(cv.X(P(SA4+U4/2.0)), cv.Y(Yz(3.55)), "水壓", 11.5, C["deform"], weight="700")
    cv.text_px(cv.X(P(CA8)*0.40), cv.Y(Yz(6.6)), "黏土：總側壓 σ_v − 2c", 12,
               C["member"], weight="700")
    cv.text_px(cv.X(P(CA8)*0.40), cv.Y(Yz(7.2)), "（水壓已含在內，不可再加）", 11.5,
               C["load"])
    # 合力
    cv.arrow((P(96), Yz(H-YBAR)), (P(80.5), Yz(H-YBAR)), C["load"], 4.0, 12)
    cv.text_px(cv.X(P(97)), cv.Y(Yz(H-YBAR))-15, "P_A = %.2f kN/m" % PA_TOT, 13.5,
               C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(P(97)), cv.Y(Yz(H-YBAR))+7, "作用點距牆底 %.3f m" % YBAR, 12,
               C["muted"], anchor="start")
    cv.line((0, Yz(H-YBAR)), (P(96), Yz(H-YBAR)), C["load"], 1.2, dash="4 4")
    # 分塊表
    x0 = 66; xs = [x0, x0+236, x0+372, x0+486, x0+606]
    ytab = H2 - 112
    cv.rect_px(x0-12, ytab-24, 768, 28, "#ECEFF1", 6)
    for r in (0, 1):
        xx = x0 + r*372
        for j, hcell in enumerate(["分塊", "P_i (kN/m)", "y_i (m)", "力矩"]):
            off = (0, 186, 250, 330)[j]
            cv.text_px(xx+off, ytab-10, hcell, 11.5, C["text"],
                       anchor="start" if j == 0 else "end", weight="700")
    for i, (name, pi, yi) in enumerate(BLK):
        r, cnum = divmod(i, 3)
        yy = ytab + 12 + cnum*24
        xx = x0 + r*372
        cv.text_px(xx, yy, name, 11.5, C["muted"], anchor="start")
        cv.text_px(xx+186, yy, "%.2f" % pi, 11.5, C["text"], anchor="end")
        cv.text_px(xx+250, yy, "%.3f" % yi, 11.5, C["text"], anchor="end")
        cv.text_px(xx+330, yy, "%.2f" % (pi*yi), 11.5, C["text"], anchor="end")
    cv.text_px(W2/2, H2-24, "ΣP_i = %.2f kN/m　　ΣM = %.2f kN·m/m　　"
               "作用點 = ΣM/ΣP = %.3f m（距牆底）"
               % (PA_TOT, M_TOT, YBAR), 13.5, C["load"], weight="700")
    cv.save(os.path.join(OUT, "SM-2010-2-fig-2-pressure.svg"))


# ══════════════════════════════════════════════════════════
# fig-3　黏土段：總側壓 vs 靜水壓（牆背是否會脫開）
# ══════════════════════════════════════════════════════════
def fig3():
    W3, H3 = 860, 620
    xmin, xmax, ymin, ymax = -1.25, 6.7, -1.15, 5.05
    L, R, T, Bm = 62, 214, 68, 132
    sx = min((W3-L-R)/(xmax-xmin), (H3-T-Bm)/(ymax-ymin))
    cv = Canvas(W3, H3, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="黏土段檢核：總側壓真的撐得住水壓嗎？",
             sub="φ_u = 0 的總側壓 σ_a 若小於同深度的靜水壓 u，牆背會脫開並充水")
    Zy = lambda z: (H - z)*1.10          # 深度 → 繪圖高度（1.10 為版面比例）
    Q  = lambda q: q*0.075
    cv.line((0, Zy(H)), (0, Zy(HS)), C["member"], 3.0)
    for z in (4, 5, 6, 7, 8):
        cv.line((0, Zy(z)), (-0.16, Zy(z)), C["muted"], 1.2)
        cv.text_px(cv.X(-0.26), cv.Y(Zy(z)), "%d" % z, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-1.0), cv.Y(Zy(6)), "z (m)", 12.5, C["muted"])
    for q in (0, 20, 40, 60, 80):
        cv.line((Q(q), Zy(H)), (Q(q), Zy(H)-0.14), C["border"], 1.2)
        cv.text_px(cv.X(Q(q)), cv.Y(Zy(H))+17, "%g" % q, 12, C["muted"])
    cv.text_px(cv.X(Q(40)), cv.Y(Zy(H))+40, "壓力 (kN/m²)", 12.5, C["muted"], weight="700")
    zs = [HS + i*(H-HS)/200.0 for i in range(201)]
    cv.poly([(Q(sa_clay(z)), Zy(z)) for z in zs], C["member"], 3.0)
    cv.poly([(Q(u_of(z)), Zy(z)) for z in zs], C["deform"], 3.0, dash="7 5")
    cv.polygon([(Q(sa_clay(z)), Zy(z)) for z in zs if z <= ZX]
               + [(Q(u_of(z)), Zy(z)) for z in reversed([z for z in zs if z <= ZX])],
               "rgba(220,38,38,0.28)", C["load"], 1.6)
    cv.dot((Q(UX), Zy(ZX)), 6.0, fill=C["load"])
    cv.text_px(cv.X(Q(UX))+10, cv.Y(Zy(ZX)), "z = %.3f m　σ_a = u = %.2f" % (ZX, UX),
               12.5, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(Q(sa_clay(H)))+9, cv.Y(Zy(H)), "σ_a = σ_v − 2c", 12.5,
               C["member"], anchor="start", weight="700")
    cv.text_px(cv.X(Q(u_of(H)))+9, cv.Y(Zy(H)), "u = γ_w(z − 2)", 12.5,
               C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(Q(6)), cv.Y(Zy(4.0))-16, "σ_a ＜ u：牆背受拉，會脫開", 12,
               C["load"], anchor="start", weight="700")
    rows = ["z = 4 m：σ_a = %.2f ＜ u = %.2f ⇒ σ_h' = %.2f（負值，土壤無法承拉）"
            % (CA4, u_of(HS), CA4-u_of(HS)),
            "z = %.3f m：兩者相等（%.2f kN/m²），以下 σ_a ＞ u，牆背恢復受土壓" % (ZX, UX),
            "保守修正：該段取 max(σ_a, u)，P_A 約增加 %.1f kN/m"
            % (0.5*(u_of(HS)-CA4)*(ZX-HS))]
    for i, t in enumerate(rows):
        cv.text_px(W3/2, H3-92+i*24, t, 12.5, C["load"] if i < 2 else C["muted"],
                   weight="700" if i < 2 else "400")
    cv.text_px(W3/2, H3-20, "主答仍寫 φ_u = 0 的標準分布；這一段檢核是區隔「會套公式」"
               "與「知道公式邊界」的地方", 12.5, C["text"], weight="700")
    cv.save(os.path.join(OUT, "SM-2010-2-fig-3-crack-check.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2(); fig3()
    print("Ka1=%.4f γ'=%.2f σa2=%.3f σa4=%.3f u4=%.2f 砂底總=%.3f" % (KA1, GPS, SA2, SA4, U4, TOT4))
    print("σv4=%.2f 黏頂=%.2f σv8=%.2f 牆底=%.2f" % (SV4, CA4, SV8, CA8))
    for n, p_, y_ in BLK: print("  %-22s P=%8.3f  y=%.3f  M=%9.3f" % (n, p_, y_, p_*y_))
    print("ΣP=%.3f ΣM=%.3f ȳ=%.4f" % (PA_TOT, M_TOT, YBAR))
    print("交會 z=%.4f  u=%.3f  σa=%.3f" % (ZX, UX, sa_clay(ZX)))
