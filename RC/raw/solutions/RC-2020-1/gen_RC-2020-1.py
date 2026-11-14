#!/usr/bin/env python3
"""
RC-2020-1 梁版系統 T 形梁 — 題目附圖重繪腳本

用法：python3 gen_RC-2020-1.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2020-1-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
考卷附圖未依比例；本圖水平、垂直分開取比例（垂直放大），同屬示意。
FIGURES
  fig-1-problem  題目附圖重繪  攔：70 讀成翼板底到梁底（h = 80、d = 74）；400 讀成淨距
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-flange    有效翼板寬三條上限  攔：be 用梁中心距 400
  fig-2-tsection  T 形梁三聯圖        攔：a > hf 仍用矩形公式
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2020-1"

# ── 判讀清單（RC-2020-1-problem.md §4，已確認）──
H = 70.0        # #1 版頂到梁腹底（全深）
HF = 10.0       # #2 版厚
COV = 6.0       # #3 拉力筋中心到梁腹底
BW = 50.0       # #4 梁腹寬（三根相同）
S = 400.0       # #5 梁中心距（量到梁腹中心線）
VX = 3.6        # 垂直放大倍數（示意）


def fig1_problem():
    W, Hc = 980, 470
    sx = 0.74
    cv = Canvas(W, Hc, sx=sx, ox=W / 2, oy=120)
    cv.panel("梁版斷面（重繪，示意）", "依題目正本判讀清單 #1–#5；垂直方向放大，與考卷同為未依比例")
    y = lambda v: v * VX          # 垂直放大
    xs = [-S, 0.0, S]
    xl, xr = -S - 160, S + 160
    # 版（兩端斷開）＋三根梁腹
    pts = [(xl, y(H)), (xr, y(H)), (xr, y(H - HF))]
    for xc in reversed(xs):
        pts += [(xc + BW / 2, y(H - HF)), (xc + BW / 2, 0), (xc - BW / 2, 0), (xc - BW / 2, y(H - HF))]
    pts += [(xl, y(H - HF))]
    cv.polygon(pts, "#EDF1F6", C["member"], 2.4)
    for xe in (xl, xr):
        cv.line((xe, y(H) + 6), (xe, y(H - HF) - 6), C["muted"], 1.4, dash="4 3")
    for xc in xs:
        cv.line((xc, y(H) + 70 / sx / 1), (xc, -30), C["dim"], 1.0, dash="6 4")
        cv.dot((xc, y(COV)), 6.5, fill=C["tension"], stroke="#FFFFFF", w=1.2)
    cv.arrow((BW / 2 + 45, y(COV) + 22), (8, y(COV) + 2), C["tension"], 1.6, 8)
    cv.math((BW / 2 + 45, y(COV) + 22), "A_{s}", 15, C["tension"], dx=16, weight="700")
    # 尺寸
    cv.dim((-S, y(H) + 70), (0, y(H) + 70), "400", off=0, label_off=-14)
    cv.dim((0, y(H) + 70), (S, y(H) + 70), "400", off=0, label_off=-14)
    cv.dim((xr, y(H)), (xr, y(H - HF)), "10", off=-24, label_off=-26)
    cv.dim((-S / 2, 0), (-S / 2, y(H)), "70", off=0, label_off=-22)
    cv.dim((-BW / 2, 0), (BW / 2, 0), "50", off=34, label_off=16)
    cv.dim((-BW / 2, 0), (-BW / 2, y(COV)), "6", off=-38, label_off=-14)
    cv.text_px(cv.X(xr) - 4, cv.Y(-38), "單位：cm", 12.5, C["muted"], "end")
    cv.text_px(cv.X(-S / 2) + 30, cv.Y(y(H) * 0.45), "版頂 → 梁腹底", 12, C["accent"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（重繪）",
            sub="版厚 10；70 由版頂量到梁腹底（全深）；6 由拉力筋中心量到梁腹底；梁腹寬 50；400 為梁中心距",
            note="h = 70、d = 64（不是 h = 80、d = 74）；與鄰梁淨距 = 400 − 50 = 350",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "70 讀成翼板底到梁底；400 讀成淨距")]

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
# 由題目給定量與 §4 的分解法現算，檔尾對 §4 公佈值 assert
# ══════════════════════════════════════════════════════════
from recipes import bar_compare
FC, FY, ES, ECU, MU, PHI, SPAN = 210.0, 4200.0, 2.04e6, 0.003, 130e5, 0.9, 500.0
D = H - COV
BE_LIST = [("跨度 / 4", "500 / 4", SPAN / 4),
           ("腹寬 + 2 × 8hf", "50 + 2×80", BW + 2 * 8 * HF),
           ("腹寬 + 淨距", "50 + (400 − 50)", BW + (S - BW))]
BE = min(v for _, _, v in BE_LIST)
CF = 0.85 * FC * (BE - BW) * HF
MNF = CF * (D - HF / 2)
MNW = MU / PHI - MNF
KW = FY / (0.85 * FC * BW)                       # a = KW·Asw
ASW = (D - (D * D - 2 * KW * MNW / FY) ** 0.5) / KW    # Asw·fy·(d − KW·Asw/2) = Mnw 的小根
A_ = KW * ASW
C_ = A_ / 0.85
AS = CF / FY + ASW
ET = ECU * (D - C_) / C_
CW = 0.85 * FC * BW * A_


def fig1_flange():
    path = os.path.join(OUT, f"{TAG}-fig-1-flange.svg")
    cases = [(n, d + ("　→ 控制" if v == BE else ""), v, f"{v:g} cm",
              C["bmd"] if v == BE else C["member2"]) for n, d, v in BE_LIST]
    bar_compare(cases, title=f"{TAG}　有效翼板寬 be：三條上限取最小",
                sub="題文明列三條規定；400 是梁中心距，淨距 = 400 − 50 = 350",
                note=f"be = {BE:g} cm 由跨度控制；誤用 400（梁距）或 210 都會讓翼板多算壓力、As 偏小",
                path=path)
    return path


def fig2_section():
    path = os.path.join(OUT, f"{TAG}-fig-2-tsection.svg")
    section3(BE, HF, BW, H, True, C_, A_, ECU, FY / ES,
             layers=[dict(z=D, n=1, kind="T", eps=ET)],
             forces=[dict(z=HF / 2, F=CF, kind="C", name="C_{f}"),
                     dict(z=A_ / 2, F=CW, kind="C", name="C_{w}"),
                     dict(z=D, F=AS * FY, kind="T", name="T")],
             sec_sub="be = 125、hf = 10、bw = 50、h = 70",
             width_labels=("125", "50"),
             depth_dims=[(0, HF, "10", "R", 26), (0, D, f"d={D:g}", "L", 44, -BW / 2)],
             title=f"{TAG}　T 形梁：a = {A_:.2f} cm > hf = 10，應力塊伸入腹板",
             sub=f"翼板懸出 Cf → Asf = {CF/FY:.2f}；腹板 Cw → Asw = {ASW:.2f}；As = {AS:.2f} cm²",
             note=f"矩形試算 a = 11.07 > hf 已否定矩形假設；εt = {ET:.5f} ≥ 0.005 → φ = 0.9",
             path=path)
    return path


FIGURES += [(fig1_flange, "§4 Step 1", "be 用梁中心距 400 或只檢核 8hf"),
            (fig2_section, "§4 Step 4–5", "a > hf 仍用矩形公式；翼板懸出與腹板分不清")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    assert H - COV == 64.0 and S - BW == 350.0
    print("assert OK")
    assert BE == 125.0 and abs(CF - 133875) < 1 and abs(CF / FY - 31.88) < 0.005
    assert abs(ASW - 27.04) < 0.01 and abs(AS - 58.92) < 0.01 and abs(A_ - 12.72) < 0.01
    assert abs(C_ - 14.97) < 0.01 and abs(ET - 0.00983) < 2e-5
    print("assert（解題圖解）OK")
