---
name: "exam-practice-sheet"
description: "exam-wiki 五科（SS/RC/SD/SM/SA）由考卷原檔產生限時練習試卷 PDF：單題、單元選題或整年模擬考，附原卷參考公式與作答紙。說「出一份 XX-YYYY-N 練習卷」「模擬考」「限時練習」時使用。"
---

# 限時練習試卷（exam-practice-sheet）

把歷屆考題做成「考場等級」的練習卷：題目、題內公式、附圖、全卷共用參考公式都是**考卷原件影本**，後面接印有題號頁碼的作答紙。使用者寫完拍照上傳，再進入批改。

適用知識庫：structural-exam-wiki（github.com/yjc5760/structural-exam-wiki）的科目資料夾 `SS/`、`RC/`、`SA/`、`SD/`、`SM/`。題號格式 `XX-YYYY-N`，前兩碼決定科目資料夾。
（尚未搬入 structural-exam-wiki 的科目，暫用原 repo `exam-wiki-<xx>`，`--root` 指向該 repo 根目錄。）

**本 skill 自帶產生器（見文末「產生器原始碼」），不依賴任何 repo 內的腳本**：執行時把它寫到暫存目錄，用 `--root` 指向要出題的那一科。各 repo 不需要也不應該再放一份。

## 核心原則（不可違反）

1. **只放考場上看得到的東西。** 題目正本的 §4 判讀清單、§2 的編者說明（「沒有給 φ」「與本題相關者」「疑為…」）、解析 `XX-YYYY-N.md`、題解圖 `figs/` 一律不進試卷——它們都是解法線索。
2. **共用參考公式整區照印。** 不可只印「與本題相關者」或用 `-eqn-*.png` 局部截圖代替：挑出該用哪條公式本身就是考點。
3. **不在試卷上加提示。** 不加單元名稱、考點標籤、難度。

## 產生器做的事

- 依題號找考卷 `raw/exams/XX-YYYY_*.pdf`；有題目正本 `raw/solutions/<id>/<id>-problem.md` 就用它的考卷路徑、題號、配分，沒有就由題號推（第 N 題），配分由考卷題文「（N 分）」「共 N 分」判讀。
- 題首偵測三段式：「一、」文字 → 只剩「、」的缺字行（SA-2011 第三題）→ 左邊界小圖（2020 年各科題號是圖片）；缺號時依位置重新編號。考卷相容漢字（如 U+F96B「參」）先 NFKC 正規化。
- 切出：卷首注意事項、本題（題首到下一題題首，可跨頁，題內公式附表附圖都在）、全卷共用參考公式區（※參考公式／◎參考公式集／＊參考資料／「請自行選擇…」）。
- 退路：切不出題目而有題目正本 → 用 §1 原文＋考卷原圖排版；掃描檔又無題目正本（目前只有 RC-2003）→ 附整份考卷影本並註明只作答本題。兩種情況都會印 `⚠`。
- 建議時間 = 配分 × 1.2 分鐘（考試 2 小時／100 分）。
- 題目正本格式（給之後補 RC／SD／SM 正本時對照）：表頭 `| 考卷 |` 列含反引號包住的 PDF 路徑與「第X題」；`| 配分 |` 列以數字開頭；§1 原文放引用區塊；§3 原圖檔名 `<id>-fig-N.png`；§2 若有共用公式頁截圖，alt 文字寫「第 N 頁…公式／資料」以便被略過。與 exam-problem-split 產出一致。

## 流程

### 1. 準備（每個 session 一次）

```bash
# 知識庫（公開，唯讀 clone 即可；使用者電腦已連線時也可直接用本機資料夾）
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/yjc5760/structural-exam-wiki
# 之後 --root 指向科目資料夾，如 structural-exam-wiki/RC
pip install --break-system-packages markdown pymupdf playwright
mkdir -p /tmp/katexdl && cd /tmp/katexdl && npm init -y >/dev/null && npm i katex@0.16
export KATEX_DIR=/tmp/katexdl/node_modules/katex
export CHROME=$(which google-chrome chromium chromium-browser 2>/dev/null | head -1)
```
CDN 連不到，所以 KaTeX 一定要用本機套件；沒有 Chromium 就 `playwright install chromium`。

