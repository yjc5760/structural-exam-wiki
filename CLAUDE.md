# 結構工程技師考試知識庫（五科合一）

> 本檔是**身份層**：分工、資料流、資料夾結構、重要規則。五科共用。
> 文中 `XX` 代表科目代碼（`SS`／`RC`／`SA`／`SD`／`SM`），各科專屬設定見 `XX/SUBJECT.md`。

## 專案說明

收錄「專門職業及技術人員高等考試結構工程技師」各科考古題的深度解析知識庫。
原本各科獨立建庫（exam-wiki-SS 等），2026-10-29 起合併為單一知識庫：**架構相同、各科一個資料夾**。
各科逐一從原 repo 搬入（SS 已於 2026-11-08 搬入），搬入步驟見下方「科目搬入」。

| 代碼 | 科目 | 資料夾 | 考卷檔名 |
|:---:|------|--------|---------|
| SS | 鋼結構設計 | `SS/` | `SS-YYYY_鋼結構設計.pdf` |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `RC/` | `RC-YYYY_鋼筋混凝土設計與預力混凝土設計.pdf` |
| SA | 結構學 | `SA/` | `SA-YYYY_結構學.pdf` |
| SD | 結構動力分析與耐震設計 | `SD/` | `SD-YYYY_結構動力分析與耐震設計.pdf` |
| SM | 土壤力學與基礎設計 | `SM/` | `SM-YYYY_土壤力學與基礎設計.pdf` |

> 命題大綱另有 `MM`（材料力學），目前未建資料夾。
> 要新增科目：在 `scripts/subject_profiles.json` 補設定後執行 `python scripts/scaffold_subject.py MM`。

- **題目編號格式：** `XX-YYYY-N`（如 `SS-2015-1`、`RC-2020-3`）
- **科目判定：** 指令中題號的前兩碼即科目；只說「解析 2024 年考卷」而未指明科目時，先問是哪一科
- **路徑慣例：** 本文件與 CLAUDE-CODE／SOLVE／SPEC 中的 `raw/`、`wiki/`、`study/` 一律指 **`XX/` 底下**的路徑；`scripts/`、`skills/` 指根目錄

**核心工作流程：**
```
在 Cowork 開啟知識庫根目錄（Project）
    ↓
說：「解析 YYYY 年 XX 考卷」（exam-solve skill）
Cowork 讀取 CLAUDE.md + XX/SUBJECT.md + 考卷 PDF + XX/raw/json/question_index.json
  → 建立所有尚無解析的題目資料夾（已有解析者跳過）
  → 從考卷擷取各題附圖，寫題目正本 XX-YYYY-N-problem.md（考卷原文＋判讀清單）
  → 等待你確認「判讀確認，請開始解題」
    ↓
【你做】檢查判讀清單（尤其標「不確定」的項目），確認後告知 Cowork（題目正本凍結）
    ↓
【重要】Cowork 一次只解一題，解完存檔後再繼續下一題
    ↓
盲解比對、勘誤（exam-wiki-pipeline／exam-errata skill）→ 同步 study/problems-view 等下游
    ↓
【你做】人工驗算後通知 Cowork 把 verificationStatus 改為 verified
```

---

## 兩個環境分工

| 環境 | 負責什麼 |
|------|---------|
| **你（使用者）** | 確認題目正本的判讀清單、hand 手寫補充、人工驗算後通知 Cowork 更新 verificationStatus；**git commit 由你自己做** |
| **Cowork** | 解題（SOLVE，**一次一題**）、存檔（.md；需要圖解時以 struct-diagram 產生 figs/）、更新 question_index.json、操作指令（status / reindex / add-method / refresh-dashboard / frequency / analyze / predict / study / find / related / unverified / query，共 12 個，詳見 CLAUDE-CODE.md）、教材 skill（單元總覽、講義、教科書、起點頁…）、直接維護 `wiki/queries/` 與 `study/`、**修正 raw/solutions/methods/ 的公式錯誤**（須驗算＋同步 study＋記 log）。寫完檔就停，列出動到的路徑交給使用者 commit |

---

## 單向資料流（每科各自一套，互不寫入）

