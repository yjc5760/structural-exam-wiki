#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-U2-3「設計規範對施工之要求」觀念講義 — SVG 向量圖解產生器

鐵則：圖上每個數字都由本檔頂端的常數與算式推出，不得憑印象填。
改一個輸入（F_EXX、Tb、mu、dz/wz…），圖形自動跟著變。

繪圖鐵則（踩過的坑）：
  * math_px/math 走襯線數學字型，**沒有 CJK 字面** → 含中文的字串一律用 text_px。
    text_px 同樣會解析 _{} / ^{}，所以中英數混排直接用 text_px 就好。
  * polygon/line/poly/circle 吃「模型座標」；像素版畫布請用 PX() 轉換 y。
  * 數學襯線字型缺 Unicode 上下標與 √ 排版不穩 → 用 ^{} / _{} 語法，根號寫成數值。
  * compose() 的 title/sub/note 走 esc()，不解析 _{}，一律純文字。
"""
import sys, os, math, glob
SD = glob.glob("/root/.claude/skills/synced/*/struct-diagram")[0]
sys.path.insert(0, os.path.join(SD, "scripts"))
from structdraw import Canvas, C, compose, member_shape

OUT = "figs"
os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 輸入常數（所有圖上的數字皆由此推算）
# ═══════════════════════════════════════════════════════════════
# --- 填角銲（E70 銲條，LRFD）---
F_EXX = 490.0                                # MPa，E70 銲條抗拉強度
PHI_W, K_SHEAR = 0.75, 0.6
THROAT = 1.0/math.sqrt(2.0)                  # 0.7071，等腳填角銲銲喉係數
VM_EXACT = 1.0/math.sqrt(3.0)                # 0.5774，von Mises 剪切降伏
WELD_SIZES = [6.0, 8.0, 10.0, 12.0]          # mm
def weld_cap(w):                             # kN / mm 銲長
    return PHI_W*K_SHEAR*F_EXX*THROAT*w/1000.0

# --- 銲腳尺寸與回銲 ---
WMIN_TABLE = [(6.0, 3.0), (13.0, 5.0), (19.0, 6.0), (1e9, 8.0)]
def w_min(t):
    for lim, w in WMIN_TABLE:
        if t <= lim: return w
    return 8.0
def w_max(t):
    return t if t < 6.0 else t - 2.0
T_DEMO = 12.0                                # 示範板厚 mm
W_DEMO = 8.0                                 # 示範銲腳 mm
END_RETURN = (2.0, 4.0)

# --- 高拉力螺栓 A325 M22 ---
FU_B, FY_B, AS_B = 825.0, 660.0, 303.0       # MPa, MPa, mm2
TB = 0.7*FU_B*AS_B/1000.0                    # kN 最小預拉力
FYAS = FY_B*AS_B/1000.0                      # kN 降伏軸力
TB_OVER_FY = TB/FYAS
PHI_SC, DU, HSC, NS = 1.00, 1.13, 1.00, 1
MU_CASES = [("噴砂除銹 Class B", 0.50, C["bmd"]),
            ("一般除銹 Class A", 0.33, C["compr"]),
            ("塗裝面（規範禁用）", 0.15, C["load"])]
def slip_cap(mu):                            # kN / 螺栓
    return PHI_SC*mu*DU*HSC*TB*NS

# --- 節點域（梁 H600x200x11x17；柱 H400x400x13x21）---
DB, TFB = 600.0, 17.0
DC, TFC, TWC = 400.0, 21.0, 13.0
DZ, WZ = DB - TFB, DC - TFC
TZ_REQ = (DZ + WZ)/90.0

# --- 碳當量與預熱 ---
def CE_iiw(Cc, Mn, Cr=0.0, Mo=0.0, V=0.0, Ni=0.0, Cu=0.0):
    return Cc + Mn/6.0 + (Cr+Mo+V)/5.0 + (Ni+Cu)/15.0
CE_SN490B = CE_iiw(0.16, 1.35)
CE_SM570 = CE_iiw(0.18, 1.45, Cr=0.20, Mo=0.10, V=0.05, Ni=0.20, Cu=0.15)
CE_LIMIT = 0.44
PREHEAT = [(19.0, 10.0), (38.0, 65.0), (65.0, 110.0), (1e9, 150.0)]
def preheat(t):
    for lim, T in PREHEAT:
        if t <= lim: return T
    return 150.0
DRY_T = (300.0, 350.0)                       # 低氫銲條烘乾溫度 degC
HOLD_T = (100.0, 150.0)                      # 保溫筒溫度 degC
INTERPASS_MAX = 350.0

# --- 電化學標準電極電位（V vs SHE）---
E_ZN, E_FE, E_CU = -0.76, -0.44, +0.34

# --- 韌性與延性 ---
CVN_J, CVN_T = 27.0, 0.0
YR_LIMIT = 0.80
RA_Z = 25.0
T_BOXCOL = 40.0                              # 箱型柱強制 C 級的板厚門檻 mm


# ═══════════════════════════════════════════════════════════════
# 版面工具
# ═══════════════════════════════════════════════════════════════
def pcv(w, h, xr, yr, pad):
    L, R, T, B = pad
    sx = min((w-L-R)/(xr[1]-xr[0]), (h-T-B)/(yr[1]-yr[0]))
    ox = L + (w-L-R-(xr[1]-xr[0])*sx)/2 - xr[0]*sx
    oy = B + (h-T-B-(yr[1]-yr[0])*sx)/2 - yr[0]*sx
    return Canvas(w, h, sx=sx, ox=ox, oy=oy)


def pxcv(w, h):
    """像素畫布：模型單位＝像素，但 y 仍由底部起算（用 PX 轉換）。"""
    return Canvas(w, h, sx=1, ox=0, oy=0)


def PX(cv, x, y):
    """像素座標 (x, y 由頂端起算) → 模型座標，供 polygon/poly/line/circle 使用。"""
    return (x, cv.h - y)


def plotbox(w, h, xr, yr, box):
    cv = Canvas(w, h, sx=1, ox=0, oy=0)
    x0, x1, y0, y1 = box
    fx = lambda v: x0 + (v-xr[0])/(xr[1]-xr[0])*(x1-x0)
    fy = lambda v: y0 + (v-yr[0])/(yr[1]-yr[0])*(y1-y0)
    return cv, fx, fy, (lambda a, b: (fx(a), fy(b)))


def axis_frame(cv, x0, x1, y0, y1, xlab, ylab):
    cv.arrow((x0, y0), (x1+16, y0), C["muted"], 1.8, 9)
    cv.arrow((x0, y0), (x0, y1+16), C["muted"], 1.8, 9)
    cv.text_px(x1+24, cv.h-y0+4, xlab, 13.5, C["muted"], "start")
    cv.text_px(x0, cv.h-y1-30, ylab, 13.5, C["muted"])


def vdown(cv, x, y0, y1, col, w=2.4):
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1-9:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"/>')
    cv.parts.append(f'<polygon points="{x:.1f},{y1:.1f} {x-5.2:.1f},{y1-10:.1f} '
                    f'{x+5.2:.1f},{y1-10:.1f}" fill="{col}"/>')


def harrow(cv, x0, x1, y, col, w=2.4):
    d = 1 if x1 > x0 else -1
    cv.parts.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1-9*d:.1f}" y2="{y:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"/>')
    cv.parts.append(f'<polygon points="{x1:.1f},{y:.1f} {x1-10*d:.1f},{y-5.2:.1f} '
                    f'{x1-10*d:.1f},{y+5.2:.1f}" fill="{col}"/>')


def cross(cv, x, y, r, col, w=3.2):
    cv.parts.append(f'<line x1="{x-r}" y1="{y-r}" x2="{x+r}" y2="{y+r}" stroke="{col}" '
                    f'stroke-width="{w}" stroke-linecap="round"/>')
    cv.parts.append(f'<line x1="{x-r}" y1="{y+r}" x2="{x+r}" y2="{y-r}" stroke="{col}" '
                    f'stroke-width="{w}" stroke-linecap="round"/>')


def tick(cv, x, y, r, col, w=3.2):
    cv.parts.append(f'<polyline points="{x-r},{y} {x-r*0.22},{y+r*0.72} {x+r},{y-r*0.78}" '
                    f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
                    f'stroke-linejoin="round"/>')


def hsec(cv, cx, cy, bw, dp, tf, tw, col, fill=None):
    f = fill or C["fill_c"]
    cv.rect_px(cx-bw/2, cy-dp/2, bw, tf, f, 0, col, 1.6)
    cv.rect_px(cx-bw/2, cy+dp/2-tf, bw, tf, f, 0, col, 1.6)
    cv.rect_px(cx-tw/2, cy-dp/2+tf, tw, dp-2*tf, f, 0, col, 1.6)


def bullet(cv, x, y, s, col, size=13.5, gap=20):
    cv.rect_px(x, y-10, 9, 20, col, 3)
    cv.text_px(x+gap, y, s, size, C["text"], "start")


PW, PH = 520, 600
W3, H3 = 347, 476


# ═══════════════════════════════════════════════════════════════
# 圖 1　設計假設 ←→ 施工實況
# ═══════════════════════════════════════════════════════════════
def fig1():
    cx, cy = W3/2, 168

    a = pxcv(W3, H3)
    a.panel("設計端：理想的鋼", "前四單元 U1-1 ~ U1-4 算的對象")
    hsec(a, cx, cy, 130, 126, 15, 11, C["member"], C["fill_c"])
    a.text_px(cx+18, cy, "F_{y}", 16, C["compr"], "start", weight="700")
    a.text_px(cx, cy+88, "整根桿件處處相同", 12.5, C["muted"])
    for i, s in enumerate(["均質、無缺陷、無夾雜物", "F_{y} 為一個定值",
                           "斷面連續，不被接合削弱", "韌性充足，變形前不脆斷"]):
        bullet(a, 34, 280 + i*34, s, C["compr"])
    a.text_px(W3/2, H3-36, "設計「假設」的那根鋼", 13.5, C["compr"], weight="700")

    b = pxcv(W3, H3)
    b.panel("工地端：真的做出來的鋼", "本單元 U2-3 管的對象")
    hsec(b, cx, cy, 130, 126, 15, 11, C["member"], C["fill_c"])
    # 翼板／腹板交會處的填角銲
    for sgn in (-1, 1):
        x0 = cx + sgn*5.5
        b.polygon([PX(b, x0, cy-48), PX(b, x0+sgn*24, cy-48), PX(b, x0, cy-24)],
                  C["fill_t"], C["load"], 1.8)
    b.parts.append(f'<ellipse cx="{cx}" cy="{cy-44}" rx="44" ry="17" fill="none" '
                   f'stroke="{C["accent"]}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    b.text_px(cx+50, cy-62, "HAZ 粗晶區", 12, C["accent"], "start", weight="700")
    for k in range(5):
        yy = cy + 4 + k*10
        b.parts.append(f'<line x1="{cx-56}" y1="{yy}" x2="{cx-14}" y2="{yy}" '
                       f'stroke="{C["muted"]}" stroke-width="1.7" stroke-dasharray="8 7"/>')
    b.text_px(cx-62, cy+30, "軋延夾雜物", 11.5, C["muted"], "end")
    b.parts.append(f'<path d="M {cx+22} {cy+52} q 13 -13 26 0 q 13 13 26 0" fill="none" '
                   f'stroke="{C["load"]}" stroke-width="2.0"/>')
    b.text_px(cx+22, cy+72, "殘留應力", 11.5, C["load"], "start", weight="700")
    for i, s in enumerate(["HAZ 過熱區晶粒粗大、韌性最低", "氫致冷裂（延遲裂縫）",
                           "殘留應力與拘束度", "板面油污、水氣、腐蝕"]):
        bullet(b, 34, 280 + i*34, s, C["load"])
    b.text_px(W3/2, H3-36, "規範「面對」的那根鋼", 13.5, C["load"], weight="700")

    c = pxcv(W3, H3)
    c.panel("規範在做的唯一一件事", "把偏離量壓回容許範圍")
    x0, x1 = 40, W3-40
    c.rect_px(x0, 104, (x1-x0)*0.34, 32, C["fill_m"], 6, C["bmd"], 1.8)
    c.text_px(x0+(x1-x0)*0.17, 120, "設計容許範圍", 12, C["bmd"], weight="700")
    c.rect_px(x0, 150, (x1-x0)*0.97, 32, C["fill_t"], 6, C["load"], 1.8)
    c.text_px(x0+(x1-x0)*0.485, 166, "未受管制的施工偏離量", 12, C["load"], weight="700")
    c.text_px(W3/2, 204, "三道防線各壓回一截", 12.5, C["muted"])
    rows = [("① 事前　管輸入", "材料等級・CE・銲條烘乾・WPS", C["compr"]),
            ("② 事中　管過程", "預熱／層間溫度・銲腳・回銲", C["accent"]),
            ("③ 事後　管驗收", "VT → MT／PT → UT／RT", C["bmd"])]
    for i, (t1, t2, col) in enumerate(rows):
        y = 258 + i*58
        harrow(c, x1-8, x0+(x1-x0)*0.34, y, col, 2.4)
        c.text_px(x1-4, y-16, t1, 12.5, col, "end", weight="700")
        c.text_px(x1-4, y+16, t2, 11, C["muted"], "end")
    c.text_px(W3/2, H3-36, "所有施工規範都是這三個箭頭", 13.5, C["bmd"], weight="700")

    compose([a, b, c],
            title="本單元唯一的主軸：設計假設 ←→ 施工實況",
            sub="不是背法規條文，而是問「這道工序會讓實物偏離設計假設多少」",
            note="前四單元算的是理想的鋼；本單元管的是工地真的做出來的那根鋼。"
                 "每一條施工規範都在回答同一個問題：用什麼手段把偏離量壓回容許範圍內。",
            path=f"{OUT}/u23-fig-1-assumption-vs-site.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 2　三道防線解題骨架
# ═══════════════════════════════════════════════════════════════
def fig2():
    W, H = 1200, 470
    cv = pxcv(W, H)
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)

    cols = [
        ("① 事前　管輸入", C["compr"], C["fill_c"],
         ["母材等級 SN-B／SN-C（Z 向受拉）", "碳當量 CE、降伏比 F_{y}/F_{u}",
          "低氫銲條烘乾 ＋ 保溫筒隨身", "銲接程序書 WPS、銲工資格"]),
        ("② 事中　管過程", C["accent"], "rgba(180,83,9,0.15)",
         ["預熱／層間溫度／後熱", "銲腳尺寸 w_{min} ~ w_{max}",
          "回銲 2w ~ 4w（撓性接頭禁用）", "摩阻面與銲道兩側不予塗裝"]),
        ("③ 事後　管驗收", C["bmd"], C["fill_m"],
         ["VT 目視：所有銲道的基線", "MT／PT：表面缺陷", "UT／RT：內部缺陷",
          "CJP 與耐震接頭：100% UT"]),
    ]
    CW_ = 344
    xs = [48, 48+CW_+36, 48+2*(CW_+36)]
    for (head, col, fill, rows), x in zip(cols, xs):
        cv.rect_px(x, 44, CW_, 44, fill, 10, col, 2.0)
        cv.text_px(x+CW_/2, 66, head, 16.5, col, weight="700")
        for i, s in enumerate(rows):
            y = 108 + i*62
            cv.rect_px(x, y, CW_, 48, C["panel"], 9, C["border"], 1.4)
            cv.rect_px(x, y, 7, 48, col, 3)
            cv.text_px(x+22, y+24, s, 14, C["text"], "start")
            if i < len(rows)-1:
                vdown(cv, x+CW_/2, y+48, y+62, col, 1.8)

    cv.rect_px(xs[0], 388, xs[2]+CW_-xs[0], 54, C["fill_t"], 12, C["load"], 2.2)
    cv.text_px(W/2, 406, "偏離量被壓回設計容許範圍", 15.5, C["text"], weight="700")
    cv.text_px(W/2, 428, "閱卷給分幾乎都是「名稱一半、理由一半」——每一格都要寫出它擋掉哪一種偏離",
               13.5, C["load"], weight="700")
    for x in xs:
        vdown(cv, x+CW_/2, 108+3*62+48, 388, C["muted"], 2.0)

    compose([cv],
            title="萬用解題骨架：任何施工說明題都切成三道防線",
            sub="先寫物理機制，再按「事前／事中／事後」開架構，就不會漏點",
            note="這個骨架的價值在於「不會漏」：想不到細節時，逐格自問「這一關要管什麼輸入／過程／驗收」，"
                 "通常就能補回一到兩個得分點。",
            path=f"{OUT}/u23-fig-2-three-lines.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 3　填角銲：0.707 與 0.6 的來源
# ═══════════════════════════════════════════════════════════════
def fig3():
    a = pcv(PW, PH, (-0.30, 1.45), (-0.28, 1.42), (60, 60, 96, 128))
    a.panel("銲喉 = 最短破壞面", "等腳填角銲斷面為等腰直角三角形")
    a.polygon([(-0.28, -0.26), (1.42, -0.26), (1.42, 0.0), (-0.28, 0.0)],
              C["fill_c"], C["member"], 1.8)
    a.polygon([(-0.28, 0.0), (0.0, 0.0), (0.0, 1.40), (-0.28, 1.40)],
              C["fill_c"], C["member"], 1.8)
    a.polygon([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], C["fill_t"], C["load"], 2.2)
    te = 0.5
    a.line((0.0, 0.0), (te, te), C["accent"], 4.2)
    a.dot((te, te), 5.0, fill="#FFFFFF", stroke=C["accent"], w=2.4)
    a.text_px(a.X(te/2)+14, a.Y(te/2)+18, "t_{e}", 17, C["accent"], "start", weight="700")
    a.parts.append(f'<path d="M {a.X(0.24)} {a.Y(0.0)} A {0.24*a.sx} {0.24*a.sx} 0 0 0 '
                   f'{a.X(0.17)} {a.Y(0.17)}" fill="none" stroke="{C["muted"]}" stroke-width="1.6"/>')
    a.text_px(a.X(0.30), a.Y(0.10), "45°", 12.5, C["muted"], "start")
    a.dim((0.0, -0.05), (1.0, -0.05), "w", off=26, size=15)
    a.dim((-0.05, 0.0), (-0.05, 1.0), "w", off=26, size=15)
    a.text_px(a.X(0.60), a.Y(0.62), "破壞面", 13, C["load"], "start", weight="700")
    a.text_px(PW/2, PH-96, "t_{e} = w · sin45° = w ÷ 1.414", 16, C["accent"], weight="700")
    a.text_px(PW/2, PH-68, f"= {THROAT:.4f} w ≈ 0.707 w", 16, C["accent"], weight="700")
    a.text_px(PW/2, PH-40, "0.707 是幾何常數，不是經驗值", 13, C["muted"])

    b = pxcv(PW, PH)
    b.panel("每 1 mm 銲長能扛多少", "E70 銲條 F_{EXX} = 490 MPa，LRFD")
    x0, xlim = 138, PW-110
    caps = [weld_cap(w) for w in WELD_SIZES]
    lim = max(caps)*1.10
    ytop, bh, gap = 142, 40, 26
    b.text_px(x0+(xlim-x0)*0.5, ytop-26, "單位銲長設計強度 φR_{n} / L", 13, C["muted"])
    for i, (w, cap) in enumerate(zip(WELD_SIZES, caps)):
        y = ytop + i*(bh+gap)
        bw_ = (xlim-x0)*cap/lim
        hot = abs(w-8.0) < 1e-9
        b.rect_px(x0, y, bw_, bh, C["fill_t"] if hot else C["fill_m"], 6,
                  C["load"] if hot else C["bmd"], 2.2 if hot else 1.5)
        b.text_px(x0-14, y+bh/2, f"w = {w:.0f} mm", 13.5, C["text"], "end",
                  weight="700" if hot else "400")
        b.text_px(x0+bw_-10, y+bh/2, f"{cap:.2f} kN/mm", 13.5,
                  C["load"] if hot else C["bmd"], "end", weight="700")
    b.text_px(PW/2, PH-136, "φR_{n} = 0.75 × 0.6F_{EXX} × (0.707w) × L",
              16, C["text"], weight="700")
    b.text_px(PW/2, PH-106, "0.6 來自 von Mises 剪切降伏", 13, C["muted"])
    b.text_px(PW/2, PH-80, f"τ_{{y}} = F_{{y}} ÷ 1.732 = {VM_EXACT:.3f} F_{{y}}",
              14.5, C["bmd"], weight="700")
    b.text_px(PW/2, PH-56, "規範取整為 0.6 F_{y}", 14.5, C["bmd"], weight="700")
    b.text_px(PW/2, PH-28, f"考場基準：w = 8 mm 約 {weld_cap(8.0):.2f} kN/mm",
              13.5, C["load"], weight="700")

    compose([a, b],
            title="填角銲強度公式的兩個常數，都不是背來的",
            sub="0.707 來自幾何、0.6 來自 von Mises 降伏準則",
            note="考場上先用 w = 8 mm 約 1.25 kN/mm 當基準，可立刻檢查自己算出來的量級有沒有錯一個數量級。",
            path=f"{OUT}/u23-fig-3-fillet-throat.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 4　銲接熱循環與 HAZ
# ═══════════════════════════════════════════════════════════════
def fig4():
    a = pxcv(PW, PH)
    a.panel("銲道橫斷面的分區", "局部熔化 → 急速抽冷，各區峰值溫度不同")
    cx, base = PW/2, 254
    a.rect_px(52, base, PW-104, 76, C["fill_c"], 4, C["member"], 1.6)
    zones = [(104, C["fill_t"], C["load"], "銲著金屬", "熔化後再凝固"),
             (80, "rgba(180,83,9,0.30)", C["accent"], "過熱（粗晶）區", "晶粒粗大．韌性最低"),
             (60, "rgba(180,83,9,0.14)", C["accent"], "細晶區", "正常化．韌性回升"),
             (40, C["fill_m"], C["bmd"], "部分變態區", "未完全變態")]
    for r, fill, stroke, _, _ in zones:
        a.parts.append(f'<path d="M {cx-r} {base} A {r} {r*0.86} 0 0 1 {cx+r} {base} Z" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
    a.parts.append(f'<line x1="{cx-104}" y1="{base}" x2="{cx+104}" y2="{base}" '
                   f'stroke="{C["load"]}" stroke-width="2.2"/>')
    a.text_px(cx+118, base-4, "熔合線", 11.5, C["load"], "start", weight="700")
    a.text_px(cx, base+42, "母材（未受熱影響）", 12.5, C["muted"])
    for i, (r, fill, stroke, t1, t2) in enumerate(zones):
        y = 366 + i*30
        a.rect_px(62, y-9, 20, 18, fill, 4, stroke, 1.6)
        a.text_px(92, y, t1, 12.5, stroke, "start", weight="700")
        a.text_px(196, y, t2, 11.5, C["muted"], "start")
    a.text_px(cx, 502, "HAZ = 沒有熔化、卻被熱改變組織的那一圈", 13, C["accent"], weight="700")
    a.text_px(cx, 526, "所以換銲材救不了 HAZ —— 只能靠溫度管制", 12.5, C["muted"])
    a.text_px(PW/2, PH-42, "破壞幾乎都從過熱粗晶區起裂，不是從銲道中心",
              13.5, C["load"], weight="700")

    # --- b：峰值溫度與韌性 ---
    b, fx, fy, P = plotbox(PW, PH, (0, 1.0), (0, 1.0), (100, PW-92, 212, 456))
    b.panel("離銲道愈近，韌性愈差", "峰值溫度愈高 → 晶粒愈粗")
    axis_frame(b, fx(0), fx(1.0), fy(0), fy(1.0), "距離", "")
    pts = [P(x, 0.94*math.exp(-3.1*x)+0.05) for x in [i/120 for i in range(121)]]
    b.poly(pts, C["load"], 3.4)
    b.text_px(fx(0.40), PH-fy(0.46), "峰值溫度", 13, C["load"], "start", weight="700")
    def tough(x):
        return 0.80 - 0.60*math.exp(-((x-0.12)/0.085)**2)
    pts2 = [P(x, tough(x)) for x in [i/160 for i in range(161)]]
    b.poly(pts2, C["bmd"], 3.4, dash="8 5")
    b.text_px(fx(0.50), PH-fy(0.86), "衝擊韌性 CVN", 13, C["bmd"], "start", weight="700")
    xv = 0.12
    b.line(P(xv, 0), P(xv, 0.90), C["accent"], 2.0, dash="6 5")
    b.dot(P(xv, tough(xv)), 6.0, fill=C["accent"], stroke="#FFFFFF", w=2.2)
    b.text_px(fx(xv)+4, PH-fy(0.97), "過熱粗晶區", 12.5, C["accent"], "start", weight="700")
    b.text_px(fx(xv)+12, PH-fy(tough(xv))+2, "韌性谷底", 12, C["accent"], "start", weight="700")
    b.text_px(fx(0.0)-6, PH-fy(0.90), "高", 12, C["muted"], "end")
    b.text_px(fx(0.0)-6, PH-fy(0.06), "低", 12, C["muted"], "end")
    b.text_px(PW/2, PH-152, f"故 SN490B 要求 CVN 在 {CVN_T:.0f}°C 下 ≥ {CVN_J:.0f} J",
              14, C["bmd"], weight="700")
    b.rect_px(56, PH-128, PW-112, 104, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, PH-108, "答題關鍵句", 12.5, C["load"], weight="700")
    b.text_px(PW/2, PH-84, "「銲接是局部熔化再急速抽冷，最靠近銲道的", 12.5, C["text"])
    b.text_px(PW/2, PH-62, "熱影響區過熱區晶粒粗大化、韌性最低，", 12.5, C["text"])
    b.text_px(PW/2, PH-40, "是破壞的主要起裂點。」", 12.5, C["text"])

    compose([a, b],
            title="銲接熱的第一個後果：熱影響區（HAZ）",
            sub="沒有熔化、卻被熱改變組織的那一圈，才是最脆弱的地方",
            note="這也是為什麼規範管的是「溫度」（預熱、層間、後熱）而不只是「銲材」——"
                 "溫度歷程決定 HAZ 的組織，銲材只決定銲著金屬本身。",
            path=f"{OUT}/u23-fig-4-haz.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 5　氫致冷裂三要素與預熱
# ═══════════════════════════════════════════════════════════════
def fig5():
    a = pcv(PW, PH, (-1.35, 1.35), (-1.30, 1.40), (46, 46, 96, 150))
    a.panel("氫致冷裂（延遲裂縫）的三要素", "缺一不可 → 破壞任一個就能防裂")
    R = 0.72
    cs = [((0.0, 0.42), C["load"], C["fill_t"], "氫源", "濕氣・油污・鏽"),
          ((-0.40, -0.30), C["compr"], C["fill_c"], "高拉應力", "殘留應力・拘束度"),
          ((0.40, -0.30), C["bmd"], C["fill_m"], "敏感組織", "高 CE → 麻田散鐵")]
    for p, col, fill, _, _ in cs:
        a.circle(p, R, fill=fill, stroke=col, w=2.6)
    for p, col, fill, t1, t2 in cs:
        dx = 0 if abs(p[0]) < 1e-6 else (1 if p[0] > 0 else -1)
        px_, py_ = a.X(p[0]) + dx*40, a.Y(p[1]) + (-42 if dx == 0 else 34)
        a.text_px(px_, py_, t1, 14, col, weight="700")
        a.text_px(px_, py_+18, t2, 11.5, C["muted"])
    a.dot((0.0, -0.06), 7.0, fill=C["accent"], stroke="#FFFFFF", w=2.4)
    a.text_px(a.X(0.0), a.Y(-0.06)+24, "HIC", 14, C["accent"], weight="700")
    a.text_px(PW/2, PH-124, "低氫銲條的雙溫陷阱", 14, C["load"], weight="700")
    a.text_px(PW/2, PH-98, f"烘乾 {DRY_T[0]:.0f} ~ {DRY_T[1]:.0f}°C：趕走既有水分",
              13, C["text"])
    a.text_px(PW/2, PH-76, f"保溫筒 {HOLD_T[0]:.0f} ~ {HOLD_T[1]:.0f}°C：隨身攜帶防再吸濕",
              13, C["text"])
    a.text_px(PW/2, PH-46, "兩個溫度都要寫，只寫一個扣一半", 13, C["muted"])

    b = pxcv(PW, PH)
    b.panel("預熱：一招同時破壞三個要素", "所以它是最高 CP 值的對策")
    cxs, cy0 = PW/2, 128
    b.rect_px(cxs-118, cy0, 236, 46, "rgba(180,83,9,0.18)", 10, C["accent"], 2.4)
    b.text_px(cxs, cy0+23, "預熱／層間溫度／後熱", 15, C["accent"], weight="700")
    eff = [("延長高溫停留時間", "讓氫有時間擴散逸出", "→ 打掉氫源", C["load"]),
           ("縮小溫度梯度", "降低收縮拘束", "→ 打掉高拉應力", C["compr"]),
           ("降低冷卻速率", "少生麻田散鐵", "→ 打掉敏感組織", C["bmd"])]
    for i, (t1, t2, t3, col) in enumerate(eff):
        y = cy0 + 78 + i*86
        vdown(b, cxs, y-26, y-6, C["accent"], 2.0)
        b.rect_px(cxs-172, y, 344, 62, C["panel"], 9, C["border"], 1.4)
        b.rect_px(cxs-172, y, 7, 62, col, 3)
        b.text_px(cxs-150, y+17, t1, 13.5, C["text"], "start", weight="700")
        b.text_px(cxs-150, y+37, t2, 12, C["muted"], "start")
        b.text_px(cxs+160, y+31, t3, 12.5, col, "end", weight="700")
    y2 = cy0 + 78 + 3*86
    b.text_px(cxs, y2+4, "預熱溫度依較厚板厚決定（低氫銲條）", 13, C["muted"])
    cells = [("t ≤ 19", f"{preheat(10):.0f}°C"), ("19 ~ 38", f"{preheat(30):.0f}°C"),
             ("38 ~ 65", f"{preheat(50):.0f}°C"), ("t ＞ 65", f"{preheat(80):.0f}°C")]
    cw_ = 108
    for i, (t1, t2) in enumerate(cells):
        x = cxs - 2*cw_ + i*cw_
        b.rect_px(x+3, y2+22, cw_-6, 46, C["fill_m"], 7, C["bmd"], 1.4)
        b.text_px(x+cw_/2, y2+36, t1, 11.5, C["muted"])
        b.text_px(x+cw_/2, y2+55, t2, 14, C["bmd"], weight="700")
    b.text_px(cxs, y2+88, f"板厚 mm；最高層間溫度不得超過 {INTERPASS_MAX:.0f}°C",
              12, C["muted"])

    compose([a, b],
            title="氫致冷裂：三要素模型與預熱這一招",
            sub="冷裂不是銲完就看得到——它是延遲裂縫，常在數小時到數天後才出現",
            note="答題時三要素要一起寫出來，再指出預熱能同時削弱三者；"
                 "只寫「預熱可防裂」而沒寫機制，通常只拿一半分數。",
            path=f"{OUT}/u23-fig-5-hic.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 6　層狀撕裂（Lamellar Tearing）
# ═══════════════════════════════════════════════════════════════
def fig6():
    a = pxcv(PW, PH)
    a.panel("層狀撕裂的機制", "撕裂發生在母材，不是銲道")
    # 翼板（水平厚板）與立板（T 型接頭）
    fy_, fh = 300, 86
    a.rect_px(62, fy_, PW-124, fh, C["fill_c"], 3, C["member"], 1.8)
    a.rect_px(PW/2-22, 150, 44, fy_-150, C["fill_c"], 3, C["member"], 1.8)
    # 軋延方向的夾雜物（平行板面的弱面）
    for k in range(7):
        yy = fy_ + 10 + k*10
        for seg in range(5):
            x0 = 78 + seg*(PW-156)/5
            a.parts.append(f'<line x1="{x0}" y1="{yy}" x2="{x0+(PW-156)/5*0.62}" y2="{yy}" '
                           f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    a.text_px(PW-74, fy_+fh+20, "軋延方向的夾雜物＝平行板面的弱面", 11.5, C["muted"], "end")
    # 撕裂：階梯狀
    steps = [(PW/2-26, fy_+20), (PW/2-26, fy_+30), (PW/2+4, fy_+30),
             (PW/2+4, fy_+50), (PW/2+40, fy_+50), (PW/2+40, fy_+60)]
    a.parts.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in steps) +
                   f'" fill="none" stroke="{C["load"]}" stroke-width="3.2" '
                   f'stroke-linejoin="round"/>')
    a.text_px(PW/2+62, fy_+62, "階梯狀撕裂", 12, C["load"], "start", weight="700")
    # Z 向拉力
    a.arrow(PX(a, PW/2, 176), PX(a, PW/2, 122), C["load"], 3.6, 12)
    a.text_px(PW/2+16, 130, "板厚方向（Z 向）拉力", 12.5, C["load"], "start", weight="700")
    a.text_px(PW/2+16, 150, "來自銲道收縮＋外力", 11.5, C["muted"], "start")
    a.text_px(PW/2-34, 200, "T 型接頭", 12, C["member"], "end", weight="700")
    a.text_px(PW/2, 244, "銲道", 11.5, C["load"])
    for sgn in (-1, 1):
        a.polygon([PX(a, PW/2+sgn*23, fy_), PX(a, PW/2+sgn*23, fy_-30),
                   PX(a, PW/2+sgn*53, fy_)], C["fill_t"], C["load"], 1.6)
    a.text_px(PW/2, PH-96, "鋼板是「軋」出來的，不是「鑄」出來的", 13, C["muted"])
    a.text_px(PW/2, PH-68, "平面內（X、Y）強度足夠，板厚方向（Z）最弱",
              13.5, C["text"], weight="700")
    a.text_px(PW/2, PH-38, "只要 Z 向受拉，就要問「這塊板夠不夠格」",
              13.5, C["load"], weight="700")

    b = pxcv(PW, PH)
    b.panel("觀念陷阱：換銲材救不了", "撕裂在母材，唯一有效的是換鋼材")
    rows = [("✗", "改用更高強度銲條", "撕裂在母材內，銲道強度無關", C["load"], False),
            ("✗", "加大銲腳尺寸", "拘束度反而變高，Z 向拉力更大", C["load"], False),
            ("✗", "加強 UT 檢測", "只能事後發現，不能防止", C["load"], False),
            ("✓", f"採用 SN-C 級鋼材", f"Z 向斷面收縮率 RA ≥ {RA_Z:.0f}%", C["bmd"], True),
            ("✓", "降低接頭拘束度", "改用對稱接頭、減少 Z 向受拉", C["bmd"], True)]
    for i, (mk, t1, t2, col, ok) in enumerate(rows):
        y = 112 + i*66
        b.rect_px(46, y, PW-92, 54, C["fill_m"] if ok else C["panel"], 9,
                  col if ok else C["border"], 2.0 if ok else 1.4)
        if ok:
            tick(b, 74, y+27, 11, col, 3.2)
        else:
            cross(b, 74, y+27, 9, col, 3.0)
        b.text_px(100, y+18, t1, 13.5, C["text"], "start", weight="700")
        b.text_px(100, y+38, t2, 11.5, C["muted"], "start")
    b.rect_px(46, 452, PW-92, 108, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 474, "規範的強制規定", 12.5, C["load"], weight="700")
    b.text_px(PW/2, 500, f"箱型柱內橫隔板等 Z 向受拉接合，", 12.5, C["text"])
    b.text_px(PW/2, 522, f"板厚 t ≥ {T_BOXCOL:.0f} mm 時應採 C 級鋼材", 13, C["text"], weight="700")
    b.text_px(PW/2, 544, "（C 級＝有板厚方向性能保證的等級）", 11.5, C["muted"])

    compose([a, b],
            title="層狀撕裂：唯一「換銲材沒用」的破壞",
            sub="鋼板的弱面平行板面，被 Z 向（板厚方向）拉開就沿弱面撕裂",
            note="這題只要答「換高強度銲條」就等於答錯方向。得分關鍵是先指出撕裂發生在母材，"
                 "再帶出 SN-C 級鋼材的 Z 向斷面收縮率要求。",
            path=f"{OUT}/u23-fig-6-lamellar.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 7　銲腳尺寸上下限與回銲
# ═══════════════════════════════════════════════════════════════
def fig7():
    a = pxcv(PW, PH)
    a.panel("銲腳尺寸為什麼有上下限", "兩個限制的理由完全相反")
    # 上：最小銲腳 —— T 型接頭，厚板抽熱
    y0 = 106
    a.text_px(PW/2, y0, "下限：銲腳太小 → 厚板像散熱片，冷卻過快",
              13, C["compr"], weight="700")
    bp, bt = y0+96, 42                                   # 底板頂面 y、底板厚
    a.rect_px(70, bp, PW-140, bt, C["fill_c"], 3, C["member"], 1.8)
    a.rect_px(PW/2-18, y0+24, 36, bp-(y0+24), C["fill_c"], 3, C["member"], 1.8)
    for sgn in (-1, 1):
        xe = PW/2 + sgn*18
        a.polygon([PX(a, xe, bp), PX(a, xe, bp-16), PX(a, xe+sgn*16, bp)],
                  C["fill_t"], C["load"], 1.8)
    a.text_px(PW/2+58, bp-26, "銲腳偏小", 11.5, C["load"], "start", weight="700")
    for k in range(3):
        a.arrow(PX(a, 150-k*36, bp+6), PX(a, 114-k*36, bp+30), C["compr"], 2.0, 8)
        a.arrow(PX(a, PW-150+k*36, bp+6), PX(a, PW-114+k*36, bp+30), C["compr"], 2.0, 8)
    a.text_px(PW/2, bp+bt+22, "熱被厚板迅速抽走 → 急冷 → 麻田散鐵 → 冷裂",
              11.5, C["muted"])
    a.text_px(PW/2, bp+bt+42, "所以板愈厚，規範要求的最小銲腳愈大",
              12, C["compr"], weight="700")

    # 下：最大銲腳 —— 搭接板緣的兩種畫法
    y1 = 316
    a.text_px(PW/2, y1, "上限：銲腳太大 → 熔蝕板緣，反而削弱母材",
              13, C["load"], weight="700")
    TPX = 52                                             # 上板厚在圖上的像素高
    def lap(x0_, bad):
        top = y1+42
        a.rect_px(x0_, top+TPX, 186, 26, C["fill_c"], 2, C["member"], 1.6)
        a.rect_px(x0_, top, 120, TPX, C["fill_c"], 2, C["member"], 1.6)
        xe = x0_ + 120
        wv = TPX if bad else TPX*(w_max(T_DEMO)/T_DEMO)
        a.polygon([PX(a, xe, top+TPX), PX(a, xe, top+TPX-wv),
                   PX(a, xe+wv, top+TPX)], C["fill_t"], C["load"], 2.0)
        if bad:
            a.parts.append(f'<path d="M {xe-13} {top} a 13 13 0 0 0 13 13" fill="#FFFFFF" '
                           f'stroke="{C["load"]}" stroke-width="2.2"/>')
            cross(a, xe+58, top+10, 9, C["load"], 2.8)
            a.text_px(x0_+93, top-16, "w = t：板緣被熔蝕", 11.5, C["load"], weight="700")
        else:
            a.parts.append(f'<line x1="{xe-16}" y1="{top+TPX-wv}" x2="{xe+4}" '
                           f'y2="{top+TPX-wv}" stroke="{C["bmd"]}" stroke-width="1.6" '
                           f'stroke-dasharray="3 3"/>')
            tick(a, xe+58, top+10, 10, C["bmd"], 2.8)
            a.text_px(x0_+93, top-16, "w = t − 2：留住板緣", 11.5, C["bmd"], weight="700")
    lap(48, True)
    lap(286, False)

    cells = [("最小銲腳 w_{min}", "依較厚板厚：t ≤ 6 → 3；~13 → 5；~19 → 6；再厚 → 8 mm", C["compr"]),
             ("最大銲腳 w_{max}", "t 未達 6 mm：w = t　；　t ≥ 6 mm：w = t − 2 mm", C["load"])]
    for i, (t1, t2, col) in enumerate(cells):
        y = 462 + i*50
        a.rect_px(42, y, PW-84, 42, C["panel"], 8, C["border"], 1.4)
        a.rect_px(42, y, 7, 42, col, 3)
        a.text_px(62, y+13, t1, 12.5, col, "start", weight="700")
        a.text_px(62, y+30, t2, 11, C["text"], "start")
    a.text_px(PW/2, PH-24,
              f"本例 t = {T_DEMO:.0f} mm ⇒ w 必須介於 {w_min(T_DEMO):.0f} ~ {w_max(T_DEMO):.0f} mm",
              13.5, C["accent"], weight="700")

    b = pxcv(PW, PH)
    b.panel("回銲（End Return）", "把應力尖峰與起弧缺陷移離受力端")
    # 上：一般接頭要回銲
    bx, by = 96, 132
    b.rect_px(bx, by, 300, 88, C["fill_c"], 3, C["member"], 1.8)
    b.parts.append(f'<line x1="{bx}" y1="{by+88}" x2="{bx+300}" y2="{by+88}" '
                   f'stroke="{C["load"]}" stroke-width="5"/>')
    b.parts.append(f'<line x1="{bx}" y1="{by+88}" x2="{bx}" y2="{by+50}" '
                   f'stroke="{C["accent"]}" stroke-width="5"/>')
    b.parts.append(f'<line x1="{bx+300}" y1="{by+88}" x2="{bx+300}" y2="{by+50}" '
                   f'stroke="{C["accent"]}" stroke-width="5"/>')
    b.text_px(bx+150, by+108, "主銲道", 12, C["load"], weight="700")
    b.text_px(bx+318, by+62, "回銲", 12, C["accent"], "start", weight="700")
    b.arrow(PX(b, bx+380, by+44), PX(b, bx+308, by+44), C["load"], 2.6, 9)
    b.text_px(bx+300, by+26, "端部應力尖峰", 11.5, C["load"], weight="700")
    b.text_px(PW/2, by+140, f"規範長度：{END_RETURN[0]:.0f}w ≤ ℓ ≤ {END_RETURN[1]:.0f}w",
              14.5, C["accent"], weight="700")
    b.text_px(PW/2, by+164, f"（本例 w = {W_DEMO:.0f} mm ⇒ ℓ = "
                            f"{END_RETURN[0]*W_DEMO:.0f} ~ {END_RETURN[1]*W_DEMO:.0f} mm）",
              12, C["muted"])
    b.text_px(PW/2, by+188, "上下限都是規範明訂，只寫下限不夠", 12, C["muted"])
    # 下：撓性接頭禁止回銲
    b.rect_px(46, 402, PW-92, 158, C["fill_t"], 10, C["load"], 2.0)
    b.text_px(PW/2, 424, "例外：需保持轉動撓性者嚴禁回銲", 13.5, C["load"], weight="700")
    cxx, cyy = 148, 486
    b.rect_px(cxx-16, cyy-52, 12, 104, C["fill_c"], 2, C["member"], 1.6)
    b.rect_px(cxx, cyy-30, 58, 12, C["fill_c"], 2, C["member"], 1.6)
    b.parts.append(f'<line x1="{cxx-4}" y1="{cyy-34}" x2="{cxx-4}" y2="{cyy-14}" '
                   f'stroke="{C["load"]}" stroke-width="4.5"/>')
    b.parts.append(f'<path d="M {cxx+62} {cyy-40} a 26 26 0 0 1 0 24" fill="none" '
                   f'stroke="{C["bmd"]}" stroke-width="2.2"/>')
    b.text_px(cxx+72, cyy-8, "外伸肢需能轉動", 11, C["bmd"], "start")
    b.text_px(cxx+72, cyy+10, "（簡支梁雙角鋼）", 11, C["muted"], "start")
    b.text_px(PW/2, 540, "回銲＝把鉸接焊死 → 端部被迫承受彎矩而拉裂",
              12.5, C["text"], weight="700")

    compose([a, b],
            title="銲腳與回銲：三個都是「幾何」在管冶金",
            sub="最小銲腳管冷卻速率、最大銲腳管熔蝕、回銲管應力尖峰",
            note="回銲那一格最容易漏掉例外：需保持轉動撓性的接頭（簡支梁雙角鋼的外伸肢）嚴禁回銲，"
                 "否則等於把鉸接焊成剛接。",
            path=f"{OUT}/u23-fig-7-weld-size.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 8　NDT 2x2 決策矩陣
# ═══════════════════════════════════════════════════════════════
def fig8():
    W, H = 1180, 560
    cv = pxcv(W, H)
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)
    x0, y0 = 250, 118
    cw_, ch_ = 420, 176
    # 表頭
    cv.rect_px(x0, 56, cw_, 52, C["fill_t"], 10, C["load"], 1.8)
    cv.text_px(x0+cw_/2, 74, "面積型（扁平）", 14.5, C["load"], weight="700")
    cv.text_px(x0+cw_/2, 94, "裂縫・未熔合・未滲透", 11.5, C["muted"])
    cv.rect_px(x0+cw_+16, 56, cw_, 52, C["fill_m"], 10, C["bmd"], 1.8)
    cv.text_px(x0+cw_+16+cw_/2, 74, "體積型（圓胖）", 14.5, C["bmd"], weight="700")
    cv.text_px(x0+cw_+16+cw_/2, 94, "氣孔・夾渣", 11.5, C["muted"])
    # 列頭
    for i, (t1, t2, col) in enumerate([("表面", "肉眼可達", C["compr"]),
                                       ("內部", "藏在銲道裡", C["accent"])]):
        y = y0 + i*(ch_+16)
        cv.rect_px(56, y, 178, ch_, C["panel"], 10, col, 1.8)
        cv.text_px(145, y+ch_/2-12, t1, 17, col, weight="700")
        cv.text_px(145, y+ch_/2+12, t2, 12, C["muted"])
    # 四格內容
    cells = [
        (0, 0, "MT　磁粉探傷", "鐵磁性鋼材：磁力線遇裂縫外漏，聚集磁粉",
         "表面裂縫靈敏度最高", C["load"],
         "PT　液滲：非磁性材（不鏽鋼）改用這個"),
        (0, 1, "VT　目視檢測", "肉眼＋量規：銲腳、餘高、咬邊、外觀氣孔",
         "所有銲道的無條件基線", C["bmd"],
         "最便宜也最常被低估的一關"),
        (1, 0, "UT　超音波", "聲波遇扁平缺陷大面積反射 → 回波強",
         "對未熔合與裂縫最靈敏", C["load"],
         "CJP 與耐震梁柱接頭：100% 全數檢測"),
        (1, 1, "RT　放射線", "射線穿透量隨密度差變化 → 底片黑影",
         "對氣孔、夾渣最清楚", C["bmd"],
         "扁平裂縫若與射線不平行則可能漏檢"),
    ]
    for r, c_, name, how, why, col, extra in cells:
        x = x0 + c_*(cw_+16)
        y = y0 + r*(ch_+16)
        cv.rect_px(x, y, cw_, ch_, C["panel"], 10, C["border"], 1.4)
        cv.rect_px(x, y, cw_, 6, col, 3)
        cv.text_px(x+24, y+34, name, 16, col, "start", weight="700")
        cv.text_px(x+24, y+64, how, 12.5, C["text"], "start")
        cv.text_px(x+24, y+90, why, 12.5, col, "start", weight="700")
        cv.rect_px(x+18, y+108, cw_-36, 48, "#FFFFFF", 7, C["border"], 1.2)
        cv.text_px(x+cw_/2, y+132, extra, 11.5, C["muted"])
    cv.text_px(W/2, H-32, "不必死記表格：先問「在表面還是內部」，再問「扁的還是圓的」，四格自然定位",
               14, C["text"], weight="700")

    compose([cv],
            title="NDT 不用背表：位置 × 形狀 的 2×2 決策矩陣",
            sub="位置決定看得到看不到，形狀決定用聲波還是射線",
            note="全滲透銲（CJP）與耐震梁柱接頭最怕的是內部面積型缺陷（未熔合），"
                 "所以規範指定 100% UT 全數檢測，不是抽驗。",
            path=f"{OUT}/u23-fig-8-ndt-matrix.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 9　高拉力螺栓：預拉力與轉角法
# ═══════════════════════════════════════════════════════════════
def fig9():
    Pmax = FU_B*AS_B/1000.0                      # kN 抗拉極限
    a, fx, fy, P = plotbox(PW, PH, (0, 1.0), (0, Pmax*1.15), (104, PW-70, 224, 486))
    a.panel("螺栓的軸力 — 伸長量曲線", f"A325 M22：A_{{s}} = {AS_B:.0f} mm^{{2}}")
    axis_frame(a, fx(0), fx(1.0), fy(0), fy(Pmax*1.15), "伸長量／轉角", "")
    # 曲線：彈性 → 降伏平台 → 頸縮斷裂
    def curve(x):
        if x <= 0.30:  return FYAS*x/0.30
        if x <= 0.74:  return FYAS + (Pmax-FYAS)*(1-math.exp(-(x-0.30)/0.16))
        return Pmax*(1 - 1.9*(x-0.74)**2)
    pts = [P(x, curve(x)) for x in [i/200 for i in range(int(0.92*200)+1)]]
    a.poly(pts, C["member"], 3.6)
    a.dot(P(0.92, curve(0.92)), 6.2, fill=C["load"], stroke="#FFFFFF", w=2.2)
    a.text_px(fx(0.92)+8, PH-fy(curve(0.92))-4, "斷裂", 12, C["load"], "start", weight="700")
    # 降伏與預拉力水平線
    a.line(P(0, FYAS), P(1.0, FYAS), C["compr"], 1.8, dash="6 5")
    a.text_px(fx(1.0), PH-fy(FYAS)-14, f"F_{{y}}A_{{s}} = {FYAS:.0f} kN",
              12, C["compr"], "end", weight="700")
    a.line(P(0, TB), P(1.0, TB), C["accent"], 1.8, dash="6 5")
    a.text_px(fx(1.0), PH-fy(TB)+15, f"T_{{b}} = 0.7F_{{u}}A_{{s}} = {TB:.0f} kN",
              12, C["accent"], "end", weight="700")
    xtb = 0.30*TB/FYAS
    a.dot(P(xtb, TB), 6.0, fill=C["accent"], stroke="#FFFFFF", w=2.2)
    a.text_px(fx(xtb)-16, PH-fy(TB), "規範最小預拉力", 11.5, C["accent"], "end", weight="700")
    # 塑性平台標示（畫在曲線上方，避免壓到曲線）
    ybar = PH - fy(Pmax*1.06)
    a.parts.append(f'<line x1="{fx(0.40):.1f}" y1="{ybar:.1f}" x2="{fx(0.82):.1f}" '
                   f'y2="{ybar:.1f}" stroke="{C["accent"]}" stroke-width="2.2"/>')
    for xx, d in ((fx(0.40), 1), (fx(0.82), -1)):
        a.parts.append(f'<polygon points="{xx:.1f},{ybar:.1f} {xx+9*d:.1f},{ybar-5:.1f} '
                       f'{xx+9*d:.1f},{ybar+5:.1f}" fill="{C["accent"]}"/>')
    a.text_px((fx(0.40)+fx(0.82))/2, ybar-16, "塑性平台：轉角法的操作區",
              12.5, C["accent"], weight="700")
    a.text_px(PW/2, PH-104,
              f"T_{{b}} 落在降伏的 {TB_OVER_FY*100:.0f}%（0.7F_{{u}}A_{{s}} ≈ 0.88F_{{y}}A_{{s}}）",
              13.5, C["accent"], weight="700")
    a.text_px(PW/2, PH-80, "剛好踩在降伏邊緣：進入平台後，", 12.5, C["muted"])
    a.text_px(PW/2, PH-58, "多轉一點角度，軸力增加有限，不致拉斷", 12.5, C["text"], weight="700")
    a.text_px(PW/2, PH-30, "→ 這就是「轉角法」能成立的物理理由", 13, C["compr"], weight="700")

    b = pxcv(PW, PH)
    b.panel("為什麼螺栓絕對不能重複使用", "兩種鎖固法的起算點都失準")
    b.rect_px(46, 108, PW-92, 176, C["fill_m"], 10, C["bmd"], 1.8)
    b.text_px(PW/2, 130, "第一次鎖固", 13.5, C["bmd"], weight="700")
    for i, (t1, t2) in enumerate([("扭矩法", "靠 K 值換算：T = K·d·T_{b}"),
                                  ("轉角法", "初鎖後再轉固定角度")]):
        y = 156 + i*58
        b.rect_px(66, y, PW-132, 46, "#FFFFFF", 7, C["border"], 1.2)
        b.text_px(86, y+23, t1, 12.5, C["bmd"], "start", weight="700")
        b.text_px(176, y+23, t2, 11.5, C["text"], "start")
    b.text_px(PW/2, 268, "兩種方法都會把螺栓續鎖進塑性平台", 12, C["muted"])
    vdown(b, PW/2, 288, 312, C["load"], 2.6)
    b.text_px(PW/2, 330, "螺栓產生永久塑性伸長", 13.5, C["load"], weight="700")
    vdown(b, PW/2, 344, 368, C["load"], 2.6)
    b.rect_px(46, 378, PW-92, 132, C["fill_t"], 10, C["load"], 1.8)
    for i, (t1, t2) in enumerate([("扭矩係數 K 值失準",
                                   "螺紋已塑變、潤滑層破壞 → 同樣扭矩鎖不到同樣軸力"),
                                  ("轉角法起算點失準",
                                   "已無彈性段可走，轉同樣角度可能直接拉斷")]):
        y = 396 + i*54
        b.text_px(70, y, t1, 12.5, C["load"], "start", weight="700")
        b.text_px(70, y+20, t2, 11, C["text"], "start")
    b.text_px(PW/2, 534, "二次夾緊力不可控 ⇒ 摩擦力假設整個失效", 13, C["load"], weight="700")
    b.text_px(PW/2, 560, "（承壓型連接的螺栓亦同，規範一律禁止重複使用）", 11.5, C["muted"])

    compose([a, b],
            title="高拉力螺栓：預拉力為什麼定在 0.7Fu",
            sub="它剛好踩在降伏邊緣的塑性平台上，讓轉角法可行、又不會拉斷",
            note="答「重複使用會失去預拉力」只講了一半；完整理由是螺栓已永久塑性伸長，"
                 "扭矩係數 K 與轉角法起算點雙雙失準，二次夾緊力不可控。",
            path=f"{OUT}/u23-fig-9-bolt-pretension.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 10　摩阻面與塗裝
# ═══════════════════════════════════════════════════════════════
def fig10():
    a = pxcv(PW, PH)
    a.panel("摩阻型 vs 承壓型：力從哪裡走", "兩者對「表面」的要求完全不同")
    def joint(y0, slip):
        col = C["bmd"] if slip else C["accent"]
        a.rect_px(74, y0, 200, 30, C["fill_c"], 3, C["member"], 1.6)
        a.rect_px(174, y0+30, 200, 30, C["fill_c"], 3, C["member"], 1.6)
        # 螺栓
        a.rect_px(216, y0-14, 16, 88, "rgba(107,118,132,0.35)", 3, C["member"], 1.6)
        a.arrow(PX(a, 62, y0+15), PX(a, 100, y0+15), C["load"], 2.8, 9)
        a.arrow(PX(a, 386, y0+45), PX(a, 348, y0+45), C["load"], 2.8, 9)
        if slip:
            for k in range(5):
                xx = 186 + k*18
                a.parts.append(f'<line x1="{xx}" y1="{y0+30}" x2="{xx+10}" y2="{y0+30}" '
                               f'stroke="{col}" stroke-width="3.4"/>')
            a.text_px(400, y0+14, "夾緊力 × μ", 11.5, col, "start", weight="700")
            a.text_px(400, y0+32, "＝摩擦力傳遞", 11.5, C["muted"], "start")
            a.arrow(PX(a, 224, y0-24), PX(a, 224, y0+4), col, 2.4, 8)
            a.arrow(PX(a, 224, y0+84), PX(a, 224, y0+56), col, 2.4, 8)
        else:
            a.parts.append(f'<path d="M {216} {y0+30} l -8 0" stroke="{col}" stroke-width="4"/>')
            a.rect_px(206, y0+22, 36, 16, "rgba(180,83,9,0.30)", 3, col, 1.8)
            a.text_px(400, y0+14, "螺栓桿承壓", 11.5, col, "start", weight="700")
            a.text_px(400, y0+32, "＋斷面剪力", 11.5, C["muted"], "start")
    a.text_px(PW/2, 112, "摩阻型（Slip-critical）", 13.5, C["bmd"], weight="700")
    joint(140, True)
    a.text_px(PW/2, 252, "表面狀態＝強度本身，嚴禁塗裝", 12, C["bmd"], weight="700")
    a.text_px(PW/2, 306, "承壓型（Bearing）", 13.5, C["accent"], weight="700")
    joint(334, False)
    a.text_px(PW/2, 446, "已容許滑動，表面狀態不影響強度", 12, C["accent"], weight="700")
    a.rect_px(46, 476, PW-92, 92, C["panel"], 10, C["border"], 1.4)
    a.text_px(PW/2, 498, "所以「不予塗裝」只對摩阻面是強制的", 12.5, C["text"], weight="700")
    a.text_px(PW/2, 522, "另一個常考的不塗裝範圍：", 12, C["muted"])
    a.text_px(PW/2, 546, "工地銲接處，相鄰兩側各 100 mm 不予塗裝", 12.5, C["load"], weight="700")

    b = pxcv(PW, PH)
    b.panel("塗裝讓滑動係數崩掉", f"φR_{{n}} = φ·μ·D_{{u}}·h_{{sc}}·T_{{b}}·n_{{s}}")
    x0, xlim = 176, PW-96
    caps = [slip_cap(mu) for _, mu, _ in MU_CASES]
    lim = max(caps)*1.12
    ytop, bh, gap = 158, 52, 40
    for i, ((name, mu, col), cap) in enumerate(zip(MU_CASES, caps)):
        y = ytop + i*(bh+gap)
        bw_ = (xlim-x0)*cap/lim
        b.rect_px(x0, y, bw_, bh, C["fill_t"] if i == 2 else C["fill_m"], 6, col, 2.0)
        b.text_px(x0-14, y+18, name, 12, C["text"], "end", weight="700")
        b.text_px(x0-14, y+38, f"μ = {mu:.2f}", 12.5, col, "end", weight="700")
        b.text_px(x0+bw_-10, y+bh/2, f"{cap:.1f} kN", 13.5, col, "end", weight="700")
    b.text_px((x0+xlim)/2, ytop-24, "單一螺栓的設計滑動強度", 12.5, C["muted"])
    b.text_px(PW/2, 404, f"T_{{b}} = {TB:.0f} kN、D_{{u}} = {DU:.2f}、標準孔 h_{{sc}} = "
                         f"{HSC:.2f}、單剪面", 11.5, C["muted"])
    b.rect_px(46, 428, PW-92, 140, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 450, "為什麼摩阻面嚴禁塗裝", 13, C["load"], weight="700")
    for i, s in enumerate([f"油漆使 μ 從 Class A 的 0.33 掉到 0.15 上下",
                           f"設計滑動強度只剩 Class A 的 {caps[2]/caps[1]*100:.0f}%，直接砍半",
                           "規範未經認證的塗裝面不得作為摩阻面",
                           "摩阻面若已誤塗，必須噴砂重做而非補鎖"]):
        b.text_px(PW/2, 476 + i*22, s, 11.5, C["text"])

    compose([a, b],
            title="高拉力螺栓的第二個關鍵：摩阻面的表面狀態",
            sub="摩阻型連接的強度直接正比於滑動係數，塗裝等於把設計假設拿掉",
            note="μ 的數值各版規範略有差異（Class A 約 0.33、Class B 約 0.50），"
                 "塗裝面的 0.15 為量級參考；答題重點是「正比關係」與「規範禁止」，不是背小數點。",
            path=f"{OUT}/u23-fig-10-slip.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 11　防蝕：拆除原電池
# ═══════════════════════════════════════════════════════════════
def fig11():
    a, fx, fy, P = plotbox(PW, PH, (0, 1.0), (-1.0, 0.6), (150, PW-118, 200, 500))
    a.panel("電位階梯：誰當陽極誰先溶", "標準電極電位（V vs SHE）")
    a.line(P(0, 0.6), P(0, -1.0), C["muted"], 1.8)
    metals = [("Cu 銅", E_CU, C["accent"]), ("Fe 鋼", E_FE, C["member"]), ("Zn 鋅", E_ZN, C["bmd"])]
    for name, e, col in metals:
        yy = PH - fy(e)
        a.parts.append(f'<line x1="{fx(0)-14}" y1="{yy}" x2="{fx(0.94)}" y2="{yy}" '
                       f'stroke="{col}" stroke-width="2.6"/>')
        a.text_px(fx(0)-22, yy, name, 13, col, "end", weight="700")
        a.text_px(fx(0.96), yy-13, f"{e:+.2f} V", 12.5, col, "end", weight="700")
    a.text_px(fx(0.48), PH-fy(0.52), "電位愈負 → 愈容易失去電子 → 當陽極", 11.5, C["muted"])
    # 鋅 → 鐵 的保護方向
    y_zn, y_fe = PH-fy(E_ZN), PH-fy(E_FE)
    a.parts.append(f'<line x1="{fx(0.72)}" y1="{y_zn}" x2="{fx(0.72)}" y2="{y_fe+12}" '
                   f'stroke="{C["bmd"]}" stroke-width="2.4"/>')
    a.parts.append(f'<polygon points="{fx(0.72)},{y_fe} {fx(0.72)-5.4},{y_fe+11} '
                   f'{fx(0.72)+5.4},{y_fe+11}" fill="{C["bmd"]}"/>')
    a.text_px(fx(0.70)-10, (y_zn+y_fe)/2, "鋅優先當陽極溶解", 11.5, C["bmd"], "end", weight="700")
    a.text_px(fx(0.70)-10, (y_zn+y_fe)/2+18, "鋼被迫當陰極 → 不生鏽", 11, C["muted"], "end")
    a.text_px(PW/2, PH-82, "腐蝕＝一顆自然形成的原電池", 13.5, C["text"], weight="700")
    a.text_px(PW/2, PH-58, "陽極（失電子、溶解）＋陰極＋電解液＋導電迴路",
              12, C["muted"])
    a.text_px(PW/2, PH-30, "防蝕就是把這四個要素之一拆掉", 13, C["load"], weight="700")

    b = pxcv(PW, PH)
    b.panel("塗層被劃傷之後", "這一刀決定兩種防蝕法的高下")
    def scene(y0, zinc):
        col = C["bmd"] if zinc else C["load"]
        b.rect_px(64, y0+42, PW-128, 44, C["fill_c"], 2, C["member"], 1.6)
        b.rect_px(64, y0+34, PW-128, 8, "rgba(46,125,111,0.45)" if zinc
                  else "rgba(192,57,43,0.40)", 2)
        # 劃傷
        b.parts.append(f'<path d="M {PW/2-6} {y0+34} l 6 14 l 6 -14" fill="#FFFFFF" '
                       f'stroke="{C["member"]}" stroke-width="1.6"/>')
        b.text_px(PW/2, y0+18, "劃傷", 11.5, C["muted"])
        if zinc:
            for k in range(4):
                r = 14 + k*11
                b.parts.append(f'<path d="M {PW/2-r} {y0+48} A {r} {r*0.7} 0 0 1 '
                               f'{PW/2+r} {y0+48}" fill="none" stroke="{col}" '
                               f'stroke-width="1.4" stroke-dasharray="4 4" opacity="0.7"/>')
            b.text_px(PW/2, y0+104, "鋅在傷口周圍犧牲溶解 → 保護半徑內鋼材不鏽",
                      11.5, col, weight="700")
        else:
            for k, dx in enumerate((-46, -26, 0, 26, 46)):
                b.parts.append(f'<circle cx="{PW/2+dx}" cy="{y0+54+abs(dx)*0.12}" '
                               f'r="{7-abs(dx)*0.06:.1f}" fill="rgba(192,57,43,0.35)" '
                               f'stroke="{col}" stroke-width="1.3"/>')
            b.text_px(PW/2, y0+104, "鏽從傷口往兩側鑽入塗層下方 → 保護歸零",
                      11.5, col, weight="700")
    b.text_px(PW/2, 112, "① 油漆塗裝：純物理屏障", 13.5, C["load"], weight="700")
    scene(126, False)
    b.text_px(PW/2, 288, "② 熱浸鍍鋅：屏障 ＋ 犧牲陽極", 13.5, C["bmd"], weight="700")
    scene(302, True)
    b.rect_px(46, 436, PW-92, 136, C["fill_m"], 10, C["bmd"], 1.8)
    b.text_px(PW/2, 458, "答題關鍵：兩者的保護「機制」不同層次", 12.5, C["bmd"], weight="700")
    for i, s in enumerate(["油漆：只要膜完整就有效，膜一破保護即歸零",
                           f"鍍鋅：物理屏障之外，還有電化學保護",
                           f"鋅 {E_ZN:+.2f} V 比鐵 {E_FE:+.2f} V 更負 → 鋅先溶解",
                           "所以鍍鋅層有「保護半徑」，油漆沒有"]):
        b.text_px(PW/2, 484 + i*22, s, 11.5, C["text"])

    compose([a, b],
            title="防蝕：油漆與鍍鋅差在「膜破掉之後」",
            sub="一個是純物理屏障，一個多了犧牲陽極的電化學保護",
            note="常被漏掉的施工細節：高拉力螺栓摩阻面與工地銲接處（相鄰兩側各 100 mm）"
                 "不予塗裝，等銲接與鎖固完成後再補塗。",
            path=f"{OUT}/u23-fig-11-corrosion.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 12　節點域：剪力降伏 vs 剪力挫屈
# ═══════════════════════════════════════════════════════════════
def fig12():
    a = pxcv(PW, PH)
    a.panel("節點域（Panel Zone）的幾何", "梁柱交會處那一塊柱腹板")
    ccx, ccy = PW/2, 250
    pw_, ph_ = 150, 190                      # 圖上的節點域寬高（像素）
    # 柱
    a.rect_px(ccx-pw_/2-16, 116, 16, 268, C["fill_c"], 2, C["member"], 1.6)
    a.rect_px(ccx+pw_/2, 116, 16, 268, C["fill_c"], 2, C["member"], 1.6)
    a.rect_px(ccx-pw_/2, 116, pw_, 268, "rgba(107,118,132,0.10)", 2, C["border"], 1.2)
    # 梁
    a.rect_px(ccx-pw_/2-120, ccy-ph_/2, 120, 13, C["fill_c"], 2, C["member"], 1.6)
    a.rect_px(ccx-pw_/2-120, ccy+ph_/2-13, 120, 13, C["fill_c"], 2, C["member"], 1.6)
    a.rect_px(ccx+pw_/2, ccy-ph_/2, 120, 13, C["fill_c"], 2, C["member"], 1.6)
    a.rect_px(ccx+pw_/2, ccy+ph_/2-13, 120, 13, C["fill_c"], 2, C["member"], 1.6)
    # 節點域本體
    a.rect_px(ccx-pw_/2, ccy-ph_/2, pw_, ph_, C["fill_s"], 2, C["sfd"], 2.4)
    a.text_px(ccx, ccy-16, "節點域", 13.5, C["sfd"], weight="700")
    a.text_px(ccx, ccy+6, "厚度 t_{z}", 12.5, C["sfd"], weight="700")
    a.dim((ccx-pw_/2, PH-(ccy+ph_/2)), (ccx+pw_/2, PH-(ccy+ph_/2)), "w_{z}", off=30, size=13.5)
    a.dim((ccx+pw_/2, PH-(ccy+ph_/2)), (ccx+pw_/2, PH-(ccy-ph_/2)), "d_{z}", off=34, size=13.5)
    a.text_px(ccx-pw_/2-64, ccy-ph_/2-14, "梁", 12, C["muted"])
    a.text_px(ccx, 106, "柱", 12, C["muted"])
    a.text_px(PW/2, 424, f"d_{{z}} = 梁深 − 梁翼板厚 = {DZ:.0f} mm", 12.5, C["text"])
    a.text_px(PW/2, 446, f"w_{{z}} = 柱深 − 柱翼板厚 = {WZ:.0f} mm", 12.5, C["text"])
    a.rect_px(56, 468, PW-112, 100, C["fill_s"], 10, C["sfd"], 1.8)
    a.text_px(PW/2, 490, "規範的最小厚度規定", 12.5, C["sfd"], weight="700")
    a.text_px(PW/2, 514, "t_{z} ≥ (d_{z} + w_{z}) / 90", 16, C["sfd"], weight="700")
    a.text_px(PW/2, 540, f"本例 = ({DZ:.0f} + {WZ:.0f}) / 90 = {TZ_REQ:.1f} mm",
              12.5, C["text"], weight="700")
    a.text_px(PW/2, 558, f"柱腹板 t_{{w}} = {TWC:.0f} mm ＞ {TZ_REQ:.1f} mm，OK",
              11.5, C["bmd"], weight="700")

    b = pxcv(PW, PH)
    b.panel("分母 90 在擋什麼", "一個防剪力挫屈的寬厚比門檻")
    def hyst(x0, y0, w_, h_, n, eps, col, title, sub):
        b.rect_px(x0, y0, w_, h_, "#FFFFFF", 8, C["border"], 1.3)
        cx_, cy_ = x0+w_/2, y0+h_/2
        b.parts.append(f'<line x1="{x0+10}" y1="{cy_}" x2="{x0+w_-10}" y2="{cy_}" '
                       f'stroke="{C["muted"]}" stroke-width="1.2"/>')
        b.parts.append(f'<line x1="{cx_}" y1="{y0+8}" x2="{cx_}" y2="{y0+h_-8}" '
                       f'stroke="{C["muted"]}" stroke-width="1.2"/>')
        A, B_ = w_*0.36, h_*0.36
        pts = []
        for i in range(161):
            th = 2*math.pi*i/160
            sn, cs = math.sin(th), math.cos(th)
            wgt = ((abs(sn)+eps)/(1.0+eps))**n
            pts.append(f"{cx_+A*sn:.1f},{cy_-B_*(0.62*sn + 0.60*cs*wgt):.1f}")
        b.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" '
                       f'stroke-width="2.6" stroke-linejoin="round"/>')
        b.text_px(cx_, y0-16, title, 13, col, weight="700")
        b.text_px(cx_, y0+h_+18, sub, 11, C["muted"])
        b.text_px(x0+w_-8, cy_-9, "γ", 11.5, C["muted"], "end")
        b.text_px(cx_+10, y0+14, "V", 11.5, C["muted"], "start")
    hyst(58, 150, 180, 150, 0.18, 0.55, C["bmd"], "剪力降伏", "滯迴飽滿．能耗能")
    hyst(282, 150, 180, 150, 3.4, 0.015, C["load"], "剪力挫屈", "捏縮．幾乎不耗能")
    b.text_px(PW/2, 336, "節點域是耐震設計裡「刻意讓它降伏」的元件",
              13, C["text"], weight="700")
    rows = [("腹板夠厚", "先發生剪力降伏 → 延性、穩定、可反覆耗能", C["bmd"]),
            ("腹板過薄", "先發生剪力挫屈 → 無延性的穩定性破壞", C["load"])]
    for i, (t1, t2, col) in enumerate(rows):
        y = 364 + i*58
        b.rect_px(46, y, PW-92, 46, C["panel"], 8, C["border"], 1.4)
        b.rect_px(46, y, 7, 46, col, 3)
        b.text_px(66, y+15, t1, 12.5, col, "start", weight="700")
        b.text_px(66, y+33, t2, 11.5, C["text"], "start")
    b.rect_px(46, 488, PW-92, 80, "rgba(124,58,237,0.13)", 10, C["sfd"], 1.8)
    b.text_px(PW/2, 510, "所以分母 90 不是經驗係數", 12.5, C["sfd"], weight="700")
    b.text_px(PW/2, 532, "它是一個幾何寬厚比限制，", 11.5, C["text"])
    b.text_px(PW/2, 552, "把破壞模式從「挫屈」逼回「降伏」", 11.5, C["text"], weight="700")

    compose([a, b],
            title="節點域最小厚度：分母 90 是寬厚比，不是經驗值",
            sub="耐震設計要節點域靠剪力降伏耗能，就必須先杜絕剪力挫屈",
            note="示範採梁 H600x200x11x17、柱 H400x400x13x21；改斷面時圖上數字會自動重算。"
                 "腹板不足時的常見對策是加設加勁板（doubler plate）補厚。",
            path=f"{OUT}/u23-fig-12-panel-zone.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 13　容量設計：為什麼「材料太強」反而危險
# ═══════════════════════════════════════════════════════════════
def fig13():
    def frame(cv, hinge_at_beam):
        """門型接頭立面：柱＋梁，標出塑鉸位置。"""
        cx_, base_ = W3/2, 300
        cv.rect_px(cx_-13, 132, 26, base_-132, C["fill_c"], 2, C["member"], 1.8)
        cv.rect_px(cx_+13, 232, 116, 22, C["fill_c"], 2, C["member"], 1.8)
        cv.rect_px(cx_-129, 232, 116, 22, C["fill_c"], 2, C["member"], 1.8)
        cv.parts.append(f'<line x1="{cx_-13}" y1="{228}" x2="{cx_-13}" y2="{258}" '
                        f'stroke="{C["load"]}" stroke-width="4"/>')
        cv.parts.append(f'<line x1="{cx_+13}" y1="{228}" x2="{cx_+13}" y2="{258}" '
                        f'stroke="{C["load"]}" stroke-width="4"/>')
        cv.text_px(cx_, 118, "柱", 11.5, C["muted"])
        cv.text_px(cx_-92, 216, "梁", 11.5, C["muted"])
        if hinge_at_beam:
            for sgn in (-1, 1):
                cv.dot(PX(cv, cx_+sgn*52, 243), 11, fill="rgba(46,125,111,0.35)",
                       stroke=C["bmd"], w=2.6)
            cv.text_px(cx_, 322, "塑鉸長在梁端", 12.5, C["bmd"], weight="700")
            cv.text_px(cx_, 342, "（設計希望的位置）", 11, C["muted"])
        else:
            cv.dot(PX(cv, cx_, 196), 11, fill="rgba(192,57,43,0.32)", stroke=C["load"], w=2.6)
            cv.dot(PX(cv, cx_, 286), 11, fill="rgba(192,57,43,0.32)", stroke=C["load"], w=2.6)
            cross(cv, cx_-13, 243, 8, C["load"], 3.0)
            cross(cv, cx_+13, 243, 8, C["load"], 3.0)
            cv.text_px(cx_, 322, "塑鉸被推到柱端", 12.5, C["load"], weight="700")
            cv.text_px(cx_, 342, "接頭銲道先破壞", 11, C["load"])

    a = pxcv(W3, H3)
    a.panel("材料強度正常", "梁先降伏，構架有延性")
    frame(a, True)
    for i, s in enumerate(["梁端塑鉸可反覆彎曲耗能",
                           "柱與接頭始終保持彈性",
                           "破壞有預警、可修復"]):
        bullet(a, 26, 376 + i*28, s, C["bmd"], 12)
    a.text_px(W3/2, H3-24, "強柱弱梁　＝　容量設計", 13.5, C["bmd"], weight="700")

    b = pxcv(W3, H3)
    b.panel("梁的實際 F_{y} 過高", "梁不肯降伏，力量往上游跑")
    frame(b, False)
    for i, s in enumerate(["梁太強 → 傳出的力遠高於設計值",
                           "柱與接頭沒有延性儲備",
                           "銲道脆性破壞、無預警"]):
        bullet(b, 26, 376 + i*28, s, C["load"], 12)
    b.text_px(W3/2, H3-24, "「材料變強」反而讓結構變脆", 13.5, C["load"], weight="700")

    # --- c：降伏比的應力應變意義 ---
    c, fx, fy, P = plotbox(W3, H3, (0, 1.0), (0, 1.25), (56, W3-54, 158, 350))
    c.panel("所以規範管 F_{y} 的上限", f"並要求降伏比 F_{{y}}/F_{{u}} ≤ {YR_LIMIT:.2f}")
    axis_frame(c, fx(0), fx(1.0), fy(0), fy(1.25), "ε", "σ")
    def ss(x, yr):
        fyv = yr
        if x <= 0.06: return fyv*x/0.06
        if x <= 0.06 + (1-yr)*0.9: return fyv
        return min(1.0, fyv + (1.0-fyv)*(1-math.exp(-(x-0.06-(1-yr)*0.9)/0.16)))
    for yr, col, lab, xl, dy in ((0.66, C["bmd"], "YR = 0.66", 0.44, 20),
                                 (0.95, C["load"], "YR = 0.95", 0.30, -14)):
        pts = [P(x, ss(x, yr)) for x in [i/200 for i in range(181)]]
        c.poly(pts, col, 3.0)
        c.text_px(fx(xl), H3-fy(ss(xl, yr))+dy, lab, 11.5, col, weight="700")
    c.line(P(0, 1.0), P(1.0, 1.0), C["muted"], 1.4, dash="5 4")
    c.text_px(fx(0.02), H3-fy(1.0)-11, "F_{u}", 11.5, C["muted"], "start")
    c.text_px(W3/2, 372, "降伏比低 → 降伏後還有長長的加工硬化段",
              11.5, C["bmd"], weight="700")
    c.text_px(W3/2, 392, "降伏比高 → 一降伏就接近極限，塑性行程短",
              11.5, C["load"], weight="700")
    c.rect_px(22, 408, W3-44, 52, C["fill_m"], 9, C["bmd"], 1.6)
    c.text_px(W3/2, 426, f"SN 鋼材同時管制 F_{{y}} 上限", 11.5, C["text"], weight="700")
    c.text_px(W3/2, 446, f"與降伏比 F_{{y}}/F_{{u}} ≤ {YR_LIMIT:.2f}", 11.5, C["text"], weight="700")

    compose([a, b, c],
            title="耐震加嚴：為什麼規範「不准材料太強」",
            sub="容量設計要求塑鉸只能長在梁端 —— 梁太強，力量就往柱與銲道跑",
            note="這是最違反直覺的一條：一般構材只管強度下限，耐震構材連上限都要管。"
                 "SN 鋼材同時管制 Fy 上限、降伏比與 CVN 韌性，三者缺一不可。",
            path=f"{OUT}/u23-fig-13-capacity-design.svg")


if __name__ == "__main__":
    for i in range(1, 14):
        globals()[f"fig{i}"]()
    print(f"generated 13 figures into {OUT}/")
