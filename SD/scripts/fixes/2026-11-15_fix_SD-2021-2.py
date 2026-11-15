#!/usr/bin/env python3
"""SD-2021-2 解析勘誤（2026-11-15，SD-U1-3 批 3 階段 C）：㈡ 改計入㈠的阻尼比 ξ=0.06。可重複執行。"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
if "x_{max} \\approx 5.68" in t: print("already"); sys.exit()
R = []
def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:60]); t = t.replace(old, new)

rep("| 最大位移 | 載重期間與結束後自由振動全程的最大值（判讀 #4） | 只看載重期間 |",
    "| 最大位移 | 載重期間與結束後自由振動全程的最大值（判讀 #4） | 只看載重期間 |\n"
    "| ㈡ 阻尼 | 計入㈠求得的 $\\xi=0.06$（題文「其阻尼比可由㈠計算得知」）：$x_{max}=5.68$ cm | 用無阻尼公式得 6.22 cm（本庫 2026-11-15 前的舊解） |")

rep("3. Duhamel 積分：強迫相 $(0 \\leq t \\leq t_d)$ 求端點 $x(t_d)$、$\\dot{x}(t_d)$\n"
    "4. 自由振動相 $(t > t_d)$ 求最大振幅 $\\sqrt{x(t_d)^2 + (\\dot{x}(t_d)/\\omega_0)^2}$",
    "3. 分段解（等同 Duhamel 積分）：強迫相 $(0 \\leq t \\leq t_d)$ 計入 $\\xi = 0.06$，求端點 $x(t_d)$、$\\dot{x}(t_d)$\n"
    "4. 自由振動相 $(t > t_d)$ 為有阻尼自由振動：由 $\\dot x = 0$ 求第一個波峰時刻與最大位移（無阻尼振幅只作對照）")

rep("**四大陷阱：**", "**五大陷阱：**")
rep("| 4 | 最大位移誤以為只在強迫相 | $t_d/T \\approx 0.16 < 0.5$：最大值通常在**自由振動相** |",
    "| 4 | 最大位移誤以為只在強迫相 | $t_d/T \\approx 0.16 < 0.5$：最大值通常在**自由振動相** |\n"
    "| 5 | 題目已給阻尼比（由㈠求得），㈡ 卻用無阻尼公式 | 計入 $\\xi = 0.06$：$5.68$ cm；無阻尼 $6.22$ cm 高估約 9%，只能當對照 |")

rep("$$\\text{Step 7（二）: 強迫相端點值} \\quad x(t_d) = \\frac{\\boxed{x_{st}}}{1-\\boxed{r}^2}[0 - r\\sin(\\omega_0 t_d)]$$",
    "$$\\text{Step 7（二）: 強迫相（計阻尼）} \\quad x(t) = e^{-\\xi\\omega_0 t}(A\\cos\\omega_D t + B\\sin\\omega_D t) + \\boxed{x_{st}}\\boxed{R_d}\\sin(\\Omega t - \\phi) \;\\Rightarrow\; x(t_d),\\ \\dot x(t_d)$$")
rep("$$\\text{Step 8（二）: 自由相振幅} \\quad X_{max} = \\sqrt{x(t_d)^2 + \\left(\\frac{\\dot{x}(t_d)}{\\omega_0}\\right)^2}$$",
    "$$\\text{Step 8（二）: 自由相（計阻尼）} \\quad x(\\tau) = e^{-\\xi\\omega_0 \\tau}\\left[\\boxed{x(t_d)}\\cos\\omega_D\\tau + \\frac{\\boxed{\\dot x(t_d)} + \\xi\\omega_0 x(t_d)}{\\omega_D}\\sin\\omega_D\\tau\\right],\\ \\dot x(\\tau_p) = 0 \\Rightarrow x_{max}$$")

rep("| $1-r^2$ | $1-\\pi^2 = -8.870$ | |\n| $x(t_d)$ | Duhamel 強迫相端點 | |\n| $\\dot{x}(t_d)$ | Duhamel 強迫相端點速度 | |\n| $X_{max}$ | $\\sqrt{x(t_d)^2 + (\\dot{x}(t_d)/\\omega_0)^2}$ | |",
    "| $\\omega_D$ | $\\omega_0\\sqrt{1-\\xi^2} = 9.982$ rad/sec | |\n"
    "| $R_d,\\ \\phi$ | 穩態放大 $0.1126$、相位角 $177.57^\\circ$（$r=\\pi$、$\\xi=0.06$） | |\n"
    "| $x(t_d)$ | 強迫相端點（計阻尼）$2.878$ cm | |\n"
    "| $\\dot{x}(t_d)$ | 強迫相端點速度 $0.5134$ m/s | |\n"
    "| $x_{max}$ | 自由相第一個波峰 $5.68$ cm（$t \\approx 0.202$ s）；無阻尼對照 $6.22$ cm | |")

# §4 Step 3–5 整段改寫
i0 = t.index("**Step 3：計算原理說明（Duhamel 積分兩階段法）**")
i1 = t.index("**備驗（衝擊近似法）：**")
new45 = r"""**Step 3：計算原理說明（Duhamel 積分兩階段法）**

