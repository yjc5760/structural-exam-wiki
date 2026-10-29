# 箱型柱（Box Column）

**概念 ID：** BOX-COLUMN
**知識分類：** Part 1.1 壓力桿件 / Part 1.3 梁柱桿件
**規範來源：** 鋼結構設計規範 / AISC 360 Chapter E, F, G

## 定義

**箱型柱（Box Column）** 是以四片鋼板圍合成閉口矩形截面的柱構件，命名格式：BOX B×D×t（寬×高×板厚，單位 mm）。與 I 形斷面（開口截面）相比，箱形截面具有：

- **雙軸對稱**：$I_x = I_y$（正方形箱）或接近，適合雙向受力
- **高扭轉剛度**：閉口截面扭轉常數 $J$ 遠大於開口截面
- **無 LTB 問題（充分支撐時）**：扭轉剛度大，側扭挫屈不易發生

## 斷面性質計算

以 **BOX B×D×t**（外邊長 B=D，板厚 t）為例：

### 面積
$$A = BD - (B-2t)(D-2t) = 4Bt - 4t^2 \approx 4Bt \quad \text{（t 遠小於 B 時）}$$

正方形箱（B = D）：
$$A = 4(B-t)t \approx 4Bt$$

### 慣性矩（對形心軸）
$$I_x = \frac{BD^3}{12} - \frac{(B-2t)(D-2t)^3}{12}$$

正方形：
$$I = \frac{B^4 - (B-2t)^4}{12}$$

### 塑性斷面模數 $Z$（正方形箱）

**方法：以半面積矩求 $Z$**

$$Z = \frac{B^3 - (B-2t)^3}{6}$$

推導過程：
$$Z = 2 \times \left[\text{上半} \times \bar{y}\right] = 2 \times \frac{A/2 \times \bar{y}_{上半}}{}$$

計算 $\bar{y}$（半截面形心到中性軸距離）：
$$\bar{y} = \frac{B^3/8 - (B-2t)^3/8}{A/2}$$

常見簡化：
$$Z \approx \frac{B^2 t}{2} \times 2 \quad \text{（若 t << B，翼板主導）}$$

### 彈性斷面模數
$$S = I / (B/2)$$

## 寬厚比（局部挫屈）

箱形柱板件的結實/非結實判斷（翼板受壓）：
$$\lambda_f = \frac{b}{t}，\quad b = B - 2t \quad \text{（清淨寬度，扣除角隅板厚）}$$

$$\lambda_p = \frac{50}{\sqrt{F_y[\text{tf/cm}^2]}} \quad \text{（LRFD，板件結實限值）}$$

> ⚠️ **b 的定義**：清淨寬度是 $B - 2t$（兩側各扣一個板厚），不是外邊長 $B$。

## 整體挫屈強度 $\phi_c P_n$

與 I 形柱相同，用 LRFD 柱強度公式（$\lambda_c$ → $F_{cr}$），但細長比計算用：
$$r = \sqrt{I/A} \quad \text{（閉口截面的 r 計算與 I 形相同）}$$

## 側扭挫屈（LTB）

**充分側向支撐**：$\phi_b M_n = \phi_b M_p = 0.9 F_y Z$，不需考慮 LTB。

**無充分支撐（罕見）**：閉口截面因扭轉剛度極高，LTB 很少控制設計（與開口 I 形差異顯著）。

## P-M 互制（雙軸彎矩）

箱形梁柱同樣使用 AISC H1-1 公式，但需計算雙軸方向 $M_x$、$M_y$：
$$\frac{P_u}{\phi_c P_n} + \frac{8}{9}\left(\frac{M_{ux}}{\phi_b M_{nx}} + \frac{M_{uy}}{\phi_b M_{ny}}\right) \leq 1.0 \quad \text{（當 Pu/φcPn ≥ 0.2）}$$

## 常見陷阱

1. **清淨寬度 b**：計算寬厚比時 $b = B - 2t$，考生常用 $b = B$ 而多算 $\lambda_f$。
2. **$Z$ 計算方式不同於 I 形**：不能套用 H 形斷面 $Z_x$ 公式，需重新以形心距計算。
3. **H1-1a vs. H1-1b 選擇**：先算 $P_u/\phi_c P_n$，與 0.2 比較決定公式。
4. **雙軸彎矩要同時帶入**：兩個方向的彎矩需求同時代入互制公式，不可只算一個方向。

## 相關概念

- [[COMPACT-SECTION]] — 箱形截面寬厚比判斷
- [[lrfd-column]] → `wiki/methods/lrfd-column.md` — 整體挫屈計算流程
- [[pm-interaction]] → `wiki/methods/pm-interaction.md` — P-M 互制計算
- [[BEAM-COLUMN-INTERACTION]] — 梁柱互制概念
- [[WEAK-AXIS-BEHAVIOR]] — 雙軸彎矩中的弱軸彎矩

## 出現題目

| 題號 | 考年 | 主分類 | 核心標籤 |
|------|------|--------|----------|
| [[SS-2007-2]] | 96 | 梁桿件 | 箱形斷面, Zx計算, 結實斷面 |
| [[SS-2009-2]] | 98 | 耐震設計 | 箱形柱, 節點域, Panel Zone |
| [[SS-2009-4]] | 98 | 接合設計 | 箱形斷面, 開槽銲 |
| [[SS-2022-1]] | 111 | 梁柱桿件 | BOX 800×800×32, 斷面性質, P-M互制, 雙軸 |
| [[SS-2024-4]] | 113 | 梁柱桿件 | 箱形柱, 局部挫屈 |
