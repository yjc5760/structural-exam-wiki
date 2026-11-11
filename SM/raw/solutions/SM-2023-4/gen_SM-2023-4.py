# -*- coding: utf-8 -*-
"""SM-2023-4 圖解：液性指數剖面與基底隆起量級。
   LI 由 w/LL/PL 逐層重算；隆起 FS 由 §5 的假設重算，未從文字複製。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── 鑽探表（深度 m, w %, LL %, PL %）──────────────────────
DATA = [(6, 39, 35, 11), (8, 40, 33, 10), (10, 41, 32, 12), (12, 36, 33, 11),
        (14, 42, 35, 12), (16, 45, 36, 13), (18, 41, 39, 14), (20, 42, 40, 18),
        (22, 35, 39, 20), (24, 39, 42, 18), (26, 41, 40, 16), (28, 44, 40, 15),
        (30, 32, 40, 17)]
ROWS = [(z, w, ll, pl, ll-pl, (w-pl)/(ll-pl)) for z, w, ll, pl in DATA]

H_EXC = 11.95      # 開挖深度
D_WALL = 24.0      # 連續壁底
GS, WW, GAMW = 2.70, 0.41, 9.81
EE = WW * GS                                  # e = wGs（飽和）
G_SAT_EX = (GS + EE) / (1 + EE) * GAMW        # 17.725
G_SAT = 17.7                                  # §5 採用之估算值
SIG = G_SAT * H_EXC                           # 211.5 kPa
NC = 5.14
SU_CASES = [(6.3, "N = 1 直接換算 S_u ≈ 10N/16"),
            (12.5, "放寬一倍"),
            (25.0, "一般 CL 的合理下限（N ≈ 4）")]
FS_OF = lambda su: NC * su / SIG
SU_REQ = 1.2 * SIG / NC                       # FS = 1.2 所需 S_u
N_REQ = SU_REQ / (10.0/16.0 * GAMW)           # 換回 N 值


def _seg(cv, x0, y0, x1, y1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                    'stroke-width="%s" stroke-linecap="round"%s/>' % (x0, y0, x1, y1, col, w, d))


def _dot(cv, x, y, r, col):
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="%.1f" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.0"/>' % (x, y, r, col))


def _lab(cv, x, y, txt, size, col, anchor="start", weight="700"):
    w = sum((size*1.02) if ord(ch) > 0x2E80 else (size*0.56) for ch in txt)
    x0 = {"start": x-5, "middle": x-w/2-5, "end": x-w-5}[anchor]
    cv.rect_px(x0, y-size*0.78-3, w+10, size*1.56+6, "#FFFFFFE8", 5)
    cv.text_px(x, y, txt, size, col, anchor=anchor, weight=weight)


# ══════════════════════════════════════════════════════════
# 圖一：LI 深度剖面
# ══════════════════════════════════════════════════════════
def fig1():
    W1, H1 = 980, 720
    cv = Canvas(W1, H1, sx=1.0, ox=0, oy=0, bg=C["panel"])
    cv.panel("液性指數 LI 逐層剖面：6 ~ 20 m 連續八層 LI 大於 1",
             sub="LI = (w − PL) / PI；LI 大於 1 表示天然含水量已超過液性限度，受擾動後強度趨近重模強度")
    L, Rr, T, B = 300, 320, 108, 78
    zlo, zhi = 4.0, 32.0
    xlo, xhi = 0.4, 1.6
    Xp = lambda v: L + (v-xlo)/(xhi-xlo)*(W1-L-Rr)
    Yp = lambda z: T + (z-zlo)/(zhi-zlo)*(H1-T-B)

    # LI > 1 區域底色
    cv.rect_px(Xp(1.0), Yp(zlo), Xp(xhi)-Xp(1.0), Yp(zhi)-Yp(zlo),
               "rgba(192,57,43,0.09)", 0)
    for v in [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]:
        _seg(cv, Xp(v), Yp(zlo), Xp(v), Yp(zhi), C["border"], 1.0)
        cv.text_px(Xp(v), Yp(zlo)-14, "%.1f" % v, 11.5, C["muted"])
    for z in range(6, 32, 2):
        _seg(cv, Xp(xlo), Yp(z), Xp(xhi), Yp(z), C["border"], 0.8)
    _seg(cv, Xp(1.0), Yp(zlo), Xp(1.0), Yp(zhi), C["load"], 2.4, dash="8 5")
    cv.text_px(Xp(1.0), Yp(zlo)-34, "LI = 1.0", 12.5, C["load"], weight="700")
    _seg(cv, Xp(xlo), Yp(zlo), Xp(xlo), Yp(zhi), C["muted"], 1.8)
    _seg(cv, Xp(xlo), Yp(zlo), Xp(xhi), Yp(zlo), C["muted"], 1.8)

    # 曲線
    pts = " ".join("%.2f,%.2f" % (Xp(min(max(li, xlo), xhi)), Yp(z)) for z, *_ , li in
                   [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in ROWS])
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.6" '
                    'stroke-linejoin="round"/>' % (pts, C["deform"]))

    # 關鍵深度虛線（先畫，讓 LI 標籤的白底蓋在上面）
    KEYZ = [(H_EXC, "開挖面 GL−%.2f m" % H_EXC, C["accent"]),
            (D_WALL, "連續壁底 GL−%.1f m（N 仍為 1）" % D_WALL, C["bmd"])]
    for z, lab, col in KEYZ:
        _seg(cv, Xp(xlo), Yp(z), Xp(xhi), Yp(z), col, 2.2, dash="7 5")

    # 左欄資料 + 右欄 LI 值
    cv.text_px(56, T-30, "深度 m", 11.5, C["text"], anchor="start", weight="700")
    cv.text_px(120, T-30, "w %", 11.5, C["text"], anchor="start", weight="700")
    cv.text_px(176, T-30, "LL %", 11.5, C["text"], anchor="start", weight="700")
    cv.text_px(236, T-30, "PL %", 11.5, C["text"], anchor="start", weight="700")
    for z, w, ll, pl, pi, li in ROWS:
        y = Yp(z)
        hot = li > 1.0
        col = C["load"] if hot else C["muted"]
        cv.text_px(56, y, "%d m" % z, 11.5, col, anchor="start",
                   weight="700" if hot else "400")
        cv.text_px(120, y, "%d" % w, 11.5, C["muted"], anchor="start")
        cv.text_px(176, y, "%d" % ll, 11.5, C["muted"], anchor="start")
        cv.text_px(236, y, "%d" % pl, 11.5, C["muted"], anchor="start")
        _dot(cv, Xp(li), y, 4.8, col)
        _lab(cv, Xp(li) + (12 if li <= 1.25 else -12), y, "%.2f" % li, 11.5, col,
             anchor="start" if li <= 1.25 else "end",
             weight="700" if hot else "400")

    for z, lab, col in KEYZ:
        _lab(cv, Xp(xlo)+10, Yp(z)-15, lab, 12, col)

    # 6~20 m 區間標示
    _seg(cv, Xp(xhi)+12, Yp(6), Xp(xhi)+12, Yp(20), C["load"], 3.2)
    tx = Xp(xhi)+26
    for k, (t, sz, col, wt) in enumerate([("GL−6 ~ −20 m", 12, C["load"], "700"),
                                          ("八層 LI 全部大於 1", 12, C["load"], "700"),
                                          ("＝開挖影響範圍整段", 11.5, C["muted"], "400"),
                                          ("　都在流動化的土層裡", 11.5, C["muted"], "400")]):
        cv.text_px(tx, Yp(6.6)+k*19, t, sz, col, anchor="start", weight=wt)
    for k, (t, sz, col, wt) in enumerate([("22 / 24 / 30 m 的 LI 小於 1", 11.5, C["bmd"], "700"),
                                          ("但 N 值並未變好：", 11.5, C["muted"], "400"),
                                          ("壁底 24 m 仍是 N = 1", 11.5, C["muted"], "400"),
                                          ("26 m 才升到 N = 3", 11.5, C["muted"], "400")]):
        cv.text_px(tx, Yp(25.6)+k*19, t, sz, col, anchor="start", weight=wt)

    cv.text_px((Xp(xlo)+Xp(xhi))/2, H1-40, "液性指數 LI", 13, C["text"], weight="700")
    return cv


# ══════════════════════════════════════════════════════════
# 圖二：基底隆起量級
# ══════════════════════════════════════════════════════════
def fig2():
    W2, H2, ZT = 680, 660, 28.0

    # ── (a) 破壞機制剖面 ──
    ca = Canvas(W2, H2, sx=13.0, ox=340, oy=146, bg=C["panel"])
    ca.panel("(a) 基底隆起機制", sub="坑外覆土 γH_e 把土推向坑內，坑底只靠 S_u 抵抗")
    Yz = lambda z: (ZT - z)
    XL, XR = -13.0, 13.0
    ca.polygon([(XL, Yz(0)), (XR, Yz(0)), (XR, Yz(ZT)), (XL, Yz(ZT))],
               "rgba(46,125,111,0.16)")
    ca.polygon([(0.05, Yz(0)), (XR, Yz(0)), (XR, Yz(H_EXC)), (0.05, Yz(H_EXC))], "#FFFFFF")
    ca.line((XL, Yz(0)), (0, Yz(0)), C["member"], 2.2)
    ca.line((0.05, Yz(H_EXC)), (XR, Yz(H_EXC)), C["member"], 2.4)
    ca.line((0, Yz(0)), (0, Yz(D_WALL)), C["member"], 5.4)
    _lab(ca, ca.X(0)-8, ca.Y(Yz(D_WALL))+18, "連續壁底 GL−%.1f m（N = 1）" % D_WALL,
         11, C["member"], anchor="end")
    _lab(ca, ca.X(XL)+4, ca.Y(Yz(H_EXC))+14, "開挖面 GL−%.2f m" % H_EXC, 11, C["accent"])
    _lab(ca, ca.X(XL)+4, ca.Y(Yz(0))-11, "GL±0", 11, C["muted"], weight="400")
    _lab(ca, ca.X(-12.4), ca.Y(Yz(17.2)), "CL　N = 1　LI 大於 1（6 ~ 20 m）", 11.5, C["bmd"])

    # 覆土壓力
    for k in range(5):
        x = -11.0 + k*2.4
        ca.arrow((x, Yz(H_EXC-1.9)), (x, Yz(H_EXC-0.3)), C["load"], 2.2, 8)
    _lab(ca, ca.X(-12.4), ca.Y(Yz(H_EXC-3.4)), "γH_e = %.1f × %.2f = %.1f kPa"
         % (G_SAT, H_EXC, SIG), 11.5, C["load"])
    # 隆起流線
    pts = []
    r = D_WALL - H_EXC
    for t in range(0, 181, 4):
        pts.append((r*math.cos(math.radians(t)),
                    Yz(H_EXC + r*math.sin(math.radians(t)))))
    ca.poly(pts, C["accent"], 2.6, dash="8 5")
    ca.line((-r, Yz(H_EXC)), (-r, Yz(0)), C["accent"], 2.6, dash="8 5")
    for k in range(3):
        x = 1.3 + k*2.0
        ca.arrow((x, Yz(H_EXC+1.9)), (x, Yz(H_EXC+0.3)), C["bmd"], 2.2, 8)
    _lab(ca, ca.X(1.4), ca.Y(Yz(H_EXC+3.4)), "坑底土上湧", 11.5, C["bmd"])
    _lab(ca, ca.X(-r)+8, ca.Y(Yz(4.6)), "隆起破壞面", 11.5, C["accent"])

    yb = H2 - 118
    _seg(ca, 46, yb, W2-46, yb, C["border"], 1.3)
    ca.text_px(W2/2, yb+26, "FS = N_c S_u / (γ H_e)　，　N_c = %.2f" % NC, 13,
               C["text"], weight="700")
    ca.text_px(W2/2, yb+52, "γ_{sat} 由 e = wG_s = %.3f 反推 = %.2f kN/m³（估算）"
               % (EE, G_SAT_EX), 11.5, C["muted"])
    ca.text_px(W2/2, yb+76, "分母 γH_e = %.1f kPa 固定，分子只剩 S_u 一個變數" % SIG,
               11.5, C["muted"])

    # ── (b) FS 長條 ──
    cb = Canvas(W2, H2, sx=1.0, ox=0, oy=0, bg=C["panel"])
    cb.panel("(b) 三種 S_u 取法的 FS 都遠小於 1",
             sub="即使把 S_u 放寬到一般 CL 的合理下限，FS 仍只有 %.2f" % FS_OF(25.0))
    barx, barw, y0 = 210, 300, 150
    smax = 1.35
    _seg(cb, barx + barw*1.0/smax, y0-40, barx + barw*1.0/smax, y0+3*86+26,
         C["load"], 2.4, dash="7 5")
    cb.text_px(barx + barw*1.0/smax, y0-52, "FS = 1", 12, C["load"], weight="700")
    _seg(cb, barx + barw*1.2/smax, y0-40, barx + barw*1.2/smax, y0+3*86+26,
         C["bmd"], 2.0, dash="5 4")
    cb.text_px(barx + barw*1.2/smax + 6, y0-52, "1.2", 12, C["bmd"],
               anchor="start", weight="700")
    for i, (su, why) in enumerate(SU_CASES):
        y = y0 + i*86
        fs = FS_OF(su)
        cb.text_px(barx-14, y, "S_u = %.1f kPa" % su, 12.5, C["deform"],
                   anchor="end", weight="700")
        cb.rect_px(barx, y-13, max(2.0, barw*fs/smax), 26, C["load"], 5)
        cb.text_px(barx + barw*fs/smax + 10, y, "FS = %.2f" % fs, 12.5, C["load"],
                   anchor="start", weight="700")
        cb.text_px(barx-14, y+20, why, 11, C["muted"], anchor="end")
    yb2 = y0 + 3*86 + 40
    _seg(cb, 46, yb2, W2-46, yb2, C["border"], 1.3)
    cb.text_px(W2/2, yb2+30, "要把 FS 拉到 1.2，需要 S_u ≥ %.0f kPa" % SU_REQ, 13.5,
               C["bmd"], weight="700")
    cb.text_px(W2/2, yb2+54, "換算回 SPT 約 N ≈ %.0f，與現地實測的 N = 1 差近一個數量級"
               % N_REQ, 12, C["text"])
    cb.text_px(W2/2, yb2+80, "⇒ 不先做地盤改良，抗隆起在數字上根本不成立", 12.5,
               C["load"], weight="700")
    return [ca, cb]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    compose([fig1()], title="SM-2023-4　液性指數逐層剖面：軟弱層的範圍與開挖深度的關係",
            sub="鑽探表 GL−6 ~ −30 m 每 2 m 一組 w / LL / PL，逐層換算 LI",
            note="陷阱：只算 GL−10 m 一層的 LI 不足以說明問題，逐層算過才看得出 6 ~ 20 m 連續八層都大於 1。",
            path=os.path.join(OUT, "SM-2023-4-fig-1-li-profile.svg"))
    compose(fig2(), title="SM-2023-4　基底隆起的量級估算：三種 Su 取法都過不了",
            sub="開挖深度 He = %.2f m、γsat ≈ %.1f kN/m³（由 w、Gs 反推）、Nc = %.2f"
                % (H_EXC, G_SAT, NC),
            note="數值為估算（題目未給單位重與強度），作答時須註明假設；此處要的是量級，不是精確值。",
            cols=2, path=os.path.join(OUT, "SM-2023-4-fig-2-heave.svg"))
    print("e = wGs = %.4f ; γsat(未捨入) = %.3f ; 採用 %.1f ; γHe = %.2f kPa"
          % (EE, G_SAT_EX, G_SAT, SIG))
    for su, why in SU_CASES:
        print("  Su=%5.1f kPa → FS = %.3f  (%s)" % (su, FS_OF(su), why))
    print("FS=1.2 需 Su ≥ %.2f kPa ⇒ N ≈ %.2f" % (SU_REQ, N_REQ))
    print("LI：", "  ".join("%dm=%.2f" % (z, li) for z, w, ll, pl, pi, li in ROWS))
