# 結構技師考試知識庫（五科）— 操作指令手冊（Runbook）

> **適用環境：** Cowork（直接在對話中說出指令即可）
> **科目：** 每個指令只作用於一科。題號指令（`related SS-2015-1`）由題號前兩碼判定科目；
> 其他指令在後面加科目代碼（`status RC`、`frequency SA`、`unverified SD`）。未指明且無法從對話判斷時，先問科目。
> 下文所有 `raw/`、`wiki/`、`study/` 路徑都在 **`XX/`** 底下；`scripts/`、`skills/` 指根目錄；科目專屬設定見 `XX/SUBJECT.md`。
> **wiki 已封存**（2026-11-08 起五科一律只留 `wiki/queries/`，見 CLAUDE.md），變更紀錄寫在 `wiki/queries/log.md`。
> **不適用：** 此檔案不需要 Claude Code 終端機；Cowork 承接所有指令
> **格式與命名規範：** 見 CLAUDE-SPEC.md

---

## 由 skill 負責的流程

以下流程較長，改為 skill，說觸發語句時才載入；本文件不重複其內容。原始碼在根目錄 `skills/`。

| 流程 | 觸發語句 | Skill |
|------|---------|-------|
| 解題 SOLVE（含附圖擷取、題目正本、判讀清單、重繪） | `解析 YYYY 年 XX 考卷`、`判讀確認，請開始解題`、`繼續下一題` | `exam-solve` |
| 為既有解析補題目正本 | `題目正本`、`下一批` | `exam-problem-split` |
| 一批題目的總控（定題意→盲解→勘誤→落實檢查→圖解） | `跑 XX-Un-m 第 n 批`、`這批做到哪了` | `exam-wiki-pipeline` |
| 解析勘誤／重新驗算 | `勘誤 XX-YYYY-N`、`重新驗算`、`批次勘誤 XX-Un-m`、`跑 xcheck` | `exam-errata` |
| 稽核分類、盲解比對、落實檢查 | `盲解比對`、`稽核分類` | `exam-wiki-audit` |
| 單元總覽（命題分析＋給背分界＋逐題公式表） | `做 XX-Un-m 單元總覽`、`這單元考什麼`、`哪些公式要背` | `unit-overview` |
| 全科出題頻率熱圖 | `整科出題頻率` | `subject-frequency-map` |
| 觀念講義／教科書 | `生成 XX-Un-m 講義`、`把 XX-Un-m 寫成教科書` | `unit-lecture`／`unit-textbook` |
| 起點頁 start.html | `更新 start.html`、`依清單更新起點頁` | `exam-start-page` |
| 限時練習卷 PDF | `出一份 XX-YYYY-N 練習卷`、`模擬考` | `exam-practice-sheet` |
| AI 改卷／卡關紀錄 | `改卷`、`收進知識庫`、`記一筆卡關` | `add-to-wiki` |
| 題目向量圖解 | `幫 XX-YYYY-N 畫圖解`、`補圖` | `struct-diagram` |
| 科目從原 repo 搬入 | `把 exam-wiki-XX 搬進來`、`搬 RC 科` | `exam-subject-migrate` |
| 解題影片／影片講義 | `把這題做成解題影片`、`影片轉講義` | `blackboard-solution-video`／`video-handout` |

> 以上 skill 的正本都在根目錄 `skills/`（規則 12），使用者帳號裡安裝的是全域副本。
> 各科設計哲學框架在 `XX/SUBJECT.md` §8（解題時由 exam-solve 讀取）；命名、LaTeX、VHA 模板、JSON 欄位見 `CLAUDE-SPEC.md`。
> 原 `CLAUDE-SOLVE.md` 已於 2026-11-09 刪除（2026-10-29 起只剩轉址表），內容都在上表的 skill。

---

## 指令索引

### 📦 維護

