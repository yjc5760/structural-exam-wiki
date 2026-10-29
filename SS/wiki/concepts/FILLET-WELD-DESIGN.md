# 填角銲設計（Fillet Weld Design）

**概念 ID：** FILLET-WELD-DESIGN
**知識分類：** Part 1.4 接合之分析與設計
**規範來源：** AISC 360 Chapter J / AWS D1.1 / 鋼構設計規範 第七章

---

## 定義

填角銲（Fillet Weld）是最常見的銲接形式，沿接合構件的角隅施銲，截面呈直角等腰三角形。設計強度以**有效喉厚**（Effective Throat）為基礎計算。

---

## 前置概念

- [[WELDING-PROCESSES]] — 銲接方法（SMAW、SAW、GMAW、FCAW）
- [[WELD-DEFECTS]] — 銲道瑕疵（未熔合、裂縫、氣孔）
- [[BLOCK-SHEAR-RUPTURE]] — 塊狀剪力撕裂（填角銲配合鋼板傳力時的破壞模式）

---

## 相關概念

- [[WELDED-CONNECTION-DESIGN]] — 銲接接合設計（廣義）
- [[ECCENTRIC-CONNECTION]] — 偏心接合（填角銲偏心銲縫分析）
- [[SLIP-CRITICAL-CONNECTION]] — 摩阻型接合（螺栓 vs 銲接的選擇）

---

## 關鍵公式

### 有效喉厚（Effective Throat）

$$t_e = 0.707 \times w$$

其中 $w$ 為銲腳尺寸（weld size）。

> **物理意義：** 等腰直角三角形的斜邊（喉部）對角腳長之比為 $\cos 45° = 0.707$。詳見推導 → [fillet-weld-0707.md](../code-ref/fillet-weld-0707.md)

---

### LRFD 設計強度

$$\phi R_n = \phi \cdot (0.6 F_{EXX}) \cdot A_w$$

其中：
- $\phi = 0.75$
- $F_{EXX}$：銲條最小抗拉強度（E70XX → $F_{EXX} = 485 \text{ MPa} = 4.95 \text{ tf/cm}^2$）
- $A_w = t_e \times L_w$：有效喉截面積

---

### ASD 容許強度

$$f_{allow} = 0.3 \times F_{EXX}$$

單位銲道長度容許剪力：

$$q_{allow} = 0.3 F_{EXX} \times t_e$$

---

### 最小/最大銲腳尺寸限制

| 較厚板厚 $t$ | 最小銲腳尺寸 $w_{min}$ |
|-------------|----------------------|
| $t \leq 6$ mm | 3 mm |
| $6 < t \leq 12$ mm | 5 mm |
| $12 < t \leq 20$ mm | 6 mm |
| $t > 20$ mm | 8 mm |

**最大銲腳尺寸：**
- 厚板（$t \geq 6$ mm）：$w_{max} = t - 1.5 \text{ mm}$（直邊）
- 薄板（$t < 6$ mm）：$w_{max} = t$

---

### 最小有效長度

$$L_{w,min} = 4w \quad \text{（或至少 38 mm）}$$

若銲道長度 $< 4w$，則有效長度取 $L_w/4$ 作為銲腳尺寸重新計算。

---

## 破壞模式

| 破壞位置 | 破壞類型 | 說明 |
|---------|---------|------|
| 銲喉截面 | 剪力破壞 | 最常見，控制設計 |
| 熱影響區（HAZ） | 拉力或剪力破壞 | 當母材強度不足時 |
| 趾部 / 根部 | 疲勞裂縫 | 反覆載重下易發生 |
| 母材 | 降伏或斷裂 | 當銲道過強時 |

---

## 常見陷阱

1. **漏加 0.707 係數：** 設計強度應以有效喉厚計算，不可直接用銲腳尺寸。
2. **E70XX 的 $F_{EXX}$ 混淆單位：** E70 代表 70 ksi（= $4.95 \text{ tf/cm}^2 = 485 \text{ MPa}$）。
3. **ASD 銲接容許應力：** 0.3 $F_{EXX}$ 是剪應力，非抗拉強度。
4. **回銲/end return：** 轉角銲（end return）長度 ≥ 2w，常考施工細節。
5. **斷續銲 vs 連續銲：** 斷續銲計算有效長度時只算有銲的段落。
6. **最小銲腳尺寸**由**較厚板**決定，不是較薄板。

---

## 歷年考題

| 題號 | 設計法 | 核心考法 |
|------|--------|---------|
| [SS-2019-4](../problems/SS-2019-4.md) | LRFD | 斷續填角銲、蓋板、剪力流計算銲道長度 |
| [SS-2018-3](../problems/SS-2018-3.md) | ASD | 梁柱接頭填角銲、ASD容許應力、組合應力 |
| [SS-2017-4](../problems/SS-2017-4.md) | LRFD | 偏心銲縫、托架接合、扭矩分析 |
| [SS-2015-2](../problems/SS-2015-2.md) | LRFD | 拉力桿件+填角銲、剪力遲滯 |
| [SS-2007-1](../problems/SS-2007-1.md) | ASD | 偏心填角銲、不等肢角鋼 |
| [SS-2005-3](../problems/SS-2005-3.md) | LRFD | 偏心接合、牛腿接合、銲接群分析 |
| [SS-2004-3](../problems/SS-2004-3.md) | LRFD | 偏心接合、彈性向量法 |
| [SS-2003-3](../problems/SS-2003-3.md) | LRFD | WT斷面、剪力遲滯、銲接拉力接合 |

---

*相關方法論→ [eccentric-weld.md](../methods/eccentric-weld.md)（偏心銲縫計算步驟）*
*規範推導 → [fillet-weld-0707.md](../code-ref/fillet-weld-0707.md)（0.707 有效喉厚推導）*
