# 弱軸彎曲與弱軸挫屈

**概念 ID：** WEAK-AXIS-BEHAVIOR
**知識分類：** Part 1.1 壓力桿件 / Part 1.2 撓曲桿件 / Part 1.3 梁柱桿件
**規範來源：** 鋼結構設計規範 / AISC 360 Chapter F, E

## 定義

I 形斷面有兩個主軸：
- **強軸（Strong Axis，x 軸）**：$I_x$ 大，承彎能力強
- **弱軸（Weak Axis，y 軸）**：$I_y$ 小，承彎能力弱，且無 LTB 問題

對於梁柱構件，弱軸往往控制：
1. **弱軸挫屈（Weak-axis Flexural Buckling）**：柱的 $KL/r_y$ 常大於 $KL/r_x$，弱軸細長比控制設計
2. **弱軸彎曲（Weak-axis Bending）**：梁或梁柱承受 y 方向彎矩

## 弱軸挫屈

**設計細長比取兩軸最大值：**
$$\left(\frac{KL}{r}\right)_{\max} = \max\left[\frac{K_x L_x}{r_x},\ \frac{K_y L_y}{r_y}\right]$$

對 I 形斷面（寬翼型），典型比值：$r_x/r_y \approx 1.7 \sim 2.5$

**常見情境：**
- 弱軸有側向束制（支撐點）：$K_y L_y$ 因 $L_y$ 縮短，可能不再控制
- 無側向支撐：弱軸長細比往往遠大於強軸，成為挫屈控制軸

> ⚠️ **設計原則**：永遠比較兩軸 $KL/r$，不假設哪軸一定控制。

## 弱軸彎曲（I 形梁）

弱軸彎矩 $M_y$（繞 y 軸）的設計：

**結實斷面（翼板寬厚比滿足 $\lambda \leq \lambda_p$）：**
$$\phi_b M_{ny} = 0.9 \times F_y \times Z_y$$

其中 $Z_y$（弱軸塑性斷面模數）：
$$Z_y = \frac{b_f^2 t_f}{2} + \frac{t_w h_w^2}{4} \times \text{（通常可略）}$$

$$\approx \frac{b_f^2 t_f}{2} \quad \text{（翼板主導）}$$

**弱軸無 LTB 問題**：I 形梁繞弱軸彎曲時，不會發生側向扭轉挫屈（LTB），因為彎曲本身就沿弱軸，沒有更弱的方向可以偏轉。

## 雙軸彎矩（Biaxial Bending）梁柱設計

當構件同時受強軸彎矩 $M_x$、弱軸彎矩 $M_y$ 及軸力 $P$ 時，使用 P-M 互制公式（AISC H1-1）：

$$\frac{P_u}{\phi_c P_n} \geq 0.2：\quad \frac{P_u}{\phi_c P_n} + \frac{8}{9}\left(\frac{M_{ux}}{\phi_b M_{nx}} + \frac{M_{uy}}{\phi_b M_{ny}}\right) \leq 1.0$$

$$\frac{P_u}{\phi_c P_n} < 0.2：\quad \frac{P_u}{2\phi_c P_n} + \left(\frac{M_{ux}}{\phi_b M_{nx}} + \frac{M_{uy}}{\phi_b M_{ny}}\right) \leq 1.0$$

其中 $M_{uy}$、$\phi_b M_{ny}$ 為弱軸設計需求與強度。

## 弱軸剪力

對於 I 形梁，弱軸方向（沿翼板）的剪力由**翼板**承擔（非腹板）：
$$V_{ny} = 0.6 F_y \times (2 \times b_f \times t_f) \quad \text{（兩片翼板）}$$

這與強軸剪力（腹板承擔）完全不同。

## 常見陷阱

1. **弱軸無 LTB**：弱軸彎曲梁不需計算 LTB，直接用 $\phi_b M_p = 0.9 F_y Z_y$（若斷面結實）。
2. **$Z_y$ 計算**：弱軸塑性模數約為 $b_f^2 t_f / 2$，與強軸 $Z_x$ 計算方式不同。
3. **弱軸剪力**：弱軸方向剪力由翼板承擔，公式與腹板承剪公式不同。
4. **$KL/r$ 兩軸比較**：有時強軸因 $K_x > K_y$ 或 $L_x > L_y$ 而控制，不可一律假設弱軸控制。

## 相關概念

- [[BEAM-COLUMN-INTERACTION]] — P-M 互制（含弱軸彎矩）
- [[LATERAL-TORSIONAL-BUCKLING]] — LTB 只發生在強軸彎曲
- [[FLEXURAL-BUCKLING-GENERAL]] — 整體挫屈（兩軸均需計算）
- [[BIAXIAL-BENDING-BEAM]] — 梁的雙軸彎矩概念
- [[SHEAR-FLOW-BEAM]] — 弱軸剪力流與強軸不同

## 出現題目

| 題號 | 考年 | 主分類 | 核心標籤 |
|------|------|--------|----------|
| [[SS-2002-1]] | 91 | 梁桿件 | 弱軸剪力, 翼板承剪, 剪力流 |
| [[SS-2006-1]] | 95 | 梁柱桿件 | 弱軸挫屈, KL/r兩軸比較 |
| [[SS-2022-1]] | 111 | 梁柱桿件 | 雙軸彎矩, 弱軸彎矩 My, P-M互制 |
