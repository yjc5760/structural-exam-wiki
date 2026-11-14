#!/usr/bin/env python3
"""
RC-2024-2 懸臂雙筋梁 — 題目附圖重繪腳本

用法：python3 gen_RC-2024-2.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2024-2-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
考卷註明未依比例；頂面到上排鋼筋只示意，不標尺寸（h 考卷未給）。
FIGURES
  fig-1-problem  題目附圖重繪（圖 2a 斷面＋圖 2b 懸臂）  攔：44 cm 當成 d
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-strain    底面受壓三聯圖      攔：44 當 d、壓力筋當降伏
  fig-2-cantilever 懸臂 SFD／BMD     攔：懸臂彎矩用 wL²/8
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2024-2"

# ── 判讀清單（RC-2024-2-problem.md §4，已確認）──
B = 30.0                  # #6
DD = 44.0                 # #1 上排中心到下排中心
DP = 8.0                  # #2 下排中心到底面
TOP = 8.0                 # #4 上排到頂面（示意，考卷無尺寸）
DB = 3.22                 # #10 D32 直徑（示意用）
L = 3.0                   # #8 懸臂長 (m)
D = DP + DD


def fig1_problem():
    PW, PH = 480, 620
    s = 6.2
    p1 = Canvas(PW, PH, sx=s, ox=PW / 2 - B * s / 2 - 40, oy=130)
    p1.panel("圖 2a 斷面（重繪，示意）", "依判讀清單 #1–#7；下方受壓")
    H = DP + DD + TOP
    p1.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.2)
    e = 4.5
    p1.poly([(e, e), (B - e, e), (B - e, H - e), (e, H - e), (e, e)], C["member"], 3.2)
    xin = [e + 0.6 + DB / 2, B / 2, B - e - 0.6 - DB / 2]
    for x in xin:
        p1.circle((x, DP + DD), DB / 2, fill="#FFFFFF", stroke=C["tension"], w=2.2)
    for x in (xin[0], xin[2]):
        p1.circle((x, DP), DB / 2, fill="#FFFFFF", stroke=C["compr"], w=2.2)
    p1.text_px(p1.X(B / 2), p1.Y(DP + DD) + 30, "3-#10（受拉）", 13, C["tension"], weight="700")
    p1.text_px(p1.X(B / 2), p1.Y(DP) - 26, "2-#10（受壓）", 13, C["compr"], weight="700")
    p1.text_px(p1.X(B) + 10, p1.Y(H) - 4, "#3@25", 13, C["member"], "start", weight="700")
    p1.dim((0, H), (B, H), "30 cm", off=-28, label_off=-14)
    p1.dim((B, DP + DD), (B, DP), "44 cm", off=-34, label_off=-34)
    p1.dim((B, DP), (B, 0), "8 cm", off=-34, label_off=-30)
    p1.text_px(p1.X(B) + 14, p1.Y((H + DP + DD) / 2), "（未標尺寸）", 11.5, C["muted"], "start")
    p1.text_px(p1.X(B / 2), p1.Y(0) + 34, "44 cm 兩端都在鋼筋中心", 12.5, C["accent"], weight="700")
    p1.text_px(p1.X(B / 2), p1.Y(0) + 58, "d = 8 + 44 = 52 cm（由底面量起）", 12.5, C["accent"], weight="700")
    # 圖 2b
    s2 = 105
    p2 = Canvas(PW, PH, sx=s2, ox=70, oy=300)
    p2.panel("圖 2b 懸臂梁（重繪）", "依判讀清單 #5、#8")
    p2.line((0, 0), (L, 0), C["member"], 6, cap="butt")
    p2.fixed_support((0, 0), 90, size=34)
    p2.udl((0, 0.06), (L, 0.06), 0.75, n=13, color=C["load"], w=1.6)
    p2.math((L / 2, 0.95), "ω_{u}", 17, C["load"], weight="700")
    p2.dim((0, 0), (L, 0), "3 m", off=70, label_off=16)
    p2.text_px(p2.X(L / 2), p2.Y(0) + 130, "固定端負彎矩：上緣受拉、下緣受壓", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([p1, p2], title=f"{TAG} 題目附圖（重繪）",
            sub="圖 2a：44 cm 為上排到下排鋼筋中心距、8 cm 為下排中心到底面；圖 2b：左端固定、長 3 m、全長均佈 ωu",
            note="頂面到上排鋼筋考卷沒有尺寸，全深 h 未給；彎矩計算只用 d = 52、d' = 8",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "44 cm 當成 d")]

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
# 常數取 RC-2024-2.md §4 公佈的 c、a；應變、內力、ωu 現算，檔尾對 §4 assert
# 懸臂負彎矩：受壓面在「下方」，斷面圖照實際方向畫（flip）
# ══════════════════════════════════════════════════════════
from recipes import beam_vm
K_B, K_D, K_DP, K_FC, K_FY, K_ES, K_ECU = 30.0, 52.0, 8.0, 210.0, 4200.0, 2.04e6, 0.003
K_AS, K_ASP, K_L = 3 * 8.14, 2 * 8.14, 3.0
K_C, K_A = 13.56, 11.53                        # §4 Step 2（c）、Step 5（a，取兩位）
K_EPSP = K_ECU * (K_C - K_DP) / K_C
K_FSP = K_ES * K_EPSP
K_ET = K_ECU * (K_D - K_C) / K_C
K_CC = 0.85 * K_FC * K_B * K_A
K_CS = K_ASP * round(K_FSP)
K_T = K_AS * K_FY
K_MN = K_CC * (K_D - K_A / 2) + K_CS * (K_D - K_DP)
K_PMN = 0.9 * K_MN
K_WU = 2 * K_PMN / (K_L * 100) ** 2 * 100 / 1000   # tf/m


def fig1_section():
    path = os.path.join(OUT, f"{TAG}-fig-1-strain.svg")
    section3(K_B, 0, K_B, K_D + 8, False, K_C, K_A, K_ECU, K_FY / K_ES,
             layers=[dict(z=K_DP, n=2, kind="C", eps=-K_EPSP),
                     dict(z=K_D, n=3, kind="T", eps=K_ET)],
             forces=[dict(z=K_A / 2, F=K_CC, kind="C", name="C_{c}"),
                     dict(z=K_DP, F=K_CS, kind="C", name="C'_{s}"),
                     dict(z=K_D, F=K_T, kind="T", name="T")],
             flip=True,
             sec_sub="b = 30；受壓面在下（懸臂負彎矩）",
             width_labels=("30", "30"),
             depth_dims=[(0, K_DP, "8", "L", 26), (K_DP, K_D, "44", "L", 26), (0, K_D, f"d={K_D:g}", "R", 34)],
             title=f"{TAG}　懸臂斷面（底面受壓）：斷面／應變／內力",
             sub=f"c = {K_C} cm 由底面量起；ε's = {K_EPSP:.5f} < εy → f's = {round(K_FSP):,} kgf/cm²；εt = {K_ET:.4f} → φ = 0.9",
             note=f"d = 8 + 44 = 52（44 是兩排鋼筋中心距）；Mn = {K_MN/1e5:.2f}、φMn = {K_PMN/1e5:.2f} tf·m",
             path=path)
    return path


def fig2_cantilever():
    path = os.path.join(OUT, f"{TAG}-fig-2-cantilever.svg")
    n = 60
    xs = [K_L * i / n for i in range(n + 1)]
    V = [K_WU * (K_L - x) for x in xs]
    M = [-K_WU * (K_L - x) ** 2 / 2 for x in xs]
    beam_vm(K_L, xs, V, M, supports=[(0, "fixed")], udls=[(0, K_L, "ω_{u}")],
            title=f"{TAG}　懸臂梁：固定端 Mu = ωu·L²/2 = φMn → ωu = {K_WU:.2f} tf/m",
            note=f"最大彎矩在固定端、負彎矩（上排受拉）；若誤用簡支梁 wL²/8 會高估 ωu 4 倍",
            key_V=[(0.15, f"{K_WU*K_L:.1f}", -14)],
            key_M=[(0.25, f"−{K_PMN/1e5:.2f}", 16)],
            v_unit="tf", m_unit="tf·m", path=path)
    return path


FIGURES += [(fig1_section, "§4 Step 2–5", "44 當 d；壓力筋直接當降伏；把下排當拉力筋"),
            (fig2_cantilever, "§4 Step 6", "懸臂彎矩用 wL²/8；最大彎矩位置錯")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    assert D == 52.0 and DP == 8.0
    print("assert OK")
    assert abs(round(K_FSP) - 2509) <= 1 and abs(K_ET - 0.0085) < 1e-4
    assert abs(K_CC - 61744) < 2 and abs(K_CS - 40847) < 2 and abs(K_T - 102564) < 1
    assert abs(K_MN - 4652002) < 300 and abs(K_PMN / 1e5 - 41.87) < 0.01 and abs(K_WU - 9.30) < 0.005
    print("assert（解題圖解）OK")
