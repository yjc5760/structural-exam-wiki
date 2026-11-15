# -*- coding: utf-8 -*-
"""SM-2005-1 圖解。數值全部由本檔依 SM-2005-1.md §3.5 的 L1 重算。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）──────────────────────────────────────────────
GSD, PHI, GCL, CC, HH, HA = 18.0, 32.0, 20.0, 45.0, 9.0, 1.5
# ── L2（§4）───────────────────────────────────────────────
KA   = math.tan(R(45-PHI/2))**2          # 0.30726
PATOP= GSD*HH*KA                         # 49.776
PA   = 0.5*PATOP*HH                      # 223.99
PNET = 4*CC - GSD*HH                     # 18.0
LARM = (2.0/3)*HH - HA                   # 4.5


def solve_D(pnet, Mreq):
    """0.5·p·D² + (H−h_a)·p·D − M = 0 之正根。"""
    a, b, c = 0.5*pnet, (HH-HA)*pnet, -Mreq
    return (-b + math.sqrt(b*b - 4*a*c))/(2*a)


DD = solve_D(PNET, PA*LARM)              # 5.4710
TT = PA - PNET*DD                        # 125.51
C_CRIT = GSD*HH/4.0                      # 40.5

PSC = 0.055                              # 1 kPa = 0.055 繪圖公尺
Pq = lambda q: q*PSC
Yz = lambda z: 16.0 - z                  # 深度 → 繪圖高度（樁頂 z=0 在 y=16）

W1, H1 = 900, 720


# ══════════════════════════════════════════════════════════
# fig-1　土壓力分布與自由端支撐的力矩平衡
# ══════════════════════════════════════════════════════════
def fig1():
    xmin, xmax, ymin, ymax = -4.6, 8.2, -0.6, 17.6
    L, Rm, T, Bm = 44, 44, 66, 118
    sx = min((W1-L-Rm)/(xmax-xmin), (H1-T-Bm)/(ymax-ymin))
    cv = Canvas(W1, H1, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="SM-2005-1　版樁土壓力分布與自由端支撐的力矩平衡",
             sub="砂土段三角形主動土壓；黏土段淨被動土壓為與深度無關的定值 4c − γ_s H")
    zb = HH + DD
    # 地層
    cv.polygon([(0, Yz(HH)), (7.6, Yz(HH)), (7.6, Yz(0)), (0, Yz(0))], "rgba(180,83,9,0.14)")
    cv.polygon([(-4.2, Yz(zb+1.3)), (7.6, Yz(zb+1.3)), (7.6, Yz(HH)), (-4.2, Yz(HH))],
               "rgba(63,74,90,0.14)")
    cv.line((-4.2, Yz(HH)), (7.6, Yz(HH)), C["muted"], 2.2)
    cv.line((0, Yz(0)), (7.6, Yz(0)), C["muted"], 2.0)
    cv.text_px(cv.X(5.6), cv.Y(Yz(3.0)), "砂土", 13.5, C["accent"], weight="700")
    cv.text_px(cv.X(5.6), cv.Y(Yz(3.7)), "γ_s = %g、φ_s = %g°、c = 0" % (GSD, PHI), 11.5, C["muted"])
    cv.text_px(cv.X(5.6), cv.Y(Yz(11.6)), "黏土", 13.5, C["member"], weight="700")
    cv.text_px(cv.X(5.6), cv.Y(Yz(12.3)), "γ_c = %g、φ_c = 0、c = %g kPa" % (GCL, CC), 11.5, C["muted"])
    # 版樁
    cv.line((0, Yz(0)), (0, Yz(zb)), C["member"], 4.4)
    # 地錨
    cv.arrow((0.15, Yz(HA)), (2.9, Yz(HA)), C["deform"], 3.6, 12)
    cv.text_px(cv.X(3.05), cv.Y(Yz(HA))-14, "地錨 T = %.2f kN/m" % TT, 13, C["deform"],
               anchor="start", weight="700")
    cv.dot((0, Yz(HA)), 5.4, fill=C["deform"])
    cv.dim((-0.85, Yz(HA)), (-0.85, Yz(0)), "1.5 m", off=0, color=C["dim"], size=11.5,
           label_off=-13)
    cv.dim((-2.2, Yz(HH)), (-2.2, Yz(0)), "9 m", off=0, color=C["dim"], size=12.5,
           label_off=-14)
    cv.dim((-2.2, Yz(zb)), (-2.2, Yz(HH)), "D = ?", off=0, color=C["load"], size=12.5,
           label_off=-14)
    # 主動土壓（砂土，向右推）
    cv.polygon([(0, Yz(0)), (Pq(PATOP), Yz(HH)), (0, Yz(HH))], "rgba(220,38,38,0.24)",
               C["load"], 2.2)
    for k in range(1, 7):
        z = HH*k/7.0
        cv.arrow((Pq(GSD*z*KA), Yz(z)), (0.06, Yz(z)), C["load"], 1.6, 6)
    cv.text_px(cv.X(Pq(PATOP))+8, cv.Y(Yz(HH))-11, "%.2f kPa" % PATOP, 12, C["load"],
               anchor="start", weight="700")
    cv.text_px(cv.X(Pq(PATOP*0.35)), cv.Y(Yz(4.4)), "主動土壓", 12, C["load"], weight="700")
    # 淨被動土壓（黏土，向左推）
    cv.polygon([(0, Yz(HH)), (-Pq(PNET), Yz(HH)), (-Pq(PNET), Yz(zb)), (0, Yz(zb))],
               "rgba(29,78,216,0.26)", C["deform"], 2.2)
    for k in range(5):
        z = HH + DD*(k+0.5)/5.0
        cv.arrow((-Pq(PNET), Yz(z)), (-0.06, Yz(z)), C["deform"], 1.6, 6)
    cv.text_px(cv.X(-Pq(PNET))-8, cv.Y(Yz(HH+DD*0.16)), "p_{net} = 4c − γ_s H", 12,
               C["deform"], anchor="end", weight="700")
    cv.text_px(cv.X(-Pq(PNET))-8, cv.Y(Yz(HH+DD*0.16))+18, "= %g − %g = %.1f kPa"
               % (4*CC, GSD*HH, PNET), 11.5, C["muted"], anchor="end")
    # 合力
    cv.dot((Pq(PATOP*0.4), Yz(2*HH/3.0)), 5.6, fill=C["load"])
    cv.text_px(cv.X(Pq(PATOP*0.4))+9, cv.Y(Yz(2*HH/3.0))+15, "P_a = %.2f kN/m" % PA, 12.5,
               C["load"], anchor="start", weight="700")
    cv.dot((-Pq(PNET*0.5), Yz(HH+DD*0.5)), 5.6, fill=C["deform"])
    cv.text_px(cv.X(-Pq(PNET*0.5))-9, cv.Y(Yz(HH+DD*0.62))+18, "P_{net} = %.1f·D" % PNET, 12.5,
               C["deform"], anchor="end", weight="700")
    rows = ["對地錨取矩：P_{net}·(7.5 + 0.5D) = P_a·%.1f　⇒　D² + 15D − %.3f = 0" % (LARM, PA*LARM/9.0),
            "⇒　D = %.3f m　（理論最少入土深度，FS = 1.0）" % DD,
            "水平力平衡：T = P_a − p_{net}·D = %.2f − %.1f×%.3f = %.2f kN/m" % (PA, PNET, DD, TT)]
    for i, t in enumerate(rows):
        cv.text_px(W1/2, H1-96+i*26, t, 13 if i == 1 else 12.5,
                   C["load"] if i == 1 else C["text"], weight="700")
    cv.text_px(W1/2, H1-18, "力矩點必須取在地錨——這樣才能消去未知的 T，只剩 D 一個未知數",
               12.5, C["muted"])
    cv.save(os.path.join(OUT, "SM-2005-1-fig-1-pressure.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　D 與 T 對 c 的敏感度（c → 40.5 kPa 時 D 發散）
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2 = 900, 620
    c0, c1 = 40.6, 50.0
    L, Rm, T, Bm = 82, 210, 74, 128
    Dmax = 26.0
    Xp = lambda c: L + (c-c0)/(c1-c0)*(W2-L-Rm)
    Yp = lambda d: H2 - Bm - d/Dmax*(H2-T-Bm)
    cv = Canvas(W2, H2, sx=1, bg="#FFFFFF")
    cv.panel(title="所需入土深度 D 對黏土凝聚力 c 的敏感度",
             sub="抗力係數 p_{net} = 4c − γ_s H 只剩 18 kPa（是 4c 的 10%）；c 再降一點就沒有解")
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (L, Yp(0), W2-Rm, Yp(0), C["muted"]))
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (L, Yp(0), L, T+6, C["muted"]))
    for c in range(41, 51):
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>'
                        % (Xp(c), Yp(0), Xp(c), Yp(0)+7, C["muted"]))
        cv.text_px(Xp(c), Yp(0)+22, "%d" % c, 12, C["muted"])
    for d in range(0, 27, 5):
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.1"/>'
                        % (L, Yp(d), W2-Rm, Yp(d), C["border"]))
        cv.text_px(L-10, Yp(d), "%d" % d, 12, C["muted"], anchor="end")
    cv.text_px((L+W2-Rm)/2, Yp(0)+50, "黏土凝聚力 c (kPa)", 13.5, C["text"], weight="700")
    cv.text_px(L-4, T-4, "所需入土深度 D (m)", 13, C["text"], anchor="start")
    pts = []
    cx = c0
    while cx <= c1 + 1e-9:
        pn = 4*cx - GSD*HH
        d = solve_D(pn, PA*LARM)
        if d <= Dmax: pts.append((Xp(cx), Yp(d)))
        cx += 0.02
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3.4" '
                    'stroke-linejoin="round"/>'
                    % (" ".join("%.2f,%.2f" % p for p in pts), C["load"]))
    # 漸近線
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="2.2" stroke-dasharray="7 5"/>'
                    % (Xp(C_CRIT), Yp(0), Xp(C_CRIT), T+10, C["member"]))
    cv.text_px(Xp(C_CRIT)+10, T+26, "c = γ_s H/4 = %.1f kPa" % C_CRIT, 12.5, C["member"],
               anchor="start", weight="700")
    cv.text_px(Xp(C_CRIT)+10, T+45, "p_{net} = 0 ⇒ 任何 D 都不平衡", 11.5, C["muted"], anchor="start")
    for cx, tag in ((45.0, "題給 c = 45"), (42.0, ""), (43.0, "")):
        pn = 4*cx - GSD*HH; d = solve_D(pn, PA*LARM)
        cv.parts.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="#FFFFFF" '
                        'stroke-width="2.6"/>' % (Xp(cx), Yp(d), 7 if tag else 5,
                                                  C["load"] if tag else C["muted"]))
        if tag:
            cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                            'stroke-width="1.4" stroke-dasharray="4 4"/>'
                            % (L, Yp(d), Xp(cx), Yp(d), C["load"]))
            cv.text_px(Xp(cx)+12, Yp(d)-14, "%s ⇒ D = %.2f m" % (tag, d), 13.5, C["load"],
                       anchor="start", weight="700")
        else:
            cv.text_px(Xp(cx), Yp(d)-16, "%.2f" % d, 11.5, C["muted"])
    cv.legend(W2-Rm+16, T+90, [(C["load"], "D(c) 由力矩平衡解出"),
                               (C["member"], "無解的邊界")], size=12)
    rows = ["c 只要降 10%（45 → 40.5 kPa），p_{net} 由 18 kPa 歸零，再深的版樁也救不回來",
            "——因為抗力與 D 成正比，而係數本身變成零。"]
    for i, t in enumerate(rows):
        cv.text_px(W2/2, H2-64+i*25, t, 13 if i == 0 else 12.5,
                   C["load"] if i == 0 else C["muted"], weight="700" if i == 0 else "400")
    cv.save(os.path.join(OUT, "SM-2005-1-fig-2-sensitivity.svg"))



# ══════ fig-1-problem：題目附圖重繪（2026-11-15，題目正本推廣 SM-U2-3 批 1）══════
# 幾何只取自題目正本 SM-2005-1-problem.md §4 判讀清單，不含任何解題結果。
# 用法：python gen_SM-2005-1.py [輸出資料夾]；只寫 SM-2005-1-fig-1-problem.svg 到該資料夾（預設本題 figs/）。
def _pgeo():
    sys.path.insert(0, os.path.join(HERE, ".."))      # SM/raw/solutions/geo.py
    import geo
    return geo


def _ground(cv, x0, x1, y, n=4, s=0.35):
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        cv.line((x, y), (x - s, y - s), C["member"], 1.3)


def _wall(cv, x, y0, y1, t=0.18, fill="#3F4A5A"):
    cv.polygon([(x - t / 2, y0), (x + t / 2, y0), (x + t / 2, y1), (x - t / 2, y1)], fill)


def fig_problem(out):
    g = _pgeo()
    H_EXC, Z_ANC, D_SK = 9.0, 1.5, 4.0     # 開挖 9 m（#開挖深度）、地錨頂下 1.5 m（#地錨）；入土段為示意
    Wd, Ht = 760, 640
    XL, XR = -4.0, 7.0
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **g.fit(Wd, Ht, (XL - 1.0, XR + 0.3), (-(H_EXC + D_SK + 0.6), 0.9), 30, 30, 40, 40))
    Y = lambda d: -d
    g.soil_fill(cv, 0, XR, Y(H_EXC), Y(0), "rgba(180,83,9,0.16)")
    g.soil_fill(cv, XL, XR, Y(H_EXC + D_SK + 0.4), Y(H_EXC), "rgba(63,74,90,0.20)")
    cv.line((0, Y(0)), (XR, Y(0)), C["member"], 2.4)
    _ground(cv, 3.6, 6.0, Y(0), 4, 0.3)
    cv.line((XL, Y(H_EXC)), (XR, Y(H_EXC)), C["member"], 2.0)
    _ground(cv, XL + 0.5, -1.0, Y(H_EXC), 4, 0.3)
    _wall(cv, 0, Y(0), Y(H_EXC + D_SK), 0.16)
    cv.arrow((0.1, Y(Z_ANC)), (2.8, Y(Z_ANC)), C["load"], 2.6, 10)
    cv.text_px(cv.X(1.4), cv.Y(Y(Z_ANC)) - 15, "地錨", 13.5, C["load"], weight="700")
    cv.text_px(cv.X(1.0), cv.Y(Y(4.4)), "砂土", 14, C["text"], anchor="start", weight="700")
    for i, s in enumerate(["γ_{s} = 18 kN/m^{3}", "φ_{s} = 32°", "c_{s} = 0"]):
        cv.math_px(cv.X(1.0), cv.Y(Y(5.2 + 0.75 * i)), s, 14, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(H_EXC + 0.8)), "黏土", 14, C["text"], anchor="start", weight="700")
    for i, s in enumerate(["γ_{c} = 20 kN/m^{3}", "φ_{c} = 0°", "c_{c} = 45 kPa"]):
        cv.math_px(cv.X(1.0), cv.Y(Y(H_EXC + 1.55 + 0.75 * i)), s, 14, C["text"], anchor="start")
    cv.line((-0.35, Y(H_EXC + 1.2)), (-0.75, Y(H_EXC + 1.6)), C["muted"], 1.2)
    cv.line((-0.75, Y(H_EXC + 1.6)), (-0.75, Y(H_EXC + D_SK - 0.3)), C["muted"], 1.2)
    cv.line((-0.75, Y(H_EXC + D_SK - 0.3)), (-0.35, Y(H_EXC + D_SK)), C["muted"], 1.2)
    cv.text_px(cv.X(-0.95), cv.Y(Y(H_EXC + 2.3)), "free earth support", 12.5, C["muted"], anchor="end")
    cv.text_px(cv.X(-0.95), cv.Y(Y(H_EXC + 2.9)), "（自由土壤支撐）", 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-2.0), cv.Y(Y(4.0)), "開挖側", 13, C["muted"])
    xd = XL - 0.4
    cv.dim((xd, Y(H_EXC)), (xd, Y(0)), "9 m", 0, C["dim"], 13, label_off=-24)
    for d in (0, H_EXC):
        cv.line((xd - 0.12, Y(d)), (-0.1 if d == 0 else XL, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.dim((-0.8, Y(Z_ANC)), (-0.8, Y(0)), "1.5 m", 0, C["dim"], 12, label_off=-26)
    compose([cv], title="SM-2005-1 題目附圖重繪",
            sub="依題目正本判讀清單；地下水位以上，黏土內為自由土壤支撐",
            note="攔錯用：9 m 由版樁頂量到開挖面，背填砂在右側；開挖面以下兩側都是黏土，地錨在頂下 1.5 m。",
            path=os.path.join(out, "SM-2005-1-fig-1-problem.svg"))

if __name__ == "__main__":
    fig_problem(sys.argv[1] if len(sys.argv) > 1 else OUT)
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2()
    print("Ka=%.6f p_a(9m)=%.4f P_a=%.4f 力臂=%.2f" % (KA, PATOP, PA, LARM))
    print("p_net=%.2f  D=%.5f  T=%.4f  c_crit=%.2f" % (PNET, DD, TT, C_CRIT))
    for cx in (45, 44, 43, 42, 41):
        print("  c=%4.1f p_net=%5.1f D=%6.2f" % (cx, 4*cx-162, solve_D(4*cx-162, PA*LARM)))
