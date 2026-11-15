# 有效慣性矩撓度計算法

**方法 ID：** effective-inertia-deflection
**知識分類：** 解題工具
**適用題型：** RC-U3-1 梁工作性要求（撓度）
**適用規範：** 建築物混凝土結構設計規範 2023（同 ACI 318-19）§24.2.3–24.2.4：表 24.2.3.5 有效慣性矩（$\frac23M_{cr}$ 式）；Branson 式為舊規範，僅作對照

---

## 核心原理

RC 梁受力後部分開裂，有效慣性矩 $I_e$ 介於全斷面（未開裂）$I_g$ 與全開裂斷面 $I_{cr}$ 之間，依荷載彎矩 $M_a$ 與開裂彎矩 $M_{cr}$ 的比值插值，反映梁實際的撓曲剛度。現行規範（ACI 318-19 起）採 Bischoff 形式並以 $\frac23M_{cr}$ 計（考慮收縮約束使實際開裂提早）；舊規範 Branson 三次方式在低配筋時高估剛度。

---

## 邊界條件

- $I_e \leq I_g$（不可超過全斷面慣性矩）
- 現行式：若 $M_a \leq \frac23M_{cr}$，取 $I_e = I_g$（舊 Branson 式門檻為 $M_{cr}$）
- 長期撓度：須乘以長期修正係數

---

## 步驟流程

**Step 1：開裂彎矩**

$$M_{cr} = \frac{f_r I_g}{y_t}, \quad f_r = 2\sqrt{f'_c} \text{ (kgf/cm}^2\text{)} \;=\; 0.623\sqrt{f'_c} \text{ (MPa)}$$

> ⚠️ MPa 制係數是 **0.623**（＝ ACI 318-19 的 $0.62\lambda\sqrt{f'_c}$），不是 0.7。
> 0.7 是 ACI 318-99 舊版值，與 kgf/cm² 制的 2.0 不相容（差 12%）。
> 驗算：$2.0\sqrt{f'_c}$ 以 $f'_c$ 用 kgf/cm² 換算後即得 $0.626\sqrt{f'_c}$ (MPa)。見 RC-2018-4。

**Step 2：開裂斷面慣性矩 $I_{cr}$**

設中性軸深度 $kd$（單筋梁，忽略受拉混凝土）：

$$\frac{b(kd)^2}{2} = n A_s(d - kd), \quad n = \frac{E_s}{E_c}$$

$$I_{cr} = \frac{b(kd)^3}{3} + n A_s(d - kd)^2$$

（雙筋梁另加壓力筋慣性矩項：$(2n-1)A'_s(kd-d')^2$）

**Step 3：有效慣性矩（現行規範表 24.2.3.5）**

$$I_e = \frac{I_{cr}}{1-\left(\dfrac{(2/3)M_{cr}}{M_a}\right)^2\left(1-\dfrac{I_{cr}}{I_g}\right)} \leq I_g\qquad(M_a>\tfrac23M_{cr})$$

> 對照（舊規範 Branson）：$I_e = \left(\frac{M_{cr}}{M_a}\right)^3 I_g + \left[1 - \left(\frac{M_{cr}}{M_a}\right)^3\right] I_{cr} \leq I_g$。
> 驗算（RC-2006-3，$I_g$＝312,500、$I_{cr}$＝173,923、$M_{cr}$＝4.183 tf·m）：$M_a$＝6.40 → 現行 189,914／Branson 212,623；$M_a$＝16.40 → 176,182／176,223（深度開裂時兩式趨近 $I_{cr}$）。
> 連續梁取正、負彎矩斷面 $I_e$ 平均；懸臂梁取支承斷面。

**Step 4：即時撓度（每個載重水準各自計算）**

$$\Delta_i = \frac{K M_a L^2}{E_c I_e}$$

> ⚠️ 某一部分載重（如活載重、持續活載重）造成的即時撓度要用**差值法**：$\Delta_{L}=\Delta_{D+L}-\Delta_D$，兩項各用自己載重水準的 $I_e$。不可把該部分載重單獨配上某一 $I_e$ 計算（直接法），因為 $I_e$ 下降時既有載重的撓度也增加（RC-2007-2 直接法低估約 7%）。

其中係數 $K$：均佈載重簡支梁 $K = 5/48$；均佈載重懸臂梁 $K = 1/8$；集中載重中點 $K = 1/12$。

**Step 5：長期（附加）撓度**

$$\Delta_{add} = \lambda_\Delta \cdot \Delta_{i,sus}, \quad \lambda_\Delta = \frac{\xi}{1 + 50\rho'}$$

$\Delta_{i,sus}$＝持續載重（靜載重＋持續活載重）水準的總即時撓度。

| 時間 | $\xi$ |
|------|:-----:|
| ≥ 5 年 | 2.0 |
| 1 年 | 1.4 |
| 6 個月 | 1.2 |
| 3 個月 | 1.0 |

**Step 6：總撓度**

$$\Delta_{total} = \Delta_{i,D+L} + \lambda_\Delta\,\Delta_{i,sus}$$

（等價：$\Delta_{i,sus}(1+\lambda_\Delta) + (\Delta_{i,D+L}-\Delta_{i,sus})$。驗算 RC-2007-2：$\Delta_{i,D+L}$＝1.339、$\Delta_{i,sus}$＝0.460、$\lambda_\Delta$＝1.094 → 1.84 cm，兩種寫法相同。）

---

## 常見陷阱

- $I_{cr}$ 計算時雙筋梁需加壓力筋項（係數 $(2n-1)$ 而非 $n$，因混凝土已計算過）
- 長期修正 $\lambda_\Delta$ 只乘持續載重（靜載重＋持續活載重）的即時撓度，非持續活載重只取即時撓度
- $\rho'$ 取壓力筋比（懸臂、簡支取支承／跨中斷面）；無壓力筋時 $\rho' = 0 \Rightarrow \lambda_\Delta = \xi$
- 現行式：$M_a \le \frac23M_{cr}$ 才用 $I_g$；$\frac23M_{cr}<M_a<M_{cr}$ 時 $I_e$ 已折減（RC-2007-2 靜載重水準）
- 部分載重的撓度用差值法（見 Step 4）
- 尺寸鏈先讀清楚：延伸線對齊鋼筋中心時，全深要加上下段（RC-2006-3、RC-2008-1）

---

## 出現題目（使用本方法的考題，依 question_index 標籤核實）

| 題號 | 核心應用 |
|------|---------|
| [RC-2006-3](../problems/RC-2006-3.md) | 簡支梁集中活載重，即時撓度增量 |
| [RC-2007-2](../problems/RC-2007-2.md) | 雙筋梁即時＋長期撓度，λ 修正 |
| [RC-2008-1](../problems/RC-2008-1.md) | 懸臂雙筋梁長期撓度，轉換斷面法 |
| [RC-2009-2](../problems/RC-2009-2.md) | 懸臂梁 $I_{cr}$、曲率積分、雙段 EI 法 |
| [RC-2014-2](../problems/RC-2014-2.md) | 彎矩曲率三階段分析，開裂彎矩 |

*修正日期：2026-11-15（FIX-RC-U3-B1：主式改現行規範表 24.2.3.5（$\frac23M_{cr}$ 式），Branson 降為對照；Step 4–6 改差值法與 $\Delta_{i,D+L}+\lambda_\Delta\Delta_{i,sus}$；驗算見 RC-2006-3、RC-2007-2 勘誤腳本）*
