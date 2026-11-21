---
name: "youtube-upload"
description: "把做好的講解影片上傳到使用者的 YouTube 頻道（YouTube Studio）：使用者只負責選三個檔（影片 mp4、縮圖 png、字幕 srt），其餘由 Claude 在內建瀏覽器完成——撰寫並填入標題、說明（含章節時間碼）、設定非兒童專屬、上傳字幕語言、瀏覽權限、等待檢查、發布並回報連結。當使用者說「上傳影片到 YouTube」「幫我上傳到我的頻道」「發布這支影片」「填 YouTube 標題說明」，或手上有 blackboard-solution-video／pdf-narration-video 產出的 video/ 資料夾要上架時使用。"
---

# 上傳講解影片到 YouTube

## 分工（使用者已決定，不要改）

| 誰 | 做什麼 |
|---|---|
| **使用者** | 在檔案選擇視窗選 3 個檔：影片 `<名>.mp4`、縮圖 `<名>_thumbnail.png`、字幕 `<名>.srt` |
| **Claude** | 其他全部：讀資料夾、寫標題與說明、填欄位、兒童設定、字幕語言、瀏覽權限、等檢查、發布、驗證、回報連結 |

為什麼要使用者選檔：「選取檔案」會開 Windows 原生檔案視窗，屬於 Claude 桌面 app，computer use 不能操作；內建瀏覽器沒有本機檔案上傳工具；Chrome 擴充的 file_upload 單次上限 3.8 MB。**不要再嘗試繞過**（例如把檔案轉 base64 用 JavaScript 塞進 input），使用者已選定由自己選檔。

使用者預設頻道：`https://studio.youtube.com/channel/UC5Bk4KV4rV5VEsu-zbCfO5g`（使用者另給網址時以其為準）。預設設定：**非兒童專屬**、**公開**（使用者另有指定時照指定）。

## 流程

### 1. 讀資料夾、準備文案（不需使用者）

影片資料夾通常是 `.../解題過程影片/<名稱>/video/`，用 device_bash 讀：
- `HANDOFF.md`：題目／單元、範圍、規範版本、重要決定
- `講稿.md`：各章 `## 章名` 與逐段講稿 → 寫說明欄重點
- `timeline.json` ＋ `講稿.md` → 章節時間碼：**一律跑腳本，不要心算**
  ```bash
  python <skill>/scripts/yt_chapters.py "<video 資料夾>"
  ```
  （教訓：RC-U1-1 心算時把 s36 的起點當成 F 章起點，差了 20 秒。）
- 確認三個檔都在：`*.mp4`、`*_thumbnail.png`、`*.srt`，缺的先告訴使用者

**標題**（≤100 字元，不可有 `<` `>`）：`【結構技師 XX】<主題>：<一句鉤子>（<題號或單元碼>）`
**說明**（≤5000 字元）：
```
<一句話說這支影片是什麼、範圍>
<資料依據，例如幾年份考卷>

結論：<最重要的 1–2 個結論>

📌 章節
0:00 ...
（yt_chapters.py 的輸出；第一章必須 0:00、至少 3 章、每章 ≥10 秒）

⚠ <規範版本、年份記法等注意事項>

#結構技師 #<科目> #考古題 #<主題>
```
年份照影片用民國年。說明不要寫影片沒講的內容。

### 2. 開上傳視窗，請使用者選影片

先載入 built-in-browser skill 與 `mcp__remote-devices__Claude_Browser__*` 工具（ToolSearch 前綴一次載入）。
```
preview_start: https://studio.youtube.com/channel/<頻道ID>/videos/upload?d=ud
```
截圖確認已登入且出現「上傳影片」視窗。未登入就請使用者在瀏覽器窗格登入（不要代填密碼）。

