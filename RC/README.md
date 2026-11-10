# RC — 鋼筋混凝土設計與預力混凝土設計考古題知識庫

> 本資料夾是「結構技師考試知識庫」五科之一（原獨立 repo `exam-wiki-RC`，2026-11-11 搬入）。
> 流程、規則、指令、格式見根目錄 `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md`；RC 專屬設定、解題邏輯框架與歷次變更見 **`SUBJECT.md`**。

**科目：** 專門職業及技術人員高等考試結構工程技師 — 鋼筋混凝土設計與預力混凝土設計
**收錄範圍：** 2002–2025 年（民國 91–114 年），共 100 題（verified 7 題；題目正本尚未建立）
**題目編號：** RC-YYYY-N（如 RC-2018-1 = 2018年第1題）

---

## 這個資料庫是什麼

每道考古題都有一份 **深度解析**（LaTeX 公式、逐步計算、陷阱說明），解析由 AI 完成，經人工驗算確認。讀書以 `study/`（題目瀏覽頁、單元總覽、觀念講義）為準。
題目正本（考卷原文＋判讀清單，`RC-YYYY-N-problem.md`）尚未建立，要補時說「RC 題目正本 第 1 批」（exam-problem-split）。

> wiki/ 只保留 `wiki/queries/`（稽核報告、複核報告、變更紀錄 log.md）；舊 wiki 各層已封存於 `archive/wiki/`，不再維護、內容未經全面核對。

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一份新考卷 | 對 **Cowork** 說「解析 YYYY 年 RC 考卷」（exam-solve skill） |
| 補題目正本 | 「RC 題目正本 第 n 批」（exam-problem-split） |
| 勘誤／盲解比對 | 「勘誤 RC-YYYY-N」（exam-errata）、「跑 RC-U1-1 第 n 批」（exam-wiki-pipeline） |
| 單元總覽／講義／教科書 | 「做 RC-U3-2 單元總覽」「生成 RC-U3-2 講義」「把 RC-U1-1 寫成教科書」 |
| 查詢知識 / 跨題分析 | 對 **Cowork** 直接提問 |

---

## 快速導航

| 我想找... | 去哪找 |
|----------|-------|
| **視覺化瀏覽題庫** | **雙擊 `index.html`**（題庫搜尋篩選、考點統計、進度追蹤） |
| 特定題目的解析 | `raw/solutions/RC-YYYY-N/RC-YYYY-N.md` |
| 題目渲染頁（公式／附圖可讀） | `study/problems-view/RC-YYYY-N.html` |
| 子項單元總覽（考什麼＋公式給／背＋逐題公式表） | `study/unit-RC-UN-n.html`（資料 `study/data/unit-RC-UN-n.json`；目前 U1-1、U1-2、U2-1、U3-3、U4-1） |
| 單元觀念講義 | `study/lecture-RC-UN-n.html`（+ 同名 `.pdf`） |
| 全科出題頻率熱圖 | `study/frequency-RC.html` |
| 方法論（Whitney 應力塊、P-M 互制、彎矩放大、預力損失等） | `raw/solutions/methods/` |
| 影片講義 | `影片講義/` |
| 稽核、複核報告 | `wiki/queries/`（目錄 `index.md`） |
| 操作紀錄 | `wiki/queries/log.md` |
| 舊 wiki 各層（2026-11-01 封存，唯讀參考） | `archive/wiki/`（見 `archive/README.md`） |
| 搬入前的原 repo 規則檔、知識圖譜 | `archive/exam-wiki-RC-root/` |

> `study/study-RC-*.html`、`study/formula-given-RC-*.html` 是 2026-10-31 留下的轉址頁（自動跳到單元總覽），保留給舊連結用。

---

## 檔案地圖

```
RC/
├── README.md          ← 你在這裡
├── SUBJECT.md         ← RC 科目設定（子項表、設計法、標籤詞彙、解題邏輯、CHANGELOG、與根目錄規則的差異）
├── 檔案架構索引表.md · 知識庫使用說明書.md
├── index.html         ← 離線儀表板 · dashboard-data.js（題庫快照，暫用原 repo 版，見 SUBJECT.md §10）
├── scripts/           ← 只放 RC 專屬腳本（講義附圖 gen_lecture_*、apply_figs.py）；共用腳本在根目錄 scripts/
├── 影片講義/           ← 影片轉成的圖文講義（img/、video/）
│
├── study/
│   ├── unit-*.html    ← 單元總覽 + .pdf（unit-overview）
│   ├── lecture-*.html ← 觀念講義 + .pdf（unit-lecture）
│   ├── frequency-RC.html ← 全科出題頻率熱圖
│   ├── study-*／formula-given-*.html ← 舊頁轉址
│   ├── data/          ← unit-*.json（產生單元總覽的資料）
│   ├── problems-view/ ← 題目渲染頁
│   └── assets/katex/  ← 本機 KaTeX（勿刪）
│
├── raw/               ← 原始資料（預設唯讀；例外見根目錄 CLAUDE.md 規則 1）
│   ├── exams/         ← 考卷 PDF（RC-YYYY_鋼筋混凝土設計與預力.pdf）
│   ├── json/          ← question_index.json ✏️、concepts.json（備查）、syllabus_taxonomy.json（副本）、pdf_*.txt（考卷文字抽取）
│   └── solutions/
│       ├── RC-YYYY-N/ ← 🔒 證據（.md 僅限規則 1 解析勘誤；gen_*.py、figs/ 可重產）
│       └── methods/   ← ✏️ 方法論，可修正公式（須驗算＋同步 study＋記 log）
│
├── wiki/queries/      ← 稽核／複核報告、log.md
└── archive/           ← 🗄️ wiki/（舊七層）、exam-wiki-RC-root/（原 repo 規則檔、xcheck、知識圖譜）
```

---

## 常用腳本（在知識庫根目錄執行）

```
python scripts/render_problem_view.py RC-2015-1     # 題目瀏覽頁（取代原 repo 的 gen_problems_view.py）
python scripts/build_unit_page.py RC-U1-1           # 單元總覽（--all --subject RC 全部；--check 只檢查）
cd RC && python ../scripts/build_frequency.py       # 全科出題頻率熱圖
python scripts/xcheck.py RC                         # 跨檔一致性掃描
python scripts/audit_classification.py RC RC        # 主副分類稽核
```

> 儀表板目前沿用原 repo 版（`RC_*` 變數），改回共用樣板前**不要**對 RC 執行 `refresh_dashboard.py`（見 `SUBJECT.md` §10）。

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（RC-2018-1，不是 RC-107-1）
- 不產生互動圖 `*-viz.html`；圖解一律用 struct-diagram 產生 `figs/*.svg`
- 公式必須用 LaTeX（`$f'_c$`，不可寫純文字）
- `verificationStatus` 只有人工複核後才改 `verified`
- 主副分類只填 RC 子項（見 `SUBJECT.md` §2）

> 完整規則見根目錄 **CLAUDE.md**、**CLAUDE-SPEC.md**
