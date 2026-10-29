# SM 科目設定（SUBJECT.md）— 土壤力學與基礎設計

> 本檔是 **SM 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SOLVE.md`／`CLAUDE-SPEC.md` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`SM`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `SM`（Soil Mechanics & Foundation Design） |
| 科目全名 | 土壤力學與基礎設計 |
| 題號格式 | `SM-YYYY-N`（YYYY 為西元年，例 `SM-2015-1`） |
| 考卷檔名 | `raw/exams/SM-YYYY_土壤力學與基礎設計.pdf` |
| 收錄範圍 | 尚未收錄（考卷放入 `raw/exams/` 後開始） |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立，2026-10-29 |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 |
|---------|------|------|
| `SM-U1-1` | 土壤基本性質 | 第一單元 |
| `SM-U1-2` | 土壤滲透 | 第一單元 |
| `SM-U1-3` | 土壤夯實及壓密 | 第一單元 |
| `SM-U1-4` | 土體內應力 | 第一單元 |
| `SM-U1-5` | 土壤強度特性與變形性 | 第一單元 |
| `SM-U2-1` | 淺基礎之支承力與沉陷量 | 第二單元 |
| `SM-U2-2` | 深基礎之支承力與沉陷量 | 第二單元 |
| `SM-U2-3` | 開挖之穩定性分析 | 第二單元 |
| `SM-U2-4` | 基礎型式之選擇與評估 | 第二單元 |
| `SM-U2-5` | 地層改良方法 | 第二單元 |
| `SM-U3-1` | 側向土壓力理論 | 第三單元 |
| `SM-U3-2` | 擋土結構物穩定分析 | 第三單元 |
| `SM-U3-3` | 坡地工程 | 第三單元 |
| `SM-U3-4` | 生態工法在邊坡工程之應用 | 第三單元 |

他科常見副考點：`RC-U3-2`

---

## 3. `designMethod` 欄位（本科分類軸：題型）

| 允許值 |
|--------|
| `分析計算` |
| `設計檢核` |
| `概念題` |
| `混合` |

> 分析計算＝求土壤性質、應力、沉陷、滲流量等；設計檢核＝基礎／擋土／邊坡安全係數或尺寸設計；概念題＝說明／比較題
>
> `unit-exam-intel` 的「設計法走向」區塊在本科改用上表的分類軸；儀表板篩選選項亦依此順序。

---

## 4. 互動圖內容碼（`*-viz.html`）

| 內容碼 | 圖形 | 檔名範例 |
|--------|------|---------|
| `flownet` | 流線網 | `SM-YYYY-N-flownet-viz.html` |
| `mohr` | 莫爾圓 | `SM-YYYY-N-mohr-viz.html` |
| `consolidation` | 壓密曲線／e-log σ' | `SM-YYYY-N-consolidation-viz.html` |
| `stress-dist` | 土中應力分布 | `SM-YYYY-N-stress-dist-viz.html` |
| `earth-pressure` | 側向土壓力分布 | `SM-YYYY-N-earth-pressure-viz.html` |
| `slope` | 邊坡滑動面 | `SM-YYYY-N-slope-viz.html` |

---

## 5. wiki 七層的本科解讀

Layer 1–4（concepts＋problems／philosophy／methods／diagnosis）五科相同；Layer 5–7 依科目性質調整，
**資料夾名稱維持不變**（skills 與 LINT 依資料夾名稱運作），只改顯示名稱與類別頁：

| 層 | 目錄 | 本科名稱 | 類別頁 |
|----|------|---------|--------|
| Layer 5 | `wiki/failure-modes/` | **失敗模式** | `bearing-failure` 支承力破壞（全面／局部／衝剪）<br>`settlement` 過量沉陷與差異沉陷<br>`seepage-failure` 滲流破壞（管湧、砂湧、上舉）<br>`excavation-failure` 開挖破壞（隆起、擋土失穩）<br>`slope-failure` 邊坡滑動<br>`liquefaction` 土壤液化 |
| Layer 6 | `wiki/materials/` | **土壤行為** | `phase-relations` 三相關係與分類<br>`effective-stress` 有效應力原理<br>`permeability` 滲透性<br>`consolidation-behavior` 壓密行為（正常／過壓密）<br>`shear-strength` 剪力強度（排水／不排水、膨脹／收縮） |
| Layer 7 | `wiki/code-ref/` | **規範條文對應** | （index.md 單頁） |

> LINT 第 14、15 項（類別頁齊全）以本表為準。

---

## 6. 題型診斷入口（`wiki/diagnosis/`）

| 題型 | 辨識關鍵字 | 診斷頁 |
|------|-----------|--------|
| 土壤基本性質 | 「含水量」「孔隙比」「阿太堡限度」「分類」 | `wiki/diagnosis/soil-properties.md` |
| 土壤滲透 | 「滲透係數」「流線網」「臨界水力坡降」 | `wiki/diagnosis/seepage.md` |
| 夯實與壓密 | 「最佳含水量」「壓密沉陷」「Cv」「Cc」 | `wiki/diagnosis/compaction-consolidation.md` |
| 土體內應力 | 「Boussinesq」「2:1 法」「應力增量」 | `wiki/diagnosis/stress-distribution.md` |
| 剪力強度 | 「三軸試驗」「直剪」「莫爾庫倫」「孔隙水壓參數」 | `wiki/diagnosis/shear-strength.md` |
| 淺基礎 | 「承載力」「Terzaghi」「偏心」「沉陷量」 | `wiki/diagnosis/shallow-foundation.md` |
| 深基礎 | 「樁」「摩擦樁」「群樁」「負摩擦力」 | `wiki/diagnosis/deep-foundation.md` |
| 開挖穩定 | 「隆起」「管湧」「支撐」「擋土壁」 | `wiki/diagnosis/excavation.md` |
| 側向土壓與擋土結構 | 「Rankine」「Coulomb」「滑動」「傾倒」 | `wiki/diagnosis/earth-pressure.md` |
| 坡地工程 | 「邊坡穩定」「切片法」「無限邊坡」「生態工法」 | `wiki/diagnosis/slope.md` |
| 地層改良 | 「地盤改良」「預壓」「灌漿」「排水帶」 | `wiki/diagnosis/ground-improvement.md` |

---

## 7. 主要規範／依據（Layer 7 的來源）

- 建築物基礎構造設計規範（內政部；以考卷年份適用版本為準）
- 水土保持技術規範（坡地工程）
- 公路橋梁設計規範（基礎相關章節）

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。

---

## 8. 設計哲學框架（解題邏輯起始版）

> 起始版只列各子項的主幹流程，隨題目解析累積後擴充；SOLVE 時與根目錄 `CLAUDE-SOLVE.md`
> 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。

**土壤基本性質（SM-U1-1）**
```
S·e = w·Gs；γ = (Gs + S·e) γw / (1 + e)；γ' = γsat − γw
先畫三相圖，再用已知量逐一補齊
```

**有效應力與滲流（SM-U1-2）**
```
σ' = σ − u；Darcy：q = k·i·A
流線網：q = k·H·Nf / Nd；臨界水力坡降 icr = γ' / γw（砂湧／管湧檢核）
```

**壓密（SM-U1-3）**
```
正常壓密：Sc = Cc·H / (1 + e0) · log(σ'f / σ'0)
過壓密：先以 Cs 算到 σ'c，再以 Cc 算超過的部分
時間：Tv = cv·t / Hdr²（雙向排水 Hdr = H/2）
```

**剪力強度（SM-U1-5）**
```
τf = c' + σ' tan φ'；三軸試驗依 UU／CU／CD 區分總應力與有效應力路徑
```

**淺基礎（SM-U2-1）**
```
qu = c·Nc·sc·dc·ic + q·Nq·sq·dq·iq + 0.5γ·B·Nγ·sγ·dγ·iγ
偏心：有效寬度 B' = B − 2e；地下水位修正 γ 與 q；FS = qu / q
```

**側向土壓與擋土結構（SM-U3-1、SM-U3-2）**
```
Rankine：Ka = tan²(45° − φ/2)、Kp = tan²(45° + φ/2)；Coulomb 考慮牆背摩擦
擋土牆：滑動 FS、傾倒 FS、基底承載力三項檢核
```

**邊坡（SM-U3-3）**
```
無限邊坡（無凝聚、無滲流）FS = tan φ / tan β；有限邊坡用切片法（Fellenius／Bishop）
```

---

## 9. CHANGELOG（SM 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
