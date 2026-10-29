---
name: "unit-lecture"
description: "為六科考試知識庫（exam-wiki-SS/RC/SA/SD/SM/MM）的某個命題大綱單元產生「理解導向」觀念講義，輸出 HTML + 可列印 PDF。當使用者說「生成 XX-Un-m 講義」、「幫我做這單元的觀念講義」、「我要在練這單元考題前先懂原理」、「不要死記公式的講義」、「unit-lecture」，或指名某科某單元要講義／教材／原理說明時，必須使用此 skill。內容以物理直覺與圖解為主軸，每條規範公式都追溯來源，並在最後精選最具代表性的 N 題供時間有限者練習。"
---

# unit-lecture — 單元觀念講義產生器

為結構技師考試知識庫的**單一命題大綱單元**產生理解導向講義。

**這不是速查表。** 知識庫裡通常已有 `study/study-XX-Un-m.html`（**命題分析**：這個單元考什麼）
與 `study/formula-given-XX-Un-m.html`（給／背分界：這條公式要不要背）；
本 skill 產出的是**練題之前**用來建立物理直覺的講義，三者並存、不互相覆蓋。

**檔名規則：** `study/lecture-XX-Un-m.html` + `study/lecture-XX-Un-m.pdf`（不要用 `study-` 前綴）

**兩種模式：**

| 模式 | 觸發 | 走哪些步驟 |
|------|------|-----------|
| **新建** | 該單元還沒有 `lecture-XX-Un-m.html` | Step 0 → 9 全部 |
| **改版** | 講義已存在，使用者說「優化」「圖再精準」「更新講義」「同步勘誤」 | Step 10（以 Step 1、4、5、8、9 為子步驟） |

---

## 適用科目

| 代號 | 科目 | 資料夾 |
|------|------|--------|
| SS | 鋼結構設計 | `exam-wiki-SS` |
| RC | 鋼筋混凝土設計與預力混凝土設計 | `exam-wiki-RC` |
| SA | 結構學 | `exam-wiki-SA` |
| SD | 結構動力分析與耐震設計 | `exam-wiki-SD` |
| SM | 土壤力學與基礎設計 | `exam-wiki-SM` |
| MM | 材料力學 | `exam-wiki-MM` |

> 科目全名一律以 `raw/json/syllabus_taxonomy.json` 為準，**不要憑記憶填**。
> 這張表曾把 SM 誤寫成「材料力學」、MM 誤寫成「工程數學／力學」——
> 實際上 SM 是土壤力學與基礎設計、MM 才是材料力學，兩者互換會導向錯誤的資料夾。

六科資料夾結構相同。單元代號格式 `XX-Un-m`（U＝單元號、m＝子項號），
可在該科 `CLAUDE.md` 的「命題大綱分類」表或 `syllabus_taxonomy.json` 查到。

---

## Step 0：定位

1. 從工作資料夾判斷科目（資料夾名 `exam-wiki-XX`）。使用者若指定其他科目而該資料夾未掛載，直接說明並請對方開啟該資料夾。
2. 讀 `CLAUDE.md` 確認單元代號與名稱。
3. 確認 `wiki/topics/XX-Un-m.md` 存在（該單元的題目清單）。

**立刻用 TaskCreate 建立任務清單**（採集 → 撰寫 → 數值重算＋程式繪圖 → HTML → 題號連結渲染 → PDF → 精選題 → 驗證 → log）。

若 `study/lecture-XX-Un-m.html` 已存在，改走 **Step 10（改版模式）**。

---

## Step 1：資料採集

把下列腳本寫到沙盒暫存區執行（`REPO` 換成該科在 bash 中的實際掛載路徑）：

```python
# gather.py — 用法: python3 gather.py <REPO> <XX-Un-m>
import json, sys, re, os
from collections import Counter
repo, topic = sys.argv[1], sys.argv[2]
qs = json.load(open(f'{repo}/raw/json/question_index.json'))['questions']
sel = [q for q in qs if q.get('primaryTopicId') == topic or topic in (q.get('secondaryTopicIds') or [])]
pri = [q for q in sel if q.get('primaryTopicId') == topic]
print(f'# {topic}｜主分類 {len(pri)} 題、副分類 {len(sel)-len(pri)} 題\n')
mass = Counter()
for q in sorted(sel, key=lambda x: x['moduleId']):
    tag = 'P' if q in pri else 'S'
    print(tag, q['moduleId'], q.get('year'), q.get('designMethod'), '|', '/'.join(q.get('tags', [])))
    mass.update(q.get('tags', []))
print('\n# 標籤頻次（決定章節配重與複習優先順序）')
print(mass.most_common(50))
print('\n# 知識庫可用素材')
for d in ['concepts', 'methods', 'code-ref', 'diagnosis', 'failure-modes', 'materials', 'traps']:
    p = f'{repo}/wiki/{d}'
    if os.path.isdir(p):
        print(f'-- {d}:', ', '.join(sorted(os.listdir(p))[:80]))
```

接著**讀取**與本單元標籤對應的 `wiki/concepts/`、`wiki/code-ref/`、`wiki/methods/`、
`wiki/diagnosis/`、`wiki/traps/` 頁面（一次用 `for f in ...; do cat $f; done` 批次讀，省來回）。
`code-ref/` 特別重要 —— 它記錄規範常數的推導來源，是「不死記公式」的主要彈藥。

**再查勘誤紀錄（必做）**：題解正本會被勘誤，講義若沿用舊解就會把已修正的錯誤繼續教下去
（2026-10 改版時 SS-U1-1、SS-U1-3、SA-U1-3、SD-U2-2 都查出講義落後於題解勘誤，
例如講義仍以 SS-2025-2 已被勘誤的錯解當範例、仍寫 SA-2022-3 已刪除的「b 點內鉸」）：

```bash
cd <REPO>
# 本單元題號清單（gather.py 的輸出）存成 /tmp/ids.txt 後：
grep -n -F -f /tmp/ids.txt wiki/log.md | grep -i -E '勘誤|FIX|修正|更正' | tail -40
for id in $(cat /tmp/ids.txt); do grep -l -E '修正日期|勘誤|依最新規範' raw/solutions/$id/$id.md 2>/dev/null; done
```

被勘誤過的題目，一律以 `raw/solutions/` 現行正本的數值與結論為準，並讀該題「依最新規範對照」一節。
講義引用任何題目的數字、幾何、答案時，**回正本抄，不要憑印象**。

> **原則：先採集完再寫作。** 不要邊查邊寫，會寫成拼貼。

---

## Step 2：與使用者確認（AskUserQuestion）

三個問題，附推薦選項：

1. **輸出格式** — HTML + PDF 兩份（推薦）／只要 HTML／只要 PDF
2. **深度** — 觀念圖解為主（推薦）／完整數學推導／觀念＋手算範例
3. **是否附歷屆考點對應表** — 要（推薦）／只要純觀念

若使用者已在對話中講明，就不要再問。

---

## Step 3：講義骨架

**頭尾固定，中段依標籤分群動態決定。**

| 節次 | 內容 | 必要性 |
|------|------|--------|
| §0 | **全景**：用一句話說出本單元的核心對立，並畫成對照圖 | 必要 |
| §1…§k | **主題章節**：依標籤分群，每群一節；由淺入深、前後相依 | 必要 |
| §k+1 | **解題決策流程**：真正有判斷菱形的流程圖，不是條列 | 必要 |
| §k+2 | **歷屆題 × 觀念對照表**：主分類、副分類分開列 | 依 Step 2 |
| §k+3 | **陷阱總表**：15–20 條，可在考前十分鐘掃完 | 必要 |
| §k+4 | **自我檢測**：10–12 個「為什麼」，答案用 `<details>` 摺疊 | 必要 |
| §k+5 | **★ 精選 N 題**（見 Step 6） | 必要 |

