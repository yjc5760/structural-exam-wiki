# 結構工程技師考試知識庫（五科合一）

**考試：** 專門職業及技術人員高等考試結構工程技師
**架構：** 五科共用一套流程與規則，每科一個資料夾、結構完全相同，只有考古題不同
**命題大綱：** `命題大綱.pdf`（考選部）→ `syllabus_taxonomy.json`（`XX-Un-m` 分類正本）

| 代碼 | 科目 | 資料夾 | 儀表板 | 科目設定 |
|:---:|------|--------|--------|---------|
| SS | 鋼結構設計 | `SS/` | `SS/index.html` | `SS/SUBJECT.md` |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `RC/` | `RC/index.html` | `RC/SUBJECT.md` |
| SA | 結構學 | `SA/` | `SA/index.html` | `SA/SUBJECT.md` |
| SD | 結構動力分析與耐震設計 | `SD/` | `SD/index.html` | `SD/SUBJECT.md` |
| SM | 土壤力學與基礎設計 | `SM/` | `SM/index.html` | `SM/SUBJECT.md` |

> 雙擊根目錄 `index.html` 可看五科總覽；各科題數即時統計請對 Cowork 說 `status`。

---

## 這個資料庫是什麼

每道考古題都有一份 **深度解析**（LaTeX 公式、逐步計算、陷阱說明、VHA 變數層次分析），
解析由 AI 完成，人工驗算確認後才進 wiki。

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一份新考卷 | 對 **Cowork** 說「解析 2025 年 RC 考卷」 |
| 把解析寫進 wiki | 「ingest RC-2025-1」 |
| 查詢知識 / 跨題分析 | 直接提問（可指定科目） |
| 更新儀表板 | 「更新 RC 儀表板資料」或「更新五科儀表板資料」 |
| 新增一個科目（如 MM） | 補 `scripts/subject_profiles.json` → `python scripts/scaffold_subject.py MM` |

> 完整指令清單見 **CLAUDE-CODE.md**（指令後加科目代碼，如 `status SA`）。

---

## 檔案地圖

```
（根目錄）
├── README.md · CLAUDE.md · CLAUDE-SOLVE.md · CLAUDE-CODE.md · CLAUDE-SPEC.md   ← 五科共用
├── index.html                ← 五科入口
├── syllabus_taxonomy.json    ← 命題大綱分類正本
├── 命題大綱.pdf
├── scripts/                  ← scaffold / refresh_dashboard / sync_taxonomy / xcheck / 儀表板樣板
├── skills/                   ← 配套 Cowork Skills（五科通用）
└── SS/ RC/ SA/ SD/ SM/       ← 各科：SUBJECT.md、index.html、raw/、wiki/、study/
```

---

## 如何開始解一份新考卷

```
1. 考卷 PDF 放進 XX/raw/exams/，命名 XX-YYYY_<科目名>.pdf（見 XX/SUBJECT.md §1）
2. 在 Cowork 開啟知識庫根目錄，說：「解析 YYYY 年 XX 考卷」
3. 依提醒截圖題目附圖，存入 XX/raw/solutions/XX-YYYY-N/XX-YYYY-N-fig-1.png
4. 告知 Cowork「截圖完成，請開始解題」（一次解一題）
5. 人工驗算無誤後：「將 XX-YYYY-N 的 verificationStatus 改為 verified」
6. 「ingest XX-YYYY-N」→ 該科 wiki 自動更新
```

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（SS-2015-1，不是 SS-104-1）
- PNG 截圖必須加序號（`fig-1.png`，不可寫 `fig.png`）
- 互動圖後綴必須是 `-viz.html`，內容碼依 `XX/SUBJECT.md` §4
- 公式必須用 LaTeX（`$F_y$`，不可寫純文字）
- ingest 前確認 `verificationStatus = "verified"`
- 改命題大綱分類只改根目錄 `syllabus_taxonomy.json`，再執行 `python scripts/sync_taxonomy.py`

> 完整規則見 **CLAUDE.md**、**CLAUDE-SPEC.md**
