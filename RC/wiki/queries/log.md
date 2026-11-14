# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## 2026-05-29

- **[INIT]** 從 exam-wiki-SS 克隆，全面改寫為 RC 科目（鋼筋混凝土設計與預力）
  - 改寫 CLAUDE.md（身份層）、CLAUDE-SOLVE.md（解題規範）、CLAUDE-SPEC.md（命名規格）
  - 改寫 CLAUDE-CODE.md（Runbook）、README.md（導覽）
  - 重建 wiki/index.md（RC 七層架構）、wiki/by-year.md（2002–2025 空白表格）
  - 重建 raw/json/question_index.json（空白索引）、concepts.json（RC 核心概念）
  - 科目代碼：RC｜題目編號格式：RC-YYYY-N

## 2026-06-07

- **[INGEST-BATCH]** 批次 ingest 94 題（所有 verificationStatus=verified 且 hasSolution=true）
  - 生成 wiki/problems/ 共 94 個頁面
  - 重建 wiki/index.md（依 RC-UN-n 分類，含題目連結表格）
  - 重建 wiki/by-year.md（2002–2025 年，含題號連結）
  - 涵蓋年份：2002–2025

## 2026-06-07

- **[COMPILE-ALL]** 完整重新編譯 wiki 知識庫
  - 生成 wiki/concepts/：10 個概念頁面
  - 生成 wiki/methods/：4 個解題方法論頁面
  - 確認 wiki/queries/ 存在
  - 建立 wiki/philosophy/index.md
  - wiki/problems/（94題）已於本日批次 ingest 完成
  - 未覆蓋：diagnosis/ · failure-modes/ · materials/ · code-ref/（Cowork 直接維護）

## 2026-06-07

- **[LINT-FIX]** 修復全部 7 項 lint 問題：
  - 概念頁補充：DUCTILE-FAILURE, LONG-COLUMN-MOMENT-MAGNIFIER, LONG-TERM-DEFLECTION, CREEP-SHRINKAGE, SPECIAL-MOMENT-FRAME-BEAM, SPECIAL-MOMENT-FRAME-COLUMN（6 頁）
  - 圖說補充：RC-2024-4-fig-1、RC-2025-3-fig-1（圖說缺漏）；RC-2023-4 加入 eqn-1.png 引用與 LaTeX 圖說
  - diagnosis/ 建立：beam-flexure, column-pm, shear-torsion, prestress, deflection-crack（5 頁）
  - failure-modes/ 建立：flexure, shear, crushing, deflection, cracking（5 頁）
  - materials/ 建立：concrete-stress-strain, steel-yielding, creep-shrinkage, prestress-strand（4 頁）
  - P-M 互動圖生成：10 個柱設計題（RC-2002-2 等），更新 hasViz=true

## 2026-06-07

- **[CLEANUP]** 清除 SS 鋼結構殘留：186 個檔案（problems/98 + concepts/58 + methods/19 + traps/11）
- **[CONCEPTS]** concepts.json 新增 7 個高頻概念（SHEAR-STRENGTH、TORSION-DESIGN、PUNCHING-SHEAR、SEISMIC-DESIGN、DEVELOPMENT-LENGTH、DEFLECTION-CONTROL、CRACK-WIDTH）
- **[FIX]** RC-2012-2 verificationStatus 改回 unverified（hasSolution=false，狀態矛盾修正）
- **[QUERY]** 建立 wiki/queries/題庫缺口報告（2017整年缺失、RC-2016-3、RC-2012-2）

## 2026-06-07

- **[REINDEX+INGEST]** 題庫補齊，新增 6 題（RC-2012-2、RC-2016-3、RC-2017-1~4）
  - question_index.json：共 100 題（verified+hasSolution：100 題）
  - wiki/problems/：新增 6 個頁面
  - wiki/by-year.md、wiki/index.md：重建完成
  - 題庫缺口報告更新：無缺口

## 2026-06-07

- **[CLEANUP-2]** 清除 SS 殘留 56 個（code-ref/22、philosophy/10、diagnosis/8、failure-modes/5、materials/5、queries/6）
- **[REBUILD]** 重建各目錄 RC 版 index.md（6 個目錄）
- **[ADD]** 補建 wiki/diagnosis/seismic.md

## 2026-06-08

- **[COMPILE-ALL]** 全面重建 wiki 知識庫（compile-all + ingest 完整驗證）
  - 確認 wiki/concepts/：17 個概念頁面（BALANCED-REINFORCEMENT-RATIO 至 CRACK-WIDTH 全部存在）
  - 確認 wiki/problems/：100 個題目頁面（2002–2025 全部 verified 題目）
  - 重建 wiki/index.md：採七層知識架構 + 四單元分類導航格式，含全部 100 題連結
  - 確認 wiki/by-year.md：2002–2025 完整年份表格（無需修改）
  - **[NEW]** 建立 wiki/traps/：13 個陷阱頁面 + index.md（T形梁、φ值、耐震Ve、預力fps、預力損失、扭力門檻、衝剪、細長柱、平衡鋼筋比、雙筋梁壓力筋、梁柱接頭、剪力臨界斷面、有效慣性矩）
  - **[LINT]** 執行 16 項健檢，結果：11項PASS、2項WARNING、3項SKIP（需bash）；完整報告：wiki/queries/lint-report-2026-06-08.md
  - **[FIX-1]** 同步 STIRRUP-DESIGN 至 concepts.json（第 18 個概念）
  - **[FIX-2]** 建立 wiki/code-ref/ 實體頁面（ACI-318.md、CNS-1480.md、seismic-code.md），更新 index.md；code-ref 從 stub 升格為完整規範速查層
  - 操作者：Cowork

## 2026-06-09

- **[COMPILE-ALL]** 全面重建 wiki 知識庫（全部修正），compile-all 第二次完整執行
  - 全部 100 題 wiki/problems/ 頁面確認（2002–2025 年，100 題均 verified）
  - **[CONCEPTS]** 24 個概念頁面全部以 §7.2 完整格式重新生成：
    - BALANCED-REINFORCEMENT-RATIOã€WHITNEY-STRESS-BLOCKã€BETA1-FACTOR
    - PM-INTERACTION-DIAGRAMã€BALANCED-POINTã€EFFECTIVE-MOMENT-OF-INERTIA
    - CRACKING-MOMENTã€PRESTRESS-LOSSã€EFFECTIVE-PRESTRESSã€STRONG-COLUMN-WEAK-BEAM
    - SHEAR-STRENGTHã€TORSION-DESIGNã€PUNCHING-SHEARã€SEISMIC-DESIGN
    - DEVELOPMENT-LENGTHã€DEFLECTION-CONTROLã€CRACK-WIDTHã€STIRRUP-DESIGN
    - DUCTILE-FAILUREã€LONG-COLUMN-MOMENT-MAGNIFIERã€LONG-TERM-DEFLECTION
    - CREEP-SHRINKAGEã€SPECIAL-MOMENT-FRAME-BEAMã€SPECIAL-MOMENT-FRAME-COLUMN
  - 格式特徵：每頁含完整 LaTeX 公式（$$...$$）、定義段落、前置概念、相關概念、常見陷阱、出現題目表格
  - **[INDEX]** 重建 wiki/index.md：七層知識架構表 + 24 概念快速導覽表（依四單元分類）+ 全 100 題連結
  - **[BY-YEAR]** 重建 wiki/by-year.md：2002–2025 年全 100 題，改為 [[RC-YYYY-N]] Obsidian 連結格式
  - 操作者：Cowork

## 2026-06-09

- **[METHODS]** 建立 wiki/methods/ 完整解題方法論目錄（Layer 3）
  - 新建 index.md：列出 8 個方法論頁面
  - 新建 WHITNEY-STRESS-BLOCK-METHOD.md（等值矩形應力塊，RC-U1-1/U1-2）
  - 升級 PM-INTERACTION-DIAGRAM.md（原 stub → 完整版含 LaTeX 公式與出現題目表）
  - 新建 MOMENT-MAGNIFIER.md（長柱放大彎矩法，RC-U1-3）
  - 新建 EFFECTIVE-INERTIA.md（有效慣性矩撓度計算法，RC-U3-1）
  - 新建 PRESTRESS-LOSS-CALC.md（預力損失計算流程，RC-U4-3）
  - 新建 T-BEAM-ANALYSIS.md（T 形梁彎矩強度分析法，RC-U1-1）
  - 新建 FRICTION-LOSS-METHOD.md（摩擦損失計算法，RC-U4-3）
  - 新建 SEISMIC-CAPACITY-METHOD.md（耐震能力設計法，RC-U3-3）
  - 知識庫健康狀態：wiki/ 七層架構全部完整，無缺漏
  - 操作者：Cowork

## 2026-06-10

- **[FREQUENCY]** 執行 frequency 指令，生成 wiki/queries/frequency-20260610.md
  - 統計全 100 題（2002–2025）各 topicId 出現頻次（primary + secondary）
  - 結果：RC-U1-1=22、RC-U4-1=21、RC-U1-2=19、RC-U3-3=16、RC-U2-1=16
  - 操作者：Cowork

- **[PREDICT]** 執行 predict 指令，生成 wiki/queries/predict-2026-20260610.md
  - 基於頻次統計＋近年趨勢＋補考點分析推測 2026 高機率考題
  - 優先補考點：RC-U3-1（8 年未考）、RC-U4-3（7 年未考）、RC-U1-3（10 年未考）
  - 操作者：Cowork

- **[RAW-METHODS]** 補建 raw/solutions/methods/ 來源檔案（4 個方法論 .md）
  - 新建 raw/solutions/methods/effective-inertia-deflection/effective-inertia-deflection.md
  - 新建 raw/solutions/methods/moment-magnifier-method/moment-magnifier-method.md
  - 新建 raw/solutions/methods/prestress-loss-calculation/prestress-loss-calculation.md
  - 新建 raw/solutions/methods/pm-interaction-diagram/pm-interaction-diagram.md
  - 修正 raw/→wiki/ 單向資料流缺口，4 個 wiki/methods/ 頁面現有對應原始檔
  - 操作者：Cowork

- **[TRAPS-BACKLINKS]** 建立 traps↔problems 雙向連結
  - 讀取全部 13 個 wiki/traps/ 陷阱頁，建立完整 trap→problem 對應表
  - 在 52 個 wiki/problems/ 頁末尾加入「## 相關陷阱」反向連結區塊
  - 涵蓋陷阱：T-BEAM-EFFECTIVE-WIDTH、BALANCED-RATIO-BOUNDARY、PHI-FACTOR-TRANSITION、COMPRESSION-STEEL-YIELDING、SHEAR-CRITICAL-SECTION、TORSION-THRESHOLD、DEFLECTION-EFFECTIVE-INERTIA、PUNCHING-SHEAR-CRITICAL、SEISMIC-BEAM-VE、JOINT-SHEAR-EFFECTIVE-AREA、LONG-COLUMN-SLENDERNESS、PRESTRESS-LOSS-SEQUENCE、PRESTRESS-FPS-FORMULA
  - wiki/traps/ 雙向連結完整度：13/13 陷阱頁均建立反向連結
  - 操作者：Cowork

## 2026-06-11

- **[HEALTH-CHECK]** 知識庫一致性健檢（補完 2026-06-08 lint 報告的 4 項 SKIP 掃描）
  - hasViz 比對：索引 14 題 hasViz=true ↔ raw/solutions/ 實際 16 個 *-viz.html（RC-2014-2、RC-2014-4 各 2 個），完全一致 ✅
  - hasHandwritten 比對：索引 0 題 ↔ 實際 0 個 *hand*.png，一致 ✅
  - 圖說掃描：59 個含 fig-*.png 的解析檔全部具備「圖說：」段落 ✅
  - lint 待補清單覆核：code-ref 實體頁 ✅、STIRRUP-DESIGN 已入 concepts.json ✅、raw methods 來源 ✅（均已於 06-08~06-10 解決）
  - 結論：資料層無待修項
  - 操作者：Cowork

- **[DASHBOARD]** 建立知識庫儀表板（新增使用者入口）
  - 新建 index.html（離線單檔，雙擊即用）：題庫瀏覽（年份/單元/考點/設計法/標籤/關鍵字篩選）、考點統計圖、近5年走向、高頻標籤、讀書進度追蹤（localStorage）、七層架構導覽、16 指令速查
  - 新建 dashboard-data.js（question_index.json 快照，100 題）
  - 新增指令 REFRESH-DASHBOARD（觸發語句「更新儀表板資料」），登錄於 CLAUDE-CODE.md
  - 操作者：Cowork

- **[DASHBOARD-v2]** 儀表板新增站內解析閱讀器
  - 「完整解析」改於站內彈窗開啟：內建 Markdown 渲染器（標題/表格/清單/引用/程式碼區塊/圖片）＋ KaTeX 公式渲染（$...$ 與 $$...$$，CDN 載入、離線時顯示原始 LaTeX）
  - 因瀏覽器 file:// 安全限制，採 File System Access API：首次使用授權選擇 exam-wiki-RC 資料夾一次（儲存於 IndexedDB），即可讀取所有解析檔與附圖
  - 題目附圖以 Blob URL 載入；解析內 .md 相對連結可於閱讀器內跳轉
  - 移除題卡「wiki 題目頁」連結（依使用者要求）；知識庫導覽卡片也改走站內閱讀器
  - 操作者：Cowork

- **[DASHBOARD-v3]** 解析閱讀器新增「匯出 PDF」按鈕
  - 採瀏覽器原生列印管道（目的地選「另存為 PDF」）：向量文字、中文與 KaTeX 公式完整保留、離線可用
  - 列印樣式僅輸出解析內容＋標頭（題號、來源路徑、匯出日期）；表格/圖片/公式避免跨頁截斷
  - 匯出時自動以題號設定預設 PDF 檔名
  - 操作者：Cowork

- **[METHODS-CONSOLIDATION]** 整併 wiki/methods/ 雙命名體系（lint 後續優化）
  - 問題：methods/ 同時存在大寫頁（8 個，06-09 建立、index 引用、無 raw 來源）與 kebab 頁（3 個，06-10 raw 對應版），4 組內容重複；且多數大寫頁「出現題目」表與 question_index 不符（如 EFFECTIVE-INERTIA 原列 4 題中 3 題為剪力牆/預力/扭力題）
  - 整併為 8 個 kebab-case 方法頁（符合 CLAUDE-SPEC 命名規範）：whitney-stress-block-method、pm-interaction-diagram、moment-magnifier-method、t-beam-analysis、effective-inertia-deflection、seismic-capacity-method、prestress-loss-calculation、friction-loss-method
  - 所有「出現題目」表依 question_index.json 標籤重新核實重建
  - 補建 4 個 raw 來源：whitney-stress-block-method、t-beam-analysis、friction-loss-method、seismic-capacity-method；更新既有 4 個 raw 來源為完整版（與 wiki 頁同步）
  - 重寫 wiki/methods/index.md（8 法索引）
  - MOMENT-MAGNIFIER.md、EFFECTIVE-INERTIA.md、PRESTRESS-LOSS-CALC.md 改為廢棄轉址 stub
  - 操作者：Cowork

- **[ARCHIVE]** raw/json/ 暫存檔歸檔至 study/_archive/
  - pdf_text.txt、pdf_2016_blocks.txt、pdf_2016_text.txt 已複製到 study/_archive/（附 README 說明）
  - 操作者：Cowork

- **[PENDING-DELETE]** 待刪除清單（沙箱環境因磁碟空間不足無法啟動，刪除作業暫緩）
  - raw/json/pdf_text.txt、raw/json/pdf_2016_blocks.txt、raw/json/pdf_2016_text.txt（已歸檔至 study/_archive/）
  - wiki/methods/MOMENT-MAGNIFIER.md、EFFECTIVE-INERTIA.md、PRESTRESS-LOSS-CALC.md（廢棄轉址 stub）
  - raw/solutions/RC-2015-1 ~ RC-2015-4 等資料夾內的 .placeholder 空檔
  - 檔名大小寫正規化：PM-INTERACTION-DIAGRAM.md → pm-interaction-diagram.md 等 5 檔（Windows 大小寫不敏感，連結已可解析，僅顯示名稱待改）
  - 環境恢復後對 Cowork 說「清理待刪除檔案」即可執行
  - 操作者：Cowork
- [2026-06-29] ingest RC-2023-1: �ɥR PDF �P��s��ı�ƹϪ�

## 2026-07-01

- **[DASHBOARD-v4]** 考點統計頁籤改為 frequency 指令格式；補充筆記 PDF 改為靜態資料驅動
  - 「考點統計」頁籤重寫為 frequency 指令輸出格式：高頻考點 Top10（主＋副）、各單元命題比例、近5年趨勢動態列表；移除原「設計法分布」與「高頻標籤 Top20」兩張卡片
  - dashboard-data.js 資料格式新增第 7 個欄位 pdf（補充筆記檔名陣列）；index.html 移除「📎 掃描補充 PDF」按鈕與前端即時掃描機制（injectPdfButtons/pdfCache/listDir），改為依靜態資料直接顯示「📎 補充筆記 PDF」按鈕
  - 同步更新 CLAUDE-CODE.md（REFRESH-DASHBOARD 規格）、CLAUDE-SPEC.md（補充筆記 PDF 說明）、CLAUDE.md（CHANGELOG）
  - 操作者：Cowork

- **[REFRESH-DASHBOARD]** 重新生成 dashboard-data.js
  - 掃描 raw/json/question_index.json：100 題（無變動）
  - 掃描 raw/solutions/RC-*/*-viz.html：18 個互動圖檔（無變動，維持既有 15 題的 viz 對應）
  - 掃描 raw/solutions/RC-*/*.pdf：新發現 RC-2023-1 資料夾下 2 個補充 PDF（RC-2023-1.pdf、RC-2023-1_補充.pdf），已寫入 dashboard-data.js pdf 欄位；其餘 99 題維持 []
  - 核對 raw/json/syllabus_taxonomy.json（RC 分類樹）：window.RC_TOPICS／window.RC_UNITS 內容一致，無需更動
  - 操作者：Cowork

## 2026-07-10 STUDY（子項層級 ×5）

- 指令：`study RC-U1-1`、`study RC-U1-2`、`study RC-U2-1`、`study RC-U3-3`、`study RC-U4-1`
- 產出（七區塊互動 HTML，KaTeX 渲染、自含檔案）：
  - study/study-RC-U1-1.html — 梁彎矩強度分析與設計（主 19 題／相關 22 題，排名 1，近6年 5/6）
  - study/study-RC-U1-2.html — 柱強度分析與設計（主 12／相關 20，排名 4，近6年 3/6）
  - study/study-RC-U2-1.html — 剪力強度分析與設計（主 7／相關 16，排名 6，近6年 5/6）
  - study/study-RC-U3-3.html — 韌性要求與耐震設計（主 16／相關 18，排名 2，近6年 2/6）
  - study/study-RC-U4-1.html — 預力梁斷面應力分析（主 13／相關 21，排名 3，近6年 5/6）
- 資料來源：raw/json/question_index.json（100 題，2002–2025，全數 verified）
- 考題連結格式：`../index.html#md=raw/solutions/RC-YYYY-N/RC-YYYY-N.md&t=RC-YYYY-N`（符合 CLAUDE-CODE.md STUDY 規格）
- 驗證：五頁題數與索引一致（22/20/16/18/21）、題號全數存在且相關、JS 語法檢查通過（node --check）
- 互動計算器：U1-1 矩形梁 φMn／U1-2 柱 P-M 強度點／U2-1 梁剪力檢核／U3-3 圍束箍筋 Ash／U4-1 預力梁兩階段應力
- 操作者：Cowork

## 2026-07-19

- **[UI-UPDATE]** 於 `study/` 目錄下的 5 個 `study-RC-U*.html` 主題總覽區塊右側，新增「Keynote」按鈕，並分別連結至對應的 PDF 講義檔案。
- 操作者：Cowork

## 2026-07-25 UNIT-LECTURE（RC-U1-1 觀念講義）

- 觸發：`生成 RC-U1-1 講義`（外部 `unit-lecture` skill，非本知識庫 16 指令之一）
- 產出：
  - `study/lecture-RC-U1-1.html` — 理解導向觀念講義，13 節（§0 全景 → §12 精選 5 題），10 張內嵌 SVG 圖解
  - `study/lecture-RC-U1-1.pdf` — 21 頁 A4 可列印版（MathJax→SVG + WeasyPrint）
  - `study/assets/katex/` — 離線 KaTeX（約 600 KB），本科所有 lecture 頁共用，勿刪
- 定位：與 `study/study-RC-U1-1.html`（速查頁）**並存不覆蓋**；速查頁供練題時查，講義供練題前建立物理直覺
- 內容主軸：核心對立「強度＝力的平衡／安全＝應變的幾何」；每個規範常數追來源
  （0.85 ← Rüsch 持續載重效應；β₁=2k₂ ← 應力分布形心；6120 ← εcu·Es；3/7 ← 0.003/0.007；ρmin 的 √f'c ← 破裂模數 fr=2√f'c）
- 涵蓋題數：19 主分類 + 3 副分類 = 22 題（2002–2024），全數 verified
- 精選 5 題：RC-2023-2、RC-2011-2、RC-2007-1、RC-2015-2、RC-2016-1
  （誠實標註未涵蓋：RC-2014-1 過筋梁、RC-2014-2 M-φ 三階段、RC-2015-3 負彎矩 T 形梁、RC-2022-2 材料經濟性）
- 考題連結格式：`../index.html#md=raw/solutions/RC-YYYY-N/RC-YYYY-N.md&t=RC-YYYY-N`（同 STUDY 規格）
- 驗證：22 題號與 question_index.json 完全對齊（無缺漏／誤植／年份錯誤，解析檔皆存在）；
  29 項數值以 Python 重算吻合（β₁ 分段、φ 內插、ρb/ρmax/ρmin 比值、RC-2023-1 曲率延展比算例 μφ=3.61→4.96）；
  PDF 抽查 9 頁確認無 MathJax 黑方框、SVG 文字無溢出；節號交叉引用完整
- 連動修改：README.md（快速導航＋檔案地圖）、CLAUDE.md（資料夾結構＋CHANGELOG）、
  檔案架構索引表.md（study/ 與 assets/ 兩列）、CLAUDE-CODE.md（STUDY 段落加交叉註記，未新增指令）、
  study/study-RC-U1-1.html（新增「觀念講義」按鈕）
- 操作者：Cowork
- 2026-07-25｜FIX｜**單位係數勘誤（跨科稽核發現）**。於 exam-wiki-SS 修正一批公式單位錯誤後，回頭稽核六科知識庫，在 RC 發現兩處：
  1. `wiki/code-ref/CNS-1480.md` §混凝土彈性模數：`Ec = 4270√f'c (kgf/cm²) ≈ 15100√f'c (MPa)` —— **兩個單位標籤對調**，且 kgf/cm² 制係數誤植為 4270。正確為 `Ec = 15100√f'c (kgf/cm²) = 4700√f'c (MPa)`。原式誤差達 3.2～3.5 倍，會直接毀掉撓度與轉換斷面計算。已改正並加入驗算示例（f'c=280 kgf/cm² 時兩制應同得約 25 萬 kgf/cm²）與記憶法（係數大的配單位小的）。
  2. `f_r` 的 MPa 制係數不一致：`wiki/code-ref/CNS-1480.md` 與驗證解答 RC-2018-4 均為 `0.623√f'c`，但 `wiki/concepts/GLOSSARY.md`、`wiki/traps/DEFLECTION-EFFECTIVE-INERTIA.md`、`wiki/methods/effective-inertia-deflection.md` 寫成 `0.7√f'c`（差 12%；0.7 為 ACI 318-99 舊版值）。依規則 2 以驗證解答為準，已將 GLOSSARY 與 traps 兩檔改為 0.623。
  驗算方式：以 f'c = 280 kgf/cm² = 27.5 MPa 雙制互換確認；fr 以 2.0√f'c(kgf/cm²) 為錨點換算得 0.626 ≈ 0.623。
  ⚠️ **未完成**：`wiki/methods/effective-inertia-deflection.md` 的 `0.7` 尚未修正，因其 compile 來源在 `raw/solutions/methods/effective-inertia-deflection/`，而 RC 的規則 1 目前尚未開放 methods 例外（SS 已於同日開放）。待決定是否比照 SS 修改 RC 的 CLAUDE.md 規則 1。
  同時確認：SS 的 ASD/LTB 係數錯誤（703,000 / 1,170,000 / 1,055,000、Lp=300ry、Lr 分母、λ 138/322）**未擴散**至 RC/SA/SD/SM/MM 任一科（該類公式為鋼結構專有）。
