"""Generate all precise SVG figures for lecture-SM-U1-1. Every length comes from a computed value."""
import json, math, re
import numpy as np
from scipy.interpolate import PchipInterpolator
from svglib import *

GW = 9.81
FIG = {}
NUM = {}   # numbers we print, for the audit log

# ---------------------------------------------------------------- common example
E0, S0, GS0 = 0.80, 0.60, 2.70          # demo soil used in §0, §1, §3


def phase_block(x, ybot, w, Vs, Vw, Va, U, labels=True, size=13, alpha=1.0):
    """stacked block, heights = volume*U, bottom aligned at ybot. returns (svg list, y-boundaries)"""
    out = []
    ys = ybot - Vs * U
    yw = ys - Vw * U
    ya = yw - Va * U
    op = f' opacity="{alpha}"' if alpha < 1 else ""
    out.append(R(x, ys, w, Vs * U, SOL, SOL_S, 1.6, op))
    if Vw > 1e-9:
        out.append(R(x, yw, w, Vw * U, WAT, WAT_S, 1.6, ' opacity="0.82"' if alpha == 1 else op))
    if Va > 1e-9:
        out.append(R(x, ya, w, Va * U, AIR, AIR_S, 1.6))
    if labels:
        out.append(T(x + w / 2, (ys + ybot) / 2 + 5, "土粒", size, "#fff"))
        if Vw * U > 16:
            out.append(T(x + w / 2, (yw + ys) / 2 + 5, "水", size, "#01579b"))
        if Va * U > 16:
            out.append(T(x + w / 2, (ya + yw) / 2 + 5, "空氣", size, "#616161"))
    return out, (ya, yw, ys, ybot)


# ================================================================ FIG 0-1
def fig0():
    left = '''  <rect x="40" y="55" width="300" height="200" fill="#fbf7f2" stroke="#8d6e63" stroke-width="2"/>
  <g fill="#a1887f" stroke="#6d4c41" stroke-width="1.2">
    <circle cx="80" cy="100" r="24"/><circle cx="138" cy="82" r="18"/><circle cx="190" cy="108" r="27"/>
    <circle cx="252" cy="86" r="21"/><circle cx="305" cy="114" r="23"/><circle cx="105" cy="160" r="26"/>
    <circle cx="167" cy="173" r="20"/><circle cx="227" cy="162" r="24"/><circle cx="290" cy="178" r="19"/>
    <circle cx="72" cy="215" r="21"/><circle cx="133" cy="223" r="24"/><circle cx="197" cy="217" r="18"/>
    <circle cx="257" cy="226" r="23"/><circle cx="312" cy="222" r="20"/>
  </g>
  <g fill="#4fc3f7" opacity="0.75">
    <path d="M103 118 q18 14 32 -2 q-6 22 -18 24 q-16 -6 -14 -22z"/>
    <path d="M215 134 q16 12 30 -2 q-4 20 -16 22 q-14 -6 -14 -20z"/>
    <path d="M145 196 q16 12 28 -2 q-4 20 -14 22 q-14 -6 -14 -20z"/>
    <path d="M271 200 q16 12 28 -2 q-4 20 -14 22 q-14 -6 -14 -20z"/>
  </g>'''
    b = [arrow_defs((("ar0", "#1565c0"),)), left]
    b.append(T(190, 34, "真實的土壤", 16, "#5d4037", weight=700))
    b.append(T(190, 282, "顆粒、水膜、氣泡糾纏在一起", 13.5, "#5d4037"))
    b.append(T(190, 304, "沒有一個體積量得出來", 13.5, "#5d4037"))
    b.append(T(190, 336, "量不到 → 算不了", 14, "#5d4037", weight=700))
    # arrow
    b.append(f'<path d="M352 155 H448" stroke="#1565c0" stroke-width="2.4" fill="none" marker-end="url(#ar0)"/>')
    b.append(T(400, 143, "把三相", 12.5, "#1565c0"))
    b.append(T(400, 178, "分開堆疊", 12.5, "#1565c0"))
    # right: to-scale block, total height 200 for V=1+e
    U = 200 / (1 + E0)
    Vw = S0 * E0; Va = E0 - Vw
    blk, (ya, yw, ys, yb) = phase_block(560, 255, 150, 1.0, Vw, Va, U, size=14)
    b += blk
    b.append(T(660, 34, "分析用的三相塊（按比例）", 16, "#1565c0", weight=700))
    for yy, s in [((ya + yw) / 2, f"V_{{a}} = {Va:.2f}"), ((yw + ys) / 2, f"V_{{w}} = {Vw:.2f}"),
                  ((ys + yb) / 2, "V_{s} = 1")]:
        b.append(T(550, yy + 5, s, 13, "#37474f", "end"))
    for yy, s in [((ya + yw) / 2, "W_{a} ≈ 0"), ((yw + ys) / 2, f"W_{{w}} = {Vw:.2f} γ_{{w}}"),
                  ((ys + yb) / 2, f"W_{{s}} = {GS0:.2f} γ_{{w}}")]:
        b.append(T(720, yy + 5, s, 13, "#37474f", "start"))
    b.append(T(520, 50, "體積", 12, MUT, "end"))
    b.append(T(752, 50, "重量", 12, MUT, "start"))
    b.append(T(660, 282, f"示例 e = {E0:.2f}、S = {S0:.0%}、G_{{s}} = {GS0:.2f}", 13.5, "#1565c0"))
    b.append(T(660, 304, "每個比值都變成兩段長度之比", 13.5, "#1565c0"))
    b.append(T(660, 336, "量得到 → 算得出", 14, "#1565c0", weight=700))
    return svg(880, 350, b)


