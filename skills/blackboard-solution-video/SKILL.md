---
name: "blackboard-solution-video"
description: "把考題解析（exam-wiki 的 XX-YYYY-N.md 題解、或任何有完整算式的解題文件）做成「黑板手寫風」講解影片，可直接上傳 YouTube——Manim 動畫逐步寫出算式與圖解、Gemini TTS 中文配音（Azure 備用）、對齊語音停頓的 .srt 字幕、1280×720 封面 PNG。當使用者說「把這題做成解題影片」「解題過程影片」「黑板講解影片」「幫我做 SM-2020-3 的影片」「題解轉影片」「Manim 講解」「做 YouTube 解題影片／封面／字幕」，或手上有題解想配音成教學影片時，必須使用此 skill；使用者提到接續某題的影片工作（例如有 HANDOFF.md、segments.py、durations.json）時也要使用。若來源是 PDF 投影片、要的是投影片翻頁式影片，改用 pdf-narration-video。"
---

# 黑板解題講解影片

把一題的解析做成約 3–8 分鐘的黑板講解影片。交付三個檔案：`<題號>.mp4`（不嵌字幕）、`<題號>.srt`、`<題號>_thumbnail.png`，三個都直接上傳 YouTube。

完整範例在 `references/example-SM-2020-3/`（土壤力學相對密度，22 段、6 章、6 分 22 秒），寫新題之前先看它的 `segments.py` 和 `scene.py`，照同樣的節奏與版面語言寫。踩過的坑與細節在 `references/lessons.md`，寫動畫前先讀第 2 節，做字幕或成片時讀第 4、5 節。

## 分工：誰在哪裡跑什麼

| 工作 | 在哪裡 | 為什麼 |
|---|---|---|
| 寫講稿、寫動畫、渲染、字幕、合成、封面 | Linux（Cowork 雲端沙箱或 WSL） | 需要 Manim、LaTeX、ffmpeg |
| 配音 | **使用者自己的 Windows**（雙擊 `run_tts.bat`） | 沙箱與 Cowork 本機 VM 通常連不到 Google API；金鑰也留在使用者電腦 |

工作資料夾放在使用者電腦上，例如 `解題過程影片/<題號>/video/`。每完成一步，就把該交付的檔案寫回這個資料夾。

## 流程（每個 ★ 都要停下來等使用者確認）

### 0. 接手或開始

- 資料夾裡如果有 `HANDOFF.md`，先讀它，從上次停下的地方接續。
- 讀題解（.md 或網頁）。題解裡已經畫好的附圖（figs/*.png）可以參考構圖。
- ★ 問範圍：只講主解法加陷阱（約 3 分鐘），還是整題含驗算（6–8 分鐘）。

### 1. 建資料夾、裝環境

```bash
bash <skill>/scripts/setup_render_env.sh                 # 首次：Manim、LaTeX、Iansui 字型
python <skill>/scripts/init_video.py <video資料夾> --id SM-2020-3 --topic 相對密度
```
`init_video.py` 會複製進去的檔案：`board_scene.py`（底座）、`segments.py`（講稿範本）、`scene.py`（動畫骨架）、`board.png`（黑板底圖）、配音／字幕／合成／封面／檢查工具、`run_tts.bat`、`env.example`。已存在的檔案不會覆蓋。

### 2. 寫講稿 → ★ 使用者確認

改 `segments.py`，這是唯一的改稿處：
- **SEGMENTS**：逐字旁白。數字寫國字，符號寫念法（寫法規則見 lessons.md 第 1 節）。
- **CHAPTERS**：章名，會顯示在黑板左上角。
- **BOARD**：每段黑板上要出現什麼。寫具體，例如「紅字錯誤式 (500−440)/200＝30% 打叉」。
- **SUB_SYMBOLS / SUB_KEEP**：字幕端的符號轉換，以及不要轉成數字的詞。

章節骨架：題目（列出已知、點出問什麼）→ 主解法 → 每個陷阱各一章或一段（錯在哪、錯了會得到什麼數字）→ 驗算或第二解法 → 總結（條列重點加答案）。

接著跑 `python script_md.py` 產生 `講稿.md` 給使用者審閱，再跑 `python make_srt.py --preview` 檢查數字轉換有沒有誤轉。

### 3. 寫動畫 → 無聲審閱版 → ★ 使用者回饋

照 BOARD 寫 `scene.py`，每段的形式是 `self.begin("sXX")` → 動畫 → `self.end()`。可用的 helper（`T` 中文、`M` 公式、`row`、`xmark`、色票、`clear_board`）見 `board_scene.py` 開頭的說明。

```bash
manim -ql --disable_caching scene.py Full && python frames_grid.py   # 用 Read 看 frames_grid_*.png
```
逐張檢查有沒有重疊、出界、被虛線穿過，修到乾淨為止（常見問題見 lessons.md 第 2 節）。然後用 `manim -qm` 出 720p 無聲審閱版給使用者。這時每段長度是估計值，節奏會在配音後自動對齊。

### 4. 配音（使用者在 Windows 上做）

請使用者：
1. 把 `env.example` 複製成 `.env`，填入 `GEMINI_API_KEY`（`.env` 放在影片資料夾或上層資料夾都可以）。
2. `pip install -U "google-genai>=2.25.0"`
3. 需要選聲音時先試聽：`python tts_gemini.py --audition Charon,Sadaltager,Iapetus`，再把 segments.py 裡的 `GEMINI_VOICE` 改成選定的聲音。
4. 雙擊 `run_tts.bat`，產出 `audio/s*.wav` 和 `durations.json`。

完成後把 `audio/*.wav` 和 `durations.json` 搬到渲染環境。

### 5. 成片、字幕、封面 → ★ 使用者驗收

```bash
manim -qh --disable_caching scene.py Full        # 每段長度＝真實配音＋0.6 s，寫出 timeline.json
python make_srt.py                               # <題號>.srt（對齊語音停頓）
python make_final.py                             # <題號>.mp4（不燒字幕，約 18 MB／6 分鐘）；--burn 才燒
manim -s -r 1280,720 --format png --disable_caching thumb.py Thumb   # 封面
```
- 檢查有沒有動畫比配音長：對每段確認 `timeline 長度 − (durations + 0.6) ≤ 0.1`。超過的，縮短該段動畫的 run_time。
- 封面：改 `thumb.py` 的文字區，並把 `figure()` 換成這題最有辨識度的圖（例子見 `references/example-SM-2020-3/thumb.py`）。輸出後用 Read 看一次，確認沒有出界或重疊。
- 交付：srt、thumbnail.png 寫回使用者的資料夾。
- **mp4 一律不再壓縮**：`make_final.py` 輸出的就是交付版，不要為了檔案大小再用 ffmpeg 重新編碼或調高 CRF。mp4 在 20 MB 以下就照常寫回資料夾；超過 20 MB（回寫上限，8 分鐘以上的片常見）就直接用 SendUserFile 當聊天附件給使用者下載，請他自己放進 video 資料夾，並在 HANDOFF.md 註明。聊天附件上限約 30 MB，超過時先告訴使用者，不要自行壓縮。

之後要修改：某段念錯就改稿，再請使用者跑 `run_tts.bat --only s07`，然後重跑步驟 5。字幕不準就請使用者給時間點，照 lessons.md 第 4 節調整。

### 每一步都要做的

- 更新資料夾裡的 `HANDOFF.md`：已確認的決定、目前進度、下一步、環境備註。換 session 或換人接手時就靠它。
- 使用者如果有自己的 git 流程，只寫檔、列出改了哪些路徑，不要替他 commit。
- 不要讀出、印出或打包 `.env` 的內容。