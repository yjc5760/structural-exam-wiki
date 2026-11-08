---
name: unit-textbook
description: 為六科考試知識庫（exam-wiki-SS/RC/SA/SD/SM/MM）的某個命題大綱單元產生「教科書等級」講義：以第一性原理推導每一條公式、以程式計算的向量圖解說，全書只記幾顆「種子」，其餘公式都能在草稿紙上重建；可分上下冊，輸出 HTML＋A4 PDF。當使用者說「教科書等級講義」「第一性原理講義」「向量圖解講義」「不死背公式」「記不住公式但又要準備公式」「把 XX-Un-m 寫成教科書」「unit-textbook」，或給 unit-XX-Un-m.html／lecture-XX-Un-m.html 要求寫成能推導公式的講義時，必須使用此 skill。只要觀念講義（物理直覺、較短）改用 unit-lecture。
---

# unit-textbook — 第一性原理 × 向量圖解 教科書講義

為結構技師考試知識庫的**單一命題大綱單元**寫一本「不用死背公式」的教科書講義。
讀者設定：時間有限、**記不住長串符號但記得住畫面與道理**的考生（原始使用者年近 60）。

**核心承諾**：全書只要求記住少數「種子」（4～8 個最基本的物理事實）與幾個無法推導的規範數字；
其他每一條公式都附「看圖 → 第一性原理 → 三步推導 → 極限檢查 → 30 秒重建卡」，考場上忘了也能重推。

**與其他教材的分工（不要互相覆蓋）**

| 檔案 | 回答什麼 | 產生者 |
|---|---|---|
| `study/unit-XX-Un-m.html` | 考什麼、公式考卷給不給（must／half／give） | 單元總覽（輸入來源） |
| `study/lecture-XX-Un-m.html` | 物理直覺（較短的觀念講義） | unit-lecture |
| **`study/textbook-XX-Un-m[-冊].html／.pdf`** | **每條公式怎麼從種子推出來** | **本 skill** |

---

## 適用科目

| 代號 | 科目 | 資料夾 |
|---|---|---|
| SS | 鋼結構設計 | `SS/` |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `RC/` |
| SA | 結構學 | `SA/` |
| SD | 結構動力分析與耐震設計 | `SD/` |
| SM | 土壤力學與基礎設計 | `SM/` |
| MM | 材料力學 | `MM/` |

科目全名一律以 `raw/json/syllabus_taxonomy.json` 為準。各科的種子起手建議見 `references/subject-seeds.md`（只是建議，必須用該科考題確認）。

---

## 流程總覽

| 步驟 | 做什麼 | 產出／停點 |
|---|---|---|
| 0 | 讀輸入資料 | — |
| 1 | **提出計畫給使用者審閱**（種子、章節、分冊、取捨） | ⛔ 等使用者核可 |
| 2 | 建工作資料夾 `new_unit.py` | `study/figs-src/textbook-XX-Un-m/` |
| 3 | 先寫 `calcs.py`（全部數值） | 數值表 |
| 4 | **試讀版**：第 0～2 章，給使用者看文風、字級、圖 | ⛔ 等使用者回饋 |
| 5 | 寫完其餘各章（每冊最後一章是總整理） | — |
| 6 | 驗證（`render_check.py` ＋逐張看圖＋數字對帳） | 檢查清單全過 |
| 7 | 交付：HTML／PDF 寫進 `study/`、原始碼留在 `figs-src/` | 告知檔名 |

> 使用者未回應（排程、離開）時：Step 1 用下方「預設選擇」繼續，並在交付訊息最上方寫明採用了哪些假設。

---

## Step 0　讀輸入

1. `study/unit-XX-Un-m.html` 與 **`study/data/unit-XX-Un-m.json`**（最重要）：
   - `F[]`：每條公式的 `nm`、`eq`、`lv`（`must`＝必背、`half`＝別賭、`give`＝會給）、`meta`（證據敘述）、`ok`（有印的年份）
   - `Q[]`：本單元考題（`id`、`cl` 考點群、`sum`、`ty`），以及 `risk`、`strategy`
2. `study/lecture-XX-Un-m.html`：既有觀念講義（可沿用其章節骨架與陷阱，但數字要重算）。
3. 範例要用的考題：`raw/solutions/XX-YYYY-N/XX-YYYY-N.md`（**以勘誤後版本為準**；先看 `wiki/queries/log.md` 有沒有該題的勘誤紀錄）。
4. 若 `study/figs-src/textbook-XX-Un-m/` 已有草稿，**沿用**，不要從頭來。

讀檔用 device_bash 在使用者電腦上做（只讀、不搬檔）；HTML 用 python 去標籤後擷取文字即可。

## Step 1　提出計畫（一定要先給使用者審閱）

計畫要包含（格式見 `references/planning.md`）：
1. **種子表**：4～8 顆，每顆配「用哪張圖記」「一句白話」「會推出哪些公式」。
2. **每條公式的六步格式**（看圖→白話→推導→極限檢查→給背標籤→重建卡）。
3. **章節大綱**：每章主題＋主要向量圖；最後一章是總整理（種子樹、流程圖、一頁公式卡、精選 5 題、綜合重建練習）。
4. **排版**：內文 18px、圖內最小字 14px（使用者指定過，見下方「已確認的偏好」）。
5. **待決問題**（用 AskUserQuestion，每題附預設）：
   - 既有草稿沿用或重寫（預設：沿用）
   - 一冊或分冊（單元有兩個本質不同的主軸時建議分冊，例：拉力／壓力）
   - 兩套規範（LRFD／ASD、USD／WSD…）並列或主附錄（預設：並列，並寫出兩者換算關係）
   - 久未出題或與他科重疊的子題要不要寫（依 `risk` 表；預設：精簡或不寫）

