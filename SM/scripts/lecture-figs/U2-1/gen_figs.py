"""lecture-SM-U2-1 figures redrawn 2026-11-22 (k1 gross/net, k2 three-layer head, k3 flow net, k4 SM-2015-4 bars).
Usage: python3 gen_figs.py <lecture.html>"""
import sys, os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'U1-1')); sys.path.insert(0, HERE)
from svglib import *
from calcs import N
import numpy as np
FIG = {}
BRN, BLU, RED, GRN, ORG, PUR, TEAL = "#6d4c41", "#1565c0", "#c62828", "#2e7d32", "#ef6c00", "#6a1b9a", "#00838f"
def arr(x1, y1, x2, y2, c, mk, sw=2.2, dash=None):
    return L(x1, y1, x2, y2, c, sw, dash, f' marker-end="url(#{mk})"')

def k1():
    r = N['10_4']; sc = 0.5; base = 330
    b = [arrow_defs((("k1a", RED),))]
    def col(ox, title, net):
        b.append(T(ox + 150, 30, title, 13.5, BLU if not net else GRN, weight=700))
        x = ox + 90; w = 70
        b.append(L(ox + 20, base, ox + 300, base, "#455a64", 1.4))
        b.append(R(x, base - r['q']*sc, w, r['q']*sc, "#cfd8dc", "#78909c", 1))
        if not net:
            b.append(R(x, base - r['qu']*sc, w, (r['qu'] - r['q'])*sc, "#bbdefb", BLU, 1.2))
            b.append(L(x - 20, base - r['qall_gross']*sc, x + w + 70, base - r['qall_gross']*sc, RED, 1.8, "6,4"))
            b.append(T(x + w + 72, base - r['qall_gross']*sc + 4, f"q_{{all}} = {r['qall_gross']:.1f}", 12, RED, "start", 700))
            b.append(arr(x - 30, base - r['qu']*sc, x - 30, base - r['qall_gross']*sc, RED, "k1a", 2))
            b.append(T(x - 36, base - (r['qu'] + r['qall_gross'])/2*sc, "÷ 3", 12, RED, "end", 700))
            b.append(T(ox + 150, base + 22, "q_{all} = q_{ult} / FS", 12, INK))
        else:
            b.append(R(x, base - r['qu']*sc, w, r['qnet']*sc, "#c8e6c9", GRN, 1.2))
            b.append(L(x - 20, base - r['qall_net']*sc, x + w + 70, base - r['qall_net']*sc, RED, 1.8, "6,4"))
            b.append(T(x + w + 72, base - r['qall_net']*sc + 4, f"q_{{all}} = {r['qall_net']:.1f}", 12, RED, "start", 700))
            b.append(arr(x - 30, base - r['qu']*sc, x - 30, base - (r['qnet']/3 + r['q'])*sc, RED, "k1a", 2))
            b.append(T(x - 36, base - (r['qu'] + r['qall_net'])/2*sc, "淨值 ÷ 3", 12, RED, "end", 700))
            b.append(T(ox + 150, base + 22, "q_{all} = (q_{ult} − q) / FS + q", 12, INK))
        b.append(T(x + w + 6, base - r['qu']*sc + 12, f"q_{{ult}} = {r['qu']:.1f}", 11.5, BLU, "start"))
        b.append(T(x + w + 6, base - r['q']*sc/2 + 4, f"q = γD_{{f}} = {r['q']:.0f}", 11, MUT, "start"))
    col(30, "總（gross）觀點：整根柱子除以 FS", False)
    col(430, "淨（net）觀點：只有多出來的部分除以 FS", True)
    b.append(T(400, 380, f"SM-2010-4（依題解數值、縱軸 1 kPa = {sc} px）：同一組參數，兩種定義 146.4 與 167.7 kPa，差約 15%", 11.5, MUT))
    return svg(800, 392, b)

