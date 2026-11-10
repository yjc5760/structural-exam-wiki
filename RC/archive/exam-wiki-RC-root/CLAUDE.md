# 結構工程技師考試知識庫 — 鋼筋混凝土設計與預力（RC）

> 科目代碼：RC｜資料夾：`exam-wiki-RC`｜其他科目另建獨立資料庫

## 專案說明

本資料庫專門收錄「專門職業及技術人員高等考試結構工程技師」**第三科：鋼筋混凝土設計與預力**的考古題解析知識庫。

- **科目代碼：** RC（Reinforced Concrete Design and Prestress）
- **題目編號格式：** RC-YYYY-N（如 RC-2015-1）
- **其他科目：** 各自建立獨立資料庫（exam-wiki-SS、exam-wiki-SM 等）

**核心工作流程：**
```
在 Cowork 開啟 exam-wiki-RC/ 資料夾（Project）
    ↓
說：「解析 XXXX 年考卷」
Cowork 讀取 CLAUDE.md + 考卷 PDF + question_index.json
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
（ingest 已停用（2026-11-01 wiki 封存）；驗算後直接以 raw/solutions/ 正本與 study/ 教材為準）
```

---

## 兩個環境分工

| 環境 | 負責什麼 |
|------|---------|
| **你（使用者）** | PDF 題目附圖截圖（fig-N.png）、chart/eqn/hand 補充截圖、人工驗算後通知 Cowork 更新 verificationStatus |
| **Cowork** | 解題（SOLVE，**一次一題**）、存檔（.md）、更新 question_index.json、**操作指令**（詳見 CLAUDE-CODE.md；寫入 wiki 的 ingest / compile-all / lint / add-concept 已停用（2026-11-01 wiki 封存））、直接維護 wiki/queries/ · study/（study 指令輸出） |

---

## 單向資料流

```
raw/solutions/RC-XXXX-N/RC-XXXX-N.md  ──→  study/（problems-view、講義、單元總覽）
Cowork 查詢／稽核結果                  ──→  wiki/queries/       （Cowork 直接存入）
Cowork study 指令輸出                  ──→  study/              （Cowork 直接存入）

（2026-11-01 起 wiki/ 只保留 queries/；problems/ concepts/ methods/ traps/ philosophy/
 diagnosis/ failure-modes/ materials/ code-ref/ index.md by-year.md 封存至 archive/wiki/，
 不再 ingest／compile，僅供參考，見 archive/README.md）

解題內容唯一來源：raw/solutions/ 下的 .md 檔案
索引資訊唯一來源：raw/json/question_index.json
方法論唯一來源：raw/solutions/methods/（可修正，須驗算＋記 log，見規則 1）
wiki/queries/、study/（study 輸出）：由 Cowork 直接寫入
```

---

## 資料夾結構

```
exam-wiki-RC/
├── README.md                        ← 冷啟動快速導覽
├── CLAUDE.md                        ← 本檔（身份層：分工、資料流、重要規則）
├── CLAUDE-SOLVE.md                  ← Cowork 解題 Skill
├── CLAUDE-CODE.md                   ← Claude Code 操作指令（Runbook）
├── CLAUDE-SPEC.md                   ← 規格驗證層（格式、命名、完成標準）
│
├── study/                           ← 讀書筆記與講義
│   ├── study-RC-UN.html             ← study 指令輸出（單元層級速查／複習頁）
│   ├── study-RC-UN-n.html           ← study 指令輸出（子項層級速查／複習頁）
│   ├── lecture-RC-UN-n.html/.pdf    ← unit-lecture skill 輸出（理解導向觀念講義，與 study 頁並存）
│   ├── formula-given-RC-UN-n.html/.pdf ← unit-formula-map skill 輸出（公式「給／背分界」盤點）
│   ├── RC-UN-n_*.pdf                ← 使用者放入的 Keynote／補充講義
│   └── assets/katex/                ← 離線 KaTeX（lecture 頁共用，勿刪）
│
├── raw/                             ← 所有原始資料（預設唯讀，僅 ✏️ 兩處可改）
│   ├── exams/                       ← 原始考卷 PDF（命名：RC-YYYY_鋼筋混凝土設計與預力.pdf）
│   ├── json/
│   │   ├── concepts.json            ← 概念定義（供 compile-all）
│   │   └── question_index.json      ← ⭐✏️ 題目總索引（唯一需要人工維護的 JSON）
│   └── solutions/                   ← AI 解析 + 補充截圖（每題一個資料夾）
│       ├── RC-YYYY-N/               ← 🔒 證據，不可修改（規則 1、2）
│       │   ├── RC-YYYY-N.md
│       │   ├── RC-YYYY-N-fig-1.png
│       │   └── figs/                    ← 程式產生之向量圖解（選用）
│       └── methods/                 ← ✏️ 解題方法論（可修正公式／單位，見規則 1）
│
├── wiki/
│   └── queries/                     ← 稽核與分析報告（Cowork 直接存入）
│       ├── index.md                 ← 報告目錄
│       └── log.md                   ← 操作紀錄（append only）
│
└── archive/
    ├── README.md                    ← 封存說明
    └── wiki/                        ← 2026-11-01 封存的舊 wiki（七層頁、index、by-year），不再維護
```