# ================================================================ FIG 1-1
def fig1():
    e, S, Gs = E0, S0, GS0
    Vs, Vw = 1.0, S * e; Va = e - Vw
    Ws, Ww = Gs, S * e                              # in units of gamma_w
    U = 150                                         # px per unit volume
    K = 55                                          # px per unit gamma_w
    yb = 380
    xv, wv = 250, 150
    xw, ww = 590, 110
    b = [T(430, 26, "單位土粒法：令 V_{s} = 1（按比例繪製：e = 0.80、S = 60%、G_{s} = 2.70）",
           15.5, "#0d47a1", weight=700)]
    blk, (ya, yw, ys, _) = phase_block(xv, yb, wv, Vs, Vw, Va, U, size=14)
    # weight column
    wys = yb - Ws * K; wyw = wys - Ww * K
    bands = [PG([(xv + wv, ys), (xw, wys), (xw, yb), (xv + wv, yb)], "#d7ccc8", extra=' opacity="0.55"'),
             PG([(xv + wv, yw), (xw, wyw), (xw, wys), (xv + wv, ys)], "#b3e5fc", extra=' opacity="0.6"'),
             PG([(xv + wv, ya), (xw, wyw), (xv + wv, yw)], "#eeeeee", extra=' opacity="0.8"')]
    b += bands + blk
    b.append(R(xw, wys, ww, Ws * K, SOL, SOL_S, 1.6))
    b.append(R(xw, wyw, ww, Ww * K, WAT, WAT_S, 1.6, ' opacity="0.82"'))
    b.append(T(xw + ww / 2, (wys + yb) / 2 + 5, "土粒重", 13.5, "#fff"))
    b.append(T(xw + ww / 2, (wyw + wys) / 2 + 5, "水重", 12.5, "#01579b"))
    b.append(T(xv + wv / 2, ya - 30, "體積柱（高度 ∝ 體積）", 13, MUT))
    b.append(T(xv + wv / 2, ya - 12, f"V = 1 + e = {1+e:.2f}", 13.5, INK, weight=700))
    b.append(T(xw + ww / 2, ya - 30, "重量柱（高度 ∝ 重量）", 13, MUT))
    b.append(T(xw + ww / 2, ya - 12, f"W = (G_{{s}} + Se)γ_{{w}} = {Ws+Ww:.2f}γ_{{w}}", 13.5, INK, weight=700))
    # left dims
    xd = 232
    b.append(vdim(xd, ya, yw)); b.append(vdim(xd, yw, ys)); b.append(vdim(xd, ys, yb))
    rows = [((ya + yw) / 2, "V_{a} = e − Se", f"= {Va:.2f}"),
            ((yw + ys) / 2, "V_{w} = Se", f"= {Vw:.2f}"),
            ((ys + yb) / 2, "V_{s} = 1", "（錨點）")]
    for yy, s1, s2 in rows:
        b.append(T(222, yy - 2, s1, 13.5, INK, "end"))
        b.append(T(222, yy + 16, s2, 12.5, MUT, "end"))
    # Vv bracket (far left)
    xv2 = 132
    b.append(vdim(xv2, ya, ys, "#6a1b9a"))
    b.append(T(xv2 - 12, (ya + ys) / 2, f"V_{{v}} = e = {e:.2f}", 13.5, "#6a1b9a", "middle", 700,
               f' transform="rotate(-90 {xv2-12:.1f} {(ya+ys)/2:.1f})"'))
    # right dims on weight column
    xr = xw + ww + 14
    b.append(vdim(xr, wyw, wys)); b.append(vdim(xr, wys, yb))
    b.append(T(xr + 12, (wyw + wys) / 2 + 5, f"W_{{w}} = Se·γ_{{w}} = {Ww:.2f}γ_{{w}}", 13, INK, "start"))
    b.append(T(xr + 12, (wys + yb) / 2 - 4, "W_{s} = G_{s}·γ_{w}", 13.5, INK, "start"))
    b.append(T(xr + 12, (wys + yb) / 2 + 15, f"= {Ws:.2f}γ_{{w}}", 12.5, MUT, "start"))
    b.append(T(xr + 12, wyw - 8, "W_{a} ≈ 0（空氣無重量）", 12, MUT, "start"))
    b.append(T((xv + wv + xw) / 2, (ys + yb) / 2 + 40, "×G_{s}", 13, "#5d4037", weight=700))
    b.append(T((xv + wv + xw) / 2, (yw + ys) / 2 + 4, "×1", 12.5, "#0277bd", weight=700))
    # boxes
    by = 404
    b.append(R(60, by, 330, 120, "#fff8e1", "#ffb74d", 1.4, ' rx="8"'))
    b.append(T(225, by + 24, "讀圖規則", 13.5, "#e65100", weight=700))
    for i, s in enumerate(["左柱高度 = 體積；右柱高度 = 重量",
                           "同一相在兩柱之間只差一個倍率：",
                           "水 ×γ_{w}，土粒 ×G_{s}γ_{w}，空氣 ×0",
                           "→ 兩個世界只靠 G_{s} 與 γ_{w} 相通"]):
        b.append(T(225, by + 48 + 20 * i, s, 12.5, "#5d4037"))
    b.append(R(420, by, 400, 120, "#e8f5e9", "#81c784", 1.4, ' rx="8"'))
    b.append(T(620, by + 24, "直接從圖上讀出的四個定義（示例值）", 13.5, "#2e7d32", weight=700))
    w = Ww / Ws; n = e / (1 + e)
    NUM["fig1"] = dict(Va=Va, Vw=Vw, w=w, n=n)
    for i, s in enumerate([f"e = V_{{v}}/V_{{s}} = {e:.2f}/1 = {e:.2f}",
                           f"S = V_{{w}}/V_{{v}} = {Vw:.2f}/{e:.2f} = {S:.0%}",
                           f"w = W_{{w}}/W_{{s}} = Se/G_{{s}} = {Ww:.2f}/{Ws:.2f} = {w:.1%}",
                           f"n = V_{{v}}/V = e/(1+e) = {e:.2f}/{1+e:.2f} = {n:.3f}"]):
        b.append(T(620, by + 48 + 20 * i, s, 12.5, "#1b5e20"))
    return svg(860, 540, b)


# ================================================================ FIG 2-1  (example A)
def figA():
    H0, e0, H1, Gs = 2.5, 1.30, 1.9, 2.72
    Hs = H0 / (1 + e0); Hv0 = H0 - Hs; Hv1 = H1 - Hs; e1 = Hv1 / Hs
    w0, w1 = e0 / Gs, e1 / Gs
    g0 = (Gs + e0) * GW / (1 + e0); g1 = (Gs + e1) * GW / (1 + e1)
    NUM["exA"] = dict(Hs=Hs, Hv1=Hv1, e1=e1, w0=w0, w1=w1, g0=g0, g1=g1)
    P = 110  # px per cm
    yb = 345; wcol = 120
    x0, x1 = 210, 520
    b = [arrow_defs((("arA", "#455a64"), ("arA2", "#c62828")))]
    b.append(T(400, 26, "範例 A 按比例：土粒高度 H_{s} 不動，被擠掉的只有孔隙", 15.5, "#0d47a1", weight=700))
    for x, Hv, H, lab in [(x0, Hv0, H0, "壓縮前"), (x1, Hv1, H1, "壓縮後")]:
        ys = yb - Hs * P; yt = yb - H * P
        b.append(R(x, ys, wcol, Hs * P, SOL, SOL_S, 1.6))
        b.append(R(x, yt, wcol, Hv * P, WAT, WAT_S, 1.6, ' opacity="0.82"'))
        b.append(T(x + wcol / 2, (ys + yb) / 2 + 5, "土粒", 14, "#fff"))
        b.append(T(x + wcol / 2, (yt + ys) / 2 + 5, "孔隙水（S = 1）", 13, "#01579b"))
        b.append(T(x + wcol / 2, yb + 22, lab, 14, INK, weight=700))
    # piston on state 1
    yt1 = yb - H1 * P
    b.append(R(x1 - 6, yt1 - 10, wcol + 12, 10, "#78909c"))
    for dx in (30, 60, 90):
        b.append(f'<path d="M{x1+dx} {yt1-46} V{yt1-13}" stroke="#c62828" stroke-width="2.2" marker-end="url(#arA2)"/>')
    b.append(T(x1 + wcol / 2, yt1 - 52, "加壓、排水", 12.5, "#c62828"))
    # constant Hs line
    ys = yb - Hs * P
    b.append(L(x0 - 40, ys, x1 + wcol + 40, ys, "#5d4037", 1.6, "7,4"))
    b.append(T((x0 + wcol + x1) / 2, ys - 26, "H_{s} = H_{0}/(1+e_{0})", 12.5, "#5d4037", "middle", 700))
    b.append(T((x0 + wcol + x1) / 2, ys - 9, f"= {Hs:.3f} cm（兩狀態相同）", 12.5, "#5d4037", "middle", 700))
    # left dims state 0
    yt0 = yb - H0 * P
    b.append(vdim(x0 - 18, yt0, ys)); b.append(vdim(x0 - 18, ys, yb))
    b.append(T(x0 - 28, (yt0 + ys) / 2 - 2, f"H_{{v0}} = e_{{0}}H_{{s}}", 13, INK, "end"))
    b.append(T(x0 - 28, (yt0 + ys) / 2 + 16, f"= {Hv0:.3f} cm", 12.5, MUT, "end"))
    b.append(T(x0 - 28, (ys + yb) / 2 + 5, f"{Hs:.3f} cm", 12.5, MUT, "end"))
    b.append(vdim(x0 - 110, yt0, yb, "#37474f"))
    b.append(T(x0 - 122, (yt0 + yb) / 2, f"H_{{0}} = {H0} cm", 13.5, INK, "middle", 700,
               f' transform="rotate(-90 {x0-122} {(yt0+yb)/2:.1f})"'))
    # right dims state 1
    xr = x1 + wcol + 18
    b.append(vdim(xr, yt1, ys)); b.append(vdim(xr, ys, yb))
    b.append(T(xr + 10, (yt1 + ys) / 2 - 2, f"H_{{v1}} = {H1} − {Hs:.3f}", 13, INK, "start"))
    b.append(T(xr + 10, (yt1 + ys) / 2 + 16, f"= {Hv1:.3f} cm", 12.5, MUT, "start"))
    b.append(T(xr + 10, (ys + yb) / 2 + 5, f"{Hs:.3f} cm", 12.5, MUT, "start"))
    b.append(vdim(xr + 140, yt1, yb, "#37474f"))
    b.append(T(xr + 154, (yt1 + yb) / 2, f"H_{{1}} = {H1} cm", 13.5, INK, "middle", 700,
               f' transform="rotate(90 {xr+154} {(yt1+yb)/2:.1f})"'))
    # Delta H
    b.append(L(x0 + wcol, yt0, x1 - 6, yt0, "#c62828", 1.2, "4,3"))
    xd = (x0 + wcol + x1) / 2 + 30
    b.append(vdim(xd, yt0, yt1, "#c62828"))
    b.append(T(xd - 10, (yt0 + yt1) / 2 + 5, f"ΔH = {H0-H1:.2f} cm", 13, "#c62828", "end", 700))
    b.append(T(xd - 10, (yt0 + yt1) / 2 + 23, f"= Δe·H_{{s}} = ({e0:.2f}−{e1:.3f})×{Hs:.3f}", 11.5, "#c62828", "end"))
    # result rows
    b.append(T(x0 + wcol / 2, yb + 44, f"e_{{0}} = {e0:.2f}　w_{{0}} = {w0:.1%}", 12.5, MUT))
    b.append(T(x0 + wcol / 2, yb + 63, f"γ_{{0}} = {g0:.2f} kN/m³", 12.5, MUT))
    b.append(T(x1 + wcol / 2, yb + 44, f"e_{{1}} = {Hv1:.3f}/{Hs:.3f} = {e1:.3f}　w_{{1}} = {w1:.1%}", 12.5, "#1b5e20"))
    b.append(T(x1 + wcol / 2, yb + 63, f"γ_{{1}} = {g1:.2f} kN/m³（↑）", 12.5, "#1b5e20"))
    return svg(830, 425, b)


