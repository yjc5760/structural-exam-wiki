# 結構工程技師考試知識庫（五科合一）

> 本檔是**身份層**：分工、資料流、資料夾結構、重要規則。五科共用。
> 文中 `XX` 代表科目代碼（`SS`／`RC`／`SA`／`SD`／`SM`），各科專屬設定見 `XX/SUBJECT.md`。

## 專案說明

收錄「專門職業及技術人員高等考試結構工程技師」各科考古題的深度解析知識庫。
原本各科獨立建庫（exam-wiki-SS 等），2026-10-29 起合併為單一知識庫：**架構相同、各科一個資料夾**。

| 代碼 | 科目 | 資料夾 | 考卷檔名 |
|:---:|------|--------|---------|
| SS | 鋼結構設計 | `SS/` | `SS-YYYY_鋼結構設計.pdf` |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `RC/` | `RC-YYYY_鋼筋混凝土設計與預力混凝土設計.pdf` |
| SA | 結構學 | `SA/` | `SA-YYYY_結構學.pdf` |
| SD | 結構動力分析與耐震設計 | `SD/` | `SD-YYYY_結構動力分析與耐震設計.pdf` |
| SM | 土壤力學與基礎設計 | `SM/` | `SM-YYYY_土壤力學與基礎設計.pdf` |

> 命題大綱另有 `MM`（材料力學），目前未建資料夾；SS 有題目以 `MM-U1-1` 為副考點。
> 要新增科目：在 `scripts/subject_profiles.json` 補設定後執行 `python scripts/scaffold_subject.py MM`。

- **題目編號格式：** `XX-YYYY-N`（如 `SS-2015-1`、`RC-2020-3`）
- **科目判定：** 指令中題號的前兩碼即科目；只說「解析 2024 年考卷」而未指明科目時，先問是哪一科
- **路徑慣例：** 本文件與 CLAUDE-CODE／SOLVE／SPEC 中的 `raw/`、`wiki/`、`study/` 一律指 **`XX/` 底下**的路徑

**核心工作流程：**
```
在 Cowork 開啟知識庫根目錄（Project）
    ↓
說：「解析 YYYY 年 XX 考卷」
Cowork 讀取 CLAUDE.md + XX/SUBJECT.md + 考卷 PDF + XX/raw/json/question_index.json
  → 建立所有尚無解析的題目資料夾（已有解析者跳過）
  → 提醒你將各題附圖截圖存入對應資料夾
  → 等待你通知「截圖完成，請開始解題」
    ↓
【你做】依提醒截圖存檔，完成後告知 Cowork
    ↓
【重要】Cowork 一次只解一題，解完存檔後再繼續下一題
    ↓
你加入補充截圖（chart/eqn/hand）
請 Cowork 更新 question_index.json（tags、verified）
    ↓
說：「ingest XX-YYYY-N」→ Cowork 直接執行，該科 wiki 自動更新
```

---

## 兩個環境分工

| 環境 | 負責什麼 |
|------|---------|
| **你（使用者）** | PDF 題目附圖截圖（fig-N.png）、chart/eqn/hand 補充截圖、人工驗算後通知 Cowork 更新 verificationStatus |
| **Cowork** | 解題（SOLVE，**一次一題**）、存檔（.md；需要圖解時以 struct-diagram 產生 figs/）、更新 question_index.json、**所有 wiki 操作指令**（ingest / compile-all / lint / status / reindex / add-concept / add-method / refresh-dashboard / frequency / analyze / predict / study / find / related / unverified / query，共 16 個，詳見 CLAUDE-CODE.md）、直接維護 wiki/diagnosis/ · wiki/failure-modes/ · wiki/materials/ · wiki/code-ref/ · wiki/queries/ · study/、**修正 raw/solutions/methods/ 的公式錯誤**（須驗算＋同步 wiki＋記 log） |

---

## 單向資料流（每科各自一套，互不寫入）

