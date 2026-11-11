# -*- coding: utf-8 -*-
"""SM-2018-2 圖解。所有數值由本檔依 SM-2018-2.md §3.5 的 L1 輸入重算，非硬寫座標。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）───────────────────────────────────────────────
S3_1, DSD_1, UF_1, S3_2 = 100.0, 85.0, 67.0, 250.0
# ── L2（§4）────────────────────────────────────────────────
S1_1  = S3_1 + DSD_1                       # 185
PHICU = D(math.asin(DSD_1/(S1_1+S3_1)))    # 17.35°
S3P_1, S1P_1 = S3_1-UF_1, S1_1-UF_1        # 33, 118
PHIP  = D(math.asin((S1P_1-S3P_1)/(S1P_1+S3P_1)))   # 34.26°
THETA = 45.0 + PHIP/2.0                    # 62.13°
THETA_WRONG = 45.0 + PHICU/2.0             # 53.68°（誤用 φcu）
AF    = UF_1/DSD_1                         # 0.788
DSD_2 = S3_2 * DSD_1/S3_1                  # 212.5
S1_2  = S3_2 + DSD_2                       # 462.5
UF_2  = AF * DSD_2                         # 167.5
S3P_2, S1P_2 = S3_2-UF_2, S1_2-UF_2        # 82.5, 295
PHIP_2 = D(math.asin((S1P_2-S3P_2)/(S1P_2+S3P_2)))

def circ(cv, s3, s1, col, fill="none", w=2.6):
    cen, r = (s1+s3)/2.0, (s1-s3)/2.0
    cv.circle((cen, 0), r, fill=fill, stroke=col, w=w)
    cv.dot((cen, 0), 3.6, fill=col)
    for v in (s3, s1): cv.dot((v, 0), 4.4, fill=col)
    return cen, r

def tangent(cv, s3, s1, phi, col):
    """過原點包絡線的切點（c = 0）"""
    cen, r = (s1+s3)/2.0, (s1-s3)/2.0
    a = Rad(90.0+phi)
    p = (cen + r*math.cos(a), r*math.sin(a))
    cv.dot(p, 5.2, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    return p

# ══════════════════════════════════════════════════════════
# fig-1　同一試體的總應力圓與有效應力圓（相差 u_f）＋破壞面傾角
# ══════════════════════════════════════════════════════════
PW, PH = 700, 640

def panel_two_circles():
    xmin, xmax, ymin, ymax = -20.0, 235.0, -95.0, 170.0
    L, R, T, B = 56, 40, 66, 44
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="(二) 同一組試驗數據、兩個莫爾圓",
             sub="兩圓半徑相同（= S_u = 42.5），水平相距 u_f = %g kPa" % UF_1)
    cv.line((xmin+4, 0), (xmax-4, 0), C["muted"], 1.6)
    cv.line((0, ymin+6), (0, ymax-6), C["muted"], 1.6)
    cv.math_px(cv.X(xmax-4)-2, cv.Y(0)+20, "σ (kPa)", 12.5, C["muted"], anchor="end")
    cv.math_px(cv.X(0)+8, cv.Y(ymax-6)+3, "τ (kPa)", 12.5, C["muted"], anchor="start")
    # 兩條過原點的包絡線（NC 黏土 c = 0）
    for phi, col, lab in ((PHICU, C["member2"], "總應力包絡線  φ_{cu} = %.2f°" % PHICU),
                          (PHIP,  C["load"],    "有效應力包絡線  φ' = %.2f°" % PHIP)):
        xe = min(xmax-6, (ymax-16)/math.tan(Rad(phi)))
        cv.line((0, 0), (xe, xe*math.tan(Rad(phi))), col, 2.6)
        cv.math_px(cv.X(xe)+6, cv.Y(xe*math.tan(Rad(phi))), lab, 12.5, col, anchor="end" if xe > 200 else "start",
                   weight="700")
    # 圓
    cen_t, r_t = circ(cv, S3_1, S1_1, C["member"], "rgba(63,74,90,0.07)")
    cen_e, r_e = circ(cv, S3P_1, S1P_1, C["deform"], "rgba(29,78,216,0.10)")
    tangent(cv, S3_1, S1_1, PHICU, C["member"])
    tangent(cv, S3P_1, S1P_1, PHIP, C["deform"])
    cv.math_px(cv.X(S3_1), cv.Y(0)+48, "σ_{3} = %g" % S3_1, 12.5, C["member"], weight="700")
    cv.math_px(cv.X(S1_1), cv.Y(0)+48, "σ_{1} = %g" % S1_1, 12.5, C["member"], weight="700")
    cv.math_px(cv.X(S3P_1), cv.Y(0)+22, "σ_{3}' = %g" % S3P_1, 12.5, C["deform"], weight="700")
    cv.math_px(cv.X(S1P_1), cv.Y(0)+22, "σ_{1}' = %g" % S1P_1, 12.5, C["deform"], weight="700")
    # 平移量 u_f
    cv.double_arrow((S3P_1, -r_t-24/sx), (S3_1, -r_t-24/sx), C["accent"], 2.4, 9)
    cv.math_px(cv.X((S3P_1+S3_1)/2.0), cv.Y(-r_t-24/sx)+20, "u_{f} = %g" % UF_1, 12.5,
               C["accent"], weight="700")
    cv.text_px(cv.X((S3P_1+S3_1)/2.0), cv.Y(-r_t-24/sx)+38, "整個圓左移，半徑不變", 12, C["muted"])
    return cv

def panel_specimen():
    xmin, xmax, ymin, ymax = -1.45, 1.45, -1.30, 1.30
    L, R, T, B = 40, 40, 66, 182
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=PW/2.0, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="(三) 破壞面與水平面的夾角",
             sub="必須用 φ'（有效），不是 φ_cu（總）")
    w, h = 0.42, 0.74
    cv.polygon([(-w,-h),(w,-h),(w,h),(-w,h)], "rgba(63,74,90,0.07)", C["member"], 2.6)
    for th, col, dash, lab in ((THETA, C["load"], None, "正確"),
                               (THETA_WRONG, C["member2"], "7 5", "誤用 φ_cu")):
        t = Rad(th); m = math.tan(t); ys = m*w
        p0, p1 = ((-w, -ys), (w, ys)) if ys <= h else ((-h/m, -h), (h/m, h))
        cv.line(p0, p1, col, 3.4 if dash is None else 2.6, dash=dash)
    cv.line((-w, -math.tan(Rad(THETA_WRONG))*w), (-w+0.95, -math.tan(Rad(THETA_WRONG))*w),
            C["muted"], 1.5, dash="4 3")
    tA, tB = Rad(THETA), Rad(THETA_WRONG)
    base = (-w, -math.tan(tB)*w)
    cv.poly([(base[0]+0.40*math.cos(k*tB/24), base[1]+0.40*math.sin(k*tB/24)) for k in range(25)],
            C["member2"], 1.6)
    for yy, s in ((h+0.28, -1), (-h-0.28, 1)):
        cv.arrow((0, yy), (0, yy+0.16*s), C["compr"], 3.2, 10)
    cv.text_px(cv.X(0), cv.Y(h+0.48), "σ1（垂直）＝ 最大主應力", 13, C["compr"], weight="700")
    for xx, sg in ((-w-0.42, 1), (w+0.42, -1)):
        cv.arrow((xx, 0.34), (xx+0.18*sg, 0.34), C["member2"], 3.0, 9)
    cv.text_px(cv.X(-w-0.46), cv.Y(0.50), "σ3（側向）", 12, C["member2"], anchor="end")
    cv.text_px(cv.X(w+0.46), cv.Y(0.50), "σ3（側向）", 12, C["member2"], anchor="start")
    cv.text_px(cv.X(-w+0.95), cv.Y(-math.tan(Rad(THETA_WRONG))*w)+16, "水平面", 12, C["muted"], anchor="start")
    rows = [("正確（紅實線）　θ = 45° + φ'/2 = %.2f°" % THETA, C["load"], "700"),
            ("誤用（灰虛線）　45° + φcu/2 = %.2f°" % THETA_WRONG, C["member2"], "700"),
            ("", C["muted"], "400"),
            ("為什麼是 φ' 而不是 φcu：破壞是土粒間的摩擦滑動，", C["muted"], "400"),
            ("摩擦力由「粒間接觸應力」＝ 有效應力決定；孔隙水不能傳遞剪力，", C["muted"], "400"),
            ("也就決定不了破壞面往哪裡切。誤用 φcu 會把傾角低估 %.2f°。" % (THETA-THETA_WRONG), C["text"], "700")]
    for i, (txt, col, wt) in enumerate(rows):
        if txt: cv.text_px(PW/2, PH - 150 + i*21, txt, 12.5, col, weight=wt)
    return cv

compose([panel_two_circles(), panel_specimen()],
        title="SM-2018-2 圖 1　CU 試驗的總應力圓與有效應力圓，以及破壞面傾角",
        sub="σ_3 = %g、Δσ_d = %g、u_f = %g ⇒ φ_cu = %.2f°、φ' = %.2f°、θ = %.2f°" % (S3_1, DSD_1, UF_1, PHICU, PHIP, THETA),
        note="兩圓半徑同為 S_u = %.1f kPa，僅水平相距 u_f；包絡線因 NC 黏土 c = 0 而必過原點。" % ((S1_1-S3_1)/2.0),
        cols=2, path=os.path.join(OUT, "SM-2018-2-fig-1-two-mohr.svg"))

# ══════════════════════════════════════════════════════════
# fig-2　兩個試體：總應力成比例，有效應力參數不變
# ══════════════════════════════════════════════════════════
QW, QH = 700, 620

def panel_scale(effective):
    if effective:
        pairs = ((S3P_1, S1P_1, C["deform"]), (S3P_2, S1P_2, C["bmd"]))
        phi, col_e = PHIP, C["load"]
        title, sub = "有效應力圓：φ' 不因圍壓改變", "試體 2 的 u_f2 = A_f × 212.5 = %.1f kPa" % UF_2
        xmax_, ymax_ = 340.0, 250.0
    else:
        pairs = ((S3_1, S1_1, C["deform"]), (S3_2, S1_2, C["bmd"]))
        phi, col_e = PHICU, C["member2"]
        title, sub = "總應力圓：Δσ_d 與 σ_3 成正比", "兩圓相似，比例 250/100 = 2.5"
        xmax_, ymax_ = 500.0, 185.0
    xmin_, ymin_ = -20.0, -180.0
    L, R, T, B = 52, 44, 66, 40
    sx = min((QW-L-R)/(xmax_-xmin_), (QH-T-B)/(ymax_-ymin_))
    cv = Canvas(QW, QH, sx=sx, ox=L-xmin_*sx, oy=B-ymin_*sx, bg="#FFFFFF")
    cv.panel(title=title, sub=sub)
    cv.line((xmin_+4, 0), (xmax_-4, 0), C["muted"], 1.6)
    cv.line((0, ymin_+6), (0, ymax_-6), C["muted"], 1.6)
    cv.math_px(cv.X(xmax_-4)-2, cv.Y(0)-34, "σ (kPa)", 12.5, C["muted"], anchor="end")
    xe = min(xmax_-6, (ymax_-18)/math.tan(Rad(phi)))
    cv.line((0, 0), (xe, xe*math.tan(Rad(phi))), col_e, 2.6)
    cv.math_px(cv.X(xe)-4, cv.Y(xe*math.tan(Rad(phi)))-14,
               ("φ' = %.2f°" % phi) if effective else ("φ_{cu} = %.2f°" % phi),
               13, col_e, anchor="end", weight="700")
    for k, (a, b, col) in enumerate(pairs):
        circ(cv, a, b, col, "rgba(29,78,216,0.07)" if k == 0 else "none")
        tangent(cv, a, b, phi, col)
        cv.math_px(cv.X(a), cv.Y(0)+(24 if k == 0 else 46), "%g" % a, 12.5, col, weight="700")
        cv.math_px(cv.X(b), cv.Y(0)+(24 if k == 0 else 46), "%g" % b, 12.5, col, weight="700")
        cv.dim((a, -(b-a)/2.0-(18+k*26)/sx), (b, -(b-a)/2.0-(18+k*26)/sx),
               "Δσ_d = %g" % (b-a) if not effective else "2S_u = %g" % (b-a),
               off=0, color=col, size=12.5)
    return cv

compose([panel_scale(False), panel_scale(True)],
        title="SM-2018-2 圖 2　兩個試體（σ_3 = %g 與 %g）的莫爾圓" % (S3_1, S3_2),
        sub="(一) 的比例秒解，是 c' = c_cu = 0 這個前提的幾何後果",
        note="右圖 σ_3' = %g、σ_1' = %g ⇒ sinφ' = %.4f，與左試體的 %.4f 完全相同（φ' = %.2f°）。"
             % (S3P_2, S1P_2, (S1P_2-S3P_2)/(S1P_2+S3P_2), (S1P_1-S3P_1)/(S1P_1+S3P_1), PHIP_2),
        cols=2, path=os.path.join(OUT, "SM-2018-2-fig-2-scaling.svg"))
print("phicu=%.4f phi'=%.4f theta=%.4f theta_wrong=%.4f Af=%.4f dsd2=%.2f uf2=%.2f phip2=%.4f"
      % (PHICU, PHIP, THETA, THETA_WRONG, AF, DSD_2, UF_2, PHIP_2))