> **原理：** 衝擊型載重的動力響應需分兩相計算，阻尼比用㈠求得的 $\xi = 0.06$（題文「其阻尼比可由㈠計算得知」）——
> - **強迫相** $0 \leq t \leq t_d$：有阻尼 SDOF 受 $p_0\sin\Omega t$、由靜止開始，解 = 穩態特解＋衰減齊次解（等同 Duhamel 積分 $x(t)=\frac{1}{m\omega_D}\int_0^t p(\tau)e^{-\xi\omega_0(t-\tau)}\sin[\omega_D(t-\tau)]\,d\tau$）
> - **自由振動相** $t > t_d$：以強迫相末端值 $x(t_d)$、$\dot{x}(t_d)$ 為初始條件的有阻尼自由振動，由 $\dot x = 0$ 找第一個波峰

**Step 4：強迫相 $(0 \leq t \leq t_d)$ 的響應（計阻尼）**

$$\omega_D = \omega_0\sqrt{1-\xi^2} = 10\sqrt{1-0.06^2} = 9.982 \text{ rad/sec}$$

穩態特解 $x_p = C\sin\Omega t + D\cos\Omega t$，其中 $r = \pi$：

$$C = x_{st}\frac{1-r^2}{(1-r^2)^2+(2\xi r)^2},\qquad D = -x_{st}\frac{2\xi r}{(1-r^2)^2+(2\xi r)^2}$$

$$(1-r^2)^2 + (2\xi r)^2 = 8.870^2 + 0.3770^2 = 78.81 \;\Rightarrow\; R_d = \frac{1}{\sqrt{78.81}} = 0.1126,\quad \phi = 177.57^\circ$$

齊次解 $e^{-\xi\omega_0 t}(A\cos\omega_D t + B\sin\omega_D t)$，由 $x(0)=0$、$\dot x(0)=0$：$A = -D$，$B = (\xi\omega_0 A - C\Omega)/\omega_D$。

代入 $t = t_d = 0.1$ sec（程式計算，見頁尾驗算腳本）：

$$x(t_d) = 0.02878 \text{ m} = 2.878 \text{ cm},\qquad \dot x(t_d) = 0.5134 \text{ m/sec}$$

強迫相內位移單調增加，最大即端點值 $2.878$ cm。

**Step 5：自由振動相 $(t > t_d)$ 的最大位移（計阻尼）**

令 $\tau = t - t_d$：

$$x(\tau) = e^{-\xi\omega_0\tau}\left[x(t_d)\cos\omega_D\tau + \frac{\dot x(t_d)+\xi\omega_0 x(t_d)}{\omega_D}\sin\omega_D\tau\right]$$

$\dot x(\tau_p) = 0$ 的第一個根：

$$\tan\omega_D\tau_p = \frac{B_f\omega_D - \xi\omega_0 A_f}{A_f\omega_D + \xi\omega_0 B_f},\quad A_f = x(t_d),\ B_f = \frac{\dot x(t_d)+\xi\omega_0 x(t_d)}{\omega_D}\;\Rightarrow\;\tau_p = 0.1016 \text{ s}\ (t \approx 0.202 \text{ s})$$

$$x_{max} = x(\tau_p) = 0.05677 \text{ m}$$

$$\boxed{x_{max} \approx 5.68 \text{ cm} \quad \text{（發生於自由振動相，} t \approx 0.202\text{ s；}R_d = x_{max}/x_{st} = 0.568\text{）}}$$

**對照：不計阻尼**（本庫舊解的算法）：

$$x_1(t) = \frac{x_{st}}{1-r^2}\left[\sin(\Omega t) - r\sin(\omega_0 t)\right],\quad x_1(t_d) = 2.98 \text{ cm},\ \dot x_1(t_d) = 0.5456 \text{ m/sec}$$