**§0 那句話怎麼找**：問自己「這單元所有公式的差異，最終都源自哪一個物理對立？」
例：SS-U1-1 是「拉力是材料強度問題，壓力是幾何穩定問題」。
找不到這句話，代表你還沒讀懂這個單元 —— 回 Step 1。

**中段分群**：把標籤頻次表分成 4–8 個考點群，每群一節。
群的順序要讓後面的節能引用前面的結論（例：先講 Euler，才能講有效長度 K）。

---

## Step 4：寫作原則（品質的來源，逐條照做）

1. **每節從「這條公式在怕什麼」開始，不從公式開始。** 公式是結論，不是起點。

2. **每個規範常數都要交代出處。** 沒有「規範就是這樣規定」這種句子。
   典型：`0.6` ← von Mises 的 `1/√3`；`0.877` ← 初始彎曲 L/1000 的折減；
   `φ` 值差異 ← 破壞模式的延性與離散度。
   查不到出處就翻 `wiki/code-ref/`；還是查不到，就誠實寫「規範以試驗迴歸得到，物理意義為…」。

3. **用極限檢查取代背表。** 教讀者拿 `x→0`、`x→∞`、對稱情況去驗證公式方向。
   例：`U = 1 − x̄/L`，`x̄=0 → U=1`、`L→∞ → U→1`。忘記表格值時能自救。

4. **「兩個東西並排」是最有效的解釋裝置。** 拉 vs 壓、柱挫屈 vs 板挫屈、
   LRFD vs ASD、理論 K vs 設計 K、延性破壞 vs 脆性破壞。並排就自己解釋了自己。

5. **安全係數／折減係數一律用「破壞有沒有預警」解釋。**
   延性破壞變形大、看得見 → 係數寬鬆；脆性破壞無預警 → 係數嚴格。
   這條邏輯貫穿所有結構規範，講一次可以通吃。

6. **陷阱寫成三段式**（沿用 `wiki/traps/` 的格式）：觸發信號 → 錯誤思維 → 正確認知，
   並標註出自哪一題。

7. **每個大主題結尾要能濃縮成一條 5–7 步的箭頭因果鏈**，讓讀者用嘴巴講得出來。
   講義最後把所有因果鏈集中重列一次。

8. **圖優先於文字，文字優先於推導。** 使用者選「觀念圖解為主」時，
   數學只留關鍵幾步 + 結論，把省下的篇幅給圖與直覺。

9. **範例的答案要能自我檢查。** 例如同一題用 LRFD 與 ASD 各算一次，
   比值應落在 1.4–1.6；比值離譜代表算錯。教讀者建立這種檢查習慣。

10. **誠實標註未涵蓋範圍。** 精選題沒涵蓋到的考點群要明白列出，
    不要讓讀者誤以為練完就滿分。

11. **口吻**：對著一個有基礎、時間不夠的考生說話。不客套、不重複、不寫「總而言之」。

12. **規範要寫版本。** 引用係數、條文時寫明出自哪一版（台灣現行規範／AISC 360-05／-16／-22／ACI 318-19…）。
    題目寫「我國規範」就以台灣規範為主答，國外規範放「版本提醒」框。
    2026-08〜10 的勘誤一再遇到版本混用：摩阻型 φ＝1.0／0.85＋h_sc 是 AISC 360-05 的寫法、
    強柱弱梁台灣 (13.6-3) 梁側乘 1.25 而 AISC 341 是 1.1R_y＋M_uv、ASD 的 C_m 沒有 0.4 下限。

13. **查不到出處的規定就刪。** 寫進講義的每一條規定都要能指到規範條文或 `wiki/code-ref/`。
    SS-U1-3 曾寫了一條不存在的「ΣP_u/ΣP_e2 ≤ 0.6（B₂ ≤ 2.5）」，散布在 7 處。

14. **關於考古題的敘述一律由 `question_index.json` 算出。** 「近 6 年出過 4 次」「從沒有連續兩年出過」
    「本單元 25 題」這類句子要用腳本數，不要憑印象（SA-U1-3、SM-U1-3 都查出與題庫不符）。

---

## Step 5：SVG 圖解——一律由程式依數值繪製

全部用**內嵌 SVG**（不要外部圖檔，PDF 才能一起帶走），而且**不可手寫座標**。

> **為什麼這條是硬規則**：2026-10 五科（SS／SD／SM／SA／RC）講義全面改版時，逐張檢查舊的手繪圖，
> 查出的不只是美觀問題，而是**會教錯觀念的錯**：標記點不在曲線上（SS-U1-4 U 曲線）、
> 節點域兩側翼板力方向畫反而互相抵消（SS-U1-4）、RBS 畫在立面（應在平面）、
> 塊狀剪力的剪力面沒穿過孔（SS-U1-1、U1-4）、穩定平衡的球懸在谷底曲線下方（SS-U1-1）、
> 影響線正負畫反（SA-U1-3）、2-DOF 振態 −0.414 畫成 −1（SD-U1-1）、
> 零空氣孔隙曲線與夯實曲線交叉兩次（SM-U1-1）、理論曲線畫在規範直線下方（SS-U1-2）。
> 這些錯的共同成因只有一個：**座標是目測填的**。由公式算出座標，這類錯就不會發生；
> 若圖畫錯，代表數字錯，回頭查數字即可。

### 5.1 四種圖型（不變）

| 模式 | 用途 | 要點 |
|------|------|------|
| **左右對照圖** | §0 的核心對立、兩種設計法、兩種破壞模式 | 中線分隔，兩側結構完全鏡像，底部各寫一行結論 |
| **狀態序列圖** | 漸進的物理過程（逐步降伏、三種平衡、載重歷程） | 3 格並排，每格下方一行說明，用顏色標示嚴重度遞增 |
| **函數曲線圖** | 規範曲線 vs 理想曲線、分段公式的交界 | 座標軸與刻度，理想曲線用虛線、規範曲線用粗實線，**標出交界點座標** |
| **決策流程圖** | 解題流程 | 菱形判斷節點、每條分支都有「是／否」標籤、**沒有死路**、最後匯流到同一個收尾框 |

### 5.2 程式繪圖的做法

1. **繪圖函式庫**：優先沿用 `struct-diagram` skill 的 `scripts/structdraw.py`
   （數學座標 y 向上、`_{下標}` `^{上標}` 數學字串、六科統一色票；SD-U1-2 已這樣用）。
   該科已有講義用的 `svglib.py`／`lib.py` 時沿用同一份，**不要每份講義各寫一套**。
2. **數值先行**：把本講義所有手算範例寫成 `calcs.py`（或圖腳本內的函式）重算一次，
   **圖上的每個數字、每個座標都從這裡取**，並以 `assert` 對帳講義內文的數字。
   需要彎矩圖、變形曲線、振態時，用小型求解器實算（純 Python 平面剛架勁度法、
   特徵值、級數解），不要畫「看起來像」的曲線。
3. **曲線一律取點**：由公式取 100–200 點畫折線，不用貝茲曲線。
   標記點（交界點、範例答案點）用**同一個函式**算座標，才保證落在曲線上。