**不要在核可前開始寫。**

## Step 2　建工作資料夾

在知識庫根目錄執行：
```bash
python3 <skill>/scripts/new_unit.py XX-Un-m                 # 單冊
python3 <skill>/scripts/new_unit.py XX-Un-m --volumes a,b   # 分冊（key 用英文）
```
產生 `study/figs-src/textbook-XX-Un-m/`：`lib.py`、`plot.py`、`build.py`、`render_check.py`、`textbook.json`、`calcs.py`、`ch0.html`、`figs_ch0.py`。
然後編輯 `textbook.json`（`meta`、各冊 `title`／`h1`／`sub`／`theme`／`chapters`）。

章號**跨冊連續**（上冊 0～6、下冊 7～12），交互參照時看章號就知道在哪一冊。

## Step 3　先寫 calcs.py

講義、圖、範例中的**每一個數字**都必須由 `calcs.py` 算出（圖檔 import 它；內文抄它印出的值）。
選一個**貫穿全冊的範例**（例：同一支角鋼從第 2 章算到第 5 章收尾），讓讀者看到各條公式如何接成一個完整答案。
考題數字取自勘誤後的題解；與既有講義不一致時（例：四捨五入 30.15 → 30.1 而舊講義寫 30.2），**以重算為準並告訴使用者**，不要擅自改別份教材。

## Step 4　試讀版（第 0～2 章）

1. 第 0 章「讀法」：種子表＋種子家族樹圖、五步驟圖、標籤與顏色說明、全書地圖（分冊時列兩冊）。
2. 第 1、2 章依 `references/style-guide.md` 寫。
3. `python3 build.py <冊>` → `python3 render_check.py <html> <outdir>`（見 Step 6）。
4. 交給使用者，**明確問兩件事**：字級（內文／圖內最小字）是否合適；範例與推導的深度是否合適。

## Step 5　寫完其餘各章

每章一組 `chN.html`＋`figs_chN.py`，結構照 `assets/chapter_template.html`：
lead（讀完能寫出什麼）→ 公式標籤表 → 各小節（種子框、圖、derive、check、why、trap）→ 範例 → 30 秒重建卡 → 🙈 蓋住重推（details）→ 陷阱總表。
每冊最後一章是**總整理**：種子樹圖、解題流程圖、一頁公式卡（LRFD／ASD 並列＋從哪裡推＋標籤）、精選 5 題（取自 `risk`／`strategy`）、綜合重建練習。

向量圖規則見 `references/figure-guide.md`；寫作規則見 `references/style-guide.md`。

## Step 6　驗證（交付前全部要過）

```bash
cd study/figs-src/textbook-XX-Un-m
python3 calcs.py                      # 印出所有數值，與內文逐一對照
python3 build.py all                  # 輸出到 study/
python3 render_check.py ../../textbook-XX-Un-m.html /tmp/chk --pdf ../../textbook-XX-Un-m.pdf
```
`render_check.py` 回報：KaTeX 錯誤數（須 0）、逐張圖截圖、SVG 文字超出畫布／互相重疊（須 0）、輸出 A4 PDF（自我測驗答案展開）。
**自動檢查抓不到「文字壓到曲線」**，所以每張 `fig_NN.png` 仍要目視。完整清單見 `references/checklist.md`。

PDF 需要 Python Playwright＋Chromium（Cowork 雲端環境內建）。使用者電腦沒有時：把 `study/assets/katex/`、HTML 與工作資料夾 stage 到雲端渲染，再把 PDF commit 回 `study/`。

## Step 7　交付

- `study/textbook-XX-Un-m[-冊].html`、`.pdf`
- 原始碼留在 `study/figs-src/textbook-XX-Un-m/`（可重跑）
- 不修改 `raw/`；不改寫其他教材（發現其錯誤時告訴使用者，由使用者決定）。
- 回覆：一兩句說明完成內容＋需要使用者知道的差異（例：與舊講義不同的數字、假設性的簡化模型）。

---

## 已確認的偏好（原始使用者）

- 內文 18px；**圖內最小字 14px**（`lib.py` 的 `MINFS=14` 會強制夾住，放大後要重新檢查重疊）。
- 先交計畫、核可後才寫；先交試讀版（0～2 章）再寫完。
- 兩套設計法並列，並寫出換算關係（例：ASD ＝ LRFD ÷ 1.5）。

## 參考檔

| 檔案 | 內容 |
|---|---|
| `references/planning.md` | 計畫書範本、怎麼挑種子、怎麼分冊與分章 |
| `references/style-guide.md` | 六步格式、各種框的用法、標籤、顏色、誠實原則 |
| `references/figure-guide.md` | 向量圖原則、`lib.py`／`plot.py` API、已踩過的排版坑 |
| `references/checklist.md` | 交付前檢查清單 |
| `references/subject-seeds.md` | SS／RC／SA／SD／SM／MM 種子起手建議 |
| `assets/` | 章節、圖檔、calcs、textbook.json 範本 |
| `examples/SS-U1-1/` | 實作範例（拉力篇第 0～2 章原始碼與設定） |
