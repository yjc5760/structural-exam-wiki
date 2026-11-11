# 結構工程技師考試知識庫 — 土壤力學與基礎設計（SM）

> 科目代碼：SM｜資料夾：`exam-wiki-SM`｜其他科目另建獨立資料庫

## 專案說明

本資料庫專門收錄「專門職業及技術人員高等考試結構工程技師」**土壤力學與基礎設計**科目的考古題解析知識庫。

- **科目代碼：** SM（Soil Mechanics & Foundation Design）
- **題目編號格式：** SM-YYYY-N（如 SM-2015-1）
- **其他科目：** 各自建立獨立資料庫（exam-wiki-RC、exam-wiki-SS 等）

**核心工作流程：**
```
在 Cowork 開啟 exam-wiki-SM/ 資料夾（Project）
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
~~說：「ingest SM-XXXX-N」→ Cowork 直接執行，wiki 自動更新~~（已停用（2026-11-01 wiki 封存））
```

---

## 兩個環境分工

| 環境 | 負責什麼 |
|------|---------|
| **你（使用者）** | PDF 題目附圖截圖（fig-N.png）、chart/eqn/hand 補充截圖、人工驗算後通知 Cowork 更新 verificationStatus |
| **Cowork** | 解題（SOLVE，**一次一題**）、存檔（.md）、更新 question_index.json、**所有操作指令**（ingest / compile-all / lint 已停用（2026-11-01 wiki 封存）；status / reindex / add-concept / add-method / refresh-dashboard / frequency / analyze / predict / study / find / related / unverified / query，共 16 個，詳見 CLAUDE-CODE.md）、直接維護 wiki/queries/ · study/（study 指令輸出） |

---

## 單向資料流

```
raw/solutions/SM-XXXX-N/SM-XXXX-N.md  ──→  study/problems-view 等學習頁（直接讀 raw）
raw/solutions/methods/                 ──→  （唯一版本，直接閱讀與修正）
Cowork 查詢結果／稽核報告              ──→  wiki/queries/       （Cowork 直接存入）
Cowork study 指令輸出                  ──→  study/              （Cowork 直接存入）

archive/wiki/                          ──   2026-11-01 封存的舊 wiki 各層（problems/concepts/methods/traps/
                                            philosophy/diagnosis/failure-modes/materials/code-ref、index.md、by-year.md），
                                            凍結不再更新，僅供查舊

解題內容唯一來源：raw/solutions/ 下的 .md 檔案
索引資訊唯一來源：raw/json/question_index.json
方法論唯一來源：raw/solutions/methods/（可修正，須驗算＋記 log，見規則 1）
wiki/queries/（含 log.md）、study/：由 Cowork 直接寫入
ingest / compile-all 已停用（2026-11-01 wiki 封存）
```

---

## 資料夾結構

```
exam-wiki-SM/
├── README.md                        ← 冷啟動快速導覽
├── CLAUDE.md                        ← 本檔（身份層：分工、資料流、重要規則）
├── CLAUDE-SOLVE.md                  ← Cowork 解題 Skill
├── CLAUDE-CODE.md                   ← Claude Code 操作指令（Runbook）
├── CLAUDE-SPEC.md                   ← 規格驗證層（格式、命名、完成標準）
│
├── study/                           ← 讀書筆記、講義、study 指令 HTML 輸出（study-SM-UN.html / study-SM-UN-n.html）
│
├── raw/                             ← 所有原始資料（預設唯讀，僅 ✏️ 三處可改）
│   ├── exams/                       ← 原始考卷 PDF（命名：SM-YYYY_土壤力學與基礎設計.pdf）
│   ├── json/
│   │   ├── concepts.json            ← 概念定義（供 compile-all）
│   │   └── question_index.json      ← ⭐✏️ 題目總索引（唯一需要人工維護的 JSON）
│   └── solutions/                   ← AI 解析 + 補充截圖（每題一個資料夾）
│       ├── SM-YYYY-N/               ← 🔒 證據，不可修改（規則 1、2）
│       │   ├── SM-YYYY-N.md         ←   🔒 內容凍結，但 ✏️ 附圖引用行／圖說可補正（規則 1-C）
│       │   ├── SM-YYYY-N-fig-1.png  ←   ✏️ 命名不符規範時可改名（規則 1-C）
│       └── methods/                 ← ✏️ 解題方法論（可修正公式／單位，見規則 1）
│
├── wiki/
│   └── queries/                     ← 查詢結果與稽核報告 ← Cowork (直接存入)
│       ├── index.md                 ← 報告清單
│       └── log.md                   ← 操作紀錄（append only）
│
└── archive/
    └── wiki/                        ← 2026-11-01 封存的舊 wiki（凍結，不再更新；說明見 archive/README.md）
        ├── index.md、by-year.md
        └── concepts/ methods/ traps/ problems/ philosophy/ diagnosis/ failure-modes/ materials/ code-ref/
```

---

## 知識分類骨架（七層）——已封存