4. **物理方向先寫出來再畫**：力、反力、剪力流、轉向、影響線正負、振態符號——
   先在腳本裡寫出平衡式或符號約定，箭頭方向由正負號決定。
   成對的力（翼板力偶、節點域、摩擦）特別要確認是「同向疊加」還是「相對抵消」。
5. **視圖要選對**：平面／立面／斷面各自看得到什麼不同；特徵只在某個視圖看得到時
   （RBS 削翼板寬度、ESW 在內橫隔板與柱壁交會處），就畫在那個視圖並在圖上註明。
6. **用範例的實際尺寸**：有手算範例的單元，圖就畫那個範例（如 L125×125×12、
   H400×200），圖上寫比例尺（「1 cm = 8 px」）；向量圖多個向量用同一比例尺。
7. **可重跑**：HTML 內每張圖以 `<!--FIG:id-->`（或 `data-fig="id"`）標記，
   腳本只替換標記後的 `<svg>…</svg>`，找不到或重複時直接報錯。
   重跑兩次結果應逐位元相同。
8. **腳本存放**：`<REPO>/scripts/lecture-figs/XX-Un-m/`（`gen_figs.py`＋必要的 `calcs.py`），
   與講義一起版控。各科既有位置（`study/figs-src/`、`scripts/gen_lecture_*`）沿用即可，不必搬。
9. **每張圖說寫出「這張圖攔的錯」**：除了說明圖在講什麼，點出讀者最容易畫錯／想錯的那一點。

### 5.3 SVG 硬規則（踩過的坑）

- **SVG `<text>` 裡不可以放 `\(...\)` 數學式**——KaTeX auto-render 不處理 SVG 文字節點。
  SVG 內用純文字＋`<tspan>` 下標（`F<tspan dy="4" font-size="70%">y</tspan>`，之後要把 dy 歸零）。
- **marker、gradient、clipPath 的 id 加上圖號前綴**（`f61-arrow`），整頁 id 不可重複；
  不同圖共用同名 id 時，後面的圖會套到前面圖的箭頭顏色。
- **缺字**：`⅔` 等分數字元、`✔ ✘ ✗` 在常用中文字型與襯線字型都缺字；`x̄`、`ȳ` 用組合字元
  （U+0304）時要用**直立**襯線字型，不要用斜體（橫線會偏位），也不要用 `text-decoration:overline`（橫線離字太遠）。
- 中文字寬約等於 font-size：**估算文字寬度 = 字數 × font-size**，據此配置位置；
  方框內文字寧可分兩行，不要靠加寬方框解決。
- 靠左／靠右對齊的長標籤會超出畫布，而 viewBox 不會報錯——一律用 5.4 的腳本檢查。
- 每張圖下方一定要有 `<div class="cap">`，不是只寫圖號。

### 5.4 圖的驗證（每張圖都做，不可只看 PDF）

在**瀏覽器**裡逐張檢查（雲端容器有預裝 Chromium／Playwright）：

```python
# figcheck.py — 用法: python3 figcheck.py <lecture.html> <shots_dir>
import sys, asyncio, json
from playwright.async_api import async_playwright
JS = """() => [...document.querySelectorAll('.fig>svg')].map((svg,i)=>{
  const vb=svg.viewBox.baseVal, bb=[...svg.querySelectorAll('text')].map(t=>{const b=t.getBBox();return [b.x,b.y,b.width,b.height,t.textContent]});
  const out=bb.filter(b=>b[0]<vb.x-1||b[1]<vb.y-1||b[0]+b[2]>vb.x+vb.width+1||b[1]+b[3]>vb.y+vb.height+1).map(b=>b[4]);
  const ov=[];for(let a=0;a<bb.length;a++)for(let c=a+1;c<bb.length;c++){const A=bb[a],B=bb[c];
    const w=Math.min(A[0]+A[2],B[0]+B[2])-Math.max(A[0],B[0]),h=Math.min(A[1]+A[3],B[1]+B[3])-Math.max(A[1],B[1]);
    if(w>2&&h>2)ov.push(A[4]+' × '+B[4]);}
  return {i,out,ov};})"""
async def main(src, d):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1000,'height':900}, device_scale_factor=1.3)
        await pg.goto('file://' + src); await pg.wait_for_timeout(1500)
        print('katex 式數', await pg.evaluate("document.querySelectorAll('.katex').length"),
              '｜錯誤', await pg.evaluate("document.querySelectorAll('.katex-error').length"))
        for r in await pg.evaluate(JS):
            if r['out'] or r['ov']: print('圖', r['i'], '出界:', r['out'], '重疊:', r['ov'])
        for i, e in enumerate(await pg.query_selector_all('.fig')): await e.screenshot(path=f'{d}/fig{i:02d}.png')
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
```

1. 出界、重疊清單應為空（線條壓字等腳本抓不到的，靠截圖目視）。
2. **用 Read 逐張看截圖**，看的不是美觀而是物理：方向、正負、交點位置、視圖、比例。
3. KaTeX 錯誤數必須是 0。

---

## Step 6：精選 N 題

**預設 5 題**；使用者說幾題就給幾題。

先跑覆蓋率計算取得候選，**再用判斷定案**（腳本只提供資訊，不做決定）：

```python
# pick.py — 用法: python3 pick.py <REPO> <XX-Un-m> <N>
import json, sys
from collections import Counter
repo, topic, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
qs = json.load(open(f'{repo}/raw/json/question_index.json'))['questions']
sel = [q for q in qs if q.get('primaryTopicId') == topic or topic in (q.get('secondaryTopicIds') or [])]
mass = Counter()
for q in sel: mass.update(q['tags'])
total = sum(mass.values())
chosen, cov = [], set()
for _ in range(N):                       # 貪婪最大覆蓋
    best = max((q for q in sel if q not in chosen),
               key=lambda q: sum(mass[t] for t in set(q['tags']) - cov))
    gain = sum(mass[t] for t in set(best['tags']) - cov)
    chosen.append(best); cov |= set(best['tags'])
    print(f"{best['moduleId']} ({best['year']}) 新增權重 {gain}"
          f" 累計 {sum(mass[t] for t in cov)/total:.0%} | {'/'.join(best['tags'])}")
print('\n未涵蓋且出現 >=2 次的標籤：',
      [(k, v) for k, v in mass.most_common() if k not in cov and v >= 2])
```

**定案準則（覆蓋率只是起點）：**

- 一題能練到最多**獨立技能**者優先（例：同一題要求 LRFD 與 ASD 各算一次）。
- 彼此**重疊最少**；貪婪結果若有兩題高度重疊，換掉後者。
- **觀念鏈題**（計算量小但牽動多題的因果鏈）投報率最高，一定要留一席。
- **需要自己建立前置資料**的題型（自算斷面性質、自建模型）留一席，這是別題練不到的。
- 同分時選**近年題**。
- 標籤語彙有同義詞（如「對位圖 / nomograph」）與符號標籤（如 `λc`、`Fcr`），
  raw 覆蓋率會低估。**改以「考點群」報告涵蓋度**，並誠實列出未涵蓋的群。

**每題要寫出：** 題號（連到渲染頁面，見 Step 7「題號連結」）、考年、**為什麼選它**、讀本講義哪幾節、
**做完要能回答的問題**。最後附「練這幾題的正確方法」與 1–2 題候補。

---

## Step 7：產出 HTML

存到 `<REPO>/study/lecture-XX-Un-m.html`。

### 數學式離線化（必做）

沙盒無法連 CDN，且使用者可能離線閱讀。把 KaTeX 放進該科 repo：