def k2():
    r = N['22_3']; h = r['h']; H = r['H']
    b = [T(150, 26, "三層串聯（水由上往下）", 13.5, BLU, weight=700), T(560, 26, "總水頭沿深度的變化（按比例）", 13.5, BLU, weight=700)]
    top = 60; sc = 1.2   # px per mm depth
    cols = ["#ffe0b2", "#c8e6c9", "#ffcdd2"]; nm = "ABC"
    z = [0, 50, 150, 200]
    for i in range(3):
        b.append(R(90, top + z[i]*sc, 70, H[i]*sc, cols[i], "#8d6e63", 1.2))
        b.append(T(125, top + (z[i] + z[i+1])/2*sc + 4, nm[i], 13, INK, weight=700))
        b.append(T(84, top + (z[i] + z[i+1])/2*sc + 4, f"{H[i]} mm", 11, MUT, "end"))
        b.append(T(166, top + (z[i] + z[i+1])/2*sc + 4, "k = " + ["10⁻² cm/s", "10⁻¹ cm/s", "10⁻³ cm/s"][i], 11, MUT, "start"))
    for i, lab in enumerate("abcd"):
        b.append(T(166 + 110, top + z[i]*sc + 4, lab, 11, MUT, "start"))
    b.append(T(150, top + 200*sc + 38, "R = H/k：5000 / 1000 / 50000（C 層佔 89%）", 11.5, RED))
    # right plot: x = head, y = depth (same depth scale)
    px0, px1 = 380, 760
    X = lambda v: px0 + v/600*(px1 - px0); Y = lambda d: top + d*sc
    b.append(L(px0, top, px1, top, "#455a64", 1.3)); b.append(L(px0, top, px0, Y(200), "#455a64", 1.3))
    for v in (0, 200, 400, 600):
        b.append(T(X(v), top - 8, f"{v}", 10.5, MUT))
    b.append(T(px1, top - 22, "總水頭 h (mm)", 11, MUT, "end"))
    for d in z:
        b.append(L(px0, Y(d), px1, Y(d), "#eceff1", 1, "3,3"))
    pts = [(X(hh), Y(d)) for hh, d in zip(h, z)]
    b.append(PL(pts, BLU, 2.8))
    for (xx, yy), hh, lab in zip(pts, h, "abcd"):
        b.append(C(xx, yy, 4, BLU))
    b.append(T(X(h[0]) - 6, Y(0) + 16, f"h_{{a}} = {h[0]:.0f}", 11.5, BLU, "end"))
    b.append(T(X(h[1]) - 6, Y(50) + 4, f"h_{{b}} = {h[1]:.1f}", 11.5, BLU, "end"))
    b.append(T(X(h[2]) - 8, Y(150) + 2, f"h_{{c}} = {h[2]:.1f}", 11.5, BLU, "end"))
    b.append(T(X(0) + 8, Y(200) + 16, "h_{d} = 0（基準）", 11.5, BLU, "start"))
    for i, (d0, d1) in enumerate([(0, 50), (50, 150), (150, 200)]):
        b.append(T(X(150), Y((d0 + d1)/2) - (12 if i == 2 else -4), f"層 {nm[i]}：Δh = {r['dh'][i]:.1f} mm，i = {r['i'][i]:.3g}", 11.5, RED, "start"))
    b.append(T(560, Y(200) + 38, "坡降越大的層，水頭線越平（同樣深度掉更多水頭）", 11.5, INK))
    return svg(800, 346, b)

def k3():
    from flownet import head, stream, xs, ys, JB, JW, I0, I50
    import contourpy
    H = head(); P = stream()
    b = [T(400, 24, "SM-2018-3 的幾何：數值解流線與等勢線（作答仍依考卷流網：N_{f} = 3、N_{d} = 10）", 13.5, "#0d47a1", weight=700)]
    xa, xb, ya, yb = -26, 76, -17.2, 7.5
    U = 7.2; ox, oy = 40, 70
    X = lambda x: ox + (x - xa)*U; Y = lambda y: oy + (yb - y)*U
    b.append(R(X(xa), Y(6.3), (0 - xa)*U, 6.3*U, "#e1f5fe"))
    b.append(L(X(xa), Y(6.3), X(0), Y(6.3), BLU, 1.6)); b.append(T(X(xa) + 4, Y(6.3) - 6, "上游水面", 11, BLU, "start"))
    b.append(R(X(xa), Y(0), (xb - xa)*U, 17.2*U, "#f5f0e8"))
    b.append(R(X(xa), Y(-17.2), (xb - xa)*U, 10, "#b0bec5"))
    b.append(T(X(xb) - 4, Y(-17.2) + 9, "不透水層", 10.5, "#37474f", "end"))
    b.append(L(X(xa), Y(0), X(xb), Y(0), "#5d4037", 1.6))
    b.append(T(X(xb) - 4, Y(0) - 6, "下游水面＝地表", 11, BLU, "end"))
    b.append(R(X(0), Y(6.8), 50*U, 8.4*U, "#90a4ae", "#455a64", 1.4))
    b.append(T(X(25), Y(2.5), "混凝土壩（寬 50 m）", 12, "#263238", weight=700))
    b.append(R(X(-0.25), Y(-1.6), 0.5*U, 7.8*U, "#37474f"))
    gx, gy = np.meshgrid(xs, ys, indexing='ij')
    def lines(F, levels, col, sw, dash=None):
        cg = contourpy.contour_generator(gx, gy, np.ma.masked_invalid(F))
        for lv in levels:
            for seg in cg.lines(lv):
                pts = [(X(x), Y(y)) for x, y in seg if xa <= x <= xb]
                if len(pts) > 2: b.append(PL(pts, col, sw, dash))
    lines(H, [6.3*(1 - n/10) for n in range(1, 10)], RED, 1.1)
    lines(P, [1/3, 2/3], TEAL, 2.0)
    # boundary flow lines
    b.append(PL([(X(-0.25), Y(-1.6)), (X(-0.25), Y(-9.4)), (X(0.25), Y(-9.4)), (X(0.25), Y(-1.6)), (X(50), Y(-1.6))], TEAL, 2.6))
    b.append(L(X(xa), Y(-17.2), X(xb), Y(-17.2), TEAL, 2.6))
    for nm, x in zip('abcde', [0.25, 12.5, 25, 37.5, 50]):
        b.append(C(X(x), Y(-1.6), 3.5, PUR)); b.append(T(X(x) + (10 if nm == 'a' else 0), Y(-1.6) + 16, nm, 11.5, PUR, weight=700))
    b.append(vdim(X(xa) - 12, Y(6.3), Y(0), "#455a64", 4)); b.append(T(X(xa) - 16, Y(3.15) + 4, "6.3", 10.5, MUT, "end"))
    b.append(vdim(X(52) + 6, Y(0), Y(-1.6), "#455a64", 3)); b.append(T(X(52) + 12, Y(-0.8) + 4, "1.6", 10.5, MUT, "start"))
    b.append(T(X(1.2), Y(-9.4) + 4, "截水牆底 −9.4", 10.5, "#37474f", "start"))
    b.append(T(X(xa) + 4, Y(-17.2) - 6, "−17.2", 10.5, MUT, "start"))
    yl = Y(-17.2) + 34
    b.append(L(60, yl, 90, yl, TEAL, 2.4)); b.append(T(96, yl + 4, "流線：壩底＋牆面、不透水層是兩條邊界流線，中間兩條 → 3 個流槽", 11.5, TEAL, "start"))
    b.append(L(60, yl + 22, 90, yl + 22, RED, 1.2)); b.append(T(96, yl + 26, "等勢線：上游地表 h = 6.3 → 下游地表 h = 0，每條差 0.63 m（10 降），與流線正交", 11.5, RED, "start"))
    return svg(800, int(yl + 44), b)

