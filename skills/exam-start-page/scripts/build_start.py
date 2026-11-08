#!/usr/bin/env python3
"""exam-wiki 五科共用「從這裡開始」起點頁產生器。

用法：python scripts/build_start.py --repo <科目資料夾，如 SS> [--out start.html]

資料來源（皆在 repo 內，不寫死在程式）：
  study/data/start-links.json   各單元連結（parse_links.py 從清單合併）
  raw/json/syllabus_taxonomy.json  科目／單元名稱
  raw/json/question_index.json     題數（全科、各單元）
樣式：科目資料夾 scripts/start.css（若有）→ 與本檔同目錄的 start.css → skill 的 assets/start.css。
任何欄位為空就不輸出那一列，所以教材還沒做齊的科目也能先產生。
"""
import argparse, json, re, sys
from collections import Counter
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent


def a(href, text, cls="", ext=None):
    if ext is None:
        ext = href.startswith("http")
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{escape(href)}"{c}{tgt}>{text}</a>'


def li(href, text):
    return f"<li>{a(href, text)}</li>" if href else ""


def inline_links(pairs, sep=" ・ "):
    return sep.join(a(h, escape(t)) for t, h in pairs)


class Site:
    def __init__(self, repo: Path):
        self.repo = repo
        self.cfg = json.loads((repo / "study/data/start-links.json").read_text(encoding="utf-8"))
        self.subj = self.cfg["subject"]
        tax = json.loads((repo / "raw/json/syllabus_taxonomy.json").read_text(encoding="utf-8"))
        s = next(x for x in tax["subjects"] if x["id"] == self.subj)
        self.subj_name = self.cfg.get("subject_name") or s["name"]
        self.item_names = {i["id"]: i["name"] for u in s["units"] for i in u["items"]}
        qs = json.loads((repo / "raw/json/question_index.json").read_text(encoding="utf-8"))["questions"]
        self.n_q = len(qs)
        self.per_unit = Counter(q.get("primaryTopicId") for q in qs)
        self.units = self.cfg["units"]
        for u in self.units:
            u.setdefault("name", self.item_names.get(u["id"], u["id"]))
            for k in ("textbook", "textbook_videos", "solutions", "practice"):
                u.setdefault(k, [])
        self.g = self.cfg["global"]
        self.missing = []

    # ---------- 檢查相對連結是否存在 ----------
    def check(self, href):
        if href and not href.startswith("http") and not href.startswith("#"):
            if not (self.repo / href).exists():
                self.missing.append(href)
        return href

    def unit_block(self, i, u):
        c = self.check
        for k in ("overview", "lecture", "video_handout"):
            c(u.get(k, ""))
        tb = "".join(f"<li>{a(c(h), '教科書' if t == '教科書' else '教科書：' + escape(t))}</li>"
                     for t, h in u["textbook"])
        tv = [list(x) for x in u["textbook_videos"]]
        heads = {t.split(" ", 1)[0] for t, _ in tv if " " in t}
        if len(tv) > 1 and len(heads) == 1 and all(" " in t for t, _ in tv):
            tv = [[t.split(" ", 1)[1], h] for t, h in tv]   # 去掉各集共同前綴（如「塑性分析」）
        tbv = f"<li>教科書講解影片：{inline_links(tv)}</li>" if tv else ""
        vids = [(t, u.get(k)) for t, k in (("觀念講義影片", "lecture_video"), ("動畫版", "lecture_anim")) if u.get(k)]
        if len(vids) == 1 and vids[0][0] == "動畫版":
            vids = [("觀念講義影片（動畫版）", vids[0][1])]
        vid_line = f"<li>{inline_links(vids)}</li>" if vids else ""
        if u["solutions"]:
            sols = "".join(f'<li>{a(h, f"<span class=qid>{escape(q)}</span> {escape(t)}")}</li>'
                           for q, t, h in u["solutions"])
        else:
            sols = "".join(f'<li>{a(c(h), f"<span class=qid>{escape(q)}</span> {escape(t)}（解析頁）")}</li>'
                           for q, t, h in u["practice"])
        nvid, nq = len(u["solutions"]), self.per_unit.get(u["id"], 0)
        bits = [f"歷屆 {nq} 題"] if nq else []
        if nvid:
            bits.append(f"{nvid} 支解題影片")
        elif u["practice"]:
            bits.append(f"{len(u['practice'])} 題精選")
        practice_block = (f"""
    <div class="col wide">
      <h4><span class="dot d6"></span>試一題 → <span class="dot d4"></span>練題目 <small>讀完講義先任選一題試寫；之後每題都先自己寫，寫過才看解答</small></h4>
      <ul class="sols">{sols}</ul>
    </div>""" if sols else "")
        overview = u.get("overview", "")
        return f"""
<details class="unit" id="{u['id']}"{' open' if i == 0 else ''}>
  <summary>
    <span class="unum">{i+1}</span>
    <span class="utitle"><span class="uid">{u['id']}</span>{escape(u['name'])}</span>
    <span class="ucount">{' ・ '.join(bits)}</span>
  </summary>
  <div class="ubody">
    <div class="col">
      <h4><span class="dot d1"></span>先看（15 分鐘）</h4>
      <ul>{li(overview, '單元總覽：考什麼、哪些公式要背') or '<li>單元總覽製作中</li>'}</ul>
      <h4><span class="dot d2"></span>懂原理 <small>文字或影片選一種</small></h4>
      <ul>
        {li(u.get('lecture', ''), '觀念講義（網頁）')}
        {vid_line}
        {li(u.get('video_handout', ''), '影片講義（圖文）')}
        {li(u.get('slides_pdf', ''), '講義簡報 PDF')}
        {tb}
        {tbv}
      </ul>
    </div>
    <div class="col">
      <h4><span class="dot d3"></span>記公式</h4>
      <ul>
        {li(u.get('formula_video', ''), '公式記憶影片')}
        {li(overview, '單元總覽的「必須自己背」清單')}
      </ul>
      <h4><span class="dot d5"></span>問到懂</h4>
      <ul>
        {li(u.get('notebooklm', ''), 'NotebookLM 單元筆記本') or '<li>把單元總覽與觀念講義丟給 AI 提問</li>'}
      </ul>
    </div>{practice_block}
  </div>
</details>"""

    # ---------- 進度表 ----------
    def plan(self, weeks):
        """回傳 [(起週, 迄週, 單元們)]。第 1 週定方向、最後至少 1 週總複習。
        單元數 ≤ 可用週數：每單元 1 週；12 週版多出的週數依歷屆題數分給大單元（weeks12 可逐單元指定）。
        單元數 > 可用週數：連續單元合併同一週。"""
        avail = weeks - 2
        n = len(self.units)
        if n == 0:
            return []
        if n > avail:
            base, rem = divmod(n, avail)
            groups, k = [], 0
            for j in range(avail):
                sz = base + (1 if j < rem else 0)
                groups.append(self.units[k:k + sz]); k += sz
            return [(2 + j, 2 + j, grp) for j, grp in enumerate(groups)]
        # weeks12：該單元在 12 週版的指定週數；沒指定的單元先排 1 週，
        # 多出的週數依歷屆題數由多到少每單元加 1 週（最後至少留 1 週總複習）。
        alloc = [u.get("weeks12", 1) if weeks >= 12 else 1 for u in self.units]
        if weeks >= 12:
            free = [k for k, u in enumerate(self.units) if "weeks12" not in u]
            free.sort(key=lambda k: -self.per_unit.get(self.units[k]["id"], 0))
            extra = max(0, avail - sum(alloc))
            for k in free[:extra]:
                alloc[k] += 1
        out, w = [], 2
        for u, d in zip(self.units, alloc):
            out.append((w, w + d - 1, [u]))
            w += d
        assert w <= weeks, f"{weeks} 週進度表排不下"
        return out

    def schedule_rows(self, weeks):
        def lab(s, e):
            return f"第 {s} 週" if s == e else f"第 {s}–{e} 週"
        rows = [("第 1 週", "定方向", "看出題頻率熱圖與讀書策略影片，排定自己的單元順序；開始 " + self.units[0]["id"])]
        last = 1
        for s, e, grp in self.plan(weeks):
            name = "、".join(f"{u['id']} {u['name']}" for u in grp)
            if len(grp) > 1:
                what = "每單元：單元總覽 → 觀念講義 → 試寫一題 → 背公式 → 練 2 題以上"
            elif e > s:
                what = "第一週：單元總覽、觀念講義、試寫一題、背公式；之後：清單上的考古題全部自己寫一遍"
            else:
                what = "單元總覽 → 觀念講義 → 試寫一題 → 公式影片 → 練 3 題以上"
            rows.append((lab(s, e), name, what))
            last = e
        rows.append((lab(last + 1, weeks), "總複習", "重看各單元總覽的「必背公式」，限時重寫錯過的題目，用 AI 改卷找出還沒補起來的盲點"))
        return "".join(f"<tr><td>{escape(x)}</td><td>{escape(y)}</td><td>{escape(z)}</td></tr>" for x, y, z in rows)

    # ---------- 整頁 ----------
    def build(self):
        g, S, N = self.g, self.subj, self.subj_name
        site = self.cfg["site"]
        # 樣式：科目資料夾 scripts/start.css（自訂）→ 與本檔同目錄（根目錄 scripts/）→ skill 的 assets/
        cands = [self.repo / "scripts/start.css", HERE / "start.css", HERE.parent / "assets/start.css"]
        css = next(c for c in cands if c.exists()).read_text(encoding="utf-8")
        units_html = "".join(self.unit_block(i, u) for i, u in enumerate(self.units))
        n_vid = sum(len(u["solutions"]) for u in self.units)
        n_tb = sum(len(u["textbook"]) for u in self.units)
        n_nb = sum(1 for u in self.units if u.get("notebooklm"))
        stats = [(len(self.units), "個重點單元"), (self.n_q, "題歷屆考題")]
        if n_tb:
            stats.append((n_tb, "冊教科書"))
        if n_vid:
            stats.append((n_vid, "支解題影片"))
        if n_nb:
            stats.append((n_nb, "本 NotebookLM 筆記本"))
        stats_html = "".join(f"<div><b>{v}</b>{t}</div>" for v, t in stats)
        wiki = g.get("wiki", "index.html")
        feedback = g.get("feedback", "")
        freq = self.check(g.get("frequency", ""))
        cta = a(freq, "第一步：看出題頻率熱圖", "btn primary") if freq else a(wiki, "進入題庫儀表板", "btn primary", ext=False)
        if g.get("strategy_video"):
            cta += a(g["strategy_video"], "▶ 全科讀書策略影片", "btn ghost")
        topics = g.get("topic_videos", [])
        topic_html = (f"""
  <div class="tip"><b>跨單元主題影片</b>　{inline_links(topics)}</div>""" if topics else "")
        fb = a(feedback, "回報") if feedback else "回報"
        gc = g.get("goatcounter", "")
        gc_html = (f'<script data-goatcounter="https://{escape(gc)}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
                   if gc else "<!-- 流量統計：在 start-links.json 的 global.goatcounter 填 GoatCounter 代碼即啟用 -->")
        return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(N)} 從這裡開始</title>
