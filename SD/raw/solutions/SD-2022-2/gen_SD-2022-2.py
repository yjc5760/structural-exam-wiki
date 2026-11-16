#!/usr/bin/env python3
"""SD-2022-2 解題圖解（struct-diagram；2026-11-16，組 U3-1-G2 階段 E）
fig-1 特殊抗彎矩構架梁的閉合箍筋區、間距與搭接禁區（立面）＋梁寬上限（平面），數值取自 §5.1 示例
（柱 c1＝c2＝60 cm、梁 h＝70 cm、d＝64 cm、主筋 D25），條文為 112 年版混凝土規範 18.3.2–18.3.4。
用法：python3 gen_SD-2022-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, FONT, esc
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2022-2"
# ── §5.1 示例（cm）──
C1 = C2 = 60.0; H = 70.0; D = 64.0; DB = 2.54; LN = 560.0
S_HOOP = min(D/4, 6*DB, 15.0)          # 18.3.4.4 → 15
S_MID = D/2                            # 18.3.4.6 → 32
S_LAP = min(D/4, 10.0)                 # 18.3.3.3 → 10
Z = 2*H                                # 18.3.4.1、18.3.3.3 → 140
FIRST = 5.0                            # 第一道 ≤ 5 cm
BW_MAX = C2 + 2*min(C2, 0.75*C1)       # 18.3.2.1(c) → 150
BW_OLD = C2 + 1.5*H                    # 舊式 → 165
ZOLD = 2*D                             # 舊解誤記 2d → 128

def elevation():
    W, Hc = 1100, 450
    cv = fit(W, Hc, (-C1 - 30, LN + C1 + 30), (-150, 200), L=20, R=20, T=60, B=20)
    cv.panel("(a) 立面：閉合箍筋區與搭接禁區（2h，不是 2d）")
    y0, y1 = 0.0, H
    for xc in (-C1, LN):                                       # 柱
        cv.polygon([(xc, -120), (xc + C1, -120), (xc + C1, 190), (xc, 190)], "#E4E7EC", C["member"], 2.0)
    cv.polygon([(0, y0), (LN, y0), (LN, y1), (0, y1)], "#FFFFFF", C["member"], 2.4)  # 梁
    # 搭接禁區（含接頭內）：淡紅底
    for a, b in ((-C1, Z), (LN - Z, LN + C1)):
        cv.polygon([(a, y1 + 8), (b, y1 + 8), (b, y1 + 30), (a, y1 + 30)], C["fill_t"], C["load"], 1.2)
    cv.text(((-C1 + Z)/2, y1 + 19), "禁止搭接", 13, C["load"])
    cv.text(((LN - Z + LN + C1)/2, y1 + 19), "禁止搭接", 13, C["load"])
    cv.polygon([(Z, y1 + 8), (LN - Z, y1 + 8), (LN - Z, y1 + 30), (Z, y1 + 30)], C["fill_m"], C["bmd"], 1.2)
    cv.text((LN/2, y1 + 19), f"可搭接（搭接段閉合箍筋 s ≤ {S_LAP:g} cm）", 12.5, C["bmd"])
    # 箍筋
    xs = []
    x = FIRST
    while x <= Z + 1e-9: xs.append(x); x += S_HOOP
    x = Z + S_MID
    while x < LN - Z - 1e-9: xs.append(x); x += S_MID
    x = LN - FIRST
    right = []
    while x >= LN - Z - 1e-9: right.append(x); x -= S_HOOP
    xs += right
    for xx in xs:
        dense = xx <= Z + 1e-9 or xx >= LN - Z - 1e-9
        cv.line((xx, y0 + 5), (xx, y1 - 5), C["deform"] if dense else C["member2"], 1.6 if dense else 1.3)
    # 尺寸
    cv.dim((0, y0), (Z, y0), f"2h = {Z:g} cm", off=26, label_off=14, color=C["accent"])
    cv.dim((LN - Z, y0), (LN, y0), f"2h = {Z:g} cm", off=26, label_off=14, color=C["accent"])
    cv.dim((0, y0), (ZOLD, y0), f"2d = {ZOLD:g} cm", off=62, label_off=14, color=C["muted"])
    cv.text_px(cv.X(ZOLD) + 70, cv.Y(y0) + 62, "← 舊解誤記，偏短", 12.5, C["muted"])
    cv.dim((0, y0), (LN, y0), f"l_{{n}} = {LN:g} cm", off=100, label_off=14)
    cv.text_px(cv.X(LN/2) + 120, cv.Y(y0) + 114, f"（淨跨 ≥ 4d = {4*D:g} cm）", 12.5, C["muted"])
    cv.text_px(cv.X(0) + 6, cv.Y(y1) - 50, f"閉合箍筋：第一道 ≤ {FIRST:g} cm；s ≤ min(d/4, 6d_b, 15 cm) = {S_HOOP:g} cm", 12.5, C["deform"], "start")
    cv.text_px(cv.X(LN/2), cv.Y(y0) + 22, f"其他區段：U 型肋筋（耐震彎鉤） s ≤ d/2 = {S_MID:g} cm", 12.5, C["muted"])
    cv.text((-C1/2, 150), "柱", 13, C["muted"]); cv.text((LN + C1/2, 150), "柱", 13, C["muted"])
    return cv

def plan():
    W, Hc = 1100, 300
    ext = min(C2, 0.75*C1)
    cv = fit(W, Hc, (-200, 470), (-100, 100), L=20, R=20, T=60, B=16)
    cv.panel("(b) 平面：梁寬上限 = 柱寬 + 每側 min(c_{2}, 0.75c_{1})")
    # 舊式（虛線）
    cv.polygon([(0, -BW_OLD/2), (300, -BW_OLD/2), (300, BW_OLD/2), (0, BW_OLD/2)], "none", C["muted"], 1.4)
    cv.line((0, -BW_OLD/2), (300, -BW_OLD/2), C["muted"], 1.6, dash="6 4"); cv.line((0, BW_OLD/2), (300, BW_OLD/2), C["muted"], 1.6, dash="6 4")
    # 現行上限
    cv.polygon([(0, -BW_MAX/2), (300, -BW_MAX/2), (300, BW_MAX/2), (0, BW_MAX/2)], C["fill_m"], C["bmd"], 2.2)
    cv.polygon([(-C1, -C2/2), (0, -C2/2), (0, C2/2), (-C1, C2/2)], "#D5DAE2", C["member"], 2.4)   # 柱
    cv.text((-C1/2, 0), "柱", 13, C["text"])
    cv.dim((-C1, -C2/2), (-C1, C2/2), f"c_{{2}} = {C2:g}", off=-22, label_off=-36)
    cv.dim((-C1, C2/2), (0, C2/2), f"c_{{1}} = {C1:g}", off=-14, label_off=-14)
    cv.dim((300, -BW_MAX/2), (300, BW_MAX/2), f"b_{{w,max}} = {BW_MAX:g} cm", off=24, label_off=70, color=C["bmd"])
    cv.dim((40, C2/2), (40, BW_MAX/2), f"{ext:g}", off=-14, label_off=16, color=C["accent"])
    cv.dim((40, -BW_MAX/2), (40, -C2/2), f"{ext:g}", off=-14, label_off=16, color=C["accent"])
    cv.text((170, 0), f"每側外伸 ≤ min(c_{{2}}, 0.75c_{{1}}) = {ext:g} cm", 13, C["bmd"])
    cv.text_px(cv.X(150), cv.Y(BW_OLD/2) - 12, f"舊式 柱寬 + 1.5h = {BW_OLD:g} cm（虛線，已不適用）", 12, C["muted"])
    return cv

def fig1():
    a = elevation(); b = plan()
    title = f"{TAG}　特殊抗彎矩構架梁的配筋規定（示例：柱 60×60 cm、梁 h = 70 cm、d = 64 cm、D25）"
    top = 60; W = a.w; Ht = top + a.h + b.h            # 兩格不同高，手動上下疊放
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Ht}" viewBox="0 0 {W} {Ht}">'
           f'<defs><clipPath id="ca"><rect width="{W}" height="{a.h}"/></clipPath><clipPath id="cb"><rect width="{W}" height="{b.h}"/></clipPath></defs>'
           f'<rect width="{W}" height="{Ht}" fill="#FFFFFF"/>'
           f'<text x="{W/2}" y="36" font-family="{FONT}" font-size="17.5" fill="{C["text"]}" text-anchor="middle" font-weight="700">{esc(title)}</text>'
           f'<g transform="translate(0,{top})" clip-path="url(#ca)">{"".join(a.parts)}</g>'
           f'<g transform="translate(0,{top + a.h})" clip-path="url(#cb)">{"".join(b.parts)}</g></svg>')
    path = f"{OUT}/{TAG}-fig-1-hoop-zones.svg"; os.makedirs(OUT, exist_ok=True)
    open(path, "w", encoding="utf-8").write(svg); return path

FIGURES = [(fig1, "攔下 2d／2h 混淆、舊版間距 8d_b／24d_h／30 cm、舊式梁寬 柱寬＋1.5h")]
if __name__ == "__main__":
    for fn, catches in FIGURES: fn(); print(fn.__name__, "—", catches)