# ================================================================ FIG 3-1
def fig3():
    e, S, Gs = E0, S0, GS0
    gd = Gs * GW / (1 + e); gt = (Gs + S * e) * GW / (1 + e)
    gsat = (Gs + e) * GW / (1 + e); gp = gsat - GW; gmax = Gs * GW
    NUM["fig3"] = dict(gd=gd, gt=gt, gsat=gsat, gp=gp, gmax=gmax)
    U = 70; w = 130; ytop = 48; yb = ytop + (1 + e) * U
    xs = [45, 260, 475, 690]
    b = [arrow_defs((("ar3", "#c62828"),))]
    b.append(T(450, 24, "同一塊土（e = 0.80、G_{s} = 2.70），孔隙裡裝的東西不同 → 四個單位重", 15.5,
               "#0d47a1", weight=700))
    specs = [
        ("乾單位重 γ_{d}", "#616161", "S = 0", "G_{s}γ_{w}/(1+e)", gd, 0.0),
        ("濕單位重 γ_{t}", "#0277bd", f"S = {S:.0%}", "(G_{s}+Se)γ_{w}/(1+e)", gt, S),
        ("飽和單位重 γ_{sat}", "#0277bd", "S = 1", "(G_{s}+e)γ_{w}/(1+e)", gsat, 1.0),
        ("有效單位重 γ′", "#c62828", "S = 1，扣浮力", "γ_{sat} − γ_{w}", gp, 1.0)]
    for i, (name, col, s_txt, f_txt, val, s) in enumerate(specs):
        x = xs[i]
        blk, _ = phase_block(x, yb, w, 1.0, s * e, e - s * e, U, size=13,
                             alpha=0.55 if i == 3 else 1.0)
        b += blk
        if i == 3:
            b.append(f'<path d="M{x+w+16} {yb-8} V{ytop+14}" stroke="#c62828" stroke-width="2.4" marker-end="url(#ar3)"/>')
            b.append(T(x + w + 24, (ytop + yb) / 2 + 4, "浮力", 12, "#c62828", "start"))
        cx = x + w / 2
        b.append(T(cx, yb + 24, name, 14.5, col, weight=700))
        b.append(T(cx, yb + 44, s_txt, 12.5, "#455a64"))
        b.append(T(cx, yb + 64, f_txt, 12.5, "#455a64"))
        b.append(T(cx, yb + 86, f"= {val+1e-9:.2f} kN/m³", 13.5, col, weight=700))
    # number line
    x0, x1, vmax = 60, 860, 28.0
    k = (x1 - x0) / vmax
    ya = 372
    X = lambda v: x0 + v * k
    b.append(T(450, ya - 58, "放到同一條數線上：大小順序是驗算工具", 13.5, "#37474f", weight=700))
    b.append(R(X(gmax), ya - 14, x1 - X(gmax), 28, "#ffebee"))
    b.append(T((X(gmax) + x1) / 2, ya - 20, "不可能", 12, "#c62828", weight=700))
    b.append(L(x0, ya, x1, ya, "#455a64", 2))
    for v in range(0, 29, 2):
        b.append(L(X(v), ya - 5, X(v), ya + 5, "#455a64", 1.2))
        b.append(T(X(v), ya + 20, f"{v}", 11, MUT))
    b.append(T(x1, ya + 38, "kN/m³", 11.5, MUT, "end"))
    marks = [(gp, "γ′", "#c62828", 1), (GW, "γ_{w}", "#78909c", -1), (gd, "γ_{d}", "#616161", -1),
             (gt, "γ_{t}", "#0277bd", 1), (gsat, "γ_{sat}", "#01579b", -1), (gmax, "G_{s}γ_{w}", "#b71c1c", 1)]
    for v, lab, col, side in marks:
        b.append(C(X(v), ya, 5.5, col, "#fff", 1.5))
        if side < 0:
            b.append(L(X(v), ya - 8, X(v), ya - 22, col, 1.2))
            b.append(T(X(v), ya - 40, lab, 13, col, weight=700))
            b.append(T(X(v), ya - 26, f"{v+1e-9:.2f}", 11, col))
        else:
            b.append(L(X(v), ya + 26, X(v), ya + 40, col, 1.2))
            b.append(T(X(v), ya + 56, lab, 13, col, weight=700))
            b.append(T(X(v), ya + 72, f"{v+1e-9:.2f}", 11, col))
    # gamma' = gsat - gw bracket: same length segments
    yb2 = ya + 92
    b.append(hdim(yb2, X(GW), X(gsat), "#c62828", 5))
    b.append(hdim(yb2, X(0), X(gp), "#c62828", 5))
    b.append(T((X(GW) + X(gsat)) / 2, yb2 + 18, "γ_{sat} − γ_{w}", 12, "#c62828"))
    b.append(T((X(0) + X(gp)) / 2, yb2 + 18, "γ′：兩段等長", 12, "#c62828"))
    return svg(900, 490, b)


# ================================================================ FIG 4-1
STD = [(6, 16.6), (8, 17.5), (10, 18.25), (12, 18.6), (14, 18.3), (16, 17.6), (18, 16.9), (20, 16.2)]
MOD = [(5, 17.9), (7, 18.8), (9, 19.3), (10, 19.4), (11, 19.25), (13, 18.65), (15, 18.0), (17, 17.35)]