$$X_{max}^{(\xi=0)} = \sqrt{x_1(t_d)^2 + \left(\frac{\dot{x}_1(t_d)}{\omega_0}\right)^2} = \sqrt{0.02980^2 + 0.05456^2} = 0.0622 \text{ m} = 6.22 \text{ cm}$$

不計阻尼高估約 9%。題目明說阻尼比由㈠求得，要計入；6.22 cm 只能當上界對照。

驗算：分段閉合解、`solve_ivp` 數值積分、Duhamel 卷積三條路徑都得 $x_{max} = 5.677$ cm。

![SD-2021-2 圖二：上格為半正弦脈衝載重時程，下格為位移時程；計阻尼 ξ=0.06 的位移在 t_d=0.1 s 時為 2.88 cm，自由振動相第一個波峰 5.68 cm（t≈0.20 s），並以細虛線對照不計阻尼的 6.22 cm](figs/SD-2021-2-fig-2-pulse.svg)

*圖 2　載重與位移時程（ξ＝0.06）。強迫相在 $t_d$ 之前沒有極值，端點值 $2.88$ cm 只是自由相的初始條件；最大值 $5.68$ cm 發生在載重結束**之後**的第一個波峰。細虛線是不計阻尼的對照（$6.22$ cm），振幅不衰減、也比較大。*


"""
t = t[:i0] + new45 + t[i1:]

rep("兩法結果相近（6.37 ≈ 6.22 cm），衝擊近似略高（保守側）✓",
    "衝擊近似 6.37 cm 是不計阻尼的近似，與不計阻尼的精確值 6.22 cm 相近 ✓；計入 $\\xi = 0.06$ 後為 5.68 cm。")

rep("本題(二)以無阻尼公式計算，$\\xi = 6\\%$ 時精確解略小（阻尼耗能）。若含阻尼：強迫相使用 Duhamel 積分卷積積分 $x(t) = \\frac{1}{m\\omega_d}\\int_0^t p(\\tau)e^{-\\xi\\omega_0(t-\\tau)}\\sin[\\omega_d(t-\\tau)]d\\tau$，計算量大，**考場上以無阻尼答案加說明「阻尼使響應略小」即可。**",
    "題文明說「其阻尼比可由㈠計算得知」，表示㈡ 要用 $\\xi = 0.06$。計入阻尼得 $5.68$ cm，不計阻尼 $6.22$ cm，差約 9%——已超過一般認定「阻尼影響可忽略」的程度，因為最大值出現在 $t \\approx 0.2$ s，阻尼已作用將近三分之一個週期（$e^{-\\xi\\omega_0 \\cdot 0.2} = 0.887$）。"
    "考場上可用分段閉合解（Step 4、5）手算；若時間不夠，至少寫出不計阻尼值並說明「計入阻尼後約小 9%」，但主答案應是計阻尼的 5.68 cm。")

rep("| **0.159（本題）** | **自由振動相** | **0.621** | 與 §4 Step 5 之 6.22/10 相符 ✓ |",
    "| **0.159（本題）** | **自由振動相** | **0.621** | 與 §4 不計阻尼對照值 6.22/10 相符 ✓（計 $\\xi=0.06$ 為 0.568） |")
rep("本題 $t_d/T = 0.159$，故最大值在自由振動相，動力放大 $R_d = 6.22/10 = 0.622$ ✓",
    "本題 $t_d/T = 0.159$，故最大值在自由振動相；無阻尼震譜讀得 $R_d = 0.622$，計入 $\\xi = 0.06$ 後 $R_d = 5.68/10 = 0.568$ ✓（震譜表與圖三皆為無阻尼）")

t = t.rstrip("\n") + "\n\n*修正日期：2026-11-15（㈡ 最大位移改計入㈠求得的阻尼比 ξ＝0.06：6.22 cm → 5.68 cm，t≈0.202 s；原解以無阻尼公式計算，與題文「其阻尼比可由㈠計算得知」不符。改 §1 常見誤讀、§3 作戰計畫與陷阱、§3.5、§4 Step 3–5、圖二、§5 爭議點 1 與震譜表註；驗證：scripts/fixes/2026-11-15_verify_SD-2021-2.py 分段閉合解、solve_ivp、Duhamel 三路一致 MISMATCHES: 0）*\n"
p.write_text(t, encoding="utf-8"); print("fixed")
