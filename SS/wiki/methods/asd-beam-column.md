# ASD 梁柱桿件設計流程（雙軸彎矩互制）

**方法 ID：** asd-beam-column
**知識分類：** 解題工具 / 梁柱桿件設計（ASD）
**適用題型：** SS-U1-3 梁柱桿件（ASD 設計法）
**出現題數：** ~8 題

---

## 核心原理

ASD 梁柱以**互制方程式（Interaction Equations）** 整合軸壓應力與雙軸彎曲應力，並依 $f_a/F_a$ 大小選擇方程式。

### 判斷式：fa/Fa 與 0.15 比較

$$\frac{f_a}{F_a} < 0.15：\text{簡化式（Eq.3）}$$

$$\frac{f_a}{F_a} \geq 0.15：\text{完整式（Eq.2）}$$

---

## 互制方程式

### Equation (2)（$f_a/F_a \geq 0.15$，含二階放大）

$$\frac{f_a}{F_a} + \frac{C_{mx}f_{bx}}{\left(1 - \dfrac{f_a}{F'_{ex}}\right)F_{bx}} + \frac{C_{my}f_{by}}{\left(1 - \dfrac{f_a}{F'_{ey}}\right)F_{by}} \leq 1.0$$

$$\frac{f_a}{0.6F_y} + \frac{f_{bx}}{F_{bx}} + \frac{f_{by}}{F_{by}} \leq 1.0 \quad \text{（截面強度檢核）}$$

### Equation (3)（$f_a/F_a < 0.15$）

$$\frac{f_a}{F_a} + \frac{f_{bx}}{F_{bx}} + \frac{f_{by}}{F_{by}} \leq 1.0$$

---

## 各符號說明

| 符號 | 意義 | 計算方式 |
|------|------|---------|
| $f_a = P/A$ | 實際軸壓應力 | 直接計算 |
| $F_a$ | 容許軸壓應力 | 見 [[asd-column]]（Cc 法） |
| $f_{bx} = M_x/S_x$ | 強軸彎矩應力 | 直接計算 |
| $f_{by} = M_y/S_y$ | 弱軸彎矩應力 | 直接計算 |
| $F_{bx}$ | 容許強軸彎矩應力（含 LTB） | 見下方「LTB 段落計算」 |
| $F_{by}$ | 容許弱軸彎矩應力 | $= 0.75 F_y$（結實斷面） |
| $C_{mx}$, $C_{my}$ | 等效彎矩係數 | $0.6 - 0.4(M_1/M_2)$ |
| $F'_{ex}$, $F'_{ey}$ | 尤拉修正應力 | $= \dfrac{12\pi^2 E}{23(KL/r)^2}$（與 $F_a$ 彈性段公式相同） |

---

## 解題步驟

```
Step 1  計算實際應力
        fa = P/A
        fbx = Mx/Sx，fby = My/Sy

Step 2  計算 Fa（容許軸壓應力）
        → 見 asd-column（Cc 法，取兩軸 KL/r 最大值）

Step 3  判斷 fa/Fa：與 0.15 比較 → 選方程式

Step 4  計算 Fbx（容許強軸彎矩應力）
        → 依 L/rT 判斷 LTB 段（見下方）

Step 5  確認 Fby = 0.75Fy（結實斷面弱軸）

Step 6  計算 Cm（等效彎矩係數）
        Cm = 0.6 - 0.4(M1/M2)
        M1/M2 為小端/大端力矩比，同曲率為正

Step 7  計算 F'e（尤拉修正應力）
        F'e = 12π²E / [23(KL/r)²]
        ⚠️ 彈性挫屈段：F'e = Fa（不需另算）

Step 8  代入互制方程式（兩個都要驗）
```

---

## Fbx 容許強軸彎矩應力（含 LTB）

以 $L/r_T$ 為判斷依據（$r_T$ = 翼板有效迴轉半徑）：