把文末「產生器原始碼」一字不改地用 Write 寫到 `/tmp/exam-practice-sheet/make_practice_sheet.py`（不要寫進 repo）。

### 2. 決定題目

| 使用者說 | 做法 |
|---|---|
| 指定題號「SS-2019-2」 | 直接用 |
| 「2021 年 SD 模擬考」 | 該年全部題號（看 `raw/solutions/` 或 `raw/json/question_index.json`），`--name mock-SD-2021` |
| 「RC-U2-1 給我兩題」 | 讀 `raw/json/question_index.json` 的 `questions`，篩 `primaryTopicId`（必要時含 `secondaryTopicIds`），優先近年、`hasSolution: true`（批改要有題解可對）；**選題理由不寫在試卷上**，回覆也只說題號，不說考點 |
| 「隨便出一題」 | 依出題頻率高的單元挑；避開這次對話已練過的題 |

題號模糊（只說「鋼構那題合成梁」）時先問，不要猜。

### 3. 產生

```bash
G=/tmp/exam-practice-sheet/make_practice_sheet.py
python3 $G RC-2019-2 --root structural-exam-wiki/RC                          # 單題
python3 $G SD-2021-1 SD-2021-2 SD-2021-3 SD-2021-4 --name mock-SD-2021 --root structural-exam-wiki/SD
python3 $G SM-2019-3 --pages 3 --root structural-exam-wiki/SM               # 作答紙張數（預設每題 2 張）
```
輸出在該 repo 的 `study/practice/<名稱>-practice.html`、`.pdf`。

### 4. 檢查（每份都要做）

```bash
pdftoppm -r 45 -png <repo>/study/practice/<名稱>-practice.pdf /tmp/pv
```
用 Read 看題目頁與參考公式頁，確認：題目從題首開始、沒切掉第一行、沒混入下一題，跨頁題後半有接上；圖、表、題內公式完整；該卷有共用參考公式時那一頁有出現且是整區；題頭沒有孤立在頁尾；表頭配分合理（顯示「考卷未判讀到」時，用題目正本或考卷目視確認後告訴使用者實際配分）。

有 `⚠` 或切錯：先看是不是新的考卷版式，修 skill 內的產生器原始碼（改完用 propose_skills 更新本 skill），重跑；不要手工拼圖了事。

### 5. 交付

- 用 SendUserFile 送 PDF（display: attach），一行說明：題號、配分、建議時間。不描述題目內容或考點。
- 提醒：寫完拍照（一頁一張、正面、光線均勻），附實際用時上傳。
- **不要 git commit／push。** 列出新增的 `study/practice/*` 路徑，交給使用者自己決定要不要 commit。

## 之後：批改上傳的手寫答案

1. 先列出從照片讀到的關鍵數值、假設與最終答案，請使用者確認讀對了（手寫 φ、ψ、λ、下標最常認錯）。
2. 確認後再對照 `XX-YYYY-N.md` 題解與規範，用程式獨立驗算數字。
3. 錯誤分類：觀念、規範條文／係數、計算、單位、漏檢核、表達（圖、假設、條文引用不清，影響部分給分）。
4. 依使用者要求決定先只指錯讓他自己訂正，還是直接給完整對照。
5. 若題解本身疑似有錯，改走 exam-errata，不要在批改中順手改題解。

## 已知狀況

- RC-2003 是掃描檔且 RC 尚無題目正本 → 只能附整份考卷；補上正本後自動改為單題排版。
- 2020 年各科題號在文字層是圖片，已由左邊界小圖偵測處理。
- 少數考卷文字層把括號拆到別行，配分以題目正本為準；SS-2004、SS-2016 的考卷判讀總分不足 100，但 SS 有題目正本，不受影響。

