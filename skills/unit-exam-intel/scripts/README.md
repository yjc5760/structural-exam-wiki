# unit-exam-intel / scripts

| 檔案 | 做什麼 | 何時跑 |
|------|--------|--------|
| `stats.py` | 從 `raw/json/question_index.json` 算出頁面需要的每一個數字 | Step 1，產頁前 |
| `verify.py` | 把成品頁的 `Q[]`、篩選鈕、KPI 跟索引對帳 | Step 5，產頁後 |

兩支都只依賴 Python 標準函式庫，沙盒直接可跑，不需安裝任何套件。

```bash
python3 skills/unit-exam-intel/scripts/stats.py  SS-U1-1
python3 skills/unit-exam-intel/scripts/stats.py  SS-U1-1 --json > /tmp/intel.json
python3 skills/unit-exam-intel/scripts/verify.py SS-U1-1
```

`verify.py` 會 import `stats.py`（同目錄），兩檔不要分開搬。
離開碼 0 = 全過，1 = 有錯並逐條列出。

## 為什麼要有這兩支

命題情報頁上的每個數字都可以被重算，所以每個數字都應該被重算。
人眼看不出「篩選鈕寫 (7) 但實際 8 筆」，也不會去重數 24 個考年——
SS-U1-1 舊頁的 KPI 就把「近 6 考年 4/6」寫成「6/6」、「共 6 題」寫成「7 題」，
錯了將近一年沒被發現。
