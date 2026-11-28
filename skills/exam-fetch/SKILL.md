---
name: "exam-fetch"
description: "結構技師考試知識庫（SS/RC/SA/SD/SM）下載考古題：從考選部考畢試題查詢平臺找出新年度結構工程技師試題，用 scripts/fetch_exams.py 存進各科 raw/exams/ 並記錄來源，接著交給 exam-solve。使用者說「下載考古題」「下載 YYYY 年考卷」「有沒有新考題」「抓新年度考題」「檢查考卷是否和官網一致」時使用。"
---

# exam-fetch — 下載新年度考古題（五科通用）

考卷原件來自考選部「考畢試題查詢平臺」（`https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx`）。
下載一律用根目錄的 `scripts/fetch_exams.py`：它會從當年試題清單自動找出結構工程技師那場考試，
因為官網每年的考試、類科、科目代碼都不同，所以不要手寫或猜代碼。
本 skill 決定要下載哪幾年、哪幾科，在使用者電腦上執行腳本（computer use 代跑，或請使用者手動跑），再驗收結果。

## 0. 先知道的限制

- **Claude 的沙盒（含 Cowork 的 device_bash）連不到 moex.gov.tw**（網路白名單擋下，回 403）。
  腳本必須在**使用者的 Windows 本機**執行：有 computer use 時由 Claude 雙擊批次檔代跑（步驟 2A），否則請使用者手動跑（步驟 2B）。
  不要反覆重試，也不要改用 curl、代理或其他繞路方式。
- 可以先用 device_bash 試一次 `curl -sS -m 15 -o /dev/null -w "%{http_code}" https://wwwq.moex.gov.tw/exam/`：
  回 200 才代表這次環境連得到，可以直接用 device_bash 跑腳本；其餘走步驟 2。
- 內建瀏覽器（Claude_Browser）在使用者電腦上，連得到官網，可以用來**查看**官網是否已公布某年試題，但不用它下載檔案。
- `raw/exams/` 是證據：既有考卷一律不覆蓋（腳本本身也不會覆蓋）。

## 1. 確認範圍

1. 看各科 `XX/raw/exams/` 現有的最新年度，以及使用者要的年份或科目；沒指定就是「現有最新年度＋1 到今年」、五科全下。
2. 材料力學（MM）目前沒有科目資料夾，腳本會略過；使用者要 MM 時，先提醒用 `scripts/scaffold_subject.py MM` 建資料夾。
3. 不確定官網是否已公布時，用內建瀏覽器開 `wFrmExamQandASearch.aspx?y=<西元年>`，找「結構工程技師」。
   找不到就告訴使用者「官網尚未公布」，停止。

## 2A. computer use 代跑（優先；2026-11-28 實測可行）

computer use 工具（`mcp__remote-devices__computer_*`）在本次對話可用、或有 `enable__mcp__remote-devices__computer` 時走這條；使用者要求「用 computer use」時也走這條。
先載入 `computer-use` skill。

1. **寫批次檔**（device_bash 寫進 `.work/`，它在 gitignore 裡；CRLF 換行；參數依步驟 1 的範圍）：
   ```
   printf '%s\r\n' '@echo off' 'chcp 65001 >nul' 'cd /d "%~dp0.."' 'set PYTHONIOENCODING=utf-8' \
     'where python >nul 2>&1 && (python scripts\fetch_exams.py <參數> > .work\fetch.log 2>&1) || (py scripts\fetch_exams.py <參數> > .work\fetch.log 2>&1)' \
     'type .work\fetch.log' 'pause' > .work/fetch.bat
   ```
   批次檔只放這一行腳本呼叫，不加其他指令；輸出導向 `.work\fetch.log` 供之後讀取。
2. **取得權限**：`computer_resolve_access(["File Explorer"])` → `computer_request_access`（理由寫「在檔案總管雙擊 .work\fetch.bat，用你電腦的網路下載考卷」）。
   檔案總管與終端機都只給 **click** 等級：不能打字、不能在網址列／搜尋框／執行視窗輸入，**只用滑鼠點兩下**，也不要用任何方式繞過這個限制。
