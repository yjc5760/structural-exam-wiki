#!/usr/bin/env python3
"""
RC-2021-1 T 形簡支梁斷面 — 題目附圖重繪腳本

用法：python3 gen_RC-2021-1.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2021-1-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
FIGURES
  fig-1-problem  題目附圖重繪  攔：60 cm 當全深；鋼筋 10 cm 當淨保護層
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-tsection  T 形斷面三聯圖      攔：a ≤ hf 時用 bw 算強度
  fig-2-shear     半跨剪力圖          攔：用支承面剪力設計肋筋
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2021-1"

# ── 判讀清單（RC-2021-1-problem.md §4，已確認）──
BF, TF = 100.0, 10.0      # #1 翼板寬 100、厚 10
HW = 60.0                 # #2 翼板底到梁底
BW = 40.0                 # #3 腹寬
YS = 10.0                 # #4 鋼筋重心距梁底
H = TF + HW


def fig1_problem():
    W, Hc = 640, 560
    s = 3.4
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - BF * s / 2 - 20, oy=110)
    cv.panel("T 形斷面（重繪）", "依題目正本判讀清單 #1–#4")
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    pts = [(x0, 0), (x1, 0), (x1, HW), (BF, HW), (BF, H), (0, H), (0, HW), (x0, HW)]
    cv.polygon(pts, "#EDF1F6", C["member"], 2.6)
    cv.dot((BF / 2, YS), 9, fill=C["member"], stroke="#FFFFFF", w=1.2)
    cv.dim((0, H), (BF, H), "100 cm", off=-30, label_off=-14)
    cv.dim((BF, H), (BF, HW), "10 cm", off=-26, label_off=-34)
    cv.dim((BF, HW), (BF, 0), "60 cm", off=-26, label_off=-34)
    cv.dim((x0, 0), (x0, YS), "10 cm", off=-40, label_off=-36)
    cv.dim((x0, 0), (x1, 0), "40 cm", off=30, label_off=15)
    cv.text_px(cv.X(BF / 2), cv.Y(0) + 82, "60 cm 由翼板底量到梁底；10 cm 由鋼筋重心量到梁底", 12.5, C["accent"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（圖一，重繪）",
            sub="翼板 100 × 10、腹寬 40；60 cm 為翼板底到梁底；鋼筋重心距梁底 10 cm",
            note="h = 10 + 60 = 70 cm，d = 70 − 10 = 60 cm",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "60 cm 當全深；10 cm 當淨保護層")]

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
# 由題目給定量現算（RC-2021-1.md §4 Part 1–2 的作法），檔尾對 §4 公佈值 assert
# ══════════════════════════════════════════════════════════
S_BF, S_HF, S_BW, S_H, S_D = 100.0, 10.0, 40.0, 70.0, 60.0
S_FC, S_FY, S_FYT, S_ES, S_ECU = 240.0, 4200.0, 2800.0, 2.04e6, 0.003
S_L, S_DL, S_LL = 8.0, 1.8, 4.5
WU = max(1.2 * S_DL + 1.6 * S_LL, 1.4 * S_DL)
MU = WU * S_L ** 2 / 8 * 1e5                      # kgf·cm
K1 = 0.85 * S_FC * S_BF
S_A_CALC = S_D - (S_D ** 2 - 2 * MU / 0.9 / K1) ** 0.5  # 假設 a ≤ hf 的小根（7.233）
S_A = 7.24                                        # §4 Part 1 公佈值（取兩位後再算 As = 35.17）
S_C = S_A / 0.85
S_AS = K1 * S_A / S_FY
S_ET = S_ECU * (S_D - S_C) / S_C
VU0 = WU * S_L / 2                                # 支承面
VUD = WU * (S_L / 2 - S_D / 100)                  # 臨界斷面（距支承面 d）
VC = 0.53 * S_FC ** 0.5 * S_BW * S_D / 1000       # tf
AV = 2 * 0.7133
VS = VUD / 0.75 - VC
S_REQ = AV * S_FYT * S_D / (VS * 1000)
VS10 = AV * S_FYT * S_D / 10 / 1000
CAP10 = 0.75 * (VC + VS10)
S_SUP = AV * S_FYT * S_D / ((VU0 / 0.75 - VC) * 1000)   # 若誤用支承面剪力


def fig1_section():
    path = os.path.join(OUT, f"{TAG}-fig-1-tsection.svg")
    section3(S_BF, S_HF, S_BW, S_H, True, S_C, S_A, S_ECU, S_FY / S_ES,
             layers=[dict(z=S_D, n=1, kind="T", eps=S_ET)],
             forces=[dict(z=S_A / 2, F=K1 * S_A, kind="C", name="C_{c}"),
                     dict(z=S_D, F=S_AS * S_FY, kind="T", name="T")],
             sec_sub="bf = 100、hf = 10、bw = 40、h = 70",
             width_labels=("100", "40"),
             depth_dims=[(0, S_HF, "10", "R", 26), (0, S_D, f"d={S_D:g}", "L", 44, -S_BW / 2)],
             title=f"{TAG}　跨中 T 形斷面：a = {S_A:.2f} cm < hf = 10，按寬 100 的矩形梁計算",
             sub=f"wu = {WU:.2f} tf/m，Mu = {MU/1e5:.2f} tf·m；(As)req = {S_AS:.2f} cm²",
             note=f"受壓區全在翼板內，寬度用 bf = 100 而不是 bw = 40；As,min 才用 bw；εt = {S_ET:.4f} → φ = 0.9",
             path=path)
    return path


def fig2_shear():
    path = os.path.join(OUT, f"{TAG}-fig-2-shear.svg")
    W, Hc = 900, 470
    sx, sy = 175.0, 8.2                           # px / m、px / tf
    cv = Canvas(W, Hc, ox=110, oy=80)
    cv.panel("半跨剪力圖（支承面 → 跨中）", "Vu 線性遞減；臨界斷面取距支承面 d")
    P = lambda x, v: (x * sx, v * sy)
    cv.polygon([P(0, 0), P(0, VU0), P(S_L / 2, 0)], C["fill_s"], C["sfd"], 2.4)
    cv.line(P(0, 0), P(S_L / 2 + 0.25, 0), C["member"], 2)
    for v, lab, col, dash in [(0.75 * VC, f"φVc = {0.75*VC:.2f}", C["muted"], "6 4"),
                              (CAP10, f"φ(Vc + Vs) = {0.75*(round(VC,2)+round(VS10,2)):.2f}（s = 10 cm）", C["bmd"], None)]:
        cv.line(P(0, v), P(S_L / 2 + 0.25, v), col, 2, dash=dash)
        cv.text_px(cv.X(2.3 * sx), cv.Y(v * sy) - 13, lab, 12.5, col, "start", weight="700")
    xd = S_D / 100
    cv.line(P(xd, 0), P(xd, VUD), C["accent"], 2, dash="4 3")
    cv.dot(P(xd, VUD), 5.5, fill=C["accent"])
    cv.text_px(cv.X(xd * sx) + 10, cv.Y(VUD * sy) - 16, f"臨界斷面 Vu = {VUD:.2f} tf", 13, C["accent"], "start", weight="700")
    cv.dot(P(0, VU0), 5, fill=C["sfd"])
    cv.text_px(cv.X(0) + 12, cv.Y(VU0 * sy) - 4, f"支承面 {VU0:.2f}（不用於設計）", 12.5, C["sfd"], "start")
    cv.dim(P(0, 0), P(xd, 0), "d = 0.6 m", off=-30, label_off=-13)
    cv.text_px(cv.X(S_L / 2 * sx), cv.Y(0) + 22, "跨中 x = 4 m", 12, C["muted"])
    cv.text_px(cv.X(0) - 8, cv.Y(0) + 22, "支承面", 12, C["muted"])
    compose([cv], title=f"{TAG}　近支承處剪力：Vs = Vu/φ − Vc → smax",
            sub=f"Vs = {VUD:.2f}/0.75 − {VC:.2f} = {round(VUD/0.75,2)-round(VC,2):.2f} tf；s = Av·fyt·d / Vs = {S_REQ:.2f} cm → 取 10 cm",
            note=f"臨界斷面在支承面外 d 處；若用支承面剪力 {VU0:.2f} 會得 s ≈ {S_SUP:.1f} cm，過度保守",
            path=path)
    return path


FIGURES += [(fig1_section, "§4 Part 1", "a ≤ hf 時仍用 bw 算強度；As,min 用 bf"),
            (fig2_shear, "§4 Part 2", "用支承面剪力設計；φVc 與 φ(Vc+Vs) 搞混")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    assert H == 70.0 and H - YS == 60.0
    print("assert OK")
    assert abs(WU - 9.36) < 1e-9 and abs(MU / 1e5 - 74.88) < 1e-6
    assert abs(S_A_CALC - 7.24) < 0.01 and abs(S_AS - 35.17) < 0.05
    assert abs(VUD - 31.82) < 0.01 and abs(VC - 19.71) < 0.01 and abs(VS - 22.72) < 0.01
    assert abs(S_REQ - 10.55) < 0.01 and abs(CAP10 - 32.76) < 0.01
    print("assert（解題圖解）OK")
