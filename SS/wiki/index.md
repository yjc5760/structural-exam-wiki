# 鋼結構設計考古題知識庫

**科目代碼：** SS（Steel Structure Design）
**考試名稱：** 專門職業及技術人員高等考試結構工程技師 — 第四科：鋼結構設計
**題目總數：** 98 題（2002–2025 年）
**已驗證：** 0 題 ／ **待驗證：** 98 題（2026-08-22 全庫重置，待逐題重新驗算）

> ⚠️ = 尚未驗證（unverified）；驗證後執行 `ingest SS-XXXX-N` 即可生成題目頁。

---

## 快速導航

- [依年份瀏覽 →](by-year.md)
- [命題大綱分類 →](topics/index.md)（SS-U1-1 拉壓桿件 · SS-U1-2 梁 · SS-U1-3 梁柱 · SS-U1-4 接合 · SD-U3-1 耐震）
- [解題方法論 →](#part-3解題方法論)（共軛梁法 · Cb 因子）
- [設計哲學 →](philosophy/index.md)（LRFD/ASD 各題型解題邏輯）
- [所有概念索引 →](#概念索引)
- [術語速查 GLOSSARY →](concepts/GLOSSARY.md)（符號 · 公式 · 設計法對照）
- [知識庫使用說明書 →](../知識庫使用說明書.md)（工作流程 · 指令手冊 · 讀書策略）

---

## Part 1：核心構件設計

### 1.1 拉力／壓力桿件（SS-U1-1）

**核心概念：**
- [[RESIDUAL-STRESS]] — [殘留應力](concepts/RESIDUAL-STRESS.md)
- [[TANGENT-MODULUS-THEORY]] — [切線模數理論](concepts/TANGENT-MODULUS-THEORY.md)
- [[COLUMN-STRENGTH-CURVE]] — [柱強度曲線](concepts/COLUMN-STRENGTH-CURVE.md)
- [[FLEXURAL-BUCKLING-GENERAL]] — [彎曲挫屈（一般概念）](concepts/FLEXURAL-BUCKLING-GENERAL.md)
- [[SHEAR-LAG]] — [剪力遲滯](concepts/SHEAR-LAG.md)
- [[BLOCK-SHEAR-RUPTURE]] — [塊狀剪力撕裂](concepts/BLOCK-SHEAR-RUPTURE.md)

**相關題目（共 ~28 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2025-2](problems/SS-2025-2.md) | 114年 | ASD | 拉力桿件、剪力遲滯、U值、ASD容許應力法 |
| ⚠️ [SS-2024-1](problems/SS-2024-1.md) | 113年 | LRFD | 殘留應力、切線模數、柱強度曲線 |
| ⚠️ [SS-2024-2](problems/SS-2024-2.md) | 113年 | LRFD | 剪力遲滯 |
| ⚠️ [SS-2023-1](problems/SS-2023-1.md) | 112年 | LRFD | 壓力桿件、拉力桿件 |
| ⚠️ [SS-2023-2](problems/SS-2023-2.md) | 112年 | ASD | 柱強度曲線、整體挫屈 |
| ⚠️ [SS-2022-2](problems/SS-2022-2.md) | 111年 | ASD | 壓力桿件、拉力桿件 |
| ⚠️ [SS-2018-2](problems/SS-2018-2.md) | 107年 | LRFD | 壓力桿件 |
| ⚠️ [SS-2017-3](problems/SS-2017-3.md) | 106年 | ASD | 柱強度曲線（ASD） |
| ⚠️ [SS-2016-3](problems/SS-2016-3.md) | 105年 | LRFD | 殘留應力、柱強度曲線、切線模數 |
| ⚠️ [SS-2015-2](problems/SS-2015-2.md) | 104年 | LRFD | 拉力桿件、剪力遲滯、塊狀剪力 |
| ⚠️ [SS-2015-3](problems/SS-2015-3.md) | 104年 | ASD | 組合柱、有效長度 |
| ⚠️ [SS-2014-1](problems/SS-2014-1.md) | 103年 | LRFD | 整體挫屈、柱強度曲線、λc推導、殘留應力 |
| ⚠️ [SS-2011-2](problems/SS-2011-2.md), SS-2011-4 | 100年 | — | 壓力/拉力桿件 |
| *(更多見 [by-year.md](by-year.md))* | | | |

---

### 1.2 撓曲桿件（SS-U1-2）

**核心概念：**
- [[LATERAL-TORSIONAL-BUCKLING]] — [側向扭轉挫屈 (LTB)](concepts/LATERAL-TORSIONAL-BUCKLING.md) ⭐ 最高頻（13 題）
- [[BENDING-MODIFICATION-FACTOR-CB]] — [彎矩梯度修正係數 Cb](concepts/BENDING-MODIFICATION-FACTOR-CB.md)
- [[PLATE-GIRDER-DESIGN]] — [板梁設計](concepts/PLATE-GIRDER-DESIGN.md)
- [[TENSION-FIELD-ACTION]] — [張力場效應](concepts/TENSION-FIELD-ACTION.md)
- [[SHEAR-FLOW-BEAM]] — [梁之剪力流](concepts/SHEAR-FLOW-BEAM.md)
- [[SHAPE-FACTOR]] — [形狀因數](concepts/SHAPE-FACTOR.md)
- [[WEB-LOCAL-YIELDING]] — [腹板局部降伏](concepts/WEB-LOCAL-YIELDING.md)

**相關題目（共 ~23 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2025-1](problems/SS-2025-1.md) | 114年 | LRFD | 結實斷面、塑性彎矩、銲接組合斷面、完全側向支撐 |
| ⚠️ [SS-2025-3](problems/SS-2025-3.md) | 114年 | LRFD | LTB側扭挫屈、Lp、Lr、熱軋斷面 |
| ⚠️ [SS-2024-3](problems/SS-2024-3.md) | 113年 | LRFD | LTB側扭挫屈 |
| ⚠️ [SS-2021-3](problems/SS-2021-3.md) | 110年 | LRFD | LTB側扭挫屈 |
| ⚠️ [SS-2019-2](problems/SS-2019-2.md) | 108年 | LRFD | 撓曲構材 |
| ⚠️ [SS-2016-4](problems/SS-2016-4.md) | 105年 | LRFD | LTB + 整體挫屈 |
| ⚠️ [SS-2016-1](problems/SS-2016-1.md) | 105年 | ASD | 撓曲構材 |
| ⚠️ [SS-2015-1](problems/SS-2015-1.md) | 104年 | LRFD | **LTB、斷面選擇、剪力強度、使用性撓度** |
| ⚠️ [SS-2014-3](problems/SS-2014-3.md) | 103年 | LRFD | 非彈性LTB、Cb係數、雙向彎曲、弱軸強度上限 |
| ⚠️ [SS-2012-1](problems/SS-2012-1.md) | 101年 | LRFD | LTB側扭挫屈 |
| ⚠️ [SS-2011-3](problems/SS-2011-3.md) | 100年 | LRFD | LTB側扭挫屈 |
| ⚠️ [SS-2008-1](problems/SS-2008-1.md), SS-2008-3 | 97年 | — | LTB側扭挫屈 |
| ⚠️ [SS-2007-3](problems/SS-2007-3.md) | 96年 | LRFD | LTB側扭挫屈 |
| *(更多見 [by-year.md](by-year.md))* | | | |

