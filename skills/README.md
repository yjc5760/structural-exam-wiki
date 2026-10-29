# 結構技師考試知識庫 Skills（五科通用）

本目錄收錄與**結構技師考試知識庫（SS／RC／SA／SD／SM）**配套的 Cowork Skills（原放在 `SS/skills/`，2026-10-29 移至根目錄共用）。

> ⚠️ 這些 skill 以**科目資料夾**（例如 `RC/`）為工作目錄，讀 `raw/json/question_index.json` 與 `raw/json/syllabus_taxonomy.json`；
> 後者是根目錄正本的同步副本（`python scripts/sync_taxonomy.py`）。skill 說明中的 `exam-wiki-XX` 一律對應現在的 `XX/` 資料夾。
安裝後可在 Claude Cowork 中直接呼叫，無需重複貼上指令。

---

## 安裝方式

1. 在 Claude Cowork 中開啟知識庫根目錄作為工作資料夾
2. 點擊下方對應的 `.skill` 檔案
3. 點「**Save skill**」即完成安裝
4. 安裝後直接對 Claude 說觸發語句即可使用

---

## Skills 清單

### `vha-treasure-map.skill`

**功能：** 將考題 VHA（變數層次分析）轉化為互動式「藏寶圖」HTML 儀表板

**觸發語句：**
- 「幫 SS-2020-3 做藏寶圖儀表板」
- 「VHA 轉化為儀表板」
- 「VHA dashboard」
- 「把 SS-XXXX-N 的 VHA 做成互動頁面」

**輸出：** `wiki/queries/SS-YYYY-N-treasure-map.html`（自包含 HTML，可直接開啟）

**儀表板功能：**
- KaTeX 數學式渲染（公式不顯示 raw LaTeX）
- 變數以顏色區分：L1 給定（綠）、L2 推導（藍）、本步求解（琥珀框）、最終未知（紅框）
- 知識線索卡片可相互連結，標示陷阱難關
- 自評進度追蹤（掌握 / 卡關 / 待複習）

**前置條件：** 目標題目需有完整的 `raw/solutions/SS-YYYY-N/SS-YYYY-N.md`，且包含 §3.5 VHA 區塊

---

### `unit-lecture.skill`

**功能：** 為某個命題大綱單元產生「理解導向」觀念講義（HTML + 可列印 PDF）

**觸發語句：**
- 「生成 SS-U1-2 講義」
- 「幫我做這單元的觀念講義」
- 「我要在練這單元考題前先懂原理」
- 「不要死記公式的講義」

**輸出：** `study/lecture-XX-Un-m.html` ＋ `study/lecture-XX-Un-m.pdf`

**與既有 `study-XX-Un-m.html` 的分工：**

| | `study-*.html`（既有） | `lecture-*.html`（本 skill） |
|---|---|---|
| 定位 | **命題分析**（考什麼） | 練題**之前**的觀念建立 |
| 內容 | 出題頻率、考點結構、考點漂移、考題清單、命題風險 | 物理直覺、原理圖解、公式來源 |
| 時機 | 決定練題順序、考前押題 | 第一次接觸該單元 |

兩者並存，互不覆蓋。

**講義結構：** §0 全景對照 → 依標籤分群的主題章節 → 解題決策流程圖 →
歷屆題×觀念對照表 → 陷阱總表 → 自我檢測（摺疊答案）→ ★ 精選 N 題（預設 5 題）

**特色：**
- 每個規範常數都追溯來源（如 `0.6` ← von Mises 的 `1/√3`）
- 以「破壞有沒有預警」統一解釋所有 φ 值與安全係數的差異
- 全內嵌 SVG 圖解，**一律由程式依範例數值繪製**（腳本存 `scripts/lecture-figs/`，可重跑）+ 本機 KaTeX（`study/assets/katex/`，離線可讀）
- 兩種模式：新建講義／改版既有講義（Step 10：截圖盤點 → 勘誤對帳 → 重繪 → PDF 重出 → log）
- 精選題附覆蓋率分析，並**誠實列出未涵蓋的考點群**
- PDF 走 MathJax→SVG + WeasyPrint（沙盒無 Chromium，此為唯一可行路徑）