```
XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md          ──→ XX/study/problems-view/XX-YYYY-N.html（scripts/render_problem_view.py）
XX/raw/solutions/XX-YYYY-N/XX-YYYY-N-problem.md  ──→ 同頁「📄 題目正本」區塊（放在解析之前）
XX/raw/json/question_index.json                  ──→ XX/dashboard-data.js（scripts/refresh_dashboard.py）
                                                 ──→ XX/study/unit-XX-Un-m.html（scripts/build_unit_page.py，資料 XX/study/data/unit-*.json）
                                                 ──→ XX/study/frequency-XX.html（scripts/build_frequency.py）
XX/study/data/start-links.json                   ──→ XX/start.html（scripts/build_start.py）
XX/raw/solutions/ ＋ question_index              ──→ XX/study/lecture-*、textbook-*（講義，Cowork 維護）
Cowork 查詢、稽核、盲解報告、卡關紀錄            ──→ XX/wiki/queries/（直接存入）
變更紀錄                                         ──→ XX/wiki/queries/log.md（append only）

根目錄 syllabus_taxonomy.json（唯一正本）──→ XX/raw/json/syllabus_taxonomy.json（副本，scripts/sync_taxonomy.py）

解題內容唯一來源：XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md
題意唯一來源：XX/raw/solutions/XX-YYYY-N/XX-YYYY-N-problem.md（尚未建立者以考卷 PDF 為準）
索引資訊唯一來源：XX/raw/json/question_index.json
方法論唯一來源：XX/raw/solutions/methods/（可修正，見規則 1）
命題大綱唯一來源：根目錄 syllabus_taxonomy.json（來自根目錄 命題大綱.pdf）
科目專屬設定唯一來源：scripts/subject_profiles.json ↔ XX/SUBJECT.md（兩者同步維護）
封存：XX/archive/wiki/（舊七層 wiki，唯讀參考、不再維護）
```

> **跨科題目**：題目只放在它所屬考卷的科目資料夾，不要把題目複製到他科；分類也只用本科子項（見「命題大綱分類」）。

---

## 資料夾結構

```
（知識庫根目錄）
├── README.md                ← 冷啟動導覽（五科總覽）
├── CLAUDE.md                ← 本檔（身份層）
├── CLAUDE-SOLVE.md          ← 指向 skills/exam-solve（解題流程已改為 skill）
├── CLAUDE-CODE.md           ← 12 個指令 Runbook
├── CLAUDE-SPEC.md           ← 格式／命名／完成標準
├── index.html               ← 五科入口頁（GitHub Pages 首頁）
├── syllabus_taxonomy.json   ← ⭐ 命題大綱分類正本（XX-Un-m）
├── 命題大綱.pdf              ← 考選部命題大綱原件
├── scripts/                 ← 五科共用腳本（各科資料夾不再放副本）
│   ├── subject_profiles.json   ← 科目專屬設定（考卷檔名、designMethod、常見圖解）
│   ├── scaffold_subject.py     ← 建立新科目骨架（不覆蓋既有檔）
│   ├── refresh_dashboard.py    ← 「更新儀表板資料」
│   ├── sync_taxonomy.py        ← 命題大綱正本 → 各科副本
│   ├── xcheck.py               ← 跨檔一致性掃描（python scripts/xcheck.py XX）
│   ├── extract_figure.py       ← 從考卷 PDF 擷取附圖
│   ├── render_problem_view.py  ← 題解 .md → study/problems-view/
│   ├── build_unit_page.py ＋ unit_page_template.html ← 單元總覽
│   ├── build_frequency.py      ← 全科出題頻率熱圖
│   ├── build_start.py ＋ parse_links.py ＋ start.css ← 起點頁
│   ├── audit_classification.py ← 主副分類稽核
│   └── templates/dashboard-index.html ← 五科共用儀表板樣板
├── skills/                  ← 配套 Cowork Skills 原始碼與 .skill 打包檔（五科通用）
│
├── SS/ RC/ SA/ SD/ SM/      ← 各科資料夾，結構相同：
│   ├── SUBJECT.md               ← 科目層設定＋科目 CHANGELOG
│   ├── README.md · 檔案架構索引表.md
│   ├── index.html · dashboard-data.js   ← 科目儀表板
│   ├── start.html               ← 起點頁（有做的科目）
│   ├── scripts/                 ← 只放本科一次性腳本（如 fixes/），共用腳本在根目錄
│   ├── raw/                     ← 原始資料（預設唯讀，例外見規則 1）
│   │   ├── exams/               ← XX-YYYY_<科目名>.pdf
│   │   ├── json/                ← question_index.json ✏️、concepts.json（備查）、syllabus_taxonomy.json（副本）
│   │   └── solutions/
│   │       ├── XX-YYYY-N/       ← 🔒 證據（.md、-problem.md 僅限規則 1 條件）
│   │       └── methods/         ← ✏️ 方法論
│   ├── study/                   ← unit-／lecture-／textbook-／frequency- 教材、data/、problems-view/、assets/katex/
│   ├── wiki/queries/            ← 稽核／盲解／查詢報告、卡關紀錄、log.md
│   └── archive/wiki/            ← 🗄️ 舊七層 wiki（唯讀參考）
```

