# exam-wiki-SD 根目錄檔案（2026-11-11 搬入時的參考副本）

exam-wiki-SD 原為獨立 repo，2026-11-11 搬進 structural-exam-wiki/SD/。
這裡保存搬家當下原 repo 根目錄的規則檔與工具，供比對用：

| 檔案 | 說明 |
|------|------|
| CLAUDE.md | SD 當時的身份層（規則 1 為 index＋methods 兩處例外；完整 CHANGELOG 2026-07-25～11-01；「單位與符號慣例」已移入 `SD/SUBJECT.md` §3.1） |
| CLAUDE-CODE.md／CLAUDE-SOLVE.md／CLAUDE-SPEC.md | SD 當時的指令、解題、規格層（CLAUDE-SOLVE.md「設計哲學框架」已原文移入 `SD/SUBJECT.md` §8.2，三處疑點加註；CLAUDE-SPEC.md 的設計法 USD／WSD 與 §8 標籤表是 RC 殘留，未移入） |
| README.md | 原 repo 的冷啟動導覽（`SD/README.md` 已改寫為合併後路徑） |
| xcheck.py | SD 版跨檔掃描。與根目錄 `scripts/xcheck.py` 只差封存區判斷：SD 版以科目資料夾為準去找 `archive/wiki/`，根目錄版以執行目錄為準（合併後實際掃不到封存區）。是否改根目錄見 `SD/SUBJECT.md` §10 |

**這些是唯讀參考，不再維護。** 現行規則以根目錄 CLAUDE*.md 與 SD/SUBJECT.md 為準。
原 repo 與 git 歷史：https://github.com/yjc5760/exam-wiki-SD（舊網站維持上線）。
