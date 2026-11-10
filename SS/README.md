# SS — 鋼結構設計考古題知識庫

> 本資料夾是「結構技師考試知識庫」五科之一（原獨立 repo `exam-wiki-SS`，2026-11-08 搬入）。
> 流程、規則、指令、格式見根目錄 `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md`；SS 專屬設定、設計哲學框架與歷次變更見 **`SUBJECT.md`**。

**科目：** 專門職業及技術人員高等考試結構工程技師 — 第四科：鋼結構設計
**收錄範圍：** 2002–2025 年（民國 91–114 年），共 98 題
**題目編號：** SS-YYYY-N（如 SS-2015-1 = 2015年第1題）

---

## 這個資料庫是什麼

每道考古題都有一份 **深度解析**（LaTeX 公式、逐步計算、陷阱說明），解析由 AI 完成，經盲解比對與人工驗算確認。讀書以 `study/`（題目瀏覽頁、單元總覽、觀念講義、教科書）與 `start.html` 起點頁為準。

> wiki/ 只保留 `wiki/queries/`（稽核報告、盲解紀錄、變更紀錄 log.md）；舊 wiki 各層已封存於 `archive/wiki/`，不再維護、內容未經全面核對。

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一份新考卷 | 對 **Cowork** 說「解析 YYYY 年 SS 考卷」（exam-solve skill） |
| 勘誤／盲解比對 | 「勘誤 SS-YYYY-N」（exam-errata）、「跑 SS-U1-2 第 n 批」（exam-wiki-pipeline） |
| 單元總覽／講義／教科書 | 「做 SS-U1-1 單元總覽」「生成 SS-U1-1 講義」「把 SS-U1-1 寫成教科書」 |
| 更新起點頁 | 「依清單更新 SS 的 start.html」（exam-start-page） |
| 查詢知識 / 跨題分析 | 對 **Cowork** 直接提問 |

---

## 快速導航

| 我想找... | 去哪找 |
|----------|-------|
| **給考生的入口** | **`start.html`**（學習路徑、各單元教材、進度表） |
| **視覺化瀏覽題庫** | **雙擊 `index.html`**（題庫搜尋篩選、考點統計、進度追蹤） |
| 特定題目的解析 | `raw/solutions/SS-YYYY-N/SS-YYYY-N.md`（題目正本 `SS-YYYY-N-problem.md`） |
| 題目渲染頁（公式／附圖可讀） | `study/problems-view/SS-YYYY-N.html` |
| 子項單元總覽（考什麼＋公式給／背＋逐題公式表） | `study/unit-SS-UN-n.html`（資料 `study/data/unit-SS-UN-n.json`） |
| 單元觀念講義、教科書 | `study/lecture-SS-UN-n.html`、`study/textbook-SS-UN-n*.html`（+ 同名 `.pdf`） |
| 全科出題頻率熱圖 | `study/frequency-SS.html` |
| 影片講義 | `影片講義/` |
| 稽核、盲解比對報告 | `wiki/queries/`（總帳 `audit-ledger-SS.json`） |
| 操作紀錄 | `wiki/queries/log.md` |
| 舊 wiki 各層（概念、方法、陷阱、規範對應…） | `archive/wiki/`（封存，僅供參考） |
| 搬入前的原 repo 規則檔 | `archive/exam-wiki-SS-root/` |

---

## 檔案地圖

```
SS/
├── README.md          ← 你在這裡
├── SUBJECT.md         ← SS 科目設定（子項表、designMethod、設計哲學、CHANGELOG、與根目錄規則的差異）
├── 檔案架構索引表.md · 知識庫使用說明書.md
├── start.html         ← 起點頁（python scripts/build_start.py --repo SS）
├── index.html         ← 離線儀表板 · dashboard-data.js（題庫快照）
├── scripts/           ← 只放 SS 一次性腳本（add_backlink.py、fixes/）；共用腳本在根目錄 scripts/
├── 影片講義/           ← 影片轉成的圖文講義
│
├── study/
│   ├── unit-*.html    ← 單元總覽 + .pdf（unit-overview）
│   ├── lecture-*.html ← 觀念講義 + .pdf（unit-lecture）
│   ├── textbook-*.html← 教科書 + .pdf（unit-textbook）
│   ├── frequency-SS.html ← 全科出題頻率熱圖
│   ├── data/          ← unit-*.json、start-links.json／.txt（產生頁面的資料）
│   ├── problems-view/ ← 題目渲染頁
│   └── assets/katex/  ← 本機 KaTeX（勿刪）
│
├── raw/               ← 原始資料（預設唯讀；例外見根目錄 CLAUDE.md 規則 1）
│   ├── exams/         ← 考卷 PDF（SS-YYYY_鋼結構設計.pdf）
│   ├── json/          ← question_index.json ✏️、concepts.json（備查）
│   └── solutions/
│       ├── SS-YYYY-N/ ← 🔒 證據（.md、-problem.md 僅限規則 1 條件）
│       └── methods/   ← ✏️ 方法論，可修正公式（須驗算＋記 log）
│
├── wiki/queries/      ← 稽核／盲解報告、audit-ledger、log.md
└── archive/           ← 🗄️ wiki/（舊七層）、exam-wiki-SS-root/（原 repo 規則檔）
```

---

## 常用腳本（在知識庫根目錄執行）

```
python scripts/render_problem_view.py SS-2025-1     # 題目瀏覽頁
python scripts/build_unit_page.py SS-U1-1           # 單元總覽（--all --subject SS 全部；--check 只檢查）
cd SS && python ../scripts/build_frequency.py       # 全科出題頻率熱圖
python scripts/build_start.py --repo SS             # 起點頁
python scripts/xcheck.py SS                         # 跨檔一致性掃描
python scripts/audit_classification.py SS SS        # 主副分類稽核
```

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（SS-2015-1，不是 SS-104-1）
- PNG 截圖必須加序號（`fig-1.png`，不可寫 `fig.png`）
- 不產生互動圖 `*-viz.html`；圖解一律用 struct-diagram 產生 `figs/*.svg`
- 公式必須用 LaTeX（`$F_y$`，不可寫純文字）
- `verificationStatus` 只有人工複核後才改 `verified`
- 主副分類只填 SS 子項（見 `SUBJECT.md` §2）

> 完整規則見根目錄 **CLAUDE.md**、**CLAUDE-SPEC.md**