---

### 1.3 梁柱桿件（SS-U1-3）

**核心概念：**
- [[BEAM-COLUMN-INTERACTION]] — [梁柱互制行為](concepts/BEAM-COLUMN-INTERACTION.md)
- [[P-DELTA-EFFECT]] — [P-Δ 二階效應](concepts/P-DELTA-EFFECT.md)
- [[MOMENT-AMPLIFICATION-CM]] — [彎矩放大係數 Cm](concepts/MOMENT-AMPLIFICATION-CM.md)
- [[FRAME-STABILITY-ADVANCED]] — [構架穩定性（進階）](concepts/FRAME-STABILITY-ADVANCED.md)
- [[LEANER-COLUMN-EFFECT]] — [靠桿效應](concepts/LEANER-COLUMN-EFFECT.md)
- [[BIAXIAL-BENDING-BEAM]] — [梁之雙軸彎曲](concepts/BIAXIAL-BENDING-BEAM.md)

**相關題目（共 ~14 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2022-1](problems/SS-2022-1.md) | 111年 | LRFD | 梁柱桿件、柱強度曲線、LTB |
| ⚠️ [SS-2020-3](problems/SS-2020-3.md) | 109年 | LRFD | 梁柱桿件 |
| ⚠️ [SS-2019-3](problems/SS-2019-3.md) | 108年 | ASD | 梁柱桿件（ASD互制） |
| ⚠️ [SS-2014-4](problems/SS-2014-4.md) | 103年 | LRFD | P-M互制、B1/B2放大法、二階效應、斜撐構架、地震力組合 |
| ⚠️ [SS-2013-4](problems/SS-2013-4.md) | 102年 | LRFD | 梁柱桿件 |
| ⚠️ [SS-2012-3](problems/SS-2012-3.md) | 101年 | LRFD | 梁柱桿件 |
| ⚠️ [SS-2009-1](problems/SS-2009-1.md) | 98年 | LRFD | 梁柱、強柱弱梁 |
| *(更多見 [by-year.md](by-year.md))* | | | |

