# 結構工程技師考試知識庫（五科）
# 規格與檢核清單（CLAUDE-SPEC.md）

> 本文件為知識庫的所有「資料格式、命名規則、JSON 欄位、完成標準」唯一依據。
> **Cowork 進行任何新增或修改時，必須遵守本文件的規定。**
> 五科共用；科目專屬的允許值（designMethod、互動圖內容碼、七層類別）見 `XX/SUBJECT.md`。
> 範例多取自 SS，其他科照同一格式代換科目代碼即可。

---

## 1. 命名規則（全專案適用）

所有資料夾與檔案名稱必須**完全小寫或大寫（依規定），單字間以短橫線（`-`）連接**。

### 1.1 題庫與模組

- 學科（Subject）代碼：`SS`／`RC`／`SA`／`SD`／`SM`（另保留 `MM`），以根目錄 `syllabus_taxonomy.json` 的 `subjects[].id` 為準。
- 每科一個資料夾，資料夾名稱＝科目代碼（大寫）。
- 題號模組（ModuleId）：`XX-YYYY-N`
  - YYYY 為**西元年**（如 2015、2024）。
  - N 為該卷題號（如 1、2、3、4，部分有 5）。
  - 例：`SS-2015-1`

### 1.2 圖檔與補充檔案

- 題目附圖：`XX-YYYY-N-fig-n.png`（由使用者手動截圖）
- 官方設計圖表截圖：`XX-YYYY-N-chart-n.png`
- 參考公式截圖：`XX-YYYY-N-eqn-n.png`
- 手寫補充：`XX-YYYY-N-hand-n.png`
- PDF 補充筆記：`*.pdf`（由使用者放入對應題目資料夾，命名無強制規範）

> **⚠️ 禁止：** 不可使用 `SS-2015-1-fig.png`（必須有後置序號 `-1`）。

### 1.3 `study/` 產出命名

`study/` 底下有兩種用途不同的教材，**以前綴區分，不可混用**：

| 前綴 | 檔名 | 產生方式 | 定位 |
|------|------|---------|------|
| `study-` | `study/study-XX-UN.html`（單元層級）<br>`study/study-XX-UN-n.html`（子項層級） | 單元層級：`study` 指令<br>子項層級：`unit-exam-intel` skill | **命題分析**（子項層級）：出題頻率、考點結構、考點漂移、設計法走向、考題清單、命題風險。決定練題順序、考前押題用 |
| `lecture-` | `study/lecture-XX-UN-n.html`<br>`study/lecture-XX-UN-n.pdf` | `unit-lecture` skill | **觀念講義**：物理原理、公式來源、圖解推導。第一次接觸該單元、練題**之前**用 |
| `formula-given-` | `study/formula-given-XX-UN-n.html`<br>`study/formula-given-XX-UN-n.pdf` | `unit-formula-map` skill | **給／背分界**：逐條公式 × 逐年考卷證據，判斷哪些會印給你、哪些必須自己背。排讀書計畫時用 |

- 兩者針對同一子項時**並存**，後者不可覆蓋前者。
- 講義的 PDF 與 HTML **同名**，僅副檔名不同。
- 共用資源放 `study/assets/`（目前有 `assets/katex/`，供 `lecture-*.html` 離線渲染數學式）。
  此目錄**必須進版控**，刪除會導致所有講義的數學式無法顯示。

> **⚠️ 禁止：** 觀念講義不可命名為 `study-XX-UN-n.html`（會覆蓋該子項的命題分析頁）。
> 三份教材的檔名固定為 `lecture-`（觀念講義）／`formula-given-`（給／背分界）／`study-`（命題分析），不可互換。

### 1.4 互動圖（HTML）

- 由 Cowork 在解析時生成，格式為 `XX-YYYY-N-[內容碼]-viz.html`
- 內容碼依科目而定，**允許值見 `XX/SUBJECT.md` §4**（新內容碼要同步加到 `scripts/subject_profiles.json`）。SS 的內容碼：
  - 梁設計/剪力力學：`sfd-bmd`
  - 梁柱桿件（軸力與雙向彎矩）：`pm`
  - 側扭挫屈判斷：`ltb`
  - 柱強度曲線：`column-curve`
  - 接合詳圖：`connection`
- 例：`SS-2018-2-pm-viz.html`

> **⚠️ 禁止：** 不可使用 `SS-2018-2-viz.html` 或 `SS-2018-2-pm.html`。必須有特定的內容碼及 `-viz` 後綴。

### 1.5 Wiki 概念與方法論（由 Cowork 建立）

- 概念頁 ID（ConceptId）：`大寫-大寫.md`
  - 例：`EFFECTIVE-LENGTH-FACTOR.md`、`LATERAL-TORSIONAL-BUCKLING.md`
