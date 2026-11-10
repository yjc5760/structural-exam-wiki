---
name: "unit-overview"
description: "exam-wiki 某子項的「單元總覽」unit-XX-Un-m.html（命題分析＋公式給／背＋逐題公式表合一頁）的新建、改版與同步。知識庫有 scripts/build_unit_page.py（目前 SA、SS）時，或要把它導入其他科時，命題分析、給背分界、單元總覽都用此 skill。"
---

# 單元總覽（unit-XX-Un-m.html）

一頁回答三件事：這單元考什麼、哪些公式考卷會給／要自己背、每一題要背哪幾條。
取代舊的 `study-XX-Un-m.html`（命題分析）與 `formula-given-XX-Un-m.html`（給／背分界）；舊兩頁與其 skill 已停用，不做轉址頁。
原理與圖解仍由 `lecture-XX-Un-m.html`（unit-lecture）負責；全科排名看 `frequency-XX.html`（subject-frequency-map）。

## 何時用

- 知識庫根目錄 `scripts/` 有 `build_unit_page.py` 與 `unit_page_template.html`（structural-exam-wiki 五科共用；在根目錄執行 `python scripts/build_unit_page.py XX-Un-m`，或在科目資料夾執行 `python ../scripts/build_unit_page.py XX-Un-m`）。
- 使用者說「做 XX-Un-m 命題分析」「整理 XX-Un-m 主要公式／給背分界」「單元總覽」「這單元考什麼」「哪些公式要背」「索引改分類後同步單元頁」。
- 該科還沒有任何單元總覽時：先問使用者要不要導入（建立 `study/data/unit-XX-Un-m.json` 即可，腳本已在根目錄共用）。舊的 unit-exam-intel／unit-formula-map 已停用，不要再用。

## 資料流（唯一事實來源）

```
study/data/unit-XX-Un-m.json   ← 唯一要維護的檔
raw/json/question_index.json   ← 題數、主副考點、排名、viz、verified 一律由此算
解題過程影片/<題號>/video/*.mp4 ← 有影片就加 🎬
   ↓ python scripts/build_unit_page.py XX-Un-m   （--all 全部；--check 只檢查）
study/unit-XX-Un-m.html        ← 產出，勿手改
```

資料檔欄位：`name` `short` `date` `clusters{代號:{icon,name,desc,color}}` `drift` `driftNote` `type` `risk`（HTML；風險表每列最後一格 `<td data-f="i,j"></td>` 會渲染成公式標籤）`judge` `judgeMore` `strategy`（可用 `<span data-qs="2+3" data-count></span>` 自動列出同時用到 F2、F3 的題號）`three` `footer` `mxCols[]`（逐年表欄名，最後一欄必須是材料／斷面數值）`MXR{年:備註}` `F[]` `Q[]` `base[]` `baseShort` `baseNote` `refAreaYears` `mxNote`。

- `F[i]`：`g` 主題、`lv` must／half／give、`nm`、`sh`（表格用短標籤，≤8 字）、`c` 逐年表欄位、`eq`（LaTeX，`$$…$$`／`\\(…\\)`）、`meta`（證據敘述，寫到題號）、`ok`（該式被考卷印出的年份；give 類不用填，由題目推）。
- `Q[]`：`{id, cl, sum, ty, f:[公式索引]}`。**卡片上「考了卻沒給」的題號、逐年表的 ✗、考題總表的標籤全部由 `Q[].f` 推出**，不要另外手填年份清單。
- `base`：幾乎每題都要用、在總表不另標的公式（如傾角變位方程＋節點平衡、影響線定義、自由度判定）。

## 選用欄位（各科差異）

- `"giveCol": false`：give 類公式不限定放在逐年表最後一欄（SS 的 give 類分散在各欄）；逐年表合計改為全欄加總，`--check` 也不檢查這條。預設 true（SA 行為）。
- `"showDesignMethod": true`：題目列加註索引的 `designMethod`（LRFD／ASD／混合／概念題），有設計法欄位的科目（SS、RC）建議開。
- viz 圖示：索引有 `hasViz` 就用；沒有時自動偵測 `raw/solutions/<id>/*viz*.html`。

## 流程

