# SM 土壤力學與基礎設計 知識庫

> **科目：** SM（結構工程技師高考）
> **題庫：** 96 題已 ingest（96 題已解析，2002–2025 年考卷已就位）
> **驗算狀態：** 96 題目前皆為 `unverified`（2026-08-28 依使用者指示全數翻回待驗算，以便修訂解析內容）
> **格式：** SM-YYYY-N（例：SM-2015-1）
> **操作指令：** 見 CLAUDE-CODE.md　｜　**解題規範：** 見 CLAUDE-SOLVE.md

---

## 七層知識架構

本知識庫依以下七層組織所有知識：

| 層 | 目錄 | 維護者 | 說明 |
|----|------|:------:|------|
| Layer 1 | [concepts/](concepts/) · [problems/](problems/) | Cowork (ingest/compile) | 核心概念定義 + 題目解析 |
| Layer 2 | [philosophy/](philosophy/) | Cowork (compile-all) | 設計哲學（總應力法／有效應力法／安全係數哲學） |
| Layer 3 | [methods/](methods/) | Cowork (compile-all) | 解題方法論（承載力公式／土壓力理論／邊坡穩定法） |
| Layer 4 | [diagnosis/](diagnosis/) | Cowork (直接存入) | 題型診斷決策樹 |
| Layer 5 | [failure-modes/](failure-modes/) | Cowork (直接存入) | 失敗模式（承載力破壞／過大沉陷／滲流破壞／邊坡滑動／擋土結構失穩） |
| Layer 6 | [materials/](materials/) | Cowork (直接存入) | 材料行為（土壤分類特性／滲透特性／壓密特性／剪力強度特性） |
| Layer 7 | [code-ref/](code-ref/) | Cowork (直接存入) | 規範條文對應（建築物基礎構造設計規範等） |

---

## 概念頁快速導覽（24 個核心種子概念）

### 第一單元（SM-U1）：土壤基本性質、滲透、夯實壓密、應力、強度

| 概念 ID | 概念名稱 | 分類 |
|---------|---------|------|
| [PHASE-RELATIONSHIP](concepts/PHASE-RELATIONSHIP.md) | 土壤三相關係 | SM-U1-1 |
| [ATTERBERG-LIMITS](concepts/ATTERBERG-LIMITS.md) | 阿太堡限度 | SM-U1-1 |
| [USCS-CLASSIFICATION](concepts/USCS-CLASSIFICATION.md) | 統一土壤分類系統 | SM-U1-1 |
| [DARCYS-LAW](concepts/DARCYS-LAW.md) | 達西定律 | SM-U1-2 |
| [FLOW-NET](concepts/FLOW-NET.md) | 流網分析 | SM-U1-2 |
| [COMPACTION-CURVE](concepts/COMPACTION-CURVE.md) | 夯實曲線 | SM-U1-3 |
| [CONSOLIDATION-THEORY](concepts/CONSOLIDATION-THEORY.md) | Terzaghi 一維壓密理論 | SM-U1-3 |
| [PRECONSOLIDATION-PRESSURE](concepts/PRECONSOLIDATION-PRESSURE.md) | 過壓密應力與超壓密比 | SM-U1-3 |
| [COEFFICIENT-OF-CONSOLIDATION](concepts/COEFFICIENT-OF-CONSOLIDATION.md) | 壓密係數與時間因數 | SM-U1-3 |
| [EFFECTIVE-STRESS-PRINCIPLE](concepts/EFFECTIVE-STRESS-PRINCIPLE.md) | 有效應力原理 | SM-U1-4 |
| [BOUSSINESQ-STRESS-INCREASE](concepts/BOUSSINESQ-STRESS-INCREASE.md) | Boussinesq 應力增量理論 | SM-U1-4 |
| [MOHR-COULOMB-FAILURE-CRITERION](concepts/MOHR-COULOMB-FAILURE-CRITERION.md) | Mohr-Coulomb 破壞準則 | SM-U1-5 |
| [UNDRAINED-SHEAR-STRENGTH](concepts/UNDRAINED-SHEAR-STRENGTH.md) | 不排水剪力強度 | SM-U1-5 |
| [TRIAXIAL-TEST-TYPES](concepts/TRIAXIAL-TEST-TYPES.md) | 三軸試驗分類 | SM-U1-5 |

### 第二單元（SM-U2）：淺基礎、深基礎、開挖、基礎型式、地層改良

