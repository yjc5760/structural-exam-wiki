# CHANGELOG（根目錄／跨科）

> 影響多科或根目錄的變更記在本檔（只可 append）。
> 2026-11-09 起由 `CLAUDE.md` 末尾移出：CLAUDE.md 每個工作階段都會自動載入，歷史紀錄不必常駐；另可避免盲解比對時被舊勘誤結論污染（見 `exam-wiki-audit`）。

> 各科自己的變更紀錄在 `XX/SUBJECT.md` §9（SS 在獨立 repo 時期的完整紀錄已移至 `SS/SUBJECT.md`）。

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | **五科合併為單一知識庫**：根目錄 CLAUDE／CODE／SOLVE／SPEC／README 改寫為五科通用（`XX` 代號）；SS 專屬內容（CHANGELOG、設計哲學框架、互動圖內容碼）移入 `SS/SUBJECT.md`；依 SS 架構以 `scripts/scaffold_subject.py` 建立 RC／SA／SD／SM 骨架；`syllabus_taxonomy.json` 以根目錄為正本、各科 `raw/json/` 放同步副本；儀表板改為五科共用樣板（`KB_SUBJECT` 驅動）並新增根目錄五科入口頁；`skills/` 與 `xcheck.py` 移至根目錄共用；改為單一 git repo | 五科架構相同、只有考古題不同，分開維護使同一條規則要改五次 |
| 2026-10-29 | **解題與勘誤流程改為 skill**：新增 `skills/exam-solve/`（原 CLAUDE-SOLVE.md 的 SOLVE 流程＋CLAUDE-SPEC.md §4.1 完成檢核）與 `skills/exam-errata/`（規則 1 解析勘誤四條件的執行流程＋xcheck 分診）；CLAUDE-SOLVE.md 改為索引頁，ADD-METHOD 移入 CLAUDE-CODE.md；CLAUDE-CODE.md 新增「由 skill 負責的流程」對照表 | 只在解題／勘誤時才需要的長流程不必每次常駐；規則仍留在 CLAUDE.md，格式仍以 CLAUDE-SPEC.md 為唯一依據 |
| 2026-10-29 | **停用互動圖（`*-viz.html`）**：圖解一律由 `struct-diagram` skill 產生靜態 SVG＋PNG（`figs/`＋`gen_XX-YYYY-N.py`），exam-solve 解完一題後提議、exam-errata 勘誤後重跑；規則 1 的勘誤例外由 `*-viz.html` 改為 `gen_*.py`／`figs/`；SS 既有 19 份 viz 保留為舊檔 | 互動圖與 struct-diagram 功能重疊；靜態圖可重跑、可審核、可進 PDF 與影片管線 |
| 2026-10-29 | **附圖改由 Cowork 從考卷擷取**：新增 `scripts/extract_figure.py`（preview 座標格線找範圍、crop 產生 500 dpi 證據圖＋向量抽取）；exam-solve 階段一改為「擷取 → 判讀清單（使用者確認）→ struct-diagram 重繪」，觸發語改為「判讀確認，請開始解題」 | 免手動截圖；把判讀攤開確認可在解題前攔下判讀錯誤（SS-2013-4 試作：12 項盲讀全數與勘誤後解析一致，另抓到一處公式來源誤記） |
| 2026-11-08 | **SS 由獨立 repo `exam-wiki-SS` 重新搬入**（只搬檔案、不含 git 歷史；舊網站維持上線）；SS 較新的 skills（exam-start-page、unit-textbook、unit-* SKILL.md）、`xcheck.py`、勘誤回報表單併入根目錄；移除已停用的 formula-recall-deck、vha-treasure-map | 10-29 合併後 SS 仍在原 repo 持續更新，兩邊分岔 |
| 2026-11-08 | **根目錄規則整併（以 SS 11-01 以後的規則為準，升為五科通用）**：① wiki 封存（只留 `wiki/queries/`，其餘移 `archive/wiki/`），停用 ingest／compile-all／lint／add-concept（CLAUDE-CODE.md 16 → 12 個指令）；② 記錄檔改為 `wiki/queries/log.md`；③ 規則 1 加第五處例外「題目正本 `-problem.md`」；④ methods 修改條件 ② 與解析勘誤條件 ③ 改為同步 study／problems-view／單元資料；⑤ 規則 5、7 改寫（verified 人工複核、study 頁由正本產生），新增規則 11「共用的東西只放一份」；⑥ 單元總覽、起點頁列為標準教材；⑦ 共用腳本（render_problem_view、build_unit_page、build_frequency、build_start、parse_links、audit_classification）移至根目錄 `scripts/`，`build_unit_page.py` 一併修正 SM／MM 科目名稱對調；⑧ 新增「科目搬入」步驟；scaffold 骨架、skills 同步改寫 | 共用規則與腳本只維護一份；RC／SA／SD／SM 搬入時直接套用 |
| 2026-11-08 | **主副分類只能填本科子項（五科一律）**：原本副分類可掛他科子項，改採 SS 2026-10-30 起的規則；`subject_profiles.json` 各科 `relatedTopics` 清空、scaffold 範本與各科 `SUBJECT.md` §2 同步；「科目搬入」加一步分類稽核 | 頻率熱圖、單元總覽、分類稽核只認本科子項，他科代號會被排除或報錯 |
| 2026-11-08 | **skill 正本與安裝**：帳號裡 8 個 exam-wiki 用 skill（add-to-wiki、exam-wiki-pipeline、exam-problem-split、exam-wiki-audit、exam-practice-sheet、subject-frequency-map、blackboard-solution-video、video-handout）備份進 `skills/`（exam-practice-sheet 改指 structural-exam-wiki、subject-frequency-map 改用根目錄 build_frequency）；新增規則 12「skill 以 repo `skills/` 為正本」 | 帳號安裝版與 repo 版各自演進已分岔，需要單一正本 |
| 2026-11-08 | 新增 `skills/exam-subject-migrate/`：把 SS 搬入的實際流程寫成 skill（盤點→去處對照→複製→規則寫進 SUBJECT.md→分類稽核→重產驗證→收尾），供 RC／SA／SD／SM 搬入時使用 | 讓其他科照同一流程搬入，不必每次重想 |
| 2026-11-09 | **根目錄說明檔精簡**：① 刪除 `CLAUDE-SOLVE.md`（10-29 起只剩轉址表），對照列併入 `CLAUDE-CODE.md`「由 skill 負責的流程」；各科 `SUBJECT.md`、`SS/檔案架構索引表.md`、`scripts/scaffold_subject.py`、`README.md` 的引用同步改指 `skills/exam-solve`；② CHANGELOG 由 `CLAUDE.md` 末尾移為根目錄 `CHANGELOG.md`，規則 3 與資料夾結構同步；寫 CHANGELOG 的 skill（exam-errata、exam-start-page、exam-subject-migrate、exam-wiki-audit、exam-wiki-pipeline、subject-frequency-map、unit-exam-intel）與 `skills/README.md` 改指 `XX/SUBJECT.md` §9／`CHANGELOG.md`，並重新打包；③ `CLAUDE-CODE.md` 刪除 STUDY 子項層級舊規格（七區塊），FREQUENCY 改指 `subject-frequency-map` | CLAUDE.md 常駐內容只留規則；解題流程早已改為 skill，轉址檔與重複段落徒增維護點 |
| 2026-11-09 | **SA 由獨立 repo `exam-wiki-SA` 搬入**（只搬檔案、不含 git 歷史；舊網站維持上線），細節見 `SA/SUBJECT.md` §9；共用腳本跟著修：① `render_problem_view.py` 併入 SA `md2view.py` 的「清單前補空行」（Python-Markdown 不認緊貼文字的清單）與 `**分析法：**` 頁首同步；② `unit_page_template.html` 併入 SA 的頁尾 `mathIn` 修正；③ `unit_page_template.html`／`build_frequency.py` 的「← 從這裡開始（SS 學習路徑）」改用科目代碼，該科沒有 `start.html` 時自動拿掉；④ 根目錄 `index.html` 五科入口改讀 `window[code+'_QUESTIONS']`（SA 暫用原 repo 儀表板 `SA_*`） | ① 會改變 SS 下次重產的結果：SS 98 頁中 81 頁有「文字後緊接清單」，目前渲染成「1. …<br />」純文字，重產後變成真正的清單（本次未重產 SS）；②③ 對 SS 已驗證：單元總覽只多一行 `mathIn(footer)`、頻率熱圖返回列保留 |
| 2026-11-11 | **停用 `unit-exam-intel`、`unit-formula-map`**：兩者已由 `unit-overview`（單元總覽）整合；SS、SA 已無舊 `study-`／`formula-given-` 頁，RC／SD／SM 尚無任何單元頁，故不做轉址頁。移除所有「尚未導入的科目改用舊 skill」的退路說法與轉址說明：`CLAUDE-SPEC.md` 教材表刪 `study-`／`formula-given-` 列；`CLAUDE-CODE.md`、`skills/README.md`（刪兩節）、`skills/unit-overview`、`skills/unit-lecture`（教材互連改為講義↔單元總覽兩顆按鈕，與現行講義一致）、`skills/subject-frequency-map`（分工表、Step 4 偵測表、附錄與 `scripts/` 副本同步為根目錄 v1.2）、五科 `SUBJECT.md` 設計法說明、`scripts/scaffold_subject.py`、`scripts/sync_taxonomy.py` 註解、SS／SA `README.md`、各科 `檔案架構索引表.md`、`SS/知識庫使用說明書.md`；重新打包 `unit-overview`、`unit-lecture`、`subject-frequency-map` 三個 `.skill` | 單元總覽已能產生完整內容，舊 skill 留著會讓新科目走回舊路 |
| 2026-11-11 | **移除 RC／SD／SM 科目資料夾裡的 `scripts/build_frequency.py`**（三份相同的舊版 v1.1，教材欄還在找已停用的 `formula-given-`）；三科 `scripts/` 只有這一檔，整個資料夾移除；三科 `檔案架構索引表.md` 刪掉對應那一行。之後一律用根目錄 `scripts/build_frequency.py`（v1.2，函式為舊版超集） | 規則 11：共用腳本只放根目錄一份 |
| 2026-11-11 | **RC 由獨立 repo `exam-wiki-RC` 搬入**（只搬檔案、不含 git 歷史；舊網站維持上線），細節見 `RC/SUBJECT.md` §9；共用部分跟著修：① `render_problem_view.py` 的 `pre()` 加「引言（> …）後緊接清單補空行」（RC-2009-1；對 SS／SA 全部正本渲染 0 差異）；② `unit_page_template.html` 圖例拿掉已停用的「📊 解析含互動圖」（併入 RC 版，SS／SA 下次重產才會反映）；③ `subject_profiles.json` RC `examFile` 與 `CLAUDE.md` 科目表的 RC 考卷檔名更正為實際的 `RC-YYYY_鋼筋混凝土設計與預力.pdf`；④ 根目錄 `index.html` 註解補 RC（暫用原 repo 儀表板 `RC_*`）；`CLAUDE.md` 專案說明補 RC 搬入日期 | ① 原本會把清單吃進引言；③ 24 份既有考卷都是簡稱檔名，`raw/exams/` 為證據不改名，改設定配合實檔 |
| 2026-11-11 | **`skills/exam-problem-split` 開工說明改為合併後路徑**：§0 改指 `structural-exam-wiki/XX/raw/exams/`、題目瀏覽頁一律用根目錄 `render_problem_view.py`（刪除 `md2view.py`／`gen_problems_view.py` 的分科說明）、規則 1 已在根目錄不用再改、`tagSystem` 補 `problemStatus` 只剩 RC／SD／SM；尚未搬入的科目先停下請使用者搬入；開頭補路徑慣例、exam-solve 改指 `skills/exam-solve/`；§2 證據圖擷取改指根目錄 `extract_figure.py`；重新打包 `.skill` | 原寫法是五科合併前的分科 repo 說法，照做會到舊 repo 找考卷、用已停用的渲染腳本 |
| 2026-11-11 | **SM 由獨立 repo `exam-wiki-SM` 搬入**（只搬檔案、不含 git 歷史；舊網站維持上線），細節見 `SM/SUBJECT.md` §9；共用部分跟著修：① `scripts/subject_profiles.json` SM 的 `methodAxis` 由 scaffold 誤設的「題型：分析計算／設計檢核／概念題／混合」更正為原 repo 實際使用的「分析法：總應力法／有效應力法／概念題／混合」（含判準），`codes` 依封存的 code-ref 補齊；② `audit_classification.py` 解析標頭別名補「分析法」（SM、SA 的標頭都寫 `**分析法：**`，原本整欄沒被比對）——SS、RC 稽核結果不變，SM 0 筆，**SA 新冒出 4 筆**（SA-2010-1～4 索引 `designMethod` 為「待分類」、標頭已寫分析法），未改 SA；③ 根目錄 `index.html` 註解補 SM（暫用原 repo 儀表板 `SM_*`）；`CLAUDE.md` 專案說明補 SM 搬入日期。另更正本表同日「RC／SD／SM 尚無任何單元頁」一句：SM 原 repo 有舊式 `study-SM-*`（8 頁）與 `formula-given-SM-*`（7 頁），尚未改成單元總覽（見 `SM/SUBJECT.md` §10） | ① 不改則 SM 儀表板與單元總覽的篩選選項與 96 題索引值對不上；② 稽核腳本才真的檢查得到 SM／SA 的分析法標頭 |
| 2026-11-11 | **SD 由獨立 repo `exam-wiki-SD` 搬入**（只搬檔案、不含 git 歷史；舊網站維持上線），細節見 `SD/SUBJECT.md` §9；根目錄只改 `index.html` 註解（補 SD，暫用原 repo 儀表板 `SD_*`）與 `CLAUDE.md` 專案說明搬入日期，**共用腳本未改**（`render_problem_view.py`、`build_frequency.py` 原 repo 版都是根目錄的舊版）。搬入時發現、列待使用者決定：① **`scripts/xcheck.py` 在合併後的架構下五科都掃不到 `XX/archive/wiki/`**（註解說舊目錄不存在時改掃封存處，但判斷以執行目錄為準）；原 SD 版以科目資料夾為準，實測 SD A=3、SM A=2、SA A=7、RC A=23、SS A=0——要不要掃已凍結的封存區屬五科通用決定；② SD 索引用 `analysisMethod` 欄位、75 種自由文字，與根目錄 `designMethod` 固定值不合；③ SD `raw/solutions/methods/` 8 份全是 RC 方法論殘留（5 份與 RC 相同、3 份為 RC 舊版），SD 無任何引用 | ① 影響五科稽核結果，不宜由單科搬家順手改；②③ 屬 SD 索引與 raw 內容，須使用者確認 |
| 2026-11-11 | **`scripts/audit_classification.py`：索引同時有 `designMethod` 與 `analysisMethod` 時，解析標頭對照 `analysisMethod`**（SD 分類軸定案時連帶修改，細節見 `SD/SUBJECT.md` §3、§9） | SD 把 99 題歸成四值寫進 `designMethod`、保留原長描述 `analysisMethod`，解析標頭「分析方法」寫的是長描述；不改會有 53 筆誤報。目前只有 SD 兩欄並存，SS／RC／SA／SM 稽核輸出改前改後逐字相同 |