> 共用腳本的執行位置：在**根目錄**執行並帶科目（`python scripts/build_unit_page.py SS-U1-1`、
> `python scripts/build_start.py --repo SS`），或在**科目資料夾**執行（`cd SS && python ../scripts/build_frequency.py`）。
> 兩種都可以；各腳本開頭的說明寫明參數。

---

## wiki 封存（2026-11-08 起五科一律適用）

舊的七層 wiki（concepts／problems／philosophy／methods／diagnosis／failure-modes／materials／code-ref、traps、topics、index.md、by-year.md）
是 AI 一次生成、與正本重複，且未持續核對（SS 2026-11-01 掃描發現 45 項錯誤，見 `SS/wiki/queries/觀念方法頁掃描-SS-2026-11-01.md`），
每次勘誤又多一份同步負擔，因此**各科只保留 `wiki/queries/`**，其餘搬到 `XX/archive/wiki/` 封存：

- 封存內容唯讀、不再維護、不再 compile，引用前必須與正本核對
- 讀書以 `study/`（題目瀏覽頁、單元總覽、觀念講義、教科書）為準；題解正本為 `raw/solutions/`；方法論正本為 `raw/solutions/methods/`
- 會寫 wiki 的指令（ingest、compile-all、lint、add-concept）停用
- 變更紀錄由 `wiki/log.md` 改為 `wiki/queries/log.md`（搬移時原檔整份移過去，內容不改）

**科目搬入**（RC、SA、SD、SM 從原 repo 搬來時；執行步驟見 `skills/exam-subject-migrate/SKILL.md`，說「把 exam-wiki-XX 搬進來」即會載入）：
1. 只搬檔案、不帶 git 歷史；原 repo 與其 GitHub Pages 舊網址先維持不動
2. 原 repo 的 `wiki/` 除 `queries/` 外整批移到 `XX/archive/wiki/`；`wiki/log.md` 移為 `wiki/queries/log.md`
3. 原 repo 的通用腳本若比根目錄新，先比對再併入根目錄 `scripts/`，科目資料夾不留副本
4. 原 repo 根目錄的 CLAUDE*.md 存參考副本於 `XX/archive/<原repo名>-root/`，本科專屬規則寫進 `XX/SUBJECT.md`
   - 跑 `python scripts/audit_classification.py XX XX`：主副分類指向他科的題目，列出改歸本科子項的建議，**經使用者確認後**才改 `question_index.json`（記 log）
5. 搬完逐檔比對、在新位置重跑該科腳本，再交給使用者 commit

---

## 命題大綱分類

> topicId 格式：`XX-Un-m`（U = 單元號，m = 子項號），合法值以根目錄 `syllabus_taxonomy.json` 為準，
> 各科子項表見 `XX/SUBJECT.md` §2。
> `primaryTopicId` 填最主要考點；跨子項時用 `secondaryTopicIds` 列出。

**分類原則（五科一律）：** `primaryTopicId`、`secondaryTopicIds` **只能填本科子項**，不引用他科的單元。題目涉及他科觀念時，歸到本科最接近的子項（例：SS 的耐震接頭 → SS-U1-4、強柱弱梁 P-M → SS-U1-3、My／Mp 形狀因子 → SS-U2-1）。
（SS 自 2026-10-30、五科自 2026-11-08 起。理由：頻率熱圖、單元總覽、分類稽核都只認本科子項，他科代號會被排除或報錯。）
`python scripts/audit_classification.py XX XX` 會把指向他科的主副分類列為問題。

---

## 重要規則