```
XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md ──→ XX/wiki/problems/      （ingest）
XX/raw/json/concepts.json               ──→ XX/wiki/concepts/      （compile-all）
XX/raw/solutions/methods/               ──→ XX/wiki/methods/       （compile-all）
   ↑ 修正公式錯誤時改「這一端」，不要只改 wiki 副本（否則下次 compile 會被蓋回）
XX/raw/json/question_index.json         ──→ XX/dashboard-data.js   （更新儀表板資料）
Cowork 查詢結果                         ──→ XX/wiki/queries/       （直接存入）
Cowork study／教材 skill 輸出           ──→ XX/study/              （直接存入）
Cowork 跨層知識工具                     ──→ XX/wiki/diagnosis/ · failure-modes/ · materials/ · code-ref/

根目錄 syllabus_taxonomy.json（唯一正本）──→ XX/raw/json/syllabus_taxonomy.json（副本，scripts/sync_taxonomy.py）

解題內容唯一來源：XX/raw/solutions/ 下的 .md 檔案
索引資訊唯一來源：XX/raw/json/question_index.json
命題大綱唯一來源：根目錄 syllabus_taxonomy.json（來自根目錄 命題大綱.pdf）
科目專屬設定唯一來源：scripts/subject_profiles.json ↔ XX/SUBJECT.md（兩者同步維護）
```

> **跨科題目**：題目只放在它所屬考卷的科目資料夾。他科子項只能出現在
> `secondaryTopicIds`（例：SS 題掛 `SD-U3-1`），不要把題目複製到他科。

---

## 資料夾結構

```
（知識庫根目錄）
├── README.md                ← 冷啟動導覽（五科總覽）
├── CLAUDE.md                ← 本檔（身份層）
├── CLAUDE-SOLVE.md          ← 指向 skills/exam-solve（解題流程已改為 skill）
├── CLAUDE-CODE.md           ← 16 個指令 Runbook
├── CLAUDE-SPEC.md           ← 格式／命名／完成標準
├── index.html               ← 五科入口頁（GitHub Pages 首頁）
├── syllabus_taxonomy.json   ← ⭐ 命題大綱分類正本（XX-Un-m）
├── 命題大綱.pdf              ← 考選部命題大綱原件
├── scripts/
│   ├── subject_profiles.json   ← 科目專屬設定（考卷檔名、designMethod、常見圖解、七層類別）
│   ├── scaffold_subject.py     ← 建立新科目骨架（不覆蓋既有檔）
│   ├── refresh_dashboard.py    ← 「更新儀表板資料」的實作
│   ├── sync_taxonomy.py        ← 正本 → 各科副本
│   ├── xcheck.py               ← 跨檔一致性掃描（python scripts/xcheck.py XX）
│   └── templates/dashboard-index.html ← 五科共用儀表板樣板
├── skills/                  ← 配套 Cowork Skills 原始碼與 .skill 打包檔（五科通用；含 exam-solve、exam-errata）
│
├── SS/ RC/ SA/ SD/ SM/      ← 各科資料夾，結構完全相同：
│   ├── SUBJECT.md               ← 科目層設定＋科目 CHANGELOG
│   ├── README.md · 檔案架構索引表.md
│   ├── index.html · dashboard-data.js   ← 科目儀表板
│   ├── scripts/build_frequency.py
│   ├── raw/                     ← 原始資料（預設唯讀，例外見規則 1）
│   │   ├── exams/               ← XX-YYYY_<科目名>.pdf
│   │   ├── json/                ← question_index.json ✏️、concepts.json、syllabus_taxonomy.json（副本）
│   │   └── solutions/
│   │       ├── XX-YYYY-N/       ← 🔒 證據（.md 僅限勘誤，見規則 1）
│   │       └── methods/         ← ✏️ 方法論
│   ├── study/                   ← lecture-／formula-given-／study-／frequency- 教材、problems-view/、assets/katex/
│   └── wiki/                    ← 七層知識庫（見下）
```

---

## 知識分類骨架（七層，五科共用資料夾名稱）

| 層 | 目錄 | 維護者 | 內容 |
|----|------|:------:|------|
| Layer 1 | `concepts/` + `problems/` | Cowork (ingest/compile) | 核心概念與題目頁 |
| Layer 2 | `philosophy/` | Cowork (compile-all) | 設計／分析哲學（各題型解題邏輯的「為什麼」） |
| Layer 3 | `methods/` | Cowork (compile-all) | 解題方法論 |
| Layer 4 | `diagnosis/` | Cowork (直接存入) | 題型診斷決策樹 |
| Layer 5 | `failure-modes/` | Cowork (直接存入) | 失敗模式（SA 解讀為「行為模式與判斷」） |
| Layer 6 | `materials/` | Cowork (直接存入) | 材料行為（SA＝勁度與基本假設、SM＝土壤行為） |
| Layer 7 | `code-ref/` | Cowork (直接存入) | 規範條文對應（SA＝定理與原理出處） |