## 2026-11-14 規範版本政策改為「一律用現行最新台灣規範」

- **[RULE]** 根目錄 `CLAUDE.md` 新增「規範版本」一節與重要規則 13：考古題一律依現行最新版台灣規範解題，不依考試年份；題目指定舊版台灣規範時仍用現行版、§5 註明差異；唯一例外為題目明確指定 ACI（RC）或 AISC（SS）。題目明確給定的數值、載重組合、係數、公式仍照題目用。既有解析不整批重解，遇到時依新規則改寫。
- **[SUBJECT]** 五科 `SUBJECT.md` §7 改寫：刪除「以考卷年份適用版本為準」，列出現行版本（RC 建築物混凝土結構設計規範 2023 年版；SD 建築物耐震設計規範及解說 111.10.1 生效；SM 建築物基礎構造設計規範 113.1.1 生效；SS 鋼構造建築物鋼結構設計技術規範 96 年版／99 年部分修正）；RC §8、SD §8 內「依考卷年份」字樣同步。`scripts/subject_profiles.json` codes 同步並加 `_meta.codePolicy`（規則 10）。
- **[SKILL]** `skills/exam-solve`、`exam-errata`、`exam-wiki-audit` 的 SKILL.md 改為現行台灣規範並重新打包 `.skill`；帳號端需重新安裝這三個 skill。
- 使用者指示（2026-11-14 對話）；版本資訊依內政部國土管理署公告、行政院公報查證。備份：裝置工作階段 `~/bk3/`。
- **[RULE] 2026-11-14 補充**：題目印出的舊規範公式、係數、φ、載重組合與載重因數、容許值、規範表格也改用現行台灣規範（考卷印在題目或提示裡也一樣）；照題目用的只限題意資料（幾何、材料強度、載重大小與位置、鋼筋規格與面積、斷面性質表、題目直接給的數值參數如 Lp、Lr、Cb、有效預力）。題目正本仍照錄考卷原式。CLAUDE.md、五科 SUBJECT.md §8 引言、exam-solve／exam-errata／exam-wiki-audit 同步並重新打包。
- **[RULE] 2026-11-14 補充**：重要規則 12 加註——更新 skill 時除寫回 repo `skills/` 並重新打包，還要把更新過的 `.skill` 檔直接傳到對話裡，讓使用者點檔案卡片按「Save skill」安裝。
- **[RULE] 2026-11-14 補充（容許值例外）**：考卷給的容許值若在現行規範允許範圍內（比現行規範嚴，或落在某一類別內，如 RC 預力構材 U／T／C 類）視為題目設計條件照用，§5 註明屬哪一類與須補的檢核；超出現行規範上限才改用現行上限。`CLAUDE.md`「規範版本」、`skills/exam-solve`、`exam-errata`、`exam-wiki-audit` 同步並重新打包 `.skill`。起因：RC-U4-1 批 1 盲解比對（RC-2007-4 的 $3\sqrt{f'_c}$ 屬現行 T 類、RC-2021-4 的 $1.6\sqrt{f'_c}$ 比 U 類嚴），使用者 2026-11-14 對話選定此通則。

