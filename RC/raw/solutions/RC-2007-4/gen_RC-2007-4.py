#!/usr/bin/env python3
"""RC-2007-4 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2007-4-problem.md §4，已確認）
用法：python3 gen_RC-2007-4.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2007-4"
# ── 判讀清單（RC-2007-4-problem.md §4，已確認）──
# #2 斷面形狀（由下往上）：下翼 55×17.5、下斜坡 18.7（55→17.5）、腹板 17.5×47.5、上斜坡 11.3（17.5→40）、上翼 40×17.5
SEG = [17.5, 18.7, 47.5, 11.3, 17.5]
BT, BB, BW = 40.0, 55.0, 17.5
Y = [0.0]
for h in SEG:
    Y.append(Y[-1] + h)
HT = Y[-1]                                  # 112.5
PROPS = ["S^t = 83,082 cm³", "S_b = 101,370 cm³", "I_o = 5.2×10^{6} cm⁴", "A = 3,613 cm²",
         "r² = 1,445 cm²", "c_t = 62.8 cm", "c_b = 51.5 cm"]


def fig1_problem():
    W, Hc = 900, 760
    s = 4.6
    cv = Canvas(W, Hc, sx=s, ox=250, oy=110)
    cv.panel("I 形預力梁斷面（重繪）", "依題目正本判讀清單 #1–#2；圖右為考卷所給斷面性質（照錄）")
    pts = [(-BB / 2, Y[0]), (BB / 2, Y[0]), (BB / 2, Y[1]), (BW / 2, Y[2]), (BW / 2, Y[3]),
           (BT / 2, Y[4]), (BT / 2, Y[5]), (-BT / 2, Y[5]), (-BT / 2, Y[4]), (-BW / 2, Y[3]),
           (-BW / 2, Y[2]), (-BB / 2, Y[1])]
    cv.polygon(pts, "#EDF1F6", C["member"], 2.6)
    cv.dim((-BT / 2, HT), (BT / 2, HT), "40 cm", off=-22, label_off=-14)
    cv.dim((-BB / 2, 0), (BB / 2, 0), "55 cm", off=24, label_off=14)
    cv.dim((-BW / 2, Y[2] + 24), (BW / 2, Y[2] + 24), "17.5", off=0, label_off=-12)
    xr = BB / 2 + 6
    for i, h in enumerate(SEG):
        cv.dim((xr, Y[i + 1]), (xr, Y[i]), f"{h:g}", off=-6, label_off=-22)
    cv.dim((xr + 14, HT), (xr + 14, 0), "112.5 cm", off=-6, label_off=-34)
    for y in Y[1:-1]:
        cv.line((BW / 2 + 1, y), (xr - 1, y), C["dim"], 1, dash="3 3")
    x0 = 610
    for i, t in enumerate(PROPS):
        cv.text_px(x0, 200 + i * 40, t, 15, C["text"], "start")
    cv.rect_px(x0 - 18, 170, 250, 300, "none", 10, C["border"], 1.2)
    cv.text_px(x0 + 107, 520, "c_t＋c_b＝114.3 ≠ 112.5", 13.5, C["load"], weight="700")
    cv.text_px(x0 + 107, 546, "（考卷數據自相矛盾）", 12.5, C["muted"])
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="對稱 I 形梁；梁距 2.2 m、橋面版厚 20 cm 置於上翼頂（版不在原圖中，未畫）",
                   note="五段尺寸和為 112.5 cm，與考卷所給 ct＋cb＝114.3 不符；本庫依使用者確認照考卷數據，版置於 114.3 頂面",
                   path=os.path.join(OUT, f"{TAG}-fig-1-problem.svg"))


# ══════════════════════════════════════════════════════════
# 解題圖解（階段 E，2026-11-14）：共用的小型座標圖工具
# ══════════════════════════════════════════════════════════
class Plot:
    """像素框內的 x–y 座標圖（框左上角 x0,y0、寬 w、高 h；y 軸向上為正）"""
    def __init__(self, cv, x0, y0, w, h, xr, yr):
        self.cv, self.x0, self.y0, self.w, self.h, self.xr, self.yr = cv, x0, y0, w, h, xr, yr
    def X(self, v): return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w
    def Y(self, v): return self.y0 + (self.yr[1] - v) / (self.yr[1] - self.yr[0]) * self.h
    def _raw(self, s): self.cv.parts.append(s)
    def band(self, ylo, yhi, color, op=0.13):
        y1, y2 = self.Y(max(ylo, yhi)), self.Y(min(ylo, yhi))
        self._raw(f'<rect x="{self.x0:.1f}" y="{y1:.1f}" width="{self.w:.1f}" height="{y2-y1:.1f}" '
                  f'fill="{color}" fill-opacity="{op}"/>')
    def vband(self, xlo, xhi, color, op=0.13):
        x1, x2 = self.X(xlo), self.X(xhi)
        self._raw(f'<rect x="{x1:.1f}" y="{self.y0:.1f}" width="{x2-x1:.1f}" height="{self.h:.1f}" '
                  f'fill="{color}" fill-opacity="{op}"/>')
    def seg(self, p0, p1, color, w=2.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._raw(f'<line x1="{self.X(p0[0]):.1f}" y1="{self.Y(p0[1]):.1f}" x2="{self.X(p1[0]):.1f}" '
                  f'y2="{self.Y(p1[1]):.1f}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="round"/>')
    def hline(self, y, color, w=1.8, dash="7 5"):
        self.seg((self.xr[0], y), (self.xr[1], y), color, w, dash)
    def vline(self, x, color, w=1.6, dash="5 4", y0=None, y1=None):
        self.seg((x, self.yr[0] if y0 is None else y0), (x, self.yr[1] if y1 is None else y1), color, w, dash)
    def curve(self, pts, color, w=3.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        pp = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self._raw(f'<polyline points="{pp}" fill="none" stroke="{color}" stroke-width="{w}"{d} '
                  f'stroke-linejoin="round" stroke-linecap="round"/>')
    def dot(self, x, y, color, r=5.5):
        self._raw(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="#FFFFFF" '
                  f'stroke="{color}" stroke-width="2.6"/>')
    def frame(self, xticks, yticks, xlab, ylab, xfmt="{:g}", yfmt="{:g}"):
        cv = self.cv
        for t in yticks:
            self.seg((self.xr[0], t), (self.xr[1], t), C["border"], 1.0)
            cv.text_px(self.x0 - 10, self.Y(t), yfmt.format(t), 12, C["muted"], "end")
        for t in xticks:
            cv.text_px(self.X(t), self.y0 + self.h + 18, xfmt.format(t), 12, C["muted"])
        self._raw(f'<rect x="{self.x0}" y="{self.y0}" width="{self.w}" height="{self.h}" fill="none" '
                  f'stroke="{C["member2"]}" stroke-width="1.4"/>')
        cv.text_px(self.x0 + self.w / 2, self.y0 + self.h + 44, xlab, 13, C["text"])
        cv.text_px(self.x0, self.y0 - 16, ylab, 13, C["text"], "start")


def save_png(svg_path):
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=svg_path[:-4] + ".png", scale=2.0)
    except ImportError:
        print("（未安裝 cairosvg，略過 PNG）")

# ── 解題圖 fig-2：由 RC-2007-4.md §4 Step 4–5 解得 ──
S_BC   = 171_234.0        # 合成斷面梁底斷面模數 (cm^3)，§4 Step 3
ARM    = 500.0            # 跨中集中載重的彎矩臂 L/4 (cm)，§4 Step 5
F_PRE  = 17.90            # 活載前梁底累積應力（壓為正），§4 Step 4 彙整表
FC     = 350.0            # 梁 f'c
K_P    = ARM / S_BC * 1000.0          # 每 1 tf 的梁底拉應力 (kgf/cm^2/tf)
LIM_EX = round(3.0 * math.sqrt(FC), 1)   # 考卷容許拉應力 3√f'c（§4 取 56.1 代入）
LIM_U  = round(2.0 * math.sqrt(FC), 1)   # 現行規範 U 類上限（§5 取 37.4）
LIM_T  = round(3.2 * math.sqrt(FC), 1)   # 現行規範 T 類上限（§5 取 59.9）
P0, PU, PEX, PT = (F_PRE + 0) / K_P, (F_PRE + LIM_U) / K_P, (F_PRE + LIM_EX) / K_P, (F_PRE + LIM_T) / K_P


def fig2_class():
    W, H = 1000, 625
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　梁底應力隨集中活載重 P 變化：考卷容許值落在現行規範哪一類", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "壓為正、拉為負；分類依建築物混凝土結構設計規範（2023），kgf/cm² 制", 13, C["muted"])
    pl = Plot(cv, 120, 110, 610, 380, (0.0, 30.0), (-75.0, 25.0))
    pl.band(0, -LIM_U, C["bmd"], 0.13)
    pl.band(-LIM_U, -LIM_T, C["accent"], 0.14)
    pl.band(-LIM_T, -75, C["load"], 0.12)
    pl.frame(range(0, 31, 5), range(-75, 26, 25), "跨中集中活載重 P（tf）", "梁底應力（kgf/cm²）")
    pl.hline(0, C["member2"], 1.4, None)
    pl.hline(-LIM_EX, C["load"], 2.2, "8 5")
    pl.curve([(0, F_PRE), (30, F_PRE - K_P * 30)], C["deform"], 3.4)
    for p, f, col in [(P0, 0, C["bmd"]), (PU, -LIM_U, C["bmd"]), (PEX, -LIM_EX, C["load"]), (PT, -LIM_T, C["accent"])]:
        pl.vline(p, col, 1.5, "4 4", -75, f)
        pl.dot(p, f, col)
    # 區帶名稱（右側說明欄）
    xr = 750
    rows = [(0, -LIM_U, C["bmd"], "U 類（未開裂）", f"拉應力 ≤ 2.0√f'c = {LIM_U:.1f}"),
            (-LIM_U, -LIM_T, C["accent"], "T 類（過渡）", f"≤ 3.2√f'c = {LIM_T:.1f}，撓度用開裂斷面"),
            (-LIM_T, -75, C["load"], "C 類（開裂）", "開裂斷面分析＋裂縫控制")]
    for lo, hi, col, name, desc in rows:
        ym = pl.Y((lo + hi) / 2)
        cv.text_px(xr, ym - 10, name, 14, col, "start", weight="700")
        cv.text_px(xr, ym + 12, desc, 11.5, C["muted"], "start")
    cv.text_px(pl.X(1.0), pl.Y(-LIM_EX) + 16, f"考卷容許拉應力 3√f'c = {LIM_EX:.1f}", 12.5, C["load"], "start", weight="700")
    # 交點數值（x 軸下方第二列）
    for p, txt, col, dy in [(P0, f"{P0:.2f}", C["bmd"], 0), (PU, f"{PU:.1f}", C["bmd"], 0),
                            (PEX, f"{PEX:.1f}", C["load"], 0), (PT, f"{PT:.1f}", C["accent"], 16)]:
        cv.text_px(pl.X(p), pl.Y(-75) - 12 - dy, txt, 12.5, col, weight="700")
    cv.text_px(pl.X(P0) + 8, pl.Y(0) - 14, "梁底開始受拉", 12, C["bmd"], "start")
    cv.text_px(W / 2, H - 46, f"主線 P = {PEX:.1f} tf（照考卷 3√f'c）：此時梁底拉應力 {LIM_EX:.1f}，屬 T 類，須另以開裂斷面檢核撓度", 13.5, C["load"], weight="700")
    cv.text_px(W / 2, H - 22, f"若要求不開裂（U 類）只能到 {PU:.1f} tf；把 3√f'c 當成「未開裂」或舊稱「B 級」就是漏了這一層", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-class.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "把 c_t＋c_b 當成圖上量得的梁高、忽略考卷數據矛盾"),
           (fig2_class, "§5 梁底拉力容許值", "把考卷 3√f'c 當成未開裂（舊稱 B 級），漏了 T 類的開裂斷面撓度檢核")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert abs(PEX - 25.3) < 0.05 and abs(PU - 18.9) < 0.05 and abs(PT - 26.6) < 0.05 and abs(P0 - 6.13) < 0.01, (P0, PU, PEX, PT)
    print(TAG, "OK", f"P0={P0:.2f} PU={PU:.2f} PEX={PEX:.2f} PT={PT:.2f}")
