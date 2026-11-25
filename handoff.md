# 交接與進度備忘（handoff.md）

> 更新時間：2026-11-26 07:35

---

## 一、本次工作完成概況

### 1. 結構動力學（SD）起點頁（Start Page）全面建置完工
- **起點頁資料與產物**：
  - 建立 `SD/study/data/start-links.txt` 與 `SD/study/data/start-links.json`，涵蓋 SD 7 大單元（單元總覽、觀念講義、教科書、公式記憶／觀念／教科書影片、各 5 支精選解題影片，共 57 支 YouTube 影片與教材連結）。
  - 使用 `scripts/build_start.py` 編譯產出 `SD/start.html` 一站式學習路徑起點頁，所有站內連結正確指引至五科合一架構（`structural-exam-wiki/SD/...`）。
  - 同步更新科目備忘 `SD/SUBJECT.md` 與 `CHANGELOG.md`。

### 2. 五科儀表板站內閱讀器授權路徑提示統一修正
- 修正 `RC/index.html`、`SA/index.html`、`SD/index.html`、`SM/index.html`、`SS/index.html`：
  - 首次使用站內閱讀器的授權提示「選擇 exam-wiki-XX 資料夾」與選錯資料夾的警告 alert「請選擇 exam-wiki-XX 資料夾本身」，統一改為「選擇 XX 科目資料夾」（例如「選擇 SD 科目資料夾」）。
  - 對齊五科合一目錄架構與共用樣板 `scripts/templates/dashboard-index.html`，消除使用者因尋找舊獨立 repo 資料夾名稱而產生的困惑。

### 3. 前階段重大成果回顧（已完成並上線）
- **結構動力學（SD）教科書等級專題教材（Unit Textbook）**：7 大單元（U1-1, U1-2, U1-3, U2-2, U2-3, U3-1, U3-2）HTML 與印刷級 PDF 全數完工。
- **結構動力學（SD）單元總覽（Unit Overview）**：7 大單元資料與 PDF 全面建置完工。
- **結構動力學（SD）觀念講義（Lecture）**：全系列改版與對帳完成。
- **土壤力學與基礎工程（SM）起點頁 `SM/start.html`**：整合完成。

---

## 二、本次變更檔案清單

1. **SD 起點頁相關檔案**：
   - `SD/start.html`
   - `SD/study/data/start-links.json`
   - `SD/study/data/start-links.txt`
2. **五科儀表板提示更新**：
   - `RC/index.html`
   - `SA/index.html`
   - `SD/index.html`
   - `SM/index.html`
   - `SS/index.html`
3. **歷程與交接筆記**：
   - `CHANGELOG.md`
   - `SD/SUBJECT.md`
   - `handoff.md`

---

## 三、踩坑與注意事項
- **五科合一閱讀器資料夾授權**：
  - 站內閱讀器透過 File System Access API 檢查的是所選目錄下的 `raw/solutions/{qid}.html`，因此使用者必須選擇各科目目錄本身（如 `SD/`、`RC/`），而非專案根目錄。提示文字已明確對齊。
- **CRLF/LF 格式一致性**：
  - 各科目儀表板 `index.html` 維持原有的換行規範（CRLF），避免產生不必要的全檔 diff。

---

## 四、下一步建議
1. **SM-U2-1（淺基礎）單元總覽改版**：SM 僅剩 U2-1 待更新至新版單元總覽格式。
2. **結構分析（SA）與鋼結構設計（SS）教材推進**：比照 RC、SM 與 SD 之標準化流程，陸續建置 SA 與 SS 的單元總覽、觀念講義、教科書專題教材及起點頁。