def fig4():
    # ---- left: e ruler for example B
    Gs = 2.70; ems, emx = 2.70 * 440 / 850 - 1, 2.70 * 640 / 850 - 1
    w = 50 / 850; e = w * Gs / 0.27
    Dr = (emx - e) / (emx - ems)
    NUM["exB"] = dict(emin=ems, emax=emx, e=e, Dr=Dr)
    b = [T(225, 30, "相對密度 D_{r}｜範例 B（SM-2020-3）按比例", 15, "#2e7d32", weight=700),
         T(695, 30, "相對夯實度 R.C.｜夯實曲線按比例（G_{s} = 2.70）", 15, "#c62828", weight=700),
         L(450, 16, 450, 392, "#b0bec5", 2, "7,5")]
    yt, ybm = 70, 300
    Y = lambda ev: yt + (emx - ev) / (emx - ems) * (ybm - yt)   # emax top
    xr = 150
    b.append(R(xr - 9, yt, 18, ybm - yt, "#f1f8e9", "#9ccc65", 1))
    b.append(R(xr - 9, yt, 18, Y(e) - yt, "#a5d6a7"))
    b.append(L(xr, yt, xr, ybm, "#455a64", 2))
    for ev in np.arange(0.4, 1.01, 0.1):
        b.append(L(xr - 13, Y(ev), xr - 9, Y(ev), "#455a64", 1))
        b.append(T(xr - 17, Y(ev) + 4, f"{ev:.1f}", 10.5, MUT, "end"))
    for ev, lab, col, wt in [(emx, f"e_{{max}} = {emx:.3f}（最鬆）", INK, None),
                             (e, f"e = {e:.3f}（現地）", "#2e7d32", 700),
                             (ems, f"e_{{min}} = {ems:.3f}（最密）", INK, None)]:
        b.append(L(xr - 9, Y(ev), xr + 22, Y(ev), col, 2.2 if wt else 1.6))
        b.append(T(xr + 28, Y(ev) + 5, lab, 12.5, col, "start", wt))
    b.append(vdim(xr + 205, Y(emx), Y(e), "#2e7d32"))
    b.append(vdim(xr + 235, Y(emx), Y(ems), "#455a64"))
    b.append(T(xr + 199, (Y(emx) + Y(e)) / 2 + 4, f"{emx-e:.3f}", 11.5, "#2e7d32", "end"))
    b.append(T(xr + 241, (Y(emx) + Y(ems)) / 2 + 4, f"{emx-ems:.3f}", 11.5, "#455a64", "start"))
    b.append(T(225, 364, f"D_{{r}} = (e_{{max}} − e)/(e_{{max}} − e_{{min}}) = {emx-e:.3f}/{emx-ems:.3f} = {Dr:.0%}",
               12.5, "#1b5e20", weight=700))
    b.append(T(225, 386, "參考點：這種土自己的兩個極限（與夯實能量無關）", 12, "#455a64"))
    # ---- right: compaction curves
    px0, px1, py0, py1 = 530, 870, 300, 62
    w0, w1, g0, g1 = 4, 22, 15.5, 21.0
    X = lambda wv: px0 + (wv - w0) / (w1 - w0) * (px1 - px0)
    Yg = lambda gv: py0 - (gv - g0) / (g1 - g0) * (py0 - py1)
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    for wv in range(4, 23, 2):
        b.append(L(X(wv), py0, X(wv), py0 + 4, "#455a64", 1))
        b.append(T(X(wv), py0 + 16, f"{wv}", 10, MUT))
    for gv in np.arange(16, 21.01, 1):
        b.append(L(px0 - 4, Yg(gv), px0, Yg(gv), "#455a64", 1))
        b.append(T(px0 - 7, Yg(gv) + 4, f"{gv:.0f}", 10, MUT, "end"))
    b.append(T(px1, py0 + 30, "w (%)", 11.5, MUT, "end"))
    b.append(T(px0 - 4, py1 - 10, "γ_{d} (kN/m³)", 11.5, MUT, "start"))
    ww = np.linspace(w0, w1, 120)
    zav = Gs * GW / (1 + ww / 100 * Gs)
    pts = [(X(a), Yg(c)) for a, c in zip(ww, zav) if c <= g1]
    b.append(PL(pts, "#0288d1", 1.8, "6,4"))
    b.append(T(X(9.2), Yg(21.0) + 4, "零空氣孔隙線 S = 100%", 11.5, "#0288d1", "start"))
    for data, col, dash, lab in [(STD, "#c62828", None, "標準夯實"), (MOD, "#6a1b9a", "7,3", "修正夯實（能量較高）")]:
        xs_, ys_ = zip(*data)
        f = PchipInterpolator(xs_, ys_)
        wv = np.linspace(xs_[0], xs_[-1], 100); gv = f(wv)
        Smax = max((a / 100 * Gs) / (Gs * GW / c - 1) for a, c in zip(wv, gv))
        assert Smax < 0.95, Smax
        b.append(PL([(X(a), Yg(c)) for a, c in zip(wv, gv)], col, 2.6, dash))
        i = int(np.argmax(gv)); NUM.setdefault("compaction", {})[lab] = (float(wv[i]), float(gv[i]), float(Smax))
    # standard peak & 95 % window
    fs = PchipInterpolator(*zip(*STD))
    wv = np.linspace(6, 20, 2801); gv = fs(wv); i = int(np.argmax(gv))
    omc, gmx = wv[i], gv[i]; g95 = 0.95 * gmx
    ok = wv[gv >= g95]; wa, wb = ok[0], ok[-1]
    NUM["RC95"] = dict(omc=omc, gmax=gmx, g95=g95, wa=wa, wb=wb)
    b.append(L(px0, Yg(gmx), X(omc), Yg(gmx), "#c62828", 1.1, "4,3"))
    b.append(L(X(omc), Yg(gmx), X(omc), py0, "#c62828", 1.1, "4,3"))
    b.append(C(X(omc), Yg(gmx), 4.5, "#c62828"))
    b.append(T(X(omc) - 8, Yg(gmx) - 8, f"γ_{{d,max}} = {gmx:.2f}", 11.5, "#c62828", "end", 700))
    b.append(T(X(omc), py0 + 30, f"OMC {omc:.0f}%", 11, "#c62828"))
    b.append(L(px0, Yg(g95), px1 - 60, Yg(g95), "#2e7d32", 1.4, "5,3"))
    b.append(T(px1 - 56, Yg(g95) + 4, f"95%：{g95:.2f}", 11, "#2e7d32", "start"))
    b.append(R(X(wa), py0 - 7, X(wb) - X(wa), 7, "#a5d6a7"))
    b.append(L(X(wa), Yg(g95), X(wa), py0, "#2e7d32", 1, "2,2"))
    b.append(L(X(wb), Yg(g95), X(wb), py0, "#2e7d32", 1, "2,2"))
    b.append(T((X(wa) + X(wb)) / 2, py0 - 12, f"合格窗口 w ≈ {wa:.1f}～{wb:.1f}%", 11, "#1b5e20"))
    b.append(T(X(10), Yg(19.4) - 10, "修正夯實", 11.5, "#6a1b9a", "middle", 700))
    b.append(T(X(19.2), Yg(16.6) + 26, "標準夯實", 11.5, "#c62828", "middle", 700))
    b.append(T(695, 364, "R.C. = 工地 γ_{d} / 實驗室 γ_{d,max}", 12.5, "#b71c1c", weight=700))
    b.append(T(695, 386, "參考點綁死在某一夯實能量：換能量，峰值與 OMC 一起搬家", 12, "#455a64"))
    return svg(920, 400, b)


