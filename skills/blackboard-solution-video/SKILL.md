---
name: "blackboard-solution-video"
description: "把考題解析（exam-wiki 的 XX-YYYY-N.md 題解、或任何有完整算式的解題文件）做成「黑板手寫風」講解影片，可直接上傳 YouTube——Manim 動畫逐步寫出算式與圖解、Azure TTS 台灣華語女聲 zh-TW-HsiaoChenNeural 配音（預設語速，不用 Gemini，由 Claude 直接生成）、1080p 成片一路跑完不停下確認、對齊語音停頓的 .srt 字幕、1280×720 封面 PNG。當使用者說「把這題做成解題影片」「解題過程影片」「黑板講解影片」「幫我做 SM-2020-3 的影片」「題解轉影片」「Manim 講解」「做 YouTube 解題影片／封面／字幕」，或手上有題解想配音成教學影片時，必須使用此 skill；使用者提到接續某題的影片工作（例如有 HANDOFF.md、segments.py、durations.json）時也要使用。若來源是 PDF 投影片、要的是投影片翻頁式影片，改用 pdf-narration-video。"
---

# 黑板解題講解影片

把一題的解析做成黑板講解影片，**影片長度沒有限制**，整題講完為止。交付三個檔案：`<題號>.mp4`（1920×1080，不嵌字幕）、`<題號>.srt`、`<題號>_thumbnail.png`，三個都直接上傳 YouTube。

## 使用者的固定要求（每次都照做）

- **配音**：Azure 女聲 `zh-TW-HsiaoChenNeural`，語速用預設（`+0%`，不加 prosody rate）。**不要用 Gemini**，即使 Azure 出錯也不要自行改用 Gemini，先回報錯誤。
- **配音由 Claude 直接生成**：不要請使用者雙擊或執行 `run_tts.bat`，Claude 自己在使用者電腦上跑（見步驟 4）。
- **一路跑到 1080p 成片，不停下來等確認**：講稿、動畫、配音、成片、字幕、封面依序做完，中間不問使用者。只有真正無法繼續時（缺金鑰、題解看不懂、工具壞掉）才停下說明。
- **長度不限**：預設講整題（主解法＋陷阱＋驗算＋總結），不為了縮短而刪內容。
- **完成後列出改動的檔案路徑**，git commit 由使用者自己做，不要替他 commit。

完整範例在 `references/example-SM-2020-3/`（土壤力學相對密度，22 段、6 章、6 分 22 秒），寫新題之前先看它的 `segments.py` 和 `scene.py`，照同樣的節奏與版面語言寫。踩過的坑與細節在 `references/lessons.md`，寫動畫前先讀第 2 節，做字幕或成片時讀第 4、5 節。

## 分工：誰在哪裡跑什麼

| 工作 | 在哪裡 | 為什麼 |
|---|---|---|
| 寫講稿、寫動畫、渲染、字幕、合成、封面 | Linux（Cowork 雲端沙箱或 WSL） | 需要 Manim、LaTeX、ffmpeg |
| 配音 | **使用者自己的 Windows**，由 Claude 透過 device_bash 直接執行（不請使用者跑 bat） | 沙箱連不到 Azure Speech；金鑰也留在使用者電腦 |

工作資料夾放在使用者電腦上，例如 `解題過程影片/<題號>/video/`。每完成一步，就把該交付的檔案寫回這個資料夾。

## 流程（全程自動，不停下等確認）

### 0. 接手或開始

