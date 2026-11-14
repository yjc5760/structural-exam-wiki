#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RC-2013-4 先拉預力梁・Mcr 與鋼腱極限應變 — 解題圖解產生腳本（2026-11-14，RC-U4-1 批 1 階段 E）
用法：python3 gen_RC-2013-4.py [輸出目錄]（預設 figs/）
三條鐵則：常數區只放 §3.5 L1 給定值，應力與容許值一律現算，檔尾對 §4 公佈值 assert。
FIGURES
  fig-1-strain  鋼腱極限應變三層疊加  攔：只算 fps/Ep、漏掉 εpe 或去壓應變"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2013-4"

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
B_W, H_T, ECC = 30.0, 60.0, 20.0
F_E, A_PS = 65_000.0, 6.5
F_PU, FC = 17_100.0, 350.0
E_P = 2.04e6                          # 考卷記為 E_s
GAM_B1 = 0.5                          # 參考式係數（γp/β1）
EPS_CU = 0.003
A_G, I_G = B_W * H_T, B_W * H_T ** 3 / 12
D_P = H_T / 2 + ECC
E_C = 15_000 * math.sqrt(FC)          # 自行假設
BETA1 = 0.85 - 0.05 * (FC - 280) / 70
RHO = A_PS / (B_W * D_P)
F_PS = F_PU * (1 - GAM_B1 * RHO * F_PU / FC)
C_NA = A_PS * F_PS / (0.85 * FC * BETA1 * B_W)
EPS_PE = F_E / A_PS / E_P
F_CE = F_E / A_G + F_E * ECC ** 2 / I_G
EPS_CE = F_CE / E_C
EPS_FL = EPS_CU * (D_P - C_NA) / C_NA
EPS_U = EPS_PE + EPS_CE + EPS_FL
EPS_WRONG = F_PS / E_P


def fig1_strain():
    W, H = 1060, 520
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　鋼腱極限應變的三層疊加（×10^{{-3}}）", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"dp = {D_P:.0f} cm、c = {C_NA:.2f} cm、εcu = {EPS_CU}；先拉法有握裹", 13, C["muted"])
    # 左：從斷面到鋼腱的三個階段（深度比例為真）
    top, hp = 110, 300
    yv = lambda d: top + d / H_T * hp
    x0, ks = 230, 9000.0
    cv.rect_px(70, top, 44, hp, C["panel"], 4, C["member2"], 1.2)
    cv.parts.append(f'<circle cx="92" cy="{yv(D_P):.1f}" r="6" fill="{C["load"]}"/>')
    cv.text_px(64, yv(D_P), f"dp = {D_P:.0f}", 11.5, C["load"], "end")
    cv.parts.append(f'<line x1="{x0}" y1="{top}" x2="{x0}" y2="{top+hp}" stroke="{C["member2"]}" stroke-width="1.4"/>')
    xt, xb = x0 - EPS_CU * ks, x0 + EPS_CU * (H_T - C_NA) / C_NA * ks
    cv.parts.append(f'<polygon points="{x0},{yv(C_NA):.1f} {xt:.1f},{top} {x0},{top}" fill="{C["fill_c"]}" stroke="{C["compr"]}" stroke-width="2"/>')
    cv.parts.append(f'<polygon points="{x0},{yv(C_NA):.1f} {xb:.1f},{top+hp} {x0},{top+hp}" fill="{C["fill_t"]}" stroke="{C["tension"]}" stroke-width="2"/>')
    cv.parts.append(f'<line x1="{x0}" y1="{yv(D_P):.1f}" x2="{x0+EPS_FL*ks:.1f}" y2="{yv(D_P):.1f}" stroke="{C["load"]}" stroke-width="2.4"/>')
    cv.text_px(xt, top - 14, f"εcu = {EPS_CU}", 12, C["compr"], weight="700")
    cv.text_px(x0 + 8, yv(C_NA) - 12, f"c = {C_NA:.2f}", 12, C["accent"], "start", weight="700")
    cv.text_px(x0 + EPS_FL * ks / 2, yv(D_P) - 14, "③ 撓曲增量", 12, C["load"], weight="700")
    cv.text_px(210, top + hp + 40, "③ 只是斷面應變圖上看得到的那一段", 11.5, C["muted"])
    # 右：堆疊長條
    X0, BW, vmax = 470, 470, 14.0
    sc = BW / vmax
    rows = [("本解：三層合計", [(EPS_PE, C["accent"], "①"), (EPS_CE, C["sfd"], "②"), (EPS_FL, C["load"], "③")]),
            ("常見誤讀：只算 fps / Ep", [(EPS_WRONG, C["dim"], "")])]
    for i, (name, segs) in enumerate(rows):
        y = 170 + i * 110
        cv.text_px(X0, y - 34, name, 13.5, C["text"], "start", weight="700")
        x = X0
        for v, col, tag in segs:
            cv.rect_px(x, y - 16, v * 1e3 * sc, 32, col, 0)
            if v * 1e3 * sc > 34:
                cv.text_px(x + v * 1e3 * sc / 2, y, f"{tag} {v*1e3:.2f}", 12.5, "#FFFFFF", weight="700")
            x += v * 1e3 * sc
        tot = sum(s[0] for s in segs)
        cv.text_px(x + 10, y, f"{tot*1e3:.2f}", 14, C["load"] if i == 0 else C["muted"], "start", weight="700")
    cv.text_px(X0, 170 + 30, f"② 去壓應變 {EPS_CE*1e3:.2f}：鋼腱處混凝土預壓 {F_CE:.2f} 先被消除", 11.5, C["sfd"], "start")
    cv.text_px(X0, 280 + 30, f"fps = {F_PS:,.0f} 是參考式的應力，不是由應變算出；除以 Ep 只得 {EPS_WRONG*1e3:.2f}", 11.5, C["muted"], "start")
    cv.legend(X0, 360, [(C["accent"], "① 有效預應變 εpe = fse/Ep"), (C["sfd"], "② 去壓應變 εce = fce/Ec"), (C["load"], "③ 撓曲增量 εcu(dp−c)/c")])
    cv.text_px(W / 2, H - 22, f"鋼腱極限應變 εps,u = {EPS_U*1e3:.2f}×10^{{-3}} ≈ 0.013；攔：只算 fps/Ep、漏掉 εpe 或去壓應變", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-strain.svg")
    cv.save(path); save_png(path)
    return path


FIGURES = [(fig1_strain, "§4 Step 8", "只算 fps/Ep；漏掉有效預應變或去壓應變")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert round(F_PS) == 15290 and round(C_NA, 2) == 13.92 and abs(EPS_U - 12.98e-3) < 0.01e-3, (F_PS, C_NA, EPS_U)
    assert abs(EPS_PE - 4.902e-3) < 1e-6 and abs(EPS_CE - 0.3002e-3) < 1e-6 and abs(EPS_FL - 7.778e-3) < 2e-6, (EPS_PE, EPS_CE, EPS_FL)
    print(TAG, "OK", f"εps,u={EPS_U*1e3:.3f}e-3")