1. **對帳題目集合**：列出索引中 `primaryTopicId == XX-Un-m` 與 `secondaryTopicIds` 含它的題號。`build_unit_page.py --check` 會擋下資料檔多出或缺少的題。
2. **考點群與命題段落**：依題目內容分 3–4 群（每題只歸一群）；前後段漂移以主考點依題號排序後對切（前半取 ⌊n/2⌋ 題）；題型＝計算／繪圖／推導／說明；近 6 考年取索引最後 6 個考年。所有數字寫完後用腳本由 `Q[].cl`、`Q[].ty` 重算核對，**不可憑印象**。
3. **公式卡**：以考卷原文為證據判 must／half／give，**照下方「公式卡證據流程」做，不可只靠文字抽取**。`ok` 只填考卷真的印出那條式子的年份。
4. **逐題標公式用途（最花時間、也最容易錯的一步）**：
   - 判準：**該題題解實際寫出或套用了這條式子才算**。「也可用」「以它為理論根據」不算；結構上必然的第一步（如桁架先判靜定）可算。
   - 做法：每條公式寫一個關鍵字 regex，對本單元每份 `raw/solutions/<id>/<id>.md` 計數；列出「舊資料宣稱用到但 0 命中」與「沒宣稱但大量命中」兩種差異，逐一開題解原文判斷。
   - 同一年有兩題以上屬本單元時，年份層級的舊證據無法分配到題目——必須逐題看。
   - 發現題解方法與分類不符（例：考卷明文指定傾角變位法卻掛在最小功法），**不要自己改索引**，記在 footer 與 log 的待複核，回報使用者。
   - 更正舊證據時，`meta` 敘述裡的題號也要一起改，並在 `footer` 列出「相對於舊版的證據更正」。
5. **產生與檢查**：`python scripts/build_unit_page.py XX-Un-m`。用 Playwright 開 1280 與 390 寬各看一次：console 無錯、`.katex-error` 為 0、`document.documentElement.scrollWidth` 不超過視窗寬、逐年表合計合理。
6. **PDF**：Playwright 先把 `#mxBox` 設為 open，`emulateMedia('print')`，`page.pdf({format:'A4', printBackground:true, scale:0.85})`，存成 `study/unit-XX-Un-m.pdf`。
7. **下游同步**（新建單元或改檔名時）：`scripts/build_frequency.py` 重跑（教材欄偵測 unit-／lecture-／記憶片）；`study/problems-view/*.html` 的按鈕列指向 `../unit-XX-Un-m.html`；`lecture-XX-Un-m.html` 導覽列。不產生舊的 `study-`／`formula-given-` 檔，也不做轉址頁。
8. **記錄**：該科 `wiki/queries/log.md` 追加（append only）；`XX/SUBJECT.md` §9 CHANGELOG 加一列。使用者自己 commit：寫完檔就停，列出動到的路徑。

## 公式卡證據流程（步驟 3 必讀；原 unit-formula-map 的核心）

### A. 全年份文字抽取

```bash
mkdir -p /tmp/txt && cd raw/exams
for f in XX-*.pdf; do pdftotext -layout "$f" "/tmp/txt/${f%.pdf}.txt"; done
```

**抽全部年份，不是只抽有本單元題目的年份**：參考公式常是整張考卷共用一區，別單元的題目也可能順帶印出本單元的式子。

### B. 定位參考公式（三種擺法都算「有給」）

| 擺法 | 特徵 | 例 |
|------|------|----|
| 集中式 | 最後一題之後，標題多為「※參考公式」「參考資料」 | SS 104、108、110 年 |
| 隨題式 | 緊跟在該題題目正下方 | SS 107、111、113 年 |
| 內文式 | 混在題目敘述裡當已知條件給值 | SS 106 年給 `Cc=128`、96 年給 `U=0.85` |

```bash
grep -n -E "參考公式|參考資料|下列公式|公式如下|附錄|僅供參考" /tmp/txt/*.txt
```

再用本單元特徵符號補搜一輪（SS 壓力桿件 `0.419|0.877|0.658|Cc|Fa`；RC `0.85f'c|β1|ρ|Vc`；SD `ζ|ω_n|Sa`），避免漏掉沒有標題的隨題式公式。

### C. ⚠️ 強制轉圖目視（不可略過）

`pdftotext` 對掃描頁與嵌圖公式無能為力，而且會成功抽出中文題幹、只讓公式那塊消失，看起來像「該年沒給」。符合任一條件的頁面一律轉圖用 Read 親眼看：

- 抽取結果有「參考公式」「參考資料」字樣，後面卻沒有公式符號
- 該年有本單元題目，但整份抽不到任何公式
- 抽出的公式明顯斷裂（如只剩 `= ，= exp−0.419∙`，變數全掉光）
- 題目寫「如下式」「依下式計算」「參考公式：」但下一行是空的

