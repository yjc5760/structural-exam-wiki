#!/usr/bin/env python3
"""RC-2003-1 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2003-1-problem.md §4，已確認）
用法：python3 gen_RC-2003-1.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2003-1"
# ── 判讀清單（RC-2003-1-problem.md §4，已確認）──
B, H = 35.0, 70.0          # #2
DP, DNS = 63.0, 58.0       # #1 預力（實心）63、非預力（空心）58，皆由頂面量起
R = 1.52 / 2               # 15.2 mm 鋼絞線（示意按實際直徑）
# 水平位置考卷未標尺寸，依考卷附圖比例示意
XS_P = [B * k for k in (0.17, 0.39, 0.61, 0.83)]
XS_N = [B * 0.17, B * 0.83]


def fig1_problem():
    W, Hc = 860, 700
    s = 6.6
    cv = Canvas(W, Hc, sx=s, ox=230, oy=110)
    cv.panel("圖 1 梁斷面（重繪）", "依題目正本判讀清單 #1–#3；三條尺寸皆由頂面量起")
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
    for x in XS_P:
        cv.circle((x, H - DP), R * 1.6, C["member"], C["member"], 1.0)
    for x in XS_N:
        cv.circle((x, H - DNS), R * 1.6, "#FFFFFF", C["member"], 1.8)
    cv.dim((0, H), (B, H), "35 cm", off=-22, label_off=-14)
    for x0, y1, lab, off in ((0, 0, "70 cm", 104), (0, H - DP, "63 cm", 66), (0, H - DNS, "58 cm", 28)):
        cv.dim((x0, H), (x0, y1), lab, off=off, label_off=16)
    cv.line((B + 1, H - DNS), (B + 6, H - DNS + 2), C["muted"], 1)
    cv.text((B + 6.5, H - DNS + 2), "2−15.2mmφ 非預力（空心）", 13, C["text"], "start")
    cv.line((B + 1, H - DP), (B + 6, H - DP - 3), C["muted"], 1)
    cv.text((B + 6.5, H - DP - 3), "4−15.2mmφ 預力（實心）", 13, C["text"], "start")
    cv.text_px(W / 2, Hc - 34, "鋼絞線水平位置考卷未標尺寸，依原圖比例示意", 12, C["muted"])
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="b＝35、h＝70 cm；預力 4 根 dp＝63、非預力 2 根 d＝58（皆自頂面量起）",
                   note="空心（上排）＝非預力、實心（下排）＝預力；圖 2 應力-應變曲線屬曲線圖，不重繪，見證據圖",
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

# ── 解題圖 fig-2：由 RC-2003-1.md §3.5 L1、§4 Step 1–5 解得 ──
B_W, H_T, D_P, D_NS = 35.0, 70.0, 63.0, 58.0
A_P, A_NS = 4 * 1.387, 2 * 1.387
FC, E_PS, F_PE, F_PU = 350.0, 2.0e6, 12_000.0, 19_000.0
F_PY, K2, F0 = 16_950.0, 65_000.0, 16_400.0     # 考卷圖 2：比例限、第二段斜率與截距
EPS_CU = 0.003
C_NA = 16.5                                       # §4 Step 3 試算收斂值
BETA1 = 0.85 - 0.05 * (FC - 280) / 70
EPS_PE = F_PE / E_PS
EPS_PY = F_PY / E_PS
sig = lambda e: E_PS * e if e <= EPS_PY else K2 * e + F0
EPS_FLEX_P = EPS_CU * (D_P - C_NA) / C_NA
EPS_PS = EPS_PE + EPS_FLEX_P
EPS_NS = EPS_CU * (D_NS - C_NA) / C_NA
F_PS, F_NS = sig(EPS_PS), sig(EPS_NS)
A_BLK = BETA1 * C_NA
M_N = (F_PS * A_P * (D_P - A_BLK / 2) + F_NS * A_NS * (D_NS - A_BLK / 2)) / 1e5


def fig2_strain():
    W, H = 1060, 580
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　應變一致性：兩種鋼絞線的應變從哪裡來、落在圖 2 的哪一段", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"c = {C_NA} cm（§4 試算收斂）、εcu = {EPS_CU}；預力鋼絞線另有有效預應變 εpe = {EPS_PE:.3f}", 13, C["muted"])
    # 左：應變分布（深度比例為真，應變為示意比例）
    top, hp = 110, 380
    yv = lambda d: top + d / H_T * hp
    x0, ks = 250, 9000.0
    cv.rect_px(150, top, 46, hp, C["panel"], 4, C["member2"], 1.2)
    for d, col, lab in [(D_NS, C["member2"], "非預力 d = 58"), (D_P, C["load"], "預力 dp = 63")]:
        cv.parts.append(f'<circle cx="173" cy="{yv(d):.1f}" r="6" fill="{col}"/>')
        cv.text_px(144, yv(d), lab, 11.5, col, "end")
    cv.parts.append(f'<line x1="{x0}" y1="{top}" x2="{x0}" y2="{top+hp}" stroke="{C["member2"]}" stroke-width="1.4"/>')
    xt = x0 - EPS_CU * ks
    xb = x0 + EPS_CU * (H_T - C_NA) / C_NA * ks
    cv.parts.append(f'<polygon points="{x0},{yv(C_NA):.1f} {xt:.1f},{top} {x0},{top}" fill="{C["fill_c"]}" stroke="{C["compr"]}" stroke-width="2"/>')
    cv.parts.append(f'<polygon points="{x0},{yv(C_NA):.1f} {xb:.1f},{top+hp} {x0},{top+hp}" fill="{C["fill_t"]}" stroke="{C["tension"]}" stroke-width="2"/>')
    cv.text_px(xt, top - 14, f"εcu = {EPS_CU}", 12, C["compr"], weight="700")
    cv.parts.append(f'<line x1="130" y1="{yv(C_NA):.1f}" x2="{x0+200}" y2="{yv(C_NA):.1f}" stroke="{C["accent"]}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    cv.text_px(x0 + 8, yv(C_NA) - 12, f"中性軸 c = {C_NA}", 12, C["accent"], "start", weight="700")
    for d, e_flex, extra, col in [(D_NS, EPS_NS, 0.0, C["member2"]), (D_P, EPS_FLEX_P, EPS_PE, C["load"])]:
        xe = x0 + e_flex * ks
        cv.parts.append(f'<line x1="{x0}" y1="{yv(d):.1f}" x2="{xe:.1f}" y2="{yv(d):.1f}" stroke="{col}" stroke-width="2.4"/>')
        if extra:
            cv.parts.append(f'<line x1="{xe:.1f}" y1="{yv(d)+9:.1f}" x2="{xe+extra*ks:.1f}" y2="{yv(d)+9:.1f}" stroke="{C["accent"]}" stroke-width="5"/>')
    cv.text_px(x0 + 6, yv(D_NS) - 14, f"εns = {EPS_NS:.6f}（只有撓曲應變）", 11.5, C["member2"], "start", weight="700")
    cv.text_px(x0 + 6, yv(D_P) + 30, f"εps = {EPS_PE:.3f} ＋ {EPS_FLEX_P:.6f} = {EPS_PS:.6f}", 11.5, C["load"], "start", weight="700")
    cv.text_px(300, top + hp + 22, "左圖深度按比例；橙色粗段＝有效預應變", 11.5, C["muted"])
    # 右：圖 2 雙直線
    pl = Plot(cv, 600, 110, 400, 360, (0.0, 0.018), (0.0, 20_000.0))
    pl.frame([0, 0.004, 0.008, 0.012, 0.016], [0, 5000, 10000, 15000, 20000], "應變 ε", "應力（kgf/cm²）",
             xfmt="{:g}", yfmt="{:,.0f}")
    pl.hline(F_PU, C["load"], 1.6, "6 5")
    cv.text_px(pl.X(0.0005), pl.Y(F_PU) - 12, f"fpu = {F_PU:,.0f}", 11.5, C["load"], "start")
    pl.curve([(0, 0), (EPS_PY, F_PY), (0.018, sig(0.018))], C["member"], 3.0)
    pl.vline(EPS_PY, C["dim"], 1.4, "4 4", 0, F_PY)
    cv.text_px(pl.X(EPS_PY), pl.Y(0) - 12, f"{EPS_PY:.6f}", 11, C["muted"])
    pl.dot(EPS_NS, F_NS, C["member2"]); pl.dot(EPS_PS, F_PS, C["load"])
    cv.text_px(pl.X(EPS_NS) - 10, pl.Y(F_NS) + 4, f"fns = {F_NS:,.0f}（彈性段）", 12, C["member2"], "end", weight="700")
    cv.text_px(pl.X(EPS_PS), pl.Y(F_PS) + 26, f"fps = {F_PS:,.0f}（第二段）", 12, C["load"], weight="700")
    cv.text_px(800, 82, "考卷圖 2（兩種鋼絞線共用）", 12.5, C["text"], weight="700")
    cv.text_px(W / 2, H - 46, f"Mn = {M_N:.1f} tf·m：預力鋼絞線進入第二段、非預力鋼絞線仍在彈性段", 13.5, C["bmd"], weight="700")
    cv.text_px(W / 2, H - 22, "攔：把非預力鋼絞線當成普通鋼筋（彈塑性 fy）；漏掉 εpe；預力／非預力深度對調", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-strain.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "預力與非預力深度對調（63／58 認反）"),
           (fig2_strain, "§4 Step 3", "非預力鋼絞線當普通鋼筋；漏掉 εpe；深度對調")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert round(F_PS)==17340 and round(F_NS)==15091 and round(M_N,1)==75.8 and abs(BETA1-0.80)<1e-12, (F_PS,F_NS,M_N)
    print(TAG, "OK")