> Layer 5–7 的**資料夾名稱五科一致**（skills 與 LINT 依名稱運作），各科的顯示名稱與類別頁定義在 `XX/SUBJECT.md` §5。
> 另有 `traps/`（陷阱，compile-all）、`topics/`（命題大綱分類頁）、`queries/`（查詢存檔）。

---

## 命題大綱分類

> topicId 格式：`XX-Un-m`（U = 單元號，m = 子項號），合法值以根目錄 `syllabus_taxonomy.json` 為準，
> 各科子項表見 `XX/SUBJECT.md` §2。
> `primaryTopicId` 填最主要考點；跨子項（含跨科）時用 `secondaryTopicIds` 列出。

---

## 重要規則

1. **`XX/raw/` 目錄下所有檔案一律不可修改**，僅以下四處例外：
   - `XX/raw/json/question_index.json`（索引唯一人工維護處）
   - `XX/raw/json/syllabus_taxonomy.json`（**只能**由 `scripts/sync_taxonomy.py` 從根目錄正本覆寫，不可手改）
   - `XX/raw/solutions/methods/`（方法論文件，可修正公式錯誤與單位標註）
   - `XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md`（**個別題目解析，僅限「解析勘誤」**，見下方條件）

   > **為什麼 methods/ 是例外**：本規則要保護的是**證據**（考卷、AI 解析、驗證過的答案），
   > 這些一旦被改就失去可追溯性。但 `raw/solutions/methods/` 存的是**可維護的知識整理**，
   > 且它是 `wiki/methods/` 的 compile 來源 —— 只改 wiki 副本的話，下次 `compile-all` 會被蓋回舊版。
   >
   > **修改 methods/ 的三個條件（缺一不可）**：
   > ① 修正前先做**數值驗算**（邊界代入、量綱檢查、與驗證解答交叉比對），不可憑印象改；
   > ② 改完**同步覆蓋** `wiki/methods/` 對應檔；
   > ③ 在該科 `wiki/log.md` 記錄**改了什麼、為什麼、怎麼驗證的**。
   >
   > **為什麼「解析勘誤」是例外**：本規則要保護的是**可追溯性**，不是保護錯誤。
   > `raw/solutions/XX-YYYY-N/XX-YYYY-N.md` 是解題內容的**唯一正本**，
   > `wiki/problems/` 與 `study/problems-view/` 都由它生成 —— 只改下游副本，
   > 下次 `ingest` 會被蓋回錯誤版本，等於錯誤永久留存。
   >
   > ⚠️ **教訓（SS，2026-07-30／08-22）**：VERIFY 已查出 `SS-2013-2.md` 的量級筆誤，卻因舊條文
   > 「不在例外內」而不敢修；該檔後續被查出把考卷原文「柱 CD 為**靠桿**」讀成「鉸接」，挫屈載重高估約 3 倍。
   > **規則不該讓已知錯誤留在正本裡。**
   >
   > **修改 `XX-YYYY-N.md` 的四個條件（缺一不可）**（執行步驟見 `skills/exam-errata/SKILL.md`）：
   > ① **回考卷原文**：以 `raw/exams/` 的 PDF 為準重新判讀題意與圖說。
   >    ⚠️ 考卷常為 Adobe-CNS1 CID 字型，`pdftotext` **抽不到中文**，公式與附表也常以影像嵌入；
   >    支承符號、鉸接圓圈、尺寸線只能目視 —— 必須轉圖（300–450 dpi）**逐頁目視判讀**；
   > ② **數值獨立重算**：每個數字以程式重算，並做量綱檢查與雙路徑交叉驗算，不可憑印象改；
   > ③ **同步全部下游**：`wiki/problems/`、`study/problems-view/`、該題 `figs/`（重跑 `gen_XX-YYYY-N.py`）、
   >    `raw/json/question_index.json`（tags）、必要時 `dashboard-data.js` 與 `study/study-*.html`；
   > ④ 在該科 `wiki/log.md` 記錄**改了什麼、為什麼錯、怎麼驗證的**，並在 .md 頁尾加「修正日期」。
   >
   > **不在例外內（仍完整受保護）**：`raw/exams/`（考卷原件）、同資料夾的
   > `-fig-*.png`／`-chart-*.png`／`-eqn-*.png`／`-hand-*.png`（使用者截圖證據）、
   > 使用者放入的補充筆記 `*.pdf`。勘誤只准動 `.md` 正本與 Cowork 自己生成的 `gen_XX-YYYY-N.py`、`figs/`（SS 的舊 `*-viz.html` 為停用舊檔，不再修改）。
   >
   > **驗證狀態連動**：解析一經勘誤，該題 `verificationStatus` 必須退回 `unverified`，
   > 由使用者人工複核後才可改回 `verified`（規則 5）。

