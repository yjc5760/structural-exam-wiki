# -*- coding: utf-8 -*-
"""SM-2017-4 圖解：開挖三項穩定檢核（管湧／上舉／隆起）。
   所有數值由本檔依 SM-2017-4.md §4 的鑽探資料重算，未從文字複製。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── 鑽探柱狀（深度上界, 下界, 分類, γt tf/m³, N）──────────
LAYERS = [(0.00, 1.24, "ML",    1.82, 1),
          (1.24, 3.42, "ML-CL", 1.74, 2),
          (3.42, 7.85, "ML",    1.82, 3),
          (7.85, 10.32, "CL",   1.86, 4),
          (10.32, 16.50, "SM",  1.95, (14+12+14)/3.0)]
GW = 1.0                    # γw tf/m³
H_EXC = 8.0                 # 開挖深度
D_TIP = 14.0                # 版樁底
Z_CLSM = 10.32              # CL / SM 交界（上舉受壓面）
WT_D = 1.0                  # 設計地下水位
WT_M = 5.21                 # 鑽探實測地下水位
Q = 1.0                     # 地表超載 tf/m²
G_CL = 1.86

# ── (二) 管湧 ────────────────────────────────────────────
def piping(wt):
    Dout = D_TIP - wt
    Din = D_TIP - H_EXC
    L = Dout + Din
    dH = H_EXC - wt
    i = dH / L
    ic = (G_CL - GW) / GW
    return Dout, Din, L, dH, i, ic, ic / i

P_OUT, P_IN, P_L, P_DH, P_I, P_IC, P_FS = piping(WT_D)
M_OUT, M_IN, M_L, M_DH, M_I, M_IC, M_FS = piping(WT_M)

# ── (三) 上舉（土湧）───────────────────────────────────
HPLUG = Z_CLSM - H_EXC                   # 2.32 m
W_RES = G_CL * HPLUG                     # 4.3152 tf/m²
def uplift_FS(wt):
    return W_RES / (GW * (Z_CLSM - wt))
U_D = GW * (Z_CLSM - WT_D)               # 9.32
FS_UP_D = W_RES / U_D                    # 0.463
FS_UP_M = uplift_FS(WT_M)                # 0.844
WT_FS1 = Z_CLSM - W_RES / GW             # FS = 1 所需水位
WT_FS2 = Z_CLSM - (W_RES / 2.0) / GW     # FS = 2 所需水位

# ── (四) 隆起 ────────────────────────────────────────────
def overburden(z_to):
    s = 0.0
    for a, b, _, g, _ in LAYERS:
        lo, hi = max(a, 0.0), min(b, z_to)
        if hi > lo:
            s += (hi - lo) * g
    return s
SIGV = overburden(H_EXC)                 # 14.392 tf/m²
NC = math.pi + 2                         # 5.1416

N_SM = (14 + 12 + 14) / 3.0              # 13.333（S-7/S-8/S-9 逐點讀值）
T_CL = Z_CLSM - H_EXC                    # 2.32
T_SM = D_TIP - Z_CLSM                    # 3.68
N_AVG = (4 * T_CL + N_SM * T_SM) / (D_TIP - H_EXC)
SU_W = 10 * N_AVG / 16.0                 # 6.077
FS_HV_W = SU_W * NC / (SIGV + Q)         # 2.03
SU_CL = 10 * 4 / 16.0                    # 2.50
FS_HV_CL = SU_CL * NC / (SIGV + Q)       # 0.84
SU_FLAT = 10 * ((4*T_CL + 14*T_SM)/(D_TIP-H_EXC)) / 16.0   # 若 SM 一律取 N=14
FS_FLAT = SU_FLAT * NC / (SIGV + Q)


def _seg(cv, x0, y0, x1, y1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                    'stroke-width="%s" stroke-linecap="round"%s/>' % (x0, y0, x1, y1, col, w, d))


def _dot(cv, x, y, r, col):
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="%.1f" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.2"/>' % (x, y, r, col))


def _lab(cv, x, y, txt, size, col, anchor="start", weight="700"):
    w = sum((size*1.02) if ord(ch) > 0x2E80 else (size*0.56) for ch in txt)
    x0 = {"start": x-5, "middle": x-w/2-5, "end": x-w-5}[anchor]
    cv.rect_px(x0, y-size*0.78-3, w+10, size*1.56+6, "#FFFFFFE8", 5)
    cv.text_px(x, y, txt, size, col, anchor=anchor, weight=weight)


def _wt(cv, x, y, col):
    cv.polygon([(x-0.34, y), (x+0.34, y), (x, y-0.55)], "none", col, 2.0)
    cv.line((x-0.24, y-0.78), (x+0.24, y-0.78), col, 1.7)


# ══════════════════════════════════════════════════════════
# 圖一：剖面與三個檢核面
# ══════════════════════════════════════════════════════════
def fig1():
    W1, H1, ZT = 1340, 820, 16.6
    cv = Canvas(W1, H1, sx=38.0, ox=620, oy=68, bg=C["panel"])
    cv.panel()
    Yz = lambda z: (ZT - z)
    XLOG, XL, XR = -14.4, -9.4, 13.4     # 柱狀圖欄 / 地層左緣 / 右緣

    LC = {"ML": "rgba(180,83,9,0.13)", "ML-CL": "rgba(180,83,9,0.20)",
          "CL": "rgba(46,125,111,0.20)", "SM": "rgba(124,58,237,0.14)"}
    for a_, b_, cls, g, n in LAYERS:
        b_ = min(b_, ZT)
        cv.polygon([(XL, Yz(a_)), (XR, Yz(a_)), (XR, Yz(b_)), (XL, Yz(b_))], LC[cls])
        _seg(cv, cv.X(XLOG), cv.Y(Yz(a_)), cv.X(XR), cv.Y(Yz(a_)), C["border"], 1.2)
    # 開挖（右側 x>0，挖到 8 m）
    cv.polygon([(0.06, Yz(0)), (XR, Yz(0)), (XR, Yz(H_EXC)), (0.06, Yz(H_EXC))], "#FFFFFF")
    cv.line((0.06, Yz(H_EXC)), (XR, Yz(H_EXC)), C["member"], 2.6)
    cv.line((XL, Yz(0)), (0, Yz(0)), C["member"], 2.2)
    cv.line((0, Yz(0)), (0, Yz(D_TIP)), C["member"], 6.0)
    cv.text_px(cv.X(0)-10, cv.Y(Yz(D_TIP))+20, "鋼版樁底 GL−%.1f m" % D_TIP, 12,
               C["member"], anchor="end", weight="700")

    # ── 柱狀圖欄（左側獨立欄位，不與剖面重疊）──
    _seg(cv, cv.X(XL), cv.Y(Yz(0)), cv.X(XL), cv.Y(Yz(ZT)), C["border"], 1.4)
    for a_, b_, cls, g, n in LAYERS:
        b2 = min(b_, ZT)
        ym = cv.Y(Yz((a_+b2)/2))
        cv.text_px(cv.X(XLOG)+6, ym-9, "%s　GL−%.2f ~ −%.2f" % (cls, a_, b2), 11.5,
                   C["text"], anchor="start", weight="700")
        cv.text_px(cv.X(XLOG)+6, ym+10,
                   "γ_t = %.2f　N = %s" % (g, ("%.3f（S-7/8/9 平均）" % n) if cls == "SM" else "%g" % n),
                   11.5, C["muted"], anchor="start")

    # 水位
    _wt(cv, -8.2, Yz(WT_D), C["deform"])
    cv.line((XL, Yz(WT_D)), (0, Yz(WT_D)), C["deform"], 1.8, dash="7 5")
    cv.text_px(cv.X(-7.6), cv.Y(Yz(WT_D))-16, "設計水位 GL−%.1f m" % WT_D, 12,
               C["deform"], anchor="start", weight="700")
    cv.line((XL, Yz(WT_M)), (0, Yz(WT_M)), C["muted"], 1.5, dash="4 5")
    cv.text_px(cv.X(XL)+8, cv.Y(Yz(WT_M))-9, "（鑽探實測水位 GL−%.2f m）" % WT_M, 11,
               C["muted"], anchor="start")

    # 地表超載
    for k in range(5):
        x = -8.6 + k*1.9
        cv.arrow((x, Yz(-1.05)), (x, Yz(-0.12)), C["load"], 2.0, 8)
    cv.text_px(cv.X(-4.9), cv.Y(Yz(0))-34, "q = %.1f tf/m²" % Q, 12, C["load"],
               anchor="start", weight="700")

    # ── (二) 管湧：最高流線 ──
    cv.arrow((-0.45, Yz(WT_D)), (-0.45, Yz(D_TIP-0.3)), C["load"], 2.6, 9)
    cv.line((-0.45, Yz(D_TIP-0.3)), (0.45, Yz(D_TIP-0.3)), C["load"], 2.6)
    cv.arrow((0.45, Yz(D_TIP-0.3)), (0.45, Yz(H_EXC+0.2)), C["load"], 2.6, 9)
    cv.text_px(cv.X(-0.72), cv.Y(Yz(3.4)), "D_{out} = %.1f m" % P_OUT, 11.5,
               C["load"], anchor="end", weight="700")
    cv.text_px(cv.X(0.72), cv.Y(Yz(12.6)), "D_{in} = %.1f m" % P_IN, 11.5,
               C["load"], anchor="start", weight="700")

    # ── (三) 上舉：CL 覆土塞與受壓面 ──
    cv.polygon([(0.06, Yz(H_EXC)), (6.4, Yz(H_EXC)), (6.4, Yz(Z_CLSM)), (0.06, Yz(Z_CLSM))],
               "rgba(46,125,111,0.34)", C["bmd"], 2.2)
    cv.text_px(cv.X(3.2), cv.Y(Yz((H_EXC+Z_CLSM)/2))-9, "CL 覆土塞 %.2f m" % HPLUG,
               12, C["bmd"], weight="700")
    cv.text_px(cv.X(3.2), cv.Y(Yz((H_EXC+Z_CLSM)/2))+10,
               "W = %.2f × %.2f = %.3f tf/m²" % (G_CL, HPLUG, W_RES), 11.5, C["bmd"])
    for k in range(4):
        x = 0.9 + k*1.7
        cv.arrow((x, Yz(Z_CLSM+1.0)), (x, Yz(Z_CLSM+0.10)), C["load"], 2.0, 8)
    cv.line((0.06, Yz(Z_CLSM)), (XR, Yz(Z_CLSM)), C["load"], 2.2, dash="8 5")
    cv.text_px(cv.X(6.8), cv.Y(Yz(Z_CLSM))+18,
               "受壓面 GL−%.2f m（CL / SM 交界）" % Z_CLSM, 12, C["load"],
               anchor="start", weight="700")

    # ── (四) 隆起破壞面：以開挖面角點為圓心、半徑＝入土深度的圓弧 ──
    r_arc = D_TIP - H_EXC
    pts = [(r_arc*math.cos(math.radians(t)), Yz(H_EXC + r_arc*math.sin(math.radians(t))))
           for t in range(0, 181, 3)]
    cv.poly(pts, C["accent"], 2.8, dash="9 6")
    cv.line((-r_arc, Yz(H_EXC)), (-r_arc, Yz(0)), C["accent"], 2.8, dash="9 6")
    cv.text_px(cv.X(-5.75), cv.Y(Yz(4.2)), "隆起破壞面", 12.5, C["accent"],
               anchor="start", weight="700")
    cv.text_px(cv.X(-5.75), cv.Y(Yz(4.2))+19, "r = 入土深度 %.1f m" % r_arc, 11.5,
               C["accent"], anchor="start")
    cv.text_px(cv.X(-5.75), cv.Y(Yz(4.2))+37, "繞過壁底 ⇒ 穿過 SM 層", 11.5,
               C["accent"], anchor="start")

    # ── 三個檢核方塊（統一放在開挖空區）──
    boxes = [
        (0.4, C["load"],
         ["(二) 管湧　最高流線＝緊貼壁面的最短路徑",
          "L = %.1f + %.1f = %.1f m　ΔH = %.1f − %.1f = %.1f m" % (P_OUT, P_IN, P_L, H_EXC, WT_D, P_DH),
          "i = ΔH / L = %.4f　；　i_c = (γ_t − γ_w)/γ_w = %.2f" % (P_I, P_IC),
          "FS = i_c / i = %.2f　（安全）" % P_FS]),
        (3.0, C["bmd"],
         ["(三) 上舉（土湧）　受壓水頭由 GL−%.1f m 傳到 SM 層頂" % WT_D,
          "h_w = %.2f − %.1f = %.2f m　U = γ_w h_w = %.2f tf/m²" % (Z_CLSM, WT_D, Z_CLSM-WT_D, U_D),
          "FS = W / U = %.3f / %.2f = %.2f　（極不安全）" % (W_RES, U_D, FS_UP_D),
          "欲得 FS = 2，坑內水位須降到 GL−%.2f m" % WT_FS2]),
        (5.6, C["accent"],
         ["(四) 隆起　FS = S_u·N_c / (γH + q)，N_c = π + 2 = %.4f" % NC,
          "γH（GL 0 ~ %.1f m 逐層累加）= %.3f tf/m²" % (H_EXC, SIGV),
          "N_{avg} = (4×%.2f + %.3f×%.2f)/%.1f = %.3f" % (T_CL, N_SM, T_SM, D_TIP-H_EXC, N_AVG),
          "S_u = 10N/16 = %.3f tf/m²　⇒　FS = %.2f　（安全）" % (SU_W, FS_HV_W)]),
    ]
    for zt, col, lines in boxes:
        bx, by = cv.X(0.9), cv.Y(Yz(zt))
        cv.rect_px(bx, by-14, 424, 86, "#FFFFFFF2", 8, col, 1.5)
        for k, t in enumerate(lines):
            cv.text_px(bx+12, by+2+k*20, t, 12 if k else 12.5,
                       col if k in (0, 3) else C["text"], anchor="start",
                       weight="700" if k in (0, 3) else "400")

    cv.dim((XR-0.35, Yz(0)), (XR-0.35, Yz(H_EXC)), "H = 8.0 m", off=0, label_off=-46)
    cv.dim((XR-0.35, Yz(H_EXC)), (XR-0.35, Yz(D_TIP)), "D = 6.0 m", off=0, label_off=-46)
    return cv


# ══════════════════════════════════════════════════════════
# 圖二：上舉 FS 對坑內水位
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2 = 700, 560
    cv = Canvas(W2, H2, sx=1.0, ox=0, oy=0, bg=C["panel"])
    cv.panel("上舉安全係數對地下水位深度的敏感度",
             sub="抵抗力 W = γ_{CL} × H_{plug} = %.3f tf/m² 固定；上揚力隨水位深度而降" % W_RES)
    L, Rr, T, B = 96, 178, 104, 92
    xlo, xhi = 0.0, 10.32
    ylo, yhi = 0.0, 4.0
    Xp = lambda x: L + (x-xlo)/(xhi-xlo)*(W2-L-Rr)
    Yp = lambda y: (H2-B) - (y-ylo)/(yhi-ylo)*(H2-T-B)
    for yv in [0, 1, 2, 3, 4]:
        _seg(cv, Xp(xlo), Yp(yv), Xp(xhi), Yp(yv), C["border"], 1.0)
        cv.text_px(Xp(xlo)-9, Yp(yv), "%d" % yv, 11.5, C["muted"], anchor="end")
    for xv in [0, 2, 4, 6, 8, 10]:
        _seg(cv, Xp(xv), Yp(ylo), Xp(xv), Yp(ylo)+6, C["muted"], 1.4)
        cv.text_px(Xp(xv), Yp(ylo)+20, "%d" % xv, 11.5, C["muted"])
    _seg(cv, Xp(xlo), Yp(ylo), Xp(xhi), Yp(ylo), C["muted"], 1.8)
    _seg(cv, Xp(xlo), Yp(ylo), Xp(xlo), Yp(yhi), C["muted"], 1.8)

    # FS = 1 危險區底色
    cv.rect_px(Xp(xlo), Yp(1.0), Xp(xhi)-Xp(xlo), Yp(ylo)-Yp(1.0),
               "rgba(192,57,43,0.10)", 0)
    _seg(cv, Xp(xlo), Yp(1.0), Xp(xhi), Yp(1.0), C["load"], 2.0, dash="7 5")
    cv.text_px(Xp(xlo)+8, Yp(1.0)-12, "FS = 1（破壞界線）", 11.5, C["load"],
               anchor="start", weight="700")
    cv.text_px(Xp(9.9), Yp(0.28), "危險區：FS 小於 1", 11.5, C["load"],
               anchor="end", weight="700")

    pts = []
    n = 400
    for k in range(n+1):
        x = xlo + (xhi-0.06-xlo)*k/n
        y = uplift_FS(x)
        if y <= yhi:
            pts.append("%.2f,%.2f" % (Xp(x), Yp(y)))
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3.0" '
                    'stroke-linejoin="round"/>' % (" ".join(pts), C["deform"]))

    marks = [(WT_D, "設計水位 GL−1.0 m", C["load"], -14, -34, "end"),
             (WT_M, "實測水位 GL−5.21 m", C["muted"], -12, -52, "end"),
             (WT_FS1, "FS = 1 需降至 GL−%.2f m" % WT_FS1, C["accent"], 12, 22, "start"),
             (WT_FS2, "FS = 2 需降至 GL−%.2f m" % WT_FS2, C["bmd"], -12, -30, "end")]
    for xv, lab, col, dx, dy, an in marks:
        y = uplift_FS(xv)
        _dot(cv, Xp(xv), Yp(y), 5.6, col)
        cv.text_px(Xp(xv)+dx, Yp(y)+dy, lab, 11.5, col, anchor=an, weight="700")
        cv.text_px(Xp(xv)+dx, Yp(y)+dy+16, "FS = %.2f" % y, 11.5, col, anchor=an)

    cv.text_px((Xp(xlo)+Xp(xhi))/2, Yp(ylo)+46, "坑內地下水位深度 (GL− m)", 13, C["text"])
    cv.text_px(Xp(xlo)-52, T-14, "FS", 13, C["text"], anchor="start")
    cv.text_px(Xp(xhi)+14, T+6, "U = γ_w (%.2f − z_w)" % Z_CLSM, 11.5, C["deform"],
               anchor="start", weight="700")
    cv.text_px(Xp(xhi)+14, T+26, "z_w → %.2f m 時 U → 0" % Z_CLSM, 11, C["muted"],
               anchor="start")
    cv.text_px(Xp(xhi)+14, T+58, "重點：即使採用最寬鬆", 11, C["load"], anchor="start")
    cv.text_px(Xp(xhi)+14, T+76, "的實測水位，FS 仍 小於 1", 11, C["load"],
               anchor="start", weight="700")
    cv.text_px(Xp(xhi)+14, T+94, "⇒ 開挖前必須先降", 11, C["muted"], anchor="start")
    cv.text_px(Xp(xhi)+14, T+112, "　 SM 層受壓水頭", 11, C["muted"], anchor="start")
    return cv


# ══════════════════════════════════════════════════════════
# 圖三：S_u 取用範圍之爭
# ══════════════════════════════════════════════════════════
def fig3():
    W3, H3, ZT = 680, 600, 15.0

    def panel(su, fs, title, sub, arc_deep, col, rng):
        cv = Canvas(W3, H3, sx=19.0, ox=340, oy=187, bg=C["panel"])
        cv.panel(title, sub=sub)
        Yz = lambda z: (ZT - z)
        XL, XR = -8.6, 8.6
        LC = {"ML": "rgba(180,83,9,0.13)", "ML-CL": "rgba(180,83,9,0.20)",
              "CL": "rgba(46,125,111,0.20)", "SM": "rgba(124,58,237,0.14)"}
        for a_, b_, cls, g, n in LAYERS:
            b2 = min(b_, ZT)
            if b2 <= a_:
                continue
            cv.polygon([(XL, Yz(a_)), (XR, Yz(a_)), (XR, Yz(b2)), (XL, Yz(b2))], LC[cls])
        cv.polygon([(0.05, Yz(0)), (XR, Yz(0)), (XR, Yz(H_EXC)), (0.05, Yz(H_EXC))], "#FFFFFF")
        cv.line((XL, Yz(0)), (0, Yz(0)), C["member"], 2.0)
        cv.line((0.05, Yz(H_EXC)), (XR, Yz(H_EXC)), C["member"], 2.4)
        cv.line((0, Yz(0)), (0, Yz(D_TIP)), C["member"], 5.0)
        cv.line((XL, Yz(Z_CLSM)), (XR, Yz(Z_CLSM)), C["muted"], 1.3, dash="6 4")
        _lab(cv, cv.X(-2.6), cv.Y(Yz(Z_CLSM))+13, "CL / SM 交界 GL−%.2f m" % Z_CLSM, 10.5,
             C["muted"], weight="400")
        cv.text_px(cv.X(XL)+4, cv.Y(Yz(0))-11, "GL±0", 10.5, C["muted"], anchor="start")
        _lab(cv, cv.X(XL)+4, cv.Y(Yz(H_EXC))-12, "開挖面 GL−8.0 m", 10.5, C["member"])
        _lab(cv, cv.X(0)-8, cv.Y(Yz(D_TIP))+17, "壁底 GL−14.0 m", 10.5, C["member"],
             anchor="end")
        _lab(cv, cv.X(XL)+4, cv.Y(Yz(9.3)), "CL　N = 4", 11, C["bmd"])
        _lab(cv, cv.X(XL)+4, cv.Y(Yz(12.4)), "SM　N = %.2f" % N_SM, 11, C["sfd"])

        z0, z1 = rng
        # S_u 取用範圍：右側縱向括號
        xb = XR - 0.9
        cv.line((xb, Yz(z0)), (xb, Yz(z1)), col, 2.4)
        cv.line((xb-0.35, Yz(z0)), (xb+0.35, Yz(z0)), col, 2.4)
        cv.line((xb-0.35, Yz(z1)), (xb+0.35, Yz(z1)), col, 2.4)
        cv.text_px(cv.X(xb)+12, cv.Y(Yz((z0+z1)/2))-9, "S_u 取用範圍", 11, col,
                   anchor="start", weight="700")
        cv.text_px(cv.X(xb)+12, cv.Y(Yz((z0+z1)/2))+9, "GL−%.1f ~ −%.2f m" % (z0, z1), 11,
                   col, anchor="start")

        # 破壞面
        if arc_deep:
            r = D_TIP - H_EXC
            pts = [(r*math.cos(math.radians(t)), Yz(H_EXC + r*math.sin(math.radians(t))))
                   for t in range(0, 181, 4)]
            cv.poly(pts, col, 2.6, dash="8 5")
            cv.line((-r, Yz(H_EXC)), (-r, Yz(0)), col, 2.6, dash="8 5")
        else:
            r = (Z_CLSM - H_EXC)
            pts = [(r*math.cos(math.radians(t)), Yz(H_EXC + r*math.sin(math.radians(t))))
                   for t in range(0, 181, 4)]
            cv.poly(pts, col, 2.6, dash="8 5")
            cv.line((-r, Yz(H_EXC)), (-r, Yz(0)), col, 2.6, dash="8 5")
        _lab(cv, cv.X(-r)-8, cv.Y(Yz(3.2)), "破壞面", 11.5, col, anchor="end")

        yb = H3 - 128
        _seg(cv, 46, yb, W3-46, yb, C["border"], 1.3)
        cv.text_px(W3/2, yb+28, "S_u = %.2f tf/m²" % su, 14.5, col, weight="700")
        cv.text_px(W3/2, yb+54, "FS = %.2f × %.4f / (%.3f + %.1f) = %.2f"
                   % (su, NC, SIGV, Q, fs), 12.5, C["text"])
        cv.text_px(W3/2, yb+82, "⇒ %s" % ("安全（大於 1.2）" if fs >= 1.2 else "不安全（FS 小於 1）"),
                   13.5, col, weight="700")
        return cv

    a = panel(SU_CL, FS_HV_CL, "(a) 破壞面只在 CL 薄層內",
              "壁體剛度不足、坑底先破壞時的下限", False, C["load"], (H_EXC, Z_CLSM))
    b = panel(SU_W, FS_HV_W, "(b) 破壞面繞過壁底（本解）",
              "GL−8 ~ −14 m 依厚度加權平均 N 值", True, C["bmd"], (H_EXC, D_TIP))
    return [a, b]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    compose([fig1()], title="SM-2017-4　開挖三項穩定檢核：管湧、上舉（土湧）、隆起",
            sub="設計水位 GL−1.0 m、開挖 GL−8.0 m、版樁底 GL−14.0 m、q = 1.0 tf/m²",
            note="三個檢核用的是三個不同的面：管湧沿壁面、上舉在 CL/SM 交界、隆起繞過壁底。",
            path=os.path.join(OUT, "SM-2017-4-fig-1-section.svg"))
    compose([fig2()], title="SM-2017-4　上舉破壞：安全係數對坑內水位",
            sub="FS = W / U = %.3f / [γw × (%.2f − zw)]，zw 為坑內地下水位深度" % (W_RES, Z_CLSM),
            note="降水目標 GL−%.2f m 是由 FS = 2 反推，不是任意取的整數。" % WT_FS2,
            path=os.path.join(OUT, "SM-2017-4-fig-2-uplift.svg"))
    compose(fig3(), title="SM-2017-4　隆起的爭議：Su 取用範圍決定結論",
            sub="γH = %.3f tf/m²、q = %.1f tf/m²、Nc = π + 2 = %.4f 三者都相同" % (SIGV, Q, NC),
            note="同一題、同一組鑽探資料，只因 Su 取用範圍不同，FS 由 %.2f 變成 %.2f。"
                 % (FS_HV_CL, FS_HV_W),
            cols=2, path=os.path.join(OUT, "SM-2017-4-fig-3-su-range.svg"))
    print("(二) L=%.1f dH=%.1f i=%.4f ic=%.2f FS=%.3f" % (P_L, P_DH, P_I, P_IC, P_FS))
    print("    實測水位 L=%.2f dH=%.2f i=%.3f FS=%.2f" % (M_L, M_DH, M_I, M_FS))
    print("(三) Hplug=%.2f W=%.4f U=%.2f FS=%.3f | FS=1 @ %.3f m, FS=2 @ %.4f m, 實測 FS=%.3f"
          % (HPLUG, W_RES, U_D, FS_UP_D, WT_FS1, WT_FS2, FS_UP_M))
    print("(四) γH=%.3f Nc=%.4f N_SM=%.3f N_avg=%.3f Su=%.3f FS=%.3f"
          % (SIGV, NC, N_SM, N_AVG, SU_W, FS_HV_W))
    print("     只取 CL：Su=%.2f FS=%.3f ；SM 一律 N=14：Su=%.3f FS=%.3f"
          % (SU_CL, FS_HV_CL, SU_FLAT, FS_FLAT))