| 概念 ID | 概念名稱 | 分類 |
|---------|---------|------|
| [BEARING-CAPACITY-THEORY](concepts/BEARING-CAPACITY-THEORY.md) | 淺基礎承載力理論 | SM-U2-1 |
| [SETTLEMENT-COMPONENTS](concepts/SETTLEMENT-COMPONENTS.md) | 瞬時沉陷與壓密沉陷 | SM-U2-1 |
| [PILE-CAPACITY-COMPONENTS](concepts/PILE-CAPACITY-COMPONENTS.md) | 樁基承載力組成 | SM-U2-2 |
| [PILE-GROUP-EFFICIENCY](concepts/PILE-GROUP-EFFICIENCY.md) | 群樁效應 | SM-U2-2 |
| [EXCAVATION-STABILITY](concepts/EXCAVATION-STABILITY.md) | 開挖穩定性 | SM-U2-3 |
| [GROUND-IMPROVEMENT-METHODS](concepts/GROUND-IMPROVEMENT-METHODS.md) | 地層改良方法 | SM-U2-5 |

### 第三單元（SM-U3）：側向土壓力、擋土結構、坡地工程、生態工法

| 概念 ID | 概念名稱 | 分類 |
|---------|---------|------|
| [RANKINE-EARTH-PRESSURE](concepts/RANKINE-EARTH-PRESSURE.md) | Rankine 土壓力理論 | SM-U3-1 |
| [COULOMB-EARTH-PRESSURE](concepts/COULOMB-EARTH-PRESSURE.md) | Coulomb 土壓力理論 | SM-U3-1 |
| [RETAINING-WALL-STABILITY](concepts/RETAINING-WALL-STABILITY.md) | 擋土結構穩定分析 | SM-U3-2 |
| [SLOPE-STABILITY-ANALYSIS](concepts/SLOPE-STABILITY-ANALYSIS.md) | 邊坡穩定分析 | SM-U3-3 |

---

## 題目頁（依命題大綱分類）

### 第一單元（SM-U1）