## 產生器原始碼

寫到 `/tmp/exam-practice-sheet/make_practice_sheet.py`，內容如下（一字不改）：

````python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""限時練習試卷產生器（exam-wiki 各科共用：SS／RC／SD／SM／SA／MM）

輸出 study/practice/<名稱>-practice.html ＋ .pdf。本檔不綁定任何一科：skill 執行時寫到暫存目錄，對哪個 repo 用 --root 指定（或在該 repo 根目錄執行）。

用法（在該科 repo 根目錄執行，或加 --root <repo>）：
  python make_practice_sheet.py RC-2019-2                 # 單題
  python make_practice_sheet.py RC-2019-2 --pages 3       # 作答紙 3 張（預設每題 2 張）
  python make_practice_sheet.py SD-2021-1 SD-2021-2 SD-2021-3 SD-2021-4 --name mock-SD-2021
  python make_practice_sheet.py SS-2019-2 --typeset       # 有題目正本時改用 §1 排版
  python make_practice_sheet.py SS-2019-2 --no-pdf

試卷＝考生在考場上看得到、且與本題有關的東西，全部取自考卷原檔 raw/exams/XX-YYYY_*.pdf：
  1. 卷首：第 1 頁抬頭與注意事項
  2. 本題：從「X、」題首切到下一題題首（可跨頁），題內公式、附表、附圖一併在內
  3. 全卷共用參考公式區（※參考公式／◎參考公式集／＊參考資料…）：整區照印，不只印「相關者」
  不取題目正本的判讀清單與編者說明，不洩漏解法線索。