---

### 1.4 接合設計（SS-U1-4）

**核心概念：**
- [[SLIP-CRITICAL-CONNECTION]] — [摩阻型接合](concepts/SLIP-CRITICAL-CONNECTION.md)
- [[BLOCK-SHEAR-RUPTURE]] — [塊狀剪力撕裂](concepts/BLOCK-SHEAR-RUPTURE.md)（見 1.1 亦有）
- [[SHEAR-FLOW-BEAM]] — [梁之剪力流](concepts/SHEAR-FLOW-BEAM.md)
- [[FILLET-WELD-DESIGN]] — [填角銲設計](concepts/FILLET-WELD-DESIGN.md)
- [[ECCENTRIC-CONNECTION]] — [偏心接合](concepts/ECCENTRIC-CONNECTION.md)

**相關題目（共 24 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2024-4](problems/SS-2024-4.md) | 113年 | 概念題 | 梁柱接頭、電熱熔渣銲、層狀撕裂、HAZ脆化、NDT |
| ⚠️ [SS-2023-4](problems/SS-2023-4.md) | 112年 | 概念題 | 填角銲、對接銲、破壞形式、塊狀剪力 |
| ⚠️ [SS-2021-2](problems/SS-2021-2.md) | 110年 | LRFD | 填角銲、塊狀剪力、高拉力螺栓、搭接接合 |
| ⚠️ [SS-2021-4](problems/SS-2021-4.md) | 110年 | 概念題 | 高拉力螺栓、摩阻型螺栓、混合接合 |
| ⚠️ [SS-2020-4](problems/SS-2020-4.md) | 109年 | ASD | 腹板續接、四鈑接合、A490螺栓 |
| ⚠️ [SS-2019-4](problems/SS-2019-4.md) | 108年 | LRFD | 填角銲、斷續銲接、蓋板組合斷面、剪力流 |
| ⚠️ [SS-2018-3](problems/SS-2018-3.md) | 107年 | ASD | 填角銲、梁柱接頭、銲道容許應力、組合應力 |
| ⚠️ [SS-2017-2](problems/SS-2017-2.md) | 106年 | LRFD | 高強度螺栓、摩阻型接合、夾緊力、摩擦係數 |
| ⚠️ [SS-2017-4](problems/SS-2017-4.md) | 106年 | LRFD | 填角銲、偏心銲縫、托架接合、彈性向量法 |
| ⚠️ [SS-2012-4](problems/SS-2012-4.md) | 101年 | LRFD | 剪力板、A325螺栓、承壓型螺栓、梁柱接頭 |
| ⚠️ [SS-2009-4](problems/SS-2009-4.md) | 98年 | 概念題 | 開槽銲、SAW、UT超音波、高拉力螺栓間距 |
| ⚠️ [SS-2007-1](problems/SS-2007-1.md) | 96年 | ASD | 填角銲、偏心接合、剪力遲滯、銲道容許應力 |
| ⚠️ [SS-2006-2](problems/SS-2006-2.md) | 95年 | LRFD | 高拉力螺栓、預拉力、塊狀剪力 |
| ⚠️ [SS-2006-5](problems/SS-2006-5.md) | 95年 | LRFD | 箱型柱梁柱接頭、連續板、節點域、CJP銲 |
| ⚠️ [SS-2005-3](problems/SS-2005-3.md) | 94年 | LRFD | 填角銲、偏心接合、牛腿接合、彈性向量法 |
| ⚠️ [SS-2004-2](problems/SS-2004-2.md) | 93年 | ASD | 拉力構材續接、高拉力螺栓、翼板連接 |
| ⚠️ [SS-2004-3](problems/SS-2004-3.md) | 93年 | LRFD | 填角銲、偏心接合、彈性向量法、托架 |
| ⚠️ [SS-2003-3](problems/SS-2003-3.md) | 92年 | LRFD | 剪力遲滯、螺栓接合、塊狀剪力、WT斷面 |
| ⚠️ [SS-2002-4](problems/SS-2002-4.md) | 91年 | ASD | 偏心螺栓群、彈性分析法、向量疊加 |
| *(另見副分類含接合的題目：SS-2015-2、SS-2024-2、SS-2022-2 等)* | | | |