請使用者選檔前先 `tabs_context` 看窗格狀態；隱藏時請他按 Ctrl+Shift+B（需在桌面 app）。訊息裡給**完整 Windows 路徑**方便貼上，並把擬好的標題、說明一起貼出讓他過目。
> 「請點『選取檔案』，貼上 `C:\...\video\<名>.mp4`，選好回覆『選好了』。」

### 3. 填詳細資訊

```
find "textbox" → 標題 ref（"新增可描述影片內容的標題…"）、說明 ref（"向觀眾介紹你的影片…"）
browser_batch: click 標題 → ctrl+a → type 標題 → click 說明 → ctrl+a → type 說明
```
驗證（點擊座標常重疊，**一定要驗**）：
```js
[...document.querySelectorAll('#textbox')].map(e=>e.getAttribute('aria-label')+' => '+e.innerText.length)
```
兒童設定：用 JS 列出 `tp-yt-paper-radio-button` 的 `name`，`find "radio"` 取 ref，**用 computer left_click 點** `VIDEO_MADE_FOR_KIDS_NOT_MFK`，再用 JS 確認 `hasAttribute('checked')`。

### 4. 縮圖（使用者選檔）

把縮圖區捲到可見：`document.querySelector('ytcp-uploads-dialog ytcp-thumbnail-uploader').scrollIntoView({block:'center'})`
請使用者點「縮圖 → 上傳檔案」選 `<名>_thumbnail.png`，回覆後截圖確認縮圖已出現。

### 5. 字幕（Claude 開好，使用者選檔）

1. 點步驟列「影片元素」→ 字幕「新增」（`#subtitles-button`）。語言若要求選擇，選「中文（台灣）」。
2. 出現輸入方式選單時選「**上傳檔案**」（不要點「手動輸入」；誤點的話用編輯器右上 ⋮ →「上傳檔案」）。
3. 「選取要上傳的字幕檔案類型」選「**包含時間碼**」→ 按「繼續」→ 此時開檔案視窗，請使用者選 `<名>.srt`。
4. 使用者回覆後截圖：第一行時間與文字要和 .srt 第 1 條一致（編輯器時間格式為 分:秒:影格）。
5. 按「完成」，等 3 秒，確認影片元素頁的字幕顯示「中文（台灣）版本：由你提供」。

### 6. 瀏覽權限與發布

1. 按「下一步」到「瀏覽權限」（用 `find "下一步"` 的 ref、computer click；**不要用 JS `.click()`**——RC-U1-1 用 JS 點「發布」沒有生效，影片停在草稿）。
2. 等檢查：底部要出現「檢查完畢，未發現任何問題」。還在「已檢查 N%」就每 30 秒看一次（`computer wait` 分段等，單次 JS 等待不要超過 ~40 秒）。
   - 若按發布時跳出「內容尚未檢查完成…仍要發布／知道了」：點「**知道了**」，等檢查完再發布，不要選「仍要發布」。
   - 檢查發現版權或其他問題 → 停下來告訴使用者，不要發布。
3. `find "radio"` → 點 `PUBLIC`（或使用者指定的權限），JS 確認 checked，按鈕文字變「發布」。
4. 點「發布」（computer click）。
5. **驗證**：分享對話框出現 `https://youtu.be/<id>`；再導到 `https://studio.youtube.com/video/<id>/edit`，頁首不可有「這部影片目前為草稿狀態」，標題、兒童設定正確。若仍是草稿：點「編輯草稿」重新走第 6 步。

### 7. 回報

一兩句話：已公開、連結 `https://youtu.be/<id>`、字幕與縮圖已上傳；有任何沒做到的（例如檢查有警告）明講。

## 注意

- 使用者說了「公開」就是發布的同意，不必再問；但要選「仍要發布」略過檢查、或檢查有問題時，一定先問。
- 不要動頻道其他影片、播放清單、頻道設定；「自動配音」等頻道橫幅不要點。
- 這是 repo `skills/` 的正本；改了要重新打包 `skills/youtube-upload.skill` 並把 .skill 傳到對話（見 CLAUDE.md 規則 12）。
