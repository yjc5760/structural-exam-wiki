#!/usr/bin/env python3
"""
RC-2022-1 雙筋矩形梁斷面（雙層拉力筋）— 題目附圖重繪腳本

用法：python3 gen_RC-2022-1.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2022-1-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
鋼筋直徑取考卷表 1 標稱直徑，按真實比例畫。
FIGURES
  fig-1-problem  題目附圖重繪  攔：2.5 cm 當中心距；淨保護層量到主筋；D22 位置畫錯
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-strain    雙層拉力筋三聯圖    攔：壓力筋直接當降伏
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2022-1"

# ── 判讀清單（RC-2022-1-problem.md §4，已確認）──
B, H = 30.0, 60.0         # #1
COV = 4.0                 # #2 淨保護層（到箍筋外緣）
DS = 1.27                 # #3 箍筋 D13
D25, D22, D19 = 2.54, 2.22, 1.91   # 表 1 標稱直徑
CLR = 2.5                 # #6 上下層淨距


def fig1_problem():
    W, Hc = 640, 660
    s = 7.0
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - B * s / 2 - 30, oy=120)
    cv.panel("梁斷面（重繪，真實比例）", "依題目正本判讀清單 #1–#7")
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.4)
    # 箍筋（外緣距面 4 cm，線寬中心在 4 + DS/2）
    e = COV + DS / 2
    cv.poly([(e, e), (B - e, e), (B - e, H - e), (e, H - e), (e, e)], C["member"], DS * s * 0.8)
    xin0, xin1 = COV + DS, B - COV - DS
    # 下層 3-D25
    y25 = COV + DS + D25 / 2
    xs25 = [xin0 + D25 / 2, B / 2, xin1 - D25 / 2]
    for x in xs25:
        cv.circle((x, y25), D25 / 2, fill=C["tension"], stroke="#FFFFFF", w=1)
    # 上層 2-D22（在兩側 D25 正上方，淨距 2.5）
    y22 = COV + DS + D25 + CLR + D22 / 2
    for x in (xs25[0], xs25[2]):
        cv.circle((x, y22), D22 / 2, fill="#FFFFFF", stroke=C["tension"], w=2)
    # 壓力筋 2-D19（頂角）
    y19 = H - COV - DS - D19 / 2
    for x in (xin0 + D19 / 2, xin1 - D19 / 2):
        cv.circle((x, y19), D19 / 2, fill=C["compr"], stroke="#FFFFFF", w=1)
    # 尺寸
    cv.dim((0, 0), (B, 0), "30 cm", off=34, label_off=15)
    cv.dim((0, 0), (0, H), "60 cm", off=-72, label_off=-28)
    cv.dim((B, H), (B, H - COV), "4 cm", off=-28, label_off=-30)
    cv.dim((B, COV), (B, 0), "4 cm", off=-28, label_off=-30)
    for yy in (H - COV / 2, COV / 2):
        cv.text_px(cv.X(B) + 76, cv.Y(yy), "淨保護層（到箍筋外緣）", 12, C["muted"], "start")
    cv.dim((0, y25 + D25 / 2), (0, y22 - D22 / 2), "2.5 cm", off=-22, label_off=-28)
    # 標籤
    cv.text_px(cv.X(B / 2), cv.Y(y19) + 26, "2-D19", 13, C["compr"], weight="700")
    cv.text_px(cv.X(B / 2), cv.Y(y22) - 2, "2-D22", 13, C["tension"], weight="700")
    cv.text_px(cv.X(B / 2), cv.Y(y25) + 28, "3-D25", 13, C["tension"], weight="700")
    cv.text_px(cv.X(B / 2), cv.Y(H / 2), "D13 箍筋", 13, C["member"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（重繪）",
            sub="30 × 60 cm；D13 箍筋、淨保護層 4 cm 量到箍筋外緣；下層 3-D25、其上 2-D22（淨距 2.5）、頂角 2-D19",
            note="2.5 cm 是兩層鋼筋的淨距（D22 底緣到 D25 頂緣），不是中心距",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "2.5 cm 當中心距；保護層量到主筋")]

# ══════════════════════════════════════════════════════════
# 斷面／應變／內力三聯圖（T 形、雙筋、多層拉力筋、受壓面可在下方）
# 本段為 RC-U1-1 批 2 圖解共用寫法，各題腳本各存一份（腳本須可獨立重跑）
# ══════════════════════════════════════════════════════════
def _sec_outline(bf, hf, bw, hdraw):
    """回傳 [(x, z)]，z 由受壓面往內量；矩形時 bf == bw。"""
    if bf <= bw or hf <= 0:
        return [(-bw/2, 0), (bw/2, 0), (bw/2, hdraw), (-bw/2, hdraw)]
    return [(-bf/2, 0), (bf/2, 0), (bf/2, hf), (bw/2, hf), (bw/2, hdraw),
            (-bw/2, hdraw), (-bw/2, hf), (-bf/2, hf)]


def _comp_zone(bf, hf, bw, a):
    if bf <= bw or hf <= 0 or a <= hf:
        w = bf if (bf > bw and hf > 0) else bw
        return [[(-w/2, 0), (w/2, 0), (w/2, a), (-w/2, a)]]
    return [[(-bf/2, 0), (bf/2, 0), (bf/2, hf), (-bf/2, hf)],
            [(-bw/2, hf), (bw/2, hf), (bw/2, a), (-bw/2, a)]]


def section3(bf, hf, bw, hdraw, h_known, c, a, eps_cu, eps_y, layers, forces,
             flip=False, PW=340, PH=470, title=None, sub=None, note=None, path=None,
             sec_sub="", width_labels=None, depth_dims=()):
    """layers: [dict(z=深度, n=根數, kind='T'|'C', name='3-D25', eps=應變(拉正壓負))]
       forces: [dict(z=合力位置, F=kgf, kind='C'|'T', name='C_{c}')]
       depth_dims: [(z0, z1, '標註', 側別 'L'|'R', 偏移px)] 畫在斷面圖上"""
    top, bot = 118, 56
    ky = (PH - top - bot) / hdraw

    def zy(z):                       # 深度 → Canvas 的 y（Canvas 會再翻轉）
        py = (PH - bot - z*ky) if flip else (top + z*ky)
        return PH - py

    # ---- 斷面 ----
    kx = min(ky, (PW - 120) / bf)
    p1 = Canvas(PW, PH)
    p1.panel("斷面", sec_sub)
    X1 = lambda x: PW/2 - 8 + x*kx
    P1 = lambda x, z: (X1(x), zy(z))
    out = _sec_outline(bf, hf, bw, hdraw)
    p1.polygon([P1(*q) for q in out], "#EDF1F6", C["member"], 2.4)
    if not h_known:                  # 全深未給：遠端以虛線收邊
        p1.line(P1(-bw/2, hdraw), P1(bw/2, hdraw), "#EDF1F6", 4)
        p1.line(P1(-bw/2, hdraw), P1(bw/2, hdraw), C["muted"], 1.6, dash="5 4")
        p1.text(P1(0, hdraw), "全深未給", 11.5, C["muted"], dy=(-12 if flip else 12))
    for zone in _comp_zone(bf, hf, bw, a):
        p1.polygon([P1(*q) for q in zone], C["fill_c"], "none")
    p1.line(P1(-bf/2 - 4, a), P1(bf/2 + 4, a), C["compr"], 1.6, dash="6 4")
    p1.line(P1(-bf/2 - 4, c), P1(bf/2 + 4, c), C["accent"], 1.6, dash="3 3")
    for L_ in layers:
        n = L_["n"]
        for i in range(n):
            xb = (-bw/2 + bw*(0.18 + 0.64*i/(n - 1))) if n > 1 else 0
            p1.dot(P1(xb, L_["z"]), 5.2,
                   fill=(C["tension"] if L_["kind"] == "T" else C["compr"]), stroke="#FFFFFF", w=1.2)
    if width_labels:
        wt, wb = width_labels
        p1.dim(P1(-bf/2, 0), P1(bf/2, 0), wt, off=(24 if flip else -24), label_off=(13 if flip else -13))
        if bf > bw:
            p1.dim(P1(-bw/2, hdraw), P1(bw/2, hdraw), wb, off=(-24 if flip else 24), label_off=(-13 if flip else 13))
    for dd in depth_dims:
        z0, z1, lab, side, off = dd[:5]
        if len(dd) > 5:
            x = dd[5]                # 指定量測線所在的 x（例如沿腹板外緣）
        else:
            x = (bf/2 if side == "R" else -bf/2)
            x = x if z0 < hf or bf <= bw else (bw/2 if side == "R" else -bw/2)
        sgn = 1 if side == "R" else -1
        o = off if flip else -off
        p1.dim(P1(x, z0), P1(x, z1), lab, off=sgn*o, label_off=sgn*(-12 if not flip else 12))
    sg = -1 if flip else 1           # 正常方向：a 線在上、標籤寫在線上方；N.A. 標籤寫在線下方
    p1.text_px(12, PH - zy(c) + 9*sg, "N.A.", 11, C["accent"], "start", weight="700")
    p1.math_px(18, PH - zy(a) - 9*sg, "a", 13, C["compr"], weight="700")

    # ---- 應變 ----
    p2 = Canvas(PW, PH)
    p2.panel("應變（平面保持平面）", f"中性軸 c = {c:.2f} cm")
    x0 = PW*0.40
    zmax = max(L_["z"] for L_ in layers)
    emax = max([eps_cu] + [abs(L_["eps"]) for L_ in layers])
    ks = 92 / emax
    P2 = lambda e, z: (x0 + e*ks, zy(z))     # 壓應變畫在右（正）、拉應變畫在左
    p2.line(P2(0, -2), P2(0, zmax + 3), C["ghost"], 2, dash="5 4")
    p2.polygon([P2(0, 0), P2(eps_cu, 0), P2(0, c)], C["fill_c"], C["compr"], 2.2)
    et_far = eps_cu*(zmax - c)/c
    p2.polygon([P2(0, c), P2(-et_far, zmax), P2(0, zmax)], C["fill_t"], C["tension"], 2.2)
    for s in (1, -1):               # ±εy 參考線
        p2.line(P2(s*eps_y, -1), P2(s*eps_y, zmax + 2), C["accent"], 1.2, dash="2 3")
    if flip:                         # 受壓面在下：εy 標在下緣外側，避開拉力筋標註
        p2.math_px(x0 - eps_y*ks, PH - zy(0) + 16, "ε_{y}", 12, C["accent"])
    else:
        p2.math_px(x0 + eps_y*ks, PH - zy(zmax + 2) + 14, "ε_{y}", 12, C["accent"])
    p2.math_px(x0 + eps_cu*ks + 4, PH - zy(0) + (10 if not flip else -10),
               f"ε_{{cu}}={eps_cu:g}", 12, C["compr"], "start", weight="700")
    used2 = [PH - zy(0) + (10 if not flip else -10)]
    for L_ in layers:
        e = L_["eps"]
        col = C["tension"] if e > 0 else C["compr"]
        p2.dot(P2(-e, L_["z"]), 4.2, fill=col)
        tag = "ε_{s}" if L_["kind"] == "T" else "ε'_{s}"
        yy = PH - zy(L_["z"]) - (9 if e > 0 else 0)
        for _ in range(12):
            hit = [u for u in used2 if abs(u - yy) < 17]
            if not hit: break
            yy = (max(hit) + 17) if not flip else (min(hit) - 17)
        used2.append(yy)
        p2.math_px(x0 + 8 if e > 0 else x0 + (-e)*ks + 8, yy,
                   f"{tag}={abs(e):.5f}", 12, col, "start", weight="700")
    p2.text_px(x0 + 6, PH - zy(c), "N.A.", 11.5, C["accent"], "start", weight="700")

    # ---- 內力 ----
    p3 = Canvas(PW, PH)
    p3.panel("內力（kgf → tf）", f"等值應力塊 a = {a:.2f} cm")
    x3 = PW*0.42
    Fmax = max(abs(f["F"]) for f in forces)
    P3 = lambda x, z: (x3 + x, zy(z))
    blk = 58
    for zone in _comp_zone(bf, hf, bw, a):
        zs = [q[1] for q in zone]
        z0, z1 = min(zs), max(zs)
        wfrac = (zone[1][0] - zone[0][0]) / bf
        p3.polygon([P3(0, z0), P3(blk*wfrac, z0), P3(blk*wfrac, z1), P3(0, z1)], C["fill_c"], C["compr"], 1.6)
    p3.line(P3(0, -2), P3(0, zmax + 3), C["ghost"], 2, dash="5 4")
    used = []

    arrow_ys = [PH - zy(f["z"]) for f in forces]

    def free_y(y0, alts):
        for y in [y0] + [y0 + d for d in alts]:
            if all(abs(u - y) >= 16 for u in used) and all(abs(ay - y) >= 9 for ay in arrow_ys):
                used.append(y); return y
        used.append(y0); return y0

    for f in forces:
        L = 26 + 64*abs(f["F"])/Fmax
        if f["kind"] == "C":
            p3.arrow(P3(blk + 6 + L, f["z"]), P3(blk + 6, f["z"]), C["compr"], 2.8, 10)
            p3.math_px(x3 + blk + 20, free_y(PH - zy(f["z"]) - 17, (35, -34, 52, -50, 68)), f'{f["name"]}={f["F"]/1000:.1f}', 12, C["compr"], "start", weight="700")
        else:
            p3.arrow(P3(-4, f["z"]), P3(-4 - L, f["z"]), C["tension"], 2.8, 10)
            p3.math_px(x3 + 8, free_y(PH - zy(f["z"]) - 17, (35, -34, 52, -50, 68)), f'{f["name"]}={f["F"]/1000:.1f}', 12, C["tension"], "start", weight="700")
    return compose([p1, p2, p3], title=title, sub=sub, note=note, path=path)


# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
# 常數只放 RC-2022-1.md §4 公佈的 c；其餘由幾何與應變相容現算，檔尾對 §4 assert
# ══════════════════════════════════════════════════════════
FC, FY, ES, ECU = 280.0, 5600.0, 2.04e6, 0.003
C_SOL = 17.66                                   # §4 Step 4 二次方程解
Y1, Y2 = 4 + 1.27 + 2.54/2, 4 + 1.27 + 2.54 + 2.5 + 2.22/2   # §4 Step 1：6.54、11.42（距底）
DP_ = 4 + 1.27 + 1.91/2                          # d' = 6.225
AS1, AS2, ASP = 3*5.067, 2*3.871, 2*2.865
D1, D2 = H - Y1, H - Y2
DBAR = H - (AS1*Y1 + AS2*Y2)/(AS1 + AS2)         # 51.81（§4 取形心 d）
A_SOL = 0.85*C_SOL
EPSY = FY/ES
eps = lambda z: ECU*(z - C_SOL)/C_SOL            # 拉正
FSP = min(ES*(-eps(DP_)), FY)
CC = 0.85*FC*A_SOL*B
CSN = ASP*(FSP - 0.85*FC)
T1, T2 = AS1*FY*(1 if eps(D1) >= EPSY else ES*eps(D1)/FY), AS2*FY*(1 if eps(D2) >= EPSY else ES*eps(D2)/FY)
MN = CC*(DBAR - A_SOL/2) + CSN*(DBAR - DP_)


def fig1_section():
    path = os.path.join(OUT, f"{TAG}-fig-1-strain.svg")
    section3(B, 0, B, H, True, C_SOL, A_SOL, ECU, EPSY,
             layers=[dict(z=DP_, n=2, kind="C", eps=eps(DP_)),
                     dict(z=D2, n=2, kind="T", eps=eps(D2)),
                     dict(z=D1, n=3, kind="T", eps=eps(D1))],
             forces=[dict(z=A_SOL/2, F=CC, kind="C", name="C_{c}"),
                     dict(z=DP_, F=CSN, kind="C", name="C'_{s}"),
                     dict(z=D2, F=T2, kind="T", name="T_{2}"),
                     dict(z=D1, F=T1, kind="T", name="T_{1}")],
             sec_sub="30 × 60；3-D25＋2-D22／2-D19",
             width_labels=("30", "30"),
             depth_dims=[(0, DP_, "d'", "L", 26), (0, D2, f"{D2:.2f}", "R", 30), (0, D1, f"{D1:.2f}", "R", 62)],
             title=f"{TAG}　雙層拉力筋＋壓力筋：斷面／應變／內力",
             sub=f"c = {C_SOL} cm（§4 Step 4）；各層應變由平面保持平面算出；ε_y = fy/Es = {EPSY:.6f}".replace("ε_y", "εy"),
             note=f"d' = {DP_:.3f}；壓力筋 ε's = {-eps(DP_):.5f} < εy → f's = {FSP:.0f}，未降伏；兩層拉力筋都已降伏（D22 層 εs = {eps(D2):.5f}）",
             path=path)
    return path


FIGURES += [(fig1_section, "§4 Step 5", "壓力筋直接當降伏；只用形心 d 而不知上層 D22 是否降伏")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    assert abs((COV + DS + D25 / 2) - 6.54) < 1e-9
    print("assert OK")
    # ── 解題圖解對 §4 公佈值 assert ──
    assert abs(A_SOL - 15.01) < 0.01 and abs(DBAR - 51.81) < 0.01
    assert abs(-eps(DP_) - 0.001943) < 2e-6 and abs(FSP - 3963.7) < 1.0
    assert abs(CC - 107171) < 60 and abs(CSN - 21348) < 15 and abs(MN/1e5 - 57.21) < 0.02
    print("assert（解題圖解）OK")
