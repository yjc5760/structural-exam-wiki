# ASD 梁容許彎曲應力 Fb 推導

**Code-Ref ID：** asd-beam-fb-derivation
**對應方法頁：** [[asd-beam]]（`wiki/methods/asd-beam.md`）
**相關概念：** [[LATERAL-TORSIONAL-BUCKLING]] [[BENDING-MODIFICATION-FACTOR-CB]]

---

## 一、公式全覽

ASD（AISC ASD 9th Edition）梁容許彎曲應力 $F_b$ 依受壓翼板側向支撐間距 $L$ 分三段：

### 緊密撐（$L \leq L_c$）

$$\boxed{F_b = 0.66 F_y}$$

### 中等細長（非彈性 LTB，AISC ASD **F1-6**）

適用範圍 $\sqrt{\dfrac{102{,}000\,C_b}{F_y}} \le \dfrac{L}{r_T} \le \sqrt{\dfrac{510{,}000\,C_b}{F_y}}$：

$$\boxed{F_b = \left[\frac{2}{3} - \frac{F_y(L/r_T)^2}{1{,}530{,}000\,C_b}\right] F_y \le 0.60F_y}\qquad(\text{ksi})$$

> $C_b$ 已在括號內，**不要再乘一次外層 $C_b$**。

### 彈性 LTB（**F1-7**，$L/r_T > \sqrt{510{,}000C_b/F_y}$）

$$\boxed{F_b = \frac{170\,000\,C_b}{(L/r_T)^2}}\qquad(\text{ksi})$$

> ✅ **兩式接軌驗算**：在分界點 $L/r_T = \sqrt{510{,}000C_b/F_y}$ 上，F1-6 與 F1-7 必須給出相同的 $F_b$；
> 在下界 $\sqrt{102{,}000C_b/F_y}$ 上，F1-6 必須剛好給出 $0.60F_y$。
> （$F_y = 36$ ksi、$C_b = 1$：分界 $L/r_T = 53.2 \sim 119.0$，下界 $F_b = 21.6 = 0.6F_y$ ✓，
> 分界點兩式皆得 $12.0$ ksi ✓）**抄錯係數時這個檢查會立刻抓到。**

### ⚠️ 另一條容易被混進來的公式（不是 LTB）

$$F_b = \left[0.79 - 0.002\,\frac{b_f}{2t_f}\sqrt{F_y}\right]F_y \qquad(\text{ksi，AISC ASD F1-3})$$

這條是**翼板局部挫屈（FLB）** 的非結實過渡公式，變數是<b>寬厚比 $b_f/2t_f$</b>，
與 $L/r_T$（LTB）無關。兩者是不同的失敗模式，**不可互相取代，也不參與「取較大值」**。

---

## 二、分界點定義

### $L_c$（緊密撐上限）

$$L_c = \min\left(\frac{76\,b_f}{\sqrt{F_y}},\ \frac{20{,}000}{(d/A_f)F_y}\right) \qquad (\text{in、ksi 制})$$

三種單位制的等價係數：

| 單位制 | 第一式 | 第二式 |
|--------|--------|--------|
| in、ksi | $76\,b_f/\sqrt{F_y}$ | $20{,}000/((d/A_f)F_y)$ |
| cm、tf/cm² | $20\,b_f/\sqrt{F_y}$ | $1{,}406/((d/A_f)F_y)$ |
| mm、MPa | $200\,b_f/\sqrt{F_y}$ | $137{,}900/((d/A_f)F_y)$ |

- $b_f$：受壓翼板寬度
- $d/A_f$：梁深除以受壓翼板面積
- ⚠️ 第一式分母是 $\sqrt{F_y}$ **不是** $F_y$；第二式分母才是 $F_y$。兩式的 $F_y$ 次方不同，抄的時候特別容易混。

物理意義：$L \leq L_c$ 時，側向扭轉挫屈不控制，梁可達塑性強度 $F_b = 0.66F_y$。

### $L_u$（彈性 LTB 起始點）

$L_u$ 定義為「非彈性 LTB 與彈性 LTB 的分界」，即：

非彈性段上限公式 = 彈性段公式，解出 $L/r_T$。

---

## 三、各段推導邏輯

### 段 1：$F_b = 0.66 F_y$（緊密撐）

- 梁有充分側向支撐，不發生 LTB
- $M_n = M_p = Z_x F_y$（塑性彎矩）
- ASD 安全係數 $FS = 5/3 \approx 1.67$（全規範統一值，不是由 0.66 反推的）
- $F_b = \dfrac{M_p}{S_x \cdot FS} = \dfrac{Z_x}{S_x}\cdot\dfrac{F_y}{1.67}$
- 對 I 型鋼 $Z_x/S_x \approx 1.12$：$F_b = \dfrac{1.12}{1.67}F_y = 0.67F_y \approx \mathbf{0.66F_y}$ ✓