> 2026-11-01 起七層目錄全部移至 `archive/wiki/`，凍結不再更新；下表僅保留作歷史說明。

Wiki 導航曾依七層知識架構組織（前三層由 Cowork 透過 compile-all/ingest 生成，後四層由 Cowork 直接維護）：

| 層 | 目錄 | 維護者 | 內容 |
|----|------|:------:|------|
| Layer 1 | `concepts/` + `problems/` | Cowork (ingest/compile) | 核心土力/基礎觀念（土壤基本性質/滲透/壓密/土體應力/剪力強度/承載力/樁基/土壓力/邊坡穩定） |
| Layer 2 | `philosophy/` | Cowork (compile-all) | 設計哲學與實務（總應力法 vs 有效應力法、容許應力設計 vs 極限狀態設計、安全係數選取哲學） |
| Layer 3 | `methods/` | Cowork (compile-all) | 解題方法論（Terzaghi/Meyerhof承載力理論、Rankine/Coulomb土壓力理論、Fellenius/Bishop邊坡穩定法、壓密沉陷計算） |
| Layer 4 | `diagnosis/` | Cowork (直接存入) | 題型診斷決策樹 |
| Layer 5 | `failure-modes/` | Cowork (直接存入) | 失敗模式（承載力破壞/過大沉陷/滲流破壞（管湧砂湧）/邊坡滑動/擋土結構失穩） |
| Layer 6 | `materials/` | Cowork (直接存入) | 材料行為（土壤分類特性/滲透特性/壓密特性/剪力強度特性） |
| Layer 7 | `code-ref/` | Cowork (直接存入) | 規範條文對應（建築物基礎構造設計規範、大地工程手冊、建築物耐震設計規範） |

> **補充目錄 `traps/`（已封存於 `archive/wiki/traps/`）：** 不屬於七層架構，由 compile-all 從題目解析萃取陷阱頁面，與 concepts/ 並列為輔助導航。

---

## 命題大綱分類（依官方命題大綱，93年3月公告）

> topicId 格式：`SM-UN-n`，U = 單元號，n = 子項號。
> `primaryTopicId` 填最主要考點；跨子項時用 `secondaryTopicIds` 列出。
> 最新鮮的官方分類請直接查閱 `raw/json/syllabus_taxonomy.json` 中 `id: "SM"` 的段落。

### 第一單元（SM-U1）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U1-1 | 土壤基本性質 |
| SM-U1-2 | 土壤滲透 |
| SM-U1-3 | 土壤夯實及壓密 |
| SM-U1-4 | 土體內應力 |
| SM-U1-5 | 土壤強度特性與變形性 |

### 第二單元（SM-U2）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U2-1 | 淺基礎之支承力與沉陷量 |
| SM-U2-2 | 深基礎之支承力與沉陷量 |
| SM-U2-3 | 開挖之穩定性分析 |
| SM-U2-4 | 基礎型式之選擇與評估 |
| SM-U2-5 | 地層改良方法 |

### 第三單元（SM-U3）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U3-1 | 側向土壓力理論 |
| SM-U3-2 | 擋土結構物穩定分析 |
| SM-U3-3 | 坡地工程 |
| SM-U3-4 | 生態工法在邊坡工程之應用 |

---

## 重要規則

