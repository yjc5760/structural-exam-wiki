# -*- coding: utf-8 -*-
"""FIX SM-2015-3 §5 第 2 點：Peck (1943) 等值凝聚力原式分母應為 2H（舊文寫 H，得 39.72、N=3.45「判成堅硬黏土」為錯）。
正確：n'=0.75 → c̄=19.86、N=6.90，仍為軟～中等黏土，pa=57.55 kN/m²；主答（n'=1.0 等值式）41.1 kN/m²、FS 1.50 不變。
在 SM/ 下執行；可重複執行。"""
import math
p = "raw/solutions/SM-2015-3/SM-2015-3.md"
t = open(p, encoding="utf-8").read()
if "FIX：Peck 等值凝聚力分母 2H" in t:
    raise SystemExit("already fixed")
def W(p, s):
    with open(p, "r+b") as f:
        f.seek(0); f.write(s.encode("utf-8")); f.truncate()
def R(t, a, b):
    assert t.count(a) == 1, (a[:60], t.count(a)); return t.replace(a, b)
ts = 16.5*9*math.tan(math.radians(32))
c1 = (0.5*ts + 30*5)/8; c75 = (ts + 5*0.75*60)/16; pa75 = max(137 - 4*c75, 0.3*137)
chk = {"sand": (ts, 92.80), "c1": (c1, 24.55), "c75": (c75, 19.86), "N75": (137/c75, 6.90), "pa75": (pa75, 57.55),
       "P75": (0.5*2*pa75 + 6*pa75, 402.85), "Nbot": (137/30, 4.57)}
mm = [k for k, (a, b) in chk.items() if abs(a-b) > 0.006*max(1, b)]
print("MISMATCHES:", len(mm), mm); assert not mm
i = t.index("2. **等值凝聚力 $\\bar{C_u}$ 的兩種公式版本"); j = t.index("3. **$m$ 係數")
t = t[:i] + r"""2. **等值凝聚力 $\bar{C_u}$ 與 Peck 的 $n'$（2026-11-15 勘誤本段）**：
   本解析的形式
   $$\bar{C_u} = \frac{1}{H}\left[\tfrac{1}{2}\gamma_s K_s H_s^2 \tan\phi_s + C_u(H - H_s)\right] = 24.55 \text{ kN/m}^2$$
   與 Peck (1943) 原式
   $$\bar{C_u} = \frac{1}{2H}\left[\gamma_s K_s H_s^2 \tan\phi_s + (H-H_s)\,n' q_u\right]$$
   是**同一條式子取 $n' = 1.0$**（$q_u = 2C_u$）。Das 等教科書建議 $n' = 0.5 \sim 1.0$、常用 $0.75$：
   $\bar{C_u} = (92.80 + 225)/16 = 19.86 \text{ kN/m}^2$、$N = 137/19.86 = 6.90 > 4$，**仍是軟弱至中度黏土**，
   $p_a = \max(137 - 79.45,\ 41.1) = 57.55 \text{ kN/m}^2$（不再由 $0.3\bar{\gamma}H$ 控制），總推力 $402.85 \text{ kN/m}$，比本解大 40%。
   （本段 2026-11-15 前把原式的分母誤寫成 $H$，得 $\bar{C_u} = 39.72$、$N = 3.45$ 而稱「會判成堅硬黏土」，該說法錯誤，已刪。）
   第三種判法直接用坑底黏土的 $C_u = 30$：$N = 137/30 = 4.57 > 4$，同樣是軟弱至中度。
   三種判法都指向軟弱至中度黏土的形狀；$p_a$ 則介於 $41.1$（$n'=1.0$，本解）與 $57.55 \text{ kN/m}^2$（$n'=0.75$），作答時務必寫出所用公式、$K_s$ 與 $n'$。

""" + t[j:]
t = t.rstrip("\n") + "\n\n*修正日期：2026-11-15（FIX：Peck 等值凝聚力分母 2H：§5 第 2 點更正 Peck (1943) 原式（分母 2H），刪除「Das 式 N = 3.45 判成堅硬黏土」的錯誤說法，補 $n'=0.75$ 時 $p_a = 57.55$ kN/m²；主答 41.1 kN/m²、FS 1.50 不變；依 `wiki/queries/盲解比對-SM-U2-3-B1-2026-11-15.md`；腳本 `scripts/fixes/2026-11-15_fix_SM-2015-3_peck_formula.py`）*\n"
W(p, t); print("ok", p)
