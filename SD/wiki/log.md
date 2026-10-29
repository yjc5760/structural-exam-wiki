# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## 2026-10-29 — 依 SS 架構建立 SD 科目骨架

**操作類型：** 初始化

### 完成事項
- 以 `scripts/scaffold_subject.py SD` 建立目錄結構、`SUBJECT.md`、空的 `question_index.json`／`concepts.json`。
- 建立 wiki 導航頁：`index.md`、`by-year.md`、`topics/`（8 個子項）、`diagnosis/`、`failure-modes/`、`materials/`、`code-ref/` 的索引與類別頁。
- 複製共用資源：`study/assets/katex/`、`scripts/build_frequency.py`；`index.html` 使用五科共用樣板。

### 下一步
- 將歷年考卷放入 `raw/exams/`（命名 `raw/exams/SD-YYYY_結構動力分析與耐震設計.pdf`），開始「解析 YYYY 年 SD 考卷」。
