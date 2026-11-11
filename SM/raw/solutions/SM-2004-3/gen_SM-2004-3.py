# -*- coding: utf-8 -*-
"""SM-2004-3 圖解。數值全部由本檔依 SM-2004-3.md §3.5 的 L1 重算。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）──────────────────────────────────────────────
H, GT, GSAT, PHI, PDES, GW = 6.0, 19.2, 19.2, 35.0, 146.0, 9.81
# ── L2（§4）───────────────────────────────────────────────
KA   = math.tan(Rad(45 - PHI/2))**2          # 0.27099
GP   = GSAT - GW                             # 9.39
PA0  = 0.5*KA*GT*H**2                        # 93.654（無水）
CO   = 0.5*GW*(1.0 - KA)                     # 3.5758  ← Ph(x) 的二次項係數
XCR  = math.sqrt((PDES - PA0)/CO)            # 3.826
def Ph(x):  return PA0 + CO*x**2
def Pa(x):  return PA0 - 0.5*KA*GW*x**2
def Pw(x):  return 0.5*GW*x**2
# 臨界狀態的壓力分布控制點（深度自地表起算）
DW    = H - XCR                              # 2.174 地下水位深度
S_DW  = KA*GT*DW                             # 11.31
S_BOT = S_DW + KA*GP*XCR                     # 21.05
U_BOT = GW*XCR                               # 37.53
S_DRY = KA*GT*H                              # 31.22（無水時牆底值）

PW_, PH_ = 720, 660


# ══════════════════════════════════════════════════════════
# fig-1　剖面 ＋ 兩種水位的壓力分布疊合
# ══════════════════════════════════════════════════════════
def panel_section():
    xmin, xmax, ymin, ymax = -3.1, 9.3, -1.5, 8.4
    L, R, T, Bm = 34, 34, 62, 100
    sx = min((PW_-L-R)/(xmax-xmin), (PH_-T-Bm)/(ymax-ymin))
    cv = Canvas(PW_, PH_, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="題目剖面：水位高度 x 是未知數",
             sub="牆後回填土 γ_t = γ_sat = %g kN/m³（本題唯一的「非典型」設定）" % GT)
    cv.polygon([(-1.9, 0), (0, 0), (0, H), (-0.9, H)], "rgba(148,163,184,0.30)",
               C["member"], 2.4)
    cv.polygon([(0, 0), (8.6, 0), (8.6, H), (0, H)], "rgba(180,83,9,0.13)")
    cv.line((0, H), (8.6, H), C["muted"], 2.0)
    cv.line((-2.5, 0), (8.6, 0), C["muted"], 2.0)
    cv.polygon([(0, 0), (8.6, 0), (8.6, XCR), (0, XCR)], "rgba(29,78,216,0.14)")
    cv.line((0, XCR), (8.6, XCR), C["deform"], 1.8, dash="8 5")
    cv.polygon([(7.1, XCR), (7.7, XCR), (7.4, XCR+0.40)], "none", C["deform"], 2.0)
    cv.line((7.15, XCR+0.52), (7.65, XCR+0.52), C["deform"], 1.8)
    cv.text_px(cv.X(7.9), cv.Y(XCR)-13, "G.W.T.", 13, C["deform"], anchor="start",
               weight="700")
    cv.dim((0.7, 0), (0.7, XCR), "x", off=0, color=C["deform"], size=15, label_off=15)
    cv.dim((-2.45, 0), (-2.45, H), "6 m", off=0, color=C["dim"], size=13, label_off=-14)
    cv.text_px(cv.X(4.7), cv.Y(H*0.74), "非凝聚性回填土　c = 0、φ = %g°" % PHI,
               13, C["accent"], weight="700")
    cv.text_px(cv.X(4.7), cv.Y(H*0.74)+21, "水位以下改用 γ' = %g − %g = %.2f kN/m³"
               % (GSAT, GW, GP), 12, C["muted"])
    cv.text_px(cv.X(4.7), cv.Y(XCR*0.45), "水位以下：有效應力 σ_v' 用 γ'，另加孔隙水壓 u",
               12, C["deform"])
    cv.arrow((0.0, H/3.0), (-1.35, H/3.0), C["load"], 3.6, 12)
    cv.text_px(cv.X(1.25), cv.Y(H/3.0)-16, "土壓力＋水壓力推向左", 12, C["load"],
               anchor="start", weight="700")
    cv.arrow((-2.35, -0.72), (-0.15, -0.72), C["deform"], 3.6, 12)
    cv.text_px(cv.X(-1.25), cv.Y(-0.72)+20, "牆體可抵抗 %g kN/m" % PDES, 12.5,
               C["deform"], weight="700")
    cv.text_px(PW_/2, PH_-64, "忽略牆摩擦（δ = 0）且地表水平 ⇒ 適用 Rankine，"
               "K_A = tan²(45° − φ/2) = %.4f" % KA, 13, C["text"], weight="700")
    cv.text_px(PW_/2, PH_-40, "「忽略毛細現象」＝ 水位以上不產生吸力，該段仍以 u = 0 計算",
               12, C["muted"])
    return cv


PSC = 0.10          # 繪圖用：1 kPa = 0.10 繪圖公尺（避免兩軸單位不同卻等向縮放）


def panel_dist():
    xmin, xmax, ymin, ymax = -1.9, 7.4, -1.35, 7.7
    L, R, T, Bm = 40, 40, 62, 112
    sx = min((PW_-L-R)/(xmax-xmin), (PH_-T-Bm)/(ymax-ymin))
    cv = Canvas(PW_, PH_, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="牆背壓力分布：無水 vs. x = %.3f m" % XCR,
             sub="有效土壓力只掉一點，水壓力卻是滿額加上去")
    P = lambda q: q*PSC                       # kPa → 繪圖公尺
    cv.line((0, 0), (0, H), C["member"], 3.2)
    for z in (0, 2, 4, 6):
        cv.line((0, H-z), (-0.16, H-z), C["muted"], 1.3)
        cv.text_px(cv.X(-0.24), cv.Y(H-z), "%g" % z, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-1.42), cv.Y(H/2.0), "深度", 12.5, C["muted"])
    cv.text_px(cv.X(-1.42), cv.Y(H/2.0)+19, "z (m)", 12.5, C["muted"])
    for q in (0, 20, 40, 60):
        cv.line((P(q), 0), (P(q), -0.16), C["muted"], 1.3)
        cv.text_px(cv.X(P(q)), cv.Y(0)+18, "%g" % q, 12, C["muted"])
    cv.text_px(cv.X(P(32)), cv.Y(0)+41, "側向壓力 (kN/m²)", 12.5, C["muted"], weight="700")
    cv.poly([(0, H), (P(S_DRY), 0)], C["muted"], 2.2, dash="7 5")
    cv.legend(cv.X(P(30)), cv.Y(6.55),
              [(C["accent"], "有效土壓力"), (C["deform"], "孔隙水壓力"),
               (C["muted"], "無水時的分布（底部 %.2f kN/m²）" % S_DRY)], size=12)
    cv.polygon([(0, H), (P(S_DW), H-DW), (P(S_BOT), 0), (0, 0)],
               "rgba(180,83,9,0.24)", C["accent"], 2.4)
    cv.polygon([(P(S_DW), H-DW), (P(S_BOT), 0), (P(S_BOT+U_BOT), 0)],
               "rgba(29,78,216,0.24)", C["deform"], 2.4)
    cv.line((P(S_DW), H-DW), (0, H-DW), C["deform"], 1.4, dash="5 4")
    cv.text_px(cv.X(P(S_DW))+8, cv.Y(H-DW)-11, "G.W.T.　z = %.3f m" % DW, 11.5,
               C["deform"], anchor="start")
    cv.text_px(cv.X(P(S_BOT)*0.45), cv.Y(1.15), "有效土壓力", 12.5, C["accent"], weight="700")
    cv.text_px(cv.X(P(S_BOT)*0.45), cv.Y(1.15)+18, "P_a = %.2f kN/m" % Pa(XCR), 12, C["accent"])
    cv.text_px(cv.X(P(S_BOT+U_BOT/2.0)), cv.Y(2.35), "水壓力", 12.5, C["deform"], weight="700")
    cv.text_px(cv.X(P(S_BOT+U_BOT/2.0)), cv.Y(2.35)+18, "P_w = %.2f kN/m" % Pw(XCR),
               12, C["deform"])
    cv.text_px(cv.X(P(S_BOT+U_BOT)), cv.Y(-0.52), "%.2f" % (S_BOT+U_BOT), 12,
               C["text"], weight="700")
    rows = ["P_a = %.2f kN/m（%.1f%%）　　P_w = %.2f kN/m（%.1f%%）"
            % (Pa(XCR), 100*Pa(XCR)/PDES, Pw(XCR), 100*Pw(XCR)/PDES),
            "合計 %.1f kN/m ＝ 設計抵抗力 ⇒ 恰好發生滑移" % Ph(XCR)]
    for i, t in enumerate(rows):
        cv.text_px(PW_/2, PH_-70+i*25, t, 12.5 if i == 0 else 13.5,
                   C["muted"] if i == 0 else C["text"], weight="400" if i == 0 else "700")
    return cv


def fig1():
    compose([panel_section(), panel_dist()], cols=2,
            title="SM-2004-3　水位上升如何改寫牆背壓力",
            note="只佔牆高 %.0f%% 的下段積水，就貢獻了總推力的 %.0f%%——"
                 "水從來不是配角。" % (100*XCR/H, 100*Pw(XCR)/PDES),
            path=os.path.join(OUT, "SM-2004-3-fig-1-pressure.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　P_h(x) 曲線與臨界水位
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2 = 860, 600
    xmin, xmax, ymin, ymax = -0.55, 6.75, -22.0, 250.0
    L, R, T, Bm = 76, 190, 74, 96
    sxx = (W2-L-R)/(xmax-xmin); syy = (H2-T-Bm)/(ymax-ymin)
    cv = Canvas(W2, H2, sx=1, bg="#FFFFFF")
    Xp = lambda x: L + (x-xmin)*sxx
    Yp = lambda y: H2 - Bm - (y-ymin)*syy
    cv.panel(title="總水平推力隨水位高度 x 的變化",
             sub="P_h(x) = ½K_Aγ_t H² + ½γ_w(1 − K_A)x²  ——  必為遞增的二次式")
    # 座標軸
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (Xp(0), Yp(0), Xp(6.6), Yp(0), C["muted"]))
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (Xp(0), Yp(0), Xp(0), Yp(240), C["muted"]))
    for x in range(0, 7):
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>'
                        % (Xp(x), Yp(0), Xp(x), Yp(-7), C["muted"]))
        cv.text_px(Xp(x), Yp(0)+21, "%d" % x, 12.5, C["muted"])
    for v in range(0, 241, 40):
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.1"/>'
                        % (Xp(0), Yp(v), Xp(6.6), Yp(v), C["border"]))
        cv.text_px(Xp(0)-11, Yp(v), "%d" % v, 12.5, C["muted"], anchor="end")
    cv.text_px((Xp(0)+Xp(6.6))/2, Yp(0)+48, "地下水位高度 x (m)", 13.5, C["text"], weight="700")
    cv.text_px(Xp(0)-6, Yp(240)-30, "水平推力 (kN/m)", 13.5, C["text"], anchor="start")
    xs = [i*6.6/300 for i in range(301)]
    def curve(f, col, w, dash=None):
        pts = " ".join("%.2f,%.2f" % (Xp(x), Yp(f(x))) for x in xs)
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
                        'stroke-linejoin="round"%s/>' % (pts, col, w, d))
    curve(Pa, C["accent"], 2.6, "8 5")
    curve(Pw, C["deform"], 2.6, "8 5")
    curve(Ph, C["load"], 3.6)
    # 設計抵抗力
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="2.2" stroke-dasharray="6 4"/>'
                    % (Xp(0), Yp(PDES), Xp(6.6), Yp(PDES), C["member"]))
    cv.text_px(Xp(6.6)+8, Yp(PDES), "設計抵抗力 %g kN/m" % PDES, 12.5, C["member"],
               anchor="start", weight="700")
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="1.6" stroke-dasharray="4 4"/>'
                    % (Xp(XCR), Yp(0), Xp(XCR), Yp(PDES), C["load"]))
    cv.parts.append('<circle cx="%.1f" cy="%.1f" r="7" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.6"/>' % (Xp(XCR), Yp(PDES), C["load"]))
    cv.text_px(Xp(XCR), Yp(PDES)-24, "x = %.3f m" % XCR, 14.5, C["load"], weight="700")
    for x, f, col, lab in ((6.35, Ph, C["load"], "P_h = P_a + P_w"),
                           (6.35, Pw, C["deform"], "P_w = ½γ_w x²  ↑"),
                           (6.35, Pa, C["accent"], "P_a（有效土壓）  ↓")):
        cv.text_px(Xp(6.6)+8, Yp(f(x)), lab, 12.5, col, anchor="start", weight="700")
    rows = ["x = 0（無水）：P_h = %.2f kN/m" % Ph(0),
            "x = %.3f m：P_h = %.1f kN/m ＝ 設計值，開始滑移" % (XCR, Ph(XCR)),
            "x = 6 m（水位到地表）：P_h = %.1f kN/m，是無水時的 %.2f 倍" % (Ph(6), Ph(6)/Ph(0))]
    for i, t in enumerate(rows):
        cv.text_px(W2/2, H2-62+i*22, t, 12.5,
                   C["load"] if i == 1 else C["muted"], weight="700" if i == 1 else "400")
    cv.save(os.path.join(OUT, "SM-2004-3-fig-2-thrust-curve.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print("KA=%.5f γ'=%.2f PA0=%.3f 係數=%.4f x=%.4f" % (KA, GP, PA0, CO, XCR))
    print("分布控制點 σ(dw)=%.2f σ(bot)=%.2f u=%.2f 合=%.2f 乾底=%.2f"
          % (S_DW, S_BOT, U_BOT, S_BOT+U_BOT, S_DRY))
    print("Pa=%.2f Pw=%.2f Ph=%.2f  Ph(0)=%.2f Ph(6)=%.2f"
          % (Pa(XCR), Pw(XCR), Ph(XCR), Ph(0), Ph(6)))
