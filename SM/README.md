# SM — 土壤力學與基礎設計考古題知識庫

> 本資料夾是「結構技師考試知識庫」五科之一（原獨立 repo `exam-wiki-SM`，2026-11-11 搬入）。
> 流程、規則、指令、格式見根目錄 `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md`；SM 專屬設定（分析法判準、標籤詞彙、解題邏輯框架）與歷次變更見 **`SUBJECT.md`**。

**科目：** 專門職業及技術人員高等考試結構工程技師 — 土壤力學與基礎設計
**收錄範圍：** 2002–2025 年（民國 91–114 年），共 96 題（2026-09-18 起全庫重新驗算中，目前全部 unverified；題目正本尚未建立）
**題目編號：** SM-YYYY-N（如 SM-2018-1 = 2018年第1題）

---

## 這個資料庫是什麼

每道考古題都有一份 **深度解析**（LaTeX 公式、逐步計算、陷阱說明），解析由 AI 完成，經人工驗算確認。讀書以 `study/`（題目瀏覽頁、命題分析、觀念講義）為準。
題目正本（考卷原文＋判讀清單，`SM-YYYY-N-problem.md`）尚未建立，要補時說「SM 題目正本 第 1 批」（exam-problem-split）。

> wiki/ 只保留 `wiki/queries/`（稽核報告、變更紀錄 log.md）；舊 wiki 各層已封存於 `archive/wiki/`，不再維護、內容未經全面核對。

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一份新考卷 | 對 **Cowork** 說「解析 YYYY 年 SM 考卷」（exam-solve skill） |
| 補題目正本 | 「SM 題目正本 第 n 批」（exam-problem-split） |
| 勘誤／盲解比對 | 「勘誤 SM-YYYY-N」（exam-errata）、「跑 SM-U1-3 第 n 批」（exam-wiki-pipeline） |
| 講義／教科書 | 「生成 SM-U2-2 講義」「把 SM-U1-3 寫成教科書」 |
| 查詢知識 / 跨題分析 | 對 **Cowork** 直接提問 |

> SM 的單元教材仍是舊式「命題分析＋給／背＋講義」三件套，尚未改成單元總覽（`unit-overview`）；要改之前先看 `SUBJECT.md` §10。

---

## 快速導航

| 我想找... | 去哪找 |
|----------|-------|
| **視覺化瀏覽題庫** | **雙擊 `index.html`**（題庫搜尋篩選、考點統計、進度追蹤） |
| 特定題目的解析 | `raw/solutions/SM-YYYY-N/SM-YYYY-N.md` |
| 題目渲染頁（公式／附圖可讀） | `study/problems-view/SM-YYYY-N.html` |
| 子項命題分析（這個單元考什麼） | `study/study-SM-UN-n.html`（U1-1、U1-3、U1-5、U2-1、U2-2、U2-3、U3-1、U3-3） |
| 公式給／背分界 | `study/formula-given-SM-UN-n.html`（+ 同名 `.pdf`；7 個子項） |
| 單元觀念講義 | `study/lecture-SM-UN-n.html`（+ 同名 `.pdf`；U1-1、U1-3、U1-5、U2-1、U2-2、U2-3、U3-1） |
| 全科出題頻率熱圖 | `study/frequency-SM.html` |
| 方法論（承載力、壓密沉陷、流線網、土壓力、擋土牆、樁、Fellenius／Bishop） | `raw/solutions/methods/` |
| 影片講義 | `影片講義/` |
| 稽核報告 | `wiki/queries/`（目錄 `index.md`） |
| 操作紀錄 | `wiki/queries/log.md` |
| 舊 wiki 各層（2026-11-01 封存，唯讀參考） | `archive/wiki/`（見 `archive/README.md`） |
| 搬入前的原 repo 規則檔 | `archive/exam-wiki-SM-root/` |

---

## 檔案地圖

```
SM/
├── README.md          ← 你在這裡
├── SUBJECT.md         ← SM 科目設定（子項表、分析法判準、標籤詞彙、解題邏輯、CHANGELOG、與根目錄規則的差異）
├── 檔案架構索引表.md · 知識庫使用說明書.md
├── index.html         ← 離線儀表板 · dashboard-data.js（題庫快照，暫用原 repo 版，見 SUBJECT.md §10）
├── scripts/           ← 只放 SM 專屬腳本（lecture-figs/U1-1/ 講義附圖）；共用腳本在根目錄 scripts/
├── 影片講義/           ← 影片轉成的圖文講義（img/、video/）
│
├── study/
│   ├── study-*.html   ← 命題分析（舊式，unit-exam-intel 產出）
│   ├── formula-given-*.html ← 公式給／背分界 + .pdf（舊式）
│   ├── lecture-*.html ← 觀念講義 + .pdf（unit-lecture）
│   ├── frequency-SM.html ← 全科出題頻率熱圖（v1.1）
│   ├── gen_lecture-SM-U1-5_figs.py ← U1-5 講義附圖產生器
│   ├── problems-view/ ← 題目渲染頁
│   └── assets/katex/  ← 本機 KaTeX（勿刪）
│
├── raw/               ← 原始資料（預設唯讀；例外見根目錄 CLAUDE.md 規則 1）
│   ├── exams/         ← 考卷 PDF（SM-YYYY_土壤力學與基礎設計.pdf）
│   ├── json/          ← question_index.json ✏️、concepts.json（備查）、syllabus_taxonomy.json（副本）、pdf_*.txt（考卷文字抽取）
│   └── solutions/
│       ├── SM-YYYY-N/ ← 🔒 證據（.md 僅限規則 1 解析勘誤；gen_*.py、figs/ 可重產）
│       └── methods/   ← ✏️ 方法論，可修正公式（須驗算＋同步 study＋記 log）
│
├── wiki/queries/      ← 稽核報告、log.md
└── archive/           ← 🗄️ wiki/（舊七層）、exam-wiki-SM-root/（原 repo 規則檔、xcheck）
```

---

## 常用腳本（在知識庫根目錄執行）

```
python scripts/render_problem_view.py SM-2015-1     # 題目瀏覽頁（勘誤後重產單題）
cd SM && python ../scripts/build_frequency.py --check   # 全科頻率對帳（改成單元總覽前不要重產頁面）
python scripts/xcheck.py SM                         # 跨檔一致性掃描
python scripts/audit_classification.py SM SM        # 主副分類稽核
```

> 儀表板目前沿用原 repo 版（`SM_*` 變數），改回共用樣板前**不要**對 SM 執行 `refresh_dashboard.py`（見 `SUBJECT.md` §10）。

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（SM-2018-1，不是 SM-107-1）
- 不產生互動圖 `*-viz.html`；圖解一律用 struct-diagram 產生 `figs/*.svg`
- 公式必須用 LaTeX（`$c'$`、`$\phi'$`，不可寫純文字）
- `designMethod` 是**分析法**四值（總應力法／有效應力法／概念題／混合），判準見 `SUBJECT.md` §3
- `verificationStatus` 只有人工複核後才改 `verified`
- 主副分類只填 SM 子項（見 `SUBJECT.md` §2）

> 完整規則見根目錄 **CLAUDE.md**、**CLAUDE-SPEC.md**