- 資料夾裡如果有 `HANDOFF.md`，先讀它，從上次停下的地方接續。
- 讀題解（.md 或網頁）。題解裡已經畫好的附圖（figs/*.png）可以參考構圖。
- 範圍不用問：預設整題含陷阱與驗算，長度不限。使用者另有指定才照他說的。

### 1. 建資料夾、裝環境

```bash
bash <skill>/scripts/setup_render_env.sh                 # 首次：Manim、LaTeX、Iansui 字型
python <skill>/scripts/init_video.py <video資料夾> --id SM-2020-3 --topic 相對密度
```
`init_video.py` 會複製進去的檔案：`board_scene.py`（底座）、`segments.py`（講稿範本）、`scene.py`（動畫骨架）、`board.png`（黑板底圖）、配音／字幕／合成／封面／檢查工具、`run_tts.bat`、`env.example`。已存在的檔案不會覆蓋。

### 2. 寫講稿（不等確認，直接往下做）

改 `segments.py`，這是唯一的改稿處：
- **SEGMENTS**：逐字旁白。數字寫國字，符號寫念法（寫法規則見 lessons.md 第 1 節）。
- **CHAPTERS**：章名，會顯示在黑板左上角。
- **BOARD**：每段黑板上要出現什麼。寫具體，例如「紅字錯誤式 (500−440)/200＝30% 打叉」。
- **SUB_SYMBOLS / SUB_KEEP**：字幕端的符號轉換，以及不要轉成數字的詞。

章節骨架：題目（列出已知、點出問什麼）→ 主解法 → 每個陷阱各一章或一段（錯在哪、錯了會得到什麼數字）→ 驗算或第二解法 → 總結（條列重點加答案）。

接著跑 `python script_md.py` 產生 `講稿.md`（留在資料夾供使用者事後查看，不用等他看），再跑 `python make_srt.py --preview` 自己檢查數字轉換有沒有誤轉，有誤就修，然後直接進下一步。

### 3. 寫動畫 → 自我檢查（不出審閱版、不等回饋）

照 BOARD 寫 `scene.py`，每段的形式是 `self.begin("sXX")` → 動畫 → `self.end()`。可用的 helper（`T` 中文、`M` 公式、`row`、`xmark`、色票、`clear_board`）見 `board_scene.py` 開頭的說明。

```bash
manim -ql --disable_caching scene.py Full && python frames_grid.py   # 用 Read 看 frames_grid_*.png
```
逐張檢查有沒有重疊、出界、被虛線穿過，修到乾淨為止（常見問題見 lessons.md 第 2 節）。不用出 720p 無聲審閱版，直接進配音。這時每段長度是估計值，節奏會在配音後自動對齊。

### 4. 配音（Claude 直接在使用者的 Windows 上跑 Azure TTS）

聲音固定：Azure `zh-TW-HsiaoChenNeural`（女聲），語速預設 `+0%`。**不用 Gemini**；`run_tts.bat` 必須呼叫 `tts_azure.py`，若發現它指向 `tts_gemini.py` 就改回來。

1. 金鑰：使用者 Windows 上已設好 `AZURE_SPEECH_KEY`、`AZURE_SPEECH_REGION`（`.env` 或環境變數）。Claude 只檢查變數「是否存在」，不讀出內容；真的沒有才請使用者照 `env.example` 填。缺套件時 Claude 自己 `pip install azure-cognitiveservices-speech`。
2. **Claude 自己執行，不請使用者雙擊 bat**：用 device_bash 進到影片資料夾，執行 `run_tts.bat` 等效的指令（`python tts_azure.py`；中斷後續跑用 `run_tts_resume.bat` 等效的續跑參數）。指令較久就背景執行，用 device_bash 看 `tts_azure.log` 與 `audio/` 追進度。
3. device_bash 不可用時，才改用 computer use 開檔案總管、到影片資料夾、雙擊 `run_tts.bat`，同樣由 Claude 操作、不交給使用者（細節見 lessons.md 第 3、6 節）。
4. Azure 失敗（金鑰錯、額度、網路）時停下回報原因，不要改用 Gemini。

產出 `audio/s*.wav`（48 kHz）、`durations.json`、`tts_azure.log`。完成後確認每一段都有、都是 48 kHz、`audio/.azure_voice` 是 `zh-TW-HsiaoChenNeural`，再把 `audio/*.wav` 和 `durations.json` 搬到渲染環境。

### 5. 成片（1080p）、字幕、封面 → 直接交付

```bash
manim -qh --disable_caching scene.py Full        # 1920×1080；每段長度＝真實配音＋0.6 s，寫出 timeline.json
python make_srt.py                               # <題號>.srt（對齊語音停頓）
python make_final.py                             # <題號>.mp4（不燒字幕，約 18 MB／6 分鐘）；--burn 才燒
manim -s -r 1280,720 --format png --disable_caching thumb.py Thumb   # 封面
```
- 用 ffprobe 確認成片是 1920×1080；不是就重渲，不要降解析度交付。
- 檢查有沒有動畫比配音長：對每段確認 `timeline 長度 − (durations + 0.6) ≤ 0.1`。超過的，縮短該段動畫的 run_time。
- 封面：改 `thumb.py` 的文字區，並把 `figure()` 換成這題最有辨識度的圖（例子見 `references/example-SM-2020-3/thumb.py`）。輸出後用 Read 看一次，確認沒有出界或重疊。
- 交付：srt、thumbnail.png 寫回使用者的資料夾。
- **mp4 一律不再壓縮**：`make_final.py` 輸出的就是交付版，不要為了檔案大小再用 ffmpeg 重新編碼或調高 CRF。mp4 在 20 MB 以下就照常寫回資料夾；超過 20 MB（回寫上限，8 分鐘以上的片常見）就直接用 SendUserFile 當聊天附件給使用者下載，請他自己放進 video 資料夾，並在 HANDOFF.md 註明。聊天附件上限約 30 MB，超過時先告訴使用者，不要自行壓縮。

交付後使用者才看片驗收。之後要修改：某段念錯就改稿，Claude 自己用 device_bash 重跑該段配音（`run_tts.bat --only s07` 的等效指令），然後重跑步驟 5。字幕不準就請使用者給時間點，照 lessons.md 第 4 節調整。

### 6. 收尾回報

最後回覆列出這次新增或改動的所有檔案路徑（使用者電腦上的路徑，含 segments.py、scene.py、audio/、durations.json、mp4、srt、thumbnail.png、HANDOFF.md 等），並提醒 git commit 由使用者自己做。

### 每一步都要做的

- 更新資料夾裡的 `HANDOFF.md`：已確認的決定、目前進度、下一步、環境備註。換 session 或換人接手時就靠它。
- 不要替使用者 git commit：只寫檔，最後列出改了哪些路徑。
- 不要讀出、印出或打包 `.env` 的內容。