```bash
mkdir -p /tmp/v && cd /tmp/v && npm install katex --no-audit --no-fund
D=<REPO>/study/assets/katex && mkdir -p $D/fonts
cp /tmp/v/node_modules/katex/dist/katex.min.css /tmp/v/node_modules/katex/dist/katex.min.js $D/
cp /tmp/v/node_modules/katex/dist/contrib/auto-render.min.js $D/
cp /tmp/v/node_modules/katex/dist/fonts/*.woff2 $D/fonts/     # 只複製 woff2，約 600KB
```

`<head>` 用相對路徑引用（同一個 `assets/` 可被該科所有講義共用）：

```html
<link rel="stylesheet" href="assets/katex/katex.min.css">
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:false});"></script>
```

行內數學一律用 `\( ... \)`，展示式用 `$$ ... $$`（**不要**用單 `$`，會誤判貨幣符號）。

**KaTeX 寫法地雷（都會變成紅字錯誤或吃掉內容）：**

| 寫法 | 結果 | 改成 |
|------|------|------|
| `\text{tf·m}` | `·` 在 text mode 轉成 `\cdotp` → 紅字錯誤 | `\text{tf}\cdot\text{m}` |
| `96%`（在數學式內） | `%` 是 TeX 註解，後面整段消失 | `96\%` |
| `\((<C_c\)` 這類 `<` 緊接字母 | 被 HTML 當成標籤，吃掉整段 | `&lt;` 或 `\lt`，並在 `<` 後加空格 |

驗收時以瀏覽器數 `.katex-error`，必須為 0（Step 5.4 的腳本會印出）。

### 版面 CSS（house style，沿用以維持六科一致）

```css
:root{--ac:#1565c0;--ac2:#e3f2fd;--tension:#2e7d32;--tension2:#e8f5e9;
--comp:#c62828;--comp2:#ffebee;--warn:#ef6c00;--warn2:#fff3e0;
--key:#6a1b9a;--key2:#f3e5f5;--bg:#f7f9fb;--card:#fff;--ink:#263238;--mut:#607d8b;--bd:#dfe6ea}
*{box-sizing:border-box}
body{margin:0;font-family:"Microsoft JhengHei","Noto Sans TC",-apple-system,sans-serif;
background:var(--bg);color:var(--ink);line-height:1.75;font-size:15.5px}
header{background:linear-gradient(135deg,#0d47a1,#1976d2 60%,#42a5f5);color:#fff;padding:34px 26px}
header h1{margin:0 0 8px;font-size:1.6em}header .sub{opacity:.9;font-size:.93em;margin:0}
header .meta{margin-top:12px;font-size:.82em;opacity:.8}
nav{position:sticky;top:0;z-index:20;background:#fff;border-bottom:2px solid var(--bd);
padding:9px 14px;display:flex;flex-wrap:wrap;gap:6px;box-shadow:0 2px 6px rgba(0,0,0,.05)}
nav a{text-decoration:none;color:var(--ac);font-size:.85em;padding:4px 11px;border-radius:14px;background:var(--ac2)}
nav a:hover{background:var(--ac);color:#fff}
main{max-width:980px;margin:0 auto;padding:24px 18px 80px}
section{margin-bottom:46px}
h2{font-size:1.32em;border-left:6px solid var(--ac);padding-left:12px;margin:44px 0 18px;line-height:1.4}
h3{font-size:1.08em;margin:30px 0 10px;color:#0d47a1}
h4{font-size:.99em;margin:20px 0 8px;color:#37474f}
.lead{font-size:1.03em;background:#fff;border:1px solid var(--bd);border-left:5px solid var(--ac);
border-radius:0 10px 10px 0;padding:14px 18px;margin:16px 0}
.box{background:var(--card);border:1px solid var(--bd);border-radius:11px;padding:16px 18px;margin:16px 0}
.why{background:var(--key2);border:1px solid #ce93d8;border-left:5px solid var(--key);
border-radius:0 10px 10px 0;padding:13px 17px;margin:16px 0}
.why b:first-child{color:var(--key)}
.trap{background:var(--warn2);border:1px solid #ffcc80;border-left:5px solid var(--warn);
border-radius:0 10px 10px 0;padding:13px 17px;margin:16px 0}
.trap b:first-child{color:#e65100}
.tens{background:var(--tension2);border:1px solid #a5d6a7;border-left:5px solid var(--tension);
border-radius:0 10px 10px 0;padding:13px 17px;margin:16px 0}
.comp{background:var(--comp2);border:1px solid #ef9a9a;border-left:5px solid var(--comp);
border-radius:0 10px 10px 0;padding:13px 17px;margin:16px 0}
.fig{background:#fff;border:1px solid var(--bd);border-radius:11px;padding:16px 14px 10px;margin:20px 0;overflow-x:auto}
.fig>svg{display:block;margin:0 auto;max-width:100%;height:auto}
.fig .cap{font-size:.85em;color:var(--mut);text-align:center;margin-top:10px;line-height:1.6}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.9em;background:#fff}
th,td{border:1px solid var(--bd);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eceff1;font-weight:600}
tbody tr:nth-child(even){background:#fafcfd}
ul,ol{margin:10px 0 10px 4px;padding-left:22px}li{margin:5px 0}
.pill{display:inline-block;font-size:.76em;padding:2px 8px;border-radius:10px;margin-right:4px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:760px){.grid2{grid-template-columns:1fr}}
details{background:#fff;border:1px solid var(--bd);border-radius:9px;padding:10px 14px;margin:12px 0}
summary{cursor:pointer;font-weight:600;color:var(--ac)}
details p{border-left:3px solid #e0e0e0;padding-left:12px;margin:8px 0;color:#37474f}
.qlink{color:#1565c0;text-decoration:none;border-bottom:1px dotted #90caf9;font-weight:600}
.katex-display{margin:14px 0!important;overflow-x:auto;overflow-y:hidden}
footer{text-align:center;color:var(--mut);font-size:.83em;padding:26px;border-top:1px solid var(--bd)}
```

> ⚠️ 一定是 `.fig>svg`（子選擇器），**不可寫成 `.fig svg`**：後者會把圖說裡 KaTeX 根號的 SVG
> 也變成 `display:block`，根號整個消失（SS-U1-2、U1-3 與 SD 三份講義都中過）。
> 若另外寫了 `svg text{font-family:…}`，要改成 `svg text:not([font-family])`，
> 否則會蓋掉 SVG 內指定的數學字型。

用途約定：`.why` 紫＝為什麼／物理直覺；`.trap` 橘＝陷阱；`.lead` 藍＝該節主張；
`.box` 白＝手算範例；`.tens`/`.comp` 綠/紅＝成對概念的兩側。

### 分段寫檔

講義通常 1000+ 行。先 Write 出骨架（head + nav + `<!--APPEND-->` 佔位 + footer），
再用 Edit 反覆把 `<!--APPEND-->` 換成「新內容 + `<!--APPEND-->`」逐節長出來。
一次寫完容易中斷且難修。

### 與同子項既有教材互連（必做，最容易漏）

同一個子項往往已經有其他教材躺在 `study/`：

同一個子項最多有三份教材躺在 `study/`，三者並存、互不覆蓋：