# ================================================================ FIG 4-2  dual ruler
def fig4b():
    Gs = 2.70
    rmin, rmax, r = 850 / 640, 850 / 440, 1.700
    emx, ems = Gs / rmin - 1, Gs / rmax - 1
    e = Gs / r - 1
    Dr_e = (emx - e) / (emx - ems); Dr_lin = (r - rmin) / (rmax - rmin)
    NUM["fig4b"] = dict(Dr_e=Dr_e, Dr_lin=Dr_lin, rmin=rmin, rmax=rmax)
    x0, x1 = 150, 770
    X = lambda d: x0 + d * (x1 - x0)
    y1, y2 = 110, 270
    b = [T(460, 26, "同一個現地狀態，放在兩把尺上：ρ_{d} 與 e 是倒數關係，刻度不等距", 15.5, "#0d47a1", weight=700)]
    for y, lab, col in [(y1, "e 尺（定義，等距）", "#2e7d32"), (y2, "ρ_{d} 尺（誤用，等距）", "#c62828")]:
        b.append(L(x0, y, x1, y, col, 3))
        b.append(T(x0 - 14, y + 5, lab, 12.5, col, "end", 700))
    b.append(T(x0, y1 - 40, "最鬆 D_{r} = 0", 11.5, MUT)); b.append(T(x1, y1 - 40, "最密 D_{r} = 1", 11.5, MUT))
    # e ruler ticks (top labels)
    for ev in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]:
        d = (emx - ev) / (emx - ems)
        if 0 <= d <= 1:
            b.append(L(X(d), y1 - 7, X(d), y1, "#2e7d32", 1.3))
            b.append(T(X(d), y1 - 12, f"e={ev:.1f}", 10.5, "#2e7d32"))
    # rho ticks: on rho ruler (equal) and mapped onto e ruler, connected by fan lines
    for rv in [1.4, 1.5, 1.6, 1.7, 1.8, 1.9]:
        d_lin = (rv - rmin) / (rmax - rmin)
        d_e = (emx - (Gs / rv - 1)) / (emx - ems)
        b.append(L(X(d_e), y1 + 2, X(d_lin), y2 - 2, "#b0bec5", 1, "3,3"))
        b.append(L(X(d_e), y1, X(d_e), y1 + 8, "#c62828", 1.3))
        b.append(L(X(d_lin), y2, X(d_lin), y2 + 8, "#c62828", 1.3))
        b.append(T(X(d_lin), y2 + 22, f"{rv:.1f}", 10.5, "#c62828"))
    for d, v in [(0, rmin), (1, rmax)]:
        b.append(L(X(d), y1 - 8, X(d), y1 + 8, INK, 2)); b.append(L(X(d), y2 - 8, X(d), y2 + 8, INK, 2))
        b.append(T(X(d), y2 + 40, f"{v:.3f}", 11, INK, weight=700))
    b.append(T(X(0) - 4, y1 + 26, f"{emx:.3f}", 11, INK, "middle", 700))
    b.append(T(X(1) + 4, y1 + 26, f"{ems:.3f}", 11, INK, "middle", 700))
    b.append(T((x0 + x1) / 2, y2 + 40, "ρ_{d}（g/cm³）", 10.5, MUT))
    # the field state
    b.append(L(X(Dr_e), y1, X(Dr_lin), y2, "#37474f", 2.4))
    b.append(C(X(Dr_e), y1, 7, "#2e7d32", "#fff", 2)); b.append(C(X(Dr_lin), y2, 7, "#c62828", "#fff", 2))
    b.append(T(X(Dr_e) - 14, y1 + 28, f"現地 e = {e:.3f} → D_{{r}} = {Dr_e:.1%}（正解）", 12.5, "#2e7d32", "end", 700))
    b.append(T(X(Dr_lin) - 12, y2 - 14, f"現地 ρ_{{d}} = {r:.3f} → {Dr_lin:.1%}（線性內插，錯）", 12.5, "#c62828", "end", 700))
    b.append(R(150, 330, 620, 56, "#fff3e0", "#ffcc80", 1.2, ' rx="8"'))
    b.append(T(460, 352, "兩端點重合，中間全部錯位：ρ_{d} 每增加 0.1，e 減少得越來越少（e = G_{s}ρ_{w}/ρ_{d} − 1）", 12.5, "#e65100"))
    b.append(T(460, 374, f"所以偏差不是捨入誤差，而是 {100*(Dr_e-Dr_lin):.1f} 個百分點的系統性低估", 12.5, "#e65100", weight=700))
    return svg(920, 400, b)


# ================================================================ FIG 5-1
def fig5():
    Gs, SL, PLv, LLv, wn = 2.70, 13.0, 22.0, 38.0, 42.0
    PI = LLv - PLv; LI = (wn - PLv) / PI
    NUM["fig5"] = dict(PI=PI, LI=LI)
    x0, x1, wmax = 110, 830, 50
    X = lambda wv: x0 + wv / wmax * (x1 - x0)
    # top panel: V/Vs vs w
    py0, py1, v0, v1 = 210, 58, 1.2, 2.45
    Y = lambda v: py0 - (v - v0) / (v1 - v0) * (py0 - py1)
    b = [T(470, 24, "上：乾燥／加水時土體積怎麼變　下：同一條含水量軸上的四個狀態（按比例）", 15, "#0d47a1", weight=700)]
    b.append(L(x0, py0, x1, py0, "#455a64", 1.4)); b.append(L(x0, py0, x0, py1, "#455a64", 1.4))
    for v in [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]:
        b.append(L(x0 - 4, Y(v), x0, Y(v), "#455a64", 1)); b.append(T(x0 - 7, Y(v) + 4, f"{v:.1f}", 10, MUT, "end"))
    b.append(T(x0 - 40, (py0 + py1) / 2, "V / V_{s} = 1 + e", 12, "#455a64", "middle", None,
               f' transform="rotate(-90 {x0-40} {(py0+py1)/2:.1f})"'))
    vsl = 1 + SL / 100 * Gs
    curve = [(X(0), Y(vsl)), (X(SL), Y(vsl))] + [(X(wv), Y(1 + wv / 100 * Gs)) for wv in (SL, wmax)]
    b.append(PL(curve, "#5d4037", 2.8))
    b.append(T(X(SL / 2), Y(vsl) - 28, "低於 SL：再乾也不縮", 11.5, "#5d4037"))
    b.append(T(X(SL / 2), Y(vsl) - 11, "（空氣進入孔隙）", 11, MUT))
    b.append(T(X(23), Y(1.42), "高於 SL：飽和，V/V_{s} = 1 + wG_{s}", 11.5, "#5d4037", "start"))
    b.append(T(X(23), Y(1.42) + 17, "斜率 = G_{s}，體積隨 w 線性變化", 11, MUT, "start"))
    # bottom number line
    yl = 300
    zones = [(0, SL, "#eceff1", "#90a4ae", "固態", "#37474f"), (SL, PLv, "#fff3e0", "#ffb74d", "半固態", "#e65100"),
             (PLv, LLv, "#e8f5e9", "#81c784", "塑性", "#2e7d32"), (LLv, wmax, "#e3f2fd", "#64b5f6", "液態", "#1565c0")]
    for a, c, f, s, lab, tc in zones:
        b.append(R(X(a), yl - 40, X(c) - X(a), 40, f, s, 1))
        b.append(T((X(a) + X(c)) / 2, yl - 15, lab, 13, tc, weight=700))
    b.append(L(x0, yl, x1 + 10, yl, "#455a64", 2))
    for wv in range(0, 51, 5):
        b.append(L(X(wv), yl, X(wv), yl + 5, "#455a64", 1)); b.append(T(X(wv), yl + 18, f"{wv}", 10, MUT))
    b.append(T(x1 + 14, yl + 18, "w (%)", 11, MUT, "start"))
    for wv, lab, sub in [(SL, "SL", "縮限"), (PLv, "PL", "塑限"), (LLv, "LL", "液限")]:
        b.append(L(X(wv), py1, X(wv), yl, "#c62828", 1.2, "5,3"))
        b.append(T(X(wv), py1 - 6, f"{lab} {wv:.0f}%", 11.5, "#c62828", weight=700))
    # current w
    b.append(L(X(wn), Y(1 + wn / 100 * Gs), X(wn), yl + 70, "#00695c", 1.8))
    b.append(C(X(wn), Y(1 + wn / 100 * Gs), 5, "#00695c"))
    b.append(C(X(wn), yl, 6, "#00695c", "#fff", 1.5))
    b.append(T(X(wn) + 6, Y(1 + wn / 100 * Gs) + 18, f"現地 w = {wn:.0f}%", 12, "#00695c", "start", 700))
    # PI bracket
    yp = yl + 40
    b.append(hdim(yp, X(PLv), X(LLv), "#6a1b9a", 6, 2))
    b.append(T((X(PLv) + X(LLv)) / 2, yp + 18, f"PI = LL − PL = {PI:.0f}（線段長度：材料本性）", 12, "#6a1b9a", weight=700))
    # LI axis
    yli = yl + 80
    LIX = lambda li: X(PLv + li * PI)
    b.append(L(LIX(-1.2), yli, LIX(1.6), yli, "#00695c", 1.6))
    for li in [-1, -0.5, 0, 0.5, 1, 1.5]:
        b.append(L(LIX(li), yli - 4, LIX(li), yli + 4, "#00695c", 1.2))
        b.append(T(LIX(li), yli + 18, f"{li:g}", 10.5, "#00695c"))
    b.append(T(LIX(-1.2) - 8, yli + 4, "LI 座標", 12, "#00695c", "end", 700))
    b.append(C(LIX(LI), yli, 6, "#00695c"))
    b.append(T(LIX(LI) + 10, yli - 8, f"LI = ({wn:.0f}−{PLv:.0f})/{PI:.0f} = {LI:.2f} > 1", 12, "#00695c", "start", 700))
    b.append(T(470, yli + 44, "PI 量的是「這段多長」（材料）；LI 量的是「現在站在哪」（狀態）：PL 處 LI = 0，LL 處 LI = 1",
               12, "#455a64"))
    return svg(940, 440, b)