---

## 知識分類骨架（七層）

> ⚠️ 2026-11-01 起本節所列目錄已封存至 `archive/wiki/`，不再 compile／ingest，以下僅保留作為歷史說明。

Wiki 導航依七層知識架構組織（前三層由 Cowork 透過 compile-all/ingest 生成，後四層由 Cowork 直接維護）：

| 層 | 目錄 | 維護者 | 內容 |
|----|------|:------:|------|
| Layer 1 | `concepts/` + `problems/` | Cowork (ingest/compile) | 核心構件設計（梁/柱/板/基礎/預力） |
| Layer 2 | `philosophy/` | Cowork (compile-all) | 設計哲學與實務（強度折減/韌性/耐震） |
| Layer 3 | `methods/` | Cowork (compile-all) | 解題方法論（P-M互制/等效側力法/損失計算） |
| Layer 4 | `diagnosis/` | Cowork (直接存入) | 題型診斷決策樹 |
| Layer 5 | `failure-modes/` | Cowork (直接存入) | 失敗模式（彎曲/剪力/壓碎/撓度/裂縫） |
| Layer 6 | `materials/` | Cowork (直接存入) | 材料行為（混凝土應力應變/鋼筋降伏/潛變收縮） |
| Layer 7 | `code-ref/` | Cowork (直接存入) | 規範條文對應（ACI 318/CNS 1480/耐震規範） |

> **補充目錄 `wiki/traps/`：** 不屬於七層架構，由 compile-all 從題目解析萃取陷阱頁面，與 concepts/ 並列為輔助導航。

---

## 命題大綱分類（依官方命題大綱，93年3月公告）

> topicId 格式：`RC-UN-n`，U = 單元號，n = 子項號。
> `primaryTopicId` 填最主要考點；跨子項時用 `secondaryTopicIds` 列出。

### 第一單元（RC-U1）

| topicId | 命題大綱子項 |
|---------|------------|
| RC-U1-1 | RC 梁彎矩強度分析與設計 |
| RC-U1-2 | RC 柱強度分析與設計 |
| RC-U1-3 | 細長柱 |
| RC-U1-4 | 柱設計圖之應用 |

### 第二單元（RC-U2）

| topicId | 命題大綱子項 |
|---------|------------|
| RC-U2-1 | RC 剪力強度分析與設計 |
| RC-U2-2 | RC 扭力強度設計 |
| RC-U2-3 | 鋼筋錨定長度與斷點計算 |

### 第三單元（RC-U3）

| topicId | 命題大綱子項 |
|---------|------------|
| RC-U3-1 | 梁工作性要求（含撓度、裂縫） |
| RC-U3-2 | 樓版與基腳設計 |
| RC-U3-3 | 韌性要求與耐震設計 |

### 第四單元（RC-U4）

| topicId | 命題大綱子項 |
|---------|------------|
| RC-U4-1 | 預力梁斷面應力分析 |
| RC-U4-2 | 預力量與偏心量設計 |
| RC-U4-3 | 預力損失 |
| RC-U4-4 | 預力梁剪力分析與設計 |

---

## 重要規則