| topicId | 子項 | 題目 |
|---------|------|------|
| SM-U1-1 | 土壤基本性質 | [[SM-2023-1]] 名詞解釋<br>[[SM-2020-3]] 相對密度<br>[[SM-2019-1]] 含水量<br>[[SM-2016-2]] 三相關係<br>[[SM-2008-1]] 三相關係<br>[[SM-2007-1]] 三相關係<br>[[SM-2005-2]] 三相關係<br>[[SM-2004-1]] 三相關係<br>[[SM-2024-4]] 樁基承載力（副）<br>[[SM-2023-4]] 開挖穩定性（副）<br>[[SM-2020-1]] 有效應力原理（副）<br>[[SM-2019-3]] 相對夯實度（副）<br>[[SM-2014-4]] 壓密沉陷（副）<br>[[SM-2014-1]] 無限邊坡分析（副）<br>[[SM-2011-4]] 開挖穩定性（副）<br>[[SM-2011-1]] 零空氣孔隙曲線（副）<br>[[SM-2009-3]] 有效應力原理（副）<br>[[SM-2006-4]] 夯實曲線（副） |
| SM-U1-2 | 土壤滲透 | [[SM-2022-3]] Darcy定律<br>[[SM-2018-3]] 流網<br>[[SM-2011-2]] 流網<br>[[SM-2010-3]] 滲流力<br>[[SM-2024-2]] 無限邊坡分析（副）<br>[[SM-2021-1]] 有效應力原理（副）<br>[[SM-2020-2]] 板樁（副）<br>[[SM-2017-4]] 開挖穩定性（副）<br>[[SM-2015-4]] 抽水降階（副）<br>[[SM-2011-1]] 零空氣孔隙曲線（副）<br>[[SM-2009-3]] 有效應力原理（副）<br>[[SM-2009-1]] 夯實曲線（副）<br>[[SM-2007-2]] 流砂（副） |
| SM-U1-3 | 土壤夯實及壓密 | [[SM-2025-1]] Terzaghi壓密理論<br>[[SM-2024-3]] 地下水位下降<br>[[SM-2022-1]] 夯實試驗<br>[[SM-2021-2]] Terzaghi壓密理論<br>[[SM-2019-3]] 相對夯實度<br>[[SM-2019-2]] Terzaghi壓密理論<br>[[SM-2018-1]] Terzaghi壓密理論<br>[[SM-2017-2]] 夯實曲線<br>[[SM-2017-1]] 夯實曲線<br>[[SM-2016-1]] e-log p'曲線<br>[[SM-2015-4]] 抽水降階<br>[[SM-2015-1]] 壓密沉陷<br>[[SM-2014-4]] 壓密沉陷<br>[[SM-2013-2]] 夯實曲線<br>[[SM-2012-2]] 單向度壓密試驗<br>[[SM-2011-3]] 壓密沉陷<br>[[SM-2009-1]] 夯實曲線<br>[[SM-2006-4]] 夯實曲線<br>[[SM-2005-3]] 體積變化係數<br>[[SM-2003-2]] 壓密沉陷<br>[[SM-2002-3]] 夯實曲線<br>[[SM-2002-1]] 壓密沉陷<br>[[SM-2023-1]] 名詞解釋（副）<br>[[SM-2019-1]] 含水量（副）<br>[[SM-2016-2]] 三相關係（副）<br>[[SM-2011-1]] 零空氣孔隙曲線（副）<br>[[SM-2008-1]] 三相關係（副）<br>[[SM-2006-1]] Mohr-Coulomb破壞準則（副）<br>[[SM-2005-2]] 三相關係（副）<br>[[SM-2004-4]] 預壓法（副） |
| SM-U1-4 | 土體內應力 | [[SM-2025-4]] Boussinesq理論<br>[[SM-2021-1]] 有效應力原理<br>[[SM-2020-1]] 有效應力原理<br>[[SM-2009-3]] 有效應力原理<br>[[SM-2004-2]] 莫爾圓<br>[[SM-2024-3]] 地下水位下降（副）<br>[[SM-2016-1]] e-log p'曲線（副）<br>[[SM-2015-4]] 抽水降階（副）<br>[[SM-2012-1]] 三軸試驗（副）<br>[[SM-2011-3]] 壓密沉陷（副）<br>[[SM-2010-2]] Rankine主動土壓力（副）<br>[[SM-2010-1]] UU試驗（副）<br>[[SM-2008-2]] Skempton孔隙水壓參數（副）<br>[[SM-2007-2]] 流砂（副）<br>[[SM-2003-3]] 開挖穩定性（副）<br>[[SM-2003-2]] 壓密沉陷（副） |
| SM-U1-5 | 土壤強度特性與變形性 | [[SM-2025-2]] 三軸試驗<br>[[SM-2024-1]] 三軸試驗<br>[[SM-2018-2]] CU試驗<br>[[SM-2013-3]] 三軸試驗<br>[[SM-2012-1]] 三軸試驗<br>[[SM-2011-1]] 零空氣孔隙曲線<br>[[SM-2010-1]] UU試驗<br>[[SM-2008-2]] Skempton孔隙水壓參數<br>[[SM-2007-2]] 流砂<br>[[SM-2006-1]] Mohr-Coulomb破壞準則<br>[[SM-2003-4]] 正常壓密<br>[[SM-2002-4]] 正常壓密<br>[[SM-2019-1]] 含水量（副）<br>[[SM-2017-4]] 開挖穩定性（副）<br>[[SM-2008-3]] 開挖穩定性（副）<br>[[SM-2003-1]] 基地調查（副） |

### 第二單元（SM-U2）

| topicId | 子項 | 題目 |
|---------|------|------|
| SM-U2-1 | 淺基礎之支承力與沉陷量 | [[SM-2020-4]] Terzaghi承載力公式<br>[[SM-2017-3]] 平鈑載重試驗<br>[[SM-2010-4]] Meyerhof承載力公式<br>[[SM-2009-2]] 筏式基礎<br>[[SM-2016-4]] Coulomb土壓力（副）<br>[[SM-2016-3]] 加勁擋土結構（副）<br>[[SM-2011-3]] 壓密沉陷（副）<br>[[SM-2011-1]] 零空氣孔隙曲線（副）<br>[[SM-2004-4]] 預壓法（副）<br>[[SM-2003-2]] 壓密沉陷（副） |
| SM-U2-2 | 深基礎之支承力與沉陷量 | [[SM-2024-4]] 樁基承載力<br>[[SM-2023-3]] 打入樁<br>[[SM-2021-3]] 樁基承載力<br>[[SM-2014-2]] 樁沉陷<br>[[SM-2012-3]] 樁基承載力<br>[[SM-2007-3]] 樁基承載力<br>[[SM-2006-2]] 摩擦樁<br>[[SM-2005-4]] 墩基<br>[[SM-2019-1]] 含水量（副）<br>[[SM-2013-4]] 土壤液化（副）<br>[[SM-2013-1]] 加勁擋土結構（副） |
| SM-U2-3 | 開挖之穩定性分析 | [[SM-2023-4]] 開挖穩定性<br>[[SM-2022-4]] 板樁<br>[[SM-2020-2]] 板樁<br>[[SM-2017-4]] 開挖穩定性<br>[[SM-2015-3]] 開挖穩定性<br>[[SM-2014-3]] 開挖穩定性<br>[[SM-2012-4]] 開挖穩定性<br>[[SM-2011-4]] 開挖穩定性<br>[[SM-2008-3]] 開挖穩定性<br>[[SM-2007-4]] 板樁<br>[[SM-2005-1]] 板樁<br>[[SM-2003-3]] 開挖穩定性<br>[[SM-2011-2]] 流網（副）<br>[[SM-2010-3]] 滲流力（副）<br>[[SM-2009-2]] 筏式基礎（副）<br>[[SM-2006-3]] 側向滑動（副）<br>[[SM-2003-1]] 基地調查（副） |
| SM-U2-4 | 基礎型式之選擇與評估 | [[SM-2013-4]] 土壤液化<br>[[SM-2004-4]] 預壓法<br>[[SM-2003-1]] 基地調查<br>[[SM-2002-2]] 液化防治（副） |
| SM-U2-5 | 地層改良方法 | [[SM-2002-2]] 液化防治<br>[[SM-2023-4]] 開挖穩定性（副）<br>[[SM-2019-2]] Terzaghi壓密理論（副）<br>[[SM-2015-1]] 壓密沉陷（副）<br>[[SM-2013-4]] 土壤液化（副）<br>[[SM-2008-3]] 開挖穩定性（副）<br>[[SM-2004-4]] 預壓法（副） |

