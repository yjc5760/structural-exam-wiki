---
name: unit-formula-map
description: >
  為六科考試知識庫（exam-wiki-SS/RC/SA/SD/SM/MM）的某個命題大綱單元，
  逐條盤點主要公式，並以歷屆考卷原文為證據，分辨出「哪些公式考卷通常會印給你」、
  「哪些必須自己背得出來」，輸出可篩選 HTML + 可列印 PDF。
  當使用者說「整理 XX-Un-m 主要公式」、「哪些公式題目會給」、「哪些要自己背」、
  「給背分界」、「公式給不給表」、「考卷會不會附公式」、「unit-formula-map」，
  或問某單元的公式該不該花時間背時，必須使用此 skill。
  判定一律以 raw/exams/ 的考卷原文為準，不得憑印象；
  掃描影像頁必須逐頁目視判讀，不可只靠文字抽取。
---

# unit-formula-map — 單元公式「給／背分界」盤點器

回答一個很實際的問題：**這個單元的公式，我到底要背哪些？**

考生的時間有限。有些公式考卷幾乎必印（背了是浪費），有些從來不印（沒背就整題卡死）。
本 skill 把某單元的主要公式逐條攤開，用**歷屆考卷原文**當證據判定，
讓背誦資源能精準投放。

**這不是公式速查表。** 知識庫裡通常已有 `study/study-XX-Un-m.html`（**命題分析**：這個單元考什麼）
與 `study/lecture-XX-Un-m.html`（觀念講義：為什麼成立）；本 skill 是第三種用途 —— **背誦決策**。
三者並存，互不覆蓋。

**檔名規則：** `study/formula-given-XX-Un-m.html` + `study/formula-given-XX-Un-m.pdf`

---

## 適用科目

| 代號 | 科目全名 | 資料夾 | 子項數 |
|------|---------|--------|-------|
| SS | 鋼結構設計 | `exam-wiki-SS` | 7 |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `exam-wiki-RC` | 14 |
| SA | 結構學 | `exam-wiki-SA` | 10 |
| SD | 結構動力分析與耐震設計 | `exam-wiki-SD` | 8 |
| SM | 土壤力學與基礎設計 | `exam-wiki-SM` | 14 |
| MM | 材料力學 | `exam-wiki-MM` | 13 |

> 科目全名與子項清單一律以 `raw/json/syllabus_taxonomy.json` 為準，**不要憑記憶填**
> （曾有其他文件把 SM 誤寫成「材料力學」、MM 誤寫成「工程數學」）。

單元代號格式 `XX-Un-m`。一次只做**一個單元**；使用者要整科時，逐單元重複呼叫。

---

## Step 0：定位

1. 確認目前工作資料夾是哪一科（看 `CLAUDE.md` 開頭的科目代碼）。
   若使用者講的單元代號科別與目前資料夾不符，**先問清楚**，不要自行猜測切換。
2. 讀 `raw/json/syllabus_taxonomy.json` 取得該單元的正式名稱。
3. 讀 `raw/json/question_index.json`，篩出屬於本單元的題目：

   ```python
   import json
   d = json.load(open('raw/json/question_index.json'))
   qs = d['questions']          # ← 注意：最外層是 dict，題目在 'questions' 鍵下
   unit = 'SS-U1-1'
   hit = [q for q in qs
          if q.get('primaryTopicId') == unit
          or unit in (q.get('secondaryTopicIds') or [])]
   ```

   記下每題的 `moduleId`、`designMethod`、`tags`，以及它是主考點（primary）還是副考點（secondary）。
   **副考點也要納入** —— 副考點年份同樣構成「考了卻沒給公式」的證據。

4. 若該單元一題都沒有，直接告知使用者並停止（沒有考卷證據就無從判定）。

---

## Step 1：建立證據基礎（本 skill 的核心，不可便宜行事）

### 1-1　全年份文字抽取

```bash
mkdir -p /tmp/txt
cd raw/exams
for f in XX-*.pdf; do pdftotext -layout "$f" "/tmp/txt/${f%.pdf}.txt"; done
```

**抽全部年份，不是只抽有本單元題目的年份。** 因為參考公式常是整張考卷共用一區，
別科／別單元的題目也可能順帶印出本單元要用的公式。

### 1-2　定位參考公式區塊

考卷把公式印出來有**三種擺法，三種都算「有給」**：