<meta name="description" content="結構技師「{escape(N)}」考古題知識庫的學習路徑：出題頻率、單元總覽、觀念講義、教科書、公式記憶、解題影片與 AI 協作，一頁看懂怎麼讀。">
<meta property="og:title" content="{escape(N)}（{S}）從這裡開始">
<meta property="og:description" content="把歷屆考古題變成知識庫：客製化講義與教科書、列印考題限時練、AI 改卷找盲點，免費使用。">
<meta property="og:url" content="{escape(site)}start.html">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet">
<style>
{css}
.feats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.feat{{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:14px 16px;font-size:15px}}
.feat b{{display:block;font-size:16px;margin-bottom:2px}}
.feat p{{margin:0;color:var(--muted);font-size:14px;line-height:1.6}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <b>exam-wiki-{S}</b>
  <nav>{a('#path','路徑',ext=False)}{a('#units','單元',ext=False)}{a('#plan','進度表',ext=False)}{a(wiki,'題庫儀表板',ext=False)}</nav>
</div></header>

<main class="wrap">
<div class="hero">
  <div class="kicker">結構技師 ・ {escape(N)}（{S}）</div>
  <h1>從這裡開始</h1>
  <p class="lead">這是用歷屆考古題集成的知識庫：從題目長出單元總覽、觀念講義和教科書，列印考題限時寫，再讓 AI 幫你改卷、找出學習盲點。照著下面六步走，不用一次把所有連結點完。</p>
  <div class="cta">{cta}</div>
  <div class="stats">{stats_html}</div>
</div>

<section id="what">
  <h2>這個知識庫能做什麼</h2>
  <p class="sub">所有教材都從考古題出發，考什麼就讀什麼。</p>
  <div class="feats">
    <div class="feat"><b>考古題知識庫</b><p>歷屆 {self.n_q} 題逐題解析，依命題大綱分類，可依單元、年份、考點篩選。{a(wiki,'開啟題庫',ext=False)}</p></div>
    <div class="feat"><b>客製化講義與教科書</b><p>每個單元都有單元總覽、觀念講義；重點單元另有從第一性原理推導公式的教科書。</p></div>
    <div class="feat"><b>列印考題限時寫</b><p>題庫裡每題都能單獨開啟、列印，照考場節奏限時寫，寫完再對解析。</p></div>
    <div class="feat"><b>AI 改卷找盲點</b><p>寫完把手寫解答拍照丟給 AI，對照題解逐步批改，找出卡住的觀念。{a('#ai','怎麼問',ext=False)}</p></div>
  </div>
</section>

<section id="path">
  <h2>六步學習路徑</h2>
  <p class="sub">每個單元都照這個順序走一遍。</p>
  <ol class="path">
    <li style="--c:var(--d1)"><div class="n">STEP 1</div><h3>定方向</h3><p>全科先看出題頻率熱圖和讀書策略影片；每個單元開始前，先花 15 分鐘看單元總覽，知道這單元考什麼。</p><span class="t">全科 30 分鐘＋每單元 15 分鐘</span></li>
    <li style="--c:var(--d2)"><div class="n">STEP 2</div><h3>懂原理</h3><p>讀觀念講義，或看講義影片，選一種就好。第一次接觸、覺得抽象，先看動畫版；想知道公式怎麼來，讀教科書。</p><span class="t">每單元 2–3 小時</span></li>
    <li style="--c:var(--d6)"><div class="n">STEP 3</div><h3>試一題</h3><p>還沒準備好也先寫一題。寫不出來沒關係，卡過一次，後面看講義和解答時才知道自己在找什麼。</p><span class="t">30 分鐘</span></li>
    <li style="--c:var(--d3)"><div class="n">STEP 4</div><h3>記公式</h3><p>懂了原理再背。用公式記憶影片，配合單元總覽的「必須自己背」清單。</p><span class="t">每單元約 1 小時</span></li>
    <li style="--c:var(--d4)"><div class="n">STEP 5</div><h3>練題目</h3><p>列印考題限時自己寫，只看考卷會給的公式。寫完或卡住 5 分鐘以上，才看解題影片。</p><span class="t">每題 30–40 分鐘</span></li>
    <li style="--c:var(--d5)"><div class="n">STEP 6</div><h3>問到懂</h3><p>讓 AI 改你的手寫解答、指出盲點；還是不懂就丟進 NotebookLM 追問，直到能自己講給別人聽。</p><span class="t">隨時</span></li>
  </ol>
  <div class="tip">
    <b>三個原則</b>
    <ul class="rules">
      <li><b>解題影片一定在自己寫過之後才看。</b>先看再寫會產生「我懂了」的錯覺，到考場還是寫不出來。</li>
      <li><b>讀資料不超過總時間的三分之一</b>，其餘時間都拿來練題。已有基礎的人，看完單元總覽就可以直接試寫，寫不出來再回講義查。</li>
      <li><b>答案和題解對不上，不一定是你錯。</b>部分題解仍在校對中，歡迎{fb}，你的回報會讓題解更正確。</li>
    </ul>
  </div>
</section>

<section id="units">
  <h2>各單元教材</h2>
  <p class="sub">依建議讀書順序排列，點開即可看到該單元全部教材。</p>
  {units_html}{topic_html}
</section>

<section id="plan">
  <h2>進度表範例</h2>
  <p class="sub">依你距離考試的時間選一個，照自己的步調調整。</p>
  <div class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-t="w8">8 週衝刺</button>
    <button role="tab" aria-selected="false" data-t="w12">12 週穩讀</button>
  </div>
  <div class="tablewrap" id="w8"><table><thead><tr><th>時間</th><th>單元</th><th>要做的事</th></tr></thead><tbody>{self.schedule_rows(8)}</tbody></table></div>
  <div class="tablewrap" id="w12" hidden><table><thead><tr><th>時間</th><th>單元</th><th>要做的事</th></tr></thead><tbody>{self.schedule_rows(12)}</tbody></table></div>
</section>

<section id="ai">
  <h2>怎麼跟 AI 協作</h2>
  <p class="sub">把 AI 當成隨時可以問的家教和改卷老師。下面幾種問法可以直接複製使用。</p>
  <div class="prompts">
    <div class="prompt"><b>AI 改卷</b>上傳手寫解答照片和題解，問：<code>請逐步對照題解批改我的解答，標出第一個出錯的步驟，說明我缺的是哪個觀念，不要直接重寫給我。</code></div>
    <div class="prompt"><b>卡在某一步</b>貼上題目和你算到的地方，問：<code>我算到這裡就卡住了，下一步為什麼要這樣做？先不要給我答案，給我提示。</code></div>
    <div class="prompt"><b>確認真的懂了</b>讀完一個觀念後，問：<code>請出 3 題考這個觀念的小題，等我回答後再告訴我對不對。</code></div>
    <div class="prompt"><b>公式從哪來</b>對一條公式問：<code>這條公式的物理意義是什麼？每個變數變大時結果會怎麼變？</code></div>
  </div>
</section>
</main>

<footer><div class="wrap">
  <p><b>使用須知：</b>本站內容由作者整理並借助 AI 產生，已盡力校對，但仍可能有錯誤；請以現行規範與正式教材為準。</p>
  <p><b>發現錯誤或有建議？</b>{a(feedback,'填寫勘誤回報') if feedback else '歡迎回報'}（需 GitHub 帳號，免費註冊），每一則回報都會讓這份教材更好。</p>
  <p>考古題來源：考選部公開試題。 ・ {a(wiki,f'題庫儀表板（全部 {self.n_q} 題）',ext=False)}</p>
</div></footer>

<script>
document.querySelectorAll('.tabs button').forEach(b => b.addEventListener('click', () => {{
  document.querySelectorAll('.tabs button').forEach(x => x.setAttribute('aria-selected', x === b));
  ['w8','w12'].forEach(id => document.getElementById(id).hidden = id !== b.dataset.t);
}}));
</script>
{gc_html}
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    s = Site(repo)
    html = s.build()
    out = Path(args.out) if args.out else repo / "start.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out)
    if s.missing:
        print("⚠ 以下相對連結在 repo 找不到檔案（可能尚未建立或尚未 push）：")
        for m in sorted(set(s.missing)):
            print("   ", m)


if __name__ == "__main__":
    main()