### 第三單元（SM-U3）

| topicId | 子項 | 題目 |
|---------|------|------|
| SM-U3-1 | 側向土壓力理論 | [[SM-2019-4]] Coulomb土壓力<br>[[SM-2015-2]] Rankine主動土壓力<br>[[SM-2010-2]] Rankine主動土壓力<br>[[SM-2004-3]] Rankine主動土壓力<br>[[SM-2025-3]] 重力式擋土牆（副）<br>[[SM-2022-4]] 板樁（副）<br>[[SM-2020-2]] 板樁（副）<br>[[SM-2018-4]] 懸臂式擋土牆（副）<br>[[SM-2016-4]] Coulomb土壓力（副）<br>[[SM-2016-3]] 加勁擋土結構（副）<br>[[SM-2014-3]] 開挖穩定性（副）<br>[[SM-2013-1]] 加勁擋土結構（副）<br>[[SM-2009-4]] 重力式擋土牆（副）<br>[[SM-2008-3]] 開挖穩定性（副）<br>[[SM-2007-4]] 板樁（副）<br>[[SM-2006-3]] 側向滑動（副）<br>[[SM-2005-1]] 板樁（副） |
| SM-U3-2 | 擋土結構物穩定分析 | [[SM-2025-3]] 重力式擋土牆<br>[[SM-2022-2]] 加勁擋土結構<br>[[SM-2018-4]] 懸臂式擋土牆<br>[[SM-2016-4]] Coulomb土壓力<br>[[SM-2016-3]] 加勁擋土結構<br>[[SM-2013-1]] 加勁擋土結構<br>[[SM-2009-4]] 重力式擋土牆<br>[[SM-2015-2]] Rankine主動土壓力（副）<br>[[SM-2004-3]] Rankine主動土壓力（副） |
| SM-U3-3 | 坡地工程 | [[SM-2024-2]] 無限邊坡分析<br>[[SM-2023-2]] 邊坡穩定<br>[[SM-2021-4]] Fellenius法<br>[[SM-2014-1]] 無限邊坡分析<br>[[SM-2008-4]] 平面滑動分析<br>[[SM-2006-3]] 側向滑動<br>[[SM-2013-1]] 加勁擋土結構（副） |
| SM-U3-4 | 生態工法在邊坡工程之應用 | _尚無_ |

> 每次 `ingest SM-XXXX-N` 後，Cowork 會在對應子項下方加入題目連結（格式：`[[SM-YYYY-N]] — 核心考點`）。此表由 `compile-all` 依 `question_index.json` 自動生成。

---

## 其他導航

- [by-year.md](by-year.md) — 依考年瀏覽
- [log.md](log.md) — 操作紀錄（append only）
- [diagnosis/index.md](diagnosis/index.md) — 題型診斷決策樹
- [failure-modes/index.md](failure-modes/index.md) — 失敗模式分類
- [materials/index.md](materials/index.md) — 材料行為
- [code-ref/index.md](code-ref/index.md) — 規範條文對應
- [methods/index.md](methods/index.md) — 解題方法論
- [traps/index.md](traps/index.md) — 陷阱頁（補充目錄）
- [queries/index.md](queries/index.md) — 查詢結果存檔
- [philosophy/index.md](philosophy/index.md) — 設計哲學頁
