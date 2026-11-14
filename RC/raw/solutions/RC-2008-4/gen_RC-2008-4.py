#!/usr/bin/env python3
"""RC-2008-4 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2008-4-problem.md §4，已確認）
用法：python3 gen_RC-2008-4.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2008-4"
# ── 判讀清單（RC-2008-4-problem.md §4，已確認）──
BF, TF = 90.0, 15.0        # #2 版寬 90、版厚 15
BW, HB = 30.0, 70.0        # #1 梁 30×70（版底量到梁底）
CGS = 20.0                 # #4 c.g.s. 距梁底


def fig1_problem():
    W, Hc = 700, 640
    s = 4.6
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - 10, oy=120)
    cv.panel("圖四 跨中合成斷面（重繪）", "依題目正本判讀清單 #1–#4；梁 70 cm 不含版")
    cv.polygon([(-BW / 2, 0), (BW / 2, 0), (BW / 2, HB), (-BW / 2, HB)], "#EDF1F6", C["member"], 2.6)
    cv.polygon([(-BF / 2, HB), (BF / 2, HB), (BF / 2, HB + TF), (-BF / 2, HB + TF)], "#E3E9F2", C["member"], 2.4)
    cv.circle((0, CGS), 1.4, "#FFFFFF", C["member"], 1.8)
    cv.line((-BW / 2 - 12, CGS), (-1.6, CGS), C["muted"], 1)
    cv.text((-BW / 2 - 13, CGS + 2.6), "c.g.s.", 13, C["text"], "end")
    cv.dim((-BF / 2, HB + TF), (BF / 2, HB + TF), "90 cm", off=-24, label_off=-14)
    cv.dim((BF / 2, HB + TF), (BF / 2, HB), "15 cm", off=-28, label_off=-24)
    cv.dim((BW / 2, HB), (BW / 2, 0), "70 cm", off=-40, label_off=-26)
    cv.dim((-BW / 2, CGS), (-BW / 2, 0), "20 cm", off=26, label_off=24)
    cv.dim((-BW / 2, 0), (BW / 2, 0), "30 cm", off=26, label_off=14)
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="樓版 90×15 cm（f'c＝280）＋預力梁 30×70 cm（f'c＝350），梁置中；c.g.s. 距梁底 20 cm",
                   note="70 cm 由版底量到梁底（梁全深），合成斷面總深 85 cm；梁距考卷未給，90 cm 即合成斷面翼寬",
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

# ── 解題圖 fig-2：由 RC-2008-4.md §4 Step 3–6 解得（圖中壓應力畫為正；§4 內文以壓為負）──
L_SPAN = 1500.0                              # 跨度 (cm)
F1_BOT, F1_TOP = 122.64, 67.84               # Stage 1 梁底／梁頂壓應力大小（§4 Step 3）
S_CB, S_CT, S_SL = 44_849.0, 116_311.0, 65_741.0   # 合成斷面：梁底、梁頂、版頂（轉換）斷面模數
N_R = math.sqrt(280 / 350)
FC1, FC2 = 350.0, 280.0
M1 = 10.0 * L_SPAN ** 2 / 8                  # 每 1 tf/m 活載重的跨中彎矩 (kgf·cm)
K_BOT, K_TOP, K_SL = M1 / S_CB, M1 / S_CT, M1 * N_R / S_SL
LIM_B, LIM_S = 0.45 * FC1, 0.45 * FC2
W_BOT = F1_BOT / K_BOT
W_TOP = (LIM_B - F1_TOP) / K_TOP
W_SL = LIM_S / K_SL
F_WRONG = 159.83                             # §5：版重誤放合成斷面時 Stage 1 梁底
# 註：§4 Step 5 寫 122.64×44,849＝5,498,900，精確為 5,500,281 → w 精確 1.9557（正本取 1.955，差 0.03%）


def fig2_wll():
    W, H = 1000, 620
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　三個纖維的壓應力隨活載重 w_{{LL}} 變化：誰先碰到限值", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "圖中壓應力畫為正（§4 內文以壓為負）；梁、版各依自身 f'c 取 0.45f'c；全斷面不得受拉", 13, C["muted"])
    pl = Plot(cv, 110, 110, 600, 380, (0.0, 4.0), (-40.0, 180.0))
    pl.frame([0, 1, 2, 3, 4], range(-40, 181, 40), "活載重 w_{LL}（tf/m）", "壓應力（kgf/cm²）")
    pl.band(0, -40, C["load"], 0.10)
    pl.hline(0, C["load"], 2.0, "8 5")
    pl.hline(LIM_B, C["deform"], 1.8, "8 5")
    pl.hline(LIM_S, C["bmd"], 1.8, "8 5")
    pl.curve([(0, F1_BOT), ((F1_BOT + 40) / K_BOT, -40)], C["deform"], 3.4)
    pl.curve([(0, F1_TOP), (4, F1_TOP + 4 * K_TOP)], C["member2"], 3.0)
    pl.curve([(0, 0), (4, 4 * K_SL)], C["bmd"], 3.0)
    for w, f, col in [(W_BOT, 0, C["load"]), (W_SL, LIM_S, C["bmd"]), (W_TOP, LIM_B, C["member2"])]:
        pl.vline(w, col, 1.5, "4 4", -40, f); pl.dot(w, f, col)
        cv.text_px(pl.X(w), pl.Y(-40) - 12, f"{w:.2f}", 12.5, col, weight="700")
    pl.dot(0, F_WRONG, C["dim"], 5)
    cv.text_px(pl.X(0.08), pl.Y(F_WRONG) - 12, f"版重誤放合成斷面：Stage 1 梁底 {F_WRONG} 已超限", 11.5, C["muted"], "start")
    cv.text_px(pl.X(0.5), pl.Y(F1_BOT - 0.5 * K_BOT) - 18, "梁底", 13, C["deform"], "start", weight="700")
    cv.text_px(pl.X(1.0), pl.Y(F1_TOP + 1.0 * K_TOP) - 16, "梁頂", 13, C["member2"], "start", weight="700")
    cv.text_px(pl.X(1.6), pl.Y(1.6 * K_SL) + 20, "版頂（×n）", 13, C["bmd"], "start", weight="700")
    xr = 728
    for y, col, name, desc in [(LIM_B, C["deform"], f"梁 0.45f'c = {LIM_B}", f"梁頂到 w = {W_TOP:.2f}"),
                               (LIM_S, C["bmd"], f"版 0.45f'c2 = {LIM_S:.0f}", f"版頂到 w = {W_SL:.2f}"),
                               (0, C["load"], "不得受拉（0）", f"梁底到 w = {W_BOT:.2f}（控制）")]:
        cv.text_px(xr, pl.Y(y) - 9, name, 13, col, "start", weight="700")
        cv.text_px(xr, pl.Y(y) + 11, desc, 11.5, C["muted"], "start")
    cv.text_px(W / 2, H - 46, f"控制條件是梁底不得受拉：w_{{LL}} ≈ {W_BOT:.2f} tf/m（§4 取 1.955；版寬 90 cm 合 {W_BOT/0.9:.2f} tf/m²）", 13.5, C["load"], weight="700")
    cv.text_px(W / 2, H - 22, f"攔：版也用 350 的 0.45f'c（{LIM_B}）；以為壓應力限值控制；把版重放到合成斷面", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-wll.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "把 70 cm 當成含版總深；c.g.s. 量錯基準"),
           (fig2_wll, "§4 Step 5–6", "版用梁的 0.45f'c；以為壓應力控制；版重放到合成斷面")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert abs(W_BOT-1.955)<0.002 and abs(N_R-0.8944)<1e-4, (W_BOT, W_TOP, W_SL)
    print(TAG, "OK")
