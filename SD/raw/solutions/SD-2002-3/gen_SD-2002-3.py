#!/usr/bin/env python3
"""SD-2002-3 解題圖解（struct-diagram；2026-11-16，X-G1 階段 E）
fig-3-weights：㈢ 施加 2w(x) 時三種算法得到的週期比（以均質簡支梁示例數值積分；比值與結構無關，線彈性下恆成立）。
攔下的錯誤：舊解把「施加載重 2w」讀成「自重加倍」，答 T′＝√2T；直接代原式也會得到 √2T，但真實週期不變。
用法：python3 gen_SD-2002-3.py [輸出目錄]；再跑 struct-diagram 的 render.py 產 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
sys.path.insert(1, os.environ.get("STRUCT_DIAGRAM_SCRIPTS") or os.path.join(_HERE, "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
from structdraw import C
from recipes import bar_compare
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2002-3"

def integ(f, n=2000):                      # Simpson 積分 [0,1]
    h = 1/n; s = f(0) + f(1)
    for i in range(1, n): s += (4 if i % 2 else 2)*f(i*h)
    return s*h/3
w, g = 1.0, 9.81                           # 示例：均質簡支梁，w、EI、L 取 1
u = lambda x, p: p*(x**4 - 2*x**3 + x)/24
T = lambda num, den: 2*math.pi*math.sqrt(num/(g*den))
T0 = T(integ(lambda x: w*u(x, w)**2), integ(lambda x: w*u(x, w)))                  # 施加 w
T_naive = T(integ(lambda x: w*u(x, 2*w)**2), integ(lambda x: w*u(x, 2*w)))         # 施加 2w，權重仍寫 w
T_fix = T(integ(lambda x: w*u(x, 2*w)**2), integ(lambda x: 2*w*u(x, 2*w)))         # β 權重改用施加力 2w
T_mass2 = T(integ(lambda x: 2*w*u(x, 2*w)**2), integ(lambda x: 2*w*u(x, 2*w)))     # 舊解：2w 同時當質量與力
cases = [("施加 w（原式）", "γ＝∫w u²dx、β＝∫w u dx", T0/T0, f"{T0/T0:.3f}·T", C["deform"]),
         ("直接代原式（錯）", "u′＝2u，權重仍寫 w", T_naive/T0, f"{T_naive/T0:.3f}·T", C["load"]),
         ("修正後（週期不變）", "β 改用施加力 p＝2w", T_fix/T0, f"{T_fix/T0:.3f}·T", C["bmd"]),
         ("舊解（答非所問）", "當成自重加倍：質量也加倍", T_mass2/T0, f"{T_mass2/T0:.3f}·T", C["member2"])]
def fig3():
    p = f"{OUT}/{TAG}-fig-3-weights.svg"
    bar_compare(cases, title="㈢ 施加載重改為 2w(x)、質量不變：公式需要修正", sub="長條長度＝週期相對值（最大者為 100%）；週期與施加力大小無關，位能要用施加力做的功",
                note="數值以均質簡支梁數值積分（Simpson）示例；比值 √2 與 1 對任何線彈性結構成立", path=p)
    return p
FIGURES = [(fig3, "施加 2w 直接代原式高估 √2；修正後週期不變")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
