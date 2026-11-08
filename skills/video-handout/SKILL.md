---
name: "video-handout"
description: "把黑板講解影片（blackboard-solution-video 產出的 video/ 資料夾）轉成忠實反映影片的圖文講義 HTML＋PDF。使用者說「影片轉講義」「把解題過程影片做成講義」時使用。"
---

# 影片 → 圖文講義（video-handout）

把 exam-wiki（SS/RC/SA/SD/SM/MM）`解題過程影片/<主題>/video/` 裡的黑板講解影片，轉成**忠實反映影片內容**的圖文講義：文字取自旁白逐字稿，圖片取自影片各段結束時的完整黑板畫面。輸出單一 HTML（內嵌影片＋章節跳轉）與 A4 PDF。

**忠實原則**：不新增影片沒講的觀念、不改數字、不補推導。只做三件事：①旁白念法轉回數學符號（KaTeX）②把並列內容整理成表格／重點框 ③挑出代表性黑板畫面。

---

## ⚠️ 輸出位置（先讀這節）

`解題過程影片/` 在 `.gitignore` 裡，**不會被 push 到 GitHub Pages**。講義若只放在那裡，網站上的圖片與影片全部 404。因此：

| 東西 | 放哪 | 是否上網站 |
|---|---|:-:|
| 講義 HTML | `影片講義/<ID>_<主題名>.html` | ✅ |
| 黑板截圖 | `影片講義/img/<ID>/sNN.jpg` | ✅ |
| 影片 | `影片講義/video/<ID>.mp4`（從 `解題過程影片/<主題>/video/` **複製**，原檔不動） | ✅ |
| KaTeX | 引用既有 `study/assets/katex/` → HTML 內寫 `../study/assets/katex/` | ✅ |
| PDF | `解題過程影片/<主題>/<ID>_影片講義.pdf` | ❌（本機用） |

- `<主題名>` = 主題資料夾名去掉 `<ID>` 與空白，例如 `SS-U1-1 拉力及壓力桿件` → `SS-U1-1_拉力及壓力桿件.html`。資料夾名只有 ID（如 `SS-2005-1`）時檔名就是 `<ID>.html`。**檔名不可有空格**（URL 會變 `%20`）。
- 所有相對路徑都以 `影片講義/` 為基準：`img/<ID>/…`、`video/<ID>.mp4`、`../study/assets/katex/…`。**不可**寫 `handout/img/`、`../../study/`（那是舊版放在 `解題過程影片/<主題>/` 時的路徑，搬到 `影片講義/` 後全部失效）。
- 單支 mp4 必須 < 100 MB（GitHub 單檔上限）；超過就停下來告訴使用者，不要 push 不上去才發現。

## 0. 輸入盤點

使用者通常給 `...\解題過程影片\<主題>` 路徑（在使用者電腦上 → 用 device_bash，掛載於 `$HOME/mnt/<資料夾>/`）。先列出 `video/`：

| 檔案 | 用途 | 必要 |
|---|---|---|
| `<ID>.mp4` | 截圖來源 | ✅ |
| `segments.py` | `CHAPTERS`（章節→段落）、`SEGMENTS`（逐字旁白）、`SUB_SYMBOLS`（念法→符號） | ✅ 權威講稿 |
| `講稿.md` | 同上的易讀版，含每段「🖍 黑板」描述——寫圖說時很好用 | 建議 |
| `durations.json` | 各段配音秒數 | ✅ 用來切段 |
| `<ID>.srt` | 實際字幕時間軸 | ✅ 用來切段 |
| `HANDOFF.md` | 例題已複算的數值 | 參考 |

若講稿.md 與 segments.py 不一致，以 segments.py 為準（配音念的就是它）。

## 1. 求各段起訖時間（device_bash 執行）

timeline.json 通常不在使用者端，用「SRT 起點 + durations 下限」對位：第 k 段起點＝第一個起點 ≥ 前段起點＋前段配音長 − 0.3 s 的字幕。