| 檔案 | 回答什麼 | 使用時機 | 產出者 |
|------|---------|---------|--------|
| `lecture-XX-Un-m.html` / `.pdf` | **為什麼**成立（物理原理） | 第一次接觸該單元、練題前 | 本 skill |
| `formula-given-XX-Un-m.html` / `.pdf` | 這條公式**要不要背** | 排讀書計畫、決定背誦優先序 | `unit-formula-map` |
| `study-XX-Un-m.html` | 這個單元**考什麼**（命題事實） | 決定練題順序、考前押題 | `unit-exam-intel` |

> ⚠️ `study-XX-Un-m.html` 的正式名稱是**「命題分析」**，不是「速查頁」。
> 「速查頁」是 2026-08 以前那版七區段深度複習頁的舊名，該版已被 `unit-exam-intel`
> 重構為只回答「考什麼」的命題情報頁，**全站不再使用「速查頁」這個詞**。
>
> ⚠️ **不要放 Keynote 或課堂投影片按鈕**（`XX-Un-m_<單元名>.pdf` 那類使用者自備的
> 課堂 PDF）。使用者已明確要求移除 —— 它與上面三份教材的分工重疊，且檔名由使用者
> 自訂、容易連到不存在的檔案。

**這幾份教材如果彼此不連，使用者會忘記其他幾份存在。** 產出講義後一定要做雙向連結：

1. **講義 → 其他教材**：在 `<nav>` 尾端加一組連結，固定三顆。
   放在 `<nav>` 裡是刻意的 —— `build_pdf.py` 會把 `<nav>` 整段移除，
   列印版不會出現連不到的本機連結。

```html
<span style="flex:1"></span>
<a href="study-XX-Un-m.html" title="命題分析：出題頻率、考點結構、考題清單、命題風險"
   style="background:#e3f2fd;color:#1565c0">📊 命題分析</a>
<a href="formula-given-XX-Un-m.html" title="哪些公式考卷會給、哪些必須自己背"
   style="background:#ffebee;color:#c62828">🎯 給／背分界</a>
<a href="lecture-XX-Un-m.pdf" target="_blank" title="本講義的列印版"
   style="background:#eceff1;color:#455a64">🖨️ 本頁 PDF</a>
```

2. **命題分析頁 → 講義**：`study-XX-Un-m.html` 的按鈕列應有四顆
   （觀念講義 📘 → HTML、講義 PDF 🖨️、給／背分界 🎯、分界 PDF 🖨️），
   規格見 `unit-exam-intel` 的 SKILL.md Step 4-2。
   按鈕列上方那塊 `.role` 黃底說明裡的使用順序，一律寫成：
   **觀念講義（練題前）→ 給／背分界（決定背誦優先序）→ 命題分析（考前排練題順序）**。

3. 先 `ls study/` 確認哪些檔案真的存在，**不要連到不存在的檔案**；
   缺哪一份就不放哪一顆按鈕（例如該單元還沒做 `formula-given-` 就只放兩顆）。

### 題號連結：連到渲染頁面，不要連到 .md（必做）

**不要**把題號連到 `../wiki/problems/XX-YYYY-N.md` 或直接連到 `raw/solutions/.../*.md`。
使用者點開 `.md` 只會看到瀏覽器顯示的純文字（或觸發下載），公式、表格、圖片全部沒有渲染，體驗很差。

**也不要**以 `wiki/problems/` 作為內容來源 —— 它是 `ingest` 壓縮過的精簡版（通常只有原始解析的 1/2～1/3 長度），
而且**不含圖片**（圖片檔實際只放在 `raw/solutions/XX-YYYY-N/` 底下）。
`raw/solutions/XX-YYYY-N/XX-YYYY-N.md` 才是 CLAUDE.md 定義的「解題內容唯一來源」，內容最完整、圖片同資料夾可直接取用。

**正確做法：** 為每個被講義引用的題號，從 `raw/solutions/` 產生一份獨立的渲染 HTML
（`study/problems-view/XX-YYYY-N.html`），再把講義裡的題號連到那份渲染頁（新分頁開啟）。
這份 HTML 不是知識庫正本，只是顯示層，可重複產生、不影響 `raw/` 或 `wiki/`。

**Step A — 先確認 markdown 套件、蒐集本講義引用到的所有題號：**

```bash
pip install markdown --break-system-packages -q
```

```bash
cd <REPO> && grep -oP 'XX-[0-9]{4}-[0-9]+(?=\.md)' study/lecture-XX-Un-m.html | sort -u > /tmp/ids.txt
cat /tmp/ids.txt   # 檢查有沒有漏題、有沒有多餘題號
```

**Step B — `render_problems.py`（渲染 raw/solutions → study/problems-view/，六科通用，只需改 `REPO`）：**

```python
# 用法: python3 render_problems.py <REPO> <ids_file>
import re, os, sys
import markdown

REPO, IDS_FILE = sys.argv[1], sys.argv[2]
OUT_DIR = os.path.join(REPO, "study", "problems-view")
os.makedirs(OUT_DIR, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{qid} — 題目解析</title>
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<script defer src="../assets/katex/katex.min.js"></script>
<script defer src="../assets/katex/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},
  {left:'$',right:'$',display:false},{left:'\\\\(',right:'\\\\)',display:false}],throwOnError:false});"></script>
<style>
:root{--ac:#1565c0;--bg:#f7f9fb;--card:#fff;--ink:#263238;--mut:#607d8b;--bd:#dfe6ea}
*{box-sizing:border-box}
body{margin:0;font-family:"Microsoft JhengHei","Noto Sans TC",-apple-system,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.75;font-size:15.5px}
header{background:linear-gradient(135deg,#0d47a1,#1976d2 60%,#42a5f5);color:#fff;padding:22px 26px}
header h1{margin:0;font-size:1.15em}
header .back{display:inline-block;margin-top:10px;font-size:.82em;color:#fff;background:rgba(255,255,255,.18);
  padding:4px 12px;border-radius:14px;text-decoration:none}
main{max-width:880px;margin:0 auto;padding:26px 22px 70px}
h1,h2,h3{color:#0d47a1} h2{font-size:1.2em;border-left:6px solid var(--ac);padding-left:12px;margin:34px 0 14px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.92em;background:#fff}
th,td{border:1px solid var(--bd);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#eceff1;font-weight:600} tbody tr:nth-child(even){background:#fafcfd}
code{background:#eceff1;padding:1px 5px;border-radius:4px;font-size:.92em}
img{max-width:100%;display:block;margin:14px auto;border:1px solid var(--bd);border-radius:8px}
.katex-display{margin:12px 0!important;overflow-x:auto;overflow-y:hidden}
footer{text-align:center;color:var(--mut);font-size:.8em;padding:22px;border-top:1px solid var(--bd)}
</style></head><body>
<header><h1>{qid} 題目解析</h1><a class="back" href="javascript:history.back()">← 返回講義</a></header>
<main>{body}</main>
<footer>來源：raw/solutions/{qid}/{qid}.md（知識庫解題內容唯一正本；本頁僅為渲染顯示）</footer>
</body></html>"""

def convert(qid):
    src = os.path.join(REPO, "raw", "solutions", qid, f"{qid}.md")
    if not os.path.exists(src):
        print("MISSING", qid); return
    text = open(src, encoding="utf-8").read()

    # 保護 $$...$$ 與 $...$，避免被 markdown 誤處理
    stash_list = []
    def stash(m):
        stash_list.append(m.group(0)); return f"@@MATH{len(stash_list)-1}@@"
    text = re.sub(r"\$\$.+?\$\$", stash, text, flags=re.S)
    text = re.sub(r"(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)", stash, text, flags=re.S)

    # 圖片：裸檔名（無 /）代表跟 .md 同資料夾，換算成相對 study/problems-view/ 的路徑；
    # 已經帶路徑（含 /）的連結視為已經正確，不要再加前綴（避免重複拼接）
    text = re.sub(r"\]\(([^/)]+\.(?:png|jpg|jpeg))\)",
                  lambda m: f"](../../raw/solutions/{qid}/{m.group(1)})", text)

    # 逐行檢查：緊接在段落後、沒有空行分隔的清單，補一個空行，
    # 否則 python-markdown／CommonMark 不會把它辨識成清單
    lines = text.split("\n"); fixed = []
    for line in lines:
        is_li = re.match(r"^\s*([-*+]|\d+\.)\s", line)
        prev = fixed[-1] if fixed else ""
        prev_is_li = re.match(r"^\s*([-*+]|\d+\.)\s", prev)
        if is_li and prev.strip() and not prev_is_li:
            fixed.append("")
        fixed.append(line)
    text = "\n".join(fixed)

    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
    body = re.sub(r"@@MATH(\d+)@@", lambda m: stash_list[int(m.group(1))], body)

    # [[wiki-link]] 在渲染頁沒有連結目標（連到 wiki/concepts、wiki/methods），
    # 顯示成一個小標籤即可，不要留原始雙中括號
    body = re.sub(r"\[\[([^\]]+)\]\]",
        r'<span style="background:#e3f2fd;color:#1565c0;border-radius:8px;padding:1px 7px;'
        r'font-size:.88em;font-weight:600">\1</span>', body)

    out = TEMPLATE.format(qid=qid, body=body)
    open(os.path.join(OUT_DIR, f"{qid}.html"), "w", encoding="utf-8").write(out)
    print("OK", qid)

for qid in [l.strip() for l in open(sys.argv[2]) if l.strip()]:
    convert(qid)
```

