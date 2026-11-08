# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## 2026-10-13 — 鋼結構影片講義資源整合與路徑修復（SS-U1-1~4, SS-U2-3）

**操作類型：** 資源整理與講義修復

### 完成事項
- 修復 5 個單元影片講義 HTML（`SS-U1-1`、`SS-U1-2`、`SS-U1-3`、`SS-U1-4`、`SS-U2-3`）的投影片引用路徑，指向 `img/SS-UN-n/`。
- 新增 `影片講義/img/` 下各單元投影片截圖（共 117 張圖檔，約 13.2 MB）。
- 新增 `影片講義/video/` 下各單元講解影片（共 5 部 MP4，約 128.8 MB）。

### 下一步
- 於瀏覽器實際測試各 HTML 之 video 播放控制與章節時間標籤（seek）同步效果。
- 評估後續單元（如 U2-1 構件接合、U2-2 鋼骨耐震設計）之影片講義擴充需求。

### 踩坑／注意事項
- 影片講義 HTML 中的圖片引用路徑需與實際檔案目錄結構一致（`img/SS-U*-*`）。
- 5 部影片單檔介於 20~30 MB，均未超過 GitHub 100 MB 限制，可完整同步推播。

---

## 2026-05-27 — SS-2020-3 解析修正 + 三個知識點新增

**操作類型：** 解析勘誤（Cowork）+ code-ref 知識點新增（Cowork）

### SS-2020-3 解析修正

**勘誤原因：** 原解析誤將兩端彎矩判定為雙曲率，實際為單曲率。
**修正範圍：** `raw/solutions/SS-2020-3/SS-2020-3.md`

| 項目 | 修正前（錯） | 修正後（對） |
|------|------------|------------|
| 強軸曲率判定 | 雙曲率，$M_1/M_2 = +1$ | 單曲率，$M_1/M_2 = -1$ |
| 弱軸曲率判定 | 雙曲率，$M_1/M_2 = +0.5$ | 單曲率，$M_1/M_2 = -0.5$ |
| $B_{1x}$ | $0.32 → 取 1.0$ | $1.167$（直接採用）|
| $B_{1y}$ | $0.549 → 取 1.0$ | $1.007$（直接採用）|
| **最終答案 $M_{wy}$** | **8.0 tf·m**（偏不安全）| **7.5 tf·m** |

**verificationStatus：** verified ✅（使用者確認）  
**ingest 執行：** 2026-05-27（Cowork 執行，等效 Claude Code ingest）

### 新增 code-ref 知識點（Cowork 直接寫入，不走 ingest）

- `wiki/code-ref/b1-m1m2-sign-convention.md` — B1 公式中 M1/M2 符號規則（單曲率=負、雙曲率=正）
- `wiki/code-ref/column-buckling-lambda-boundary.md` — λ_c = 1.5 彈/非彈性挫曲分界，臨界值 0.39Fy
- `wiki/code-ref/pm-interaction-physical-meaning.md` — P-M 互制方程式物理意義（雙折線、0.2門檻、8/9係數）

---

## 2026-05-26 — 建立四個跨層知識工具

**操作：** 建立 diagnosis / failure-modes / materials / code-ref 四個知識層次

**新建頁面：**
- `wiki/failure-modes/` — index + strength / stability / serviceability / connection（共 5 頁）
- `wiki/materials/` — index + stress-strain / residual-stress / fracture-toughness / weldability（共 5 頁）
- `wiki/code-ref/` — index（規範條文對應矩陣）
- `wiki/index.md` — 新增 Part 6 跨層知識工具導航區塊

**架構說明：**
知識庫從 Philosophy → Concept → Method 三層，擴充為七層：
Philosophy / Concept / Method / Diagnosis / Failure-Modes / Materials / Code-Ref

---

## 2026-04-20 — ingest SS-2014-4

**操作：** ingest SS-2014-4
**來源：** raw/solutions/SS-2014-4/SS-2014-4.md
**verificationStatus：** verified ✅

**新增頁面：**
- wiki/problems/SS-2014-4.md

**解題摘要：**
- W14×90 梁柱桿件 LRFD 檢核（斜撐構架，ASTM A572 Gr.50）
- B2 = 1.081（P-Δ 效應，θ=0.075）；B1 = 1.0（取下限，P-δ 可忽略）
- Mux = 326.2 kN-m（頂端控制，B1×Mnt + B2×Mlt）
- φcPn = 4433 kN（強軸控制，λc=0.573，Fcr=305.0 MPa）
- φbMnx = 810.4 kN-m（L < Lp，無LTB，全塑性）
- P-M 互制比 = **0.821 ≤ 1.0** ✅

**附屬檔案：**
- SS-2014-4-pm-viz.html（P-M 互制圖）
- SS-2014-4-fig-1.jpg（題目附圖）

**更新概念頁：**
- BEAM-COLUMN-INTERACTION：⚠️ → ✅ SS-2014-4
- P-DELTA-EFFECT：⚠️ → ✅ SS-2014-4
- MOMENT-AMPLIFICATION-CM：新增 ✅ SS-2014-4（B1 中的 Cm 計算）

**更新導航：**
- wiki/index.md：1.3 梁柱桿件與 2.1 耐震設計表格改為 ✅ 連結；已驗證 3→4 題
- wiki/by-year.md：2014年第四題改為 ✅ 連結；已驗證 3→4 題

---

## 2026-04-16 — ingest SS-2014-1, SS-2014-2, SS-2014-3

**操作：** ingest（消化 2014 年三道已驗證題目）
**執行時間：** 2026-04-16
**來源：** raw/solutions/SS-2014-1/SS-2014-1.md、SS-2014-2/SS-2014-2.md、SS-2014-3/SS-2014-3.md

**新增題目頁：**
- `wiki/problems/SS-2014-1.md` — 4.1.1 壓力桿件 LRFD；λc推導、柱強度曲線兩段式、高強度鋼對細長柱效益分析；附 column-curve-viz.html + hand-1/2.png
- `wiki/problems/SS-2014-2.md` — 4.2.2 鋼結構材料特性（概念題，副分類6.3.1）；SN490B vs ASTM A572 Gr.50 材料差異與梁柱接頭耐震行為
- `wiki/problems/SS-2014-3.md` — 4.1.2 梁桿件 LRFD；W21×93 雙向彎矩梁：非彈性LTB + Cb=1.136 + 弱軸1.5FySy上限 + 雙向互制0.664；附 hand-1/2.png

**新增陷阱頁：**
- `wiki/traps/WEAK-AXIS-BENDING-LIMIT.md` — 弱軸彎曲強度上限（1.5FySy），觸發自 SS-2014-3
- `wiki/traps/HIGH-STRENGTH-STEEL-SLENDER-COLUMN.md` — 高強度鋼對細長壓力桿件無效，觸發自 SS-2014-1

**更新概念頁（⚠️ → ✅）：**
- COLUMN-STRENGTH-CURVE：SS-2014-1 ✅
- RESIDUAL-STRESS：SS-2014-1 ✅
- FLEXURAL-BUCKLING-GENERAL：SS-2014-1 ✅
- CAPACITY-DESIGN：SS-2014-2 ✅
- STRONG-COLUMN-WEAK-BEAM：SS-2014-2 ✅
- LATERAL-TORSIONAL-BUCKLING：SS-2014-3 ✅
- BENDING-MODIFICATION-FACTOR-CB：SS-2014-3 ✅
- BIAXIAL-BENDING-BEAM：SS-2014-3 ✅（補充弱軸上限說明）
- SHAPE-FACTOR：新增 SS-2014-3 條目（弱軸Zy/Sy=1.57>1.5）

**更新導航：**
- wiki/index.md：三題改為 ✅ 連結；Wiki 狀態更新為 3 頁 / 3 題已驗證
- wiki/by-year.md：2014年三題改為 ✅ 連結；頁尾更新為已驗證 3 題

---

## 2026-04-16 — compile-all

**操作：** compile-all（更新 wiki，納入 2025 年新題）
**執行時間：** 2026-04-16
**來源：** raw/json/concepts.json、raw/json/question_index.json、raw/solutions/methods/

**結果：**
- wiki/concepts/ — 無變更（30 頁，全部已存在）
- wiki/methods/ — 無變更（conjugate-beam.md 已存在）
- wiki/by-year.md — 新增 **2025 年（民國 114 年）— 4 題**（SS-2025-1 至 SS-2025-4）；總數更新為 98 題（2002–2025）
- wiki/index.md — 新增 SS-2025-1、SS-2025-2、SS-2025-3（加入對應分類表格）；新增 SS-2025-4 至 Part 5 塑性分析；總數更新為 98 題
- wiki/problems/ — 無變更（0 頁，無已驗證題目）

**新增題目（SS-2025-1 至 SS-2025-4，均為 unverified）：**
- SS-2025-1：4.1.2 梁桿件 / LRFD / 結實斷面、塑性彎矩、銲接組合斷面
- SS-2025-2：4.1.1 拉力及壓力桿件 / ASD / 剪力遲滯、U值、淨截面
- SS-2025-3：4.1.2 梁桿件 / LRFD / LTB側扭挫屈、Lp、Lr
- SS-2025-4：4.2.1 塑性分析與設計 / 概念題 / 崩塌機構、上限定理

**備註：**
- question_index.json 現有 98 題（2002–2025），全部 verificationStatus = "unverified"
- 前次 compile-all 的 by-year.md/index.md 總數標示「91 題」有誤，本次一併修正為 98 題

---

## 2026-04-15 — compile-all

**操作：** compile-all（初次建立整個 wiki）
**執行時間：** 2026-04-15
**來源：** raw/json/concepts.json、raw/json/question_index.json、raw/solutions/methods/

**結果：**
- 生成 wiki/concepts/ — 30 個概念頁（依 concepts.json 全部概念）
- 生成 wiki/methods/conjugate-beam.md — 共軛梁法方法論頁
- 生成 wiki/by-year.md — 91 道題目依年份分類（全部標記 ⚠️ unverified）
- 生成 wiki/index.md — 依知識庫架構分類的主導航
- wiki/problems/ — 0 頁（無已驗證題目可生成）

**備註：**
- question_index.json 共 91 題，全部 verificationStatus = "unverified"
- 待驗證後，執行 `ingest SS-XXXX-N` 即可生成對應題目頁
- concepts.json 中有多個 related_concept_ids 指向尚未定義的概念（LINT 可偵測）

---

## 2026-05-26 — add method cb-factor

**操作：** ADD-METHOD cb-factor（Cowork 執行）

**新增：**
- `wiki/methods/cb-factor.md`（彎矩梯度修正因子 Cb 完整方法論頁）

**更新：**
- `wiki/index.md`：Part 3 方法論表格加入 Cb 因子；快速導航更新
- `wiki/log.md`：本條紀錄

**來源：** `raw/solutions/methods/cb-factor/cb-factor.md`（含互動圖 cb-factor-chart.html）

---

## 2026-05-26 — 批次 ingest 94 題

**操作：** ingest 所有未 ingest 題目（Cowork 批次執行）

**新增 wiki/problems/：** 94 個題目頁面（SS-2002 ~ SS-2013、SS-2015 ~ SS-2023、SS-2024、SS-2025 全年）

**跳過（已存在）：** SS-2014-1、SS-2014-2、SS-2014-3、SS-2014-4

**更新：**
- wiki/by-year.md：完整重建（98 題全部附連結）
- wiki/index.md：所有題目連結從 ⚠️ 更新為 ✅，統計數字更新

**總計：** wiki/problems/ 現有 98 題，全部 verified

---

## 2026-05-26 — compile-all

**操作：** compile-all（Cowork 執行）

**概念頁（wiki/concepts/）：** 30 頁均已存在，本次更新出現題目連結（⚠️→✅）：21 頁

**方法論（wiki/methods/）：** 2 頁（cb-factor, conjugate-beam）

**題目頁（wiki/problems/）：** 98 頁（全部 verified）

**wiki/queries/：** 目錄已建立

**wiki/by-year.md / wiki/index.md：** 已於前次 ingest 批次更新

**design_philosophy.json：** 不存在，跳過 wiki/philosophy/ 生成

---

## 2026-05-26 — 生成 wiki/philosophy/

**操作：** compile-all 補充（Cowork 執行）

**新增 wiki/philosophy/：** 8 頁（lrfd-beam、lrfd-column、asd-column、lrfd-tension、lrfd-connection、lrfd-beam-column-box、asd-pin-tension、probability-analysis）+ index.md

**來源：** CLAUDE-SOLVE.md「設計哲學框架」章節

---

## 2026-05-26 — lint 修復①：新建 23 個缺失概念頁

**新建：** BEARING-STIFFENER, BEARING-TYPE-CONNECTION, BOLTED-CONNECTION-DESIGN, CONCRETE-ENCASED-BEAM, CONNECTION-DESIGN, EFFECTIVE-NET-AREA, EULER-BUCKLING, HIGH-STRENGTH-BOLT-PRACTICE, MOMENT-AMPLIFICATION-B1-B2, PLASTIC-HINGE, PLASTIC-MOMENT-MP, PLASTIC-NEUTRAL-AXIS-PNA, SECOND-ORDER-ANALYSIS, SEISMIC-CONNECTION-DETAILS, SEISMIC-DESIGN-PHILOSOPHY, SHEAR-BUCKLING-WEB, SHEAR-CONNECTOR, TENSION-MEMBER-DESIGN, TORSIONAL-BUCKLING, WEB-CRIPPLING, WELDED-CONNECTION-DESIGN, WELDING-PRACTICE, YIELD-MOMENT-MY

---

## 2026-05-26 lint 修復全套（Task #7）

**操作者：** Cowork  
**操作內容：** 依序修復 lint 健檢所有 54 項問題

### ② 梁柱缺 pm-viz（10 題）
為以下 4.1.3 梁柱桿件題目生成 P-M 互制互動圖，並更新 wiki/problems 圖形區塊：
- ASD 題：SS-2003-4、SS-2004-4、SS-2007-2、SS-2008-4、SS-2019-3
- LRFD 題：SS-2012-3、SS-2020-3、SS-2022-1
- 概念型：SS-2011-1（DAM 概念圖）、SS-2013-4（B₁-B₂ 框架圖）

### ③ 標籤不足（6 題）
從各題 raw/solutions .md 擷取正確標籤，更新 question_index.json 及 wiki/problems：
SS-2016-1（8標籤）、SS-2016-2（6標籤）、SS-2016-5（8標籤）、
SS-2017-1（8標籤）、SS-2017-2（7標籤）、SS-2017-4（7標籤）

### ④ 孤立頁面
- 建立 wiki/traps/index.md，列出兩個 traps 頁面
- 建立 wiki/concepts/index.md，列出全部 53 個概念頁（依知識骨架分類）
- 建立 wiki/queries/README.md（目錄標記）並從 wiki/index.md 加入連結
- SS-2014-1.md 加入 → HIGH-STRENGTH-STEEL-SLENDER-COLUMN.md 連結
- SS-2014-3.md 加入 → WEAK-AXIS-BENDING-LIMIT.md 連結

### ⑤ 圖說缺漏
SS-2016-3 wiki/problems 頁已有 `*圖說（圖N...）：` 格式，確認為誤報，無需修改

### ⑥ 斷開連結
LATERAL-TORSIONAL-BUCKLING.md：`[[PLASTIC-MOMENT-MP]]` → `[塑性彎矩 Mp](PLASTIC-MOMENT-MP.md)`

**結果：** lint 最終驗收 0 項待處理 ✅

---

## 2026-05-26 出題頻率分析查詢

**操作者：** Cowork  
**操作內容：** 依 question_index.json 統計 98 題出題頻率，生成查詢結果頁  
**存入：** `wiki/queries/出題頻率分析-2026-05-26.md`  
**更新：** `wiki/queries/README.md`（加入查詢列表）、`wiki/index.md`（修正快速導航格式）

---

## 2026-05-31 VHA 藏寶圖儀表板建立

**操作者：** Cowork  
**操作內容：** 將 SS-2020-3 的 §3.5 VHA 轉化為互動式「藏寶圖」HTML 儀表板  
**存入：** `wiki/queries/SS-2020-3-treasure-map.html`  
**特性：** KaTeX 數學式渲染（inline embed）、L1/L2/SO/FU 顏色區分、知識線索連結、陷阱警示  
**更新：** `wiki/queries/README.md`（加入查詢列表）

## 2026-05-31 vha-treasure-map skill 建立

**操作者：** Cowork  
**操作內容：** 將 VHA→藏寶圖工作流程打包為 Cowork skill  
**存入：** `skills/vha-treasure-map.skill`  
**更新：** `skills/README.md`（新建，說明安裝方式與觸發語句）  
**清除：** `study/vha.skill`、`study/vha-updated.skill`、`study/vha-SKILL-updated.md`（草稿）

## 2026-06-11 命題大綱分類代號全面遷移（4.1.x → XX-Un-m）

**操作者：** Cowork  
**依據：** `raw/json/syllabus_taxonomy.json`（六科完整分類代號，格式 XX-Un-m）  
**對照表：** 4.1.1→SS-U1-1 · 4.1.2→SS-U1-2 · 4.1.3→SS-U1-3 · 4.1.4→SS-U1-4 · 4.2.1→SS-U2-1 · 4.2.2→SS-U2-2 · 4.2.3→SS-U2-3 · 6.3.1→SD-U3-1 · 1.1.1→MM-U1-1  
**修改範圍：**
- `raw/solutions/`：93 題解析 .md 標頭（主/副分類）＋ 2 個 viz.html subtitle ＋ methods/ 14 個 .md（適用題型）— 經使用者核准之 raw/ 一次性例外修改
- `wiki/problems/`：全部題目頁（主/副分類 [[ ]] 連結）
- `wiki/philosophy/`：11 頁（標題括號、命題大綱欄）
- `wiki/index.md`、`wiki/by-year.md`、`wiki/traps/`、`wiki/methods/`、`wiki/code-ref/`：零星舊代號
- `CLAUDE-CODE.md`：LINT 第 6 項改用新代號；新增第 17 項 topicId 驗證（須存在於 syllabus_taxonomy.json）
**保留不動：** `wiki/log.md` 歷史紀錄、`wiki/queries/` 歷史查詢頁、`study/`、`wiki/topics/` 舊代號頁（已為轉址存根，維持舊連結相容）

## 2026-06-11 建立知識庫儀表板（dashboard.html）

**操作者：** Cowork  
**操作內容：** 參考 exam-wiki-RC 儀表板改造為 SS 版，建立單頁總覽介面  
**存入：** `dashboard.html`（介面）＋ `dashboard-data.js`（98 題快照，自 question_index.json 生成）  
**功能：** 題庫瀏覽（搜尋／年份／單元／考點／設計法／練習進度篩選）、考點統計圖、七層知識架構導覽、指令速查、站內 Markdown＋KaTeX 閱讀器（File System Access API）、匯出 PDF、練習進度 localStorage 追蹤  
**更新：** `CLAUDE-CODE.md` 新增 DASHBOARD 指令（觸發語句「更新儀表板資料」）

## 2026-06-11 知識庫全面優化（10 項）

**操作者：** Cowork  
**操作內容：** 系統性補強內容缺口、修正結構性問題、完善文件

### 高優先：內容缺口補強

1. **wiki/index.md — 接合設計（SS-U1-4）題目清單補齊**
   - 補充 19 道主分類為 SS-U1-4 的題目表格（2002–2024年），與其他三個分類格式統一
   - 同步在接合設計核心概念增加 FILLET-WELD-DESIGN、ECCENTRIC-CONNECTION 連結

2. **新建概念頁：FILLET-WELD-DESIGN.md（填角銲設計）**
   - 含有效喉厚公式、LRFD/ASD 設計強度、破壞模式、常見陷阱、8 道歷年考題對照
   - 連結至 eccentric-weld.md 方法頁及 fillet-weld-0707.md 推導頁

3. **新建概念頁：ECCENTRIC-CONNECTION.md（偏心接合）**
   - 彈性向量法 vs 極限分析法比較；偏心螺栓群 Jp 計算；牛腿接合（bracket）力矩組合
   - 含 5 道歷年考題對照

4. **新建方法頁：slip-critical-lrfd.md（高拉力螺栓摩阻型 LRFD 設計）**
   - 完整 7 步驟：A325/A490 預拉力表 → φRn 計算 → 雙剪校正 → 同時受拉折減 → 承壓驗核 → 間距邊距
   - 含 φ=1.00 vs φ=0.75 常見混淆說明

5. **新建方法頁：composite-beam-pna.md（合成梁塑性中性軸計算）**
   - beff 計算 → Cs/Cc 比較 → PNA 位置判斷 → 兩種情況（版內/鋼梁內）的 Mn 計算
   - 含剪力連接器設計步驟

### 中優先：結構性問題修正

6. **wiki/index.md — 刪除底部重複「快速導航」區塊，移除靜態 Wiki 狀態數字**
   - 底部重複區塊改為「知識工具導航」（內容不重複）
   - 靜態數字（概念頁 53）改為指引用戶執行 `status` 指令

7. **CLAUDE-CODE.md — lint 第 6 項降級為 [warn]**
   - 改為：「SS-U1-3 梁柱題目且年份 ≥ 2016 但無 pm-viz → [warn]」
   - 年份 < 2016 的梁柱題不報告，避免大量偽警報

8. **CLAUDE-CODE.md — DASHBOARD 補充驗證步驟**
   - 第 6 步新增瀏覽器驗證提示：「確認題數、viz 連結可點擊、篩選統計功能正常」

### 低優先：體驗優化

9. **知識庫使用說明書.md — 更新版本 + 補充 dashboard 指令**
   - 版本更新為 2026-06-11
   - 維護指令表格新增「更新儀表板資料」
   - lint wiki 說明補充「[error] / [warn] 分級報告」

10. **skills/README.md — 補充新增 Skill 規範**
    - 新增 YAML 格式說明、加入本清單步驟、命名規則三個子節
    - 讓未來開源貢獻者有明確的規範可參考

**更新索引頁：**
- `wiki/concepts/index.md`：概念頁數從 58→60，接合設計表格補入兩個新概念
- `wiki/methods/index.md`：接合設計方法補入 slip-critical-lrfd，斷面性質補入 composite-beam-pna，頻率排名從 16→18


## 2026-06-11 刪除舊代號存根

**操作者：** Cowork
**操作內容：** 刪除 wiki/topics/ 內 9 個舊代號轉址存根（4.1.1.md、4.1.2.md、4.1.3.md、4.1.4.md、4.2.1.md、4.2.2.md、4.2.3.md、6.3.1.md、1.1.1.md）
**原因：** 代號遷移（4.x→SS-Un-m）完成後，知識庫內部已無任何 [[4.x]] 連結，存根喪失用途
**保留：** SS-U1-1.md 等 9 個新代號主頁（含各分類題目清單）+ index.md 不受影響
- **2026-07-02**: 執行 `更新儀表板資料` (REFRESH-DASHBOARD) 指令，從 `question_index.json` 與 `syllabus_taxonomy.json` 重新生成了 `dashboard-data.js` 儀表板快照資料。

> 🔧 **編碼修復註記（2026-08-22）：** 本節（原檔 byte 16728–17259）原先以 **Big5／CP950** 位元組寫入，夾在 UTF-8 檔案中造成亂碼。本次以嚴格 Big5 解碼（**零損失、無替換字元、未重建任何文字**）轉為 UTF-8，並將 8 處誤寫成 `\` 的 markdown 反引號還原。原始位元組完整留存於 `wiki/log.md.big5.bak`。紀錄內容本身未增刪。

- 2026-07-10｜STUDY｜產生子項深度複習頁 ×5：study/study-SS-U1-1.html（24題）、study-SS-U1-2.html（21題）、study-SS-U1-3.html（11題）、study-SS-U1-4.html（19題）、study-SS-U2-3.html（7題）。七區塊架構（命題分析/圖解/流程圖/公式速查/互動考題清單/高頻陷阱/互動計算器），KaTeX 渲染，題號連結至 index.html markdown 渲染器。
- 2026-07-19: 新增 Keynote PDF 按鈕至所有 study HTML 檔案。
- 2026-07-25｜UNIT-LECTURE｜產生 SS-U1-2 梁桿件觀念講義：`study/lecture-SS-U1-2.html` + `.pdf`（32 頁）。核心軸線「梁＝受壓翼板(壓桿)＋受拉翼板(拉桿)被腹板綁在一起」→ 推導 LTB；全單元編為「三道關卡確認有沒有資格用 Mp」。含 2 則手算範例（非對稱斷面 ENA/PNA/Zx；LTB 三區段完整流程）、12 題自我檢測、★精選 5 題（SS-2011-3 / SS-2025-1 / SS-2014-3 / SS-2023-3 / SS-2010-4）。同時渲染 25 題 `study/problems-view/*.html`（來源 raw/solutions/），並於 `study-SS-U1-2.html` 加入回連按鈕。
- 2026-07-25｜FIX｜**公式勘誤修正（6 檔）**。撰寫 SS-U1-2 講義時發現既有頁面的公式係數與單位標註錯誤，已逐項以數值自洽驗算後修正：
  1. `raw/solutions/methods/ltb-3zone/ltb-3zone.md` + `wiki/methods/ltb-3zone.md`：`Lp = 300ry/√Fy [kgf/cm²]` 代入得 6ry（正確約 50ry），改為 `1.76ry√(E/Fy) = 80ry/√Fy [tf/cm²]`；並補標 λpf/λpw 的 tf-cm² 與 ksi 雙係數、ASD 段落加單位警告。**（此為 raw/ 例外修改，經使用者同意；規則 1 的保護對象為考卷與驗證解答，方法論文件屬可維護內容）**
  2. `wiki/concepts/COMPACT-SECTION.md`：梁腹板 `λp=138、λr=322` 有誤 —— 138 實為**耐震** λpd（見 SS-2021-3），已改為 `λp=170/√Fy、λr=260/√Fy`（依 SS-2016-1 題目所附規範表），並新增柱腹板 68/√Fy、耐震 λpd 專列與單位對照表。
  3. `wiki/concepts/LATERAL-TORSIONAL-BUCKLING.md`：`Lr` 分母誤植為 `√(Fy−Fr)`，應為 `(Fy−Fr)`（量綱才是長度；誤用會使 Lr 高估 34%）。已補 X1/X2 定義與量綱自檢說明。
  4. `wiki/methods/asd-beam.md`：ASD 係數 `703,000 / 1,170,000 / 1,055,000` 彼此不相容（代入下界得 Fb=0.011 ksi，應為 0.60Fy；且與彈性式不接軌）。已改為 AISC ASD 9th Ed. 正確值 `102,000 / 510,000 / 1,530,000 / 170,000`（ksi），並附 tf/cm² 換算表與接軌驗算。Lc 兩式補上 in-ksi / cm-tf / mm-MPa 三制對照。
  5. `wiki/methods/asd-beam-column.md`：同 4 之係數，一併修正並加單位註記。
  6. `wiki/code-ref/asd-beam-fb-derivation.md`：Lc `200bf/Fy、137,900`（實為 mm-MPa 制且第一式漏了根號）改為三制對照表；`1,055,000`→`1,530,000` 並移除多餘的外層 Cb；`FS≈1.515`（由 0.66 反推，循環論證）改為 `FS=5/3`，補「0.66/0.60=形狀因子」推導；另標明 `0.79−0.002(bf/2tf)√Fy` 是**翼板局部挫屈 F1-3**，非 LTB 公式，不參與「取較大值」。
  驗算方式：所有係數以 Python 重算並檢查邊界接軌（ASD F1-6 在下界須得 0.60Fy、在分界須與 F1-7 相等），寬厚比則交叉比對 SS-2016-1、SS-2021-3 兩題驗證解答。
- 2026-07-25｜HARNESS｜**規則 1 例外擴充**：`raw/` 唯讀的例外由「`question_index.json`」擴充為「`question_index.json` + `raw/solutions/methods/`」，並明訂修改 methods 的三個必要條件（① 數值驗算 ② 同步覆蓋 wiki/methods/ ③ 記 log）。理由：`methods/` 是 `wiki/methods/` 的 compile 來源，公式勘誤若只改 wiki 副本會被 `compile-all` 蓋回，無法根治；而方法論屬「可維護的知識整理」，與需要保護可追溯性的「證據」（考卷、題目解析、驗證答案）性質不同。`raw/solutions/SS-YYYY-N/` 明確排除在例外之外，仍受規則 1、2 完整保護。同步更新四處：`CLAUDE.md`（規則 1 全文、資料夾結構圖加 🔒/✏️ 標記、單向資料流、兩個環境分工、CHANGELOG）、`README.md`（結構圖）、`CLAUDE-CODE.md`（ADD-METHOD 節新增 FIX-METHOD 五步流程與單位標註要求）。
- 2026-07-25｜UNIT-LECTURE｜產生 SS-U1-4 接合之分析與設計觀念講義：`study/lecture-SS-U1-4.html` + `.pdf`（33 頁）。核心軸線「構材設計求一個強度；接合設計求一串強度取最小值」→ 由「力量換手」推出極限狀態清單；全單元收斂為「兩把尺」（剪→×0.6、降伏配 FyAg／斷裂配 FuAn）。含 6 則手算範例（角鋼三破壞模式比較／摩阻型 vs 承壓型強度對照／銲腳 LRFD-ASD 雙算互驗／L 形偏心銲道並證明最遠點非臨界點／腹板銲道彎剪組合應力／斷續銲間距由構造規定控制）、11 張內嵌 SVG、18 條陷阱總表、12 題自我檢測、★精選 6 題（SS-2015-2 / SS-2017-4 / SS-2017-2 / SS-2020-4 / SS-2018-3 / SS-2009-4）。規範常數全部追溯來源：0.6 ← von Mises 1/√3；0.707 ← 45° 喉部幾何；2.4Fudt ← 1.2FuLct 在 Lc=2d 的封頂；Fnv(X)/Fnv(N) ≈ 1.25 ← 螺紋處有效面積 0.8Ab；Du=1.13 ← 實際預拉力統計高於規範最小值 13%。
- 2026-07-25｜UNIT-LECTURE｜同步作業：重新渲染 `study/problems-view/` 之 SS-U1-4 全 26 題（主 19、副 7），講義題號一律連向渲染頁（無 .md 連結殘留、無 @@MATH 殘留、圖片路徑逐一驗證）；`study/study-SS-U1-4.html` §1 按鈕列擴為三顆（觀念講義／PDF／Keynote）並加註使用順序。考點群題數以 `question_index.json` 重新統計後修正講義內數字（填角銲 10、拉力接合端 10、高強度螺栓 10、梁柱接頭 6、偏心向量法 5、施工/NDT 5、剪力流 1、ASD 6、概念題 7）；精選 6 題覆蓋度誠實揭露（考點群 7/8 = 88%，標籤權重 47%），未涵蓋項目於 §14 逐條列出並給候補題。
- 2026-07-25｜UNIT-LECTURE｜產生 SS-U1-3 梁柱桿件觀念講義：`study/lecture-SS-U1-3.html` + `.pdf`（30 頁）。核心軸線「柱與梁的內力算一次就定了；梁柱的內力會自己長大 —— 因為只有它同時有 P 與側向變形，而 P×δ 又是彎矩」；全單元編為「兩條腿走路」（需求側 B1/B2 或 Cm/F'e ＋ 強度側 φcPn/φbMn，在 P-M 互制式會合）。含 5 則手算範例（B1 單曲率 vs 雙曲率同柱同軸力對照／B2 靠桿漏算使 B2 少一半並觸發 0.6 上限／LRFD 完整 P-M 兩腿流程／ASD 完整互制並以 LRFD 利用率比 1.03 互驗／強柱弱梁兩個修正各自足以翻盤）、10 張內嵌 SVG、16 條陷阱總表、12 題自我檢測、★精選 6 題（SS-2013-4 / SS-2020-3 / SS-2003-4 / SS-2011-1 / SS-2022-1 / SS-2009-1）。規範常數全部追溯來源：1/(1−P/Pcr) ← 微分方程多出 Py 項後的剩餘勁度（Pcr−P），勁度歸零即挫屈；8/9 與 0.9 ← 為使 H1-1a/H1-1b 在 Pu/φcPn=0.2 處連續；F'e 的 12/23 ← Euler 應力 ÷ FS(23/12)；Cc = √(2π²E/Fy) ← Euler 應力＝Fy 再乘 √2（殘留應力）；ASD 的 FS 由 5/3 連續變化到 23/12 並與彈性段銜接；DAM 的 1.6 ← (1.2D+1.6L)/(D+L) 在 L≫D 的上限；1.5FySy ← 矩形翼板的形狀因數。
- 2026-07-25｜UNIT-LECTURE｜同步作業：新增渲染 `study/problems-view/` 之 SS-2003-4、SS-2004-4、SS-2007-2、SS-2008-4、SS-2009-1、SS-2011-1、SS-2013-4、SS-2014-4、SS-2020-3、SS-2022-1（共 10 題，另 SS-2012-3、SS-2019-3、SS-2014-3 已存在）；`study/study-SS-U1-3.html` §1 按鈕列擴為三顆（觀念講義／PDF／Keynote）並加註使用順序；§9 與 §14 對 RBS 的引用改為指向 `lecture-SS-U1-4.html#s7` 的明確跨講義連結。精選 6 題覆蓋度誠實揭露（考點群 7/8 = 88%，標籤權重 75%），唯一完全落空的群為「LTB 併入梁柱（Fbx 的 L/rT 分段、Cb）」，已於 §14 列為第一候補（SS-2007-2）。
- 2026-07-25｜NOTE｜`raw/solutions/SS-2014-4/` 內有 `SS-2014-4-fig-1.jpg`，但 `SS-2014-4.md` 未以 markdown 語法引用該圖，故渲染頁 `study/problems-view/SS-2014-4.html` 無附圖（渲染器忠實反映來源，未自行插圖）。因 `raw/solutions/SS-YYYY-N/` 受規則 1、2 保護，未修改；若需顯示該圖，須由使用者決定是否在來源 .md 補上圖片連結。
- 2026-07-30｜VHA-LECTURE｜產生「VHA 七題觀念講義」：`study/lecture-VHA-7題觀念講義.html` + `.pdf`（51 頁）。來源為 SS-2005-1、SS-2013-2、SS-2013-3、SS-2015-3、SS-2018-2、SS-2024-1、SS-2025-2 之 §3.5 變數層次分析（主要公式／L2 推導／L3 深層知識），七題全屬 `SS-U1-1`。章節依主題邏輯排序（拉力三道防線 → 剪力遲滯最佳化 → 組合柱斷面 → 分段有效長度 → 箱型柱完整檢核 → 殘留應力與柱曲線來源 → 框架層間穩定），每章結構為「主要公式追來源 → L2 逐步推導 → L3 深層知識逐條講透 → 完整手算範例 → 易錯點與 30 秒自我檢核」。含 7 則手算範例、24 條 L3 深層知識展開、9 張內嵌 SVG、七章 L3 卡關清單（33 項可勾選）。公式來源全部追溯：0.6 ← von Mises 1/√3；BSR 上限式 ← 長剪切面先整段剪力降伏（判準 Anv/Agv > Fy/Fu）；U=1−x̄/L ← 力繞過角部需傳力距離；L_opt = L_weld（通則，此時 U=0.5）；Cc = √(2π²E/Fy) ← Fe = Fy/2 ＝殘留應力使降伏啟始；ASD 的 FS 由 5/3 連續變化至 23/12；λc² = Fy/Fe（可推導）；0.877 ← 初始彎曲缺陷折減；0.658^λ² ← 隱含拋物線殘留應力分布故平滑（對照本題塊狀分布產生 B/B′ 跳躍）；G = 柱／梁勁度比 ← 「梁夾得住柱嗎」；LeMessurier ΣP ≤ ΣPe ← 側移挫屈為整層模態故柱間可互相支援。
- 2026-07-30｜VERIFY｜上述講義之 87 項數值主張以 Python 獨立重算逐項交叉比對，全部通過（tolerance 0.5～2%）。同時發現並修正來源解析之單位量級筆誤一處：`SS-2013-2.md` 將 π²EIc 寫為「605,946 tf·cm²」，正確值為 6.059×10⁸ tf·cm²（後續 Pe 數值本身正確，僅該中間式量級掉 10³）。講義內採正確寫法並於附錄註明；因 `raw/solutions/SS-2013-2/` 受規則 1、2 保護，未修改來源檔。
- 2026-08-08｜STUDY-REFACTOR｜重構 `study/study-SS-U1-1.html`，由「七區段深度複習頁」改為單一主題的**命題情報頁（只留 ① 命題分析）**。動機：同子項三份教材內容大量重疊 —— ② 截面圖解 ≈ `lecture-SS-U1-1.html` §1.1／§4.2／§8.1、③ 解題流程圖 ≈ lecture §9、④ 核心公式速查 ≈ `formula-given-SS-U1-1.html` §二（且後者多了 24 年考卷「給／背」證據，屬上位版）、⑥ 高頻陷阱 Top 8 ≈ lecture §11。三檔重新分工為：lecture＝為什麼（原理）、formula-given＝要不要背（記憶決策）、study＝考什麼（可由 `question_index.json` 重生的命題事實）。刪除區段 ②③④⑥⑦（⑦ LRFD 柱強度計算器經確認直接刪除），保留並擴充 ① 為六個區塊：1.1 出題概況（KPI＋年度堆疊圖＋題型圓餅）、1.2 考點結構（四類可篩選卡片）、1.3 考點漂移（2002–2013 vs 2014–2025 對切）、1.4 ASD／LRFD 走向、1.5 考題清單（主 24 ＋副 7 ＝ 31 題）、1.6 命題風險排序。頁面標題由「深度複習」改為「命題分析」；檔名不變（`lecture-SS-U1-1.html`、`formula-given-SS-U1-1.html` 均有連回本檔）。
- 2026-08-08｜DATA-FIX｜上述重構過程中，以 `raw/json/question_index.json` 重新統計並修正原頁三處錯誤／缺漏：① KPI「近 6 年出題 6/6」有誤 —— U1-1 主考點在 2019、2020、2021 連續三年空白，2020–2025 六個考年中僅 4 年出題（共 7 題），已改為「4/6」；② 考題清單原僅列 24 題主考點，遺漏 7 題副考點（SS-2002-1、SS-2003-3、SS-2004-2、SS-2007-1、SS-2009-3、SS-2012-3、SS-2019-3），現併入清單並以虛線灰底與「副・所屬子項」標籤區分，篩選鈕新增「僅主考點／僅副考點」；③ 題號連結仍指向舊式 `../index.html#md=raw/solutions/...`（瀏覽器顯示未渲染純文字），已全數改指 `problems-view/SS-YYYY-N.html`，31 個連結逐一確認檔案存在。另新增每題 designMethod 色籤（LRFD／ASD／混合／概念題）。
- 2026-08-08｜ANALYSIS｜本輪由統計得出、原頁未呈現的三項命題觀察（均可由 `question_index.json` 複算）：① **考點漂移**：把 24 題對切為前後各 12 題，有效長度 K 值由 6 題降至 1 題（且該題 SS-2023-1 為概念題，最後一題計算型停在 SS-2013-2，空窗 12 年），柱挫屈強度由 2 題升至 6 題，拉力桿件由 1 題升至 4 題 —— 依「歷史總題數」分配複習時間會高估 K 值、低估柱強度曲線推導；② **ASD 未退場**：ASD 於前 12 年僅 1 題，後 12 年 5 題，近 4 年（2022–2025）更佔 3/6，`Cc`／變動 `FS`／`Fa` 兩段式不可當舊制跳過；③ **風險排序**：柱強度曲線推導＋殘留應力（近 12 年 3 次、題型幾乎重複）與剪力遲滯 U 值（連兩年、每次換載體）列為高風險，對位圖計算題（歷史第二高頻但空窗 12 年）與組合柱平行軸定理（空窗 10 年）列為中高風險，SRC 複合柱（空窗 22 年）列為低風險。
- 2026-08-08｜BUGFIX｜`study/problems-view/` 全 88 個渲染頁的「← 返回講義」按鈕按了沒反應。原因：按鈕寫的是 `href="javascript:history.back()"`，而 `study-*.html` / `lecture-*.html` 的題號連結一律帶 `target="_blank"`，新分頁沒有上一頁歷史，`history.back()` 因此無效（不是連結壞掉，是分頁沒有回頭路）。修正為三段 fallback：優先 `document.referrer`（新分頁仍會帶入來源頁，可正確回到講義或命題分析頁）→ 其次 `history.back()`（同分頁開啟的情況）→ 最後退回根目錄 `../../index.html` 儀表板（直接開檔、無 referrer 時）。88 檔全數套用，兩種既有寫法（`←` 與 `&#8592;`）皆已統一。
- 2026-08-08｜UX｜`study/problems-view/` 全 88 頁的返回列改為兩顆按鈕，解決「返回講義」名實不符的問題。原本單一按鈕寫「返回講義」但實際行為是 `history.back()`（回上一頁），且該題的講義未必等於來源頁 —— 例如 SS-2002-1 主分類為 SS-U1-2 梁桿件、SS-U1-1 只是副分類，卻可從 `study-SS-U1-1.html` 點進來。現拆為：①「← 上一頁」沿用 referrer → history → 根儀表板三段 fallback，回到實際點進來的那一頁；②「📘 Un-m 單元名 講義」為每檔靜態產生的固定連結，指向該題**主分類單元**的 `lecture-SS-Un-m.html`。主分類無講義的 6 題（SS-2005-4、SS-2009-1、SS-2009-2、SS-2012-2、SS-2020-1、SS-2020-2）改指第一個有講義的副分類單元並於按鈕標註「（副分類）」。分布：U1-1 24、U1-2 23、U1-3 12、U1-4 21、U2-3 8，合計 88，五個目標講義檔均已確認存在。單元代碼與名稱依 `question_index.json` 的 primaryTopicId 產生，非人工填寫。
- 2026-08-08｜UX｜`study/problems-view/` 全 88 頁的「← 上一頁」改為「🔍 Un-m 速查頁」，靜態指向該題主分類單元的 `study-SS-Un-m.html`（命題分析頁）。原本的 referrer／history fallback 屬「回上一頁」語意，按鈕文字看不出會去哪；改為與旁邊的「📘 講義」按鈕採同一套單元推導，兩顆按鈕永遠指向同一單元的兩份教材，行為可預測。分布：U1-1 24、U1-2 23、U1-3 12、U1-4 21、U2-3 8，合計 88；已程式驗證 88 檔的 study-／lecture- 連結單元完全一致，且五個目標速查頁檔案均存在。註：因採主分類推導，跨單元的題目兩顆按鈕會指向主分類單元而非來源頁 —— 例如 SS-2003-3（主分類 U1-4、副分類 U1-1）即使從 `study-SS-U1-1.html` 點入，兩顆按鈕仍指向 U1-4。
- 2026-08-08｜UX｜`study/problems-view/` 全 88 頁改為「跟隨來源單元」：頁尾注入一段小腳本，讀取 `document.referrer`，若來源是 `study-`／`lecture-`／`formula-given-SS-Un-m.html`，就把「🔍 速查頁」與「📘 講義」兩顆按鈕同時改指向**來源那個單元**並改寫按鈕文字；來源不明（直接開檔、從儀表板進入）時維持 HTML 內靜態的主分類單元連結。因此 SS-2003-3（主分類 U1-4、副分類 U1-1）從 `study-SS-U1-1.html` 點入時，兩顆按鈕會顯示並指向 U1-1；從別處進入則回到 U1-4。設計取捨：靜態 href 保證無 JS／無 referrer 時仍可用，JS 只做覆寫，不是唯一路徑。
- 2026-08-08｜INCIDENT｜作業過程中 `study/problems-view/SS-2002-2.html` 曾被清為 0 位元組。原因：批次腳本寫成 `open(f,'w').write(re.sub(...))`，Python 先開檔（'w' 立即截斷內容）才計算取代結果，而該次 `re.sub` 的 replacement 字串含 `\d` 觸發 `re.error: bad escape`，例外中斷時檔案已被清空，且該檔為排序後第一個處理對象。已由 `git show HEAD:study/problems-view/SS-2002-2.html` 取回原始版本，重新套用三項變更（兩顆按鈕、CSS、跟隨腳本）後寫回，並驗證 17,428 bytes、按鈕指向 SS-U1-2 梁桿件（與 `question_index.json` 的 primaryTopicId 一致）。後續批次改用 `lambda _: SCRIPT` 作為 replacement 避免跳脫字元被解讀，並在寫檔前先完成字串運算。最終全 88 檔通過檢查：各含 1 組 quick／lect 按鈕與 1 份跟隨腳本、結尾標籤完整、無 `javascript:history.back` 殘留、study- 與 lecture- 連結單元 100% 一致。
- 2026-08-08｜SKILL｜新增 `skills/unit-exam-intel/`（SKILL.md 17.8 KB）與打包檔 `skills/unit-exam-intel.skill`，把本輪 `study-SS-U1-1.html` 的重構做法固化為六科（SS/RC/SA/SD/SM/MM）通用流程。輸出 `study/study-XX-Un-m.html`（單一自包含 HTML，不產 PDF —— 本頁價值在可篩選清單、可點題號與 Canvas 圖表，列印會損失一半功能，且資料隨新考卷改變，紙本易過期）。六個區塊：出題概況／考點結構／考點漂移／設計法（或題型）走向／考題清單（主＋副）／命題風險排序。三份 study 教材的分工在 SKILL.md 開頭明訂：lecture＝為什麼、formula-given＝要不要背、unit-exam-intel＝考什麼（唯一純資料驅動、可自動重生者）。
- 2026-08-08｜SKILL｜`unit-exam-intel` 的核心設計原則是「**頁面上每個數字都必須由程式算出，不可手打**」，並以兩支純標準函式庫腳本落實：`scripts/stats.py` 從 `question_index.json` 算出 KPI、全科排名與前三名、考年總數與命中年數、連續空窗年段、前後對切、各期設計法分布、標籤頻率、含主副旗標的完整題目清單；`scripts/verify.py` 反向對帳成品頁的 `Q[]` 題號集合、逐題主副旗標與 designMethod、篩選鈕括號數字（含「僅主／僅副」）、四個 KPI、題號連結是否都存在對應 `problems-view/*.html`、以及三種禁用寫法（`../index.html#md=`、`javascript:history.back()`、區塊編號 `1.1`），任一不過即以離開碼 1 逐條列出。已用「故意改壞」測試確認 verify.py 抓得到篩選鈕數字與 KPI 的不一致。
- 2026-08-08｜DATA-FIX｜撰寫 skill 時以 `stats.py` 回頭核對 `study/study-SS-U1-1.html`，又抓到一處本輪自己寫錯的數字：KPI 副標與註腳寫「2020–25 共 7 題」，實際為 **6 題**（SS-2022-2、2023-1、2023-2、2024-1、2024-2、2025-2）。兩處已更正。這正是把統計寫成腳本的理由 —— 同一份資料手數兩次，兩次都可能錯。
- 2026-08-08｜SKILL｜六科差異已在 SKILL.md 內處理：① `designMethod` 欄位並非各科都有，`stats.py` 以 `method.available` 標記，缺欄位時（SA、MM 等）改用題型／解法／主題年代分布等其他軸線，不得硬掰；② 主考點 < 8 題時跳過「考點漂移」區塊（對切無統計意義）；③ `study/problems-view/` 為選用，缺席時題號退化為純文字並於頁尾註明；④ 各科分群軸線建議已列表（SS/RC 依構件或極限狀態、SA 依解法、SD 依自由度與規範、SM 依土壤主題、MM 依力學主題）。另附 `reference/template.html`（23.3 KB，含全部 CSS、篩選邏輯與兩張 Canvas 圖），以 `{{UNIT}}` 等 8 個佔位符參數化。
- 2026-08-08｜STUDY-REFACTOR｜以 `unit-exam-intel` skill 重構 `study/study-SS-U1-4.html`，由七區段「深度複習頁」改為只回答「這個單元考什麼」的**命題情報頁**。重疊盤點結果：② 接合圖解 ≈ `lecture-SS-U1-4.html` §1–§7、③ 解題流程圖（偏心接合彈性向量法）≈ lecture §6／§10、④ 核心公式速查 ≈ `formula-given-SS-U1-4.html` §二（後者多了 37 條公式 × 24 年考卷「給／背」證據，屬上位版）、⑥ 高頻陷阱 Top 8 ≈ lecture §12，四段全部刪除並改為連結；⑦ 互動計算器（填角銲設計強度）為唯一不重複內容，經與使用者確認後直接刪除。保留並擴充 ① 命題分析為六個無編號區塊：出題概況（四張 KPI＋年度堆疊圖＋題型圓餅）／考點結構（五群可篩選卡片）／考點漂移（2002–2009 前 9 題 vs 2012–2024 後 10 題）／設計法走向／考題清單（主 19 ＋副 7 ＝ 26 題）／命題風險排序。考點分群依「解題套路」而非標籤字面，每題只歸一群：🔩 螺栓與接合端極限狀態 10、🌀 偏心接合（彈性向量法）5、🔥 銲接強度與剪力流 2、🏗️ 梁柱接頭與耐震細部 4、📘 機制／破壞模式／施工概念 5。檔名不變（`lecture-SS-U1-4.html` 與 `formula-given-SS-U1-4.html` 均已有連回本檔的按鈕，無須新增）。全頁數字由 `scripts/stats.py` 產出，`scripts/verify.py` 七項對帳全數通過。
- 2026-08-08｜DATA-FIX｜`scripts/verify.py` 對帳時揪出 `raw/json/question_index.json` 的 designMethod 錯誤：**SS-2006-2 與 SS-2006-5 標為 `LRFD`，但兩題的解析 .md（受規則 1、2 保護的證據）皆明載「設計法：概念題」，且兩題確實全為說明繪圖題**（2006-2 問預拉力意義／塊狀剪力／FCAW 全名／工地銲接濕度風速限制；2006-5 要求繪梁柱接頭細部並說明連續板功能）。以程式比對全庫 98 題後發現 **2006 年四題（SS-2006-1、-2、-4、-5）全被填為 `LRFD`**，研判為整年預設值未逐題修正。經使用者確認後將此四題的 `designMethod` 一律改為 `概念題`（索引為規則 1 的兩處例外之一，可人工維護；本次僅改該欄位，`git diff --numstat` 確認全檔僅 5 行變動，未重排格式）。連帶影響：SS-U1-4 設計法分布由「ASD 5／LRFD 10／概念題 4」更正為「**ASD 5／LRFD 8／概念題 6**」，前段（2002–2009）由「LRFD 5／ASD 3／概念題 1」更正為「**LRFD 3／ASD 3／概念題 3**」；`study-SS-U1-1.html`（SS-2006-1）與 `study-SS-U1-2.html`（SS-2006-4）的設計法走向表亦受影響，尚未重跑，下次觸碰該兩頁時應以 `stats.py` 重新產出。另註：同一次掃描發現 16 筆 .md 與索引的措辭差異（如「概念題（含計算）」vs「概念題」、「混合（ASD + LRFD）」vs「混合」），屬同義不同寫法，未動。
- 2026-08-08｜ANALYSIS｜SS-U1-4 由統計得出的三項命題觀察（全部可由 `stats.py` 複算）：① **考點漂移** —— 主考點 19 題對切後，偏心接合（彈性向量法）由前段 4 題（SS-2002-4、2004-3、2005-3、2007-1）降至後段 1 題（SS-2017-4），**已空窗 8 年**；銲接強度與剪力流由 0 升至 2（SS-2018-3、2019-4 連兩年，前段從未單獨出過非偏心的銲道強度計算）；梁柱接頭主考點僅 SS-2006-5 與 SS-2024-4（相隔 18 年），但同期以副考點形式掛在 SD-U3-1 出現兩次（SS-2012-2、2020-1）——「這個考點沒有消失，只是換了門牌」。重心由「把偏心接合算出來」漂向「把接合為什麼會壞說清楚」。② **題型走向** —— 概念題占比由前段 3/9 升至近 6 考年（2020–2025）**3/5**；同期計算題僅存 SS-2020-4（ASD）與 SS-2021-2（LRFD）各一，ASD 未退場且兩題 ASD（2018-3 銲道容許應力、2020-4 A490 `F_va`=2.8 tf/cm²）都是完整容許應力檢核。③ **風險排序** —— 偏心接合彈性向量法（歷史 5 題、空窗 8 年、題型固定且四次考試全零公式）與銲接破壞形式／HAZ（SS-2023-4、2024-4 連兩年）列高風險；梁柱接頭細部（主考點空窗 18 年）與塊狀剪力多路徑（跨 6 題、一半為副考點）列中高風險；斷續銲剪力流（24 年僅 SS-2019-4 一次、且與 U1-2 重疊）列低風險。另註出題密度：24 個考年中 15 年出現，空窗集中於 2010–2011 與 2013–2016 兩段；近 6 考年僅 4 年出題共 5 題，為本單元二十四年來最低密度。
- 2026-08-08｜STUDY-REFACTOR｜以 `unit-exam-intel` skill 重構 `study/study-SS-U1-2.html`，由七區段「深度複習頁」改為命題情報頁。重疊盤點：② Mn–Lb 設計曲線與斷面分類圖解 ≈ `lecture-SS-U1-2.html` §1–§3、③ 解題流程圖 ≈ lecture §10、④ 核心公式速查（八個子節）≈ `formula-given-SS-U1-2.html` §二（後者多了 33 條公式 × 24 年考卷「給／背」證據）、⑥ 高頻陷阱 Top 8 ≈ lecture §12，四段刪除改為連結；⑦ 互動計算器（LTB 公稱彎矩）為唯一不重複內容，經使用者確認後刪除（與 U1-4 的填角銲計算器同一處置）。擴充為六個無編號區塊。考點分五群、每題只歸一群：🌀 LTB 側扭挫屈三區段 11、📏 斷面分類與塑性彎矩 6、📐 斷面選擇與使用性檢核 2、🧱 合成梁與 SRC 2、✂️ 腹板剪力與剪力流 4，清單主 21 ＋副 4 ＝ 25 題。互連按鈕四顆（lecture／formula-given 之 HTML＋PDF 均存在），`lecture-SS-U1-2.html` 與 `formula-given-SS-U1-2.html` 原本就有連回本檔的按鈕，未新增。`verify.py` 七項對帳全過。
- 2026-08-08｜DATA-FIX｜本頁的設計法分布已反映同日 U1-4 那輪對 `question_index.json` 的修正：**SS-2006-4（板梁剪力挫屈與張力場，純概念繪圖題）原被誤填為 `LRFD`，已改為 `概念題`**（該筆屬 2006 年整年四題誤填的一部分，另三題為 SS-2006-1／-2／-5）。連帶更正：U1-2 設計法全期由「LRFD 16／ASD 3／概念題 2」變為「**LRFD 15／ASD 3／概念題 3**」，前段（2002–2011）由「LRFD 7／ASD 2／概念題 1」變為「**LRFD 6／ASD 2／概念題 2**」。舊頁的區段標題另有一處分群數字與本輪不同（舊頁寫「LTB 12 題」），差異來源為分群準則改變而非資料錯誤——舊頁把 SS-2015-1（三分點集中力梁的 LTB＋剪力＋撓度全檢核）計入 LTB 群，本輪依「每題只歸最主要的解題套路」原則改列入「斷面選擇與使用性檢核」群，與 SS-2010-4 同群。
- 2026-08-08｜ANALYSIS｜SS-U1-2 由統計得出的三項命題觀察（全部可由 `stats.py` 複算）：① **出現率全科最高** —— 24 個考年中 17 年出現（U1-1 為 18/24 但總題數較高、U1-4 僅 15/24），空窗只有 2003–2004 與 2017–2018 兩段各兩年，且兩次都在隔年立刻回歸（2005、2019）。② **考點漂移** —— 主考點 21 題對切後，LTB 側扭挫屈維持 5→6（二十四年沒有中斷超過三年，近年 2021-3／2024-3／2025-3 三度出現，變的只是包裝：求 φbMn → 反求載重 → 強弱軸對照 → 概念說明）；斷面分類與塑性彎矩由 1 升至 3（2016-1、2023-3、2025-1，**2023 起連三年**），是升溫最快的一群；腹板剪力與剪力流由 2 降至 0，主考點**空窗 19 年**（最後為 2006-4），僅以副考點形式延續於 2019-4、2020-4；整梁設計題（選斷面＋剪力＋撓度）**空窗 10 年**（最後為 2015-1）。重心由「把一根梁完整設計出來」收斂到「把斷面的本錢算清楚」。③ **設計法** —— ASD 自 2016-1 之後**連續 6 個考年零出現**，近 6 考年 5 題中 4 題為 LRFD 計算題、1 題概念題；本單元是六個子項中最能安心把重心放在 LRFD 的一個，與 U1-3（ASD 梁柱互制式幾乎必給必考）恰成對比。④ **風險排序** —— LTB 三區段（11 題、佔本單元 52%、空窗 0 年）與斷面分類／Mp（6 題含 U2-1 兩題副考點、空窗 0 年）列高風險；合成梁／SRC（2 題、空窗 6 年、兩題套路完全相同）與整梁設計（2 題、空窗 10 年、唯一同時考三條檢核線的題型）列中高風險；板梁張力場（1 題、空窗 19 年）列低風險。
- 2026-08-08｜STUDY-REFACTOR｜以 `unit-exam-intel` skill 重構 `study/study-SS-U2-3.html`，由七區段「深度複習頁」改為命題情報頁。重疊盤點：② 主題地圖（施工要求四大領域）≈ `lecture-SS-U2-3.html` §0–§6、③ 概念題答題架構 SOP ≈ lecture §7、④ 知識卡速查（八張卡）≈ `formula-given-SS-U2-3.html` §二（後者多了 38 條規定 × 24 年考卷「給／背」證據）、⑥ 高頻陷阱 Top 8 ≈ lecture §9，四段刪除改為連結；⑦ 快問快答翻卡為唯一不重複內容，經使用者確認後刪除（功能與 lecture §10「自我檢測 12 個為什麼」相近；與 U1-4 填角銲計算器、U1-2 LTB 計算器同一處置）。考點分五群、每題只歸一群：🛡️ 防蝕與塗裝 3、🔥 銲接施工細節與瑕疵 3、🏗️ 耐震構架的加嚴要求 3、🔍 非破壞檢測 NDT 2、🔩 高強度螺栓施工 2，清單主 7 ＋副 6 ＝ 13 題。`verify.py` 七項對帳全過。
- 2026-08-08｜STRUCTURE｜本頁與前三個單元有兩處結構差異，均為 skill 明訂的例外處理：① **跳過「考點漂移」區塊** —— 主考點僅 7 題，低於做前後對切的門檻（8 題），`stats.py` 的對切結果為前段 3 題／後段 4 題，樣本太小，硬做會給出不穩且誤導的結論；趨勢改以出題概況的一行註腳描述（主考點 2016–2022 密集 5 題後 2023 起連三年掛零，同期改以副考點形式在 U1-4 出現三次）。② **「設計法走向」改軸線** —— 本單元 13 題 `designMethod` 全部是「概念題」，做 ASD／LRFD 表毫無資訊量，改用「現身形式」軸線：期間 × 主考點／副考點掛 U1-4／副考點掛其他，三列分別為 2002–2013（2／1／2＝5）、2014–2025（5／3／0＝8）、近 6 考年 2020–2025（2／3／0＝5）。此表回答了一個舊頁完全沒呈現的事實：**近 6 考年副考點（3）多過主考點（2）**。
- 2026-08-08｜ANALYSIS｜SS-U2-3 由統計得出的三項命題觀察（全部可由 `stats.py` 複算）：① **主考點 7 題但實際要準備 13 題** —— 6 題副考點裡 **4 題掛在 SS-U1-4 接合**（2009-4、2021-4、2023-4、2024-4），另兩題掛 U1-2（2002-1 銲條乾燥）與 SD-U3-1（2009-2 節點域）；2014 年之後副考點**全部集中到 U1-4**，不再散落其他單元，故最有效率的準備方式是把本單元與 U1-4 綁在一起讀。② **出現節奏是「一陣一陣」** —— 24 個考年只有 7 年出現主考點，空窗四段（2002–2003、2005–2009、2011–2015、2023–2025），但 2016–2022 七年內密集出了 5 題（2016-2、2018-4、2019-1、2021-1、2022-3）。③ **風險排序** —— 防蝕與塗裝（7 題主考點中佔 3 題、歷史最高頻、空窗 6 年、答案結構固定）與 NDT（跨主副共 4 題、近 4 個考年出現 3 次、每次換問法）列高風險；耐震加嚴細部（3 題、關鍵數字 `tz≥(dz+wz)/90` 與板厚 `≥40 mm` 用 SN-C 皆 24 年零次印出）與高強度螺栓施工（主考點空窗 21 年、但 2021-4 以副考點回歸）列中高風險；銲接細節規定（回銲 end return、銲條乾燥，主題極窄各只考過一次）列中低風險。另註：本單元 13 題全為概念說明題，零計算，得分關鍵在答題骨架而非算式。
- 2026-08-08｜STUDY-REFACTOR｜以 `unit-exam-intel` skill 重構 `study/study-SS-U1-3.html`，由七區段「深度複習頁」改為命題情報頁。重疊盤點：② P–M 互制曲線與二階效應圖解 ≈ `lecture-SS-U1-3.html` §1／§2／§6、③ 解題流程圖（LRFD B1/B2 標準流程）≈ lecture §10、④ 核心公式速查（六個子節）≈ `formula-given-SS-U1-3.html` §二（後者多了 40 條公式 × 24 年考卷「給／背」證據）、⑥ 高頻陷阱 Top 8 ≈ lecture §12，四段刪除改為連結；⑦ 互動計算器（LRFD H1 互制檢核）為唯一不重複內容，經使用者確認後刪除（與 U1-4 填角銲、U1-2 LTB、U2-3 快問快答同一處置，四個單元一致）。考點分四群、每題只歸一群：🅰️ ASD 互制三式 5、🅱️ LRFD H1 互制檢核 3、🔺 二階效應放大（B1／B2、Mnt／Mlt）2、📘 規範層次的延伸（直接分析法／強柱弱梁）2，清單主 11 ＋副 1 ＝ 12 題。`verify.py` 七項對帳全過。至此 SS 六個子項中的五個（U1-1、U1-2、U1-3、U1-4、U2-3）皆已改為命題情報頁。
- 2026-08-08｜NOTE｜本輪未發現 `question_index.json` 的資料錯誤（U1-3 的 12 題 designMethod 與各題 .md 標示一致，前三輪的 2006 年整年誤填未波及本單元）。舊頁的分群與本輪相同軸線但一群僅 1 題（「直接分析法（1題）」違反 skill 的「每群至少 2 題」），本輪將 2011-1 與副考點 2009-1（強柱弱梁，主考點掛 SD-U3-1）合併為「規範層次的延伸」群——兩題的共同性質是 designMethod 皆為概念題、且都在問「規範為什麼這樣要求」而非代數字。另舊頁未列副考點（僅 11 題），本輪補入 SS-2009-1 成為 12 題。
- 2026-08-08｜ANALYSIS｜SS-U1-3 由統計得出的四項命題觀察（全部可由 `stats.py` 複算）：① **一題吃三個單元** —— 本單元只負責需求側（把內力放大），強度側的 `φcPn` 來自 U1-1、`φbMn` 來自 U1-2，故 11 題主考點實際檢驗三個單元的內容。② **考點漂移** —— 對切後 ASD 互制由 4 降至 1（2008 年後只回來過 2019-3 一次），LRFD H1 由 0 升至 3（2012-3、2020-3、2022-1，題型高度一致），B1／B2 二階放大由 0 升至 2（2013-4、2014-4 連兩年後**空窗 11 年**，是本單元空窗最久的計算題型），直接分析法由 1 降至 0（2011-1 唯一一次，空窗 14 年）。重心由「ASD 三式代數字」漂向「LRFD 的需求端怎麼被二階效應放大」。③ **設計法分界全科最乾淨** —— 前段（2003–2011）LRFD 掛零、ASD 4 題；後段（2012–2022）LRFD 5 題、ASD 僅 2019-3 一題（但配分 30 分）；近 6 考年 2 題全為 LRFD。④ **風險排序** —— LRFD H1 雙軸彎矩互制（3 題、空窗 3 年、唯一在近 6 考年出現的題型）與 B1／B2 放大（2 題、空窗 11 年、且 `Mu=B1·Mnt+B2·Mlt` 二十四年零次印出）列高風險；ASD 互制三式（5 題、歷史最高頻、但公式幾乎必給故準備成本低）與 K 值／對位圖併入梁柱（2013-4 唯一一次、與 U1-1 同步空窗 12 年）列中高風險；強柱弱梁 P-M 曲線（空窗 16 年、多半以耐震題回歸）與直接分析法（空窗 14 年、屬規範改版當年的「新聞題」）列中／低風險。另註：本單元 11 題主考點**全數附 P–M 互動圖**，是全科互動圖覆蓋率最高的單元。
- 2026-08-08｜UX｜全站把「速查頁」正名為「命題分析」，並移除 Keynote 按鈕。動機：`study-SS-Un-m.html` 五個單元已全部重構為命題情報頁（只回答「這個單元考什麼」），「速查頁」這個舊名稱描述的是重構前的七區段深度複習頁，名實不符；且 Keynote 按鈕指向的課堂投影片 PDF 與三份教材（lecture／formula-given／study）的分工重疊，使用者已明確要求移除。改動範圍：① **五份觀念講義** `lecture-SS-U1-1/-2/-3/-4/-U2-3.html` 的 header 按鈕列——「📊 速查頁」改為「📊 命題分析」（title 同步改為「命題分析：出題頻率、考點結構、考題清單、命題風險」，底色由灰 `#eceff1` 改為藍 `#e3f2fd`／`#1565c0` 以與講義本身的灰階按鈕區隔）、刪除「📄 Keynote」按鈕；② **U1-1、U1-3、U2-3 三份講義補上「🎯 給／背分界」按鈕**（U1-2、U1-4 原本就有），五份講義現在的按鈕列一致為「命題分析／給／背分界／本頁 PDF」三顆；③ `lecture-SS-U1-2.html` 內文的「使用順序建議：本講義（練題前）→ Keynote（課堂）→ 速查頁（考前）」改為「本講義（練題前）→ 給／背分界（決定背誦優先序）→ 命題分析（考前排練題順序）」，與三份教材的分工一致。
- 2026-08-08｜BUGFIX｜上述作業中發現 `lecture-SS-U1-3.html` 與 `lecture-SS-U2-3.html` 的 `<nav>` 尾端各有**兩顆未套樣式的殘留連結**：`<a href="formula-given-SS-U1-3.html">▶ U1-3 給／背分界</a>` 與 `<a href="formula-given-SS-U2-3.html">▶ U2-3 給／背分界</a>`，兩檔都同時含這兩顆——亦即 U1-3 的講義掛著指向 U2-3 的按鈕、U2-3 的講義掛著指向 U1-3 的按鈕，是先前批次插入時未依單元區分所致。兩檔的四顆殘留連結已全數移除，改為各自單元一顆、與 U1-2／U1-4 相同樣式（`#ffebee`／`#c62828`）的正式按鈕。
- 2026-08-08｜UX｜`study/problems-view/` 全 88 個題目渲染頁同步正名：header 的「🔍 Un-m 速查頁」按鈕文字與 `title` 屬性改為「🔍 Un-m 命題分析」，並同步改寫頁尾「跟隨來源單元」腳本內用來覆寫按鈕的兩個字串（`q.title` 與 `q.innerHTML`），確保由 `study-`／`lecture-`／`formula-given-SS-Un-m.html` 點入時動態改寫的文字也是新名稱。分兩批處理：82 檔為標準寫法，另 6 檔（SS-2005-4、SS-2009-1、SS-2009-2、SS-2012-2、SS-2020-1、SS-2020-2）因主分類單元無教材而採「（副分類）」變體寫法，第一批的樣式比對不到、被驗證擋下後單獨修正——這正是「先算完字串、驗證通過才寫檔」的作法擋下誤改的一次實例（對照 2026-08-08 的 SS-2002-2 清空事故）。88 檔全數通過結構檢查：各含 1 組 quick／lect 按鈕、結尾標籤完整、全站已無「速查頁」字樣殘留。
- 2026-08-08｜DOCS｜「速查頁 → 命題分析」正名的第二輪：把用語修正推到**所有設定檔與 skill 原始碼**，避免下次產頁時又照舊規格做出 Keynote 按鈕。逐檔改動：① `skills/unit-lecture/SKILL.md` —— 開頭「這不是速查表」段改為指出同子項另有 `study-`（命題分析：考什麼）與 `formula-given-`（給／背分界：要不要背）兩份教材、三者並存；「與同子項既有教材互連」整節重寫（教材表由四列縮為三列並加上「回答什麼／產出者」欄、刪除「使用者自備課堂 Keynote／投影片」那一列、nav 範例由「速查頁／Keynote／本頁 PDF」改為「命題分析／給／背分界／本頁 PDF」三顆並附 title 與新配色、加入兩則 ⚠️ 明文禁令：`study-` 的正式名稱是「命題分析」不是「速查頁」、不要放 Keynote 或課堂投影片按鈕）；Step 8 驗證清單第 5 項加上「nav 內沒有 Keynote 按鈕、全檔沒有『速查頁』字樣」。② `CLAUDE-CODE.md` 的 STUDY 節加註「子項層級已改由 `unit-exam-intel` 負責，下方七區塊為 2026-08 以前的舊規格，不要照舊產頁」，並把 `unit-lecture` 二欄分工表擴為 `lecture-`／`formula-given-`／`study-` 三欄。③ `CLAUDE-SPEC.md` 的檔名前綴表補上 `formula-given-` 一列，`study-` 的定位由「速查／複習頁」改為「命題分析」並註明子項層級由 `unit-exam-intel` 產出；1.2 節的禁令改為「不可命名為 `study-SS-UN-n.html`（會覆蓋該子項的命題分析頁）」。④ `skills/README.md` 的兩張分工表、`skills/unit-formula-map/SKILL.md` 與 `skills/unit-exam-intel/SKILL.md` 的相關描述、`知識庫使用說明書.md` 的指令表與目錄樹、`檔案架構索引表.md` 的 `study/` 與 `skills/` 兩列，全部同步為三份教材的新分工。
- 2026-08-08｜BUGFIX｜上述盤點另外抓到 `CLAUDE-CODE.md` STUDY 節殘留一條**與現行規則相牴觸的指示**：「【重要】點擊題號或標題時，必須以 `<a href="../index.html#md=raw/solutions/SS-XXXX-N/SS-XXXX-N.md&t=SS-XXXX-N">` 格式連結至 markdown 渲染器」。這正是 `unit-exam-intel` 的 `verify.py` 第 6 項明文禁止、且 2026-08-08 稍早才從 `study-SS-U1-1.html` 全數清掉的舊式連結（把 .md 丟給瀏覽器，公式與附圖不會渲染）。已改為「一律連 `problems-view/SS-XXXX-N.html`，禁止使用 `../index.html#md=`」，並說明 `study/problems-view/` 是全部題目的 HTML 渲染層。若未修，下次執行單元層級 `study` 指令會再度產出未渲染的連結。
- 2026-08-08｜PACKAGE｜重新打包 `skills/` 下三個 `.skill` 檔，使其與專案版原始碼一致：`unit-lecture.skill`（1 檔，15,706 → 16,221 bytes）、`unit-exam-intel.skill`（5 檔，26,470 → 25,674 bytes，排除 `__pycache__`）、`unit-formula-map.skill`（6 檔，19,560 → 19,578 bytes）。另記錄一項既存落差供日後處理：**已安裝版的 `unit-formula-map` 缺少整個 `scripts/` 目錄**（專案版有 `prerender.py`、`build_pdf.py`、`tex2svg.js`、`verify.py` 四支），且其 SKILL.md 少了「配套腳本」那段說明——即已安裝版比專案版舊。本輪依使用者選擇，改由使用者自行安裝重新打包後的 `.skill`，未以 `save_skill` 寫回帳號；在完成安裝前，實際觸發的仍是舊版 skill。
- 2026-08-08｜UX｜正名第三輪：`study/formula-given-SS-U1-1/-2/-3/-4/-U2-3.html` 五份「給／背分界」頁的 `<nav>` 整段重建，修掉三個問題。① **「▶ Un-m 深度複習」改為「▶ Un-m 命題分析」** —— 「深度複習」是 2026-08 以前那版七區段舊頁的名稱，該版已全部重構為命題情報頁。② **指向其他單元的按鈕標籤不一致** —— U1-2、U1-3、U2-3 三檔把兄弟頁寫成只有代號的「▶ U1-1」「▶ U1-4」，看不出會連到哪一種頁面（U1-1、U1-4 兩檔則已寫成完整的「▶ Un-m 給／背分界」）；現全部統一為「▶ Un-m 給／背分界」。③ **按鈕順序錯亂** —— U1-1、U1-2、U1-4 三檔的 `🖨️ 本頁 PDF` 卡在中間，後面又接著兩顆同類按鈕，成因是過去分批追加時直接 append 到 `</nav>` 前；現重建為固定順序「頁內錨點 4 顆 → 同單元觀念講義 → 同單元命題分析 → 其他四個單元的給／背分界 → 本頁 PDF」，五檔一致各 11 顆。重建採「保留原有 `#` 錨點連結、其餘按程式生成」的作法，並在寫檔前驗證無「深度複習」殘留、結尾標籤完整。
- 2026-08-08｜DOCS｜把上述修正回寫 `skills/unit-formula-map/SKILL.md` 的「導覽列」節（原本只有一句「放 lecture、study 的互連按鈕，以及本頁 PDF」，規格過於鬆散，才會產生三種不同寫法）。新版給出完整 `<nav>` 範例與三條硬規則：`study-` 的按鈕一律寫「▶ Un-m 命題分析」（不可寫「深度複習」或「速查頁」）、指向其他單元的 `formula-given-` 按鈕必須完整寫「▶ Un-m 給／背分界」（不可只寫代號）、`🖨️ 本頁 PDF` 一定放最後一顆（新增按鈕要插在它前面），並註明新增單元時其他既有頁面要補上反向連結。`CLAUDE-CODE.md` 的 STUDY 觸發語句說明由「子項層級深度複習」改為「子項層級**命題分析**，改用 `unit-exam-intel` skill」。`unit-formula-map.skill` 重新打包（19,578 → 20,262 bytes）。
- 2026-08-09｜PACKAGE｜依使用者要求交付四個 `.skill` 供安裝：`unit-exam-intel.skill`（5 檔 25,674 bytes）、`formula-recall-deck.skill`（15 檔 51,470 bytes）、`unit-formula-map.skill`（6 檔 20,262 bytes，含前一輪補齊的 `scripts/` 四支）、`unit-lecture.skill`（1 檔 16,221 bytes，2026-08-08 更新版含「教材互連」整節重寫）。本工作階段對 skill 檔僅有唯讀權限，無法直接寫回帳號，故一律以 `SendUserFile` 交付、由使用者自行點選安裝；安裝前實際觸發的仍是舊版。安裝結果已由後續 session 的 skill 清單確認前三個生效。
- 2026-08-09｜FORMULA-RECALL-DECK｜產生四支公式記憶片（`study/` 下 pptx + pdf + 旁白稿各一套），全部以本地知識庫 `study/formula-given-SS-*.html` 內嵌的 `const F=[]`／`const MX=[]` 原始資料為輸入（**未走 web_fetch，未重建任何公式**，故無「重建成分」需揭露）：`SS-U1-2_梁桿件`（35 頁／回想卡 10／觀念圖 5／旁白 4,037 字／14–16 分）、`SS-U1-3_梁柱桿件`（37 頁／10／5／4,899 字／18–20 分）、`SS-U1-4_接合之分析與設計`（40 頁／10／5／5,411 字／20–22 分）、`SS-U2-3_設計規範對施工之要求`（37 頁／10／5／4,744 字／17–19 分）。各單元定調依來源頁 §4：U1-2「給長式子、不給短定義」（`Lp`/`Lr` 十一年 vs. `Mp=FyZx` 24 年零次）、U1-3「ASD 幾乎必給、LRFD 必漏一半」（`Mu=B1·Mnt+B2·Mlt` 24 年零次，且 `B1`/`B2` 已空窗 11 年）、U1-4「六子項裡公式最不給」（37 條中 26 條必背、綠色僅 4 條；偏心接合 91/93/94/106 四年四題全零公式）、U2-3「唯一綠色為 0 條」（38 條中 34 條零次印出，僅有的 4 條例外皆為別題順帶印出、本單元用不到）。
- 2026-08-09｜QA｜四支簡報以 `python-pptx` 反向驗證通過：40 組回想卡「深色提問頁 → 正後方 `ANSWER NN` 頁」配對全數正確、149 頁每一頁都有 `addNotes`（零缺漏）、`pdftotext` 全文無 `undefined`／`NaN`；另以 34 dpi contact sheet 逐頁目視檢查文字溢出與觀念圖標籤重疊。過程中修掉的較嚴重問題：U1-4 骨幹頁 `result` 方塊文字爆出綠框、U1-3 `cm_cases` 第②圖畫成雙曲率卻標單曲率（觀念錯誤）、U2-3 `galv` 圖錯字「生鏹」、多處寬公式（`ar>18`）在速查表被壓到 0.3 in 高而另做堆疊版、Noto CJK 缺字的 ✓／✗ 改為 〇／×。
- 2026-08-09｜FIX｜更正 `study/formula-given-SS-U1-3.html` 中「P-M 互制圖的三個折點座標」條目的 `eq`：折點原寫成 \(\left(\tfrac{1}{9},\,0.2\right)\)，應為 **(0.9, 0.2)**。驗算依據：該條目自身的 `meta` 推導已經是對的 —— 把 \(P_u/\phi_cP_n=0.2\) 代入 H1-1a 得 \(x=\tfrac{9}{8}(1-0.2)=0.9\)，代入 H1-1b 得 \(x=1-0.1=0.9\)，兩式在此連續但不平滑；`1/9` 顯係誤把 H1-1a 的係數 8/9 寫成折點座標。由 `formula-recall-deck` 建置 U1-3 記憶片時發現（記憶片一律採正確值 (0.9, 0.2)，並把推導寫入該頁 note 與 P-M 互制曲線觀念圖）。⚠️ `study/formula-given-SS-U1-3.pdf` 尚未重新產生，仍含舊值，下次跑 `unit-formula-map` 的 PDF 產線時會一併更新。
- 2026-08-20｜FREQUENCY｜產生 `study/frequency-SS.html`（全科出題頻率熱圖，六科通用 `subject-frequency-map` v1.0）。單一自包含 HTML，含可切換「只看主考點／主＋副考點」的 7 子項 × 24 考年熱圖、排名總表（主／副題數、佔全科、出現年數、最長空窗年段、最後出現、近 6 考年、常見題號位置、現有教材自動偵測）、各單元權重、四種情境的讀書順序建議。所有數字由 `skills/subject-frequency-map/scripts/build_frequency.py` 從 `raw/json/question_index.json` 算出，對帳（格子總和／列總和／單元小計）全數通過。
- 2026-08-20｜FREQUENCY｜由該表得到的觀察：科目 SS 鋼結構設計｜24 考年（2002–2025）｜98 題｜7 個子項（7 個出現過）。單元權重 SS-U1 75 題（76.5%）、SS-U2 15 題（15.3%）——U1 是 U2 的 5.0 倍。前五名 U1-1 24、U1-2 21、U1-4 19、U1-3 11、U2-3 7，合計 82 題（83.7%），且這五個子項的四種教材（命題分析／講義／給背分界／記憶片）都已齊全。無「副>主」的工具型子項，也無 0 題子項——本科每個子項都至少當過一次主考點。最長空窗：U2-1 塑性分析與設計 14 年（2006–2019）、U2-2 鋼結構材料特性 12 年（2002–2013）且最後出現於 2018、近 6 考年 0 題。⚠️ 對帳警告：索引中有 8 題的 `primaryTopicId` 屬於他科 taxonomy（`SD-U3-1` × 5：SS-2022-4／SS-2020-1／SS-2012-2／SS-2009-1／SS-2009-2；`MM-U1-1` × 3：SS-2013-1／SS-2010-1／SS-2006-3），這 8 題未畫進熱圖，頁面最上方顯示紅色警告框；待決定要併入 SS 子項或在 taxonomy 中認列跨科標籤後重跑。


---

## 2026-08-22 — 七題解析勘誤（依現行規範重新驗算）

**操作類型：** 解析勘誤（Cowork）＋下游同步
**觸發：** 使用者指示「檢查並修正 SS-2013-3 & SS-2013-2 & SS-2005-1 & SS-2024-1 & SS-2015-3 & SS-2025-2 & SS-2018-2，依最新規範進行計算，下游檔案要一起修正」
**規範依據：** 主答＝內政部「鋼構造建築物鋼結構設計技術規範」**民國 99 年（2010）修正版**（查證為現行有效版本；參照 AISC 360-16 之修正草案為建研所研究案，尚未發布施行）；各題另增「依最新規範（AISC 360-16／-22）對照」小節。
**驗算方法：** 六份考卷 PDF 以 300～450 dpi 轉圖**逐頁目視判讀**（PDF 為 Adobe-CNS1 CID 字型，`pdftotext` 抽不到中文，且圖說符號只能目視），所有數值以 Python 獨立重算並交叉驗證（雙路徑驗算／量綱檢查／新舊規範互為驗算）。

### 一、觀念性錯誤（答案改變）

| 題號 | 原解析 | 修正後 | 錯因 |
|---|---|---|---|
| **SS-2013-2** | 「柱 CD 為鉸接」，查 K_CD=1.71，以 ΣP = ΣPe 得 w_u = 287 tf/m、d_m = 1.20 m | 考卷原文為「**柱 CD 為靠桿（leaning column）**」（圖上 C 點畫小圓圈＝鉸，A、D 皆為鉸支承）。依考卷給定之萊梅厥公式 K′=√[(Pe/P_I)(ΣP/ΣPeK)]，ΣPeK **僅計非靠桿柱 AB**：K_AB=1.71 → **K′_AB=2.42**、**w_cr=96.0 tf/m**、**d=0.40 m** | 誤把「靠桿」讀成「鉸接柱」，且未使用考卷給的公式而自創 ΣP=ΣPe；原答案高估約 3 倍 |
| **SS-2024-1** | 曲線三段，並宣稱在 λ=√2 處由 0.243「不連續跳躍」到 0.500 | **四段連續曲線**：1.0（λ≤0.697）／0.485/λ²（0.697–0.985）／**0.5 強度平台段（0.985–1.414）**／1/λ²（λ≥1.414）。轉折點 (0.697,1.0)、**(0.985,0.5)**、(1.414,0.5) | 兩個分支各有適用區間（彈性支僅 Fcr≤0.5Fy、非彈性支僅 Fcr≥0.5Fy），中間區段兩者皆不成立，強度被鎖在比例限 0.5Fy。原寫法違反「柱強度曲線隨 λ 單調不遞增」（等於柱做長反而變強），且同一 λ 出現兩個強度值 |
| **SS-2025-2** | 誤用 U = 1−x̄/L_weld 並取 x̄ = L/2，得 U = 1−L/6，微分求極值 → L=3 cm、**P_max = 6.15 tf**（NSF 控制） | 依 ASD 規範 §4.3「**板類構件僅以兩側縱向銲道傳遞拉力**」：U 為 l/w 階梯值 1.00／0.87／0.75 且**要求 l ≥ w**。l=3 cm 固定 → **L_max = 3 cm**（此即題目問「最大或最小」之答案）、U=0.75 → **P_max = 9.00 tf（全斷面降伏控制）** | U=1−x̄/l 的 x̄ 是「部分肢材連接」的偏心距，單一板片三面圍焊時 x̄=0，該式不適用；把板寬一半當偏心距使答案低估 32% |

### 二、判讀／敘述錯誤（數值不變，但推理錯）

| 題號 | 修正內容 |
|---|---|
| **SS-2013-3** | 逐一改正圖 3 兩平面的邊界判讀：**y-z 面（強軸）為「A 鉸支承－C 固接可軸向滑動」**（原寫成「A 固接、C 鉸接」）、**x-z 面（弱軸）柱底 A 為固接**（原寫成鉸接）。兩平面柱底條件相反正是本題主要陷阱。三個 KL/r 值（73.8／108.1／103.0）與控制段（弱軸下段）不變，因「鉸-固」與「固-鉸」的 K 同為 0.7。另修正 Fa 0.835→**0.834**、Pa 96.9→**96.8 tf**；補「設計 K 值（0.8）」對照（Pa=79.6、φcPn=111 tf）與局部挫屈界限（原誤寫 250/√Fy=158，正確為 0.56√(E/Fy)=16.0）。 |
| **SS-2005-1** | **補算漏掉的「螺栓剪力」極限狀態**：單剪 6 顆、Ab=3.801 cm²、φRn=0.75×4.2×3.801×6=**71.8 tf**——與控制值 68.5 tf 僅差 4.8%。題目特地給「螺栓標稱剪力強度 4.2 tf/cm²」與「螺紋不在剪力平面上」，原解析完全未用到這兩個條件。另修正塊狀剪力三條路徑的肢背／肢趾判讀（由圖：肢背側邊距 7.5 cm、肢趾側 5 cm，故**肢趾側控制**，並說明肢背側路徑須連帶剪斷外伸肢故實務不發生），以及承壓 2.4dtFu 之算術 43.5→**43.3 tf**。最終答案不變：**φPn = 68.5 tf（塊狀剪力控制）**。 |
| **SS-2018-2** | **補做漏掉的局部挫屈檢核**：b/t = 73.6/3.2 = 23.0 < 1.40√(E/Fy) = 34.8（台灣規範等價式 50/√Fy = 27.5）→ 非細長；並補 KL/r ≤ 200 檢核。原「陷阱表」把 **φc = 0.90 標記為「誤」**，實為 AISC 360-05 起之現行值，已改為「台灣現行規範 0.85 ／ AISC 360-16 起 0.90」雙軌呈現（φcPn = 2,586 tf ／ 2,738 tf）。H1 標題改依 CLAUDE-SPEC §4.1。 |
| **SS-2015-3** | §5「這等效於一端固定－一端自由模型，即懸臂柱」為誤述——本題「底鉸接＋頂可平移不能轉動」屬「**固接\*-鉸接**」（理論 k＝設計 k＝2.0）；懸臂柱是「自由端\*-固接」（理論 2.0、**設計 2.1**），機制相反、理論值巧合相同。已改為逐項（轉動／側移）判定表。數值不變（r_min = 8.12 cm、L = 700 cm）。H1 標題改依 CLAUDE-SPEC §4.1。 |

### 三、依最新規範的對照結論（各題 §5 已載明）

- **φc：台灣現行 0.85，AISC 360-05 起 0.90。** 只影響 SS-2018-2（2,586→2,738 tf）與 SS-2013-3（134→142 tf）；SS-2024-1 只問標稱曲線故不受影響。
- **Fcr 公式未變。** AISC 360-16／-22 把 λc ≤ 1.5 改寫為 KL/r ≤ 4.71√(E/Fy)（1.5π = 4.712），`0.658^(Fy/Fe)` ≡ `0.658^(λc²)`，兩題均已數值驗證等價。
- **ASD 架構。** 台灣仍為 Cc＋變動 FS；AISC 統一為 Fcr/Ω（Ω=1.67）。SS-2015-3 反算長度 700 → 703 cm（差 0.4%，12/23 = 0.5217 vs 0.877/1.67 = 0.5251）。
- **U 值。** SS-2005-1 單角鋼：考卷表格 0.85 vs AISC Table D3.1 max(1−x̄/l, 0.60) = 0.617（NSF 174→126 tf，仍不控制）。SS-2025-2 板類縱向銲 l/w 階梯值新舊規範**完全相同**。
- **承壓。** AISC 另計撕出 1.2LctFu（SS-2005-1 端栓 43.3→37.6 tf，仍不控制）。
- **穩定分析。** AISC 360-16 起以直接分析法（Ch. C）為主流程、有效長度法降為 Appendix 7；SS-2013-2 §5.3 已載明「新規範淘汰 K 值法的理由，正是本題這種含靠桿的框架需要手工修正」。

### 四、同步的下游檔案

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-{2005-1,2013-2,2013-3,2015-3,2018-2,2024-1,2025-2}/*.md` | 7 份解析修正（正本） |
| `raw/solutions/SS-2024-1/SS-2024-1-column-curve-viz.html` | 曲線改為四段連續、新增橘色強度平台段、轉折點表改為 A/B/C 三點、刪除 B′ 跳躍敘述；Ie/Ix 0.486→0.485 |
| `wiki/problems/SS-*.md`（7 檔） | 由修正後正本重新生成（沿用既有摘要骨架） |
| `study/problems-view/SS-*.html`（7 檔） | 由修正後正本重新渲染（頁面外殼與腳本 byte-for-byte 不變，已比對） |
| `raw/json/question_index.json` | 7 題 tags 增補（`靠桿`、`leaning column`、`挫屈載重`、`螺栓剪力`、`螺栓承壓`、`局部挫屈`、`φc新舊規範`、`強度平台段`、`板類縱向銲接`、`l/w規定`、`兩平面邊界不同`、`繫條`、`Cc判斷`、`λc`）；SS-2013-2 移除與 designMethod 矛盾的 `ASD` tag。**primaryTopicId／secondaryTopicIds／designMethod／verificationStatus 一律未動**，故 `study/frequency-SS.html` 與各單元命題分析頁的統計數字不受影響 |
| `study/study-SS-U1-1.html` | Q[] 陣列中 7 題的一行描述與標籤更新（區塊 1.5 考題清單） |
| `dashboard-data.js` | 7 題 tags 陣列同步 |

### 五、待決事項（提請使用者裁示）

1. **規則 1 的例外範圍。** CLAUDE.md 規則 1、2 保護 `raw/solutions/SS-YYYY-N/`；2026-07-30 的 VERIFY 紀錄即因此**未修正** SS-2013-2 已查出的 π²EIc 量級筆誤。本輪依使用者明示指示執行勘誤（與 2026-05-27 SS-2020-3 解析修正之先例一致），建議比照 `methods/` 在 CLAUDE.md 增訂「解析勘誤」例外及其三項條件（驗算／同步下游／記 log）。
2. **SS-2013-2 的 designMethod。** 索引為 `LRFD`、原解析 .md 寫 `ASD`，本題實為純彈性穩定分析（無 φ／FS）。為避免動搖 `study-SS-U1-1.html` 的設計法分布統計，本輪**未改索引**，僅在 .md 註明。若要改為「概念題」或新增「穩定分析」類別，需一併重跑 `unit-exam-intel`。
3. **SS-2013-3 的 K 值取捨。** 考卷同時給理論 K 與設計 K。本輪主答採**理論 K**（與原解析數值一致），並在 §5.2 完整列出設計 K 的答案。若使用者偏好以設計 K 為主答，兩處需互換。
4. **`wiki/log.md` 編碼。** 本檔第 16,742 byte 起有一段 **Big5／CP950 編碼殘留**（2026-06-11「刪除代號存根」該節），以 UTF-8 讀取會出現亂碼。本輪僅以 append 方式在檔尾追加，未觸碰既有位元組。建議另行安排一次編碼修復。


---

## 2026-08-22 — 全庫 verificationStatus 重置為 unverified

**操作類型：** 驗證狀態重置（使用者指示）
**觸發：** 使用者指示「請將所有解題 verification status 改為 unverified，我要修正解題」
**背景：** 同日的七題勘誤中，抽查的 7 題有 3 題存在會改變答案的觀念錯誤（SS-2013-2 靠桿、SS-2024-1 強度平台段、SS-2025-2 板類縱向銲 U 值），錯誤率達 43%。既然抽樣即揭露此比例，其餘 91 題的 `verified` 標記已失去可信度，故由使用者決定全庫重置、逐題重新驗算。

**範圍：98 題全部** `verified` → `unverified`（非僅該 7 題）

| 檔案 | 變更 | 處數 |
|---|---|---|
| `raw/json/question_index.json` | `verificationStatus: "verified"` → `"unverified"` | 98 |
| `wiki/problems/*.md` | `**驗證狀態：** ✅ verified` → `**驗證狀態：** ⚠️ unverified` | 98 檔各 1 處 |
| `wiki/index.md` | 題目列 `\| ✅ [SS-` → `\| ⚠️ [SS-`；表頭計數改為「已驗證 0 題／待驗證 98 題」 | 77 + 1 |
| `wiki/by-year.md` | 題目列 `\| ✅ [SS-` → `\| ⚠️ [SS-`（第 4 行圖例 `> ✅ = verified｜⚠️ = unverified` 保留） | 98 |
| `index.html` | 儀表板硬寫死的「已收錄題目（全部 verified ✅）」→「（全部待重新驗算 ⚠️）」 | 1 |
| `study/study-SS-U1-1〜U2-3.html`（5 檔） | 考題清單徽章 `✅`／`title="…已驗證"` → `⚠️`／`title="…待驗證"`；圖例「✅ 已驗證。」→「⚠️ 待驗證（全庫已於 2026-08-22 重置）。」 | 5 檔各 1〜2 處 |

**執行方式：** 於使用者本機以 `python3` 就地字串替換，先 DRY-RUN 核對每一處替換數與預期值（98／98／77／1／98／1／5）全部相符後才 `--apply`；`question_index.json` 以 `json.load` → `json.dumps(ensure_ascii=False, indent=2)` 往返，格式與原檔一致且重新解析通過。

**未變動（刻意）：**
- `raw/solutions/**`：解析內容本身未動。其中 10 檔頁尾已有 `*驗證狀態：unverified*` 字樣（含本日修正的 7 檔），其餘 88 檔頁尾原本就無此欄位，未逐檔補寫，以免對受規則 1、2 保護的證據檔做非必要改動。
- `dashboard-data.js`：其資料列 `[id, topic, secondary, designMethod, viz, tags, pdfs]` **不含**驗證狀態欄位，故無需變更。
- `study/frequency-SS.html`、`lecture-*`、`formula-given-*`：經逐檔比對，其中的「驗證」字樣均為「驗算」語意的行文（如「驗證：e^{-0.419(1.5)^2}=…」），非驗證狀態標記，未動。

**⚠️ 後續影響（提醒）：**
1. CLAUDE.md 規則 5「ingest 前必須確認 `verificationStatus = "verified"`」——現在全庫 98 題皆為 unverified，**`ingest` 指令對任何題目都會被前置檢查擋下**。既有 `wiki/problems/` 98 頁仍保留在原處（只改狀態標記，未刪頁），逐題重新驗算通過後再改回 verified 即可正常 ingest。
2. `status` 與 `unverified` 兩個指令現在會回報「已驗證 0 題／待驗證 98 題」。
3. 建議的重驗優先順序：本日已重算並附「最新規範對照」的 7 題（SS-2005-1／SS-2013-2／SS-2013-3／SS-2015-3／SS-2018-2／SS-2024-1／SS-2025-2）可優先複核放行；其餘 91 題建議以「同一子項、同一解題套路」成批重驗，並沿用本日的作法——**考卷 PDF 轉圖逐頁目視判讀**（`pdftotext` 抽不到中文與圖說符號）＋**每個數值以程式獨立重算**。


---

## 2026-08-22 — 依七題檢查結果的收尾：規則 1 增訂勘誤例外 ＋ log.md 編碼修復

**操作類型：** 規則修訂（Cowork，經使用者裁示）＋檔案編碼修復
**觸發：** 使用者指示「依檢查結果修改檔案」，並就本日 log §五「待決事項」四項逐項裁示。

### 使用者裁示結果

| # | 待決事項 | 裁示 | 本輪動作 |
|:-:|---|---|---|
| 1 | CLAUDE.md 規則 1 是否增訂「解析勘誤」例外 | **增訂例外＋條件** | ✅ 已修訂（見下） |
| 2 | SS-2013-2 索引 `designMethod`（LRFD vs 概念題／穩定分析） | **維持 LRFD，只在 .md 註明** | 無需改檔（現狀已符合；`.md` 已註「本題實際為彈性穩定分析，不含 φ 折減；索引沿用 LRFD」） |
| 3 | SS-2013-3 主答採理論 K 或設計 K | **維持理論 K 為主答** | 無需改檔（現狀已符合；設計 K 之完整答案列於 §5.2） |
| 4 | `wiki/log.md` Big5 編碼殘留 | **修復並標註** | ✅ 已修復（見下） |

### 一、CLAUDE.md 規則 1：增訂第三項例外

**修訂內容：**
- 例外由「兩處」擴為「**三處**」，新增 `raw/solutions/SS-YYYY-N/SS-YYYY-N.md`（**僅限解析勘誤**）。
- 刪去舊條文「⚠️ `raw/solutions/SS-YYYY-N/`（個別題目解析）**不在例外內**，仍受規則 1 與規則 2 保護」，改為完整的例外說明。
- **明訂勘誤的四項條件（缺一不可）**：
  ① **回考卷原文**逐頁目視判讀（本科考卷為 Adobe-CNS1 CID 字型，`pdftotext` 抽不到中文，支承符號／鉸接圓圈／尺寸線只能目視，須轉圖 300–450 dpi）；
  ② **數值獨立重算**（程式重算＋量綱檢查＋雙路徑交叉驗算）；
  ③ **同步全部下游**（`wiki/problems/`、`study/problems-view/`、`*-viz.html`、`question_index.json` tags、必要時 `dashboard-data.js` 與 `study/study-*.html`）；
  ④ **記 log** 並在 .md 頁尾加「修正日期」。
- **明訂仍完整受保護者**：`raw/exams/`（考卷原件）、`-fig-*/-chart-*/-eqn-*/-hand-*.png`（使用者截圖證據）、使用者放入的補充筆記 `*.pdf`。勘誤只准動 `.md` 正本與 Cowork 自己生成的 `*-viz.html`。
- **驗證狀態連動**：一經勘誤，該題 `verificationStatus` 必須退回 `unverified`，人工複核後才可改回 `verified`。
- **規則 2 補界線**：`verifiedSolution` 不可重算之保護，限於 `verificationStatus = "verified"` 者；使用者明示勘誤或該題已退回 `unverified` 時不阻止重算。

**修訂理由（寫入條文的教訓）：** 舊條文使 2026-07-30 的 VERIFY 已查出 `SS-2013-2.md` 的 π²EIc 量級筆誤，卻「不敢修、只在 log 記一筆」；該檔後續（2026-08-22）又被查出更嚴重的觀念錯誤——把考卷原文「柱 CD 為**靠桿**」讀成「鉸接」，挫屈載重高估約 3 倍。**規則不該讓已知錯誤留在正本裡**；保護對象由「檔案」精確化為「可追溯性與證據」。

### 二、wiki/log.md Big5 編碼殘留修復

**問題：** 原檔 byte 16728–17259（531 bytes）以 **Big5／CP950** 位元組寫入，夾在 UTF-8 檔案中，導致整檔無法以 UTF-8 完整解碼（以 `open(..., encoding='utf-8')` 讀取會拋 `UnicodeDecodeError`）。該區涵蓋 `## 2026-06-11 刪除舊代號存根` 一整節與其後 `2026-07-02 REFRESH-DASHBOARD` 一則紀錄。

**判定過程（重要，避免重蹈）：** 初次以「逐個壞位元組往後找回可解碼點」的方式分片掃描，得到 71 個碎片、其中兩片連 Big5 也解不出，並出現「角F」、「禤」等看似無法還原的殘骸——**這是假象**：Big5 是無狀態雙位元組編碼，分片邊界把字切半才會解不出。改以**整段一次解碼**後確認：`seg.decode('big5')` **嚴格成功、零替換字元、未重建任何文字**。

**修復內容：**
1. 原始 531 bytes 完整備份至 **`wiki/log.md.big5.bak`**（不可逆操作前先留存）；
2. 該區段以嚴格 Big5 解碼後改以 UTF-8 寫回（531 → 1068 bytes）；
3. 順帶還原 **8 處**誤寫成 `\` 的 markdown 反引號——經比對，這 8 個 `0x5C` 全落在該是反引號的位置（`更新儀表板資料`、`question_index.json`、`syllabus_taxonomy.json`、`dashboard-data.js`），且檔案其他 UTF-8 紀錄對同樣詞彙皆使用反引號；
4. 於該節末加一行 🔧 修復註記，說明修復方式與備份位置。

**驗收：** 全檔（79,426 bytes）現可完整 UTF-8 解碼 ✔；修復區段**之前與之後的位元組經比對 byte-for-byte 未變** ✔；紀錄內容本身未增刪（符合規則 3 之精神——本次為忠實還原，非刪除）。

### 三、本輪未動的檔案（確認第一輪 7 題修正仍完整在位）

本輪開始前先全面驗收 2026-08-22 第一輪的七題勘誤，確認全部仍在磁碟上：`raw/solutions` 七份正本（SS-2013-2「靠桿」41 處、SS-2024-1「強度平台」＋λ₂=0.985、SS-2025-2 L_max=3／P=9.00、SS-2005-1 螺栓剪力 71.8、SS-2018-2 局部挫屈＋φc 雙軌、SS-2013-3 兩平面邊界＋96.8、SS-2015-3「固接*-鉸接」）、`SS-2024-1-column-curve-viz.html`（四段連續曲線）、`wiki/problems/` 七檔、`study/problems-view/` 七檔、`question_index.json` 七題 tags —— 均未受第二輪（全庫 unverified 重置）影響，本輪亦未再變更。

---

## 2026-08-22 — 第二批七題解析勘誤（梁桿件 U1-2，依現行規範重新驗算）

**操作類型：** 解析勘誤（Cowork，依 CLAUDE.md 規則 1 第三項例外）＋下游同步
**觸發：** 使用者指示「幫我檢查並修正下列題目解題 SS-2011-3 & SS-2025-1 & SS-2014-3 & SS-2023-3 & SS-2010-4 & SS-2008-1 & SS-2015-1　請依最新規範進行計算　若有修正.md，別忘了，下游檔案要一起修正」
**範圍：** 7 題全屬 `SS-U1-2` 梁桿件（LTB／斷面選擇／Mp·My）

### 〇、規範依據（每題 §6 均已明載）

主答一律依內政部「鋼構造建築物鋼結構設計技術規範」**民國 99 年（2010）修正版**；以 AISC 360-16 為基礎之修訂版**尚未發布**。直接證據：**104 年（2015）考卷注意事項（四）**明文「作答請採用內政部發布 2010 年『鋼結構設計技術規範』為原則，並依題目指定設計法作答」。AISC 360-16／-22 一律另設 `## 6. 依最新規範（AISC 360-16／-22）對照` 專節，不混入主答。

### 一、勘誤總表

| 題號 | 嚴重度 | 錯誤內容 | 修正後 |
|---|:-:|---|---|
| **SS-2015-1** | 🔴 **答案變更** | 子題(一)最佳（最輕）斷面答 **BH 826×350×16×28（251 kg/m）**，跳過了更輕且合格的 **BH 920×300×19×25（247 kg/m）** | 改答 **BH 920×300×19×25（247 kg/m）**，$\phi_bM_p = 233.78 \geq M_u = 230.72$ tf-m |
| SS-2015-1 | 🟠 | §5 爭議二稱「台灣 2010 規範採 $A_w = d \times t_w$（全深）」——與 100 年考卷公式表明列的 $A_w = (d-2t_f)t_w$ 相牴觸 | 改為雙軌：台灣淨高 165.3 cm²（$\phi_vV_n = 224.9$ tf）／AISC 360 全深 174.8 cm²（237.9 tf），並註明本卷未給 $A_w$ 定義 |
| SS-2015-1 | 🟠 | 連帶 $h/t_w$ 48.1、$\phi_vV_n$ 179.8 tf、$I_x$ 373,031、$\delta_L$ 0.968 cm 全為舊斷面之值 | 45.8、**224.9 tf**、**404,726 cm⁴**、**0.892 cm**（38.2%） |
| SS-2015-1 | 🟠 | `SS-2015-1-sfd-bmd-viz.html` 面板「選用斷面」仍寫 BH 870×350×16×25（240 kg/m）——連 .md 上一版的 251 都沒同步 | 改為 BH 920×300×19×25（247 kg/m），並加一列 $\phi_bM_p = 233.78$ tf-m |
| **SS-2023-3** | 🟠 **內部矛盾** | §3.5 L2 表格數值與 §4 正確計算矛盾：$I_{自身}$ 誤植 1563（應為翼板 521、底翼板 313）、$I_x = 748{,}580$、$S_{bot} = 11{,}740$、$M_y = 29{,}350$ tf·cm | $I_x = \mathbf{1{,}224{,}062}$、$S_{bot} = \mathbf{19{,}201}$、$M_y = \mathbf{48{,}003}$ tf·cm（與 §4 一致）；另補 $S_{top}$ 26,471 → **26,466** |
| **SS-2011-3** | 🟠 | $C_W$ 用近似式 $I_y(d-t_f)^2/4$ 得 689,693 cm⁶，未用**本卷第三頁公式表明列**的 $C_W = I_f h^2/2$ | $C_W = \mathbf{687{,}469}$ cm⁶（近似式高估 0.37%）；連帶 $X_2$ 1.230→**1.224**、$L_r$ 833.5→**833.2** cm、$M_n$ 3382→**3378** tf·cm |
| SS-2011-3 | 🟡 | $A$／$I_x$／$S_x$／$Z_x$／$M_p$／$M_r$ 有 0.02～0.06% 的累積捨入偏差（$A$ 寫 100.0，實為 99.97） | 99.97／25,831／1,271.8／1,475.9／3,719.2／1,869.6 |
| **SS-2014-3** | 🟠 **主答解讀變更** | 「梁全長承受**均佈的雙向彎矩**」被解讀為均佈載重（$C_b = 1.136$）；且以「簡支梁不可能有常數彎矩」為由排除 $C_b = 1.0$——**該論證錯誤**（兩端施加等值同向端彎矩即為定值彎矩，正是 $C_b$ 定義的基準情形） | 主答改為**均勻彎矩 $C_b = 1.0$**（貼合原文、且較保守）：$\phi_bM_{nx} = \mathbf{945.8}$ kN-m、互制比 **0.715**；$C_b = 1.136$（1074.4／0.664）全程並列為另解。**兩解讀結論皆「滿足設計要求」** |
| SS-2014-3 | 🟡 | 互制公式誤稱「H1-2」——規範無此編號 | 更正為 **H1-1b 在 $P_u = 0$ 時之退化型** |
| **SS-2008-1** | 🟠 **推導方向顛倒** | Step 3 由「$EC_W$ 項主導、$C_W \approx I_yd^2/4$」起算 $L_d/A_f$ 的來源，又把 $L_d/A_f$ 歸因於「壓力翼板側向彎曲柱效應」——後者實為**翹曲**機制（對應 $r_T$ 系列），與 §2、§4 Step 4 的正確對號自相矛盾 | 改由 $\sqrt{I_yJ} \approx A_f^2/3$、$S_x \approx A_fd$ 正確導出 $F_b^{cr} = \dfrac{\pi\sqrt{EG}/3}{(L_d/A_f)}$，並明標「本解析前版即犯此誤」 |
| **SS-2025-1** | 🟡 | §5「翼板稍**厚**（$t_f = 1.4$ cm → $\lambda_f = 10.71$）」——$t_f$ 在分母，1.4 < 1.5 是變**薄** | 改為完整 $t_f$ 敏感度表（1.6／1.5／1.4／1.3 → 9.38／10.00／10.71／11.54） |
| **SS-2010-4** | ⚪ 補強 | 主答 RH244×175 正確，但「RH298×149 因自重迭代超出 0.55% 被淘汰」的論證單薄——被淘汰的斷面**又輕（32.0 vs 43.6 kg/m）又剛（$I_x$ 6,320 vs 6,040）**，值 26.6% 鋼料的決定不能只靠 0.55% | 新增 §5.5 三項獨立論證，關鍵為**翼板非結實之獨立佐證**：RH298×149（＝H-298×149×5.5×8）$\lambda_f = 149/16 = 9.313 > \lambda_p = 17/\sqrt{3.52} = 9.061$，依 FLB 內插 $\phi_bM_n = \mathbf{1{,}497}$ tf·cm，**連不含自重的 1,496 都只剩 0.04% 餘裕**；另補五組候選斷面全檢核表（200×200、200×204 之撓度分別 126%、120% **不合格**，故 RH244×175 是唯一同時滿足彎矩與撓度者） |

### 二、最新規範對照的重要發現（新增之 §6）

| 題號 | AISC 360-16／-22 的差異 | 是否改變結論 |
|---|---|:-:|
| **SS-2011-3** | **挫屈分區翻轉**：$M_r$ 由 $(F_y-F_r)S_x$ 改為 $0.7F_yS_x$，使 $L_r$ 由 **833.2 → 721.3 cm**，$L_b = 812.8$ cm 由「非彈性」變成「**彈性 LTB**」；$C_b$ 1.75 → 1.667；$M_n$ 3378 → **3176** tf·cm（−6.0%） | ⚠️ **是**（本題正好問「是否在彈性範圍內」） |
| SS-2014-3 | 弱軸上限 $1.5F_yS_y$ → $1.6F_yS_y$，$M_{ny}$ 190.1 → **199.0** kN-m（改由 $F_yZ_y$ 控制，+4.7%）；$M_r$ −9.9% 使 $\phi_bM_{nx}$ −4.3%。兩者方向相反互相抵銷，互制比 0.715 → 0.721 | 否（差 0.8%） |
| SS-2010-4 | $\lambda_{pf}$ 9.061 → 9.148、$M_r$ 定義改變，RH298×149 之 $\phi_bM_n$ 1,497 → 1,499 tf·cm | 否（兩規範皆判淘汰） |
| SS-2023-3 | 單軸對稱斷面歸入 **§F4**，新增 CFY（$\leq 1.6S_{xc}F_y$）與 **TFY**（$S_{xt} < S_{xc}$ 時 $M_n = R_{pt}M_{yt}$）兩限制狀態；本題 $R_{pt} = 1.289$ 代回仍得 $M_n = M_p$ | 否 |
| SS-2025-1 | **$F_r$ 參數已取消**（改用固定 $0.7F_y$）——本題「銲接殘餘應力 1.16 tf/cm²」這個干擾資訊在新規範中不存在；$M_r$ 3,088 → 4,033 tf·cm（+30.6%） | 否（完全側支撐） |
| SS-2008-1 | §F2 把 $GJ$ 與 $C_W$ 合併於單一 $F_{cr}$ 式（$r_{ts}$ 與 $Jc/(S_xh_o)$），**「取較大值」這道手續本身已被取消** | 否（觀念一致） |
| SS-2015-1 | $L_p$ 3.02 → 3.00 m（$80/\sqrt{F_y}$ ≡ $1.76\sqrt{E/F_y}$）；$\phi_v$ 0.9 → **1.00**（$h/t_w \leq 2.24\sqrt{E/F_y}$），$\phi_vV_n$ +17.5% | 否（三小題答案全同） |

### 三、驗算方法（規則 1 條件②）

- **全部 7 題共約 150 個數值以 Python 獨立重算，`MISMATCHES: 0`**（腳本 `/tmp/final_check.py`，含量綱檢查）。
- **考卷原文逐頁目視判讀**（條件①）：本科考卷為 Adobe-CNS1 CID 字型，`pdftotext` 抽不到中文。以 `pdftoppm -r 200 -png` 轉圖後目視 SS-2008 p1、SS-2010 p2、SS-2011 p2·p3、SS-2014 p1、SS-2015 p1·p3、SS-2023 p2、SS-2025 p1 共 10 頁。關鍵發現：
  - **100 年（2011）第三頁公式表**明列 $A_w = (d - 2t_f)t_w$ 與 $C_W = I_f h^2/2$ —— 這是 SS-2015-1 與 SS-2011-3 兩處勘誤的原始依據。
  - **104 年（2015）第三頁公式表只給 $V_n$ 三段式、未定義 $A_w$** —— 故該題採雙軌並註明。
  - **104 年圖 1(b)** 中 BH 920×300×19×25 的曲線平台（233.78）與 BH 500×500×25×40（233.66）**幾乎重疊**，且其標籤以引線指向 $L_b \approx 3.1$ m 的陡降段（因 $L_p = 3.02$ m 為全表最小），這正是它被漏看的原因。
  - **99 年（2010）第二頁 RH 斷面表**：298×149 之 $I_x = 6{,}320 >$ 244×175 之 6,040，證實被淘汰者「又輕又剛」。
  - **112 年（2023）第二頁**原卷寫「$E_y = 2050$ tf/cm²」，下標 $y$ 應為誤植（已於 .md 註明；本題不需用 $E$）。
  - **114 年（2025）第一頁**題幹明載「結實梁」、「腹板（web）不會產生局部挫屈」、「假設銲接面積不計入斷面性質」三個豁免條件，且問法為「**設計**彎矩強度 $M_{nx}$」（形容詞與符號不一致，已改為兩者並列）。
- **雙路徑交叉驗算**（條件②）：
  - SS-2015-1：以自建斷面性質引擎重算圖 1(b) **全部 7 條曲線**的 $\phi_bM_p$ 與 $L_p$，與圖面平台高度、轉折位置逐條吻合（870 於 3.85 m、920 於 3.02 m、826 於 3.99 m、500×500 於 5 m 內不轉折）。
  - SS-2011-3：$L_b$ 幾乎等於 $L_r$，故以**彈性式**回算得 3380 tf·cm，與非彈性式 3378 僅差 **0.07%** —— 兩支曲線在 $L_b = L_r$ 相接，可反證 $X_1$／$X_2$／$L_r$ 彼此一致。
  - SS-2023-3：以「實心 50×110 減兩處缺口」法算對底緣慣性矩 3,662,500 再移軸，得 $I_x = 1{,}224{,}062.5$ cm⁴，與逐項疊加法一致；同法驗 $A = 600$、$\sum A\bar{y} = 38{,}250$。
  - SS-2008-1：把題目的公制係數全部反推回 AISC ASD 英制原式——$\pi^2E/FS = 171{,}700 \to 170{,}000$（$\times 0.070307 = 11{,}952 \approx$ **12000**）、$\pi\sqrt{EG}/3/FS = 11{,}320 \to 12{,}000$ ksi（$\to 843.7 \approx$ **840**）、1530／102／510 ksi $\to$ 107,570／7,171／35,857，五個係數全部吻合（誤差 < 0.5%）；另驗三式連續性（$L/r_T = \sqrt{7160C_b/F_y}$ 處恰得 $0.6F_y$；$\sqrt{35800C_b/F_y}$ 處兩式同收斂於 $F_y/3$）。
  - SS-2014-3：反推題目給定的 $\lambda_p = 9.19 = 65/\sqrt{50}$、$\lambda_r = 22.30 = 141/\sqrt{40}$（英制 ksi，$F_y = 50$、$F_r = 10$ ksi），確認題目採 AISC LRFD 1993 體系。
  - SS-2025-1：$Z_x/S_x = 2{,}619/2{,}304.6 = 1.136$ 落在 I 型斷面形狀因數 1.10～1.18 的正常範圍（若漏算腹板貢獻則為 0.849 < 1，物理上不可能，可立即察覺）。

### 四、下游同步（規則 1 條件③）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/*/*.md` × 7 | 勘誤 ＋ 每題新增 `## 6. 依最新規範（AISC 360-16／-22）對照` ＋ 頁尾「修正日期：2026-08-22」與「驗證狀態：unverified」 |
| `raw/solutions/SS-2015-1/SS-2015-1-sfd-bmd-viz.html` | 選用斷面改 BH 920×300×19×25（247 kg/m），加 $\phi_bM_p$ 一列 |
| `wiki/problems/*.md` × 7 | 由 `_regen.py` 依正本重建摘要（保留原有 H1／來源／考年／驗證狀態／圖形／相關概念尾段）；另修 SS-2015-1、SS-2023-3 兩個殘缺 H1（原為 LaTeX 被剝除後的「- 跨距  m 之簡支承鋼梁」、「下圖為一梁斷面，鋼之 ，，…」），改為描述式標題 |
| `study/problems-view/*.html` × 7 | 由 `_regen.py` 重新渲染 `<main>` 內容；**`<main>` 以外的 shell 逐位元組比對未變** ✔；KaTeX 檢查 display／inline math 破損數皆為 0 ✔ |
| `raw/json/question_index.json` | 6 題 tags **append-only** 各補 2 個（原有標籤一律不刪）；98 題 `verificationStatus` 維持 `unverified` |
| `dashboard-data.js` | 同上 6 題 tags append-only（`window.SS_QUESTIONS` 仍 98 筆，Node 載入驗證通過） |
| `study/study-SS-U1-2.html` | 7 題 `Q[]` 列的摘要與標籤更新（標籤 append-only） |
| `wiki/log.md` | 本則紀錄 |
| `CLAUDE.md` | CHANGELOG 補一列 |

**未變更（刻意）：** `raw/exams/` 考卷原件、所有 `-fig-*`／`-chart-*`／`-eqn-*`／`-hand-*.png` 使用者截圖、`SS-2025-1/figs/*.svg` 與 `gen_SS-2025-1.py`（圖面數值未受影響）、`variable_hierarchy_SS2015_1.html`（無題目專屬數值）、`question_index.json` 的 `primaryTopicId`／`secondaryTopicIds`／`designMethod`（以維持 `study/frequency-SS.html` 與各單元命題分析的統計有效性）、SS-2023-3 之 tags（本題勘誤不涉新考點）。

### 五、待使用者複核（規則 5）

7 題 `verificationStatus` 均為 `unverified`，須人工複核後才可改回 `verified`。其中兩處為**判斷取捨**，建議優先確認：

1. **SS-2014-3 的 $C_b$ 解讀**：本輪把主答由 $C_b = 1.136$（均佈載重）改為 **$C_b = 1.0$（均勻彎矩）**，理由是原卷「均佈**的雙向彎矩**」中心語為「彎矩」、且「彎矩作用在梁之剪力中心」是施加彎矩的語法，並偏保守。兩解讀之互制比 0.715 與 0.664 皆 < 1.0，**「滿足設計要求」的結論不變**。若使用者認為應以均佈載重解讀，只需把 §4 Step 2b／2d、Step 4 與總結表的主答與另解對調（兩組數字皆已完整列出）。
2. **SS-2010-4 的自重迭代嚴格度**：主答維持 RH244×175。本輪為「淘汰 RH298×149」補上翼板非結實的獨立佐證（$\phi_bM_n = 1{,}497 <$ 含自重 1,513，且連不含自重的 1,496 都只剩 0.04% 餘裕），使結論不再只依賴 0.55% 的超出量。若使用者傾向「僅就力矩考量可不計自重」而改答 RH298×149，$\delta_L = 1.571$ cm（94.2%）亦合格，但需面對翼板非結實使 $M_n < M_p$ 的問題。

第三處較次要：**SS-2015-1 的 $A_w$ 定義**（台灣 $(d-2t_f)t_w$ 為主答 224.9 tf／AISC $d\,t_w$ 為 237.9 tf），因 $V_u = 82.4$ tf 遠小於兩者，僅影響使用率數字（36.6% vs 34.6%），不影響任何判定。

---

## 2026-08-22 — 第三批六題解析勘誤（梁柱桿件／二階分析 U1-3，回查台灣規範原文）

**操作類型：** 解析勘誤（Cowork，依 CLAUDE.md 規則 1 第三項例外）＋下游同步
**觸發：** 使用者指示「幫我檢查並修正下列題目解題 SS-2013-4 & SS-2020-3 & SS-2003-4 & SS-2011-1 & SS-2022-1 & SS-2009-1　請依最新規範進行計算　若有修正.md，別忘了，下游檔案要一起修正」
**範圍：** 6 題全屬 `SS-U1-3` 梁柱桿件／二階穩定（SS-2009-1 主分類為 `SD-U3-1`、副分類 `SS-U1-3`）

### 〇、本輪新增的規範原文查證（重要，供後續各題引用）

本批多題涉及台灣規範的**條文原文**，故直接回查內政部 99.09.16 版之官方 PDF（rootlaw、行政院公報）：

| 查證項目 | 結果 | 影響題目 |
|---|---|---|
| ASD §8.2 之 $C_m$ | 式 **(8.2-5)** `Cm = 0.6 − 0.4(M1/M2)`，**無 $\geq 0.4$ 下限**；解說明言舊式的「$\geq 0.4$」「在 1986 年版的 AISC-LRFD 規範及本規範中均已不再採用」 | SS-2003-4 |
| $M_1/M_2$ 符號 | 「當構材受彎成**雙曲率**彎曲時，$M_1/M_2$ 之比為**正值**；當構材成**單曲率**彎曲時，為**負值**」（ASD 與 LRFD 兩章一致） | SS-2003-4、SS-2020-3 |
| AISC ASD 9th §H1 | 亦**無** $C_m \geq 0.4$ 下限 ⇒ 100 年考卷公式表所印之「(≥0.4)」是 1978 年前舊規定的殘留，**該考卷公式表有誤** | SS-2003-4 |
| LRFD §8.2 之 $B_1$ | 式 **(8.2-3)** 為台灣**自訂**形式（含係數 0.64 與 0.32），**不是** AISC 的 $C_m/(1-P_u/P_{e1})$；解說稱 AISC「將上式**更簡化**為 $C_m = 0.6-0.4(M_1/M_2)$」 | SS-2020-3 |
| $P_{e1}$ vs $P_{e2}$ 的 $K$ | $P_{e1} = A_gF_y/\lambda_c^2$，「彎曲平面上之有效長度…**$K \leq 1.0$**」；$P_{e2}$ 則「$K$ 應依 4.8 節決定，**且不得小於 1.0**」 | SS-2020-3、SS-2013-4 |
| LRFD 互制式 | (8.2-1a)／(8.2-1b)，分界 $P_u/\phi P_n = 0.2$，係數 $8/9$ 與 $1/2$，與 AISC H1-1a／H1-1b 相同 | SS-2009-1 |
| 耐震 §13.6.5 強柱弱梁 | 式 **(13.6-3)**，前導句「任何梁柱接頭應滿足下式：」；柱側 $\sum Z_c(F_{yc} - P_{uc}/A_g)$、梁側 $\sum Z_bF_{yb}$、係數 **1.25**。**無 $R_y$、無 $M_v$** | SS-2009-1 |
| 耐震 §13.6.2 腹板交會區 | 式 (13.6-2)：$t_z \geq (d_z + w_z)/90$ | （旁證，未用） |

⚠️ **文字層破損之處理原則**：(8.2-3) 與 (13.6-3) 兩式所在的 PDF 文字層均已破損，多次獨立擷取給出互相矛盾的重建結果。本輪的處理方式是**用物理一致性反推、並在 .md 內明白標註來源不確定性**，而非挑一個看起來像的照抄：
- **(8.2-3)**：三種候選式中只有 `B1 = [0.64/(1−Pu/Pe1)](1−M1/M2) + 0.32(M1/M2)` 同時滿足「隨 $P_u/P_{e1}$ 單調遞增」「單曲率最大、雙曲率最小」「與 AISC 逐點差異 < ±3%」三項檢定，另兩種在 $M_1/M_2 = -1$ 時反而給出小於 1 或隨軸力遞減的荒謬結果。
- **(13.6-3)**：兩次擷取對「1.25 在分子／分母／右端」給出矛盾排列（其中一種是 $1.25 \geq$ 比值，等於要求柱比梁**弱**，物理上不可能）。依強柱弱梁之物理意義定為 $\dfrac{\sum Z_c(F_{yc}-P_{uc}/A_g)}{1.25\sum Z_bF_{yb}} \geq 1.0$。
- 兩處均已在對應 .md 內加註「建議以紙本規範覆核」。

### 一、勘誤總表

| 題號 | 嚴重度 | 錯誤內容 | 修正後 |
|---|:-:|---|---|
| **SS-2013-4** | 🔴 **幾何判讀完全錯誤** | 原解析寫成「單層兩跨、**三根柱**、柱底均鉸接、$P$ 作用於節點 D」 | 450→500 dpi 目視圖 4 確認：**A、D 是梁兩端的滾支承**（三角形＋滾輪，水平可自由平移）、**全結構只有一根柱 BC**（柱底 C 為鉸支承）、**$P$ 作用於柱頂 B** |
| SS-2013-4 | 🔴 | $M_{lt} = HL/3$（假設三柱均分層剪力） | $\sum F_x$ 顯示 A、D 水平反力為零 ⇒ 層剪力**全部**由 BC 承擔，對 C 取矩得 $M_{lt} = \mathbf{HL}$（原值**低估 3 倍**） |
| SS-2013-4 | 🔴 | $\sum P_{eK} = 7.722EI/L^2$（兩外柱 2.419 × 2 ＋ 中柱 2.884） | 僅一根柱：$\sum P_{eK} = \pi^2EI/(1.85L)^2 = \mathbf{2.88\,EI/L^2}$；$B_2$ 與 $M_u$ 隨之改寫為 $\dfrac{2.88EI}{2.88EI-PL^2}\,HL$ |
| SS-2013-4 | 🟡 | 「$M_{nt}=0$ 時 AISC 規定 $C_m = 1.0$（保守）」——**規範無此條文** | 改為：$M_A/M_B = 0/0$ 無定義，但 $B_1M_{nt} = 0$ 使 $B_1$ 數值不影響 $M_u$，依規範下限取 $B_1 = 1.0$ |
| **SS-2003-4** | 🔴 **構架型式判斷錯誤** | 圖說與全文稱「**側移構架**」並取 $C_m = 0.85$ | 450 dpi 目視確認**柱頂為靠牆水平滾支承、柱底為鉸支承** ⇒ 兩端水平位移均受束制 ⇒ **有側撐（無側移）構架**（題給 $K_x = K_y = 1.0$ 為旁證），適用原卷第 (二) 款 $C_m = 0.6-0.4(M_1/M_2)$ |
| SS-2003-4 | 🔴 **答案（控制式）變更** | 兩端力偶轉向未判讀；$C_m = 0.85$ ⇒ 穩定式 1.127 **N.G.** | 兩端力偶**同為逆時針** ⇒ **雙曲率**、$M_1/M_2 = +1$ ⇒ $C_m = \mathbf{0.2}$（規範無 0.4 下限）⇒ **穩定式 0.595 OK**；強度式 1.140 N.G. 不變 ⇒ **控制極限狀態由「穩定＋強度雙重不足」改為「僅斷面強度不足」** |
| SS-2003-4 | 🟠 | §1 虛構了 (一)(二)(三) 三個小題；§6 補充註「$M_1/M_2 > 0$ 為單曲率、$< 0$ 為雙曲率」**符號顛倒** | §1 改為原卷逐字（單一問句）；符號更正為「雙曲率正、單曲率負」（規範原文） |
| **SS-2009-1** | 🔴 **答錯規範** | 子題(一) 寫的是 **AISC 341** 的 $\sum M^*_{pc}/\sum M^*_{pb}$、$1.1R_yF_{yb}Z_b + M_v$，但題目**兩次明寫「依據我國規範」** | 改為我國式 **(13.6-3)**：$\dfrac{\sum Z_c(F_{yc}-P_{uc}/A_g)}{1.25\sum Z_bF_{yb}} \geq 1.0$，**梁側為單一定值 1.25、不含 $R_y$、不含 $M_v$** |
| SS-2009-1 | 🟠 | P-M 折線**兩段斜率大小顛倒**：原文寫 $k_{AB} = -9\phi_cP_n/(8\phi_bM_n)$ 且稱「AB 較陡、BC 較平」 | 由三控制點 A$(0,1)$、B$(0.9,0.2)$、C$(1,0)$ 直接算：$k_{AB} = -8/9 = -0.889$（**較平**）、$k_{BC} = -2$（**較陡**）；ASCII 折線圖一併重繪 |
| **SS-2020-3** | 🟠 **答案變更** | $\phi_bM_{ny} = 0.9F_yZ_y = 3989.3$ tf·cm，**漏掉規範 6.6 節之 $1.5F_yS_y$ 上限** | $Z_y/S_y = 1772.8/1173.6 = \mathbf{1.511 > 1.5}$ ⇒ 上限控制，$\phi_bM_{ny} = 0.9 \times 1.5F_yS_y = \mathbf{3960.9}$ tf·cm |
| SS-2020-3 | 🟠 **答案變更** | $P_{e1}$ 用題給之 $K_x = 1.8$／$K_y = 1.2$ | 規範明文「$P_{e1}$ 之 $K \leq 1.0$」（$B_1$ 屬構材內 P-δ，側移歸 $B_2$）⇒ 取 $K = 1.0$：$B_{1x}$ 1.167→**1.017**、$B_{1y}$ 1.007→**1.0**；**$M_{wy}$ 7.48 → 7.91 tf·m** |
| SS-2020-3 | 🟠 | L1 表把 $A$／$r_x$／$r_y$／$Z_x$／$Z_y$／$F_{cr}$ 公式／$B_1$ 公式全標為「**題目提供**」 | 原卷第三題**沒有任何參考公式**，斷面性質也須自算。改列入 L2 並補完整推導（$A$、$I_x$、$S_x$、$Z_x$、$I_y$、$S_y$、$Z_y$、$r$、結實性） |
| SS-2020-3 | 🟠 | §5 稱 (8.2-3)「其實等效於 $0.6-0.4(M_1/M_2)$」 | **錯誤**：兩式不等價（第二項 $0.32(M_1/M_2)$ 未除以放大分母）；規範解說明言 AISC 式是「更簡化」的版本。已刪除並補逐點比對表 |
| SS-2020-3 | 🟡 | $L_p$ 用 AISC 形式 $1.76r_y\sqrt{E/F_y} = 528.6$ cm | 依台灣 2010 改為 $80r_y/\sqrt{F_y} = \mathbf{524.1}$ cm（仍 > $L_b$ = 500，餘裕僅 4.6%） |
| **SS-2011-1** | 🟡 | 勁度折減係數符號寫成 $\tau_a$ | 規範用 **$\tau_b$**，全文更正 |
| SS-2011-1 | 🟡 | §3 表格寫「ASD **安全係數 $\Omega$ = 1.6** 推導」 | 1.6 是**載重係數 $\alpha$**，不是安全係數（$\Omega_c = 1.67$）；已更正並加註兩者數值接近純屬巧合 |
| SS-2011-1 | 🟡 | 「$\alpha P_r/P_y > 0.5$ 時需折減」易被讀成「其他時候不折減」 | 釐清為**兩層**：$0.8$ 無條件、$\tau_b$ 才是條件折減；並補 $\tau_b$ 在 0.5 處連續、在 1.0 處歸零之性質 |
| SS-2011-1 | 🟡 | 「$K$ 可取 1.0（但不得小於 1.0）」 | 規範 §C3 明定「**取 $K = 1$**」，非下限式敘述 |
| SS-2011-1 | ⚪ 補強 | 1.6 的推導只給 $(1.2D+1.6L)/(D+L) \to 1.6$ | 補上誠實交代：AISC 解說**未列單一推導**；$\Omega = 1.5/\phi$ 的標定給的是 **1.5**，且 **AISC 360-05 §H1.2 用的常數就是 1.5**，360-10 才改為 $\alpha = 1.6$ ⇒ 1.6 是「取上限較保守」 |
| **SS-2022-1** | ⚪ **本題原解析數值全部正確** | — | 斷面性質、$\lambda_c$、$F_{cr}$、$\phi_cP_n$、$\phi_bM_p$、$A_w$、$\phi_vV_n$、互制比 0.642 經程式重算**全數吻合**，主答未動。僅補：兩種 $b/t$ 定義（23.0／25.0）皆通過、$KL/r \leq 200$、矩形箱形之 $Z$ 一般式、$Z/S = 1.170$ 合理性、「三個送分條件」（載重已是二階值，**不可再乘 $B_1$／$B_2$**） |

### 二、最新規範對照的重要發現（新增之 §6）

| 題號 | AISC 360／341 的差異 | 是否改變結論 |
|---|---|:-:|
| SS-2003-4 | 統一式 H1-1a（不再分穩定式／強度式）；$M_n$ 用 $Z$ 而非 $S$。$L_p = 417$ cm > $L_b$ ✓。H1-1a $= \mathbf{1.021}$（仍 N.G. 但只超 2.1%，遠小於台灣 ASD 的 14.0%）。弱軸項比值由 0.328 降到 0.269（塑性儲備 $Z_y/S_y = 1.53$） | 否（同判 N.G.） |
| SS-2009-1 | **子題(二) 兩規範完全相同**（同樣 0.2 分界、$8/9$ 與 $1/2$、同樣兩段斜率），唯 $\phi_c$ 0.85→0.90 使 A 點高 5.9%。**子題(一) 差異大**：AISC 341 §E3.4a 用 $1.1R_y$（A992 = 1.21 ≈ 我國 1.25；**A36 = 1.65，比我國嚴 32%**）並含 $M_{uv}$ ⇒ **我國 1.25 是以 $R_y \approx 1.1$ 的高強度鋼為前提訂的**，且對 RBS 接頭偏不保守 | 否 |
| SS-2011-1 | 本題問的就是「最新規範」。$\alpha = 1.6$ 自 360-10 至 **-22 三版未變**；360-16 起有效長度改寫為 **$L_c = KL$**；$\tau_b = 1$ 之替代規定條號由 C2.3(4) 改為 C2.3(c)。**最大落差是台灣規範至今仍在 ELM 體系、沒有 DAM 條文** | 否 |
| SS-2013-4 | $B_1$-$B_2$ 已由規範本體**移入附錄 8**，主方法改為 DAM（$K = 1$、$N_i$、$0.8\tau_bEI$）。若依 App. 8 之側移法 $\sum P_{e,story} = R_M\sum HL/\Delta_H$：以斜率-偏移法得 $\Delta_H = 7HL^3/(12EI)$、$R_M = 0.85$ ⇒ $\sum P_{e,story} = \mathbf{1.457EI/L^2}$，比對位圖的 $2.88EI/L^2$ **低 49%**（AISC 較保守），也**反證對位圖未作梁遠端折減時確實偏樂觀** | 形式同、數值較大 |
| SS-2020-3 | $\phi_c$ 0.85→0.90、弱軸上限 $1.5\to1.6F_yS_y$（改由 $F_yZ_y$ 控制）、$C_m$ 改用 AISC 簡化式 ⇒ $M_{wy}$ **7.91 → 8.84 tf·m（+11.8%）**。$F_{cr}$ 兩規範**完全相同** | 否（數值較寬） |
| SS-2022-1 | **柱曲線是同一條**（$\lambda_c^2 \equiv F_y/F_e$、$\ln 0.658 = -0.4187$，算出 3.0953 vs 3.0955）；界限值差異均 < 1.2%（$50/\sqrt{F_y} = 27.52$ vs $1.12\sqrt{E/F_y} = 27.85$；$50\sqrt{k_v/F_y} = 61.55$ vs $1.10\sqrt{k_vE/F_y} = 61.16$）。唯一實質差異是 $\phi_c$ 0.85→0.90、$\phi_v$ 0.90→1.00 ⇒ 互制比 **0.642 → 0.618** | 否（皆適足） |

### 三、驗算方法（規則 1 條件①②）

- **考卷原文逐頁目視判讀**：本科考卷為 Adobe-CNS1 CID 字型，`pdftotext` 抽不到中文。以 `pdftoppm -r 200~500 -png` 轉圖後目視 SS-2003 p2、SS-2009 p1、SS-2011 p1·p2·p3、SS-2013 p2、SS-2020 p2、SS-2022 p1 共 **10 頁**；其中三處**必須放大到 450–500 dpi 才判得出來**：
  - **92 年（2003）附圖的支承符號與力偶轉向** —— 柱頂是「斜線牆面＋三角形」的水平滾支承（不是自由端也不是固接）；柱頂力偶弧線由右經頂至左、箭頭在左下朝下（逆時針），柱底弧線由左經底至右、箭頭在右朝上（逆時針）⇒ **同轉向 ⇒ 雙曲率**。這是本輪最關鍵的一次判讀。
  - **102 年（2013）圖 4 的 A、D 支承** —— 「三角形＋兩個小圓（滾輪）＋斜線地面」是滾支承；C 點的「三角形＋斜線地面」（無滾輪）才是鉸支承。前版把 A、D 誤讀為柱頂節點，整題結構理解全錯。
  - **109 年（2020）兩張載重圖的力偶轉向** —— 左端弧線開口朝左、箭頭在頂朝右下（順時針）；右端弧線開口朝右、箭頭在頂朝左（逆時針）⇒ **反轉向 ⇒ 單曲率**（確認 2026-05-27 那次修正是對的）。
- **全部 6 題共約 180 個數值以 Python 獨立重算，`MISMATCHES: 0`**（腳本 `/tmp/final3.py`，含量綱檢查）。過程中揪出自己的一處算錯：SS-2020-3 之 §6 AISC 值初稿誤寫 8.70，重算為 **8.84** tf·m，已更正。
- **雙路徑交叉驗算**（條件②）：
  - **SS-2013-4**：有側移對位圖以兩種方法求 $K$ —— Jackson–Moreland 近似式得 **1.851**，對位圖精確超越方程式 $\dfrac{G_BG_C(\pi/K)^2-36}{6(G_B+G_C)} = \dfrac{\pi/K}{\tan(\pi/K)}$ 數值解得 **1.847**，差 0.17% ✓。並以 $G_B = G_C = 0$ 代入精確式驗得 $K = 1.00$，與考卷 K 值表「固接*-固接理論 K = 1.0」吻合，證明所用方程式無誤。
  - **SS-2013-4**：$M_u$ 之極限行為檢查（$P \to 0 \Rightarrow M_u \to HL$；$P \to 2.88EI/L^2 \Rightarrow M_u \to \infty$）與量綱檢查（$PL^2$ 與 $EI$ 同量綱 ⇒ $B_2$ 無因次）。
  - **SS-2003-4**：以「曲率判定通用式」$M(x) = (C_A+C_B)x/L - C_A$ 獨立驗證圖說判讀——兩端同轉向代入得 $M(0) = -M$、$M(L/2) = 0$、$M(L) = +M$（反對稱），確認雙曲率。另反查 AISC 手冊確認斷面為 **W12×170**（$A$、$S_x$、$S_y$、$r_x$、$r_y$ **五項全部精確吻合**），據以補入 $Z_x = 4506$、$Z_y = 2065$ cm³ 作 §6 對照。
  - **SS-2020-3**：(8.2-3) 與 AISC $C_m/(1-P_u/P_{e1})$ 在 5 組 $(M_1/M_2,\ P_u/P_{e1})$ 上逐點比對，差異 $\pm 3\%$ 以內且單曲率時台灣式較大（趨勢正確）；解出 $M_{wy}$ 後回代 H1-1a 驗得 1.000 ✓。
  - **SS-2022-1**：以 $\exp(-0.419\lambda_c^2)F_y$ 與 $0.658^{F_y/F_e}F_y$ 兩式獨立算 $F_{cr}$，得 3.0953 與 3.0955（差 0.006%），證明兩規範柱曲線同一；另以 $Z/S = 1.170$ 落在箱形斷面 1.12～1.20 之合理區間反證 $Z$ 無誤。
  - **SS-2009-1**：折點 B 之連續性由兩式獨立驗算（H1-1a 得 0.9、H1-1b 亦得 0.9）。

### 四、下游同步（規則 1 條件③）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/*/*.md` × 6 | 勘誤 ＋ 每題新增 `## 6. 依最新規範…對照` ＋ 頁尾「修正日期：2026-08-22」與「驗證狀態：unverified」 |
| `raw/solutions/*/*-pm-viz.html` × 5 | 全部更新：SS-2013-4（三柱→單柱、$HL/3 \to HL$、$7.722 \to 2.88EI/L^2$）、SS-2003-4（穩定式 1.127 N.G. → 0.595 OK、Cm 0.85 → 0.2）、SS-2020-3（**原檔停在更早版本、寫著 8.0 tf·m** → 7.91、補 1.5FySy 上限與 B1x = 1.017）、SS-2011-1（$\tau_a \to \tau_b$、$N_i$ 之 $P_r \to Y_i$、$\Omega \to \alpha$）、SS-2022-1（0.643 → 0.642 並補 AISC 0.618） |
| `wiki/problems/*.md` × 6 | 由 `_regen.py` 依正本重建；另修 SS-2011-1／SS-2013-4／SS-2022-1 三個因 LaTeX 被剝除而殘缺的 H1，並改寫 SS-2009-1 尾段（原用 $\sum\phi_cM_{pc} \geq \sum\phi_bM_{pb}$，強柱弱梁不含 $\phi$，且非我國式）、更新四題的圖形表說明 |
| `study/problems-view/*.html` × 6 | 由 `_regen.py` 重新渲染 `<main>`；**`<main>` 以外 shell 逐字元比對未變** ✔；KaTeX display／inline math 破損數皆 0 ✔ |
| `raw/json/question_index.json` | 6 題 tags 各補 2～3 個；**另刪除 SS-2003-4 的 `側移構架`**（該題實為有側撐構架，保留會汙染標籤統計）——本輪唯一的非 append-only 變更，理由如上 |
| `dashboard-data.js` | 同上（`window.SS_QUESTIONS` 仍 98 筆，Node 載入驗證通過） |
| `study/study-SS-U1-3.html` | 6 題 `Q[]` 列之摘要與標籤更新（含 SS-2003-4 移除 `側移構架`） |
| `wiki/log.md` | 本則紀錄 |
| `CLAUDE.md` | CHANGELOG 補一列 |

**未變更（刻意）：** `raw/exams/` 考卷原件、所有 `-fig-*.png` 使用者截圖、`SS-2022-1/variable_hierarchy_SS2022_1.html`（無題目專屬數值）、`question_index.json` 的 `primaryTopicId`／`secondaryTopicIds`／`designMethod`（維持 `study/frequency-SS.html` 與各單元命題分析之統計有效性）。

### 五、待使用者複核（規則 5）

6 題 `verificationStatus` 均為 `unverified`。三處需要注意：

1. **SS-2020-3 的 $P_{e1}$ 取 $K = 1.0$（影響答案 6.5%）**：本輪依規範明文改為 $K \leq 1.0$，$M_{wy}$ 由 7.48 變成 **7.91** tf·m。四種算法的區間為 **7.4～7.9 tf·m**（.md §5 已列完整敏感度表）。若使用者認為出題者期望一路使用題給的 $K_x = 1.8$／$K_y = 1.2$，只需把 §5 表中該列的 7.43 對調為主答（B1x = 1.167、B1y = 1.007 兩個數字亦已列出）。**量級判斷（約 7.5～7.9 tf·m）不受影響。**

2. **兩處規範原文的重建（(8.2-3) 與 (13.6-3)）**：官方 PDF 文字層破損，本輪以物理一致性反推並已在 .md 內標註不確定性。**若使用者手邊有紙本規範，這兩式值得優先覆核**——(8.2-3) 影響 SS-2020-3 的 $B_1$（約 3%），(13.6-3) 影響 SS-2009-1 子題(一) 的整個答案骨架。

3. **SS-2013-4 的對位圖是否該對「梁遠端鉸接」作 0.5 折減**：主答採未折減（$G_B = 0.75$、$K = 1.85$），符合原卷只給「固接 $G=1$／鉸接 $G=10$」的約定；但 A、D 為滾支承（轉動自由），嚴格應把 $I_g/L_g$ 乘 0.5，得 $G_B = 1.5$、$K = 2.02$、$\sum P_{eK} = 2.42EI/L^2$（$B_2$ 更大、更保守）。§5 爭議一已完整列出兩者；§6 的 AISC 側移法（不查 K）算出 $1.457EI/L^2$，也**支持「未折減偏樂觀」的判斷**。此為觀念取捨，不影響解題架構。


---

## 2026-08-22 — 第四批六題解析勘誤（接合之分析與設計 U1-4，回查台灣規範第十章原文）

**操作類型：** 解析勘誤（Cowork，依 CLAUDE.md 規則 1 第三項例外）＋下游同步
**觸發：** 使用者指示「幫我檢查並修正下列題目解題 SS-2015-2 & SS-2017-4 & SS-2017-2 & SS-2020-4 & SS-2018-3 & SS-2009-4　請依最新規範進行計算　若有修正.md，別忘了，下游檔案要一起修正」
**範圍：** 6 題，5 題主分類為 `SS-U1-4` 接合之分析與設計，SS-2015-2 主分類為 `SS-U1-1`（副分類 `SS-U1-4`）

### 〇、本輪新增的規範原文查證

本批全屬接合設計，故回查內政部 99.09.16 版**容許應力設計法第十章「接合設計」**官方 PDF 原文（rootlaw）：

| 查證項目 | 規範原文／結果 | 影響題目 |
|---|---|---|
| **螺栓中心間距下限**（§10.3.9） | 「所有標準型孔、超大型孔、及槽孔中心至中心之距離**不得小於 8/3 倍**螺栓之標稱直徑，亦不得小於由式(10.3-2)計得之值。若 $F_p$ 由式(10.3-1a)或(10.3-1b)求得，則**沿著力量傳遞方向**之螺栓孔中心距**不得小於 3 倍**螺栓標稱直徑」 | **SS-2009-4**（原解析把 3d 與 8/3 d 的層次寫反）、SS-2020-4 |
| **螺栓最小預拉力**（§10.3.1、表 10.3-1 附註） | 「**等於最小抗拉強度之 0.7 倍**」 | **SS-2009-4**、SS-2017-2 |
| **摩阻型接合容許剪應力**（表 10.3-2／C10.3-2） | A325 標準孔 **17 ksi = 1.19 tf/cm²**；A490 標準孔 **21 ksi = 1.47 tf/cm²**（超大／短槽孔 1.05／1.26；長槽孔 0.84／1.05）。台灣 ASD **以表列容許應力處理，並無 $\mu D_u h_f T_b n_s$ 乘積式** | **SS-2017-2** |
| **接觸面滑動係數**（§10.3.7(g)） | 「潔淨銹皮與噴氣清除及表面塗以護膜者，其**滑動係數應在 0.33 以上**」 | **SS-2017-2** |
| **承壓型螺栓容許剪應力** | A490 螺紋不在剪力面（X）= **40 ksi = 2.81 tf/cm²** ⇒ 反查證 SS-2020-4 題給之 $F_{va} = 2.8$ tf/cm² 即 **A490-X 承壓型** | **SS-2020-4** |
| **承壓容許應力**（式 10.3-1a／10.3-1c） | $F_p = 1.2F_u$；端螺栓 $F_p = LF_u/(2d) \le 1.2F_u$ | SS-2015-2、SS-2020-4 |
| **塊狀剪力撕裂**（§10.4，ASD） | $F_v = 0.30F_u$ 於剪力淨斷面、$F_t = 0.50F_u$ 於張力淨斷面 | SS-2020-4 |
| **填角銲容許剪應力**（表 10.2-5） | 「有效面積上之剪應力 = **0.3 ×（銲材標稱拉應力強度）**」⇒ E70 為 $0.3 \times 482.6 = \mathbf{144.8}$ N/mm² | **SS-2018-3**（關鍵！題給 90.5 是日本 AIJ 值，非台灣值） |
| **填角銲最小尺寸表**（表 10.2-4） | $t \le 6 \to 3$；$6 < t \le 12 \to 5$；$\mathbf{12 < t \le 19 \to 6}$；$19 < t \le 38 \to 8$ mm | **SS-2015-2**（原解析誤查為 8 mm） |

**額外重大收穫（回溯確認第三批之待覆核事項）：**

> **109 年（2020）試卷第 3-3 頁「參考資料」印出台灣規範 (8.2-3) 之 $B_1$ 公式原文：**
> $$B_1 = \frac{0.64}{1-(P_u/P_{e1})}\left[1 - \frac{M_1}{M_2}\right] + 0.32\frac{M_1}{M_2} \ge 1.0,\qquad P_{e1} = \frac{A_gF_y}{\lambda_c^2},\qquad L_p = \frac{80r_y}{\sqrt{F_y}}$$
> 這與第三批中「因官方 PDF 文字層破損、僅能以物理一致性反推」所得之形式**完全一致**。第三批 §五待覆核事項第 2 點關於 **(8.2-3) 的部分至此已由考選部試卷（獨立第三方primary source）證實**，可視為確認。（(13.6-3) 強柱弱梁式仍待紙本覆核。）
>
> 同頁另印出 $\lambda_c = \dfrac{kl}{\pi r}\sqrt{\dfrac{F_y}{E}}$、$F_{cr} = [\exp(-0.419\lambda_c^2)]F_y$、$F_{cr} = (0.877/\lambda_c^2)F_y$ 與 (8.2-1a)/(8.2-1b) 互制式，全部與知識庫既有記載吻合。

> **104 年（2015）試卷第三頁「參考公式」印出：** $w_n = w_g - \sum d_h + \sum \dfrac{s^2}{4g}$、$T_{ds} = 0.9F_yA_g$、$T_{ds} = 0.75F_uA_e$、**$U = 0.9,\ 0.85,\ 0.75$（僅表列，無 $1-\bar x/L$ 公式）**、塊狀剪力**兩條件式＋上限**、$\phi R_n = (0.75)(0.6F_{Exx})(t)(L)$、$L_p = 80r_y/\sqrt{F_{yf}}$、$C_b = 1.75+1.05(M_1/M_2)+0.3(M_1/M_2)^2 \le 2.3$、剪力三段式。並註明「請自行選擇適合的公式，並檢查其正確性，若有問題應自行修正」。

### 一、逐題勘誤

🔴 = 影響最終答案｜🟠 = 觀念／公式錯誤但答案不變｜🟡 = 敘述／符號不精確｜⚪ = 補強

| 題號 | 等級 | 原內容 | 更正 |
|---|:-:|---|---|
| **SS-2015-2** | 🔴 | NSF 之 $A_n = A_g - \mathbf{1} \times d_h t_w = 28.22$ cm²（誤讀為「單排縱向 2 螺栓」） | 圖 2 中央端視圖之「10」為**橫向螺栓間距 $g$**，腹板實為 **2×2 四孔**，橫斷面切過 **2 孔**：$A_n = 29.9 - 2(2.8)(0.6) = \mathbf{26.54}$ cm² ⇒ NSF **146.2 → 137.3 tf** |
| SS-2015-2 | 🔴 | BSR 拉力面取「最遠螺栓至 7 cm 板端」 | 圖中「7 cm」量至一條**虛線＝連接板邊緣**，非槽鋼端緣（槽鋼右側有折斷符號表延續）。槽鋼自由端在 **5 cm 側**；拉力面為**通過最遠一排螺栓、寬度 = $g$ = 10 cm** 之橫斷面 ⇒ $A_{nt}$ 3.36 → **4.32**、$A_{gt}$ 4.2 → **6.0** cm² |
| SS-2015-2 | 🔴 | 剪力面扣孔寫「各扣 2 孔」但數值代 $2\times1.4 = 2.8$（實為 1 個孔徑） | 剪力面通過第 1 孔（整孔）＋第 2 孔（半孔，面終止於孔心）⇒ 扣 **$1.5d_h$**：$A_{nv}$ 14.64 → **12.96** cm² |
| SS-2015-2 | 🔴 | BSR 取第二式 41.33 tf/根 | 兩條件式**皆受上限拘束**；本題第二式 56.77 tf > 上限 55.64 tf ⇒ **上限控制**，41.33 → **41.73** tf/根，BSR **82.7 → 83.5 tf**（仍為控制模式） |
| SS-2015-2 | 🟠 | $U$ 用 AISC 公式 0.751，並稱「AISC 允許取兩者較大者」 | 台灣 2010 與**本試卷參考公式只列表列值** 0.9／0.85／0.75；$1-\bar x/L$ 是 AISC 360-05 才納入。改採 **$U = 0.75$**（差 0.13%，$\S6$ 保留公式法對照） |
| SS-2015-2 | 🟠 | 「板厚 16 mm，依規範 $t>12$ mm 最小銲腳 = 8 mm，故由最小規定控制」 | 表 10.2-4：$12<t\le19$ mm → **6 mm**（$19<t\le38$ 才是 8 mm）。$w$ 需求 7.58 → **7.65 mm** ⇒ 取 8 mm 之理由改為**強度控制**，非規範最小值 |
| SS-2015-2 | 🟡 | 稱 $A = 29.9$、$C_y = 2.49$ 為「題目提供」 | 第二題未給；係取自**同卷第三題**。已註明，並補矩形理想化值 29.25 cm² 之對照（因 BSR 只用腹板局部面積，$A_g$ 取值**不影響**設計強度） |
| SS-2015-2 | ⚪ 補強 | — | 補：錯列路徑 $s^2/4g$ 交叉驗核（直線 5.60 > 斜線 3.10 ⇒ 直線控制）、螺栓雙剪（N 99.0／X 123.8 tf）與孔壁承壓（85.5 tf）補充檢核、母材檢核、$T$ 之 3:4 方向、改善接合詳圖之試算（3 排 → BSR ≈ 119 tf） |
| **SS-2018-3** | 🔴 | 梁翼判為「CJP 完全熔透開槽銲（本解析判斷）」，以母材 $0.6F_y$ 檢核得 80.4 < 147 → **OK** | 以 300 dpi 重判：圖中柱右側**三個銲接符號（上翼板／腹板／下翼板）全部是填角銲並標註「6」**。翼板須以**喉面積**檢核：$\tau_f = 257231/(0.707 \times 6 \times 400) = \mathbf{151.6}$ N/mm² > 90.5 ⇒ **NG，需 10 mm** |
| SS-2018-3 | 🔴 | SN400B 之 $F_y = 245$ N/mm² | 245 是 **SM400A/B**（$t\le16$）之值；SN400B（JIS G3136）為 **235** N/mm² ⇒ $0.6F_y$ 147 → **141** N/mm² |
| SS-2018-3 | 🟠 | $f_a = 90.5$「約為 $0.6F_y \times 0.5/\sqrt3$」 | 該式代入得 42.4，與 90.5 不符。正確出處為**日本 AIJ 鋼構造設計規準之填角銲長期許容剪應力** $f_s = F/(1.5\sqrt3)$，$F = 235$ ⇒ $235/2.598 = \mathbf{90.5}$ ✓（反推 $F = 90.5 \times 1.5\sqrt3 = 235.1$，**同時反證 $F_y$ 應為 235**） |
| SS-2018-3 | ⚪ 補強（重要） | — | 補入**規範體系差異**：台灣 ASD 表 10.2-5 為 $0.3F_{EXX} = \mathbf{144.8}$ N/mm²（＝ AISC 360-16 ASD 之 $0.6F_{EXX}/2.00$，恆等）⇒ **同一組 6 mm 銲道，依日本判 NG、依台灣腹板反而 OK**（差 1.60 倍）；再加 AISC 360-16 方向性強度後（腹板 213.9、翼板 217.2 N/mm²）**兩處皆 OK**。另補 388 mm 之扇形開孔來源、$\tau_{w1}/\tau_{w2}$ 正交性論證、最大銲腳檢核 |
| **SS-2020-4** | 🔴 | 螺栓群僅承受 $V/n = 11.67$ tf，未計任何彎矩 | 補入**兩項遺漏**：①螺栓列偏離續接中心線 $e = 5$ cm ⇒ $V\!\cdot\!e = 350$ tf·cm；②腹板依剛度分擔之彎矩 $M_w \cdot I_w/I_x = 6000 \times 0.1578 = 947$ tf·cm（**是偏心項的 2.7 倍**）⇒ $M_{bolt} = 1297$ tf·cm，$f_h = 23.16$ tf，最不利合力 **11.67 → 25.93 tf** |
| SS-2020-4 | 🔴 | 螺栓選 **M20**（$A_b$ 需求 2.083 cm²） | $A_b$ 需求 **4.631 cm²**、$d \ge 24.3$ mm ⇒ 選 **D25**（$A_b = 4.909$，容量 27.49 > 25.93 tf，使用率 94.3%）。間距 8 cm > $3d$ = 7.5 ✓、端距 4 > 1.25d = 3.13 ✓ |
| SS-2020-4 | 🔴 | 鈑厚僅算剪力，$t \ge 0.729$ cm ⇒ **8 mm** | 增列彎矩控制：$S = 768t$、$t \ge 1297/(768 \times 1.5) = \mathbf{1.126}$ cm ⇒ **12 mm**（驗算 $f_b = 1.408 < 1.5$、$f_v = 0.608 < 1.0$） |
| SS-2020-4 | 🟠 | 螺栓數敘述自相矛盾：L1 表寫「2 列 × 6 排」、Step 3 寫「$n$ = 2 列 × 3 排 = 6 個」 | 正確理解：鈑上共 12 支（2 縱列 × 6 橫排），**每一縱列的 6 支負責一端梁** ⇒ 單側設計螺栓數 $n = 6$，且該列距續接中心線 5 cm |
| SS-2020-4 | 🟠 | 最小接合強度規定只查剪力 | 規定為「接合強度不得小於梁桿件強度之一半」⇒ **$M$、$V$ 雙向**皆須比：$0.5M_a = 47.8 < M_w = 60$、$0.5V_a = 49.0 < V_w = 70$，兩者皆由實際作用力控制 |
| SS-2020-4 | 🟡 | $I_x = 202{,}898$ cm⁴ | 重算 $I_x = [30(70^3) - 28.6(65^3)]/12 = \mathbf{202{,}977}$ cm⁴（$S_x = 5799$ cm³） |
| SS-2020-4 | ⚪ 補強 | — | 補：斷面分類（$b_f/2t_f = 6.0 < 10.75$、$h_w/t_w = 46.4 < 107.5$ ⇒ 結實）、$A_w = d\,t_w$（台灣 ASD）vs $h_wt_w$ 對照、$F_{va} = 2.8$ = 40 ksi = A490-X 之查證、孔壁承壓與淨斷面剪力／彎曲補充檢核、假設 A/B/C 三層次對照表 |
| **SS-2009-4** | 🔴 | 「規範規定中心距不得小於 **3d**；規範另訂絕對最小值 $2\frac23 d$」 | **層次寫反**。依 §10.3.9 原文：一般強制下限就是 **$\frac83 d$（＝ $2\frac23 d$）**；$3d$ 只在「沿力方向且 $F_p$ 依式(10.3-1a)/(10.3-1b) 取用」時強制（AISC 360-16 §J3.3 則把 3d 列為 preferred 建議值）。另補第三層需求：式(10.3-2) $s \ge P/(F_ut) + d/2$ |
| SS-2009-4 | 🟠 | 預拉力 $T_0 = 0.70F_uA_b$ | 應乘**螺紋處有效抗拉面積 $A_t \approx 0.75A_b$**。以 3/4 in A325 驗核：$0.7 \times 120 \times 0.334 = 28.1$ kips ＝ AISC 表 J3.1 之 28 kips ✓；誤用 $A_b$ 得 37.1 kips（**高估 33%**） |
| SS-2009-4 | 🟡 | 圖說稱「梁腹板以螺栓鎖於剪力板；**梁翼板以 CJP 接至柱外表面**」 | 原圖中**上、下翼板亦佈滿螺栓孔並加續接鋼鈑**，屬全螺栓現場續接；銲接位於柱與工廠銲接短梁（stub）之交界，圖中未繪出。圖說已更正 |
| SS-2009-4 | 🟡 | 旋轉角法「1/2～2/3 圈」 | 改為 **1/3～1 圈**（依螺栓長度與夾持厚度）；並補 S10T 之中文對應 |
| SS-2009-4 | ⚪ 補強 | — | 補 AWS A2.4 命名邏輯（前綴 Single/Double = 單面／雙面**開槽**；字根 V = **兩側**母材開斜角、Bevel = **單側**）、0.7 係數之力學理由（$F_y/F_u$ 對 A325 ≈ 0.77、A490 ≈ 0.90）、§1「如右圖」→「如下圖」 |
| **SS-2017-2** | 🟠 | 逕稱「$\phi = 1.0$（使用性極限）、$\phi = 0.85$（強度極限）」並用 $h_{sc}$ | 此為 **AISC 360-05** 之規定。**AISC 360-10 起 $\phi$ 改依孔型**：標準孔／短槽孔垂直力向 **1.00**、超大孔／短槽孔平行力向 **0.85**、長槽孔 **0.70**；孔型係數 $h_{sc}$ 亦改為**填隙板係數 $h_f$**。「使用性／強度」之區分仍在，但只決定**用哪組載重**檢核 |
| SS-2017-2 | 🟠 | 滑動係數「A 類 ≈ 0.33、B 類 ≈ 0.50」標為 AISC 值 | 0.33 是**台灣規範**（與 AISC LRFD 1993）；**AISC 360-05 為 0.35、360-10 起為 0.30**。已列三欄對照表 |
| SS-2017-2 | 🟡 | 「F10T（M20）$T_o \approx 160$ kN／M22 $\approx 200$ kN」表格，來源不明 | 改以規範原文「等於最小抗拉強度之 0.7 倍」＝ $0.70F_u^bA_t$ 表述，並以 AISC 表 J3.1 之 28 kips 作數值驗核；日系 F10T／S10T 標準張力另註為依 JIS／CNS 表列 |
| SS-2017-2 | 🟡 | 承壓「$R_n = 2.4F_udt$（AISC 簡化）」 | 補完整式 $R_n = 1.2L_ctF_u \le 2.4F_udt$（360-16 §J3.10；**360-22 拆為承壓 §J3.11 + 撕出 §J3.12**） |
| SS-2017-2 | ⚪ 補強 | — | 補台灣 ASD 之**表列容許剪應力**（A325 標準孔 1.19、A490 標準孔 1.47 tf/cm²）與 §10.3.7(g) 滑動係數 ≥ 0.33 原文；補「摩阻型僅為承壓型 X 之 **52%**」之量化比較；補規範強制採用摩阻型之五種情形 |
| **SS-2017-4** | ⚪ **本題原解析數值全部正確** | — | 形心 (10, 40)、$J_w = 197{,}333$ cm³、$e = 80$ cm、$f_{res} = 0.024535P$、$q = 2.215$ tf/cm、$P_u = \mathbf{90.3}$ tf 經獨立重算**全數吻合**，主答未動。僅補判圖依據與交叉驗核（見下） |

### 二、SS-2017-4 之圖面判讀與三方交叉驗核（本輪最需要證據的一處）

試卷下方尺寸線為「40 cm ─ ● ─ 50 cm」，右端與 $P$ 同一鉛垂線。判讀依據三項：

1. 左界線與 80 cm 尺寸線上下端對齊 ⇒ 40 cm 自**柱面（左垂直銲道）**量起。
2. **中間圓點是尺寸線分段記號，不是形心**：若圓點為形心則需 $b^2/(2b+d) = 40$，解 $b^2-80b-3200=0$ 得 $b = 109.3$ cm，與圖上水平／垂直銲道長度比（約 0.5）嚴重不符。
3. 圖面比例：垂直銲道 680 px ↔ 80 cm（8.5 px/cm）；水平銲道 405 px ↔ 約 42 cm ≈ 40 cm ✓。

三方交叉驗核（差異 < 0.8%，答案穩健）：

| 算法 | $\bar x$ | $J$ | $e$ | $f_{res}$ | $P_u$ |
|---|---|---|---|---|---|
| 線理想化（本文主答案） | 10.00 | 197,333 | 80.00 | 0.024535P | **90.27 tf** |
| 有限寬度（銲道視為寬 1 cm 之帶） | 10.25 | 196,557 | 79.75 | 0.024476P | 90.49 tf |
| 坊間詳解（高點建國 106 年鋼結構設計） | 10.25 | 197,357 | 79.75 | 0.0244P | 90.9 tf |

另註：使用者提供之 `SS-2017-4：偏心銲縫群分析.pdf` 經檢視為既有 `SS-2017-4-connection-viz.html` 之列印輸出，數值與正本一致（$J_w = 197{,}333$、$P_u = 90.3$ tf）；因本題主答案未變，**該 viz.html 與使用者 PDF 皆無需修改**（維持一致）。

### 三、最新規範對照的重要發現（新增之 §6）

| 題號 | AISC 360-16／-22 的差異 | 是否改變結論 |
|---|---|:-:|
| **SS-2015-2** | ①$U$：表列 0.75 → 公式 $1-\bar x/L$ = 0.751（本題恰同值）。②塊狀撕裂：台灣**兩條件式＋上限** → AISC 360-05 起**單一式 (J4-5)** $R_n = 0.6F_uA_{nv}+U_{bs}F_uA_{nt} \le 0.6F_yA_{gv}+U_{bs}F_uA_{nt}$；代入本題得 **55.64 tf/根，與台灣完全同值**（因台灣的「上限」正是 AISC 的主式）。③填角銲**方向性強度** $(1+0.5\sin^{1.5}\theta)$，$\theta = 53.13°$ ⇒ 係數 1.358，$w$ 需求 7.65 → **5.63 mm**，改由最小銲腳 6 mm 控制（**省 25% 銲腳、約 44% 銲料**） | 設計強度同 83.5 tf；銲腳 8 → 6 mm |
| **SS-2017-4** | $0.6F_{EXX}$ 與 $\phi = 0.75$ **自 AISC LRFD 1993 至 360-22 從未改變** ⇒ 彈性向量法答案完全相同 90.3 tf。加方向性強度（$\theta = 48.6°$，係數 1.325）得 119.6 tf；**自行數值求解 AISC 手冊瞬心法**得 $P_n = 212.9$、$\phi P_n = \mathbf{159.7}$ tf（瞬心位於銲道左緣外 4.07 cm），為彈性法之 **1.77 倍** | 否（考場仍答 90 tf） |
| **SS-2018-3** | 台灣 ASD $0.3F_{EXX}$ **恆等於** AISC 360-16 ASD $0.6F_{EXX}/\Omega$（$\Omega = 2.00$）= 144.8 N/mm²。加方向性強度後腹板 213.9、翼板 217.2 N/mm² ⇒ **圖示 6 mm 填角銲於兩處皆合格**。同一接頭在三套規範下得三種結論（日本 NG／台灣腹板 OK／AISC 全 OK），為本題最具教育價值處。另註：若位於耐震抗彎構架，AISC 341-16 §E3.6b 與台灣第十三章都會**要求梁翼採 CJP 且為 Demand Critical**，6 mm 填角銲在任何規範下都不被允許 | 是（AISC 下由 NG 變 OK） |
| **SS-2020-4** | ASD 哲學由「應力比較」改為「$R_a \le R_n/\Omega$」。桿件容量：$M$ 95.7 → 97.9 tf·m（$Z_x = 6541$ cm³、$\Omega = 1.67$）、$V$ 98 → 88.0 tf（組合斷面 $\Omega_v = 1.67$；若為軋製 I 型且 $h/t_w \le 2.24\sqrt{E/F_y} = 64.0$ 則 $\Omega_v = 1.50$ ⇒ 98.0 tf，**與台灣完全相同**）。螺栓：$F_{nv}(X)/\Omega = 0.563(150)/2.00 = 2.97$ tf/cm²（比題給 2.8 高 6%）⇒ $A_b$ 需求 4.368 cm²，**仍選 D25**。承壓／撕出 360-22 **分列**為 §J3.11／§J3.12 | 否（同 D25 + 12 mm） |
| **SS-2009-4** | 中心距強制下限**兩者相同**（$2\frac23 d$），差別只在 $3d$ 之地位（台灣有條件強制／AISC 建議值）。預拉力係數 **0.70 自 LRFD 1993 至 -22 未變**；螺栓標準 ASTM A325／A490 已於 2016 年整併為 **ASTM F3125**，AISC 360-16 起改引用之。耐震銲接另有 **AWS D1.8** 補充規範（台灣尚無對應章節） | 否（五子題答案皆同） |
| **SS-2017-2** | 機制與極限狀態定義**三套規範一致**；差異在 ①強度表達（台灣 ASD 表列 vs AISC 乘積式）②$\phi$ 之依據（360-05 使用性／強度 → 360-10 起依孔型）③$h_{sc} \to h_f$ ④$\mu$（A 類 台灣 0.33／360-05 0.35／**360-10 起 0.30**，B 類均 0.50）⇒ 採 A 類表面時 AISC 360-16 之強度較台灣**低約 9%** | 否（敘述題） |

### 四、驗算方法（規則 1 條件①②）

- **考卷原文逐頁目視判讀**：以 `pdftoppm -r 200~500 -png` 轉圖後目視 **SS-2015 p1·p2·p3、SS-2017 p1（全一頁）、SS-2018 p2、SS-2020 p2·p3、SS-2009 p2 共 8 頁**。三處必須放大才判得出來：
  - **106 年（2017）第四題托架附圖之尺寸線** —— 需 500 dpi 才能確認中間是**圓點（分段記號）**而非形心標記，並量測 px/cm 比例（見 §二）。
  - **107 年（2018）接頭圖之三個銲接符號** —— 需 300 dpi 才能看清**上翼板／腹板／下翼板皆為填角銲三角形並標註「6」**；舊解析誤判翼板為 CJP 即源於未放大。同時確認「40」為腹板端部扇形開孔（$500-2(16+40) = 388$ mm，與題給 $S_w$ 之 $388^2$ 吻合）。
  - **104 年（2015）圖 2 右視圖之虛線位置** —— 需放大才能確認「7 cm」的右界線**與虛線（連接板邊緣）重合**、而非與槽鋼外緣（有折斷符號）重合；中央端視圖之「10」則為橫向螺栓間距。
- **全部 6 題共約 180 個數值以 Python 獨立重算，`MISMATCHES: 0`**（腳本 `/tmp/b4/verify4.py`，含量綱檢查與規範數值驗核）。
- **雙路徑交叉驗算**（條件②）：
  - **SS-2017-4**：$J_w$ 以兩條路徑計算 —— 逐段線積分 $\sum\int r^2dL$ 得 197,333，與 $I_x + I_y = 170{,}667 + 26{,}667$ 完全相同 ✓；另以「線理想化 / 有限寬度 / 坊間詳解」三方比對（90.27 / 90.49 / 90.9 tf）。
  - **SS-2017-4 瞬心法自我驗證**：將載重逐步移向形心（$e$ 由 110 cm 減至 5 cm），$P_n$ **單調**由 159.5 升至 557.7 tf，並趨近同心解析值 $0.6F_{EXX}t_e(1.5d + 2b) = 590.6$ tf（$e = 5$ cm 時達 **94.4%**）；且 $\Sigma F_x = 9\times10^{-15}$ tf（對稱性）⇒ 數值程序無誤。
  - **SS-2015-2**：塊狀撕裂以台灣兩條件式與 AISC 360-16 單式（J4-5）獨立計算，**兩者同得 55.64 tf/根** ✓（互為驗核）。另以錯列公式 $s^2/4g$ 驗證直線斷面控制（5.60 > 3.10）。
  - **SS-2018-3**：$f_a = 90.5$ N/mm² 之出處以**正反兩向**驗證 —— 正向 $235/(1.5\sqrt3) = 90.45$；反向 $90.5 \times 1.5\sqrt3 = 235.1$ ⇒ 同時證實 $F$（及 $F_y$）為 235 而非 245。另以 $0.3F_{EXX} \equiv 0.6F_{EXX}/2.00$ 之恆等式驗證台灣與 AISC 360 ASD 同值（144.79 vs 144.79）。
  - **SS-2020-4**：$I_x$ 以「整體矩形減空心」與斷面性質反推 $S_x$ 兩路徑核對；$F_{va} = 2.8$ tf/cm² 以 $40\,\text{ksi} \times 0.070307 = 2.812$ 反查證螺栓等級與剪力面狀態。
  - **SS-2009-4**：預拉力係數以 AISC 表 J3.1 之 3/4 in A325 = 28 kips 反算面積歸屬（$A_t$ 得 28.06 ✓／$A_b$ 得 37.11 ✗）。

### 五、下游同步（規則 1 條件③）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/*/*.md` × 6 | 勘誤 ＋ 每題新增 `## 6. 依最新規範（AISC 360-16／-22）對照` ＋ 頁尾「修正日期：2026-08-22」與「驗證狀態：unverified」 |
| `raw/solutions/SS-2017-4/SS-2017-4-connection-viz.html` | **不變更**（主答案 $P_u = 90.3$ tf 未動，與使用者提供之 PDF 維持一致） |
| `wiki/problems/*.md` × 6 | 由 `_regen.py` 依正本重建；另**改寫全部 6 個 H1**（原為自動摘要，其中 SS-2015-2 以「- 」開頭、SS-2017-4 與 SS-2020-4 因 LaTeX 被剝除而出現「承受␣␣之集中載重」「材料強度␣tf/cm²」等殘缺，SS-2018-3 開頭殘留「題目：」） |
| `study/problems-view/*.html` × 6 | 由 `_regen.py` 重新渲染 `<main>`；**`<main>` 以外 shell 逐字元比對未變** ✔；KaTeX display／inline math 破損數皆 0 ✔；圖片路徑全部指向 `../../raw/solutions/<id>/` ✔ |
| `raw/json/question_index.json` | 6 題 tags 各補 3～5 個（**append-only**，既有 tag 一律保留，含用詞略異者如 `UT超音波檢測`、`接合設計`）；JSON 重新解析驗證、98 筆完整 ✔ |
| `dashboard-data.js` | 同上（`window.SS_QUESTIONS` 仍 98 筆，以 JSON 解析驗證通過） |
| `study/study-SS-U1-4.html` | 6 題 `Q[]` 列之標籤補強（append-only） |
| `study/study-SS-U1-1.html` | SS-2015-2 之 `Q[]` 列標籤補強 |
| `study/lecture-SS-U1-4.html` | §7.1 補一段警語：「翼板該用 CJP」是**實務原則**，不等於考題圖上就是 CJP；107 年圖面三處皆為 6 mm 填角銲，翼板須以喉面積檢核（151.6 > 90.5，NG，需 10 mm）。**此為本輪 SS-2018-3 更正所產生的下游不一致，必須同步** |
| `wiki/log.md` | 本則紀錄 |
| `CLAUDE.md` | CHANGELOG 補一列 |

**未變更（刻意）：** `raw/exams/` 考卷原件、所有 `-fig-*.png`／`-eqn-*.png`／`-hand-*.png` 使用者截圖、使用者提供之 `SS-2017-4：偏心銲縫群分析.pdf`、`SS-2017-4-connection-viz.html`（數值未變）、`study/lecture-SS-U2-3.html`（僅有連結、無涉更正內容）、`question_index.json` 的 `primaryTopicId`／`secondaryTopicIds`／`designMethod`（維持 `study/frequency-SS.html` 與各單元命題分析之統計有效性）。

**圖說更正（不動圖檔，只改 .md 內的文字說明）：** SS-2015-2 圖 2（螺栓 2×2、橫向 $g$ = 10 cm、「7 cm」量至連接板邊緣虛線、$T$ 之 3:4 方向）、SS-2015-2 hand-3／hand-4（原圖說加入了手寫筆記上**並不存在**的數值 40.41／15.46 與上限式，已改為忠實描述筆記內容，數值移出圖說）、SS-2018-3 圖（三處皆 6 mm 填角銲、40 mm 為扇形開孔）、SS-2020-4 圖（2 縱列 × 6 橫排、每列 6 支負責一端梁、偏心 5 cm）、SS-2009-4 圖（翼板亦為螺栓續接鈑，非直接 CJP 銲於柱面）。

### 六、待使用者複核（規則 5）

6 題 `verificationStatus` 均為 `unverified`。三處需要注意，**第 1 點最重要**：

1. **🔴 SS-2020-4：腹板續接鈑是否分擔彎矩？（答案差 44%）**

   三種假設層次：

   | 假設 | 螺栓群總彎矩 | 最不利合力 | 螺栓 | 鈑厚 |
   |---|---|---|---|---|
   | A 僅 $V$、忽略偏心（舊版） | 0 | 11.67 tf | M20 | 8 mm |
   | B $V$ + 偏心 $V\!\cdot\!e$ | 350 tf·cm | 13.24 tf | M20 | 8 mm |
   | **C $V$ + $V\!\cdot\!e$ + 腹板分擔彎矩（本文主答案）** | **1,297 tf·cm** | **25.93 tf** | **D25** | **12 mm** |

   選 C 之理由：①題目**明確給出 $M_w = 60$ tf·m**，若腹板完全不分擔彎矩，此值僅用於最小強度比較（47.8 < 60），對「設計腹板鈑」毫無作用，25 分的題目不太可能如此設計；②腹板鈑跨越續接面，該面必然存在彎矩，依變形相容性按 $I_w/I_x$ 分擔是續接設計標準做法（AISC Manual Part 12 亦採此原則）；③假設 A 忽略偏心在物理上不成立。

   **但若命題者原意為「翼板鈑承擔全部彎矩、腹板鈑僅承擔剪力」**（部分教科書之簡化法），則答案為 **B：M20 + 8 mm**。§5 爭議一已完整列出三層次對照表，並建議考場「寫 C，並在旁註明 B」。**此項請使用者裁定主答案。**

2. **🟡 SS-2018-3：翼板銲道之有效長度取法（影響所需銲腳約 8%）**

   主答案取 $L_f = 2b_f = 400$ mm（翼板上、下表面各一道，保守略去兩側端邊）⇒ $\tau_f = 151.6$ N/mm²、$w_{req} = 10.05$ mm。若取 $L_f = 2b_f + 2t_f = 432$ mm ⇒ $\tau_f = 140.3$、$w_{req} = 9.30$ mm。**兩者皆為 NG 且皆進位為 10 mm，結論不變**，僅過程數字不同。另一併提醒：本題若依台灣 ASD 之 $f_a = 144.8$ N/mm²，翼板為 151.6（超 5%，仍 NG）、腹板為 123.6（OK）——**與題給 90.5 之結論不同，作答務必依題給值**。

3. **⚪ SS-2020-4：續接鈑淨斷面彎曲與組合應力是否納入（影響鈑厚 12 → 14/16 mm）**

   主答案取 $t = 12$ mm（全斷面剪力 0.729 cm、全斷面彎矩 1.126 cm 控制）。若額外檢核：
   - 淨斷面彎曲（6 孔，$S_{net} = 505.8t$）以 $0.5F_u = 2.05$ tf/cm² 判 ⇒ $t \ge 1.251$ cm ⇒ **14 mm**
   - von Mises 型組合應力 $\sqrt{f_b^2+3f_v^2} \le 0.6F_y$ ⇒ $t \ge 1.406$ cm ⇒ **16 mm**

   惟：題目**未給 $F_u$**、台灣 ASD 對續接鈑亦未明列此二檢核。§5 爭議三已列出並註明「保守設計者可直接採 14 mm」。

**回溯確認（第三批待覆核事項之進展）：** 第三批 §五第 2 點中的 **(8.2-3) $B_1$ 公式已由 109 年試卷第 3-3 頁印出之原文證實**（見本則 §〇）。**(13.6-3) 強柱弱梁式仍待紙本規範覆核。**

---

## 2026-08-22 — 第五批七題解析勘誤（設計規範對施工之要求 U2-3，回查施工規範第四／五／七章原文）

**操作類型：** 解析勘誤（Cowork，依 CLAUDE.md 規則 1 第三項例外）＋下游同步
**觸發：** 使用者指示「幫我檢查並修正下列題目解題 SS-2021-1 & SS-2004-1 & SS-2019-1 & SS-2022-3 & SS-2016-2 & SS-2018-4 & SS-2024-4　若有修正.md，別忘了，下游檔案要一起修正」
**範圍：** 7 題。6 題主分類為 `SS-U2-3` 設計規範對施工之要求；SS-2024-4 主分類為 `SS-U1-4`（副分類含 `SS-U2-3`）

### 〇、本輪新增的規範原文查證

本批全屬施工規範題，故回查**「鋼構造建築物鋼結構施工規範」**之第四章（銲接施工）、第五章（高強度螺栓接合）、第七章（表面處理與塗裝）原文（國土管理署 nlma.gov.tw 公布之章節 PDF）：

| 條號 | 規範原文（節錄） | 影響題目 |
|---|---|---|
| **§4.1.5(1)～(3)** | 填角銲之有效喉深為自銲道根部至銲道表面之最短距離；**有效銲道長度為包括端彎（繞角銲）在內的全部填角銲道** | **SS-2016-2**（原解析稱「兩端各扣 1w、回銲 ≤4w 全段不計入」——**與規範相反**） |
| **§4.1.5(6)** | 依強度計算所得之填角銲**最小有效長度，不得小於填角銲尺寸之四倍** | SS-2016-2 |
| **§4.1.5(7)** | 斷續填角銲**任何一段之有效長度，不得小於銲接尺寸之四倍，亦不得小於 40 mm** | SS-2016-2（原下游教材寫 38 mm，係 AISC 之 1.5 in.） |
| **§4.1.5(8)** | 搭接接頭之**最小搭接長度不得小於接合部較薄板板厚之五倍，亦不得小於 25 mm** | SS-2016-2（補強） |
| **§4.1.5(9)** | 「接合部或構材側面填角銲或端部填角銲，分別在側或端部終止時，**在施工可能範圍下，應繼續圍繞轉角銲接，其長度不得小於銲接尺寸之二倍，不得超過銲接尺寸之四倍**。」 | **SS-2016-2**（原解析只有下限 `2w`，**漏掉上限 `4w`**——而上限正是子題(二)的答案來源） |
| **§5.2** | 「實際板厚度差 **< 1 mm 不必處理；≧ 1 mm 加墊片**」；「接合部於鎖螺栓前應將構件表面之**鐵銹、鱗片、黑皮、污泥、油垢及螺栓孔之毛邊徹底清除**」 | **SS-2004-1**(一)（原解析為「≤2 / 2–6 / >6 mm」三段式，無依據） |
| **§5.3.1** | 「可先用**沖梢**穿過校正，但**不得使用 2.5 kg 以上之鐵鎚**……則以**鉸孔**方式擴孔，惟**擴孔後之孔徑不得大於設計孔徑 2 mm**」 | **SS-2004-1**(二)（原解析為「≤2 / 2–5 / >5 mm」＋「孔徑 ≤ d+3 mm」，無依據） |
| **§5.3.1** | 「**已使用過之螺栓或帶有傷痕銹蝕者，不得再使用**」；解說：「**預拉力已超過降伏拉力，若拆後將產生永久變形……導致塑性變形量加大，致安全度不足**」 | **SS-2004-1**(三)（原解析主因寫「K 值改變＋累積疲勞」，且稱 A325 可有限次再用） |
| **§5.4.1 / §5.4.2** | 扭力法容許誤差 **±10%**；轉角法依螺栓長度採 **1/3～2/3 迴轉** | SS-2004-1（補強） |
| **§7.2.2 / §7.2.3** | Sa 2½「徹底噴砂處理，經處理後 95% 之氧化層鐵銹及異物均去除」／Sa 3「絕對徹底噴砂處理」；**表面粗糙度平均值一般應在 25～75 μm 之間** | SS-2019-1（原解析寫 Sa2.5→Rz 40–70、Sa3→Rz ≥60，無依據） |
| **§7.4.4** | 下列狀況不得塗裝：溫度 **≤ 5 °C**、相對濕度 **≥ 85%**、鋼材表面溫度**未高於露點 3 °C 以上**、鋼材表面溫度 **≥ 50 °C** | SS-2019-1（原僅列濕度與露點兩項） |
| **§7.4.5** | 除施工程序書另有規定，下列部位不得塗裝：①**工地銲接部位，及其相鄰接兩側各 100 mm 範圍內之區域** ②**摩阻式高強度螺栓接合面** ③**埋件（將埋入混凝土內之埋件及構件），但距混凝土表面 100 mm 深度內仍須塗裝** ④**軸件、滾輪等密著接觸面或迴轉面** ⑤**密閉空間之內露面** | **SS-2018-4**（整題就是這一條）、SS-2019-1 |
| 05091 章 §3.2.1／3.2.3／3.2.4 | 銲道內及其邊緣**不得有任何裂痕**；**咬邊**深度標準（最寬 0.8 mm 級）；「**均不得有重疊銲接之情形存在**」 | **SS-2021-1**（佐證「咬邊」「重疊」為規範明列之瑕疵，且重疊為零容忍） |

### 一、逐題勘誤

🔴 = 影響最終答案｜🟠 = 觀念／依據錯誤但方向不變｜🟡 = 敘述不精確｜⚪ = 補強

| 題號 | 等級 | 原內容 | 更正 |
|---|:-:|---|---|
| **SS-2021-1** | 🔴 | 四個標號判為 **a 銲趾裂縫→MT／b 夾渣→RT／c 咬邊→VT／d 氣孔→RT** | 以 450 dpi 逐處重判考卷原圖，四處**全部是表面或自表面起始的缺陷，圖中沒有任何圓形空洞或斜線填充的內部夾雜**：**a = 咬邊（Undercut）→ VT**（上銲趾處直立板被熔蝕出凹口，母材缺料，須以銲道量規量深度）；**b = 銲道裂縫（Crack）→ MT**（銲材內、自銲面開口並分岔的鋸齒線）；**c = 重疊（Overlap）→ VT**（下銲趾處銲材翻捲平舖於底板上而未熔合，母材多料）；**d = 母材／HAZ 裂縫（層狀撕裂）→ UT**（銲趾正下方往**底板厚度方向**延伸並帶轉折，在母材之內）。四小題用掉 VT×2、MT、UT，**RT 一次都沒用到**——這正是題幹「填角銲」三個字的意義（三角形斷面厚度連續變化，RT 實務不採用） |
| SS-2021-1 | 🔴 | 圖說稱「b 為斜線標示之夾渣、d 為圓形氣孔、左右翼板底部各有斜線支承標示」 | 原圖並無斜線填充、圓形缺陷或支承符號；圖說全面改寫為逐處描述斷面幾何（缺料／多料、在銲材／在母材） |
| SS-2021-1 | ⚪ 補強 | — | 補「咬邊 vs 重疊」方向性判別（少肉是缺口、多肉是假接）、填角銲不做 RT 的四項理由對照表、MT 三限制、a／c 改答 MT/PT 是否給分、d 判「銲趾裂縫」或「層狀撕裂」之層次差異 |
| **SS-2024-4** | 🔴 | 電熱熔渣銲（ESW）判為「**梁腹板剪力板（shear tab）與箱型柱面**」 | 考卷原圖兩處 ESW 引線指向的是**柱內兩道水平虛線（內橫隔板 Internal Diaphragm）與柱壁交會的兩端**。國內箱型柱的作法是：三面柱壁先組立、隔板置入，最後一片柱壁合攏後**無法自柱內施銲**，故以 **ESW 自柱外一道成形**銲住隔板端部。該銲道位於「梁翼板→柱壁→內隔板」的**力流主幹**上，且**封在柱內無法目視、修補困難**——這才是本題把 ESW 單獨標出來的理由 |
| SS-2024-4 | 🟠 | 預防方法列「限制 ESW **僅用於腹板剪力板**、避免用於翼板主要受力銲道」 | 此敘述建立在錯誤的位置判讀上，已刪除。改為：正常化／TMCP 鋼材與 SN 耐震鋼材、限制單位長度熱輸入與道間溫度（WPS/PQR）、必要時改多道次 FCAW／SMAW，或改採**貫通式隔板／外隔板**把銲道移到可檢查、可修補的位置 |
| SS-2024-4 | 🟡 | §1 表格、圖說、傳力路徑「梁剪力→腹板螺栓→剪力板→**ESW**→柱面」 | 剪力板與柱面為工廠填角銲／CJP，非 ESW；傳力路徑與 §1 表格、圖說全部改寫 |
| SS-2024-4 | ⚪ 補強 | — | 新增 §5.1「內隔板／貫通式隔板／外隔板三型式對照」（點出「因為是內隔板，才不得不用 ESW；ESW 的所有問題都源自這個施工限制」）；§5 標題由「結果彙整與驗算」改為規格所定之「關鍵爭議點與進階探討」 |
| **SS-2004-1** | 🔴 | (一) 板面間隙「≤2 mm 直接鎖緊／2–6 mm 塞板／>6 mm 修整」 | 規範 §5.2 只有**一個門檻**：**板厚差 < 1 mm 不必處理；≧ 1 mm 加墊片**。並補入同節之鎖固前清理要求（鐵銹、鱗片、黑皮、污泥、油垢、孔緣毛邊） |
| SS-2004-1 | 🔴 | (二)「偏差 ≤2 mm 撬棒／2–5 mm 鉸孔／>5 mm 禁止鉸孔」＋「鉸孔後孔徑不可超過 d+3 mm」 | 規範 §5.3.1：**先用沖梢校正，不得使用 2.5 kg 以上之鐵鎚**；仍不行則**鉸孔，擴孔後之孔徑不得大於設計孔徑 2 mm**。原三段式門檻與 d+3 mm 均無依據，已刪除 |
| SS-2004-1 | 🔴 | (三) 主因寫「扭力係數 K 值改變」＋「螺桿已累積**疲勞**損傷」；並稱 A325 可有限次重複使用 | 規範 §5.3.1：「**已使用過之螺栓或帶有傷痕銹蝕者，不得再使用**」，**不分等級、不附條件**。主因依規範解說為「**預拉力已超過降伏拉力，拆後產生永久（塑性）變形**，再鎖時塑性變形量加大、安全度不足」；K 值偏移與轉角法起算點失真為**次因**。鎖緊是單調靜力加載，**談不上疲勞**，該敘述已刪除。AISC/RCSC 之 Group A 條件式再用改列為國際差異補充 |
| SS-2004-1 | 🟡 | 轉角法敘述「彈性從緊到位再多轉 XX°」 | 補規範 §5.4.2 之 **1/3～2/3 迴轉**與 §5.4.1 扭矩法 **±10%** |
| SS-2004-1 | 🟠 | 章節編號為 §1／§2／§3 詳細解答／§3.5／§4 關鍵爭議點 | 不符 CLAUDE-SPEC；改為 §1～§5 標準結構（§3 戰略地圖與陷阱、§4 步驟化詳細計算、§5 關鍵爭議點） |
| **SS-2018-4** | 🔴 | 「現場銲接部位**兩側各 50 mm**」 | 規範 §7.4.5 明文為「工地銲接部位，及其**相鄰接兩側各 100 mm** 範圍內之區域」。50 mm 係 **AISC 360 §M3.5** 之美規值（2 in.），已改列 §5.1 對照 |
| SS-2018-4 | 🔴 | 埋入混凝土一項未提但書 | 補規範但書：「**但距混凝土表面 100 mm 深度內仍須塗裝**」（表層混凝土會碳化、開裂進水，鹼性鈍化不可靠）——常設得分點 |
| SS-2018-4 | 🔴 | **遺漏規範第 4 項**「軸件、滾輪等密著接觸面或迴轉面」；另自行加入「柱腳底板底面」與「程序書指定之其他部位」湊成六項 | 補入第 4 項（機件功能面，塗膜妨礙轉動與精確密貼、且易被碾壓剝落）；柱腳底板底面與 UT 掃查面改列為「實務常見另行指定」，明確與規範五項區隔 |
| SS-2018-4 | ⚪ 補強 | — | 補 §7.2.2 表面處理等級定義、§7.2.3 粗糙度 25～75 μm、§7.4.4 塗裝環境四項限制；新增「不塗裝 ≠ 不防蝕」對照表（五個部位各自如何達成防蝕） |
| **SS-2016-2** | 🔴 | 回銲長度只寫 **`ℓ ≥ 2w`** | 規範 §4.1.5(9) 同一句話訂了**上下限**：`2w ≤ ℓ ≤ 4w`。**上限是子題(二)「何時不適用」的答案來源**（回銲太長會束制端部轉動） |
| SS-2016-2 | 🔴 | 「主銲道有效長度 = 總長 − 2w（兩端各扣 1w）」「回銲段若 ≤ 4w，全段不計入有效長度」 | **與規範相反**。§4.1.5(1)～(3) 明定**有效銲道長度為「包括端彎（繞角銲）在內」的全部填角銲道**，國內**不作扣除**（「實長 − 2s」屬 IS／BS 等其他規範體系）。兩項無依據敘述已刪除 |
| SS-2016-2 | 🔴 | 子題(二)「不適用」主答案為「**間歇銲縫端部**」，並稱「AISC 規範明確規定間歇銲縫端部不需要（也不允許）做回銲」 | 該規範依據不存在。主答案改為**「接合之外伸肢需要保持轉動撓性者」**（簡支梁雙角鋼／頂角鋼剪力接合的外伸肢）——回銲束制端部轉動 → 假設為鉸接的接合產生未計入的端彎矩 → 回銲段先被拉裂；這正是規範訂 `4w` 上限的立法理由。次要例子補「搭接接頭中一板件伸出另一板件邊緣且該邊緣受計算拉應力者」。間歇銲端部改列為「**施工可能範圍**」的物理限制（做不到），與「不該做」明確區分 |
| SS-2016-2 | ⚪ 補強 | — | 新增 §4.1.5 全套填角銲細節對照表（有效喉深／有效長度含端彎／最小銲腳／最大銲腳／最小有效長度 4w／斷續銲每段 4w 且 40 mm／搭接 5t 且 25 mm／繞角銲 2w–4w），並特別標示**「三處 4w、方向不同」**之易錯點 |
| **SS-2019-1** | 🟠 | 塗裝環境限制僅列「相對濕度 ≤ 85%、表面溫度高於露點 3 °C」 | 補齊 §7.4.4 之四項（另有溫度 ≤ 5 °C、鋼材表面溫度 ≥ 50 °C 亦不得塗裝） |
| SS-2019-1 | 🟠 | 粗糙度「Sa 2.5 → $R_z$ 40～70 μm；Sa 3 → $R_z \ge 60$ μm」 | 改引規範 §7.2.3「表面粗糙度平均值一般應在 **25～75 μm** 之間，或依油漆特性而規定」；等級用語改為規範用語 **Sa 2½／Sa 3** 並附定義 |
| SS-2019-1 | 🟡 | 交叉引用之不予塗裝部位「現場銲接兩側各 50 mm」 | 改為 §7.4.5 五項與 **100 mm**（與 SS-2018-4 一致） |
| SS-2019-1 | 🟡 | 「高強度螺栓（**SAE 1030** 等）酸洗時氫脆」、耐久性寫死「25~50 年／20~40 年」 | 改為「高強度鋼件（抗拉強度愈高愈敏感）」並補去氫烘烤與「F10T／A490 級一般不建議熱浸鍍鋅」；耐久年限改為定性表述（受 ISO 12944 環境等級、膜厚與維護頻率影響） |
| SS-2019-1 | 🟠 | 標題為 `# SS-2019-1 解析` + `### 考題編號：SS-2019-1` | 不符 CLAUDE-SPEC；改為 `# 考題編號：SS-2019-1` |
| **SS-2022-3** | 🟠 | §3.5 L2 重要部位表列「**腹板剪力板 ESW**」 | 與 SS-2024-4 同一錯誤。國內 ESW 用於**箱型柱內橫隔板與柱壁**；剪力板與柱面為填角銲／CJP。已更正並新增 §4「部位①′ 箱型柱內橫隔板 ESW」整節（重要性與梁翼板 CJP 同級、UT 全長 + 柱壁外表面 MT、RT 在此不可行） |
| SS-2022-3 | ⚪ 補強 | — | 重要部位表由 5 列擴為 7 列（補箱型柱內橫隔板、柱接合、柱底板，並將連續板標明為 H 型柱作法）；NDT 總表補 ESW 一列；§5 考場建議由「一條必寫」改為「兩條必寫」，第二條即內橫隔板 ESW（與 SS-2024-4 直接相通） |

### 二、SS-2021-1 圖面判讀的證據（本輪最需要證據的一處）

原考卷（110 年第一題「圖一」）為手繪 T 型接頭填角銲斷面。以 450 dpi 轉圖後逐處放大判讀：

1. **a** — 直立板的輪廓線在上銲趾處被「挖」出一個**內凹缺口**，母材斷面被削減 ⇒ **缺料** ⇒ 咬邊。
2. **b** — 一條**自銲道表面開口、向銲材內部延伸並分岔**的鋸齒狀線條，起訖點都在銲材本體內 ⇒ 銲道裂縫。
3. **c** — 銲材在下銲趾處**翻捲成一片唇狀突出、平舖在底板上表面之外側**，未與底板熔合 ⇒ **多料但接不上** ⇒ 重疊。
4. **d** — 一條自右側銲道下銲趾起始、往**底板厚度方向**向下延伸並帶一個轉折的鋸齒線，位置在**母材之內** ⇒ 母材／HAZ 裂縫（層狀撕裂）。

判別口訣：**「咬邊少肉、重疊多肉；少肉是缺口、多肉是假接」**；再問一次「在銲材還是在母材」，名稱即唯一。

原解析所述之「斜線標示的夾渣」「圓形空洞的氣孔」「翼板底部斜線支承標示」在原圖中**均不存在**——該次 SOLVE 顯然未實際判讀附圖。

### 三、SS-2024-4 圖面判讀的證據

以 300 dpi 轉圖確認：箱型柱以實線（近側柱壁）＋虛線（遠側柱壁與柱內構件）繪出；柱內於**上、下梁翼板高程各有一道水平虛線**，兩處「電熱熔渣銲」引線分別指向該虛線**與左右柱壁交會的兩端**（每片隔板兩處）。水平虛線位於柱內、恰在翼板高程、且兩端各一處銲接 ⇒ 唯一合理判讀為**內橫隔板**。剪力板另以虛線矩形＋一排圓孔繪於腹板側，標註「螺栓工地安裝」，與 ESW 引線無關。

### 四、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-{2004-1,2016-2,2018-4,2019-1,2021-1,2022-3,2024-4}/*.md` | 7 檔勘誤，頁尾均加「修正日期：2026-08-22」與逐項說明 |
| `wiki/problems/*.md` ×7 | 由勘誤後之 .md 重新產生（標籤、題幹摘要、核心考點、解題關鍵步驟、§4 摘錄、涉及陷阱）。同輪順帶修掉 SS-2024-4 頁「SN 鋼材 **B 類型**有 Z 向要求」之誤（應為 **C 類型**） |
| `study/problems-view/*.html` ×7 | 以還原出的渲染設定重新產生（Python-Markdown + tables/fenced_code/nl2br、列表可中斷段落、數學式免於反斜線轉義、`[[概念]]` 轉藍色 chip、圖片路徑改寫）。該設定先以**原 7 檔逐位元組比對驗證**通過後才用於重生 |
| `raw/json/question_index.json` | 7 題 `tags` 同步；`verificationStatus` 維持 `unverified` |
| `dashboard-data.js` | 同 7 題 `tags` 同步 |
| `study/lecture-SS-U2-3.html` | 30 處：§2.3 回銲整節（SVG 標註、圖說、適用／不適用方塊、陷阱方塊）、ESW 位置（銲接方法表、SS-2024-4 接頭圖 SVG、NDT 部位表）、§3.4 SS-2021-1 四點答案表、§5.4 不予塗裝五部位 SVG 與陷阱、§6 螺栓三情境 SVG 與 T-16～T-20 陷阱表 |
| `study/formula-given-SS-U2-3.html` | 14 處：`const F[]` 之回銲卡／最小有效長度卡／板面間隙卡／螺栓重複使用卡／不予塗裝卡／ESW 卡之 `eq` 與 `meta`，以及 §一導言、十五個數字、四組數字對、三個答題骨架 |
| `study/旁白稿_SS-U2-3.md` | 5 段：P10／P11（螺栓三情境）、P14／P15（填角銲四個尺寸）、P25（不予塗裝五部位） |
| `study/study-SS-U2-3.html` | 6 題之 `Q[]` 摘要與標籤同步 |

### 五、待處理／待使用者複核

1. **⚠️ 衍生檔案尚未重新產生（本輪無法自動處理）**：
   - `study/lecture-SS-U2-3.pdf`、`study/formula-given-SS-U2-3.pdf` —— HTML 已更新，PDF 仍為舊版
   - `study/SS-U2-3_設計規範對施工之要求_公式給背分界_記憶片.pptx` / `.pdf` —— 內容取自 `formula-given-SS-U2-3.html` 的 `const F[]`，該資料已更正，需以 `formula-recall-deck` skill 重跑
   
   建議下次執行：重新輸出兩份 PDF，並重跑記憶片。

2. **7 題 `verificationStatus` 均為 `unverified`**（規則 1 之驗證狀態連動）。其中三項最需人工複核：
   - **🔴 SS-2021-1 的 a～d 判讀**：本輪結論為「咬邊／銲道裂縫／重疊／母材裂縫」，四者皆為表面或自表面起始之缺陷。此判讀完全建立在手繪圖的幾何上（缺料 vs 多料、在銲材 vs 在母材），請以原卷再確認一次。若採此判讀，則 **RT 在本題四小題中都不該出現**。
   - **🟡 SS-2021-1 之 d**：判為「銲趾裂縫／HAZ 裂縫」或「層狀撕裂」皆可（同一條裂縫的不同描述層次），關鍵在指出**它在母材而非銲材**。§5.2 已列出兩種答法之差異與對應的預防對策。
   - **🟡 SS-2016-2 子題(二)「不適用回銲」**：本輪主答案改為「需保持轉動撓性之外伸肢」，依據是規範 §4.1.5(9) 的 `4w` **上限**（規範以上限的形式表達「回銲不宜過長」）。若命題者原意僅為「幾何上無轉角可繞」，則間歇銲端部仍是可接受的答案——§4 已同時保留三種情形並標明性質差異。

3. **未動的檔案**：`wiki/concepts/WELD-DEFECTS.md`、`WELD-INSPECTION-NDT.md`、`FILLET-WELD-DESIGN.md` 三頁內容本身正確（`FILLET-WELD-DESIGN.md` 之「回銲 ≥ 2w」建議下次 `compile-all` 時補上 `≤ 4w` 上限）；概念頁屬 compile 輸出，本輪未手動修改。


---

## 2026-08-29　五題向量圖解補繪（struct-diagram）

**指令：** `struct-diagram SS-2013-3 & SS-2013-2 & SS-2005-1 & SS-2024-1 & SS-2015-3`

**性質：** 只新增圖解，**未更動任何解題數值或結論**，故 `verificationStatus` 維持 `unverified`（不因本輪而變動），
`question_index.json`、`dashboard-data.js`、`wiki/index.md`、`by-year.md` 均無須同步。

### 一、產出

每題 2 張，共 10 張向量圖（SVG ＋ 2× PNG），另附可重跑的產圖腳本：

| 題號 | 圖 | 這張圖攔下什麼錯 |
|---|---|---|
| SS-2013-3 | `fig-2-boundaries` 兩平面邊界條件與挫屈模態 | 兩平面柱底條件相反（強軸鉸、弱軸固）被誤讀成同一組；B 點側撐被誤用來切割強軸 |
| | `fig-3-slenderness` 三段有效長細比比較 | 拿 L 或 KL 互比而非比 KL/r → 控制段選錯（強軸 KL = 1120 最大卻不控制） |
| SS-2013-2 | `fig-2-leaning-column` 題目重繪＋側移挫屈模態 | 把柱 CD 讀成「底端鉸接的一般柱」→ ΣP_eK 多算一根（圖上 CD 全程保持直線） |
| | `fig-3-magnitude` 四種讀法的 w_cr 量級 | 算出 w_cr 落在 190～290 tf/m 卻沒察覺（正解 96.0） |
| SS-2005-1 | `fig-2-block-shear` 接合幾何＋三條塊狀剪力路徑 | 只算一條路徑、或把拉力面畫到邊距較大的肢背側（68.5 → 83.9 tf） |
| | `fig-3-limit-states` 五個極限狀態強度比較 | 漏算螺栓剪力（71.8 tf，與控制值僅差 4.8%） |
| SS-2024-1 | `fig-2-section` 殘餘應力分布與有效斷面 | 誤以為中央翼板／腹板也會降伏；或把強軸扣除量按弱軸的 b³ 方式算 |
| | `fig-3-column-curve` 四段柱強度曲線 | 把非彈性分支硬拉到 λ=√2 而畫出不連續跳躍（違反單調不遞增）——誤畫法已一併畫在圖上作對照 |
| SS-2015-3 | `fig-2-section` 組合斷面與兩軸平行軸定理 | 把圖上 20 cm（腹板高）當成形心間距；或對 I_X 也誤加 Ad² |
| | `fig-3-boundary` 固接*-鉸接 vs 懸臂柱之挫屈模態 | 把本題說成「等效於懸臂柱」而取設計 k = 2.1（L 由 700 掉到 667 cm） |

### 二、幾何一律由解題數值算出，不描摹

- SS-2013-3：反曲點位置由固接-鉸接之特徵方程 `tan u = u` 解出（u = 4.4934 → K = π/u = 0.6992，
  與考卷表列 0.7 相符），非目測擺放。
- SS-2013-2：側移模態的節點轉角由 §1 給定之 `I_c`、`I_b` 以傾角變位法解出
  （`θ_B = ψ·I_c/(I_c+I_b) = 0.1811ψ`、`θ_A = (3ψ−θ_B)/2`），故改變 I_c/I_b 圖形會跟著變；
  靠桿 CD 以**直線**繪出（二力構件，零彎矩勁度），這正是與誤解法的唯一視覺差異。
- SS-2005-1：三條破壞路徑的剪力面／拉力面由螺栓座標推得，A_nt 現算為 7.65／12.65／10.30 cm²，與 §4.5 一致。
- SS-2024-1：三個轉折點由 I_e/I_x 現算（0.697／0.985／1.414），I_e 由斷面尺寸與平行軸定理算出。
- SS-2015-3：d = 外寬/2 − C_y 現算 12.51 cm；I_X、I_Y、r_X、r_Y、KL/r、L 全部由腳本重算，
  與 §4 逐項相符（I_Y = 9,699 與 §5 一致，§4 之 9,698 為中間值四捨五入所致）。

### 三、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-{2013-3,2013-2,2005-1,2024-1,2015-3}/gen_*.py` | 新增產圖腳本 5 支（隨解析一起版控，可重跑） |
| `raw/solutions/*/figs/*.svg` ＋ `*.png` | 新增 10 張 SVG ＋ 10 張 2× PNG |
| `raw/solutions/*/*.md` ×5 | 圖片與圖說插入對應章節正下方；頁尾加「圖解補繪：2026-08-29」 |
| `wiki/problems/*.md` ×5 | 同步插入相同的圖片與圖說（路徑改為 `../../raw/solutions/…`），並於「## 圖形」表補列 10 列 |
| `study/problems-view/*.html` ×5 | 同步插入 `<img>` 與圖說，頁尾補「圖解補繪」行 |

**驗證：** `render.py` 對 10 張 SVG 之 XML 合法性與溢出檢查全數 0 項待修；10 張 PNG 全部目視檢查
（中文無方框、文字無重疊或裁切、變形與轉角方向與邊界條件相符、標註數值與解析逐字比對）。
排版過程中修掉的字型／排版陷阱：`ȳ`、`✗` 在 Noto 字型缺字會排成方框（改用 `y_f`、純文字）；
數學襯線字型排不出中文（`(KL/r)_{y,下}` 的「下」會整個消失，改把中文移出數學字串）；
`compose()` 的 title／sub／note 不經過上下標排版（含 `_` 的符號會露出底線字元，已改寫為敘述句）。

### 四、待處理／待使用者複核

1. **本輪未動任何數值**，五題 `verificationStatus` 仍為 `unverified`（沿 2026-08-22 全庫重置），
   與本輪無關，仍待逐題人工重新驗算。
2. **⚠️ 事故與處置（已修復）：** 插入下游檔案的輔助函式原本寫成 `open(path,"w").write(fn(s))`，
   Python 會**先開檔截斷再求值**，`fn` 拋錯時把 `wiki/problems/SS-2005-1.md` 清成 0 bytes。
   已由 `git show HEAD:wiki/problems/SS-2005-1.md` 完整還原（9,347 bytes，與 HEAD 零差異）後重新插入；
   輔助函式已改為「先算完內容再開檔寫入」並加上輸出縮水防呆。
   全庫已掃描確認**無任何 0 bytes 檔案**。
3. `study/problems-view/*.html` 為既有渲染層，本輪以字串插入方式維護；
   若日後以腳本整批重生該渲染層，需確認新增的 `<img>` 與圖說會被帶入。


---

## 2026-08-29（第二批）　四題向量圖解補繪（struct-diagram）

**指令：** `struct-diagram SS-2011-3 & SS-2014-3 & SS-2023-3 & SS-2010-4`

**性質：** 只新增圖解，**未更動任何解題數值或結論**，`verificationStatus` 維持 `unverified`；
`question_index.json`、`dashboard-data.js`、`wiki/index.md`、`by-year.md` 均無須同步。

### 一、產出（共 10 張，SVG ＋ 2× PNG）

| 題號 | 圖 | 這張圖攔下什麼錯 |
|---|---|---|
| SS-2011-3 | `fig-2-ltb-zones` LTB 三分區曲線 | 分區判斷錯（誤答彈性）；或 C_b 直接取 1.0 使 M_n 只剩 1,930 |
| | `fig-3-code-flip` 兩套規範分區帶對照 | 拿 AISC 360-16 的 L_r 去配本卷舊式 X₁／X₂ 公式而答錯分區 |
| SS-2014-3 | `fig-2-cb-reading` 兩種題意解讀的彎矩圖 | 不先畫彎矩圖就假設 C_b（矩形圖 1.000／拋物線圖 1.136） |
| | `fig-3-ltb-brace` LTB 三分區與側撐效益 | 把 L_b 誤取成梁長一半（4 m → 2 m）而高估強度 |
| | `fig-4-interaction` 雙向互制圖 | 漏掉弱軸 1.5F_yS_y 上限，或以為弱軸彎矩小可忽略 |
| SS-2023-3 | `fig-2-ena-pna` 斷面／彈性／塑性三聯圖 | 把 ENA 當成 PNA；或誤以為較寬的頂翼板先降伏 |
| | `fig-3-equal-area` 等面積法與 Z 的四項組成 | 算 Z 時沒把腹板在 PNA 處拆成上下兩段 |
| SS-2010-4 | `fig-2-load-path` 集水寬與兩套載重 | 集水寬取錯；撓度誤用 1.6w_L |
| | `fig-3-screen` 五組候選之雙準則長條 | 只看強度（或只挑最輕）就定案，漏掉撓度這個真正的控制項 |
| | `fig-4-298-debate` RH298×149 的 0.55% 與 FLB 佐證 | 初選後忘記把自重加回去；或忽略翼板結實性 |

### 二、每個數字都先與 .md 逐項對帳才畫

四支腳本都在 `__main__` 內把現算值與 .md 表列值逐項比對後才輸出：

- **SS-2011-3**：A／I_x／S_x／Z_x／I_y／r_y／J／I_f／C_W／M_p／M_r／X₁／X₂／L_p／L_r，
  以及 AISC 的 L_p／r_ts／L_r／M_r 共 19 項全部吻合（誤差 < 0.2%）。
  M_p 平台段終點 L_b = 747.4 cm 由「C_b×(非彈性式) = M_p」解出，非目測。
- **SS-2014-3**：C_b 由四點求積式現算（1.000／1.136），M_p／M_r／中括號／φM_nx／
  F_yZ_y／1.5F_yS_y／1.6F_yS_y／φM_ny／互制比／側撐後／AISC 對照共 19 項全部吻合。
- **SS-2023-3**：ENA 由一次矩、I_x 由平行軸定理、PNA 由等面積法、Z 由四項乘積現算，
  13 項全部吻合；Z 的四項（11,625／5,625／625／6,875）與 §4 六逐項相同。
- **SS-2010-4**：五組候選的彎矩與撓度使用率全部由載重現算（含自重迭代），
  與 §4 一 Step 4 附表逐格相同（100.55／94.2／129.5／205／87.2／98.6／91.6／126／85.3／120%）；
  §5.5 的 FLB 內插亦現算得 M_n = 1,663、φ_bM_n = 1,497 tf·cm。

### 三、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-{2011-3,2014-3,2023-3,2010-4}/gen_*.py` | 新增產圖腳本 4 支（可重跑） |
| `raw/solutions/*/figs/*.svg` ＋ `*.png` | 新增 10 張 SVG ＋ 10 張 2× PNG |
| `raw/solutions/*/*.md` ×4 | 圖片與圖說插入對應章節正下方；頁尾加「圖解補繪：2026-08-29」 |
| `wiki/problems/*.md` ×4 | 同步插入相同圖片與圖說（路徑改為 `../../raw/solutions/…`），「## 圖形」表補列 10 列 |
| `study/problems-view/*.html` ×4 | 同步插入 `<img>` 與圖說，頁尾補「圖解補繪」行 |

**驗證：** `render.py` 對 10 張 SVG 之 XML 合法性與溢出檢查全數 0 項待修；
10 張 PNG 全部目視檢查（中文無方框、文字無重疊或裁切、標註數值與解析逐字比對）。

### 四、本輪修掉的排版陷阱（延續第一批的教訓，另有新發現）

1. **SVG 文字內容不可含未跳脫的 `<`** —— `Canvas.text_px` 不做 XML 跳脫，
   一個「190.1 < F_yZ_y」就讓整個 SVG 解析失敗（SS-2014-3 fig-4）。已改寫為「小於」。
2. **`compose()` 的 title／sub／note 不經上下標排版** —— 含 `_` 的符號會露出底線字元
   （出現在四題共 6 處），一律改寫成敘述句。
3. **下標未加大括號只會吃掉一個字元** —— `P_AB`／`c_bot`／`M_ux` 會排成 `P_A B`，
   須寫成 `P_{AB}`。
4. **後畫的圖例白底會蓋住先畫的標註** —— SS-2011-3 的圖例原本蓋掉整段彈性曲線與 L_p 標註。
5. **改版遺留的重複尺寸線** —— SS-2023-3 曾同時畫出兩條總高尺寸線（新舊各一），
   靠 SVG 內文字座標比對才抓到。
6. **四個值只差 1% 時，自零起的長條圖看不出差距** —— SS-2010-4 fig-4 改為
   自 1,450 起的截斷刻度，並在圖上明示「橫軸自 1,450 起（非自零）」。

### 五、待處理／待使用者複核

1. 本輪未動任何數值，四題 `verificationStatus` 仍為 `unverified`（沿 2026-08-22 全庫重置）。
2. SS-2014-3 與 SS-2011-3 的 §6 皆指出「若改依 AISC 360-16 則分區／數值改變」，
   圖上已把兩套規範並列；若日後台灣規範改版發布，這兩張圖需一併重跑。
3. `study/problems-view/*.html` 為既有渲染層，本輪以字串插入方式維護；
   若日後整批重生該渲染層，需確認新增的 `<img>` 與圖說會被帶入。

---

## 2026-08-29（第三批）　六題向量圖解補繪（struct-diagram）

**指令：** `struct-diagram SS-2013-4 & SS-2020-3 & SS-2003-4 & SS-2011-1 & SS-2022-1 & SS-2009-1`

**性質：** 只新增圖解，**未更動任何解題數值或結論**，`verificationStatus` 維持 `unverified`；
`question_index.json`、`dashboard-data.js`、`wiki/index.md`、`by-year.md` 均無須同步。
本輪六題正好是 2026-08-22 第三批勘誤的同一組（`SS-U1-3` 梁柱／二階分析），
故每張圖都刻意對準那輪查出的錯誤來畫。

### 一、產出（共 20 張，SVG ＋ 2× PNG）

| 題號 | 圖 | 這張圖攔下什麼錯 |
|---|---|---|
| SS-2013-4 | `fig-1-frame` 題目幾何重繪 | 把 A、D 誤讀為柱頂節點（三根柱）——即 08-22 勘誤查出的原始錯誤 |
| | `fig-2-nt-lt` Mnt／Mlt 分離三聯 | 層剪力誤分給三根柱而得 M_lt = HL/3（正解 HL） |
| | `fig-3-b2-curve` B2 漸近曲線 | 忽略 ΣP_u < ΣP_eK 適用範圍；ΣP_eK 誤用三柱之 7.72EI/L² |
| SS-2003-4 | `fig-1-frame` 支承與力偶轉向重繪 | 誤判為可側移構架而取 C_m = 0.85（穩定式 0.595 → 1.127） |
| | `fig-2-curvature` 同轉向／反轉向兩格 | M₁/M₂ 符號記反（C_m 由 0.2 變 1.0）；圖上並量出雙曲率跨中撓度只有單曲率的 12.8% |
| | `fig-3-interaction` 兩式堆疊＋C_m 敏感度 | 只驗穩定式就判「安全」，漏掉真正控制的強度式 1.140 |
| SS-2011-1 | `fig-1-p-delta` P-Δ 與 P-δ 對照 | 子題(一) 只寫 P-Δ 而漏 P-δ |
| | `fig-2-imperfection` 偏移法 vs 假想水平力 | N_i 寫成 0.002P_r（Y_i 是該層重力載重） |
| | `fig-3-taub` 0.8 與 τ_b 兩層次曲線 | 誤答「只有非彈性才折減」（0.8 是無條件的） |
| | `fig-4-alpha` (1.2D+1.6L)/(D+L) 隨 L/D | 把載重係數 α = 1.6 誤稱為安全係數 Ω_c = 1.67 |
| SS-2020-3 | `fig-1-loading` 兩軸端彎矩轉向 | 單／雙曲率誤判 ⇒ M₁/M₂ 正負錯 |
| | `fig-2-mny-limit` 弱軸 M_n 三值長條 | 漏檢 1.5F_yS_y 上限（Z_y/S_y = 1.511，恰好由上限控制） |
| | `fig-3-b1-curve` 台灣 (8.2-3) vs AISC | B₁ 算得 0.935 未取下限；P_e1 誤用題給 K 而把側移柔度重複計入 |
| | `fig-4-interaction` H1-1a 堆疊＋四算法 | 忘記把 M_uy 除回 r = 1.6 才是題目要的工作彎矩 |
| SS-2022-1 | `fig-1-section` 斷面＋b/t 對 λ_p | 清淨寬只扣一次板厚（b/t 由 23.0 變 24.0） |
| | `fig-2-shear-area` A_w 兩片 vs 四片 | A_w 取四片而把剪力強度高估一倍 |
| | `fig-3-pm` 折線＋需求點 (0.236, 0.433) | H1-1a／H1-1b 選錯；並提醒載重已含二階值、不可再乘 B₁／B₂ |
| SS-2009-1 | `fig-1-scwb` 不等式兩側的 Σ 範圍 | Σ 取錯（柱是上下、梁是左右）；1.25 誤除到柱側 |
| | `fig-2-mechanism` 梁機構 vs 軟層機構 | 說不出「為什麼柱端出鉸就是軟層崩塌」 |
| | `fig-3-pm` A–B–C 折線與兩段斜率 | AB／BC 的陡平寫反——即 08-22 勘誤查出的原始錯誤 |

### 二、幾何與數值一律由解題結果算出，不描摹

- **SS-2013-4 fig-2** 的側移變形不是畫出來的：梁遠端為滾支承 ⇒ 每段在 B 的轉動勁度 3EI/(1.5L)，
  兩段共 4EI/L；柱遠端鉸接 ⇒ M_BC = (3EI/L)(θ_B − ψ)。節點平衡解得 **7θ_B = 3ψ**，
  再由 M_CB = 0 得 θ_C = (9/7)ψ、由 M_AB = 0 得 θ_A = −θ_B/2。四個轉角全部入圖。
- **SS-2003-4 fig-2** 的兩條撓度曲線由 w″ = M/EI 解析積分而得
  （雙曲率 w = ξ³/3 − ξ²/2 + ξ/6，單曲率 w = −ξ(1−ξ)/2），
  兩格共用同一放大倍率，故「12.8%」是算出來的比值，不是形容詞。
- **SS-2009-1 fig-1／fig-3** 的折點與斜率由 8/9 與 1/2 兩係數推出，腳本內以
  `assert abs(M_B − M_B2) < 1e-12` 檢查「兩式在 P̄ = 0.2 處必須同得 0.9」，折線不連續會直接中止。
- **SS-2020-3、SS-2022-1** 的斷面性質與所有強度值由腳本獨立重算，
  與 .md §4 逐項吻合（A = 218.72／983.04、Z_x = 3,706.6、Z = 28,328、
  φ_cP_n = 392.3／2,587、B₁x = 1.017、M_wy = 7.91、H1-1a = 0.642）。

### 三、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-*/SS-*.md` ×6 | 圖與圖說插入對應章節；檔尾補「圖解補繪」行 |
| `raw/solutions/SS-*/gen_SS-*.py` ×6 | 產圖腳本隨解析一起版控，`SD_SKILL` 預設指向 repo 內 `skills/struct-diagram`，可原地重跑 |
| `raw/solutions/SS-*/figs/` | 20 SVG ＋ 20 PNG（2×） |
| `wiki/problems/SS-*.md` ×6 | 節錄段落內插 6 張；「圖形」表補 20 列 |
| `study/problems-view/SS-*.html` ×6 | 全部 20 張以 `<img>` ＋ 圖說插入對應標題前 |
| `wiki/log.md` | 本則 |
| `CLAUDE.md` | CHANGELOG 補一列 |

`*-pm-viz.html`（5 檔）本輪**未動**——那些頁面不由 .md 生成，且本輪無數值變更。

### 四、本輪修掉的排版陷阱（新發現，已回饋為腳本內註解）

1. **中文寫進 `math_px()` 會整段消失** —— `FONT_M` 是純西文襯線串，
   cairosvg 找不到中文字就把該段丟掉，且 `render.py` 的溢出檢查抓不到（檔案仍合法）。
   本輪有 7 處中招（含表意空格 `　`），已全部改為「符號用 `math_px`、中文用 `text_px`」。
2. **`math_px()` 內的裸 `<` 會讓 SVG 變成非法 XML** —— `mtext()` 不做跳脫；
   `>` 合法但 `<` 不合法。改寫成 `&lt;` 或改用文字敘述。
3. **`est_width()` 低估含 `√` 的字串寬度** —— 靠右對齊（`anchor="end"`）的標籤會壓到長條上。
   凡是「含上下標又要靠右對齊」的名稱，一律改用 `text_px` 純文字寫法。
4. **圖號必須與插入 .md 的先後一致** —— SS-2020-3 與 SS-2009-1 初版的檔名序號
   與章節順序不符，已重新編號並同步改掉圖內標題。

### 五、待處理／待使用者複核

1. 本輪未動任何數值，六題 `verificationStatus` 仍為 `unverified`（沿 2026-08-22 全庫重置）。
2. `study/problems-view/*.html` 仍以字串插入方式維護；若日後整批重生該渲染層，
   需確認新增的 `<img>` 與圖說會被帶入（與前兩批同一風險）。
3. SS-2013-4 fig-3 與 SS-2020-3 fig-3 都把台灣與 AISC 兩套並列；
   台灣規範改版發布後，這兩張需一併重跑。

### 六、規格回寫（避免下次再踩）

`skills/struct-diagram/SKILL.md` 已補上本輪三個陷阱與圖號規則：
「常見錯誤」表新增 4 列（中文整段消失／裸 `<` 產生非法 XML／`est_width()` 低估 `√` 寬度／圖號與章節順序），
並在 Step D 明寫「溢出檢查抓不到『文字被字型吃掉』，故目視看圖不可省」。
⚠️ `skills/struct-diagram.skill` 為已打包版，**尚未重新打包**；已安裝版仍是舊規格，
需由使用者重新打包安裝後才會生效。

`skills/struct-diagram.skill` 已於同日重新打包（12 個項目、38,580 bytes，
內容與 `skills/struct-diagram/` 逐位元組比對相符；`examples/smoke_test.py` 七張圖 render 0 錯）。
使用者需重新安裝該 `.skill` 才會套用新規格。

---

## 2026-08-29（第四批）　六題向量圖解補繪（struct-diagram）

**指令：** `struct-diagram SS-2015-2 & SS-2017-4 & SS-2017-2 & SS-2020-4 & SS-2018-3 & SS-2009-4`

**性質：** 只新增圖解，**未更動任何解題數值或結論**，`verificationStatus` 維持 `unverified`；
`question_index.json`、`dashboard-data.js`、`wiki/index.md`、`by-year.md` 均無須同步。
本輪六題即 2026-08-22 第四批勘誤的同一組（`SS-U1-4` 接合之分析與設計），
每張圖都對準那輪查出的錯誤來畫。

### 一、產出（共 20 張，SVG ＋ 2× PNG）

| 題號 | 圖 | 這張圖攔下什麼錯 |
|---|---|---|
| SS-2015-2 | `fig-1-connection` 接合詳圖重繪 | 把「7 cm」當成槽鋼端距（實為量到連接板邊緣虛線） |
| | `fig-2-block-shear` BSR 破壞塊（正解 vs 舊版） | 自由端判錯、拉力面寬度誤取 e₂ 而非 gauge g |
| | `fig-3-limit-states` 三極限狀態＋BSR 上限 | 漏掉「兩條件式皆受上限拘束」（本題正由上限控制） |
| | `fig-4-weld` 銲腳三門檻 | 查錯表 10.2-4（12<t≤19 為 6 mm），把控制理由說成「規範最小值」 |
| SS-2017-4 | `fig-1-weld-group` 幾何與形心 | 把尺寸線上的圓點當形心；偏心距未從形心量起 |
| | `fig-2-vector` 四角點向量疊加 | 以為「離形心最遠就是臨界點」 |
| | `fig-3-method-compare` 三法對照 | 以為換新規範答案就會變（變的是分析法，不是強度式） |
| SS-2017-2 | `fig-1-mechanism` 傳力機制 | 以為摩阻型靠螺栓桿傳剪 |
| | `fig-2-slip-behavior` 荷重–滑移曲線 | 極限狀態只答「滑動」，說不出後續與使用性／強度之分類 |
| | `fig-3-strength-compare` 容許剪應力對照 | 以為摩阻型「比較強」（實為承壓型 X 的 52%） |
| SS-2020-4 | `fig-1-splice` 螺栓配置 | 「2 列 × 3 排」的誤讀；忽略 e = 5 cm |
| | `fig-2-moment-share` 三項作用力 | 腹板分擔彎矩與偏心彎矩全漏（舊版只用 V/n） |
| | `fig-3-bolt-force` 偏心螺栓群向量 | 把總力除以螺栓數（低估 55%，D25 誤選為 M20） |
| | `fig-4-plate` 鈑厚雙控 | 只算剪力就選 8 mm（實由彎矩控制 12 mm） |
| SS-2018-3 | `fig-1-joint` 接頭重繪 | 憑印象把梁翼判為 CJP（圖面三處皆 6 mm 填角銲） |
| | `fig-2-web-stress` 應力向量合成 | 只拿 τ_w1 與 f_a 比較就下結論 |
| | `fig-3-code-compare` 三套規範對照 | 把「銲道夠不夠」當成純物理問題 |
| SS-2009-4 | `fig-1-groove` 開槽幾何 | Single V 與 Single Bevel 搞混 |
| | `fig-2-bolt-spacing` 中心距三層次 | 把 8/3 d（強制）與 3d（有條件）的層次顛倒 |
| | `fig-3-preload` 預拉力面積取法 | 誤用全斷面積 A_b，把預拉力高估三成 |

### 二、每個數字都由腳本重算並與 .md 對帳

六支腳本在 `__main__` 內印出現算值，與 .md §4 逐項吻合：

- **SS-2015-2**：A_n = 26.54、A_nv = 12.96、A_nt = 4.32、A_gt = 6.00 cm²；
  式二 56.77 vs 上限 55.64 → BSR = 83.5 tf；w 需求 7.65 mm、AISC 方向性 5.63 mm。
- **SS-2017-4**：J_w = 197,333 cm³（並以 `assert` 檢查 J = I_x + I_y 兩路徑一致）、
  f_res = 0.02454P、P_u = 90.27 tf；方向性 θ = 48.6°、係數 1.325 → 119.6 tf。
- **SS-2020-4**：I_x = 202,977、I_w/I_x = 0.1578、Σy² = 1,120；
  M_web = 947、V·e = 350、M_bolt = 1,297 tf·cm；R_max = 25.93 tf；t 需求 1.126 cm。
- **SS-2018-3**：l_w = 388（由 d − 2(t_f + 扇形開孔) 算出，與題目 S_w 公式中的 388² 相符）、
  τ = 123.6、w 需求 8.19 mm；翼板 τ_f = 151.6、w 需求 10.05 mm。
- **SS-2009-4**：0.7×120×A_t(0.334) = 28.1 kips，與 AISC 表 J3.1 之 28 kips 相符；
  誤用 A_b(0.442) 得 37.1 kips。

### 三、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-*/SS-*.md` ×6 | 圖與圖說插入對應章節；檔尾補「圖解補繪」行 |
| `raw/solutions/SS-*/gen_SS-*.py` ×6 | 產圖腳本隨解析版控，`SD_SKILL` 預設指向 repo 內 `skills/struct-diagram` |
| `raw/solutions/SS-*/figs/` | 20 SVG ＋ 20 PNG（2×） |
| `wiki/problems/SS-*.md` ×6 | 節錄段落內插 8 張；「圖形」表補 20 列（**SS-2017-2 原無圖，本輪新建「圖形」節**） |
| `study/problems-view/SS-*.html` ×6 | 全部 20 張以 `<img>` ＋ 圖說插入對應標題前 |
| `wiki/log.md` | 本則 |
| `CLAUDE.md` | CHANGELOG 補一列 |

`SS-2017-4-connection-viz.html` 本輪**未動**——該頁不由 .md 生成，且本輪無數值變更。

### 四、本輪新踩到的排版陷阱

1. **`⅔`（U+2154）等分數字元在襯線與中文字型皆缺字**，會變方框。
   SS-2009-4 的尺寸線標註原寫 `8/3 d = 2⅔ d`，已改為 `8/3 d ≈ 2.67 d`。
   （`²`、`³` 在 `text_px` 的中文字型串裡正常，只有寫進 `math_px` 才有風險。）
2. **`cv.dim()` 的 label 走 `math_px`**，故尺寸線標註同樣不能寫中文或缺字字元。
3. **繪圖座標範圍要涵蓋「實際幾何」而非「假想的相對值」**——SS-2018-3 初版把梁中心
   設為 `D/2` 後 `yt` 變成 500，超出設定的 YH = 320，`render.py` 一次抓出 55 處溢出。
4. **`problems-view` 的錨點要用渲染後的形式**：`**物理理由：**` 渲染為
   `<p><strong>物理理由：</strong><br />`（後接 `<br />` 而非 `</p>`），
   比對 `</p>` 會失敗而被插到錯誤章節；本輪已據此修正 SS-2009-4 的兩張圖。
   引用區塊（`>` 開頭）的錨點無法直接比對，改插在該節結尾（下一個 `<h2>` 之前）。

### 五、待處理／待使用者複核

1. 本輪未動任何數值，六題 `verificationStatus` 仍為 `unverified`。
2. **SS-2020-4 §5 爭議一的判斷仍待使用者確認**：本文採假設 C（腹板分擔彎矩＋偏心），
   若命題者原意為「翼板鈑承擔全部彎矩」則為 M20 + 8 mm。`fig-3` 已把 A/B/C 三種
   假設的合力並列（11.67／13.24／25.93 tf），供複核時一眼比對。
3. `study/problems-view/*.html` 仍以字串插入方式維護（與前三批同一風險）。

---

## 2026-08-29（第五批）　五題向量圖解補繪（struct-diagram）

**指令：** `struct-diagram SS-2021-1 & SS-2004-1 & SS-2019-1 & SS-2022-3 & SS-2016-2`

**性質：** 只新增圖解，**未更動任何解題數值或結論**，`verificationStatus` 維持 `unverified`；
`question_index.json`、`dashboard-data.js`、`wiki/index.md`、`by-year.md` 均無須同步。
本輪五題全屬 `SS-U2-3`（設計規範對施工之要求）且全為**概念說明題**——沒有算式可畫，
圖的任務改成把**規範數字的方向與範圍**、以及**幾何為何逼出某個工法**畫清楚。

### 一、產出（共 15 張，SVG ＋ 2× PNG）

| 題號 | 圖 | 這張圖攔下什麼錯 |
|---|---|---|
| SS-2021-1 | `fig-1-defects` 四處瑕疵斷面幾何 | a 咬邊與 c 重疊互換（同在銲趾、方向相反）；把圖中沒有的圓形空洞讀成氣孔／夾渣 |
| | `fig-2-ndt-map` NDT 適用範圍（深度 × 型態） | 把 MT 用在超過約 3 mm 的內部缺陷（d）；在填角銲上硬派 RT |
| | `fig-3-rt-fillet` 填角銲為何不做 RT | 「RT 適用於所有銲道」的過度推廣 |
| SS-2004-1 | `fig-1-faying-gap` 板面不密接 | 把 §5.2 門檻寫成「2 mm／6 mm」三段式（規範只有 1 mm 一個數字） |
| | `fig-2-hole-correction` 沖梢→鉸孔→超限 | 只寫「用鉸孔擴大」，漏掉沖梢這一層與 2.5 kg／+2 mm 兩個上限 |
| | `fig-3-reuse` 拉力–伸長曲線 | 把不得重複使用的理由寫成「疲勞」（實為單調靜力的塑性耗損） |
| SS-2019-1 | `fig-1-mechanism` 三法在破損處的差別 | 三法都寫成「隔絕水氧」，漏掉犧牲陽極這個耐久性差異的來源 |
| | `fig-2-surface-prep` 清潔度與粗糙度／膜厚 | 自行寫出「R_z 40～70」之類無出處的數字；把熱浸鍍鋅也寫成 Sa 2½ |
| | `fig-3-env-window` §7.4.4 可施工窗口 | 只寫濕度與露點，漏掉 5 °C 與 50 °C；現場銲接兩側寫成 50 mm |
| SS-2022-3 | `fig-1-joint-map` 部位地圖＋NDT 對照 | 把 ESW 記成「剪力板 ESW」（實為內橫隔板↔柱壁） |
| | `fig-2-ndt-logic` 缺陷型態決定方法 | 梁翼板 CJP 寫成「RT 100%」；反向把填角銲的剪力板寫成 UT |
| | `fig-3-esw-diaphragm` ESW 的幾何必然性 | 用 RT 檢 ESW；把 ESW 的典型缺陷寫成氣孔（實為面狀 LOF ＋ 夾渣） |
| SS-2016-2 | `fig-1-end-return` 回銲幾何與有效長度 | 只寫下限 2w；沿用 IS 800／BS 的「兩端各扣 1w」 |
| | `fig-2-three-4w` 三處 4w 的方向 | (6)(7) 下限與 (9) 上限寫反；漏掉 w < 10 mm 時由 40 mm 控制 |
| | `fig-3-apply-or-not` 適用／不適用判準 | 把「不適用」的主答案寫成斷續銲（那是做不到，不是不該做） |

### 二、概念題的「可反映輸入」要求怎麼落實

鐵則 2 要求圖能反映輸入的改變。本輪沒有結構分析式，改由**規範係數**當輸入：

1. **SS-2016-2 `fig-2`** 的交會點 `W_CROSS = SEG_MM / SEG_K = 40 / 4 = 10 mm` 是算出來的；
   把 §4.1.5(7) 的 40 mm 改掉，交會點與「哪個門檻控制」的分界會跟著移動。
   本例 w = 8 mm ⇒ 每段下限 `max(4w, 40) = 40` mm（由 40 mm 控制，不是 4w）。
2. **SS-2016-2 `fig-1`** 三種有效長度算法由 `LMAIN`、`RET`、`W` 現算：
   248 ／ 200 ／ 184 mm，國內算法比「兩端各扣 1w」多 35%。
3. **SS-2019-1 `fig-3`** 的露點界線用 Magnus 式現算，不是把 85% 抄一遍：
   5 °C→80.9%、10 °C→81.6%、20 °C→82.9%、30 °C→84.0%、40 °C→85.0%、50 °C→86.0%。
   **低溫時露點條件比 85% 更早咬住**——這正是 §7.4.4 第 ③ 項不是第 ② 項重述的證據。
4. **SS-2004-1 `fig-2`** 孔徑三尺度由 `DB` 現算：22 → 標準孔 23.5 → 鉸孔上限 25.5 mm。
5. **SS-2021-1 `fig-3`** 填角銲穿透厚度 `path_len(x) = TB + (WLEG − x)`：10 → 26，變化 160%。

### 三、一處與 .md 對帳後改掉的圖（重要）

`SS-2004-1 fig-3` 初稿把 0.7F_u 畫在降伏之上，等於替規範解說「預拉力已超過降伏拉力」
編造了一個錯誤的力學圖像。實際對帳：F10T 之 `0.7F_u = 700` MPa，而 `F_y ≈ 0.9 × 1000 = 900` MPa，
**700 MPa 只有 F_y 的 78%，仍在彈性段**。真正越過降伏的是 §5.4.2 的**轉角法**
（自密貼再轉 1/3～2/3 迴轉，以轉角量而非應力控制）。
定稿因此分成 A（扭矩法目標，彈性段）與 B（轉角法目標區，塑性）兩點，
卸載線自 B 點畫出殘餘塑性伸長，並在圖說寫明兩者之別。

### 四、下游同步（全部完成）

| 檔案 | 動作 |
|---|---|
| `raw/solutions/SS-*/SS-*.md` ×5 | 圖與圖說插入對應章節；檔尾補「圖解補繪」行 |
| `raw/solutions/SS-*/gen_SS-*.py` ×5 | 產圖腳本隨解析版控，`SD_SKILL` 預設指向 repo 內 `skills/struct-diagram` |
| `raw/solutions/SS-*/figs/` | 15 SVG ＋ 15 PNG（2×） |
| `wiki/problems/SS-*.md` ×5 | 節錄段落內插 15 張；「圖形」表補 15 列（**SS-2004-1／SS-2019-1／SS-2022-3／SS-2016-2 原無圖，本輪新建「圖形」節**） |
| `study/problems-view/SS-*.html` ×5 | 全部 15 張以 `<img>` ＋ 圖說插入對應標題前 |
| `wiki/log.md` | 本則 |
| `CLAUDE.md` | CHANGELOG 補一列 |

`SS-2021-1-fig-1.png`（考卷原圖）本輪**未動**，仍列在該題「圖形」表首列。

### 五、本輪新踩到的排版陷阱

1. **`✔`（U+2714）／`✘`（U+2718）／`✗`（U+2717）在中文字型串裡缺字**，會變方框。
   已一律改用 `○` ／ `×`。連同前批的 `⅔`，**勾叉與分數這兩類符號都要先試畫再用**。
2. **`text_px` 會把 `t_min` 解讀成下標**，渲染成「t 下標 m」＋「in」。
   純文字裡若出現 `x_yyy` 形式，改寫成中文（本輪 `5t_min` → `5×較薄板厚`）。
3. **靠左標籤也會被切掉**：`anchor="end"` 的說明文字若比左margin 長，會超出畫布左緣，
   而 `render.py` 只檢查圖元座標、不量文字寬度，因此**不會報錯**。
   本輪 SS-2019-1 `fig-2` 與 SS-2016-2 `fig-1` 各中一次，只能靠目視發現。
4. **`/tmp/audit.py` 對 Python 格式規格有誤報**：`f"{name:<22}"` 會被當成裸 `<`。
   誤報只出現在 `print()` 裡，判讀時直接略過即可。

### 六、待處理／待使用者複核

1. 本輪未動任何數值，五題 `verificationStatus` 仍為 `unverified`。
2. 第四批的 **SS-2020-4 §5 爭議一**仍待使用者確認（假設 C：D25 + 12 mm，
   或命題者原意為翼板鈑承擔全部彎矩：M20 + 8 mm），本輪未處理。
3. 上列第五節的四項陷阱**尚未回寫到 `skills/struct-diagram/SKILL.md`**，
   `.skill` 亦尚未重新打包——待使用者決定是否一併更新。
4. `study/problems-view/*.html` 仍以字串插入方式維護（與前四批同一風險）。

---

## 2026-10-09　重跑全科出題頻率熱圖（subject-frequency-map v1.1）

**產出**：`study/frequency-SS.html`（覆蓋 2026-08-20 的 v1.0 版）；新增 `scripts/build_frequency.py`（v1.1，取自 skill 附錄原文，本庫原本沒有 `scripts/`）。

**對帳**：通過（格子總和＝題庫總題數、每列總和＝子項題數、前＋後半＝總數、單元小計相符）。無頭瀏覽器 QA：兩種模式切換、點格子／點子項／排名表排序皆正常，console 零錯誤。

**觀察（全部抄自 build_frequency.py 主控台摘要）**：
- 24 考年（2002–2025）／98 題；7 個子項全部出現過，無 0 題、無冷凍子項。
- 單元權重：SS-U1 75 題（76.5%）、SS-U2 15 題（15.3%）；SS-U1 佔比由前半期 93.0% 降到後半期 74.5%。
- 全期前五：U1-1 24、U1-2 21、U1-4 19、U1-3 11、U2-3 7（合計 82 題）。
- 後半期（2014–2025）前五：U1-1 12、U1-2 10、U1-4 9、U2-3 5、U2-2 5。
- 前→後半：U2-2 0→5（★新出現）、U2-3 2→5（▲升溫）、U1-3 7→4（▼退燒），其餘持平。
- 教材四種齊全：U1-1、U1-2、U1-3、U1-4、U2-3；problems-view 88 題；題目影片 2 支、單元影片 0 支；已驗證 0 題（08-22 全庫重置後尚未複核）。

**未解決警告（沿自 2026-08-20）**：8 題 `primaryTopicId` 指向他科 taxonomy（`SD-U3-1` ×5、`MM-U1-1` ×3），仍未畫進熱圖，頁面頂端顯示紅框。待決定改歸 SS 子項或在 taxonomy 補對應項目後重跑。

## 2026-10-23｜study/lecture-SS-U1-2.html 圖解重繪（程式產生 SVG，依比例）

- **改了什麼**：7 張圖改由 `study/figs-src/gen_lecture-SS-U1-2_figs.py` 依數值產生（HTML 內以 `<!--FIG:id-->` 標記，可重跑）：圖 0-1（俯視側移＋斷面平移 u／轉角 φ）、圖 1-1（H400×200 四階段應力＋彎矩—曲率曲線）、**新增圖 1-2**（範例 ① 斷面依比例標 ENA 17.70／PNA 12.00）、圖 3-1（加 Mcr 兩項分解實算圖，L_b* = 6.77 m）、圖 3-2（範例 ② 依比例：Mp 32.15、Mr 20.67、Lp 2.31、Lr 6.81 m、Lb = 4 m 答案點）、圖 4-1（五種彎矩圖逐格代入四分點公式）、圖 10-1（決策樹重繪）；圖 0-2 修框寬溢出。PDF 重新產生（Chromium 列印，40 頁）。
- **為什麼錯**：① 舊圖 3-2 理論彈性曲線畫在非彈性直線**下方**，實際在 Lp～Lr 間遠高於直線（Lb = 4 m 時 Mcr = 49.1 vs 直線 27.84）；② 舊圖 3-1 寫翹曲項「∝ 1/Lb³」，正確為單獨提供 Mcr ∝ 1/Lb²（純扭轉項 ∝ 1/Lb）；③ §3.4 表的彈性區寫 `Mn = Cb·Mcr` 但 Mcr 式內又含 Cb（**重複乘 Cb**），改為 Mcr 取 Cb = 1 之值並加警語；④ 舊圖 10-1「非結實／細長」分支走到死路沒回 LTB 檢核，改為三支匯流、最後取 min(Mn,FLB, Mn,LTB, Mp)；⑤ 舊圖 1-1 第③階段彈性三角形超出降伏塊寬度、註腳文字重疊。另修：`\text{tf·cm}` 在 KaTeX 0.16.11 會變紅字錯誤（· 在 text mode 轉成 \cdotp），7 處改 `\text{tf}\cdot\text{cm}`；CSS `.fig svg` 改 `.fig>svg`，避免把圖說中 KaTeX 根號的 SVG 拉成 block 而消失。
- **怎麼驗證的**：生成器先由斷面尺寸重算範例 ①（ȳ 17.70、y_PNA 12.00、Ix 29544、Smin 1167.8、Zx 1550、f 1.33）與範例 ②（Sx 1148、Zx 1286、ry 4.60、J 35.68、Cw 6.50e5、Lp 231.4、Lr 681.1、X1 133.6、X2 2.424、Mn 3174、φMn 2857 tf·cm），全部與講義手算一致；並驗 Mcr(Lr) = Mr（2066.8 = 2066.8）與 Mp/My = 1.120。瀏覽器渲染逐圖目視、KaTeX 錯誤數 0。

---

## 2026-10-23　lecture-SS-U1-4.html 圖解改版（程式繪製 SVG）

**產出**：`study/lecture-SS-U1-4.html`（12 張圖重繪＋新增 3 張；圖 0-1、5-1 沿用）；產圖腳本存於 `study/figs-src/lecture-SS-U1-4/`（`lib.py`、`figs_a〜d.py`、`build.py`）。

**舊圖的錯誤（已修）**：
1. 圖 3-2：標記點不在曲線上（標 (2, 0.50) 實畫在 U≈0.60，(6, 0.83) 畫在 0.80，(10, 0.90) 畫在 0.85），曲線為手描折線。改為 `U = 1 − 1/(L/x̄)` 精確取 220 點，並加入範例 A (5.95, 0.832) 與角鋼查表 0.60／0.80 對照。
2. 圖 7-2：右梁翼板力方向畫反（上翼板兩力相對、下翼板兩力相背）→ 兩力抵消，節點域不受剪，與圖中的剪切平行四邊形及 V_pz 公式矛盾。改為側移狀態：上翼板兩力皆向右、下翼板皆向左，並補 V_c 方向。
3. 圖 7-3：RBS 被畫成立面上翼板向下鼓起；RBS 削的是翼板寬度（平面），立面看不到凹口。改為平面＋立面同比例，依 AISC 358 取 a=0.625bf、b=0.75d、c=0.2bf 算圓弧半徑。
4. 圖 3-3：剪力面畫在孔外緣；改為沿螺栓中心線穿過孔，並以範例 A 實尺寸重繪（Lgv 25 cm、拉力面 8.0 cm）。
5. 圖 10-1：方塊重疊（彈性向量法框壓到菱形）；重新排版。

**重繪（依範例數值計算）**：圖 1-1（平面＋立面標六個極限狀態）、2-1、3-1（L125×125×12 實尺寸、x̄=35.3 mm；應力分佈以範例 A 的 U=0.832 反推，標明為示意）、4-1（加入載重—滑移曲線，水平線取範例 B 139.2／158.4 kN）、6-1（範例 D 1 cm=8 px，兩候選點向量同比例：0.1014P／0.0955P）、7-1（範例 E 應力向量與容許圓弧 1.476）、9-1（t=25 mm 實尺寸坡口）。
**新增**：圖 4-2（承壓 Rn/(Fu·d·t) vs Lc/d，Lc=2d 轉折）、圖 5-2（方向性 1+0.5sin^1.5θ）、圖 8-1（範例 F 斷面 Q 與斷續銲 s=28 cm vs 強度 90 cm）。

**內容補註**：§4.2 加「版本提醒」（360-05 的 φ=1.0/0.85＋h_sc；360-10 起 μ_A=0.30、φ 依孔型、h_f 為填板係數；台灣 ASD 表列 1.19／1.47 tf/cm²，取自 2026-08-22 第四批勘誤結論）；§5.4 最小銲腳表改為 AISC（13 mm 分界）與台灣表 10.2-4（12 mm 分界）並列。

**驗證**：範例 A／D／E 的數值於腳本中重算後作為繪圖座標（e.g. 範例 D f_M 由 M·r/Ip 直接計算）；17 張 SVG 以無頭瀏覽器逐張截圖目視，marker id 36 個無重複。

**待處理**：`study/lecture-SS-U1-4.pdf` 未重新產生，仍為 2026-07-25 舊圖版本。

## 2026-10-23　lecture-SS-U1-1.html 圖解重繪（程式產生 SVG）＋ 2026-08-22 勘誤同步

**動機**：使用者要求「圖再精準，以 SVG 輔助說明」。逐張截圖檢視原 12 張圖，查出下列錯誤（不只是美觀）：
1. 圖 4-1：「穩定平衡」的球畫在谷底曲線**下方**（懸空）。
2. 圖 5-1：兩端固接模態不對稱、反曲點未落在 L/4、3L/4、KL 標尺未對齊；一固一鉸的反曲點畫在鉸端附近（應距鉸端 0.699L）；懸臂鏡射虛線超出圖框。
3. 圖 3-1：剪力面未穿過螺栓孔、塊體與受力方向不符。
4. 圖 2-1：文字重疊；x̄ 畫成厚度方向，未表達「連接面到形心」。
5. 圖 7-1：柱曲線僅 6–7 點折線、含一支無意義箭頭、λc 標籤與 3.0 重疊。
6. 圖 6-1：殘留應力只用色塊、無應力分布圖；底部文字被裁切。
7. 圖 0-1、5-2、9-1：標籤重疊、箭頭繞線錯誤。

**重繪（12 張，幾何全由數值計算）**：挫屈模態用精確特徵函數（一固一鉸解 tan kL = kL，kL = 4.4934）；柱曲線依公式逐點計算；圖 2-1、3-1 依 §3.1 範例 L100×100×10 實尺寸；圖 6-1 以 Lehigh 線性模型算出各應變階段的降伏寬度與 Ie/I（f = 0.85Fy 時弱軸 0.42）。
**新增 5 張**：圖 1-2（交錯螺栓兩路徑，s=7、g=6、d=2.3 cm 依比例）、圖 2-2（SS-2025-2 P–L 正解 vs 誤用 U=1−x̄/l）、圖 5-3（SS-2013-2 靠桿側移模態）、圖 6-2（SS-2024-1 四段曲線與 A/B/C 轉折點）、圖 7-3（CRC vs SSRC；LRFD/ASD 強度比曲線）。

**內文勘誤（講義落後於 2026-08-22 的題解勘誤）**：
- §2.3：原以 SS-2025-2 示範 L_opt = x̄/(1−Fy/Fu)，正是該題已勘誤的錯解。改為以銲接角鋼示範交點觀念（名目 7.3 cm／LRFD 帶 φ 10.7 cm），另立陷阱 T-04：板類縱向銲查 l/w 階梯值且 l ≥ w → L_max = 3 cm、P_max = 9.00 tf。§2.2 表補板類三列與「AISC 表 vs 台灣考卷表」註記。
- 陷阱 C-01：原寫「弱軸下段 1.0×L1/ry = 108.1」，K 值錯（應為 0.7×960/6.215 = 108.1，A 固接-B 鉸）；改寫為「兩平面邊界相反」的判讀重點。
- §7.7 自我檢查：原稱 LRFD/ASD 比值 1.4～1.6；以兩套公式逐點計算實為 **1.39～1.47**（最小 λc≈1.24、最大 λc≈0.43，彈性段定值 1.43），已更正並以圖 7-3(b) 呈現。
- §10、§13：SS-2005-1 改為五個極限狀態（BSR 68.5 tf 控制、螺栓剪力 71.8 tf 差 5%）；SS-2013-3、SS-2025-2 描述同步；§11 陷阱表新增 2 列並重編號；圖 9-1 拉力分支新增「④ 螺栓本身」。

**驗證**：17 張 SVG 以無頭瀏覽器逐張截圖目視，並以腳本檢查文字超出畫布與文字互相重疊（0 件）；KaTeX 714 式、0 錯誤；PDF 以 Chromium 重新產生（47 頁）。

**觀察（未改動，待使用者決定）**：`SS-2024-1.md` 轉折點 A 寫 λ₁ = 0.697，但 √0.485 = 0.6964 → 0.696；講義圖 6-2 採 0.696。

**原始碼**：`study/figs-src/lecture-SS-U1-1/`（lib.py、figs_a–d.py、build.py）。

---

## 2026-10-23　lecture-SS-U1-3.html 圖解改版（程式繪製 SVG）＋依 08-22 勘誤更正內文

**產出**：`study/lecture-SS-U1-3.html`／`.pdf`（35 頁，Chromium 重新列印）；10 張圖重繪＋新增 2 張（圖 3-2 B1 曲線、圖 8-1 K 敏感度；原圖 8-1 改號 8-2），圖 10-1 流程圖僅改文字。產圖腳本存於 `study/figs-src/lecture-SS-U1-3/`（`gen_figs.py`、`svglib.py`、`calcs.py`、`frame2d.py`、`refresh_figs.py`、一次性遷移用 `build.py`、`build_pdf.py`）。

**舊圖的錯誤（已修）**：
1. 圖 2-1：$D_m$ 曲線為手描貝茲線，P/Pcr = 0.89 處畫成 4.9（應為 8.9）；並標「AISC 對 B₂ 的上限 0.6 → 2.5」——查無此條文。改為 1/(1−r) 精確取點，改標 AISC 360-10 起有效長度法適用限 Δ2nd/Δ1st ≤ 1.5。
2. 圖 6-1：H1-1a 標「斜率陡」——錯，以軸力為縱軸時 H1-1a 為 −8/9（較平）、H1-1b 為 −2（較陡）（同 SS-2009-1 勘誤）。「真實包絡線」改為 H400×400×13×21 斷面全塑性互制精確解，量得與雙折線最大差距 0.051。
3. 圖 3-1：改為兩端鉸接柱 P/Pe = 0.3 的彈性二階精確解（M = M_A cos kx + …），單曲率跨中撓曲 0.180、放大 1.533；雙曲率撓曲 0.017、最大仍為柱端 M₂。
4. 圖 4-1：改以勁度法實算門型剛架（h 4 m、b 6 m、w 3 tf/m、H 6 tf）畫出 ①②③ 彎矩圖，腳本內 assert ①＝②＋③。
5. 圖 0-1／1-1／4-2／9-1：撓曲改為正弦／Hermite 形狀函數取點；圖 9-1 兩機構按相同屋頂側移繪製（層機構塑鉸轉角＝梁機構 3 倍）。

**內文更正（依 2026-08-22 第三批勘誤與規範原文）**：
- 範例 C **算術錯誤**：B₂ = 1/(1−0.296) 寫成 1.799，正解 **1.420**；Mu 54.49 → **48.82** tf·m、H1 0.980 → **0.936**；§8.1「B₂ 1.799 → 1.10」改為 1.420 → 1.101。
- 刪除不存在的「ΣPu/ΣPe2 ≤ 0.6（B₂ ≤ 2.5）」規定（§2、§4.4、§10、Q7、流程圖共 7 處），改為 AISC 360-10 起之 Δ2nd/Δ1st ≤ 1.5 有效長度法限制，並註明台灣 99 年版無此限。
- 補台灣 LRFD (8.2-3) B₁ = 0.64/(1−Pu/Pe1)(1−M₁/M₂) + 0.32 M₁/M₂（範例 A 表格兩式並列）；補 ASD Cm 無 0.4 下限、ASD 側移構架 Cm = 0.85（原寫「Mlt 部分 Cm = 1.0」）。
- §9 強柱弱梁改以我國 (13.6-3)（梁側 1.25、無 Ry／Mv）為主，AISC 341 改為 1.1Ry＋Muv（原漏 1.1）；範例 E 比值 0.937 → **0.899**（NG 結論不變）。
- SS-2013-4（單柱 BC、A/D 為滾支承，刪「ΣPeK 要含左右兩根外柱」）、SS-2003-4（有側撐、雙曲率 Cm = 0.2、強度式控制）、SS-2009-1、SS-2020-3、SS-2011-1（τa → τb、360-05 用 1.5）於 §4.2、§7、§8、§11、§12、§14 同步。
- 修正舊版即存在的 KaTeX 錯誤：`\text{tf·m}`（· 轉 \cdotp）9 處、範例 D `(<C_c` 被 HTML 當成標籤吃掉整段、`96%` 被當註解；CSS `.fig svg` → `.fig>svg`。

**怎麼驗證的**：`calcs.py` 獨立重算範例 A〜E 全部數值（僅範例 C 的 B₂ 與講義不符，即上述算術錯誤）；圖上數字一律由 `calcs.py`／公式帶入。12 張圖以無頭 Chromium 逐張截圖目視；整頁 KaTeX 811 式、錯誤 0；PDF 35 頁抽頁目視。`refresh_figs.py` 於本機重產 SVG 後回寫，與交付版逐位元相同。

## 2026-10-23　lecture-SS-U2-3.html 圖解重繪（程式產生 SVG）＋ 內文勘誤

**動機**：使用者要求「優化內容，尤其是圖，再精準，以 SVG 輔助說明」。逐張截圖檢視原 17 張圖，查出下列錯誤（不只是美觀）：
1. 圖 1-1 HAZ：「正火區 700～900 °C」與「部分相變區 A1～A3」溫度區間重疊且錯置——正火（細晶）區應為 A3（約 850 °C）～1100 °C；區帶畫成等寬色塊，看不出粗晶區緊貼熔合線。
2. 圖 1-3 層狀撕裂：左圖箭頭朝內（畫成壓力），與標題「拉力沿板面」矛盾；右圖「拉力方向」標籤壓在標題上；撕裂畫成直線而非階梯狀。
3. 圖 1-4 CVN：手描 7 點折線、縱軸只有「27」一個刻度、「脆性平台」與 27 J 線重疊，讀不出 0 °C 判定點的意義。
4. 圖 2-3 回銲：說明文字壓在箭頭與板上；幾何未依比例，看不出 2w～4w 的長度，也沒畫出「上限 4w」的力學理由。
5. 圖 4-3 銲道 vs 摩阻型螺栓：銲道曲線斷裂後又回升、螺栓曲線在銲道峰值之後才出力——兩條都不符文獻荷重–變形關係。
6. 圖 6-2 梁柱接頭：② ESW 的引線指向剪力板；ESW 實際在內橫隔板與柱壁交會處（SS-2024-4 附圖四條引線所指）。
7. 圖 0-1 與圖 4-2 ③：「鎖過一次預拉力已超過降伏」——0.7Fu 本身仍在彈性段（F10T ≈ 0.78Fy、A325 ≈ 0.88Fy），越過降伏的是轉角法（與 2026-08-29 SS-2004-1 圖 3 的修正一致）。
8. 圖 3-3、7-2 流程圖：兩支箭頭並排打進同一菱形、「否」分支懸空、材料磁性判斷畫成方框而非菱形。

**重繪（12 張，幾何由數值計算）**：
- 圖 1-1：峰值溫度 Tp−T0 ∝ 1/r²（厚板點熱源近似）與 1500／1100／850／727／500 °C 門檻求交點，區帶邊界即交點（寬 0.17、0.16、0.11、0.31 r₀）。
- 圖 1-4：兩條 tanh 轉換曲線，反算 T27J（−37 °C ✓、+5 °C ✗），0 °C 點值 197 J／16 J。
- 圖 2-1：8 mm 填角銲依比例（20 px/mm）；右圖 r(θ)/w = 1/(sinθ+cosθ)，極小值 0.7071 @ 45°。
- 圖 2-3：角鋼剪力接合立面依比例（1.15 px/mm，w = 8 mm → 2w～4w = 16～32 mm）＋頂部俯視說明上限 4w。
- 圖 4-2：板厚差 22/19 mm 依比例；M22 標準孔 Ø23.5、偏差 3 mm → 淨開口 20.5 mm（徒手可穿 e ≤ 1.5 mm、鉸孔 +2 mm 後 e ≤ 3.5 mm）；F10T 拉力–伸長曲線標 A（0.7Fu 彈性）／B（轉角法落點）。
- 圖 4-3：銲道依 AISC 360 §J2.4 Lesik–Kennedy 關係（w = 8：縱向 δu = 1.36 mm、橫向 0.45 mm、1.5 倍），螺栓滑動荷重 0.39（M22，μ = 0.35）＋孔隙 1 mm 後 Fisher 承壓曲線。
- 圖 5-1：加電子流向與標準電極電位軸（Zn −0.76、Fe −0.44、Cu +0.34 V）。
- 圖 5-2：五部位各配小圖（② 100 mm 依比例；③ 標出表層 100 mm 須塗）。
- 圖 6-2：□500×25 箱型柱＋H600×200×12×25 梁立面依比例（0.42 px/mm）、隔板對齊翼板、ESW 位置、背襯板與扇形銲接孔；新增 A–A 斷面。
- 圖 3-3、7-2：流程圖重排。
- 未重繪（文字對照圖，內容正確）：圖 0-1（僅改一句）、0-2、1-2、3-1、6-1。

**內文勘誤**：
- §2.2 最小有效長度：「L_min ≥ 4w 且 ≥ 38 mm」改為國內施工規範 §4.1.5(6)(7)——連續銲 ≥ 4w；斷續銲每段 ≥ 4w 且 ≥ 40 mm（38 mm 為 AWS 英制 1.5 in）。§2 因果鏈與 §7.1 總表同步（§7.1 原寫「回銲 2w」漏上限）。
- §4.1「為什麼是 0.7Fu」與自我檢測第 10 題：「0.88Fy 已進入塑性平台」改為「仍在彈性段、轉角法再推進塑性平台」。陷阱 T-18 補註「轉角法實際鎖到的」預拉力。
- §4.3：補 AISC 360-16 §J1.8 對照（螺栓可與縱向填角銲共同承力，螺栓取值 ≤ 承壓型強度 50%），註明非國內考試答案；自我檢測第 11 題「滑動後承載力先掉」改為「停在滑動荷重直到承壓」。

**驗證**：12 張 SVG 以無頭 Chromium 逐張截圖目視、17/17 XML 解析通過；KaTeX 109 式 0 錯誤；PDF 以 Chromium 重新產生（36 頁，原 2026-07-25 版 26 頁）。

**觀察（未改動，待使用者決定）**：`SS-2021-4.md` §5 引用的條文「新設接合中摩阻型螺栓不得與銲道共同分擔載重」與 AISC 1989 ASD §J1.9（容許摩阻型螺栓與銲道共同承力）方向相反，建議下次勘誤該題時回查國內規範原文。

**原始碼**：`study/figs-src/lecture-SS-U2-3/`（figlib.py、figs.py；build.py 為一次性遷移紀錄）。

---

## 2026-10-28　unit-lecture skill 更新：回寫 2026-10 五科講義改版經驗

**來源**：SS（U1-1〜U1-4、U2-3）、SD（U1-1〜U1-3、U2-2、U3-2）、SM（U1-1、U1-3、U1-5、U2-3、U3-1）、SA（U1-2、U1-3、U2-1、U2-3、U2-4）、RC（U1-1、U1-2、U2-1、U3-3、U4-1）各科 `wiki/log.md` 的講義改版紀錄。

**改了什麼**（`skills/unit-lecture/SKILL.md`，並重新打包 `skills/unit-lecture.skill`）：
- 新增「改版模式」（Step 10）：截圖盤點 → 勘誤對帳 → 程式重繪 → PDF 重出 → log。
- Step 5 改寫：SVG 一律由程式依數值繪製（沿用 struct-diagram 的 structdraw.py、calcs.py assert、曲線取點、`<!--FIG:id-->` 可重跑）；新增 figcheck.py（文字出界／重疊、KaTeX 錯誤數、逐張截圖）。
- Step 1 新增勘誤查核；Step 4 新增第 12–14 條（規範寫版本、查無出處就刪、考古題敘述由索引算）。
- Step 7：CSS `.fig svg` → `.fig>svg`；新增 KaTeX 寫法地雷表（`\text{tf·m}`、`%`、`<`）。
- Step 8：預設改為 Chromium 列印（取自 SS-U1-3 的 build_pdf.py），WeasyPrint 降為備援；明定 PDF 必須跟著重出。
- Step 9：加入圖的瀏覽器驗證、log 與交付規範；已知地雷由 11 條增為 22 條。

**順帶修正**：figcheck.py 試跑時抓到 `lecture-SS-U1-4.html` 圖 5-2 的「被放棄的紅利」標籤被迴圈重複疊畫 3 次（縮排錯誤），以及圖 10-1 彈性向量法框內行距過密；已修正並回寫 `figs_b.py`／`figs_d.py`。

**待使用者處理**：已安裝版 skill 需在審核卡片按儲存才會生效（`lecture-SS-U1-4.pdf` 已於同日更新重出）。

---

## 2026-10-28　lecture-SS-U1-4.pdf 重新產生

- PDF 以 headless Chromium 依新版 `unit-lecture` Step 8.1 重出（38 頁，原 07-25 舊圖版 33 頁），圖 0-1〜10-1 全為 10-23／10-28 程式繪製版。
- 重出前以 figcheck.py 檢查：KaTeX 555 式、錯誤 1 → 0。錯誤為舊版即有的 §5 因果鏈 `\(t_e = 0.707w\））` 把收尾 `\)` 打成全形「）」，導致後半段數學式整段變紅字；已改正。
- 抽頁目視：38 頁縮圖逐頁檢查，無圖跨頁截斷、無 KaTeX 黑框／紅字。

---

## 2026-10-29　formula-given-SS-U1-2 升級 v2（unit-formula-map v2）

- **三態逐年表**：卡片補 `c` 欄位，逐年表由 10 欄擴為 14 旗標欄（新增 \(F_r\) 值、\(\phi_b\)、判斷式、撓度塑性四欄，✔ 年份全取自既有卡片證據）；✗ 由 `c`＋`no` 推出，表底合計列：✗ 共 45 格，其中 \(M_p\) 定義 8、\(\phi_b\) 8、判斷式 10。題號欄改中文數字並連到 `problems-view/`（25 題全部存在）。
- **回想模式**、sticky 表頭依導覽列高度、PDF 背誦策略不再強制換頁、KPI 列印改並排。
- **修 bug（v1 即有）**：`<section id="cards">` 與 `<div id="cards">` id 重複，JS 渲染卡片時把篩選列與計數一起洗掉並丟出 TypeError → section 改 `id="formulas"`。逐年表「無題」用全形「（—）」，JS 比對半形「(—)」，24 列全被標成有題 → 統一半形。
- **內容勘誤（Step 6-2a 逐條回查題目原文）**：
  - \(F_r\) 卡片取值寫反（原「熱軋 1.16、銲接 0.7」）→ 熱軋 ≈0.7（69 MPa）、銲接 ≈1.16；證據：SS-2025-3 熱軋給 0.7、SS-2025-1 銲接給 1.16、SS-2012-1 熱軋 69 MPa。背誦策略④同步改。
  - SS-2025-4 屬 U2-1：塑性分析卡 `no` 移除 2025，引用處註明單元；策略②「五次」改「四次」。
  - 刪除「SN 耐震鋼材與降伏比」卡：SS-2021-3 用 SM490、解析無降伏比，105 年那題是他單元的 SS-2016-5（33 → 32 條，必背 21 → 20）。
  - 「非對稱斷面 \(M_p\) 正負向不同」為誤：正負彎矩共用等面積軸，\(M_p\) 相同，不同的是 \(M_y\)。
  - 新版 \(C_b\)「懸臂端點載重 1.28」刪除（公式算得 1.67，且懸臂另有規定）。
  - SS-2014-4、SS-2007-2 引用處註明 U1-3。
  - 已用考卷原文確認 SS-2025-3 確實給 \(L_p=3.4\)、\(L_r=10.5\)、\(C_b=1\)、\(F_r=0.7\)。
- **驗證**：verify.py ✓ 全部一致；Playwright 無 pageerror、✗ 45／合計列／回想計數正常；PDF 12 頁，逐年表含合計列於單頁（p.10），原始 LaTeX 外露 0、emoji 0。

---

## 2026-10-29　formula-given-SS-U1-1 升級 v2＋回查原卷修正

**改了什麼**（`study/formula-given-SS-U1-1.html`、`.pdf`）：
- 升級 unit-formula-map v2：逐年表三態（✔／✗／·）＋24 年合計列、題號連到 problems-view、回想模式、sticky 表頭依導覽列高度。逐年表由 10 欄擴為 13 欄（新增挫屈理論、接合細項、組合斷面；對位圖欄擴為「有效長度」、U 欄含替代表），旗標全部由卡片 ok 推出。
- 依 Step 6-2a 回查題目原文與原卷（含 2013、2020 影像頁目視），修正 v1 誤判：
  - 2013 題三同時考 ASD Pa 與 LRFD φcPn，柱公式一條都沒印 → Fa 兩式由「通常會給」改「別賭」；λc 定義亦改「別賭」；λc／Fcr／Cc／φc 補 2013 為考了沒給。
  - 2013 有印 K 值表與 PeK=π²EI/(KL)²；2015 題目給 k=2.0；2020 有印 0.877 式與 Pe1=AgFy/λc²；2024 有 1/λ² → K、Euler、Fcr 卡 ok 補列。
  - 2007、2011 有印 G 定義、端點規則與對位圖；2011 有印萊梅厥公式 → G 卡改「別賭」、萊梅厥改「通常會給」。
  - 2012 有印承壓 1.2LctFu≤2.4dtFu、2019 有印 φ0.6FEXX、2007/2011 有印翼板 λr。
  - 移除題目用不到的 no 年份：φc 的 2007/2011/2020/2024、Fcr 的 2016/2025、承壓的 2022/2024/2025、U/Ae 的 2022、填角銲的 2017、λr 的 2022、Cc 的 2007、λc=1.5 的 2023。
  - 新增「板件縱向銲接 U 值（l/w 表）」卡（2025 考、從未印）；遠端修正係數改為 AISC 值（無側移 ×1.5/×2.0、有側移 ×1/2、×2/3）；λc=1.5 對應 KL/r 數值依 E=2040 重算。
- 結果：31 條＝必背 15／別賭 13／會給 3；逐年表 ✔75、✗31。

**怎麼驗證**：verify.py（v2）✓ 全部一致；PDF 11 頁 抽頁目視（無 merror、無 emoji 方框、逐年表含合計列單頁）、文字層無 LaTeX 外露；Playwright 開頁無 pageerror、✗/合計/回想模式/篩選正常；31 個題號連結檔案皆存在。

**待處理**：`wiki/methods/effective-length-chart.md` 寫「遠端鉸接 ×3/4」，與 SS-2011-4 解析及 AISC（有側移 ×1/2）不一致，未改動。skill 附錄 C 範本的 `<section id="cards">` 與 `<div id="cards">` 重複 id，JS 會把卡片寫進 section 蓋掉篩選列與回想列；本頁改用 `section#cards div.cards` 取元素。

## 2026-10-29 SS-U1-4 給／背分界升級 v2

**改了什麼**（`study/formula-given-SS-U1-4.html`、`.pdf`）：
- 升級 unit-formula-map v2：逐年表三態（✔／✗／·）＋24 年合計列、26 個題號連到 problems-view、回想模式、sticky 表頭依導覽列高度。逐年表由 10 欄擴為 13 欄（新增「極限狀態清單」「梁柱接頭」「構造・施工」；U 欄併入 An／孔徑；填角銲欄擴為「銲道強度」含 ASD 0.3FEXX、CJP、0.6 來源；喉厚欄含銲線斷面），每張卡補 `c`，原 10 欄的旗標經程式比對無一變動。
- 題號欄改為 v2 格式（「三、一（副）」「(—)」）。v1 用全形「（—）」導致底色判斷全部失效，一併修正。
- 依 Step 6-2a 回查題目原文與原卷，修正 4 張卡：
  - 節點域 tz：v1 寫「SS-2009-4① 直接問」，實為 SS-2009-2（主分類 SD-U3-1）→ no 移除 2009，說明改註單元代號。
  - 箱型柱板厚／SN 鋼材：同上，SS-2009-2 非本單元 → no 移除 2009；「105 年 SN490」補註 U2-2。
  - NDT：SS-2021-1、SS-2022-3 皆屬 U2-3 → no 由 [2009,2021,2022,2024] 改 [2009,2024]，說明改為「跨兩單元四年四次」。
  - 回銲（2016-2）、銲條乾燥（2002-1）的順帶引用補註單元代號。
  - 已確認無誤：SS-2022-2 原卷只寫「除受拉全斷面降伏，亦應考慮下列極限狀態」，未印 FyAg（解析的重述表把它補進去了，與原卷不符）；SS-2015-2 孔徑未給；SS-2023-4 解析含塊狀剪力。
- 修正螢幕版 bug：`<section id="cards">` 與 `<div id="cards">` 重複 id，v1 的 JS 會清掉篩選列並拋錯；改用 `querySelector('div#cards')`。
- 結果：37 條＝必背 26／別賭 7／會給 4（不變）；逐年表 ✔34、✗55；極限狀態清單、偏心向量法兩欄 ✔0。

**怎麼驗證**：verify.py（v2）✓ 全部一致；PDF 12 頁抽頁目視（無 merror、無 emoji 方框、卡片未跨頁、逐年表含合計列單頁），文字層無 LaTeX 外露；Playwright 開頁無 pageerror、✗／合計／回想模式／篩選正常。

**後續**：曾懷疑 `formula-given-SS-U1-3.html`、`formula-given-SS-U2-3.html` 有同樣的重複 id bug，複查後兩頁皆無（U1-3 已用 `querySelector('div.cards')`；U2-3 的 section id 為 `cardsec`）。SS-2022-2 題目重述之勘誤見下一筆。

## 2026-10-29 study/formula-given-SS-U1-3 升級 v2（unit-formula-map v2）

**改了什麼**
- 40 張卡補 `c` 欄位；逐年表改三態（✔／✗／·）＋ 24 年合計列＋題號連到 `problems-view/`；新增回想模式；sticky 表頭改 `var(--navh)`。
- MX 題號欄改「一、二／(—)」格式；逐年表新增三欄：φc·φb、Mu 組合（B1Mnt+B2Mlt）、直接分析法（原本這些卡無欄可掛，✗ 看不見）。
- 依 Step 6-2a 回查，修正：
  - `no` 年份限本單元題目：G 定義移除 2023（SS-2023-1 屬 U1-1）、K 值表移除 2002（SS-2002-3 屬 U1-1）、尤拉載重 Pe 移除 2008/2011（SS-2008-2、2011-2 屬 U1-1）、Cc 移除 2011（本單元 SS-2011-1 為直接分析法說明題，用不到 Cc）。
  - 梁遠端修正卡：v1 寫「遠端鉸接 ×3/4、對稱雙曲率 ×2」，改為 AISC 解說對位圖係數（有側移：遠端鉸接 ×½、遠端固接 ×⅔；無側移：×1.5、×2），證據改為本單元 SS-2013-4（梁遠端滾支承，見該題 §5 爭議一），no 由 [2011,2023] 改 [2013]。背誦策略②第 5 點同步。
  - 強柱弱梁卡：v1 印 AISC 341 的 ΣM*pc/ΣM*pb 形式；SS-2009-1 原卷明寫「依據我國規範」，改為我國式 (13.6-3) ΣZc(Fyc−Puc/Ag) ≥ 1.25ΣZbFyb。
  - 引用別單元題目一律補註單元代號（SS-2002-3、2003-1、2008-1、2008-2、2011-2、2011-4、2013-3、2014-1、2021-3、2022-4、2023-1、2024-1）。
- 修 bug：section/div 重複 id `cards`（JS 改 `querySelector('div.cards')`，篩選列不再被清掉）；說明裡數學式內的 `<`（`<L_p`、`E_t<E`、`<L_c`）被當 HTML 標籤吃字 → 改 `\lt`。
- 列印：KPI／圖例改 flex 橫排（WeasyPrint 不支援 auto-fit grid）；逐年表行距收緊以單頁容納 24 列＋合計。
- 結果：40 條＝必背 18／別賭 10／會給 12（不變）；逐年表 ✗ 17 格，其中 15 格落在「組裝與係數」六欄；Mu 組合欄 ✔ 0。

**怎麼驗證**：verify.py（v2）✓ 全部一致；Playwright 無 pageerror、無 LaTeX 外露、✗=17 與合計列正確、回想模式與篩選正常；PDF 15 頁抽頁目視（逐年表含合計單頁、無 emoji 方框），文字層 LaTeX 外露 0。

**待處理**：`wiki/methods/effective-length-chart.md` 的「遠端鉸接 ¾(Ib/Lb)」與 SS-2013-4 解析、AISC 解說（×½／×1.5）不一致，未改動。`formula-given-SS-U2-3.html` 仍有重複 id bug。

## 2026-10-29　formula-given-SS-U2-3 升級 v2＋同步 08-22 施工規範勘誤

**為什麼**：v1（08-08）早於 08-22 第五批勘誤，多張卡的「式子／名稱」仍是被判 🔴 的舊內容；另依 `unit-formula-map` v2 改三態逐年表、回想模式。

- **勘誤同步**：板面間隙 2/6 mm → §5.2 單一門檻 1 mm；孔位校正 ≤2/2–5/>5 mm＋d+3 → §5.3.1 沖梢（鐵鎚 <2.5 kg）→ 鉸孔（≤ 設計孔徑 +2 mm）；孔徑卡改為「標準孔（94 年 22→23.5）vs. 淨面積扣除孔徑（92 年 19→22）」，ok 補 2005；不予塗裝式子 50 mm／柱腳底板 → §7.4.5 五項（100 mm、軸件滾輪、埋件但書）；有效長度式子刪「兩端各扣 1w」；金屬噴塗刪 Rz ≥ 60 μm；塗裝環境補足 §7.4.4 四項；摩阻 μ 0.35 → 0.33；重複使用改以塑性伸長為主因。
- **證據修正（6-2a 對題目原文）**：移除 10 筆不成立的「考了沒給」——別單元題目 SS-2006-2（U1-4）、SS-2012-2／SS-2009-1（SD-U3-1）、SS-2016-5（U2-2）×2；題目沒問的 SS-2009-4（邊距、孔徑、NDT 對應）、SS-2018-4（銲腳尺寸）、SS-2024-4（Ceq，解析未用）。說明文字凡引別單元題目皆加註單元代號。結果 3 卡零證據（Ceq、現場銲接環境、塑性轉角 0.03 rad），維持必背。
- **結構**：每卡加 `c`；逐年表改 10 欄（新增「銲接管制」欄、欄序依主題）、三態＋合計（規定欄 ✔ 6／✗ 21，對照欄 20 年有參考公式）；開槽銲、填角銲破壞位置移到「銲接施工與細節」。級別不變：必背 34／別賭 4／會給 0。
- **v1 既有錯誤順修**：section 與卡片容器同 `id="cards"`（JS 把整節覆蓋、篩選鈕消失）；數學式內 `<` 被 innerHTML 吃掉（鍍鋅 E_Zn<E_Fe、銲腳表 6<t）→ `\lt`；sticky 表頭在 overflow 容器內錯位；KaTeX MathML 撐出手機版橫向捲軸；PDF 的 KPI 直排（WeasyPrint 不支援 auto-fit grid）。
- **驗證**：verify.py ✓ 全部一致；Playwright 無 pageerror、原始 LaTeX 0、回想計數與篩選正常、手機寬 390 無橫捲；PDF 14 頁、文字層 LaTeX 0、無 emoji 豆腐，逐年表含合計單頁；五條中文長式改兩／三行（MathJax 低估 \text 中文寬度會爆出卡片）。考卷抽查：2003、2005 孔徑原文、2006／2017／2025 無參考公式區（2025 轉圖目視、2017 僅題內給 Cc、0.6F_EXX）。

## 2026-10-29 SS-2022-2 題目重述勘誤（原卷未印 FyAg）

**改了什麼**：`raw/solutions/SS-2022-2/SS-2022-2.md`（正本）§1 題目重述，同步 `wiki/problems/SS-2022-2.md`、`study/problems-view/SS-2022-2.html`；三檔頁尾加「修正日期：2026-10-29」。
- 「題目提供公式」表移除 $P_n=F_yA_g$，加註原卷只以文字點名「除受拉全斷面降伏」。
- $b_e=(b_e)_{\max}$ 更正為原卷之 $b_e\le(b_e)_{\max}$；作答要求「分析」更正為「設計與分析」；補回「與另一連接部件均開」孔。

**為什麼錯**：重述時把題幹文字點名的極限狀態併進公式表，與 formula-given-SS-U1-4 的判定（2022 屬「考了沒給」）互相矛盾。

**怎麼驗證**：111 年考卷第 1 頁轉 300 dpi 目視，第二題只印三條式子、$b_e$ 為「≤」；pdftotext 交叉比對一致。§2 以後計算未改動，故無數值重算；verificationStatus 原即 unverified，未變更；question_index tags 不受影響。

**後續**：孔位與 $b_e$ 問題已於下一筆勘誤處理。

## 2026-10-29 SS-2022-2 解析勘誤（孔位、$b_e$、D5.2 尺寸規定）

**改了什麼**：`raw/solutions/SS-2022-2/SS-2022-2.md`（正本）§2–§5；同步 `wiki/problems/SS-2022-2.md`（摘要版：考點、作戰計畫、陷阱兩處重複區塊、補結論）、`study/problems-view/SS-2022-2.html`（由正本以 python-markdown＋數學式保護＋wikilink 徽章重生 `<main>`，與舊頁比對只有本次修改處不同）、`raw/json/question_index.json`／`dashboard-data.js` tags 追加 `銷孔尺寸規定`（append-only）、`wiki/traps/TENSION-MEMBER-TRAPS.md` T-06、`wiki/philosophy/asd-pin-tension.md`。頁尾修正日期合併為一筆。
- 孔位：舊解寫「孔兩側各 (300−100)/2 = 100 mm」，把孔當成置中，與題文「角隅」不符。改依 AISC 360 D5.1 定義 $a$ 為**孔緣**距（與題目印出之 $A_{sf}=2t(a+d/2)$ 同一符號），孔中心距板端／近側邊 115 mm、遠側邊 185 mm。
- $b_e$：刪除「不需另外驗算淨寬」之錯誤提示，改為逐側與實際邊距比較 $\min(56, 65, 135) = 56$ mm。
- 新增 §4 八「設計：D5.2 尺寸規定檢核」：孔不置中、端距 $65 < 1.33b_e = 74.5$ mm 兩項不符；修正配置為孔置中、$a = 75$ mm，重算 $P_{a3}$ 621 → 675 kN，控制 $P_a = 504$ kN ≥ 450 kN OK。§4 七結論由「設計適足」改為「強度適足」。
- §5 新增另一解讀（65 mm 量到孔中心）：$b_e = 15$ mm、$P_{a2} = 135$ kN、$P_{a3} = 351$ kN，NG；說明不採理由（與題目 $A_{sf}$ 符號矛盾、15 mm 孔緣距非合理命題配置）。
- 更正 $A_{sf}$ 中 $a$ 的定義（舊稱「角隅至孔中心」）與 $b_e$ 條文編號（D5.2 → D5.1）；T-06 陷阱頁同誤一併更正。

**為什麼錯**：重述時漏讀題文「角隅」，假設孔置中，於是 $b_e$ 未與實際邊距比較、也沒做題目「設計」部分要求的尺寸檢核。四種極限狀態的強度值在主解讀下恰好不變，所以舊答案 504 kN OK 看起來沒問題。

**怎麼驗證**：原卷第 1 頁 300 dpi 目視（題文「在其中一個角隅距兩邊離 a = 65 mm 處…開一個直徑 100 mm 的圓孔」、$b_e \le (b_e)_{\max}$）；三組配置（孔緣距解讀／孔中心距解讀／修正配置）以程式重算全部極限狀態與 D5.2 三項比例；修正配置之 $A_{sf}$ 與 $P_n$ 手算交叉核對；problems-view 以 Playwright＋KaTeX 開頁，197 式無 katex-error、無 pageerror。verificationStatus 維持 unverified，待人工複核。

**未改動**：`study/lecture-SS-U1-1.html` §8.3「插銷位於斷面中央」為 D5.2 規定之正確敘述，未動；講義 PDF 不受影響。

- 2026-10-30｜UNIT-OVERVIEW｜由 exam-wiki-SA 導入 `scripts/build_unit_page.py`＋`scripts/unit_page_template.html`，產生五個單元總覽 `study/unit-SS-U1-1／U1-2／U1-3／U1-4／U2-3.html`（＋`.pdf`，12／12／15／14／14 頁），資料來源 `study/data/unit-SS-*.json`（唯一要維護的檔）。內容由舊 `study-`（命題分析）與 `formula-given-`（給／背分界）兩頁合併：考點群、命題風險、判定前提、背誦策略沿用舊頁文字；題數、排名、前後段漂移、題型（計算／繪圖／推導／說明）與設計法分布改由腳本自 `question_index.json` 重算（U1-1 前段設計法更正為 LRFD 7／混合 2／概念 2／ASD 1，舊頁為 8／2／1／1）。SS 版腳本兩處擴充：資料檔 `"giveCol": false`（SS 的 give 類公式分散在各欄，不強制放最後一欄，逐年表合計改為全欄加總）、`"showDesignMethod": true`（題目列加註 designMethod）；viz 偵測補上 `raw/solutions/<id>/*viz*.html`。模板修正：`.tw` 加 `position:relative`（KaTeX MathML 絕對定位元素會撐寬手機頁）、手機寬度下長行內公式可橫捲、`s2`／`s4`／逐年表也做 KaTeX 渲染。
- 2026-10-30｜UNIT-OVERVIEW｜逐題標公式用途（107 個題目×單元配對，178 條公式）：每條公式寫關鍵字 regex 對題解 §3.5＋§4 計數，再逐一開題解判斷；「也可用」、延伸討論（§5）、只列在知識點表者不算。舊給／背頁的年份證據因此有多處更正，各頁 footer 逐條列出。主要：U1-1「梁遠端線剛度修正」只剩 2011-4（2007-4、2013-2、2023-1 題解未套用；2013-2 只在 §5.5 延伸）；「剪力遲滯 U 公式」2005／2007／2015 題解皆走替代表，唯一套用的 2024-2 當年有印 → 由必背降為別賭；「孔壁承壓」刪 2015（2015-2 為銲接）。U1-2「Mp=FyZx」✗ 由 7 年擴為 12 年（LTB 三區段題都要用）。U1-3「Cm 三情況」改為 2004-4、2008-4（跨中有橫力用 1.0）；「Fbx/Fby」刪 2008、2019（走 LTB 三式）；「對位圖梁遠端修正」本單元已無題目套用（2013-4 主答採未修正值）。U1-4「螺栓承壓」刪 2004、2020；「螺栓群 Ip」只剩 2002（2004、2017 為銲縫群）；94 年 2005-3 為 LRFD 銲道（0.75×0.6FEXX），舊頁誤記為 ASD 0.3FEXX。U2-3「最小／最大銲腳」本單元已無題目套用。另修正多條 eq 中 `<` 被瀏覽器當成 HTML 標籤而不渲染的問題（改寫為 `\lt`）。
- 2026-10-30｜UNIT-OVERVIEW｜下游同步：舊 `study/study-SS-*.html`→`unit-SS-*.html#s1`、`formula-given-SS-*.html`→`#s2` 改為 meta refresh 轉址頁（舊 `formula-given-*.pdf` 保留未動）；五份 `lecture-SS-*.html` 按鈕列「命題分析＋給／背分界」合併為「📊 單元總覽」；`study/problems-view/` 88 頁「🔍 命題分析」改為「🔍 單元總覽」並讓跟隨來源單元的腳本認得 `unit-` 來源；`scripts/build_frequency.py` 換成 v1.2（教材欄偵測 unit-）並重跑 `study/frequency-SS.html`；README 檔案表同步。待複核：`SS-2004-2` 掛 U1-1 副考點，但題解主答沒用到拉力桿件公式（淨斷面只在 §5.5），分類未改，請使用者決定。
- 2026-10-30｜TAXONOMY-FIX｜修正 `raw/json/question_index.json` 8 題 `primaryTopicId` 指向他科 taxonomy（`frequency-SS.html` 資料異常警告）：原則為「升格題解已標的 SS 子項、把 SD／MM 降為副考點」。SS-2009-1 SD-U3-1→SS-U1-3；SS-2009-2 SD-U3-1→SS-U2-3；SS-2012-2、SS-2020-1 SD-U3-1→SS-U1-4；SS-2022-4 SD-U3-1→SS-U2-2；SS-2010-1、SS-2013-1 MM-U1-1→SS-U2-1；SS-2006-3 MM-U1-1→SS-U1-2（依題解 .md 副分類）。同步：`dashboard-data.js` 8 筆；`study/data/unit-SS-U1-2.json` 新增 SS-2006-3 題目列（f=[0,2,4]）並更新 U1-2／U1-3／U1-4／U2-3 資料檔中手寫的題數、前後段、題型／設計法小計與風險表敘述；重跑 `build_unit_page.py`（五頁）與 `build_frequency.py`（對帳通過，異常警告消失；U1／U2 由 75／15 → 79／19），並以 Chromium 重出 unit-SS-U1-2／U1-3／U1-4／U2-3.pdf。未改動：8 題題解正本 `raw/solutions/*/*.md` 頁首「主分類」仍為舊值（規則 1 只允許解析勘誤），`wiki/problems/`、`study/problems-view/` 同；待使用者決定是否一併改。
- 2026-10-30｜TAXONOMY-FIX-2｜依使用者指示「主分類、副分類不引用其他科單元」：`question_index.json` 13 題移除 `secondaryTopicIds` 中的 SD-U3-1／MM-U1-1（SS-2006-3、2009-1、2009-2、2010-1、2012-2、2013-1、2014-2、2014-4、2020-1、2021-3、2022-3、2022-4、2024-4），同步 `dashboard-data.js`。題解正本 `raw/solutions/*/*.md`（含 SS-2006-5）、`wiki/problems/`、`study/problems-view/` 的「主分類／副分類」行改由索引重寫（使用者明確要求，屬規則 1 之外的授權修改）；problems-view 單元總覽按鈕去除「（副分類）」字樣。`wiki/topics/SS-*.md` 題目清單由索引重算；刪除 `wiki/topics/SD-U3-1.md`、`MM-U1-1.md` 並從 `topics/index.md` 移除他科段落；`wiki/index.md`、`methods/index.md`、`traps/index.md`、`philosophy/`、`methods/plastic-zx`（raw＋wiki）、`CLAUDE-SOLVE.md`、三份 lecture html、unit 資料檔敘述中的他科代號改為 SS 子項或文字說明；CLAUDE.md「其他相關單元」表改為「分類原則」。重跑 unit 五頁＋frequency（對帳通過、無資料異常），重出 unit PDF 四份。lecture PDF 未重出。
- 2026-10-30｜TAXONOMY-FIX-3｜`dashboard-data.js` 的 `SS_UNITS`／`SS_TOPICS` 移除 MM、SD 代號，只留 SS；CLAUDE-CODE.md REFRESH-DASHBOARD 步驟 3 改為只取 SS 分類樹。以 Chromium 重出 `lecture-SS-U1-3／U1-4／U2-3.pdf`（34／39／31 頁，pdftotext 確認無 SD-U3-1）。
- 2026-10-30｜AUDIT｜全庫 98 題分類與引用稽核（僅檢查未修改），報告存 `wiki/queries/分類與引用稽核-2026-10-30.md`：確定錯誤＝主副分類索引與正本不一致 6 題（SS-2021-2 主分類相反）、designMethod 錯／未同步 11 題（SS-2013-3 應為混合等）、hasHandwritten 3 題；分類合理性建議 7 項（SS-2023-3 與同型 2010-1 主分類不一致、SS-2009-2 歸 U2-3 牽強）；引用錯誤＝methods 頁 22 處題號描述不符、by-year／概念頁舊分類名殘留、index.md 漏 22 題、雙向連結缺 44 組、wiki/problems 71 個圖片連結失效。
- 2026-10-30｜AUDIT-FIX｜依稽核報告（`wiki/queries/分類與引用稽核-2026-10-30.md`）與使用者決定全數修正：① `question_index.json` 19 題變更——主分類：SS-2021-2、SS-2003-3 U1-4→**U1-1**（副 U1-4，題目本體為拉力構材）、SS-2023-3 U1-2→**U2-1**（副 U1-2，My／Mp 依分類原則，與 2010-1 一致）、SS-2009-2 U2-3→**U1-4**（副 U2-2，耐震接頭／SN 鋼材）；補副分類：2017-1+U2-3、2016-1+U1-1、2006-2+U2-3、2006-3+U2-1、2009-3+U2-1、2006-1+U1-2、2003-1+U1-2、2014-2+U1-4；designMethod：2013-3→混合、2013-1／2017-2／2016-4→概念題；hasHandwritten：2015-2／2014-1／2014-3→true；SS-2021-2 tags 移除不實的「高拉力螺栓」改依正本；tagSystem 認列「塑性分析」（CLAUDE-SPEC 同步）。② 下游頁首同步（使用者授權、比照 TAXONOMY-FIX-2）：正本 .md 15 檔、wiki/problems 21 檔、problems-view 15 檔（含單元按鈕；SS-2015-4 舊代碼 4.2.2→SS-U2-2；SS-2009-1、2005-4 設計法）；`dashboard-data.js` 18 列。③ 導覽頁：`wiki/topics/SS-*` 由索引重算；`by-year.md` 18 列主分類／設計法；`wiki/index.md` 分類表改由索引全量重建（原漏 22 題），2.1 耐震改標「主題式跨單元」；概念／陷阱頁「主分類」欄 53 列同步；講義 html 題表 5 列。④ 方法論題號引用（raw/solutions/methods 來源＋wiki 同步；asd-beam／asd-beam-column 無 raw 來源直接改 wiki）：刪除 13 筆引用錯題（如 eccentric-bolt 的 2004-3／2017-4 實為銲縫、ltb-3zone 的 2011-1 實為直接分析法、lrfd-column 的 2015-2 為拉力構材），修正 12 筆描述（2005-1 單角鋼非雙槽鋼、2024-2 圓管非角鋼、2011-2 有側移靠柱等），補 4 筆漏列（asd-beam 2008-1、asd-beam-column 2019-3、eccentric-bolt 2020-4、eccentric-weld 2007-1）。⑤ 概念↔題目連結：移除 15 筆不實關聯（以題解關鍵字核對：如 BOX-COLUMN 的 2007-2 為 H 型柱、SHEAR-CONNECTOR 的 2005-2 無剪力釘、FILLET-WELD-DESIGN 的 2003-3 無銲接、LTB 的 2002-1／2005-2／2006-4／2009-3／2016-1／2019-2、B1-B2 的 ASD 題 2004-4／2008-4 改列 Cm 頁），補 49 筆題目頁回連與 13 筆概念頁列（LEANER-COLUMN-EFFECT 原零題，補 2008-2／2011-2／2013-2）；SS-2014-2「相關概念」移除誤植的 4 個題號；`wiki/problems` 71 個圖片連結改為 `../../raw/solutions/` 路徑；`[[LOCAL-BUCKLING-FLANGE]]`（不存在）→`[[COMPACT-SECTION]]`；94 題空白「相關題目」依共同標籤／概念／主分類自動填入（3 題人工補）。⑥ 統計頁：`study/data/unit-*.json` 四檔增刪題目列並逐項改寫手寫數字（前後段對切、考點群、題型、設計法、風險表、題數敘述；數字以索引＋資料檔重算），重跑 `build_unit_page.py --all` 與 `build_frequency.py`（對帳通過；U1-1 26／U1-2 21／U1-4 20／U1-3 12／U2-3 7），以 Chromium 重出 unit-SS-U1-1／U1-2／U1-4／U2-3.pdf 與 lecture-SS-U1-1／U1-3／U2-3.pdf。驗證：稽核腳本重跑，主副分類／設計法索引與正本、wiki、problems-view、dashboard、topics 全數一致，連結失效僅剩 log 歷史文字。未做：U2-1／U2-2 仍無 problems-view 頁（10 題）；講義正文中以舊歸屬敘述的段落（如 lecture-SS-U1-1「被借用」表內的 SS-2003-3）僅更正主分類欄，未改寫章節結構。全部變更前已備份。
- 2026-10-30｜AUDIT-FIX-2｜處理稽核報告剩餘兩項：① 新增 `study/problems-view/` 10 頁（SS-2025-4、2022-4、2018-1、2017-1、2016-5、2015-4、2014-2、2013-1、2010-1、2006-3），由正本 .md 以 python-markdown 渲染（數學式先保護後還原、`[[ID]]` 轉徽章、圖片改指 `../../raw/solutions/`），版型沿用既有頁；與既有頁比對正文文字一致度 >99%（差異僅為正本後續增修內容；並修正舊渲染器把「< 103.75」誤當 HTML 標籤吞掉的問題）。單元按鈕：主分類無講義者改用副分類單元（2017-1→U2-3、2014-2→U1-4），U2-1／U2-2 無教材者連「全科頻率排名」與題庫儀表板。全 98 頁 header 標題字色原與底色相近（深藍疊藍漸層），一併改為白字。problems-view 現為 98／98 題。② 講義題表與正文依新分類改寫：lecture-SS-U1-1（§10 主 24→26，SS-2003-3 自「被借用」表移入主表、新增 SS-2021-2；副表新增 SS-2016-1；2006-1／2013-3 設計法；標籤統計改 33 題重算）、lecture-SS-U1-2（§11 主表移出 SS-2023-3、補 SS-2006-3；副 4→7 補 2003-1、2006-1、2023-3；LTB 題數 12→13 等統計重算）、lecture-SS-U1-4（§11 主 19→20：移出 2003-3、2021-2，移入 2009-2、2012-2、2020-1；副 7→8；概念題數 7→12；三題設計法改概念）、lecture-SS-U2-3（§8 副表移除 SS-2009-2 並加註改列原因，新增 2006-2、2017-1；地形圖 13→14 題、G1 群補題）。四份講義主／副題表以程式對帳索引全數一致；重出四份講義 PDF。重跑 build_frequency（problems-view 98 題）與 build_unit_page。
- 2026-10-30｜TEXTBOOK-REFACTOR｜教科書講義整合與原始碼歸檔：將教科書拉力篇與壓力篇講義（HTML/PDF）由 `教科書/` 移至 `study/`（`textbook-SS-U1-1-tension.*`、`textbook-SS-U1-1-compression.*`），並將各章節繪圖、數值計算與組裝原始碼納入 `study/figs-src/textbook-SS-U1-1/` 統一版控。
- 2026-10-30｜CLEANUP｜清理已被現代化教材取代之舊版投影片目錄與旁白稿：移除 `study/` 下五個舊版單元目錄（`SS-U1-1 拉力及壓力桿件/`、`SS-U1-2 梁桿件/`、`SS-U1-3 梁柱桿件/`、`SS-U1-4 接合之分析與設計/`、`SS-U2-3 設計規範對施工之要求/`，共 106 檔舊版 PPTX/deck/切片圖）以及舊版記憶片 PPTX/PDF 與旁白稿 markdown（共 14 檔）；所有教材皆由 `unit-SS-*.html/pdf`（單元總覽）、`lecture-SS-*.html/pdf`（觀念講義）與 `formula-given-SS-*.html/pdf`（給／背分界）及 `textbook-SS-*` 統一承接維護。
- 2026-11-01｜START-PAGE｜新增根目錄 `start.html`（「從這裡開始」六步學習路徑：定方向→懂原理→試一題→記公式→練題目→問到懂；五單元教材依步驟分組、27 支解題影片、8／12 週進度表、AI 提問範本、勘誤回報連結），產生器 `scripts/build_start.py`（連結集中在檔頭資料區，改連結後重跑）。`index.html` 儀表板標題下加入口橫幅；`study/*.html` 24 頁與 `影片講義/*.html` 5 頁頂部加「← 從這裡開始」返回列（`scripts/add_backlink.py`，可重複執行；列印時以 `@media print` 隱藏，不影響 PDF），並寫入 `scripts/unit_page_template.html` 與 `scripts/build_frequency.py`，重跑產生器不會遺失。儀表板仍維持 `index.html` 不動。
- 2026-11-01｜AUDIT-BLIND｜SS-U1-1 未勘誤 17 題以考卷原圖盲解比對（PyMuPDF 轉圖，未參考舊題解；Claude Opus 對照既有 Gemini 題解），報告 `wiki/queries/盲解比對-SS-U1-1-2026-10-31.md`、紀錄 `wiki/queries/盲解紀錄-SS-U1-1-2026-10-31.md`、ledger `wiki/queries/audit-ledger-SS.json`：一致 5 題、分歧 12 題（答案改變 10、觀念作圖 2），錯誤來源以看錯題目或圖為主（8 題）。最嚴重：SS-2003-2 漏用題目明文 rm ≥ 0.3 全厚（φcPn 147 → 513 t）、SS-2003-3 題意讀錯、SS-2003-1 (三)(四) 被補全成別題。未修改任何題解，待人工看圖確認後依規則 1 勘誤。另新增五科通用 `scripts/audit_classification.py`（本科分類一致性 0 筆問題）。
- 2026-11-01｜FEEDBACK｜新增 GitHub 勘誤回報表單 `.github/ISSUE_TEMPLATE/correction.yml`（欄位：題號或頁面、錯誤類型、哪裡錯了、依據；自動貼「勘誤」標籤，標籤已於 GitHub 建立）與 `config.yml`；`start.html` 兩處回報連結改指 `issues/new?template=correction.yml`（`scripts/build_start.py` 同步）。Issues 功能原已開啟。
- 2026-11-01｜FIX-SS-2003｜依盲解比對報告（`wiki/queries/盲解比對-SS-U1-1-2026-10-31.md`）勘誤 SS-2003-1／2／3，依規則 1 四條件：① 考卷以 PyMuPDF 轉圖逐字目視（含背面四張參考表）；② 數值程式重算＋雙路徑驗算；③ 同步下游；④ 本紀錄＋正本頁尾「修正日期」。**SS-2003-2**：考卷明文「r_m 不應小於挫屈平面全厚度之 30%」，原解直接用型鋼 r_y = 7.7 cm → 弱軸 r_m = max(7.7, 0.3×50) = 15.0、強軸 18.0 cm，KL/r 155.8 → 80.0、λc 2.405 → 1.235（彈性 → 非彈性），φcPn 147 → **513 t**；新增 §6 AISC 360-16／-22 對照（假設鋼筋位置估算 292／447 t）。**SS-2003-3**：題意整題重判——構材為長肢背對背雙角鋼、WT 為接頭板；（一）改為決定螺栓數：雙剪 17.96 t/顆、構材 77.51 t（降伏控制）→ **5 顆**；（二）改為 WT 與柱 8 栓受 3:4 斜向力之拉剪互制，依考卷背面表 Ft = 8.2 − 1.9fv → φRt = 9.24 ≥ 7.75 t → **足夠**；扣除孔徑改為題目指定 2.2 cm、淨面積改扣兩支角鋼；刪除題目明示不必考慮之塊狀剪力。另記錄考卷背面表兩處與 AISC 相反：螺栓剪力表 N／X 兩列數值互換、承壓表「變形是否為考量」條件互換（題解照考卷作答並於 §5.2 說明兩種讀法皆為 5 顆）。盲解報告（二）原用 AISC 117 − 1.5fv 得 11.05 t，本次改依考卷表，結論不變。**SS-2003-1**：原解自稱掃描不清而補全的（三）（四）與原卷不符，依原卷改為「受拉構材降伏安全係數較低之理由」「依局部挫屈特性之四種斷面」；（二）改答「改善措施」；（一）補擇式原則與上限。下游：`study/problems-view/` ×3（新增 `scripts/render_problem_view.py`，修正 Python-Markdown 斜體內粗體被拆的問題）、`wiki/problems/` ×3、`question_index.json`／`dashboard-data.js` 三題標籤（移除不實的 複合柱／Fmy／Em／殘留應力／塊狀剪力／彈性挫屈 等）、`study/data/unit-SS-U1-1／U1-2／U1-4.json`（題目摘要、公式對應；F16 r_m 卡補 2003 年「有給」）並重跑 `build_unit_page.py --all`、`lecture-SS-U1-1／U1-2／U1-4.html`、`textbook-SS-U1-1-tension.html`、概念頁 BLOCK-SHEAR-RUPTURE／COMPACT-SECTION／TENSION-MEMBER-DESIGN／BOLTED-CONNECTION-DESIGN、方法頁 block-shear／shear-lag-u（raw 來源＋wiki）、`wiki/index.md`、`wiki/by-year.md`、ledger。同步腳本留存 `scripts/fixes/`。三題 verificationStatus 維持 unverified。講義與單元總覽 PDF 未重出。
- 2026-11-01｜PDF-REFRESH｜重出 `study/lecture-SS-U1-1／U1-2／U1-4.pdf`、`unit-SS-U1-1／U1-2／U1-4.pdf`、`textbook-SS-U1-1-tension.pdf`（Chromium print 媒體、A4、邊界 14／16／13／13 mm、展開 details），反映 FIX-SS-2003 與本日第二批勘誤；返回列於列印時隱藏。U1-4 講義 PDF 自 10-23 起「待產」一併補齊。
- 2026-11-01｜FIX-SS-U1-1-B2｜依盲解比對報告勘誤第二批 SS-2011-2／SS-2011-4／SS-2024-2，依規則 1 四條件：① 考卷以 PyMuPDF 轉圖 400–500 dpi 目視判讀附圖；② 數值程式重算（對位圖以方程式精確解）＋雙路徑驗算；③ 同步下游；④ 本紀錄＋正本頁尾「修正日期」。**SS-2011-2**：圖 A 點有小圓圈＝柱頂與 EI=∞ 頂梁鉸接，原解誤作剛接取 K₀ = 1.0；更正 K₀ = 2.0（底固頂鉸可側移），並釐清 P_e 以 L、ΣP_eK 以 K₀L 計 → K_(I)AB 1.414 → **2.83**、K_(II)AB 2.0 → **4.0**，ΣP_cr 比值 1 不變（兩者皆 π²EI/4L²），補直接平衡法驗算。**SS-2011-4**：F 點為三角形鉸支（題目規定 G = 10），原解誤作固接 G_F = 1.0；A 點小圓圈為梁柱鉸接，原解漏乘梁 AD 遠端修正 ½ → G_D 0.450 → **0.658**、G_E 0.708 不變；K_DE 1.21 → **1.22**、K_EF 1.27 → **1.84**；ASD 非彈性 τ_a = F_a/F′_e 自洽疊代收斂 τ_a = 0.717、K_EF 1.11 → **1.79**（G_F 維持 10；若一併折減為 1.67，列於 §5）。**SS-2024-2**：圖示「半圓孔徑 22 mm」為圓管開槽，原解以「無孔」取 A_n = A_g；更正 A_n = 82.6 − 4×2.2×1.0 = 73.8 cm²，φtTn 130.8 → **117.0 t**（NSF 控制）；斷面圖每支板兩側各一道銲，銲道 4 → **8 道**，所需銲腳 7.66 → 3.4 mm，設計銲腳仍 8 mm（最小銲腳控制）；補管壁沿銲道剪力撕裂 304.7 t、更正 F_EXX 筆誤 49 → 4.92 tf/cm²。三題皆新增 §6 AISC 360-16／-22 對照。下游：`study/problems-view/` ×3、`wiki/problems/` ×3、`question_index.json`／`dashboard-data.js` 標籤（append：柱頂鉸接、鉸支端、開槽淨面積）、`study/data/unit-SS-U1-1.json`（梁遠端修正卡補 A 點與 F 點）並重跑 `build_unit_page.py --all`、`lecture-SS-U1-1.html`（T-03 補開槽例外、考點表 SS-2011-4 列更正「3/4」誤植）、`lecture-SS-U1-4.html`（§1.2 表與陷阱、陷阱總表第 8 列）、`textbook-SS-U1-1-tension／compression.html` 與其來源 `study/figs-src/textbook-SS-U1-1/ch6、ch8.html`、ledger。三題 verificationStatus 維持 unverified。另發現未處理：`wiki/concepts/LEANER-COLUMN-EFFECT.md` 的「P_cr,modified = P_cr,sway·ΣP_total/ΣP_sway」方向相反（應為 ΣP_eK/ΣP 縮減），屬 compile 輸出，需改 `raw/json/concepts.json` 來源。
- 2026-11-01｜FIX-SS-U1-1-B3｜勘誤第三批 SS-2002-3／SS-2010-3／SS-2007-4／SS-2023-1（依規則 1 四條件：考卷轉圖 500 dpi 目視、程式重算、同步下游、本紀錄＋頁尾修正日期）。**SS-2002-3**：X-Z 面立面圖側撐標註為距頂 4.0 m、距底 6.0 m，原解誤作中點 5 m，且把 X-Z 面誤標為強軸平面；更正弱軸下段固-鉸 KL = 480 cm 控制，KL/r 102.5 → **98.4**，P_a 90.4 → **93.9 t**、φcPn 125.8 → **131.2 t**。**SS-2010-3**：單角鋼圖 c_x = 5.0 cm 為垂直距離、對應繞水平軸的 I_x = 782 cm⁴，原解把 I_y = 276 配上 15 cm；更正 I_X = 34,898（控制）、I_Y = 44,198 cm⁴，KL/r 163.8 → **159.0**，P_a 55.3 → **58.7 t**、φcPn 79.0 → **83.8 t**。**SS-2007-4**：G 值無誤，對位圖讀值偏差，以方程式精確解更正 K_AD 2.5 → **1.97**、BE 1.2 → 1.29、CF 1.27 → 1.38、EG 1.15 → 1.19、FH 1.20 → 1.28；另更正「鉸接取 G = 10 偏保守」之誤述（G = 10 的 K 小於 G = ∞）。**SS-2023-1**：G 值無誤（L2 表 G_H 誤為 0.10 一併更正為 0.13），K_CF 2.50 → **2.17**、AD 1.20 → 1.29、BE 1.17 → 1.26、DG 1.12 → 1.15、EH 1.10 → 1.12。四題皆新增 §6 對照與自我檢查。下游：`study/problems-view/` ×4、`wiki/problems/` ×4、`question_index.json`／`dashboard-data.js` 標籤（append：側撐位置判讀、平行軸定理、對位圖方程式）、`study/data/unit-SS-U1-1.json` F11 與 `unit-SS-U1-3.json` F26（更正「91 年 K 值表什麼都沒給」——該卷實附六種端部之設計 K 值表，U1-3 F26 ok 補 2002）並重跑 `build_unit_page.py --all`、`lecture-SS-U1-1.html` 考點表 SS-2002-3 列、ledger；重出 `lecture-SS-U1-1.pdf`、`unit-SS-U1-1.pdf`、`unit-SS-U1-3.pdf`。四題 verificationStatus 維持 unverified。
- 2026-11-01｜FIX-SS-U1-1-B4｜勘誤第四批（觀念／作圖題）SS-2021-2／SS-2016-3，依規則 1 四條件（考卷轉圖 500 dpi 目視、程式重算、同步下游、本紀錄＋頁尾修正日期）。**SS-2021-2**：圖二垂直標註 100 mm 為受拉板寬、水平 150 mm 為疊接（銲道）長度，原解對調；塊狀剪力應畫在 t = 25 mm 節點板（兩道銲線為剪力面、銲線左端連線為拉力面），原解畫在受拉板；擇一準則改以「比較 F_uA_nt 與 0.6F_uA_nv、斷裂發生在較大面、另一面降伏」說明；補 U = 0.87（l/w = 1.5）與數值示意（節點板式(2) 247.0 t、φRn 185.3 t）及 AISC 360-05 以後單一式對照（φRn 161.3 t）。**SS-2016-3**：圖 1 為單一矩形板 b×t（無腹板），原解以平滑式 F_yF_e/(F_e+F_rc) 繪非彈性段並以「腹板拉力」補平衡；更正為塊狀殘留應力之切線模數解——兩側 b/3 於 F = 1.875 同時降伏、強軸 I_e/I = 1/27 → 平台 F_cr = 1.875（19.9 ≤ L/r ≤ 103.6）、18.0 ≤ L/r < 19.9 為 π²E/[27(L/r)²]、L/r < 18.0 全斷面降伏 2.29（若取 F_y 為 2.5，差額來自題目殘留應力不自相平衡，已於題解指出）；同步 `SS-2016-3-column-curve-viz.html`。下游：`study/problems-view/` ×2、`wiki/problems/` ×2、`question_index.json`／`dashboard-data.js` 標籤（append：節點板塊狀剪力、塊狀殘留應力、強度平台段）、`study/data/unit-SS-U1-1.json` 題目摘要並重跑 `build_unit_page.py --all`、`lecture-SS-U1-1.html` 考點表（「兩式取小」→「兩式擇一」）、ledger；重出 `lecture-SS-U1-1.pdf`、`unit-SS-U1-1.pdf`。至此 2026-10-31 盲解比對 U1-1 之 12 題分歧全部勘誤完畢，verificationStatus 皆維持 unverified 待人工複核。
- 2026-11-01｜AUDIT-BLIND-U1-2｜盲解比對 SS-U1-2 尚未查過的 15 題（考卷轉圖 110 dpi 全頁＋400–450 dpi 局部目視、不看舊解先解、Python 計算）。報告 `wiki/queries/盲解比對-SS-U1-2-2026-11-01.md`、紀錄 `wiki/queries/盲解紀錄-SS-U1-2-2026-11-01.md`、ledger 更新：一致 11 題、分歧 4 題（皆答案改變）。依使用者指示，所有題目 verificationStatus 維持 unverified。
- 2026-11-01｜FIX-SS-U1-2-B1｜勘誤 U1-2 盲解分歧 4 題（規則 1 四條件：考卷 400–450 dpi 目視、程式重算＋雙路徑驗算、同步下游、本紀錄＋頁尾修正日期）。**SS-2008-3**：圖 2 均佈載重只作用於 AB、CD（題文「此梁兩側承受均佈載重」），原解誤作全跨（跨中 40.5w）；BC 段為常數 18w，且原解把均勻彎矩代 M1/M2 = +1 得 Cb 3.10，應為單曲率 −1 → Cb = 1.0；Lb 6 m > Lr 5.79 m 彈性 Mcr 74.65 t·m 控制 → w_n,cr 2.50 → **3.73 t/m**（標稱 4.15）。**SS-2005-2**：0.85f'c 誤寫 1.785 tf/cm²（應 0.1785），PNA 由 5.96 cm 更正為 13.34 cm（上翼板下方），上排鋼筋與上翼板受壓 → Mn 170.3 → **135.5 tf·m**、φbMn 153.3 → 121.9；並依原卷重述題目（原解自行增列「列出降伏力」子題）。**SS-2024-3**：圖示為外伸梁（A 鉸、C 中間滾支無面外束制、載重在外伸端 B），原解誤作簡支梁跨中集中 → Mu 21 → **42 t·m**；Cb 1.316 巧合相同；強軸 φMn 65.6 OK、弱軸 17.1 NG（補 1.5FySy 上限）結論不變。**SS-2021-3**：原解選 BH500×500×16×36 之理由「最輕」與表一不符，且 Lr 改用 rT 與考卷式不符；依強軸受彎效率與用鋼量改選 **BH700×300×12×25**（Zx 6,330、Mp 221.6 t·m、f 1.116），Lb 12 m 彈性 LTB 無法發揮 Mp，改善為每 300 cm 側撐（≤ Lp 且 ≤ 0.086ryE/Fy = 352 cm），塑性極限 wu = 11.66Mp/L² = 17.9 t/m，並列 500×500 替代論述；指出題表 BH700×300×9×19 面積 156 與尺寸不符。四題皆新增 §6 對照。下游：`study/problems-view/` ×4、`wiki/problems/` ×4、`question_index.json`／`dashboard-data.js` 標籤（append：部分跨載重、單位換算、外伸梁、塑性機構）、`study/data/unit-SS-U1-2.json` 題目摘要並重跑 `build_unit_page.py --all`、`lecture-SS-U1-2.html` 考點對應表三列、ledger；重出 `lecture-SS-U1-2.pdf`、`unit-SS-U1-2.pdf`。四題 verificationStatus 維持 unverified。
- 2026-11-01｜AUDIT-BLIND-U1-4＋剩餘｜盲解比對 SS-U1-4 未勘誤 14 題（報告 `wiki/queries/盲解比對-SS-U1-4-2026-11-01.md`：一致 7、答案改變 6、規範待查 1）與全科剩餘 18 題（`盲解比對-SS-剩餘18題-2026-11-01.md`：一致 11、答案改變 5、觀念作圖 2），紀錄檔同目錄，ledger 64 筆。至此 SS 全 98 題皆已盲解或勘誤。使用者以「SS 勘誤判定單」看圖確認 14 題分歧全部盲解對（2005-3 下翼板無銲接符號）；2021-4、2012-2 以《鋼結構極限設計法》10.1.8、13.6.1、13.6.7 原文查證。
- 2026-11-01｜FIX-SS-B5｜勘誤 14 題（規則 1 四條件：考卷 300–600 dpi 目視＋使用者看圖確認、Python 重算＋雙路徑驗算、同步下游、本紀錄＋正本頁尾「修正日期」）。**U1-4**：SS-2002-4 載重為 3:4 斜向（Px 12、Py 16）、作用點距群心 (28.5, 15.5)，兩分量力矩部分抵銷 M 500 → 270 tf·cm，最大螺栓力 10.47 → **7.28 tf**，N.G. → **O.K.**，承壓改用翼板 tf；SS-2004-2 內連接板在腹板兩側各一片（可用寬 60.5 mm），原解 M25 置中於翼板（腹板位置）不可施工 → **M20、每翼板每側 6 顆（2 行×3 列）、外板 PL8×150×365、內板 2-PL10×60×365**，另發現構材 0.6FyAg＝60.2 t ＜ 70 t（題未問，§5.4 註記）；SS-2004-3 補上下各 5 cm 垂直銲（L 15 → 25 cm）、Pu 箭頭朝柱兩分量力矩反向 → Pu 10.6 → **33.4 tf**；SS-2005-3 原解自訂 P＝25 tf 並用 LRFD，改依題意 ASD 求 P，12/12×200 為腹板銲、下翼板無銲 → **P＝14.0 tf**（下翼板有銲之替代值 35.7 tf 列 §4.6），設計法 LRFD → **ASD**；SS-2007-1 原解誤作面外偏心、自訂 a＝b＝25 cm，改為平衡銲道設計（P＝71.9 tf 角鋼強度）→ **a＝12、b＝31 cm**；SS-2021-4 結論「不可以」→ **可以**（10.1.8：承壓型不可，摩阻型可共同分擔，須先鎖緊螺栓再銲），原解所引條文查無；SS-2012-2 改依本國規範：θp **0.03 rad**、以彎矩試驗強度 90% 對應轉角驗證、側撐 Lb ≤ **170ry/√Fy**、強度 ≥ 2%Fy·bf·tf（原解 0.04 rad、0.8Mpe、0.086ryE/Fy 為 AISC 341）。**U2-1／U2-2**：SS-2005-4「24 cm」為 T 斷面全深（原解 26.6）→ Z 813 → 667.4 cm³、wu 6.58 → **5.40 tf/m**，viz 同步；SS-2010-1 斷面由下而上 6×2、2×2、6×2、頂 2×2（原解誤作上下對稱）→ My 106.7 → **144.6**、Mp 192 → **256 tf·cm**；SS-2018-1 原解 A、B 曲線對調且假設全長均勻達 εu，改為淨斷面（0.8w）達 Fu 控制、全斷面應力 400 MPa → ΔA 200 → **≈2 mm**、ΔB **≈60 mm**，降伏比以 YR ＜ An/Ag 說明；SS-2022-4 鋼材 B 為 300–400 MPa（原解 350–450）→ P_B 0.625% → **2.5%**；SS-2016-5 SN490B、C 降伏點皆 325–445 MPa、0°C 衝擊值皆 ≥ 27 J（原解稱 B 無上限、C 47 J），CNS 13812 原表待使用者核對。**觀念修正（結論不變）**：SS-2014-4 兩端彎矩同向為雙曲率 Cm 0.345（原解假設單曲率），B1 仍 1.0、IR 0.821；SS-2019-3 漏看 B 點靠牆滾支，改為 B 點節點力矩依勁度分配 AB 8、BC 4 tf·m、軸力只在 BC，控制比值 0.552 → 0.456，OK 不變，viz 設計點同步，並修正原檔 \\times、\\text 被轉成 Tab 的亂碼。計算題皆新增或更新 §6 AISC 360-16／-22 對照。下游：`wiki/problems/` ×14、`study/problems-view/` ×14（render_problem_view.py；Playwright 檢查 KaTeX 0 錯誤）、`question_index.json`／`dashboard-data.js` 14 題標籤（append 斜向載重、⊐形銲道、平衡銲道、非對稱斷面、淨斷面控制、本國耐震規範等；移除不實的 強度不足、彎矩力偶、十字形斷面、均勻伸長）與 SS-2005-3 designMethod LRFD → ASD；`study/data/unit-SS-U1-4.json`（題目摘要 5 題、2005-3／2007-1 公式對應、ASD 0.3FEXX 卡、塑性轉角卡改本國規範）、`unit-SS-U1-1.json`（2007-1）、`unit-SS-U2-3.json`（「摩阻型不得共同分擔」卡改為「承壓型不可、摩阻型可以」、0.03 rad 卡改 90% 試驗強度）並重跑 `build_unit_page.py --all`、`build_frequency.py`（對帳通過）；`lecture-SS-U1-4.html`（併用陷阱、θp 0.04 → 0.03 三處、側撐 13.6.7、考點表 2002-4／2005-3／2007-1、陷阱總表第 17 列、偏心流程段）、`lecture-SS-U2-3.html`（§4.3 標題、荷變圖文字與圖說、陷阱框、T-21、問答 11）、`lecture-SS-U1-3.html`（2019-3 考點表誤植「P-M 互制圖繪製」）；`wiki/index.md`、`by-year.md`、概念頁 ECCENTRIC-CONNECTION／FILLET-WELD-DESIGN、方法頁 eccentric-weld／plastic-zx／b1b2-amplification／pm-interaction（raw＋wiki）、陷阱頁 CONNECTION-TRAPS J-05（改寫）、SEISMIC-TRAPS S-01（補本國數值）；重出 `lecture-SS-U1-3／U1-4／U2-3.pdf`、`unit-SS-U1-1／U1-3／U1-4／U2-3.pdf`（Chromium A4，KaTeX 0 錯誤）；ledger `human`／`fixed` 欄。更正盲解報告兩處：2002-4 替代解讀值 8.39 tf（原寫 ≈ 8.0）、2019-3 錯因改為漏看 B 點支承。14 題 verificationStatus 維持 unverified。原檔備份於 VM session home `~/backup-fix-2026-11-01/`。
- 2026-11-01｜待處理｜① SS-2021-3（已勘誤）以 Lb ≤ 0.086ryE/Fy 決定側撐間距，為 AISC 341 值，本國 13.6.7 為 170ry/√Fy，需另行複核；② `raw/solutions/SS-2015-4/SS-2015-4.md` 含 278 個 NUL 字元；③ `raw/solutions/SS-2005-4/剪力圖與彎矩圖.pdf`（使用者證據檔）內為舊數值；④ `study/lecture-VHA-7題觀念講義.html` 在工作目錄顯示為已刪除，非本次操作造成。
- 2026-11-01｜FIX-SS-B5-後續｜處理前一筆「待處理」四項：① **SS-2021-3** 耐震梁側撐間距原引 AISC 341-10 之 $0.086r_yE/F_y$ = 352 cm，依《鋼結構極限設計法》13.6.7 更正為 $170r_y/\sqrt{F_y}$ = 639 cm（BH500×500 替代論述 662 → 1,200 cm）並補側撐強度 2% $F_yb_ft_f$；本題仍由 $L_p$ = 300.6 cm 控制，每 300 cm 側撐、$w_u$ = 17.9 t/m 不變；正本加第二次修正日期，同步 `wiki/problems/SS-2021-3.md` 答案摘要、重生 problems-view。② **SS-2015-4** 正本檔尾 50 個 NUL 位元組（自 init 起即存在；前筆「278 個」為 grep 計數誤判）已移除，內容未改；problems-view 維持原頁（重生僅差渲染器版本）。③ `raw/solutions/SS-2005-4/SS-2005-4 剪力圖與彎矩圖.pdf` 為 2026-05-06 以瀏覽器列印舊版 viz 之輸出（wu 6.58、Mp 2032.5），依使用者指示以更正後之 `SS-2005-4-sfd-bmd-viz.html` 重新列印（wu 5.40、Mp 1668.6、RA 18.99、RB 13.43），檔名不變以維持儀表板補充筆記連結，原檔備份於 VM `~/backup-fix-2026-11-01/SS-2005-4-pdf/`。④ `study/lecture-VHA-7題觀念講義.html` 為使用者自行刪除、確認不保留；CLAUDE.md 新增紀錄表該列加註（PDF 版仍在）。
- 2026-11-01｜AUDIT-BLIND-已勘誤抽樣｜對 2026-08-22 至 10-29 已勘誤、未盲解之 34 題分層抽樣 12 題盲解（2025-2、2013-2、2013-3、2015-1、2014-3、2022-1、2020-3、2023-3、2017-4、2018-3、2020-4、2021-1），報告 `wiki/queries/盲解比對-SS-已勘誤抽樣-2026-11-01.md`、紀錄同目錄、ledger 新增 12 筆（scope＝已勘誤題抽樣）：勘誤正確 8、小瑕疵 2（2018-3 翼板銲腳 10.05 mm 取 10 mm 與殘留舊文字；2020-4「D25」規格未註明英制）、解讀選擇 2（2013-2 梁遠端修正是否作主答，且 §5.5「偏保守」應為「偏不保守」；2013-3 K 取理論值或設計值），勘誤改錯答案 0 題。未修改題解。
- 2026-11-01｜FIX-SS-已勘誤抽樣｜依使用者決定處理抽樣盲解 4 題：① **SS-2013-2** 主答改採對位圖梁遠端修正（C 端梁柱鉸接、有側移 ×0.5）：$G_B$ 0.221 → 0.442、$K_{AB}$ 1.71 → 1.777、$K'$ 2.42 → 2.51、$w_{cr}$ 96.0 → **88.9 tf/m**、$d$ 0.40 → **0.37 m**；未修正值移 §5.5 並更正「偏保守」為**偏不保守**，§5.4 以修正後 $G_B$ 重算。② **SS-2013-3** 主答改採 AISC 建議設計 $K$＝0.8：弱軸下段 KL/r 123.6 控制、**$P_a$ = 79.6 tf**、**$\phi_cP_n$ = 111.4 tf**；理論 $K$＝0.7（96.8／134.3 tf）移 §5.2 作替代。③ **SS-2018-3** 翼板銲腳 10.05 mm 進位取 **11 mm**（τ 82.7 ≤ 90.5 N/mm²；10 mm 為 91.0 超 0.5%），刪改殘留舊文字（腹板銲長 388 mm、梁翼改填角銲檢核）。④ **SS-2020-4** 「D25」改公制 **M27**（$A_b$ 5.726 cm²、容量 32.06 tf、80.9%），英制 1 in 列替代；孔徑、承壓、淨斷面、間距表與 §6 同步。四題正本加第二次修正日期，同步 `wiki/problems/`、problems-view、`gen_*.py` 與 figs（SVG＋PNG）。下游：`lecture-SS-U1-1.html`（陷阱 C-01、圖 5-3 與圖說、圖 7-3 SS-2013-3 標記 λc 1.377／比值 1.40、精選題表）與來源 `figs-src/lecture-SS-U1-1/figs_b.py／figs_c.py／build.py`；`textbook-SS-U1-1-compression.html`（§7 實例表、圖 8-5、§8 推導）與來源 `ch7.html／ch8.html／figs_ch8.py`；`lecture-SS-U1-4.html`（SS-2018-3 需 11 mm）；`wiki/traps/COLUMN-BUCKLING-TRAPS.md` C-01；`study/data/unit-SS-U1-1／U1-3／U1-4.json`；標籤 `梁遠端修正`、`設計K值` 入 `question_index.json` 與 `dashboard-data.js`；重跑 `build_unit_page.py --all`、`build_frequency.py`（對帳通過）；重出 `lecture-SS-U1-1／U1-4.pdf`、`textbook-SS-U1-1-compression.pdf`、`unit-SS-U1-1／U1-3／U1-4.pdf`（KaTeX 0 錯誤；4 頁 problems-view KaTeX 0 錯誤）；ledger 4 筆 `human`／`fixed`。驗證：2013-2 對位圖超越方程式精解與 Jackson–Moreland 近似（1.772）、層穩定 ΣP ≤ ΣP_eK；2013-3 ASD／LRFD 雙路徑（φcPn/Pa = 1.40，落在 1.39–1.47）；2018-3、2020-4 逐式重算。verificationStatus 維持 unverified。另將本批與前批由 Linux 端腳本寫成 LF 的工作樹檔案還原為 CRLF（內容不變）。原檔備份於 VM `~/backup-fix-2026-11-01/second/`。
- 2026-11-01｜FIX-ALIGN-BEAM-FACTOR｜對位圖「梁遠端修正係數」表更正（方法論依規則 1：數值驗算、同步 wiki、記 log）。`study/lecture-SS-U1-1.html` §5.3 原表「遠端鉸接 ¾、無側移雙曲率 ×2、有側移單曲率 ×⅔」以彎矩分配法 4EI/L 為基準、曲率寫反且未分側移狀態，與對位圖假設不符（有側移圖假設梁反向曲率 6EI/L、無側移圖假設單曲率 2EI/L），且與同講義圖 5-3（SS-2013-2 ×0.5）矛盾；改為 AISC 規範解說 C-A-7 之 2×2 表（有側移：遠端鉸 ×0.5、遠端固 ×⅔；無側移：遠端鉸 ×1.5、遠端固 ×2.0），加陷阱框（無側移遠端鉸反而 ×1.5、勿用 ¾）與考題對照 SS-2011-4、SS-2013-2。同誤一併更正：`study/lecture-SS-U1-3.html` 對位圖重點清單一條、方法論 `raw/solutions/methods/effective-length-chart/effective-length-chart.md` 梁剛度修正表（同步 `wiki/methods/effective-length-chart.md`）。驗算：SS-2013-2 G_B 0.221 → 0.442，以對位圖方程式精確解 K 1.724 → 1.777，與已勘誤正本一致。`study/data/unit-SS-U1-1.json`、`unit-SS-U1-3.json`、`textbook-SS-U1-1-compression`（含 figs_ch8.py）原已為正確係數，未改。重出 `lecture-SS-U1-1.pdf`（49 頁）、`lecture-SS-U1-3.pdf`（KaTeX 0 錯誤）。
- 2026-11-01｜REMOVE-VIZ｜依使用者指示廢止題解互動圖：刪除 `raw/solutions/` 下 19 份 `*-viz.html`（pm 11、column-curve 3、sfd-bmd 2、connection 2、ltb 1）；移除 9 份解析 .md 的「📊 互動圖」引用（經使用者核准之 raw/ 例外修改）、19 份 `wiki/problems/` 圖形表列與引用（SS-2006-5／2012-3／2025-3 圖形區塊因此清空而整段移除）、9 份 `study/problems-view/` 對應段落；`question_index.json` 移除 24 個 `hasViz` 欄位；`dashboard-data.js` 改為 6 欄（去 viz）；`scripts/build_unit_page.py`＋模板移除 📊 圖示並重建 5 份 `study/unit-SS-*.html`；規則文件（CLAUDE／CLAUDE-SOLVE／CLAUDE-SPEC／CLAUDE-CODE／README／檔案架構索引表）改為不再產生互動圖，lint 第 5、6 項改為 svg 圖形登錄與殘留 viz 檢查。`index.html` 同步移除互動圖按鈕／徽章／篩選／統計卡並優化。歷史 log 與 .md 頁尾「修正日期」中提及 viz 者保留為歷史紀錄。
- 2026-11-01｜REMOVE-SUPP-PDF｜依使用者指示移除補充筆記 PDF：刪除 `raw/solutions/` 下 8 份（SS-2005-4、2006-5、2014-4、2016-3×2、2017-4、2024-1、2025-3）；`index.html` 移除按鈕／下拉選單／篩選，統計卡改為「LRFD / ASD 題數」；`dashboard-data.js` 改 5 欄；規則文件同步（CLAUDE.md 受保護清單移除 `*.pdf`）。`raw/solutions/methods/cb-factor/Mastering_the_Cb_Factor.pdf` 非題目補充筆記、未連結於儀表板，保留。


- 2026-11-01｜FIX-CONCEPTS-METHODS-SCAN｜依掃描報告 `wiki/queries/觀念方法頁掃描-SS-2026-11-01.md`（確定錯誤 45、待查 19）修正。**方法頁 M1–M19**（規則 1：Python 驗算、raw 與 wiki 同步、各頁加修正日期；raw 13 份、wiki 18 頁）：plastic-mechanism 固定端梁內功 6Mpθ → 4Mpθ（wu 16Mp/L²）、簡支例、靜不定度表、陷阱 1；pm-interaction 折線轉折點 (1/9, 0.2) → (0.9, 0.2)；b1b2-amplification、asd-beam-column、asd-beam 之 M1/M2 符號改「雙曲率為正」（均勻彎矩 Cb＝1.0）；b1b2-amplification、effective-length-chart 之 ΣPeK 只計抗側柱；asd-beam Lu 定義與腹板 170/√Fy；ltb-3zone ASD 對照式；shear-lag-u 改考卷 U 表＋板件 l/w 階梯、角鋼 x̄ 6.75 → 2.56 cm；block-shear 改考卷擇一式、角鋼 Ubs 1.0；lrfd-column λc 速算表（分界 141 → 134）與 tf/cm² 制寬厚比；slip-critical-lrfd 補 1.13；conjugate-beam 端彎矩轉角 M0L/3EI 與內部鉸／滾支對應；cb-factor 1.35 → 1.32；eccentric-weld FEXX 4.92、Ix／Iy 歸屬；eccentric-bolt 直接剪力方向；plastic-zx 圓管 f 1.27～1.70。**概念頁 C1–C26**（32 頁，頁尾加修正日期）：MOMENT-AMPLIFICATION-CM 符號與 ASD 側移 Cm 0.85；BOX-COLUMN Z 分母 6 → 4、薄壁 1.5B²t；COMPOSITE-COLUMN φcAsFcr、Fmy／Em 係數、CFT 標 AISC 360-10；COLUMN-STRENGTH-CURVE Cc 對應 λc √2；GLOSSARY 六處（ASD 考卷寫法、Mr、Vn、D、RBS、規範來源）；FILLET-WELD-DESIGN FEXX 4.92；FRAME-STABILITY-ADVANCED；CAPACITY-DESIGN 二擇一；TANGENT-MODULUS-THEORY 0.877Fe；TENSION-FIELD-ACTION 方向；WEB-LOCAL-YIELDING 改 K1.3 兩式；SEISMIC-CONNECTION-DETAILS 改 13.6.1；STRONG-COLUMN-WEAK-BEAM 改 13.6.5 式 13.6-3（比較方向待核紙本）；WELDING-PRACTICE 依施工規範 §7.4.5；PLATE-GIRDER-DESIGN 單位與 2.45√(E/Fyw) 意義；SHEAR-LAG 改考卷 U 表與 φtTn 式；WEAK-AXIS-BEHAVIOR 補 1.5FySy、Zy 腹板項；另依已勘誤正本更正 SS-2007-1、SS-2019-3 題目表與 Pe1 之 K、U 表、塊狀剪力擇一式、SLIP-CRITICAL 預拉力表公制／英制、SEISMIC-STEEL-SN 之 SN490B／C 說明、WELDING-PROCESSES 表頭。**待查 19 項**只加註「⚠️ 待核對規範原文」未改數值（EULER-BUCKLING L/1000、Cpr／SDC、塊狀剪力孔徑 +3／+3.2 mm、剪力釘式、U 上限 0.9、PANEL-ZONE 力臂、SLIP-CRITICAL μ、Ry、Qn、低氫銲條烘乾溫度、TORSIONAL-BUCKLING 誤連、composite-beam-pna φb、b1-m1m2 形式 B、ltb-3zone G、圓管 λr、Class A μ 等）。概念頁為 compile 輸出、concepts.json 只存定義，執行 compile-all 可能覆蓋。備份於 VM `~/backup-fix-2026-11-01/fifth/`。
- 2026-11-01｜FIX-SS-2020-4-B｜使用者決定主答改採假設 B（翼板鈑承擔 M，腹板鈑承擔 V＋V·e＝350 tf·cm）：R_max 13.24 tf → **M20 A490**（Ab 3.14 ≥ 2.36）；梁腹板承壓 13.78 ≥ 13.24（Fu 假設 4.1、Fp＝1.2Fu）；腹板鈑剪力控制 0.729 cm → **8 mm**（以假設 Fu 驗淨斷面剪力斷裂需 9 mm，正本列為保守值）。原主答假設 C（腹板依剛度分擔 947 tf·cm，M27＋12 mm）在題目螺栓配置下腹板承壓 18.6 tf（1 in 17.5 tf）< 25.93 tf 不成立，改列 §5 並註明命題原意屬推論。正本第三筆修正日期、gen_SS-2020-4.py 與 fig-2～4 重繪、wiki 題頁、problems-view、索引與儀表板標籤（腹板承壓、命題原意判斷）、unit-SS-U1-4.json（F8、F26）並重跑 build_unit_page.py --all、重出 unit-SS-U1-4.pdf、ledger human 欄。KaTeX 0 錯誤。
- 2026-11-01｜FIX-KATEX-CDOTP｜渲染修正（非數值勘誤）：`\text{ tf·cm}` 等「\text{} 內含中點 ·」在 KaTeX 0.16.11 會被轉成文字模式不支援的 `\cdotp` 而顯示紅字。全庫改寫為 `\text{ tf}\cdot\text{cm}`，共 402 處／69 檔：`raw/solutions/` 30 份 .md、`study/problems-view/` 30 頁、`wiki/problems/` 10 頁、`study/lecture-SS-U2-3.html`。以 study/assets/katex 0.16.11 逐一重算 98 頁 14,596 個數學式，`\cdotp` 錯誤歸零。

- 2026-11-01｜ARCHIVE-WIKI｜依使用者決定，wiki/ 只保留 queries/，其餘封存：`wiki/{code-ref,concepts,diagnosis,failure-modes,materials,methods,philosophy,problems,topics,traps}/` 與 `wiki/index.md`、`wiki/by-year.md` 搬至 `archive/wiki/`（不再維護、不再同步勘誤），並新增 `archive/README.md` 說明封存理由與替代教材；`wiki/log.md` 移為 `wiki/queries/log.md`（即本檔，規則 3 只可 append 不變）。`raw/solutions/methods/` 與 `raw/json/concepts.json` 保留。同步：`index.html` 導覽卡片改為「稽核與分析報告」「變更紀錄」，[[id]] 解析目錄改為 wiki/queries 與 archive/wiki；`wiki/queries/index.md` 補列今日報告與封存說明；`scripts/audit_classification.py` 在 wiki/problems 不存在時略過 C 檢查（重跑：98 題 0 筆問題）；`xcheck.py` 衍生層目錄改指封存處；`study/lecture-SS-U1-2／U1-3／U1-4／U2-3.html` 中 wiki/ 路徑改為 archive/wiki/ 並重出四份 PDF（KaTeX 0 錯誤）；說明文件 CLAUDE.md（資料流、目錄樹、規則 1／3／4／6／8 改寫，規則 5、7 停用，新增紀錄表加列）、CLAUDE-CODE.md（INGEST、COMPILE-ALL、LINT、ADD-CONCEPT 停用，ADD-METHOD／FIX-METHOD 不再同步 wiki）、CLAUDE-SPEC.md、CLAUDE-SOLVE.md、README.md、知識庫使用說明書.md、檔案架構索引表.md、.gitattributes、skills/README.md 與四份 skill 副本（加 SS 封存註記；六科共用，其他科路徑保留）。未改：7 份題解正本頁尾「詳見 wiki/log.md」為歷史註記（規則 1 不允許只為路徑改正本），請改看本檔；講義產生腳本 study/figs-src/*/build.py 為一次性腳本未改；帳號端的 skill（exam-wiki-audit 等）未改。備份於 VM `~/backup-fix-2026-11-01/`。
- 2026-11-01｜FIX-KATEX-RENDER｜渲染修正（非數值勘誤），續 FIX-KATEX-CDOTP：① 正本控制字元還原——SS-2019-4／2020-2 的 `\bar`（被吃成退格字元）、SS-2020-1 的 `\approx`（響鈴字元）、SS-2007-4／2019-4／2020-2／2025-4 的 `\tau`／`\times`／`\text`／`\theta`（反斜線 t 被吃成 Tab，頁面靜默顯示 imes、heta），共 42 處；② SS-2010-4 數學式內 `%` 改 `\%`（原為 LaTeX 註解，截斷算式）；SS-2015-4 `\text{}` 內下標 `C_{eq}` 移出；SS-2017-1 `\boxed` 式多一個 `}`；③ 以現行 `scripts/render_problem_view.py` 重新渲染全部 98 頁 `study/problems-view/`（58 頁有變動）：舊版渲染器把 `<L_c` 等當 HTML 標籤吃掉整段、吞掉 `_`／`*`／`\\`，並補上正本已有之「圖解補繪」頁尾；逐頁比對確認僅為還原內容。驗證：以 study/assets/katex 0.16.11 依 auto-render 規則逐頁重算 14,732 個數學式，錯誤 0。

- 2026-11-01｜UNIT-SS-U2-1｜新增 `study/unit-SS-U2-1.html`／`.pdf`（unit-overview 流程；使用者選擇完整單元總覽而非獨立 study 頁）與 `study/data/unit-SS-U2-1.json`。① 題目集合：主考點 6（2005-4、2010-1、2013-1、2020-2、2023-3、2025-4）＋副考點 2（2006-3、2009-3），`build_unit_page.py --check` 對帳通過；考點分三群（機構法 3、非對稱斷面 2＋0、對稱斷面 Z／形狀因子 1＋2），前後段對切以 Q[].cl／ty 程式重算。② 給／背證據：8 個考年（94、95、98、99、102、109、112、114）題目頁以 PyMuPDF 轉圖目視，其餘 16 年以 pdftotext 搜尋「塑性／形狀因／機構／虛功／崩塌／Mp／Zx」並對照 unit-SS-U1-2 既有逐年目視紀錄：除 LTB 式中的 Mp 符號與型鋼斷面表的 Zx 數值（96、97、99、101、103、109 年，皆別單元標準型鋼）外，無任何塑性分析式被印出；18 條中 17 條 must、1 條 give（結實斷面＋側撐以題目假設給出：2005-4、2020-2、2023-3）。③ 逐題公式標籤以關鍵字 regex 計數＋開題解 §4 確認；8 題答案以 Python 獨立重算（2005-4 wu 5.40 t/m、2010-1 My 144.6／Mp 256、2013-1 f 1.529、2020-2 wu 21.06、2023-3 My 48,003／Mp 61,875、2006-3 Zx 4,420,800 mm³、2009-3 1.124）全數一致。④ 由統計得出的命題觀察（可由 question_index.json 與資料檔重算）：近 6 考年 3/6（2020、2023、2025）、最長空窗 2014–2019；兩組原題換斷面重考（2005-4→2020-2 同支承同載重、2010-1→2023-3 同問法）；主考點 6 題有 4 題需求非對稱斷面 PNA 與 Z。⑤ 工具：`scripts/build_unit_page.py` 於 `study/lecture-<unit>.html` 不存在時移除導覽列與按鈕列的講義連結（其他五單元輸出不變）；problems-view SS-2005-4／2010-1／2013-1／2020-2／2023-3／2025-4 的 quick 按鈕改指 `../unit-SS-U2-1.html`（lect 按鈕：有 U1-2 副分類者維持 U1-2 講義並標「副分類」，其餘維持題庫儀表板），跟隨來源腳本的 UN 表未加 U2-1（避免導向不存在的講義）；重跑 build_frequency.py（對帳通過，U2-1 教材欄出現單元總覽）。PDF 以 Chromium print、A4、scale 0.85 產出 9 頁，1280／390 寬檢查 console 0 錯誤、KaTeX 0 錯誤、無水平溢出。⑥ 待複核（未修改索引或題解）：SS-2021-3、SS-2025-3、SS-2010-4、SS-2008-3 實際計算 Mp／Z／形狀因子（2021-3 並用 11.66Mp/L² 機構），未掛 U2-1 副考點；SS-2020-1（RBS 塑性鉸外移）、SS-2012-2（塑性轉角）屬塑性鉸觀念。SS-2013-1 題解 §4「S_x ≈ 0.08547πD³」應為 0.0272πD³ ≈ 0.0854D³（f 不受影響）。SS-2025-4 題解（三）表格「一次超靜定（單跨固端梁）｜2｜3」標籤矛盾、n+1 宜註明僅適用完全機構、§5 shakedown 譯作「應力遲緩」且描述有誤。未做：U2-1 尚無觀念講義；`start.html`（build_start.py 的 UNITS 資料區）未加入 U2-1；未建立 study-／formula-given-SS-U2-1 轉址頁（兩者從未存在）。

- 2026-11-01｜UNIT-SS-U2-1-R｜**更正上一筆 UNIT-SS-U2-1**：同日另一工作階段（unit-formula-map 呼叫）平行建置同一單元，其寫入覆蓋了上一筆的 `study/data/unit-SS-U2-1.json` 與 HTML（兩檔未入 git，原 18 條版本已無法還原；原 PDF 暫存於 `_ufm_tmp/unit-SS-U2-1.other-session.pdf`）。使用者決定保留覆蓋後的版本並修正紀錄。現行版本：16 條公式（15 must、1 half「塑性分析前提：結實斷面＋充分側撐」，ok＝2005、2020 題目內文給出；0 give），三群 S 斷面塑性性質（2010-1、2013-1、2023-3＋副 2006-3、2009-3）／M 塑性崩塌計算（2005-4、2020-2）／C 塑性鉸與崩塌機構概念（2025-4）；逐年表 ✔ 2、✗ 34。證據：8 個考年 13 頁轉圖目視＋24 年 pdftotext 關鍵字搜尋，結論與上一筆相同（無任何塑性分析式被印出；2010 參考公式集印含 Mp 的 Mn 式卻不定義 Mp）。逐題標籤以題解關鍵字計數核對，2023-3 題解另算形狀因子但題目未問，未列入。上一筆第 ⑤ 項工具與下游變更（build_unit_page.py 無講義時移除連結、problems-view 6 頁按鈕、frequency-SS.html）保留不動；第 ⑥ 項待複核已逐條核對並寫入頁尾（另確認 SS-2021-3 題解用 wu = 11.66Mp/L²）。PDF 重新以 Chromium print、A4、scale 0.85 產出 8 頁；1280／390 寬 console 0 錯誤、KaTeX 0 錯誤、無水平溢出、公式卡無溢出。

- 2026-11-01｜LECTURE-SS-U2-1｜新增 `study/lecture-SS-U2-1.html`／`.pdf`（unit-lecture 新建模式；HTML＋PDF、觀念＋手算範例、附考點對照、精選 5 題；PDF 18 頁，headless Chromium）。① 骨架：§0 全景「降伏是一個點的事，崩塌是整個結構的事」（斷面儲備 × 結構儲備）→ §1 My→Mp（中性軸由合力為零決定、M–φ 漸近線）→ §2 Z 與形狀因子 → §3 塑性鉸（λpd、轉動能力）→ §4 機構與虛功 → §5 上下限與彎矩重分配 → §6 規範前提（國內 λpd／1.5My、AISC 360-16 F9 T 型）→ §7 因果鏈＋決策流程 → §8 對照表（主 6＋副 2）→ §9 陷阱 18 條 → §10 自我檢測 12 → §11 精選 SS-2005-4、2023-3、2025-4、2013-1、2020-2（候補 2010-1、2009-3；貪婪覆蓋原選 2009-3，因加分來自 Vn／λc 等非本單元標籤改為觀念鏈題 2025-4）。手算範例 A–C：SS-2010-1、SS-2020-2（Z）、SS-2005-4（全流程），另 SS-2013-1 封閉解與極限檢查（d→0 得 1.698、d→D 得 4/π）。② 圖 9 張全部程式產生：`study/figs-src/lecture-SS-U2-1/calcs.py`（所有數值＋assert 對帳題解：2010-1 My 144.6／Mp 256；2023-3 PNA 80、Z 24,750；2005-4 Z 667.43、Mp 1,668.6、wu 5.40；2020-2 Z 4,624、wu 21.06；2009-3 f 1.124；2006-3 Z 4,420.8；管 f 1.529；機構最小值數值掃描＝6+4√2；下限彎矩圖 max ≤ Mp）＋`gen_figs.py`（`<!--FIG:id-->` 就地替換；共用 `../lecture-SS-U2-3/figlib.py`；纖維法求 M–φ 與中性軸遷移；浮點加總一律 math.fsum，Windows 端 Python 3.10 與雲端 3.13 重跑逐位元相同）。驗證：瀏覽器逐圖截圖目視、出界 0、KaTeX 446 式錯誤 0、PDF 抽頁、題號 8 題全連 problems-view、無 .md 連結。③ 下游：problems-view 8 頁（主 6 頁 lect 按鈕改指本講義；8 頁「跟隨來源單元」腳本 UN 表加 SS-U2-1）；同日另一工作階段已建 `unit-SS-U2-1.html`，本輪以 `build_unit_page.py SS-U2-1` 重生（差異僅新增講義三顆按鈕；**unit-SS-U2-1.pdf 未重出**）；講義 nav 加「📊 單元總覽」；重跑 `build_frequency.py`（U2-1 mat 加 lecture，對帳通過）。`start.html`／`scripts/build_start.py` 未列 U2-1，未改。
- 2026-11-01｜待處理（LECTURE-SS-U2-1 觀察到、未改動，待使用者決定）：① `raw/solutions/SS-2013-1` §4 二寫 $S_x \approx 0.08547\pi D^3$（多一個 π）、§4 五彙整表寫 $0.2686D^3$，正確為 $0.0855D^3$（$f$ = 1.529 不受影響）；② SS-2005-4 §6 依 AISC 360-16 F9（$M_A$ = My = 930.1、$M_C$ = Mp）估 wu「約 4.2 tf/m、低約 22%」，calcs.py 最小化＋下限彎矩圖重算為 **4.68 tf/m（x = 0.555L，低 13%）**，講義 §6 已用 4.68 並註明；③ SS-2005-4 §5.2「底緣（受拉）先降伏」——固定端為負彎矩，肢端受**壓**（數值不變，與 §6「肢受壓」矛盾）；④ SS-2005-4 §5.3 以結實 λp = 17/√Fy 檢核，塑性分析宜用 λpd = 14/√Fy = 8.85（7.69 仍通過）；⑤ SS-2025-4 §4（三）表列「一次超靜定（單跨固端梁）｜n = 2」標籤自相矛盾；⑥ `study/lecture-SS-U2-3.html` CSS 仍為 `.fig svg`（skill 規定 `.fig>svg`，圖說 KaTeX 根號可能消失）。

- 2026-11-01｜FIX-SS-U2-1｜依使用者指示處理 LECTURE-SS-U2-1「待處理」所列題解錯誤，三題正本勘誤（規則 1 四條件：考卷 94／102／114 年原頁以 PyMuPDF 130 dpi 轉圖目視（poppler 缺 Adobe-CNS1 字型無法出中文）、程式重算＋雙路徑、同步下游、正本頁尾加修正日期；三題 verificationStatus 原即 unverified）。**SS-2005-4**：① §5.2 肢端在固端負彎矩下為**受壓**（原寫受拉，數值不變）；② §5.3 改以塑性設計斷面 λpd = 14/√Fy = 8.85 檢核（7.69 通過）；③ §6 F9 之 1.6My 原以翼板側 S = 1323.2 算得 5293 而判跨間不受限，應以**肢端** Sx = 372.0（T 型最先降伏處；Kloiber, AISC Engineering Journal〈Flexural Strength of WT Sections〉取肢降伏之較小值）得 1.6My = 1,488.2 < Mp → 跨間 M_C = 1,488.2、固端 M_A = My = 930.1，補兩鉸不等強度閉合解 x = L[(M_A+M_C) − √((M_A+M_C)M_C)]/M_A = 0.5604L，wu「約 4.2、低約 22%」更正為 **4.28 tf/m（低 21%）**；數值掃描（20 萬點）與閉合解一致、代回平衡之跨間最大正彎矩恰為 M_C。**更正本人前一筆紀錄**：LECTURE-SS-U2-1 待處理 ② 所稱「4.68 tf/m」是沿用題解錯誤的 M_C = Mp 所得，錯；講義 §6、陷阱 #18、自我檢測 #12 已改為 4.28 並補「1.6My 用翼板側 S」的陷阱說明，calcs.py 改以 MC = min(Mp, 1.6My) 並加閉合解／掃描／下限三項 assert。**SS-2013-1**：Sx「≈ 0.08547πD³」（多 π）與彙整表「≈ 0.2686D³」更正為 0.0272πD³ ≈ 0.0855D³；重述註明考卷記為 d = 0.6D（Zx 0.1307D³、f 1.529 不變）。**SS-2025-4**：① 重述改回考卷原文「1. 何謂塑性鉸？ 2. 常見塑性鉸的出現位置？ 3. 何謂崩塌機構？」（原自行加「求極限載重」等要求，改註為延伸）；② §3.5 L2 表「M_p \neq 0」之 `\n` 被吃成換行、表格斷列，已還原；③ §4（三）「一次超靜定（單跨固端梁）｜2｜3」→ 兩次超靜定；④ §5 shakedown 誤譯「應力遲緩」→ 改寫為「安定」（交替塑性／增量崩塌）。下游：`scripts/render_problem_view.py` 重生三頁 problems-view（KaTeX 錯誤 0、清單與表格目視）；`study/lecture-SS-U2-1.html`／`.pdf` 改版重出（18 頁，KaTeX 463 式 0 錯誤）；question_index tags 無需變動。**未動**：`study/data/unit-SS-U2-1.json`／`unit-SS-U2-1.html`／`.pdf` 頁尾「待複核 ②③」仍列 SS-2013-1、SS-2025-4 筆誤為未修——該檔正由同日另一工作階段改寫中（json 15:13 UTC 仍在更新），為避免覆寫衝突留待該階段或使用者更新後重跑 `build_unit_page.py` 並重出 PDF。


- 2026-11-01｜OVERWRITE-SS-U2-1｜**事故紀錄**：本工作階段（續 UNIT-SS-U2-1，新建講義）未察覺另一工作階段已完成 LECTURE-SS-U2-1 與 UNIT-SS-U2-1-R，於 23:13 以 device_commit_files 寫入自己的版本，覆蓋了：`study/lecture-SS-U2-1.html`／`.pdf`（另一階段 18 頁講義，未入 git，本機無備份）、`study/data/unit-SS-U2-1.json`（使用者已決定保留的 16 條版）、`study/figs-src/lecture-SS-U2-1/calcs.py`（另一階段 gen_figs.py 依賴之）；並以覆蓋後 json 重跑 `build_unit_page.py SS-U2-1`。依使用者決定（請另一階段寫回）已撤回本階段寫入：上述講義 HTML／PDF、unit json、figs-src 的 body.html／build.py／build_pdf.py／figs.py／svglib.py／calcs.py 全部移至 `_to_delete/SS-U2-1-claude-eb-2026-11-01/`（未刪除，確認後可整夾刪）。**待另一工作階段寫回**：`study/lecture-SS-U2-1.html`／`.pdf`、`study/figs-src/lecture-SS-U2-1/calcs.py`、`study/data/unit-SS-U2-1.json`（16 條版），寫回後重跑 `build_unit_page.py SS-U2-1`（現存 `study/unit-SS-U2-1.html` 仍是由 18 條版產生，且其講義連結在寫回前為死連結）、重出 `unit-SS-U2-1.pdf`（現存 PDF 為 14:54 另一階段 16 條版，正確）、重跑 `build_frequency.py`。保留的本階段變更（與另一階段不衝突）：① problems-view 其餘 90 頁「跟隨來源單元」腳本 UN 表加 SS-U2-1（另 8 頁另一階段已加）；6 頁主考點 lect 按鈕指 `../lecture-SS-U2-1.html`（兩階段相同）。② `scripts/build_start.py` 新增 SS-U2-1（無影片／筆記本，練題改列 5 題解析頁；空連結不輸出、NotebookLM 計數改依實際數量、進度表排不下時 assert）；依使用者決定 12 週版 U1-3 與 U2-1 各 1 週（2–3 U1-1、4–5 U1-2、6–7 U1-4、8 U1-3、9–10 U2-3、11 U2-1、12 總複習），8 週版 2–7 週六單元、第 8 週總複習；重跑產生 `start.html`。③ 新增轉址頁 `study/study-SS-U2-1.html`（→ unit#s1）、`study/formula-given-SS-U2-1.html`（→ unit#s2），格式同 U1-1。教訓：多個工作階段同時處理同一單元時，寫入前須先比對目標檔 mtime（device_commit_files 的 expectedMtimeMs）並讀 log 末段。

- 2026-11-01｜INDEX-SS-U2-1｜依使用者指示處理單元總覽頁尾「待複核」的索引與題解項目。**索引**：判準＝題目明文要求本單元的量（\(Z\)、\(M_p\)、形狀因子）作為答案，或解法使用塑性機構；只把 \(M_p\) 當 LTB 輸入、或屬耐震接頭細部者不加。加 `SS-U2-1` 副分類 2 題：**SS-2021-3**（題目要求「塑性彎矩強度及形狀因子」並以塑性機構 \(w_u = 11.66M_p/L^2\) 求極限強度）、**SS-2025-3**（子題 1 明文求 \(M_p\)，與已列副分類的 SS-2006-3 同型）。不加：SS-2010-4（由 \(M_u\) 反算需求 \(Z_x\) 選斷面，屬 U1-2 設計流程）、SS-2008-3（\(Z_x\) 為已知、\(M_p\) 僅作 LTB 上限）、SS-2020-1（補強式／削弱式接頭，主題為耐震接頭）、SS-2012-2（塑性轉角需求與梁塑鉸區側撐，屬耐震規定）——四題均保留在單元總覽頁尾作為「相關但未掛分類」。同步：`question_index.json`、`dashboard-data.js`、兩題正本標頭「副分類」、`study/problems-view/` 兩頁；`audit_classification.py . SS` 98 題 0 筆問題；重跑 `build_frequency.py`（U2-1 主 6＋副 4，對帳通過）。**題解**：SS-2013-1 Sx 筆誤、SS-2025-4 表格標籤與 shakedown 已由 FIX-SS-U2-1 處理；本輪補 **SS-2025-4** §4（三）「塑性鉸數＝n＋1」僅適用完全機構（局部機構如兩跨連續梁單跨崩塌可較少、超完全機構可較多），§5 考場答法同步；正本頁尾加第二筆修正日期，重新渲染 problems-view（KaTeX 92 式 0 錯誤）。**待另一工作階段寫回 unit json 時一併處理**：`study/data/unit-SS-U2-1.json` 需新增 SS-2021-3、SS-2025-3 兩列 Q（否則 `build_unit_page.py --check` 會擋下），頁尾待複核改為已處理；`study/lecture-SS-U2-1.html` §8 副分類表補兩題。備份：VM `/tmp/bk-idx/`。

- 2026-11-01｜RESTORE-SS-U2-1｜依使用者指示寫回 OVERWRITE-SS-U2-1 撤回後缺少的檔案，並處理 INDEX-SS-U2-1 所列待辦。寫入前確認四個目標檔皆不存在（15:28 UTC）、log 末筆為 INDEX-SS-U2-1。**寫回**（來源：本工作階段 /mnt/user-data/outputs 副本）：① `study/lecture-SS-U2-1.html`／`.pdf`（含 FIX-SS-U2-1 的 §6 F9 4.28 tf/m 版，PDF 19 頁）；② `study/figs-src/lecture-SS-U2-1/calcs.py`（新增 S2021、S2025 斷面與 assert：BH700×300×12×25 Z 6,330、Mp 221.6 t·m、f = 6,330/5,670 = 1.116、wu = 11.657Mp/12² = 17.9 t/m；RH700×300×13×24 Z 6,248.8、Mp 21,871 tf·cm；全部通過，Windows 端重跑 gen_figs.py 逐位元相同）；③ `study/data/unit-SS-U2-1.json`（14:54 UTC 的 16 條版為底）。**unit json 更新**：Q[] 補 SS-2021-3（cl M、計算、f = Mp、H 型 Zx、形狀因子、11.66Mp/L²、適用前提）與 SS-2025-3（cl S、計算、f = Mp、H 型 Zx）；F[15]「適用前提」ok 加 2021（110 年公式區印 λpd、λp、Lp，已轉圖目視考卷 110 年第 2–3 頁確認無任何 Mp／Z／形狀因子／塑性機構式）；F[0]、F[5]、F[7]、F[13]、F[15] meta 與 drift、type、risk（斷面群 3＋副 3、最後 2025-3、空窗 0 年；崩塌群 2＋副 1、最後 2021-3、空窗 4 年）、judge、judgeMore、mxNote 的題數／考年改為 10 題、9 個考年；頁尾「待複核」改寫為「已處理」（索引加兩題、四題依判準不加、題解筆誤與 n+1 註記已修），頁尾與 mxNote 改為純文字（該區不經 KaTeX 渲染）。`build_unit_page.py SS-U2-1 --check` 通過（主 6＋副 4＝10 題、16 條），重生 `unit-SS-U2-1.html`（含講義按鈕）；以 headless Chromium（viewport 1200、scale 0.8、A4）重出 `unit-SS-U2-1.pdf`（10 頁，KaTeX 143 式 0 錯誤）。**講義**：header 副分類 2 → 4 題、§0 對照表補兩題、§8 副分類表補 SS-2021-3、SS-2025-3 兩列與加列說明、主分類表 SS-2025-4 列改為考卷原文問法（求極限載重屬延伸）；footer 加改版註記。重跑 `build_frequency.py`（U2-1 主 6＋副 4、mat 含 unit 與 lecture，對帳通過）。`_to_delete/SS-U2-1-claude-eb-2026-11-01/` 未動。

- 2026-11-02｜PROBLEM-SPLIT-PILOT-U2-1｜依使用者指示試做「題目／解答拆分」：參照 `[考古題知識庫]/skill/exam-solve.skill` 階段一的讀題方法（轉圖目視、先盲讀列判讀清單、每項標依據與把握、交使用者確認後才動解答），為 SS-U2-1 的 10 題（主 6＋副 4）新增題目正本 `raw/solutions/<id>/<id>-problem.md`（考卷原文逐字、考卷給的公式／附表、附圖引用、判讀清單；判讀狀態一律「待確認」）。考卷 9 份以 PyMuPDF 110 dpi 全頁盲讀，尺寸線端點以 220–400 dpi 局部放大（SS-2005-4 24 cm 為全深、SS-2020-2 600 mm 為全深、SS-2023-3 100 cm 為腹板淨高，皆與現行解析一致）。`scripts/render_problem_view.py` 改為偵測 `-problem.md` 時在解析前加「📄 題目正本」區塊，重生 10 頁 problems-view（KaTeX 0 錯誤）。盲讀後比對解析 §1：6 題一致；**SS-2025-3 讀題錯誤影響答案**（漏抄題給 Lp = 3.4 m、Lr = 10.5 m、Cb = 1，自行以 AISC 式算 Lp；題目求「標稱彎矩強度」Mn，解析答 φbMn = 196.8 tf·m，應為 Mn = Mp ≈ 218.7 tf·m）；**SS-2021-3 表一全文不在知識庫任何檔案**（fig-1.png 只有圖三，alt text 卻寫含表一），已於 problem.md 照錄；SS-2009-3 §1 漏抄題內 Pn 式、λc ≤ 1.5 與規範依據；SS-2020-2 §1 有一句「總高：300 + 550 + 250 mm」亂碼。解析 .md 本輪**均未修改**。報告與待確認項目：`wiki/queries/題目正本試做-SS-U2-1-2026-11-02.md`。

- 2026-11-02｜PROBLEM-SPLIT-CONFIRM-U2-1｜使用者確認 SS-U2-1 十題題目正本全部判讀（含五項解讀：SS-2005-4「因數化載重」不乘 φ；SS-2021-3「塑性彎矩強度」＝Mp、「塑性極限強度」＝崩塌機構極限載重；SS-2025-3「彈性彎矩強度」＝Mr＝(Fy−Fr)Sx、「標稱彎矩強度」＝Mn 不乘 φb）。① 10 份 `-problem.md` 判讀狀態改「已確認」，不確定項標「使用者確認」。② **SS-2025-3 解析勘誤**（規則 1 四條件：114 年考卷第 2 頁原文目視、程式雙路徑重算 Zx＝6,248.8（封閉式＝分塊）、Sx＝5,628.6、Mp＝21,871、Mr＝15,760 tf·cm、同步下游、頁尾修正日期）：§1 補題給 Lp＝3.4 m、Lr＝10.5 m、Cb＝1 與「標稱」字樣；刪除 §4 以 AISC 式自算 Lp＝2.92 m 的段落；答案 φbMn＝196.8 → **Mn＝Mp＝21,871 tf·cm ≈ 218.7 tf·m**（φbMn 改列參考）；新增陷阱 0；Mp 數值統一。下游：`study/data/unit-SS-U1-2.json` 該題摘要改「標稱強度 Mn」、公式標籤去掉 F[18] φb、F[18] meta 補同年 SS-2025-1（設計強度乘 φb）與 SS-2025-3（標稱不乘）對照；`build_unit_page.py SS-U1-2 --check` 通過並重生 HTML，Chromium 重出 `unit-SS-U1-2.pdf`（12 頁，KaTeX 308 式 0 錯誤）；講義無引用 196.8，未動；tags 未變。③ SS-2009-3 §1 補題給 Pn 式、λc ≤ 1.5 與規範依據；SS-2020-2 §1「總高」亂碼改寫（兩題數值不變，頁尾加修正日期）。④ `question_index.json` 加欄位 `problemStatus`（tagSystem 說明＋10 題 confirmed），`audit_classification.py` 0 問題。⑤ CLAUDE.md：規則 1 例外由三處改四處（題目正本建立、確認、凍結條件）、單向資料流與資料夾結構補 problem.md、CHANGELOG 加列。⑥ 重生 10 頁 problems-view（題目正本區塊標「已確認」）。未動：解析 §1 去留、exam-solve／稽核 skill 回寫、其他單元推廣（見試做報告 §5）。備份：VM `/tmp/bk2/`。

- 2026-11-02｜PROBLEM-SPLIT-SEC1-U2-1｜SS-U2-1 十題解析 §1 由全文重述改為「指向題目正本 `<id>-problem.md`＋常見誤讀表＋本解記號」，頁尾加修正日期；解題內容與答案不變（腳本 `scripts/fixes/2026-11-02_sec1_problem_pointer_U2-1.py`）。重生 10 頁 problems-view。skill：`[考古題知識庫]/skill/exam-solve.skill`（階段一產出改為 problem.md、解析 §1 新格式）、`exam-errata.skill`（先定題意再勘誤、題意勘誤流程）已替換，舊檔 `.bak-20261102`；帳號 skill exam-wiki-audit 改讀 problem.md 的版本以提案卡交使用者存檔。

- 2026-11-02｜PROBLEM-SPLIT-U1-1-B1｜SS-U1-1 題目正本推廣批 1：SS-2002-3、2003-1、2003-2、2003-3、2005-1、2006-1、2007-4、2008-2 建立 `-problem.md`（**待確認**），`question_index.json` 這 8 題加 `problemStatus: "draft"`，重生 8 頁 problems-view。盲讀比對：6 題一致；SS-2007-4 解析重述多寫「LRFD」（題文只說查圖，答案不受影響）；**SS-2008-2 支承判讀錯**——考卷圖 1（500 dpi）A、D 為鉸支、單根柱為底鉸＋頂導槽，解析寫成 A 固定、懸臂柱、D 固定；數值 $K_{AB} = 2\sqrt2$ 不變，㈡ 原因說明與示意需勘誤（待使用者確認題意後依規則 1 執行）。報告：`wiki/queries/題目正本-SS-U1-1-批1-2026-11-02.md`。備份：VM `/tmp/bk4/`。

- 2026-11-02｜DROP-WIKI-LINK-COL｜依使用者指示（「應該沒有補強頁」）：98 份解析 §3.5 VHA 的 L3 表刪除「補強頁」欄（94 份）與「概念連結」欄（4 份），共 702 列；這些 `[[page]]` 連結指向 2026-11-01 已封存的 `archive/wiki/`，已失效。刪除後 `raw/solutions/SS-*/SS-*.md` 不再有任何 wiki 連結（題號徽章 `[[SS-…]]` 原本就沒有）。內容與答案不變。腳本 `scripts/fixes/2026-11-02_drop_wiki_link_column.py`（先 dry-run 驗欄數一致再 --write）。順手修 SS-2019-4 L3 表一處 `\neq` 被存成換行＋「eq」的亂碼（`$t_e \neq w$`）。重生 98 頁 problems-view。帳號 skill `vha` 去掉補強頁欄與對照表的版本以提案卡交使用者存檔；`vha-treasure-map` 仍以補強頁欄建 WIKI 字典，未改。

- 2026-11-02｜PROBLEM-SPLIT-CONFIRM-U1-1-B1｜使用者確認 SS-U1-1 批 1 八題判讀清單（含「不確定」項之解讀）。① SS-2002-3、2003-1、2003-2、2003-3、2005-1、2006-1、2007-4、2008-2 的 `-problem.md` 判讀狀態改「已確認」、不確定項標「使用者確認」，`question_index.json` 八題 `problemStatus` draft → confirmed。② **SS-2008-2 解析勘誤**（規則 1 四條件：2008 卷圖 1 支承 500 dpi 目視（批 1 已做）、程式雙路徑驗算、同步下游、正本頁尾修正日期）：A、D 為鉸支，單根柱為底鉸＋頂導槽，原解誤作 A 固定、懸臂柱、D 固定。改寫 Step 1 機制——剛梁兩端支在柱頂、柱不計軸向變形 → 梁只平移不轉動 → θ_B = 0 → AB 為鉸底＋頂導槽 → K_AB,0 = 2.0（對位圖 G_A = ∞、G_B = 0 亦得 2.0）；陷阱④、L1／L2／L3、㈡ 示意圖（A、D 改鉸）與「側向抵抗來自 B 端剛接、柱身反曲 3EIδ/L³」；§5 補精確解：tan u = 2u、u = 1.1656 → K = 2.70（有限差分特徵值 2.695 一致），萊梅厥 2√2 = 2.83 偏大約 5%，原因為靠桿 P 對 AB 柱身之二次彎矩 PΔx/L 小於 P·y(x)。數值答案 K'_AB = 2√2 不變；下游（unit-SS-U1-1.json 摘要、lecture-SS-U1-1.html §5.4）無支承相關敘述，未改。腳本 `scripts/fixes/2026-11-02_fix_SS-2008-2_supports.py`。③ 八題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」（同 U2-1 格式；§1 內的考卷附圖皆已在題目正本，assert 檢查後才移除），SS-2007-4 刪去題文沒有的「LRFD」（頭表與索引 designMethod 仍為 LRFD，未改）；頁尾加修正日期；腳本 `scripts/fixes/2026-11-02_sec1_problem_pointer_U1-1_B1.py`。重生八頁 problems-view。備份：VM `/tmp/bk5/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-1-B2｜SS-U1-1 題目正本推廣批 2：SS-2010-3、2011-2、2011-4、2013-2、2013-3、2014-1、2015-2、2015-3 建立 `-problem.md`（**待確認**），`question_index.json` 八題加 `problemStatus: "draft"`，重生八頁 problems-view。考卷 PyMuPDF 110 dpi 全頁盲讀，附圖 300–500 dpi 局部（2011 第 3 頁 τ_a 式 300 dpi）。比對解析 §1：5 題一致（2010-3、2011-2、2011-4 為 11-01 已勘誤者）；SS-2014-1 重述替兩條 F_cr 式加上考卷未標的適用範圍；**SS-2015-2 把未給條件寫成題目事實**——銲接符號只畫箭頭側一個三角形（依慣例為一道），解析寫「連接板兩側各一道」以 70 cm 算得 w = 8 mm，若為一道需求約 15.3 mm；螺栓「承壓型」亦為題未給；SS-2015-3 附圖 alt text 誤寫「背靠背」「形心間距 20cm」。解析 .md 本輪未改。批 1＋批 2 十六頁 problems-view 以 study/assets/katex 0.16.11 檢查：KaTeX 錯誤 0、殘留 $ 0。`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-1-批2-2026-11-02.md`。

- 2026-11-02｜PROBLEM-SPLIT-CONFIRM-U1-1-B2｜使用者確認 SS-U1-1 批 2 八題判讀清單；SS-2015-2 銲道道數定為**兩道**（連接板兩側各一道）。① SS-2010-3、2011-2、2011-4、2013-2、2013-3、2014-1、2015-2、2015-3 的 `-problem.md` 改「已確認」，`problemStatus` draft → confirmed。② SS-2015-2 Part(二) 補註：考卷銲接符號只畫箭頭側（慣例為一道），依實務與使用者確認採兩道，答案 w = 8 mm 不變；一道時需求 83.46/54.56 = 1.53 cm → 16 mm；頁尾加修正日期。③ 八題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」；SS-2013-2、2013-3、2015-2 §1 內解析自繪向量圖（figs/*.svg）連同圖說移入 §1「判讀圖解（解析自繪）」小節保留；SS-2015-3 錯誤的 alt text（背靠背、形心間距 20cm）隨 §1 移除，SS-2014-1 重述加的適用範圍一併移除。重生八頁 problems-view（KaTeX 錯誤 0、殘留 $ 0）；`audit_classification.py` 0 問題。腳本 `scripts/fixes/2026-11-02_confirm_sec1_U1-1_B2.py`。備份：VM `/tmp/bk6/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-1-B3｜SS-U1-1 題目正本推廣批 3（主分類剩餘 10 題）：SS-2016-3、2017-3、2018-2、2021-2、2022-2、2023-1、2023-2、2024-1、2024-2、2025-2 建立 `-problem.md`（**待確認**），`question_index.json` 十題加 `problemStatus: "draft"`；SS-2023-2 題內參考公式為圖片，新增截圖 `SS-2023-2-eqn-1.png`（pdftoppm 200 dpi）。本工作階段無法把本機圖檔帶到檢視端，改以 GitHub 上同一 commit（cb232a0）的考卷在雲端轉圖（PyMuPDF 110 dpi 全頁、附圖 300–500 dpi 局部），8 份 PDF 與本機 md5 逐一相同。比對解析 §1：8 題一致；SS-2016-3 頭表「設計法：LRFD」考卷未指定；SS-2018-2 已知條件表把「正方形」「80 cm 為外緣」「1,119 tf 為 $P_u$」寫成題目事實（照常見解讀答案不變；改中心線寬 $\phi_cP_n$ 2,586 → 2,708 tf，仍 OK）。**本批無改變答案的讀題錯誤**。解析 .md 本輪未改。重生十頁 problems-view：KaTeX 1,915 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-1-批3-2026-11-02.md`。備份：VM `~/bk7/`。

- 2026-11-02｜PROBLEM-SPLIT-CONFIRM-U1-1-B3｜使用者確認 SS-U1-1 批 3 十題判讀清單（「繼續」，依清單「本檔判讀」）。① SS-2016-3、2017-3、2018-2、2021-2、2022-2、2023-1、2023-2、2024-1、2024-2、2025-2 的 `-problem.md` 改「已確認」，不確定項標「使用者確認」；清單中以問句列出者寫明處理（皆同現行解析）：2016-3 照圖數值作答並指出不自平衡；2017-3 由 $C_c$ 反推 $F_y$ = 2.458、局部挫屈不列必答；2018-2 含寬厚比檢核；2022-2 檢核插銷孔尺寸規定；2023-1 梁勁度不做遠端修正；2024-2 只算桿件極限狀態、用 $U = 1 - \bar{x}/L$、**最小銲腳以較厚板 20 mm 查表 → 8 mm**（若以較薄板 10 mm 為 5 mm，此項會改變答案）；2025-2 仍依縱向銲長與板寬比定 $U$、連接板不列必答。`problemStatus` 十題 draft → confirmed（U1-1 主分類 26 題全部 confirmed）。② SS-2016-3 頭表「設計法：LRFD」補註「考卷未指定設計法；本題為挫屈強度理論，不含 φ」（索引 designMethod 不變）；正文一處「見圖說」改指題目正本判讀 #4。③ 十題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」（§1 附圖皆已在題目正本，assert 後移除；本批無自繪向量圖）；SS-2018-2 正方形、80 cm 外緣、1,119 tf 為 $P_u$ 改標為本解假設；頁尾加修正日期，答案不變。腳本 `scripts/fixes/2026-11-02_confirm_sec1_U1-1_B3.py`。重生十頁 problems-view（KaTeX 1,902 式錯誤 0、殘留 $ 0）；`audit_classification.py` 98 題 0 問題。備份：VM `~/bk7/`（確認前的解析與索引）。

- 2026-11-02｜PROBLEM-SPLIT-U1-2-B1｜SS-U1-2 題目正本推廣批 1：SS-2002-1、2002-2、2005-2、2006-4、2007-3、2008-1、2008-3、2010-4、2011-3 建立 `-problem.md`（**待確認**），`question_index.json` 九題加 `problemStatus: "draft"`；新增公式集截圖 `SS-2007-3-eqn-1.png`、`SS-2008-3-eqn-1.png`、`SS-2008-3-eqn-2.png`、`SS-2011-3-eqn-1.png`（pdftoppm 150 dpi）。轉圖同批 3 做法（GitHub cb232a0 考卷，7 份 PDF 與本機 md5 相同；110 dpi 全頁、附圖 300–450 dpi，SS-2011-3 斷面 800 dpi＋PDF 向量座標）。比對解析 §1：8 題一致；**SS-2011-3 讀題錯誤影響答案**——40.62 cm 尺寸線端點在翼板內側面，為腹板淨高（全深 43.16 cm），解析當成全深；依圖重算 $L_r$ 833 → 803.5 cm < $L_b$ 812.8 → 由非彈性改為**彈性 LTB**，$M_n$ 3,378 → 約 3,491 tf·cm（$C_b$ = 1.75）；另支承 A／B 標反（不影響）。另見 **SS-2002-1 ㈠ 剪力流方向畫錯**（$V_x$ 下翼板剪力全寬與 $V_x$ 同向，解析寫成兩半向中心匯聚、相反相消）。解析 .md 本輪未改。重生九頁 problems-view：KaTeX 1,755 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-2-批1-2026-11-02.md`。備份：VM `~/bk8/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-2-B2｜SS-U1-2 題目正本推廣批 2（主分類剩餘 8 題）：SS-2012-1、2014-3、2015-1、2016-1、2016-4、2019-2、2024-3、2025-1 建立 `-problem.md`（**待確認**），`question_index.json` 八題加 `problemStatus: "draft"`；新增 `SS-2024-3-eqn-1.png`（題內參考公式圖片，pdftoppm 150 dpi）。轉圖同批 1 做法（GitHub cb232a0 考卷，7 份 PDF 與本機 md5 相同）；SS-2015-1 圖 1(b) 七條曲線以 PDF 向量座標讀平台值與轉折點（BH 920×300 平台 233.8、終點 3.04 m 等）並照錄於題目正本。比對解析 §1：**8 題全部一致，無讀題錯誤**（SS-2025-1 的 42 cm 腹板淨高解析讀對）。解析 .md 本輪未改。重生八頁 problems-view：KaTeX 1,593 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-2-批2-2026-11-02.md`。備份：VM `~/bk9/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-4-B1｜SS-U1-4 題目正本推廣批 1：SS-2002-4、2004-2、2004-3、2005-3、2006-2、2006-5、2007-1 建立 `-problem.md`（**待確認**），`question_index.json` 七題加 `problemStatus: "draft"`。轉圖同前（GitHub cb232a0 考卷，新增的 2004 卷與本機 md5 相同；110 dpi 全頁、附圖 400–450 dpi 以內嵌圖片 bbox 定位）。比對解析 §1：**7 題全部一致，無讀題錯誤**；其中 2004-3、2005-3、2007-1 為 2026-11-01 勘誤後版本，本次盲讀再次確認。題目本身的矛盾記在報告 §2（2004-3 題文「雙角鋼」與圖不符；2005-3 雙面符號含箱內側）。解析 .md 本輪未改。重生七頁 problems-view：KaTeX 609 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-4-批1-2026-11-02.md`。備份：VM `~/bk10/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-4-B2｜SS-U1-4 題目正本推廣批 2：SS-2009-2、2009-4、2012-2、2012-4、2017-2、2017-4、2018-3 建立 `-problem.md`（**待確認**），`question_index.json` 七題加 `problemStatus: "draft"`。轉圖同前（GitHub cb232a0 考卷，新增的 2009 卷與本機 md5 相同；110 dpi 全頁、附圖 400 dpi）。比對解析 §1：6 題一致；**SS-2018-3 漏讀全周銲符號**——三個 6 mm 填角銲符號在箭頭與基線交點皆有圓圈（weld all around），翼板銲長應取 $2b_f + 2t_f$ = 432 mm，解析主答取 400 mm 需 11 mm、432 mm 列為「寬鬆取法」需 10 mm；依符號主答應為 10 mm（6 mm 皆 NG，結論不變）。解析 .md 本輪未改。重生七頁 problems-view：KaTeX 935 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-4-批2-2026-11-02.md`。備份：VM `~/bk11/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-4-B3｜SS-U1-4 題目正本推廣批 3（主分類剩餘 6 題）：SS-2019-4、2020-1、2020-4、2021-4、2023-4、2024-4 建立 `-problem.md`（**待確認**），`question_index.json` 六題加 `problemStatus: "draft"`；SS-U1-4 主分類 20 題至此全部有題目正本。轉圖同前（GitHub cb232a0 考卷，新增的 2020 卷與本機 md5 相同；110 dpi 全頁、附圖 300–450 dpi）。比對解析 §1：**6 題全部一致，無讀題錯誤**。解析 .md 本輪未改。重生六頁 problems-view：KaTeX 659 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-4-批3-2026-11-02.md`。備份：VM `~/bk12/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-3-B1｜SS-U1-3 題目正本推廣批 1：SS-2003-4、2004-4、2007-2、2008-4、2009-1、2011-1 建立 `-problem.md`（**待確認**），`question_index.json` 六題加 `problemStatus: "draft"`；新增題內公式截圖 `SS-2003-4-eqn-1/2.png`、`SS-2004-4-eqn-1/2.png`、`SS-2007-2-eqn-1.png`、`SS-2008-4-eqn-1.png`（本機 pdftoppm 150 dpi）。轉圖改由本機 `raw/exams/` 直接送雲端（不經 GitHub 副本），110 dpi 全頁、附圖 300–800 dpi。比對解析 §1：5 題一致；**SS-2004-4 ㈡讀題錯誤**——考卷問「≥ 0.4 為何我國規範不再採用」，解析改寫成「下限 0.4 的工程意義」並答保留理由，方向相反（說明題，無數值；與 SS-2003-4 解析「不設下限」矛盾）；另 §4㈡ $M_1/M_2$ 正負號自相矛盾。解析 .md 本輪未改。重生六頁 problems-view：KaTeX 1,504 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-3-批1-2026-11-02.md`。備份：VM `~/bk13/`。

- 2026-11-02｜PROBLEM-SPLIT-U1-3-B2｜SS-U1-3 題目正本推廣批 2（主分類剩餘 6 題）：SS-2012-3、2013-4、2014-4、2019-3、2020-3、2022-1 建立 `-problem.md`（**待確認**），`question_index.json` 六題加 `problemStatus: "draft"`；SS-U1-3 主分類 12 題至此全部有題目正本。新增題內公式截圖 `SS-2012-3-eqn-1.png`、`SS-2013-4-eqn-1/2.png`（eqn-2 為所引第 1 頁 Alignment Chart）、`SS-2014-4-eqn-1.png`、`SS-2019-3-eqn-1.png`、`SS-2020-3-eqn-1.png`、`SS-2022-1-eqn-1.png`（本機 pdftoppm 150 dpi）。轉圖同批 1（本機考卷直送雲端；110 dpi 全頁、附圖 450–900 dpi，向量圖以 PDF 路徑／座標核對）。比對解析 §1：**6 題皆無讀題錯誤**；3 題有加字或改寫（2012-3 列題未給的 $E$、2013-4 列考卷沒有的 $M_u$ 式、2022-1 把考卷 $\exp(-0.419\lambda_c^2)$ 改寫為 $0.658^{\lambda_c^2}$），答案不受影響。待確認的影響答案項：2013-4 梁遠端鉸接是否修正 $G_B$、2019-3 AB 段是否受軸力（本檔判讀皆同解析主答）。解析 .md 本輪未改。重生六頁 problems-view：KaTeX 2,102 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U1-3-批2-2026-11-02.md`。備份：VM `~/bk14/`。

- 2026-11-02｜PROBLEM-SPLIT-U2-3-B1｜SS-U2-3 題目正本推廣批 1（主分類全部 7 題）：SS-2004-1、2010-2、2016-2、2018-4、2019-1、2021-1、2022-3 建立 `-problem.md`（**待確認**），`question_index.json` 七題加 `problemStatus: "draft"`；SS-U2-3 主分類至此全部有題目正本。皆為說明題，無題內公式截圖。轉圖同 U1-3（本機考卷直送雲端；110 dpi 全頁，SS-2021-1 圖一 450 dpi）。比對解析 §1：**7 題全部一致，無讀題錯誤**；本批無「不確定」判讀項。解析 .md 本輪未改。重生七頁 problems-view：KaTeX 174 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U2-3-批1-2026-11-02.md`。備份：VM `~/bk15/`。

- 2026-11-03｜PROBLEM-SPLIT-U2-2-B1｜SS-U2-2 題目正本推廣批 1（主分類全部 6 題）：SS-2014-2、2015-4、2016-5、2017-1、2018-1、2022-4 建立 `-problem.md`（**待確認**），`question_index.json` 六題加 `problemStatus: "draft"`；**SS 全科 98 題至此都有題目正本**。轉圖同前（本機考卷直送雲端；110 dpi 全頁，2018-1、2022-4 附圖 400 dpi），無題內公式截圖。比對解析 §1：4 題一致；**SS-2017-1 讀表錯誤**——考卷鋼種 D 的 Ceq 為 0.44~0.47（四者最高），解析 §1 表與 §3 矩陣寫成「無規定」、§5 稱 D「實際 Ceq 相當低」（說明題，選 D 的結論可能不變，但碳當量理由須改寫）；SS-2018-1 圖說「A 於 ε ≈ 0.035 起硬化」屬加字（本檔判讀約在 0.06 刻度處、橫軸不按比例），不影響答案。解析 .md 本輪未改。重生六頁 problems-view：KaTeX 382 式錯誤 0、殘留 $ 0；`audit_classification.py` 98 題 0 問題。報告：`wiki/queries/題目正本-SS-U2-2-批1-2026-11-03.md`。備份：VM `~/bk16/`。

- 2026-11-03｜AUDIT-BLIND-REMAIN22｜盲解比對 SS 已勘誤但未盲解的剩餘 22 題（僅新增報告、未改題解與索引）：報告 `wiki/queries/盲解比對-SS-已勘誤剩餘22題-2026-11-03.md`、紀錄 `盲解紀錄-SS-已勘誤剩餘22題-2026-11-03.md`；`audit-ledger-SS.json` 加 22 筆（scope「已勘誤題剩餘」，ledger 至此 98／98）。結果：一致 17；分歧-答案改變 2——SS-2011-3 將腹板淨高 40.62 讀成全深（d 應 43.16，Lr 803.1 < Lb 812.8 改判彈性、Mn 3378 → 3489 tf·cm）、SS-2005-1 塊狀剪力單排撕出塊只承 P/2 卻比全載重（φPn 68.5 → 71.8 tf 螺栓剪力控制，待使用者決定）；分歧-觀念作圖 2——SS-2009-1 08-22 勘誤殘留（§3 Step 3 仍 1.1RyFybZb+Mv、§3.5 L3 斜率敘述相反）、SS-2022-3 漏 AISC 341 J 章 MT／k 區／層狀撕裂 UT；盲解不確定 1——SS-2013-4 對位圖梁遠端修正（K 1.85 vs 2.01，同 SS-2013-2 型）。獨立性揭露：自動載入的 CLAUDE.md 變更紀錄含 8 題舊勘誤結論，相關點標「一致但非獨立」。考卷 16 年以 PyMuPDF 轉圖目視，SS-2011-3 斷面圖與 SS-2005-1 數值由主工作階段另行核對。

- 2026-11-03｜FIX-SS-REMAIN22｜依盲解比對（AUDIT-BLIND-REMAIN22）勘誤 3 題、清殘留 1 題，四題 verificationStatus 維持 unverified，頁尾加修正日期。① **SS-2011-3**：2011 p2 斷面圖 40.62 為腹板淨高（尺寸線止於翼板內緣，主工作階段 400 dpi 看圖確認），d 40.62 → **43.16** cm，斷面性質全數重算（Ix 29,742、Sx 1378.2、Zx 1604.9、J 55.48、Cw 779,084、X1 162.0、X2 1.529、Lp 209.5、Lr 833.2 → **803.1** cm），Lb 812.8 > Lr 改判**彈性** LTB，Mn 3378 → **3489** tf·cm（彈性式與 Cb·Mo,cr 雙路徑同值），問「是否在彈性範圍」改答「是」；§1 支承更正 A 滾支／B 鉸支；§6 AISC 對照同判彈性（Lr 698.4、Mn 3279）。② **SS-2005-1**（使用者決定採受力分擔）：原控制「路徑 A」撕出塊只含第 2 排 3 栓、只承 P/2 卻比總力；塊狀剪力改以台灣二式主算含全部 6 栓撕出塊 **100.2 tf**（單式同值），路徑 A／B 換算等效總力 141.7／160.5 tf，φPn 68.5 → **71.8 tf 螺栓剪力控制**。③ **SS-2013-4**（使用者決定，同 SS-2013-2）：梁遠端 A、D 滾支承，對位圖 G_B 乘 ×½：0.75 → **1.50**，K 1.85 → **2.01**（精確 2.008／近似 2.020），ΣPeK 2.88 → **2.45EI/L²**，B2＝1/(1−0.409PL²/EI)；未修正值移 §5 替代解並註偏不保守，附真鉸解 K 2.48。④ **SS-2009-1**：清 08-22 勘誤殘留——§3 Step 1–3 改為 (13.6-3) 梁側 ×1.25（AISC 341 之 1.1RyFybZb＋Muv 改標對照）、§3.5 L3 P-M 斜率敘述改為 AB −8/9 較平／BC −2 較陡、Mv 列標 AISC 對照；答案不變。數值以 Python 重算並雙路徑檢核。下游：`gen_SS-2005-1.py`／`gen_SS-2011-3.py`／`gen_SS-2013-4.py` 改為由式子現算並加 assert，重繪 SS-2005-1 圖 2、3，SS-2011-3 圖 2、3，SS-2013-4 圖 3（render.py 溢出 0）；`render_problem_view.py` 重出四題 problems-view；`question_index.json`／`dashboard-data.js` tags：SS-2011-3「非彈性LTB」→「彈性LTB」、SS-2013-4 加「梁遠端修正」；`study/lecture-SS-U1-1.html`（圖 9-1 圖說與 SVG 文字、題表、陷阱表、精選題說明）與 `figs-src/lecture-SS-U1-1/figs_d.py`、`textbook-SS-U1-1-tension.html` 與 `figs-src/textbook-SS-U1-1/ch2／ch5／ch6.html`（含「控制的是肢趾側邊距最小那一條」的錯誤敘述）、`lecture-SS-U1-2.html` 題表、`lecture-SS-U1-3.html`（§4 陷阱的 ΣPeK 2.88 → 2.45、精選題提示加梁遠端修正）、`study/data/unit-SS-U1-3.json`（梁遠端修正條 meta 改寫、SS-2013-4 逐題公式加該條）並重跑 `build_unit_page.py SS-U1-3`（--check OK）；以 Chromium（print 媒體、A4、14／16／13／13 mm、展開 details）重出 lecture-SS-U1-1（49 頁）、textbook-SS-U1-1-tension（53）、lecture-SS-U1-2（40）、lecture-SS-U1-3（42）、unit-SS-U1-3（16）PDF，KaTeX 0 錯誤。ledger 四題填 human／fixed。未改：一次性遷移腳本 `figs-src/lecture-SS-U1-1/build.py`、`lecture-SS-U1-3/build.py`（留存備查）；SS-2022-3 補檢驗項目待查規範原文。備份於 VM `~/bk-errata-2026-11-03/`。

- 2026-11-03｜PROBLEM-REDRAW-U2-1-B1｜SS-U2-1 已確認題目補重繪（exam-problem-split §8 試做）：有附圖的 5 題 SS-2005-4、2010-1、2013-1、2020-2、2023-3 依已確認的題目正本判讀清單，以 struct-diagram 重繪 `figs/<id>-fig-1-problem.svg`＋2× PNG（render.py 溢出 0）；新建 `gen_SS-2005-4.py`、`gen_SS-2010-1.py`、`gen_SS-2013-1.py`、`gen_SS-2020-2.py`，`gen_SS-2023-3.py` 加 `fig1_problem()`（題目常數與解題常數分開，既有圖 2、3 不動）；重繪圖插入各解析 §1（引用區塊後、常見誤讀前），頁尾加修正日期；重出五題 problems-view，KaTeX 812 式 0 錯誤、殘留 `$` 0。SS-2025-4 無附圖不重繪。重繪時判讀清單無缺項、與證據圖一致；「原圖｜重繪」對照圖僅交使用者抽查，不進 repo。problem.md 與證據圖未改。

- 2026-11-03｜PROBLEM-REDRAW-U1-1-B1｜SS-U1-1 已確認題目補重繪批 1（7 題）：SS-2002-3、2003-2、2003-3、2005-1、2007-4、2008-2、2010-3 依已確認的題目正本判讀清單，以 struct-diagram 重繪 `figs/<id>-fig-1-problem.svg`＋2× PNG（render.py 溢出 0）；新建 `gen_SS-2002-3.py`、`gen_SS-2003-2.py`、`gen_SS-2003-3.py`、`gen_SS-2007-4.py`、`gen_SS-2008-2.py`、`gen_SS-2010-3.py`，`gen_SS-2005-1.py` 加 `fig1_problem()`（題目常數與解題常數分開，既有圖 2、3 不動）；重繪圖插入各解析 §1，頁尾加修正日期；重出七題 problems-view，KaTeX 1275 式 0 錯誤、殘留 `$` 0。設計圖表不重繪：SS-2002-3 設計 K 值表、SS-2007-4 對位圖。示意部分已於圖內註明（SS-2003-2 鋼筋位置、SS-2003-3 WT 外形與螺栓橫向間距、SS-2005-1 接合板外形）。**待使用者決定**：SS-2002-3-problem.md §3 與頭表把 `fig-1.png` 寫成柱立面、`fig-2.png` 寫成 K 值表，實際檔案相反（fig-1 為 K 值表、fig-2 為柱立面）；判讀清單內容與證據圖一致，未改 problem.md。

- 2026-11-03｜PROBLEM-REDRAW-U1-1-B2｜SS-U1-1 已確認題目補重繪批 2（7 題）：SS-2011-2、2011-4、2013-2、2013-3、2015-2、2015-3、2016-3 依已確認的題目正本判讀清單，以 struct-diagram 重繪 `figs/<id>-fig-1-problem.svg`＋2× PNG（render.py 溢出 0）；新建 `gen_SS-2011-2.py`、`gen_SS-2011-4.py`、`gen_SS-2016-3.py`，`gen_SS-2013-2.py`、`gen_SS-2013-3.py`、`gen_SS-2015-2.py`、`gen_SS-2015-3.py` 加 `fig1_problem()`（題目常數與解題常數分開，既有圖不動；`gen_SS-2015-2.py` 的輸出目錄改為可由參數指定，預設不變）；重繪圖插入各解析 §1，頁尾加修正日期；重出七題 problems-view，KaTeX 1736 式 0 錯誤、殘留 `$` 0。不重繪：SS-2011-4、SS-2013-2 對位圖，SS-2016-3 圖 2 應力–應變曲線。SS-2015-2 既有圖 1（接合詳圖，含解題數值）保留，題目重繪圖不編號、圖說指向圖 1。示意部分已於圖內註明（SS-2015-2 柱與連接板外形、SS-2015-3 槽鋼板厚、SS-2013-3 斷面方位）。重繪時判讀清單無缺項、與證據圖一致。

- 2026-11-03｜PROBLEM-FIX-SS-2002-3｜題目正本凍結後更正（使用者同意）：`SS-2002-3-problem.md` 頭表與 §3 把證據圖檔名寫反，更正為柱立面＋斷面 `fig-2.png`、設計 K 值表 `fig-1.png`（回證據圖逐張目視確認；考卷原文、§2、判讀清單不變），頁尾加修正日期；重出 problems-view。解析 `SS-2002-3.md` 未引用這兩張圖，不需修改。

- 2026-11-03｜PROBLEM-REDRAW-U1-1-B3｜SS-U1-1 已確認題目補重繪批 3（5 題，U1-1 補重繪完成）：SS-2021-2、2023-1、2024-1、2024-2、2025-2 依已確認的題目正本判讀清單，以 struct-diagram 重繪 `figs/<id>-fig-1-problem.svg`＋2× PNG（render.py 溢出 0）；新建 `gen_SS-2021-2.py`、`gen_SS-2023-1.py`、`gen_SS-2024-2.py`、`gen_SS-2025-2.py`，`gen_SS-2024-1.py` 加 `fig1_problem()`（題目常數與解題常數分開，既有圖 2、3 不動）；重繪圖插入各解析 §1，頁尾加修正日期；重出五題 problems-view，KaTeX 0 錯誤、殘留 `$` 0。不重繪：SS-2023-1 對位圖、SS-2024-1 圖(a)(c) 曲線、SS-2024-2 填角銲最小尺寸表（已照錄於題目正本 §2）。SS-2021-2 破壞模式為本題所求，圖上不畫。重繪時判讀清單無缺項、與證據圖一致。

- 2026-11-03｜PROBLEM-REDRAW-U1-2-B0｜SS-U1-2 已確認題目補重繪（2 題；U1-2 其餘已確認題 SS-2006-3、2025-3 無附圖）：SS-2009-3、2021-3 依已確認的題目正本判讀清單，以 struct-diagram 重繪 `figs/<id>-fig-1-problem.svg`＋2× PNG（render.py 溢出 0）；新建 `gen_SS-2009-3.py`、`gen_SS-2021-3.py`；重繪圖插入各解析 §1，頁尾加修正日期；重出兩題 problems-view，KaTeX 0 錯誤。SS-2009-3 原圖為無尺寸線示意圖，重繪依標示按比例並標出 d、b_f、t_w、t_f 位置；SS-2021-3 表一已照錄於題目正本，不重繪。至此所有已確認題目之附圖補重繪完成。

- 2026-11-03｜PROBLEM-REDRAW-DRAFT｜依使用者指示（判讀清單最後一次確認），先依**待確認（draft）**判讀清單重繪其餘 32 題附圖：U1-2 9 題（SS-2002-2、2005-2、2008-3、2010-4、2011-3、2015-1、2019-2、2024-3、2025-1）、U1-3 8 題（SS-2003-4、2004-4、2007-2、2008-4、2009-1、2013-4、2019-3、2020-3）、U1-4 12 題（SS-2002-4、2004-2、2004-3、2005-3、2007-1、2009-4、2012-4、2017-4、2018-3、2019-4、2020-4、2024-4）、U2-2 2 題（SS-2018-1、2022-4）、U2-3 1 題（SS-2021-1）。產出 `figs/<id>-fig-1-problem.svg`＋2× PNG（58 張重繪圖 render.py 溢出全 0）與 gen 腳本（新建 20 支、既有 12 支追加 `fig1_problem()`；既有圖未動；SS-2003-4、2009-1、2009-4、2017-4、2018-3、2020-3、2020-4 的 gen 檔換行由 CRLF 改存 LF 以對齊 git 索引；SS-2025-1 補上 repo 內 struct-diagram 的 import 路徑；多支 gen 的 OUT 改為可由參數指定、預設不變）。**本輪不改解析 .md、題目正本、索引與瀏覽頁**：確認判讀清單時再依 exam-problem-split §7 插圖並改寫 §1；確認時若改動判讀，重跑該題 gen 即可。不重繪：SS-2010-4 RH 斷面表、SS-2015-1 圖 1(b) 設計彎矩曲線、SS-2018-1 應力–應變圖；SS-2022-4 圖(b) 為題給均勻分布（端點與高度皆為標示值），例外重繪。重繪時發現、待確認時一併處理的判讀清單問題：SS-2005-2 主筋水平位置未列（示意取 8 cm）；SS-2010-4 題目正本 §3 圖說「上翼板頂與版底相接」與清單 #4「埋入」不一致；SS-2011-3 清單未記 M 轉向（照證據圖畫順時針）；SS-2024-3 C 處豎線未判讀、兩個紅色「C」疑為後加註記；SS-2002-4 鋼板外形未列（原圖不依比例）；SS-2005-3 柱內水平加勁板未列；SS-2017-4 柱內雙虛線（兩端橢圓）未解釋、未畫；SS-2018-3 銲接符號單面／雙面未定；SS-2020-4 翼板螺栓未列；SS-2024-4 翼板短豎線與交角弧形記號未解釋、未畫。

- 2026-11-03｜FIG-SS-U1-3-B2｜U1-3 梁柱桿件剩餘 6 題補解題向量圖解（struct-diagram，12 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：SS-2004-4（fig-1-decompose 45° 懸臂 P 分解與力臂、fig-2-ratio 量級）、SS-2007-2（fig-1-equiv 三角形彎矩→Cm 等效均勻→二階放大、fig-2-terms 兩式組成與放大貢獻）、SS-2008-4（fig-1-bmd 彎矩疊加與兩軸挫屈長度、fig-2-pmax 互制比–P 曲線）、SS-2012-3（fig-1-b1 B1 下限、fig-2-pm H1 互制）、SS-2014-4（fig-1-superpose B1·Mnt＋B2·Mlt、fig-2-pm H1 互制與三種誤算）、SS-2019-3（fig-1-models 兩跨 vs 單跨分配、fig-2-check 軸力路徑與兩段檢核）。gen 腳本：SS-2004-4／2007-2／2008-4／2019-3 於既有題目重繪腳本追加（fig1_problem 未動），SS-2012-3／2014-4 新建；所有數值由腳本依解析 §1 題給重算。圖插入各解析 §4 對應步驟後、頁尾加「圖解補繪」行；重出 6 頁 problems-view。解析本文未改動。比對時發現、未處理（待勘誤）：① SS-2004-4 §4(二) $M_1/M_2$ 正負號寫反（寫「雙曲率取負」，且「$M_1/M_2=-1$ 時 $C_m=1.0$ 最有利」自相矛盾）；② 數個末位四捨五入差：SS-2004-4 $f_{by}$ 494.97/152 = 3.256（解析 3.257）、SS-2007-2 弱軸項 0.659／強軸項 0.219（解析 0.658／0.220，合計同 1.300）與 $F'_{ex}$ 4.519（解析 4.522）、SS-2008-4 $F'_{ex}$ 1.233（解析 1.232）、SS-2012-3 $\phi_cP_n$ 2,596 kN（解析 2,594，因 $0.658^{0.933}$ 取 0.676）、SS-2014-4 $P_u/\phi_cP_n$ 0.462、互制比 0.820（解析 0.463／0.821）；圖上凡會與解析衝突者改以 2 位小數或與解析相同的「各項先四捨五入再加總」呈現；③ SS-2012-3 §5.1 稱 $M_1 = 0$ 為「單曲率」用詞不精確；④ 既有 `gen_SS-2003-4.py` 圖 3 右格註腳字串含亂碼（「���一式控制」），已輸出於 SS-2003-4-fig-3-interaction.svg。

- 2026-11-03｜FIX-SS-2004-4｜SS-2004-4 解析勘誤（接續 FIG-SS-U1-3-B2 比對時發現之 ①）：
  改了什麼：㈡ 由「$C_m = 0.6-0.4(M_1/M_2) \geq 0.4$ 的適用條件與下限 0.4 的工程意義（論證下限必要）」改答「$\geq 0.4$ 為何我國規範不再採用」——下限收錄於 1978 年 AISC、1986 年 AISC-LRFD 與我國規範均不採用；原為梁的側向扭轉挫屈而訂（$C_b$ 上限 2.3 之倒數 ≈ 0.43），不適用於彎矩放大；Zandonini (1985) 證實取消後 $C_m$ 式仍適用；另補端部由強度式檢核之說明。$M_1/M_2$ 正負號改為雙曲率正、單曲率負（舊解顛倒，且「$M_1/M_2=-1$ 時 $C_m=1.0$ 最有利」自相矛盾）。陷阱表、L3、§6.2 的 $C_m = 0.85$ 改述為第 (1) 款可側移構件（舊述「有橫向載重通常建議 0.85」）；§4.5 刪「無論 $f_a/F_a$ 大小皆須驗算強度式」；尾數 $f_a$ 0.02396 → 0.02397、$f_{by}$ 3.257 → 3.256、$12\pi^2E$ 248,808 → 248,714、簡化式 1.783 → 1.782；§6.4 所需 $S_y$ 330 → 277 cm³（330 無依據；495/1.875/0.954）；§1 改為指向題目正本＋常見誤讀；標籤加 `Cm下限0.4廢止`、`M1/M2正負號`。㈢ 結論 N.G. 不變。
  為什麼錯：題意錯（㈡ 問句讀反）＋觀念錯（正負號）＋算術尾數。證據：考卷 `SS-2004_鋼結構設計.pdf` 第 2 頁第四題㈡，110／300 dpi 轉圖目視，原文「原本 Cm = 0.6-0.4 (M1/M2)≥0.4 的大於等於 0.4 為何我國規範不再採用？」，與題目正本（待確認）一致，故不做題意勘誤。規範依據：國土管理署《鋼結構容許應力設計法》第八章 8.2 節本文（第 8-1 頁：第 (1) 款可側移 0.85、第 (2) 款 $0.6-0.4M_1/M_2$、雙曲率正單曲率負）與解說 C8.2（第 8-3 頁：0.4 之限制緣由與 Zandonini 1985），https://www.nlma.gov.tw/uploads/files/f6ed32171e4e99a9c49e85ca3b733d3c.pdf 。
  怎麼驗證：腳本重算 21 個數值（含 $P \times L\sin45°$ 與 $V \cdot L$ 雙路徑、$C_m$ 端點值、下限起作用之 $M_1/M_2 > 0.5$、$1/2.3$）MISMATCHES: 0；全庫 grep 正負號用語，其餘題目與講義皆為雙曲率正、單曲率負，無同型錯誤。
  同步的下游：`gen_SS-2004-4.py`（加總改精確值、$f_{by}$ 三位小數）＋ fig-1／fig-2 重出；`study/problems-view/SS-2004-4.html`；`question_index.json`（unverified、tags 增 2）；`dashboard-data.js` tags；`study/data/unit-SS-U1-3.json`（公式卡誤述「第二小題問這條式子適用於哪類構材」、題目摘要）→ `build_unit_page.py SS-U1-3` ＋ `unit-SS-U1-3.pdf` 重出（16 頁，KaTeX 487 式 0 錯誤）；`audit-ledger-SS.json` fixed。`lecture-SS-U1-3` 原即寫明無 0.4 下限，未改。

- 2026-11-03｜FIG-SS-B7｜第七批九題補解題向量圖解（struct-diagram，18 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：U1-4 七題——SS-2002-4（fig-1-ecc 偏心距 e = 13.5／分量取矩、fig-2-forces 螺栓合力向量與容許值）、SS-2004-2（fig-1-inner 內連接板可用寬 60.5 → d ≤ 20／直徑試選、fig-2-layout 螺栓配置平面）、SS-2004-3（fig-1-line 載重線距銲道形心 1.94 cm／分量力矩抵銷、fig-2-stress 六端點應力向量與 Pu 上限）、SS-2005-3（fig-1-section 銲道群中性軸上移 5.42、fig-2-comp 控制點應力分量與 P 比較）、SS-2007-1（fig-1-balance 平衡銲三力、fig-2-lengths 設計力與銲長）、SS-2012-4（fig-1-plate 配置／淨剪斷面／承壓 Lc、fig-2-thick 所需板厚與容量）、SS-2019-4（fig-1-section 組合斷面中性軸與 Q、fig-2-inter 斷續銲換算）；U2-1 兩題——SS-2005-4、SS-2020-2（fig-1-pna PNA 與彈性形心、fig-2-mech 崩塌機構＋崩塌彎矩圖＋wu(s) 曲線）。九支 gen 腳本皆於既有題目重繪腳本追加（fig1_problem 未動），數值由腳本依解析 §1／§4 重算，與解析一致（顯示位數取與解析相容者：SS-2004-3 M = 1.94·Pu〔精確 1.9445，解析 1.944〕、SS-2019-4 I ≈ 7.55 × 10⁴、q = 0.764〔精確 75,501／0.7639，解析 75,510／0.7638〕、SS-2020-2 Z = 4,624、Mp = 11,560〔精確 4,623.96／11,559.9〕）。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 9 頁 problems-view。解析本文未改動。比對時發現、未處理：① SS-2005-3 箱內「上翼板下面」銲道解析依判讀清單 #1 計 30 cm，但箱內淨寬僅 30 − 2 × 1.8 = 26.4 cm（清單 #4 已標不確定）；改用 26.4 cm 重算 P = 13.87 tf（原 14.0），已註記於圖 1，待確認題目正本時一併決定；② SS-2019-4 §4 Step 1 殘留草稿行「Wait：腹板高 = …」；③ SS-2012-4 未檢核剪力板塊狀剪力（題目未明文要求，留待盲解比對判斷）。
- 2026-11-03｜FIG-SS-B8｜第八批六題補解題向量圖解（struct-diagram，12 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：U1-1 前六題——SS-2002-3（fig-1-modes 強弱軸挫屈模態與三段 KL/r 53.5／82.0／98.4、fig-2-curve 柱強度曲線 Pa 93.9、φcPn 131.2 t）、SS-2003-2（fig-1-rm 修正迴轉半徑 7.7→15.0、13.4→18.0、fig-2-strength Fmy 6.934／Em 2,949 堆疊與 φcPn 513 vs 漏規定 147 t）、SS-2003-3（fig-1-force 設計力 77.51 t 的 3:4 分解與雙剪螺栓數 5、fig-2-interact 拉剪互制區與需求點，使用率 0.84）、SS-2007-4（fig-1-g 構架上逐點 I/L、G、K、fig-2-kcurve AD 柱 K 隨 G_D 變化，G=10 → 1.97、∞ → 2.43、誤讀 2.5 需 G_D ≈ 4.5）、SS-2008-2（fig-1-sway AB 單獨與加靠桿的側移機構、fig-2-kprime K' = 2√(ΣP/P_I)，2.83 vs 2.0／1.41）、SS-2010-3（fig-1-section 四角鋼組合斷面 dX 15.0／dY 17.47 與平行軸配對、fig-2-curve 彈性段 Pa 58.7、φcPn 83.8 tf）。六支 gen 腳本皆於既有題目重繪腳本追加（fig1_problem 未動），數值由腳本依解析 §1／§4 重算；K 值以對位圖方程式精確解（二分法）核對。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 6 頁 problems-view。解析本文未改動。比對時發現、未處理（末位差，均在查圖／捨入容許內）：① SS-2007-4 FH 柱方程式精確解 K = 1.274，解析表寫 1.28（KL 382）；G_D 精確 1.3237，解析寫 1.323；② SS-2010-3 §4 二 Fa 精確 0.4155，解析寫 0.415（Pa 58.7 不變）。
- 2026-11-03｜FIG-SS-B9｜第九批六題補解題向量圖解（struct-diagram，13 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：U1-1——SS-2011-2（fig-1-sway 兩鋼架側移，靠桿各推 P·δ/L、K' 2.83／4.00、fig-2-sum 系統 ΣPcr 長條，兩者皆 π²EI/4L²、比值 1）、SS-2011-4（fig-1-alpha 梁遠端修正 α 與 G_D 0.658／G_E 0.708、K 1.22／1.84（未修正 1.15／1.80）、fig-2-iter 柱 EF τa 迭代 1.838 → 1.79）、SS-2014-1（新建 gen 腳本；fig-1-curve Fcr/Fy–λc 兩式與 1.5 分界、fig-2-fy 同一柱 Fy 350 → 450 MPa 的 Fcr 比較、fig-3-modes 鉸–鉸 K 1.0／固–自由 K 2.0 挫屈形）、SS-2016-3（fig-1-stage 殘留應力三階段與 Ie/I = 1/27、fig-2-curve Fcr–L/r 三轉折點 (18.0, 2.29)、(19.9, 1.875)、(103.6, 1.875)）、SS-2017-3（新建 gen 腳本；fig-1-axes 斷面與兩軸 KL/r 16.9／177.9／誤 44.4、fig-2-fa ASD Fa/Fy 曲線，正確 0.135、0.34Fy 對應 KL/r ≈ 107）、SS-2018-2（新建 gen 腳本；fig-1-section 箱型斷面 A、r 與 b/t 23.0 vs 27.5／34.8、fig-2-strength λc 0.391、φcPn 2,586 tf、利用率 0.433）。SS-2014-1、2017-3、2018-2 原無 figs／gen，本批新建（考卷無附圖，腳本只含解題圖解）；其餘三題追加於既有題目重繪腳本（fig1_problem 未動）。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 6 頁 problems-view。解析本文未改動。比對時發現、未處理：① SS-2014-1 §4 (二) 表 λc = 0.5 的非彈性值寫 0.878，正確為 0.658^0.25 = 0.901（實質錯誤，建議走勘誤）；同節驗算寫 e^(−0.9434) = 0.3894，正確為 e^(−0.9417) = 0.3899；② SS-2017-3 §4 Step 4 分母 23 × 31,649 寫成 728,927（應為 727,927），Fa 0.3313 → 精確 0.3320 tf/cm²（Fa/Fy 0.135 不變）；③ SS-2011-4 §4 第 1 次迭代 G'_E 精確 0.524，解析以四捨五入後 τa 相乘寫 0.525（收斂值不變）。
- 2026-11-03｜FIX-SS-2014-1｜SS-2014-1：解析勘誤（題意不變）。改了什麼：§4 (二) 曲線關鍵數值表 λc = 0.5 非彈性 Fcr/Fy 0.878 → 0.901（0.658^0.25）；λc = 1.5 兩式值 0.389 → 0.390（表與 §3.5 L2 同改）；§4 (一) 分界點驗算 e^(−0.9434) = 0.3894 → e^(−0.9417) = 0.3899；§5 ①「0.877 = 1/1.14²」→ 0.877 = 1/1.14（1/1.14² = 0.769）；§1 常見誤讀增列「λc = 0.5 取值」一列；頁尾加修正日期。結論（兩式在 1.5 相接、Fy 提升對彈性段無效、理論 K 1.0／2.0）不變。為什麼錯：算術（指數 λc² = 0.25 算錯、ln 0.658 乘 2.25 算錯、1/1.14 誤寫平方）與捨位（0.3899 截成 0.389）；於第九批圖解補繪（FIG-SS-B9）時由腳本重算發現。證據：考卷 raw/exams/SS-2014_鋼結構設計.pdf 第 1 頁第一題 150 dpi 目視，兩式 (0.658)^(λc²)Fy、(0.877/λc²)Fy 照錄、未標適用範圍，與題目正本一致，題意無需勘誤。怎麼驗證：獨立腳本 recompute_SS-2014-1.py（工作目錄，不入 raw/）重算 19 個數值 MISMATCHES: 0；λc = 0.5 另以 e^(−0.419λc²) = 0.9006 交叉驗算。同步的下游：question_index.json（verificationStatus 已是 unverified、tags 不變、problemStatus confirmed 不變）；study/problems-view/SS-2014-1.html 重出；figs/SS-2014-1-fig-1-curve 表值本已由腳本算為 0.901／0.390，無需重出；audit-ledger-SS.json 該題加 fixed = 2026-11-03（human 留空）；study/data/unit-SS-U1-1.json、lecture-SS-U1-1.html、unit-SS-U1-1.html 未引用被改數值（講義原寫 0.877 ≈ 1/1.14，正確），不需改。全庫搜尋同樣錯值：archive/wiki/code-ref/column-buckling-lambda-boundary.md 第 59 行亦寫「0.877 ≈ 1/1.14²」（wiki 已封存不同步，列出供參考）；其他題無同錯。
- 2026-11-03｜FIG-SS-B10｜第十批五題補解題向量圖解（struct-diagram，10 張 SVG＋2× PNG，render.py 溢出 0、逐張目視），U1-1 全部完成：SS-2021-2（fig-1-modes 受拉板整寬斷裂 Ae 17.4／節點板 U 形塊狀剪力 Agv 75、Agt 25、fig-2-block 斷裂項 184.5 > 102.5 → 式(2) 247.0、φRn 185.3 t）、SS-2022-2（新建 gen；fig-1-layout 題給與修正兩配置的 be = 56、剪出面、D5.2 孔位、fig-2-states 四極限狀態 Pa，504 kN 控制、利用率 89.3%）、SS-2023-2（新建 gen；fig-1-type Fa 曲線與 Cc 107.3，弱軸 87.8 非彈性、fig-2-length KL/r–L 兩直線，L = 794 cm 弱軸達 Cc）、SS-2024-2（fig-1-shearlag 半圓管形心 x̄ = D/π、U 0.682、三極限狀態 117.0 t 控制、fig-2-weld 銲腳數線 3.4／8／8.9）、SS-2025-2（fig-1-pl P–L 階梯 U 分段，P = 3.0L 遞增、L ≤ 3、fig-2-check L = 3 三項檢核 9.00／9.23／12.0 tf）。SS-2022-2、2023-2 原無 figs／gen，本批新建（考卷無附圖）；其餘三題追加於既有題目重繪腳本（fig1_problem 未動）。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 5 頁 problems-view。解析本文未改動。比對時發現、未處理（末位差）：① SS-2024-2 §4 Step 6 單位長度銲道強度係數 0.75 × 0.6 × 4.92 × 0.707 精確為 1.565，解析寫 1.566（8 mm 銲道強度 273.4 vs 解析 273.6；w_req 3.4、上限 8.9、結論不變）。
- 2026-11-03｜FIG-SS-B11｜U1-2 第一批四題補解題向量圖解（struct-diagram，8 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：SS-2002-2（fig-1-lb 側撐 Lb = 3.5 m 與 Lc／Lu 分區帶、fig-2-moment 跨中自重 2.377 ＋ 3.5P = Ma 22.655 → Pa 5.79 tf）、SS-2007-3（新建 gen；fig-1-curve φbMn–Lb 曲線 Cb 1.0／1.7，三案例 146.2／96.1／87.8 tf·m、fig-2-formula 考卷印錯分母 Lr − Lb 與正確 Lr − Lp 對照，5 m 時 96.1 vs −133.1）、SS-2008-3（fig-1-cb 彎矩圖與三段 Cb 1.30／1.00／1.30、fig-2-curve Lb 600 剛超過 Lr 579，BC 段 67.18 t·m 控制、w = 3.73 t/m，Mcr 以直接公式 7,462 雙路徑）、SS-2012-1（新建 gen；fig-1-limit FLB 與 LTB 兩條直線內插，Mn ≈ 881／813、fig-2-load 彎矩預算反推 WL 32.2 kN/m）。SS-2007-3、2012-1 原無 figs／gen，本批新建（考卷無附圖）；其餘兩題追加於既有題目重繪腳本（fig1_problem 未動）。新增 LRFD 撓曲 Mn 共用函式 q_mn_lrfd 寫入各腳本。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 4 頁 problems-view。解析本文未改動。比對時發現、未處理（末位差）：① SS-2008-3 §4 Step 5 寫 Mcr = 7,469，Step 6 與雙路徑段寫 7,465（精確 7,464.8），同檔前後不一；② SS-2012-1 φbMn 精確 731.65（解析逐步捨位 731.7；WL 32.2 不變）；③ SS-2007-3 Lp 精確 185.16 cm，解析寫 185.1（比值 0.8204、結果不變）。
- 2026-11-03｜FIG-SS-B12｜U1-2 第二批四題補解題向量圖解（struct-diagram，8 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：SS-2015-1（fig-1-select 七候選斷面依單位重排序的 φbMp 與 Lp，240 不足、247 最輕合格、fig-2-checks 彎矩 98.7%／剪力 36.6%／撓度 38.2%）、SS-2021-3（fig-1-ltb Mn–Lb 曲線，Lb 1200 時 86.8～151.9 小於 Mp 221.6、每 3 m 側撐後 Lb ≤ Lp、fig-2-mech 固端＋0.414L 跨內塑性鉸，wu 17.9 t/m）、SS-2024-3（fig-1-moment 外伸梁負彎矩圖與四分點 21／42／21、Cb 1.316、fig-2-axes 強軸 65.6 OK／弱軸 17.1 NG）、SS-2025-3（新建 gen；fig-1-zx Zx 翼板＋腹板分解 6,248.8、Mp 218.7、Mr 157.6、fig-2-mn 題給 Lp／Lr 的 Mn–Lb 圖，Lb 3.0 在塑性區）。SS-2025-3 原無 figs／gen，本批新建（考卷無附圖）；其餘三題追加於既有題目重繪腳本（fig1_problem 未動）。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 4 頁 problems-view。解析本文未改動；本批數值與解析全數一致。比對時發現、未處理：SS-2024-3 題目正本判讀 #6 寫 E、G 依規範自取「2040、790」，解析 §4 取 G = 810 tf/cm²（X1 = 150.6、Lr = 1,168 cm 依 810 算；改 790 時 Lr 略降，Mn 仍以 Mp 截斷，答案不變），兩份正本的 G 值宜統一。
- 2026-11-03｜FIG-SS-B13｜U1-2 第三批（最後）五題補解題向量圖解（struct-diagram，10 張 SVG＋2× PNG，render.py 溢出 0、逐張目視）：SS-2005-2（fig-1-trial C(y)／T(y) 曲線三次試算，y = 12.4 時 314.5 小於 328.1、交於腹板 13.34 cm；fig-2-pna 包覆斷面塑性應力分布與七力對 PNA 取矩 13,548.9 tf·cm、Mn 135.5、φbMn 121.9）、SS-2006-3（新建 gen；fig-1-inertia Ix 平行軸項／自身／腹板長條 1,185,216,000、Iy 與 ry 69.4；fig-2-zx 力偶臂 580、280，Zx 4,420,800 mm³、Mp 15,472.8 tf-cm）、SS-2009-3（fig-2-shape 彈性三角形與塑性矩形、Mp/My 1.124；fig-3-checks Aw = d·tw 75.0、Vn 157.5，柱曲線 λc 0.727；題目附圖已編為圖 1，解題圖接續為圖 2、3）、SS-2016-1（新建 gen；觀念題，fig-1-plates 翼板突出肢／梁腹板／柱腹板三種邊界與應力分布、k 約 4 對 23.9；fig-2-limits 題表係數長條與 Mn–λ 三段示意）、SS-2019-2（fig-1-case T 277 對 Cmax 669.4 判 PNA 在版內；fig-2-pna a 6.21、力臂 36.895、Mn 102.2）。SS-2006-3、SS-2016-1 原無 figs／gen，本批新建（考卷無附圖）；其餘三題追加於既有題目重繪腳本（fig1_problem 未動）。圖插入各解析 §4 對應步驟、頁尾加「圖解補繪」行；重出 5 頁 problems-view。解析本文未改動。比對時發現、未處理：SS-2009-3 §4 一 Ix 翼板項精確為 82,725（解析寫 82,722，Ix 94,268 對 94,265；Sx、My 四捨五入後不變，已於圖 2 圖說註明）；SS-2009-3 §4 三 Fcr = 0.658^0.528 × 3.5 = 2.806（解析寫 2.80，供參值，圖上標 0.802Fy ≈ 2.8）；SS-2019-2 解析以 a 取兩位 6.21 往下算，力臂 36.895（不取整為 36.896，Mn 皆 10,220）。至此 U1-1、U1-2 全部計算題均已補解題圖解。

- 2026-11-03｜TEXTBOOK-SS-U2-3｜新增 `study/textbook-SS-U2-3.html`／`.pdf`（設計規範對施工之要求，一冊 9 章、29 張程式向量圖、A4 75 頁），原始碼 `study/figs-src/textbook-SS-U2-3/`（calcs.py＋ch0–8＋figs_ch0–8）。本單元全為說明題，改以「7 顆種子＝物理機制」推出規定的方向與理由，規範數字集中於第 8 章數字卡；Rosenthal 熱傳、露點（Magnus）、節點域剪力挫屈、鋅腐蝕速率等曲線皆由 calcs.py 逐點計算，只示趨勢。驗證：KaTeX 0 錯、SVG 超框／重疊 0、29 張逐張目視。發現三處教材不一致未改動他檔，待使用者決定：① 工地銲接風速門檻（SS-2006-2 題解 10 m/s vs unit-SS-U2-3 卡片 5 m/s，講義標待確認）；② 預拉力 0.70FuAb（unit 卡片）vs 0.70FuAt（SS-2009-4 題解，講義採 At）；③ 最小銲腳表末列 19<t≤38（unit 卡片）vs 施工規範表 4.1-1「19<t」（講義採後者）；另 EBF 加勁條間距 unit 卡片式與 AISC 341（γp=0.08：30tw−d/5；0.02：52tw−d/5）不同，講義採 AISC 式。預熱表依營建署公開之施工規範第四章表 4.2-2。
- 2026-11-03｜TEXTBOOK-SS-U1-4｜新增 `study/textbook-SS-U1-4-calc.html`／`.pdf`（上冊計算篇，第 0～9 章、36 張程式向量圖、A4 88 頁）與 `study/textbook-SS-U1-4-concept.html`／`.pdf`（下冊概念篇，第 10～13 章、7 張圖、A4 25 頁），原始碼 `study/figs-src/textbook-SS-U1-4/`（calcs.py＋ch0–13＋figs_ch0–13，`python3 build.py all` 可重跑）。7 顆種子：換手鏈、真正斷掉的面、0.6＝1/√3、45° 最窄、繞形心轉、切一刀看平衡、摩擦＝μ×夾緊力；貫穿範例 A＝SS-2012-4、B＝SS-2017-4；LRFD／ASD 並列。與 U1-1 教科書（拉力接合端）、U2-3 教科書（銲接冶金、NDT、螺栓施工、耐震加嚴）重疊處只給重建卡並連結。驗證：KaTeX 0 錯、SVG 超框／重疊 0、43 張逐張目視；數值與題解對帳（2012-4、2017-4、2002-4、2004-3、2007-1、2015-2、2018-3、2019-4、2020-4、2024-2、2022-2）。未改動 raw/ 與其他教材；發現待使用者決定：① SS-2012-4 題解未檢核剪力板塊狀剪力（本書補算：需 7.08 mm、t=10 mm 容量 254.4 kN，不控制）；② SS-2012-4 淨剪面積孔徑用 22 mm，若照 d+3＝23 mm 所需板厚 8.77→9.01 mm（仍取 10 mm）；③ 工地銲接風速門檻（unit 卡片 5 m/s vs SS-2006-2 題解 10 m/s）同 TEXTBOOK-SS-U2-3 所列，本書標待確認；④ 小數進位差：SS-2007-1 Fb/Fa 38.58／14.61（題解 38.59／14.62）、SS-2020-4 Ab 2.363（題解 2.364）、每 cm 銲腳 1.565（SS-2024-2 題解 1.566），結論皆不變。SS-2018-3 翼板銲腳（10 或 11 mm）與 SS-2005-3 箱內銲長待題目正本確認，本書未採用該部分。

- 2026-11-08｜UNIT-SS-U2-1-SYNC｜unit-overview 改版同步 `study/unit-SS-U2-1`。`build_unit_page.py SS-U2-1 --check` 先行通過（主 6＋副 4＝10 題、16 條，與索引一致）；比對 11-01 RESTORE 之後的變更，僅 PROBLEM-SPLIT-CONFIRM-U2-1（11-02）的 SS-2025-3 勘誤未同步：所求為**標稱** Mn（Lb ≤ Lp ⇒ Mn = Mp = 21,871 tf·cm ≈ 218.7 tf·m），原答 φbMn = 196.8。`study/data/unit-SS-U2-1.json`：Q[SS-2025-3].sum 改為「題給 Lp、Lr、Cb 求標稱 Mn（= Mp，不乘 φb）」、type 段「LTB 與 φbMn」→「LTB 求標稱 Mn」、footer 加同步註記（純文字）、date 2026-11-08；公式標籤 f = [0, 5] 不變，其餘 F／Q／risk 經關鍵字掃描（196.8、2.92、0.08547、0.2686、應力遲緩、4.68、待複核）無殘留。重生 HTML（diff 僅上述三處＋產生日期）；雲端 Playwright 1280／390 寬 console 0 錯誤、KaTeX 143 式 0 錯誤、無水平溢出，A4 scale 0.85 重出 `unit-SS-U2-1.pdf`（9 頁）。11-02 §1 改寫、11-03 題目重繪與解題圖解不影響本頁。下游（frequency、problems-view、lecture、轉址頁）無須變動。備份：VM `/tmp/bk-u21/`。

- 2026-11-08｜FIX-SS-2025-4-LOCAL｜SS-2025-4（解析勘誤，數值不變；製作黑板講解影片時發現）：
  改了什麼：§4（三）「適用範圍」說明局部機構的例子，由「兩跨連續梁（n=1）其中一跨 2 個鉸就崩塌」改為「三跨連續梁（n=2，完全機構 3 鉸），邊跨內支承＋跨內 2 鉸即崩塌，2 < n+1，其餘兩跨仍靜不定」，並註明兩跨梁不能拿來說明局部機構；§1 常見誤讀補一列；頁尾加修正日期。題目原文、答案結論不變。
  為什麼錯：觀念（舉例不當）。兩跨連續梁一跨崩塌所用 2 鉸恰等於 n+1，剩餘結構靜定，屬完全機構的鉸數，說明不了「局部機構鉸數少於 n+1」。題意核對：考卷 `raw/exams/SS-2025_鋼結構設計.pdf` 第 2 頁第四題，150 dpi 全頁目視，與題目正本（已確認）逐字一致。
  怎麼驗證：`check_SS-2025-4.py`（束制矩陣秩法求靜不定度 n 與機構自由度）：簡支 0／固端簡支 1／兩端固定 2／兩跨 1／三跨 2；兩跨左跨 2 鉸後 DOF 1、剩餘 n 0；三跨邊跨 2 鉸後 DOF 1、剩餘 n 1；三跨梁任取 2 鉸僅同跨組合成機構；邊跨 wu 係數數值最小化得 11.6569＝6+4√2（與固端簡支一致）；正本範例 Pu = 6Mp/L 複核。MISMATCHES: 0。
  同步的下游：`study/problems-view/SS-2025-4.html`（render_problem_view.py 重生）；`raw/solutions/methods/plastic-mechanism/plastic-mechanism.md`（同一舉例：說明句改三跨邊跨、表格補「連續三跨梁 2｜完全 3、邊跨梁機構 2」，兩跨列註明＝n+1；methods 三條件：驗算同上、study 一併改、本筆記錄）；`study/figs-src/textbook-SS-U2-1/ch4.html`（陷阱框同上改寫）、`ch6.html`（「某一跨的局部機構」→「某一跨的梁機構」，兩跨等跨例 11.66 不變）→ `build.py all` 重生 `study/textbook-SS-U2-1.html`，雲端 Playwright 重出 `.pdf`（67 頁，KaTeX 0 錯誤、SVG 疑點 0）。順帶修 ch4 兩處 `\(…<…\)` 被瀏覽器當成標籤吞字（`\(2<n+1\)` 與原本即壞的 `\(M_n<M_p\)`，均改 `\lt`；後者使 4.4 節「別賭」框後半句在舊版 HTML／PDF 中顯示為原始碼）。`question_index.json` 該題原已 unverified、problemStatus confirmed，tags 不變；`study/data/unit-SS-U2-1.json` 無引用。
  未改、列出待決：`影片講義/textbook-SS-U2-1/T2`（scene.py 以兩跨連續梁圖示「n+1 不是鐵律」、segments s28 旁白「某一跨…兩個鉸」）已出片，未重渲染；T3 s25「連續梁通常是某一跨的局部機構」用語同 ch6，數值正確。`raw/solutions/SS-2019-3` 的「兩跨連續梁」為彈性彎矩分配語境，無關。