```python
# tl.py — 在 video/ 目錄執行；輸出 /tmp/tl.json
import json, glob, subprocess
d = json.load(open('durations.json'))
srt = open(glob.glob('*.srt')[0], encoding='utf-8').read().strip().split('\n\n')
def t(s):
    h, m, r = s.split(':'); sec, ms = r.split(','); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
ents = []
for b in srt:
    L = b.split('\n'); a, e = L[1].split(' --> '); ents.append((t(a), t(e), ''.join(L[2:])))
keys = sorted(d)
starts, idx = [ents[0][0]], [0]
for k in range(1, len(keys)):
    lim = starts[-1] + d[keys[k-1]] - 0.3
    j = next(i for i, x in enumerate(ents) if x[0] >= lim and i > idx[-1])
    starts.append(ents[j][0]); idx.append(j)
vdur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',
                             glob.glob('*.mp4')[0]], capture_output=True, text=True).stdout)
out = {}
for k, key in enumerate(keys):
    end = starts[k+1] if k+1 < len(keys) else vdur - 0.3
    subs = [x[2] for x in ents[idx[k]:(idx[k+1] if k+1 < len(keys) else len(ents))]]
    out[key] = dict(start=starts[k], end=end, subs=subs)
    print(key, round(starts[k], 2), round(end, 2), subs[0], '…', subs[-1])
json.dump(out, open('/tmp/tl.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
```

**檢查**：印出的每段首句／末句要和 segments.py 該段開頭／結尾對得上；對不上就是切錯段，先修再往下。

## 2. 截取每段結束畫面＋複製影片

每段取「下一段開始前 0.5 s」——此時該段黑板已寫完、下一段還沒清板。截圖直接輸出到 `影片講義/img/<ID>/`。

```bash
# 在知識庫根目錄執行（影片講義/ 與 解題過程影片/ 的上一層）
ID=SS-U1-1; SRC="解題過程影片/SS-U1-1 拉力及壓力桿件"
mkdir -p "影片講義/img/$ID" 影片講義/video
cp "$SRC/video/$ID.mp4" 影片講義/video/
ls -l "影片講義/video/$ID.mp4"   # 確認 < 100 MB
ID="$ID" SRC="$SRC" python3 - <<'EOF'
import json, subprocess, os
tl = json.load(open('/tmp/tl.json'))
ID, SRC = os.environ['ID'], os.environ['SRC']
mp4 = f'{SRC}/video/{ID}.mp4'
for k, v in tl.items():
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{v['end']-0.5:.2f}",'-i',mp4,'-frames:v','1',
                    '-vf','scale=1600:-2','-q:v','3',f'影片講義/img/{ID}/{k}.jpg'], check=True)
EOF
```

## 3. 目視檢查並挑圖

用 device_stage_files 把全部 jpg 拉進雲端，以 PIL 拼 2×2 聯絡表（4 張一頁）再用 Read 看圖。每張都要看——同時把黑板上的字、公式抄下來，寫正文時對照。

**挑圖規則（去重）**：
- 同一塊黑板跨多段逐步疊加 → 只留**最完整的那一張**（通常是清板前最後一段）。
- 後段把前段某些元素擦掉／換掉（例如塗色區、旁註消失）→ 兩張都留。
- 每章至少一張；題目圖、陷阱圖、總結圖必留。
- 一般 26 段影片 → 約 14–18 張。未使用的 jpg 可留著（使用者端刪檔需權限，別硬刪），交付時說明哪些有用到。

## 4. 寫講義 HTML

存成 `影片講義/<ID>_<主題名>.html`。圖片 `img/<ID>/sNN.jpg`，影片 `video/<ID>.mp4`，KaTeX `../study/assets/katex/`（路徑規則見最上方「輸出位置」）。

**結構**：
1. 封面：科目／命題大綱代碼／「影片講義」、標題、影片長度・章數・段數、核心一句話（深色黑板風色塊）。
2. 目錄：章名＋起始時間（取該章第一段 start）。
3. 內嵌 `<video controls preload="metadata">`；每章標題旁放 `<button class="seek" data-t="秒">▶ m:ss</button>`，點擊設定 currentTime 並播放。
4. 每章 `<section>`：依段落順序交錯放「黑板圖（figure＋figcaption：左邊說明、右邊『影片 m:ss』＝截圖時間）」與「旁白整理文字」。
5. 頁尾註明來源（mp4、segments.py、srt）。