- 方法論 ID（MethodId）：`小寫-小寫.md`
  - 例：`conjugate-beam.md`、`b1b2-amplification.md`

### 1.6 根目錄與科目層的共用檔

| 檔案 | 位置 | 規則 |
|------|------|------|
| `syllabus_taxonomy.json` | 根目錄（正本） | 只改正本，改完執行 `python scripts/sync_taxonomy.py` |
| `syllabus_taxonomy.json` | `XX/raw/json/`（副本） | 不可手改（供 skills 以科目資料夾為工作目錄時讀取） |
| `SUBJECT.md` | `XX/` | 科目層設定與科目 CHANGELOG，與 `scripts/subject_profiles.json` 同步 |
| `index.html` | `XX/` | 五科共用樣板副本，不可個別修改（改 `scripts/templates/dashboard-index.html`） |
| `dashboard-data.js` | `XX/` | 只由 `scripts/refresh_dashboard.py` 產生 |

---

## 2. 原始資料層（`raw/`）規範

### 2.1 JSON 規範

**`raw/json/question_index.json`**（唯一由人工維護/授權 Cowork 更新的檔案）
> 每新增一題解析，必須確保對應條目完整填寫。

```json
{
  "moduleId": "SS-2015-1",         // YYYY 必須為西元
  "year": 2015,
  "number": 1,
  "primaryTopicId": "SS-U1-2",     // 對應 syllabus_taxonomy.json 的子項 ID
  "secondaryTopicIds": ["SS-U2-2"],// 跨考點時填寫（必為陣列）
  "designMethod": "LRFD",          // 允許值依科目，見 XX/SUBJECT.md §3（SS：LRFD / ASD / 概念題 / 混合 / 塑性分析）
  "hasSolution": true,             // 只要有 .md 就是 true
  "verificationStatus": "verified",// unverified / needs-review / verified
  "hasHandwritten": false,         // 有無 -hand-*.png
  "hasViz": true,                  // 有無 *-viz.html
  "tags": [                        // 至少 3 個具體考點標籤
    "結實斷面",
    "Cb係數",
    "塑性彎矩"
  ]
}
```

> ⚠️ 注意：所有 YYYY 均為西元。

**`raw/json/concepts.json`**（由 Cowork 生成與維護，供 compile 使用）
```json
{
  "LATERAL-TORSIONAL-BUCKLING": {
    "topicId": "SS-U1-2",
    "name_zh": "側向扭轉挫屈",
    "name_en": "Lateral-Torsional Buckling, LTB",
    "definition": "...",
    "related_concept_ids": ["PLASTIC-MOMENT", "RESIDUAL-STRESS"]
  }
}
```

### 2.2 題目附屬檔案（由 Cowork 或使用者產生）

所有附檔存放在該題資料夾內（`raw/solutions/XX-XXXX-N/`）。

**圖形嵌入要求（在 .md 中）：**

1.  **使用者截圖的 PNG 檔 (`-fig`, `-chart`, `-eqn`, `-hand`)**：
    - 必須提供準確的 alt text 與 `*圖說：...*` 說明（讓 AI 看不到圖也能解題）。
    - 範例：
      ```markdown
      ![SS-2015-1 題目附圖：長度 6m 之簡支梁，受中心集中活載重 PL 及均佈靜載重 qD](SS-2015-1-fig-1.png)

      *圖說：6m 簡支梁，兩端鉸接，跨中受 PL=10t。上方載重為均佈靜載重 2t/m（含自重）。斷面型式為 W400x200x8x13。*
      ```

2.  **使用者補充的 PDF 檔 (`*.pdf`)**：
    - 命名無強制規範（例：`老師解答.pdf` 或 `筆記.pdf`）。
    - 放入資料夾後，不需在 .md 內引用；但需對 Cowork 說 `更新儀表板資料`，儀表板的題卡會自動產生「📎 補充筆記 PDF」按鈕。

3.  **Cowork 生成的互動 HTML 圖 (`*-viz.html`)**：
    - 在 `.md` 中以特定標記顯示連結。
    - 範例：
      ```markdown
      > 📊 互動圖：[梁柱 P-M 互制圖 (SS-2018-2-pm-viz.html)](SS-2018-2-pm-viz.html)
      ```

---

## 3. Wiki 輸出層（`wiki/`）規範

此層檔案除了 `wiki/diagnosis/`、`wiki/failure-modes/`、`wiki/materials/`、`wiki/code-ref/` 與 `wiki/queries/` 之外，其餘均由 `ingest` 或 `compile all` 指令生成。

### 3.1 題解 Markdown 模板（由 ingest 寫入）

> 從 `raw/` 讀入時，Cowork 會在文檔最開頭（H1 之後，正文之前）注入 Meta 區塊。

