# SD 科目設定（SUBJECT.md）— 結構動力分析與耐震設計

> 本檔是 **SD 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SOLVE.md`／`CLAUDE-SPEC.md` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`SD`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `SD`（Structural Dynamics & Seismic Design） |
| 科目全名 | 結構動力分析與耐震設計 |
| 題號格式 | `SD-YYYY-N`（YYYY 為西元年，例 `SD-2015-1`） |
| 考卷檔名 | `raw/exams/SD-YYYY_結構動力分析與耐震設計.pdf` |
| 收錄範圍 | 尚未收錄（考卷放入 `raw/exams/` 後開始） |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立，2026-10-29 |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 |
|---------|------|------|
| `SD-U1-1` | 結構動力基本性質及原理 | 第一單元 |
| `SD-U1-2` | 運動方程式推導 | 第一單元 |
| `SD-U1-3` | 單自由度、多自由度系統之動態分析及應用 | 第一單元 |
| `SD-U2-1` | 地震力之設計規範 | 第二單元 |
| `SD-U2-2` | 建築耐震設計規範 | 第二單元 |
| `SD-U2-3` | 橋梁耐震設計規範 | 第二單元 |
| `SD-U3-1` | 結構耐震設計（含 RC 結構與鋼結構） | 第三單元 |
| `SD-U3-2` | 隔減震原理 | 第三單元 |

他科常見副考點：`SA-U2-4`、`RC-U3-3`、`SS-U1-4`

---

## 3. `designMethod` 欄位（本科分類軸：題型）

| 允許值 |
|--------|
| `動力分析` |
| `規範計算` |
| `概念題` |
| `混合` |

> 動力分析＝運動方程式、自由／強制振動、振態疊加等計算；規範計算＝依耐震規範計算地震力或檢核；概念題＝說明／比較題
>
> `unit-exam-intel` 的「設計法走向」區塊在本科改用上表的分類軸；儀表板篩選選項亦依此順序。

---

## 4. 互動圖內容碼（`*-viz.html`）

| 內容碼 | 圖形 | 檔名範例 |
|--------|------|---------|
| `response` | 時間歷程反應 | `SD-YYYY-N-response-viz.html` |
| `spectrum` | 反應譜／設計譜 | `SD-YYYY-N-spectrum-viz.html` |
| `mode` | 振態形狀 | `SD-YYYY-N-mode-viz.html` |
| `frf` | 動力放大係數／頻率反應 | `SD-YYYY-N-frf-viz.html` |

---

## 5. wiki 七層的本科解讀

Layer 1–4（concepts＋problems／philosophy／methods／diagnosis）五科相同；Layer 5–7 依科目性質調整，
**資料夾名稱維持不變**（skills 與 LINT 依資料夾名稱運作），只改顯示名稱與類別頁：

| 層 | 目錄 | 本科名稱 | 類別頁 |
|----|------|---------|--------|
| Layer 5 | `wiki/failure-modes/` | **失敗模式** | `resonance` 共振與動力放大<br>`irregularity` 平面／立面不規則（軟層、弱層、扭轉）<br>`brittle-failure` 脆性破壞（短柱剪力、接頭、錨定）<br>`site-effects` 場址效應（土壤放大、液化、近斷層） |
| Layer 6 | `wiki/materials/` | **材料與構件行為** | `hysteresis` 遲滯行為與消能<br>`damping` 阻尼（黏滯、等效、Rayleigh）<br>`ductility` 韌性、R 與 Fu 的關係<br>`isolation-devices` 隔震與消能元件 |
| Layer 7 | `wiki/code-ref/` | **規範條文對應** | （index.md 單頁） |

> LINT 第 14、15 項（類別頁齊全）以本表為準。

---

## 6. 題型診斷入口（`wiki/diagnosis/`）

| 題型 | 辨識關鍵字 | 診斷頁 |
|------|-----------|--------|
| 單自由度自由振動 | 「自然頻率」「阻尼比」「對數遞減」 | `wiki/diagnosis/sdof-free.md` |
| 單自由度強制振動 | 「簡諧載重」「衝擊」「Duhamel」「動力放大」 | `wiki/diagnosis/sdof-forced.md` |
| 運動方程式推導 | 「推導運動方程式」「廣義座標」「Lagrange」 | `wiki/diagnosis/eom.md` |
| 多自由度系統 | 「振態」「特徵值」「振態疊加」「參與因子」 | `wiki/diagnosis/mdof.md` |
| 建築耐震規範計算 | 「設計地震力」「V」「SDS」「SD1」「Fu」「Ra」 | `wiki/diagnosis/building-code.md` |
| 橋梁耐震規範 | 「橋梁」「橋墩」「支承」「落橋」 | `wiki/diagnosis/bridge-code.md` |
| 結構耐震設計 | 「韌性構架」「強柱弱梁」「容量設計」 | `wiki/diagnosis/seismic-design.md` |
| 隔減震 | 「隔震」「消能」「阻尼器」「週期延長」 | `wiki/diagnosis/isolation.md` |

---

## 7. 主要規範／依據（Layer 7 的來源）

- 建築物耐震設計規範及解說（內政部；以考卷年份適用版本為準）
- 公路橋梁耐震設計規範（交通部）
- 建築物隔震與消能相關章節

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。

---

## 8. 設計哲學框架（解題邏輯起始版）

> 起始版只列各子項的主幹流程，隨題目解析累積後擴充；SOLVE 時與根目錄 `CLAUDE-SOLVE.md`
> 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。

**單自由度系統（SD-U1-1、SD-U1-3）**
```
運動方程式：m ü + c u̇ + k u = p(t)
ωn = √(k/m)；ζ = c / (2 m ωn)；ωD = ωn √(1 − ζ²)
簡諧載重：動力放大係數 Rd = 1 / √[(1 − r²)² + (2ζr)²]，r = ω/ωn
一般載重：Duhamel 積分；衝擊／脈衝載重：最大反應（衝擊譜）
```

**運動方程式推導（SD-U1-2）**
```
選廣義座標 → 寫出動能 T、位能 V、非保守力虛功 → Lagrange 方程或虛功原理
等效質量、等效勁度、等效載重要在同一個廣義座標上一致
```

**多自由度系統（SD-U1-3）**
```
(K − ω²M) φ = 0 → 振態頻率與振態；振態對 M、K 正交
振態疊加：Γn = φnᵀ M ι / φnᵀ M φn；反應譜各振態最大值以 SRSS／CQC 組合
```

**建築耐震設計規範（SD-U2-2）**
```
工址 → SDS、SD1（含場址放大）→ 基本振動週期 T → 設計譜 SaD
結構系統 → R → Ra → Fu；用途係數 I
V = (SaD·I / (1.4 αy Fu))m · W（依考卷年份規範版本的修正與下限規定）
→ 豎向分配 Fx → 層間變位、意外扭矩、垂直不規則等檢核
```

**隔減震（SD-U3-2）**
```
隔震：延長週期、增加阻尼 → 降低上部結構加速度，代價是隔震層位移變大
消能：以遲滯或黏滯元件吸收能量，提高等效阻尼比
```

---

## 9. CHANGELOG（SD 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