1. **`raw/` 目錄下所有檔案一律不可修改**，僅以下兩處例外：
   - `raw/json/question_index.json`（索引唯一人工維護處）
   - `raw/solutions/methods/`（方法論文件，可修正公式錯誤與單位標註）

   > **為什麼 methods/ 是例外**：本規則要保護的是**證據**（考卷、AI 解析、驗證過的答案），
   > 這些一旦被改就失去可追溯性。但 `raw/solutions/methods/` 存的是**可維護的知識整理**，
   > 且它是方法論的唯一來源（舊 `wiki/methods/` 已於 2026-11-01 封存至 archive/wiki/，不再同步）。
   > 發現公式或係數錯誤時，必須改 raw 來源才算根治。
   >
   > **修改 methods/ 的兩個條件（缺一不可）**：
   > ① 修正前先做**數值驗算**（邊界代入、量綱檢查、與驗證解答交叉比對），不可憑印象改；
   > ② 在 `wiki/queries/log.md` 記錄**改了什麼、為什麼、怎麼驗證的**。
   > （原「同步覆蓋 `wiki/methods/`」一項已隨 2026-11-01 wiki 封存取消）
   >
   > ⚠️ `raw/solutions/RC-YYYY-N/`（個別題目解析）**不在例外內**，仍受規則 1 與規則 2 保護。

2. **`verifiedSolution` 是最終答案，不可質疑或重新計算**
3. **`wiki/queries/log.md` 只可 append，不可刪除已有紀錄**
4. **wiki/ 只保留 queries/（Cowork 直接維護）**；`archive/wiki/` 為 2026-11-01 封存的舊 compile 輸出，不可修改、不再維護
5. **ingest 前必須確認 verificationStatus = "verified"**（ingest 已停用（2026-11-01 wiki 封存））
6. 概念連結使用 `[[concept_id]]`（Obsidian 相容）
7. ~~每次 ingest 同時更新 index.md 和 by-year.md~~（已停用（2026-11-01 wiki 封存））
8. **格式與命名規範見 CLAUDE-SPEC.md；操作指令（ingest/compile/lint/status）見 CLAUDE-CODE.md，全部由 Cowork 執行**

---