```bash
pdftoppm -r 110 -png "raw/exams/XX-YYYY_科目名.pdf" /tmp/img/YYYY   # 頁數 ≥10 檔名補零（YYYY-01.png），先 ls 再 Read
```

符號、下標看不清楚時提高到 300 dpi 以上。實績：SS 102、105、112、113 四年公式全為影像；113 年的 LTB 公式組與最小銲腳表、109 年第 3 頁參考資料皆為嵌圖——只靠文字抽取會整年誤判成零公式年。

### D. 記下考卷免責聲明

多數年份寫「請自行選擇適合的公式，並檢查其正確性」，近年寫「計算公式僅供參考應自負確認與勘誤責任」。原文引用進頁面（`baseNote` 或 `footer`）：**給了公式 ≠ 免背**，考生仍須認得哪條該用、哪條被印錯。

### E. 公式清單來源（去重合併）

- `raw/solutions/methods/*/`：適用本單元的方法論
- `study/lecture-XX-Un-m.html`、`study/textbook-XX-Un-m*.html`（若已存在）：各章主公式
- `raw/solutions/<id>/<id>.md` 的 §3.5 VHA「主要公式」與 L2／L3（最貼近實戰）
- 不要讀 `archive/wiki/`（已封存、未經核對）

清單要涵蓋四類，後三類最常漏、也最不會被印出：① 主體計算式；② 判斷式與分界（`λc ≤ 1.5` 用哪條、拉力筋是否降伏）；③ 係數與折減值（`φc = 0.85`、孔徑 `db + 3 mm`）；④ 流程骨架（「三種極限狀態取小」「兩軸都算取大」）。

### F. 判定規則（保守：拿不準就往上歸）

| `lv` | 條件 |
|------|------|
| **must**（必背） | 從未印出；或有「考了卻沒給」且佔比高 |
| **half**（別賭） | 多數年份有給，但有明確沒給的先例；或給的是舊版／簡化版需自行判斷 |
| **give**（通常會給） | 考該題型幾乎必印，且無「考了卻沒給」先例 |

把 must 誤判成 give 的代價遠大於反過來多背幾條。

四種情況要在 `meta` 點明：
1. **新舊兩種寫法混用**（`exp(-0.419λc²)Fy` 與 `0.658^(λc²)Fy`）：兩種各列一張卡，說明是同一條。
2. **誘餌**：印了公式但那條不能直接用（SS 113 年印「無殘餘應力」理想曲線，題目要含殘餘應力的）。
3. **用了卻不定義**（96、100 年印含 `Cc` 的 `Fa` 式，沒給 `Cc` 定義）：至少降到 half。
4. **少給關鍵一步**（104 年給填角銲強度式，沒給 `t = 0.707w`，題目要算的正是 `w`）。

`meta` 要具體到年份與題號，不寫「常常會給」這種空話。

## 環境備註（exam-wiki-SA）

- 知識庫在使用者 Windows 本機，透過 device_bash 操作；本機 python3 可跑 build 腳本，但沒有 Playwright——截圖與 PDF 在雲端容器做：stage HTML 回容器、`npm pack katex` 放到 `assets/katex/` 同層、產 PDF 後 commit 回 `study/`。
- 頁面不要發布成 claude.ai artifact（教材連結是本機相對路徑）。

## 陷阱

- 公式字串裡的 `<`、`>`（如 `6<t\le 12`）會被瀏覽器當成 HTML 標籤吃掉、KaTeX 不渲染：資料檔內一律寫 `\lt`、`\gt`。
- 從舊頁搬文字時，`href="study-…"`、`href="formula-given-…"` 要改成 `unit-…`；舊頁的逐年合計句（寫死的 ✔／✗ 格數）不要搬，`mxsum` 由頁面自己算。

- 舊給／背頁的年份證據常有錯：誤把「也可用」算成用到、把載重位置看錯（2017-3 右柱載重恰在柱中點，用 PL/8 不是 Pab²/L²）、引用到勘誤前的舊數值。逐題核對時以題解最新版為準。
- 有給過的 half 類公式：當年題目的標籤會顯示為綠框虛線，卡片另列「考了、當年有印」，不算進 ✗。
- 某條公式在本單元沒有任何題用到時仍可保留卡片，但 `meta` 要明講「本單元題解沒有直接套用」。