---

## Part 2：設計哲學與實務

### 2.1 耐震設計（SD-U3-1 / SS-U1-4 耐震）

**核心概念：**
- [[STRONG-COLUMN-WEAK-BEAM]] — [強柱弱梁](concepts/STRONG-COLUMN-WEAK-BEAM.md)
- [[PANEL-ZONE]] — [節點域 (Panel Zone)](concepts/PANEL-ZONE.md)
- [[REDUCED-BEAM-SECTION]] — [梁翼板削減式接頭 (RBS)](concepts/REDUCED-BEAM-SECTION.md)
- [[CAPACITY-DESIGN]] — [容量設計法](concepts/CAPACITY-DESIGN.md)
- [[CONTINUITY-PLATE]] — [連續板](concepts/CONTINUITY-PLATE.md)

**相關題目（共 ~6 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2024-4](problems/SS-2024-4.md) | 113年 | LRFD | 強柱弱梁、節點域、RBS、容量設計 |
| ⚠️ [SS-2014-4](problems/SS-2014-4.md) | 103年 | LRFD | 梁柱桿件（含耐震組合）、B1/B2二階效應 |
| ⚠️ [SS-2014-2](problems/SS-2014-2.md) | 103年 | 概念題 | SN490B vs A572、耐震鋼材、容量設計、強柱弱梁 |
| ⚠️ [SS-2012-2](problems/SS-2012-2.md) | 101年 | LRFD | 結構耐震設計 |
| ⚠️ [SS-2009-2](problems/SS-2009-2.md) | 98年 | LRFD | 節點域 |

---

### 2.2 材料科學（SS-U2-2）

**關鍵材料概念：**
- SN 耐震鋼材（降伏比 ≤ 0.8、衝擊韌性要求）— 含於 [[CAPACITY-DESIGN]] 頁面
- [[COMPOSITE-BEAM]] — [合成梁](concepts/COMPOSITE-BEAM.md)
- [[COMPOSITE-COLUMN]] — [合成柱](concepts/COMPOSITE-COLUMN.md)

