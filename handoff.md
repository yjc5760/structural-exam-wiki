# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-22 22:00

---

## 一、本次工作完成概況

### 1. 土壤力學與基礎工程（SM）單元總覽與觀念講義大升級
- **單元總覽（Unit Overview）建立與重產**：
  - 依照 `unit-overview` 規範新建 `SM/study/data/unit-SM-U2-2.json`（19 條公式卡、11 題）、`unit-SM-U3-2.json`（19 條、9 題，首次建立命題分析與給背）、`unit-SM-U3-3.json`（16 條、7 題）。
  - 編譯產出對應 `unit-SM-U2-2.html/pdf`、`unit-SM-U3-2.html/pdf`、`unit-SM-U3-3.html/pdf`（A4, scale 0.85, 展開 `#mxBox`, Katex 0 錯誤）。
  - 同步更新既有 `unit-SM-U2-3`，並重新生成全科命題頻率熱圖 `frequency-SM.html`。
  - 儀表板 `dashboard-data.js` 與 `index.html` 之 `UNIT_PAGES` 清單同步更新。

- **觀念講義（Lecture）新建與改版**：
  - 新建 `study/lecture-SM-U3-2.html/pdf`（擋土結構物穩定，9 題，9 張向量解析圖，17 頁）。
  - 新建 `study/lecture-SM-U3-3.html/pdf`（坡地工程，7 題，8 張向量解析圖，13 頁）。
  - 改版升級 `study/lecture-SM-U2-2.html/pdf`（深基礎）與 `study/lecture-SM-U2-1.html/pdf`（淺基礎），全面落實第一性原理與向量圖解。
  - 微調 `lecture-SM-U1-1`（圖 6-2 CH 標籤位置）與 `lecture-SM-U3-1`（圖 7-2 合力標籤防重疊）並重出 PDF。

- **題解勘誤與安全係數修正**：
  - 勘誤 `SM-2016-4 ㈡`：原解有效寬度 $B'$ 與梯形峰值 $q_{max}$ 混用，修正為純有效寬度法 $q_u/(\Sigma V/B')$，承載力安全係數由 1.89 修正為 2.52（結論仍為小於 3.0 不適宜）。
  - 狀態維持 `unverified`，更新 `audit-ledger-SM.json` 與 `SM/raw/solutions/SM-2016-4/SM-2016-4.md`。

- **全庫導覽與死連結清理**：
  - 盤點並修正 54 頁 `problems-view/*.html` 頁首「Ux-y 命題分析」連至已歸檔舊 `study-` 頁之死連結，全面導正連往對應 `lecture-SM-*.html` 觀念講義。
  - 將 22 頁題目返回鍵改連新上線之 `unit-` 單元總覽頁。
  - 對照內政部國土管理署 113 年生效之建築物基礎構造設計規範，核對抗滑動、抗傾覆、支承力、抗隆起等各項門檻與安全係數。

### 2. 前段進度回顧（同日完成）
- **RC 全 7 單元教科書講義與起點頁（`RC/start.html`）建置完工**：
  - 完成 RC-U1-1 至 RC-U4-2 共 7 份教科書等級講義（HTML + PDF）。
  - 完成 `RC/start.html` 整合 7 單元資源與 57 支 YouTube 影片連結。

---

## 二、本次變更檔案清單
1. **SM 單元總覽與講義資料庫**：
   - `SM/study/data/unit-SM-U2-2.json`、`unit-SM-U2-3.json`、`unit-SM-U3-2.json`、`unit-SM-U3-3.json`
   - `SM/study/unit-SM-*.html` / `*.pdf`（U2-2, U2-3, U3-2, U3-3）
   - `SM/study/lecture-SM-*.html` / `*.pdf`（U1-1, U1-3, U1-5, U2-1, U2-2, U2-3, U3-1, U3-2, U3-3）
   - `SM/scripts/lecture-figs/`（U1-1, U2-1, U2-2, U3-2, U3-3 繪圖腳本）
2. **SM 題解與題目頁面**：
   - `SM/raw/solutions/SM-2016-4/SM-2016-4.md`（勘誤）
   - `SM/study/problems-view/*.html`（96 題導覽連結導正）
   - `SM/raw/json/question_index.json`、`SM/dashboard-data.js`、`SM/index.html`、`SM/study/frequency-SM.html`
3. **科目紀事與 Wiki 紀錄**：
   - `SM/SUBJECT.md`、`SM/README.md`、`SM/wiki/queries/log.md`、`SM/wiki/queries/audit-ledger-SM.json`
   - `SM/檔案架構索引表.md`、`SM/知識庫使用說明書.md`
4. **交接備忘**：
   - `handoff.md`

---

## 三、踩坑與注意事項
- **偏心基礎承載力計算**：在同時有偏心及傾斜時，若採用 Meyerhof 有效寬度法（$B' = B - 2e$），分母應為均勻底壓 $\Sigma V / B'$，切勿與未折減寬度下的梯形峰值 $q_{max} = \frac{\Sigma V}{B}(1 + \frac{6e}{B})$ 混用。
- **單元總覽編譯依賴**：`build_unit_page.py` 需確保 JSON 中所有引用的公式卡編號、題目編號與題解內容完全存在，否則校驗會阻擋編譯。
- **返回導覽一致性**：題目瀏覽頁（problems-view）頂部導航若指向已搬移或已歸檔（archive）之頁面，需及時校正至現行之 `unit-*.html` 或 `lecture-*.html`。

---

## 四、下一步建議
1. **SM 剩餘子項單元總覽改版**：接續將尚未改版的子項（U1-1、U1-3、U1-5、U2-1、U3-1）依照 U2-2/U3-2/U3-3 格式逐步升級為單元總覽。
2. **起點頁擴充**：比照 `RC/start.html`，為 SM 規劃並建置整合讀書順序與影片資源之 `SM/start.html`。
3. **跨科目起點頁檢視**：針對 SA（結構分析）、SS（鋼結構）與 SD（耐震設計）評估起點頁與講義鏈結狀態。