## 2026-11-14 — SS、RC 儀表板相容 `KB_*` 變數

- **[FIX]** `SS/index.html`、`RC/index.html` 在載入 `dashboard-data.js` 後加相容段：有 `window.KB_*` 時轉成本科 `SS_*`／`RC_*` 變數。原因：兩頁是搬入前的舊版頁面，只讀科目前綴變數，而 `scripts/refresh_dashboard.py` 寫 `KB_*`；RC 今天重建 `dashboard-data.js` 後儀表板已顯示「找不到 dashboard-data.js」。未改用 `scripts/templates/dashboard-index.html`：兩頁有樣板沒有的功能（起點頁入口、結果列／清除篩選、手機版版面、題解新分頁開啟），改樣板會失去。
- `SS/dashboard-data.js` 改由 `refresh_dashboard.py SS` 重建（內容與索引一致，98 題）；SS 設計法篩選補「塑性分析」。
- 驗證：node 載入 `dashboard-data.js`＋相容段，SS 98 題／7 子項、RC 100 題／14 子項，未知子項 0、tags 空 0、設計法皆在篩選選項內。SA／SD／SM 的 `dashboard-data.js` 仍是科目前綴變數，與各自頁面相符，未動；之後對這三科跑 `refresh_dashboard.py` 前要先加同一段相容碼。

