#!/usr/bin/env python3
"""RC-2021-4 題目附圖重繪腳本（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2021-4-problem.md §4，已確認）
用法：python3 gen_RC-2021-4.py [輸出目錄]（預設 figs/）；只畫考卷給的東西。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2021-4"
# ── 判讀清單（RC-2021-4-problem.md §4，已確認）──
S = 250.0                 # #3 梁中心距
BW, HB = 30.0, 50.0       # #2 預鑄梁
TF = 12.0                 # 場鑄板厚
YP_MID = 10.0             # #4 跨中鋼腱距梁底
YP_END = 25.0             # #4 兩端在梁高一半
L = 1200.0                # 跨度 12 m


def fig1_problem():
    W, Hc = 1000, 380
    s = 1.35
    cv = Canvas(W, Hc, sx=s, ox=W / 2, oy=90)
    cv.panel("圖四之一 合成斷面（重繪）", "依題目正本判讀清單 #1–#3、#5；62 cm 由板頂量到梁底")
    xe = 1.2 * S
    cv.polygon([(-xe, HB), (xe, HB), (xe, HB + TF), (-xe, HB + TF)], "#E3E9F2", C["member"], 2.2)
    for x in (-S, 0.0, S):
        cv.polygon([(x - BW / 2, 0), (x + BW / 2, 0), (x + BW / 2, HB), (x - BW / 2, HB)], "#EDF1F6", C["member"], 2.4)
        cv.line((x, -14), (x, HB + TF + 26), C["muted"], 1, dash="6 4")
        cv.circle((x, YP_MID), 3.4, C["member"], C["member"], 1)
    cv.dim((-S, HB + TF + 18), (0, HB + TF + 18), "250 cm", off=0, label_off=-13)
    cv.dim((0, HB + TF + 18), (S, HB + TF + 18), "250 cm", off=0, label_off=-13)
    cv.dim((xe, HB + TF), (xe, HB), "12 cm", off=-22, label_off=-26)
    cv.dim((-BW / 2 - 30, HB + TF), (-BW / 2 - 30, 0), "62 cm", off=0, label_off=24)
    cv.dim((BW / 2 + 8, YP_MID), (BW / 2 + 8, 0), "10 cm", off=-6, label_off=-24)
    cv.dim((-BW / 2, 0), (BW / 2, 0), "30 cm", off=22, label_off=14)
    cv.text((BW / 2 + 22, 30), "預力鋼腱（圖中標 A_s）", 12.5, C["text"], "start")
    return compose([cv], title=f"{TAG} 題目附圖之一（重繪）",
                   sub="場鑄板 12 cm＋預鑄梁 30×50 cm，梁中心距 250 cm（淨距 220 cm）",
                   note="62 cm＝12＋50（板頂到梁底）；圖中實心圓即預力鋼腱位置（跨中距梁底 10 cm）",
                   path=os.path.join(OUT, f"{TAG}-fig-1-problem.svg"))


def fig2_problem():
    W, Hc = 1000, 520
    kx, s = 0.27, 2.6     # 水平 1 cm → 0.6 單位（示意壓縮），垂直按比例
    X = lambda x: x * kx
    cv = Canvas(W, Hc, sx=s, ox=80, oy=150)
    cv.panel("圖四之二 立面與鋼腱線形（重繪）", "依題目正本判讀清單 #4；水平向壓縮示意，垂直依比例")
    cv.polygon([(0, 0), (X(L), 0), (X(L), HB), (0, HB)], "#EDF1F6", C["member"], 2.4)
    cv.line((-6, YP_END), (X(L) + 6, YP_END), C["ghost"], 1.2, dash="7 4")
    pts = [(X(x), YP_END - (YP_END - YP_MID) * 4 * x * (L - x) / L ** 2) for x in [L * i / 60 for i in range(61)]]
    cv.poly(pts, C["load"], 2.6)
    cv.line((X(L / 2), -8), (X(L / 2), HB + 18), C["muted"], 1, dash="6 4")
    cv.text((X(L / 2), HB + 21), "CL（跨中）", 13, C["text"])
    cv.support((0, 0), "pin")
    cv.support((X(L), 0), "roller")
    cv.dim((0, YP_END), (0, 0), "25 cm", off=24, label_off=26)
    cv.dim((X(L), HB), (X(L), 0), "50 cm", off=-24, label_off=-26)
    cv.dim((X(L / 2) + 6, YP_MID), (X(L / 2) + 6, 0), "10 cm", off=-4, label_off=-24)
    cv.text((X(L / 2) + 4, (YP_END + YP_MID) / 2), "h＝15", 13, C["text"], "start")
    cv.dim((0, -14), (X(L), -14), "12 m", off=0, label_off=14)
    cv.dim((0, HB + 12), (X(L / 2), HB + 12), "B = 6 m", off=0, label_off=-13)
    cv.arrow((0, -24), (30, -24), C["muted"], 1.6, 8)
    cv.text((33, -24), "x", 13, C["muted"], "start")
    return compose([cv], title=f"{TAG} 題目附圖之二（重繪）",
                   sub="簡支（左鉸右滾）；拋物線鋼腱兩端在梁高一半（距梁底 25 cm、偏心 0），跨中距梁底 10 cm",
                   note="跨中垂距 h＝25−10＝15 cm；B 為支承至跨中距離（12 m 的一半）",
                   path=os.path.join(OUT, f"{TAG}-fig-2-problem.svg"))


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

# ── 解題圖 fig-3：由 RC-2021-4.md §4 Step 2–6、§5 爭議點 4 解得 ──
FE, A_C, I_C = 210_000.0, 4_164.0, 1_266_748.0   # 有效預力、合成斷面 A、I（§4 Step 2）
YB, CT, E_P  = 44.83, 17.17, 34.83                # 形心至梁底／頂、鋼腱偏心（§4 Step 2–3）
MD, ML1      = 2_880_000.0, 1_800_000.0           # 靜載重彎矩、每 1 tf/m 活載重彎矩 (kgf·cm)
FC = 350.0
F_BOT0 = FE / A_C + FE * E_P * YB / I_C - MD * YB / I_C     # 有效預力＋靜載重 梁底
F_TOP0 = FE / A_C - FE * E_P * CT / I_C + MD * CT / I_C     # 同上 梁頂
K_BOT, K_TOP = ML1 * YB / I_C, ML1 * CT / I_C               # 每 1 tf/m 的應力變化
LIM_C, LIM_D = 0.6 * FC, 0.45 * FC                          # 全部載重／持續載重壓應力
LIM_EX, LIM_U = 1.6 * math.sqrt(FC), 2.0 * math.sqrt(FC)    # 考卷拉應力／現行 U 類上限
WL_EX, WL_U = (F_BOT0 + LIM_EX) / K_BOT, (F_BOT0 + LIM_U) / K_BOT
WL_TOP = (LIM_C - F_TOP0) / K_TOP


def fig3_wl():
    W, H = 1000, 640
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG}　梁中點纖維應力隨活載重 w_{{L}} 變化：五條限值各管什麼", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "讀法①（預力與全部載重皆以合成斷面計算）；壓為正、拉為負，kgf/cm²", 13, C["muted"])
    pl = Plot(cv, 110, 110, 600, 400, (0.0, 5.0), (-60.0, 240.0))
    pl.band(LIM_D, LIM_C, C["accent"], 0.10)
    pl.frame([0, 1, 2, 3, 4, 5], range(-60, 241, 60), "活載重 w_{L}（tf/m）", "纖維應力（kgf/cm²）")
    pl.hline(0, C["member2"], 1.4, None)
    pl.hline(LIM_C, C["load"], 2.0, "8 5")
    pl.hline(LIM_D, C["accent"], 2.2, "8 5")
    pl.hline(-LIM_EX, C["load"], 2.0, "8 5")
    pl.hline(-LIM_U, C["bmd"], 1.8, "3 4")
    w_end = min(5.0, (F_BOT0 + 60.0) / K_BOT)          # 梁底線畫到圖框下緣為止
    pl.curve([(0, F_BOT0), (w_end, F_BOT0 - K_BOT * w_end)], C["deform"], 3.4)
    pl.curve([(0, F_TOP0), (5, F_TOP0 + K_TOP * 5)], C["member2"], 3.0)
    pl.dot(0, F_BOT0, C["load"], 6.5)
    pl.vline(WL_EX, C["load"], 1.5, "4 4", -60, -LIM_EX); pl.dot(WL_EX, -LIM_EX, C["load"])
    pl.vline(WL_U, C["bmd"], 1.5, "4 4", -60, -LIM_U); pl.dot(WL_U, -LIM_U, C["bmd"])
    cv.text_px(pl.X(WL_EX) - 6, pl.Y(-60) - 12, f"{WL_EX:.2f}", 12.5, C["load"], "end", weight="700")
    cv.text_px(pl.X(WL_U) + 6, pl.Y(-60) - 12, f"{WL_U:.2f}", 12.5, C["bmd"], "start", weight="700")
    cv.text_px(pl.X(0.55), pl.Y(192), f"有效預力＋靜載重：梁底 {F_BOT0:.1f}", 12.5, C["load"], "start", weight="700")
    cv.text_px(pl.X(2.2), pl.Y(F_BOT0 - K_BOT * 2.2) - 16, "梁底", 13, C["deform"], "start", weight="700")
    cv.text_px(pl.X(4.2), pl.Y(F_TOP0 + K_TOP * 4.2) - 14, "梁頂", 13, C["member2"], "start", weight="700")
    xr = 728
    for y, col, name, desc in [(LIM_C, C["load"], f"0.60f'c = {LIM_C:.0f}", "全部載重壓應力（考卷值＝現行值）"),
                               (LIM_D, C["accent"], f"0.45f'c = {LIM_D:.1f}", "持續載重壓應力（考卷未給）"),
                               (-LIM_EX, C["load"], f"1.6√f'c = {LIM_EX:.2f}", f"考卷拉應力 → w = {WL_EX:.2f}（控制）"),
                               (-LIM_U, C["bmd"], f"2.0√f'c = {LIM_U:.2f}", f"現行 U 類上限 → w = {WL_U:.2f}（對照）")]:
        yy = pl.Y(y) + (-46 if y == -LIM_EX else 18 if y == -LIM_U else 0)   # 兩條拉應力線太近：一上一下
        cv.text_px(xr, yy - 9, name, 13, col, "start", weight="700")
        cv.text_px(xr, yy + 11, desc, 11.5, C["muted"], "start")
    cv.text_px(W / 2, H - 52, f"活載重前梁底就已壓到 {F_BOT0:.1f}，超過持續載重限值 {LIM_D:.1f}；活載重只會讓梁底壓應力變小，所以這項與 w_{{L}} 無關",
               13, C["load"], weight="700")
    cv.text_px(W / 2, H - 26, f"只看考卷的 0.6f'c（{LIM_C:.0f}）會以為梁底合格；梁頂到 w_{{L}} = {WL_TOP:.2f} 才達 0.6f'c，不控制", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-3-wl.svg")
    cv.save(path); save_png(path)
    return path

FIGURES = [(fig1_problem, "§1（題目正本 §4）", "62 cm 當成梁深、梁距當成淨距"),
           (fig2_problem, "§1（題目正本 §4）", "鋼腱端點偏心不為 0、跨中垂距取錯"),
           (fig3_wl, "§5 爭議點 4", "只看考卷 0.6f'c，漏了現行規範持續載重 0.45f'c；把 1.6√f'c 換成 U 類上限")]
if __name__ == "__main__":
    for f, _, _ in FIGURES:
        f()
    assert abs(F_BOT0-207.4)<0.05 and abs(K_BOT-63.70)<0.01 and round(WL_EX,2)==3.73 and round(WL_U,2)==3.84 and round(WL_TOP,2)==9.00, (F_BOT0,K_BOT,WL_EX,WL_U,WL_TOP)
    print(TAG, "OK")