| 擺法 | 特徵 | 範例 |
|------|------|------|
| (a) 集中式 | 最後一題之後，標題多為「※參考公式」「參考資料」 | SS 104、108、110 年 |
| (b) 隨題式 | 緊跟在該題題目正下方 | SS 107、111、113 年 |
| (c) 內文式 | 混在題目敘述裡當已知條件給值 | SS 106 年直接給 `Cc=128`、96 年直接給 `U=0.85` |

搜尋關鍵字（各科通用）：

```bash
grep -n -E "參考公式|參考資料|下列公式|公式如下|附錄|僅供參考" /tmp/txt/*.txt
```

再用該單元的特徵符號補搜一輪（例如 SS 壓力桿件用 `0.419|0.877|0.658|Cc|Fa`；
RC 可用 `0.85f'c|β1|ρ|Vc`；SD 可用 `ζ|ω_n|SaSd`），避免漏掉沒有標題的隨題式公式。

### 1-3　⚠️ 強制逐頁目視判讀（不可略過）

`pdftotext` 對**掃描影像頁**與**以圖片嵌入的公式**完全無能為力，
而且失敗方式很陰險：它會成功抽出中文題幹，只有公式那一塊靜靜消失，看起來像「該年沒給」。

因此，符合以下**任一**條件的頁面，一律轉圖用 Read 工具親眼看過：

- 文字抽取結果裡出現「參考公式」「參考資料」等字樣，**但後面沒有跟著公式符號**
- 該年有本單元的題目，但整份抽取結果找不到任何公式
- 抽出的公式有明顯斷裂（例如只剩 `= ，  = exp −0.419 ∙ ，`，變數全掉光）
- 題目文字提到「如下式」「依下式計算」「參考公式：」但下一行是空的

```bash
mkdir -p /tmp/img
pdftoppm -r 110 -png "raw/exams/XX-YYYY_科目名.pdf" /tmp/img/YYYY
# 再把 PNG 複製到 outputs 目錄下用 Read 工具開啟
```

> **注意 `pdftoppm` 的輸出檔名**：頁數 <10 時是 `YYYY-1.png`，≥10 時補零成 `YYYY-01.png`。
> 先 `ls` 確認再 Read，不要直接猜檔名。

> **實績**：SS 這一輪，2013（對位圖＋萊梅厥公式）、2016（λp/λr 表）、
> 2023（Cc 與 Fa 全式）、2024（λ 與四條柱曲線）**四年的公式全都是影像**，
> 只靠文字抽取會全部誤判成「沒給」，結論會整個歪掉。

### 1-4　記下考卷的免責聲明

多數年份會寫「請自行選擇適合的公式，並檢查其正確性，若有問題應自行修正」，
近年更直接寫「題目所列之計算公式僅供參考應自負確認與勘誤責任」。

**這句話要原文引用進成果頁**，因為它是整份分析的前提：
**給了公式 ≠ 免背**，考生仍須認得哪一條該用、哪一條被改錯。

---

## Step 2：建立該單元的公式清單

依序從這些來源蒐集，去重後合併：

| 來源 | 取什麼 |
|------|--------|
| `wiki/methods/*.md` | 「適用題型」欄含本單元代號者，取其核心原理與解題步驟裡的每條式子 |
| `study/lecture-XX-Un-m.html`（若已存在） | 各章的主公式與其來源推導 |
| `wiki/concepts/`、`wiki/failure-modes/`、`wiki/materials/` | 本單元相關頁的判定式與門檻值 |
| `raw/solutions/XX-YYYY-N/*.md` | §3.5 VHA 的「主要公式」與 L2/L3 條目（最貼近實戰） |
| `wiki/code-ref/` | 規範條文的係數與適用範圍 |

**清單要涵蓋四類，不要只列「長得像公式」的東西** —— 最常被漏掉的正是後三類，
而它們恰好是最不會被印在考卷上的：

1. **主體計算式**：`Fcr = 0.658^(λc²) Fy`、`Mn = As fy (d - a/2)` 這種
2. **判斷式與分界**：`λc ≤ 1.5 用哪條`、`KL/r 與 Cc 誰大`、`拉力筋是否降伏`
3. **係數與折減值**：`φc = 0.85`、`φ = 0.75`、`孔徑 = db + 3 mm`、`β1 的取值規則`
4. **流程骨架**：「三種極限狀態取小」「兩軸都算取大」這類**沒有數學符號但決定給分**的規則

每條記錄：`公式名稱`、`LaTeX 式子`、`所屬主題分群`（3–6 群，如壓力/拉力/有效長度…）。