題目正本 raw/solutions/<id>/<id>-problem.md 可有可無：有就用它的考卷路徑、題號、配分；沒有就由題號推
（XX-YYYY-N → 第 N 題），配分由考卷題文「（N 分）」「共 N 分」判讀。
題首偵測：「一、」文字 → 只剩「、」的缺字行 → 左邊界小圖（2020 年各科題號是圖片）；有缺號時依位置重新編號。
退路：切不出題目時用題目正本 §1 排版；掃描檔又沒有題目正本時附整份考卷影本並註明只作答本題。
建議時間：依考試 2 小時／100 分換算，每 1 分 1.2 分鐘。
需要：pip install markdown pymupdf playwright；PDF 用 Chromium 列印，KaTeX 由 KATEX_DIR 指定本機 katex 套件
（npm i katex），Chromium 執行檔可用 CHROME 指定。
"""
import argparse, base64, html, os, re, sys, unicodedata
from pathlib import Path
import markdown
import pymupdf

def _root(p=None):
    """知識庫根目錄：--root ＞ 目前目錄（有 raw/exams）＞ 腳本所在 repo"""
    for c in ([Path(p)] if p else []) + [Path.cwd(), Path(__file__).resolve().parent.parent]:
        if (c / "raw/exams").is_dir():
            return c.resolve()
    sys.exit("找不到知識庫根目錄（需含 raw/exams/），請在 exam-wiki-XX 根目錄執行或加 --root")


ROOT = SOL = OUT = None


def set_root(p=None):
    global ROOT, SOL, OUT
    ROOT = _root(p)
    SOL, OUT = ROOT / "raw/solutions", ROOT / "study/practice"
KATEX_CDN = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
SUBJECT = {"SS": "鋼結構設計", "RC": "鋼筋混凝土設計與預力", "SA": "結構學",
           "SD": "結構動力分析與耐震設計", "SM": "土壤力學與基礎設計", "MM": "材料力學"}  # 以考卷檔名為準，此表僅備用
NUM = "一二三四五六七八"
RE_MARK = re.compile(rf"^([{NUM}])\s*[、，.]")
RE_SHARED = re.compile(r"(參考公式|公式集|參考資料)")
RE_SHARED_OK = re.compile(r"請自行|公式集|^[＊*※◎]\s*參考資料")
RE_HEADER = re.compile(r"代號|頁次|第.頁|全.頁|共.頁|^\s*全\s*$|等\s*別|類\s*科|科\s*目|座\s*號|考試時間")
ZOOM = 2.6


# ───────────────────────── 題目正本 ─────────────────────────
def section(text, n):
    m = re.search(rf"^## {n}\..*?$(.*?)(?=^## \d+\.|^---\s*$|\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


def meta(text, key):
    m = re.search(rf"^\|\s*{key}\s*\|\s*(.+?)\s*\|\s*$", text, flags=re.M)
    return m.group(1) if m else ""


def md_html(src):
    store = []

    def keep(m):
        store.append(m.group(0))
        return f"\u0000M{len(store) - 1}\u0000"

    src = re.sub(r"\$\$.+?\$\$", keep, src, flags=re.S)
    src = re.sub(r"(?<![\\$])\$(?!\$)[^\n$]+?\$", keep, src)
    src = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", src)
    out = markdown.markdown(src, extensions=["tables", "nl2br"])
    return re.sub("\u0000M(\\d+)\u0000", lambda m: html.escape(store[int(m.group(1))], quote=False), out)


def b64img(data, cls):
    return f'<img class="{cls}" src="data:image/png;base64,{base64.b64encode(data).decode()}" alt="">'


# ───────────────────────── 考卷原檔 ─────────────────────────
class Exam:
    def __init__(self, pdf):
        self.doc = pymupdf.open(pdf)
        self.shared = []   # (page, y) 共用參考公式區起點
        self.text = {}     # (page, y) → 行文字（配分判讀用）
        self.scanned = all(not pg.get_text().strip() for pg in self.doc)
        named, anon = {}, []
        for i, pg in enumerate(self.doc):
            for b in pg.get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    # 考卷常用相容漢字（如 U+F96B 參），先正規化
                    t = unicodedata.normalize("NFKC", "".join(s["text"] for s in l["spans"])).strip()
                    x, y = l["bbox"][0], l["bbox"][1]
                    m = RE_MARK.match(t)
                    if m and m.group(1) not in named:
                        named[m.group(1)] = (i, y)
                    elif re.match(r"^[、，]\s*\S", t) and x < 90:      # 題號字遺失、只剩頓號（SA-2011 第三題）
                        anon.append((i, y))
                    elif RE_SHARED.search(t) and RE_SHARED_OK.search(t) and "在第" not in t:
                        self.shared.append((i, y))
            if not named:   # 題號是小圖片（2020 年各科考卷）：左邊界、題文前的小圖
                for im in pg.get_image_info():
                    r = pymupdf.Rect(im["bbox"])
                    if r.x0 < 62 and 10 < r.width < 40 and r.height < 20 and (i > 0 or r.y0 > pg.rect.height * .2):
                        anon.append((i, r.y0 + r.height / 2 - 10))   # 「一」只有一橫，取圖中心往上半行
        ks = [c for c in NUM if c in named]
        if anon or ks != list(NUM[:len(ks)]):
            # 有缺號：依位置重新編號
            pos = sorted(set(list(named.values()) + anon))
            pos = [p for k, p in enumerate(pos) if k == 0 or not (p[0] == pos[k - 1][0] and abs(p[1] - pos[k - 1][1]) < 4)]
            self.marks = {NUM[k]: p for k, p in enumerate(pos[:len(NUM)])}
        else:
            self.marks = named
        self.stops = sorted(list(self.marks.values()) + self.shared)

    def block_text(self, ch):
        """本題文字（判讀配分用）：逐行取，去掉重複描字（部分考卷粗體是同一行印兩次）"""
        if ch not in self.marks:
            return ""
        s = self.marks[ch]
        nxt = [m for m in self.stops if m > s]
        e = min(nxt) if nxt else (len(self.doc), 0)
        out = []
        for i in range(s[0], min(e[0], len(self.doc) - 1) + 1):
            for b in self.doc[i].get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    if (s[0], s[1] - 3) <= (i, l["bbox"][1]) < e:
                        t = unicodedata.normalize("NFKC", "".join(x["text"] for x in l["spans"]))
                        if t not in out:
                            out.append(t)
        return re.sub(r"\s+", "", "".join(out))

    def content_box(self, i):
        pg = self.doc[i]
        rects = [pymupdf.Rect(b[:4]) for b in pg.get_text("blocks")]
        rects += [d["rect"] for d in pg.get_drawings() if d["rect"].height < pg.rect.height * .9]
        rects += [pymupdf.Rect(im["bbox"]) for im in pg.get_image_info()]
        rects = [r for r in rects if r.is_valid and not r.is_empty]
        top = 0
        for b in pg.get_text("blocks"):   # 跳過頁首（代號、頁次）
            if b[1] < pg.rect.height * .25 and RE_HEADER.search(unicodedata.normalize("NFKC", b[4])):
                top = max(top, b[3])
        body = [r for r in rects if r.y0 >= top - 1]
        y0 = min((r.y0 for r in body), default=top)
        y1 = max((r.y1 for r in body), default=pg.rect.height)
        return y0, y1

    def next_stop(self, start):
        later = [s for s in self.stops if s > start]
        return later[0] if later else (len(self.doc) - 1, float("inf"))

    def region(self, start, end):
        """(page,y) → (page,y) 之間的影像（逐頁切）"""
        imgs = []
        for i in range(start[0], min(end[0], len(self.doc) - 1) + 1):
            c0, c1 = self.content_box(i)
            y0 = start[1] - 5 if i == start[0] else c0 - 4
            y1 = end[1] - 6 if i == end[0] else c1 + 6
            y1 = min(y1, c1 + 6)
            if y1 - y0 < 12:
                continue
            pg = self.doc[i]
            clip = pymupdf.Rect(0, max(0, y0), pg.rect.width, min(pg.rect.height, y1))
            imgs.append(pg.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), clip=clip).tobytes("png"))
        return imgs

    def cover(self):
        """第 1 頁抬頭＋注意事項：切到第一題題首；題首抓不到時切到注意事項最後一行"""
        if self.scanned:
            return []
        first = [s for s in self.stops if s[0] == 0]
        if first:
            return self.region((0, 0), min(first))
        ys = [b[3] for b in self.doc[0].get_text("blocks")
              if re.search(r"注意|計算器|抄題|本國文字|參考資料在第|座\s*號", unicodedata.normalize("NFKC", b[4]))]
        return self.region((0, 0), (0, max(ys) + 12)) if ys else []

    def question(self, ch):
        if ch not in self.marks:
            return None, None
        s = self.marks[ch]
        nxt = [m for m in self.marks.values() if m > s]
        end = min(nxt) if nxt else (len(self.doc) - 1, float("inf"))
        inside = [x for x in self.shared if s < x < end]
        # 題內若有共用公式區（如 SS-2023 第二題下方），題目只切到它之前，公式區另列
        cut = min(inside) if inside else end
        return self.region(s, cut), inside

    def all_pages(self):
        return [pg.get_pixmap(matrix=pymupdf.Matrix(2, 2)).tobytes("png") for pg in self.doc]

    def shared_regions(self):
        return [(s, self.region(s, self.next_stop(s))) for s in self.shared]


# ───────────────────────── 組卷 ─────────────────────────
def find_pdf(qid):
    subj, year = qid.split("-")[:2]
    c = sorted((ROOT / "raw/exams").glob(f"{subj}-{year}_*.pdf"))
    return c[0] if c else None


def points(text):
    """由題文判讀配分：「共 N 分」優先；否則取括號分數，總分＝最大值（若等於其餘之和）或總和"""
    text = re.sub(r"\s+", "", text)
    m = re.search(r"共(\d+)分", text)
    if m:
        return int(m.group(1)), f"{m.group(1)} 分"
    # 文字層常把括號拆到別行，左右括號有一邊就算
    v = [int(a or b) for a, b in re.findall(r"[（(](\d+)分|(?<![\d（(])(\d+)分[）)]", text)]
    if not v:
        return 25, "25 分（考卷未判讀到，暫以 25 計）"
    if len(v) == 1:
        return v[0], f"{v[0]} 分"
    big = max(v)
    if v.count(big) == 1 and big == sum(v) - big:
        return big, f"{big} 分"
    return sum(v), f"{sum(v)} 分（" + "、".join(map(str, v)) + "）"


def problem_info(qid):
    """題目正本可有可無：有就讀考卷路徑、題號、配分；沒有就由題號推（XX-YYYY-N → 第 N 題）"""
    p = SOL / qid / f"{qid}-problem.md"
    t = p.read_text(encoding="utf-8") if p.exists() else ""
    k = meta(t, "考卷") if t else ""
    pdf = re.search(r"`([^`]+\.pdf)`", k)
    pdf = ROOT / pdf.group(1) if pdf else find_pdf(qid)
    ch = re.search(rf"第([{NUM}])題", k)
    ch = ch.group(1) if ch else NUM[int(qid.split("-")[2]) - 1]
    pts_raw = meta(t, "配分") if t else ""
    pts = int(re.match(r"\d+", pts_raw).group()) if re.match(r"\d+", pts_raw) else None
    return t, pdf, ch, pts, pts_raw


def typeset_question(qid, t):
    d = SOL / qid
    lines = [re.sub(r"^>\s?", "", ln) for ln in section(t, 1).splitlines() if ln.startswith(">")]
    body = re.sub(r"\n*參考公式與圖表[:：]\s*（見 §2）\s*$", "\n\n參考公式與圖表：", "\n".join(lines).strip())
    parts = [f'<div class="qtext">{md_html(body)}</div>']
    # 題內公式截圖；只截「與本題相關者」的共用公式頁截圖不取（改印整區）
    eqns = [d / f for alt, f in re.findall(r"!\[([^\]]*)\]\(([^)\s]+-eqn-\d+\.png)\)", section(t, 2))
            if not re.search(r"第 ?\d+ ?頁.*(公式|資料)", alt) or "所引" in alt]
    eqns = [e for e in eqns if e.exists()]
    figs = [d / f for f in re.findall(r"!\[[^\]]*\]\(([^)\s]+\.png)\)", section(t, 3)) if "-fig-" in f]
    figs = [f for f in figs if f.exists()]
    if eqns:
        parts.append('<div class="figs">' + "".join(b64img(e.read_bytes(), "eqn") for e in eqns) + "</div>")
    if figs:
        parts.append('<div class="figs">' + "".join(b64img(f.read_bytes(), "fig") for f in figs) + "</div>")
    return "\n".join(parts)


def build(ids, name, pages, force_typeset):
    exams, covers, refs, qs, notes = {}, [], [], [], []
    for qid in ids:
        t, pdf, ch, pts, pts_raw = problem_info(qid)
        ex = None
        if pdf and pdf.exists():
            ex = exams.get(pdf) or exams.setdefault(pdf, Exam(pdf))
            if pdf not in [c[0] for c in covers]:
                covers.append((pdf, ex.cover()))
        if pts is None:
            pts, pts_raw = points(ex.block_text(ch)) if ex else (25, "25 分")
        imgs, inside = (ex.question(ch) if ex and ch and not force_typeset else (None, None))
        # 跨頁連續題（如 SS-2003-4 題文接在共用頁之後）以外，題內 eqn 截圖若存在而原卷切不到，退回排版
        if imgs:
            q_html = "".join(b64img(b, "crop") for b in imgs[1:])
            first = b64img(imgs[0], "crop")
            src = "原卷影本"
        elif t:
            q_html, first = typeset_question(qid, t), ""
            src = "題目正本排版（考卷題首抓不到）" if not force_typeset else "題目正本排版"
            if not force_typeset:
                notes.append(f"{qid}：考卷文字層抓不到題首，題目改用題目正本排版")
        elif ex:   # 掃描檔、又沒有題目正本：整份考卷照印，請考生只作答本題
            q_html = "".join(b64img(b, "crop") for b in ex.all_pages())
            first, src = "", f"整份考卷影本（掃描檔切不出單題），請只作答第{ch}題"
            notes.append(f"{qid}：考卷為掃描檔且無題目正本，附整份考卷，只作答第{ch}題")
        else:
            sys.exit(f"{qid}：找不到考卷 PDF（raw/exams/{qid[:7]}_*.pdf）也沒有題目正本")
        qs.append((qid, pts, pts_raw, first, q_html, src))
        if ex:
            for s, rimgs in ex.shared_regions():
                key = (pdf, s)
                if key not in [r[0] for r in refs] and rimgs:
                    refs.append((key, rimgs))
    total = sum(q[1] for q in qs)
    minutes = round(total * 1.2)
    pdf0 = problem_info(ids[0])[1]
    subj = pdf0.stem.split("_", 1)[1] if pdf0 and "_" in pdf0.stem else SUBJECT.get(ids[0].split("-")[0], "")
    label = "、".join(ids) if len(ids) <= 4 else f"{ids[0]} 等 {len(ids)} 題"
    head = f"""<div class="head"><h1>結構技師 {subj}・限時練習</h1>
