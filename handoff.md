# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-22 18:25

---

## 一、目前進度概況
- **鋼筋混凝土設計與預力（RC）教科書等級講義與起點頁全數建置完成**：
  - RC 全 7 個單元已全數依循第一性原理推導與向量圖解（unit-textbook 規範）產出獨立教科書講義（HTML + PDF + 圖源腳本）。
  - 單元覆蓋：
    1. `RC-U1-1` 梁彎矩強度分析與設計
    2. `RC-U1-2` 柱強度分析與設計
    3. `RC-U2-1` 剪力強度分析與設計
    4. `RC-U3-2` 樓版與基腳設計
    5. `RC-U3-3` 韌性要求與耐震設計
    6. `RC-U4-1` 預力梁斷面應力分析（預力上冊）
    7. `RC-U4-2` 預力量與偏心量設計（預力下冊）
  - **RC 起點頁（`RC/start.html`）建置完成**：
    - 依循讀書順序（U1-1 → U1-2 → U4-1 → U4-2 → U3-3 → U3-2 → U2-1）整合 7 大單元資源。
    - 彙整單元總覽、觀念講義、教科書、解題與公式講義影片（共 57 支 YouTube 連結）。
    - 連結資料結構化於 `RC/study/data/start-links.json` 與 `RC/study/data/start-links.txt`。

---

## 二、本次變更檔案
1. **起點頁與連結資料庫**（`RC/`）：
   - `RC/start.html`（新產生起點頁）
   - `RC/study/data/start-links.json`（結構化連結）
   - `RC/study/data/start-links.txt`（來源連結清單）
2. **科目規格說明**：
   - `RC/SUBJECT.md`（追加 2026-11-22 start.html 起點頁紀事）
3. **版本控制忽略清單**：
   - `.gitignore`（忽略批次上傳輸出日誌 `*_results.json`）
4. **交接備忘**：
   - `handoff.md`

---

## 三、踩坑與注意事項
- **起點頁路徑指向**：`scripts/build_start.py` 預設 repo/feedback 需注意指到 `structural-exam-wiki` 而非舊獨立 repo。
- **Git 追蹤規範**：
  - 批次上傳產生的日誌（如 `batch_upload_results.json`）及本機影音/暫存目錄均已在 `.gitignore` 排除，避免入版控。
  - 提交時避免 `git add .`，僅 stage 本次相關產出。

---

## 四、下一步建議
1. 依序檢查 SS（鋼結構）與 SA（結構分析）之起點頁與影片清單連結是否需要擴充或同步。
2. 針對新產生的 `RC/start.html` 進行線上 GitHub Pages 瀏覽測試與排版驗證。
3. 接續規劃 SD（耐震設計）或 SM（基礎工程）之系列教材改版。