---

## Step 3：逐條判定（三級）

對每一條公式，掃過全部年份，得出兩個年份清單：

- **`ok`**：該年考卷印出此式（含 (a)(b)(c) 三種擺法）
- **`no`**：該年有本單元題目、且該題用得到此式，**但考卷沒印**

### 判定規則（採保守標準）

| 級別 | 判定條件 | 給考生的訊息 |
|------|---------|------------|
| **必背** | `ok` 為空；或曾出現「考了卻沒給」（`no` 非空）且 `no` 佔比高 | 自己要寫得出來 |
| **別賭** | 多數年份有給，但有明確沒給先例；或給的是舊版／簡化版需自行判斷修正 | 仍建議背 |
| **通常會給** | 凡考該題型幾乎必印，且無「考了卻沒給」的先例 | 背概念與用法即可 |

**保守標準的意思是：拿不準就往上歸。** 判定的目的是幫使用者控制風險，
把「必背」誤判成「會給」的代價，遠大於反過來多背幾條。

### 必須特別標註的四種情況

1. **同一條公式有新舊兩種寫法，考卷混用。**
   例：`Fcr = exp(-0.419λc²)Fy`（舊版規範）與 `Fcr = 0.658^(λc²) Fy`（AISC 現行）數值幾乎相同，
   但同一年只會給其中一種 —— 考生必須認得兩者是同一條。**兩種都要各自列一張卡。**

2. **給了公式，但那條不能直接用（誘餌）。**
   例：SS 113 年印出四條「無殘餘應力理想曲線」，題目要的卻是「含殘餘應力」的曲線。
   這種要在說明裡點破，不能只標「有給」。

3. **用了卻不定義。**
   例：SS 96、100 年印了含 `Cc` 的 `Fa` 式，卻沒給 `Cc = √(2π²E/Fy)` 的定義。
   這種一律降級到「別賭」以上。

4. **給了式子，但少給關鍵一步。**
   例：SS 104 年給填角銲 `φRn = 0.75×0.6F_EXX×t×L`，卻沒給 `t = 0.707w`，
   而題目要算的正是銲腳 `w`。

### 說明文字的寫法

每條的說明要具體到**年份與題號**，不要寫「常常會給」這種空話。
好的寫法長這樣：

> 24 年只有 91、92 兩年印出 φc=0.85。其餘所有 LRFD 柱題都預設你知道。
> 最常見的扣分是誤用 φ=0.9（那是彎矩用的）。

---

## Step 4：產出 HTML

自包含單檔，存 `study/formula-given-XX-Un-m.html`。結構固定四節：

| 節 | 內容 |
|----|------|
| 一、我怎麼判定的 | 三種擺法說明、考卷免責聲明原文引用、三級圖例、KPI 統計 |
| 二、公式逐條分界 | 可依「級別 × 主題」雙軸篩選的卡片清單 |
| 三、逐年證據表 | 24（或該科年份數）× 主要公式欄的 ✔ 矩陣，含每年備註 |
| 四、背誦策略 | 從證據推出的具體建議，不是泛泛而談 |

### 資料與呈現分離（重要）

把公式資料寫成 JS 陣列 `F`（卡片）與 `MX`（逐年矩陣），由 JS 渲染。
這樣才能做篩選，也讓後續 PDF 腳本能直接把資料撈出來重排。

```js
const F = [
 {g:"主題分群", lv:"must|half|give", nm:"公式名稱",
  eq:"$$LaTeX$$",
  meta:"具體到年份題號的說明，可含 \\(行內math\\)",
  ok:[2015,2024], no:[2016,2025]},
 // ...
];
// MX 每列：[西元年, 民國年, "本單元題號", ...10 個 0/1 欄, "備註"]
```

### ⚠️ 數學式分隔符（踩過的坑）

KaTeX auto-render 只設定了 `$$…$$`（顯示）與 `\(…\)`（行內）。
**行內數學一律用 `\(…\)`，絕對不要用單一 `$…$`** —— 用了不會渲染，
會在頁面上直接露出原始 LaTeX，而且很容易到列印階段才被發現。

在 JS 字串裡要寫成 `\\(` 與 `\\)`（反斜線需跳脫）。

### KaTeX 資源

用本機路徑 `assets/katex/katex.min.css` 等（離線可讀），不要用 CDN：

```html
<link rel="stylesheet" href="assets/katex/katex.min.css">
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'\\(',right:'\\)',display:false}],throwOnError:false});"></script>
```