**相關題目（共 ~6 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2022-4](problems/SS-2022-4.md) | 111年 | 概念題 | 鋼材材料、強柱弱梁 |
| ⚠️ [SS-2018-1](problems/SS-2018-1.md) | 107年 | 概念題 | 鋼材材料 |
| ⚠️ [SS-2017-1](problems/SS-2017-1.md) | 106年 | 概念題 | 鋼材材料 |
| ⚠️ [SS-2016-5](problems/SS-2016-5.md) | 105年 | 概念題 | 鋼材材料 |
| ⚠️ [SS-2015-4](problems/SS-2015-4.md) | 104年 | 概念題 | SN耐震鋼材、降伏比、衝擊韌性 |
| ⚠️ [SS-2014-2](problems/SS-2014-2.md) | 103年 | 概念題 | SN490B vs A572、耐震鋼材、降伏比、衝擊韌性 |

---

### 2.3 施工與品管（SS-U2-3）

**核心概念：**
- [[WELDING-PROCESSES]] — [銲接方法](concepts/WELDING-PROCESSES.md)（SMAW、SAW、GMAW、FCAW）
- [[WELD-DEFECTS]] — [銲道瑕疵](concepts/WELD-DEFECTS.md)
- [[WELD-INSPECTION-NDT]] — [銲道非破壞檢測](concepts/WELD-INSPECTION-NDT.md)（VT、UT、MT）

**相關題目（共 ~7 題）：**

| 題號 | 年份 | 設計法 | 核心考點 |
|------|------|--------|---------|
| ⚠️ [SS-2022-3](problems/SS-2022-3.md) | 111年 | 概念題 | 施工規範、強柱弱梁 |
| ⚠️ [SS-2021-1](problems/SS-2021-1.md) | 110年 | 概念題 | 施工規範 |
| ⚠️ [SS-2019-1](problems/SS-2019-1.md) | 108年 | 概念題 | 施工規範 |
| ⚠️ [SS-2018-4](problems/SS-2018-4.md) | 107年 | 概念題 | 施工規範 |
| ⚠️ [SS-2016-2](problems/SS-2016-2.md) | 105年 | 概念題 | 施工規範 |
| ⚠️ [SS-2010-2](problems/SS-2010-2.md) | 99年 | 概念題 | 施工規範 |
| ⚠️ [SS-2004-1](problems/SS-2004-1.md) | 93年 | 概念題 | 施工規範 |

---

## Part 3：解題方法論

| 方法 | 說明 | 適用題型 |
|------|------|---------|
| [共軛梁法](methods/conjugate-beam.md) | 位移計算轉換為靜力學問題 | 梁桿件撓度計算 |
| [彎矩梯度修正因子 $C_b$](methods/cb-factor.md) | LTB 強度非均勻彎矩修正，四分點公式 | SS-U1-2 梁桿件、SS-U1-3 梁柱桿件 |
| 虛功法（單位載重法） | 通用位移計算 | 任意點位移 |
| 傾角變位法 | 靜不定分析 | 連續梁、構架 |
| 彎矩分配法 | 靜不定分析 | 連續梁 |

---

## Part 4：材力基礎（MM-U1-1）

**斷面性質題（共 3 題）：**

| 題號 | 年份 | 核心考點 |
|------|------|---------|
| ⚠️ [SS-2013-1](problems/SS-2013-1.md) | 102年 | 斷面性質計算 |
| ⚠️ [SS-2010-1](problems/SS-2010-1.md) | 99年 | 斷面性質計算 |
| ⚠️ [SS-2006-3](problems/SS-2006-3.md) | 95年 | 斷面性質計算 |

---

## Part 5：塑性分析（SS-U2-1）

**塑性設計題（共 5 題）：**

