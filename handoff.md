# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-22 09:40

---

## 一、目前進度概況
- **鋼筋混凝土設計與預力（RC）教科書等級講義全數完工**：
  - RC 全 7 個單元已全數依循第一性原理推導與向量圖解（unit-textbook 規範）產出獨立教科書講義（HTML + PDF + 圖源腳本）。
  - 單元覆蓋：
    1. `RC-U1-1` 梁彎矩強度分析與設計（先前已 commit）
    2. `RC-U1-2` 柱強度分析與設計（本次新增）
    3. `RC-U2-1` 剪力強度分析與設計（本次新增）
    4. `RC-U3-2` 樓版與基腳設計（本次新增）
    5. `RC-U3-3` 韌性要求與耐震設計（本次新增）
    6. `RC-U4-1` 預力梁斷面應力分析（預力上冊，本次新增）
    7. `RC-U4-2` 預力量與偏心量設計（預力下冊，本次新增）

---

## 二、本次變更檔案
1. **教科書講義 HTML & PDF**（`RC/study/`）：
   - `textbook-RC-U1-2.html`, `.pdf`
   - `textbook-RC-U2-1.html`, `.pdf`
   - `textbook-RC-U3-2.html`, `.pdf`
   - `textbook-RC-U3-3.html`, `.pdf`
   - `textbook-RC-U4-1.html`, `.pdf`
   - `textbook-RC-U4-2.html`, `.pdf`
2. **圖源與章節程式碼**（`RC/study/figs-src/`）：
   - `textbook-RC-U1-2/`
   - `textbook-RC-U2-1/`
   - `textbook-RC-U3-2/`
   - `textbook-RC-U3-3/`
   - `textbook-RC-U4-1/`
3. **專案操作紀錄**：
   - `RC/wiki/queries/log.md`（追加 TEXTBOOK-RC-ALL 紀錄）

---

## 三、踩坑與注意事項
- **PDF 溢出截字問題**：長數學公式（展示式）需採 `aligned` 換行，避免邊界 overflow 截字。
- **Git 追蹤規範**：
  - `解題過程影片/`、`Claude outputs/` 與 `.work/` 等影音/暫存目錄均在 `.gitignore` 排除，不入版控。
  - 提交時避免 `git add .`，僅 stage 本次相關產出。

---

## 四、下一步建議
1. 檢視或發布教學影音資源（配合 `youtube-publisher` skill）。
2. 或展開其他科目（SA 結構分析、SS 鋼結構、SD 耐震設計、SM 基礎工程）之教科書等級教材改版。
