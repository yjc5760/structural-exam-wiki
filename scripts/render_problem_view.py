#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由題解正本重新渲染 study/problems-view/<id>.html（只換 <main> 內容，頁首按鈕、樣式、腳本保留）

用法：python scripts/render_problem_view.py SS-2003-2 [SS-2003-3 ...]（根目錄或科目資料夾皆可；一次只處理同一科）
  - 來源：raw/solutions/<id>/<id>.md（解題內容唯一正本）
  - 若有 raw/solutions/<id>/<id>-problem.md（題目正本：考卷原文＋判讀清單），渲染在解析之前（2026-11-02 起試做）
  - 數學式先保護再還原（$$…$$、$…$），避免 markdown 吞掉 < > _ *
  - [[ID]] 轉為藍色徽章；相對路徑圖片改指 ../../raw/solutions/<id>/
  - 頁面不存在時，以同目錄任一既有頁為版型，並依索引主分類設定單元按鈕
需要：pip install markdown
"""
import html, json, re, sys
from pathlib import Path
import markdown

# 2026-11-08 移到知識庫根目錄 scripts/（五科共用）；科目資料夾依題號前兩碼決定
REPO = Path(__file__).resolve().parent.parent
ROOT = VIEW = None


def set_subject(qid):
    global ROOT, VIEW
    cwd = Path.cwd()
    ROOT = cwd if (cwd / "raw/json/question_index.json").exists() else REPO / qid.split("-")[0]
    if not (ROOT / "raw/solutions").is_dir():
        sys.exit(f"找不到 {ROOT}/raw/solutions")
    VIEW = ROOT / "study/problems-view"
BADGE = ('<span style="background:#e3f2fd;color:#1565c0;border-radius:8px;padding:1px 7px;'
         'font-size:.88em;font-weight:600">{}</span>')


def render_md(qid, text):
    text = text.replace("\x00", "")
    store = []

    def keep(m):
        store.append(m.group(0))
        return f"\u0000M{len(store) - 1}\u0000"

    text = re.sub(r"\$\$.+?\$\$", keep, text, flags=re.S)
    text = re.sub(r"(?<![\\$])\$(?!\$)[^\n$]+?\$", keep, text)
    text = re.sub(r"\[\[([^\]]+)\]\]", lambda m: BADGE.format(html.escape(m.group(1))), text)
    # Python-Markdown 會把「斜體內含粗體」拆壞（*a **b** c* → <em>a </em><em>b</em>…），
    # 故先把程式碼以外的 **粗體** 轉成 <strong>
    parts = re.split(r"(```.*?```|`[^`\n]+`)", text, flags=re.S)
    text = "".join(pt if i % 2 else re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", pt)
                   for i, pt in enumerate(parts))
    out = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])

    def img(m):
        src = m.group(1)
        if not re.match(r"(https?:|/|\.\./)", src):
            src = f"../../raw/solutions/{qid}/{src}"
        return f'src="{src}"'

    out = re.sub(r'src="([^"]+)"', img, out)
    out = re.sub("\u0000M(\\d+)\u0000", lambda m: html.escape(store[int(m.group(1))], quote=False), out)
    return out


def main(ids):
    if len({q.split("-")[0] for q in ids}) > 1:
        sys.exit("一次只處理同一科的題號")
    set_subject(ids[0])
    for qid in ids:
        md = ROOT / f"raw/solutions/{qid}/{qid}.md"
        page = VIEW / f"{qid}.html"
        tpl = page if page.exists() else next(VIEW.glob("*.html"))
        t = tpl.read_text(encoding="utf-8")
        body = render_md(qid, md.read_text(encoding="utf-8"))
        prob = ROOT / f"raw/solutions/{qid}/{qid}-problem.md"
        if prob.exists():
            # 題目正本（考卷原文＋判讀清單）放在解析之前；未確認時摺疊標題標「待確認」
            ptxt = prob.read_text(encoding="utf-8")
            state = "待確認" if "**待確認**" in ptxt else "已確認"
            body = ('<details class="prob" open style="background:#fffde7;border:1px solid #ffe082;'
                    'border-left:5px solid #f9a825;border-radius:0 10px 10px 0;padding:10px 18px;margin:0 0 26px">'
                    f'<summary style="cursor:pointer;font-weight:700;color:#e65100">📄 題目正本：考卷原文・附圖・判讀清單（{state}）</summary>'
                    + render_md(qid, ptxt) + "</details>\n" + body)
        new = re.sub(r"(<main>\n?).*?(\n?</main>)", lambda m: m.group(1) + body + m.group(2), t, count=1, flags=re.S)
        if tpl != page:
            old = tpl.stem
            new = new.replace(f"{old} — 題目解析", f"{qid} — 題目解析").replace(f"<h1>{old} 題目解析</h1>", f"<h1>{qid} 題目解析</h1>")
            new = new.replace(f"raw/solutions/{old}/{old}.md", f"raw/solutions/{qid}/{qid}.md")
        page.write_text(new, encoding="utf-8")
        print(f"{qid} → {page.relative_to(ROOT)}（{len(body):,} 字元）")


if __name__ == "__main__":
    main(sys.argv[1:] or sys.exit(__doc__))
