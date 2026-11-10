# 結構工程技師考試知識庫（五科）
# 規格與檢核清單（CLAUDE-SPEC.md）

> 本文件為知識庫的所有「資料格式、命名規則、JSON 欄位、完成標準」唯一依據。
> **Cowork 進行任何新增或修改時，必須遵守本文件的規定。**
> 五科共用；科目專屬的允許值（designMethod、常見圖解）見 `XX/SUBJECT.md`。
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

- 題目附圖：`XX-YYYY-N-fig-n.png`（由 Cowork 以 `scripts/extract_figure.py` 從考卷 500 dpi 擷取；使用者手動截圖亦可）
- 題目附圖向量抽取：`XX-YYYY-N-fig-n-vector.svg`（附圖在 PDF 中為向量線條時產生）
- 題目重繪：`figs/XX-YYYY-N-fig-n-problem.svg`＋`.png`（struct-diagram，依已確認的判讀清單產生）
- 官方設計圖表截圖：`XX-YYYY-N-chart-n.png`
- 參考公式截圖：`XX-YYYY-N-eqn-n.png`
- 手寫補充：`XX-YYYY-N-hand-n.png`
- PDF 補充筆記：`*.pdf`（由使用者放入對應題目資料夾，命名無強制規範）

> **⚠️ 禁止：** 不可使用 `SS-2015-1-fig.png`（必須有後置序號 `-1`）。

### 1.3 `study/` 產出命名

`study/` 底下的教材**以前綴區分，不可混用**：

| 前綴 | 檔名 | 產生方式 | 定位 |
|------|------|---------|------|
| `unit-` | `study/unit-XX-UN-n.html`／`.pdf`，資料 `study/data/unit-XX-UN-n.json` | `unit-overview` skill（`scripts/build_unit_page.py`） | **單元總覽**：命題分析＋公式給／背＋逐題公式表合一頁。決定練題順序、背誦優先序用 |
| `lecture-` | `study/lecture-XX-UN-n.html`／`.pdf` | `unit-lecture` skill | **觀念講義**：物理原理、公式來源、圖解。第一次接觸該單元、練題**之前**用 |
| `textbook-` | `study/textbook-XX-UN-n[-<冊名>].html`／`.pdf` | `unit-textbook` skill | **教科書**：以第一性原理推導每條公式，可分上下冊 |
| `frequency-` | `study/frequency-XX.html` | `subject-frequency-map` skill（`scripts/build_frequency.py`） | **全科出題頻率熱圖**：整科從哪裡開始讀 |
| （起點頁） | `XX/start.html`，資料 `study/data/start-links.json` | `exam-start-page` skill（`scripts/build_start.py`） | 給考生的入口：學習路徑、各單元教材、進度表 |

- 同一子項的各種教材**並存**，不可互相覆蓋。
- 講義、教科書、單元總覽的 PDF 與 HTML **同名**，僅副檔名不同。
- 共用資源放 `study/assets/`（目前有 `assets/katex/`，供教材頁離線渲染數學式）。
  此目錄**必須進版控**，刪除會導致所有講義的數學式無法顯示。
- 由資料檔產生的頁面（`unit-`、`frequency-`、`start.html`）不手改 HTML，改資料檔後重跑腳本。

> **⚠️ 禁止：** 觀念講義不可命名為 `study-XX-UN-n.html` 或 `unit-XX-UN-n.html`（會覆蓋其他教材）。

### 1.4 圖解（struct-diagram）

- **互動圖（`*-viz.html`）已於 2026-10-29 停用**，不再新增（SS 既有 19 份已於 2026-11-01 刪除）。
- 圖解一律由 `struct-diagram` skill 以程式產生，放在題目資料夾：
  - 產圖腳本：`XX-YYYY-N/gen_XX-YYYY-N.py`（可重跑，隨解析版控）
  - 圖檔：`XX-YYYY-N/figs/XX-YYYY-N-fig-<序號>-<英文短語意>.svg` ＋ 同名 2× `.png`
  - 例：`SA-2025-1-fig-2-dof.svg`
- ⚠️ 與使用者截圖的命名區分：截圖是 `XX-YYYY-N-fig-n.png`（資料夾根層），程式圖在 `figs/` 底下且有英文短語意。
- `.md` 只引用 SVG 相對路徑，不可 base64 內嵌。

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
  "tags": [                        // 至少 3 個具體考點標籤
    "結實斷面",
    "Cb係數",
    "塑性彎矩"
  ]
}
```

> ⚠️ 注意：所有 YYYY 均為西元。

**`raw/json/concepts.json`**（compile-all 已停用，保留備查，不再維護）
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

3.  **struct-diagram 產生的圖解 (`figs/*.svg`)**：
    - 插在對應章節正下方，附 alt text 與「*圖 n　…*」圖說；圖說要說出這張圖攔下什麼錯。
    - 範例：
      ```markdown
      ![SA-2025-1 自由度辨識圖](figs/SA-2025-1-fig-2-dof.svg)

      *圖 2　自由度辨識。「忽略軸向變形」直接決定勁度矩陣是 3×3 還是 6×6。*
      ```

---

## 3. 題解呈現與連結規範

> 2026-11-08 起 wiki 封存，題目頁不再由 ingest 寫入 `wiki/problems/`；本節編號保留（§3.3、§3.4 被 skills 引用）。

### 3.1 題目瀏覽頁（`study/problems-view/`）

- 由 `python scripts/render_problem_view.py XX-YYYY-N` 從 `raw/solutions/XX-YYYY-N/XX-YYYY-N.md` 產生；有題目正本時渲染在解析之前。
- 只換 `<main>` 內容，頁首按鈕、樣式、腳本保留；**不手改**，改正本後重跑。

### 3.2 內部連結格式

- 題目連結：`[[SS-2015-1]]`（大寫；儀表板與 problems-view 會轉為藍色徽章）
- 方法論連結：`[[b1b2-amplification]]`（小寫小寫-小寫，對應 `raw/solutions/methods/`）
- 概念連結 `[[CONCEPT-ID]]` 只出現在舊檔與 `archive/wiki/`，新內容不再使用
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

### 4.2 題目正本確認後

- [ ] `XX-YYYY-N-problem.md` 頭表「判讀狀態」改為**已確認**
- [ ] `question_index.json` 該題 `problemStatus` 改為 `confirmed`
- [ ] 解析 §1 與題目正本一致（衝突時以題目正本為準，走 exam-errata 勘誤解析）
- [ ] 重跑 `scripts/render_problem_view.py XX-YYYY-N`
- [ ] 在 `wiki/queries/log.md` 紀錄此操作