```markdown
# 考題編號：[XX-XXXX-N]

**主分類：** `SS-U1-2` 梁桿件
**副分類：** 無
**設計法：** LRFD
**標籤：** `LTB` `Cb係數` `非結實斷面`

---
（接續 raw/solutions/XX-XXXX-N/XX-XXXX-N.md 內容）
```

### 3.2 內部連結格式（Wiki 化）

- 概念連結：`[[LATERAL-TORSIONAL-BUCKLING]]`（不帶 .md，大寫大寫-大寫）
- 題目連結：`[[SS-2015-1]]`（大寫）
- 方法論連結：`[[b1b2-amplification]]`（小寫小寫-小寫）
- GitHub 內文跳轉錨點規則：`#小寫英數與短橫線`。
  - 例：跳轉至 `## 2. 考點分析` → `[前往考點](#2-考點分析)`

### 3.3 公式編排與 KaTeX 規範

1.  **公式顯示環境：**
    - 獨立數學式（display mode）必須使用 `$$...$$`，並前後空行。
    - 行內數學式（inline mode）必須使用 `$...$`。
    - 在 Markdown 表格中，不要使用複雜的 display mode。
2.  **上標與下標：** 多字元下標必須加大括號（如 `F_{cr}`，不是 `F_cr`）。
3.  **符號一致性：** 單位使用正體字 `\text{ kN}`，如 `$P = 100 \text{ kN}$`。

### 3.4 變數層次分析（VHA）格式模板

> 在解析檔案的 `## 3.5 變數層次分析 (Variable Hierarchy Analysis)` 必須嚴格遵照以下 Markdown 格式輸出。

```markdown
## 3.5 變數層次分析 (Variable Hierarchy Analysis)
> 複習提示：第一次解題後，在每個卡住的知識點旁標記 `⚠`；第二次複習時只看有 `⚠` 的項目。

### 最終目標
計算梁柱桿件承受雙向彎矩下的 P-M 互制比，判斷是否 ≤ 1.0。

### 本題關鍵公式（依計算順序）
- 1. $A_g = b_f t_f \times 2 + (d - 2t_f)t_w$  (求全斷面積)
- 2. $\lambda_c = \frac{KL}{r\pi}\sqrt{\frac{F_y}{E}}$ (求柱細長比)
- 3. $F_{cr} = 0.658^{\lambda_c^2} F_y$ (求柱壓應力，含 $\boxed{\lambda_c}$)
- 4. $P_n = \boxed{A_g} \times \boxed{F_{cr}}$ (求標稱軸力)

### L1：題目直接給定
_看到題目就能讀出的數字，不需要任何公式。_

| 符號 | 數值 | 說明 |
|:---:|:---|:---|
| $K$ | 1.0 | 兩端鉸接柱有效長度係數 |
| $L$ | 600 cm | 桿件總長 |
| $F_y$ | 2.5 tf/cm² | A36 鋼降伏應力 |
| $E$ | 2040 tf/cm² | 鋼材彈性模數 |

### L2：需知識點推導
_需要知道公式名稱與適用條件，套入 L1 即可算出。_

**第一階段：斷面幾何性質**
| 符號 | 公式／來源 | 卡關? |
|:---:|:---|:---|
| $A_g$ | $b_f t_f \times 2 + (d - 2t_f)t_w$ | |
| $r_y$ | $\sqrt{I_y/A_g}$ | |

**第二階段：柱軸力設計 (LRFD)**
| 符號 | 公式／來源 | 卡關? |
|:---:|:---|:---|
| $\lambda_c$ | $\frac{KL}{r\pi}\sqrt{\frac{F_y}{E}}$ | |
| $F_{cr}$ | 非彈性區挫屈：$0.658^{\lambda_c^2} F_y$ | |

### L3：深層知識（不懂就卡住）

| 知識點 | 說明 | 卡關? |
|:---|:---|:---|
| LTB 判斷條件 | 未知 $L_b$ 時須先檢核 $L_b$ 與 $L_p, L_r$ 關係決定強度 | |
| 強弱軸挫屈控制 | $P_n$ 須取 $x$ 軸與 $y$ 軸挫屈強度的較小值 | |
```

---

## 4. 完成標準清單

### 4.1 Cowork 解完一題後（SOLVE）

見 `skills/exam-solve/SKILL.md`「完成檢核」（2026-10-29 移入，避免兩份清單不同步）。

### 4.2 ingest 到 Wiki
- [ ] 前置檢查：`verificationStatus === "verified"`
- [ ] `wiki/problems/[id].md` 被建立
- [ ] 對應的 `concepts.json` 條目的相關題目表格已更新
- [ ] `wiki/index.md` 與 `wiki/by-year.md` 已追加此題連結
- [ ] 在 `wiki/log.md` 紀錄此操作