<table><tr><td>題目：{label}</td><td>總分：{total} 分</td><td>建議時間：<b>{minutes} 分鐘</b></td></tr>
<tr><td>開始：<span class="blank"></span></td><td>結束：<span class="blank"></span></td><td>實際用時：<span class="blank"></span> 分</td></tr></table>
<div class="notice">比照考場：不看講義與題解，可用計算器，詳列計算過程與單位。題目與參考公式皆為考卷原件影本；
參考公式照考場整區附上，請自行判斷適用者。寫完拍照（一頁一張、正面、光線均勻），連同實際用時上傳批改。</div></div>"""
    out = [head]
    for pdf, imgs in covers:
        if imgs:
            out.append('<div class="sec">卷首（原卷）</div>' + "".join(b64img(b, "crop cover") for b in imgs))
    for qid, pts, pts_raw, first, q_html, src in qs:   # 題頭與第一張影本綁在一起，避免題頭孤立在頁尾
        out.append(f'<div class="q"><div class="keep"><div class="sec">【{qid}】配分 {html.escape(pts_raw or f"{pts} 分")}'
                   f'<span class="src">{src}</span></div>{first}</div>{q_html}</div>')
    if refs:
        out.append('<div class="refs"><div class="sec">考卷附參考公式／參考資料（原卷影本，全區照印）</div>'
                   + "".join("".join(b64img(b, "crop") for b in r) for _, r in refs) + "</div>")
    tag = ids[0] if len(ids) == 1 else name
    for i in range(1, pages + 1):
        out.append(f'<div class="sheet"><div class="bar"><span>作答紙　題號：{"＿＿＿＿" if len(ids) > 1 else tag}</span>'
                   f'<span>{tag}　第 {i}／{pages} 頁</span></div><div class="grid"></div></div>')
    page = f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>{html.escape(name)} 限時練習</title>
<link rel="stylesheet" href="{KATEX_CDN}/katex.min.css">
<script defer src="{KATEX_CDN}/katex.min.js"></script>
<script defer src="{KATEX_CDN}/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}});document.body.dataset.ready=1"></script>
<style>{CSS}</style></head><body>
{''.join(out)}
</body></html>"""
    return page, notes