> ⚠️ **以下係數為 ksi 制**（$F_y$ 用 ksi）。tf/cm² 制的對應係數見 [[asd-beam]] 的換算表
> （$F_y[\text{ksi}] = 14.223\,F_y[\text{tf/cm}^2]$）。

$$\sqrt{\frac{102{,}000\,C_b}{F_y}} \le \frac{L}{r_T} \leq \sqrt{\frac{510{,}000\,C_b}{F_y}}：$$

$$F_{bx} = \left[\frac{2}{3} - \frac{F_y (L/r_T)^2}{1{,}530{,}000\,C_b}\right]F_y \leq 0.60F_y \quad \text{（非彈性 LTB，AISC ASD F1-6）}$$

$$\frac{L}{r_T} > \sqrt{\frac{510{,}000\,C_b}{F_y}}：\quad F_{bx} = \frac{170{,}000\,C_b}{(L/r_T)^2} \quad \text{（彈性 LTB，F1-7）}$$

上式與下方「公式二」（$12{,}000C_b/(Ld/A_f)$）**取較大值**，並受 $F_{bx} \leq 0.60F_y$ 限制。
（取大的理由：兩式分別只計翹曲扭轉與只計純扭轉，都是保守下界 —— 見 [[asd-beam-fb-derivation]]。）

**補充（另一段公式）：**
$$F_{bx} = \frac{12\,000\,C_b}{L \cdot d / A_f} \quad \text{（另一彈性 LTB 計算式，取大值）}$$

**簡化情況：**
- 充分側撐（$L_b \leq L_p$ 當量）：$F_{bx} = 0.66F_y$

---

## 常見陷阱

1. **F'e 與 Fa 關係**：當 $KL/r > C_c$（彈性挫屈段），$F'_e$ 的計算公式與 $F_a$ **完全相同**（$12\pi^2E/23(KL/r)^2$），不需另外計算。
2. **兩個互制方程式都要驗**：即使 $f_a/F_a \geq 0.15$ 選了 Equation (2)，Equation (2) 的**截面強度式**（含 $0.6F_y$）也必須同時驗算。
3. **Cm 符號定義**：$M_1/M_2$ 同曲率（雙曲反撓）為**正**，反曲率為**負**；一端為零時 $M_1/M_2 = 0 \Rightarrow C_m = 0.6$。
4. **Cb 用於 Fbx 而非 Fby**：弱軸沒有 LTB，$F_{by}$ 不用 $C_b$。
5. **rT vs ry**：$r_T$ 是翼板有效迴轉半徑（含翼板 + 腹板上 1/3），不等於 $r_y$。

---

## 相關連結

- [[asd-column]] — 容許軸壓應力 $F_a$ 計算
- [[cb-factor]] — $C_b$ 係數計算（用於 $F_{bx}$）
- [[pm-interaction]] — LRFD 對應：P-M 互制公式
- [[b1b2-amplification]] — LRFD 對應：B1-B2 放大法

## 出現題目

| 題號 | 考年 | 主分類 | 核心標籤 |
|------|------|--------|----------|
| [[SS-2002-4]] | 91 | 梁柱桿件 | ASD, 梁柱互制, 雙軸 |
| [[SS-2003-4]] | 92 | 梁柱桿件 | ASD, B1放大, 側移構架 |
| [[SS-2004-4]] | 93 | 梁柱桿件 | ASD, 梁柱互制, 弱軸 |
| [[SS-2007-2]] | 96 | 梁柱桿件 | ASD, 雙軸彎矩, LTB, Cm放大係數 |
| [[SS-2008-1]] | 97 | 梁柱桿件 | ASD, 梁柱, Fbx |
| [[SS-2008-4]] | 97 | 梁柱桿件 | ASD, 梁柱, F'e |
| [[SS-2010-3]] | 99 | 梁柱桿件 | ASD, 互制方程式 |
| [[SS-2011-4]] | 100 | 梁柱桿件 | ASD, LeMessurier, 梁柱 |