## 2026-11-14 — `render_problem_view.py` 頁首分析法欄位不再覆蓋年份

- **[FIX]** `scripts/render_problem_view.py`：同步 `**分析法：**` 到頁首 `meta2` 時，若該頁頁首尚無分析法欄位（最後一段是「YYYY 年（民國 …）」），改為附加一段，不再把年份覆蓋掉。只影響有 `meta2` 的頁面（目前為 SA）。發現於 SA 一致性整理（SA-2008-3、2008-4、2019-4 三頁已還原重產），詳見 `SA/wiki/queries/log.md` FIX-SA-CONSISTENCY。

## 2026-11-15 audit_classification.py：補「混合」設計法雙向比對

- `scripts/audit_classification.py` 與 `skills/exam-wiki-audit/SKILL.md` 附錄腳本：標頭設計法主值（括號前）含「混合」⇔ 索引為「混合」，不一致即報（原子字串比對放過「WSD / USD 混合」對索引 WSD，RC-2018-4 漏報）；重新打包 `skills/exam-wiki-audit.skill`
- 驗證：五科重跑，SS／RC／SA／SM 0 筆、SD 34 筆皆與修改前相同（無新增誤報）；合成測試（RC-2018-4 索引改 WSD、RC-2004-5 改 USD）兩題皆被報出
- 已知：skill 附錄腳本與 `scripts/` 版本原本就分岔（附錄缺 SD analysisMethod 對照，SD 報 87 筆；scripts 版另有已封存 wiki 的 C/D/E 檢查），本次未合併