跑法：`python3 render_problems.py <REPO> /tmp/ids.txt`

**Step C — 把講義裡的題號連結改指到渲染頁：**

```python
import re
path = '<REPO>/study/lecture-XX-Un-m.html'
s = open(path, encoding='utf-8').read()
s, n = re.subn(r'href="\.\./wiki/problems/(XX-\d{4}-\d+)\.md"',
    r'href="problems-view/\1.html" target="_blank"', s)
print('replaced', n)
open(path, 'w', encoding='utf-8').write(s)
```

若題號是新產生（第一次寫連結，講義裡原本只有純文字題號），直接輸出：
`<a class="qlink" href="problems-view/{qid}.html" target="_blank">{qid}</a>`。

**驗證（不可省）：**

- 每個渲染出的 `.html` 都要有對得上的 `<img` 數量（用 `raw/solutions/<id>/` 底下 `*.png` 數量核對），
  沒有圖片的題目 0 張是正常的，不算錯誤。
- `grep -l "@@MATH" study/problems-view/*.html` 應該**沒有輸出**（代表數學式全部還原）。
- 抽 2–3 題檢查圖片路徑真實存在（`test -f <算出來的絕對路徑>`）。
- 講義裡不應該再有任何 `href=".*\.md"` 殘留：`grep -c '\.md"' study/lecture-XX-Un-m.html` 應為 0。

---

## Step 8：產出 PDF

**預設用 headless Chromium 列印**（2026-10 起五科講義的 PDF 都是這樣產的）：
KaTeX 直接在瀏覽器裡渲染，與 HTML 版一模一樣，不必另外轉數學式。
雲端容器預裝 Chromium／Playwright（`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`，不要 `playwright install`）。
HTML 必須放在 `study/` 底下（或連同 `study/assets/katex/` 一起複製過去）才載得到 KaTeX。

### 8.1 `build_pdf.py`（Chromium）

```python
# 用法: python3 build_pdf.py <study/lecture-XX-Un-m.html> <out.pdf> "<頁尾文字>"
import sys, re, os, asyncio
from playwright.async_api import async_playwright
SRC, PDF, FOOT = sys.argv[1], sys.argv[2], sys.argv[3]
doc = open(SRC, encoding="utf-8").read()
doc = re.sub(r"<nav>.*?</nav>", "", doc, flags=re.S)          # 列印版不放本機連結
doc = (doc.replace("<details>", '<div class="det">').replace("</details>", "</div>")
          .replace("<summary>", '<p class="sum">').replace("</summary>", "</p>"))   # 摺疊答案攤平
doc = doc.replace("</head>", """<style>
@page{size:A4;margin:14mm 13mm 16mm 13mm}
html,body{background:#fff!important;font-family:"Microsoft JhengHei","Noto Sans CJK TC",sans-serif;font-size:10.2pt;line-height:1.62}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
main{max-width:none;padding:0}
header{padding:20px 22px}header h1{font-size:19pt}header .sub{font-size:10pt}header .meta{font-size:8.5pt}
section{margin-bottom:20px}
h2{font-size:14pt;margin:20px 0 10px;break-after:avoid}h3{font-size:11.6pt;margin:15px 0 6px;break-after:avoid}
h4{font-size:10.6pt;break-after:avoid}
table{font-size:8.9pt}th,td{padding:4px 6px}tr{break-inside:avoid}
.fig,.why,.trap,.tens,.comp,.box,.lead{break-inside:avoid}
.fig{padding:10px 8px 6px;margin:12px 0}.fig .cap{font-size:8.6pt}
.why,.trap,.tens,.comp,.lead{padding:9px 13px;margin:11px 0;font-size:9.8pt}
.det{background:#fff;border:1px solid #dfe6ea;border-radius:8px;padding:8px 12px;margin:8px 0;break-inside:avoid}
.sum{font-weight:600;color:#1565c0;margin:0 0 4px}
.det p{border-left:3px solid #e0e0e0;padding-left:10px;color:#455a64;font-size:9.6pt}
footer{font-size:8.5pt;padding:14px}
</style></head>""")
tmp = os.path.join(os.path.dirname(os.path.abspath(SRC)), "_print_tmp.html")
open(tmp, "w", encoding="utf-8").write(doc)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + tmp)
        await pg.wait_for_function("document.querySelectorAll('.katex').length > 20", timeout=30000)
        await pg.wait_for_timeout(800)
        await pg.pdf(path=PDF, format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template=f'<div style="width:100%;text-align:center;font-size:8px;color:#78909c">{FOOT}　<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                     margin=dict(top="14mm", bottom="16mm", left="13mm", right="13mm"))
        await b.close()
asyncio.run(main()); os.remove(tmp); print("PDF ->", PDF)
```

**PDF 一定要跟著 HTML 重出。** 改版時最常漏的就是這一步（SS-U1-4、SD-U1-1、SD-U2-2 都曾留下舊圖版 PDF），
而講義 nav 的「🖨️ 本頁 PDF」與命題分析頁都連到它——舊 PDF 等於把已修正的錯誤繼續發出去。
真的無法重出時，在 `wiki/log.md` 與交付訊息都寫明「PDF 未更新」。

### 8.2 備援：MathJax → WeasyPrint（環境沒有 Chromium 時）

舊流程（2026-07 首批講義所用），僅在沒有 Chromium 的環境使用：MathJax 把 TeX 轉成內嵌 SVG → WeasyPrint 排版。

#### 8.2.1 環境（分開執行，單次 bash 上限 45 秒）

```bash
# 一定要裝在 /tmp，不要裝在掛載資料夾 —— 掛載點會漏檔（version.js、*.d.ts 掉失）
mkdir -p /tmp/v && cd /tmp/v && npm install mathjax-full@3.2.2 --no-audit --no-fund
```
```bash
pip install weasyprint --break-system-packages -q     # 約 40 秒
```

