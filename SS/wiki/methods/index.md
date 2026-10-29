# 解題方法論索引

> **用途：** 「我知道這題大概要算什麼，但步驟不記得了」→ 直接找對應方法頁。
>
> 每個方法頁包含：完整計算步驟、關鍵公式、歷屆出現題目、常見陷阱。

---

## 依題型分組

### 壓力桿件（SS-U1-1）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [LRFD 柱設計（λc 法）](lrfd-column.md) | 題目給 Pu，用 LRFD 驗核或選斷面 | ⭐⭐⭐⭐ 16題 |
| [ASD 柱設計（Cc 法）](asd-column.md) | 題目給 P（服務載重），用 ASD 容許應力法 | ⭐⭐⭐ 10題 |
| [有效長度對位圖（G 值法）](effective-length-chart.md) | 框架柱，需從構架幾何求 K 值 | ⭐⭐⭐ 7題 |

### 拉力桿件（SS-U1-1）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [剪力遲滯 U 值計算](shear-lag-u.md) | 非全斷面連接（角鋼、槽鋼、T 型鋼） | ⭐⭐⭐ 7題 |
| [塊狀剪力（Block Shear）](block-shear.md) | 螺栓群邊緣區塊撕裂失敗模式 | ⭐⭐⭐ 8題 |

### 梁桿件（SS-U1-2）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [LTB 三區段判斷（LRFD）](ltb-3zone.md) | 已知 Lb，判斷區段求 φbMn | ⭐⭐⭐⭐⭐ 18題 |
| [ASD 梁設計（Lc/Lu/Fb 法）](asd-beam.md) | ASD 法，依 Lb 與 Lc/Lu 比較求 Fb | ⭐⭐⭐ 6題 |
| [Cb 彎矩梯度係數](cb-factor.md) | LTB 計算中需考慮非均勻彎矩 | ⭐⭐⭐ 多題 |
| [塑性斷面模數 Zx 計算](plastic-zx.md) | 求組合斷面或非標準斷面的 Zx | ⭐⭐⭐ 10題 |
| [共軛梁法（位移計算）](conjugate-beam.md) | 求梁撓度或轉角（靜定梁） | ⭐⭐ 多題 |

### 梁柱桿件（SS-U1-3）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [P-M 互制驗核（LRFD）](pm-interaction.md) | 同時有 Pu 與 Mu，驗核 H1-1a/b 公式 | ⭐⭐⭐ 6題 |
| [B1-B2 二階放大法（LRFD）](b1b2-amplification.md) | 框架有側移，需放大彎矩後再驗核 P-M | ⭐⭐⭐ 6題 |
| [B1 放大係數 M1/M2 符號規則](b1-m1m2-sign-convention.md) | 判斷單曲率/雙曲率決定 Cm，最常混淆的符號陷阱 | ⭐⭐⭐ 多題 |
| [ASD 梁柱雙軸互制](asd-beam-column.md) | ASD 法，雙軸彎矩 + 軸壓互制方程式 | ⭐⭐⭐ 8題 |

### 接合設計（SS-U1-4）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [偏心螺栓群（彈性向量法）](eccentric-bolt.md) | 螺栓群有偏心距（托架、牛腿） | ⭐⭐ 3題 |
| [偏心銲縫群（線圖法）](eccentric-weld.md) | 銲縫有偏心距（銲縫線圖 Ip 計算） | ⭐⭐ 3題 |
| [摩阻型接合（LRFD）](slip-critical-lrfd.md) | 高拉力螺栓，預拉力×摩擦係數×剪力面數 | ⭐⭐ 5題 |
| [塊狀剪力](block-shear.md) | （同拉力桿件，接合處也適用） | — |

### 斷面性質（MM-U1-1）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [塑性斷面模數 Zx 計算](plastic-zx.md) | PNA 法求 Zx（含非對稱斷面） | ⭐⭐⭐ 10題 |
| [合成梁 PNA 計算](composite-beam-pna.md) | 組合梁塑性應力分佈、正彎矩強度 | ⭐⭐ 3題 |

### 塑性分析（SS-U2-1）