## 2026-11-15 起點頁腳本：影片講義支援分集
- `scripts/parse_links.py`：清單「影片講義」段同一單元多行 → `video_handout` 存成 `[[標題, 網址], …]`（標題取檔名去掉單元代號）；只有一份時仍存字串
- `scripts/build_start.py`：`video_handout` 為清單時輸出「影片講義（圖文，N 集）：各集連結」，並逐一檢查相對連結
- 原因：SA 的影片講義每單元分 2–7 集，舊格式只容一份
- 驗證：SS 用新腳本 dry-run 無任何 `~` 變更，重產 `start.html` 與現有檔逐位元組相同
- 同步 `skills/exam-start-page/`（scripts、references/format.md）並重新打包 `skills/exam-start-page.skill`
- 同日追加：觀念講義影片（`lecture_anim`／`lecture_video`）也支援分集，存法與顯示同影片講義；SS 重產仍逐位元組相同

## 2026-11-17 移除版控中各科影片講義並更新 .gitignore（符合 GitHub 倉庫容量限制）
- 依使用者指示，將各科 `*/影片講義/`（共 1,123 份檔案，含 MP4 影片與截圖）自版控移除，改為本地存放不納入 Git。
- `.gitignore` 新增 `**/影片講義/`。
- 同步更新 RC、SA、SD、SM、SS 之 README.md，移除影片講義目錄說明。