# ================================================================ FIG 6-1 GSD
GSD = {
    "well": [(0.03, 1), (0.075, 4), (0.12, 10), (0.7, 30), (3.0, 60), (12, 88), (40, 100)],
    "gap": [(0.04, 1), (0.1, 10), (0.25, 30), (0.42, 38), (1.2, 40), (3.0, 42), (5.0, 50), (8.0, 60), (20, 90), (45, 100)],
    "uni": [(0.12, 0), (0.2, 10), (0.3, 30), (0.4, 60), (0.6, 95), (0.85, 100)],
}


def Dx(curve, p):
    for d, q in curve:
        if q == p:
            return d
    raise ValueError


def fig6():
    x0, x1 = 90, 790
    lo, hi = -2, 2                      # 0.01 .. 100 mm
    X = lambda d: x0 + (math.log10(d) - lo) / (hi - lo) * (x1 - x0)
    py0, py1 = 340, 70
    Y = lambda p: py0 - p / 100 * (py0 - py1)
    b = [T(440, 24, "粒徑分佈曲線（按真實對數座標；D_{10}、D_{30}、D_{60} 為曲線上的讀值）", 15, "#0d47a1", weight=700)]
    for a, c, f, lab, lx_, lp in [(0.01, 0.075, "#eceff1", "細料（粉土＋黏土）", 0.0274, 93), (0.075, 4.75, "#fff8e1", "砂", 1.6, 4),
                                  (4.75, 100, "#efebe9", "礫石", 30, 4)]:
        b.append(R(X(a), py1, X(c) - X(a), py0 - py1, f))
        b.append(T(X(lx_), Y(lp), lab, 12, "#8d6e63", weight=700))
    for p in range(0, 101, 20):
        b.append(L(x0, Y(p), x1, Y(p), "#e0e0e0", 1))
        b.append(T(x0 - 6, Y(p) + 4, f"{p}", 10.5, MUT, "end"))
    for k in range(lo, hi + 1):
        for m in range(1, 10):
            d = m * 10 ** k
            if d > 10 ** hi: break
            b.append(L(X(d), py0, X(d), py0 + (6 if m == 1 else 3), "#455a64", 1))
        b.append(L(X(10 ** k), py1, X(10 ** k), py0, "#cfd8dc", 1))
        b.append(T(X(10 ** k), py0 + 18, f"{10**k:g}", 10.5, MUT))
    b.append(L(x0, py0, x1, py0, "#455a64", 1.8)); b.append(L(x0, py0, x0, py1, "#455a64", 1.8))
    b.append(T(440, py0 + 36, "粒徑 D (mm，對數座標) →　變粗", 12, "#455a64"))
    b.append(T(38, (py0 + py1) / 2, "通過百分比 (%)", 12, "#455a64", "middle", None,
               f' transform="rotate(-90 38 {(py0+py1)/2:.1f})"'))
    for d, lab in [(0.075, "#200"), (0.425, "#40"), (2.0, "#10"), (4.75, "#4")]:
        b.append(L(X(d), py1 - 4, X(d), py0, "#8d6e63", 1.2, "3,3"))
        b.append(T(X(d), py1 - 8, f"{lab} {d:g}", 10.5, "#5d4037"))
    styles = {"well": ("#1565c0", None, 3), "gap": ("#c62828", "8,5", 2.4), "uni": ("#2e7d32", "2,3", 2.6)}
    res = {}
    for key, pts in GSD.items():
        ds, ps = zip(*pts)
        f = PchipInterpolator(np.log10(ds), ps)
        ld = np.linspace(math.log10(ds[0]), math.log10(ds[-1]), 160)
        pv = np.clip(f(ld), 0, 100)
        col, dash, sw = styles[key]
        b.append(PL([(X(10 ** a), Y(c)) for a, c in zip(ld, pv)], col, sw, dash))
        D10, D30, D60 = Dx(pts, 10), Dx(pts, 30), Dx(pts, 60)
        Cu, Cc = D60 / D10, D30 ** 2 / (D10 * D60)
        p200 = float(f(math.log10(0.075))) if ds[0] < 0.075 else 0.0
        res[key] = dict(D10=D10, D30=D30, D60=D60, Cu=Cu, Cc=Cc, p200=p200)
    NUM["gsd"] = res
    # well-graded: leaders to axis
    r = res["well"]
    for p, d in [(10, r["D10"]), (30, r["D30"]), (60, r["D60"])]:
        b.append(L(x0, Y(p), X(d), Y(p), "#1565c0", 1.1, "4,3"))
        b.append(L(X(d), Y(p), X(d), py0, "#1565c0", 1.1, "4,3"))
        b.append(C(X(d), Y(p), 4.5, "#1565c0", "#fff", 1.2))
        b.append(T(X(d) + 5, Y(p) + 16, f"D_{{{p}}} = {d:g}", 11, "#0d47a1", "start", 700) if p != 60 else T(X(d) - 6, Y(p) - 8, f"D_{{{p}}} = {d:g}", 11, "#0d47a1", "end", 700))
    # gap-graded points
    r = res["gap"]
    for p, d in [(10, r["D10"]), (30, r["D30"]), (60, r["D60"])]:
        b.append(C(X(d), Y(p), 4, "#c62828", "#fff", 1.2))
    b.append(T(X(r["D30"]) - 6, Y(30) - 8, f"D_{{30}} = {r['D30']:g}", 11, "#c62828", "end", 700))
    b.append(T(X(r["D60"]) + 7, Y(60) + 14, f"D_{{60}} = {r['D60']:g}", 11, "#c62828", "start", 700))
    b.append(L(X(6.3), Y(29), X(2.2), Y(40.6), "#c62828", 1))
    b.append(T(X(6.5), Y(26), "平台＝缺中間粒徑", 11.5, "#c62828", "start", 700))
    # legend table
    lx, ly = 470, 392
    b.append(R(lx - 380, ly, 760, 70, "#fafafa", "#cfd8dc", 1, ' rx="6"'))
    rows = [("well", "良好級配", "#1565c0", "✓ SW"), ("gap", "間斷級配", "#c62828", "✗ C_{c} < 1"), ("uni", "均勻級配", "#2e7d32", "✗ C_{u} < 6")]
    for i, (k, name, col, verdict) in enumerate(rows):
        r = res[k]; xx = lx - 370 + i * 253
        b.append(L(xx, ly + 20, xx + 28, ly + 20, col, 3, styles[k][1]))
        b.append(T(xx + 34, ly + 25, name, 12.5, col, "start", 700))
        b.append(T(xx + 34, ly + 45, f"C_{{u}} = {r['D60']:g}/{r['D10']:g} = {r['Cu']:.1f}", 11.5, INK, "start"))
        b.append(T(xx + 34, ly + 63, f"C_{{c}} = {r['Cc']:.2f}　{verdict}", 11.5, col, "start", 700))
    return svg(880, 472, b)


