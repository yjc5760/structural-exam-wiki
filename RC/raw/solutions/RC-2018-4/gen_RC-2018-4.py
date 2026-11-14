#!/usr/bin/env python3
"""RC-2018-4 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2018-4-problem.md §4，已確認）
用法：python3 gen_RC-2018-4.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2018-4"
# ── 判讀清單（RC-2018-4-problem.md §4，已確認）──
B, H = 35.0, 70.0          # #2
YP = 15.0                  # #1 鋼鍵（套管）中心距梁底
DUCT = 7.5                 # 題文：套管直徑 7.5 cm（施預力後灌漿）


def fig1_problem():
    W, Hc = 640, 680
    s = 6.6
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - B * s / 2, oy=120)
    cv.panel("後拉預力梁斷面（重繪）", "依題目正本判讀清單 #1–#4；套管直徑按比例")
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
    cv.circle((B / 2, YP), DUCT / 2, "#C9D3E0", C["member"], 1.8)
    cv.circle((B / 2, YP), 1.2, C["member"], C["member"], 1.0)
    cv.line((B / 2 + DUCT / 2, YP + 1), (B + 6, YP + 6), C["muted"], 1)
    cv.text((B + 6.5, YP + 6), "套管 7.5 cmφ（灌漿）", 13, C["text"], "start")
    cv.text((B + 6.5, YP + 2.2), "A_{ps}＝14 cm²", 13, C["text"], "start")
    cv.dim((B, H), (B, 0), "70 cm", off=-34, label_off=-28)
    cv.dim((0, YP), (0, 0), "15 cm", off=30, label_off=26)
    cv.dim((0, 0), (B, 0), "35 cm", off=26, label_off=14)
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="矩形 35×70 cm；單一鋼鍵置中，套管中心距梁底 15 cm → dp＝55 cm",
                   note="考卷原圖未依比例（15 cm 尺寸線端點不精確），依慣例解讀為鋼鍵中心至梁底",
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

# ── 解題圖 fig-2：由 RC-2018-4.md §4 Step 1–10、§5.6 解得 ──
B_W, H_T, D_P = 35.0, 70.0, 55.0           # 斷面寬、全深、d_p（§4）
FE, A_PS = 100_000.0, 14.0                  # 有效預力、鋼鍵面積
FPU, FC = 19_000.0, 420.0
BETA1, PHI = 0.75, 0.90
FPS_SC, MN_SC = 15_721.0, 101.7             # §5.6 應變相容結果（f_ps、M_n tf·m）
EPS_PS = 0.0079                             # §5.6 極限狀態鋼鍵應變
A_G = B_W * H_T; I_G = B_W * H_T ** 3 / 12; Y_B = H_T / 2; S_B = I_G / Y_B
E_C = D_P - Y_B
F_R = 2.0 * math.sqrt(FC)
M_CR = S_B * (FE / A_G + FE * E_C * Y_B / I_G + F_R) / 1e5      # tf·m
FSE = FE / A_PS
RHO = A_PS / (B_W * D_P)
FPS = math.floor(FPU * (1 - round(0.5 * round(RHO, 6) * round(FPU / FC, 2), 4)) + 0.5)
                                            # 考卷參考公式①（主線；§4 Step 7 逐步取位得 15,875）
A_BLK = A_PS * FPS / (0.85 * FC * B_W)
MN = A_PS * FPS * (D_P - A_BLK / 2) / 1e5


def fig2_checks():
    W, H = 1040, 500
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　近似式的適用條件與「是否拉斷」的完整檢核", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "上：鋼鍵應力（kgf/cm²）；下：彎矩（tf·m）。只比 fps 小於 fpu 不夠，三項都要看", 13, C["muted"])

    def rows(y0, items, vmax, unit_fmt, marks):
        X0, BW = 330, 560
        sc = BW / vmax
        for v, lab, col in marks:
            x = X0 + v * sc
            cv.parts.append(f'<line x1="{x:.1f}" y1="{y0-30}" x2="{x:.1f}" y2="{y0+len(items)*50-10}" '
                            f'stroke="{col}" stroke-width="2.2" stroke-dasharray="7 5"/>')
            cv.text_px(x, y0 - 40, lab, 12.5, col, weight="700")
        for i, (name, desc, v, col) in enumerate(items):
            y = y0 + i * 50
            cv.text_px(40, y - 7, name, 13.5, C["text"], "start", weight="700")
            cv.text_px(40, y + 13, desc, 11.5, C["muted"], "start")
            cv.rect_px(X0, y - 13, BW, 26, "#EDF1F6", 6)
            cv.rect_px(X0, y - 13, v * sc, 26, col, 6)
            cv.text_px(X0 + v * sc + 8, y, unit_fmt.format(v), 13, C["text"], "start", weight="700")

    rows(140, [("有效應力 fse", f"= {FSE/FPU:.3f} fpu，低於門檻 → 近似式條件不成立", FSE, C["load"]),
               ("fps（考卷公式①，主線）", "照考卷公式計算", FPS, C["member2"]),
               ("fps（應變相容，§5.6）", f"極限應變 εps ≈ {EPS_PS:.4f}，遠小於斷裂應變（約 0.035）", FPS_SC, C["bmd"])],
         FPU * 1.1, "{:,.0f}", [(0.5 * FPU, f"0.5fpu = {0.5*FPU:,.0f}", C["accent"]), (FPU, f"fpu = {FPU:,.0f}", C["load"])])
    rows(330, [("開裂彎矩 Mcr", "有效預力＋fr = 2√f'c", M_CR, C["member2"]),
               ("設計強度 φMn（應變相容）", f"φ = {PHI}，Mn = {MN_SC}（主線近似式 {MN:.1f}，差 {abs(MN-MN_SC)/MN_SC*100:.1f}%）", PHI * MN_SC, C["bmd"])],
         MN * 1.1, "{:.1f}", [(1.2 * M_CR, f"1.2Mcr = {1.2*M_CR:.1f}", C["accent"])])
    cv.text_px(W / 2, H - 52, f"φMn = {PHI*MN_SC:.1f} ≥ 1.2Mcr = {1.2*M_CR:.1f}：開裂時混凝土拉力轉給鋼鍵，也不致瞬間拉斷", 13.5, C["bmd"], weight="700")
    cv.text_px(W / 2, H - 26, "攔兩件事：fse 未達 0.5fpu 還直接套近似式；拉斷只比 fps 與 fpu 就結束", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-checks.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "15 cm 量到套管邊緣、d_p 取 70−15 以外的值"),
           (fig2_checks, "§4 Step 7、§5.6", "f_se 未達 0.5f_pu 仍直接套近似式；拉斷只比 f_ps 與 f_pu")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert FPS==15875 and round(MN,1)==102.5 and round(M_CR,1)==43.4 and round(1.2*M_CR,1)==52.1 and round(PHI*MN_SC,1)==91.5, (FPS,MN,M_CR)
    print(TAG, "OK")
