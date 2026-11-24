# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-24 21:10

---

## 一、本次工作完成概況

### 1. 結構動力學（SD）單元總覽（Unit Overview）7 子項全面導入
- **子項單元總覽建立與編譯（unit-overview）**：
  - 完成 7 個子項資料檔：`SD/study/data/unit-SD-U1-1.json`、`unit-SD-U1-2.json`、`unit-SD-U1-3.json`、`unit-SD-U2-2.json`、`unit-SD-U2-3.json`、`unit-SD-U3-1.json`、`unit-SD-U3-2.json`。
  - 編譯產出 7 份單元總覽 HTML 與 A4 PDF（`study/unit-SD-*.html` / `*.pdf`），`--check` 檢驗全過（資料檔題目集合 100% 符合索引主＋副分類）。
  - 全科收錄 107 條公式卡（must / half / give 分級），建立 196 筆逐題公式用途紀錄（核對題解第一性原理套用）。
  - 考卷公式印製證據全面核對：99 份題目正本與 24 年考卷交叉驗證，24 年中 19 年曾印製 SD 公式／譜式，各題用途嚴格核實。

### 2. 結構動力學（SD）觀念講義（Lecture）全系列建置與對帳改版
- **新建 2 份高品質觀念講義**：
  - `study/lecture-SD-U2-3.html` / `.pdf`（15 頁）：Rayleigh 法、簡支梁週期、三軸反應譜、縱向振動單元。附圖由 `scripts/lecture-figs/SD-U2-3/` 向量繪製，數值由 `calcs.py` assert 對帳。
  - `study/lecture-SD-U3-1.html` / `.pdf`（17 頁）：容量設計、強柱弱梁、圍束筋、耐震梁柱細部、短柱效應、懸臂梁法、側推分析與崩塌機構。附圖由 `scripts/lecture-figs/SD-U3-1/` 與共用向量庫 `figkit.py` 繪製。
- **改版 5 份現有觀念講義**：
  - `lecture-SD-U1-1`、`lecture-SD-U1-2`、`lecture-SD-U1-3`、`lecture-SD-U2-2`、`lecture-SD-U3-2`：全面對齊 11-15 與 11-16 題解勘誤（如阻尼脈衝精確解、施加 2w 非質量加倍、臺灣規範耐震參數查表非 ASCE 7 固定比值、隔震系統有效週期與串聯模型等）。
  - 修復 SVG 圖形排版與字體樣式相容性，更新重跑附圖腳本。
  - 7 份講義均以 Headless Chromium 重產 PDF，通過 Playwright 雙視界、KaTeX 0 錯誤、Console 0 錯誤檢驗。

### 3. SD 全庫導覽與連結全面導正
- **題目瀏覽頁（problems-view）99 頁全面更新**：
  - 頁首按鈕統一改為「單元總覽（主分類）＋ 觀念講義（有講義之主/副分類）」，移除舊版給/背分界鈕，導覽連結與 referrer 完全對齊新架構。
- **全科索引與儀表板同步**：
  - 重產 `SD/study/frequency-SD.html` 命題頻率熱圖，教材欄完整對齊 7 個單元總覽與 7 份觀念講義。
  - 更新 `SD/README.md`、`SD/SUBJECT.md` 與 `SD/wiki/queries/log.md`。

### 4. 土壤力學與基礎工程（SM）起點頁（Start Page）完工
- **新建 `SM/start.html` 一站式複習起點頁**：
  - 依教材清單彙整產出 `SM/study/data/start-links.txt` 與 `start-links.json`。
  - 整合 SM 8 大單元總覽、觀念講義、教科書等級講義、公式記憶／觀念／教科書影片及精選 5 支解題影片連結，對齊 structural-exam-wiki 站內架構。
  - 同步更新 `SM/SUBJECT.md`。

---

## 二、本次變更檔案清單

1. **SD 單元總覽資料庫與輸出**：
   - `SD/study/data/unit-SD-*.json`（7 個單元）
   - `SD/study/unit-SD-*.html` / `*.pdf`（7 個單元）
2. **SD 觀念講義、製圖與輸出**：
   - `SD/study/lecture-SD-*.html` / `*.pdf`（新建 U2-3, U3-1；改版 U1-1, U1-2, U1-3, U2-2, U3-2）
   - `SD/scripts/lecture-figs/`（U2-3, U3-1 繪圖腳本、common/figkit.py）
   - `SD/scripts/lecture_U1-2_figs.py`, `lecture_U1-3_figs.py`, `build_figs_SD-U3-2.py`
3. **SD 導覽與題目瀏覽頁**：
   - `SD/study/problems-view/SD-*.html`（99 頁題目瀏覽頁導覽鈕更新）
   - `SD/scripts/fixes/2026-11-24_problems_view_lecture_btn.py`
   - `SD/study/frequency-SD.html`, `SD/README.md`, `SD/SUBJECT.md`, `SD/wiki/queries/log.md`
4. **SM 起點頁與連結資料**：
   - `SM/start.html`
   - `SM/study/data/start-links.json`, `start-links.txt`
   - `SM/SUBJECT.md`
5. **交接備忘**：
   - `handoff.md`

---

## 三、踩坑與注意事項
- **SD 規範條文與題解對帳細節**：
  - 臺灣耐震規範與 ASCE 7 的關鍵差異在於近斷層參數與地盤分類為鄉鎮分別查表，而非固定比值（$S_{DS} = \frac{2}{3}S_{MS}$）；$V^*$ 分母工址係數（一般工址 $4.2\alpha_y$、臺北盆地 $3.5\alpha_y$）已在講義與單元總覽標註。
  - 阻尼脈衝問題（如 SD-2003-2、2021-2）高阻尼下脈衝近似誤差甚大，講義與公式卡均明確強調需使用分段精確解或計入阻尼比。
- **自動化圖檢與視覺複核**：
  - U2-3、U3-1 講義的新製圖檔均已通過數值 assert 與 Playwright 邊界/出界檢查，建議使用者可抽空快速目視新圖排版效果。

---

## 四、下一步建議
1. **結構動力學（SD）起點頁 `SD/start.html`**：比照 RC 與 SM，為 SD 整合 7 大單元總覽、觀念講義與解題索引，建立一站式起點頁。
2. **SM-U2-1（淺基礎）單元總覽**：SM 目前僅剩 U2-1 單元總覽待改版為新版格式。
3. **推進結構分析（SA）與鋼結構設計（SS）**：依照 SD/SM/RC 成熟之單元總覽與講義規格，拓展其餘科目。