1. **`XX/raw/` 目錄下所有檔案一律不可修改**，僅以下五處例外：
   - `XX/raw/json/question_index.json`（索引唯一人工維護處）
   - `XX/raw/json/syllabus_taxonomy.json`（**只能**由 `scripts/sync_taxonomy.py` 從根目錄正本覆寫，不可手改）
   - `XX/raw/solutions/methods/`（方法論文件，可修正公式錯誤與單位標註）
   - `XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md`（**個別題目解析，僅限「解析勘誤」**，見下方條件）
   - `XX/raw/solutions/XX-YYYY-N/XX-YYYY-N-problem.md`（**題目正本**，見下方條件）

   > **為什麼 methods/ 是例外**：本規則要保護的是**證據**（考卷、AI 解析、驗證過的答案），
   > 這些一旦被改就失去可追溯性。但 `raw/solutions/methods/` 存的是**可維護的知識整理**，
   > 發現公式或係數錯誤時，必須改這個來源才算根治。
   >
   > **修改 methods/ 的三個條件（缺一不可）**：
   > ① 修正前先做**數值驗算**（邊界代入、量綱檢查、與驗證解答交叉比對），不可憑印象改；
   > ② 若 `study/` 講義或單元資料（`study/data/unit-*.json`）引用同一公式，一併更正；
   > ③ 在該科 `wiki/queries/log.md` 記錄**改了什麼、為什麼、怎麼驗證的**。
   >
   > **為什麼「解析勘誤」是例外**：本規則要保護的是**可追溯性**，不是保護錯誤。
   > `raw/solutions/XX-YYYY-N/XX-YYYY-N.md` 是解題內容的**唯一正本**，
   > `study/problems-view/` 由它生成 —— 只改下游副本，下次重新渲染會被蓋回錯誤版本，等於錯誤永久留存。
   >
   > ⚠️ **教訓（SS，2026-07-30／08-22）**：VERIFY 已查出 `SS-2013-2.md` 的量級筆誤，卻因舊條文
   > 「不在例外內」而不敢修；該檔後續被查出把考卷原文「柱 CD 為**靠桿**」讀成「鉸接」，挫屈載重高估約 3 倍。
   > **規則不該讓已知錯誤留在正本裡。**
   >
   > **修改 `XX-YYYY-N.md` 的四個條件（缺一不可）**（執行步驟見 `skills/exam-errata/SKILL.md`）：
   > ① **回考卷原文**：以 `raw/exams/` 的 PDF 為準重新判讀題意與圖說（有題目正本者先核對題目正本）。
   >    ⚠️ 考卷常為 Adobe-CNS1 CID 字型，`pdftotext` **抽不到中文**，公式與附表也常以影像嵌入；
   >    支承符號、鉸接圓圈、尺寸線只能目視 —— 必須轉圖（300–450 dpi）**逐頁目視判讀**；
   > ② **數值獨立重算**：每個數字以程式重算，並做量綱檢查與雙路徑交叉驗算，不可憑印象改；
   > ③ **同步全部下游**：`study/problems-view/`（`scripts/render_problem_view.py`）、該題 `figs/`（重跑 `gen_XX-YYYY-N.py`）、
   >    `raw/json/question_index.json`（tags）、`dashboard-data.js`、`study/` 講義與 `study/data/unit-*.json`（重跑 `scripts/build_unit_page.py`），必要時重出 PDF；
   > ④ 在該科 `wiki/queries/log.md` 記錄**改了什麼、為什麼錯、怎麼驗證的**，並在 .md 頁尾加「修正日期」。
   >
   > **題目正本 `XX-YYYY-N-problem.md` 的條件**（建立流程見 `skills/exam-solve`、`skills/exam-problem-split`）：
   > 依「一律轉圖目視、先盲讀」寫成；判讀清單每項標「圖上依據」與「把握」，不確定項排前面；
   > 建立時頭表「判讀狀態」為**待確認**，經使用者確認後改**已確認**並凍結，`question_index.json` 同步 `problemStatus`（draft／confirmed）。
   > 凍結後要改，須回考卷原圖重判、記 log，並重驗所有依該題意寫成的解析與講義。
   > 本檔只寫考卷有什麼（原文逐字、公式／附表照錄、圖面文字），**不寫解法**；解析 §1 與它衝突時以題目正本為準、勘誤解析。
   >
   > **不在例外內（仍完整受保護）**：`raw/exams/`（考卷原件）、同資料夾的
   > `-fig-*.png`／`-fig-*-vector.svg`／`-chart-*.png`／`-eqn-*.png`／`-hand-*.png`（考卷擷取圖與使用者截圖，皆為證據）、
   > 使用者放入的補充筆記 `*.pdf`。勘誤只准動 `.md` 正本與 Cowork 自己生成的 `gen_XX-YYYY-N.py`、`figs/`（SS 的舊 `*-viz.html` 已停用刪除）。
   >
   > **驗證狀態連動**：解析一經勘誤，該題 `verificationStatus` 必須退回 `unverified`，
   > 由使用者人工複核後才可改回 `verified`。