- 2026-07-25｜HARNESS + FIX｜規則 1 例外擴充（比照 SS）：`raw/` 唯讀例外增列 `raw/solutions/methods/`，並訂三項條件（驗算／同步 wiki／記 log）；`CLAUDE.md`（規則 1、結構圖 🔒/✏️ 標記、單向資料流、CHANGELOG）與 `CLAUDE-CODE.md`（新增 FIX-METHOD 流程）同步更新。依此完成前一筆待辦：`raw/solutions/methods/effective-inertia-deflection/` 的 `f_r = 0.7√f'c (MPa)` 已改為 `0.623√f'c` 並同步覆蓋 `wiki/methods/`。至此 RC 全庫 6 處 f_r 定義一致（0.623），與驗證解答 RC-2018-4 相符。
- 2026-07-26｜FIX｜**梁柱接頭 γ 係數全庫勘誤（8 檔 15 處）**：撰寫 RC-U3-3 觀念講義時發現全庫對 `φVn = φγ√f'c·Aj` 的 γ 存在**三套互相矛盾**的數字。
  **錯在哪：**
  1. `wiki/code-ref/ACI-318.md` §18.8.4.2、`wiki/code-ref/seismic-code.md`、`wiki/traps/JOINT-SHEAR-EFFECTIVE-AREA.md`：寫成 `1.0 / 0.75 / 0.50`（另加「僅一面有梁 0.30」）—— **不對應任何常用單位制**。
  2. `wiki/diagnosis/seismic.md`：寫成 `3.2（內）/ 2.4（邊）/ 1.6（角）` —— 數字**整組往下移了一階**；3.2 實為「其他類接頭」的值，被誤標為內接頭。
  3. `wiki/code-ref/CNS-1480.md`：把差異歸因於「舊 CNS/ACI-318-99 用 4.0/3.2/2.4 vs 新 ACI-318-08 用 1.0/0.75/0.50」—— **歸因錯誤**，差異來自單位制而非規範版本；且兩欄數字皆有誤。
  4. `wiki/philosophy/seismic-philosophy.md`：RC-2018-2 標為 `γ=1.6（外接頭）`（應為 3.2）；RC-2005-3 標為 `γ=3.2（內接頭筆誤需判斷）`（該題本就是**外／角接頭**，3.2 正確，原註解反而把正確值說成筆誤）。
  5. `raw/solutions/methods/seismic-capacity-method/` 與 `wiki/methods/SEISMIC-CAPACITY-METHOD.md`：`1.7 / 1.2 / 1.0` 數值接近正確（MPa 制）但**未標單位制**，且 1.2 應為 1.25 —— 正是全庫混淆的根源。
  **改成什麼：** 八個檔案統一改為三單位制對照表 —— 四面有梁（內接頭）`psi 20 / MPa 1.7 / kgf-cm² 5.3`；三面或對面兩面（T 形）`15 / 1.25 / 4.0`；其他（外／角接頭）`12 / 1.0 / 3.2`，並註明「同一組值的三種單位制，非三套規範」與「作答須寫明單位制」。
  **怎麼驗證的（依規則 2，以 verified 解答為錨點）：**
  - `wiki/problems/RC-2005-3.md`（verified）明載「角柱（外接頭）=3.2、T 形接頭=4.0、十字形（內接頭）=5.3」，並附推導 `γ = 12 psi^0.5 × 0.265 = 3.18 ≈ 3.2`。
  - `wiki/problems/RC-2003-3.md`（verified）明載「內部接頭四面有梁圍束，γ=5.3（kgf/cm² 制，對應 ACI psi 制之 20）」。
  - 量綱換算獨立重算：psi→kgf/cm² 乘 √0.0703 = 0.2651（20→5.303、15→3.977、12→3.182）；psi→MPa 乘 √0.006895 = 0.08304（20→1.661、15→1.246、12→0.996）。三組值互相自洽。
  - 註記：RC-2018-2 內柱寫 5.4 屬換算取捨（5.303 進位），已於表下說明，不視為衝突。
  **順帶修正（同檔同性質、同樣以 verified 解答驗證）：** `wiki/diagnosis/seismic.md` 柱密箍區間距的第三條件寫成固定 `14cm`，與 RC-2013-2、RC-2012-3 兩份 verified 解答所用 `so = 10+(35-hx)/3 ≤ 15cm` 不符，已改正。
  **規則遵循：** `code-ref/`、`diagnosis/` 屬規則 4 例外，可直接維護；`raw/solutions/methods/` 依規則 1 例外修改，已完成驗算＋同步覆蓋 `wiki/methods/`＋本筆紀錄三項條件。`traps/`、`philosophy/` 雖非規則 4 例外，但經核對 CLAUDE-CODE.md 的 COMPILE-ALL 步驟，其生成清單僅含 concepts/ · methods/ · problems/ · index.md · by-year.md，**不會重新生成 traps/ 與 philosophy/**（INGEST 僅更新 traps 的「出現題目」表格），故直接修正不會被蓋回，且其內容原本即與自身來源（verified 解答）矛盾。
  **未處理／待確認：** `wiki/diagnosis/seismic.md` 梁密箍區長度寫 `lo = max(2h, ln/4, 450mm)`，但 ACI 318 §18.6.4.1 與 RC-2025-2 verified 解析均為單一條件 `2h`；因不確定 `ln/4, 450mm` 是否引自其他規範（如中等抗彎構架），暫未更動，待使用者確認。
- 2026-07-26｜FIX｜**梁密箍區長度 lo 勘誤（承前一筆待確認事項，使用者裁示依 ACI 318 §18.6.4.1 修正）**：
  **錯在哪：** `wiki/diagnosis/seismic.md` 決策樹將特殊矩形框架梁的密箍區長度寫成 `lo = max(2h, ln/4, 450mm)（梁端）`。
  ACI 318 §18.6.4.1 對**梁**只有**單一條件**：自支承構材面向跨中量起 `2h`（h 為梁全高）；
  `ln/6`、`450mm` 是**柱**的規定（§18.7.5.1 `lo ≥ max(h, lu/6, 450mm)`），`ln/4` 則不屬於任一條。
  **改成什麼：** 改為 `lo = 2h（單一條件，自柱面量起）`，並加註「梁沒有 ln/6、ln/4 或 450mm，那是柱 §18.7.5.1」；
  同檔「常見陷阱」條目由籠統的「梁和柱的密箍區定義不同」改寫為明列兩者公式與條文號。
  **怎麼驗證的：** ① 條文對照 ACI 318 §18.6.4.1（梁）vs §18.7.5.1（柱）；
  ② 驗證解答 `RC-2025-2` 明載「密箍區：自柱面算起 2h」（單一條件）；
  ③ 反向核對柱題 `RC-2012-3`、`RC-2013-2`、`RC-2009-1` 三份 verified 解答，其 `max(..., lu/6, 45cm)` 三式取大**均為柱**，證實三條件屬柱而非梁。
  **全庫掃描結果：** 修正後全庫已無 `ln/4` 記載；`code-ref/ACI-318.md` §18.6.4.4、`code-ref/seismic-code.md`、
  `concepts/SPECIAL-MOMENT-FRAME-BEAM.md`、`methods/SEISMIC-CAPACITY-METHOD.md` 對梁均已正確寫為 `≥ 2h`，無須更動。
  **⚠️ 未更動（受規則 1、2 保護，僅記錄）：** `raw/solutions/RC-2016-2/RC-2016-2.md` 第 63／140／258／353 行寫
  `lo = max(2h, ln/6, 45cm)` 並標註「ACI 318-14 §18.6.4.1」—— 條文號與三條件不符（三條件應屬 §18.7.5.1 柱）。
  惟該題實算 `max(140, 125, 45) = 140 cm` 由 `2h` 控制，**最終答案 140 cm 不受影響**，
  依規則 2（verifiedSolution 為最終答案，不可質疑或重算）不予更動；其 ingest 副本 `wiki/problems/RC-2016-2.md` 亦同步保留原樣。
  若日後決定修訂該題敘述，須經使用者確認後再動 raw 端。
- 2026-07-26｜FIX｜**剪力臨界斷面「d 偏移」判準改寫為條件式（`wiki/traps/SHEAR-CRITICAL-SECTION.md`）**：
  **錯在哪：** 原頁把「倒 T 型梁」直接列入「不可使用此有利規定（必須取支承面）」清單，寫成**構件形狀 → 結論**。
  但唯一的證據來源 `RC-2020-2`（verified）判定該題倒 T 梁**可以**採 d 偏移，理由是「均佈載重施加於梁頂部（壓力側），並非自下翼板懸吊」，
  並附完整物理說明（「若載重從拉力側懸吊進入腹板，斜壓撐機制就不成立」）與實務註記。原頁敘述與自身來源矛盾。
  另原頁「可取 d 處」只列兩個條件（支承提供壓力、支承限制開裂），與 ACI 318 §9.4.3.2 的三條件不符（漏了「無集中載重」，且第二條非規範文字）。
  **改成什麼：**
  ① 「臨界斷面規則」段改以 ACI 318 §9.4.3.2 **三條件 (a)(b)(c)** 為主體（支承反力產生壓力／載重在頂面／區間內無集中載重），
     並加註「判準是條件，不是構件名稱」；原有的構件案例改列為「典型會違反哪一條」。
  ② 倒 T 型梁改為條件式：違反的是 (b)，且明確指出「同樣是倒 T 梁，載重在頂面則仍可用」。
  ③ 「梁端搭接接頭」非 §9.4.3.2 列舉條件，標示為**實務補充考量**，保留但要求採用時註明依據（未刪除原有內容）。
  ④ 常見陷阱表同步改寫；「出現題目」表補上 RC-2023-3。
  **⚠️ 同時揭露一項知識庫內部衝突（未判定、未更動任何 raw 內容）：**
  懸臂梁能否採 d 偏移，兩份 verified 解答處理**相反** ——
  `RC-2006-1` 取固定端面不折減（理由：固定端剪力最大、無斜壓桿效應）；
  `RC-2023-3` 取距固定端 d 處（理由：ACI 9.4.3.2 固定端反力向上、端區受壓，條件 (a) 成立）。
  依**規則 2**（verifiedSolution 為最終答案，不可質疑或重算），本次修改**不判定何者為準**，
  改為在 traps 頁與講義中並陳兩者及其理由，並提示作答時須寫出條件判斷過程。
  **此項若要收斂，須由使用者裁示；在裁示前 raw/solutions/ 兩題均維持原狀。**
  **怎麼驗證的：** ① 對照 ACI 318 §9.4.3.2 三條件；② 逐字核對 RC-2020-2、RC-2006-1、RC-2023-3 三份 verified 解答的原文理由；
  ③ 全庫掃描確認無其他檔案重複「倒 T 梁一律不可」的敘述。
  **規則遵循：** `traps/` 非規則 4 例外目錄，但經核對 CLAUDE-CODE.md，COMPILE-ALL 的生成清單僅含
  concepts/ · methods/ · problems/ · index.md · by-year.md（INGEST 僅更新 traps 頁的「出現題目」表格），
  **不會重新生成 traps/ 頁面本體**，故直接修正不會被蓋回。同步更新 `study/lecture-RC-U2-1.html` §4.1。
- 2026-07-26｜FIX（**使用者單次授權修改 raw/solutions/，不含數值**）｜**懸臂梁 d 偏移判準收斂：RC-2006-1 與 RC-2023-3 論證統一為 ACI 318 §9.4.3.2 三條件**
  **背景：** 前一筆紀錄揭露兩份 verified 解答對「懸臂梁能否採 d 偏移」處理相反。經與使用者確認後裁示收斂。
  **授權範圍（使用者明示）：** 僅修改**理由文字**，兩題的**答案與所有數值一律不動** ——
  RC-2006-1 維持 $V_u = 19{,}913$ kgf、$V_s = 16{,}704$ kgf、$s = 13.2$ cm；RC-2023-3 維持 $V_u = 7.425$ tf、$e_{\max} = 10.4$ cm。
  因未更動 verifiedSolution，**規則 2 未被觸及**。
  **錯在哪（僅 RC-2006-1 的論證結構）：** 原文「懸臂梁均布載重的剪力由自由端向固定端遞增，固定端最大，且無斜壓桿效應，故臨界斷面應取在固定端面」——
  ① 「固定端剪力最大」是**事實正確但推論無效**：簡支梁 $V(x)=w(L/2-x)$ 同樣是支承面最大、向內遞減，卻可採 d 偏移；
     d 偏移規定的前提本來就是「支承面剪力最大」，此句無法區分兩者。
  ② 「無斜壓桿效應」是實質論點，但對「與柱／牆同澆、載重在頂面」的懸臂梁站不住腳（頂面載重可沿斜壓桿走到固定端底部的壓力弦，即反力交入柱之處）。
  **改成什麼：**
  ・`raw/solutions/RC-2006-1/`：第 5 節改為 §9.4.3.2 三條件對照表，結論改為「**條件 (a)（支承細節）題目未明示、無法確認 → 保守取固定端面**」；
    加註「勿用錯理由」方塊點出上述 ① 的邏輯瑕疵；並列出若 (a) 成立則 $s = 15.2$ cm（供對照，非答案）。陷阱列與計算段標註同步。
  ・`raw/solutions/RC-2023-3/`：Step 1 與 L3 知識點補上三條件逐一檢核 (a)✓(b)✓(c)✓，並註明「判準是條件不是構件名稱」。
  ・兩題互相加上交叉連結。
  **同步更新：** `wiki/problems/RC-2006-1.md`（ingest 副本敘述）、`study/problems-view/RC-2006-1.html` 與 `RC-2023-3.html`（重新產生）、
  `wiki/traps/SHEAR-CRITICAL-SECTION.md`（懸臂梁段由「兩份解答衝突」改為「條件不同」）、`study/lecture-RC-U2-1.html` §4.1 與 PDF。
  **怎麼驗證的：** ① 條文對照 ACI 318 §9.4.3.2 三條件；② 邏輯反證（簡支梁同為支承面最大卻可折減）；
  ③ 數值重算確認兩題答案未變（13.2 cm、7.425 tf、10.4 cm 皆與原解一致）；④ 全庫掃描確認舊理由字串已無殘留。
  **⚠️ 規則狀態：** 本次修改 `raw/solutions/RC-YYYY-N/` 屬**使用者單次授權**，`CLAUDE.md` 規則 1 **維持原文未擴充例外**（使用者裁示）。
  日後同類勘誤仍須逐次取得授權。

## 2026-08-08 unit-formula-map：RC-U1-1 / RC-U1-2

- 新增 `study/formula-given-RC-U1-1.html` + `.pdf`（30 條公式：必背 24 / 別賭 6 / 通常會給 0）
- 新增 `study/formula-given-RC-U1-2.html` + `.pdf`（30 條公式：必背 24 / 別賭 4 / 通常會給 2）
- 證據來源：`raw/exams/` 民國 91–114 年共 24 份考卷（pdftotext 全年份抽取 + 92 年掃描影像卷逐頁目視判讀）
- 交叉驗證：`verify.py` 卡片 ok 年份 vs 逐年矩陣 ✔，兩份皆「全部一致」
- 兩頁互相加上導覽按鈕；CLAUDE.md / README.md / 檔案架構索引表.md 同步登錄第三種教材型態

## 2026-08-08 unit-formula-map：RC-U2-1 / RC-U3-3 / RC-U4-1

- 新增 `study/formula-given-RC-U2-1.html` + `.pdf`（24 條：必背 20 / 別賭 3 / 通常會給 1）
- 新增 `study/formula-given-RC-U3-3.html` + `.pdf`（27 條：必背 17 / 別賭 4 / 通常會給 6）
- 新增 `study/formula-given-RC-U4-1.html` + `.pdf`（23 條：必背 14 / 別賭 4 / 通常會給 5）
- 92 年掃描影像卷以 200 dpi 重新逐頁目視，確認第一題鋼絞線 σ-ε 曲線、第二題 λd 詳細式、第四題剪力牆門檻／φ=0.6／λdh 的原文內容
- 交叉驗證：`verify.py` 三份皆「全部一致」；抽樣回查 93、102、107、108、112 年考卷原文確認 fps 與橫膈版 Vn 的標記
- `formula-given-RC-U1-1/U1-2` 兩頁 nav 補上指向新三頁的按鈕；U1-2 的 Ash 卡片加註「同一條在 U3-3 列為別賭（98 年說明題沒給）」

## 2026-08-08 unit-exam-intel：RC-U1-1 / RC-U1-2 舊 study 頁重構為命題情報頁

### 重構了什麼、刪了哪些重複區段

- `study/study-RC-U1-1.html`、`study/study-RC-U1-2.html` 由早期「七區段深度複習頁」改寫為
  六區塊命題情報頁（出題概況／考點結構／考點漂移／題型走向／考題清單／命題風險），**檔名不變**
  （`lecture-*`、`formula-given-*` 都連回這兩個檔名，改名要同步三處）。
- 逐區段重疊盤點後的處置：

  | 舊區段 | 重複於 | 處置 |
  |---|---|---|
  | ① 命題分析 | 無 | 保留並擴充成六區塊 |
  | ② 截面圖解 | lecture §2／§4／§5（U1-1）、§2～§5（U1-2） | 刪，改由 nav 連結 |
  | ③ 解題流程圖 | lecture §8（U1-1）、§9（U1-2） | 刪，改由 nav 連結 |
  | ④ 核心公式速查 | formula-given §二（多了逐年考卷給／背證據，是上位版） | 刪，改由按鈕連結 |
  | ⑤ 考題清單 | lecture 精選題章節（無篩選、無渲染頁連結） | 保留並補上副考點與分群篩選 |
  | ⑥ 高頻陷阱 Top 8 | lecture 陷阱總表 | 刪 |
  | ⑦ 互動計算器 | 唯一內容 | **經使用者確認後刪除** |

- 依使用者指示一併處理：移除本次兩頁的 Keynote PDF 按鈕（`RC-U1-n_*.pdf` 仍保留在 `study/`，
  只是不再從這兩頁連出）；`lecture-RC-U1-1.html` 補上缺漏的回連按鈕（命題分析／給背分界／本頁 PDF），
  `lecture-RC-U1-2.html` 的「📊 速查頁」改名為「🔍 命題分析」並以「🎯 給／背分界」取代 Keynote 鍵。
  註：`lecture-RC-U2-1/U3-3/U4-1` 與 `study-RC-U2-1/U3-3/U4-1` 的 Keynote 按鈕**本次未動**（不在本次單元範圍）。

### 過程中修正的資料錯誤

- **`study/problems-view/` 原僅 64／100 頁**，U1-1 的 22 題中有 17 題沒有渲染頁，
  舊 study 頁只好連 `../index.html#md=raw/solutions/...`（瀏覽器拿到未渲染的純文字，公式與附圖全失效）。
  已用 `outputs/build_problems_view.py`（markdown + 離線 KaTeX，與既有頁模板一致）補齊到 **100／100**，
  兩頁題號一律改連 `problems-view/XX-YYYY-N.html` 並 `target="_blank"`。
- **既有 64 頁的返回鍵是 `javascript:history.back()`**，在 `target="_blank"` 開的新分頁按了沒有反應
  （新分頁沒有上一頁歷史）。全部改為「命題分析＋講義」雙鈕靜態連結，並注入「跟隨來源單元」腳本
  （讀 `document.referrer`，來源是 `study-`／`lecture-`／`formula-given-RC-Un-m.html` 時覆寫兩鍵指向來源單元；
  無 JS 或無 referrer 時靜態 href 保底）。
- **`RC-2002-2.html`、`RC-2011-4.html` 兩頁的 `#9`（鋼筋號數）被舊轉檔器誤判為 Markdown 標題**，
  頁面出現 `<h1>9 截面積 = 6.47 cm²…</h1>`。新轉檔器在送進 markdown 前把 `#` + 數字換成佔位字元，
  轉完再還原，兩頁已重生並確認 `<h[1-6]>數字` 的誤判數為 0。
- **舊 study-RC-U1-1 頁的觀察句寫「近 5 年連續出題（2020–2024）」**，但 2025 年考卷四題（RC-2025-1～4）
  無一屬 U1-1，正確描述是「近 6 考年 5／6 年出題，2025 年整年缺席」。新頁 KPI 直接抄 `stats.py`。
- **（僅記錄、未修改）** `raw/solutions/RC-2019-1/RC-2019-1.md` 與 `RC-2019-2/RC-2019-2.md` 的表頭
  主分類寫成 `RC-U1`（缺子項號），正確應為 `RC-U1-1`、`RC-U1-2`。`question_index.json` 的
  `primaryTopicId` 是對的，統計不受影響；因受規則 1、2 保護，個別題目解析未予更動。

### 由統計得出的命題觀察（全部可由 `scripts/stats.py` 複算）

- **RC-U1-1**：主 19／副 3，佔全科 19.0%，全科排名 #1（#2 的 RC-U3-3 為 16 題）；24 考年中 14 年出現，
  空窗年段 2008–2010、2012–2013、2017–2018；近 6 考年 5／6 年共 8 題。
  漂移（前 9 題 2002–2015 → 後 10 題 2016–2024）：雙筋梁 2→3、鋼筋量限制 1→2、單筋矩形梁 2→2、
  T 形梁 3→2、彎矩–曲率韌性 1→1。重心從「認斷面型式」移向「解邊界條件」——後段雙筋梁三題
  （2022-1、2023-2、2024-2）全部是壓力筋**未**降伏，前段 2002-4 則是恰好降伏。
  設計法：19 題全為 USD，本科無 ASD／LRFD 雙軌問題，故改以問法分軸（分析／設計／韌性／鋼筋量上下限）。
- **RC-U1-2**：主 12／副 8，佔全科 12.0%，全科排名 #4（前為 RC-U4-1 13 題、後為 RC-U3-2 7 題）；
  24 考年中 11 年出現，空窗年段 2006–2007、2012–2014、2022–2023；近 6 考年僅 2／6 年共 2 題。
  漂移（前 6 題 2002–2011 → 後 6 題 2011–2024）：互制圖單點求解 2→3、細長柱 1→0，其餘四群持平。
  重心從「建整條 P-M 互制圖」收斂成「解互制圖上的一個點」；細長柱主考點已移交 RC-U1-3
  （2006-2、2016-3 的 primaryTopicId 皆為 U1-3），柱曲率韌性主考點自 2011-3 起空窗 14 年。
  設計法：USD 11 題＋概念題 1 題（2011-1），後段無概念題。
- 兩頁均以 `scripts/verify.py` 對帳通過（題號集合、主／副旗標、designMethod、篩選鈕數字、
  KPI 四項、題號連結存在性、禁用寫法七項全過）。

## 2026-08-08 unit-exam-intel：RC-U2-1 / RC-U3-3 / RC-U4-1 舊 study 頁重構為命題情報頁

### 重構了什麼、刪了哪些重複區段

- `study/study-RC-U2-1.html`、`study-RC-U3-3.html`、`study-RC-U4-1.html` 由早期「七區段深度複習頁」
  改寫為命題情報頁，**檔名不變**。處置沿用 U1-1／U1-2 這一輪已與使用者確認的原則：
  ② 截面／構造圖解 → 刪（重複於 lecture 各章）；③ 解題流程圖 → 刪（lecture §8／§9）；
  ④ 核心公式速查 → 刪（formula-given 是含逐年考卷證據的上位版）；⑥ 高頻陷阱 Top 8 → 刪（lecture 陷阱總表）；
  ⑦ 互動計算器（U2-1 梁剪力檢核／U3-3 柱 Ash 檢核／U4-1 預力兩階段應力）→ **刪**；
  ① 命題分析 → 保留並擴充；⑤ 考題清單 → 保留並補上副考點與分群篩選。
- **U2-1 主考點只有 7 題（< 8），依 skill 規定跳過「考點漂移」區塊**，改在出題概況註腳寫一行趨勢描述，
  並把該位置換成「剪力的角色：主考點 7 題 vs 副考點 9 題」表（依副考點的來源單元分類）。
  故 U2-1 只有五個區塊，nav 也不放漂移連結。
- 三份 `lecture-RC-U2-1/U3-3/U4-1.html` 的 nav：「📊 速查頁」改名「🔍 命題分析」，
  「📄 Keynote」以「🎯 給／背分界」取代。至此 `study/` 底下已無任何 Keynote 按鈕
  （`RC-U2-1_*.pdf` 等檔案仍保留在資料夾內，只是不再從教材頁連出）。

### 過程中發現的資料問題（逐項）

- **`RC-2021-4` 的 `designMethod` 記為「概念題」，但解析內容是 WSD 容許應力計算題**
  （後拉預鑄梁與場鑄板組成 T 型梁，求最大均布活載重，`raw/solutions/RC-2021-4/RC-2021-4.md`
  表頭自己寫的是「WSD 工作應力法（容許應力設計法）」）。
  本頁一律以 `question_index.json` 為準（`verify.py` 會強制比對），因此頁面上 U4-1 的
  「近 6 考年 概念題 1 題」與「後段概念題 1 題」都含這一筆。
  已在 `study-RC-U4-1.html` 的設計法區塊加上 ⚠️ 資料註記。**未逕行修改索引**，待確認後更正並重算。
- **（僅記錄、未修改）** 解析 .md 表頭主分類缺子項號者再添兩例：
  `RC-2019-3.md` 寫 `RC-U3`（應為 `RC-U3-3`）、`RC-2018-4.md` 寫 `RC-U4` 且把 `RC-U4-1` 放在副分類
  （索引記的是 `primaryTopicId = RC-U4-1`，正確）。連同前一批的 `RC-2019-1`、`RC-2019-2`，
  目前已知 4 例。索引皆正確，統計不受影響；因受規則 1、2 保護，個別題目解析未予更動。
- 舊 U2-1／U3-3／U4-1 頁的觀察句未逐句留存比對（舊頁 ① 區已整段重寫），
  但三頁的 KPI 與清單題數本次全部改由 `stats.py` 產生、`verify.py` 對帳。

### 由統計得出的命題觀察（全部可由 `scripts/stats.py` 複算）

- **RC-U2-1（剪力）**：主 7／副 9，佔全科 7.0%，排名 #6；24 考年只出現 7 年，
  **且沒有任何一年出過兩題**（2006、2009、2010、2014、2017、2020、2023 各一題），空窗年段多達七段。
  7 題主考點全為 USD。**副考點 9 題比主考點還多**，來源為 U3-3 ×5、U2-2 ×2、U1-1 ×1、U4-4 ×1
  ——剪力在本科主要是「當配角」，最大入口是耐震剪力鏈（M_pr → V_e → V_c=0 → 密箍）。
  7 題主考點沒有一題是單純配箍筋，每題都另綁一個判斷（軸力修正／STM／介面剪力／倒 T 的 d 偏移／扭力門檻）。
- **RC-U3-3（韌性與耐震）**：主 16／副 2，佔 16.0%，排名 #2；24 考年中 12 年出現，
  空窗年段 2006–2008、2014–2015、2020–2021、2023–2024。出題高度成組：2012 年一年考 3 題
  （2012-2 梁 → 2012-3 柱 → 2012-4 接頭，同一構架連環題），2003、2004 各 2 題。
  漂移（前 8 題 2003–2012 → 後 8 題 2012–2025）：耐震梁 1→2、韌性觀念與細則 2→1，
  柱圍束／接頭／牆體各持平。重心從「背耐震構造規定」移向「走完能力設計法的因果鏈」
  ——後段 8 題有 6 題要先反推一個設計力才能開始算。
  設計法：USD 12＋概念題 4；**概念題比例 25%（4／16）為全科 13 個單元最高**
  （第二名 RC-U4-3 為 1／5＝20%，RC-U1-1 為 0%），此數字由索引全表統計得出。
  柱圍束 A_sh 是本單元最高頻標籤（×3）卻自 2013-2 起空窗 12 年，是本頁風險排序第一名。
- **RC-U4-1（預力斷面應力）**：主 13／副 8，佔 13.0%，排名 #3；24 考年中 13 年出現，
  空窗年段僅 2015–2017、2019–2020、2024–2025 三段，是全科最規律的單元之一；
  **清單 21 題有 19 題是考卷的第 4 或第 5 題（其中 17 題正好是第 4 題）**。
  漂移（前 6 題 2003–2009 → 後 7 題 2011–2023）：組合斷面疊加 3→1、彈性應力與使用性 1→3、
  開裂彎矩與極限強度 2→3。重心從「把組合斷面應力疊起來」移向「選對斷面、階段與 f_ps 公式」。
  設計法：**WSD 7＋混合 4＋USD 1＋概念題 1**，是全科唯一必須準備兩套設計法的單元；
  全科 100 題裡 WSD 共 16 題，**16 題全部落在 U4 單元群**（U4-1 七、U4-2 五、U4-3 四），
  U1／U2／U3 一題都沒有；U4-1 的 8 題副考點在索引中亦全為 WSD。
- 三頁均以 `scripts/verify.py` 對帳通過；另以獨立腳本重算漂移對切、設計法分布、近 6 考年、
  副考點來源與分群唯一性，與頁面手寫表格逐格相符。

## 2026-08-20 subject-frequency-map：產出 RC 全科出題頻率熱圖 `study/frequency-RC.html`

### 產了什麼

- `study/frequency-RC.html`（單一自包含 HTML，無外部相依，25,319 字元），由
  `subject-frequency-map/scripts/build_frequency.py` 從 `raw/json/question_index.json` ＋
  `raw/json/syllabus_taxonomy.json` 產生，更新日期標記 2026-08-20。
- 頁面內容：可切換「只看主考點／主＋副考點」的 14 子項 × 24 考年熱圖、排名總表
  （主／副題數、佔全科、出現年數、最長空窗含年段、最後出現、近 6 考年、常見題號位置、現有教材）、
  各單元權重表、五種情境的讀書順序建議。
- 排名表教材欄由腳本掃描 `study/` 自動產生，本次偵測到 20 個綠色可點標籤
  ＝ RC-U1-1、U1-2、U2-1、U3-3、U4-1 五個子項各有四種教材（命題分析／講義／給背分界／記憶片）齊全；
  其餘 9 個出現過的子項四欄皆灰色（尚未製作）。
- **對帳全過**：熱圖主考點格子總和 ＝ 題庫總題數 100、每列總和 ＝ 該子項主考點題數、
  單元小計加總相符；無孤兒 `primaryTopicId`（索引與 taxonomy 的子項代碼完全對得起來），頁面未出現紅色警告框。
- 目視 QA：headless Chromium 開啟，console 乾淨無錯誤；兩個模式各重畫一次皆正常
  （主考點模式 42 顆橘點，切到主＋副後歸零並改為併入格值）；tooltip 題號格式正確
  （例：`2005：RC-2005-2、(副)RC-2005-3`）。

### 由這張表得到的命題觀察（全部由 `build_frequency.py` 算出，未手打）

- **規模**：24 考年（2002–2025）、100 題、14 個子項，其中 13 個曾當過主考點。每年題數不一致，
  故熱圖各欄總和 ＝ 該年題數。熱圖色階上限為 3（主考點與主＋副兩個模式皆同，`maxP = maxA = 3`）。
- **單元權重**：RC-U1 33 題（33.0%）＞ RC-U3 29 題（29.0%）＞ RC-U4 24 題（24.0%）＞
  RC-U2 14 題（14.0%）。最重的 U1 是最輕的 U2 的 **2.4 倍**。
- **前五名**：U1-1 梁彎矩 19、U3-3 韌性與耐震 16、U4-1 預力斷面應力 13、U1-2 柱強度 12、
  U3-2 樓版與基腳 7，**合計 67 題、佔全科 67.0%**——五個子項吃掉三分之二的題數。
  其中 U1-1、U3-3、U4-1、U1-2 四個已有完整四種教材。
- **工具型子項只有一個**：全科唯一副考點多於主考點的是 **U2-1 剪力（主 7／副 9）**。
  這與 SM 那種「一半以上子項都是工具型」的結構不同：RC 的副考點分布相對集中，
  切到「主＋副」模式後只有 U2-1 這一列明顯變深。
- **0 題子項**：**U1-4 柱設計圖之應用**，24 個考年 0 題——命題大綱有列，考卷上從沒以它為主考點出現過，
  可以直接跳過（排名表以粉紅底標示）。
- **最長空窗**：U2-3 鋼筋錨定長度與斷點計算 **22 年**（2004–2025 空窗，最後出現 2003）、
  U4-4 預力梁剪力 **20 年**（2002–2021 空窗，2022 回歸一次）、U4-3 預力損失 **10 年**（2006–2015）。
  U3-1 梁工作性要求（含撓度、裂縫）主考點 6 題但已 8 年空窗（2010–2017），最後出現 2018。
- **近 6 考年（2020–2025）共 24 題**，集中在少數幾列。
- 本頁只用於**分配時間**，不作押題；押題請看各子項 `study-RC-Un-m.html` 的「命題風險排序」。

## 2026-08-20 struct-diagram 圖解整併 RC-2015-1；發現並修正 index.html 的 KaTeX 版本問題

### 一、RC-2015-1 向量圖解整併

- `raw/solutions/RC-2015-1/files/` 內 struct-diagram 的產出整併回正本：新建 `figs/` 子資料夾，
  收入 4 組 SVG＋2× PNG 與生成腳本 `gen_RC-2015-1.py`（可重跑）。
  `files/` 殘留的已合併 md 與 `.patch` 移至 `files/_to_delete/`（device_bash 不能刪檔，待人工清除）。
- 驗證後才套用：把 `RC-2015-1-figs.patch` 套到整併前的正本，結果與 `files/RC-2015-1.md`
  **逐字元相同**，確認 patch 內容無夾帶未預期改動後才寫入。行尾維持 CRLF。
- §1 依使用者決定改為**考卷原圖與向量重繪並列**（圖 1a／圖 1b），不以重繪取代截圖。
- **數值修正（隨 patch 一併帶入，原值為四捨五入累積誤差）：**
  $C'_s$ 127,126 → **127,112** kgf；$P_{n,b}$ 430,686 → **430,672** kgf；
  $M_{n,\max}$ 13,585,411 → **13,585,103** kgf·cm；$\varphi M_{n,\max}$ 88.98 → **88.97** tf·m；
  $\varphi P_{n,\max}$ 689,134 → **689,117** kgf。四捨五入後的結論值（135.85 tf·m、89.0 tf·m）不變。
- **新增三節進階討論：** 純彎矩點補算（$c=8.60$ cm，$M_n=65.79$ tf·m，$\varphi M_n=59.21$ tf·m）；
  $\varphi M_n$ 峰值不在平衡點（右移至 $\varepsilon_t=0.005$、$c=19.50$ cm，達 **104.08 tf·m**）；
  原文「純彎矩（0, ~tf·m）」的空缺補為 59.2。
- **下游同步三處：** `wiki/problems/RC-2015-1.md`（圖形區＋解題關鍵步驟數字＋兩條進階結論）、
  `study/problems-view/RC-2015-1.html`（**由新正本完整重新渲染**，非手改）。
  渲染器設定先以整併前的正本反推驗證：python-markdown `['tables','nl2br','fenced_code']`
  ＋ 數學式遮罩／清單前補空行／圖片路徑補前綴三道處理，產出與現有 HTML 逐字元相同後才用於新版。
- `CLAUDE-SPEC.md` 新增 **§5.1 向量圖解（`figs/`）規範**：命名、SVG/PNG 成對、腳本可重跑、
  與考卷原圖並存、數值以腳本為準並同步三處；§3 允許檔案類型表與目錄同步加列。
- 驗證：15 個圖片相對路徑全部存在；舊數值全庫零殘留；四檔 CRLF 未破壞；圖 3／圖 4 目視確認數值一致。

### 二、KaTeX 版本問題（既有，非本次造成）

- 現象：`\text{}` 內的 `·`（U+00B7）被 KaTeX 轉為 `\cdotp`，而該指令在舊版**僅限數學模式**，
  於文字模式成為未定義指令。此寫法全庫 **391 處、散在 136 個檔案**（`tf·m`、`kgf·cm` 等單位）。
- 實測版本界線：**KaTeX ≤ 0.16.9 失敗，≥ 0.17.0 正常**（0.13.24／0.15.6／0.16.4／0.16.9／0.16.11
  全部失敗；0.17.0／0.18.0／0.18.1 全部正常）。以 `markdown.math.macros` 把 `\cdotp` 映射成 `\cdot`
  的偏方**實測無效**，因報錯發生在巨集展開之前。
- 影響分流：`study/assets/katex/` 是 **0.18.1**，故 `study/` 底下 11 個頁面（含 problems-view）**渲染正常**；
  **`index.html` 從 CDN 載入 `katex@0.16.11`**，落在失敗區間，且因 `throwOnError:false` 不跳錯，
  而是靜默印出字面的 `kgf\cdotpcm`、`tf\cdotpm`——主儀表板的 md 預覽長期渲染錯誤而未被察覺。
- **修正：** `index.html` 的 KaTeX 來源由 CDN 改為本機副本 `study/assets/katex/`（0.18.1），
  與 `study/` 各頁同一份；離線亦可正常渲染（原本離線是降級為不渲染），並在該段加註「不可退回 0.16.x」的原因。
  `mathHint` 提示文字同步改為「找不到 study/assets/katex/」。
- 未處理：VS Code 內建 Markdown 預覽自帶舊版 KaTeX，仍會對 `·` 報 ParseError。
  依使用者決定不處理——校稿一律以 `study/problems-view/` 與儀表板為準，VS Code 預覽僅作純文字編輯用。

### 三、既有問題（本次未動，供日後處理）

- 全庫工作目錄為 CRLF、git 內儲存為 LF，`.gitattributes` 未設 `text=auto eol=lf`，
  導致 `git status` 幾乎每個檔案都顯示 modified、diff 全檔翻紅（未經修改的 `RC-2002-1.md`
  亦顯示 410 行全異動）。檢視實際改動須用 `git diff --ignore-cr-at-eol`；
  本次真正改動為 4 檔 160 增 27 刪。修正需一次全庫規模的 commit，留待使用者決定。

## 2026-08-20（補正）KaTeX `·` 問題：巨集偏方其實有效，前一則紀錄的判斷有誤

> 本則更正同日前一則「二、KaTeX 版本問題」中「以 `markdown.math.macros` 把 `\cdotp`
> 映射成 `\cdot` 的偏方**實測無效**」的結論。該結論的**現象描述正確、歸因錯誤**：
> 巨集其實有生效，錯的是映射目標。依規則 3 不刪改既有紀錄，於此補正。

- 重測發現：套用 `macros {"\cdotp":"\cdot"}` 後，錯誤訊息由
  `Undefined control sequence: \cdotp` 變成 `Undefined control sequence: \cdot`
  ——**代表巨集確實展開了**，只是 `\cdot` 與 `\cdotp` 同為數學模式專用指令，
  在 `\text{}` 內一樣未定義，所以照樣失敗。前一則誤判為「報錯發生在巨集展開之前」。
- **可行解：把 `·` 直接映射到 Unicode `⋅`（U+22C5 DOT OPERATOR）**，即
  `"markdown.math.macros": { "·": "⋅" }`。實測：
  - KaTeX 0.16.11（VS Code 內建同級）：全部通過，輸出 `kgf⋅cm`、`tf⋅m（標稱最大彎矩）`，
    與 KaTeX 0.18.1 的**原生輸出逐字相同**。
  - KaTeX 0.18.1（本庫 `study/assets/katex/`）：同樣通過，故日後升級不會反噬。
  - 數學模式中原本就正常的 `·`（如 `5 · 3`）不受影響；表格內 `M_n (tf·m)`、
    `kN·m`、`N·mm` 一併正常。
- 其他候選皆不可用：`\textperiodcentered`、`\textbullet` 在 KaTeX 0.16.x 未定義；
  `\char"00B7` 渲染出錯字；`\raisebox{0.25em}{.}` 變成句點；映射回 `·` 本身會無限展開。
- 已產出 `.vscode/settings.json`（含完整原因註解，另關閉中文庫必然觸發的
  非 ASCII 高亮橫幅）。**該檔無法由 Cowork 寫入**——遠端工具禁止寫 `.vscode`，
  須由使用者自行建立或貼入使用者設定。
- 影響範圍不變：此為 VS Code 預覽端的修法，不動 `raw/` 任何檔案，
  `index.html` 改用本機 0.18.1 的修正仍然必要且已完成。

---

## 2026-08-21 全庫 verificationStatus 一律改回 `unverified`

- 使用者回報：`raw/solutions/` 部分解析內容有誤，需重新驗算。
- 依 CLAUDE-SPEC.md §9，將 `raw/json/question_index.json` 中
  **全部 100 題**的 `verificationStatus` 由 `verified` 改為 `unverified`（其餘欄位未動）。
- 影響：依規格 `unverified` 不得 ingest；`wiki/problems/` 既有頁面保留不刪，
  待逐題人工驗算通過後再逐題改回 `verified` 並重新 ingest。
- `raw/solutions/*.md` 內文未修改；其中 RC-2018-2 / RC-2018-3 / RC-2018-4
  的「驗算狀態」欄本來就標 `unverified`，與 JSON 一致。

---

## 2026-08-21 RC-2015-1 修正：補上「最大極限彎矩載重 = 104.1 tf·m」的完整計算過程

### 問題

- 使用者回報：本題答案 104.1 tf·m 只出現在 §5 進階討論的一張兩列表格裡，**沒有計算過程**；
  §4 主線把平衡點的 89.0 tf·m 當成答案，與題目問的「最大**極限**彎矩載重」不符。

### 修正內容（正本 `raw/solutions/RC-2015-1/RC-2015-1.md`）

- §4 由「單階段」改為**兩階段**：Step 1–7 平衡點（標稱峰值，中間對照）；
  新增 Step 8（判斷 φMn 峰值位置）、Step 9（拉力控制界限六小步完整計算）、
  Step 10（掃描 c 驗證單峰），並新增「答案」區塊。
- 主線答案改為 $(\varphi M_n)_{\max} = 104.1$ tf·m（$c=19.50$ cm、$\varepsilon_t=0.005$、$\varphi P_n=224.6$ tf）。
- 新增陷阱⑤「把 φ×標稱峰值當成最大極限彎矩」：$\max(\varphi M_n)=104.1 \neq \varphi\cdot\max(M_n)=89.0$。
- §2、§3、§3.5 同步改寫（核心觀念雙峰值表、核心推論二、作戰計畫兩階段六步驟、
  VHA 新增「拉力控制界限」層次與 Step 8–9 公式）。
- 符號釐清：標稱峰值仍記 $M_{n,\max}$，設計峰值改記 $(\varphi M_n)_{\max}$，避免混用。

### 過程中發現並更正的既有資料錯誤

- §5「純彎矩點（補算）」原記 $f'_s = 605$ kgf/cm²，實際為 **428** kgf/cm²
  （$c=8.60$ 時 $\varepsilon'_s = 0.003\times0.60/8.60 = 0.000210$，$f'_s = E_s\varepsilon'_s = 428$）。
  $M_n = 65.79$、$\varphi M_n = 59.21$ 不受影響（$C'_s$ 僅約 1.4 tf），故只改該項並加註。
- §4 Step 10 掃描表與 §5 各比值均由獨立腳本複算，與圖 2／圖 4 的 `gen_RC-2015-1.py` 結果一致，
  既有向量圖**無須重繪**（圖 4 本來就把 φMn 峰值畫在 εt=0.005）。

### 下游同步（依 figs-integration 的三處規則）

- `wiki/problems/RC-2015-1.md`：標題、核心考點、解題關鍵步驟（7 步 → 15 步）、公式、陷阱全面改寫；
  驗證狀態改標 `⏳ unverified`。
- `study/problems-view/RC-2015-1.html`：以 python-markdown 管線重新產生 `<main>`；
  **重跑前先用原 md 做過往返測試，確認可逐位元組還原既有頁面**，再套新內容。
- `raw/json/question_index.json`：RC-2015-1 的 tags 增列「拉力控制界限」「設計強度峰值」；
  `verificationStatus` 依使用者指示維持 `unverified`。
- `wiki/index.md`、`wiki/by-year.md`：該題的一行描述由「平衡點最大彎矩」改為「最大極限彎矩載重（拉力控制界限）」。

### 待辦

- 其餘 99 個 `wiki/problems/*.md` 仍顯示 `✅ verified`，與 JSON 的 `unverified` 不一致，尚未批次同步。

---

## 2026-08-21（同日續）三件收尾：重建腳本入庫、驗證狀態全庫同步、柱題橫向複核

### 一、新增 `scripts/gen_problems_view.py`

- 把 RC-2015-1 修正時用過、且經**逐位元組往返驗證**的 python-markdown 管線固化成腳本。
- 預設**不吃全庫**：不給題號就什麼都不做，要全庫必須明寫 `--all`（避免順手改動上百頁）。
- `--check` 可先比對不寫檔。

### 二、`wiki/problems/*.md` 驗證狀態同步

- 98 個摘要頁的 `✅ verified` → `⏳ unverified（2026-08-21 全庫改標，待逐題人工驗算）`，與 JSON 一致。
- **未動 2 個**：RC-2015-1（已於前一則自帶註記）、RC-2023-1（見下方「發現的結構問題」）。

### 三、柱題橫向複核（10 道 P-M／平衡點相關題，逐題重算）

結論：**沒有第二題犯 RC-2015-1 的同型錯誤**——其餘各題的軸力都由題目鎖定，不存在「峰值在哪」的問題。
但複核過程抓到 5 類其他問題，均已修正：

| 題號 | 問題 | 處置 |
|------|------|------|
| RC-2024-3 | §5 簡化法算術錯：$346{,}270$ 應為 $346{,}097$（$15.21\times238+10.14\times238=6{,}033$） | 已改，並補上分項 |
| RC-2024-3 | 「偏向平衡點側」與實算不符（$P_b=136.6$、$P_0=541.5$、本題 $340.1$，位置比例 **0.50**） | 改為實數敘述 |
| RC-2019-2 | 圖片 alt-text 的 $b$／$h$ 與圖說相反（alt 寫 b=70/h=50，圖說與計算用 h=70/b=50） | 改 alt；解題本體零錯誤 |
| RC-2008-2 | 「平衡點…彎矩最大附近」未分標稱／設計 | 加「標稱」並補本斷面對照表（$\max M_n=87.68$ @ $c_b$ vs $\max\varphi M_n=64.90$ @ $\varepsilon_t=0.005$） |
| RC-2011-1 | 步驟六「平滑連線」對**設計**曲線不成立（漏 $\varepsilon_t=0.005$ 折點與 $0.80\phi P_{n0}$ 截平） | 加註兩處不連續，並指向 RC-2015-1 |
| RC-2011-1 | 步驟五取點漏掉 $c>h$ 段，且未指定必取 $c_b$ 與 $0.375d$ | 補三段掃描與兩個必取點 |
| RC-2011-1 | $\phi P_{u,\max}$ 把 $\phi$ 計入兩次 | 改為 $P_{u,\max}=\phi P_{n,\max}$ |
| RC-2011-1 | 純彎點直接假設 $\varphi=0.90$ | 改為須實算 $\varepsilon_t$ 再定 |
| RC-2011-3 | 同一個 275,700 kgf 同時被標成 $P_n$ 與 $P_u$，L144 自相矛盾 | 符號統一，並新增 §5「題意歧義」 |

### 四、RC-2011-3 的題意歧義（**待人工定案**）

原卷（RC-2011 第三題）寫「$P_u=0.9P_b$，其中 $P_b$ 為…**標稱**軸壓強度」，而同卷第一題自行定義
「$P_u$ 及 $M_u$ 分別為…**設計**軸力強度及設計彎矩強度」——出題者混寫兩個層次。兩種解讀都自洽：

| 解讀 | $c$ | $\varepsilon_t$ | $\varphi$ | $\varphi M_n$ | $\mu_\phi$ |
|------|----:|----------------:|----------:|--------------:|-----------:|
| A（現行、坊間通行） $P_n=0.9P_b$ | 29.61 | 0.002472 | 0.685 | 56.75 | 1.70 |
| B（照字面） $\varphi P_n=0.9P_b$ | 39.63 | 0.001087 | 0.650 | **50.25** | **2.21** |

另注意 Part (二) 的 $N=275{,}700/1.3$ **只有在解讀 B 下才嚴格成立**（$\gamma$ 應除設計值）。
本頁暫採 A 並完整保留 B 的數字，待比對標準答案後擇一。

### 五、φ 公式全庫兩式並存（**已就 RC-2015-1 定案，其餘待處理**）

- 舊式 $\varphi=0.65+\frac{\varepsilon_t-0.002}{0.003}\times0.25$（以 0.002 為壓力控制界限）
- 現行式 $\varphi=0.65+0.25\frac{\varepsilon_t-\varepsilon_{ty}}{0.005-\varepsilon_{ty}}$（以 $\varepsilon_{ty}=f_y/E_s$ 為界）

庫內 4 份用舊式（RC-2004-2、RC-2015-1、RC-2015-2、RC-2015-3）、4 份用現行式
（RC-2011-1／-2／-3、RC-2019-1）。**`wiki/code-ref/ACI-318.md` §21.2.2 明文採現行式**，
故以現行式為準。本次已把 **RC-2015-1** 改過來：平衡點 $\varepsilon_t=\varepsilon_{ty}$ 恰在壓力控制界限，
$\varphi=0.650$（非 0.655），$\varphi M_n(c_b)$ 由 89.0 → **88.3** tf·m、$\varphi P_{n,b}$ 由 282.1 → **279.9** tf。
**本題答案 104.1 tf·m 不受影響**（該點 $\varepsilon_t=0.005$，$\varphi=0.90$ 兩式相同）。
RC-2004-2、RC-2015-2、RC-2015-3 尚未改，待統一。

### 六、連帶修正的衍生層（原本仍寫舊說法）

- `wiki/concepts/PM-INTERACTION-DIAGRAM.md`：RC-2015-1 描述改寫；並修正一條**觀念錯誤**——
  原寫「壓力控制區 φ 須依**軸力**插值（0.65 至 0.9）」，實際 φ 依 $\varepsilon_t$ 判定，
  且壓力控制區內 φ 恆為 0.65 不內插。
- `wiki/concepts/BALANCED-POINT.md`：補「平衡點只是標稱峰值」與 φ 內插上下界。
- `wiki/methods/PM-INTERACTION-DIAGRAM.md`、`wiki/philosophy/usd-column-pm.md`：RC-2015-1 一行描述改寫。
- `wiki/problems/RC-2015-1.md`、`RC-2011-3.md` 同步。
- 6 個 problems-view 頁以新腳本重建。

### 發現但**尚未處理**的兩件事

1. **`wiki/problems/RC-2023-1.md` 不是摘要頁**——它是 `raw/solutions/RC-2023-1/RC-2023-1.md` 的
   **逐位元組完整複本**（7,879 bytes 相同），章節是 §1–§5 解析結構而非「題幹摘要／核心考點／…」。
   違反「raw/solutions 為唯一正本」的規則，且會隨正本修改而漂移。需要重寫成正規摘要頁。
2. **`study/problems-view/` 是歷次不同管線的混合體**。以 `gen_problems_view.py --check --all` 實測 100 頁：
   20 頁與現行管線一致、34 頁未補清單空行（清單被壓成 `<br />` 沒有 `<ul>`）、2 頁未開 nl2br、
   44 頁以上皆非。其中 **35 頁的數學式未遮罩就送進 markdown**，`&` `<` `>` 被轉義、`\\` 被吃掉，
   **這些頁的 KaTeX 實際渲染失敗**（`\begin{cases}` 首當其衝）。清單見 log 附註或重跑 `--check --all`。
   全庫重建會一次改動約 80 頁，應當成獨立批次作業。

---

## 2026-08-21（同日續二）六題先驗算後補圖：RC-2011-3 / RC-2008-2 / RC-2010-1 / RC-2006-2 / RC-2017-1 / RC-2004-3

使用者要求「在畫圖前先檢查解題的正確性」。四題（RC-2010-1、RC-2017-1、RC-2006-2、RC-2004-3）
以獨立 agent 深查、全部數字用 python3 重算並由本人複核；RC-2011-3、RC-2008-2 沿用前一則的結果。
**結論：六題沒有一題能直接畫圖**，其中 RC-2010-1 的錯誤改變答案本身。

### 一、RC-2010-1（圓形螺旋柱）——答案改變

- **$P_u$ 公式漏掉 $0.85$。** 原式 $P_u = f'_{cc}(A_{ch}-A_{st}) + f_yA_{st}$。
  決定性反證：令 $\rho_s = 0$（完全不配螺旋筋）代入得 1,649 tf $= 0.97P_y$——
  沒有橫向鋼筋的柱在蓋層剝落後還留 97% 承載力，物理上不可能。
  $0.85$ 是「圓柱試體強度→構材內實際強度」的折減，與撓曲的 Whitney 應力塊無關（原稿 §3 陷阱❸講錯），核心混凝土一樣要乘。
- **改採 MacGregor 式**（使用者定案）：$P_u = 0.85f'_c(A_{ch}-A_{st}) + 4.1f_L A_{ch} + f_yA_{st}$。
  這是唯一能反推出 $\rho_{s,\min}$ 係數 0.45（理論 0.4146）的一式，與檔案自述一致。
- **$\rho_s$ 定義統一為 $4A_{sp}/(D_c s)$**（分母核心量到螺筋外緣，與 $A_{ch}$ 同基準，且保住 $f_L = \rho_s f_{yt}/2$ 恆等式）。
  原稿用 $4A_{sp}/[(D_c-d_b)s]$，大 1.9% 且混用兩套基準。
- **修正後的數字：** $\rho_s = 0.00747$、$f_L = 15.69$、$f'_{cc} = 414.3$、
  蓋層損失 $233.9$ tf vs 圍束補償 $233.6$ tf、**$P_u = 1{,}697$ tf $\approx P_y = 1{,}697$ tf（差 0.02%，零餘裕）**。
  原稿的 1,880 tf 與「$P_u > P_y$ ✅ 通過」作廢——它把 0.02% 的邊界講成 10.8% 的餘裕，
  且與自己「$\rho_s < \rho_{s,\min}$ ❌」的判定互相矛盾。修正後兩項同時不通過，才自洽。
- **螺距 $s = 10$ cm 不是題目給的。** agent 從原卷 PDF 取出第一題圖上的全部文字物件，
  只有「主筋 12-#10」「#4 螺筋」「68 cm」「75 cm」四項，**無間距標註**（同卷第二題倒是有標「D13 @ 10 cm」）。
  已改寫為明示的假設，並新增 §5⑤「不依賴假設的作法」（令 $\rho_s = \rho_{s,\min}$ 反推）。
- 設計建議由 $s \le 9.4$ 改為 $s \le 9.20$ cm；$\phi P_{n,\max}$ 補上「$\rho_s$ 不足時不具螺旋柱優待」的但書。
- 附圖 `RC-2010-1-pm-viz.html` 原本把**圓柱當成 75×75 方柱**（$A_g$ 高估 27%）且用橫箍柱的 0.80/0.65，
  已改為等面積方形 66.47 cm、螺旋柱 0.85/0.75，並加上「本圖僅為形狀示意」的警語。

### 二、RC-2004-3（圍束箍筋）——建議值違反自己算出的上限

- $s \le 7.36$ cm 卻進位寫成 7.4 並建議「7 或 **7.5** cm」。間距上限只能**無條件捨去**，7.5 直接不合格 → 改為 $s = 7$ cm。
- §5①「公式一**永遠**較公式二嚴」是錯的。門檻為 $A_g/A_{ch} > 1.3$：50/65 cm 方柱由公式一控制，
  70/100 cm 就換公式二控制——邊長超過約 65 cm 的方柱都會翻轉。已補上對照表。
- $h_c$ 定義自相矛盾（標「中心到中心」卻用外緣值 42）。**全庫統一量到箍筋外緣**（使用者定案），
  故 $A_{ch} = h_c^2$ 成立；`RC-2009-1` 的舊版定義也一併加註統一。
- 補上 $s_x = 10 + (35-h_x)/3$ 的完整推導（$h_x = 18.46 \to 15.51 \to$ 取上限 15，本題結果巧合相同）、
  加密區外的 $s \le 15$ cm、以及「保護層 4 cm 是假設」的明示。

### 三、RC-2017-1（加大柱雙折線）——解法對，但附圖用了自己禁止的方法

- §4 確實對雙折線分區積分（$C_c = 133bc$），$M_{n,b} = 89.3$ tf·m 重算吻合；
  掃描 $c = 5\sim90$ cm 確認 $M_n$ 極大值就在 $c_b$。**主體零錯誤。**
- 但 `RC-2017-1-pm-viz.html` 用 `Cc = 0.85*fc*a*b`——正是 .md 自己列為「陷阱 #1」的做法，
  $C_c$ 高估 **14.1%**、$P_{n,b}$ 高估 14.5%。已改寫為雙折線數值積分，
  重算得 $P_b = 196.5$ tf、$M_b = 89.31$ tf·m、$\varphi M_b = 58.49$，與正文完全一致。
- $e = 0$ 取 $0.8f'_c$ 得 634 tf 沒有論證。雙折線下 $P(\varepsilon)$ 的峰值在 $\varepsilon = 0.002$ 為 **745 tf**
  （該處鋼筋 $f_s = 4{,}080 < f_y$ 尚未降伏）。已在 §4 Step 3 並陳兩個定義與完整數值表。
- §5 爭議3「題目未明確說明 8 支 D25 的排列」是**事實錯誤**：考卷原文寫「分布於長向之兩邊，保護層 6.5cm」，
  圖1 也畫得清楚。真正的歧義是**根數**（文字 8 支 vs 圖上含舊筋共 16 支），已改寫並附兩種讀法的完整數字。
- fig-1 的 alt 描述一張不存在的雙 panel 圖（「左為原柱、右為加大後」），實際只有一張；已改。

### 四、RC-2006-2（細長柱）——數值全對，缺一個規範步驟

- $M_c = 36.5$ tf·m 逐項重算吻合，符號約定內部一致（318-02 原生組合），$I_{se}$ 的 6 根 @18 cm 沒數錯。
- 缺 **$M_{2,\min} = P_u(1.5+0.03h) = 12.0$ tf·m** 的檢核（$27 > 12$ 不控制，答案不變，但卷面省略會扣分）；
  已補上，並附「若由 $M_{2,\min}$ 控制則 $C_m$ 須取 1.0」的配套規定，以及 $kl_u/r < 100$、界限上限 40 兩項檢核。
- §5 有一格 `$|M_1/M_2|$` 未跳脫 `|`，整張表不渲染；已改為 `\lvert…\rvert`。$E_c$ 精度 250,995 → 250,998。
- **跨檔**：`methods/moment-magnifier-method` 把 318-14 新慣例（單曲度取負）配 318-02 舊公式，
  照它自己的規則算本題會得「不需放大、$M_c = 27$」，與本題直接衝突。已補兩版對照表並修正 $C_m$ 表列與相關題連結。

### 五、向量圖解：六題共 17 張

每張都對應一個具體的錯，產圖腳本檔尾對 §4 公佈值做 assert（六支腳本共 97 項檢核，在有 structdraw.py 的環境下全數通過）：

| 題號 | 張數 | 最關鍵的一張 |
|------|:---:|------|
| RC-2010-1 | 3 | 圖 2 $P_y$/$P_u$ 三段分解——蓋層損失 233.9 vs 圍束補償 233.6，並把漏 0.85 的錯誤式並排讓它爆表 |
| RC-2004-3 | 2 | 圖 2 五個間距上限長條圖，畫出 7.4 與 7.5 越線的位置 |
| RC-2017-1 | 4 | 圖 3 雙折線分區積分 vs Whitney 疊圖，標出 $C_c$ 差 14.1% |
| RC-2006-2 | 3 | 圖 2 單曲率 vs 雙曲率的變形＋彎矩圖對照 |
| RC-2011-3 | 3 | 圖 3 $\phi_y$ 彈性 NA vs $\phi_u$ Whitney NA 雙應變圖 |
| RC-2008-2 | 3 | 圖 3 P-M 四點定位，同時標標稱峰值 87.68 與設計峰值 64.90 |

- 新增 `scripts/apply_figs.py`：把圖與圖說插回正本（圖 1 到 §2 之前、其餘到 §5 之前）並重建 problems-view，**冪等**。
- `render.py` 溢出／XML 檢查全數 0 個需修正；六題的 problems-view 已重建並通過 `--check`。
- RC-2011-3 的圖採**解讀 A**（$P_n = 0.9P_b$，使用者定案），腳本檔頭已註明。

### 待辦（本次未做）

1. φ 公式仍有 3 份用舊式（RC-2004-2、RC-2015-2、RC-2015-3），未統一為現行式。
2. `study/lecture-RC-U1-2.html` 的範例 D 仍寫 $P_u = 1{,}880$ tf，且「$\rho_{s,\min}$ 推導」段落用它自己的公式推不出來——需同步本次 RC-2010-1 的修正。
3. `wiki/concepts/PM-INTERACTION-DIAGRAM.md` 等衍生層已於前一則修過，但 `RC-2010-1`、`RC-2004-3` 的相關概念頁尚未逐一比對。
4. 前一則列出的兩件事（RC-2023-1 摘要頁是正本複本、problems-view 35 頁數學式壞掉）仍未處理。

## 2026-08-21 XCHECK：RC 梁題七題複核與改正

**範圍：** RC-2023-2、RC-2011-2、RC-2007-1、RC-2015-2、RC-2016-1、RC-2024-1、RC-2019-1
（全為 RC-U1-1 梁彎矩，RC-2016-1 副分類 RC-U3-3）
**方法：** 逐式獨立重算（Python，非重讀原文）＋比對 `raw/exams/` 原卷 PDF ＋放大附圖判讀 ＋比對全庫既有約定。
完整報告：`複核報告_RC梁題七題_2026-08-21.md`（庫根目錄）。

### 一、RC-2015-2：主線答案改了（最嚴重的一件）

原解取「最大鋼筋量」$\varepsilon_t = 0.004$ 得 $\varphi M_n = 114.0$ tf·m。**答案位置錯**。

原卷寫「在**適當設置拉力鋼筋後**，此梁斷面可具有之最大設計彎矩強度」——$A_s$ 是可調變數，
所求為 $\max_c[\varphi M_n]$。掃描結果峰值在**拉力控制界限** $\varepsilon_t = 0.005$：

| $\varepsilon_t$ | $A_s$ | $M_n$ | $\varphi$ | $\varphi M_n$ |
|---|---|---|---|---|
| 0.004 | 62.97 | 139.55 | 0.815 | 113.7 |
| 0.005 | 56.27 | 127.53 | 0.900 | **114.8 ← 峰值** |
| 0.006 | 50.78 | 116.98 | 0.900 | 105.3 |

$\varphi$ 相對自身漲 10.4%、$M_n$ 只掉 8.6% → 折點極大值。**用舊式 φ 算結論一樣**（113.97 < 114.78）。
旁證：同卷第一題 RC-2015-1 用了一模一樣的句型（「在適當調整軸壓載重後…」），已於 2026-08-21 定案在拉力控制界限。

- 主線改為 114.8 tf·m（$A_s = 56.27$、$c = 23.63$、$\varphi = 0.90$），$\varepsilon_t = 0.004$ 保留為對照，附六列掃描表證明單峰。
- §5 抵換表的「最大韌性 φMn 約 9.5 tf·m」**錯一倍**，實算 18.6（$M_n = 20.7$，$A'_s$ 落在拉力區的 14,351 kgf 那一項漏掉會少 3%）；同表 $\mu \approx 2.0$ 實算 1.87。整表重做。
- φ 過渡區公式由舊式改為現行式（0.817 → 0.815）。**[[solve-design-vs-nominal]] 的待統一清單剩 RC-2004-2、RC-2015-3。**

### 二、RC-2011-2：兩個實質問題 + 算術

1. **漏檢 $\varepsilon_t \geq 0.004$。** $\varepsilon_t = 0.002771 < 0.004$，依土木401／ACI §9.3.3.1
   **$A_s = 0.9A_{sb}$ 是規範禁止的超筋斷面**。出題者給 0.9 就是要看這個。已補 §5 ②。
2. **附圖尺寸鏈歧義。** 右側「10→90→10」是背對背箭頭的連續尺寸鏈，直讀為 $h=110$、$d=100$
   → $\varphi M_n = 358.7$ tf·m。**定案採原讀法 $h=100$、$d=90$**：量像素後翼板 10 cm 與底部保護層 10 cm
   都是 35～38 px、全高 354 px ≈ 101 cm，整張圖只有對 $h=100$ 才合比例，是「90」的下箭頭畫錯位置。
   已在 §1 圖說與 §5 ⑥ 明寫歧義並留檔兩組數字。
3. **算術：** $C_c$ 626,630 → **627,103**；連鎖修正 $A_{sb}$ 149.2→149.31、$A_s$ 134.3→134.38、
   $a$ 37.40→37.43、$c_u$ 46.75→46.79、$\varepsilon_t$ 0.002775→0.002771、$\phi$ 0.711→0.7105、
   $M_n$ 418.3→418.7、$\varphi M_n$ 297.4→**297.5**、$k_yd$ 40.94→40.95。$\mu_\phi$ 仍為 1.53。
4. §5 ① 的 $A_{sb,\text{web}}=120.9$ 與 $A_{sb,\text{rect}}=121.1$ 自相矛盾（同一個量），統一為 120.97 並補 $\rho_b$ 推導。
5. §5 ③ 「矩形應力塊力臂較大所以中性軸要更深」因果講反——$k_yd$ 是幾何量（轉換斷面一次矩），
   與載重無關；$c_u$ 才由力平衡決定。已改寫，並註明兩者深淺無普適因果。

### 三、RC-2016-1：結論對，過程有三處要補

1. **漏算梁端正彎矩。** $M_E = 16.5 > 0.9M_{D,\text{end}} = 8.44$，地震反向那端**翻號**成 $+8.06$ tf·m。
   小於跨中 9.375 故底筋仍由跨中控制、答案不變，但組合表必須有這一格。已新增「組合四」與表列。
2. **Step 7 不等式寫反**（原寫 $7.35 < 7.23$，實為 >），且 $A_s$ 單位打成 tf·m。已改寫為表格。
3. **耐震底筋規定比的是彎矩強度不是面積。** 實算 $M_{n,\text{bot}}/M_{n,\text{top}} = 19.84/38.41 = 0.517 \geq 0.50$ ✓（僅餘 3%）；
   面積比 0.535 較樂觀、**方向固定偏不保守**。新增 §4 Step 8。
4. $\rho_{\max}$ 由舊制 $0.75\rho_b$（0.02137）改為 $\varepsilon_t \geq 0.004$（$A_{s,\max} = 45.52$ cm²），與 RC-2024-1 統一。
5. 補 4-D22 的間距檢核（$s = 5.37$ cm ✓）與 $d = 63.9 \approx 63$ 的相符性。

### 四、RC-2023-2：算式全對，但原卷條件互相矛盾

原卷同時要求「8 根 D32 **採雙排排列**」與「間距**均依規範最小值**」，在 $b_w = 30$ 下不可能同時成立：

$$s_{\text{clear}} = \frac{30 - 8 - 2 - 4(3.22)}{3} = 2.37 \text{ cm} < d_b = 3.22 \text{ cm}\ ✗$$

三排（3+3+2）才合格，$d$ 由 60.53 掉到 58.38、$\varphi M_n$ 由 **136 → 130.6 tf·m（−3.9%）**。
主線維持 4+4（依原卷文字、坊間通行），§1 與 §5 ① 明寫矛盾並附對照表。
順帶記下一個結構：**換排列只改力臂，不改 $c$／$a$／$f'_s$**（後者由力平衡決定，與 $d$ 無關）。

### 五、RC-2019-1：進位

$M_u/f_y = 8{,}572{,}000/4200 = **2040.95**$（原寫 2041.4）→ 常數項 213.1 → **212.69** → $A_s$ 45.7 → **45.5**（精解 45.52）。
原答案偏保守 0.4%、§4.6 自我驗算也自洽，但常數項本身是錯的。另補 $\varepsilon_t = 0.00450 \geq 0.004$ 的延性檢核。

### 六、判定無實質錯誤

**RC-2007-1、RC-2024-1** 全部複算相符。各補一件：
- RC-2007-1：層間距寫法不一致（文字說取 3 cm、計算用 2.87）已統一；新增「餘裕只有 0.9%」的敏感度表
  （層間距取 4.0 cm 時 $\varphi M_n = 70.20 < M_u$ 就不足），並註明備案 7-D29 **排不成 4+3**（$s = 2.84 < 2.87$）須三排。
- RC-2024-1：新增高強度鋼筋的拉力控制界限說明（$\varepsilon_{ty}+0.003$，SD690 為 0.006382，不是 0.005）。

### 七、跨檔同步

- `wiki/code-ref/ACI-318.md` §21.2.1/21.2.2：拉力控制界限由固定 0.005 改為 $\varepsilon_{ty}+0.003$，
  補 §9.3.3.1（梁 $\varepsilon_t \geq 0.004$）一列，並加高強度鋼筋警告框。
- `wiki/problems/` 七頁摘要：標題答案、核心考點、關鍵步驟、陷阱、標籤全部同步。
- `raw/json/question_index.json`：七題 `verificationStatus` 改 **verified**，`tags` 由正本 §標籤 重新抓取
  （RC-2011-2 9→13、RC-2015-2 8→10、RC-2023-2 8→10）。
- `study/problems-view/` 七頁以 `scripts/gen_problems_view.py` 單題重建，重跑 `--check` 得 **same=7**（管線冪等）。
  未動 `--all`。

### 待辦（本次未做）

1. φ 舊式仍有 2 份：RC-2004-2、RC-2015-3。
2. 前兩則列出的兩件事（RC-2023-1 摘要頁是正本複本、problems-view 35 頁數學式壞掉）仍未處理。
3. 本次七題皆無向量圖解（`figs/`），RC-2015-2 的 φMn–εt 掃描曲線與 RC-2011-2 的兩種尺寸讀法對照圖值得補。
4. `_to_delete/patch-2026-08-21.tgz` 為本次套改用的暫存包，可刪。

## 2026-08-22 XCHECK：RC 剪力／扭力題五題複核與改正

**範圍：** RC-2020-2、RC-2014-3、RC-2009-3、RC-2017-2、RC-2023-3（全為 RC-U2-1，副分類：RC-2017-2 → RC-U1-2、RC-2023-3 → RC-U2-2）
**方法：** 逐式獨立重算（Python，非重讀原文）＋以 `pdftotext`／`pdftoppm` 取回 `raw/exams/` 原卷原文與附圖逐格判讀
＋依使用者指示「原卷規範為主線＋最新規範（土木 401-112／ACI 318-19）對照」。

### 總表

| 題號 | 判定 | 主線答案（改後） | 改前 |
|---|:---:|---|---|
| RC-2020-2 | 🔴 主線錯 | (一) **不可** d 偏移；(二) $s_{\max}=16.6$ cm；(三) 97.8 tf | (一) 可以；(二) 24.1 cm；(三) 97.8 tf |
| RC-2014-3 | 🔴 主線錯 | 18.75 / **32.40** / **10.57** tf | 18.75 / 28.01 / 16.87 tf |
| RC-2009-3 | 🔴 幾何判讀錯 | $a=50$ cm、$\theta=45°$、$P_{\max}=$ **127.5 tf**（斜壓桿控制） | $a=30$、$\theta=59°$、136 tf（CCT 節點控制） |
| RC-2017-2 | 🟠 定義不一致 | $V_u=$ **195.7 tf**、每側 **17 支 D19**、$L_{\min}=155$ cm | 100.8 tf、9 支、80 cm |
| RC-2023-3 | 🟡 算術／單位 | 7.425 tf、$e=10.4$ cm（數值不變，修 $\phi V_c$ 與 tf·m 換算） | 同（$\phi V_c$ 12,370→12,336；$\phi T_{th}$ 7.745→**0.775** tf·m） |

### 一、RC-2020-2：附圖判讀改變小題(一)與(二)（最嚴重）

放大 `RC-2020-2-fig-1.png` 側視圖：全深 90 cm 對應 502 px，$w_u$ 的載重箭頭起始線在距梁頂 380 px ≈ 68 cm、
箭頭尖端落在 70 cm 處——**正是下翼板頂面**。倒 T 型「獨立」梁的載重是壓在下翼板（拉力側）上，
即承托梁（ledger beam）的懸吊式載重，§9.4.3.2 條件 (b)「載重施加於構材頂部或其附近」**不成立**。

→ 臨界斷面取**支承面**，$V_u = w_uL/2 = 60$ tf（非 47.4 tf）。
$V_s = 60/0.75-26.07 = 53.93$ tf，**超過 $2V_c = 52.15$ tf（僅 3.4%）**，
規範上限因此從 $\min(d/2,60)=42$ 落到 $\min(d/4,30)=21$ cm；強度需求 $894{,}005/53{,}926 = 16.58$ cm 控制。

原文的 24.1 cm **偏不安全 45%**，且兩個分支（是否偏移、d/2 還是 d/4）同時錯。
另修：$A_{v,\min}$ 係數 0.35 → **3.5**（原文低 10 倍，結論不變）；§5 新增懸吊鋼筋 $A_h \ge w_u/(\phi f_y) = 4.76$ cm²/m。

### 二、RC-2014-3：軸壓上限漏乘修正因子、軸拉走錯路徑

**Case 2（軸壓）：** 土木 401-100 的軸壓上限是 $0.93\sqrt{f'_c}b_wd\sqrt{1+0.0284N_u/A_g}$，不是 $0.93\sqrt{f'_c}b_wd$。
$N_u/A_g = 11.905$ → 因子 $\sqrt{1.3381} = 1.1568$ → $V_c = 28{,}011\times1.1568 = 32{,}402$ kgf。原文 28.01 tf **低估 13.5%**。
（$M_m = -27{,}500 < 0$ 時規範規定直接取此上限，這一點原文是對的。）

**Case 3（軸拉）：** $M_m$ 條文明寫「承受軸壓力之構材」。軸拉應走專用式
$V_c = 0.53(1+0.0284N_u/A_g)\sqrt{f'_c}b_wd = 0.53\times0.6619\times16.733\times1800 = 10{,}566$ kgfã€‚
原文把 $N_u<0$ 代入 $M_m$ 得 16.87 tf，比**無軸拉**的簡化式 15.96 tf 還高，物理上站不住腳；
該讀法已在正本 §4 Case 3 留檔（原卷「可能使用之公式」只印 $M_m$，故坊間有此解）。

趨勢檢核：32.40（壓）> 18.75（無）> 10.57（拉）✓ 單調。

### 三、RC-2009-3：原卷尺寸鏈讀錯，全題幾何重算

原卷底部是**七段連續尺寸鏈 20｜30｜20｜30｜20｜30｜20 = 170 cm**，四段 20 cm 是四塊鈑
（左支承／左載重／右載重／右支承），且原圖把**「純彎區」標註在中央那段 30 cm 上**。
故支承鈑中心 10／160、載重鈑中心 60／110 → $L = 150$ cm、$a = 50$ cm、$\theta = 45°$。
原文讀成「支承至載重 = 30、純彎區 = 20」（$L = 80$、$\theta = 59°$），與圖上鈑位置矛盾，
也讓題目給的「承壓鈑 20 cm」無處可用。

重算（$T = 0.5P$、$F_{\text{diag}} = 0.7071P$、$w_s = 28.28$ cm）：

| 限制 | 改後 | 改前 |
|---|:---:|:---:|
| 斜壓桿（$\beta_s=0.75$） | **127.5 tf ← 控制** | 149.8 |
| CCT 節點（承壓／背面／壓桿面三面同值） | 136.0 | 136.0 ← 原控制 |
| 拉力桿降伏 | 144.6 | 241.1 |
| CCC 節點／水平壓桿 | 170.0 | 170.0 / 283.3 |

45° 幾何使 CCT 三面同時為 136.0 tf，可當計算正確的自我驗證。破壞模式仍為脆性，但控制項改為**斜壓桿劈裂／壓碎**。
§5 補：承壓鈑 20→30 cm 可把控制項推向拉力桿降伏（延性）。

### 四、RC-2017-2：介面剪力定義改為與第一題一致（經使用者確認）

原文用均勻 $0.8f'_c \times A_{\text{wing}} = 100.8$ tf，但 RC-2017-1 Part (c) 自己是用**雙折線分區積分**算的：
$c_b = 37.66$ cm，轉折點 $x_{\text{peak}} = c_b/3 = 12.55$ cm **落在翼板（0～15 cm）之內**，
翼板應力 168 → 210（峰值）→ 189.5，積分得 $C_{c,\text{wing}} = 114{,}454$ kgf（均勻假設低估 12.0%）。
且壓力筋在 $d' = 6.5 < t_w = 15$，**整支埋在新混凝土內**，其 $C'_s = 81{,}288$ kgf 同樣必須跨越介面。

→ $V_u = 195{,}742$ kgf、$A_{vf} = 62.14$ cm²、**17 支 D19**（原卷 $A_b = 3.871$；用實際 D19 的 2.865 則需 22 支）。
$V_n = 260{,}989$ kgf，介面應力上限 $0.2f'_c = 42.0$ kgf/cm² → $L_{\min} = 155.4$ cm、D19 @ 9 cm。
三種定義（100.8／114.5／195.7 tf）已列表對照於正本 §5。

另修兩處：① $V_n$ 上限誤引「5.52 MPa」那一行（該行是**未粗糙化**用），粗糙面應為
$\min(0.2f'_c,\ 3.3{+}0.08f'_c,\ 11\ \text{MPa})$，本題仍由 $0.2f'_c$ 控制故 $L_{\min}$ 數值不受影響；
② 錨定不能當鋼筋伸展長度（D19 需 $\approx105$ cm），須走 ACI 318 第 17 章化學植筋＋新翼側彎鉤／頭錨。
③ 記錄原卷自身筆誤：D19 的 $A_b$ 實為 2.865 cm²，3.871 是 D22。
④ 工程結論：柱淨高 300 cm 時可用傳遞長度 ≈150 cm < 155.4 cm，本題真正被卡住的是介面應力上限，不是植筋量。

### 五、RC-2023-3：數值正確，修算術／單位並補題意歧義留檔

- $\phi V_c$：12,370 → **12,336** kgf（$0.53\sqrt{280}\times35\times53\times0.75$）
- $\phi T_{th} = 77{,}515$ kgf·cm $=$ **0.775** tf·m（原文寫 7.745 tf·m，差 10 倍；$1$ tf·m $= 10^5$ kgf·cm）
- $T_{th}$ 由 103,262 → **103,354** kgf·cm（SI 路徑），kgf 制係數由 0.266 → **0.2652**（精確值），兩法互驗差 0.4%
- $e_{\max} = 10.44$ cm（不變）
- 新增「所能承受」的**題意歧義留檔**：讀法 A（需求，本解主線）7.425 tf → $e = 10.4$ cm；
  讀法 B（容量）$5\phi V_c = 61.7$ tf → $e = 1.26$ cm。採 A 因讀法 B 會讓題給的 $W_u = 2.5$ tf/m 完全用不到；
  但同庫 `RC-2020-2` 小題(三)「所能抵抗」確為容量題、句型幾乎相同，故建議考場兩者並寫。

### 六、依最新規範對照（五題都加了 §5 專節）

| 題號 | 原卷指定 | 401-112／ACI 318-19 下的答案 | 條文變動 |
|---|---|---|---|
| RC-2020-2 | 108 年規範／401-100 | **相同**（16.6 cm／97.8 tf） | $d$ 偏移、間距門檻、$V_{s,\max}$、$A_{v,\min}$ 均未變 |
| RC-2014-3 | 401-100 | **15.96／19.53／12.39 tf** | $M_m$ 法與軸拉專用式**全面廢除**，改線性項 $N_u/(6A_g)$ |
| RC-2009-3 | ACI（未指版） | **相同**（127.5 tf） | $\beta_s$ 術語改「邊界／內部壓桿」、新增 $\beta_c$（本題 = 1.0）、無腹筋懲罰 $0.60\lambda \to 0.4$ |
| RC-2017-2 | 401-100 | **相同**（195.7 tf／17 支） | 摩擦剪力法幾乎未改；318-19 明訂 $f_y \le 420$ MPa |
| RC-2023-3 | 401-110 | **相同**（7.425 tf／10.4 cm） | 401-110 本即以 318-19 為藍本 |

### 七、施作內容（下游同步）

- `raw/solutions/{RC-2020-2,RC-2014-3,RC-2009-3,RC-2017-2,RC-2023-3}/*.md`：正本全面改寫（含 §1 附圖／原卷原文重述、§3.5 變數層次、§4 逐步計算、§5 最新規範對照）。
- `wiki/problems/` 五頁摘要：H1 標題答案、核心考點、關鍵步驟、公式、陷阱、標籤、「依最新規範對照」段全部同步。
- `raw/json/question_index.json`：五題 `tags` 依正本 §標籤重新抓取（2020-2 6→10、2014-3 8→10、2009-3 12→15、2017-2 7→11、2023-3 8→10）。`verificationStatus` 維持 `unverified`（待人工複核）。
- `dashboard-data.js`：五題 tags 同步（100 列結構未動，已驗證每列 7 元素）。
- `wiki/index.md`、`wiki/by-year.md`：五題一行說明改為含改後答案。
- `study/problems-view/` 五頁以 `scripts/gen_problems_view.py` **單題**重建（written=5，未動 `--all`）。
- `wiki/code-ref/ACI-318.md`：§22.5 剪力表整段重寫（原「含軸力修正 $= \frac{1}{6}\sqrt{f'_c}(1+N_u/14A_g)b_wd$」是錯的，
  318-19 應為 $[0.53\lambda\sqrt{f'_c}+N_u/(6A_g)]b_wd$）；補 $\lambda_s$ 尺寸效應、$V_{s,\max}$、$A_{v,\min}$ kgf 制係數、
  $d$ 偏移三條件、舊制 $M_m$／軸拉專用式對照框；§22.7 補 $T_{th}$ 的 kgf 制係數 0.265（$T_{cr} = 1.06$）；
  新增 **§22.9 摩擦剪力法** 與 **第 23 章 壓拉桿模式** 兩節。

### 七之二（同日續）：橫向一致性掃描後的補正

用 `grep -rln` 掃全庫哪些非 problems 頁面引用了這五題，發現三處與改後主線**直接矛盾**，一併同步：

- `wiki/traps/SHEAR-CRITICAL-SECTION.md`：原文兩處把 RC-2020-2 當成「載重在頂面 → **仍可** $d$ 偏移」的
  範例（還標了 verified），與改後結論完全相反。已改為「RC-2020-2 正是條件 (b) 不成立、**不可** 偏移的範例」，
  並補上「兩種讀法相差 45%」與「務必放大附圖確認載重箭頭終止高度」。
  另修同頁「忘記軸力的影響」一列：原寫「壓用 $140A_g$、拉用 $35A_g$」（$140$ 無出處），
  已改為舊制的 $\sqrt{1+N_u/(35.2A_g)}$ 上限加強與軸拉專用式，並註明 318-19 改用 $N_u/(6A_g)$。
- `wiki/concepts/SHEAR-STRENGTH.md`、`wiki/concepts/STIRRUP-DESIGN.md`、`wiki/philosophy/usd-shear.md`：
  RC-2020-2／RC-2014-3／RC-2009-3／RC-2017-2 的一行說明改為含改後結論。
- `study/study-RC-U2-1.html`（命題情報頁）：內嵌資料列中 RC-2020-2、RC-2014-3 兩題的
  description 與 tags 同步（其餘三題該頁未列為主考點，無資料列）。

> 註：`wiki/traps/`、`wiki/concepts/`、`wiki/philosophy/` 依 CLAUDE.md 規則 4 屬 compile 輸出。
> 本次比照 2026-08-21 XCHECK 的做法**手動同步**，以免下次 `compile-all` 之前 wiki 顯示與正本矛盾的內容；
> 來源（`raw/solutions/`）已先改，故下次 compile-all 不會被蓋回舊結論。

### 驗證

- `gen_problems_view.py . <五題> --check` → **same=5**（管線冪等、HTML 與正本一致）
- `dashboard-data.js` 100 列全數 JSON 解析通過、每列 7 元素、行數 130 未變
- `question_index.json` 100 題解析通過，僅 tags 陣列有差異
- 關鍵新值已出現在 problems-view：16.6 cm／不可以（NO）／32,402／10,566／127,500／45°／195,742／17 支 D19／0.775／12,338
- 舊值僅殘留在**刻意保留的對照段**（RC-2020-2 的 24.1 cm 對照、RC-2009-3 的 59° 讀法 B 對照）；
  `7.745 tf·m`、`28,010 tf` 等錯誤值已清零

### 待辦（本次未做）

1. 五題皆無向量圖解（`figs/`）。最值得補的三張：RC-2020-2 的「載重在下翼板 vs 梁頂」對照圖、
   RC-2009-3 的尺寸鏈兩種讀法與 45° STM 桁架圖、RC-2017-2 的翼板雙折線應力分布積分圖。
2. 五題 `verificationStatus` 仍為 `unverified`，待使用者人工驗算後通知改 `verified` 並 ingest。
3. `RC-2014-3` 的 $M_m$ 軸拉讀法（16.87 tf）是否有坊間標準解答可交叉比對，尚未查證。
4. 前幾則 log 列出的舊待辦（φ 舊式 RC-2004-2／RC-2015-3、problems-view 35 頁數學式壞掉）仍未處理。

---

## 2026-08-22 XCHECK：RC 預力題五題複核與改正

**範圍：** RC-2011-5、RC-2006-4、RC-2004-5、RC-2023-4、RC-2012-1（全為 RC-U4-1；副分類：2011-5→RC-U4-3、2006-4→RC-U4-2、2004-5→RC-U4-3）
**方法：** 逐式獨立重算（Python，非重讀原文）＋以 `pdftotext -layout`／`pdftoppm` 取回 `raw/exams/` 原卷原文與附圖逐項判讀
（2004、2006 兩份原卷缺 Adobe-CNS1 語言包，先裝 `poppler-data` 才能正確抽出中文）
＋依使用者指示「**依最新規範（土木 401-112／ACI 318-19）計算**」，五題全部新增 §6 專節做逐條對照。

### 總表

| 題號 | 判定 | 主線答案（改後） | 改前 |
|---|:---:|---|---|
| RC-2011-5 | 🟡 算式全對，附註錯 | 18.75／183.34／10,417；110.64／2.12／**9,889**（不變） | 同 |
| RC-2006-4 | 🔴 §5 容許值錯，壓應力判定反轉 | 梁頂 +161.6 壓 **✅通過**；梁底 −106.3 拉 → **Class C 已開裂** | 兩者皆判「❌超限」 |
| RC-2004-5 | 🟡 主線全對，§5 數字打錯 | $M_{cr}=50.7$、$\phi M_n=66.3$ tf·m（不變） | 同 |
| RC-2023-4 | 🔴 上限引錯＋主線漏算 | $M_n=$ **22.5 tf·m/m**（含 $A_{s,\min}$）；僅絞線 18.5 為對照 | 18.5 tf·m/m |
| RC-2012-1 | 🔴 工法標記錯＋檢核不全 | 應力四值不變；工法 **先拉→後拉**；超限區段 **201 cm**；未開裂判定；錨定區 $0.70f_{pu}$ ❌ | 標為先拉法，只點自由端一點 |

### 一、RC-2023-4：兩處規範引用錯誤，其一改動主線答案（最嚴重）

**(1) $f_{ps}$ 上限配錯分支。** 無握裹腱的兩個分支是**公式＋上限成套**的
（土木 401-110 §20.3.2.4.1／ACI 318-19 §20.3.2.4.1）：

| 跨深比 | $f_{ps}$ | 上限 |
|---|---|---|
| $\ell/h \le 35$ | $f_{se}+700+f'_c/(100\rho_p)$ | $f_{se}+4200$（420 MPa）|
| $\ell/h > 35$ | $f_{se}+700+f'_c/(300\rho_p)$ | $f_{se}+\mathbf{2100}$（210 MPa）|

原文用 300 的公式配 4200 的上限（15,200），實際應為 13,100。$f_{ps}=12{,}119$ 兩者都過，
**答案不變但檢核形同虛設**（餘裕由「21%」修正為 7.5%）。
另：原文把判準寫成「簡支 vs. 懸臂」，規範判準是**跨深比**（$\ell/h=40$、$\ell/d_p=45.5$，兩種取法同分支）。

**(2) 漏算規範強制的最小握裹鋼筋（主線改變）。** 原卷寫「配置無握裹鋼絞線及**普通具握裹鋼筋，兩者間距均為 20 cm**」、
給了 $f_y=4200$、卷首並明訂「依土木 401-110 作答，未依規範作答不予計分」。
§7.6.2.3 對無握裹腱單向版強制 $A_{s,\min}=0.004A_{ct}$：

$$A_{ct}=20\times12.5=250\ \text{cm}^2 \Rightarrow A_{s,\min}=1.00\ \text{cm}^2/\text{條帶}$$
$$T=17{,}815+4{,}200=22{,}015,\quad a=3.083,\quad c=4.111,\quad \varepsilon_t=0.0131$$
$$M_n=22{,}015\times20.458\times5=\mathbf{22.5\ \text{tf·m/m}}\quad(\text{僅絞線 }18.5)$$

改判理由：$f_y$ 在舊讀法下完全用不到；「兩者間距均為 20 cm」不算鋼筋就沒有意義；
題目問的是 $M_n$（斷面完整標稱強度）。**兩讀法都已留檔於正本 §5-2，考場建議並寫。**
此項改動最需人工複核，`verificationStatus` 維持 `unverified`。

### 二、RC-2006-4：容許應力係數自創，壓應力判定整個反轉

原文用 $0.4f'_c=140$ 與 $3\sqrt{f'_c}=56.1$——**這兩個係數在土木 401 與 ACI 318 任何版本都查不到**。

| 位置 | 應力 | 正確容許值（§24.5） | 改前 | 改後 |
|---|---|---|:---:|:---:|
| 梁頂（持續載重） | 125.9 | $0.45f'_c=157.5$ | ❌ | ✅ |
| 梁頂（含瞬時活載） | 161.6 | $0.60f'_c=210$ | ❌ | ✅ |
| 梁底（拉） | 106.3 | U $2.0\sqrt{f'_c}=37.4$／T $3.2\sqrt{f'_c}=59.9$ | ❌超限 | **Class C（已開裂）** |

真正的結論不是「壓應力超限」，而是 $f_{bot}=106.3$ 為 $f_r=2.0\sqrt{350}=37.4$ 的 **2.84 倍**，
斷面在使用載重下必然開裂 → 屬 **Class C**，**未開裂全斷面彈性疊加只是名目值**，
撓度須用 $I_{cr}$、須做裂縫控制。此註記為本題完整得分的關鍵。
另修：版頂位置「35.93 cm」為筆誤（實際代入的 29.93 才對）；版頂容許壓應力 $0.4f'_{c2}=112 \to 0.60f'_{c2}=168$；
$I_c$ 精算 4,188,695（原 4,188,623，差 0.002%）、$S_{c,top}=280{,}622$／$S_{c,bot}=64{,}369$（比值 4.36）；
wiki 摘要頁「解題關鍵步驟 3」原本正負號寫顛倒、「圖形」誤記為「無」（實有 `RC-2006-4-fig-1.png`），一併更正。
$\gamma_c=2400$ kgf/m³ 為原卷未給之假設，已在 §5 標明（改 2300 則為 +153.2／−97.9，Class C 結論不變）。

### 三、RC-2012-1：工法標成「先拉法」，實為後拉法

原卷兩處直接推翻：① 「**在混凝土達 7 天強度時開始拉預力**」——先拉法是先張拉後澆置，不可能等混凝土硬化才張拉；
② 「忽略鋼鍵與**套管**所占有面積」——套管是後拉法專有。
數值不受影響（題目已叫我們忽略孔洞），但影響標籤、觀念，且使 §5 的錨定區上限檢核變得相關。

補三項原文缺漏：
1. **超限是一整段**：$f_{bot}(\xi)=15.63-28.53(\xi/610)^2 > 12.52 \Rightarrow \xi < \mathbf{201}$ cm，
   自由端起約梁長 1/3 全段超限（補充鋼筋須涵蓋此段＋$\ell_d$）。原文只點自由端一點。
2. **題目給的 $f_r$ 全文未用**：$f_r=2.0\sqrt{f'_{ci}}=31.3 > 15.63$ → **斷面未開裂**，
   故補救屬「配握裹鋼筋承擔拉力」而非重新設計斷面。這是原卷給 $f_r$ 的用意。
3. **鋼腱應力上限新舊制答案不同**：$f_{pi}=0.75f_{pu}=14{,}250$，
   舊制（318-11／401-100）「傳遞後 $\min(0.82f_{py},0.74f_{pu})=14{,}022$」→ ❌ 超 1.6%；
   318-14 起**該通則已刪除**，改為張拉時 $\min(0.80f_{pu},0.94f_{py})=15{,}200$ → ✅，
   但**後拉法錨定裝置處** $0.70f_{pu}=13{,}300$ → ❌ 超 7.1%。梁身斷面合法、錨定區須處理。
另修：補充鋼筋應力依 §24.5.3.2 為 $f_s=\min(0.6f_y,\,2100)$（原文寫 $0.5f_y$，本題 $f_y=4200$ 巧合同值 2,100，
但 $f_y$ 不同時會算錯）；$f_y$ 原卷未給，已標明為假設。

### 四、RC-2011-5：算式與六個答案全對，兩處附註錯

- §5① 表寫「$A_{c2}=A_{c1}+nA_{sp}$」→ $2500+6\times24=2644 \ne 2800$（**與題給矛盾**）。
  正確為 $A_{c2}=A_g+(n-1)A_{sp}$，$A_g$ 含導管孔：回推 $A_g=2680$、導管孔 $=180$ cm²。
  兩個要點：灌漿後孔要加回；鋼腱只加 $(n-1)$ 倍（$nA_{sp}$ 是先拉法不扣佔位的寫法）。
- §5③「四控制條件」的係數是 **MPa 制**（0.25／0.5／0.45）混進全篇 kgf/cm² 文件，
  已改為 kgf 制（$0.60f'_{ci}$、$0.80\sqrt{f'_{ci}}$、Class U $2.0\sqrt{f'_c}$、$0.45f'_c$／$0.60f'_c$）並附 SI 對照。
- 新增**方法歧義留檔**：腱應力的 $\Delta f_c$ 起算點。主線（讀法 A，含 $M_G$）9,889 與混凝土應力算法一致；
  若視 $M_G$ 為灌漿前已作用（讀法 B）則 $\Delta f_c=82.44$、$f_s=9{,}661$（差 2.3%）。兩組數字均留檔。
- 逐項複算相符：18.75／183.33／10,416.7；59.547／96.711／51.095／−94.595 → 110.642／2.116；120.33×6=722。

### 五、RC-2004-5：主線全對，§5② 數字打亂

- 複算相符：$\beta_1=0.80$、$f_{ce}=56.47$、$M_{cr}=5{,}069{,}695$ kgf·cm $=50.70$ tf·m、
  $\rho_p=0.001925$、$f_{ps}=15{,}751.3$、$\omega_p=0.0866$、$a=8.154$、$M_n=73.67$、$\phi M_n=66.30$ tf·m。
- §5② 「$\beta_1$ 若取 0.85 則 $f_{ps}=16{,}793$」**不可能**（大於 $f_{pu}=16{,}500$）。正確 **15,795**（$16{,}500\times0.9573$），
  比 15,751 大 0.28%——原文那句「約 0.3%」反而是對的，只有數字打亂。
- 補：$\varepsilon_t$ 判 $\phi$。$c=a/\beta_1=10.19$、$\varepsilon_t=0.003(80-10.19)/10.19=\mathbf{0.0206} \gg 0.005$ → $\phi=0.9$
  （與舊制 $\omega_p \le 0.36\beta_1$ 同結論）。$\omega_p$ 判準為 ACI 318-99 舊制，現行已刪除，改用淨拉應變。
- 補：近似式前提 $f_{se}\ge0.5f_{pu}$（本題 $0.6f_{pu}$ ✓）；有黏結腱**無 $f_{py}$ 上限**（上限只加在無黏結腱），
  故 $f_{ps}=15{,}751 > f_{py}=14{,}025$ 合法。
- 補：$\phi M_n/(1.2M_{cr})=66.30/60.84=1.09$，**餘裕僅 9%**，是脆性破壞警戒線的邊緣。

### 六、依最新規範對照（五題都加了 §6 專節）

| 題號 | 原卷指定 | 401-112／ACI 318-19 下的答案 | 條文變動 |
|---|---|---|---|
| RC-2011-5 | 未指定 | **相同**（六個值全不變） | 純彈性疊加未改；容許應力改 Class U/T/C 分級 |
| RC-2006-4 | 未指定 | 應力值**相同**，但判定改寫：壓應力 ✅、拉應力 → **Class C** | $0.45/0.60f'_c$、$2.0/3.2\sqrt{f'_c}$、$I_{cr}$、裂縫控制 |
| RC-2004-5 | 未指定（93 年為 318-99 世代） | **相同**（50.7／66.3） | $\omega_p \to \varepsilon_t$；$f_{ps}$ 式、$f_r$、$1.2M_{cr}$ 均未變 |
| RC-2023-4 | 土木 401-110 | **22.5 tf·m/m**（含 $A_{s,\min}$） | 401-110 本即以 318-19 為藍本，條文未動；是原文引用錯 |
| RC-2012-1 | 未指定（101 年為 401-100 世代） | 應力四值**相同**；鋼腱上限判定**改變** | 傳遞後通則刪除，改錨定裝置 $0.70f_{pu}$；補充筋 $0.6f_y\le2100$ |

### 七、施作內容（下游同步）

- `raw/solutions/{RC-2011-5,RC-2006-4,RC-2004-5,RC-2023-4,RC-2012-1}/*.md`：正本改寫
  （§1 補原卷原文核對、勘誤框、§4 補步驟、§5 改寫爭議點、**新增 §6 依最新規範對照**）。
- `wiki/problems/` 五頁摘要：標題／答案／核心考點／關鍵步驟／公式／陷阱／圖形欄／新增「依最新規範對照」段全部同步。
- `raw/json/question_index.json`：RC-2023-4 tags 8→10（新增 `跨深比分支`／`fps上限2100`／`最小握裹鋼筋`，移除 `L/dp比值`）、
  RC-2012-1 tags 8→9（`先拉法`→`後拉法`、`有黏結腱`→`有黏裹腱`、新增 `超限區段長度`）。其餘三題 tags 未動。
  五題 `verificationStatus` 維持 `unverified`。
- `dashboard-data.js`：同上兩題 tags 同步（100 列結構未動，已驗證每列 7 元素、行數 130 未變）。
- `knowledge_graph.html`：同上兩題 `p(...)` 節點 tags 同步。
- `wiki/index.md`、`wiki/by-year.md`：五題一行說明改為含改後答案。
- `study/problems-view/` 五頁以 `scripts/gen_problems_view.py` **單題**重建（written=5，未動 `--all`）。
- `study/study-RC-U4-1.html`：RC-2023-4、RC-2012-1、RC-2006-4 三筆內嵌資料列的 description 與 tags 同步。
- `wiki/code-ref/ACI-318.md`：**RC-U4 段整段重寫**——修正條文編號錯位（有黏結為 §20.3.2.3、無黏結為 §20.3.2.4）；
  補無黏結腱兩分支的**配對上限**（4200／2100）、$\gamma_p$ 取值表、$f_{se}\ge0.5f_{pu}$ 前提、有黏結腱無 $f_{py}$ 上限；
  新增 **§20.3.2.5.1 鋼腱應力上限新舊制對照**、**§24.5 Class U/T/C 全表**、**§7.6.2.3 最小握裹鋼筋**、
  **§21.2.2 預力構材 $\phi$**、**§9.6.2.1 $\phi M_n \ge 1.2M_{cr}$**、**後拉法三斷面定義**（含 $A_t=A_n+nA_{ps}$ 之勘誤）。
- `wiki/traps/PRESTRESS-FPS-FORMULA.md`：公式對照段整段重寫（兩分支成套上限、$\gamma_p$ 表、前提、$A_{s,\min}$、
  $\varepsilon_t$ 取代 $\omega_p$）；判斷流程重畫；陷阱表增列 5 列。
- `wiki/philosophy/prestress-philosophy.md`：RC-2023-4 一行說明同步。

> 註：`wiki/traps/`、`wiki/philosophy/`、`wiki/code-ref/` 中前兩者依 CLAUDE.md 規則 4 屬 compile 輸出。
> 比照 2026-08-21／08-22 兩次 XCHECK 的做法**手動同步**，以免下次 `compile-all` 之前 wiki 顯示與正本矛盾；
> 來源（`raw/solutions/`）已先改，故下次 compile-all 不會被蓋回舊結論。

### 驗證

- `gen_problems_view.py . <五題> --check` → **same=5**（管線冪等、HTML 與正本一致）
- `question_index.json` 100 題 JSON 解析通過、moduleId 無重複，僅 tags 陣列有差異
- `dashboard-data.js` 100 列全數 JSON 解析通過、每列 7 元素、行數 130 未變
- 關鍵新值已出現在 problems-view：180（導管孔）／9,661（讀法 B）／0.45f'c／Class C／15,795／0.0206／
  2100（上限）／22.5／201（超限區段）／0.70f_{pu}／後拉法
- 舊錯值僅殘留在**刻意保留的對照段**（RC-2023-4 的 $f_{se}+4200$ 兩處係兩分支對照表；RC-2006-4 的 0.4f'c／3√f'c 係勘誤引述）

### 待辦（本次未做）

1. **`RC-2007-4` 用了同一組自創容許值** $0.4f'_c$ 與 $3\sqrt{f'_c}$（正本 §1 表格與 §4①、§5），
   且據此求出的 $P_{\max}=25.3$ tf 是該題的**控制答案**——換成 Class U（$2.0\sqrt{f'_c}=37.4$）會直接改變答案。
   全庫掃描確認只剩這一題有此問題，建議列為下一輪 XCHECK 的第一順位。
2. RC-2023-4 主線由 18.5 改為 22.5 tf·m/m 屬**判斷性改動**（$A_s$ 未直接給數字），最需人工複核。
3. 五題皆無向量圖解（`figs/`）。最值得補的三張：RC-2012-1 的「懸臂梁彎矩圖＋偏心方向＋底纖維應力沿梁長變化（含 201 cm 超限區段）」、
   RC-2006-4 的「兩階段斷面切換與 $S_{c,top}/S_{c,bot}=4.36$ 的應力放大」、RC-2011-5 的「淨／變換／合成三斷面幾何對照」。
4. 五題 `verificationStatus` 仍為 `unverified`，待使用者人工驗算後通知改 `verified` 並 ingest。
5. 前幾則 log 列出的舊待辦（φ 舊式 RC-2004-2／RC-2015-3、problems-view 35 頁數學式壞掉）仍未處理。

---

## 2026-08-22（第二輪）XCHECK：RC 耐震題五題複核與改正

**範圍：** RC-2025-2、RC-2013-2、RC-2012-3、RC-2005-3、RC-2022-4（全為 RC-U3-3；副分類：2025-2→RC-U2-1、2013-2→RC-U1-2、2012-3→RC-U2-1、2005-3→RC-U1-1、2022-4→RC-U1-2）
**方法：** 逐式獨立重算（Python，非重讀原文）＋以 `pdftotext -layout`／`pdftoppm` 取回 `raw/exams/` 原卷原文與附圖逐項判讀
（2012 年附圖以 160 dpi 轉圖目視確認柱 60×60／12-#7／核心 48 cm、梁 50×60／頂 6-#8／底 4-#7）
＋依使用者指示「**依最新規範計算**」，五題全部新增 §6 專節。
**規範版本查證（網路）：** 土木 401-112 為 **2023 年 8 月**出版之現行版（後續僅 2024-06-24 勘誤表、2025-05-16 鋼筋焊接條文修訂，未出新版號）；
「公路橋梁耐震評估與補強設計規範」109 年底定稿、**110-03-23** 交技(110)字第 1105003536 號頒布，**交通部迄今未再更新**。

### 總表

| 題號 | 判定 | 主線答案（改後） | 改前 |
|---|:---:|---|---|
| RC-2025-2 | 🔴 密箍區外設計錯 | 密箍區 4 腳 D13@15（152 cm）**不變**；**一般區改 2 腳 D13@20**；第一支箍筋 **≤5 cm** | 一般區 2 腳@30，第一支 7.5 cm |
| RC-2013-2 | 🟠 密箍區外間距違規 | $s=12$ cm、5 腳 D13、$A_{sh}=6.35$ **不變**；**區外 15 cm**（非 19.3） | 區外「D13@15 或 **@19**」 |
| RC-2012-3 | 🔴 柱設計剪力差 2 倍 | $V_u=$ **25.17 tf**（原 50.33）；$s=9$ cm **不變**；**新增區外 13 cm** | $V_u=50.33$ tf、$s_{shear}=17.2$ cm |
| RC-2005-3 | 🔴 兩處疊加錯 | $T=1.25f_yA_s$、$V_{col}=M_{pr}/H$ ⇒ **$V_{jh}=131.5$ tf**（$\le\phi V_n=163.8$ ✓） | $V_{jh}=81.9$ tf |
| RC-2022-4 | 🟡 算式全對 | $L_p=0.595$、$\mu_\phi=4.0$、$\mu_\theta=\mu=2.63$ **不變**；新增「需求讀法」留檔 | 同（$M=232.5$ 未用） |

### 一、RC-2012-3：柱地震設計剪力高估一倍（最嚴重的觀念錯）

原文寫 $V_u = (M_{pr,top}+M_{pr,bot})/l_n = (75.5+75.5)/3.0 = 50.33$ tf，
把**一根柱的上下兩端各給了一個完整的梁 $M_{pr}$**。少了關鍵一步：**接頭處梁傳來的彎矩由上下兩根柱依勁度分擔**。

正確推導（單跨構架，每個外圍接頭只有一根梁）：

$$\Sigma M_{col} = \Sigma M_{pr,\text{beam}} = M_{pr}^- = 75.52\ \text{tf·m}
\ \Rightarrow\ M_{col,\text{上}} = M_{col,\text{下}} = 37.76$$
$$V_u = \frac{37.76+37.76}{3.0} = \frac{\Sigma M_{pr,\text{beam}}}{l_n} = \boxed{25.17\ \text{tf}}$$

**分子是「一個接頭」的梁 $M_{pr}$ 總和，不是上下兩個接頭相加。**
最終 $s = 9$ cm 由圍束公式一控制，**不受影響**；但 $s_{shear}$ 由 17.2 改為 34.3 cm，
且此觀念**直接影響 RC-2012-4 的接頭剪力檢核**（$V_{col}$ 是 $V_{jh}$ 的減項）。

另補兩項：① **塑鉸區外間距** $\le \min(6d_b,\,15) = 13.3$ cm → 取 13 cm（原文完全未提）；
② **$b_c$／$A_{ch}$ 定義敏感度留檔**：附圖標的 48 cm 是主筋心距，規範定義量至箍筋外緣為 52.76 cm，
兩者 $A_{sh1}/s$ 差 74%（0.540 vs 0.310）⇒ 分別得 $s = 9$ cm（圍束控制）與 $s = 13$ cm（$6d_b$ 幾何控制）。
**主線保留 48 cm**（附圖明標、且保守），另一讀法已於正本 §5④ 列表留檔。

### 二、RC-2005-3：$V_{col}$ 公式差 2 倍 ＋ 未用 $1.25f_y$（兩錯疊加）

**(1) $V_{col} = 2M_n/H$ 錯 → 應為 $M_n/H$。** 接頭處梁彎矩由上下柱各半分擔、柱反曲點在樓層中高：
$V_{col} = \dfrac{M/2}{H/2} = \dfrac{M}{H}$。原文 §4③ 的說明文字本身就自相矛盾
（先寫出 $(M_n/2)/(H/2)$，又斷言 $V_{col}\times(H/2) = M_n$）。

**(2) 梁筋拉力應取 $1.25f_y$。** $V_{jh} = \gamma\sqrt{f'_c}A_j$ 這條檢核**只存在於耐震專章**，
其配套規定 §18.8.2.1 明訂用 $1.25f_y$；用了耐震的**強度**公式就必須用耐震的**力**。

$$T = 1.25(30.42)(4200) = 159{,}705\ \text{kgf},\quad a = 11.18,\quad M_{pr} = 102.86\ \text{tf·m}$$
$$V_{col} = 10{,}286{,}000/365 = 28.18\ \text{tf},\quad
V_{jh} = 159{,}705 - 28{,}181 = \boxed{131.5\ \text{tf}}$$
$$\phi V_n = 0.85\times3.2\times\sqrt{280}\times3600 = 163.8\ \text{tf}\ \ge\ 131.5\ ✓\ (\text{利用率 } 80\%)$$

三種算法對照（$1.25f_y$ 131.5／$f_y$ 104.8／舊版 81.9 tf）已列表留檔，**結論都是通過**，但餘裕差很多。

**⚠ 依最新規範可能翻轉結論：** ACI 318-19 Table 18.8.4.3 新增「**柱未延伸至接頭上方**（屋頂層接頭）」一組較低的 $\gamma$
（四面 1.5／三面或一雙對面 1.0／其他 **0.7** MPa ≈ kgf 制 4.7／3.2／**2.2**）。
若本角柱接頭位於屋頂層：$\phi V_n = 0.85\times2.2\times16.733\times3600 = \mathbf{112.6}$ tf $< 131.5$ tf ⇒ **不通過（超出 17%）**。
原卷未交代樓層，正本與摘要頁均已明列此假設。
另修：$\gamma$ 中間檔土木 401 與 101 年考卷原文印的是 **3.9**（原文寫 4.0）；$b_j$ 改引規範原式 $\min(b+h,\,b+2x)\le b_{col}$。

### 三、RC-2025-2：密箍區外用「重力剪力」設計（結論不安全）

原文寫「一般區 $V_u = 9$ tf（重力剪力），$\phi V_c = 27.3 > 9$，取 $s = 30$ cm」——**把重力剪力圖誤當成耐震設計剪力**。
$V_e$ 是由兩端 $M_{pr}$ 產生、**沿全梁都存在**的剪力：

$$V_e(x) = \max(46.43 - 2x,\ 28.43 + 2x)\ \text{tf}\quad(x\ \text{自左柱面，m})$$

| 位置 | $V_e$ |
|---|:---:|
| 柱面 | 46.43 tf |
| 密箍區外緣 $x = 1.52$ m | **43.39 tf** ← 一般區控制值 |
| 跨中 $x = 4.5$ m | **37.43 tf** ← 包絡線最小值（**不是 9 tf**）|

$\phi V_c = 0.75\times35.65 = 26.74$ tf **連跨中都不夠**。
改正：一般區 $V_s \ge 43{,}394/0.75 - 35{,}652 = 22{,}207$ kgf ⇒ $s \le 21.5$ cm ⇒ 取
**2 腳 D13 @20 cm**（$\phi(V_c+V_s) = 44.6 \ge 43.4$ ✓，且 $20 \le d/2 = 33.5$ ✓）。

另修三項：
- **第一支箍筋距柱面 $\le$ 5 cm**（§18.6.4.4 對**梁**的明文；$s_o/2$ 是**柱** §18.7.5.3 的規定）——原文寫 7.5 cm。
- **$A_{v,\min}$ 的 kgf/cm² 係數是 3.5 與 0.2**（原文用 SI 的 0.35／0.0625，低 10 倍／3.1 倍）：$0.0750$ cm²/cm。
- $V_{s,\max} = 2.12\sqrt{f'_c}b_wd = 142.6$ tf（原文 143.2，SI 換算進位）；$\phi V_c$ 寫 27.3 應為 26.7。

密箍區主線（$M_{pr}^- = 188.1$／$M_{pr}^+ = 148.8$ tf·m、$V_e = 46.43$ tf、地震佔比 80.6% → $V_c = 0$、
$2h = 152$ cm、$s_{req} = 15.4$ vs $s_o = 15$ → 15 cm、$\phi V_s = 47.7 \ge 46.4$）**逐項複算全部正確**。
新增兩項可行性驗算：8-D32 單排所需寬度 58.84 $\le$ 60 ✓；4 腳箍筋之被支撐鋼筋間距 19.8 $<$ 35 cm ✓。

### 四、RC-2013-2：密箍區「以外」的間距違規

原文 §5③ 寫「$s_{outside} \le 6d_b = 19.3$ cm，D13@15 或 **D13@19** 即可」。
ACI 318-19 §18.7.5.5／土木 401 明定 $l_o$ 以外 $s \le \min(6d_b,\ 150\ \text{mm}) = \mathbf{15}$ cm——**19 cm 違規**。
「$6d_b$」從來不是單獨成立的上限。

另修 $h_x$：$h_c = 42$ 是量到**箍筋外緣**，主筋心距應扣**兩個**箍筋直徑：
$(42 - 2\times1.27 - 3.22)/4 = \mathbf{9.06}$ cm（原文 $(42-1.27-3.22)/4 = 9.38$）。
兩種繫筋配置（全配／跳一根）之 $s_o$ 分別為 18.65／15.63，**都被 15 cm 上限截住，結論不變**。

主線（$h_c = 42$、$A_{ch} = 1764$、$A_{sh1}/s = 0.5257$ 控制、$s = \min(12.5,\,19.3,\,15) \to 12$ cm、
需 4.97 腳 → 5 腳、外方箍＋3 繫筋、$A_{sh} = 6.35 \ge 6.31$ ✓）**全部複算相符**（餘裕僅 0.7%）。
另補：$\rho_g = 5.21\%$（$1\%\sim6\%$ ✓）、繫筋 $135°/90°$ 逐層交錯、$l_o = \max(50,\ l_u/6)$、並重繪箍筋配置圖說。

### 五、RC-2022-4：算式全對，補「需求 vs 容量」讀法留檔

逐項複算相符：內插 $\phi_y = 0.005$／$M_y = 220$／$\phi_u = 0.020$／$M_u = 245$；
$L_p = \max(0.5535,\ 0.5951) = 0.595$ m（**下限式控制**）；$\delta_y = 1.7067$ cm、$\theta_y = 0.005333$；
$\delta_u = 1.1136(0.017067) + 0.015(0.595)(2.9025) = 4.4911$ cm；$\mu_\phi = 4.00$、$\mu_\theta = \mu = 2.632$。

**新增留檔：** 題目給的 $M = 232.5$ tf·m **恰為內插後 $M_y = 220$ 與 $M_u = 245$ 的正中點**，卻全文未用。

| | 讀法 A（主線，照原卷公式下標 $u$） | 讀法 B（在 $M = 232.5$ 評估「需求」） |
|---|---|---|
| $\phi$ | 0.020 | $\phi_d = 0.0125$ |
| $\mu_\phi$ | **4.00** | **2.50** |
| $\delta$ | 4.491 cm | 3.099 cm |
| $\mu_\theta = \mu$ | **2.63** | **1.82** |
| 語意 | 實為**韌性容量** | 才是**韌性需求** |

採 A 為主線（題幹明寫「根據規範**所列公式**……評估」，公式下標即 $u$）；$M = 232.5$ 用來確認已降伏（$>220$）且未達極限（$<245$）。
考場建議兩者並寫，並可補「容量／需求 $= 2.63/1.82 = 1.44$，尚有 44% 韌性餘裕」。

另修兩處：① 摘要頁誤寫「$d_b$ 用 mm、$f_y$ 用 MPa」——正確是 **$L$、$d_b$ 用 m、$f_y$ 用 kgf/cm²**
（係數 0.0022／0.0044 已由 Priestley 原式的 0.022／0.044 除以 10.197 換算，代入時勿再換算）；
② 補 $\mu \approx 1+(\mu_\phi-1)\lambda$ 的交叉驗算：$\lambda = 3\frac{L_p}{L}(1-0.5\frac{L_p}{L}) = 0.506$ →
$1+3(0.506) = 2.518$，與**去掉 $M_u/M_y$ 硬化項**後的 $\delta_u/\delta_y$ 完全吻合。

### 六、依最新規範對照（五題都加了 §6 專節）

| 題號 | 原卷指定 | 401-112／ACI 318-19 下的答案 | 條文變動 |
|---|---|---|---|
| RC-2025-2 | **土木 401-112**（卷首明訂） | **相同**（原卷即現行規範） | 無落差；修的是原文引錯的條文 |
| RC-2013-2 | 土木 401-100 | **相同**（$s=12$ cm、5 腳 D13） | $A_{sh}$ 加第三式（門檻 $0.3A_gf'_c = 210$ tf，未觸發）；$l_o$ 外間距 15 cm |
| RC-2012-3 | 未指定（401-100 世代） | **相同**（$s=9$ cm） | 同上（門檻 302 tf，未觸發）；含軸壓 $V_c$ 由乘法改加法（取 $V_c=0$ 故用不到） |
| RC-2005-3 | 未指定（401-86／318-99 世代） | 中間樓層 **相同**（通過）；**屋頂層則不通過** | Table 18.8.4.3 新增屋頂層接頭 $\gamma$（角柱 3.2 → **2.2**） |
| RC-2022-4 | 公路橋梁耐震評估與補強設計規範（109/12） | **相同**（該規範即現行版，未更新） | 無 |

### 七、施作內容（下游同步）

- `raw/solutions/{RC-2025-2,RC-2013-2,RC-2012-3,RC-2005-3,RC-2022-4}/*.md`：正本改寫
  （§1 補原卷原文核對、勘誤框、§4 補／改步驟、§5 改寫爭議點、**新增 §6 依最新規範對照**）。
- `wiki/problems/` 五頁摘要：標題／答案／核心考點／關鍵步驟／公式／陷阱／圖形欄／新增「依最新規範對照」段全部同步。
- `raw/json/question_index.json`：五題 tags 全部重抓（2025-2 7→9、2013-2 8→9、2012-3 10→11、2005-3 9→11、2022-4 8→9）。
  `verificationStatus` 全部維持 `unverified`。
- `dashboard-data.js`、`knowledge_graph.html`：五題 tags 同步（100 列／每列 7 元素、行數 130 均已驗證）。
- `wiki/index.md`、`wiki/by-year.md`：五題一行說明改為含改後答案。
- `study/problems-view/` 五頁以 `scripts/gen_problems_view.py` **單題**重建（written=5，未動 `--all`）。
- `study/study-RC-U3-3.html`：五題內嵌資料列的 description 與 tags 同步。
- `wiki/code-ref/seismic-code.md`：**多處實質修正**——
  ① 梁密箍區間距仍寫 ACI 318-11 的 $\min(d/4,8d_b,24d_{sw},300\text{mm})$，已改為 318-14 起的 $\min(d/4,6d_b,150\text{mm})$；
  ② $A_{sh}$ 只列兩式，已補第三式 $0.2k_fk_nP_u/(f_{yt}A_{ch})$ 與 $k_f$、$k_n$ 定義及觸發條件；
  ③ **完全沒有柱的間距規定**，已補 $l_o$ 內 $\min(b/4,6d_b,s_o)$、$l_o$ 外 $\min(6d_b,150\text{mm})$、$h_x\le350$mm、繫筋彎鉤交錯；
  ④ 柱設計剪力補「由梁 $M_{pr}$ 經接頭反推」路徑並警示不可寫成 $2\Sigma M/l_u$；補柱 $V_c=0$ 條件；
  ⑤ 接頭 $\gamma$ 表改為 318-19 六檔（含屋頂層），中間檔 4.0 → **3.9**；$b_j$ 公式改引規範原式；
  ⑥ 新增「密箍區外仍受包絡線控制」與 $A_{v,\min}$ kgf 制係數兩節。
- `wiki/traps/SEISMIC-BEAM-VE.md`：修正 **$V_c=0$ 條件不等號寫反**（原寫「$P_u/(A_gf'_c)\ge0.05$ 則 $V_c=0$」，
  與同頁下方正確敘述自相矛盾）；密箍區間距改新制；新增「步驟四：密箍區外仍要設計」；陷阱表增列 4 列。
- `wiki/traps/JOINT-SHEAR-EFFECTIVE-AREA.md`：$V_{col}$ 補完整推導並警示「$2\Sigma M/H$ 大一倍」；
  $A_j$／$b_j$ 改引規範原式；$\gamma$ 表改為六檔（中間檔 4.0 → 3.9，新增屋頂層組）；陷阱表增列 3 列。

> 註：`wiki/traps/` 依 CLAUDE.md 規則 4 屬 compile 輸出。比照前兩次 XCHECK 的做法**手動同步**，
> 以免下次 `compile-all` 之前 wiki 顯示與正本矛盾；來源（`raw/solutions/`）已先改，故不會被蓋回舊結論。

### 驗證

- `gen_problems_view.py . <五題> --check` → **same=5**（管線冪等、HTML 與正本一致）
- `question_index.json` 100 題解析通過、moduleId 無重複，僅 tags 陣列有差異
- `dashboard-data.js` 100 列全數 JSON 解析通過、每列 7 元素、行數 130 未變
- `knowledge_graph.html` 五個 `p(...)` 節點 tags 已同步
- 關鍵新值已出現在 problems-view：43.4／20 cm／5 cm（第一支箍筋）／9.06／15 cm（區外）／25.17／13.3／131.5／112.6／0.0125／1.82／0.595
- 舊錯值僅殘留在**刻意保留的勘誤／對照段**：RC-2012-3 的「50.33」兩處（勘誤說明）、
  RC-2025-2 的「$8d_b$」一處（318-11 舊制對照）、RC-2005-3 的「$8d_b$」一處（$\ell_{dh}\ge8d_b$，正確條文）
- 規範版本以網路查證（土木 401-112 現行、公路橋梁耐震評估規範 110-03-23 頒布迄今未更新）

### 待辦（本次未做）

1. **`RC-2012-4`（梁柱外接頭剪力）必受本輪 RC-2012-3 更正影響**：$V_{col}$ 是 $V_{jh}$ 的減項，
   若該題沿用舊的 $V_u = 50.33$ tf，$V_{jh}$ 會被低估。**列為下一輪第一順位**。
2. 同理應複查 `RC-2003-3`、`RC-2018-2` 兩題接頭題是否也用了 $2\Sigma M/H$ 與 $\gamma = 4.0$。
3. `RC-2007-4` 的自創容許值（$0.4f'_c$、$3\sqrt{f'_c}$）仍未處理（見 2026-08-22 第一輪 XCHECK 待辦 1）。
4. RC-2023-4 主線由 18.5 改 22.5 tf·m/m 仍待人工複核（第一輪待辦 2）。
5. 本輪五題與前輪五題 `verificationStatus` 均為 `unverified`，待人工驗算後通知改 `verified` 並 ingest。
6. 五題皆無向量圖解（`figs/`）。最值得補的三張：RC-2025-2 的「$V_e$ 包絡線 vs 重力剪力圖」對照、
   RC-2012-3／RC-2005-3 共用的「接頭彎矩分擔與 $V_{col}$ 推導」示意圖、RC-2013-2 的箍筋＋繫筋斷面配置圖。
7. 前幾則 log 列出的舊待辦（φ 舊式 RC-2004-2／RC-2015-3、problems-view 35 頁數學式壞掉）仍未處理。

> **2026-08-22 補記（第二輪 XCHECK 續）：** 另修 `wiki/code-ref/ACI-318.md` §18.6／§18.7／§18.8 三段——
> 梁加密區間距同樣仍寫 ACI 318-11 的「$8d_b$／$24d_{sw}$／300 mm」（且 LaTeX 破損），已改為 $\min(d/4,6d_b,150\text{mm})$；
> $A_{sh}$ 補第三式與 $k_f$／$k_n$；補 §18.7.5.1／18.7.5.3／18.7.5.2／18.7.5.5 柱間距全套與 $V_c=0$ 條件；
> 柱設計剪力補「由梁 $M_{pr}$ 經接頭反推」並警示不可寫成 $2\Sigma M/l_u$；
> 接頭段補 §18.8.2.1（$1.25f_y$、$\phi=0.85$）、§15.4.2.4（$A_j$、$b_j$）、Table 18.8.4.3 六檔 $\gamma$（中間檔 4.0→3.9、新增屋頂層組）、§18.8.5.1（$\ell_{dh}$）。
> 至此「318-11 舊間距值」在全庫的三處（seismic-code.md、SEISMIC-BEAM-VE.md、ACI-318.md）已全部改正。

---

## 2026-08-31　struct-diagram 六題向量圖解 ＋ RC-2016-1／RC-2019-1 數值訂正

### 產圖（每題 3 張，共 18 張；SVG＋2× PNG，腳本可重跑）

| 題號 | 圖 1 | 圖 2 | 圖 3 |
|---|---|---|---|
| `RC-2023-2` | 斷面配筋與淨間距檢核 | 應變／應力三聯（a 對 h_f） | 4+4 vs 3+3+2（中性軸不變） |
| `RC-2011-2` | 兩種尺寸讀法對照 | ε_t 規範帶狀圖（0.004 界限） | 彈性 NA vs Whitney 塑性 NA |
| `RC-2007-1` | 有效翼板寬三條件 | 單排✗／兩排✓與實際 d | φM_n 對層間淨距的敏感度 |
| `RC-2015-2` | φM_n 掃描與折點極大值 | c_u < d' 壓筋落拉力區 | 強度－韌性抵換曲線 |
| `RC-2016-1` | 三組合彎矩圖（梁端翻號） | 四控制點彎矩比較 | 彎矩強度比 vs 面積比 |
| `RC-2019-1` | 斷面／應變／應力三聯 | 過渡區 φ–ε_t 內插 | 二次方程雙根取捨 |

- 檔案：`raw/solutions/<題號>/figs/<題號>-fig-N-<語意>.svg`＋`.png`，
  產圖腳本 `raw/solutions/<題號>/figs/gen_<題號>.py`（常數區只放 §1 給定值，
  其餘一律現算，檔尾對 §4／§5 公佈值 `assert`；改輸入重跑，圖形跟著變）。
- 驗證：`render.py` XML＋溢出檢查 18/18 通過；18 張 PNG 全數目視檢查
  （中文字型、標註重疊、數值與解題檔逐位比對）。
- 已插回六題正本的對應章節（不是堆在檔尾），並重建 `study/problems-view/` 六頁。

### 訂正一：`RC-2016-1` §4 Step 8「面積比 vs 彎矩強度比」方向講反（🔒 觀念錯誤）

原文寫「**面積比恆大於彎矩強度比**……用面積比判斷會**偏不保守**」，並引 $7.74/14.46 = 0.535$。

- $0.535$ 是拿**實配底筋 7.74** 除**需求頂筋 14.46** 混算出來的，既不是面積比也不是強度比。
- 實配面積比 $= 7.74/15.48 = \mathbf{0.500}$；彎矩強度比 $= 19.85/38.42 = \mathbf{0.517}$。
- 因 $M_n = A_sf_y(d-a/2)$，$A_s$ 小者力臂長（61.05 對 59.10 cm），故
  $\dfrac{M_{n,\text{bot}}}{M_{n,\text{top}}} \geq \dfrac{A_{s,\text{bot}}}{A_{s,\text{top}}}$
  （只要 $A_{s,\text{bot}} \leq A_{s,\text{top}}$）——**面積比恆不大於強度比，是偏保守的快篩**，
  用它判斷不會誤放行，方向與原文相反。

### 訂正二：`RC-2016-1` 其餘數值

| 位置 | 原值 | 訂正 | 說明 |
|---|---|---|---|
| §4 Step 1 $\rho_b$ | 201.8／4200 → 0.04805 → 0.02849 | 202.3／4200 → 0.04817 → **0.02856** | $0.85\times0.85\times280 = 202.3$，非 201.8 |
| §4 Step 1 舊制對照 | $0.75\rho_b = 0.02137$、$A_{s,\max} = 47.11$ | **0.02142**、**47.24** cm² | 隨 $\rho_b$ 連動（$\varepsilon_t = 0.003745$ 不變） |
| §4 Step 8 $M_{n,\text{top}}$ | 3,841,000 kgf-cm＝38.41 | **3,842,000＝38.42** tf-m | |
| §4 Step 8 $M_{n,\text{bot}}$ | 1,984,000 kgf-cm＝19.84 | **1,985,000＝19.85** tf-m | 比值 0.517 不變 |

### 訂正三：`RC-2019-1` $A_{s,\min}$

$\max(0.00276,\ 0.00333)\times 50\times 63 = 10.50$ cm²（原寫 10.49），§4.6 兩處。

### 下游同步

- `wiki/problems/RC-2016-1.md`：47.11→47.24、Step 7 與陷阱條的面積比敘述改寫。
- `wiki/problems/RC-2019-1.md`：$A_{s,\min}$ 10.49→10.50；「用到的公式」的 $\phi$ 由**舊式**
  $0.65+(\varepsilon_t-0.002)\times 0.25/0.003$ 改為本庫統一的**現行式**
  $0.65+0.25(\varepsilon_t-\varepsilon_{ty})/(0.005-\varepsilon_{ty})$，$\varepsilon_{ty}=0.002059$；
  題幹摘要的過渡區下界同步由 0.002 改為 $\varepsilon_{ty}$。
- 六題 `wiki/problems/` 頁的「圖形」區塊新增向量圖解清單。
- `study/problems-view/` 六頁以 `gen_problems_view.py` 重建（已含上述訂正）。

### 待辦（本次未做）

1. `study/RC-U1-1_梁彎矩強度分析與設計_公式給背分界_記憶片.pdf` 與
   `study/RC-U3-3_韌性要求與耐震設計_公式給背分界_記憶片.pdf` 內含舊值 `0.535`，
   PDF 無法就地修改，**需以 formula-recall-deck 重新產生**。
2. `wiki/queries/xcheck-RC-2026-07-26.md:118` 引用 `RC-2016-1.md:188` 的 `0.02137`、
   `複核報告_RC梁題七題_2026-08-21.md:334` 引用 `10.49`：兩者皆為**有日期的當時快照**，
   本次刻意不動，僅在此記錄其引用值已被上游訂正。
3. `scripts/apply_figs.py` 的 `FIGS` 表未加入本次六題（本次採「插到對應章節正下方」的
   逐節配置，與該腳本「圖 1 插 §2 前、其餘插 §5 前」的粗配置不同）。若日後要走該管線，
   需先決定採哪一種配置。
---

## 2026-08-31　struct-diagram 第二輪：預力混凝土五題向量圖解 ＋ 三處數值訂正

**指令：** `/struct-diagram RC-2011-5 & RC-2006-4 & RC-2004-5 & RC-2023-4 & RC-2012-1`
（使用者選：全部修含下游／15 張全做）

### 產出（15 張，每題 3 張，SVG + 2× PNG，腳本可重跑）

| 題號 | 圖 1 | 圖 2 | 圖 3 |
|---|---|---|---|
| RC-2011-5 | `fig-1-sections` 淨／變換／合成三斷面性質對照 | `fig-2-stress` 三階段應力疊加 | `fig-3-tendon` 腱應力 10,417→9,167→9,889 |
| RC-2006-4 | `fig-1-composite` 裸梁 vs 組合轉換斷面（$\bar y=65.07$、$I_c=4{,}188{,}695$） | `fig-2-stress` 兩階段疊加＋「版 DL 誤放組合斷面」對照 | `fig-3-allow` 五條容許應力利用率與 Class C |
| RC-2004-5 | `fig-1-mcr` 底纖維 $56.47\to0\to-37.42$ 兩段歷程 | `fig-2-section` 斷面／應變／應力塊 | `fig-3-strength` $M_{cr}$／$1.2M_{cr}$／$\phi M_n$／$M_n$ |
| RC-2023-4 | `fig-1-branch` 兩個跨深比分支的 $f_{ps}$ 曲線與配套上限 | `fig-2-section` 20 cm 條帶（含 $A_{s,\min}$、$A_{ct}$） | `fig-3-mn` 18.5／22.5／23.6 tf·m/m |
| RC-2012-1 | `fig-1-eccentricity` 懸臂彎矩方向決定偏心在上方 | `fig-2-stress` 固定端 vs 自由端 | `fig-3-overrun` $f_{bot}(\xi)$ 與 201 cm 超限段 |

檔案位置：`raw/solutions/<題號>/figs/`，產圖腳本同置於 `figs/gen_<題號>.py`。
15 張全數通過 `render.py` 的 XML 合法性與溢出檢查（0 個需要修正），並逐張目視複核。

### 訂正一：`RC-2004-5` 有效預力連鎖

$P_e = 6.16 \times 9{,}900 = \mathbf{60{,}984}$ kgf（原寫 61,024，乘法本身就錯）。連帶：

| 位置 | 原值 | 訂正 | 說明 |
|---|---|---|---|
| §4② $f_{ce}$ | $16.95 + 39.55 = 56.50$ | $\mathbf{16.94 + 39.53 = 56.47}$ | 隨 $P_e$ 連動 |
| §4② $f_r$ | $2\sqrt{350} = 37.4$ | $\mathbf{37.42}$ | 原式取 2 位有效數字，使 $M_{cr}$ 落在 50.69／50.70 邊界；改列 37.42 後 $M_{cr}=54{,}000\times93.89=5{,}070{,}060$，$\boxed{50.7}$ 與 $1.2M_{cr}=60.84$ 均維持原值 |
| §4④ $\omega_p$ | 0.0867 | $\mathbf{0.0866}$ | $97{,}026/1{,}120{,}000 = 0.08663$ |
| §5② $\beta_1=0.85$ 誤用之 $\phi M_n$ | 66.44（+0.2%） | $\mathbf{66.48}$（+0.3%） | $f_{ps}=15{,}795 \Rightarrow a=8.176$、$M_n=73.86$、$\phi M_n=66.476$ |

$M_{cr} = 50.7$、$\phi M_n = 66.3$ 兩個答案本身不變。

### 訂正二：`RC-2006-4` Step 4 分母與 Step 3 不一致

Step 3 已算出 $S_{c,top} = 280{,}622$、$S_{c,bot} = 64{,}369$，Step 4 卻代入
280,552 與 64,372（來源不明的舊值）。已改為與 Step 3 一致；
$+35.6$／$-155.4$ 兩個結果不變（$10^7/280{,}622 = 35.63$、$10^7/64{,}369 = 155.36$）。

### 訂正三：`RC-2012-1` Step 7 拉力合力

$T = \tfrac12 \times 15.63 \times 22.5 \times 30 = 5{,}275.125 \to \mathbf{5{,}275}$ kgf（原寫 5,276）。
下一行的 $A_s = 5{,}275/2{,}100 = 2.51$ cm² 本來就用 5,275，屬同段內自相矛盾，非結果錯誤。

### 下游同步

- `wiki/problems/RC-2004-5.md`：$P_e$、$f_{ce}$、$f_r$、$M_{cr}$ 計算式、$\omega_p$ 同步訂正。
- `wiki/problems/RC-2006-4.md`、`RC-2012-1.md`：檢查後確認原本即為正確值，未動。
- 五題 `wiki/problems/` 頁的「圖形」區塊新增向量圖解清單。
- `study/problems-view/` 五頁以 `gen_problems_view.py` 重建。

### 備註

- 五個 `.md` 均為 CRLF，插圖與訂正全程以位元組層級處理，換行未被轉換。
- 本次未在使用者端執行 `py_compile`（上一輪產生的 `__pycache__` 無法以 `rm` 移除，
  已於 8/31 移至 `_to_delete/pycache_20260831/`，待使用者自行刪除）。

## 2026-09-02

### 完成事項

- 新增 RC 梁題 5 題（RC-2009-3, RC-2014-3, RC-2017-2, RC-2020-2, RC-2023-3）的 struct-diagram 向量圖解。
- 將圖片產生結果與註解，更新至對應的 .md 與 study/problems-view/ 的 .html 檔案中。
- 更新 scripts/apply_figs.py 的圖解中繼資料與註解。

## 2026-09-07

### 完成事項

- 新增耐震群 5 題（`RC-2025-2`、`RC-2013-2`、`RC-2012-3`、`RC-2005-3`、`RC-2022-4`）的
  struct-diagram 向量圖解，共 **17 張**（SVG + 2× PNG）與 5 支可重跑的 `gen_*.py`。
  `render.py` 溢出檢查全數 0 個需修正，17 張 PNG 逐張目視確認。
- `scripts/apply_figs.py` 擴充：新增 `ANCHORS` 機制（圖塊插在指定原文行之後，
  取代原本「圖 1 → §2 之前、其餘 → §5 之前」的粗略規則），並新增 `REPLACE` 掛勾（目前為空）。
  五題的圖號一律**依 .md 內出現先後**重排，冪等重跑已測試。
- `study/problems-view/` 五頁以 `gen_problems_view.py` 重建，`--check` 回報 same=5。

### 解題正本訂正（`raw/solutions/`，共 45 處）

| 題號 | 訂正 |
|---|---|
| `RC-2025-2` | Step 6 的 $5.08\times2800\times67/15$ 誤寫 **63,701**（正解 **63,534**），連帶 $\phi V_s$ 由 47.8 改為 **47.7** tf，與「最終設計」表原本就寫的 47.7 一致；$M_{pr}^-$ 全檔統一為 **188.1**（原 §3.5／Step 2 寫 188.2、§Step 8／§6 寫 188.1），連帶 $336.9\to37.43\to46.43$；Step 5 分子 953,072 → **953,008**；§2 出題者意圖第 4 點原仍寫「第一支箍筋 $\le s_o/2$」，與同檔 §3 陷阱 6、§6 的勘誤矛盾，已改為梁的 **$\le 5$ cm** |
| `RC-2013-2` | §5② 兩處「相鄰主筋間距 ≈ **9.4** cm」是 8/22 勘誤前的殘值，已改為 **9.06** cm；新增 **Step 5c：第一支箍筋位置**（柱為 $\le s_o/2 = 6$ cm，§18.7.5.3；與梁的 5 cm 不可互換），並在 Step 6 彙整表補列 |
| `RC-2012-3` | §5① 不等號寫反：$\phi V_c = 23.7 \ \mathbf{\ge}\ V_u = 25.17$ 改為 **$<$**（下一句「箍筋僅需承擔 $(25.17-23.7)/0.75$」本身就預設 $<$）；§5④ 取法 B 的 $A_{sh1}/s$ 由 0.310 改為 **0.309**（精算 0.30947）；§3.5 與 §4 Step 3 把 48 cm 說成「箍筋中心線至中心線」，與 §3 陷阱 4／§5④ 矛盾，已改為「**主筋中心至主筋中心**」；§5 小節順序 ①④⑤②③ 重排為 ①②③④⑤ |
| `RC-2005-3` | §3.5 Step 5 的 $b_j = \min(b_c,\ b_w+0.5h_c)$ 是坊間簡化式，與同檔 §4⑤ 自己的更正矛盾，已改用規範原式 $\min(b_w+h_c,\ b_w+2x) \le b_c$；$\phi V_n$ 尾數統一為 **163,851** kgf（§4⑥ 原 163,848、§3.5 原 163,800，且單位誤寫「163.8 t」）；§5② 的「$\times 3.193$ 由 MPa 換 kgf/cm²」推不出 5.3，已補正為「5.3 出自 psi 路徑（$20/3.771$），3.9／3.2／2.2 出自 SI 路徑（$\times3.193$），三套各自取整、不可互相反推」 |
| `RC-2022-4` | $\delta_u$ 精確值 **0.044913 m（4.491 cm）**（彙整表原寫 4.493、§5 表寫 4.491，自相矛盾）；$\theta_y$ 由 0.005335 改為 **0.005333**；$\theta_u$ 改為 0.014035；$L_p$ 第一式改印 4 位（$0.2975$／$0.5535$）以免與下限式 0.5951 的比較看起來像進位問題；容量／需求比由 $2.63/1.82 = 1.44$ 改為 **$2.632/1.816 = 1.449$**。$\mu_\phi = 4.00$、$\mu_\theta = \mu = 2.63$ 三個結論不變 |

### 下游同步

- `study/lecture-RC-U3-3.html`（RC-U3-3 單元講義）**四段手算例都還在教勘誤前的錯值**，已全部同步：
  - RC-2012-3：$V_u = (75.5+75.5)/3.0 = \mathbf{50.33}$ tf → 改為接頭彎矩由上下柱分擔的三步推導，**25.17 tf**；
    §5.2 的通式 $V_u^{col} = (M_{pr,top}+M_{pr,bot})/l_n$ 分子容易被讀成「梁端 $M_{pr}$」（正是 50.33 的來源），
    已改寫為柱端彎矩並加註「分母是一根柱的淨高、分子是一個接頭的梁彎矩總和」；
    自我檢查③的剪應力由 15.5 改為 **7.77** kgf/cm²（$0.46\sqrt{f'_c}$）。
  - RC-2005-3：$T = A_sf_y$ → **$1.25A_sf_y$**；$V_{col} = 2M_n/H = 45.9$ → **$M_{pr}/H = 28.18$** tf；
    $V_{jh} = 81.9$（利用率 50%）→ **131.5 tf（80%）**；$b_j$ 改用規範原式；$\phi V_n$ 163,848 → 163,851；
    §6.1 的 $V_{jh}/V_{col}$ 由 1.78 改為 **4.67** 倍，內接頭那句對比敘述一併重寫。
  - RC-2025-2：188.2／46.44／61.92／15.4 全部同步，並改正「**第一支距柱面 $\le s/2 = 7.5$ cm**」
    → 梁為 $\le 5$ cm（§18.6.4.4），$s_o/2$ 是柱的規定（§18.7.5.3）。
  - RC-2022-4：位數同步（0.005333／0.044913／0.014035／0.2975）。
  - §6.2 γ 表：T 形接頭 kgf 制 **4.0 → 3.9**、SI 制 **1.25 → 1.2**，並補上「三套數字各自取整、不可互相反推」的說明。
  - 陷阱二原把 $\min(d/4,\,8d_b,\,24d_{b,tie},\,300\text{ mm})$ 引註為「ACI 318-19 §18.6.4.4」，
    並把新舊制描述成兩個並存選項。已改為：舊制屬 **318-11 及更早**，**318-14 起**為 $\min(d/4,\,6d_b,\,150\text{ mm})$；
    RC-2025-2 原卷明訂土木 401-112，沒有選擇空間。
- `wiki/problems/RC-2005-3.md`：**上半段整段仍是 8/22 勘誤前的值**（標題、題幹摘要、核心考點、
  解題關鍵步驟、用到的公式、涉及陷阱），而同頁「驗證狀態」卻已聲稱「$V_{col}$ 與 $T$ 均已更正」——
  自相矛盾。已全段同步為 $1.25f_y$ 主線，γ 表 T 形由 4.0 改 3.9。
- `wiki/problems/RC-2013-2.md`：核心考點與解題關鍵步驟各補一條「第一支箍筋位置（柱：$s/2 = 6$ cm）」。
- `wiki/concepts/SPECIAL-MOMENT-FRAME-BEAM.md`：密箍區間距仍寫 $\min(d/4,\,8d_b,\,24d_{b,箍筋},\,300\text{ mm})$
  且未標版本，已改為 $\min(d/4,\,6d_b,\,150\text{ mm})$ 並註明舊值屬 318-11 世代。
  （`raw/json/concepts.json` 的 `key_formula` 未載間距條件，故上游無須改。）
- `wiki/code-ref/seismic-code.md`、`wiki/traps/SEISMIC-BEAM-VE.md` 檢查後確認早在 2026-08-22 已正確，未動。
- `wiki/problems/` 五頁的「圖形」區塊**未**新增向量圖解清單——全庫既有 11 個有向量圖的題目
  （含 RC-2020-2）都沒有列，向量圖是透過 `study/problems-view/` 呈現，維持既有慣例。

### 未處理（需重新解題，不在本次同步範圍）

- 🔴 **`RC-2012-4`**：$V_{jh} = T_1 - V_{col} = 159.7 - \mathbf{50.33} = 109.4$ tf 沿用 `RC-2012-3` 的舊 $V_{col}$。
  改用正確的 **25.17 tf** 會得 $V_{jh} \approx 134.4$ tf，**該題答案與判定都會變**，屬解題範圍而非同步範圍。
  影響檔案：`raw/solutions/RC-2012-4/RC-2012-4.md`、`wiki/problems/RC-2012-4.md`、
  `study/problems-view/RC-2012-4.html`。與 2026-08-22 記錄的「列為下一輪第一順位」為同一件事，仍未消。

### 追記：清除傳輸管道注入的 C2PA 內容憑證

圖檔從容器寫回本機時，傳輸管道在每個檔案裡加了 C2PA（Content Credentials）簽章：

- SVG：在 `<svg>` 上加 `xmlns:c2pa` 並插入 `<metadata><c2pa:manifest>…base64…</c2pa:manifest></metadata>`，
  每檔多約 7.4 KB（例如 `RC-2005-3-fig-2-gamma.svg` 由 18,796 脹到 26,034 B）。
- PNG：多一個 `caBX` 私有 chunk，每檔固定 5,758 B。

既有 11 題（`RC-2020-2` 等）的向量圖都沒有這層簽章，且它會讓「磁碟上的圖 ≠ `gen_*.py` 的產物」，
與 `CLAUDE-SPEC.md` §5.1「生成腳本必須可重跑」的可稽核性相違，故全部移除。
移除後複驗：**17 張 SVG 與腳本重跑結果 md5 完全相同**；17 張 PNG 的 chunk 串仍為 IHDR…IEND 完整且可正常解碼。

### 備註

- 五個解題 `.md` 與 `wiki/` 下的 `.md` 均為 CRLF、`study/` 下的 `.html` 均為 LF，
  全程以位元組層級判斷後原樣寫回，換行未被轉換（改後逐檔複數）。
- 五題的 `verificationStatus` 仍為 `unverified`，本次只做算式自洽與下游一致性，**未做人工驗算**。

## 2026-09-07（第二輪）：`RC-2012-4` 重解 —— 清掉 2026-08-22 留下的最後一筆待辦

`RC-2012-3` 於 2026-08-22 把柱設計剪力由 $V_{col} = 50.33$ 更正為 **25.17 tf**（接頭梁彎矩由上下柱分擔），
當時即記錄「這會直接影響 `RC-2012-4` 的接頭剪力檢核，列為下一輪第一順位」。本次處理完畢。

### 為什麼會錯

`RC-2012-4` 的 $V_{jh} = T_1 - V_{col}$ 裡，$V_{col}$ 是**減項**。
減項被高估一倍，$V_{jh}$ 就被低估——而且錯的方向是「**看起來更安全**」，最難察覺。

### 主線數值變更

| 項目 | 舊版 | 重解後 | 依據 |
|---|:---:|:---:|---|
| $T_1 = A_{s,top}f_{ps}$ | 159.7 tf | 159.7 tf（不變） | $30.42\times5250$，$f_{ps}=1.25f_y$（§18.8.2.1） |
| $V_{col}$ | $2M_{pr}/l_n$ = 50.33 tf ✗ | $\Sigma M_{pr,\text{beam at joint}}/l_n = 75.52/3.0 = \mathbf{25.17}$ tf | RC-2012-3（已更正） |
| $V_{jh}$ | 109.4 tf | $159{,}705-25{,}175 = 134{,}530$ kgf $= \mathbf{134.5}$ tf（**+23%**） | $V_{jh}=T_1-V_{col}$ |
| $b_j$ | $\min(b_c,\ b_w+h_c) = 60$（坊間簡化式） | $\min(b_w+h_c,\ b_w+2x) \le b_c$；梁置中 $x=5$ ⇒ 60 cm | §15.4.2.4。梁比柱窄（50<60）正是兩式分家處，本題梁置中故 $b_w+2x \equiv b_c$，數值巧合相同 |
| 強度 | 「$\phi V_n$」= 192.8 tf（**其實沒乘 $\phi$**） | $V_n = 192.8$ tf；$\phi V_n = 0.85V_n = \mathbf{163.85}$ tf | $\phi=0.85$ 接頭剪力專用（§21.2.1(e)），與 `RC-2005-3` 一致 |
| 利用率 | 57%（餘裕 43%） | **82%（餘裕 18%）** | $134.5/163.85$ |
| 判定 | ✅ 足夠 | ✅ **足夠（不變）** | 但餘裕從「很寬鬆」變成「還可以」 |

**結論沒有翻轉，但兩個新結果值得記住：**
1. 忽略 $V_{col}$ 的保守下限 $V_{jh} \approx T_1 = 159.7$ tf，利用率已達 **97%**——
   這個接頭其實相當吃緊，$V_{col}$ 這個減項幾乎就是通過與否的關鍵。
2. 若為**屋頂層**角隅接頭，ACI 318-19 Table 18.8.4.3 之 $\gamma$ 降為 2.2 ⇒
   $\phi V_n = 112.65$ tf $< 134.5$ tf **不通過（超出 19%）**。
   原卷附圖是單跨多層構架的 **2F／3F 外圍剖面**（見 `RC-2012-2`），柱連續向上延伸，故主線取 $\gamma = 3.2$。

### 驗算方式

- 由 §1 給定值全程重算（`RC-2012-2` 的 $M_{pr}^- = 159{,}705 \times (54-13.421/2) = 7{,}552{,}400$ kgf·cm 複驗相符）。
- **交叉驗算：** `RC-2005-3` 的角柱接頭同為 $\gamma=3.2$、$A_j=3{,}600$ cm²、$f'_c=280$，
  $\phi V_n$ 亦為 163.85 tf ✓——兩題強度端必須一致，只有需求端不同（134.5 vs 131.5 tf）。
- 另一搖擺方向（底筋受拉）$V_{jh} = 81.27-13.70 = 67.6$ tf，確認頂筋向控制。

### 本次一併補上的內容（原頁缺漏）

- **新增 §6「依最新規範對照」**——原頁沒有這一節（同批五題都有），屋頂層 $\gamma=2.2$ 的風險就落在這裡。
- §5① 三種讀法對照表（主線／不乘 $\phi$／舊版），三者都通過但餘裕 18%／30%／43%。
- §5② 改善方案表補上兩件事：正交向增設梁要升級 $\gamma$，該梁必須**寬 $\ge \frac34$ 柱寬且深 $\ge$ 最深梁的 $\frac34$**
  才算數；以及「**加密接頭箍筋不能補強度不足**」（箍筋只提供圍束，不在 $\gamma\sqrt{f'_c}A_j$ 裡）——這是常見誤答。
- §5④ 接頭橫向鋼筋合規性：§18.8.3.2 的減半條件是「四面有梁」，角隅接頭不適用，
  題目給的 4-leg #4 @ 9 cm 正是柱塑鉸區配置 ⇒ 符合 §18.8.3.1 ✓。
- §5⑤ 梁頂筋錨定：$\ell_{dh} = 4200\times2.54/(17.2\times16.733) = 37.1$ cm $\le$ 柱深扣保護層可用之 54 cm ✓（餘裕不大）。

### 下游同步

- `wiki/problems/RC-2012-4.md`：標題、題幹摘要、核心考點、解題關鍵步驟、用到的公式、涉及陷阱全段重寫。
- `study/problems-view/RC-2012-4.html`：以 `gen_problems_view.py` 重建（11,817 → 25,418 B）。
- `raw/json/question_index.json`：`RC-2012-4` 標籤 `3.2係數` → `γ係數3.2`，並新增
  `接頭彎矩分擔`、`Vcol反推`、`1.25fy`、`φ0.85接頭`、`屋頂層接頭折減`（git diff 僅 +7/−2 行，格式未被重排）。
- `raw/solutions/RC-2012-3/RC-2012-3.md`：§4 Step 1 的前向註記由「務必改正」改為記錄已完成，
  並重建其 problems-view。
- `study/lecture-RC-U3-3.html`：
  - 錯誤複習表第 19 列的 $b_j$ 仍寫坊間簡化式 `min(bc, bw+0.5hc)`，已改為規範原式 `min(bw+hc, bw+2x) ≤ bc`；
  - 章首總表的接頭剪力通式原寫 $V_{jh}=T_{top}+T_{bot}-V_{col}$（外接頭沒有第二項，且第二項應為壓力 $C_{bot}$），
    已改為分列內接頭 $T_{top}+C_{bot}-V_{col}$ 與外接頭 $T_{top}-V_{col}$，並標明 $\phi=0.85$。

### 備註

- `RC-2012-4` 的 `verificationStatus` 仍為 `unverified`：本次只做算式自洽、跨題交叉驗算與下游一致性，**未做人工驗算**。
- 順手對齊：屋頂層 $\phi V_n = 0.85\times2.2\times\sqrt{280}\times3600$ 的全精度值是 **112,648** kgf，
  `RC-2005-3` 原寫 112,646 kgf／112.6 tf、`RC-2012-4` 本次也先寫成 112,646，已兩題統一為 **112,648 kgf ＝ 112.65 tf**。
- 2026-08-22 待辦清單至此清空；`RC-2007-4` 的自創容許值（$0.4f'_c$、$3\sqrt{f'_c}$）仍未處理，
  屬 2026-08-22 第一輪 XCHECK 的待辦 1，與本次無關。

## 2026-09-07

- **[FIX]** 修正 RC-2012-4 解答：接頭剪力檢核，柱剪力 V_col 採用已分擔過的值（M_pr/l_n），並補計 phi=0.85；更新相關數字與利用率。
- **[FIX]** 補充 RC-2013-2 解答：第一支箍筋位置，明確區分柱用 s/2、梁用 5 cm。
- **[UPDATE]** 執行腳本與更新：更新圖檔 (apply_figs.py) 與五題相關圖檔，並重新編譯更新相關 study 與 wiki 頁面。

## 2026-09-27

- **[ADD]** 於 `study/` 內新增 RC-U4-1 相關之四個子主題目錄：
  - `RC-U4-1 三項應力的加減`
  - `RC-U4-1 六階段四控制點`
  - `RC-U4-1 從檢核到設計`
  - `RC-U4-1 斷面與施工時序`
  包含繪圖腳本 (`gen_figs.py` 等) 及產出之 SVG/PNG 圖片、簡報檔與 PDF 檔案。

## 2026-10-01：`RC-2008-2` 斷面讀錯改正（做解題影片時對照原卷發現）

- **[FIX]** 原卷圖二為 X 向 h = 8+20+20+8 = 56 cm、Y 向 b = 20+20 = 40 cm，配筋右排（壓力側）4 根、中排 2 根、左排 2 根；舊版誤讀為 56×56、3-2-3。
  全題重算：Cc 456,960、Cs1 79,143、Cs2 22,840 kgf → **Pn = 558.9 tf、Mn = 56.04 tf·m**（舊 722 / 68.2）；
  平衡點 Pb 308.6、Mb 69.37；φMn 峰值 51.07（εt = 0.005）；P0 824.7；純彎 29.26。
- **[UPDATE]** `raw/solutions/RC-2008-2/RC-2008-2.md`（§1–§5）、`figs/gen_RC-2008-2.py`＋三張圖重出、`RC-2008-2-pm-viz.html`、
  `study/problems-view/RC-2008-2.html`（單題重建）、`wiki/problems/RC-2008-2.md`、`study/lecture-RC-U1-2.html` 範例 A、
  標籤「方形柱」→「矩形柱」（question_index.json、dashboard-data.js、study-RC-U1-2.html、PM-INTERACTION-DIAGRAM、RC-2002-2）、`scripts/apply_figs.py` 圖說。

## 2026-10-09 subject-frequency-map v1.1：重跑 RC 全科出題頻率熱圖 `study/frequency-RC.html`

- **[ADD]** `scripts/build_frequency.py`（v1.1，取自 subject-frequency-map skill 附錄，未修改）——之後一律在根目錄跑 `python scripts/build_frequency.py`。
- **[UPDATE]** `study/frequency-RC.html` 以 v1.1 重產（52,586 字元）：新增前／後半期比較與升溫／冷凍標記、後半期排名、可點熱圖（題目頁／影片）、每年合計、可排序排名表。
- 對帳通過：24 考年（2002–2025）／100 題／14 個子項（13 個出現過）；前半 2002–2013、後半 2014–2025。

### 觀察（全部抄自 build_frequency.py 主控台摘要）

- 單元權重：U1 33（33.0%）、U2 14（14.0%）、U3 29（29.0%）、U4 24（24.0%）。
- 全期前五：U1-1 19、U3-3 16、U4-1 13、U1-2 12、U3-2 7，合計 67 題。
- 後半期前五：U1-1 14、U3-3 5、U1-2 5、U4-1 4、U2-1 4。
- 升溫：U1-1 5→14、U4-2 1→4；新出現：U4-4 0→1。退燒：U3-3 11→5、U4-1 9→4、U3-1 5→1。
- 冷凍：U2-3（最後 2003）。0 題：U1-4。工具型（副>主）：U2-1（主 7／副 9）。
- 教材齊全：U1-1、U1-2、U2-1、U3-3、U4-1。影片：題目 11 支、單元 0 支；problems-view 100 題；已驗證 7 題。

## 2026-10-13 影片講義新增與檔名整理

- **[ADD]** 新增 5 單元影片講義 HTML、截圖與影片檔（`影片講義/`）：
  - RC-U1-1（梁彎矩強度分析與設計）
  - RC-U1-2（柱強度分析與設計）
  - RC-U2-1（剪力強度分析與設計）
  - RC-U3-3（韌性要求與耐震設計）
  - RC-U4-1（預力梁斷面應力分析）
  - 包含黑板截圖素材（`img/`）與講解影片（`video/`，解題過程影片略過不納入版控）。
- **[FIX]** 統一檔名規範：將 `RC-U1-1_RC 梁彎矩強度分析與設計.html` 更名為 `RC-U1-1_RC梁彎矩強度分析與設計.html`（去除中間空格以與其他單元命名一致）。

## 2026-10-24 觀念講義向量圖解全面改版與繪圖腳本建置

- **[FEAT]** 講義向量圖解由公式精準計算座標重繪（U1-1、U1-2、U2-1、U3-3、U4-1）：
  - `study/lecture-RC-U1-1.html` & `.pdf`：梁彎矩強度分析與設計（應力塊、應變幾何、平衡鋼筋比等向量圖改版）。
  - `study/lecture-RC-U1-2.html` & `.pdf`：柱強度分析與設計（P-M 互制曲線、Whitney 應力塊與變形幾何改版）。
  - `study/lecture-RC-U2-1.html` & `.pdf`：剪力強度分析與設計（剪力破壞角、剪力筋分擔比、間距上限等向量圖改版）。
  - `study/lecture-RC-U3-3.html`：耐震設計與韌性要求（塑鉸區圍束箍筋、耐震剪力要求等向量圖改版）。
  - `study/lecture-RC-U4-1.html` & `.pdf`：預力梁斷面應力分析（兩階段四控制點、應力合成圖解改版）。
- **[ADD]** 新增 4 支圖形自動生成與替換腳本（`scripts/`）：
  - `scripts/gen_lecture_RC-U1-2_figs.py`
  - `scripts/gen_lecture_RC-U2-1_figs.py`
  - `scripts/gen_lecture_RC-U3-3_figs.py`
  - `scripts/gen_lecture_RC-U4-1_figs.py`
- **[NOTE]** 踩坑／下一步提醒：
  - 各單元圖解幾何改由題目與規範數值精確推導計算，避免手繪比例偏差。
  - 後續若講義內容或規範數據有微調，可直接重跑對應的 `scripts/gen_lecture_RC-*.py` 進行更新。

## 2026-10-31 全庫主／副分類與引用關聯複核修正

- **[FIX] 分類（question_index.json＋解析表頭＋wiki 題目頁同步）**：
  - RC-2004-4：主 U1-2→**U1-3**，副 U1-3→U1-2（整題為細長比驗核，與 2006-2、2016-3 一致）
  - RC-2004-1：副補 **U2-3**（第二子題為耐震受撓搭接）
  - RC-2004-5、RC-2011-5、RC-2018-4：移除副 U4-3（有效預力題給，無損失計算）
  - RC-2006-4、RC-2007-4、RC-2008-4：移除副 U4-2（Pe、e 題給，與 2014-4、2021-4 統一）
  - 接頭剪力統一：2003-3 移除 U2-1、2012-4 移除 U1-2、2018-2 副 U1-2→U1-1（有用 Whitney 求梁端彎矩者標 U1-1）
  - RC-2009-1：副補 U2-1（柱設計剪力 Ve、Vc=0 條件，與 2012-3 一致）
  - RC-2021-4：designMethod 概念題→**WSD**（08-08 已記錄待改）
  - RC-2012-1：索引 tags 先拉法／有黏結腱→後拉法／有黏裹腱（與 2026-08-22 勘誤一致）
  - RC-2018-2～RC-2019-3 六題解析表頭：主分類由單元級（`RC-U3`）改回子項級；RC-2017-4 wiki 頁補副分類行
- **[FIX] RC-2023-1 wiki 題目頁**：原為解析正本的逐位元組複本，改寫為 SPEC §7.1 摘要頁（題幹摘要／核心考點／關鍵步驟／相關題目）
- **[FIX] 相關題目**：24 頁的「相關題目」原依題號湊數或連到無關子項（說明文字亦不符），改為同考點題目、說明取自目標題標題；另 5 頁刪除單條錯連；RC-2005-5 移除不存在的 RC-2013-5／2017-5／2020-5；RC-2012-3「相關陷阱」內的題號移回相關題目
- **[FIX]** RC-2010-1 互動圖連結改為 `../../raw/solutions/RC-2010-1/RC-2010-1-pm-viz.html`
- **[FIX] 本檔亂碼**：1,264 行 UTF-8 被 cp1252 重複編碼（`æ“ä½œ` 類），逐行還原，0 行殘留
- **[SYNC]** dashboard-data.js（18 列，含 4 列既有標籤落差）、knowledge_graph.html 資料列（27 列，僅改 p(...) 資料列，未用 generate_knowledge_graph.py 重產——其輸出格式與現行檔差異大，待另行處理）、wiki/index.md（RC-2004-4 移至 U1-3）、frequency-RC.html（build_frequency.py 重跑，對帳通過）、problems-view 16 頁表頭分類行
- **[SYNC] 命題分析頁**（unit-exam-intel verify.py 五頁全過）：U1-2 主 12→11、副 8→7（2004-4 改副；2012-4、2018-2 移出），漂移表改前 5／後 6；U1-1 副 3→4（加 2018-2）；U2-1 2003-3 換 2009-1；U4-1 設計法表 WSD 7→8、全科 WSD 16→17
- 複核報告：`複核報告_分類與引用_2026-10-31.md`
- **[FIX]** problems-view 另有 8 頁（RC-2003-3、2004-1、2007-4、2008-4、2009-1、2018-3、2018-4、2019-3）是舊管線產物，以 `scripts/gen_problems_view.py` 單題重建：修正清單被 nl2br 壓成段落、數學式未遮罩（2008-4 `f'_{c2}` 被轉成 `<em>`、2018-4 `\!` 被吃、2009-1 `<` 轉義），內容不變；重建後 `--check` 8/8 一致

## 2026-10-31 problems-view 全庫正規化

- **[FIX]** `python3 scripts/gen_problems_view.py . --all`：重建前 `--check --all` 有 53 頁與現行管線不一致（皆為舊管線產物），重建後 100/100 一致
  - 修正類型：清單被 nl2br 壓成 `<br />` 段落（無 `<ol>`/`<ul>`）、數學式未遮罩就送進 markdown（`_` 被當強調吃掉、`<` `&` 被轉義、`\!` `\\` 被吃）
  - 逐頁比對新舊頁純文字：差異僅限清單符號與數學式字元，無 HTML 手改內容遺失
- **[FIX]** Playwright 實測 100 頁 KaTeX：共 15,258 個式子，3 處解析錯誤皆為正本筆誤，已改正本後單題重建：
  - RC-2018-1 §3.5 Step 3 式尾多一個 `}`
  - RC-2008-3 `\text{ 根 #4 縱向鋼筋}`、RC-2012-3 `\text{（4 leg #4）}`：`\text{}` 內的 `#` 須寫 `\#`
  - 改正後全庫 0 處 KaTeX 錯誤

## 2026-10-31 formula-given 五頁升級 v2 ＋ 套用新分類

- **[UPGRADE]** `study/formula-given-RC-{U1-1,U1-2,U2-1,U3-3,U4-1}.html/.pdf` 由 v1 升級 unit-formula-map v2：卡片補 `c` 欄位、逐年表三態（✔ 印出／✗ 考了沒給／· 未考）＋表底合計列＋題號連 problems-view、回想模式、sticky 表頭依導覽列高度；PDF 以 MathJax＋WeasyPrint 重出
- **[FIX] 既有 bug**：五頁的卡片容器與 `<section id="cards">` 同 id，v1 渲染時把整個區段（含篩選鈕）覆蓋掉；容器改名 `cardbox`
- **[SYNC] 套用 2026-10-31 分類修正**：
  - U1-2：2004-4 改副考點；2012-4、2018-2 移出 → 刪接頭三卡（Vjh、Vn、Mpr）與「接頭 √f'c Aj」欄，E 群改名「加大柱與載重組合」；30→27 條、題目 20→18 題
  - U1-1：加 2018-2（副），Whitney 三卡 no 補 2018；題目 22→23 題
  - U2-1：2003-3 移出、2009-1（副）加入，「Vc=0 條件」「Ve」兩卡 no 補 2009
- **[FIX] 內容依 [[solve-design-vs-nominal]] 更正**：U1-2「最大彎矩出現在平衡點」改為「最大極限彎矩的位置：標稱 vs 設計」（104年一 答案在 εt=0.005，104.1 vs 88.3 tf·m），連帶改平衡點卡說明、背誦策略第 3 條、104 年備註；U1-1「εt ≥ 0.004」卡說明改正 104年二 峰值在 0.005 不在 0.004
- **[FIX]** U1-1 Ec／kd／μφ 三卡 no 原含 2005（引用的 94年一 屬 U1-2 柱題），移除並在說明註明單元
- 驗證：verify.py 五頁全部一致；Playwright 五頁無 pageerror、0 個 KaTeX 錯誤、題號連結數＝本單元題數（23／18／16／18／21）、回想模式可蓋可翻；PDF 文字層無原始 LaTeX、無 emoji，逐年表含合計列單頁
- 合計：U1-1 ✔19／✗68、U1-2 ✔13／✗29、U2-1 ✔9／✗35、U3-3 ✔11／✗21、U4-1 ✔13／✗37

## 2026-10-31 導入單元總覽（unit-overview），五單元改版

- **[ADD]** `scripts/build_unit_page.py`、`scripts/unit_page_template.html`（取自 unit-overview skill；順手修正 SUBJ_NAME 的 SM／MM 對調：SM＝土壤力學、MM＝材料力學）
- **[ADD]** `study/data/unit-RC-{U1-1,U1-2,U2-1,U3-3,U4-1}.json` → `python scripts/build_unit_page.py --all` 產生 `study/unit-RC-*.html`；PDF（Playwright，A4、scale 0.85）`study/unit-RC-*.pdf`
  - 內容來源：考點群、漂移、題型走向、命題風險、只剩三天取自原 study-（命題分析）；公式卡、逐年備註、判定方法、背誦策略取自原 formula-given-（給／背 v2）
  - 設定：`giveCol:false`（RC 的 give 類分散各欄）、`showDesignMethod:true`；風險表加「必背公式」欄
  - 逐年表新增欄位：U1-1「kd/μφ 韌性」「設計流程」「鋼筋間距」、U1-2「摩擦剪力」「載重組合」、U4-1「Pe 給定」（原 v2 頁這幾張卡沒有對應欄）
  - 「設參考公式區次數」＝ 五單元逐年表合併，24 年中有 20 年印過任何 RC 公式
- **[FIX] 逐題公式用途**：「考了卻沒給」由年份層級改為逐題（`Q[].f`），每條公式以 regex 對本單元題解計數、差異逐一開題解判斷；同年多題時分配到實際用到的那題。各單元 footer 列出相對舊版的證據更正（U1-1 12 處、U1-2 9、U2-1 7、U3-3 4、U4-1 8），主要是：
  - U1-1「φ 過渡式」移除 109–112 年（各題算出皆為拉力控制 φ=0.90）、「載重組合」移除 113 年；U1-2「柱 φ」移除 110、113 年（求標稱值）；U3-3「耐震組合」移除 101 年；U4-1「ωp」移除 102／107／112 年、「預力 Mn」移除 102 年（102年四 只求 Mcr 與極限應變）
  - 卡片說明（meta）裡的題號同步改正
  - U1-2 RC-2015-1 摘要改為「峰值在拉力控制界限，不在平衡點」
- **[SYNC]** 舊 `study-RC-*.html`、`formula-given-RC-*.html` 改為轉址頁（分別轉 `unit-…#s1`、`#s2`）；`formula-given-RC-*.pdf` 未刪（已無頁面連結）
  - `study/problems-view/*.html`（100 頁）：「命題分析」鍵改「單元總覽」指向 `../unit-RC-Un-m.html`；跟隨來源腳本加認 `unit-`
  - `study/lecture-RC-*.html`：導覽列「命題分析」「給／背分界」兩鍵合併為「單元總覽」
  - `scripts/build_frequency.py`：教材偵測加 `unit`（有 unit- 時不再列 study／formula）、說明文字改指單元總覽；重跑 frequency-RC.html，對帳通過
- 驗證：`build_unit_page.py --check` 五頁通過（題目集合＝索引主＋副）；Playwright 1280／390 寬：無 console 錯誤、`.katex-error` 0、`scrollWidth` 不超出視窗；PDF 文字層無原始 LaTeX

## 2026-11-01 ARCHIVE-WIKI：wiki 封存，只保留 wiki/queries/

- **[MOVE]** `wiki/` 的 code-ref、concepts、diagnosis、failure-modes、materials、methods、philosophy、problems、traps 九個目錄及 `index.md`、`by-year.md` 移至 `archive/wiki/`（mv，未刪除）；`wiki/log.md` → `wiki/queries/log.md`（本檔）
- **[ADD]** `archive/README.md`：封存原因（未經驗證的 AI 摘要，SS 同類頁面掃描發現 45 處錯誤；內容與 raw/solutions、study/ 重複）與替代來源
- **[KEEP]** `raw/solutions/methods/`、`raw/json/concepts.json` 原地保留
- **[SYNC]** `index.html`：wiki 導航卡改為「🔍 稽核與分析報告」「📝 變更紀錄」，標題改「知識庫導覽」；ingest／compile all／lint wiki／add concept 標「已停用（2026-11-01 wiki 封存）」
- **[SYNC]** `study/lecture-RC-{U1-2,U2-1,U3-3,U4-1}.html` 的 wiki 連結改指 `archive/wiki/`、log 改指 `wiki/queries/log.md`；四份 PDF 重產（38／27／33／31 頁）
- **[SYNC]** `scripts/xcheck.py` 衍生目錄不存在時改掃 `archive/`；`generate_knowledge_graph.py` 路徑改指 `archive/wiki/` 並註明不再重產
- **[DOC]** CLAUDE.md（資料流、目錄樹、規則 1 methods 修改改為兩條件「驗算＋記 log」、規則 3/4/5/7、CHANGELOG）、CLAUDE-CODE.md、CLAUDE-SPEC.md、CLAUDE-SOLVE.md、README.md、知識庫使用說明書.md、檔案架構索引表.md、.gitattributes（加 `archive/**`）、`wiki/queries/index.md`
- 2026-11-01｜REMOVE-VIZ-PDF＋DASHBOARD｜比照 exam-wiki-SS 同日處理：① 廢止題解互動圖——刪除 `raw/solutions/` 下 18 份 `*-viz.html`（pm 12、curve／section／prestress／stress 各 1、RC-2023-1 兩份 analyzer／lifecycle），移除 RC-2018-2／2018-3／2018-4 正本與 problems-view 的「互動圖：無」欄，`question_index.json` 移除 100 個 `hasViz`，`scripts/build_unit_page.py`＋模板移除 📊 圖示並重建 5 份 `study/unit-RC-*.html`（差異僅 viz 旗標）；② 移除補充筆記 PDF——刪除 `RC-2023-1.pdf`、`RC-2023-1_補充.pdf`，正本與 problems-view 刪除對應連結；`dashboard-data.js` 改為 5 欄（去 viz、pdf）；③ `index.html`：完整解析改連 `study/problems-view/`（舊 `#md=` 深層連結與 [[題號]] 自動導向）、刪「指令速查」分頁、工作流程表改現行做法、導覽卡以全科熱圖取代舊出題頻率分析並加「⌨️ 指令清單」、新增單元教材區、統計卡「全部 verified」更正為「已收錄題目」（實際 7 verified／93 unverified）並以 USD／WSD 題數取代互動圖題數、修 ensureDir 在 dirHandle 宣告前呼叫之 TDZ（靜默恢復授權從未生效）、選到的資料夾須含 raw/solutions/本科題號、搜尋多關鍵字＋副考點名稱、結果筆數與清除篩選等；④ 規則文件（CLAUDE／CLAUDE-SOLVE／CLAUDE-SPEC／CLAUDE-CODE／README／檔案架構索引表／知識庫使用說明書）同步。公式渲染：以 study/assets/katex 0.18.1 依 auto-render 規則重算 100 頁 14,944 個數學式，錯誤 0；正本無控制字元／未跳脫 % 問題。

## 2026-11-06 清理 study 觀念簡報與旁白稿檔案

- **[CLEANUP]** 移除 `study/` 下 5 個單元簡報與向量圖資目錄（RC-U1-1、RC-U1-2、RC-U2-1、RC-U3-3、RC-U4-1，共 482 檔）及旁白稿（`旁白稿_RC-*.md`），教材正式回歸外部專用簡報與影音專案管理，使本知識庫聚焦於考題解析正本與單元總覽網頁。

## 2026-11-11 由 exam-wiki-RC 搬入 structural-exam-wiki/RC/

- **[MIGRATE-RC]** 只搬檔案、不含 git 歷史；原 repo `exam-wiki-RC` 與舊網站維持不動。搬入 `raw/`、`study/`、`wiki/queries/`、`archive/`、`影片講義/`、儀表板（原版 `RC_*`）；原 repo 根目錄兩份複核報告移入本目錄；CLAUDE*.md、xcheck.py、知識圖譜存 `archive/exam-wiki-RC-root/`；`scripts/` 只留 `gen_lecture_RC-*_figs.py`、`apply_figs.py`。逐檔比對：`raw/` 只有 `syllabus_taxonomy.json` 副本中繼資料不同（sync_taxonomy 重新同步）；`影片講義/`、`archive/`、`wiki/queries/` 一致。
- **[RENDER]** 100 頁 problems-view 改用根目錄 `render_problem_view.py` 重產（取代 `gen_problems_view.py`）：11 頁相同、89 頁差異僅為數學式 `<>&` 跳脫、斜體內粗體、表格內 `[[ID]]` 徽章、RC-2009-1 引言後清單恢復；頁首／按鈕／圖片／表格／標題數不變。5 頁單元總覽與 `frequency-RC.html` 以根目錄腳本重產：拿掉已不存在的 🎬 解題影片與記憶片 PDF 連結（11-06 移出）、返回列（無 start.html）。
- **[AUDIT]** `audit_classification.py RC RC`：0 題指向他科；RC-2009-2 標頭設計法「工作性分析（非強度設計）」≠ 索引 USD，待使用者決定（見 SUBJECT.md §10）。`xcheck.py RC`：A=0、B=0、C=0。

## 2026-11-12 PROBLEM-SPLIT-RC-U1-1-B1：題目正本草稿（RC-U1-1 2002–2015，9 題）

- **[ADD]** `raw/solutions/<id>/<id>-problem.md` 9 份（判讀狀態「待確認」）：RC-2002-4、2004-2、2005-2、2007-1、2011-2、2014-1、2014-2、2015-2、2015-3；PyMuPDF 110 dpi 全頁盲讀＋附圖 450–600 dpi，盲讀後才比對解析 §1
- **[ADD]** 證據圖 `RC-2004-2-fig-2.png`、`RC-2011-2-fig-2.png`（500 dpi 重新擷取；原 fig-1 壓有滑鼠游標，保留不刪）
- **[INDEX]** `question_index.json`：`tagSystem` 補 `problemStatus` 說明；9 題加 `"problemStatus": "draft"`
- **[RENDER]** 9 頁 `study/problems-view/` 重產（新增題目正本區塊）；KaTeX 1,749 式錯誤 0、殘留錢號 0
- **[FINDING]** §1 比對 ✅4／⚠️3／❌2：RC-2002-4 所求為 φMn（解析答 Mn 108.2 → φMn 97.3 tf-m）；RC-2011-2 PDF 向量量測證實 h=110、d=100（解析採 h=100、d=90，φMn 297.5 → 358.7 tf-m）。詳見 `題目正本-RC-U1-1-批1-2026-11-12.md`
- 解析 .md 未改；備份＝git HEAD 4102f91（本批開始時工作樹乾淨）

## 2026-11-12 PROBLEM-SPLIT-CONFIRM-RC-U1-1-B1：題目正本確認、§1 改寫、重繪附圖

- **[CONFIRM]** 使用者確認 9 份題目正本（關卡一）：`scripts/fixes/2026-11-12_confirm_sec1_RC-U1-1_B1.py` 把判讀狀態改「已確認」、不確定項加「使用者確認」、影響答案三項寫明使用者選擇；`question_index.json` problemStatus draft → confirmed（9 題）
- **[REDRAW]** 題目附圖重繪 4 題：`RC-2002-4/figs/RC-2002-4-fig-1-problem.svg`、`RC-2004-2/figs/…-fig-1-problem.svg`、`RC-2011-2/figs/…-fig-1-problem.svg`、`RC-2015-3/figs/…-fig-1-problem.svg`（＋2× PNG；新增 `gen_RC-2002-4.py`、`gen_RC-2004-2.py`、`gen_RC-2015-3.py`，RC-2011-2 併入 `figs/gen_RC-2011-2.py`）；render.py 溢出 0，並排對照目視一致
- **[SEC1]** 9 題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」；刪除加字：RC-2004-2「A、B 為鉸支承」、RC-2007-1 有效深度「假定」、RC-2015-3「（As 與 A's）」「從各受力面量起」（壓力筋位置改寫為本解假設）；RC-2011-2 原 §1 圖 1 移到「判讀圖解（解析自繪）」
- 2026-11-12｜FIX-RC-2002-4｜題意勘誤：考卷問「彎矩設計強度 φMn」（PDF 第 2 頁 φ 為 Symbol 字型替代失敗的點陣殘字 Im3，600 dpi 目視），舊解答標稱 Mn。原答 Mn = 108.2 tf·m → φMn = 92.1 tf·m（εt = 0.00441，φ 依淨拉應變內插 0.851，使用者選擇；舊版 ACI φ = 0.90 得 97.3 並列於 §5-3）。改 §1、§2、§3、§3.5（Step 6）、§4（Step 6、最終答案）、§5-3、tags 加「φMn設計強度」「過渡區φ值」
- 2026-11-12｜FIX-RC-2011-2｜題意（判讀）勘誤：附圖尺寸鏈 10＋90＋10 應讀 d = 100、h = 110 cm；舊解 2026-08-21 依 PNG 像素比例改讀 d = 90。證據：考卷 PDF 第 1 頁向量座標，外框寬 99.06 pt＝80 cm（1.238 pt/cm），腹寬 49.56 pt＝40.0、翼厚 12.36 pt＝10.0、全高 135.96 pt＝109.8 cm。φMn 297.5 → 358.7 tf·m，μφ 1.53 → 1.52，εt 0.002771 → 0.002755；§1、§3、§3.5、§4 全部、§5①②③④、§5⑥ 改寫；`figs/gen_RC-2011-2.py` H_MAIN 100 → 110、assert 改新值、3 張解題圖重跑；tags 加「尺寸鏈判讀」「d=100」
- 2026-11-12｜FIX-RC-2005-2｜題意勘誤（規範版本）：「ACI 規範允許之最大拉力筋量」考卷未註明版本，使用者選 εt ≥ 0.004 上限並配 1.2D + 1.6L（舊解 0.75Asb＋1.4D + 1.7L）。As,max 75.2 → 90.40 cm²，As 37.6 → 45.20，φMn 67.1 → 79.75 tf·m，wL 3.28 → 4.36 t/m；§2–§5 改寫，舊解與體系混用（4.02）列 §5① 對照；tags 加「εt=0.004上限」「1.2D+1.6L」
- **[VERIFY]** `scripts/fixes/2026-11-12_verify_errata_RC-U1-1_B1.py`：三題 46 個數值獨立重算 MISMATCHES: 0；交叉驗算：RC-2002-4 對中性軸取矩、φ 兩種寫法；RC-2011-2 彈性中性軸一次矩＝0、Asb 以 rect＋Asf 分拆法；RC-2005-2 εt 於 cmax 回代＝0.004、舊讀法數值重現
- **[STATUS]** RC-2002-4、RC-2011-2、RC-2005-2 verificationStatus → unverified（RC-2011-2 原為 verified）
- **[SYNC]** `study/data/unit-RC-U1-1.json`（2002-4、2005-2 摘要與公式用途；F「φ 過渡式」加 91年四、「εt≥0.004」「0.75ρb」「翼腹分解」「載重組合」說明；2005 年註）→ `build_unit_page.py RC-U1-1`（--check OK）＋ `unit-RC-U1-1.pdf` 重出（12 頁）；`study/lecture-RC-U1-1.html` §9 對照表三列與陷阱表 #10 → `lecture-RC-U1-1.pdf` 重出（25 頁，雲端無微軟正黑體，頁數由 28 變 25）；9 頁 problems-view 重產；`dashboard-data.js` 三題 tags 手動同步（依 SUBJECT.md §10 不跑 refresh_dashboard.py）；KaTeX 11 頁 1,876 式錯誤 0
- 其他題同類錯誤：未發現（U1-1 其餘 T 形梁題 d 皆直接給定）；複核報告 `複核報告_RC梁題七題_2026-08-21.md` 中 RC-2011-2「d=90 定案」已被本次推翻（報告不改）

## 2026-11-13 AUDIT-RC-U1-1-B1：盲解比對（RC-U1-1 2002–2015，9 題）＋ RC-2007-1 勘誤

- **[AUDIT]** 盲解比對 9 題：一致 8、⚠️ 分歧-觀念作圖 1（RC-2007-1）；報告 `wiki/queries/盲解比對-RC-U1-1-批1-2026-11-13.md`、紀錄 `wiki/queries/盲解紀錄-RC-U1-1-批1-2026-11-13.md`；新建 `wiki/queries/audit-ledger-RC.json`（9 筆）
- 2026-11-13｜FIX-RC-2007-1｜解析勘誤（遺漏檢核＋算式筆誤；答案不變）：
  改了什麼：① 補題目要求的最大間距檢核——裂縫控制 s_max = 38(2800/fs) − 2.5Cc ≤ 30(2800/fs)，fs = ⅔fy、Cc = 5 cm → 25.5 cm，實際中心距 8.57 cm ✓（§1 常見誤讀、§2、§3.5 Step 5／L2／L3、§4 Step 6、§5 彙整）；② §4 Step 3 As 二次式常數 15,859 → 31,661、909.4² 826,808 → 827,008、開方 873.6 → 836.9（結果 As = 36.3 cm² 原本就對）；③ §3.5 L2 Step 6 單位筆誤 7.10／7.04 → 71.0／70.4 tf·m。配筋 6-D29 兩排 3+3、φMn = 71.0 tf·m 不變
  為什麼錯：遺漏檢核——考卷 RC-2007 第 1 頁第一題末句「並依照鋼筋最大最小間距相關規定排列鋼筋」（100 dpi 全頁目視；題目正本 §1 一致），舊解標籤與步驟表寫「最小＋最大間距」但內文只算最小淨距；②③ 為算術／抄寫筆誤（盲解比對時發現，見報告）
  怎麼驗證：工作目錄 verify_RC-2007-1.py 重算 58 個數值（含 §5 敏感度表 16 值、7-D29 三排替代方案、新增 s_max 與中心距）MISMATCHES: 0；As 以二次式與先求 a 兩條路徑交叉一致（36.25 cm²）
  同步的下游：`study/problems-view/RC-2007-1.html`（render_problem_view.py）；`raw/json/question_index.json` verificationStatus verified → unverified、tags 加「裂縫控制間距」；`dashboard-data.js` 該列 tags 同步；`figs/` 數值未變不需重跑；`study/data/unit-RC-U1-1.json` 與 `lecture-RC-U1-1.html` 未引用被改數值，未改（講義 §7.3「三個一定要檢查的」只列最小淨距，列為建議補強）
  其他題同類錯誤：本批其餘 8 題未發現
- **[LEDGER]** RC-2007-1 `human`＝使用者同意勘誤（2026-11-13）、`fixed`＝2026-11-13
- **[DIAGRAM]** 階段 E 補解題圖解 6 題（數值皆已盲解比對一致；struct-diagram，repo `skills/struct-diagram/scripts`）：RC-2002-4 `fig-2-strain`（斷面／應變／內力，攔壓力筋未驗降伏、過渡區仍取 φ = 0.9）、RC-2004-2 `fig-2-vm`（載重／SFD／BMD，攔 8wu、D 取全梁中點、漏 B 負彎矩）、RC-2005-2 `fig-1-tsection`（As,max 與一半的應力塊對照）、RC-2014-1 `fig-1-strain`（原梁鋼筋不降伏 vs 補強後拉力控制）、RC-2014-2 `fig-1-mphi`（M–φ 三特徵點）、RC-2015-3 `fig-2-negative`（負彎矩斷面／應變／內力）。腳本：RC-2002-4、2004-2、2015-3 於既有 `gen_<id>.py` 新增函式；RC-2005-2、2014-1、2014-2 新建 `gen_<id>.py`；全部檔尾對 §4 公佈值 assert、render.py 溢出 0、PNG 目視檢查。.md 於對應步驟下插圖＋圖說，頁尾加「圖解補繪」（非勘誤）；6 頁 problems-view 重產
- **[FINDING]** 補圖時發現正本末位進位小差（不影響答案，未改）：RC-2014-1 補強後 c 精算 16.735（正本 16.74）、原梁 Mn 乘積 §4 寫 3,577,229、L2 表 3,578,334（精算 3,578,431，φMn 23.26 vs 正本 23.25）；RC-2014-2 Mcr 精算 7.098（正本 7.097）、Mn 精算 53.09（正本 53.10）

## 2026-11-13 PROBLEM-SPLIT-RC-U1-1-B2：題目正本草稿（RC-U1-1 2016–2024，10 題）

- **[ADD]** `raw/solutions/<id>/<id>-problem.md` 10 份（判讀狀態「待確認」）：RC-2016-1、2019-1、2020-1、2021-1、2022-1、2022-2、2023-1、2023-2、2024-1、2024-2；PyMuPDF 110 dpi 全頁盲讀＋附圖 400–500 dpi＋PDF 向量座標，盲讀後才比對解析 §1
- **[ADD]** 證據圖 `RC-2024-1-fig-2.png`、`RC-2024-2-fig-3.png`（圖 2a）、`RC-2024-2-fig-4.png`（圖 2b）（500 dpi 重新擷取；原 fig-1／fig-1、fig-2 壓有滑鼠游標，保留不刪）
- **[INDEX]** `question_index.json`：10 題加 `"problemStatus": "draft"`
- **[RENDER]** 10 頁 `study/problems-view/` 重產（新增題目正本區塊）；KaTeX 1,889 式錯誤 0、殘留錢號 0；分類稽核僅既有 RC-2009-2 一筆
- **[FINDING]** §1 比對 ✅6／⚠️1／❌3：RC-2020-1 圖上 70 為版頂到梁腹底（解析 h = 80、d = 74 → h = 70、d = 64，As 49.6 → 58.9 cm²，變 T 形分解）；RC-2024-1 60 cm 量到 As 形心（解析假設 d = 74 → d = 80，四個答案全變，目前 verified）；RC-2024-2 44 cm 為兩排鋼筋中心距（d = 44 → 52，φMn 34.5 → 41.9 tf-m、ωu 7.66 → 9.30 tf/m）。待確認另有 RC-2023-1 fy 未給、RC-2023-2 排筋與 d'。詳見 `題目正本-RC-U1-1-批2-2026-11-13.md`
- 解析 .md 未改；備份＝裝置工作階段 `~/bk2/`（10 份解析＋索引）；批 1 變更尚未 commit，與本批同在工作樹

## 2026-11-13 PROBLEM-SPLIT-CONFIRM-RC-U1-1-B2：題目正本確認、勘誤 3 題、§1 改寫、重繪附圖

- **[CONFIRM]** 使用者確認 10 份題目正本（關卡一）：`scripts/fixes/2026-11-13_confirm_sec1_RC-U1-1_B2.py` 把判讀狀態改「已確認」、影響答案項目寫明使用者選擇（RC-2020-1 #1、RC-2023-1 #1 fy＝4200、RC-2023-2 #1 4+4 兩排與 #2 d'＝6、RC-2024-1 #2、RC-2024-2 #1 #3 #9）；`question_index.json` problemStatus draft → confirmed（10 題）
- **[REDRAW]** 題目附圖重繪 7 題 `figs/<id>-fig-1-problem.svg`（＋2× PNG）：RC-2016-1、2019-1（既有 `figs/gen_<id>.py` 檔尾新增 fig1_problem，既有 3 張解題圖不動）、RC-2020-1、2021-1、2022-1、2024-1、2024-2（新建 `gen_<id>.py`）；render.py 溢出 0，原圖｜重繪並排對照目視一致（對照圖在 repo 外）
- **[SEC1]** 10 題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」；RC-2023-2 原 §1 自繪圖 fig-1-section 移至「判讀圖解（解析自繪）」；舊 §1 證據圖皆已在題目正本
- 2026-11-13｜FIX-RC-2020-1｜題意（判讀）勘誤：
  改了什麼：附圖 70 為版頂到梁腹底 → h＝70、d＝64（原解 h＝80、d＝74）；400 為梁中心距（淨距 350）。矩形試算 a＝11.07 > hf＝10，中性軸落入腹板，改按翼板懸出分解：As 49.6 → 58.92 cm²（Asf 31.88＋Asw 27.04），εt 0.0172 → 0.00983，As,min 12.33 → 10.67 cm²；§1–§5 全部改寫
  為什麼錯：判讀——尺寸線端點；考卷 2020 第 1 頁 PDF 向量：70 尺寸線 y＝519.0→581.2，版頂 518.0–519.0、翼板底 531.4、梁腹底 581.2；400 dpi 目視一致
  怎麼驗證：verify_RC-2020-1.py 重算 17 值 MISMATCHES: 0；由 As 正向反算 φMn＝Mu、中性軸二分搜尋兩路徑一致
  同步的下游：problems-view；question_index（tags 加 中性軸在腹板、翼板懸出分解、尺寸鏈判讀、d=64；原為 unverified）；dashboard-data.js tags；unit-RC-U1-1.json（RC-2020-1 摘要、公式用途加 #18 翼板／腹板分解；F#17、F#18 說明加 109年一）→ build_unit_page.py＋unit PDF 重出（12 頁）；lecture-RC-U1-1.html §9 題目表一列 → lecture PDF 重出（27 頁，雲端字型）
- 2026-11-13｜FIX-RC-2024-1｜題意（判讀）勘誤：
  改了什麼：圖 1 的 60 cm 由翼板底量到 As 形心 → d＝80（原解假設 h＝80、d＝74）。Case 1 As,max 106.4 → 111.4、As,min 9.87 → 10.67 cm²；Case 2 As,b 56.0 → 58.8、As,max 53.2 → 55.9 cm²；改 §1、§3.5 L1／L2、§4、§5 爭議點 1
  為什麼錯：判讀——尺寸線端點；考卷 2024 第 1 頁 PDF 向量：60 cm 尺寸線 y＝516.5→581.3、As 長條 578.2–584.4（中線 581.3）、梁底 596.7；500 dpi 目視一致
  怎麼驗證：verify_RC-2024-1.py 重算 15 值 MISMATCHES: 0；由 As 反算 εt＝0.004、εs＝εy 回代一致
  同步的下游：problems-view；question_index verificationStatus verified → unverified、tags 加 尺寸鏈判讀、d=80；dashboard-data.js tags；unit JSON 與講義未引用被改數值
- 2026-11-13｜FIX-RC-2024-2｜題意（判讀）勘誤：
  改了什麼：圖 2a 的 44 cm 為上排到下排鋼筋中心距 → d＝8＋44＝52（原解 d＝44）。φMn 34.5 → 41.9 tf·m（補列 Mn 46.5）、εt 0.0067 → 0.0085、ωu 7.66 → 9.30 tf/m；c、a、f's 不變；§5 φ 內插式更正（原「梁型式 0.75」說法有誤）
  為什麼錯：判讀——尺寸線端點；考卷 2024 第 2 頁 PDF 向量：44 cm 上端延伸線 y＝279.2（上排圓心 280.1）、下排圓心 371.4、8 cm 下端 397.7＝斷面底；400／500 dpi 目視一致
  怎麼驗證：verify_RC-2024-2.py 重算 12 值 MISMATCHES: 0；Mn 以對 As 與對混凝土合力取矩兩路徑一致、c 以迭代法交叉
  同步的下游：problems-view；question_index tags 加 尺寸鏈判讀、d=52（原為 unverified）；dashboard-data.js tags；unit JSON 與講義未引用被改數值
- **[CHECK]** 10 頁 problems-view 重產：KaTeX 1,968 式錯誤 0、殘留錢號 0；圖片引用全部存在；build_unit_page --check OK；分類稽核僅既有 RC-2009-2 一筆
- 其他題同類錯誤（自取 d 而非讀尺寸鏈）：RC-2012-2、RC-2018-1 解析也寫「假設 d」，不在本單元，列入後續批次核對
- 備份：裝置工作階段 `~/bk2/`（10 份解析、索引、unit JSON、講義 HTML 改前版本）；重算腳本在雲端工作區（未進 repo）
- 2026-11-13｜FIX-RC-2022-2｜解析勘誤（算術）：
  改了什麼：比較彙整表 φMn 組合一 22.75 → 21.57、組合三 25.67 → 22.43、組合二 19.53 → 19.51 tf·m；As,req 組合一 13.48 → 13.50、組合二 10.10 → 10.13 cm²，算式係數 1276.5 → 5355（＝0.85·210·30）；組合四 Mn 尾數 2,243,494 → 2,243,000；組合一、三補列 φMn 驗算；§5 補「組合二剛好夠（餘裕 <0.1%）」。結論 210／5600、2-D25 不變
  為什麼錯：算術——彙整表 φMn 無對應算式、係數抄寫錯；由盲解比對 RC-U1-1 批 2 發現（初版比對只看最終答案而漏報，同日更正）。題意無爭議（題目正本已確認，考卷 2022 第 2 頁 110 dpi 目視一致）
  怎麼驗證：v_2022_2.py 重算 22 值 MISMATCHES: 0；As 以閉合式與二分法反解 φMn＝Mu 兩路徑一致
  同步的下游：problems-view；question_index 原為 unverified（tags 不變）；unit-RC-U1-1.json、lecture-RC-U1-1 未引用被改數值（grep 確認）；ledger fixed、recheck（落實，非獨立）

## 2026-11-14 PROBLEM-SPLIT-RC-U3-3-B1：題目正本草稿（RC-U3-3 2003–2012，10 題）

- **[ADD]** `raw/solutions/<id>/<id>-problem.md` 10 份（判讀狀態「待確認」）：RC-2003-3、2003-4、2004-1、2004-3、2005-3、2009-1、2010-2、2012-2、2012-3、2012-4；PyMuPDF 110 dpi 全頁盲讀＋附圖 300–500 dpi＋PDF 向量座標，盲讀後才比對解析 §1
- **[ADD]** 證據圖 `RC-2003-4-fig-2.png`（fig-1 壓滑鼠游標）、`RC-2010-2-fig-2.png`（500 dpi，fig-1 解析度低）、`RC-2012-2-fig-3.png`（fig-2 壓滑鼠游標）、`RC-2012-3-fig-1／fig-2.png`、`RC-2012-4-fig-1／fig-2.png`（原無附圖檔，共用第二題附圖）；舊圖保留不刪
- **[INDEX]** `question_index.json`：10 題加 `"problemStatus": "draft"`
- **[RENDER]** 10 頁 `study/problems-view/` 重產（新增題目正本區塊）；KaTeX 1,625 式錯誤 0、殘留錢號 0；分類稽核僅既有 RC-2009-2 一筆
- **[FINDING]** §1 比對 ✅6／⚠️2／❌2：RC-2003-3 柱方向讀反（考卷 X 向 40、Y 向 50）且漏讀 X 向梁與柱面齊平（$b_j$ 40 → 24，φVn 150.8 → 53.3–72.4 tf，結論可能由足夠翻為不足）；RC-2003-4 牆厚 30 → 15、層高 450＋450 → 350＋450、P 為兩端各 50 靜＋25 活並有屋頂 w、900 為邊界構材中心距（BE 最大壓力 84.3 → 165.2 tf，整題需重解）；RC-2012-2 圖說「保護層 6／淨尺寸 48」用詞、RC-2012-4「原卷標為設計強度」不實（答案不受影響）。題意以外：RC-2012-3 $b_c$ 取主筋中心 48（s＝9）vs 規範箍筋外緣（s＝13）待使用者選擇。詳見 `題目正本-RC-U3-3-批1-2026-11-14.md`
- 解析 .md 未改；備份＝裝置工作階段 `~/bk3/`（10 份解析＋索引）；RC-U1-1 批 1、批 2 變更仍未 commit，與本批同在工作樹
- 2026-11-14 關卡一（影響答案項目）使用者選擇：RC-2003-3 採 X40／Y50＋X 向梁齊平；RC-2003-4 全部採用、整題重解；RC-2012-3 $b_c$ 改依規範量到箍筋外緣（同步 RC-2012-4）。其餘判讀項待整批確認；problem.md 仍為「待確認」

## 2026-11-14 PROBLEM-SPLIT-CONFIRM-RC-U3-3-B1：題目正本確認、勘誤 4 題、§1 改寫、重繪附圖

- **[CONFIRM]** 使用者回覆「判讀確認」（關卡一）：`scripts/fixes/2026-11-14_confirm_sec1_RC-U3-3_B1.py` 把 10 份題目正本判讀狀態改「已確認」、影響答案項目寫明使用者選擇（RC-2003-3 #1 #2、RC-2003-4 #1 #4 #6），`question_index.json` problemStatus draft → confirmed（10 題）、四題 tags 追加；腳本可重複執行（已確認者略過）
- **[REDRAW]** 題目附圖重繪 7 題 `figs/<id>-fig-1-problem.svg`（＋2× PNG）：RC-2003-3、2003-4、2010-2、2012-2、2012-4（新建 `gen_<id>.py`）、RC-2004-3、2012-3（既有 `figs/gen_<id>.py` 新增 problem 圖函式，既有圖不動）；render.py 溢出 0；原圖｜重繪對照（repo 外）目視一致；RC-2012-2／3／4 共用同一組幾何，各自輸出
- **[SEC1]** 10 題解析 §1 改為「指向題目正本＋常見誤讀＋本解記號」；RC-2004-3 原 §1 自繪圖 fig-1-section 移至「判讀圖解（解析自繪）」；RC-2012-3／2012-4 的延用數值表保留為「本解記號與延用數值」；舊 §1 證據圖皆已在題目正本
- 2026-11-14｜FIX-RC-2003-3｜題意（判讀）勘誤：
  改了什麼：柱方向 X 向 50／Y 向 40 → X 向 40／Y 向 50（接頭深度 h＝40）；X 向梁由置中改為上緣與柱面齊平（偏心）→ b_j 40 → 24 cm、A_j 2,000 → 960 cm²；梁筋拉力 f_y → 1.25f_y（V_u 62.0 → 77.55 tf）；γ 5.3（四面）→ 4.0（一雙對面：X 向梁 24 cm < 3/4×50）；φV_n 150.7 → 54.62 tf；結論「符合」→「**不符合**」（V_u/φV_n＝1.42）；§1–§5 全部改寫
  為什麼錯：判讀——斷面 A-A 座標軸 X 向右，40cm 為水平尺寸；X 向梁上緣、24cm 與 50cm 尺寸線上端同一水平線（考卷 2003 掃描頁背面圖 4，300 dpi 目視）；觀念——四面有梁不等於四面圍束、耐震接頭用 1.25f_y
  怎麼驗證：verify_RC-2003-3.py 重算 13 值 MISMATCHES: 0；柱剪力另以由 M_n 反推 d＝54.0 cm 精算 M_pr 交叉（V_u 77.78，差 0.3%）；γ 取 5.3 或拉力取 f_y 結論仍為不符合
  同步的下游：problems-view；question_index（原為 unverified；tags 加 偏心梁、1.25fy、一雙對面圍束、柱方向判讀）；dashboard-data.js tags；unit-RC-U3-3.json（RC-2003-3 摘要；F#11、F#12 說明）→ build_unit_page.py＋unit PDF 重出（20 頁）；lecture-RC-U3-3.html §6.2 錨點段落 → lecture PDF 重出（31 頁，雲端字型）；methods/seismic-capacity-method.md 錨點句（見下）
- 2026-11-14｜FIX-RC-2003-4｜題意（判讀）勘誤，整題重解：
  改了什麼：腹版厚 30 → 15 cm；層高 450＋450 → 350＋450（h_w＝800）；P 由「合計 50、每端 25、無活載」→ 兩端各 50 靜＋25 活，並計入屋頂 w 5＋1 tf/m；900 cm 由牆全長改為邊界構材中心距（l_w＝930、力臂 900）。A_cv 27,000 → 13,950 cm²；M_E 360 → 330 tf·m；BE 最大壓力 84.5 → 165.16 tf、BE 由受拉 36.7 tf 改為只受壓（最小 12.82 tf）；壓力構材 φ 0.65 → 0.70（與 1.4D＋1.7L 同版）；BE 主筋 4-#8 → 6-#8（4-#8 差 0.1%）；BE 箍筋 #4 閉合箍＋#4 繫筋 @7.5 cm（A_ch 改量至箍筋外緣 484 cm²）；腹版水平／垂直筋 #4@15 → #4@30（單層，ρ＝0.00282）；l_dh 19.13 cm < BE 核心 24.73 cm；垂直筋改依耐震專章 ρ_v ≥ ρ_h
  為什麼錯：判讀——平面圖 15cm 為腹版厚、30×30 為邊界構材；立面 350／450 兩段；兩支 P 各在一端；900 延伸線落在邊界構材中心（考卷 2003 掃描頁背面圖 5，400 dpi 目視）；另「作廚房用」為誤植（考卷「作耐震用」）
  怎麼驗證：verify_RC-2003-4.py 重算 37 值 MISMATCHES: 0；BE 主筋以反解 A_st 與代回 φP_n 兩路徑一致；邊界構材需求以全牆斷面應力 33.4 kgf/cm² < 0.2f'c 交叉
  同步的下游：problems-view；question_index（原為 unverified；tags 加 尺寸鏈判讀、邊界構材中心距、腹版厚15、層高350+450）；dashboard-data.js tags；lecture-RC-U3-3.html §7.1 覆沒彎矩段落 → lecture PDF 重出；unit-RC-U3-3.json／unit-RC-U2-1.json 摘要未引用被改數值（不改）
- 2026-11-14｜FIX-RC-2012-3｜解析勘誤（b_c 量測基準，使用者確認）：
  改了什麼：附圖 48 cm 為主筋中心距（題目正本 G2），b_c 由 48 改依規範量至箍筋外緣 60−2(6−1.11−1.27)＝52.76 cm、A_ch 2,304 → 2,783.6 cm²；A_g/A_ch 1.563 → 1.293（式②控制）；圍束容許間距 9.41 → 16.0 cm；控制條件由圍束式改為 6d_b＝13.3 cm；塑鉸區箍筋 4-leg #4 @9 → **@13 cm**；φV_s 96.0 → 66.5 tf；§5④ 取法 A／B 主從互換；圖 2（間距六候選）、圖 3（b_c 兩種取法）重產並修正圖內圖號
  為什麼錯：規範定義——A_sh 式的 b_c、A_ch 量至橫向鋼筋外緣；附圖 6 cm、48 cm 尺寸線端點在主筋中心（考卷 2012 第 2 頁附圖，450 dpi 目視）
  怎麼驗證：verify_RC-2012-3.py 重算 20 值 MISMATCHES: 0；gen_RC-2012-3.py 檔尾對帳 37 項全 OK
  同步的下游：problems-view；question_index（原為 unverified；tags 加 bc量至箍筋外緣、6db控制）；dashboard-data.js tags；unit-RC-U3-3.json（RC-2012-3 摘要）→ unit 頁與 PDF；lecture-RC-U3-3.html §4.1 式①／②判別例、§4 陷阱「hc（或 bc）的量法」、§5 手算例 ③ 與自我檢查 ① → lecture PDF；RC-2012-4（見下）
- 2026-11-14｜FIX-RC-2012-4｜解析勘誤（同步 RC-2012-3）：接頭箍筋 4-leg #4 @9 → @13 cm，並更正為「第三題設計結果」（原寫「題目給定」）；刪除「原卷把三式標為『設計強度』」的不實引述（考卷標題為「梁柱接頭剪力強度規定」）；接頭剪力 V_jh 134.5 tf、φV_n 163.85 tf 與結論不變；驗證：grep 全文無 @9 殘留
- **[METHODS]** `raw/solutions/methods/seismic-capacity-method/seismic-capacity-method.md`：γ 錨點句刪除「RC-2003-3（內接頭＝5.3）」，改寫為圍束定義（梁寬 ≥ 3/4 面寬）並以 RC-2003-3 為反例；題目表 RC-2003-3 說明加「偏心梁 b_j、圍束面判定」。驗證：與 RC-2003-3 勘誤後 Step 5 圍束判定表一致（24 < 37.5、40 ≥ 30）；study 中引用此句的 lecture §6.2 已同步
- **[FIX-LECTURE]** lecture-RC-U3-3.html §5 手算例 ⑤ 數學式 `\text{（只差 0.8%！）}` 的 % 未跳脫（既有 KaTeX 錯誤 1 個）→ `0.8\%`；講義 PDF KaTeX 錯誤 0
- **[CHECK]** 10 頁 problems-view 重產：KaTeX 1,673 式錯誤 0、殘留錢號 0；圖片引用全部存在；build_unit_page --check OK；generator 腳本在本機重跑輸出與 repo 一致（差異僅寫回時附加的檔案來源中繼資料）
- 備份：裝置工作階段 `~/bk3/`（10 份解析、索引、seismic-capacity-method.md 改前版本）；重算腳本在雲端工作區（未進 repo）
- 其他題同類錯誤：無引用 RC-2003-3／2003-4／2012-3 被改數值的其他題解；RC-2012-2 的 b_c 未使用（只算 M_pr），不受影響

## 2026-11-14 CODE-UPDATE-RC-U3-3-B1：RC-2003-3、RC-2003-4 改依現行台灣規範

依根目錄 `CLAUDE.md`「規範版本」（同日新增：考古題一律用現行最新台灣規範，題目印出的舊規範式子也改用現行規範），階段 B 盲解前先改寫這兩題。
- 2026-11-14｜FIX-RC-2003-4｜規範版本改寫（整題重算）：
  改了什麼：考卷印出的舊組合 0.9D±1.43E、0.75(1.4D+1.7L±1.87E)、剪力 φ＝0.6、彎鉤式 0.06f_y d_b/√f'c 改用建築物混凝土結構設計規範 2023 年版（1.4D；1.2D+1.6L；1.2D+1.0L+1.0E；0.9D+1.0E；φ 壓 0.65、剪 0.75；ACI 318-19 式 25.4.3.1 彎鉤）；地震力依讀法 B（使用者確認）：考卷 30／20 tf 屬舊規範 αy＝1.5 層級，×1.5 換到 αy＝1.0 → V_u 71.5 → 75 tf、M_u 471.9 → 495 tf·m、BE 最大壓力 165.16 → 171.5 tf、最小 12.82 → 10.25 tf（仍為壓）；BE 主筋 6-#8 不變（φPn 187.4 → 174.1 tf）；特殊邊界構材應力法 35.1 kgf/cm² < 0.2f'c → 不需特殊邊界構材，BE 箍筋由 A_sh 控制 @7.5 改為一般邊界間距 @15 cm；腹版 #4@30 不變，φV_n 211.3 → 264.1 tf（φ 0.75，非剪力控制）；l_dh 19.13 → 15 cm（下限控制）
  為什麼改：規範版本政策變更（非判讀錯誤）；地震力層級依耐震規範解說「RC 地震力載重因子取 1.0 設計者 αy 取 1.0、極限強度設計 αy 可採 1.5」推論，考卷未寫 αy，§5 附讀法 A（直接當 E）與照考卷舊式的對照
  怎麼驗證：verify_RC-2003-4_v2.py 重算 38 值 MISMATCHES: 0；BE 主筋以反解 A_st 與代回 φPn 兩路徑一致；φ 判定以 V_n 352.1 tf 與撓曲強度對應剪力 263 tf 比較
  同步的下游：problems-view；question_index／dashboard-data.js tags 加「現行台灣規範」；lecture-RC-U3-3.html §7.1 覆沒彎矩段落 → lecture PDF 重出（31 頁）；unit-RC-U3-3.json 摘要未引用被改數值
- 2026-11-14｜FIX-RC-2003-3｜規範版本改寫：一雙對面圍束 γ 4.0（92 年規範換算）→ 3.9（現行），V_n 64.26 → 62.65 tf、φV_n 54.62 → 53.25 tf，V_u/φV_n 1.42 → 1.46，結論不符合不變；改善方案（梁置中）φV_n 113.8 → 110.9 tf；§1 常見誤讀「規範」列改寫；§5 改為規範版本對照，並補「梁寬 ≥ 3/4 有效接頭寬」另一圍束讀法（γ＝5.3、φV_n 72.37 tf，仍不符合）。驗證：verify_RC-2003-3.py 13 值 MISMATCHES: 0。下游：problems-view；unit-RC-U3-3.json（摘要、F#11 說明）→ unit 頁與 PDF（20 頁）；tags 加「現行台灣規範」
- **[CHECK]** 2 頁 problems-view KaTeX 368 式錯誤 0；build_unit_page OK；兩份 PDF KaTeX 錯誤 0
- 待核對：圍束面判定（梁寬比「柱面寬」或「有效接頭寬」）與彎鉤伸展長度係數，請以 2023 年版條文原文確認；兩種讀法下 RC-2003-3 結論相同

## 2026-11-14 FIX-RC-U3-3-B1-C：盲解比對分歧三題勘誤（說明題，改依現行台灣規範）

來源：`盲解比對-RC-U3-3-批1-2026-11-14.md`（三題皆 ⚠️ 分歧-觀念作圖）。B' 判定：三題皆屬規範條文內容，非看圖類；以內政部「建築物混凝土結構設計規範」112 年版原文（nlma.gov.tw a1120815.pdf）逐條核對後直接勘誤。
- 2026-11-14｜FIX-RC-2004-1｜解析勘誤＋改依現行台灣規範：
  改了什麼：㈡梁搭接位置「須在跨中 1/2」→ 三個禁區（接頭內、距接頭面 2h、距預期降伏斷面 2h；§18.3.3.3）；刪除「同一斷面搭接 ≤ 1/2」與單位錯誤的 A_v,min＝0.35b_ws/f_yt；㈠取樣頻率「每 100 m³、每班次」→ 每日／每 120 m³／每 450 m²（§26.12.2.1），補最少 5 次試驗、強度試驗定義（15×30 兩支或 10×20 三支）、鑽心 3 個平均 ≥ 0.85f'c 且單一 ≥ 0.75f'c（§26.12.6.1）、現場養護試體 85%／35 kgf/cm²；§2、§3、§3.5、§4、§5 改寫，§5③ 新增新舊版對照
  為什麼錯：觀念——把柱縱筋搭接的「中段 1/2」套到梁；規範條文——50% 規定不存在、取樣數量錯；規範版本（原依 ACI 318-99）
  怎麼驗證：逐條對照 112 年版 §18.3.3.3、§26.12.1.1、§26.12.2.1、§26.12.3.1、§26.12.6.1、§26.5.3.2(e)（說明題，無數值重算）
  同步的下游：problems-view；question_index tags 加 鑽心試驗、梁搭接禁區2h、現行台灣規範；dashboard-data.js tags；unit-RC-U3-3.json（RC-2004-1 摘要）→ build_unit_page；lecture-RC-U3-3.html 題目表摘要
- 2026-11-14｜FIX-RC-2009-1｜解析勘誤＋改依現行台灣規範：
  改了什麼：V_c＝0 由「只要 N_u < 0.05A_gf'c」→ 兩條件同時成立（地震引致剪力 ≥ l_o 內最大需求剪力之半，且 P_u < A_gf'c/20；§18.4.6.2.1）；A_sh 兩式來源說明對調更正（0.3(A_g/A_ch−1) 補回保護層剝落損失、0.09 為大斷面最低量）；圍束區間距 min(b/4, 6d_b, 15) → min(b/4, 6d_b, s_o)，s_o＝10＋(35−h_x)/3（10～15 cm），6d_b 依 f_y 分級（§18.4.5.3）；圍束區外刪「仍須提供 A_sh」；「縱筋間距 ≤ 35 cm」→ 角筋與隔根筋受支撐、h_x ≤ 35 cm；§5② 改為全高圍束（支承不連續剛性構材且 P_u > A_gf'c/10）
  為什麼錯：觀念——條件式規定只寫一半、公式來源說反；規範條文漏用（s_o 式）
  怎麼驗證：逐條對照 112 年版 §18.4.5.3、表 18.4.5.4、§18.4.6.2.1（說明題，無數值重算）
  同步的下游：problems-view；question_index tags 加 Vc=0兩條件、s0公式、現行台灣規範；dashboard-data.js tags；unit-RC-U3-3.json（RC-2009-1 摘要）→ build_unit_page；lecture-RC-U3-3.html 原已寫兩條件與正確公式來源，不改
- 2026-11-14｜FIX-RC-2010-2｜解析勘誤（㈠）＋改依現行台灣規範：
  改了什麼：㈠「搭接面積：同一斷面搭接 ≤ 50%，超過須改機械／銲接續接」→ 縱筋比 0.01A_g ≤ A_st ≤ 0.06A_g（§18.4.4.1），說明搭接比例只影響甲／乙級、柱無 50% 上限；搭接位置／拉力搭接／圍封橫向鋼筋改註 §18.4.4.3、§18.4.5.2–3；§5② 改寫為甲／乙級判定表；㈡ l_d 82.3 cm、l_s 107 cm 不變
  為什麼錯：規範條文——柱無此規定（112 年版「同一斷面搭接不超過 50%」只見於結構牆邊界鋼筋）；題意反證——考卷附圖 12 根 D29 全數同斷面搭接（2010 第 1 頁正面附圖，500 dpi）
  怎麼驗證：逐條對照 §18.4.4.1、§18.4.4.3；㈡重算 l_d＝4200/(3.5√280)×2.87/2.5＝82.3、l_s＝107、ρ＝3.1% MISMATCHES: 0
  同步的下游：problems-view；question_index tags 加 縱筋比1%-6%、現行台灣規範（舊 tag「50%面積限制」依 append-only 保留）；dashboard-data.js tags；unit-RC-U3-3.json（RC-2010-2 摘要、公式卡「Class B 搭接與位置限制」eq 與 meta、strategy 4-1 第 5 點）→ build_unit_page；lecture-RC-U3-3.html §7.3 表（搭接等級、縱筋量、新增梁搭接位置列）、題目表與陷阱表 #26
- **[CHECK]** 3 頁 problems-view KaTeX 317 式錯誤 0、殘留錢號 0；unit 頁 build OK；lecture PDF 31 頁、unit PDF 20 頁（Playwright A4，雲端 KaTeX 0.16）KaTeX 錯誤 0
- **[B' 附記]** 同日以 112 年版原文核對盲解比對中的規範疑點：梁柱接頭係數為 5.3／3.9／3.2（非連續柱另有 2.1），RC-2003-3 舊解 γ＝3.9 正確、盲解 4.0 為換算差；耐震柱圍束區間距 6d_b（f_y 4200）、s_o 10～15 cm 確認
- 其他題同類錯誤：RC-2003-2 的「100% > 50% → Class B」為正確用法（等級判定），不改；frequency-RC.html 的「50%面積限制」來自 RC-2010-2 舊 tag（append-only），不改
- **[RECHECK]** 落實檢查 RC-2004-1、RC-2009-1、RC-2010-2：皆落實（非獨立複核）；RC-2010-2 Step 6／§3.5 L3「一律／強制 Class B」與「ACI §12.2」條號殘留於檢查時補改、problems-view 重產。報告 `落實檢查-RC-U3-3-批1-2026-11-14.md`

## 2026-11-14 DIAGRAM-RC-U3-3-B1：批 1 補解題圖解（階段 E）＋收尾（階段 F）

- **[DIAGRAM]** 7 題補向量圖解（struct-diagram，數值取自已驗證正本；SVG＋2× PNG，render.py 溢出 0）：
  - RC-2003-3 圖 2 `fig-2-joint-width`：偏心梁 vs 置中梁的有效接頭寬（b_j 24 → A_j 960、φV_n 53.25 不符合；置中 b_j 50 → 110.9 符合）——攔「偏心梁拿柱寬當 b_j」
  - RC-2003-4 圖 2 `fig-2-wall-design`：覆沒軸力（171.5／61.5／10.25 tf，力臂 900）＋斷面配筋，取代 Step 6 文字示意圖——攔力臂取錯、BE 當受拉、腹版厚 30
  - RC-2004-1 圖 1 `fig-1-beam-lap`（新增腳本）：梁搭接三禁區＋密箍——攔把柱的「中段 1/2」套到梁
  - RC-2009-1 圖 1 `fig-1-column-zones`（新增腳本）：柱立面分區＋斷面箍筋繫筋、A_sh 兩式與 V_c＝0 兩條件——攔漏 s_o、V_c＝0 只看軸力
  - RC-2010-2 圖 2 `fig-2-lap`：搭接立面（l_s＝107 cm 於中段 l_n/2，淨高示意）＋縱筋比 3.1%／6.2% 對 1%–6%——攔搭接放柱端、面積答成 50%
  - RC-2012-2 圖 2 `fig-2-mpr`：正負向 M_pr 斷面（75.5／41.1 tf·m）——攔用 fy、應力塊畫錯側
  - RC-2012-4 圖 2 `fig-2-joint-fbd`：外接頭上半部自由體＋需求／強度長條（134.5 vs 163.85；誤寫加項 184.9）——攔 V_jh＝T_1＋V_col
  - 各解析頁尾加「修正日期：2026-11-14（圖解補繪：…）」（非勘誤，pending.py 不視為已勘誤）；gen 腳本在本機重跑 SVG 與 repo 一致（差異僅寫回時附加的 C2PA 中繼資料）
- **[F 收尾]** problems-view 7 頁重產（KaTeX 1,109 式錯誤 0、殘留錢號 0、圖檔引用全部存在）；unit-RC-U3-3（20 頁）與 lecture-RC-U3-3（31 頁）PDF 已於階段 C 重出、本階段無新變動；儀表板 tags 已於階段 C 同步
- 批次狀態：10 題皆到 F（題目正本已確認、盲解 7 一致／3 分歧已勘誤落實、圖解齊），待使用者人工複核改 verified