| 題號 | 年份 | 核心考點 |
|------|------|---------|
| ⚠️ [SS-2025-4](problems/SS-2025-4.md) | 114年 | 塑性鉸、崩塌機構、極限載重、上限定理、虛功法 |
| ⚠️ [SS-2023-3](problems/SS-2023-3.md) | 112年 | 塑性分析 |
| ⚠️ [SS-2020-2](problems/SS-2020-2.md) | 109年 | 塑性分析 |
| ⚠️ [SS-2005-4](problems/SS-2005-4.md) | 94年 | 塑性分析 |

---

## 概念索引

### Part 1.1 拉力／壓力桿件
- [殘留應力](concepts/RESIDUAL-STRESS.md) — RESIDUAL-STRESS
- [切線模數理論](concepts/TANGENT-MODULUS-THEORY.md) — TANGENT-MODULUS-THEORY
- [柱強度曲線](concepts/COLUMN-STRENGTH-CURVE.md) — COLUMN-STRENGTH-CURVE ⭐
- [彎曲挫屈（一般概念）](concepts/FLEXURAL-BUCKLING-GENERAL.md) — FLEXURAL-BUCKLING-GENERAL
- [剪力遲滯](concepts/SHEAR-LAG.md) — SHEAR-LAG
- [塊狀剪力撕裂](concepts/BLOCK-SHEAR-RUPTURE.md) — BLOCK-SHEAR-RUPTURE

### Part 1.2 撓曲桿件
- [側向扭轉挫屈 (LTB)](concepts/LATERAL-TORSIONAL-BUCKLING.md) — LATERAL-TORSIONAL-BUCKLING ⭐ (13題)
- [彎矩梯度修正係數 Cb](concepts/BENDING-MODIFICATION-FACTOR-CB.md) — BENDING-MODIFICATION-FACTOR-CB
- [板梁設計](concepts/PLATE-GIRDER-DESIGN.md) — PLATE-GIRDER-DESIGN
- [張力場效應](concepts/TENSION-FIELD-ACTION.md) — TENSION-FIELD-ACTION
- [梁之剪力流](concepts/SHEAR-FLOW-BEAM.md) — SHEAR-FLOW-BEAM
- [形狀因數](concepts/SHAPE-FACTOR.md) — SHAPE-FACTOR
- [腹板局部降伏](concepts/WEB-LOCAL-YIELDING.md) — WEB-LOCAL-YIELDING

### Part 1.3 梁柱桿件
- [梁柱互制行為](concepts/BEAM-COLUMN-INTERACTION.md) — BEAM-COLUMN-INTERACTION ⭐
- [P-Δ 二階效應](concepts/P-DELTA-EFFECT.md) — P-DELTA-EFFECT
- [彎矩放大係數 Cm](concepts/MOMENT-AMPLIFICATION-CM.md) — MOMENT-AMPLIFICATION-CM
- [構架穩定性（進階）](concepts/FRAME-STABILITY-ADVANCED.md) — FRAME-STABILITY-ADVANCED
- [靠桿效應](concepts/LEANER-COLUMN-EFFECT.md) — LEANER-COLUMN-EFFECT
- [梁之雙軸彎曲](concepts/BIAXIAL-BENDING-BEAM.md) — BIAXIAL-BENDING-BEAM

### Part 1.4 接合設計
- [摩阻型接合](concepts/SLIP-CRITICAL-CONNECTION.md) — SLIP-CRITICAL-CONNECTION
- [梁之剪力流](concepts/SHEAR-FLOW-BEAM.md) — SHEAR-FLOW-BEAM（見 1.2）
- [塊狀剪力撕裂](concepts/BLOCK-SHEAR-RUPTURE.md) — BLOCK-SHEAR-RUPTURE（見 1.1）