## 2026-11-17 blackboard-solution-video：預設改為 Azure TTS 並新增斷點續跑
- `skills/blackboard-solution-video/`：
  - 配音預設改為 Azure TTS `zh-TW-HsiaoChenNeural`（台灣華語女聲），Gemini TTS 轉為備用（避開每日 quota 限制）
  - `tts_azure.py` 加入指數退避重試（最多 5 次）、日誌記錄 `tts_azure.log`，以及 `--resume` 斷點續跑功能
  - 新增 `run_tts_resume.bat` 供使用者一鍵續跑
  - 更新 `SKILL.md`、`references/lessons.md`、`scripts/kit/env.example`
  - 重新打包 `skills/blackboard-solution-video.skill`

## 2026-11-20 起點頁腳本：清單可省略影片段標題
- `scripts/parse_links.py`：
  - 「單元總覽／觀念講義／教科書」段後面直接接 YouTube 行（中間只有分隔線、沒有段標題）時，依序歸為公式記憶影片／觀念講義影片／教科書講解影片
  - 網站根目錄網址（有無結尾斜線）一律轉成 `index.html`
- 原因：SS 新清單把影片段標題換成分隔線，舊版會把影片誤塞進 overview／lecture／textbook；有段標題的舊格式解析結果不變

## 2026-11-21 新增 skill：youtube-upload
- `skills/youtube-upload/`（SKILL.md、scripts/yt_chapters.py）＋ `skills/youtube-upload.skill`；`skills/README.md` 列入「圖與影片」
- 分工：使用者選影片、縮圖、字幕三個檔；Claude 在內建瀏覽器填標題、說明（章節時間碼由 yt_chapters.py 從 timeline.json＋講稿.md 算出）、兒童設定、字幕語言、權限、等檢查、發布並驗證
- 原因：RC-U1-1 上傳時確認原生檔案視窗只能由使用者操作；心算章節時間出錯（F 章 12:32 → 實為 12:12），改由腳本產生

## 2026-11-21～22 RC 講義正確性檢查與「φ 過渡式＋梁須拉力控制」全庫勘誤
- 依據 112 年版《建築物混凝土結構設計規範》表 21.2.2 及 §9.3.3.1，全面修正 φ 過渡式為規範原式（SD420 取 εty = 0.002、分母 0.003，界限 0.005）及非預力梁須拉力控制要求。
- 15 題解析勘誤（答案改變 5 題：RC-2019-1、2024-1、2015-3、2011-3、2011-2），RC-2015-2／2016-1／2019-1 退回 unverified。
- 下游同步：15 題問題視圖、question_index.json、dashboard-data.js、單元總覽（RC-U1-1、U1-2）、講義（lecture-RC-U1-1、U1-2、U3-3、U4-1）修正與 6 份 PDF 重印。