# ================================================================ FIG 6-2 plasticity chart
def fig6b():
    x0, x1, y0, y1 = 80, 680, 380, 70
    X = lambda ll: x0 + ll / 100 * (x1 - x0)
    Y = lambda pi: y0 - pi / 60 * (y0 - y1)
    b = [T(400, 26, "塑性圖（USCS）：A 線分黏土／粉土，LL = 50 分低／高塑性", 15, "#0d47a1", weight=700)]
    for ll in range(0, 101, 10):
        b.append(L(X(ll), y0, X(ll), y1, "#eeeeee", 1)); b.append(T(X(ll), y0 + 16, f"{ll}", 10.5, MUT))
    for pi in range(0, 61, 10):
        b.append(L(x0, Y(pi), x1, Y(pi), "#eeeeee", 1)); b.append(T(x0 - 6, Y(pi) + 4, f"{pi}", 10.5, MUT, "end"))
    b.append(L(x0, y0, x1, y0, "#455a64", 1.8)); b.append(L(x0, y0, x0, y1, "#455a64", 1.8))
    b.append(T((x0 + x1) / 2, y0 + 36, "液性限度 LL (%)", 12, "#455a64"))
    b.append(T(36, (y0 + y1) / 2, "塑性指數 PI (%)", 12, "#455a64", "middle", None, f' transform="rotate(-90 36 {(y0+y1)/2:.1f})"'))
    # CL-ML zone: between PI 4 and 7, left of A-line, right of U-line
    llA4 = 4 / 0.73 + 20; llA7 = 7 / 0.73 + 20; llU4 = 4 / 0.9 + 8; llU7 = 7 / 0.9 + 8
    b.append(PG([(X(llU4), Y(4)), (X(llA4), Y(4)), (X(llA7), Y(7)), (X(llU7), Y(7))], "#d1c4e9", "#7e57c2", 1))
    b.append(T(X(llA4) - 2, Y(5.5) + 4, "CL-ML", 10.5, "#4527a0", "end", 700))
    # A-line
    llAend = 60 / 0.73 + 20
    b.append(PL([(X(llA4), Y(4)), (X(min(100, llAend)), Y(0.73 * (min(100, llAend) - 20)))], "#c62828", 2.6))
    b.append(L(X(20), Y(0), X(llA4), Y(4), "#c62828", 1.2, "3,3"))
    # U-line
    llUend = 60 / 0.9 + 8
    b.append(PL([(X(llU7), Y(7)), (X(llUend), Y(60))], "#90a4ae", 1.6, "7,4"))
    b.append(T(X(12), Y(30), "U 線（實測上限）", 11, MUT, "start"))
    b.append(T(X(12), Y(26.6), "PI = 0.9(LL − 8)", 10.5, MUT, "start"))
    # LL = 50
    b.append(L(X(50), y0, X(50), y1, "#1565c0", 1.8, "6,4"))
    b.append(T(X(50) + 4, y1 + 14, "LL = 50", 11.5, "#1565c0", "start", 700))
    ang = -math.degrees(math.atan(0.73 * (y0 - y1) / 60 / ((x1 - x0) / 100)))
    ax, ay = X(78), Y(0.73 * 58) - 9
    b.append(T(ax, ay, "A 線 PI = 0.73(LL − 20)", 12.5, "#c62828", "middle", 700, f' transform="rotate({ang:.1f} {ax:.1f} {ay:.1f})"'))
    for ll, pi in [(20, 0), (50, 21.9)]:
        b.append(C(X(ll), Y(pi), 4.5, "#c62828", "#fff", 1.5))
        b.append(T(X(ll) + 7, Y(pi) + 15, f"({ll}, {pi:g})", 11, "#c62828", "start", 700))
    # zone labels
    for ll, pi, lab, col in [(38, 23, "CL", "#4a148c"), (72, 42, "CH", "#4a148c"), (40, 4, "ML 或 OL", "#455a64"), (80, 13, "MH 或 OH", "#455a64")]:
        b.append(T(X(ll), Y(pi), lab, 15 if len(lab) == 2 else 13, col, weight=700))
    # example soil from fig 5
    b.append(C(X(38), Y(16), 6, "#00695c", "#fff", 2))
    b.append(L(X(38) - 5, Y(16) - 4, X(18), Y(41), "#00695c", 1))
    b.append(T(X(3), Y(47), "圖 5-1 的示例土 (38, 16)", 11.5, "#00695c", "start", 700))
    b.append(T(X(3), Y(43.5), f"A 線在 LL = 38 處 PI = {0.73*18:.1f} < 16 → CL", 11, "#00695c", "start"))
    return svg(760, 430, b)