| 指令 | 觸發語句 | 用途 |
|------|---------|------|
| [STATUS](#status) | `status XX`（不加代碼＝五科總表） | 查看驗證進度與統計 |
| [REINDEX](#reindex) | `reindex XX` | 掃描 solutions/，修正 hasSolution 不一致 |
| [ADD-METHOD](#add-method) | `add method XX [方法名]` | 新增解題方法論（`raw/solutions/methods/`） |
| [REFRESH-DASHBOARD](#refresh-dashboard) | `更新 XX 儀表板資料`（或「五科」） | 從 question_index.json 重新生成 dashboard-data.js |

> ⛔ **已停用（2026-11-08 起五科）**：`ingest`、`compile all`、`lint wiki`、`add concept`——它們只寫已封存的 wiki。
> 替代：分類一致性改用 `python scripts/audit_classification.py XX XX`（或 `exam-wiki-audit` skill）；跨檔數值一致性用 `python scripts/xcheck.py XX`；
> 題目頁改由 `scripts/render_problem_view.py` 產生 `study/problems-view/`。舊步驟見 git 歷史或 `SS/archive/exam-wiki-SS-root/CLAUDE-CODE.md`。

### 📊 備考分析類

| 指令 | 觸發語句 | 用途 |
|------|---------|------|
| [FREQUENCY](#frequency) | `frequency XX` | 統計各考點歷年出現次數 |
| [ANALYZE](#analyze) | `analyze XX YYYY` | 分析某年考卷考點分布 |
| [PREDICT](#predict) | `predict XX` | 推測今年最可能出現的考點 |
| [STUDY](#study) | `study XX-UN` | 彙整某單元所有題目與重點 |

### 🔍 查詢快捷類

| 指令 | 觸發語句 | 用途 |
|------|---------|------|
| [FIND](#find) | `find [關鍵字]`（預設五科一起搜） | 快速搜尋含某關鍵字的題目 |
| [RELATED](#related) | `related XX-XXXX-N` | 找出與某題考點相似的其他題目 |
| [UNVERIFIED](#unverified) | `unverified XX` | 列出所有有解析但尚未驗證的題目 |
| [QUERY](#query) | 直接提問 | 自由查詢知識庫 |

---

## STATUS

**觸發語句：** `status`（Cowork 直接執行）

**輸出格式：**
```
不加科目代碼 → 先輸出五科總表（科目｜題數｜考年範圍｜verified／unverified／needs-review｜題目正本 confirmed 數），再停止。
加科目代碼 → 讀取 XX/raw/json/question_index.json，輸出：

驗證進度：X / 總題數
✅ verified   (X題)：[列出題號]
⚠️ needs-review (X題)：[列出題號]
❌ unverified (X題)：[依年份分組列出]

solutions/ 已有解析但未驗證：[列出題號]
已 verified 但尚無 solutions/ 資料夾：[列出題號]

標籤統計（前10常見標籤）：
[標籤] : X 題
```

---

## REINDEX

**觸發語句：** `reindex`（Cowork 直接執行）

**用途：** 當 `raw/solutions/` 下的資料夾與 `question_index.json` 的 `hasSolution` 欄位不一致時（如手動新增了資料夾但忘記更新索引），用此指令自動修正。

**執行步驟：**
```
1. 掃描 raw/solutions/ 下所有子資料夾（格式：XX-YYYY-N）
2. 對每個資料夾，確認是否有對應的 .md 主解析檔
3. 與 question_index.json 比對 hasSolution 欄位：
   - 資料夾存在且有 .md → hasSolution 應為 true
   - 資料夾不存在或無 .md → hasSolution 應為 false
4. 輸出差異報告，詢問是否修正
5. 確認後批次更新 question_index.json
```

---

## ADD-METHOD

**觸發語句：** `add method [方法名]`（例：`add method 共軛梁法`）

**用途：** 在 `raw/solutions/methods/` 新增一個解題方法論文件（wiki/methods 已封存，不再建立）。

**執行步驟：**
```
1. 詢問方法論基本資訊：
   - method_id（全小寫-連字號，如 conjugate-beam）
   - 適用題型、適用規範條文
   - 核心公式、步驟摘要
2. 建立 raw/solutions/methods/[method_id]/[method_id].md（格式見下方）
3. 在 wiki/queries/log.md 追加紀錄
```

**另一種觸發：** 在 Cowork 討論某個解題方法後，說「加入知識庫」。（原在 CLAUDE-SOLVE.md，2026-10-29 移入）

**適用內容：**
```
解題工具型知識（跨多道題目使用）：
- 共軛梁法、虛功法、最小功法
- 彎矩分配法、傾角變位法
- 平行軸定理應用、組合斷面計算
- P-M 互制圖繪製
- 其他考試常用手算方法
```

**輸出物：**
```
1. raw/solutions/methods/[method-id]/[method-id].md
   → 完整說明文件（LaTeX 公式 + 步驟 + 邊界條件表）
2. raw/solutions/methods/[method-id]/[method-id]-chart.html
   → 圖形說明（如有）
```

**raw/solutions/methods/[method-id]/[method-id].md 格式：**
```markdown
# [方法名稱]

**方法 ID：** [method-id]
**知識分類：** 解題工具
**適用題型：** [列出適用的 topicId，如 `SS-U1-2`、`SS-U1-3`]

## 核心原理
## 邊界條件 / 對應關係表
## 步驟流程
## 常用型式與結果表
## 推導示範
## 圖形
## 出現題目（使用本方法的考題）
```

**修正既有方法論的公式錯誤（FIX-METHOD）**

`raw/solutions/methods/` 是規則 1 的例外，發現公式／係數／單位錯誤時可直接修正來源：

```
1. 驗算：邊界代入、量綱檢查、與 verified 題目解答交叉比對
   （只憑印象或單一參考書就改 = 不合格）
2. 改 raw/solutions/methods/[id]/[id].md
3. study/ 講義、教科書、study/data/unit-*.json 若引用同一公式，一併更正（單元資料改完重跑 scripts/build_unit_page.py）
4. 全庫 grep 同一個錯誤係數，其他頁面一併修正（archive/ 不改）
5. wiki/queries/log.md 追加紀錄：改了什麼、為什麼、怎麼驗證的
```

> **單位是最常見的錯誤來源**。同一條規範式在 ksi / tf·cm⁻² / kgf·cm⁻² / MPa 制的係數完全不同，
> 抄書時很容易把 A 制的係數配上 B 制的單位標註。
> **撰寫方法論頁時，係數一律附上單位制標註，並盡量同時給出無因次形式**（如 \(c\sqrt{E/F_y}\)）。

---

## REFRESH-DASHBOARD

**觸發語句：** `更新 XX 儀表板資料`／`更新五科儀表板資料`（Cowork 直接執行）

**用途：** `index.html`（資料夾根目錄的離線儀表板）讀取 `dashboard-data.js` 顯示題庫。當 `question_index.json` 變動（新增題目、改標籤）後，需重新生成快照。

**執行步驟：**
```
在知識庫根目錄執行：
  python scripts/refresh_dashboard.py XX       # 單科
  python scripts/refresh_dashboard.py --all    # 五科

腳本會：
1. 讀取 XX/raw/json/question_index.json 全部條目
2. 轉換為精簡陣列格式寫入 XX/dashboard-data.js 的 window.KB_QUESTIONS：
   [moduleId, primaryTopicId縮寫(去本科前綴), secondaryTopicIds縮寫, designMethod, viz內容碼陣列, tags, pdf補充筆記檔名陣列]
   - viz 內容碼：掃描 raw/solutions/XX-YYYY-N/ 下 *-viz.html（互動圖已停用，只為顯示 SS 舊檔）
   - pdf 補充筆記：掃描同資料夾所有 *.pdf（原始檔名）；無 PDF 寫入 []
3. 由根目錄 syllabus_taxonomy.json 產生 window.KB_UNITS／KB_TOPICS
   （本科子項；主副分類只能填本科子項）
4. 由 scripts/subject_profiles.json 產生 window.KB_SUBJECT（科目名、考卷檔名、designMethod 選項）
5. 在該科 wiki/queries/log.md 追加紀錄（由 Cowork 執行）
注意：XX/index.html 是五科共用樣板（scripts/templates/dashboard-index.html 的副本），
      不要個別修改；要改 UI 就改樣板，再複製到五科。
注意：SS 暫用原 repo 的 index.html／dashboard-data.js（已移除互動圖與補充 PDF 欄），
      改回共用樣板前不要對 SS 執行本指令（見 SS/SUBJECT.md §10）。
```

**補充說明：補充筆記 PDF**
- 使用者可將任意 `.pdf` 檔案放入 `raw/solutions/XX-YYYY-N/` 資料夾，命名無強制規範
- PDF 檔名清單由 REFRESH-DASHBOARD 指令掃描並寫入 dashboard-data.js（q.pdf 欄位），不再於前端即時掃描資料夾
- index.html 題庫瀏覽頁會依 dashboard-data.js 資料，對有 PDF 的題目卡片直接顯示「📎 補充筆記 PDF」按鈕（多筆時顯示筆數，點擊可選取要開啟的檔案）；無 PDF 者不顯示
- 開啟行為雙軌機制：線上環境（GitHub Pages）會直接開新分頁載入；本機環境（`file:///`）則需透過 File System Access API 授權讀取知識庫資料夾（與「📄 完整解析」共用同一次授權）。
- 使用者新增或移除 PDF 後，需對 Cowork 說「更新 XX 儀表板資料」才會反映在按鈕上

---

## FREQUENCY

**觸發語句：** `frequency XX`

**用途：** 在對話中快速列出某科高頻考點與單元比例（文字摘要，不產檔）。
要可反覆查看的熱圖頁 `study/frequency-XX.html`，改用 `subject-frequency-map` skill（`scripts/build_frequency.py`）。

**做法：** 數字一律以程式從 `raw/json/question_index.json` 計算（統計 `primaryTopicId` 與 `secondaryTopicIds`），不可手打。
輸出：高頻考點 Top 10（主／副題數）、各單元命題比例、近 5 年逐年考點。

---

## ANALYZE

**觸發語句：** `analyze XX YYYY`（例：`analyze SS 2018`）

**用途：** 深度分析某科某一年考卷的所有題目，輸出考點覆蓋、難度評估、與歷年的異同。

**輸出格式：**
```
【XX-YYYY 考卷分析】

題號 | 主考點      | 副考點    | 設計法 | 難度 | 解析狀態
-----|------------|----------|--------|------|--------
1   | SS-U1-2 梁桿件 |          | LRFD   | ★★★  | ✅ verified
...

【本年特色】：...
【與前一年比較】：...
【建議複習重點】：...
```

---

## PREDICT

**觸發語句：** `predict`（Cowork 直接執行）

**用途：** 根據歷年出題頻率與近年趨勢，推測今年（或下次考試）最可能出現的考點組合。

**執行步驟：**
```
1. 讀取 question_index.json 所有條目
2. 計算各 topicId 近10年、近5年、近3年的出題頻率
3. 找出「長期未考但高頻」的考點（潛在補考點）
4. 找出「連續出現」的高頻考點（持續重點）
5. 考慮該科每年題數與搭配慣例（通常各單元各一題）
6. 輸出預測報告與建議複習清單
```

---

## STUDY

**觸發語句：**
- `study SS-U2`（單元層級，Cowork 直接執行）
- `study SS-U1-2`（子項層級，改用 `unit-overview` skill）

**用途：** 彙整某單元／子項所有考題、重點公式、常見陷阱，產生帶圖表的互動 HTML 複習導覽頁面，存入 `study/` 目錄。

> ### ⚠️ 子項層級（`study XX-UN-n`）改由 skill 負責
>
> 子項層級一律做成**單元總覽** `study/unit-XX-Un-m.html`（`unit-overview` skill，`scripts/build_unit_page.py`），
> 一頁回答「這單元考什麼、哪些公式要背、每題要背哪幾條」。舊的 `study-XX-Un-m.html`（命題分析）與
> `formula-given-XX-Un-m.html`（給／背分界）及其 skill（`unit-exam-intel`、`unit-formula-map`）已停用，不再產生、也不做轉址頁。
> 單元層級（`study XX-UN`）沿用本節規格。（子項層級的舊「七區塊」規格已於 2026-11-09 刪除。）
>
> **教材分工（並存不覆蓋）**
> | | `lecture-`／`textbook-` | `unit-` | `frequency-` |
> |---|---|---|---|
> | 回答 | **為什麼**成立、公式怎麼推 | 這個單元**考什麼、要背什麼** | 整科**從哪裡開始讀** |
> | 產出者 | `unit-lecture`／`unit-textbook` | `unit-overview` | `subject-frequency-map` |
>
> 這些都是 skill 不是指令，不列入本文件的 12 個指令，說明見根目錄 `skills/README.md`。

**輸出格式：帶圖表的自含 HTML 檔案**（非純 Markdown，需使用 KaTeX 渲染公式）

### 單元層級（study XX-UN）頁面結構（六區塊）：
```
① 總覽（KPI 卡片 + 子項頻率橫條圖）
  - 4 個 KPI 卡：總題數、佔全科比例、排名、近6年出題率
  - 子項卡片（4個，點擊可過濾題目清單）
  - Canvas 橫向頻率條圖

② 年度熱力圖
  - 熱力格（每格=1年，深色=多題）
  - Canvas 年度堆疊長條圖（各子項不同顏色）

③ 考題清單（互動篩選）
  - 篩選按鈕（全部 + 各子項）
  - 每題顯示：題號/年度、題型摘要、關鍵 tags（前5個）、解析/圖解/驗證狀態 icon
  - 【重要】點擊題號時，一律以 `<a href="problems-view/XX-XXXX-N.html" target="_blank">` 連結至渲染層。
    **禁止使用 `../index.html#md=raw/solutions/...` 這種舊式連結**（那是把 .md 丟給瀏覽器，
    公式與附圖不會渲染，只會看到純文字）。`study/problems-view/` 是所有題目的 HTML 渲染層，
    公式、表格、附圖都已正確呈現。

④ 核心公式速查（KaTeX 渲染）
  - 每個子項一張公式卡，含主要計算公式與注意事項

⑤ 高頻陷阱 Top 8
  - 標色區分子項、附說明

⑥ 備考優先序
  - 表格：優先順序、掌握目標、備考要點
  - 整合備考策略說明框
```

**資料來源：** `raw/json/question_index.json`（從中統計各子項題數、年度分布、tags）

**命名規則：**
- 單元層級：`study/study-XX-UN.html`（例：`study/study-SS-U1.html`）
- 子項層級：由 skill 產生 `study/unit-XX-Un-m.html`（舊 `study-XX-Un-m.html` 已停用）

---

## FIND

**觸發語句：** `find [關鍵字]`（例：`find 塊狀剪力`、`find LTB`）

**用途：** 快速搜尋各科 `raw/solutions/` 下所有 .md 檔案及 `question_index.json`（可加科目代碼縮小範圍），找出含有特定關鍵字的題目。

**輸出格式：**
```
搜尋「塊狀剪力」，找到 X 筆結果：

XX-XXXX-N：[題型摘要]（出現位置：標題/tags/解析內容）
...
```

---

## RELATED

**觸發語句：** `related XX-XXXX-N`（例：`related SS-2018-2`）

**用途：** 根據 primaryTopicId、secondaryTopicIds、tags 的重疊程度，找出與指定題目最相關的其他題目，方便集中練習同類題型。

**輸出格式：**
```
【與 XX-XXXX-N 相關的題目】（依相似度排序）

★★★ XX-YYYY-N：[共同考點] [共同標籤X個]
★★☆ XX-YYYY-N：...
★☆☆ XX-YYYY-N：...
```

---

## UNVERIFIED

**觸發語句：** `unverified`（Cowork 直接執行）

**用途：** STATUS 指令的快捷版，只列出「已有解析但尚未驗算」的題目，方便追蹤待辦清單。

**輸出格式：**
```
【待驗算題目清單】（hasSolution=true 且 verificationStatus=unverified）

SS-2018-1：梁桿件設計
SS-2018-2：柱挫屈
...

共 X 題待驗算。驗算完成後說：「將 XX-XXXX-N 的 verificationStatus 改為 verified」
```

---

## QUERY

**觸發語句：** 直接提問（自由格式）

**範例：**
- 「哪些題目考到 LTB 側扭挫屈？」
- 「SS-U1-4 接合設計共出了幾題？」
- 「2015 到 2020 年有哪些題目考耐震設計？」

查詢結果可存入該科 `wiki/queries/` 供日後參考（告訴 Cowork「請存檔」即可）；跨科查詢存入主要相關科目。
