# -*- coding: utf-8 -*-
"""SM-2019-4 圖解。本題為推導題、考卷未給任何數值，
   幾何與力多邊形以一組【示範參數】計算（圖上已明標「非考題數據」）；
   所有角度、力的大小與方向一律由本檔的試驗楔平衡解算，非硬寫座標。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
R = math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── 示範參數（非考題數據，考卷全題以符號表示）─────────────
H, TH, AL = 6.0, 10.0, 12.0        # 牆高（鉛直）、牆背與鉛直夾角 θ、背填坡角 α
GAM, C_, PHI, CA, DL = 18.0, 10.0, 28.0, 6.0, 18.0

# ── §4(一) 張力裂縫深度（與 α、θ、δ、c_a 皆無關，見 §5 證明）──
ZT = 2*C_/GAM*math.tan(R(45 + PHI/2))

A = (0.0, 0.0)
E = (-H*math.tan(R(TH)), H)
D = (E[0] + ZT*math.tan(R(TH)), E[1] - ZT)
L_AD = math.hypot(D[0]-A[0], D[1]-A[1])          # 牆面有效接觸長度


def wedge(beta):
    """回傳該試驗破壞面的 (P, R, W, C, Ca, B, F, |AB|)。"""
    ta = math.tan(R(AL)); cb, sb = math.cos(R(beta)), math.sin(R(beta))
    den = sb - ta*cb
    if den <= 1e-9: return None
    t = (E[1] - ZT - ta*E[0])/den                 # 破壞面與「地表下移 Z_t」線的交點
    if t <= 0: return None
    B = (t*cb, t*sb)
    F = (B[0], E[1] + ta*(B[0]-E[0]))
    poly = [A, B, F, E]; ar = 0.0
    for i in range(4):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % 4]
        ar += x1*y2 - x2*y1
    ar = abs(ar)/2.0
    W = GAM*ar
    L_AB = math.hypot(B[0]-A[0], B[1]-A[1])
    Cf = C_*L_AB; Cak = CA*L_AD
    Kx = Cf*cb - Cak*math.sin(R(TH))
    Ky = -W + Cf*sb + Cak*math.cos(R(TH))
    aR, aP = R(90 + beta - PHI), R(TH + DL)
    det = math.cos(aR)*math.sin(aP) - math.sin(aR)*math.cos(aP)
    Rr = (-Kx*math.sin(aP) + Ky*math.cos(aP))/det
    Pp = ( Kx*math.sin(aR) - Ky*math.cos(aR))/det
    return Pp, Rr, W, Cf, Cak, B, F, L_AB


BETAS = [AL + 0.5 + (89.0 - AL - 0.5)*i/4000.0 for i in range(4001)]
CURVE = [(b, wedge(b)) for b in BETAS]
CURVE = [(b, r) for b, r in CURVE if r]
BCR, RES = max(CURVE, key=lambda kv: kv[1][0])
PA, RR, WW, CC, CAK, BB, FF, LAB = RES

PW_, PH_ = 760, 660


# ══════════════════════════════════════════════════════════
# fig-1　幾何重繪：土楔 ABFE、有效面 AB 與 AD、裂縫區 DEFB
# ══════════════════════════════════════════════════════════
def fig1():
    xmin, xmax = -3.4, max(FF[0], BB[0]) + 2.6
    ymin, ymax = -1.5, FF[1] + 1.5
    L, Rm, T, Bm = 40, 40, 66, 128
    sx = min((PW_-L-Rm)/(xmax-xmin), (PH_-T-Bm)/(ymax-ymin))
    cv = Canvas(PW_, PH_, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="考卷附圖的向量重繪：土楔 A–B–F–E 與兩條有效面",
             sub="裂縫 DE、BF 不傳力；c 只作用在 AB，c_a 只作用在 AD")
    # 牆體
    cv.polygon([A, E, (E[0]-1.9, E[1]), (A[0]-2.5, 0.0)], "rgba(148,163,184,0.30)",
               C["member"], 2.4)
    cv.line((A[0]-2.8, 0), (max(FF[0], BB[0])+2.2, 0), C["muted"], 1.4, dash="6 4")
    # 土楔（含裂縫區）
    cv.polygon([A, BB, FF, E], "rgba(180,83,9,0.16)", "none")
    # 裂縫區 D-E-F-B
    cv.polygon([D, E, FF, BB], "rgba(220,38,38,0.16)", "none")
    cv.line((E[0], E[1]), (FF[0]+1.9, FF[1] + math.tan(R(AL))*1.9), C["muted"], 2.6)
    cv.line(D, BB, C["load"], 2.2, dash="9 6")
    cv.line(A, BB, C["accent"], 3.0)
    cv.line(A, E, C["member"], 3.0)
    cv.line(A, D, C["accent"], 4.2)
    cv.line(BB, FF, C["load"], 2.6)
    cv.line(E, D, C["load"], 3.4)
    for p, lab, dx, dy in ((A, "A", -16, 16), (BB, "B", 14, 14), (FF, "F", 14, -12),
                           (E, "E", -16, -12), (D, "D", -16, 14)):
        cv.dot(p, 5.2, fill=C["text"])
        cv.text_px(cv.X(p[0])+dx, cv.Y(p[1])+dy, lab, 15, C["text"], weight="700")
    # 角度標示
    cv.line(A, (A[0]+1.5, 0), C["dim"], 1.2, dash="4 3")
    cv.text_px(cv.X(A[0])+34, cv.Y(0)-13, "β", 15, C["accent"], weight="700")
    cv.line(E, (E[0], E[1]-1.5), C["dim"], 1.2, dash="4 3")
    cv.text_px(cv.X(E[0])+11, cv.Y(E[1]-0.95), "θ", 15, C["member"], weight="700")
    cv.line(FF, (FF[0]+1.7, FF[1]), C["dim"], 1.2, dash="4 3")
    cv.text_px(cv.X(FF[0])+38, cv.Y(FF[1])-14, "α", 15, C["muted"], weight="700")
    cv.dim((A[0]-2.75, 0), (A[0]-2.75, H), "H", off=0, color=C["dim"], size=14,
           label_off=-14)
    cv.line(E, (A[0]-2.95, E[1]), C["dim"], 1.0, dash="3 3")
    cv.dim((FF[0]+0.55, FF[1]), (FF[0]+0.55, BB[1]), "Z_t", off=0, color=C["load"],
           size=14, label_off=13)
    cv.text_px(cv.X((A[0]+BB[0])/2.0)+16, cv.Y((A[1]+BB[1])/2.0)+20,
               "AB：c 作用面", 12.5, C["accent"], weight="700")
    cv.text_px(cv.X((A[0]+D[0])/2.0)-13, cv.Y((A[1]+D[1])/2.0), "AD：c_a 作用面",
               12.5, C["accent"], anchor="end", weight="700")
    cv.text_px(cv.X((E[0]+FF[0])/2.0), cv.Y((E[1]+FF[1])/2.0)-26, "張力裂縫區（不傳力）",
               12.5, C["load"], weight="700")
    rows = ["示範參數（非考題數據）：H = %g m、θ = %g°、α = %g°、γ = %g kN/m³、"
            "c = %g、φ = %g°、c_a = %g、δ = %g°" % (H, TH, AL, GAM, C_, PHI, CA, DL),
            "Z_t = 2c/γ · tan(45° + φ/2) = %.3f m　（與 α、θ、δ、c_a 皆無關，證明見 §5）" % ZT,
            "臨界破壞面 β = %.2f°　⇒　W = %.1f、C = c·AB = %.1f、C_a = c_a·AD = %.1f kN/m"
            % (BCR, WW, CC, CAK)]
    for i, t in enumerate(rows):
        cv.text_px(PW_/2, PH_-104+i*26, t, 12.5,
                   C["load"] if i == 1 else C["muted"], weight="700" if i == 1 else "400")
    cv.save(os.path.join(OUT, "SM-2019-4-fig-1-geometry.svg"))


# ══════════════════════════════════════════════════════════
# fig-2　力多邊形（五力閉合）
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2 = 880, 780
    aW, aC, aCa = -90.0, BCR, 90.0 + TH
    aR_, aP_ = 90.0 + BCR - PHI, TH + DL
    seq = [("W", WW, aW, C["muted"]), ("C", CC, aC, C["accent"]),
           ("C_a", CAK, aCa, C["accent"]), ("R", RR, aR_, C["member"]),
           ("P", PA, aP_, C["load"])]
    pts = [(0.0, 0.0)]
    for _, m, a, _c in seq:
        x, y = pts[-1]
        pts.append((x + m*math.cos(R(a)), y + m*math.sin(R(a))))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    mx = (max(xs)-min(xs)) or 1; my = (max(ys)-min(ys)) or 1
    pad = 0.20*max(mx, my)
    xmin, xmax = min(xs)-pad*1.9, max(xs)+pad*2.6
    ymin, ymax = min(ys)-pad*1.4, max(ys)+pad*1.5
    L, Rm, T, Bm = 40, 40, 70, 214
    sx = min((W2-L-Rm)/(xmax-xmin), (H2-T-Bm)/(ymax-ymin))
    cv = Canvas(W2, H2, sx=sx, ox=L-xmin*sx, oy=Bm-ymin*sx, bg="#FFFFFF")
    cv.panel(title="力多邊形：五力首尾相連必須閉合",
             sub="W、C、C_a 大小方向已知先畫；R、P 只知方向，由兩條射線的交點定出")
    cv.polygon(pts[:-1] + [pts[-1]], "rgba(148,163,184,0.10)", "none")
    OFFS = {"W": 0.155, "C": 0.13, "C_a": 0.42, "R": 0.135, "P": 0.10}
    for i, (lab, m, a, col) in enumerate(seq):
        p0, p1 = pts[i], pts[i+1]
        cv.arrow(p0, p1, col, 3.6 if lab in ("R", "P") else 3.0, 11)
        mxp = ((p0[0]+p1[0])/2.0, (p0[1]+p1[1])/2.0)
        nx, ny = -(p1[1]-p0[1]), (p1[0]-p0[0])
        nl = math.hypot(nx, ny) or 1
        off = OFFS[lab]*max(mx, my)
        cv.text_px(cv.X(mxp[0]+nx/nl*off), cv.Y(mxp[1]+ny/nl*off),
                   "%s = %.1f" % (lab, m), 13, col, weight="700")
    cv.dot(pts[0], 6.0, fill=C["text"])
    cv.text_px(cv.X(pts[0][0])+13, cv.Y(pts[0][1])-16, "起點＝終點（閉合）", 12,
               C["text"], anchor="start", weight="700")
    hdr = ["力", "大小 (kN/m)", "與水平線夾角", "備註"]
    rows = [["W  自重", "%.1f" % WW, "−90°（鉛直向下）", "γ × 面積 ABFE，已知"],
            ["C  破壞面凝聚力", "%.1f" % CC, "%+.2f°（沿 AB 向上）" % aC, "c × AB，已知"],
            ["C_a 牆面附著力", "%.1f" % CAK, "%+.2f°（沿 AD 向上）" % aCa, "c_a × AD，已知"],
            ["R  破壞面反力", "%.1f" % RR, "%+.2f°（＝90°+β−φ）" % aR_, "只知方向，法線偏 φ"],
            ["P  牆背反力", "%.1f" % PA, "%+.2f°（＝θ+δ）" % aP_, "只知方向，法線偏 δ"]]
    x0 = 54; xs2 = [x0, x0+188, x0+300, x0+470]
    ytab = H2 - 176
    cv.rect_px(x0-12, ytab-24, 690, 28, "#ECEFF1", 6)
    for j, hcell in enumerate(hdr):
        cv.text_px(xs2[j], ytab-10, hcell, 12, C["text"], anchor="start", weight="700")
    for i, r in enumerate(rows):
        yy = ytab + 16 + i*25
        col = (C["muted"], C["accent"], C["accent"], C["member"], C["load"])[i]
        for j, cell in enumerate(r):
            cv.text_px(xs2[j], yy, cell, 11.5, col if j else C["text"], anchor="start",
                       weight="700" if j == 0 else "400")
    cv.text_px(W2/2, H2-22, "主動狀態土楔向下滑 ⇒ R 與 P 都由法線「往上游方向」偏轉；"
               "偏錯邊 P 會算成被動值", 12.5, C["load"], weight="700")
    cv.save(os.path.join(OUT, "SM-2019-4-fig-2-force-polygon.svg"))


# ══════════════════════════════════════════════════════════
# fig-3　P(β) 取極大值
# ══════════════════════════════════════════════════════════
def fig3():
    W3, H3 = 860, 620
    # 只畫 P 落在 [0.45 P_a, P_a] 的 β 視窗；β→α 時 P→∞，全畫會壓扁峰值
    cut = 0.45*PA
    win = [b for b, r in CURVE if r[0] >= cut]
    b0, b1 = max(AL+1.0, min(win)-3.0), min(88.0, max(win)+3.0)
    ps = [(b, min(r[0], PA*1.06)) for b, r in CURVE if b0 <= b <= b1]
    pmax = PA
    L, Rm, T, Bm = 78, 56, 74, 148
    Xp = lambda b: L + (b-b0)/(b1-b0)*(W3-L-Rm)
    Yp = lambda p: H3 - Bm - (p-0)/(pmax*1.12)*(H3-T-Bm)
    cv = Canvas(W3, H3, sx=1, bg="#FFFFFF")
    cv.panel(title="主動土壓力＝所有試驗楔中的「極大值」",
             sub="P(β) 由力多邊形逐一解出；被動狀態才取極小值，觀念不可顛倒")
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (L, Yp(0), W3-Rm, Yp(0), C["muted"]))
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8"/>'
                    % (L, Yp(0), L, T+6, C["muted"]))
    for b in range(20, 85, 10):
        if b0 <= b <= b1:
            cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                            'stroke-width="1.2"/>' % (Xp(b), Yp(0), Xp(b), Yp(0)+7, C["muted"]))
            cv.text_px(Xp(b), Yp(0)+22, "%d°" % b, 12, C["muted"])
    step = 20
    v = 0
    while v <= pmax*1.10:
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                        'stroke-width="1.1"/>' % (L, Yp(v), W3-Rm, Yp(v), C["border"]))
        cv.text_px(L-10, Yp(v), "%d" % v, 12, C["muted"], anchor="end")
        v += step
    cv.text_px((L+W3-Rm)/2, Yp(0)+50, "試驗破壞面傾角 β", 13.5, C["text"], weight="700")
    cv.text_px(L-4, T-2, "牆背反力 P (kN/m)", 13, C["text"], anchor="start")
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3.4" '
                    'stroke-linejoin="round"/>'
                    % (" ".join("%.2f,%.2f" % (Xp(b), Yp(p)) for b, p in ps), C["load"]))
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="1.6" stroke-dasharray="5 4"/>'
                    % (Xp(BCR), Yp(0), Xp(BCR), Yp(PA), C["load"]))
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="1.6" stroke-dasharray="5 4"/>'
                    % (L, Yp(PA), Xp(BCR), Yp(PA), C["load"]))
    cv.parts.append('<circle cx="%.1f" cy="%.1f" r="7.5" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.8"/>' % (Xp(BCR), Yp(PA), C["load"]))
    cv.text_px(Xp(BCR)-16, Yp(PA)-38, "P_a = max P(β) = %.1f kN/m" % PA, 14,
               C["load"], anchor="end", weight="700")
    cv.text_px(Xp(BCR)-16, Yp(PA)-16, "臨界破壞面 β = %.2f°" % BCR, 12.5, C["muted"],
               anchor="end")
    b_lo = [b for b, p in ps if b < BCR][0]
    b_hi = [b for b, p in ps if b > BCR][-1]
    for b in (b_lo + 6, b_hi - 6):
        p = [pp for bb, pp in ps if abs(bb-b) < 0.02][0]
        cv.parts.append('<circle cx="%.1f" cy="%.1f" r="4.6" fill="#FFFFFF" stroke="%s" '
                        'stroke-width="2.2"/>' % (Xp(b), Yp(p), C["muted"]))
        cv.text_px(Xp(b), Yp(p)+20, "β = %.0f°：%.1f" % (b, p), 11.5, C["muted"])
    rows = ["取太平（β 小）→ 土楔重但破壞面長，抗力也大；取太陡（β 大）→ 土楔太輕。"
            "兩端都低於臨界值。",
            "考場寫法：列出 P(β) 的表示式，說明對 β 微分令其為零（或作圖取峰值）即得 P_a。"]
    for i, t in enumerate(rows):
        cv.text_px(W3/2, H3-56+i*25, t, 12.5, C["muted"] if i == 0 else C["text"],
                   weight="400" if i == 0 else "700")
    cv.save(os.path.join(OUT, "SM-2019-4-fig-3-max-p.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(); fig2(); fig3()
    print("Zt=%.4f  β_cr=%.3f°  P=%.3f  R=%.3f  W=%.3f  C=%.3f  Ca=%.3f  |AB|=%.3f |AD|=%.3f"
          % (ZT, BCR, PA, RR, WW, CC, CAK, LAB, L_AD))
    # 閉合檢核：五力向量和應為零
    ang = [-90.0, BCR, 90.0+TH, 90.0+BCR-PHI, TH+DL]
    mag = [WW, CC, CAK, RR, PA]
    sx_ = sum(m*math.cos(R(a)) for m, a in zip(mag, ang))
    sy_ = sum(m*math.sin(R(a)) for m, a in zip(mag, ang))
    print("閉合檢核 ΣFx=%.2e  ΣFy=%.2e" % (sx_, sy_))
