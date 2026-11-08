# 穩定失敗模式

> **核心問題：** 構材在應力尚未達 Fy 的情況下，因幾何構形突變而喪失承載能力。

---

## 穩定失敗的本質

穩定失敗 ≠ 強度失敗：
- **強度失敗**：材料應力超限
- **穩定失敗**：幾何平衡狀態突變（分歧點不穩定）

```
彈性 Euler 挫屈：
  P = P_cr → 柱突然側移（無預警）
  此時 σ = P_cr/A << Fy（材料仍在彈性範圍）
```

**非彈性挫屈**：部分斷面已降伏，但整體幾何失穩。

---

## 四種穩定失敗型式

| 型式 | 英文 | 作用構件 | 觸發參數 |
|------|------|---------|---------|
| **整體挫屈** | Global Buckling | 壓力桿件 | KL/r（細長比） |
| **側向扭轉挫屈** | Lateral-Torsional Buckling (LTB) | 梁 | Lb（側撐間距） |
| **局部挫屈** | Local Buckling | 板件 | b/t（寬厚比） |
| **扭轉挫屈** | Torsional / Flexural-Torsional Buckling | 開口薄壁柱 | λ（扭轉細長比） |

---

## 1. 整體挫屈（Global Buckling）

### 觸發條件

**彈性挫屈**（$\lambda_c > 1.5$）：

$$F_{cr} = \frac{0.877}{\lambda_c^2} F_y, \quad \lambda_c = \frac{KL}{\pi r} \sqrt{\frac{F_y}{E}}$$

**非彈性挫屈**（$\lambda_c \leq 1.5$）：

$$F_{cr} = 0.658^{\lambda_c^2} F_y$$

### 有效長度 K 值

| 邊界條件 | 理論 K | 設計用 K |
|---------|--------|---------|
| 兩端鉸支 | 1.0 | 1.0 |
| 一端固定，一端自由 | 2.0 | 2.1 |
| 兩端固定 | 0.5 | 0.65 |
| 一端固定，一端鉸支 | 0.7 | 0.80 |
| 有側移框架（一般） | — | 由對位圖查取 |

### 相關考點

- [[EULER-BUCKLING]] [[EULER-BUCKLING]]
- Method: [[lrfd-column]] [[asd-column]] [[effective-length-chart]]
- 歷屆題目：SS-2002-1, SS-2013-2, SS-2015-3, SS-2022-2

---

## 2. 側向扭轉挫屈（LTB）

### 觸發條件

梁在受彎時，壓力翼板側向位移 + 梁整體扭轉 → 喪失彎曲承載力。

### 三區段判斷

| 區段 | 條件 | Mn 計算 |
|------|------|---------|
| 塑性區 | $L_b \leq L_p$ | $M_n = M_p = F_y Z_x$ |
| 非彈性 LTB | $L_p < L_b \leq L_r$ | 線性內插 |
| 彈性 LTB | $L_b > L_r$ | $M_n = F_{cr} S_x \leq M_p$ |

$$L_p = 1.76 r_y \sqrt{\frac{E}{F_y}}, \quad L_r = 1.95 r_{ts} \frac{E}{0.7F_y} \sqrt{\frac{J}{S_x h_o} + \sqrt{\left(\frac{J}{S_x h_o}\right)^2 + 6.76\left(\frac{0.7F_y}{E}\right)^2}}$$

### 影響 LTB 的因素

- **Cb（彎矩梯度係數）**：$C_b > 1$ 時 Mn 可乘以 Cb（不超過 Mp）
- **側撐間距 Lb**：越短越好
- **斷面特性**：Iy 越大、J 越大，LTB 抵抗力越強

### 相關考點

- [[LATERAL-TORSIONAL-BUCKLING]] [[LATERAL-TORSIONAL-BUCKLING]]
- Method: [[ltb-3zone]]
- 歷屆題目：SS-2006-1, SS-2010-3, SS-2015-1, SS-2016-3, SS-2022-3

---

## 3. 局部挫屈（Local Buckling）

### 觸發條件

翼板或腹板寬厚比超過緊湊性限制，板件在應力達 Fy 前先行挫屈。

### 緊湊性分類（LRFD）

| 板件 | 結實（λ ≤ λp） | 非結實（λp < λ ≤ λr） | 細長（λ > λr） |
|------|------------|------------------|--------------|
| 翼板 | $b/t \leq 0.38\sqrt{E/F_y}$ | 至 $\sqrt{E/F_y}$ | 超過 |
| 腹板（彎曲） | $h/t_w \leq 3.76\sqrt{E/F_y}$ | 至 $5.70\sqrt{E/F_y}$ | 超過 |

### 局部挫屈的設計影響

- **結實斷面**：可發展全塑 Mp
- **非結實斷面**：Mp 到 My 之間線性折減
- **細長斷面**：彈性挫屈控制，強度低於 My

### 與 LTB 的互制

```
若 Lb 在塑性區 → 局部挫屈可能成為控制因素
若 Lb 在彈性 LTB 區 → LTB 控制，局部挫屈自動滿足
```

### 相關考點

- [[COMPACT-SECTION]]
- 歷屆題目：SS-2015-1, SS-2016-3, SS-2023-3

---

## 4. 扭轉挫屈（Torsional Buckling）

### 適用構件

開口薄壁斷面（角鋼、T形鋼、單板）：
- 扭轉剛度低 → 在細長比不高時仍可能扭轉挫屈
- 雙軸對稱 H 型鋼通常不控制

### AISC 公式框架

對於**單軸對稱或不對稱斷面**：

$$\lambda_{ez} = \frac{\pi^2 E C_w}{(KL)^2} + GJ$$

取彎曲挫屈與扭轉挫屈的較小值。

### 考試出現頻率

扭轉挫屈在台灣技師考試中較少單獨出題，但概念題可能要求：
- 說明何種斷面需考慮扭轉挫屈
- 為何 H 型鋼通常以彎曲挫屈控制

---

## 穩定失敗的設計策略

```
整體挫屈：
  → 選用 r 大的斷面（H 型鋼優於方管）
  → 加中間支撐（降低 KL）

LTB：
  → 加側撐（降低 Lb）
  → 選用 Iy, J 大的斷面
  → 利用 Cb 折減（均勻彎矩最保守）

局部挫屈：
  → 選用結實斷面（滿足 λ ≤ λp）
  → 加勁肋（腹板）

扭轉挫屈：
  → 避免使用單板或角鋼承受壓力
  → 開口斷面加閉合補強
```

---

## 相關頁面

- [[strength-failure]] — 應力超限的強度失敗
- [[connection-failure]] — 接合區穩定問題（承壓、撐開）
- Concepts: [[EULER-BUCKLING]] [[LATERAL-TORSIONAL-BUCKLING]] [[COMPACT-SECTION]] [[EULER-BUCKLING]]
- Methods: [[ltb-3zone]] [[lrfd-column]] [[asd-column]] [[effective-length-chart]]