若目標科目的 `study/assets/katex/` 不存在，從已有的科目複製一份過去。

### 導覽列

順序固定：**頁內錨點 → 同單元的另兩份教材 → 其他單元的給／背分界 → 本頁 PDF**。

```html
<nav>
  <a href="#how">判定方法</a>
  <a href="#cards">公式清單</a>        <!-- 全為說明題的單元寫「規定清單」 -->
  <a href="#matrix">逐年證據表</a>
  <a href="#strategy">背誦策略</a>
  <a href="lecture-XX-Un-m.html">▶ Un-m 觀念講義</a>
  <a href="study-XX-Un-m.html">▶ Un-m 命題分析</a>
  <!-- 其他已有 formula-given 的單元，逐一列出，標籤一律「▶ Un-m 給／背分界」 -->
  <a href="formula-given-XX-Un-k.html">▶ Un-k 給／背分界</a>
  <a href="formula-given-XX-Un-m.pdf" target="_blank"
     style="background:#eceff1;color:#455a64">🖨️ 本頁 PDF</a>
</nav>
```

**三條硬規則**（都是實際踩過的）：

- `study-XX-Un-m.html` 的按鈕一律寫 **「▶ Un-m 命題分析」**。
  不要寫「深度複習」或「速查頁」——那是 2026-08 以前那版七區段舊頁的名稱，該版已被
  `unit-exam-intel` 重構為只回答「這個單元考什麼」的命題情報頁。
- 指向**其他單元**的 `formula-given-` 按鈕，標籤必須完整寫成 **「▶ Un-m 給／背分界」**，
  不可只寫「▶ Un-m」——只寫代號時使用者看不出這顆按鈕會去哪一種頁面。
- **`🖨️ 本頁 PDF` 一定放最後一顆。** 新增其他單元的按鈕時要插在它前面；
  過去多次批次追加時直接 append 到 `</nav>` 前，造成 PDF 按鈕卡在中間、
  後面又冒出幾顆同類按鈕。

新增一個單元的 `formula-given-` 頁時，**其他單元的既有頁面也要補上指向新頁的按鈕**（雙向互連）。

---

## Step 5：產出 PDF

**沙盒沒有 Chromium，且 `playwright install` 會下載失敗（網路受限）。**
唯一可行路徑是 **MathJax→SVG + WeasyPrint**，不要浪費時間嘗試 headless 瀏覽器。

```bash
pip install weasyprint --break-system-packages -q
npm install mathjax-full --prefix /tmp/mj --silent
```

本 skill 附三支已驗證的腳本（見 `scripts/`），照順序跑：

```bash
WORK=/tmp/pdfw
# ① JS 動態內容 → 靜態 HTML
python3 scripts/prerender.py study/formula-given-XX-Un-m.html $WORK
# ② MathJax→SVG + WeasyPrint
python3 scripts/build_pdf.py study/formula-given-XX-Un-m.pdf $WORK "exam-wiki-XX｜XX-Un-m 給／背分界　"
# ③ 資料交叉驗證（HTML 一改就跑，別等出 PDF 才發現）
python3 scripts/verify.py study/formula-given-XX-Un-m.html map.json
```

`map.json` 把逐年表的欄位索引（從 3 起算）對應到卡片名稱：

```json
{"3": ["λc 定義"], "4": ["Fcr 舊版", "Fcr 新版", "Fcr 彈性"], "5": ["φc = 0.85"]}
```

### 為什麼需要 prerender

**WeasyPrint 不執行 JavaScript。** 頁面上的卡片與表格是 JS 渲染的，
直接丟給 WeasyPrint 會得到一份空殼。`prerender.py` 的工作是：

1. 用 node 把 `F` / `MX` 兩個陣列撈成 JSON（不要用正則手抄，會抄錯）
2. 在 Python 端重新生成靜態卡片 HTML —— 且**列印版重排**：
   依主題分群、組內按「必背 → 別賭 → 通常會給」排序（螢幕版維持可篩選的平鋪）
3. 把逐年表 `<thead>` 換成**純文字表頭** + `<colgroup>` 固定欄寬
   （表頭若含 MathJax SVG 會把欄寬撐歪，表格只佔 60% 頁寬還爆頁）
4. 移除 `<nav>`、篩選按鈕、`<script>`、KaTeX 連結
5. **剝除 emoji** —— WeasyPrint 沒有彩色 emoji 字型，🔴🟠🟢 會變成豆腐方框。
   列印版改用純文字標籤配色框（螢幕版保留 emoji）

