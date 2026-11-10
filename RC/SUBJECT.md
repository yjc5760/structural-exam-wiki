# RC 科目設定（SUBJECT.md）— 鋼筋混凝土設計與預力混凝土設計

> 本檔是 **RC 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md` 與根目錄 `skills/` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`RC`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `RC`（RC & Prestressed Concrete Design） |
| 科目全名 | 鋼筋混凝土設計與預力混凝土設計 |
| 題號格式 | `RC-YYYY-N`（YYYY 為西元年，例 `RC-2015-1`） |
| 考卷檔名 | `raw/exams/RC-YYYY_鋼筋混凝土設計與預力.pdf`（檔名用簡稱，與科目全名不同；24 份既有考卷皆為此名，`subject_profiles.json` 的 `examFile` 同此） |
| 收錄範圍 | 2002–2025（民國 91–114 年），100 題；題目正本尚未建立；`verificationStatus` verified 7 題、unverified 93 題（2026-11-11 搬入時） |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立骨架（2026-10-29）；內容由獨立 repo `exam-wiki-RC` 搬入（2026-11-11） |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 |
|---------|------|------|
| `RC-U1-1` | RC 梁彎矩強度分析與設計 | 第一單元 |
| `RC-U1-2` | RC 柱強度分析與設計 | 第一單元 |
| `RC-U1-3` | 細長柱 | 第一單元 |
| `RC-U1-4` | 柱設計圖之應用 | 第一單元 |
| `RC-U2-1` | RC 剪力強度分析與設計 | 第二單元 |
| `RC-U2-2` | RC 扭力強度設計 | 第二單元 |
| `RC-U2-3` | 鋼筋錨定長度與斷點計算 | 第二單元 |
| `RC-U3-1` | 梁工作性要求（含撓度、裂縫） | 第三單元 |
| `RC-U3-2` | 樓版與基腳設計 | 第三單元 |
| `RC-U3-3` | 韌性要求與耐震設計 | 第三單元 |
| `RC-U4-1` | 預力梁斷面應力分析 | 第四單元 |
| `RC-U4-2` | 預力量與偏心量設計 | 第四單元 |
| `RC-U4-3` | 預力損失 | 第四單元 |
| `RC-U4-4` | 預力梁剪力分析與設計 | 第四單元 |

**分類原則（五科一律）：** `primaryTopicId`、`secondaryTopicIds` **只能填本科子項**，不引用他科的單元。題目涉及他科觀念時，歸到本科最接近的子項（例：見根目錄 CLAUDE.md「命題大綱分類」）。
（RC 搬入時以 `audit_classification.py RC RC` 稽核：100 題主副分類全部是 RC 子項，無須改歸。）

---

## 3. `designMethod` 欄位（本科分類軸：設計法）

| 允許值 |
|--------|
| `USD` |
| `WSD` |
| `概念題` |
| `混合` |

> USD＝強度設計法（含預力梁極限強度）；WSD＝工作應力法（含預力梁傳遞／使用階段之容許應力檢核）；概念題＝說明／比較題
>
> 單元總覽（`unit-overview`）的設計法標註與儀表板篩選選項，在本科一律用上表的分類軸與順序。
> 解析標頭寫法：`**設計法：** USD強度設計法 / WSD工作應力法 / 概念題 / 混合`（索引存英文代碼或中文值，見上表）。
> 搬入時索引分布：USD 71、WSD 17、概念題 8、混合 4。

### 3.1 標準標籤詞彙（`tags`，原 repo `CLAUDE-SPEC.md` §8）

`tags` 為自由標籤（核心考點，3–8 個），優先用下表的標準寫法（例：寫 `T形梁` 不寫 `T梁`）：

| 類別 | 標準標籤 |
|------|---------|
| **梁彎曲** | 單筋矩形梁、雙筋梁、T形梁、有效翼板寬、Whitney應力塊、延性破壞、平衡鋼筋比、最大鋼筋比、最小鋼筋比 |
| **梁剪力** | 臨界斷面、Vc混凝土剪力強度、Vs腹筋剪力強度、最大間距限制、最小腹筋量 |
| **撓度裂縫** | 有效慣性矩、開裂彎矩Mcr、長期撓度修正、允許撓度、裂縫寬度控制 |
| **柱** | 短柱、長柱效應、P-M互制圖、放大彎矩法、無側移構架、有側移構架、螺旋柱、箍筋柱 |
| **板** | 單向版、雙向版、直接設計法、等效框架法、柱帶、中間帶、衝剪 |
| **基礎** | 獨立基腳、聯合基腳、彎矩設計、衝剪驗算、單向剪力 |
| **預力** | 先拉法、後拉法、彈性縮短損失、摩擦損失、錨定滑動損失、潛變損失、收縮損失、鬆弛損失、有效預力、使用性驗算 |
| **耐震** | 韌性構架、特殊矩形梁、特殊矩形柱、強柱弱梁、圍束箍筋、密箍區、接頭設計 |
| **材料** | 混凝土抗壓強度、鋼筋降伏強度、彈性模數、潛變係數、收縮應變、β1係數 |

---

## 4. 圖解（struct-diagram）

解題或勘誤後需要圖解時，用 `struct-diagram` skill 以程式產生向量圖（SVG＋2× PNG），
腳本 `gen_RC-YYYY-N.py` 與 `figs/` 放在該題資料夾，`.md` 引用 SVG 相對路徑。
（互動圖 `*-viz.html` 功能已於 2026-10-29 停用；RC 原 repo 的 18 份 viz 已於 2026-11-01 刪除。）

本科常見圖解：

- RC 斷面／應變／應力三聯圖
- P-M 交互曲線
- 梁三聯圖（載重／SFD／BMD）
- 預力斷面應力分佈與 Magnel 圖
- 鋼腱線形與偏心量

---

## 5.（保留編號）wiki 已封存

RC 自 2026-11-01、五科自 2026-11-08 起只保留 `wiki/queries/`（見根目錄 `CLAUDE.md`「wiki 封存」）。
舊七層（含本科 Layer 5–7：失敗模式／材料行為／規範條文對應）在 `archive/wiki/`，唯讀參考、未經全面核對（說明見 `archive/README.md`）。
（`scripts/subject_profiles.json` 的 RC `layers`、`diagnosis` 欄位為封存前的設定，保留不動。）

---

## 6. 題型辨識

| 題型 | 辨識關鍵字 | 封存的診斷頁（唯讀參考） |
|------|-----------|--------|
| 梁撓曲 | 單筋／雙筋、T 形梁、εt、φ 過渡區 | `archive/wiki/diagnosis/beam-flexure.md` |
| 柱與細長柱 | P-M 互制、平衡點、彎矩放大 δns／δs | `archive/wiki/diagnosis/column-pm.md`、`slender-column.md` |
| 剪力與扭力 | Vc、Vs、箍筋間距、Tth、閉合箍筋 | `archive/wiki/diagnosis/shear-torsion.md` |
| 錨定與斷筋 | ld、彎鉤、搭接、斷點 | `archive/wiki/diagnosis/development-length.md` |
| 使用性 | Ie、長期撓度 λΔ、裂縫控制鋼筋間距 | `archive/wiki/diagnosis/deflection-crack.md` |
| 樓版與基腳 | 雙向版、穿孔剪力、單向剪力、基腳尺寸 | `archive/wiki/diagnosis/slab-footing.md` |
| 耐震韌性 | 特殊抗彎矩構架、強柱弱梁、圍束箍筋、接頭剪力 | `archive/wiki/diagnosis/seismic.md` |
| 預力梁 | 傳遞／使用階段應力、Magnel 圖、預力損失、fps | `archive/wiki/diagnosis/prestress.md` |

---

## 7. 主要規範／依據

- 混凝土結構設計規範（內政部；以考卷年份適用版本為準，並對照 ACI 318）
- 建築物耐震設計規範及解說（韌性設計相關）
- 建築技術規則建築構造編

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。
> 本庫量法慣例（2026-08-21 統一，見 `RC-2009-1`、`RC-2004-3`）：圍束箍筋的 $h_c$ 與 $A_{ch}$ 一律量到箍筋**外緣**；舊版 ACI 318-99 的 $h_c$ 為中心至中心，兩套不可混用。

---

## 8. 設計哲學框架（解題邏輯起始版）

> 起始版只列各子項的主幹流程，隨題目解析累積後擴充；SOLVE 時與 `skills/exam-solve`
> 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。
>
> 原 repo 有一份較長的版本（T 形梁有效翼板寬、P-M 關鍵點、長柱判別式、ACI 有效慣性矩與長期撓度、六項預力損失式、耐震梁柱配筋細則），
> 見 `archive/exam-wiki-RC-root/CLAUDE-SOLVE.md`「設計哲學框架」。該版寫於 2026-05、未逐項核對，
> 部分係數屬舊版規範（如 ρmax ≈ 0.75ρb、εt ≥ 0.004、φ 值組合），引用前須依考卷年份核對。

**USD 梁撓曲強度（RC-U1-1）**
```
核心：φMn ≥ Mu，先由應變相容判斷破壞型態，再決定 φ
步驟：① 假設拉力筋降伏，由 C = T 求 a = As·fy / (0.85 f'c b)
      ② c = a / β1；εt = 0.003 (dt − c) / c
      ③ εt ≥ 0.005 拉力控制（φ = 0.90）；εt ≤ εy 壓力控制；其間為過渡區（φ 線性內插）
      ④ Mn = As·fy (d − a/2)；雙筋梁另判斷壓力筋是否降伏
      ⑤ 檢核最少鋼筋量與最小 εt 規定
T 形梁：先判斷 a ≤ hf（矩形梁行為）或 a > hf（翼板＋腹板分開算）
```

**RC 柱與細長柱（RC-U1-2、RC-U1-3）**
```
核心：P-M 互制——在 εcu = 0.003 下改變中性軸深度 c，逐點求 (Mn, Pn)
關鍵點：純壓、平衡點（εs = εy）、拉力控制點（εt = 0.005）、純彎
細長柱：k·lu / r 判斷可否忽略細長效應 → 不可忽略時以彎矩放大法
        無側移 δns = Cm / (1 − Pu / 0.75Pc) ≥ 1.0；Pc = π²(EI)eff / (k lu)²
```

**剪力與扭力（RC-U2-1、RC-U2-2）**
```
核心：φVn = φ(Vc + Vs) ≥ Vu，φ = 0.75
步驟：① Vu 取支承面 d 處  ② Vc（依考卷年份規範版本；新版含尺寸效應與 ρw）
      ③ Vs = Av·fyt·d / s，並檢核 Vs 上限與最大箍筋間距  ④ 最少剪力筋
扭力：先比 Tu 與門檻扭力 Tth，超過才需設計；閉合箍筋 + 縱向扭力筋
```

**預力梁應力檢核（RC-U4-1、RC-U4-2）**
```
核心：f = −P/A ± P·e·y/I ∓ M·y/I，頂／底纖維 × 傳遞／使用兩階段 = 4 個不等式
傳遞階段：Pi + 自重；使用階段：Pe（= R·Pi）+ 全部載重
Magnel 圖：把 4 個不等式寫成 1/P 對 e 的直線，可行區即容許的 (P, e) 組合
```

**預力損失（RC-U4-3）**
```
瞬時損失：彈性縮短、錨碇滑動、摩擦（曲率＋擺動）
長期損失：潛變、乾縮、鋼材鬆弛
```

---

## 9. CHANGELOG（RC 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
| 2026-10-29 | 停用互動圖（`*-viz.html`）；§4 改為 struct-diagram 圖解 | 靜態向量圖可重跑、可審核，與互動圖功能重疊 |
| 2026-11-11 | **由獨立 repo `exam-wiki-RC` 搬入本資料夾**（只搬檔案，不含 git 歷史）：先刪 10-29 scaffold 骨架（七層 wiki 空殼、空索引、共用樣板儀表板），再搬入 `raw/`（24 份考卷、100 題解析、8 份 methods）、`study/`、`wiki/queries/`、`archive/`（原 repo 11-01 已封存的舊 wiki）、`影片講義/`、儀表板 `index.html`／`dashboard-data.js`；原 repo 根目錄兩份複核報告移入 `wiki/queries/`；`scripts/` 只留 RC 專屬的 `gen_lecture_RC-*_figs.py` 與 `apply_figs.py`；原 repo 根目錄 CLAUDE*.md、xcheck.py、知識圖譜（`generate_knowledge_graph.py`＋`knowledge_graph.html`，由舊 wiki 產生、已不更新）存參考副本於 `archive/exam-wiki-RC-root/`；README、檔案架構索引表、知識庫使用說明書改為合併後路徑；`syllabus_taxonomy.json` 副本以 `sync_taxonomy.py` 重新同步；§1 考卷檔名更正為實際的 `RC-YYYY_鋼筋混凝土設計與預力.pdf`（`subject_profiles.json` `examFile` 與根目錄 CLAUDE.md 同步）；§3 補標準標籤詞彙、§6 改指封存診斷頁、§7 補量法慣例、§8 指向原 repo 長版框架 | 五科合一，RC 不再在原 repo 分岔維護。原 repo 與 GitHub Pages 舊網址維持上線不動，git 歷史保留在原 repo。未搬：`.claude/`、`.vscode/`（本機設定）、`_to_delete/`（gitignore 暫存）、`.github/workflows/pages.yml`（根目錄已有 deploy-pages.yml）、未追蹤的 `subject-frequency-map.skill`（v1.1，比根目錄 `skills/` 版舊） |
| 2026-11-11 | 共用腳本取代原 repo 版：`gen_problems_view.py` → 根目錄 `render_problem_view.py`（先併入「引言後緊接清單補空行」，對 SS／SA 渲染 0 差異），100 頁 problems-view 以新腳本重產；`build_unit_page.py`／`build_frequency.py` 改用根目錄版（根目錄 `unit_page_template.html` 併入 RC 已拿掉的「📊 解析含互動圖」圖例），5 頁單元總覽與 `frequency-RC.html` 重產 | 題目瀏覽頁：89 頁有差異、11 頁相同。差異只有 ① 數學式內 `<`、`>`、`&` 改為 HTML 跳脫（KaTeX 顯示相同、HTML 不再被誤解析）② 斜體內粗體不再拆成兩段 ③ 表格內 `[[ID]]` 轉為藍色徽章 ④ RC-2009-1 引言後一列清單恢復為清單；頁首、按鈕、腳本、圖片、表格、標題數不變。單元總覽：拿掉 6 題 🎬 與返回列（`解題過程影片/` 與 `start.html` 都不存在，原連結是死連結）、頁尾 `mathIn`；頻率熱圖：拿掉 5 個子項的「記憶片」連結（PDF 已於 11-06 移出 repo）、文字改為 v1.2 用語 |
| 2026-11-11 | 分類稽核（`audit_classification.py RC RC`）：0 題指向他科；1 筆題解標頭與索引不一致（RC-2009-2，見 §10） | 主副分類全部是 RC 子項，無須改歸 |

### 獨立 repo 時期的變更紀錄（2026-10-29～11-11，原 exam-wiki-RC/CLAUDE.md CHANGELOG，原樣保留）

> 2026-10-29 以前的紀錄見 `archive/exam-wiki-RC-root/CLAUDE.md`；11-06 的 study 清理只記在 `wiki/queries/log.md`。

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-31 | 全庫主／副分類與引用關聯複核修正：13 題分類、1 題設計法修正並同步解析表頭／wiki／儀表板／知識圖譜／frequency／命題分析頁／problems-view；24 頁「相關題目」重寫；RC-2023-1 wiki 頁改為摘要頁；wiki/log.md 亂碼還原 | 同題型分類標法不一（接頭、組合斷面、預力損失副分類），且部分相關題目依題號自動湊數、連到無關考點 |
| 2026-10-31 | 導入 unit-overview：`study/unit-RC-Un-m.html`（單元總覽＝命題分析＋公式給／背＋逐題公式表）由 `scripts/build_unit_page.py` 從 `study/data/unit-RC-Un-m.json` 產生，五單元（U1-1、U1-2、U2-1、U3-3、U4-1）上線；舊 `study-`／`formula-given-` 改轉址頁；problems-view、lecture 導覽、build_frequency 同步改指單元總覽 | 兩份單元頁內容互補但分散，「考了卻沒給」原為年份層級無法對應到題；改為逐題公式用途後證據可回溯到題解 |
| 2026-11-01 | wiki 封存：wiki/ 只保留 queries/；其餘目錄與 index.md、by-year.md 移至 archive/wiki/；wiki/log.md → wiki/queries/log.md；ingest / compile-all / lint / add-concept 停用；規則 1 methods 修改不再同步 wiki/methods/；index.html、講義連結、xcheck.py、generate_knowledge_graph.py 同步改指 | 舊 wiki 為未驗證的 AI 摘要且與 raw/solutions、study/ 重複（SS 掃描發現 45 處錯誤），改以正本與 study 教材為準 |
| 2026-11-01 | **廢止題解互動圖與補充筆記 PDF、儀表板改版**：刪除 18 份 `*-viz.html` 與 2 份題目補充 PDF；`question_index.json` 去 `hasViz`、`dashboard-data.js` 改 5 欄；`index.html` 完整解析改連 `study/problems-view/`、刪「指令速查」分頁並修資料夾授權恢復 bug | 圖解改以 `figs/*.svg` 為準；儀表板只保留讀書用功能，指令以 CLAUDE-CODE.md 為唯一正本 |

---

## 10. 本科與根目錄規則的差異

> 原 repo 的規則在 11-01 已跟上 wiki 封存，但沒有跟上 11-02 以後的題目正本與解析勘誤例外。搬入時逐項比對，RC 規則均已被根目錄涵蓋，或比根目錄窄（以根目錄為準）。
> 原 repo 規則原文見 `archive/exam-wiki-RC-root/`。以下只列仍屬 RC 專屬或待辦的項目：

| 項目 | 根目錄 | RC |
|------|--------|----|
| 規則 1 例外範圍 | 五處例外（含解析勘誤四條件、題目正本）；methods 三條件（含同步 study） | 原 repo 只有 `question_index.json`＋methods 兩處、methods 兩條件，解析 `.md` 不可改。**以根目錄版本為準**，不另立 RC 例外 |
| 題目正本 | 解題前先寫 `-problem.md`、確認後凍結 | **待辦**：RC 100 題都還沒有題目正本（`problemStatus` 欄位尚不存在）；要補時用 exam-problem-split（該 skill §0 第 2、3 點還寫著各科獨立 repo 與 `gen_problems_view.py`，見回報） |
| 解析標頭 | `**設計法：**` 值須與索引 `designMethod` 一致 | **待使用者決定**：`RC-2009-2` 標頭寫「工作性分析（非強度設計）」、索引為 `USD`（撓度／裂縫題）。可改索引為 `WSD`，或勘誤標頭為 `USD` |
| 儀表板 | 五科共用樣板＋`scripts/refresh_dashboard.py`（`KB_*`） | **待辦**：暫用原 repo 的 `index.html`／`dashboard-data.js`（`RC_*`、5 欄格式，11-01 改版的單元教材區與熱圖導覽卡）；RC 索引已有 `designMethod`，改回共用樣板只差決定要不要捨棄這些自訂區塊。改回前**不要**對 RC 執行 `refresh_dashboard.py`。根目錄 `index.html` 讀 `window[code+'_QUESTIONS']`，五科入口讀得到 RC 題數 |
| 網站網址 | — | **待辦**：舊站 `yjc5760.github.io/exam-wiki-RC` 維持上線；新站上線後在舊站加轉址 |
| 起點頁 | `start.html`（exam-start-page） | 尚未建立；單元總覽與頻率熱圖的「← 從這裡開始」返回列在沒有 `start.html` 時自動拿掉 |
| 一次性腳本 | 共用腳本在根目錄 `scripts/` | `scripts/gen_lecture_RC-*_figs.py`（講義附圖產生器）留在 RC；`scripts/apply_figs.py`（2026-10 把六題圖解插回正本，冪等）呼叫已不存在的 `scripts/gen_problems_view.py`，只留作紀錄、不要再跑 |
| 舊頁轉址 | 11-11 起不做 `study-`／`formula-given-` 轉址頁 | RC 在 10-31 已做了 10 頁轉址（各約 560 bytes），講義導覽仍連到它們，保留 |
| 解題影片／記憶片 | — | `解題過程影片/` 為 gitignore 的本機資料夾，目前是空的；記憶片 PDF 與觀念簡報 11-06 已移出 repo（改由外部專案管理），單元總覽與熱圖不再列這兩類連結 |
| `raw/exams/命題大綱.pdf` | 正本在根目錄 `命題大綱.pdf` | RC 原 repo 的副本，屬 raw 證據，保留不動 |
| 搬入前即有的死連結 | — | `RC-2022-3.md` 引用的 `RC-2022-3-fig-2.png` 不存在（只有 fig-1）；`RC-2006-1`、`RC-2017-2`、`RC-2023-3` 解析內的 `../RC-YYYY-N/RC-YYYY-N.md` 相關題目連結在題目瀏覽頁上解析成 `study/RC-YYYY-N/…`（6 處）。皆與原 repo 相同 |