1. **`raw/` 目錄下所有檔案一律不可修改**，僅以下三處例外：
   - `raw/json/question_index.json`（索引唯一人工維護處）
   - `raw/solutions/methods/`（方法論文件，可修正公式錯誤與單位標註）
   - `raw/solutions/SM-YYYY-N/SM-YYYY-N.md` 的**附圖引用區塊**（僅限圖片引用、alt text、圖說三者，見下方 1-C）

   > **為什麼 methods/ 是例外**：本規則要保護的是**證據**（考卷、AI 解析、驗證過的答案），
   > 這些一旦被改就失去可追溯性。但 `raw/solutions/methods/` 存的是**可維護的知識整理**，
   > 且它是方法論的唯一版本（舊 `wiki/methods/` 副本已於 2026-11-01 封存至 `archive/wiki/`，不再同步）。
   > 發現公式或係數錯誤時，必須改 raw 來源才算根治。
   >
   > **修改 methods/ 的三個條件（缺一不可）**：
   > ① 修正前先做**數值驗算**（邊界代入、量綱檢查、與驗證解答交叉比對），不可憑印象改；
   > ② ~~改完同步覆蓋 `wiki/methods/` 對應檔~~（已停用（2026-11-01 wiki 封存），只改 raw 一處）；
   > ③ 在 `wiki/queries/log.md` 記錄**改了什麼、為什麼、怎麼驗證的**。

   ### 1-C　附圖引用補正（窄例外）

   > **為什麼需要這個例外**：`CLAUDE-SPEC.md` 明訂「每張圖片在 .md 中必須包含 alt text + 圖說兩部分」，
   > 且完成標準含「每張 PNG 圖片有對應 `*圖說：*`」。但實務上會出現三種**規格違反**狀態：
   > ① 使用者已把截圖存進題目資料夾，`.md` 卻沒有引用它（圖被孤立，讀者看不到）；
   > ② `.md` 引用了資料夾內不存在的檔名（破圖連結）；
   > ③ 圖檔命名不符 `SM-YYYY-N-<fig|chart|eqn|hand>-N.png`（如殘留的裁切暫存檔）。
   >
   > 這三種都是**證據與解析之間的連結斷裂**，不是證據本身有爭議。
   > 補上引用是**恢復**可追溯性，而不是改動證據 —— 這正是規則 1 想保護的東西。
   > 若不允許修正，缺陷只能靠顯示層繞過，下次重新渲染又會復發。
   >
   > **可以動的範圍（白名單，僅此三項）**：
   > - `![alt text](SM-YYYY-N-<type>-N.png)` 圖片引用行
   > - 緊接其後的 `*圖說：…*` 段落
   > - 圖檔本身的檔名（改成符合命名規範）或刪除確認為重複／暫存的檔案
   >
   > **絕對不可動（違反即等同違反規則 1、2）**：
   > 題目重述的文字與數值、任何公式、計算過程、`verifiedSolution`、結論、
   > 章節結構（§1~§5）、標籤、分類。**一個數字都不准改。**
   >
   > **補正的四個條件（缺一不可）**：
   > ① 必須**先實際看過圖片內容**再寫 alt text 與圖說，不可憑檔名或上下文猜測；
   > ② 圖說須依 `CLAUDE-SPEC.md` 各類型要求撰寫（`fig` 記幾何與土層參數、`chart` 記控制點座標、
   >    `eqn` **所有公式完整 LaTeX 文字化**、`hand` 記步驟摘要），做到「看不到圖也能解題」；
   > ③ 若圖片內容與 `.md` 現有敘述**矛盾**（例：`.md` 寫「無附圖」但圖存在），
   >    **只修正該句敘述本身**，並在 `wiki/queries/log.md` 明確記下原文與新文；矛盾若牽涉數值，**停手改問使用者**；
   > ④ 在 `wiki/queries/log.md` 記錄**改了哪幾題、每題補了什麼圖、圖的內容是什麼、以及「未改動任何數值／公式／結論」的自我確認**。
   >
   > ⚠️ 除上述白名單外，`raw/solutions/SM-YYYY-N/` 仍受規則 1 與規則 2 完整保護。

2. **`verifiedSolution` 是最終答案，不可質疑或重新計算**
3. **`wiki/queries/log.md` 只可 append，不可刪除已有紀錄**
4. **wiki/ 只剩 queries/（由 Cowork 直接維護）；`archive/wiki/` 是 2026-11-01 封存的舊 wiki，凍結不可修改**
5. ~~ingest 前必須確認 verificationStatus = "verified"~~（已停用（2026-11-01 wiki 封存））
6. 概念連結使用 `[[concept_id]]`（Obsidian 相容）
7. ~~每次 ingest 同時更新 index.md 和 by-year.md~~（已停用（2026-11-01 wiki 封存））
8. **格式與命名規範見 CLAUDE-SPEC.md；操作指令（ingest/compile/lint/status）見 CLAUDE-CODE.md，全部由 Cowork 執行**

---