## 2026-11-22 SA 觀念講義 6 份正確性檢查與更正
- 完成 SA-U1-2、U1-3、U2-1、U2-3、U2-4、U3-2 手算範例重算與題解 boxed 答案核對。
- 修正：U2-4 §16 精選③ 最大正彎矩問句、U2-3 轉角個數、U1-2 Pratt 桁架節間數、U3-2 弦剪力反號理由。
- 移除失效之 Keynote 連結、更新過時題數與分類敘述；6 份 PDF 重編。

## 2026-11-22 SS 觀念講義 5 份正確性檢查與修正
- 依檢查報告修正 lecture-SS-U1-1、U1-2、U1-3、U1-4、U2-3：Cv 彈性段係數、ASD Fb 式、包覆型 SRC 強度與勁度係數、塊狀剪力依我國極限設計法規範以大小擇一式為主線、U 值表改我國值 0.90/0.85/0.75。
- 修正 M22 標準孔徑為 24 mm、重繪圖解；相關 Python 繪圖腳本同步更新並重編 5 份 PDF。

## 2026-11-26 五科儀表板站內閱讀器提示修正
- `SS/`、`SA/`、`RC/`、`SM/`、`SD/` 的 `index.html`：首次授權提示「選擇 exam-wiki-XX 資料夾」與選錯資料夾的 alert「請選擇 exam-wiki-XX 資料夾本身」，改為「選擇 XX 科目資料夾」（比照共用樣板 `scripts/templates/dashboard-index.html`）。
- 原因：搬入五科合一 repo 後已無 exam-wiki-XX 資料夾，舊提示會讓使用者選錯；閱讀器實際檢查的是所選資料夾下的 `raw/solutions/`，即科目資料夾。
- 頁面標題、副標、頁尾、匯出 PDF 頁首的 exam-wiki-XX 字樣為名稱標籤，未動。SD 另記於 `SD/SUBJECT.md` §9。

## 2026-11-28 知識庫升級：全站知識索引、信任標章、驗算腳本留存、概念字典與跨科脈絡
- 新增 `scripts/build_kb_index.py`：從五科正本（解析 §2／§3／§3.5、題目正本、question_index、audit-ledger）編譯 `kb/` 六檔——`search.html`（五科全站搜尋，同義詞展開）、`traps.html`（陷阱字典 1,678 條／451 題）、`l3.html`（L3 深層知識 1,695 條／452 題＋L3 熱點）、`concepts.html`（概念字典、跨科脈絡、規範條文反查）、`trust.html`（可信度總覽與人工複核待辦）、`kb-data.js`。根目錄 `index.html` 加入口。
- 489 頁題目瀏覽頁頁首加信任標章（`<!--trust-->…<!--/trust-->`，每頁只動這一行）；狀態由 audit-ledger 與 `verificationStatus` 推得，不另存欄位。首次結果：人工已核 6、盲解一致 293、勘誤已落實 158、分歧已裁定 5、盲解後有修改 26、勘誤後待複驗 1。`render_problem_view.py` 借他題當版型時會拿掉該題標章。
- 新增根目錄 `concept_vocabulary.json`（167 個概念、同義標籤＋上位概念＋搜尋別名，confirmed 全 false 待審）與 `cross_subject_links.json`（5 條單元層跨科脈絡，待審）；兩者只供索引，不改各科 tags 與分類。
- 規則：`CLAUDE.md` 新增規則 14，規則 1 勘誤可動檔案加 `verify_XX-YYYY-N.py`、條件 ② 要求留存驗算腳本、條件 ③ 下游加重跑 build_kb_index；`CLAUDE-SPEC.md` 新增 `codeClauses` 欄位與規範代碼表、`verify_*.py` 格式、tags 沿用字典寫法；`CLAUDE-CODE.md` FIND／UNVERIFIED 補網頁版。
- skills：`exam-errata`（驗算腳本存檔、codeClauses、重跑索引）、`exam-solve`（同）、`exam-wiki-audit`（ledger 更新後重跑索引）改寫並重新打包 `.skill`。
- 正本缺漏（索引照實呈現、未補）：38 題正本沒有陷阱段落、36 題沒有 L3 段落（SA、SD 為主；另 RC-2006-1 的 L3 寫成變數層而非深層知識，未抽取），`--check` 會逐題列出。
- 原因：題庫的知識鎖在單題文章裡無法橫向查；盲解結果只在 ledger 看不到；勘誤驗算程式用完即丟；舊 wiki 已證明手抄副本會脫鉤，所以一律改為由正本編譯的衍生視圖。