**跨科目：** 六科（SS/RC/SA/SD/SM/MM）結構相同，同一份 skill 通用。
使用前請先在 Cowork 開啟目標科目的資料夾。
科目全名以 `raw/json/syllabus_taxonomy.json` 為準
（**SM = 土壤力學與基礎設計、MM = 材料力學**，2026-08-07 前的版本把這兩科寫反了）。

**前置條件：** 該科需有 `raw/json/question_index.json` 與 `wiki/topics/XX-Un-m.md`

---

### `unit-formula-map.skill`

**功能：** 盤點某單元的主要公式，以歷屆考卷原文為證據，分辨「哪些考卷會給、哪些必須自己背」

**觸發語句：**
- 「整理 SS-U1-1 主要公式」
- 「哪些公式題目會給？哪些要自己背？」
- 「幫我做 RC-U2-1 的給背分界」
- 「考卷會不會附公式」

**輸出：** `study/formula-given-XX-Un-m.html` ＋ `study/formula-given-XX-Un-m.pdf`

**與另外兩種 study 檔的分工：**

| | `study-*.html` | `lecture-*.html` | `formula-given-*.html`（本 skill） |
|---|---|---|---|
| 定位 | **命題分析** | 練題前建立觀念 | **背誦決策** |
| 回答的問題 | 這個單元**考什麼**？ | 這條公式為什麼成立？ | 這條公式**要不要背**？ |
| 時機 | 決定練題順序、考前押題 | 第一次接觸該單元 | 排讀書計畫、決定背誦優先序 |

三者並存，互不覆蓋。

**三級判定（保守標準，拿不準就往上歸）：**

| 級別 | 意思 |
|------|------|
| 🔴 必背 | 曾經考了卻沒給；或從未被印出來過 |
| 🟠 別賭 | 多數年份有給，但有沒給先例／給的是舊版需自行修正 |
| 🟢 通常會給 | 考該題型幾乎必印，背概念與用法即可 |

**方法要點：**
- 判定一律以 `raw/exams/` 考卷原文為證據，**不得憑印象**
- 「有給」涵蓋三種擺法：集中式（最後一題後）、隨題式（題目正下方）、內文式（當已知條件給值）
- **掃描影像頁強制逐頁目視判讀** —— SS 這輪有 4 年（102、105、112、113）的公式全是影像，
  只靠 `pdftotext` 會全部誤判成「沒給」
- 公式清單涵蓋四類：主體計算式、判斷式與分界、**係數與折減值**、**流程骨架**
  （後兩類最常被漏，卻恰好最不會印在考卷上）
- 附 `scripts/`（`prerender.py` / `build_pdf.py` / `tex2svg.js` / `verify.py`），
  PDF 走 MathJax→SVG + WeasyPrint（沙盒無 Chromium，此為唯一可行路徑）
- `verify.py` 自動交叉比對「公式卡年份清單」與「逐年證據表 ✔」，兩處打架會直接報錯

**跨科目：** 六科（SS/RC/SA/SD/SM/MM）結構相同，同一份 skill 通用。
一次做**一個單元**；要整科就逐單元重複呼叫。

**前置條件：** 該科需有 `raw/exams/*.pdf`、`raw/json/question_index.json`、
`raw/json/syllabus_taxonomy.json`，以及 `study/assets/katex/`（沒有就從別科複製）

---

### `unit-exam-intel.skill`

**功能：** 為某個命題大綱單元產生「命題情報頁」——只回答「這個單元考什麼」

**觸發語句：**
- 「做 SS-U1-2 的命題分析」
- 「這單元常考哪些考點？」
- 「出題趨勢／考點漂移」
- 「哪些考點空窗很久？幫我押題」
- 「重做速查頁」（舊稱，該頁現已正名為「命題分析」）

**輸出：** `study/study-XX-Un-m.html`（單一自包含 HTML，無 PDF）

**與另外兩種 study 檔的分工：**

| | `lecture-*.html` | `formula-given-*.html` | `study-*.html`（本 skill） |
|---|---|---|---|
| 回答的問題 | 這條公式**為什麼**成立？ | 這條公式**要不要背**？ | 這個單元**考什麼**？ |
| 資料來源 | wiki + 解析 + 規範 | `raw/exams/` 考卷原文 | `raw/json/question_index.json` |
| 可否自動重生 | 否 | 半自動 | **是（純資料驅動）** |
| 時機 | 第一次接觸該單元 | 排讀書計畫 | 決定練題順序、考前押題 |