### 列印 CSS 要點

```
@page { size:A4; margin:14mm 12mm 15mm 12mm; @bottom-center{ 頁碼 } }
table { table-layout:fixed; width:100%; min-width:0 !important; }
thead { display:table-header-group }   /* 跨頁重複表頭 */
.fc, tr, .note, .warn { break-inside:avoid }
h2, h3 { break-after:avoid }
#matrix, #strategy { break-before:page }
.mjd svg { max-width:100%; max-height:56px }
```

---

## Step 6：驗證（不可略過）

### 6-1　資料自我一致性（自動）

卡片的 `ok` 年份清單與逐年矩陣 `MX` 的 ✔ 必須完全對得起來。用 `scripts/verify.py` 跑，
不要用眼睛看 —— 這一關在 SS 這輪抓到 2 筆矛盾（2008 整區參考公式漏標、
2009 把「給了 Pn 卻叫你自己算 λc」誤標成有給）。

`verify.py` 同時會檢查：公式是否以 `$$` 包住、說明是否誤用單一 `$`、有無「零證據」的卡片。

### 6-2　抽樣回查考卷原文

隨機抽 3–5 條標記，回頭對照 `/tmp/txt/` 的抽取結果或頁面圖，確認年份沒標錯。
**特別要回查標成「通常會給」的那幾條** —— 誤判成會給，代價最大。

### 6-3　PDF 抽頁目視

```bash
pdftoppm -png -r 68 study/formula-given-XX-Un-m.pdf chk/p
```

用 Read 工具至少看：首頁、每個主題分群的第一頁、逐年表頁、最後一頁。要確認：

- [ ] 數學式正常，沒有黑方框（merror）或原始 LaTeX 外露
- [ ] 沒有豆腐方框（emoji 殘留）
- [ ] 逐年表在單頁內、佔滿頁寬、沒有欄位擠爆
- [ ] 卡片沒有被切成兩頁

> 低解析度（68 dpi）截圖會讓 `102年` 看起來像 `182年`。
> 覺得數字怪的時候，用 `pdftotext -f N -l N` 抽該頁文字確認，
> **不要**直接改資料。

### 6-4　文字層檢查（自動）

```bash
pdftotext out.pdf - | grep -c '\\\\[a-zA-Z]'   # 應為 0（無原始 LaTeX 外露）
# 並確認 🔴🟠🟢 等 emoji 皆已剝除
```

---

## 輸出

| 檔案 | 說明 |
|------|------|
| `study/formula-given-XX-Un-m.html` | 互動版，可依級別×主題篩選 |
| `study/formula-given-XX-Un-m.pdf` | 列印版，A4，依主題分群排序 |

完成後用 `present_files` 呈現兩個檔案，並用**三到五句話**講重點發現
（哪幾條最該背、有沒有「零公式年」這種極端證據、有沒有誘餌型給法），
不要複述流程。

---

## 常見錯誤

| # | 錯誤 | 後果 | 對策 |
|---|------|------|------|
| 1 | 只用 `pdftotext`，跳過影像頁目視 | 整份判定歪掉（SS 有 4 年公式全是影像） | Step 1-3 強制執行 |
| 2 | 行內數學用單一 `$…$` | 頁面直接露出原始 LaTeX | 一律 `\(…\)` |
| 3 | 直接把 HTML 丟 WeasyPrint | PDF 是空殼（JS 沒執行） | 先跑 `prerender.py` |
| 4 | 試著裝 Chromium / playwright | 浪費 5–10 分鐘後失敗 | 只走 MathJax+WeasyPrint |
| 5 | `question_index.json` 當成 list 讀 | `TypeError` | 題目在 `d['questions']` |
| 6 | 只算 primary 題目 | 漏掉副考點年份的證據 | secondary 也要納入 |
| 7 | 只列「長得像公式」的式子 | 漏掉 φ 值、判斷式、流程骨架 —— 而那正是最不會給的 | Step 2 的四類都要列 |
| 8 | 說明寫「常常會給」 | 使用者無法判斷風險 | 一律寫出年份與題號 |
| 9 | 卡片與逐年表各寫各的 | 兩處數字打架 | Step 6-1 自動交叉驗證 |
| 10 | 低解析度截圖看到怪數字就改資料 | 把對的改成錯的 | 先用 `pdftotext` 抽該頁確認 |
