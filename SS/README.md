# SS — 鋼結構設計考古題知識庫

> 本資料夾是「結構技師考試知識庫」五科之一（原獨立 repo `exam-wiki-SS`，2026-10-29 併入）。
> 流程與規則見根目錄 `CLAUDE.md`；SS 專屬設定、設計哲學框架與歷次變更見 **`SUBJECT.md`**。

**科目：** 專門職業及技術人員高等考試結構工程技師 — 第四科：鋼結構設計
**收錄範圍：** 2002–2025 年（民國 91–114 年），共 98 題
**題目編號：** SS-YYYY-N（如 SS-2015-1 = 2015年第1題）

---

## 這個資料庫是什麼

每道考古題都有一份 **深度解析**（LaTeX 公式、逐步計算、陷阱說明），解析由 AI 完成，人工驗算確認後才進 wiki。

**兩個工作角色：**

| 你要做什麼 | 怎麼做 |
|-----------|--------|
| 解一道新題 | 對 **Cowork** 說「解析 XXXX 年 SS 考卷」 |
| 把解析寫進 wiki | 對 **Cowork** 說「ingest SS-XXXX-N」 |
| 查詢知識 / 跨題分析 | 對 **Cowork** 直接提問 |
| 維護橫向知識工具 | 對 **Cowork** 說（diagnosis / failure-modes / materials / code-ref） |

> 所有操作都在 Cowork 對話中完成。完整指令清單見根目錄 **CLAUDE-CODE.md**（指令後加 `SS`，如 `status SS`）。

---

## 快速導航

| 我想找... | 去哪找 |
|----------|-------|
| **視覺化瀏覽整個知識庫** | **雙擊 `index.html`**（題庫搜尋篩選、考點統計、進度追蹤、指令速查） |
| 特定題目的解析 | `raw/solutions/SS-YYYY-N/SS-YYYY-N.md` |
| 子項深度複習講義（速查型） | `study/study-SS-UN-n.html`（說 `study SS-UN-n` 生成） |
| **單元觀念講義（練題前建立原理直覺）** | `study/lecture-SS-UN-n.html` + `.pdf`（說「生成 SS-UN-n 講義」生成） |
| wiki 題目頁（含標籤/圖形） | `wiki/problems/SS-YYYY-N.md` |
| 依年份瀏覽所有題目 | `wiki/by-year.md` |
| 概念說明（LTB、柱強度等） | `wiki/concepts/` |
| 解題策略（拿到考題怎麼判斷） | `wiki/diagnosis/` |
| 規範條文對應 | `wiki/code-ref/` |
| 操作紀錄 | `wiki/log.md` |

---

## 檔案地圖

```
SS/                    （CLAUDE*.md、skills/、syllabus_taxonomy.json 在上一層根目錄，五科共用）
├── README.md          ← 你在這裡（冷啟動導覽）
├── SUBJECT.md         ← SS 科目層設定＋設計哲學框架＋CHANGELOG
├── index.html         ← 離線儀表板（五科共用樣板）
├── dashboard-data.js  ← 儀表板快照（更新儀表板資料 指令重新生成）
├── scripts/build_frequency.py ← 全科出題頻率熱圖產生器
│
├── study/             ← 讀書講義
│   ├── study-*.html   ← 速查／複習頁（study 指令輸出）
│   ├── lecture-*.html ← 單元觀念講義 + 同名 .pdf（unit-lecture skill 輸出）
│   └── assets/katex/  ← 本機 KaTeX，供 lecture-*.html 離線渲染數學式（勿刪）
│
├── raw/               ← 原始資料（預設唯讀；例外見 CLAUDE.md 規則 1）
│   ├── exams/         ← 考卷 PDF（SS-YYYY_鋼結構設計.pdf）
│   ├── json/          ← question_index.json ✏️可改、concepts.json
│   └── solutions/     ← 每題一個資料夾，含 .md + 截圖 + 補充筆記 PDF
│       ├── SS-YYYY-N/ ← 🔒 證據，不可修改
│       └── methods/   ← ✏️ 方法論，可修正公式（須驗算＋同步 wiki＋記 log）
│
└── wiki/              ← 知識庫（七層架構）
    ├── problems/      ← 所有題目頁
    ├── concepts/      ← 概念頁
    ├── methods/       ← 解題方法論
    ├── diagnosis/     ← 題型診斷決策樹
    ├── failure-modes/ ← 失敗模式分類
    ├── materials/     ← 材料行為
    └── code-ref/      ← 規範條文對應
```

---

## 如何開始解一道新題

```
1. 在 Cowork 開啟知識庫根目錄（Project）
2. 說：「解析 2025 年 SS 考卷」
3. 依提醒截圖題目附圖，存入對應資料夾
4. 告知 Cowork「截圖完成，請開始解題」
5. Cowork 輸出 SS-2025-1.md（一次一題）
6. 人工驗算無誤後，說：「將 SS-2025-1 的 verificationStatus 改為 verified」
7. 說：「ingest SS-2025-1」→ Cowork 直接寫入 wiki
```

---

## 關鍵規則（避免常見錯誤）

- 年份用**西元**（SS-2015-1，不是 SS-104-1）
- PNG 截圖必須加序號（`fig-1.png`，不可寫 `fig.png`）
- 互動圖後綴必須是 `-viz.html`（`pm-viz.html`，不是 `pm.html`）
- 公式必須用 LaTeX（`$F_y$`，不可寫純文字）
- ingest 前確認 `verificationStatus = "verified"`

> 完整規則見根目錄 **CLAUDE-SPEC.md**