## CHANGELOG

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-05-29 | 從 exam-wiki-SS 克隆，全面改寫為 RC 科目 | 建立鋼筋混凝土設計與預力獨立知識庫 |
| 2026-06-04 | 從三層架構（User/Cowork/Claude Code）改為兩層（User/Cowork） | 知識庫全程在 Cowork 運行，無獨立 Claude Code 終端機環境 |
| 2026-06-04 | Cowork 指令由 4 個擴充至 15 個（新增備考分析類、查詢快捷類、題庫維護類） | 增強備考分析與知識查詢功能 |
| 2026-06-08 | 修正 concepts.json classification 格式（RC-N → RC-UN-n）；修正 CLAUDE-SPEC.md §6 殘留 SS 類別代碼；更新 檔案架構索引表.md 快照數字；澄清 wiki/traps/ 補充目錄定位 | 知識庫 review 後修正 |
| 2026-06-11 | 新增 index.html + dashboard-data.js（離線儀表板：題庫篩選/統計/進度追蹤/指令速查）；指令由 15 個擴充至 16 個（新增 refresh-dashboard）；補完 lint SKIP 項掃描（hasViz/hasHandwritten/圖說均一致） | 建立使用者視覺化入口，提升知識庫易用性 |
| 2026-06-26 | study 指令輸出目錄從 wiki/queries/ 改為 study/；新增子項層級（study RC-UN-n）深度複習格式（七區塊：命題分析/截面圖解/解題流程/公式/考題清單/陷阱/互動計算） | 講義與複習頁集中在 study/ 管理，wiki/queries/ 保留純查詢結果 |
| 2026-06-30 | 修正 study 指令產生的考題連結路徑，改為直接連結至 `raw/solutions/` 下的原始 md 檔 | 解決透過 index.html#md 渲染器預覽時，相對路徑附圖與 PDF 補充資料無法載入的 bug |
| 2026-06-30 | index.html 題庫瀏覽新增「📎 補充筆記 PDF」按鈕與「📎 掃描補充 PDF」工具列按鈕；使用者可將任意 .pdf 放入 `raw/solutions/RC-YYYY-N/`，dashboard 透過 File System Access API 即時掃描顯示（不修改 dashboard-data.js）；更新 CLAUDE-CODE.md、CLAUDE-SPEC.md、CLAUDE.md 補充規範 | 支援每題補充筆記 PDF 快速存取 |
| 2026-07-01 | index.html「考點統計」頁籤改為呈現 frequency 指令輸出格式（高頻考點 Top10、各單元命題比例、近5年趨勢動態計算），移除原設計法分布與高頻標籤 Top20 兩張卡片 | 對齊 CLAUDE-CODE.md FREQUENCY 指令規格，避免統計呈現重複 |
| 2026-07-01 | dashboard-data.js 每題新增 pdf 補充筆記檔名陣列欄位（由 REFRESH-DASHBOARD 掃描 raw/solutions/RC-YYYY-N/ 下 *.pdf 寫入）；index.html 移除「📎 掃描補充 PDF」工具列按鈕與前端即時掃描機制（injectPdfButtons/pdfCache/listDir），改為依 dashboard-data.js 靜態資料直接顯示「📎 補充筆記 PDF」按鈕；同步更新 CLAUDE-CODE.md、CLAUDE-SPEC.md | 使用者自行放入補充 PDF 後無需手動點擊掃描按鈕，題卡即可自動顯示 PDF 連結 |
| 2026-07-02 | index.html 實作「線上/單機雙軌讀取」機制，線上環境（GitHub Pages 等非 file:/// 環境）自動使用 fetch 與相對路徑讀取 md、pdf 及圖片，免除資料夾授權提示 | 提升線上版儀表板的使用體驗，使其運作如同一般靜態網站 |
| 2026-07-02 | 實作 index.html 前端的 Hash 深度連結（#md=）邏輯，正式支援 study 頁面考題點擊跳轉功能 | 補齊前端功能，完全對齊 CLAUDE-CODE.md 中 STUDY 指令的連結規格 |
| 2026-07-25 | `study/` 新增第二種教材型態：`lecture-RC-UN-n.html/.pdf`（由外部 `unit-lecture` skill 產出的理解導向觀念講義），與 study 速查頁並存不互相覆蓋；新增共用離線資源 `study/assets/katex/`；同步更新 README.md、檔案架構索引表.md、CLAUDE-CODE.md（STUDY 段落交叉註記） | 練題前需要建立物理直覺的教材，與練題時用的速查頁定位不同，分開管理 |
| 2026-07-25 | **規則 1 例外擴充**：`raw/` 唯讀的例外從「`question_index.json`」擴充為「`question_index.json` + `raw/solutions/methods/`」，並訂出三項修改條件（驗算／同步 wiki／記 log） | `methods/` 是 `wiki/methods/` 的 compile 來源，只改 wiki 副本會被 `compile-all` 蓋回；公式勘誤需能根治。個別題目解析 `raw/solutions/RC-YYYY-N/` 仍受完整保護 |
| 2026-08-08 | `study/` 新增第三種教材型態：`formula-given-RC-UN-n.html/.pdf`（由外部 `unit-formula-map` skill 產出的公式「給／背分界」盤點），與 study 命題分析頁、lecture 觀念講義並存；首批完成 RC-U1-1、RC-U1-2；同步更新 README.md、檔案架構索引表.md | 考卷幾乎不印撓曲／P-M 公式，需以 24 年考卷原文為證據界定背誦範圍 |
| 2026-08-08 | `unit-formula-map` 再產出三個單元的公式給／背分界：RC-U2-1（剪力）、RC-U3-3（韌性與耐震）、RC-U4-1（預力斷面應力）；五份頁面全部雙向互連（nav 加上其他單元按鈕，PDF 鍵維持最後一顆） | 剪力的箍筋設計四件套、耐震的能力設計法、預力的應力疊加式皆為 24 年零次印出，需以證據界定背誦範圍 |
| 2026-08-08 | `unit-exam-intel` 將 `study-RC-U1-1.html`、`study-RC-U1-2.html` 由七區段深度複習頁重構為六區塊「命題情報頁」（出題概況／考點結構／考點漂移／題型走向／考題清單／命題風險），檔名不變；刪除與 lecture／formula-given 重複的截面圖解、解題流程、公式速查、高頻陷阱四區段與互動計算器（經使用者確認），移除 Keynote 按鈕；`study/problems-view/` 由 64 頁補齊至 100 頁，全數改用「命題分析＋講義」雙鈕並注入跟隨來源單元腳本，取代失效的 `javascript:history.back()` | 三份教材定位分工：lecture 講「為什麼」、formula-given 講「要不要背」、study 只講「考什麼」；所有數字改由 `scripts/stats.py` 產生並以 `verify.py` 對帳，杜絕手打統計（舊頁曾把「2025 年缺席」誤寫成「近 5 年連續出題」）|
| 2026-08-08 | `unit-exam-intel` 續作三個單元：`study-RC-U2-1.html`、`study-RC-U3-3.html`、`study-RC-U4-1.html` 由七區段深度複習頁重構為命題情報頁（互動計算器與 Keynote 按鈕比照 U1-1／U1-2 移除，至此 `study/` 已無 Keynote 鍵）；U2-1 因主考點僅 7 題（<8）依規格跳過「考點漂移」，改放「剪力的角色：主 7 vs 副 9」表；三份 lecture 頁 nav 的「速查頁」改為「命題分析」並補上「給／背分界」鍵 | 五個已有 lecture＋formula-given 的單元至此三份教材定位一致；本輪另發現 `RC-2021-4` 索引 designMethod 記為「概念題」但實為 WSD 計算題（已在頁面加註記、未逕改索引），以及 `RC-2019-3`、`RC-2018-4` 解析表頭主分類缺子項號 |
| 2026-08-20 | `study/` 新增第四種教材型態（科目層級）：`frequency-RC.html`（由外部 `subject-frequency-map` skill 產出的全科出題頻率熱圖），是唯一「整科視角」的頁面，與三種單元層級教材（study 命題分析／lecture 觀念講義／formula-given 給背分界）互補；排名表的教材欄自動掃描 `study/` 產生可點連結 | `unit-*` 系列一次只看一個子項，答不了「整科該從哪裡開始讀」；本頁全部數字由 `build_frequency.py` 從 `question_index.json` 算出並通過三項對帳（格子總和＝100 題、每列總和＝該子項題數、單元小計相符），題庫更新後可無人工判斷直接重跑 |
| 2026-10-09 | `frequency-RC.html` 以 subject-frequency-map v1.1 重產；新增 `scripts/build_frequency.py`（v1.1 產生器入庫） | v1.1 加入前後半期升溫／冷凍比較、後半期排名、可點熱圖；產生器改放知識庫內，可直接重跑 |
| 2026-10-31 | 全庫主／副分類與引用關聯複核修正：13 題分類、1 題設計法修正並同步解析表頭／wiki／儀表板／知識圖譜／frequency／命題分析頁／problems-view；24 頁「相關題目」重寫；RC-2023-1 wiki 頁改為摘要頁；wiki/log.md 亂碼還原 | 同題型分類標法不一（接頭、組合斷面、預力損失副分類），且部分相關題目依題號自動湊數、連到無關考點 |
| 2026-10-31 | 導入 unit-overview：`study/unit-RC-Un-m.html`（單元總覽＝命題分析＋公式給／背＋逐題公式表）由 `scripts/build_unit_page.py` 從 `study/data/unit-RC-Un-m.json` 產生，五單元（U1-1、U1-2、U2-1、U3-3、U4-1）上線；舊 `study-`／`formula-given-` 改轉址頁；problems-view、lecture 導覽、build_frequency 同步改指單元總覽 | 兩份單元頁內容互補但分散，「考了卻沒給」原為年份層級無法對應到題；改為逐題公式用途後證據可回溯到題解 |
| 2026-11-01 | wiki 封存：wiki/ 只保留 queries/；其餘目錄與 index.md、by-year.md 移至 archive/wiki/；wiki/log.md → wiki/queries/log.md；ingest / compile-all / lint / add-concept 停用；規則 1 methods 修改不再同步 wiki/methods/；index.html、講義連結、xcheck.py、generate_knowledge_graph.py 同步改指 | 舊 wiki 為未驗證的 AI 摘要且與 raw/solutions、study/ 重複（SS 掃描發現 45 處錯誤），改以正本與 study 教材為準 |
| 2026-11-01 | **廢止題解互動圖與補充筆記 PDF、儀表板改版**：刪除 18 份 `*-viz.html` 與 2 份題目補充 PDF；`question_index.json` 去 `hasViz`、`dashboard-data.js` 改 5 欄；`index.html` 完整解析改連 `study/problems-view/`、刪「指令速查」分頁並修資料夾授權恢復 bug | 圖解改以 `figs/*.svg` 為準；儀表板只保留讀書用功能，指令以 CLAUDE-CODE.md 為唯一正本 |