CSS = """
@page { size: A4; margin: 14mm 14mm 12mm; }
* { box-sizing: border-box; }
body { font-family: "Noto Serif CJK TC", "Noto Serif TC", serif; font-size: 11.5pt; line-height: 1.75;
       color: #111; max-width: 182mm; margin: 0 auto; }
.head { border: 2px solid #111; padding: 8px 14px; margin-bottom: 10px; }
.head h1 { font-size: 15pt; margin: 0 0 4px; letter-spacing: .1em; text-align: center; }
.head table { width: 100%; border-collapse: collapse; font-size: 10.5pt; }
.head td { padding: 2px 4px; }
.blank { display: inline-block; min-width: 24mm; border-bottom: 1px solid #111; }
.notice { font-size: 9.5pt; color: #333; border-top: 1px dashed #999; margin-top: 6px; padding-top: 4px; }
.sec { font-size: 10.5pt; font-weight: 700; color: #333; border-left: 4px solid #555; padding-left: 8px; margin: 10px 0 4px; }
.sec .src { font-weight: 400; color: #888; font-size: 9pt; margin-left: 10px; }
.keep { break-inside: avoid; page-break-inside: avoid; }
img.crop { display: block; width: 100%; page-break-inside: avoid; }
img.cover { width: 82%; margin: 0 auto; opacity: .9; }
.refs { page-break-before: always; }
.qtext p { margin: .3em 0; }
.figs { text-align: center; margin: 10px 0; page-break-inside: avoid; }
img.fig { max-width: 82%; max-height: 105mm; margin: 4px; }
img.eqn { max-width: 100%; margin: 4px 0; }
.sheet { page-break-before: always; height: 268mm; display: flex; flex-direction: column; }
.sheet .bar { display: flex; justify-content: space-between; font-size: 9.5pt;
              border-bottom: 1.5px solid #111; padding-bottom: 3px; margin-bottom: 2px; }
.sheet .grid { flex: 1; background-image: linear-gradient(#cfd8dc 1px, transparent 1px);
               background-size: 100% 8mm; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
@media screen { body { padding: 20px; } .sheet { display: none; } }
"""