> 💡 **0.66 與 0.60 的關係就是形狀因子**：
> $0.60F_y = F_y/1.67$ 是把「初始降伏 $M_y$」除以 FS；$0.66F_y$ 是把「塑性彎矩 $M_p$」除以同一個 FS。
> 兩者比值 $0.66/0.60 = 1.10 \approx Z_x/S_x$。這是「為何 ASD 有兩個係數」的標準答法。

### 段 2：非彈性 LTB 段（線性內插）

彈性 LTB 臨界應力（Timoshenko & Gere）：

$$F_{cr} = \frac{\pi}{L/r_T}\sqrt{\frac{E^2 C_b^2}{(L/r_T)^2} + \text{GJ 項}}$$

規範簡化為二次拋物線形式（非彈性段）：

$$F_b = \left[\frac{2F_y}{3} - \frac{F_y^2(L/r_T)^2}{1{,}530{,}000\,C_b}\right] \leq 0.60F_y \qquad(\text{ksi})$$

此拋物線在 $L/r_T \to 0$ 時給出 $F_b = \frac23 F_y$（與緊密撐段 $0.66F_y$ 接續），
在 $L/r_T = L_u/r_T = \sqrt{510{,}000C_b/F_y}$ 時與彈性段 F1-7 精確接續。

> ⚠️ **注意 1：** $C_b$ 只出現在分母括號內，**外面不要再乘一次**。
>
> ⚠️ **注意 2：** 取**較大值**的是「$L/r_T$ 家族（F1-6/F1-7）」與「$L\,d/A_f$ 式（F1-8）」這兩者，
> 不是非彈性段內部的兩條式子。理由：前者只計翹曲扭轉、後者只計純扭轉，**都是保守下界**，
> 真實梁兩種勁度都有，故取大仍保守。
> （對照：不同<b>失敗模式</b>之間才是取小。）

### 段 3：彈性 LTB 段

純 Euler 型挫屈，忽略 GJ 貢獻（細長梁假設 $J \to 0$）：

$$F_{cr} = \frac{\pi^2 E C_b}{(L/r_T)^2} \times \frac{1}{\pi} \times \text{調整} \approx \frac{170\,000\,C_b}{(L/r_T)^2} \text{ (ksi)}$$

ASD 彈性 LTB 無額外安全係數（已含在係數 170,000 中），等效 FS ≈ 1.67。

---

## 四、$r_T$ 的物理意義

$$r_T = \sqrt{\frac{I_{yr}}{A_r}}$$

- $I_{yr}$：受壓翼板 + 腹板受壓部分 1/3 對 y 軸的慣性矩
- $A_r$：同上截面積

物理意義：$r_T$ 是「等效側向迴轉半徑」，代表梁受壓側對側向挫屈的抵抗能力。寬翼板 → $r_T$ 大 → $L/r_T$ 小 → 較不易 LTB。

---

## 五、$C_b$ 的 ASD 定義

ASD 9th Edition 採用：

$$C_b = \frac{12.5 M_{max}}{2.5 M_{max} + 3 M_A + 4 M_B + 3 M_C}$$

（與 LRFD 相同，見 [[BENDING-MODIFICATION-FACTOR-CB]]）

- 均布荷重梁：$C_b \approx 1.14$
- 懸臂梁（自由端無束制）：$C_b = 1.0$（保守值）
- 純彎曲：$C_b = 1.0$

---

## 六、ASD 與 LRFD 對照

| 項目 | ASD（9th Ed.） | LRFD（360-10） |
|------|--------------|--------------|
| 全側撐 | $F_b = 0.66 F_y$ | $\phi_b M_n = 0.9 M_p$（Mn = Mp） |
| 分界長度 | $L_c$、$L_u$ | $L_p$、$L_r$ |
| 非彈性段 | 拋物線近似 | 線性內插（$M_p \to M_r$） |
| 彈性段 | $170000 C_b/(L/r_T)^2$ | $\phi_b C_b M_{cr}$（含 $S_{xc}$ 等效） |
| 修正係數 | $C_b$（相同公式） | $C_b$（相同） |
| 安全係數 | 隱含在係數中 | 顯式 $\phi_b = 0.90$ |

---

## 七、常見考題應用

| 題型 | 關鍵步驟 |
|------|---------|
| 計算容許彎矩 | ① 算 $L/r_T$ → ② 比較 $L_c$、$L_u$ → ③ 選公式算 $F_b$ → ④ $M_a = F_b S_x$ |
| $C_b$ 應用 | 算各段端點彎矩 M_A, M_B, M_C → 代入公式 |
| ASD vs LRFD 比較 | $F_b \approx \phi_b F_{cr} / 1.5$（近似等效） |

---

## 相關頁面

- [[asd-column]] — ASD 柱設計（與本頁構成 ASD 完整設計對）
- [[ltb-3zone]] — LRFD 三段式 LTB 計算流程
- [[LATERAL-TORSIONAL-BUCKLING]] — LTB 基礎理論
- [[BENDING-MODIFICATION-FACTOR-CB]] — Cb 因子推導
- [[lrfd-phi-values]] — LRFD/ASD 哲學比較