#### 8.2.2 `tex2svg.js`

```javascript
const fs = require('fs');
const P = '/tmp/v/node_modules/';
const {mathjax} = require(P + 'mathjax-full/js/mathjax.js');
const {TeX} = require(P + 'mathjax-full/js/input/tex.js');
const {SVG} = require(P + 'mathjax-full/js/output/svg.js');
const {liteAdaptor} = require(P + 'mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require(P + 'mathjax-full/js/handlers/html.js');
const {AllPackages} = require(P + 'mathjax-full/js/input/tex/AllPackages.js');
const adaptor = liteAdaptor(); RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {InputJax: new TeX({packages: AllPackages}),
                                  OutputJax: new SVG({fontCache: 'local'})});
const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = items.map(it => adaptor.outerHTML(
  doc.convert(it.tex, {display: it.display, em: 16, ex: 8, containerWidth: 800})));
fs.writeFileSync(process.argv[3], JSON.stringify(out), 'utf8');
console.log('converted ' + out.length);
```

`fontCache:'local'` 讓每個 SVG 自帶字形定義 —— WeasyPrint 不支援跨元素的全域字形快取。

#### 8.2.3 `build_pdf.py`

```python
#!/usr/bin/env python3
# 用法: python3 build_pdf.py <src.html> <out.pdf> <work_dir> "<頁尾文字>"
import re, json, subprocess, sys, html as htmllib

SRC, PDF, WORK = sys.argv[1], sys.argv[2], sys.argv[3]
FOOT = sys.argv[4] if len(sys.argv) > 4 else ''
src = open(SRC, encoding='utf-8').read()

# 1. 保護不可處理區塊（svg / style / script），只在一般 HTML 抽數學式
PROTECT = re.compile(r'(<svg\b.*?</svg>|<style\b.*?</style>|<script\b.*?</script>)', re.S | re.I)
parts = PROTECT.split(src)
items = []
def stash(tex, display):
    # 關鍵：TeX 內的 < > & 在 HTML 原始碼中被跳脫過，不還原會被 MathJax 當成
    # 對齊字元而產生 merror，PDF 上顯示為一整塊黑方框
    items.append({'tex': htmllib.unescape(tex.strip()), 'display': display})
    return '\x00MJ%d\x00' % (len(items) - 1)
for i in range(0, len(parts), 2):
    parts[i] = re.sub(r'\$\$(.+?)\$\$', lambda m: stash(m.group(1), True), parts[i], flags=re.S)
    parts[i] = re.sub(r'\\\((.+?)\\\)', lambda m: stash(m.group(1), False), parts[i], flags=re.S)

json.dump(items, open(WORK + '/math_in.json', 'w'), ensure_ascii=False)
subprocess.run(['node', WORK + '/tex2svg.js', WORK + '/math_in.json', WORK + '/math_out.json'], check=True)
rendered = json.load(open(WORK + '/math_out.json'))

doc = ''.join(parts)
doc = re.sub(r'\x00MJ(\d+)\x00',
             lambda m: ('<div class="mjd">%s</div>' if items[int(m.group(1))]['display']
                        else '<span class="mji">%s</span>') % rendered[int(m.group(1))], doc)

# 2. 移除 CDN／導覽列，<details> 攤平（列印沒有互動）
doc = re.sub(r'<link[^>]*cdn\.jsdelivr[^>]*>', '', doc)
doc = re.sub(r'<script\b[^>]*cdn\.jsdelivr.*?</script>', '', doc, flags=re.S)
doc = re.sub(r'<link[^>]*katex\.min\.css[^>]*>', '', doc)
doc = re.sub(r'<script\b[^>]*(katex|auto-render)\.min\.js.*?</script>', '', doc, flags=re.S)
doc = re.sub(r'<nav>.*?</nav>', '', doc, flags=re.S)
doc = (doc.replace('<details>', '<div class="det">').replace('</details>', '</div>')
          .replace('<summary>', '<p class="sum">').replace('</summary>', '</p>'))

doc = doc.replace('</head>', '''<style>
@page{size:A4;margin:15mm 14mm 16mm 14mm;
 @bottom-center{content:"''' + FOOT + '''  " counter(page) " / " counter(pages);
 font-family:"Noto Sans CJK TC";font-size:8.5pt;color:#78909c}}
html,body{background:#fff!important;font-family:"Noto Sans CJK TC",sans-serif;font-size:10.2pt;line-height:1.62}
main{max-width:none;padding:0}
header{padding:20px 22px;border-radius:0}
header h1{font-size:19pt}header .sub{font-size:10pt}header .meta{font-size:8.5pt}
section{margin-bottom:20px}
h2{font-size:14pt;margin:20px 0 10px;break-after:avoid}
h3{font-size:11.6pt;margin:15px 0 6px;break-after:avoid}
h4{font-size:10.6pt;break-after:avoid}
p{margin:7px 0}
table{font-size:8.9pt}th,td{padding:4px 6px}
thead{display:table-header-group}tr{break-inside:avoid}
.fig,.why,.trap,.tens,.comp,.box,.lead{break-inside:avoid}
.fig{padding:10px 8px 6px;margin:12px 0}.fig .cap{font-size:8.6pt}
.why,.trap,.tens,.comp,.lead{padding:9px 13px;margin:11px 0;font-size:9.8pt}
ul,ol{margin:6px 0 6px 2px}li{margin:3px 0}
.mjd{text-align:center;margin:11px 0;break-inside:avoid}.mjd svg{max-width:100%}
.mji svg{vertical-align:-0.22em}
mjx-container{display:inline-block}
.det{background:#fff;border:1px solid #dfe6ea;border-radius:8px;padding:8px 12px}
.sum{font-weight:600;color:#1565c0;margin:0 0 4px;border-left:none!important;padding-left:0!important}
.det p{border-left:3px solid #e0e0e0;padding-left:10px;color:#455a64;font-size:9.6pt}
a.qlink{color:#1565c0;text-decoration:none;font-weight:600}
footer{font-size:8.5pt;padding:14px}
</style></head>''')

open(WORK + '/print.html', 'w', encoding='utf-8').write(doc)
from weasyprint import HTML
HTML(filename=WORK + '/print.html', base_url=WORK).write_pdf(PDF)
print('PDF ->', PDF)
```

沙盒已內建 Noto Sans/Serif CJK，中文可正常輸出。


---

## Step 9：驗證（不可略過）

1. **圖的驗證**：依 Step 5.4 在瀏覽器逐張截圖目視，出界／重疊清單為空、KaTeX 錯誤 0。
2. **PDF 抽頁目視**：`pdftoppm -png -r 68 -f <n> -l <n> out.pdf chk/p`，
   然後用 Read 工具看圖。**至少檢查：首頁、流程圖頁、最後一頁、任一張跨頁風險大的圖。**
   要看的是：圖有沒有被切到兩頁、數學式有沒有變成黑方框、表格有沒有被切爛。
3. **題號核對**：用腳本比對講義中出現的題號與 `question_index.json` 的該單元清單，
   確認無缺漏、無誤植、考年正確。
4. **數值核對**：講義裡所有算出來的數字（範例、常數、交界點）都由 `calcs.py` 重算並 `assert`；
   圖上的數字與內文必須來自同一次計算。2026-10 改版就靠這一步抓到 SS-U1-3 範例 C 的算術錯誤
   （B₂ = 1/(1−0.296) 寫成 1.799，正解 1.420）。