| 方法 | 適用時機 | 出現頻率 |
|------|---------|---------|
| [塑性機構虛功法](plastic-mechanism.md) | 求崩塌載重 wu 或極限彎矩 Mp | ⭐⭐ 3題 |
| [塑性斷面模數 Zx 計算](plastic-zx.md) | （同梁桿件） | — |

---

## 依出現頻率排序（備考優先順序）

| 排名 | 方法 | 頻率 | 一句話說明 |
|------|------|------|---------|
| 1 | [LTB 三區段](ltb-3zone.md) | 18題 | Lb → 比 Lp/Lr → 求 Mn |
| 2 | [LRFD 柱](lrfd-column.md) | 16題 | KL/r → λc → Fcr → φcPn |
| 3 | [Zx 計算](plastic-zx.md) | 10題 | 等面積求 PNA → 面積矩求 Zx |
| 4 | [ASD 柱](asd-column.md) | 10題 | KL/r → 比 Cc → Fa → 驗核 |
| 5 | [Block Shear](block-shear.md) | 8題 | 剪力面 + 拉力面 → 取小 |
| 6 | [有效長度對位圖](effective-length-chart.md) | 7題 | GA/GB → 查圖 → K |
| 7 | [剪力遲滯 U 值](shear-lag-u.md) | 7題 | x̄/L → U → Ae = UAn |
| 8 | [P-M 互制](pm-interaction.md) | 6題 | Pr/Pc ≥ 0.2？ → H1-1a or b |
| 9 | [B1-B2 放大](b1b2-amplification.md) | 6題 | Mnt/Mlt → B1·Mnt + B2·Mlt |
| 10 | [Cb 係數](cb-factor.md) | 多題 | 四點法：(2.5Mmax+3MA+4MB+3MC)/12.5 |
| 11 | [偏心螺栓群](eccentric-bolt.md) | 3題 | Ip = Σ(x²+y²) → RM = Mr/Ip |
| 12 | [偏心銲縫群](eccentric-weld.md) | 3題 | 線圖 Ip(cm³) → fM = Mr/Ip |
| 13 | [塑性機構](plastic-mechanism.md) | 3題 | 機構數 → 虛功法 → wu |
| 14 | [共軛梁法](conjugate-beam.md) | 多題 | M/EI 圖 → 共軛梁 → 求撓度 |
| 15 | [ASD 梁設計](asd-beam.md) | 6題 | Lb → 比 Lc/Lu → Fb → Ma |
| 16 | [ASD 梁柱雙軸互制](asd-beam-column.md) | 8題 | fa/Fa → Eq.2 or 3 → 兩式均驗 |
| 17 | [摩阻型接合（LRFD）](slip-critical-lrfd.md) | 5題 | 預拉力 Tb × 摩擦係數 × 剪力面數 |
| 18 | [合成梁 PNA 計算](composite-beam-pna.md) | 3題 | Cs vs Cc 判斷→ 計算 a → Mn |

---

## 方法選擇速查

```
題目給：Pu（放大載重）
  → LRFD 設計法
  → 壓力桿件：lrfd-column
  → 梁柱桿件：lrfd-column + pm-interaction（+ b1b2 如有側移）

題目給：P（服務載重）
  → ASD 設計法
  → 壓力桿件：asd-column
  → 梁桿件：asd-beam
  → 梁柱桿件：asd-column + asd-beam-column

題目有偏心距 e
  → 螺栓群：eccentric-bolt
  → 銲縫群：eccentric-weld

題目有 Lb（側撐間距）
  → 梁桿件：ltb-3zone（± cb-factor）

題目有「角鋼」「槽鋼」只有部分肢連接
  → shear-lag-u

題目有螺栓邊緣群 + 拉力
  → block-shear（確認 Anv / Ant 路徑）

題目求最大載重 wu 或機構
  → plastic-mechanism（虛功法）
```

---

## 相關導航

- [診斷層 →](../diagnosis/index.md)（從題型出發，找對應方法）
- [失敗模式層 →](../failure-modes/index.md)（理解為什麼要用這個方法）
- [規範對應 →](../code-ref/index.md)（公式的規範出處）
