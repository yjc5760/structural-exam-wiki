# 結構工程技師考試知識庫（五科合一）

**考試：** 專門職業及技術人員高等考試結構工程技師
**架構：** 五科共用一套流程、規則、腳本與 skills，每科一個資料夾、結構相同，只有考古題與教材不同
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
解析由 AI 完成，經盲解比對與人工驗算確認。讀書以各科 `study/`（題目瀏覽頁、單元總覽、觀念講義、教科書）與 `start.html` 起點頁為準。
舊的七層 wiki 已封存於各科 `archive/wiki/`（唯讀參考）。

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一份新考卷 | 對 **Cowork** 說「解析 2025 年 RC 考卷」 |
| 勘誤／重新驗算解析 | 「勘誤 SS-2013-2」（exam-errata skill） |
| 盲解比對／一批題目總控 | 「跑 SS-U1-2 第 1 批」（exam-wiki-pipeline skill） |
| 單元總覽／講義／教科書 | 「做 SS-U1-1 單元總覽」「生成 SS-U1-1 講義」 |
| 更新起點頁 | 「依清單更新 SS 的 start.html」（exam-start-page skill） |
| 查詢知識 / 跨題分析 | 直接提問（可指定科目） |
| 更新儀表板 | 「更新 RC 儀表板資料」或「更新五科儀表板資料」 |
| 新增一個科目（如 MM） | 補 `scripts/subject_profiles.json` → `python scripts/scaffold_subject.py MM` |

> 完整指令清單見 **CLAUDE-CODE.md**（指令後加科目代碼，如 `status SA`）。

---

## 檔案地圖

```
（根目錄）
├── README.md · CLAUDE.md · CLAUDE-CODE.md · CLAUDE-SPEC.md · CHANGELOG.md   ← 五科共用
├── index.html                ← 五科入口
├── syllabus_taxonomy.json    ← 命題大綱分類正本
├── 命題大綱.pdf
├── scripts/                  ← 五科共用腳本：scaffold、儀表板、題目瀏覽頁、單元總覽、頻率熱圖、起點頁、xcheck…
├── skills/                   ← 配套 Cowork Skills（五科通用；解題 exam-solve、勘誤 exam-errata 等）
└── SS/ RC/ SA/ SD/ SM/       ← 各科：SUBJECT.md、index.html、start.html、raw/、study/、wiki/queries/、archive/
```

---

## 如何開始解一份新考卷

```
1. 考卷 PDF 放進 XX/raw/exams/，命名 XX-YYYY_<科目名>.pdf（見 XX/SUBJECT.md §1）
2. 在 Cowork 開啟知識庫根目錄，說：「解析 YYYY 年 XX 考卷」
3. Cowork 從考卷擷取附圖，寫題目正本（考卷原文＋判讀清單：支承、尺寸、載重…）
4. 檢查清單後告知 Cowork「判讀確認，請開始解題」（題目正本凍結；一次解一題）
5. 解完自動產生 study/problems-view/ 題目頁；盲解比對、勘誤見 exam-wiki-pipeline／exam-errata
6. 人工驗算無誤後：「將 XX-YYYY-N 的 verificationStatus 改為 verified」
```

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（SS-2015-1，不是 SS-104-1）
- PNG 截圖必須加序號（`fig-1.png`，不可寫 `fig.png`）
- 圖解用 `struct-diagram` 產生（`figs/*.svg`＋`gen_XX-YYYY-N.py`）；互動圖 `-viz.html` 已停用
- 公式必須用 LaTeX（`$F_y$`，不可寫純文字）
- `verificationStatus` 只有人工複核後才改 `verified`
- 共用腳本與 skill 只放根目錄一份，科目資料夾不放副本
- git commit 由使用者自己做
- 改命題大綱分類只改根目錄 `syllabus_taxonomy.json`，再執行 `python scripts/sync_taxonomy.py`

> 完整規則見 **CLAUDE.md**、**CLAUDE-SPEC.md**