# ================================================================ FIG 7-1 example C
def figC():
    Gs = 1.620 * 1.70; w = 100 / 1620
    gt = 450 / 0.25 * GW / 1000; gd = gt / (1 + w)
    Ws = 19.50 * 10000; Vb = Ws / gd; Vs = Ws / (Gs * GW)
    Vw_b = Ws * w / GW; Va_b = Vb - Vs - Vw_b
    Vw_f = Ws * 0.08 / GW; Va_f = 10000 - Vs - Vw_f
    dVw = Vw_f - Vw_b; dVa = Va_b - Va_f
    NUM["exC"] = dict(Gs=Gs, gd=gd, Vb=Vb, Vs=Vs, Vw_b=Vw_b, Va_b=Va_b, Vw_f=Vw_f, Va_f=Va_f, dVw=dVw, dVa=dVa)
    k = 280 / Vb; yb = 370; wc = 130
    xb, xf = 230, 540
    b = [arrow_defs((("arC", "#455a64"),)),
         T(440, 26, "範例 C 按比例（高度 ∝ 體積）：乾土重 W_{s} 守恆，體積差全部是孔隙", 15.5, "#0d47a1", weight=700)]
    bb, (yab, ywb, ysb, _) = phase_block(xb, yb, wc, Vs, Vw_b, Va_b, k, size=13)
    bf, (yaf, ywf, ysf, _) = phase_block(xf, yb, wc, Vs, Vw_f, Va_f, k, size=13)
    b += bb + bf
    b.append(T(xb + wc / 2, yab - 26, f"借土場 {Vb:,.0f} m³", 14, INK, weight=700))
    b.append(T(xb + wc / 2, yab - 8, f"γ_{{d}} = {gd:.2f}、w = {w:.2%}", 12, MUT))
    b.append(T(xf + wc / 2, yaf - 26, "填方 10,000 m³", 14, INK, weight=700))
    b.append(T(xf + wc / 2, yaf - 8, "γ_{d} = 19.50、w = 8%", 12, MUT))
    # left dims borrow
    xd = xb - 14
    for ya_, yb_, v in [(yab, ywb, Va_b), (ywb, ysb, Vw_b), (ysb, yb, Vs)]:
        b.append(vdim(xd, ya_, yb_))
    b.append(T(xd - 10, (yab + ywb) / 2 + 5, f"V_{{a}} = {Va_b:,.0f}", 12.5, INK, "end"))
    b.append(T(xd - 10, (ywb + ysb) / 2 + 5, f"V_{{w}} = {Vw_b:,.0f}", 12.5, INK, "end"))
    b.append(T(xd - 10, (ysb + yb) / 2 - 4, f"V_{{s}} = {Vs:,.0f}", 12.5, INK, "end", 700))
    b.append(T(xd - 10, (ysb + yb) / 2 + 14, "= W_{s}/(G_{s}γ_{w})", 11.5, MUT, "end"))
    xd = xf + wc + 14
    for ya_, yb_ in [(yaf, ywf), (ywf, ysf), (ysf, yb)]:
        b.append(vdim(xd, ya_, yb_))
    b.append(T(xd + 10, (yaf + ywf) / 2 + 5, f"V_{{a}} = {Va_f:,.0f}", 12.5, INK, "start"))
    b.append(T(xd + 10, (ywf + ysf) / 2 + 5, f"V_{{w}} = {Vw_f:,.0f}", 12.5, INK, "start"))
    b.append(T(xd + 10, (ysf + yb) / 2 + 5, f"V_{{s}} = {Vs:,.0f}（同左）", 12.5, INK, "start", 700))
    b.append(L(xb + wc, ysb, xf, ysf, "#5d4037", 1.6, "6,4"))
    b.append(T((xb + wc + xf) / 2, ysb + 22, f"W_{{s}} = {Ws:,.0f} kN 不變", 12.5, "#5d4037", weight=700))
    b.append(f'<path d="M{xb+wc+10} {(yab+ywb)/2} L{xf-10} {(yaf+ywf)/2}" stroke="#455a64" stroke-width="1.6" fill="none" marker-end="url(#arC)"/>')
    b.append(T((xb + wc + xf) / 2, (yab + ywb) / 2 - 22, f"空氣被壓掉 {dVa:,.0f} m³", 12.5, "#c62828", weight=700))
    b.append(T((xb + wc + xf) / 2, (ywb + ysb) / 2 - 2, f"加水 +{dVw:,.0f} m³", 12.5, "#0277bd", weight=700))
    b.append(R(130, yb + 18, 620, 30, "#e8f5e9", "#81c784", 1.2, ' rx="6"'))
    b.append(T(440, yb + 38, f"體積對帳：{Vb:,.0f} − 10,000 = {Vb-10000:,.0f} = 壓掉空氣 {dVa:,.0f} − 加水 {dVw:,.0f}",
               12.5, "#1b5e20", weight=700))
    return svg(880, 430, b)


# ================================================================ FIG 7-2 example D
def figD():
    gd1, gd2 = 19.6 / 1.09, 20.6 / 1.11
    x = 20 / (4 * gd1 + gd2)
    Ws1, Ws2 = 4 * x * gd1, x * gd2
    Vs = Ws1 / (2.65 * GW) + Ws2 / (2.70 * GW)
    Gm = 20 / (Vs * GW)
    S = (0.12 * 20 / GW) / (1 - Vs)
    zav12 = Gm * GW / (1 + 0.12 * Gm)
    wz = (1 / 20 - 1 / (Gm * GW)) * GW         # w at which ZAV gives 20
    NUM["exD"] = dict(x=x, Vs=Vs, Gm=Gm, S=S, zav12=zav12, wz=wz)
    px0, px1, py0, py1 = 110, 640, 330, 60
    w0, w1, g0, g1 = 6, 18, 17.5, 21.5
    X = lambda wv: px0 + (wv - w0) / (w1 - w0) * (px1 - px0)
    Y = lambda gv: py0 - (gv - g0) / (g1 - g0) * (py0 - py1)
    b = [T(380, 26, "範例 D 的可行性檢核：指定的夯實狀態落在零空氣孔隙線之上", 15, "#0d47a1", weight=700)]
    ww = np.linspace(w0, w1, 100)
    above = [(X(a), max(py1, Y(Gm * GW / (1 + a / 100 * Gm)))) for a in ww]
    b.append(PG(above + [(X(w1), py1), (X(w0), py1)], "#ffebee"))
    b.append(T(X(16.5), Y(21.1), "S > 100%：物理上不可能", 12, "#c62828", "middle", 700))
    for wv in range(6, 19, 2):
        b.append(L(X(wv), py0, X(wv), py0 + 4, "#455a64", 1)); b.append(T(X(wv), py0 + 16, f"{wv}", 10.5, MUT))
    for gv in np.arange(18, 21.6, 0.5):
        b.append(L(px0 - 4, Y(gv), px0, Y(gv), "#455a64", 1)); b.append(T(px0 - 7, Y(gv) + 4, f"{gv:.1f}", 10.5, MUT, "end"))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T(px1, py0 + 32, "w (%)", 11.5, MUT, "end")); b.append(T(px0 - 4, py1 - 10, "γ_{d} (kN/m³)", 11.5, MUT, "start"))
    for Sv, dash, sw in [(1.0, None, 2.4), (0.95, "5,4", 1.4), (0.90, "2,3", 1.4)]:
        pts = [(X(a), Y(Gm * GW / (1 + a / 100 * Gm / Sv))) for a in ww]
        pts = [p for p in pts if py1 <= p[1] <= py0]
        b.append(PL(pts, "#0288d1", sw, dash))
        k_ = [1.0, 0.95, 0.90].index(Sv); ly_ = Y(18.55) + 20 * k_
        b.append(L(X(6.5), ly_, X(7.6), ly_, "#0288d1", sw, dash))
        b.append(T(X(7.75), ly_ + 4, f"S = {Sv:.0%}" + ("（零空氣孔隙線）" if Sv == 1 else ""), 11.5, "#0277bd", "start", 700 if Sv == 1 else None))
    # target point
    tx, ty = X(12), Y(20)
    b.append(L(tx, py0, tx, ty, "#9e9e9e", 1, "3,3")); b.append(L(px0, ty, tx, ty, "#9e9e9e", 1, "3,3"))
    b.append(f'<path d="M{tx-7} {ty-7} L{tx+7} {ty+7} M{tx-7} {ty+7} L{tx+7} {ty-7}" stroke="#c62828" stroke-width="3"/>')
    b.append(C(tx, Y(zav12), 4.5, "#0288d1", "#fff", 1.5))
    b.append(vdim(tx + 26, ty, Y(zav12), "#c62828", 4))
    b.append(T(tx + 36, ty - 8, f"題目指定 (w = 12%, γ_{{d}} = 20.00) → S = {S:.1%}", 12, "#c62828", "start", 700))
    b.append(T(tx + 36, Y(zav12) + 18, f"同一 w 的上限 γ_{{d}} = {zav12:.2f}（S = 100%）", 12, "#0277bd", "start", 700))
    b.append(T(380, py0 + 56, f"混合土 G_{{s}} = W_{{s}}/(V_{{s}}γ_{{w}}) = 20/({Vs:.3f}×9.81) = {Gm:.3f}；"
               f"零空氣孔隙線 γ_{{d}} = G_{{s}}γ_{{w}}/(1 + wG_{{s}})", 12, "#455a64"))
    return svg(760, 400, b)


if __name__ == "__main__":
    FIG.update(f0=fig0(), f1=fig1(), fA=figA(), f3=fig3(), f4=fig4(), f4b=fig4b(), f5=fig5(),
               f6=fig6(), f6b=fig6b(), fC=figC(), fD=figD())
    import os
    os.makedirs("figs", exist_ok=True)
    for k, v in FIG.items():
        open(f"figs/{k}.svg", "w", encoding="utf-8").write(v)
    print(json.dumps(NUM, indent=1, default=float, ensure_ascii=False))
