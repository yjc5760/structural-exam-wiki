#!/usr/bin/env python3
"""
RC-2024-1 T 形梁斷面 — 題目附圖重繪腳本

用法：python3 gen_RC-2024-1.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2024-1-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
考卷註明未依比例；本圖 As 以下的腹板只示意，不標尺寸（h 考卷未給）。
FIGURES
  fig-1-problem  題目附圖重繪  攔：60 cm 讀成腹板高、自取 d = h − 6
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-case1-max Case 1 三聯圖       攔：a > hf 仍用矩形公式
  fig-2-case2-max Case 2 三聯圖       攔：εu 沿用 0.003、平衡量當最大量
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2024-1"

# ── 判讀清單（RC-2024-1-problem.md §4，已確認）──
BF, TF = 80.0, 20.0       # #1
DS = 60.0                 # #2 翼板底到 As 形心
BW = 40.0                 # #4
TAIL = 10.0               # #3 As 以下腹板（示意，考卷無尺寸）
D = TF + DS


def fig1_problem():
    W, Hc = 640, 600
    s = 3.6
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - BF * s / 2 - 30, oy=110)
    cv.panel("T 形斷面（重繪，示意）", "依題目正本判讀清單 #1–#5；As 以下未標尺寸")
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    yb = -TAIL
    pts = [(x0, yb), (x1, yb), (x1, DS), (BF, DS), (BF, D), (0, D), (0, DS), (x0, DS)]
    cv.polygon(pts, "#EDF1F6", C["member"], 2.6)
    cv.polygon([(BF / 2 - 8, -1.2), (BF / 2 + 8, -1.2), (BF / 2 + 8, 1.2), (BF / 2 - 8, 1.2)], C["member"])
    cv.math((BF / 2, 4.5), "A_{s}", 15, C["text"], weight="700")
    cv.dim((0, D), (BF, D), "80 cm", off=-30, label_off=-14)
    cv.dim((BF, D), (BF, DS), "20 cm", off=-30, label_off=-36)
    cv.dim((BF, DS), (BF, 0), "60 cm", off=-30, label_off=-36)
    cv.line((x1 + 2, 0), (BF + 12, 0), C["dim"], 1, dash="3 3")
    cv.dim((x0, yb), (x1, yb), "40 cm", off=30, label_off=15)
    cv.text_px(cv.X(x1) + 14, cv.Y(yb / 2), "（未標尺寸）", 12, C["muted"], "start")
    cv.text_px(cv.X(BF / 2), cv.Y(yb) + 82, "60 cm 的下端在 As 中心線，不在梁底", 12.5, C["accent"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（圖 1，重繪）",
            sub="翼板 80 × 20、腹寬 40；60 cm 由翼板底量到 As 形心；As 到梁底沒有尺寸",
            note="d = 20 + 60 = 80 cm（考卷已給）；全深 h 未給，本題也不需要",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "60 cm 讀成腹板高、自取 d = h − 6")]

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
# 由題目給定量與 §4 的應變限制現算，檔尾對 §4 公佈值 assert
# 全深 h 考卷未給：斷面只畫到 As 下方 8 cm 並以虛線收邊
# ══════════════════════════════════════════════════════════
T_BF, T_HF, T_BW, T_D, T_ES = 80.0, 20.0, 40.0, 80.0, 2.04e6
CASES = {1: dict(fc=280.0, fy=4200.0, eu=0.003), 2: dict(fc=210.0, fy=6900.0, eu=0.004)}


def tcase(k, et):
    p = CASES[k]
    c = p["eu"] / (p["eu"] + et) * T_D
    a = 0.85 * c
    cf = 0.85 * p["fc"] * (T_BF - T_BW) * T_HF
    cw = 0.85 * p["fc"] * T_BW * a
    return dict(c=c, a=a, cf=cf, cw=cw, As=(cf + cw) / p["fy"], ey=p["fy"] / T_ES, **p)


R1 = tcase(1, 0.004)                                  # Case 1 最大鋼筋量
R2 = tcase(2, 0.004)                                  # Case 2 最大鋼筋量
R2B = tcase(2, CASES[2]["fy"] / T_ES)                 # Case 2 平衡
ASMIN1 = 14 / 4200 * T_BW * T_D


def _fig(k, R, name, extra):
    path = os.path.join(OUT, f"{TAG}-fig-{k}-{name}.svg")
    section3(T_BF, T_HF, T_BW, T_D + 8, False, R["c"], R["a"], R["eu"], R["ey"],
             layers=[dict(z=T_D, n=1, kind="T", eps=0.004)],
             forces=[dict(z=T_HF / 2, F=R["cf"], kind="C", name="C_{f}"),
                     dict(z=R["a"] / 2, F=R["cw"], kind="C", name="C_{w}"),
                     dict(z=T_D, F=R["As"] * R["fy"], kind="T", name="T")],
             sec_sub=f"f'c = {R['fc']:g}、fy = {R['fy']:g}、εu = {R['eu']:g}",
             width_labels=("80", "40"),
             depth_dims=[(0, T_HF, "20", "R", 26), (0, T_D, f"d={T_D:g}", "R", 40, T_BW / 2)],
             **extra, path=path)
    return path


def fig1_case1():
    return _fig(1, R1, "case1-max", dict(
        title=f"{TAG}　Case 1 最大鋼筋量：εt = 0.004 → c = {R1['c']:.2f}、a = {R1['a']:.2f} > hf = 20",
        sub=f"Cf（翼板懸出）＋Cw（腹板 bw·a）= T → As,max = {R1['As']:.1f} cm²；As,min = 14/fy·bw·d = {ASMIN1:.2f} cm²",
        note="應力塊已伸入腹板：用 b = 80 的矩形公式會高估壓力、As,max 偏大"))


def fig2_case2():
    return _fig(2, R2, "case2-max", dict(
        title=f"{TAG}　Case 2 最大鋼筋量：εu = 0.004、εt = 0.004 → c = {R2['c']:.1f}、a = {R2['a']:.1f}",
        sub=f"As,max = {R2['As']:.1f} cm²；平衡 εs = εy = {R2['ey']:.6f} → cb = {R2B['c']:.2f}、As,b = {R2B['As']:.1f} cm²",
        note="εu 改為 0.004 後 c 變深；εy 也較大（0.00338），As,max 仍小於 As,b，最大量由 εt = 0.004 控制"))


FIGURES += [(fig1_case1, "§4 Case 1", "a > hf 仍用矩形公式；εt 限制取錯"),
            (fig2_case2, "§4 Case 2", "εu 仍用 0.003；平衡量與最大量搞混")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    assert D == 80.0
    print("assert OK")
    assert abs(R1["c"] - 34.29) < 0.01 and abs(R1["a"] - 29.14) < 0.01 and abs(R1["As"] - 111.4) < 0.05
    assert abs(R1["cf"] + R1["cw"] - 467840) < 5 and abs(ASMIN1 - 10.67) < 0.01
    assert abs(R2B["c"] - 43.35) < 0.01 and abs(R2B["a"] - 36.84) < 0.01 and abs(R2B["As"] - 58.8) < 0.05
    assert abs(R2["c"] - 40.0) < 1e-9 and abs(R2["As"] - 55.9) < 0.05 and abs(R2["cf"] + R2["cw"] - 385560) < 1
    print("assert（解題圖解）OK")