三者並存，互不覆蓋。

**六個區塊：** 出題概況（KPI＋年度堆疊圖＋題型圓餅）→ 考點結構（3–6 群可篩選卡片）
→ 考點漂移（前後對切比較）→ 設計法／題型走向 → 考題清單（**主考點＋副考點**，
可篩選、連 `problems-view/`）→ 命題風險排序（空窗年數 × 頻率 × 趨勢）

**核心原則：頁面上的每個數字都必須由程式算出，不可手打。**
附兩支腳本（純標準函式庫，沙盒直接可跑）：

| 腳本 | 做什麼 |
|------|--------|
| `scripts/stats.py` | 從 `question_index.json` 算出 KPI、排名、空窗年段、前後對切、設計法分布、標籤頻率 |
| `scripts/verify.py` | 對帳成品頁：`Q[]` 題號集合、主／副旗標、篩選鈕數字、KPI、題號連結、禁用寫法 |

> **這條規則是有代價換來的**：SS-U1-1 舊頁的 KPI 寫「近 6 年 6/6」，實際是 4/6
> （2019–2021 三年空白）；另一處寫「共 7 題」，實際 6 題。兩個錯誤都活了很久，
> 因為沒有人會去重數 24 個考年。

**另附** `reference/template.html`：完整頁面骨架（CSS＋篩選邏輯＋兩張 Canvas 圖），
複製後取代 `{{...}}` 佔位符即可。

**遷移舊頁：** 目標單元若已有早期的「七區段深度複習頁」，SKILL.md Step 6 有重疊盤點
對照表——通常只有「命題分析」與「考題清單」該留，其餘分別與 lecture、formula-given 重複。
**檔名不要改**（另外兩份教材都有連回 `study-*.html`）。

**跨科目：** 六科（SS/RC/SA/SD/SM/MM）結構相同，同一份 skill 通用。
沒有 `designMethod` 欄位的科目（SA、MM 等）會自動改用其他軸線。
一次做**一個單元**。

**前置條件：** `raw/json/question_index.json` 與 `raw/json/syllabus_taxonomy.json`
（`study/problems-view/` 為選用，沒有時題號退化為純文字）

---

## 相關 Skills（已內建於 Cowork，無需另外安裝）

| Skill | 功能 | 觸發語句 |
|-------|------|---------| 
| `vha` | 為解析 .md 加入 §3.5 VHA 區塊 | 「幫 SS-XXXX-N 做 VHA」 |
| `add-to-wiki` | 將知識點新增至六層知識庫 | 「把這個知識點加入知識庫」 |

---

## 新增 Skill 規範

如需新增 skill，請遵守以下格式規範：

### Skill 檔案格式（`.skill` 檔）

```yaml
name: "skill-name"
description: "一句話說明這個 skill 做什麼"
triggers:
  - "觸發語句 1"
  - "觸發語句 2"
instructions: |
  # Skill 指令說明
  
  ## 前置條件
  [列出執行前需滿足的條件]
  
  ## 執行步驟
  [步驟化說明]
  
  ## 輸出
  [說明產生哪些檔案、存放位置]
  
  ## 注意事項
  [邊界條件、常見錯誤]
```

### 加入本清單的步驟

1. 將 `.skill` 檔放入本目錄（`skills/`）
2. 在本 README 的「Skills 清單」補充說明（格式參考 `vha-treasure-map.skill` 的說明方式）
3. 在 `CLAUDE.md` 的 CHANGELOG 追加一行說明此次新增

### 命名規則

| 規則 | 說明 |
|------|------|
| 全小寫連字號 | `vha-treasure-map.skill`，不用底線或大寫 |
| 動詞開頭或名詞主題開頭 | 清楚表達功能，如 `generate-xxx`、`analyze-xxx` |
| 副檔名固定 `.skill` | 不可用 `.md`、`.txt` |

---

## 貢獻

歡迎 PR！新增 skill 請按照上方「新增 Skill 規範」格式操作。

