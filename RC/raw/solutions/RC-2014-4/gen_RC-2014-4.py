#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RC-2014-4 對稱 I 形預力梁・兩階段應力檢核 — 解題圖解產生腳本（2026-11-14，RC-U4-1 批 1 階段 E）
用法：python3 gen_RC-2014-4.py [輸出目錄]（預設 figs/）
三條鐵則：常數區只放 §3.5 L1 給定值，應力與容許值一律現算，檔尾對 §4 公佈值 assert。
FIGURES
  fig-1-stress  兩階段應力分布與容許值  攔：kgf/cm² 應力套 SI（MPa）係數，把合格斷面判成超限"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2014-4"

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

# ── §3.5 L1 給定 ──
L, I_C, A_C, C1, ECC = 1200.0, 469_000.0, 1100.0, 30.0, 19.8
P_I, P_E = 70_000.0, 60_000.0
W_D, W_L = 0.264, 1.1            # tf/m
FCI, FC = 300.0, 420.0
S = round(I_C / C1)              # §3.5 L2 取 15,633
M_D = W_D * (L / 100) ** 2 / 8 * 1e5
M_T = (W_D + W_L) * (L / 100) ** 2 / 8 * 1e5
# 不逐項取位（§3.5 把 P_e·e/S 寫成 76.00，精確值 75.99，故使用階段底纖維精確為 −26.51；圖上取到 0.1）
st = lambda P, M: (P / A_C - P * ECC / S + M / S, P / A_C + P * ECC / S - M / S)
T1, B1 = st(P_I, M_D)
T2, B2 = st(P_E, M_T)
R = lambda k, f: round(k * math.sqrt(f), 2)
LIM = dict(t1=R(0.8, FCI), t1_si=R(0.25, FCI), c1=0.60 * FCI,
           tU=R(2.0, FC), tT=R(3.2, FC), t2_si=R(1.0, FC), c2=0.60 * FC, c2d=0.45 * FC)


def stage(title, sub, ftop, fbot, xr, lines):
    cv = Canvas(500, 520, sx=1)
    cv.panel(title, sub)
    pl = Plot(cv, 70, 120, 390, 300, xr, (0.0, 60.0))
    pl.frame([v for v in range(int(xr[0] // 50 * 50), int(xr[1]) + 1, 50) if xr[0] <= v <= xr[1]], [],
             "應力（kgf/cm²，壓為正）", "")
    for yv, lab in [(60, "梁頂"), (30, "形心"), (0, "梁底")]:
        cv.text_px(62, pl.Y(yv), lab, 12, C["muted"], "end")
    pl.vline(0, C["member2"], 1.4, None)
    for x, col, dash, lab, row in lines:
        pl.vline(x, col, 2.0, dash)
        cv.text_px(pl.X(x), 120 + 300 + 50 + 18 * row, lab, 11.5, col, weight="700")
    pts = f"{pl.X(0):.1f},{pl.Y(60):.1f} {pl.X(ftop):.1f},{pl.Y(60):.1f} {pl.X(fbot):.1f},{pl.Y(0):.1f} {pl.X(0):.1f},{pl.Y(0):.1f}"
    cv.parts.append(f'<polygon points="{pts}" fill="{C["fill_c"]}" stroke="{C["compr"]}" stroke-width="2.4"/>')
    cv.text_px(pl.X(ftop), pl.Y(60) - 14, f"{ftop:+.1f}", 13, C["compr"], weight="700")
    cv.text_px(pl.X(fbot) + (-8 if fbot < 0 else 8), pl.Y(0) - 14, f"{fbot:+.1f}", 13,
               C["tension"] if fbot < 0 else C["compr"], "end" if fbot < 0 else "start", weight="700")
    return cv


def fig1_stress():
    g1 = stage("施加預力時（Pi、自重；f'ci = 300）", "頂、底皆受壓", T1, B1, (-50.0, 200.0),
               [(-LIM["t1"], C["bmd"], "7 5", f"0.8√f'ci = {LIM['t1']}", 0),
                (-LIM["t1_si"], C["dim"], "3 4", f"誤：0.25√f'ci = {LIM['t1_si']}", 1),
                (LIM["c1"], C["load"], "7 5", f"0.60f'ci = {LIM['c1']:.0f}", 0)])
    g2 = stage("使用載重時（Pe、全部載重；f'c = 420）", "底纖維受拉 → 依 U 類上限檢核", T2, B2, (-80.0, 260.0),
               [(-LIM["tU"], C["bmd"], "7 5", f"U 類 2.0√f'c = {LIM['tU']}", 0),
                (-LIM["tT"], C["accent"], "3 4", f"T 類上限 {LIM['tT']}", 1),
                (-LIM["t2_si"], C["dim"], "3 4", f"誤：1.0√f'c = {LIM['t2_si']}", 2),
                (LIM["c2d"], C["accent"], "3 4", f"0.45f'c = {LIM['c2d']:.0f}", 1),
                (LIM["c2"], C["load"], "7 5", f"0.60f'c = {LIM['c2']:.0f}", 0)])
    path = os.path.join(OUT, f"{TAG}-fig-1-stress.svg")
    compose([g1, g2], title=f"{TAG}　兩階段跨中應力分布與容許值（kgf/cm² 制）",
            sub=f"使用階段底纖維 {B2:+.1f}：在 U 類上限 {LIM['tU']} 之內（用掉 {-B2/LIM['tU']*100:.0f}%）→ 符合規範",
            note=f"灰色虛線是以 kgf/cm² 算應力卻套 SI（MPa）係數得到的容許值：小約 3.19 倍，會把 {-B2:.1f} 誤判為超限",
            path=path)
    save_png(path)
    return path


FIGURES = [(fig1_stress, "§4 規範容許應力驗算", "kgf/cm² 應力套 SI 係數，誤判「不符合規範」")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert all(abs(a - b) < 0.015 for a, b in zip((T1, B1, T2, B2), (5.38, 121.90, 135.60, -26.50))), (T1, B1, T2, B2)
    assert (LIM["t1"], LIM["tU"], LIM["tT"], LIM["t1_si"], LIM["t2_si"]) == (13.86, 40.99, 65.58, 4.33, 20.49), LIM
    print(TAG, "OK", f"{T1:.2f} {B1:.2f} {T2:.2f} {B2:.2f}")