5. **交叉引用**：檢查文中「見 §x.y」的節號在改版後仍然存在。
6. **教材互連**：講義 nav 的三顆按鈕、命題分析頁的按鈕都指向真實存在的檔案
   （`ls study/` 逐一核對），nav 內**沒有** Keynote／課堂投影片按鈕，
   全檔沒有「速查頁」字樣，且 PDF 版沒有殘留 nav。
7. **題號連結渲染**：依 Step 7「題號連結」小節的驗證清單逐項核對
   （無 `@@MATH` 殘留、圖片路徑存在、無 `.md` 連結殘留）。
8. **寫 log**：在 `<REPO>/wiki/log.md` 追加一筆（只可 append），寫明**改了什麼、為什麼錯、怎麼驗證的**、
   腳本位置、PDF 是否已重出、有哪些「觀察到但未改動、待使用者決定」的事項（例如題解正本與規範不符）。
   講義 footer 加一行改版日期與摘要。
9. **交付**：把講義直接寫進該科資料夾；回覆中列出**所有動到的檔案路徑**，git commit 由使用者自己做。

---

## Step 10：改版模式（講義已存在）

2026-10 五科講義改版的共同流程，照這個順序做：

1. **截圖盤點**：用 Step 5.4 的腳本把現有每張圖截下來，逐張用 Read 看，
   列出**錯誤清單**——分清「會教錯觀念的錯」（方向、正負、交點、視圖、比例、與內文數字不符）
   和「版面問題」（重疊、出界）。只有版面問題的圖可以微調，有觀念錯的一律重繪。
   沒有錯的圖（純文字對照圖等）保留不動，在 log 寫明保留哪幾張。
2. **內容對帳**：依 Step 1「再查勘誤紀錄」比對講義與 `raw/solutions/` 現行正本；
   依 Step 4 第 12–14 條檢查規範版本、查無出處的規定、考古題敘述。
   改動內文時同步所有出現處（流程圖、陷阱表、自我檢測、精選題說明常重複同一句）。
3. **重繪與新增**：依 Step 5.2 用程式產生，HTML 內加 `<!--FIG:id-->` 標記後就地替換。
   內文有講但沒有圖、而一張圖能說清楚的地方（分段公式的轉折、範例的幾何、載重—位移關係）可以新增圖，
   圖號依節次編，新增圖在 log 列出。
4. **備份**：改動前留 `.bak`（確認 `.gitignore` 已排除），或確認 git 有乾淨的上一版。
5. **CSS 檢查**：`.fig svg` → `.fig>svg`（見 Step 7）。
6. **PDF 重出**（Step 8），**驗證**（Step 9），**寫 log 與交付**（Step 9 第 8–9 項）。

---

## 已知地雷（都踩過，別再踩）

| # | 症狀 | 原因與解法 |
|---|------|-----------|
| 1 | PDF 上數學式變成整塊黑方框 | HTML 實體 `&lt;` `&gt;` 沒還原就餵給 MathJax，`&` 被當對齊字元 → `merror`。用 `html.unescape()` |
| 2 | SVG 裡出現字面的 `\(F_y\)` | KaTeX auto-render 不處理 SVG 文字節點。SVG 內改用純文字 |
| 3 | `npm install` 後 `MODULE_NOT_FOUND` | 裝在掛載資料夾會漏檔。改裝到 `/tmp` |
| 4 | CDN 抓不到（403 blocked-by-allowlist） | 沙盒只放行 npm／pypi。KaTeX 走 npm 取得後複製到 repo |
| 5 | bash 逾時 | 單次上限 45 秒。npm 與 pip 分開執行，不要串在一起 |
| 6 | 流程圖文字跑出方框 | 中文字寬≈font-size，先估寬再設 viewBox；文字寧可分行 |
| 7 | 掛載資料夾內 `rm` 失敗（Operation not permitted） | 別在掛載點做 npm 的清除；暫存一律用 `/tmp` |
| 8 | 題號連到 `wiki/problems/*.md` 或 `raw/solutions/*.md`，使用者點開只看到未渲染純文字 | 改產生 `study/problems-view/*.html`（見 Step 7「題號連結」），連結指向渲染頁並 `target="_blank"` |
| 9 | 渲染題目頁圖片破圖或路徑重複拼接（如 `.../SS-2002-3/../../raw/solutions/SS-2002-3/...`） | `wiki/problems/*.md` 本身不含圖片、且部分連結已帶相對路徑；一律以 `raw/solutions/<id>/<id>.md` 為來源，圖片路徑替換只處理「裸檔名（無 `/`）」，已帶路徑的連結不要重複加前綴 |
| 10 | markdown 清單沒被辨識、擠在同一段落裡 | 原始 `.md` 常見「一行敘述後緊接 `- 項目`、中間沒空行」，python-markdown 需要空行才辨識清單起點；轉換前先逐行掃描補空行 |
| 11 | 科目代號對到錯的資料夾（SM/MM 互換） | 舊版適用科目表把 SM 寫成材料力學、MM 寫成工程數學。一律查 `raw/json/syllabus_taxonomy.json` |
| 12 | 曲線上的標記點不在曲線上、曲線形狀與公式不符 | 手描貝茲線或目測座標。曲線與標記點用同一個函式取點（Step 5.2） |
| 13 | 受力圖成對的力方向畫反（例：節點域兩側翼板力相對 → 互相抵消、不產生剪力） | 先寫平衡式與符號約定，再由正負號決定箭頭；分清對稱載重與側移載重 |
| 14 | 特徵畫在看不到它的視圖（RBS 畫在立面、ESW 位置指錯） | 先決定平面／立面／斷面，在圖上標註視圖名稱 |
| 15 | 圖說裡的 KaTeX 根號消失 | CSS 寫成 `.fig svg` 套到 KaTeX 的 SVG。改 `.fig>svg` |
| 16 | 數學式變紅字（`\text{tf·m}`）、`%` 後內容消失、`<` 吃掉整段 | 見 Step 7「KaTeX 寫法地雷」表 |
| 17 | 不同圖的箭頭顏色互相污染 | marker id 重複。每張圖的 id 加圖號前綴 |
| 18 | `⅔`、`✔`、`✘` 顯示成方框；`x̄` 的橫線偏到旁邊 | 缺字或斜體組合字元。避開這些字元；`x̄` 用直立襯線字型 |
| 19 | 講義仍教題解已勘誤前的錯解 | 寫作前查 `wiki/log.md` 勘誤紀錄與 `raw/solutions/` 修正日期（Step 1） |
| 20 | 講義出現規範查不到的條文、或混用不同版本的係數 | Step 4 第 12、13 條：寫版本、查無出處就刪 |
| 21 | HTML 已改版，PDF 還是舊圖 | PDF 一定跟著重出（Step 8.1）；做不到就在 log 與交付訊息寫明 |
| 22 | 流程圖有死路、分支沒標籤、兩支箭頭打進同一個菱形頂點 | 先排節點座標格線再連線；每條分支標「是／否」並匯流到收尾框 |

---

## 產出後

1. 一句話交代成果與檔案位置，**不要複述講義內容**；列出動到的檔案路徑，commit 留給使用者。
2. 主動指出這份講義**沒涵蓋**什麼、以及你認為還可以再加強的地方 —— 誠實的自我批評比推銷有價值。
3. 詢問是否要對同科其他單元或其他科目比照辦理。

