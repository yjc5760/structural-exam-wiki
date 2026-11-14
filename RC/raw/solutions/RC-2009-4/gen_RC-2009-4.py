#!/usr/bin/env python3
"""RC-2009-4 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2009-4-problem.md §4，已確認）
用法：python3 gen_RC-2009-4.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2009-4"
# ── 判讀清單（RC-2009-4-problem.md §4，已確認）──
B = 30.0                         # #2
G = [3.0, 15.0, 27.0]            # 格線：尺寸鏈 3-12-12-3
PS = [(3, 3), (27, 3), (3, 27), (27, 27)]          # #1 預力鋼棒 15φ（四角）
RB = [(15, 3), (3, 15), (27, 15), (15, 27)]        # #1 D29（四邊中點）
D29 = 2.87


def star(cv, p, r=1.3):
    for k in range(4):
        a = math.pi * k / 4
        cv.line((p[0] - r * math.cos(a), p[1] - r * math.sin(a)),
                (p[0] + r * math.cos(a), p[1] + r * math.sin(a)), C["load"], 2.2)


def fig1_problem():
    W, Hc = 900, 700
    s = 12.0
    cv = Canvas(W, Hc, sx=s, ox=170, oy=130)
    cv.panel("圖二（b）斷面（重繪）", "依題目正本判讀清單 #1–#3；正中心無鋼材")
    cv.polygon([(0, 0), (B, 0), (B, B), (0, B)], "#EDF1F6", C["member"], 2.6)
    for g in G:
        cv.line((g, -1), (g, B + 1), C["ghost"], 1, dash="4 4")
        cv.line((-1, g), (B + 1, g), C["ghost"], 1, dash="4 4")
    for p in RB:
        cv.circle(p, D29 / 2, C["member"], C["member"], 1)
    for p in PS:
        star(cv, p)
    chain = [0.0] + G + [B]
    for a, b in zip(chain[:-1], chain[1:]):
        cv.dim((a, 0), (b, 0), f"{b - a:g}", off=26, label_off=14)
        cv.dim((0, b), (0, a), f"{b - a:g}", off=26, label_off=16)
    cv.dim((0, 0), (B, 0), "30 cm", off=62, label_off=14)
    cv.dim((0, B), (0, 0), "30 cm", off=70, label_off=24)
    cv.line((27.9, 27.9), (B + 4, B + 3), C["muted"], 1)
    cv.text((B + 4.5, B + 3), "預力鋼棒 15φ（4 根，四角）", 13, C["text"], "start")
    cv.line((27 + D29 / 2, 15), (B + 4, 12), C["muted"], 1)
    cv.text((B + 4.5, 12), "鋼筋 D29（4 根，四邊中點）", 13, C["text"], "start")
    cv.text((B + 4.5, 5), "純軸拉力，w_{max}＝0.03 cm", 13, C["muted"], "start")
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="30×30 cm 斷面；預力鋼棒 4 根在四角、D29 4 根在四邊中點，皆距邊 3 cm",
                   note="Ap＝4×1.77＝7.08 cm²、As＝4×6.47＝25.88 cm²；正中心格點只有格線交點、沒有鋼材",
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

# ── 解題圖 fig-2：由 RC-2009-4.md §4 Step 1–6、§5 解得 ──
AP, AS = 4 * 1.77, 4 * 6.47                 # 預力鋼棒、D29 總面積 (cm^2)
AC = 30.0 * 30.0 - AS - AP                  # 淨混凝土
FC, ES = 350.0, 2.04e6
EC, FR = 15000 * math.sqrt(FC), 2.0 * math.sqrt(FC)     # 自行假設（§1）
FPE, FPY, FY = 13_200.0, 16_330.0, 4_200.0
WMAX, DC = 0.03, 3.0
EPS_C0 = -AP * FPE / (AC * EC + AS * ES)


def tie(beta, a_eff, with_concrete=True):
    fs = WMAX / (1.08e-6 * beta * (DC * a_eff) ** (1 / 3))
    fp = min(FPE + ES * (fs / ES - EPS_C0), FPY)
    fct = FR / (1 + math.sqrt(500 * fs / ES)) if with_concrete else 0.0
    return fs, AS * fs / 1e3, AP * fp / 1e3, AC * fct / 1e3     # tf


CASES = [("本解", "β = 1.0、A = 900/8、平均應變斷面", tie(1.0, 900 / 8)),
         ("替代：只算 D29", "β = 1.0、A = 900/4", tie(1.0, 900 / 4)),
         ("舊解（已勘誤）", "β = 1.25、A = 900/4、裂縫斷面", tie(1.25, 900 / 4, False))]


def fig2_force():
    W, H = 1060, 560
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　使 w_{{max}} = 0.03 cm 的軸拉力 N 由哪三部分組成", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "左：β 的意義（拉力外緣應變 ÷ 拉筋應變）；右：N = As·fs ＋ Ap·fp ＋ Ac·fct（tf）", 13, C["muted"])
    # 左：兩種應變分布
    def strain(x0, title, eps_face, eps_bar, na):
        top, bot, wpx = 130, 330, 70
        cv.rect_px(x0, top, 34, bot - top, C["panel"], 4, C["member2"], 1.2)
        ys = bot - 30
        cv.parts.append(f'<circle cx="{x0+17}" cy="{ys}" r="6" fill="{C["member"]}"/>')
        xa = x0 + 60
        cv.parts.append(f'<line x1="{xa}" y1="{top}" x2="{xa}" y2="{bot}" stroke="{C["member2"]}" stroke-width="1.4"/>')
        if na is None:
            pts = f"{xa},{top} {xa+wpx*eps_face},{top} {xa+wpx*eps_face},{bot} {xa},{bot}"
        else:
            pts = f"{xa},{na} {xa+wpx*eps_face},{bot} {xa},{bot}"
            cv.text_px(xa - 8, na, "中性軸", 11.5, C["muted"], "end")
        cv.parts.append(f'<polygon points="{pts}" fill="{C["fill_t"]}" stroke="{C["tension"]}" stroke-width="2"/>')
        cv.parts.append(f'<line x1="{x0+17}" y1="{ys}" x2="{xa+wpx*eps_bar}" y2="{ys}" stroke="{C["accent"]}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        cv.text_px(x0 + 70, top - 22, title, 13, C["text"], weight="700")
    strain(40, "梁（彎曲）", 1.0, 0.8, 150)
    strain(200, "本題（純軸拉）", 0.9, 0.9, None)
    cv.text_px(105, 362, "β = 1.2 左右", 12.5, C["muted"])
    cv.text_px(265, 362, "應變均勻 → β = 1.0", 12.5, C["bmd"], weight="700")
    cv.text_px(185, 392, "把中性軸放在形心 → β = 1.25（錯）", 12, C["load"])
    # 右：堆疊長條
    X0, BW, vmax = 520, 440, 260.0
    sc = BW / vmax
    cols = [C["compr"], C["bmd"], C["accent"]]
    for i, (name, desc, (fs, n_s, n_p, n_c)) in enumerate(CASES):
        y = 160 + i * 92
        cv.text_px(X0, y - 34, f"{name}　{desc}", 13, C["text"], "start", weight="700")
        x = X0
        for v, col in zip((n_s, n_p, n_c), cols):
            if v > 0:
                cv.rect_px(x, y - 15, v * sc, 30, col, 0)
                if v * sc > 38:
                    cv.text_px(x + v * sc / 2, y, f"{v:.1f}", 12.5, "#FFFFFF", weight="700")
                x += v * sc
        tot = n_s + n_p + n_c
        cv.text_px(x + 10, y, f"N = {tot:.0f} tf", 14, C["load"] if i == 2 else C["text"], "start", weight="700")
        cv.text_px(X0, y + 28, f"fs = {fs:,.0f}；" + (f"Ac·fct = {n_c:.1f}" if n_c else "未計混凝土平均拉力"), 11.5, C["muted"], "start")
    cv.legend(X0, 455, [(C["compr"], "D29：As·fs"), (C["bmd"], "預力棒：Ap·fp（已降伏，取 fpy）"), (C["accent"], "混凝土平均拉力：Ac·fct")])
    cv.text_px(W / 2, H - 22, "攔兩件事：純拉時 β 取 1.25；漏掉題目明文要求的混凝土平均拉力（舊解 181 tf）", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-force.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "把預力鋼棒與 D29 位置互換、正中心多算一根"),
           (fig2_force, "§4 Step 3–6", "純拉取 β=1.25；漏掉混凝土平均拉力 A_c f_ct")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    _n = [sum(c[2][1:]) for c in CASES]
    assert round(CASES[0][2][0])==3990 and round(_n[0])==235 and round(_n[1])==215 and round(_n[2])==181, _n
    print(TAG, "OK")
