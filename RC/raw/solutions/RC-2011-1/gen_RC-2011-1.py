#!/usr/bin/env python3
"""
RC-2011-1 解題圖解腳本（說明題：設計 P–M 交互曲線的求算步驟）

用法：python3 gen_RC-2011-1.py [輸出目錄]（預設 figs/）
本題考卷沒有給斷面。圖以同單元 RC-2015-1 的斷面為例（60×60 cm、上下各 4-#10、d' = 8 cm、
f'c = 350、fy = 4200 kgf/cm²），數值一律由應變相容現算；φ 依本庫約定（ε_ty → SD420 取 0.005），
平衡點對 RC-2015-1.md §4 的 P_b、M_b 對帳。
FIGURES
  fig-1-pm  標稱與設計 P–M 交互曲線  攔：只畫標稱曲線；忘了 φ 隨 ε_t 過渡；漏了 φP_n,max 截斷
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2011-1"
FIGURES = []


# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-14，RC-U1-2 批 1 階段 E）
# 數值一律由應變相容現算（ε_cu = 0.003、Whitney 0.85f'c、壓力筋在 a 內扣 0.85f'c），檔尾對 .md §4 對帳。
# 畫法：壓力緣在上；三聯圖垂直比例共用（c、a、d 相對位置為真），水平尺度為示意。
# ══════════════════════════════════════════════════════════
ES, ECU = 2.04e6, 0.003
TF, TFM = 1e-3, 1e-5


def _b1(fc):
    return min(0.85, max(0.65, 0.85 - 0.05 * (fc - 280) / 70))


def col_section(c, h, b, fc, fy, layers):
    """layers = [(d 自壓力緣, 根數, 單根面積)]；回傳 Pn、Mn（對 h/2）與各層內力。"""
    a = min(_b1(fc) * c, h)
    Cc = 0.85 * fc * a * b
    P, M, rows = Cc, Cc * (h / 2 - a / 2), []
    for d, n, Ab in layers:
        eps = ECU * (c - d) / c
        fs = max(-fy, min(fy, ES * eps))
        F = n * Ab * (fs - (0.85 * fc if (d < a and fs > 0) else 0.0))
        rows.append(dict(d=d, n=n, eps=eps, fs=fs, F=F))
        P += F
        M += F * (h / 2 - d)
    return dict(c=c, a=a, Cc=Cc, rows=rows, P=P, M=M, h=h, b=b, fy=fy)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0):
            lo, flo = m, f(m)
        else:
            hi = m
    return (lo + hi) / 2


def _dots(cv, h, b, layers, r=6.0):
    for d, n, _ in layers:
        for i in range(n):
            cv.dot((b * (i + 1) / (n + 1), h - d), r, fill=C["member"], stroke="#FFFFFF", w=1.6)


def tri_panel(s, layers, title, sub, note, cap3=(), PW=330, PH=500):
    """柱斷面三聯圖：斷面與壓力區／應變分佈／等值應力塊與合力。"""
    h, b = s["h"], s["b"]
    SX = (PH - 150) / h
    PX = lambda px: px / SX

    def frame(name, ox, W=PW):
        cv = Canvas(W, PH, sx=SX, ox=ox, oy=74, bg="#FFFFFF")
        cv.text_px(W / 2, 30, name, 13.5, C["text"], weight="700")
        return cv

    y_na, y_a = h - s["c"], h - s["a"]
    # (1) 斷面
    W1 = int(b * SX + 200)
    c1 = frame("斷面與壓力區", 104, W1)
    c1.polygon([(0, 0), (b, 0), (b, h), (0, h)], C["fill_m"], C["member"], 2.6)
    c1.polygon([(0, y_a), (b, y_a), (b, h), (0, h)], C["fill_c"], "none")
    _dots(c1, h, b, layers)
    c1.line((-1, y_na), (b + 1, y_na), C["compr"], 2.0, dash="6 4")
    c1.line((-1, y_a), (b + 1, y_a), C["compr"], 2.4)
    c1.line((-1, h / 2), (b + 1, h / 2), C["accent"], 1.4, dash="3 4")
    c1.text_px(c1.X(b) + 6, c1.Y(y_na) + 4, f"c = {s['c']:.2f}", 12, C["compr"], "start", weight="700")
    c1.text_px(c1.X(b) + 6, c1.Y(y_a) - 10, f"a = {s['a']:.2f}", 12, C["compr"], "start", weight="700")
    c1.text_px(c1.X(b) + 6, c1.Y(h / 2) + 4, "h/2", 11.5, C["accent"], "start", weight="700")
    for d, n, _ in layers:
        c1.text_px(c1.X(0) - 6, c1.Y(h - d) + 4, f"{n} 根 d={d:g}", 11, C["muted"], "end")
    c1.text_px(c1.X(b / 2), c1.Y(h) - 12, "壓力緣", 12, C["muted"])
    c1.text_px(W1 / 2, PH - 26, f"b × h = {b:g} × {h:g} cm（h 為彎曲方向）", 12, C["muted"])

    # (2) 應變
    c2 = frame("應變分佈（線性）", PW / 2 - 40)
    dmax = max(r["d"] for r in s["rows"])
    et = s["rows"][-1]["eps"] if s["rows"][-1]["d"] == dmax else ECU * (s["c"] - dmax) / s["c"]
    sc = PX(74.0) / max(ECU, abs(et))
    c2.line((0, 0), (0, h), C["muted"], 1.6)
    c2.polygon([(0, h), (ECU * sc, h), (0, y_na)], C["fill_c"], C["compr"], 2.4)
    if et < 0:
        c2.polygon([(0, y_na), (et * sc, h - dmax), (0, h - dmax)], C["fill_t"], C["tension"], 2.4)
    c2.text_px(c2.X(ECU * sc) + 6, c2.Y(h) + 4, "ε_{cu} = 0.003", 12, C["compr"], "start", weight="700")
    ey = s["fy"] / ES
    for r in s["rows"]:
        yy = h - r["d"]
        c2.dot((0, yy), 4.6, fill=C["member"], stroke="#FFFFFF", w=1.4)
        yl = "降伏" if abs(r["eps"]) >= ey else "未降伏"
        col = C["compr"] if r["eps"] > 0 else C["tension"]
        c2.text_px(c2.X(PX(80)), c2.Y(yy) + 4, f"{r['eps']:+.5f}（{yl}）", 11, col, "start", weight="700")
    c2.text_px(PW / 2, PH - 26, f"ε_y = f_y/E_s = {ey:.6f}", 12, C["muted"])

    # (3) 合力
    c3 = frame("等值應力塊與合力", PW / 2 - 20)
    c3.line((0, 0), (0, h), C["muted"], 1.4)
    c3.line((-PX(110), h / 2), (PX(110), h / 2), C["accent"], 1.4, dash="3 4")
    fmax = max([abs(s["Cc"])] + [abs(r["F"]) for r in s["rows"]])
    k = PX(100.0) / fmax
    c3.arrow((0, h - s["a"] / 2), (s["Cc"] * k, h - s["a"] / 2), C["compr"], 3.4, 10)
    c3.text_px(c3.X(s["Cc"] * k) + 6, c3.Y(h - s["a"] / 2) + 4, f"C_c = {s['Cc']*TF:.1f} tf", 12,
               C["compr"], "start", weight="700")
    for r in s["rows"]:
        yy = h - r["d"]
        col = C["compr"] if r["F"] > 0 else C["tension"]
        c3.arrow((0, yy), (r["F"] * k, yy), col, 3.0, 9)
        anc, dx = ("start", 6) if r["F"] > 0 else ("end", -6)
        dy = 18 if r["F"] > 0 else -10
        lab = ("C_s" if r["F"] > 0 else "T") + f" = {abs(r['F'])*TF:.2f} tf"
        c3.text_px(c3.X(r["F"] * k) + dx, c3.Y(yy) + dy, lab, 11.5, col, anc, weight="700")
    y = PH - 64
    for txt, col in cap3:
        c3.text_px(PW / 2, y, txt, 12.2, col, weight="700")
        y += 20
    return compose([c1, c2, c3], title=title, sub=sub, note=note)


# ── 例題斷面：RC-2015-1（§1 本解記號）──
EX_H, EX_B, EX_FC, EX_FY = 60.0, 60.0, 350.0, 4200.0
EX_LAY = [(8.0, 4, 8.143), (52.0, 4, 8.143)]
EX_D = EX_LAY[-1][0]
AST = sum(n * a for _, n, a in EX_LAY)
P0 = 0.85 * EX_FC * (EX_H * EX_B - AST) + EX_FY * AST      # 純壓
PT = -EX_FY * AST                                           # 純拉
EY = EX_FY / ES
CAP = 0.80 * 0.65 * P0                                      # φPn,max（箍筋柱）


LIM = 0.005 if EX_FY <= 4200 else EY + 0.003     # 本庫約定：SD420 拉力控制界限取 0.005


def phi_of(et):
    if et <= EY:
        return 0.65
    if et >= LIM:
        return 0.90
    return 0.65 + 0.25 * (et - EY) / (LIM - EY)


def _sec(c):
    return col_section(c, EX_H, EX_B, EX_FC, EX_FY, EX_LAY)


def point(c):
    s = _sec(c)
    et = ECU * (EX_D - c) / c
    return s["M"], s["P"], et, phi_of(et)


CB = ECU / (ECU + EY) * EX_D                 # 平衡點 ε_t = ε_ty
CT = ECU / (ECU + LIM) * EX_D                # 拉力控制界限 ε_t = 0.005
C0 = bisect(lambda c: _sec(c)["P"], 1.0, 30.0)   # 純彎
KEY = {k: point(c) for k, c in (("B", CB), ("T", CT), ("Z", C0))}


def curves():
    cs = [0.4 * 1.03 ** i for i in range(260)]
    nom = [(0.0, P0)]
    des = [(0.0, CAP)]
    for c in reversed(cs):
        if c > 400:
            continue
        m, p, et, ph = point(c)
        nom.append((m, p))
        des.append((ph * m, min(ph * p, CAP)))
    nom.append((0.0, PT))
    des.append((0.0, 0.90 * PT))
    return nom, des


def fig1_pm():
    nom, des = curves()
    W, H = 760, 620
    L, R, T, B = 110, 250, 40, 84
    mmax = max(m for m, _ in nom) * 1.12
    pmin, pmax = PT * 1.08, P0 * 1.08
    sx = (W - L - R) / mmax
    sy = (H - T - B) / (pmax - pmin)
    k = sy / sx
    cv = Canvas(W, H, sx=sx, ox=L, oy=B + (-pmin) * sy, bg="#FFFFFF")
    tf = lambda v: v * TF
    # 軸
    cv.arrow((0, pmin * k), (0, pmax * k), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (mmax, 0), C["muted"], 1.8, 9)
    cv.text_px(cv.X(0) - 10, cv.Y(pmax * k) + 4, "P (tf)", 13, C["muted"], "end")
    cv.text_px(cv.X(mmax) + 6, cv.Y(0) + 18, "M (tf·m)", 13, C["muted"], "start")
    for p in range(-200, int(tf(P0)) + 1, 200):
        cv.line((0, p * 1e3 * k), (mmax * 0.012, p * 1e3 * k), C["muted"], 1.2)
        cv.text_px(cv.X(0) - 8, cv.Y(p * 1e3 * k) + 4, f"{p}", 11.5, C["muted"], "end")
    for m in range(0, int(mmax * TFM) + 1, 25):
        cv.line((m * 1e5, 0), (m * 1e5, -mmax * 0.012), C["muted"], 1.2)
        cv.text_px(cv.X(m * 1e5), cv.Y(0) + 18, f"{m}", 11.5, C["muted"])
    # 設計曲線（填色）與標稱曲線（灰虛線）
    cv.polygon([(m, p * k) for m, p in des], C["fill_c"], C["compr"], 2.8)
    cv.poly([(m, p * k) for m, p in nom], C["ghost"], 2.2, dash="7 5")
    # 截斷線
    cv.line((0, CAP * k), (mmax * 0.95, CAP * k), C["load"], 1.4, dash="4 4")
    cv.text_px(cv.X(mmax * 0.95) + 6, cv.Y(CAP * k) + 4, f"φP_n,max = 0.80φP_o = {tf(CAP):.0f}", 12, C["load"], "start", weight="700")
    # 關鍵點
    marks = [("B", "平衡點 ε_t = ε_{ty}", C["accent"]), ("T", "拉力控制界限 ε_t = 0.005", C["bmd"])]
    for key, lab, col in marks:
        m, p, et, ph = KEY[key]
        cv.dot((m, p * k), 5.4, fill=C["ghost"], stroke="#FFFFFF", w=1.6)
        cv.dot((ph * m, ph * p * k), 6.0, fill=col, stroke="#FFFFFF", w=1.8)
        cv.line((m, p * k), (ph * m, ph * p * k), col, 1.2, dash="3 3")
        cv.text_px(cv.X(m) + 10, cv.Y(p * k) + 4, f"{lab}（φ = {ph:.2f}）", 12, col, "start", weight="700")
    mz, pz, _, phz = KEY["Z"]
    cv.dot((mz, 0), 5.4, fill=C["ghost"], stroke="#FFFFFF", w=1.6)
    cv.dot((phz * mz, 0), 6.0, fill=C["member"], stroke="#FFFFFF", w=1.8)
    cv.text_px(cv.X(phz * mz) - 10, cv.Y(0) - 12, f"純彎 P_n = 0（φ = {phz:.2f}）", 12, C["member"], "end", weight="700")
    cv.dot((0, P0 * k), 5.4, fill=C["ghost"], stroke="#FFFFFF", w=1.6)
    cv.text_px(cv.X(0) + 10, cv.Y(P0 * k) + 4, f"純壓 P_o = {tf(P0):.0f}", 12, C["muted"], "start", weight="700")
    cv.text_px(cv.X(0) + 10, cv.Y(PT * k) + 16, f"純拉 −f_y A_st = {tf(PT):.0f}", 12, C["muted"], "start", weight="700")
    # 區段註記（放在曲線內側）
    mb, pb, _, _ = KEY["B"]
    mt, pt_, _, _ = KEY["T"]
    cv.text_px(cv.X(0.30 * mb * 0.65), cv.Y(0.72 * CAP * k), "壓力控制 φ = 0.65", 12.5, C["compr"], "start", weight="700")
    cv.text_px(cv.X(0.30 * mt * 0.9), cv.Y(0.40 * pt_ * 0.9 * k), "過渡區（內插）", 12.5, C["compr"], "start", weight="700")
    cv.text_px(cv.X(0.15 * mt * 0.9), cv.Y(0.62 * PT * 0.9 * k), "拉力控制 φ = 0.90", 12.5, C["compr"], "start", weight="700")
    # 圖例
    lx, ly = W - R + 24, 120
    cv.text_px(lx, ly - 18, "灰虛線：標稱 (M_n, P_n)", 12, C["muted"], "start", weight="700")
    cv.text_px(lx, ly + 4, "藍色區：設計 (φM_n, φP_n)", 12, C["compr"], "start", weight="700")
    cv.text_px(lx, ly + 26, "紅虛線：軸力上限截斷", 12, C["load"], "start", weight="700")
    return compose([cv], title="圖 1　標稱與設計 P–M 交互曲線（以 RC-2015-1 斷面為例）",
                   sub="60×60 cm、上下各 4-#10、f'c = 350、fy = 4200；c 由大到小掃描，每個 c 得一組 (Mn, Pn)，再乘 φ、截斷",
                   note="題目要的是設計曲線：每點乘 φ（隨 εt 由 0.65 過渡到 0.90），頂部再以 0.80φPo 截平；只畫灰虛線會失分")


FIGURES.append(("1-pm", fig1_pm, "只畫標稱曲線；φ 不隨 ε_t 過渡；漏了 φP_n,max 截斷"))


def _checks():
    mb, pb, et, ph = KEY["B"]
    for name, got, want, tol in [
        ("c_b", CB, 30.84, 0.01), ("P_b tf（RC-2015-1）", pb * TF, 430.67, 0.05),
        ("M_b tfm（RC-2015-1）", mb * TFM, 135.85, 0.02), ("φ_b", ph, 0.65, 1e-9),
        ("P_o tf", P0 * TF, 1325.2, 0.1), ("純彎 P_n", KEY["Z"][1], 0.0, 1e-3)]:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<20} 算得 {got:>12.6g}   對照 {want}")
        assert ok, f"{name} 與 RC-2015-1 解題檔不符"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("── 與 RC-2015-1.md §4 對帳（例題斷面）──")
    _checks()
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<28} 攔：{catches}")