2. **`verifiedSolution` 是最終答案，不可質疑或重新計算**
   > 界線：本條保護的是**已人工驗算確認**（`verificationStatus = "verified"`）的答案。
   > 當使用者明示要求勘誤、或該題已退回 `unverified` 時，本條不阻止重新計算。
3. **各科 `wiki/log.md` 只可 append，不可刪除已有紀錄**；影響多科或根目錄的變更記在根目錄 CHANGELOG（本檔末）
4. **wiki/ 大多數目錄是 compile 輸出，不可手動修改**；例外：diagnosis/ · failure-modes/ · materials/ · code-ref/ · queries/ 由 Cowork 直接維護
5. **ingest 前必須確認 verificationStatus = "verified"**
6. 概念連結使用 `[[concept_id]]`（Obsidian 相容）；概念 ID 在**同一科內**唯一，跨科同名概念各自建頁
7. 每次 ingest 同時更新該科 `wiki/index.md` 和 `wiki/by-year.md`
8. **格式與命名規範見 CLAUDE-SPEC.md；操作指令（16 項）見 CLAUDE-CODE.md，全部由 Cowork 執行**
9. **一個指令只動一科**：除非使用者明說跨科（例：「五科一起更新儀表板」），不要順手修改他科資料夾
10. **科目專屬設定改兩處**：改 designMethod 允許值、常見圖解、七層類別時，`scripts/subject_profiles.json` 與 `XX/SUBJECT.md` 必須同步

---

## CHANGELOG（根目錄／跨科）

> 各科自己的變更紀錄在 `XX/SUBJECT.md` §9（SS 在 2026-10-29 以前的完整紀錄已移至 `SS/SUBJECT.md`）。

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | **五科合併為單一知識庫**：根目錄 CLAUDE／CODE／SOLVE／SPEC／README 改寫為五科通用（`XX` 代號）；SS 專屬內容（CHANGELOG、設計哲學框架、互動圖內容碼）移入 `SS/SUBJECT.md`；依 SS 架構以 `scripts/scaffold_subject.py` 建立 RC／SA／SD／SM 骨架；`syllabus_taxonomy.json` 以根目錄為正本、各科 `raw/json/` 放同步副本；儀表板改為五科共用樣板（`KB_SUBJECT` 驅動）並新增根目錄五科入口頁；`skills/` 與 `xcheck.py` 移至根目錄共用；改為單一 git repo | 五科架構相同、只有考古題不同，分開維護使同一條規則要改五次 |
| 2026-10-29 | **解題與勘誤流程改為 skill**：新增 `skills/exam-solve/`（原 CLAUDE-SOLVE.md 的 SOLVE 流程＋CLAUDE-SPEC.md §4.1 完成檢核）與 `skills/exam-errata/`（規則 1 解析勘誤四條件的執行流程＋xcheck 分診）；CLAUDE-SOLVE.md 改為索引頁，ADD-METHOD 移入 CLAUDE-CODE.md；CLAUDE-CODE.md 新增「由 skill 負責的流程」對照表 | 只在解題／勘誤時才需要的長流程不必每次常駐；規則仍留在 CLAUDE.md，格式仍以 CLAUDE-SPEC.md 為唯一依據 |
| 2026-10-29 | **停用互動圖（`*-viz.html`）**：圖解一律由 `struct-diagram` skill 產生靜態 SVG＋PNG（`figs/`＋`gen_XX-YYYY-N.py`），exam-solve 解完一題後提議、exam-errata 勘誤後重跑；規則 1 的勘誤例外由 `*-viz.html` 改為 `gen_*.py`／`figs/`；SS 既有 19 份 viz 保留為舊檔 | 互動圖與 struct-diagram 功能重疊；靜態圖可重跑、可審核、可進 PDF 與影片管線 |
