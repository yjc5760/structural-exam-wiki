# subject-frequency-map / scripts

| 檔案 | 做什麼 | 何時跑 |
|------|--------|--------|
| `build_frequency.py` | 從 `raw/json/question_index.json` 算出全科頻率，產生 `study/frequency-XX.html`，並同時做對帳 | 每次題庫更新後、或新做了教材之後 |

只依賴 Python 標準函式庫，沙盒直接可跑，不需安裝任何套件。

```bash
cd exam-wiki-XX                                              # 一定要在知識庫根目錄
python3 skills/subject-frequency-map/scripts/build_frequency.py          # 自動偵測科目並產頁
python3 skills/subject-frequency-map/scripts/build_frequency.py --check  # 只對帳，不寫檔
python3 skills/subject-frequency-map/scripts/build_frequency.py --subject SS --date 2026-08-16
```

## 參數

| 參數 | 預設 | 用途 |
|------|------|------|
| `--subject` | 由 `moduleId` 自動偵測 | 科目代碼，索引混了多科時才需要指定 |
| `--index` | `raw/json/question_index.json` | 題庫索引 |
| `--taxonomy` | `raw/json/syllabus_taxonomy.json` | 命題大綱（科目名、單元、子項名稱都來自它） |
| `--study-dir` | `study` | 教材偵測掃描的目錄，也是預設輸出目錄 |
| `--out` | `<study-dir>/frequency-XX.html` | 輸出路徑 |
| `--date` | 今天 | 頁面右上角的更新日期（想產出可重現的檔案時固定它） |
| `--check` | — | 只印摘要與對帳，不寫檔 |

## 離開碼

- `0` — 產頁成功（可能帶警告，警告會印在摘要下方）
- `1` — 對帳的**算術**對不上（格子總和、列總和、單元小計），已中止且未寫檔

## 對帳檢查什麼

1. 熱圖所有主考點格子的總和 ＋ 孤兒題數 ＝ 題庫總題數
2. 每一列的格子總和 ＝ 該子項的主考點題數（副考點另檢一次）
3. 各單元小計加總 ＝ 主考點總數
4. 索引裡是否有 `syllabus_taxonomy.json` 找不到的 `primaryTopicId`（警告，頁面會出紅框）

## 為什麼要有對帳

熱圖是「把同一份資料換一種排法」，所以它必須跟原始索引逐格對得起來。
人眼看不出 14×24 的格子裡少了一題，程式看得出來——
而少一題的常見原因不是統計寫錯，是 `question_index.json` 裡有一個
`syllabus_taxonomy.json` 沒有的子項代碼（改過命題大綱、或代號打錯）。
