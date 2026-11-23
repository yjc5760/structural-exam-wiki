# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-23 21:15

---

## 一、本次工作完成概況

### 1. 土壤力學與基礎工程（SM）單元總覽（Unit Overview）全面推進
- **子項單元總覽（Unit Overview）建立與重產**：
  - **SM-U1-3（壓密與沈陷）**：新建 `SM/study/data/unit-SM-U1-3.json`（主 22＋副 8、30 條公式卡、4 群）、編譯產生 `study/unit-SM-U1-3.html`／`.pdf`（13 頁）。考卷逐題核對，發現 103 年（SM-2014-4）印製之 $T_v$–$U$ 經驗式漏平方、91 年（SM-2002-1）漏 $H$ 等印錯，均已載明於公式卡與驗算策略中。
  - **SM-U1-5（土壤剪力強度）**：新建 `SM/study/data/unit-SM-U1-5.json`（主 12＋副 4、21 條公式卡、3 群）、編譯產生 `study/unit-SM-U1-5.html`／`.pdf`（10 頁）。
  - **SM-U1-1（土壤基本物理性質與分類）**：新建 `SM/study/data/unit-SM-U1-1.json`（主 8＋副 10、19 條公式卡、4 群）、編譯產生 `study/unit-SM-U1-1.html`／`.pdf`（10 頁）。確認三相關係由獨立主考轉化為多數題型解題第一步。
  - **SM-U3-1（側向土壓力）**：新建 `SM/study/data/unit-SM-U3-1.json`（主 4＋副 13、17 條公式卡、3 群）、編譯產生 `study/unit-SM-U3-1.html`／`.pdf`（9 頁）。
  - **SM-U2-3（開挖支撐與穩定）逐題公式用途複核**：核對 17 題公式用途，移除僅為估算用途之隆起 2D 卡片，更新說明並重產 `unit-SM-U2-3.html`／`.pdf`。
  - 所有單元總覽均通過 Playwright 雙視界（1280px / 390px）檢驗，Console 0 錯誤、KaTeX 0 錯誤、無橫向溢出。

### 2. SM 教科書等級講義（Textbook）全系列建置
- **8 個重點單元教科書與向量製圖管線完工**：
  - 新建 `SM/study/figs-src/` 獨立章節製圖腳本庫（含數值計算 `calcs.py`、繪圖 `plot.py`、章節模組）。
  - 完成 8 單元教科書講義及 PDF 輸出：
    - `textbook-SM-U1-1.html` / `.pdf`（土壤基本性質）
    - `textbook-SM-U1-3.html` / `.pdf`（壓密與沈陷）
    - `textbook-SM-U1-5.html` / `.pdf`（剪力強度）
    - `textbook-SM-U2-2.html` / `.pdf`（深基礎與基樁）
    - `textbook-SM-U2-3.html` / `.pdf`（深開挖工程）
    - `textbook-SM-U3-1.html` / `.pdf`（側向土壓力）
    - `textbook-SM-U3-2.html` / `.pdf`（擋土結構物穩定）
    - `textbook-SM-U3-3.html` / `.pdf`（邊坡穩定工程）

### 3. 全庫導覽與連結全面導正
- **題目瀏覽頁（problems-view）導覽校正**：
  - 修正 46 頁題目瀏覽頁第一顆返回鍵，由重複之「觀念講義」改為連向對應「單元總覽（unit-SM-*.html）」。
  - 清理全庫舊版歸檔頁面死連結，現行 problems-view 已無任何連至舊版 `study-` 或 `formula-given-` 之失效連結。
- **全科索引與儀表板同步**：
  - 重新產出全科命題頻率熱圖 `frequency-SM.html`，教材欄位正確對齊最新 `unit-*.html`。
  - 更新 `SM/index.html` 之 `UNIT_PAGES`、`SM/README.md`、`SM/SUBJECT.md`、`SM/檔案架構索引表.md` 與 `SM/知識庫使用說明書.md`。

---

## 二、本次變更檔案清單
1. **SM 單元總覽資料庫與輸出**：
   - `SM/study/data/unit-SM-U1-1.json`, `unit-SM-U1-3.json`, `unit-SM-U1-5.json`, `unit-SM-U3-1.json`, `unit-SM-U2-3.json`
   - `SM/study/unit-SM-U1-1.html/pdf`, `unit-SM-U1-3.html/pdf`, `unit-SM-U1-5.html/pdf`, `unit-SM-U3-1.html/pdf`, `unit-SM-U2-3.html/pdf`
2. **SM 教科書講義與製圖原始碼**：
   - `SM/study/textbook-SM-U*.html` / `*.pdf`（U1-1, U1-3, U1-5, U2-2, U2-3, U3-1, U3-2, U3-3）
   - `SM/study/figs-src/`（8 個單元之章節圖檔產生腳本與資料庫）
3. **SM 題目頁面與觀念講義導覽**：
   - `SM/study/problems-view/*.html`（導正返回鍵與單元總覽連結）
   - `SM/study/lecture-SM-U1-1.html`, `lecture-SM-U1-3.html`, `lecture-SM-U1-5.html`, `lecture-SM-U3-1.html`
   - `SM/study/frequency-SM.html`, `SM/index.html`
4. **科目紀事與 Wiki 紀錄**：
   - `SM/SUBJECT.md`, `SM/README.md`, `SM/wiki/queries/log.md`, `SM/檔案架構索引表.md`, `SM/知識庫使用說明書.md`
5. **交接備忘**：
   - `handoff.md`

---

## 三、踩坑與注意事項
- **考卷原題印刷疏漏**：
  - 103 年（SM-2014-4）$T_v$–$U$ 經驗公式 $U \le 60\%$ 段漏印平方，已在單元總覽與解題策略註明需以 $T_v(50\%) = 0.196$ 檢驗考卷公式。
  - 91 年（SM-2002-1）$\Delta H = \Delta e / (1+e_0)$ 漏印試體高度 $H$，單元總覽已強調第一性原理。
- **題解假設相依性**：SM-2003-4、SM-2010-1 題解採用 $A_f=1$ 計算 UU 強度，該數值為合理工程假設但考卷未給定，已於 U1-5 公式卡明確標示。

---

## 四、下一步建議
1. **SM-U2-1（淺基礎）單元總覽改版**：目前 SM 科目僅剩 U2-1 尚未改為新版單元總覽（目前儀表板仍指引至舊頁），改版完成後 SM 全科單元總覽即 100% 覆蓋。
2. **建置 `SM/start.html` 起點頁**：比照 `RC/start.html`，整合 SM 8 大單元總覽、教科書講義、觀念講義與影音資源，提供一站式複習指引。
3. **推展其他科目（SA / SS / SD）**：評估結構分析（SA）與鋼結構（SS）之單元總覽與教科書講義規劃。