def to_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    kdir = Path(os.environ.get("KATEX_DIR", "node_modules/katex")) / "dist"

    def route(r):
        f = kdir / r.request.url.split("/dist/", 1)[1]
        r.fulfill(path=str(f)) if f.exists() else r.abort()

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        pg = b.new_page()
        if kdir.exists():
            pg.route(f"{KATEX_CDN}/**", route)
        pg.goto(html_path.resolve().as_uri())
        pg.wait_for_function("document.body.dataset.ready==1", timeout=20000)
        pg.emulate_media(media="print")
        pg.pdf(path=str(pdf_path), format="A4", prefer_css_page_size=True, print_background=True)
        b.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--name", help="輸出檔名（多題時建議指定，如 mock-2019）")
    ap.add_argument("--pages", type=int, help="作答紙頁數（預設每題 2 頁）")
    ap.add_argument("--typeset", action="store_true", help="題目用題目正本 §1 排版，不用原卷影本")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--root", help="exam-wiki-XX 根目錄（預設：目前目錄）")
    a = ap.parse_args()
    set_root(a.root)
    name = a.name or (a.ids[0] if len(a.ids) == 1 else "-".join(a.ids))
    OUT.mkdir(parents=True, exist_ok=True)
    page, notes = build(a.ids, name, a.pages or 2 * len(a.ids), a.typeset)
    hp = OUT / f"{name}-practice.html"
    hp.write_text(page, encoding="utf-8")
    print("→", hp.relative_to(ROOT))
    for n in notes:
        print(f"  ⚠ {n}")
    if not a.no_pdf:
        pp = hp.with_suffix(".pdf")
        to_pdf(hp, pp)
        print("→", pp.relative_to(ROOT))


if __name__ == "__main__":
    main()
````