# -*- coding: utf-8 -*-
"""SM-2022-4 圖解：懸臂式鋼板樁的淨壓力分布與四次式求根。
   所有數字由本檔依 SM-2022-4.md §4 重算，未從文字複製。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose

R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── 題給參數 ────────────────────────────────────────────
G, GSAT, GW, PHI = 16.5, 19.3, 9.81, 38.0
L1, L2 = 3.0, 6.0                      # 水位以上、水位至開挖面
GP = GSAT - GW                         # γ' = 9.49
KA_EX = math.tan(R(45 - PHI/2))**2     # 0.237943
KP_EX = math.tan(R(45 + PHI/2))**2     # 4.204036
# 全程用未捨入的 K 值計算（.md 內文所寫的 0.2379 / 4.2037 僅為顯示用近似）
KA, KP = KA_EX, KP_EX
DK = KP - KA
PA2 = G*L1*KA                          # 水位處主動土壓 11.776
SV9 = G*L1 + GP*L2                     # 106.44
PA3 = SV9*KA                           # 開挖面主動土壓 25.322
RATE = GP*DK                           # 37.635
L3 = PA3/RATE                          # 0.6728

# 合力與力臂（對零淨壓力點取矩）
P1, Z1 = 0.5*L1*PA2, L2 + L3 + L1/3.0
P2a, Z2a = PA2*L2, L3 + L2/2.0
P2b, Z2b = 0.5*L2*(PA3-PA2), L3 + L2/3.0
P3, Z3 = 0.5*L3*PA3, (2.0/3)*L3
PT = P1 + P2a + P2b + P3               # 137.476
MT = P1*Z1 + P2a*Z2a + P2b*Z2b + P3*Z3
ZB = MT/PT                             # 3.6914

# 四次式常數
A1 = (SV9*KP + GP*L3*DK)/RATE
A2 = 8*PT/RATE
A3 = 6*PT*(RATE*(2*ZB + L3) + SV9*KP)/RATE**2
A4 = PT*(6*ZB*SV9*KP + 6*ZB*GP*L3*DK + 4*PT)/RATE**2

def f(x):
    return x**4 + A1*x**3 - A2*x**2 - A3*x - A4

def bisect(lo, hi, n=200):
    for _ in range(n):
        m = 0.5*(lo+hi)
        if f(lo)*f(m) <= 0: hi = m
        else: lo = m
    return 0.5*(lo+hi)

L4 = bisect(1.0, 20.0)                 # 6.4516
DL = L3 + L4                           # 7.1244

# ══════════════════════════════════════════════════════════
# 圖一：淨壓力分布（A-C-D-E-F-G-B）
# ══════════════════════════════════════════════════════════
def fig1():
    W1, H1 = 1240, 820
    PSC = 0.075                        # 1 kPa = 0.075 繪圖公尺（等向縮放必需）
    Pq = lambda q: q*PSC
    ZTOT = L1 + L2 + DL
    cv = Canvas(W1, H1, sx=40.0, ox=320, oy=100, bg=C["panel"])
    Yz = lambda z: (ZTOT - z)          # 深度 → 模型 y（向上為正）
    cv.panel()

    XG, XR = -6.4, 19.6
    # 土層底色（牆左側為原地層；右側 z<9 已開挖）
    cv.polygon([(XG, Yz(0)), (XR, Yz(0)), (XR, Yz(L1)), (XG, Yz(L1))],
               "rgba(180,83,9,0.10)")
    cv.polygon([(XG, Yz(L1)), (XR, Yz(L1)), (XR, Yz(L1+L2)), (XG, Yz(L1+L2))],
               "rgba(29,78,216,0.07)")
    cv.polygon([(XG, Yz(L1+L2)), (XR, Yz(L1+L2)), (XR, Yz(ZTOT)), (XG, Yz(ZTOT))],
               "rgba(107,118,132,0.12)")
    for z in (0, L1, L1+L2):
        cv.line((XG, Yz(z)), (XR, Yz(z)), C["muted"], 1.6)

    # 開挖（牆右側、開挖面以上挖除）
    cv.polygon([(0.05, Yz(L1+L2)), (XR, Yz(L1+L2)), (XR, Yz(0)), (0.05, Yz(0))],
               "#FFFFFF", "none")
    cv.polygon([(0.05, Yz(L1+L2)), (XR, Yz(L1+L2)), (XR, Yz(L1)), (0.05, Yz(L1))],
               "rgba(29,78,216,0.10)")
    cv.line((0.05, Yz(L1+L2)), (XR, Yz(L1+L2)), C["member"], 2.6)

    # 鋼板樁
    cv.line((0, Yz(0)), (0, Yz(ZTOT)), C["member"], 5.4)

    # 水位符號（兩側同高，皆在 z = 3 m）
    for xw in (-4.6, 3.0):
        yw = Yz(L1)
        cv.polygon([(xw-0.30, yw), (xw+0.30, yw), (xw, yw-0.46)], "none", C["deform"], 2.0)
        cv.line((xw-0.21, yw-0.64), (xw+0.21, yw-0.64), C["deform"], 1.7)
    cv.text_px(cv.X(3.0)+22, cv.Y(Yz(L1))-4, "兩側水位同高 ⇒ 靜水壓抵銷", 12,
               C["deform"], anchor="start", weight="700")

    # ── 主動側（左）：A(0) – C – D – E ──
    cv.polygon([(0, Yz(0)), (-Pq(PA2), Yz(L1)), (-Pq(PA3), Yz(L1+L2)),
                (0, Yz(L1+L2+L3))], "rgba(192,57,43,0.24)", C["load"], 2.4)
    for k in range(7):
        z = (L1+L2)*(k+0.5)/7.0
        q = PA2*z/L1 if z <= L1 else PA2 + (PA3-PA2)*(z-L1)/L2
        cv.arrow((-Pq(q), Yz(z)), (-0.04, Yz(z)), C["load"], 1.5, 6)

    # ── 淨被動側（右）：E 之下線性增加，斜率 γ′(Kp−Ka) ──
    pb = RATE*L4
    cv.polygon([(0, Yz(L1+L2+L3)), (Pq(pb), Yz(ZTOT)), (0, Yz(ZTOT))],
               "rgba(29,78,216,0.22)", C["deform"], 2.4)
    for k in range(5):
        z = (L1+L2+L3) + L4*(k+0.6)/5.0
        cv.arrow((Pq(RATE*(z-L1-L2-L3)), Yz(z)), (0.04, Yz(z)), C["deform"], 1.5, 6)

    # 節點
    def node(x, z, lab, col, dx=0, dy=0, an="start"):
        cv.dot((x, Yz(z)), 4.8, fill=col)
        cv.text_px(cv.X(x)+dx, cv.Y(Yz(z))+dy, lab, 12.5, col, anchor=an, weight="700")
    node(0, 0, "A", C["load"], -12, -8, "end")
    node(-Pq(PA2), L1, "C　p_{a2} = %.3f kPa" % PA2, C["load"], -12, -8, "end")
    node(-Pq(PA3), L1+L2, "D　p_{a3} = %.3f kPa" % PA3, C["load"], -12, 16, "end")
    node(0, L1+L2+L3, "E", C["accent"], -14, 12, "end")
    node(Pq(pb), ZTOT, "F　%.1f kPa" % pb, C["deform"], 12, 0, "start")

    # E 點與 L3
    cv.text_px(cv.X(0.7), cv.Y(Yz(L1+L2+L3))-4,
               "E：淨壓力 = 0，L_3 = p_{a3} / [γ′(K_p − K_a)] = %.4f m" % L3,
               12.5, C["accent"], anchor="start", weight="700")
    cv.line((0.35, Yz(L1+L2)), (0.35, Yz(L1+L2+L3)), C["accent"], 2.4)

    # 合力 P 與力臂 z_c（對 E 取）
    zbar_depth = (L1+L2+L3) - ZB
    cv.dot((-Pq(PA3*0.52), Yz(zbar_depth)), 6.6, fill=C["load"])
    cv.text_px(cv.X(-2.35), cv.Y(Yz(zbar_depth))-10,
               "P = %.3f kN/m" % PT, 13.5, C["load"], anchor="end", weight="700")
    cv.text_px(cv.X(-2.35), cv.Y(Yz(zbar_depth))+11,
               "z_c = %.4f m（距 E）" % ZB, 12, C["muted"], anchor="end")
    cv.line((-2.30, Yz(zbar_depth)), (-Pq(PA3*0.52)-0.06, Yz(zbar_depth)),
            C["load"], 1.3, dash="4 3")
    cv.line((-Pq(PA3*0.52), Yz(zbar_depth)), (-Pq(PA3*0.52), Yz(L1+L2+L3)),
            C["load"], 1.5, dash="5 4")

    # 深度尺寸鏈
    cv.dim((XG+0.45, Yz(0)), (XG+0.45, Yz(L1)), "L1 = 3 m", off=0)
    cv.dim((XG+0.45, Yz(L1)), (XG+0.45, Yz(L1+L2)), "L2 = 6 m", off=0)
    cv.dim((XG+0.45, Yz(L1+L2)), (XG+0.45, Yz(ZTOT)), "DL = 7.12 m", off=0)

    # 參數說明（放在開挖側空白處）
    tx = 6.6
    cv.text_px(cv.X(tx), cv.Y(Yz(1.0)), "砂土：γ = 16.5 kN/m³、φ = 38°", 13,
               C["accent"], anchor="start", weight="700")
    cv.text_px(cv.X(tx), cv.Y(Yz(1.0))+22,
               "K_a = tan²(45° − φ/2) = %.4f" % KA, 12, C["muted"], anchor="start")
    cv.text_px(cv.X(tx), cv.Y(Yz(1.0))+42,
               "K_p = tan²(45° + φ/2) = %.4f" % KP, 12, C["muted"], anchor="start")
    cv.text_px(cv.X(tx), cv.Y(Yz(1.0))+62,
               "K_p − K_a = %.4f" % DK, 12, C["muted"], anchor="start")
    cv.text_px(cv.X(tx), cv.Y(Yz(4.6)), "水面下：γ_{sat} = 19.3 ⇒ γ′ = %.2f kN/m³" % GP,
               13, C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(tx), cv.Y(Yz(4.6))+22,
               "淨壓力變化率 γ′(K_p − K_a) = %.3f kPa/m" % RATE, 12,
               C["muted"], anchor="start")
    cv.text_px(cv.X(tx), cv.Y(Yz(7.4)), "開挖面（坑內）", 12.5, C["member"],
               anchor="start", weight="700")
    cv.text_px(cv.X(tx), cv.Y(Yz(11.6)), "壓力縮尺：1 kPa = %.3f m（與深度同一比例）" % PSC,
               11.5, C["muted"], anchor="start")

    return cv


# ══════════════════════════════════════════════════════════
# 圖二：四次式求根 + D_L 對安全係數的放大
# ══════════════════════════════════════════════════════════
def _seg(cv, x0, y0, x1, y1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                    'stroke-width="%s" stroke-linecap="round"%s/>' % (x0, y0, x1, y1, col, w, d))


def _dot(cv, x, y, r, col):
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="%.1f" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.2"/>' % (x, y, r, col))


def fig2():
    W2, H2 = 620, 560

    # ── (a) f(L4) 勘根曲線 ──
    xlo, xhi = 5.8, 7.0
    ylo, yhi = -700.0, 400.0
    ca = Canvas(W2, H2, sx=1.0, ox=0, oy=0, bg=C["panel"])
    ca.panel("(a) 四次式勘根：f 由負轉正只有一個正實根")
    L, Rr, T, B = 96, 42, 108, 96
    Xp = lambda x: L + (x-xlo)/(xhi-xlo)*(W2-L-Rr)
    Yp = lambda y: (H2-B) - (y-ylo)/(yhi-ylo)*(H2-T-B)
    for yv in range(-600, 401, 200):
        _seg(ca, Xp(xlo), Yp(yv), Xp(xhi), Yp(yv), C["border"], 1.0)
        ca.text_px(Xp(xlo)-9, Yp(yv), "%d" % yv, 11.5, C["muted"], anchor="end")
    _seg(ca, Xp(xlo), Yp(0), Xp(xhi), Yp(0), C["muted"], 2.0)
    _seg(ca, Xp(xlo), Yp(yhi), Xp(xlo), Yp(ylo), C["muted"], 1.8)
    for xv in [5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0]:
        _seg(ca, Xp(xv), Yp(ylo), Xp(xv), Yp(ylo)+6, C["muted"], 1.4)
        ca.text_px(Xp(xv), Yp(ylo)+20, "%.1f" % xv, 11.5, C["muted"])

    pts, n = [], 320
    for i in range(n+1):
        x = xlo + (xhi-xlo)*i/n
        y = f(x)
        if ylo <= y <= yhi:
            pts.append("%.2f,%.2f" % (Xp(x), Yp(y)))
    ca.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3.0" '
                    'stroke-linejoin="round"/>' % (" ".join(pts), C["load"]))

    # 勘根點（與 .md 表格同一組試算值）
    for xv, dx, dy in [(6.30, -14, 6), (6.40, -14, 6), (6.45, -14, 6), (6.50, 14, 4)]:
        _dot(ca, Xp(xv), Yp(f(xv)), 4.6, C["muted"])
        ca.text_px(Xp(xv)+dx, Yp(f(xv))+dy, "f(%.2f) = %+.2f" % (xv, f(xv)), 11,
                   C["muted"], anchor=("end" if dx < 0 else "start"))
    _dot(ca, Xp(L4), Yp(0), 6.6, C["load"])
    _seg(ca, Xp(L4), Yp(0), Xp(L4), Yp(ylo), C["load"], 1.6, dash="6 4")
    ca.text_px(Xp(L4)+12, Yp(ylo)-46, "L_4 = %.4f m" % L4, 13.5, C["load"],
               anchor="start", weight="700")
    ca.text_px(Xp(L4)+12, Yp(ylo)-26, "（f 在此由負變正）", 11.5, C["muted"], anchor="start")
    ca.text_px((Xp(xlo)+Xp(xhi))/2, Yp(ylo)+46, "試算深度 L_4 (m)", 13, C["text"])
    ca.text_px(Xp(xlo)-52, T-16, "f(L_4)", 13, C["text"], anchor="start")
    ca.text_px(Xp(xlo)-2, T-16,
               "f = L_4⁴ + %.3f L_4³ − %.3f L_4² − %.2f L_4 − %.2f" % (A1, A2, A3, A4),
               11.5, C["muted"], anchor="start")

    # ── (b) 臨界深度 ≠ 設計深度 ──
    cb = Canvas(W2, H2, sx=1.0, ox=0, oy=0, bg=C["panel"])
    cb.panel("(b) 臨界深度 ≠ 設計深度")
    DLS = round(L3, 4) + round(L4, 4)
    cb.text_px(W2/2, 92, "D_L = L_3 + L_4 = %.4f + %.4f = %.4f m"
               % (round(L3, 4), round(L4, 4), DLS), 14.5, C["load"], weight="700")
    cb.text_px(W2/2, 116, "（FS = 1.0 的臨界深度，不可直接施工）", 12, C["muted"])

    rows = [("×1.0（理論臨界）", DLS, C["load"], "剛好不倒，任何施工誤差都失敗"),
            ("×1.2（下限）", DLS*1.2, C["member"], "常用最小設計倍數"),
            ("×1.4（上限）", DLS*1.4, C["deform"], "軟弱或水位不確定時採用")]
    y0, barx, barw = 176, 160, 268
    smax = DLS*1.4
    for i, (lab, v, col, note) in enumerate(rows):
        y = y0 + i*96
        cb.text_px(barx-12, y, lab, 12.5, col, anchor="end", weight="700")
        cb.rect_px(barx, y-13, barw*v/smax, 26, col, 5)
        cb.text_px(barx + barw*v/smax + 10, y, "%.2f m" % v, 13, col,
                   anchor="start", weight="700")
        cb.text_px(barx, y+30, note, 11.5, C["muted"], anchor="start")
    yb = y0 + 3*96 - 6
    _seg(cb, 60, yb, W2-60, yb, C["border"], 1.4)
    cb.text_px(W2/2, yb+30, "設計貫入深度約 8.6 ~ 10.0 m　⇒　總樁長約 18 m", 13,
               C["text"], weight="700")
    cb.text_px(W2/2, yb+54, "等效做法：先把 K_p 除以 FS = 1.5 ~ 2.0 再重解四次式", 11.5,
               C["muted"])

    return [ca, cb]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    c1 = fig1()
    compose([c1], title="SM-2022-4　懸臂式鋼板樁：淨土壓力分布與零淨壓力點",
            sub="γ = 16.5、γ_sat = 19.3、φ = 38°；L1 = 3 m、L2 = 6 m",
            note="陷阱：零淨壓力點 E 不在開挖面上，而在其下 %.4f m；合力 P 與力臂 z_c 都要對 E 取。" % L3,
            path=os.path.join(OUT, "SM-2022-4-fig-1-net-pressure.svg"))
    compose(fig2(), title="SM-2022-4　四次式求根與設計貫入深度",
            sub="f(L4) = L4⁴ + A1·L4³ − A2·L4² − A3·L4 − A4 = 0，只取正實根",
            note="陷阱：L3 必須用未進位的 %.4f 相加；若先取 0.673 再相加會得 7.13，與正解差一個進位。" % L3,
            cols=2, path=os.path.join(OUT, "SM-2022-4-fig-2-quartic.svg"))
    print("Ka(exact)=%.6f Kp(exact)=%.6f ; 圖用 Ka=%.4f Kp=%.4f  γ'=%.2f  rate=%.4f"
          % (KA_EX, KP_EX, KA, KP, GP, RATE))
    print("p_a2=%.3f p_a3=%.3f  L3=%.4f" % (PA2, PA3, L3))
    print("P=%.3f  M=%.3f  zbar=%.4f" % (PT, MT, ZB))
    print("A1=%.3f A2=%.3f A3=%.2f A4=%.2f" % (A1, A2, A3, A4))
    for xv in (6.30, 6.40, 6.45, 6.4516, 6.50):
        print("  f(%.4f) = %+.2f" % (xv, f(xv)))
    print("L4=%.4f  DL=%.4f" % (L4, DL))
    print("P1=%.3f z1=%.4f | P2a=%.3f z2a=%.4f | P2b=%.3f z2b=%.4f | P3=%.3f z3=%.4f"
          % (P1, Z1, P2a, Z2a, P2b, Z2b, P3, Z3))
    print("M項 = %.3f %.3f %.3f %.3f ; σv9=%.2f ; σv9*Kp=%.3f ; γ'L3ΔK=%.3f ; rate²=%.2f"
          % (P1*Z1, P2a*Z2a, P2b*Z2b, P3*Z3, SV9, SV9*KP, GP*L3*DK, RATE**2))
    print("A3 括號 = %.2f ; A4 括號 = %.2f"
          % (RATE*(2*ZB+L3) + SV9*KP,
             6*ZB*SV9*KP + 6*ZB*GP*L3*DK + 4*PT))
