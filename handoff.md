# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-25 18:00

---

## 一、本次工作完成概況

### 1. 結構動力學（SD）教科書等級專題教材（Unit Textbook）全系列完工
- **7 大單元教科書原始碼與完整輸出（unit-textbook）**：
  - 完成 7 個子項教科書章節與附圖原始碼目錄：`SD/study/figs-src/textbook-SD-U1-1/` 至 `textbook-SD-U3-2/`（含 `build.py`, `calcs.py`, `sdfig.py`, `plot.py`, 各章節 html 與圖表生成腳本）。
  - 編譯產出 7 份教科書等級 HTML 與 A4 印刷級 PDF：
    - `SD/study/textbook-SD-U1-1.html` / `.pdf`（結構動力基本性質及原理）
    - `SD/study/textbook-SD-U1-2.html` / `.pdf`（運動方程式推導）
    - `SD/study/textbook-SD-U1-3.html` / `.pdf`（單自由度、多自由度系統之動態分析及應用）
    - `SD/study/textbook-SD-U2-2.html` / `.pdf`（建築耐震設計規範）
    - `SD/study/textbook-SD-U2-3.html` / `.pdf`（橋梁耐震設計規範）
    - `SD/study/textbook-SD-U3-1.html` / `.pdf`（結構耐震設計）
    - `SD/study/textbook-SD-U3-2.html` / `.pdf`（隔減震原理）
  - 圖表嚴格通過第一性原理計算驗證與向量數值對帳，排版對齊既有 RC、SM 與 SS 教科書規格。

### 2. 結構動力學（SD）單元總覽（Unit Overview）7 子項全面導入（前階段已完工）
- 完成 7 個子項資料檔（`SD/study/data/unit-SD-*.json`），編譯產出 7 份單元總覽 HTML 與 A4 PDF。
- 公式卡 107 條、逐題公式用途紀錄 196 筆與考卷正本交叉驗證。

### 3. 結構動力學（SD）觀念講義（Lecture）全系列建置與對帳改版（前階段已完工）
- 新建 2 份高品質觀念講義（U2-3, U3-1），改版 5 份現有講義（U1-1, U1-2, U1-3, U2-2, U3-2）。
- 全數完成向量附圖、規範條文對齊與無障礙 / KaTeX 驗證。

### 4. 土壤力學與基礎工程（SM）起點頁（Start Page）完工（前階段已完工）
- 新建 `SM/start.html` 一站式複習起點頁，整合 SM 8 大單元總覽、觀念講義、教科書等級講義與精選影片。

---

## 二、本次變更檔案清單

1. **SD 教科書專題教材源碼與圖檔腳本**：
   - `SD/study/figs-src/textbook-SD-U1-1/`
   - `SD/study/figs-src/textbook-SD-U1-2/`
   - `SD/study/figs-src/textbook-SD-U1-3/`
   - `SD/study/figs-src/textbook-SD-U2-2/`
   - `SD/study/figs-src/textbook-SD-U2-3/`
   - `SD/study/figs-src/textbook-SD-U3-1/`
   - `SD/study/figs-src/textbook-SD-U3-2/`
2. **SD 教科書輸出成果（HTML & PDF）**：
   - `SD/study/textbook-SD-U1-1.html` / `.pdf`
   - `SD/study/textbook-SD-U1-2.html` / `.pdf`
   - `SD/study/textbook-SD-U1-3.html` / `.pdf`
   - `SD/study/textbook-SD-U2-2.html` / `.pdf`
   - `SD/study/textbook-SD-U2-3.html` / `.pdf`
   - `SD/study/textbook-SD-U3-1.html` / `.pdf`
   - `SD/study/textbook-SD-U3-2.html` / `.pdf`
3. **專案筆記與科目歷程**：
   - `handoff.md`
   - `SD/SUBJECT.md`

---

## 三、踩坑與注意事項
- **教科書印刷級排版相容性**：
  - PDF 產出採用 Chromium headless 搭配 `@page` 分頁 CSS 與 KaTeX 數學式，各單元長式推導與矩陣已針對分頁符號與跨頁排版進行微調避免切字。
  - 圖表全部採用 SVG 向量抽取並內嵌，避免在放大或列印時出現失真。

---

## 四、下一步建議
1. **結構動力學（SD）起點頁 `SD/start.html`**：比照 RC 與 SM，為 SD 整合 7 大單元總覽、觀念講義、教科書等級講義與解題索引，建立一站式起點頁。
2. **SM-U2-1（淺基礎）單元總覽**：SM 目前僅剩 U2-1 單元總覽待改版為新版格式。
3. **推進結構分析（SA）與鋼結構設計（SS）**：依照 SD/SM/RC 成熟之單元總覽、觀念講義與教科書規格，拓展其餘科目。
