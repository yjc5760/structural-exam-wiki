#!/usr/bin/env python3
"""SD-2013-2 解題圖解（struct-diagram；2026-11-16，SD-U3-1 組 U3-1-G1 階段 E）
fig-2：容量設計剪力包絡（兩個側移方向，柱面至柱面）與箍筋設計強度 φV_n，標出 2h 塑鉸區（V_c=0）。
數值由腳本依勘誤後 §4 重算（M_pr 實配鋼筋、w_u=1.2D+1.0L、ℓn=6.4 m）。用法：python3 gen_SD-2013-2.py [輸出目錄]。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2013-2"
fc, fy, b, d, ln, h2 = 280., 4200., 40., 53., 6.40, 1.20
def Mpr(n):                                      # 實配 D25 根數 → M_pr (tf·m)
    As = n*5.067; a = 1.25*As*fy/(0.85*fc*b); return As*1.25*fy*(d - a/2)/1e5
MA_N, MB_N, M_P = Mpr(5), Mpr(6), Mpr(3)         # 61.20、71.21、38.95
wu = 1.2*2.7 + 1.0*1.4
Veq1, Veq2 = (MA_N + M_P)/ln, (M_P + MB_N)/ln    # 15.65、17.21
def V1(x): return Veq1 + wu*(ln/2 - x)           # 側移 1：A 端最大
def V2(x): return Veq2 + wu*(x - ln/2)           # 側移 2：B 端最大
Av = 2*1.267; Vc = 0.53*math.sqrt(fc)*b*d/1000
PHI_HINGE = 0.75*Av*fy*d/12/1000                 # @12，V_c=0：35.25
PHI_MID = 0.75*(Vc + Av*fy*d/25/1000)            # @25，計 V_c：31.02
def fig2():
    cv = fit(900, 430, (-0.9, 7.4), (-0.9, 4.6), L=14, R=14, T=14, B=14)
    K = 0.1                                       # 縱軸比例：1 tf = 0.1 單位
    for y in (0, 10, 20, 30, 40):
        cv.line((0, K*y), (ln, K*y), C["border"], 1); cv.text((0, K*y), str(y), 11.5, C["muted"], "end", dx=-6)
    for x0 in (0, ln - h2): cv.polygon([(x0, 0), (x0 + h2, 0), (x0 + h2, K*42), (x0, K*42)], "rgba(180,83,9,0.08)", "none")
    xs = [ln*i/60 for i in range(61)]
    cv.poly([(x, K*V1(x)) for x in xs], C["sfd"], 1.6, dash="5 4"); cv.poly([(x, K*V2(x)) for x in xs], C["sfd"], 1.6, dash="5 4")
    cv.poly([(x, K*max(V1(x), V2(x))) for x in xs], C["sfd"], 2.8)
    cv.poly([(0, K*PHI_HINGE), (h2, K*PHI_HINGE), (h2, K*PHI_MID), (ln - h2, K*PHI_MID), (ln - h2, K*PHI_HINGE), (ln, K*PHI_HINGE)], C["bmd"], 2.4)
    cv.line((0, 0), (ln, 0), C["muted"], 1.6); cv.line((0, 0), (0, K*44), C["muted"], 1.6)
    cv.text((0, 0), "A 柱面", 12.5, C["text"], dy=16); cv.text((ln, 0), "B 柱面", 12.5, C["text"], dy=16)
    cv.text((ln, K*V2(ln)), f"V_e = {V2(ln):.2f}", 12.5, C["sfd"], "end", dx=-4, dy=42)
    cv.text((0, K*V1(0)), f"{V1(0):.2f}", 12, C["sfd"], "start", dx=6, dy=26)
    cv.dot((ln - h2, K*V2(ln - h2)), r=4, fill=C["accent"])
    cv.text((ln - h2, K*V2(ln - h2)), f"{V2(ln - h2):.2f}", 12, C["sfd"], "start", dx=8, dy=22)
    cv.text((h2/2, K*PHI_HINGE), f"φV_n = {PHI_HINGE:.2f}（@12，V_c=0）", 12, C["bmd"], "start", dx=-30, dy=-12)
    cv.text((ln/2, K*PHI_MID), f"φ(V_c+V_s) = {PHI_MID:.2f}（@25）", 12, C["bmd"], dy=-12)
    cv.text((h2/2, K*42), "2h = 1.2 m", 12, C["accent"]); cv.text((ln - h2/2, K*42), "2h = 1.2 m", 12, C["accent"])
    cv.text((ln/2, 0), "距 A 柱面 x（ℓn = 6.4 m）；剪力 tf；虛線為兩個側移方向，實線為包絡", 12, C["muted"], dy=36)
    return cv.save(f"{OUT}/{TAG}-fig-2-shear.svg")
FIGURES = [(fig2, "設計剪力在柱面最大 32.06 tf（不折減到 d 處）；2h 外取 2h 處 26.49 tf 並可計 V_c")]
if __name__ == "__main__":
    assert abs(V2(ln) - 32.06) < 0.01 and abs(V2(ln - h2) - 26.49) < 0.01 and abs(PHI_HINGE - 35.25) < 0.01 and abs(PHI_MID - 31.02) < 0.01
    for fn, c in FIGURES: print(fn(), "—", c)
