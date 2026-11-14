#!/usr/bin/env python3
"""
RC-2024-3 題目附圖重繪＋解題圖解腳本

用法：python3 gen_RC-2024-3.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2024-3-problem.md §4 判讀清單（已確認）。
fig-1 只畫考卷給的東西；fig-2 為解題圖解，數值由應變相容現算並對 .md §4 對帳。
FIGURES
  fig-1-problem  題目附圖重繪  攔：把 8 cm 當淨保護層、拉力鋼筋層判錯
  fig-2-section  斷面／應變／合力三聯圖（c＝32 cm）  攔：拉力鋼筋層判錯；中層當降伏
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2024-3"

# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-14，RC-U1-2 題目正本推廣・批 1）
# 依據：題目正本 <id>-problem.md §4 判讀清單（已確認）。只畫考卷給的東西，不含解題結果；
# 考卷未標尺寸的位置（如鋼筋在非彎曲方向的間距）畫成示意，並在副標寫明。
# ══════════════════════════════════════════════════════════
def _pc(Wm, Hm, maxpx=330, l=90, r=110, t=120, b=110):
    s = maxpx / max(Wm, Hm)
    return Canvas(int(Wm * s + l + r), int(Hm * s + t + b), sx=s, ox=l, oy=b)


def _prect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _pbar(cv, p, r=1.25, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)

P_B = 40.0                            # 判讀 #1
P_X = (8.0, 20.0, 32.0)               # 判讀 #2（8／12／12／8，量至鋼筋中心）


def fig1_problem():
    W = H = P_B
    cv = _pc(W, H, b=120)
    _prect(cv, 0, 0, W, H, fill="#FFFFFF")
    for x in P_X:
        for y in P_X:
            if (x, y) != (20.0, 20.0):
                _pbar(cv, (x, y), 1.27, fill="#FFFFFF")
    cv.text((W / 2, H / 2), "8-#8", 15, weight="700")
    ts = (0.0,) + P_X + (W,)
    for a, b_ in zip(ts[:-1], ts[1:]):
        cv.dim((0, b_), (0, a), f"{b_ - a:.0f}", off=30, label_off=18)
        cv.dim((a, 0), (b_, 0), f"{b_ - a:.0f}", off=28, label_off=14)
    return compose([cv], title=f"{TAG} 題目附圖（圖 3 重繪）",
                   sub="依題目正本判讀清單 #1–#3；單位 cm，尺寸量至鋼筋中心（考卷註明未依比例）",
                   note="沿彎曲深度三層：3 根 @ 8、2 根 @ 20、3 根 @ 32 cm（單向彎矩，方向不影響）")


FIGURES = [
    ("1-problem", fig1_problem, "把 8 cm 當淨保護層、拉力鋼筋層判錯"),
]


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
    if min(abs(h / 2 - s["a"]), abs(h / 2 - s["c"])) < 0.08 * h:   # 與 a、c 標籤太近時改放左側
        c1.text_px(c1.X(0) - 6, c1.Y(h / 2) + 4, "h/2", 11.5, C["accent"], "end", weight="700")
    else:
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
        if abs(r["F"]) < 1.0:                                        # 應力為零的層不畫箭頭
            c3.text_px(c3.X(0) + 8, c3.Y(yy) + 4, "此層 F = 0", 11.5, C["muted"], "start", weight="700")
            continue
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


S_H, S_B, S_FC, S_FY = 40.0, 40.0, 280.0, 4200.0   # §1 本解記號
S_LAY = [(8.0, 3, 5.07), (20.0, 2, 5.07), (32.0, 3, 5.07)]
S_C = S_LAY[-1][0]                                 # 拉力鋼筋應變為零 → c = d

WORK = col_section(S_C, S_H, S_B, S_FC, S_FY, S_LAY)


def fig2_section():
    s = WORK
    return tri_panel(
        s, S_LAY,
        title="圖 2　拉力鋼筋應變為零（c = d = 32 cm）時的斷面／應變／合力",
        sub=f"a = {s['a']:.2f} cm；最外層降伏、中層 ε = {s['rows'][1]['eps']:+.6f} 未降伏、拉力層應力為零",
        note="「拉力鋼筋」是離壓力緣最遠的一層（d = 32）；中層只有 0.0011、未降伏，要用 Es·ε 算應力",
        cap3=[(f"P_n = {s['P']*TF:.1f} tf", C["text"]),
              (f"M_n = {s['M']*TFM:.2f} tf·m", C["load"])])


FIGURES.append(("2-section", fig2_section, "拉力鋼筋層判錯（c 不等於 32）；中層誤當降伏"))


def _checks():
    s = WORK
    for name, got, want, tol in [
        ("a", s["a"], 27.2, 0.001), ("ε_s1", s["rows"][0]["eps"], 0.00225, 1e-6),
        ("ε_s2", s["rows"][1]["eps"], 0.001125, 1e-6), ("ε_s3", s["rows"][2]["eps"], 0.0, 1e-12),
        ("P_n tf", s["P"] * TF, 340.06, 0.01), ("M_n tfm", s["M"] * TFM, 23.80, 0.01)]:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<8} 算得 {got:>12.6g}   .md {want}")
        assert ok, f"{name} 與解題檔不符"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("── 與 RC-2024-3.md §4 對帳 ──")
    _checks()
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")