### Part 2.1 耐震設計
- [強柱弱梁](concepts/STRONG-COLUMN-WEAK-BEAM.md) — STRONG-COLUMN-WEAK-BEAM
- [節點域 (Panel Zone)](concepts/PANEL-ZONE.md) — PANEL-ZONE
- [梁翼板削減式接頭 (RBS)](concepts/REDUCED-BEAM-SECTION.md) — REDUCED-BEAM-SECTION
- [容量設計法](concepts/CAPACITY-DESIGN.md) — CAPACITY-DESIGN
- [連續板](concepts/CONTINUITY-PLATE.md) — CONTINUITY-PLATE

### Part 2.2 材料科學
- [合成梁](concepts/COMPOSITE-BEAM.md) — COMPOSITE-BEAM
- [合成柱](concepts/COMPOSITE-COLUMN.md) — COMPOSITE-COLUMN

### Part 2.3 施工與品管
- [銲接方法](concepts/WELDING-PROCESSES.md) — WELDING-PROCESSES
- [銲道瑕疵](concepts/WELD-DEFECTS.md) — WELD-DEFECTS
- [銲道非破壞檢測](concepts/WELD-INSPECTION-NDT.md) — WELD-INSPECTION-NDT

---

---

## Part 6：跨層知識工具

### 題型診斷層（Diagnosis）
快速定位「這題考什麼、用哪個方法」：

- [題型診斷總覽](diagnosis/index.md)
- [拉力桿件題型](diagnosis/tension-member.md) — GSY / NSF / BSR 決策樹
- [壓力桿件題型](diagnosis/compression-member.md) — LRFD / ASD / 對位圖 決策樹
- [梁桿件題型](diagnosis/beam.md) — LTB 三區段判斷
- [梁柱桿件題型](diagnosis/beam-column.md) — 四步驟完整流程
- [接合設計題型](diagnosis/connection.md) — 螺栓 / 銲縫子樹
- [斷面性質題型](diagnosis/section-property.md) — Ix / Zx / f 決策樹
- [耐震設計題型](diagnosis/seismic.md) — SCWB / PZ / RBS 子樹
- [概念規範題型](diagnosis/conceptual.md) — 說明 / 比較 / 繪圖答題格式

### 失敗模式層（Failure Modes）
「這個構件以什麼方式失敗？」

- [失敗模式總覽](failure-modes/index.md)
- [強度失敗](failure-modes/strength-failure.md) — 降伏 · 淨斷面斷裂 · 塊狀剪力 · 疲勞
- [穩定失敗](failure-modes/stability-failure.md) — 整體挫屈 · LTB · 局部挫屈 · 扭轉挫屈
- [使用性失敗](failure-modes/serviceability-failure.md) — 撓度 · 振動 · 側移
- [接合失敗](failure-modes/connection-failure.md) — 螺栓剪 · 承壓 · 銲喉 · 塊狀剪力

### 材料行為層（Materials）
「鋼材的材料性質如何影響設計假設？」

- [材料行為總覽](materials/index.md)
- [應力-應變行為](materials/stress-strain.md) — Fy / Fu / 降伏比 / 超強係數
- [殘留應力](materials/residual-stress.md) — 來源 · 分布 · 對柱強度的影響
- [斷裂韌性](materials/fracture-toughness.md) — CVN · SN 鋼材分級 · 層狀撕裂
- [銲接性](materials/weldability.md) — 碳當量 · 預熱 · NDT 方法

### 規範條文對應層（Code Reference）
「公式對應哪個規範章節？」

- [規範條文索引](code-ref/index.md) — AISC 360 / 341 / AWS D1.1 章節×考點矩陣

---

## 知識工具導航

- [概念總覽](concepts/index.md)
- [查詢結果](queries/index.md)
- [常見陷阱](traps/index.md)

---

## Wiki 狀態

> 執行 `status` 指令取得最新的驗證進度、解析題數、標籤統計。
> 執行 `lint wiki` 可全面健檢知識庫完整性（17 項檢查）。
