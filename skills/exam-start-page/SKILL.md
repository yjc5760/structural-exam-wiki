---
name: exam-start-page
description: exam-wiki 五科（SS/SA/RC/SM/SD）「從這裡開始」起點頁 start.html 的新建與更新：把使用者貼的連結清單（單元總覽、講義、教科書、各類影片、解題影片）合併進 study/data/start-links.json，再產生學習路徑頁。說「更新 start.html」「依清單更新起點頁」「幫 XX 做從這裡開始」時使用。
---

# exam-start-page — 起點頁產生器

起點頁 `start.html` 是給考生的入口：知識庫能做什麼 → 六步學習路徑 → 各單元教材（可展開）→ 8／12 週進度表 → 怎麼跟 AI 協作。
首頁 `index.html` 是題庫儀表板，**不動**。

連結不寫在程式裡，全部放在 `study/data/start-links.json`；使用者每次給一份新清單，就合併一次、重產一次。

## 檔案

| 檔案 | 用途 |
|---|---|
| `scripts/parse_links.py` | 讀清單（純文字：段落標題＋「標題 網址」行），合併進 `start-links.json`，印出差異報告 |
| `scripts/build_start.py` | 讀 `start-links.json`＋`raw/json/syllabus_taxonomy.json`（科目、單元名稱）＋`raw/json/question_index.json`（題數），寫出 `start.html`，並列出找不到的相對連結 |
| `assets/start.css` | 樣式（順序：`XX/scripts/start.css` → 根目錄 `scripts/start.css` → 本檔） |
| `references/format.md` | 清單格式、JSON 欄位、合併規則的完整說明。清單格式有疑問時讀它 |

只用 Python 標準函式庫。知識庫在使用者電腦上，用 device_bash 在**知識庫根目錄**執行，以 `--repo XX` 指定科目資料夾。

**腳本放哪裡：** structural-exam-wiki 根目錄 `scripts/`（`parse_links.py`、`build_start.py`、`start.css`）五科共用一份，科目資料夾不放副本（根目錄 CLAUDE.md 規則 11）。科目要自訂樣式時才放 `XX/scripts/start.css`。本 skill 的 `scripts/`、`assets/` 是同一份的備份，供知識庫以外的環境使用。

## 流程

### 0. 第一次用在某一科時

- 該科若**已有**手寫的 `start.html` 或舊版 `scripts/build_start.py`（連結寫死在程式裡），先把舊資料轉成 `start-links.json`（用 importlib 載入舊程式的 `UNITS`／`GLOBAL`，dump 成 JSON），用新版 `build_start.py` 產生到暫存檔，跟原本的 `start.html` 比對進度表與連結數，確認轉換沒有掉資料，**再**合併新清單。
- 該科**完全沒有**起點頁：直接從清單開始，`parse_links.py` 會依清單建立 JSON（科目代號自動從單元代號判斷，網站網址預設 `https://yjc5760.github.io/exam-wiki-XX/`）。

### 1. 存清單、試合併

把使用者的清單存成 `study/data/start-links.txt`（覆蓋舊的；它是下次更新的底稿），然後：

```bash
python3 scripts/parse_links.py XX/study/data/start-links.txt --repo XX --dry-run
```

讀報告：`+` 新增、`~` 改變、`=` 清單沒提到而保留舊值。stderr 的 ⚠ 行（找不到單元代號、解題影片沒題號）必須逐條處理：修清單或手動補 JSON，不要略過不提。

### 2. 合併、產生

```bash
python3 scripts/parse_links.py XX/study/data/start-links.txt --repo XX
python3 scripts/build_start.py --repo XX
```

### 3. 檢查

- `build_start.py` 印出的「找不到的相對連結」應為空；有的話是檔案還沒建立，回報給使用者，不要自己刪連結。
- 被連結的檔案若在 git 是 untracked（`git status --short` 顯示 `??`），提醒使用者一起 commit，否則 GitHub Pages 上會 404。
- YouTube 連結數 ＝ 清單裡的影片數 ＋ 報告中「保留」的影片欄位數。對不上就是有行沒被解析到。
- 截圖看一次：展開最後一個單元，確認教材列表、解題清單、教科書講解影片那一行正常。

### 4. 收尾

- 在 `XX/SUBJECT.md` §9 CHANGELOG 加一行（日期｜做了什麼｜原因／注意事項；影響多科者改記根目錄 `CHANGELOG.md`）。
- **不要 git commit。** 列出動到的路徑交給使用者自己 commit。
- 回報時講清楚：哪些單元新增了什麼、哪些欄位因清單沒提到而保留（例如非動畫版講義影片、講義簡報 PDF、NotebookLM），讓使用者決定要不要拿掉。

## 判斷規則

- **清單沒提到的欄位一律保留**，只在回報中列出。使用者要拿掉才拿掉（直接改 JSON 把欄位設成空字串）。
- **解題影片沒寫標題**（只有題號＋網址）：沿用 JSON 裡同題號的舊標題（`solutions` 或 `practice`）；都沒有就只顯示題號，並在回報中列出請使用者補。
- **觀念講義影片**：標題含「動畫」→ `lecture_anim`，否則 → `lecture_video`。
- **單元順序**＝清單「單元總覽」段的順序（建議讀書順序）。清單沒有該段時沿用 JSON 順序。
- **教科書標籤**由檔名尾碼對照（tension→拉力桿件…）；沒對照到的新尾碼會原樣顯示英文，回報給使用者，請他給中文名後寫進 JSON 的 `textbook_labels`。
- **進度表**自動排：第 1 週定方向、最後至少 1 週總複習。單元比週數多時連續單元併週；12 週版多出的週數依歷屆題數分給大單元，單元若有 `weeks12` 則照它指定的週數。
- 行首的 `@` 等記號忽略。
- 科目名稱、單元名稱一律從 `syllabus_taxonomy.json` 讀，不手打。

## 各科注意

| 科目 | 名稱（taxonomy） | 備註 |
|---|---|---|
| SS | 鋼結構設計 | 標準版本；有 `weeks12` 覆寫（U1-3、U2-1 各 1 週） |
| SA | 結構學 | |
| RC | 鋼筋混凝土設計與預力混凝土設計 | 子項多，8 週版會併週 |
| SM | 土壤力學與基礎設計 | 子項多，8 週版會併週 |
| SD | 結構動力分析與耐震設計 | |

各科的 `question_index.json` 結構相同（`questions[].moduleId`、`primaryTopicId`）；若某科不同，先看一眼再改 `build_start.py` 的讀法，不要硬套。
