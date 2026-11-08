# 清單格式與資料欄位

## 清單（start-links.txt）

純文字。沒有網址的行是**段落標題**；有網址的行是**項目**（網址前後的文字當標題）。空行忽略，行首 `@` 忽略。

```
考古題知識庫
https://yjc5760.github.io/exam-wiki-SS/

全科出題頻率熱圖
https://yjc5760.github.io/exam-wiki-SS/study/frequency-SS.html

SS (鋼結構設計)全科讀書策略 https://youtu.be/xxxx      ← 含「讀書策略」的行不論在哪段都當全科策略影片

單元總覽                                                ← 這段的順序＝起點頁單元順序
https://yjc5760.github.io/exam-wiki-SS/study/unit-SS-U1-1.html

觀念講義
https://.../study/lecture-SS-U1-1.html

教科書                                                  ← 一單元可多冊，標籤由檔名尾碼決定
https://.../study/textbook-SS-U1-1-tension.html

公式記憶影片
SS-U1-1 拉力及壓力桿件 公式記憶 https://youtu.be/xxxx

觀念講義影片                                            ← 標題含「動畫」→ 動畫版
SS-U1-1 拉力及壓力桿件 (動畫版) https://youtu.be/xxxx

影片講義
https://.../影片講義/SS-U1-1_拉力及壓力桿件.html

教科書講解影片                                          ← 標題去掉單元代號、單元名稱、-T1 後當集名
SS-U1-1 拉力及壓力桿件 (上) 拉力篇 https://youtu.be/xxxx
SS-U2-3-T1 施工要求 第1集 銲接冶金 https://youtu.be/xxxx

主題影片                                                ← 跨單元，列在單元清單下方
DAM 直接分析法 https://youtu.be/xxxx

解題過程影片
SS-U1-1 拉力及壓力桿件                                  ← 解題段裡含單元代號、沒網址的行＝單元小標題
SS-2013-3 兩平面有效長度 https://youtu.be/xxxx
SS-2005-4 https://youtu.be/xxxx                         ← 沒標題就沿用舊標題
```

段落標題以關鍵字辨識（長的優先）：觀念講義影片、教科書講解影片、解題過程影片／解題影片、公式記憶影片、影片講義、主題影片、單元總覽、觀念講義、教科書、NotebookLM／筆記本、簡報、出題頻率、考古題知識庫／題庫儀表板、從這裡開始（略過）。
單元代號從標題或網址抓（`XX-Un-m`）；解題影片的單元取小標題，沒有小標題時查 `question_index.json` 的 `primaryTopicId`。
指向本站的網址轉成相對路徑（並把 %xx 解碼成中文檔名）。

## start-links.json

```json
{
 "subject": "SS",
 "site": "https://yjc5760.github.io/exam-wiki-SS/",
 "repo": "https://github.com/yjc5760/exam-wiki-SS",
 "subject_name": "（選填，覆寫 taxonomy 名稱）",
 "textbook_labels": {"新尾碼": "中文標籤"},
 "global": {
  "frequency": "study/frequency-SS.html",
  "strategy_video": "https://youtu.be/...",
  "wiki": "index.html",
  "feedback": "https://github.com/.../issues/new?template=correction.yml",
  "topic_videos": [["DAM 直接分析法", "https://youtu.be/..."]],
  "goatcounter": "（選填，GoatCounter 代碼）"
 },
 "units": [{
  "id": "SS-U1-1", "name": "拉力及壓力桿件",
  "overview": "study/unit-SS-U1-1.html",
  "lecture": "study/lecture-SS-U1-1.html",
  "textbook": [["拉力桿件", "study/textbook-SS-U1-1-tension.html"]],
  "textbook_videos": [["(上) 拉力篇", "https://youtu.be/..."]],
  "lecture_video": "", "lecture_anim": "https://youtu.be/...",
  "video_handout": "影片講義/SS-U1-1_拉力及壓力桿件.html",
  "slides_pdf": "", "formula_video": "https://youtu.be/...", "notebooklm": "",
  "solutions": [["SS-2013-3", "兩平面有效長度", "https://youtu.be/..."]],
  "practice": [["SS-2023-3", "標題", "study/problems-view/SS-2023-3.html"]],
  "weeks12": 1
 }]
}
```

- 任何欄位空字串／空陣列 → 起點頁不輸出那一列。
- `practice`：沒有解題影片時改列這些解析頁當練習題；有 `solutions` 就不顯示。
- `weeks12`：12 週版該單元排幾週（選填）。

## 合併規則（parse_links.py）

| 情況 | 處理 |
|---|---|
| 清單有、JSON 沒有 | 新增（報告 `+`） |
| 清單有、JSON 有且不同 | 用清單（報告 `~`） |
| 清單沒提到 | 保留 JSON 舊值（報告 `=`） |
| 清單式欄位（textbook、textbook_videos、solutions） | 該單元在該段出現 → 整組換成清單版本 |
| 「主題影片」段存在 | 整組換掉；段不存在 → 保留 |
| 清單有新單元 | 新增單元，名稱由 build 時從 taxonomy 補 |