3. **雙擊執行**：`computer_open_application("File Explorer")` → 截圖 → 依序雙擊「下載」→「structural-exam-wiki」→「.work」→「fetch」（類型為 Windows 批次檔）。
   每一步先截圖再點；畫面上已有開著 `.work` 的視窗就直接用它。
4. **讀結果**：等 20–30 秒，用 device_bash `cat .work/fetch.log`；還沒寫完就再等一下。結束後 `computer_release_lock`。
   跑完後終端機視窗會停在「按任意鍵繼續」，告訴使用者可以直接關掉。
5. 讀到結果就直接進步驟 3 驗收，不用等使用者回報。

## 2B. 請使用者手動執行（沒有 computer use 時；Windows，知識庫根目錄）

依範圍給出完整指令，一次給齊，不要只給片段：

```
cd C:\Users\yjc57\Downloads\structural-exam-wiki
python scripts\fetch_exams.py --dry-run          ← 先看會下載什麼
python scripts\fetch_exams.py                    ← 真的下載（預設：最新年度＋1 到今年、五科）
```

常用參數：

| 需求 | 參數 |
|------|------|
| 指定一年 | `--year 2026` |
| 年份範圍 | `--years 2002-2026` |
| 指定科目 | `--subject SS,RC` |
| 只檢查有無新考卷（有則結束碼 1） | `--check` |
| 比對既有考卷與官網（不覆蓋，不同時官網版另存 `*.moex-YYYYMMDD.pdf`） | `--verify --years 2002-2025` |

常見問題（直接附在指令後面告訴使用者）：
- 找不到 `python`：改用 `py`。
- SSL 憑證錯誤：先跑 `pip install --upgrade certifi`，再重跑。
- 出現「⚠ 官網有 n 份試題檔」：該科試題分成多個檔，腳本只取第一份；請使用者到官網確認其餘檔案。

然後**停下來等使用者回報**（貼上腳本輸出，或說「下載好了」）。

## 3. 驗收（讀到 2A 的 log，或使用者回報後）

用 device_bash 確認：
1. 每份預期的檔案都存在：`XX/raw/exams/XX-YYYY_<examFile>.pdf`，檔名主體取自 `scripts/subject_profiles.json` 的 `examFile`。
2. 檔頭是 `%PDF`，大小合理（通常 100–400 KB）；`pdfinfo` 看頁數。
   `pdftoppm -r 50 -f 1 -l 1 -png <pdf> .work/p<年>/<科>` 轉第一頁，用 device_stage_files 取回、把各科頁首裁切拼成一張圖目視：
   抬頭年度（民國）正確、「類科：結構工程技師」、「科目」與檔名一致。
3. 各科 `wiki/queries/log.md` 最後有一筆 `FETCH-EXAM`（來源代碼與 MD5）。
4. 使用了 `--verify` 而有檔案不一致時：列出兩份的大小，**不要自行取代原檔**。原檔是證據，由使用者決定。

回報表：

| 科目 | 年度 | 檔案 | 大小 | 頁數 | 檢查 |
|------|------|------|------|------|------|

## 4. 收尾

- 根目錄 `CHANGELOG.md` 不用記（每份下載已記在各科 log.md）；年度批次下載可在回報裡提一句。
- 提醒下一步：在 Cowork 對每科說「解析 YYYY 年 XX 考卷」（exam-solve）。
- 列出新增的檔案路徑；git commit 由使用者自己做。

## 不要做的事

- 自己猜或寫死考試代碼、類科代碼、科目代碼來組下載網址
- 沙盒連不到時反覆重試，或改用其他工具、代理繞過網路限制
- 覆蓋、改名或刪除 `raw/exams/` 既有考卷
- 使用者還沒回報（或還沒讀到 log）就假設下載成功、直接開始解題
- 用 computer use 在終端機或檔案總管網址列打字、按鍵（只能雙擊批次檔）；批次檔裡放腳本呼叫以外的指令
