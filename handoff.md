# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-28 10:18

---

## 一、本次工作完成概況

### 1. 知識庫升級：全站知識索引（`kb/`）、信任標章、概念字典與跨科脈絡
- **全站知識索引系統**：
  - 新增 `scripts/build_kb_index.py`，由五科正本（解析 §2／§3／§3.5、題目正本、`question_index.json`、audit-ledger）編譯產出 `kb/` 六檔：`search.html`（全站搜尋＋同義詞展開）、`traps.html`（陷阱字典 1,678 條／451 題）、`l3.html`（L3 深層知識 1,695 條／452 題＋熱點）、`concepts.html`（概念字典、跨科脈絡、規範條文反查）、`trust.html`（可信度總覽與人工複核待辦）、`kb-data.js`。
  - 更新根目錄 `index.html` 加入 `kb/` 各索引入口。
- **489 頁題目瀏覽頁加入信任標章**：
  - 全五科 `*/study/problems-view/*.html` 頁首加入 `<!--trust-->…<!--/trust-->` 標章（人工已核 6、盲解一致 293、勘誤已落實 158、分歧已裁定 5、盲解後有修改 26、勘誤後待複驗 1），並同步更新 `scripts/render_problem_view.py`。
- **概念字典與跨科脈絡**：
  - 新增根目錄 `concept_vocabulary.json`（167 個概念，待人工複審 `confirmed`）與 `cross_subject_links.json`（5 條單元層跨科脈絡，待審）。
- **規則與 Skills 同步**：
  - 更新 `CLAUDE.md`（規則 14、規則 1 驗算腳本 `verify_*.py` 與重跑 `build_kb_index`）、`CLAUDE-SPEC.md`（`codeClauses`、`verify_*.py` 格式）、`CLAUDE-CODE.md`、`CHANGELOG.md`。
  - 更新並重新打包 `skills/exam-errata`、`skills/exam-solve`、`skills/exam-wiki-audit`。

### 2. 考卷自動下載工具與 115 年（2026）五科考古題收錄
- 新增 `scripts/fetch_exams.py`：自動查詢考選部考畢試題查詢平臺（`wwwq.moex.gov.tw`）當年度結構工程技師試題並下載，不覆蓋既有原件，自動記錄來源代碼與 MD5 至各科 `wiki/queries/log.md`。
- 新增 `skills/exam-fetch/` 與打包檔 `skills/exam-fetch.skill`（含 computer use 代跑與手動執行流程），同步更新 `skills/README.md`、`CLAUDE.md`、`CLAUDE-CODE.md`。
- 已實測下載並驗收 **115 年（2026）五科考卷 PDF**（`RC/SA/SD/SM/SS` 各 1 份）並記入五科 `wiki/queries/log.md`。

### 3. 五科講義精選題練習卷（173 題）與講義印刷按鈕整合
- 依五科共 35 份觀念講義（`XX/study/lecture-XX-Un-m.html`）末節「精選 5 題」，批次產出 **173 份單題練習卷 HTML 與 PDF**（`XX/study/practice/<題號>-practice.html/.pdf`）及各科 `精選題索引.md`（5 份）。
- 於 35 份觀念講義的精選題題號旁加入「🖨️ 練習卷」按鈕（`a.pdfbtn`，新分頁開啟 PDF，列印講義時自動隱藏）。
- 修正 `skills/exam-practice-sheet/SKILL.md`（題首／共用公式區 y 座標改取第一個非空白 span 頂端，解決高公式切到上一行的問題）並重新打包 `skills/exam-practice-sheet.skill`。

---

## 二、本次變更檔案清單（共修改 545 檔、新增 368 檔）

1. **規則、文件與入口頁**：
   - `CLAUDE.md`、`CLAUDE-CODE.md`、`CLAUDE-SPEC.md`、`CHANGELOG.md`、`handoff.md`、`index.html`
2. **全站知識索引與字典**：
   - `scripts/build_kb_index.py`、`scripts/render_problem_view.py`
   - `concept_vocabulary.json`、`cross_subject_links.json`
   - `kb/`（6 檔：`search.html`、`traps.html`、`l3.html`、`concepts.html`、`trust.html`、`kb-data.js`）
   - `*/study/problems-view/*.html`（489 檔信任標章）
3. **考卷自動下載與 115 年考卷**：
   - `scripts/fetch_exams.py`
   - `RC/raw/exams/RC-2026_鋼筋混凝土設計與預力.pdf`、`SA/raw/exams/SA-2026_結構學.pdf`、`SD/raw/exams/SD-2026_結構動力分析與耐震設計.pdf`、`SM/raw/exams/SM-2026_土壤力學與基礎設計.pdf`、`SS/raw/exams/SS-2026_鋼結構設計.pdf`
   - 五科 `*/wiki/queries/log.md`（5 檔）
4. **精選題練習卷與講義更新**：
   - 五科 `*/study/practice/`（173 份 `.html`、173 份 `.pdf`、5 份 `精選題索引.md`，共 351 檔，約 182.9 MB）
   - 五科 `*/study/lecture-*.html`（35 檔）
5. **Skills 與打包檔**：
   - `skills/README.md`
   - 新增：`skills/exam-fetch/SKILL.md`、`skills/exam-fetch.skill`
   - 更新：`skills/exam-errata/`、`skills/exam-solve/`、`skills/exam-wiki-audit/`、`skills/exam-practice-sheet/` 及對應 `.skill` 打包檔

---

## 三、踩坑與注意事項
- **GitHub Pages 容量監控**：本次新增 `study/practice/` 173 份練習卷 PDF/HTML 約 182.9 MB，全站待部署靜態檔案總計約 **846.4 MB**（上限 1 GB，尚餘約 153 MB 空間）。後續若再新增大量 PDF（如教科書或大量練習卷），需評估排除原始 `practice/*.html` 或改採外部託管／精簡 PDF 體積，以免超過 Pages 限制。
- **帳號端 Skills 重新安裝**：本次有 5 個 `.skill` 檔新增或更新（`exam-fetch`、`exam-errata`、`exam-solve`、`exam-wiki-audit`、`exam-practice-sheet`），Cowork 帳號端需確認已安裝最新版。
- **CRLF／LF 換行警告**：部分檔案（如 `CHANGELOG.md`、HTML、log）目前為 LF 換行，Windows Git 提示會在下次 checkout 轉為 CRLF，屬正常現象。

---

## 四、下一步建議
1. **解析 115 年（2026）五科新考卷**：五科考卷 PDF 皆已收錄完成，可逐科執行 `exam-solve`（「解析 2026 年 XX 考卷」）建置題目正本與解析。
2. **複審概念字典與跨科脈絡**：檢視 `concept_vocabulary.json`（167 項 `confirmed: false`）與 `cross_subject_links.json`（5 條），並視需要補強 `build_kb_index.py --check` 列出的陷阱／L3 缺漏題。
3. **既有教材進度延續**：SM-U2-1 單元總覽改版，以及 SA／SS 教科書專題教材與起點頁建置。