def k4():
    r = N['15_4']; base = 270; sc = 0.85
    b = [T(400, 24, "SM-2015-4 抽水前後（黏土層中央點，地表下 13 m；長條按比例）", 13.5, "#0d47a1", weight=700)]
    groups = [("總應力 σ", r['sig'], "#b0bec5", "#78909c", "↓ 下降 10 kPa（3–8 m 砂由 γ_{sat} 變 γ_{dry}）"),
              ("孔隙水壓 u", r['u'], "#90caf9", BLU, "↓ 下降 24.5 kPa（滲流水頭，非靜水壓）"),
              ("有效應力 σ′", r['eff'], "#a5d6a7", GRN, "↑ 上升 14.5 kPa → 壓密")]
    for g, (nm, (a, c), f1, s1, note) in enumerate(groups):
        ox = 80 + g*240
        b.append(R(ox, base - a*sc, 50, a*sc, f1, s1, 1, ' opacity="0.55"'))
        b.append(R(ox + 58, base - c*sc, 50, c*sc, f1, s1, 1.4))
        b.append(T(ox + 25, base - a*sc - 6, f"{a:g}", 11.5, INK)); b.append(T(ox + 83, base - c*sc - 6, f"{c:g}", 11.5, INK, weight=700))
        b.append(T(ox + 54, base + 20, nm, 12.5, INK, weight=700)); b.append(T(ox + 54, base + 38, note, 10.5, s1))
    b.append(L(60, base, 760, base, "#455a64", 1.3))
    b.append(R(640, 40, 12, 10, "#b0bec5", "#78909c", 1, ' opacity="0.55"')); b.append(T(658, 49, "抽水前（淡）", 11, MUT, "start"))
    b.append(R(640, 58, 12, 10, "#b0bec5", "#78909c", 1.4)); b.append(T(658, 67, "抽水後（深）", 11, MUT, "start"))
    b.append(T(400, base + 62, "σ′ = σ − u：σ 掉 10、u 掉 24.5 → σ′ 淨增 14.5 kPa", 11.5, INK))
    return svg(800, base + 74, b)

FIG.update(k1=k1(), k2=k2(), k3=k3(), k4=k4())

def inject(path):
    s = open(path, encoding='utf-8').read()
    for k, v in FIG.items():
        tag = f'<!--FIG:{k}-->'
        if s.count(tag) != 1: raise SystemExit(f'marker {tag} count = {s.count(tag)}')
        s = re.sub(re.escape(tag) + r'\s*<svg\b.*?</svg>', lambda m: tag + '\n' + v, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s); print('injected', len(FIG))

if __name__ == '__main__':
    if len(sys.argv) > 1: inject(sys.argv[1])
    else:
        os.makedirs('/tmp/u21figs', exist_ok=True)
        for k, v in FIG.items(): open(f'/tmp/u21figs/{k}.svg', 'w').write(v)
        print('ok')