## 2026-11-28 新增考卷自動下載：scripts/fetch_exams.py
- 從考選部「考畢試題查詢平臺」（wwwq.moex.gov.tw）下載結構工程技師試題：GET `wFrmExamQandASearch.aspx?y=<年>` 找標籤含「結構工程技師」的類科，以現行六科名稱對得最多者選出高考那場（2002、2003 同年還有檢覈考試，科目名稱不同），再依科目名稱取 `wHandExamQandA_File.ashx?t=Q&code=…&c=…&s=…&q=1`。官網每年的考試／類科／科目代碼都不同，不寫死。
- 存成 `XX/raw/exams/XX-YYYY_<examFile>.pdf`（檔名取自 `scripts/subject_profiles.json`）；既有考卷一律不覆蓋，`--verify` 只比對、不同時官網版另存 `*.moex-YYYYMMDD.pdf`；每份下載在該科 `wiki/queries/log.md` 記來源代碼與 MD5。
- 實頁驗證：2002（091310，略過 091091／091261 檢覈）、2010（099220）、2019（108180）、2024（113190）、2025（114180）、2026（115180）。既有 `SS-2019_鋼結構設計.pdf` 與官網檔同為 158,171 bytes，確認本庫考卷即來自此平台。
- **115 年（2026）結構工程技師試題官網已公布**（考試代碼 115180），本庫尚未收錄。
- Cowork／Claude 沙盒連不到 moex.gov.tw（網路白名單），腳本由使用者在自己電腦執行；`CLAUDE.md`（資料流、資料夾結構、規則 1 註記）、`CLAUDE-CODE.md`（維護段落）、`skills/exam-solve`（開始前第 3 步）同步，重新打包 `exam-solve.skill`。
- 同日：下載流程包成 skill `skills/exam-fetch/`（＋`exam-fetch.skill`）：確認範圍 → 給使用者完整指令 → 驗收檔案、頁數與 log 來源 → 交給 exam-solve；`skills/README.md`、`CLAUDE-CODE.md` 列入。
- 同日：`exam-fetch` 加「computer use 代跑」：device_bash 在 `.work/` 寫批次檔，computer use（檔案總管 click 等級，只雙擊不打字）執行，讀 `.work/fetch.log` 驗收；手動執行改為備案。驗收加「第一頁抬頭目視」。實測下載 115 年五科考卷成功。

## 2026-11-28 五科講義精選題練習卷＋exam-practice-sheet 題首定位修正
- 依 35 份 `XX/study/lecture-XX-Un-m.html` 末節「時間有限就練這 5 題」的 ①–⑤，產生 173 份單題練習卷（35×5，SS-2023-3、SM-2025-3 兩單元共用）：`XX/study/practice/<題號>-practice.html/.pdf`，各科 `study/practice/精選題索引.md` 列出單元→題號→配分→建議時間。
- `skills/exam-practice-sheet`：題首／共用公式區的 y 座標改取該行第一個非空白 span 頂端（原取行 bbox）。行內有高公式（如 SD-2023 第四題 k=16π²）時行 bbox 會往上撐到上一行，造成本題切入上一題最後一行、上一題末行被切掉。重新打包 `exam-practice-sheet.skill`。
- 使用者電腦的 Cowork VM 無 Chromium（playwright 下載被白名單擋），HTML 在本機產生、PDF 於雲端 Chromium 轉印後寫回。
- 同日：35 份 `XX/study/lecture-XX-Un-m.html` 的「精選 5 題」節，①–⑤ 每題題號旁加「🖨️ 練習卷」按鈕（`a.pdfbtn`，連到 `practice/<題號>-practice.pdf`，新分頁開啟可直接列印；列印講義時按鈕隱藏）；`<head>` 加一段 `#pdfbtn-css` 樣式。只動這兩處，重跑會先移除舊按鈕再加。
