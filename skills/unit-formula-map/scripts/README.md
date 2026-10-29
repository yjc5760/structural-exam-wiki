# unit-formula-map / scripts

三支已驗證的 PDF 產線腳本。**沙盒沒有 Chromium，`playwright install` 也會下載失敗**，
所以路徑固定為 MathJax→SVG + WeasyPrint，不要再嘗試 headless 瀏覽器。

## 前置安裝

```bash
pip install weasyprint --break-system-packages -q
npm install mathjax-full --prefix /tmp/mj --silent
```

（若 mathjax 裝在別處，設環境變數 `MJ_PREFIX`。）

## 執行順序

```bash
WORK=/tmp/pdfw
python3 prerender.py study/formula-given-XX-Un-m.html $WORK
python3 build_pdf.py  study/formula-given-XX-Un-m.pdf  $WORK "exam-wiki-XX｜XX-Un-m 給／背分界　"
```

驗證（HTML 改完就跑，不要等到出 PDF 才發現）：

```bash
python3 verify.py study/formula-given-XX-Un-m.html map.json
```

## 各腳本在做什麼

| 腳本 | 職責 | 為什麼需要 |
|------|------|-----------|
| `prerender.py` | JS 動態內容 → 靜態 HTML | WeasyPrint 不執行 JS，直接丟會得到空殼 |
| `tex2svg.js` | TeX → SVG（`fontCache:'local'`） | WeasyPrint 不支援跨元素的全域字形快取 |
| `build_pdf.py` | 換數學式、套列印 CSS、出 A4 PDF | — |
| `verify.py` | 卡片 `ok` 清單 vs 逐年表 ✔ 交叉比對 | 兩處資料很容易打架，眼睛看不出來 |

## prerender 對列印版做的四件事（刻意的差異）

1. 卡片依主題分群，組內按「必背 → 別賭 → 通常會給」排序（螢幕版是可篩選平鋪）
2. 逐年表表頭改純文字（`tex2plain()`）+ `<colgroup>` 固定欄寬
   —— 表頭若留 MathJax SVG 會把欄寬撐歪，表格只佔 60% 頁寬還爆頁
3. 移除 `<nav>` / 篩選按鈕 / `<script>` / KaTeX 連結
4. 剝除 emoji —— WeasyPrint 無彩色 emoji 字型，🔴🟠🟢 會變豆腐方框

## HTML 端必須配合的兩個約定

- **卡片容器寫成 `<div class="cards" id="cards"></div>`**，逐年表寫成 `<table id="mx">`
  且 `<tbody></tbody>` 留空 —— prerender 靠這兩個錨點注入
- **行內數學一律 `\(…\)`，不要用單一 `$…$`**
  （KaTeX auto-render 沒設定單一 `$`，用了螢幕版就會露出原始 LaTeX）

## 已知陷阱

- `build_pdf.py` 偵測到 `merror` 會直接中止 —— 那代表 TeX 語法錯，
  硬出下去 PDF 上會是一整塊黑方框
- `pdftoppm` 輸出檔名：頁數 <10 是 `p-1.png`，≥10 補零成 `p-01.png`，先 `ls` 再讀
- 68 dpi 截圖會讓 `102年` 看起來像 `182年`；覺得數字怪就用
  `pdftotext -f N -l N` 抽該頁文字確認，**不要**直接改資料
