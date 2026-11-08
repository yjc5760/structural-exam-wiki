# archive/wiki — 已封存（2026-11-01）

這個資料夾是 2026-11-01 從 `wiki/` 搬來的舊內容，**不再維護、不再同步勘誤**，只留作參考。

| 目錄 | 原用途 |
|---|---|
| problems/ | 98 題題解摘要（與 raw/solutions 正本重複） |
| concepts/、methods/、traps/、code-ref/ | 觀念、方法論、陷阱、規範條文整理 |
| diagnosis/、philosophy/、failure-modes/、materials/、topics/ | 題型診斷、設計哲學、破壞模式、材料、單元題目清單 |
| index.md、by-year.md | 舊主導航、依年份瀏覽 |

**為什麼封存**
- 內容是早期由 AI 從正本編譯的摘要，未逐頁核對；2026-11-01 掃描觀念頁與方法頁 84 頁發現 45 項確定錯誤（已修正，但其餘頁面未再核對），見 `wiki/queries/觀念方法頁掃描-SS-2026-11-01.md`。
- 與 `raw/solutions/`（正本）、`study/`（講義、單元總覽、題目瀏覽頁）重複，每次勘誤都要多同步一份。

**現在請用**
- 題解：`study/problems-view/`（由正本 `raw/solutions/` 產生）
- 觀念與公式：`study/lecture-SS-*.html`、`study/unit-SS-*.html`、`study/textbook-*`
- 方法論正本：`raw/solutions/methods/`（仍維護）
- 稽核紀錄與變更紀錄：`wiki/queries/`（含 `log.md`、`audit-ledger-SS.json`）

**注意**：搬移後目錄多了一層，頁內的相對連結與圖片路徑（`../../raw/...`）可能失效；索引頁的題號連結請改用 study/problems-view。