2. **`verifiedSolution` 是最終答案，不可質疑或重新計算**
   > 界線：本條保護的是**已人工驗算確認**（`verificationStatus = "verified"`）的答案。
   > 當使用者明示要求勘誤、或該題已退回 `unverified` 時，本條不阻止重新計算。
3. **各科 `wiki/queries/log.md` 只可 append，不可刪除已有紀錄**；影響多科或根目錄的變更記在根目錄 CHANGELOG（本檔末）
4. **wiki/ 只保留 `queries/`，由 Cowork 直接維護**；舊 wiki 在 `archive/wiki/`，唯讀、不再修改
5. **`verificationStatus` 只有使用者人工複核後才可改為 `verified`**（Cowork 不得自行改）
6. 題號連結使用 `[[XX-YYYY-N]]`（Obsidian 相容；儀表板閱讀器會導向 `study/problems-view/`）
7. **study/ 頁面一律由正本產生**：單元總覽改 `study/data/unit-*.json` 後重跑腳本、起點頁改 `study/data/start-links.json` 後重跑腳本，不手改產出的 HTML
8. **格式與命名規範見 CLAUDE-SPEC.md；操作指令（12 項）見 CLAUDE-CODE.md，全部由 Cowork 執行**
9. **一個指令只動一科**：除非使用者明說跨科（例：「五科一起更新儀表板」），不要順手修改他科資料夾
10. **科目專屬設定改兩處**：改 designMethod 允許值、常見圖解等時，`scripts/subject_profiles.json` 與 `XX/SUBJECT.md` 必須同步
11. **共用的東西只放一份**：腳本放根目錄 `scripts/`、skill 放根目錄 `skills/`；科目資料夾不放副本，科目差異寫成參數或 `SUBJECT.md` 設定
12. **skill 以 repo `skills/` 為正本**：使用者帳號安裝的 skill 是全域生效的副本（所有對話、所有科目共用）。
    改 skill 一律改 `skills/<name>/` 並重新打包 `skills/<name>.skill`，再請使用者重新安裝；
    在帳號端直接改過的 skill（例如經由對話中的儲存卡片），要同步寫回 `skills/`，兩邊不可分岔

---

## CHANGELOG（根目錄／跨科）