**文字轉寫規則**：
- 旁白幾乎逐字保留，只刪口語贅字；念法用 `SUB_SYMBOLS` 反轉回符號，公式改寫成 KaTeX（`\\( \\)` 行內、`$$ $$` 獨立）。
- 黑板上有、旁白也講的公式 → 用獨立公式區塊呈現；並列的狀態／對照 → 表格。
- 「最常見的錯／陷阱」→ 紅框 `.warn`；「檢查／驗證」→ 綠框 `.ok`；「重點／不用背」→ 黃框 `.key`。
- 黑板用色有語意（例：粉紅=近端、綠=遠端、藍=弦）時，HTML 公式用 `\\color{}` 對應同色，並註明對應關係。
- 例題數值寫進前，對照 HANDOFF.md 或自行複算一次；不一致要停下來告訴使用者，不可自行改。

**KaTeX**：引用知識庫既有資產 `study/assets/katex/`（katex.min.css、katex.min.js、auto-render.min.js），HTML 在 `影片講義/` 下，所以寫 `../study/assets/katex/`；不要用 CDN。
已知坑：`\\text{kN·m}` 裡的「·」會報錯 → 寫 `\\text{kN}\\cdot\\text{m}`。

**樣式要點**：米白紙底、深綠黑板色當主色；`max-width:860px`；表格第一欄 `white-space:nowrap`（避免「② 近端轉 1」斷行）；`@media print`：A4、隱藏 video 與 seek 按鈕、figure／提示框 `break-inside:avoid`；手機寬度目錄改單欄。

## 5. 驗證與輸出 PDF（雲端容器）

在容器建出與使用者端**相同的相對結構**再渲染——結構不同就驗不出路徑錯誤：

```
build/study/assets/katex/        ← npm i katex 後複製 dist/katex.min.css、katex.min.js、fonts/、contrib/auto-render.min.js
build/影片講義/<ID>_<主題名>.html
build/影片講義/img/<ID>/*.jpg     ← 從 staged uploads 複製
```

Playwright：容器內建 chromium 版本要配合 npm 套件版本（例：`/opt/pw-browsers/chromium-1194` ↔ `playwright@1.56.0`）。版本不合會出現「Executable doesn't exist」或「Old Headless mode has been removed」——換 npm 版本，不要 `playwright install`。

```js
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:1200}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
console.log('katex errors',await p.evaluate(()=>document.querySelectorAll('.katex-error').length));
console.log('katex loaded',await p.evaluate(()=>typeof katex!=='undefined'));
console.log('broken imgs',await p.evaluate(()=>[...document.images].filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src'))));
await p.screenshot({path:'shot.png',fullPage:true});
await p.pdf({path:'out.pdf',format:'A4',printBackground:true,margin:{top:'14mm',bottom:'16mm',left:'14mm',right:'14mm'}});
await b.close();})();
```

（檔名含中文時 `file://` 路徑要 `encodeURIComponent` 檔名部分。）

**必過檢查**：
- `katex loaded true`、`katex errors 0`、`broken imgs []`；
- 使用者端再跑一次路徑對帳：HTML 內每個 `src=`／`href=` 指向的檔案都存在於 `影片講義/` 底下，且沒有任何 `handout/` 或 `../../` 字樣；
- `git check-ignore` 確認 HTML、`img/<ID>/`、`video/<ID>.mp4` 都**沒有**被 ignore；
- 全頁截圖切成 900×2400 小段逐段看：公式、表格、圖說無破版；
- PDF 用 `pdftoppm -r 50` 看前幾頁，確認分頁沒有把圖切半。

## 6. 交付

- HTML 寫到 `影片講義/`，PDF 用 device_commit_files 寫回 `解題過程影片/<主題>/`。
- 用 SendUserFile 傳 PDF（display: render）。
- **不要 git commit**：列出所有新增／變更路徑交給使用者自己 commit：`影片講義/<ID>_<主題名>.html`、`影片講義/img/<ID>/`、`影片講義/video/<ID>.mp4`。
- 提醒：push 後若網站仍顯示舊版（圖不出來但影片能播），是瀏覽器快取舊 HTML → Ctrl+F5。
- 不改 `raw/`、不動 `解題過程影片/<主題>/video/` 內任何檔案、不改 wiki/ compile 輸出。

## 回報格式（簡短）

一句說明講義涵蓋範圍（幾章、幾張黑板圖、例題數值已核對）＋檔案位置＋待 commit 路徑清單；有未使用截圖要說明。