## CHANGELOG

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-07-11 | 從 exam-wiki-RC 克隆，全面改寫為 SM 科目（土壤力學與基礎設計） | 建立土壤力學與基礎設計獨立知識庫；沿用 RC 版本已驗證的兩層（User/Cowork）工作流程與 16 個 Cowork 指令架構；清空 RC 領域專屬的 wiki 內容（題目解析、概念、方法論等），重置為空白索引，等待依「解析 XXXX 年考卷」流程逐年建立 SM 題庫 |
| 2026-07-25 | **規則 1 例外擴充**：`raw/` 唯讀的例外從「`question_index.json`」擴充為「`question_index.json` + `raw/solutions/methods/`」，並訂出三項修改條件（驗算／同步 wiki／記 log） | `methods/` 是 `wiki/methods/` 的 compile 來源，只改 wiki 副本會被 `compile-all` 蓋回；公式勘誤需能根治。個別題目解析 `raw/solutions/SM-YYYY-N/` 仍受完整保護 |
| 2026-07-30 | **規則 1 新增窄例外 1-C「附圖引用補正」**：`raw/solutions/SM-YYYY-N/SM-YYYY-N.md` 的圖片引用行、圖說段落與圖檔命名可修正，白名單外一律不可動（題目數值、公式、計算、結論、章節結構皆完全禁止）。訂四項條件（先看過圖／圖說依 SPEC 各類型要求／敘述矛盾只改該句且牽涉數值須停手問人／記 log 並自我確認未改數值） | 全庫掃描發現 8 題存在「圖檔已在資料夾但 `.md` 未引用」「引用了不存在的檔名」「命名不符規範」三類**規格違反**（`CLAUDE-SPEC.md` 已明訂每張圖須有 alt text + 圖說）。此類缺陷是「證據與解析之間的連結斷裂」，補正屬於恢復可追溯性而非改動證據；若僅靠顯示層繞過，重新渲染即復發。最嚴重者為 SM-2017-1：`.md` 寫「無須額外附圖」，但資料夾內的 fig-1 正是答題必需的圖1-1 夯實曲線與表1-1 夯實土壤工程特性 |
| 2026-08-14 | **unit-exam-intel：SM-U1-3／U3-3／U2-1／U1-5／U2-2 五個舊速查頁重構為命題情報頁**；刪除與 lecture／formula-given 重疊的四個區段與互動計算器（經使用者確認）；補產漏建的 `study/problems-view/SM-2003-1.html`；71 個 `problems-view/*.html` 的 `javascript:history.back()` 返回鍵改為「命題分析／講義」雙按鈕＋跟隨來源單元腳本；移除 `lecture-*` 五顆指向不存在 PDF 的 Keynote 死連結 | 舊速查頁的公式速查、剖面圖解、解題流程、高頻陷阱四段已被 `formula-given-*`（含逐年給／背證據）與 `lecture-*`（含 22–26 條陷阱）完整取代，留著會造成同一件事有兩個版本、改一處忘一處。重構後本頁只回答「這個單元考什麼」，所有數字皆由 `scripts/stats.py` 從 `question_index.json` 算出、由 `scripts/verify.py` 對帳，可隨題庫更新重生。過程中查出並修正：U3-3 舊頁 KPI 誤植（排名寫第 1 名，實際 #2；近 6 考年寫 4/6，實際 3/6）、五頁題號連的是不會渲染公式的 `../index.html#md=` 舊式連結、五頁皆漏列副考點（共 8 題次）、`problems-view/` 缺 SM-2003-1、`target="_blank"` 新分頁裡 `history.back()` 按了無反應 |
| 2026-08-14 | **依使用者指示，`raw/json/question_index.json` 96 題的 `verificationStatus` 全數由 `verified` 改為 `unverified`**；五個單元命題情報頁的驗算圖示同步改為由該欄位驅動（✅／⏳／⚠️），不再寫死 | 全庫重新進入待驗算狀態。逐題比對確認唯一變更欄位為 `verificationStatus`（96 筆），其餘欄位與檔案結構未動，`git diff` 不含任何非該欄位的行。連帶後果：`unverified` 依 `CLAUDE-SPEC.md` 不允許 ingest，重新驗算並改回 `verified` 前 `ingest` 會被擋；`wiki/index.md` 的「96 題已驗證 ingest」一句已與現況不符，待決定後處理 |
| 2026-08-14 | **全庫稽核：96 題分類與標籤逐題複核並修正**——`primaryTopicId` 改 29 題、`secondaryTopicIds` 補 54 題、`tags` 重寫 94 題、`designMethod` 修正 2 筆非法值「彈性理論」、補齊 `CLAUDE-SPEC.md` §9 規定但缺漏的 `moduleId`／`rocYear`／`primaryTopicName`／`hasViz` 四欄；`lecture-`／`formula-given-SM-U3-3` 改名為 `-SM-U2-3`；命題情報頁重生 6 份；`problems-view/` 補 12 頁、34 頁按鈕重新指派 | 2026-07-12 `[DATA-FIX]` 批次搬遷 17 筆舊分類 `SM-U4-*` 時自註「建議日後人工複核」，該複核從未執行，導致三個系統性錯置長期存在：12 題深開挖掛在 U3-3「坡地工程」、5 題邊坡穩定掛在 U3-4「生態工法」、5 題滲流／土體應力掛在 U2-1「淺基礎」。修正後 U1-2 滲透、U2-5 地層改良、U3-1 側向土壓力三個原本掛 0 題的子項都有了題目，U2-3 開挖穩定性由 1 題成為 12 題。7 題兩解並存者維持現況待裁決（清單見 wiki/log.md 同日條目第七節） |
| 2026-08-14 | **依使用者指示，96 題 `verificationStatus` 改回 `verified`**（撤銷同日稍早改為 `unverified` 的變更）；六個命題情報頁的驗算圖示同步由 ⏳ 回到 ✅ | 逐題比對確認唯一變更欄位為 `verificationStatus`（96 筆），其餘欄位與檔案結構未動。此舉解除了 `ingest` 的封鎖——同日全庫稽核的分類與標籤修正尚未反映到 `wiki/problems/`（34 / 96 頁仍為舊分類），需接著執行 `compile-all` 與 `refresh-dashboard` 使下游產物與索引一致。注意：僅改回狀態旗標，未重新進行人工驗算 |
| 2026-08-14 | **7 題兩解並存者依使用者裁決全部照稽核建議修正**（SM-2004-3、2008-1、2011-1、2013-1、2015-2、2015-4、2016-2）；六個命題情報頁重生、`compile-all` 重跑（48 檔）、`problems-view/` 2 頁按鈕重指 | **`SM-U3-4` 生態工法歸零**——本考科 24 個考年確實從未考過生態工法，索引終於誠實反映。另 `SM-U1-3` 由 23 減為 22 題並新增 2007–2008 空窗（原頁面「無連續空窗」的敘述已不成立，已改寫）、`SM-U2-1` 減為 4 題（排名 #10、命中 4 / 24 考年，全科最低）、`SM-U3-1` 增為 4 題 |
| 2026-08-14 | **REFRESH-DASHBOARD 重生 `dashboard-data.js`**（96 筆，含 26 題 viz、55 題副分類）；**並修正 `index.html` 的暫時性死區（TDZ）錯誤** | 儀表板資料落後於稽核後的分類。驗證時另發現既有 bug：第 415 行在 `let dirHandle`（第 455 行）宣告前就呼叫被提升的 `ensureDir`，拋出 ReferenceError，導致「靜默恢復上次資料夾授權」**從未生效**——本機開啟時每次都要重新授權。已將該呼叫移到宣告之後並加 `.catch()`，headless 驗證 pageerror 消失。至此 `question_index.json` 的下游（study／wiki／dashboard）全部同步 |
| 2026-08-14 | **十份 `lecture-`／`formula-given-` PDF 以 headless Chromium 重出**，並修正五份 lecture HTML 過時的表頭統計，以及一處我自己造成的全域替換誤傷 | PDF 不是從 HTML 自動衍生（原為 MathJax→SVG＋WeasyPrint 另一條產出線），本階段只改 HTML 與檔名，導致 PDF 全部停留在舊內容——`lecture-SM-U2-3.pdf` 內含 25 處舊代號 SM-U3-3。重出時發現 HTML 表頭的題數／佔比／排名也全是舊值，一律改為「子項現有主考點 N 題（本講義涵蓋 M 題）」句式。換引擎導致頁數增加約 20–25%、檔案增大（CJK 字型子集），為必然取捨 |
| 2026-08-16 | **unit-exam-intel：新產 `study-SM-U1-1.html`、`study-SM-U3-1.html` 兩份命題情報頁，並依使用者指示全部重做 `study-SM-U2-3.html`**；三頁的 KPI、篩選鈕數字改由 `stats.py` 直接產生（不再手打），`verify.py` 七項全過；`problems-view/` 12 頁的返回按鈕重新指派到正確的主分類單元（5 頁原為 `javascript:history.back()`、1 頁原為 `../../index.html`、6 頁原退到副分類 U1-3／U1-5），其中 5 頁補上「跟隨來源單元」腳本；`lecture-`／`formula-given-SM-U1-1`／`-SM-U3-1` 四份補上回連命題分析的按鈕 | U1-1 與 U3-1 是 2026-08-14 全庫稽核後才有足夠題數的兩個子項（U1-1 主 8 副 10、U3-1 主 4 副 13），此前沒有情報頁，其 12 題的 `problems-view` 返回鍵只好退到副分類或整個失效。U2-3 舊頁雖然 `verify.py` 全過，但分群只有 3 群且把「調查規劃／島式開挖側滑／滲流」三種完全不同的套路全塞進「開挖底面與周邊穩定」一群，改為 4 群（貫入深度／支撐系統／底面穩定與滲流／周邊風險與災害研判）後，2023-4 這個 24 年來唯一的「災害案例研判」新題型才顯示得出來。過程中查出並記錄一筆索引與題型不符（`SM-2020-3` 標 `概念題` 但實為相對密度計算），依規則未逕行修改，另記 `wiki/log.md` 待裁決 |
| 2026-08-16（第二次） | **formula-recall-deck：SM-U1-1／U1-3／U1-5／U2-3／U3-1 五支「公式給／背分界」記憶片**（各 32–33 頁、回想卡 9 張、觀念圖 4–5 張，輸出 .pptx＋.pdf＋逐頁旁白稿，共 15 檔）；**另新增 `study/frequency-SM.html` 全科出題頻率熱圖**（14 子項 × 24 考年，可切主／主＋副兩種模式，教材標籤可直接點進對應頁） | 公式清單全部直接讀 `formula-given-SM-Un-m.html` 原始碼的 `const F[]` 與 §4 背誦策略，未做任何重建；23 張觀念圖逐張讀出 PNG 目視檢查，修掉 11 處標籤重疊／中文誤入數學區塊／符號方向錯誤（逐項見 `wiki/log.md`）。頻率熱圖不屬於既有三種 study 檔，是跨子項的一頁，回答「整科該從哪裡開始讀」——由它得到的新事實：單元權重 51／28／17、前三名佔 47.9%、六個「副>主」的工具型子項、以及 U3-4 生態工法 24 年 0 題（命題大綱有列、考卷從未考過） |
| 2026-08-28 | **五題解析稽核修正（SM-2025-1／2003-2／2022-1／2019-3／2019-2）＋ struct-diagram 產出 12 張向量圖解**；依使用者指示先將 `question_index.json` 96 筆 `verificationStatus` 翻為 `unverified` 以解除規則 2 凍結，再修訂解析；五題標頭分類／分析法／標籤與 JSON 同步；下游 `study/problems-view/` 五頁、`wiki/problems/` 五頁重生、96 頁驗證旗標與 8 份命題情報頁同步 | **SM-2019-2 查出答案級錯誤**：§4 所引「表一」的兩個控制點（$T_v$=0.40→69.8%、0.50→76.4%）並不存在於考卷，實際表值為 52.55% 與 62.92%，該兩數字是憑記憶寫上的課本平均壓密度值；改依考卷表一內插得 $T_v$=0.600，答案由 209.3 天改為 **300 天**（理論值 208.5 天併列）。延伸查出考卷表一與圖二標為「平均壓密度」，但 14 列逐列吻合的是中央面局部壓密度 $U_z(Z{=}1)$，屬考卷本身的標示問題，已完整記於 §5 爭議點。另 2026-08-14 全庫稽核只改 JSON 未回改 `raw/` 標頭，導致五題主分類寫成非法的 `SM-U1`／副分類錯置／分析法與 JSON 不符——全庫同類缺陷尚存 43 題（非法主分類）與 26 題（標題方括號），清單見 `wiki/log.md` 同日條目第二節 |
| 2026-08-28（第二批） | **五題解析稽核修正（SM-2016-2／2020-3／2004-1／2008-1／2023-1）＋ struct-diagram 產出 10 張向量圖解**；五題標頭分類／分析法／標籤與 JSON 同步（`SM-2016-2` 主副分類原本顛倒）；依使用者裁決將 `SM-2020-3` 的 `designMethod` 由「概念題」改為「混合」；`SM-2023-1` 題目重述錯字「相驚密度」更正為「相對密度」；兩批共 22 張圖因原本透明背景全部補白底重出 | **SM-2008-1 查出觀念性錯誤**：解析三處宣稱「$G_s$ 是多餘資訊、用以干擾判斷」，但拿 $G_s$ 一驗即發現 $V_s + V_w = 1.011 \text{ m}^3 > 1 \text{ m}^3$（$S = 104.7\%$）——考卷指定的夯實目標（$\gamma_d = 20$、$\omega = 12\%$）超過混合土的零空氣孔隙上限 19.78，物理上做不到。$G_s$ 正是唯一能做這個檢核的參數，講反了方向。三個小題的算術答案不受影響，已改寫敘述並補完整檢核。另五題標頭全部與 2026-08-14 稽核後的 JSON 對不上，成因同第一批（只改 JSON 未回改 `raw/` 標頭）；全庫同類缺陷剩餘 37 題（非法主分類）與 22 題（標題方括號），清單見 `wiki/log.md` |
| 2026-08-28（第三批） | **五題解析稽核修正（SM-2024-1／2018-2／2010-1／2008-2／2013-3）＋ struct-diagram 產出 12 張向量圖解**；`SM-2013-3` 依考卷圖二重新判讀破壞點，答案由 $\phi'=28.86°$／$A_f=0.813$／$\theta=59.43°$ 改為 **28.04°／0.806／59.02°**，且 (二) 的 LE 孔壓曲線由「先升到正值」改正為**全程為負**；`SM-2010-1` 第 2 小題主答由 9.6 kPa 改為 **50 kPa**（$B=1$），9.6 kPa 保留為延伸；五題標頭分類／分析法／標籤與 JSON 同步；下游 `study/problems-view/` 五頁、`wiki/problems/` 五頁重生 | **SM-2013-3 查出讀圖級錯誤**：原解在左圖找應力差峰值、卻在右圖讀 $\epsilon=1.0\%$ 的孔壓，兩張圖讀在不同應變；且原文的峰值 280 在曲線上根本不存在（逐像素判讀的全域極大為 274.2，落在 $\epsilon\approx0.87\%$）。連帶查出 LE 孔壓形狀畫反——$A$ 全程小於 1，$u_{LE}=(A-1)\Delta(\sigma_1-\sigma_3)$ 不可能為正。**SM-2010-1 查出主從顛倒**：題目「試體仍維持飽和狀態」唯一的用途就是宣告 $B=1$，問的是施加圍壓所產生的水壓。另五題標頭全部與 2026-08-14 稽核後的 JSON 對不上（成因同前兩批）；本批另量化出 11 題主分類連格式都不對，全庫寫法正確者僅 51/96 |
| 2026-08-29 | **五題解析稽核修正（SM-2010-2／2015-2／2019-4／2004-3／2025-3）＋ struct-diagram 產出 12 張向量圖解**；`SM-2025-3` 依考卷附圖逐像素量測改正兩個尺寸（$H$ 由 8 改 **7 m**、$B$ 由 7 改 **6 m**），答案由 $FS=1.158$ 改為 **1.297**；`SM-2010-2` §5 的 $\gamma_w=10$ 對照值由 237.6 改正為 **239.33 kN/m**，並新增「黏土段總側壓小於靜水壓、牆背會脫開」的爭議檢核；`SM-2019-4` 補上「傾斜地表不改變 $Z_t$」的共軛應力證明；五題標頭分類／分析法／標籤與 JSON 同步；**依使用者裁決改的是 JSON 而非 .md**——三題 `designMethod` 由「混合」改為 `SM-2019-4` 概念題、`SM-2004-3` 與 `SM-2015-2` 有效應力法；下游 `study/problems-view/` 五頁、`wiki/problems/` 五頁重生，`dashboard-data.js`、`study-SM-U3-1.html`、`lecture-SM-U3-1.html` 同步 | **SM-2025-3 是四批以來第一個「錯在讀圖尺寸」的答案級錯誤**：考卷只給四個標註量，左側 `7 m` 的下箭頭落在底版**底面**、下方 `6 m` 的左箭頭落在底版**左緣**，兩者都是含分段的**總量**；原解各多加了一段。判別依據是尺寸鏈閉合（趾部 1 ＋ 斜面投影 3 ＋ 牆頂 2 ＝ 6、牆身 6 ＋ 底版 1 ＝ 7），而原解的 §3 陷阱 2 甚至把方向講反、教讀者「取 7 m 會低估」。另外，本批也是 `designMethod` 首次被判定為 JSON 有誤（前三批都是 `raw/` 標頭有誤）——2026-08-14 全庫稽核把整個 U3-1 的四題主考點一律標成「混合」，其中 `SM-2019-4` 全題無數值、`SM-2004-3`／`SM-2015-2` 是純有效應力＋水壓，都不是混用兩種分析法。全庫剩餘標頭缺陷：主分類寫法不合規 40 題、標題含方括號 19 題 |
| 2026-08-29（第二批） | **全庫 96 題標頭歸零**：標題方括號 19→0、主分類 43→0、副分類 70→0（含 12 題原本缺欄）、標籤 76→0、分析法 29→0，標頭區塊依 `question_index.json` 整段重寫，**正文逐位元未動**；**分析法 29 題逐題複核**，24 題採 JSON、5 題判定 JSON 有誤而兩層一起改（`SM-2004-2`／`SM-2009-2`／`SM-2020-4` 混合→總應力法、`SM-2011-3` 混合→有效應力法、`SM-2014-2` 有效應力法→總應力法）；**`study/problems-view/` 一次收斂**——補建 3 頁（2004-2／2022-2／2025-4）、96 頁同一管線重生、`<head>` 三變體統一、19 頁補回 blockquote 樣式、17 頁返回鍵重新指派、`SM-2016-3` 的 6 處數學底線 bug 根治；`wiki/problems` 7 頁、`dashboard-data.js` 5 列、`study-SM-U1-3`／`U2-1`／`U2-2`／`U2-3` 的 6 筆資料列與 4 個 §b4 統計區塊同步 | 四批逐題修下來只解決 20 題，量到全庫才發現落差是「一次性事件」而非零星錯誤——2026-08-14 稽核改了 JSON 的三個欄位卻沒回寫 `raw/`，一次造成 96 題中 80 題標頭失準，因此改為全庫機械同步。**分析法首次寫下成文判準**（概念題＝無數值運算／有效應力法＝出現孔隙水壓／總應力法＝全程總應力，含「題目根本沒有水」的彈性題／混合＝同題兩法並用，或三相夯實類物理換算），沒有判準時同一種題型會被標成三種值——`SM-2004-2` 與 `SM-2025-4` 性質相同卻一個混合一個總應力法，正是這樣來的。另查出兩個此前沒人看的顯示層缺陷：19 頁的 `blockquote` 樣式從缺（`.md` 有引言卻沒有樣式），以及 17 頁返回鍵指向錯單元或根本失效。全科 designMethod 分布由 41／5／29／21 變為 **41／9／25／21** |
| 2026-08-29（第三批） | **五題解析稽核修正（SM-2017-4／2015-3／2005-1／2022-4／2023-4，主分類皆 SM-U2-3）＋ struct-diagram 產出 11 張向量圖解**；`SM-2015-3` 的 Peck 包絡線形狀改正——原圖把 $6\sim8$ m 畫成硬黏土的斜降梯形，與同一份解答 Step 3 判定的「軟弱至中等黏土」自相矛盾，改為 $2\sim8$ m 維持 $41.1$ 並補上 $P=287.70$、$\bar z=4.476$，「低估 16.7%」的分母取錯亦更正為 **14.3%**；`SM-2017-4` 的 SM 層 $N$ 由整層 14 改為逐點讀值平均 **13.333**，$FS_{隆起}$ 由 2.12 改為 **2.03**，管湧 $FS$ 由 2.34 改為 **2.33**（原式先把 $i$ 捨入再相除）；`SM-2005-1` 全式改用未捨入的 $K_a$，$T$ 由 125.53 改為 **125.51**；`SM-2022-4` Step 2／3 與 $A_1\sim A_4$ 的捨入不一致校齊（$P=137.467$、$\bar z=3.6913$），並補上四次式勘根表；`SM-2023-4` 補 13 列 $LI$ 全表與基底隆起量級估算（$FS=0.15/0.30/0.61$）。下游同步：`study/problems-view/` 五頁、`wiki/problems/` 五頁、三個既有 `…-viz.html`（2005-1 的 $T$、2022-4 的 $L_3$／$D_L$ 與誤植的「錨定式board pile」、2017-4 的 $S_u$／$FS$）、`study/lecture-SM-U2-3.html` 兩處敘述 | **本批查出一個「圖與文互相矛盾」的形狀級錯誤**：`SM-2015-3` 的 Step 3 已判軟弱至中等黏土，Step 5 卻畫成硬黏土的梯形；經三條獨立途徑交叉確認（½ 形 $\bar C_u=24.55\Rightarrow N=5.58$、僅黏土 $c_u\Rightarrow N=4.57$、Das $n'$ 形 $\Rightarrow N=3.45$）三取二為軟弱至中等，誤畫會低估總推力 14.3%、形心上移 0.476 m，支撐荷重分配全盤失真。**`SM-2017-4` 查出取值級錯誤**：鑽探報告在 $10.32\sim14.00$ m 有三個試驗值（14／12／14），原解整層取 14；更關鍵的是 $S_u$ 的**取用範圍**——只取開挖面下 2.32 m 厚的 CL 得 $FS=0.84$**不安全**，取到壁底加權平均得 2.03 安全，分母完全相同，本批把兩個數字都寫進解答。其餘三題屬「中間值先捨入造成的漂移」，不影響結論但會讓圖文對不上，一併校齊。三個既有手繪 viz 的失效值是本批新增的稽核面向——`SM-2022-4-pressure-viz.html` 寫的 $D_L=7.13$ 正好就是解答文字警告的那個進位錯誤 |
| 2026-09-18 | **全庫進入 re-verify 階段，狀態與屬性修正**：全庫 erificationStatus 變更為 unverified，並在定義中加入 draft；大量更新 designMethod 分類（將原本模糊的「混合」重新歸類為 總應力法、有效應力法 或 概念題），並產出五個新單元的 study 講義目錄 (SM-U1-1, SM-U1-3, SM-U1-5, SM-U2-3, SM-U3-1)；同步更新 dashboard-data.js 與 question_index.json | 依使用者指示，展開新一輪的屬性與狀態重構工作 |
| 2026-09-20 | **新增 SM-U1-3 四份觀念講義與投影片**：完成「土壤三相關係的萬用鑰匙」、「壓密沉陷四部曲」、「壓密速率與超載預壓」、「夯實曲線與夯實能量」四個主題的 PDF、PPTX 與 SVG 圖檔及腳本 | 使用者新增 |
| 2026-09-25 | **新增 SM-U2-3 及 SM-U3-1 觀念講義與筆記**：包含開挖擋土與側向土壓力的 PDF 及分類資料夾 | 使用者新增 |
| 2026-09-25 | **新增 SM-U1-5 四份觀念講義與投影片**：完成「NC與OC分岔」、「一張莫爾圓走天下」、「兩個閥門定生死」、「真參數只有一組」四個主題的 PDF、PPTX、SVG 圖檔及展示腳本 | 使用者新增 |
| 2026-10-09 | **subject-frequency-map v1.1：重生 `study/frequency-SM.html`**，新增產生器 `scripts/build_frequency.py` | 舊頁為 v1.0（2026-08-16）且本庫無產生器可重跑；v1.1 加入前後半期比較、可點熱圖與可排序排名表。查出 U3-2 全期第 6 但後半期第 3（被總數低估）、U2-4／U2-5 冷凍、U1-5 退燒。4 個單元影片資料夾命名不符偵測規則，未顯示（見 wiki/log.md 同日條目） |
| 2026-11-01 | **wiki 封存**：`wiki/` 除 `queries/` 外的各層與 `index.md`、`by-year.md` 移至 `archive/wiki/`；`wiki/log.md` 移為 `wiki/queries/log.md`；ingest／compile-all／lint／add-concept 停用；方法論只維護 `raw/solutions/methods/`；`index.html` 導覽、`xcheck.py`、講義 SM-U1-3 路徑同步 | 比照 SS：wiki 衍生層多年未同步、與 raw 勘誤脫節，學習改用 study/ 教材與 raw 正本 |
| 2026-11-01 | **廢止題解互動圖與補充筆記 PDF；儀表板優化**：刪除 `raw/solutions/` 下 26 份 `*-viz.html`，清除 SM-2020-1 .md／problems-view 引用與 `study/study-SM-*.html` 的 📊 圖示；`question_index.json` 移除 `hasViz`；`dashboard-data.js` 改 5 欄（去 viz、pdf）；`index.html` 完整解析改連 `study/problems-view/`、刪指令速查分頁、修資料夾授權（IDB 改 `smwiki-fs`、TDZ）等；修正解析 KaTeX 渲染錯誤 | 比照 SS 同日處理；圖解改以 `figs/*.svg` 向量圖為準 |