> 各科自己的變更紀錄在 `XX/SUBJECT.md` §9（SS 在獨立 repo 時期的完整紀錄已移至 `SS/SUBJECT.md`）。

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | **五科合併為單一知識庫**：根目錄 CLAUDE／CODE／SOLVE／SPEC／README 改寫為五科通用（`XX` 代號）；SS 專屬內容（CHANGELOG、設計哲學框架、互動圖內容碼）移入 `SS/SUBJECT.md`；依 SS 架構以 `scripts/scaffold_subject.py` 建立 RC／SA／SD／SM 骨架；`syllabus_taxonomy.json` 以根目錄為正本、各科 `raw/json/` 放同步副本；儀表板改為五科共用樣板（`KB_SUBJECT` 驅動）並新增根目錄五科入口頁；`skills/` 與 `xcheck.py` 移至根目錄共用；改為單一 git repo | 五科架構相同、只有考古題不同，分開維護使同一條規則要改五次 |
| 2026-10-29 | **解題與勘誤流程改為 skill**：新增 `skills/exam-solve/`（原 CLAUDE-SOLVE.md 的 SOLVE 流程＋CLAUDE-SPEC.md §4.1 完成檢核）與 `skills/exam-errata/`（規則 1 解析勘誤四條件的執行流程＋xcheck 分診）；CLAUDE-SOLVE.md 改為索引頁，ADD-METHOD 移入 CLAUDE-CODE.md；CLAUDE-CODE.md 新增「由 skill 負責的流程」對照表 | 只在解題／勘誤時才需要的長流程不必每次常駐；規則仍留在 CLAUDE.md，格式仍以 CLAUDE-SPEC.md 為唯一依據 |
| 2026-10-29 | **停用互動圖（`*-viz.html`）**：圖解一律由 `struct-diagram` skill 產生靜態 SVG＋PNG（`figs/`＋`gen_XX-YYYY-N.py`），exam-solve 解完一題後提議、exam-errata 勘誤後重跑；規則 1 的勘誤例外由 `*-viz.html` 改為 `gen_*.py`／`figs/`；SS 既有 19 份 viz 保留為舊檔 | 互動圖與 struct-diagram 功能重疊；靜態圖可重跑、可審核、可進 PDF 與影片管線 |
| 2026-10-29 | **附圖改由 Cowork 從考卷擷取**：新增 `scripts/extract_figure.py`（preview 座標格線找範圍、crop 產生 500 dpi 證據圖＋向量抽取）；exam-solve 階段一改為「擷取 → 判讀清單（使用者確認）→ struct-diagram 重繪」，觸發語改為「判讀確認，請開始解題」 | 免手動截圖；把判讀攤開確認可在解題前攔下判讀錯誤（SS-2013-4 試作：12 項盲讀全數與勘誤後解析一致，另抓到一處公式來源誤記） |
| 2026-11-08 | **SS 由獨立 repo `exam-wiki-SS` 重新搬入**（只搬檔案、不含 git 歷史；舊網站維持上線）；SS 較新的 skills（exam-start-page、unit-textbook、unit-* SKILL.md）、`xcheck.py`、勘誤回報表單併入根目錄；移除已停用的 formula-recall-deck、vha-treasure-map | 10-29 合併後 SS 仍在原 repo 持續更新，兩邊分岔 |
| 2026-11-08 | **根目錄規則整併（以 SS 11-01 以後的規則為準，升為五科通用）**：① wiki 封存（只留 `wiki/queries/`，其餘移 `archive/wiki/`），停用 ingest／compile-all／lint／add-concept（CLAUDE-CODE.md 16 → 12 個指令）；② 記錄檔改為 `wiki/queries/log.md`；③ 規則 1 加第五處例外「題目正本 `-problem.md`」；④ methods 修改條件 ② 與解析勘誤條件 ③ 改為同步 study／problems-view／單元資料；⑤ 規則 5、7 改寫（verified 人工複核、study 頁由正本產生），新增規則 11「共用的東西只放一份」；⑥ 單元總覽、起點頁列為標準教材；⑦ 共用腳本（render_problem_view、build_unit_page、build_frequency、build_start、parse_links、audit_classification）移至根目錄 `scripts/`，`build_unit_page.py` 一併修正 SM／MM 科目名稱對調；⑧ 新增「科目搬入」步驟；scaffold 骨架、skills 同步改寫 | 共用規則與腳本只維護一份；RC／SA／SD／SM 搬入時直接套用 |
| 2026-11-08 | **主副分類只能填本科子項（五科一律）**：原本副分類可掛他科子項，改採 SS 2026-10-30 起的規則；`subject_profiles.json` 各科 `relatedTopics` 清空、scaffold 範本與各科 `SUBJECT.md` §2 同步；「科目搬入」加一步分類稽核 | 頻率熱圖、單元總覽、分類稽核只認本科子項，他科代號會被排除或報錯 |
| 2026-11-08 | **skill 正本與安裝**：帳號裡 8 個 exam-wiki 用 skill（add-to-wiki、exam-wiki-pipeline、exam-problem-split、exam-wiki-audit、exam-practice-sheet、subject-frequency-map、blackboard-solution-video、video-handout）備份進 `skills/`（exam-practice-sheet 改指 structural-exam-wiki、subject-frequency-map 改用根目錄 build_frequency）；新增規則 12「skill 以 repo `skills/` 為正本」 | 帳號安裝版與 repo 版各自演進已分岔，需要單一正本 |
| 2026-11-08 | 新增 `skills/exam-subject-migrate/`：把 SS 搬入的實際流程寫成 skill（盤點→去處對照→複製→規則寫進 SUBJECT.md→分類稽核→重產驗證→收尾），供 RC／SA／SD／SM 搬入時使用 | 讓其他科照同一流程搬入，不必每次重想 |
