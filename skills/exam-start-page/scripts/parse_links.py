#!/usr/bin/env python3
"""把使用者貼的「連結清單」(標題＋網址的純文字) 合併進 study/data/start-links.json。

用法：
  python scripts/parse_links.py <清單.txt> --repo <科目資料夾，如 SS> [--dry-run]

規則
- 清單有提到的欄位 → 覆寫；清單沒提到的欄位（NotebookLM、簡報 PDF…）→ 保留舊值，並在報告列出。
- 清單式欄位（教科書、教科書講解影片、解題影片）：該單元在清單該段出現 → 整組換成清單版本。
- 指向本站的絕對網址自動轉成相對路徑（本機與 GitHub Pages 都能開）。
- 行首的 @ 等標記符號會被忽略。
"""
import argparse, json, re, sys
from pathlib import Path
from urllib.parse import unquote

URL_RE = re.compile(r"https?://\S+")

# 段落標題關鍵字 → 段落代碼（長的先比對）
HEADINGS = [
    ("觀念講義影片", "lecture_video"),
    ("教科書講解影片", "textbook_video"),
    ("解題過程影片", "solution"), ("解題影片", "solution"),
    ("公式記憶影片", "formula_video"),
    ("影片講義", "video_handout"),
    ("主題影片", "topic"),
    ("單元總覽", "overview"),
    ("觀念講義", "lecture"),
    ("教科書", "textbook"),
    ("NotebookLM", "notebooklm"), ("筆記本", "notebooklm"),
    ("簡報", "slides_pdf"),
    ("出題頻率", "frequency"),
    ("考古題知識庫", "wiki"), ("題庫儀表板", "wiki"),
    ("從這裡開始", "self"),
]

# 教科書檔名尾碼 → 中文標籤（新尾碼可在 start-links.json 的 textbook_labels 補）
TEXTBOOK_LABELS = {
    "tension": "拉力桿件", "compression": "壓力桿件", "flexure": "撓曲", "shear": "剪力",
    "calc": "計算篇", "concept": "概念篇", "amplification": "二階效應放大",
    "interaction": "軸力彎矩互制", "torsion": "扭轉", "deflection": "撓度",
    "upper": "上冊", "lower": "下冊", "part1": "上冊", "part2": "下冊",
}


def heading_of(line):
    for kw, code in HEADINGS:
        if kw in line:
            return code
    return None


def to_rel(url, site):
    if site and url.startswith(site):
        return unquote(url[len(site):]) or "index.html"
    return url


def clean_title(t):
    t = t.strip().lstrip("@＠*•-").strip().rstrip(":：").strip()
    t = re.sub(r"\s*[:：]\s*", "：", t)
    return re.sub(r"\s+", " ", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo)
    cfg_path = repo / "study/data/start-links.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    text = Path(args.listfile).read_text(encoding="utf-8")

    subj = cfg.get("subject")
    if not subj:
        m = re.search(r"\b([A-Z]{2})-U\d+-\d+", text)
        if not m:
            sys.exit("找不到科目代號，請在清單或 start-links.json 指定")
        subj = m.group(1)
    site = cfg.get("site") or f"https://yjc5760.github.io/exam-wiki-{subj}/"
    cfg.setdefault("subject", subj)
    cfg.setdefault("site", site)
    cfg.setdefault("repo", f"https://github.com/yjc5760/exam-wiki-{subj}")
    g = cfg.setdefault("global", {})
    g.setdefault("feedback", cfg["repo"] + "/issues/new?template=correction.yml")
    labels = {**TEXTBOOK_LABELS, **cfg.get("textbook_labels", {})}

    unit_re = re.compile(rf"{subj}-U\d+-\d+")
    qid_re = re.compile(rf"{subj}-\d{{4}}-\d+")

    # 題號 → 主單元（解題影片沒有小標題時用）
    qi = repo / "raw/json/question_index.json"
    primary = {}
    if qi.exists():
        for q in json.loads(qi.read_text(encoding="utf-8"))["questions"]:
            primary[q["moduleId"]] = q.get("primaryTopicId")

    old_units = {u["id"]: u for u in cfg.get("units", [])}
    old_titles = {}
    for u in cfg.get("units", []):
        for q, t, _ in u.get("solutions", []) + u.get("practice", []):
            if t:
                old_titles.setdefault(q, t)
    old_tb_labels = {h: t for u in cfg.get("units", []) for t, h in u.get("textbook", [])}

    new = {}        # uid -> {field: value}
    order = []      # 單元總覽段的出現順序
    seen_sections = set()
    section, sol_unit = None, None
    topic_videos = []

    def U(uid):
        return new.setdefault(uid, {})

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = URL_RE.search(line)
        if not m:
            if section == "solution" and unit_re.search(line):
                sol_unit = unit_re.search(line).group(0)
                continue
            h = heading_of(line)
            if h:
                section, sol_unit = h, None
                seen_sections.add(h)
            continue
        url = m.group(0)
        title = clean_title(line[:m.start()] + " " + line[m.end():])
        href = to_rel(url, site)
        if "讀書策略" in title:
            g["strategy_video"] = url
            continue
        um = unit_re.search(title) or unit_re.search(unquote(url))
        uid = um.group(0) if um else None

        if section in ("self", None):
            continue
        if section in ("wiki", "frequency"):
            g[section] = href
            continue
        if section == "topic":
            topic_videos.append([title, url])
            continue
        if section == "solution":
            qm = qid_re.search(title)
            if not qm:
                print("⚠ 解題影片行沒有題號，略過：", line, file=sys.stderr)
                continue
            q = qm.group(0)
            t = clean_title(title[qm.end():]) or old_titles.get(q, "")
            uid = sol_unit or primary.get(q)
            if not uid:
                print("⚠ 無法判斷單元，略過：", line, file=sys.stderr)
                continue
            U(uid).setdefault("solutions", []).append([q, t, url])
            continue
        if not uid:
            print(f"⚠ [{section}] 找不到單元代號，略過：", line, file=sys.stderr)
            continue
        if section == "overview":
            U(uid)["overview"] = href
            if uid not in order:
                order.append(uid)
        elif section in ("lecture", "video_handout", "formula_video", "notebooklm", "slides_pdf"):
            U(uid)[section] = href
        elif section == "lecture_video":
            U(uid)["lecture_anim" if "動畫" in title else "lecture_video"] = url
        elif section == "textbook":
            slug = Path(unquote(href)).stem
            suf = slug.split(uid, 1)[-1].lstrip("-")
            lab = old_tb_labels.get(href) or labels.get(suf, suf) or "教科書"
            U(uid).setdefault("textbook", []).append([lab, href])
        elif section == "textbook_video":
            tm = unit_re.search(title)
            lab = title[tm.end():] if tm else title
            lab = re.sub(r"^-T\d+\s*", "", lab).strip()
            name = (old_units.get(uid) or {}).get("name", "")
            if name and lab.startswith(name):
                lab = lab[len(name):].strip()
            lab = labels.get(lab.lower(), lab)
            U(uid).setdefault("textbook_videos", []).append([lab or "講解", url])

    if "topic" in seen_sections:
        g["topic_videos"] = topic_videos

    # ---- 合併 ----
    FIELDS = ["overview", "lecture", "textbook", "textbook_videos", "lecture_video", "lecture_anim",
              "video_handout", "slides_pdf", "formula_video", "notebooklm", "solutions"]
    ids = order + [u for u in new if u not in order] + [u for u in old_units if u not in order and u not in new]
    report, units = [], []
    for uid in ids:
        old = dict(old_units.get(uid, {"id": uid}))
        upd = new.get(uid, {})
        lines = []
        for f in FIELDS:
            ov, nv = old.get(f), upd.get(f)
            if nv is not None:
                if not ov:
                    lines.append(f"  + {f}")
                elif ov != nv:
                    lines.append(f"  ~ {f}")
                old[f] = nv
            elif ov:
                lines.append(f"  = {f}（清單未提及，保留）")
        units.append(old)
        tag = "新單元" if uid not in old_units else ""
        report.append(f"{uid} {tag}\n" + ("\n".join(lines) or "  （無變動）"))
    cfg["units"] = units

    print("\n".join(report))
    if "topic" in seen_sections:
        print(f"主題影片：{len(topic_videos)} 支")
    if args.dry_run:
        print("(dry-run，未寫檔)")
        return
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", cfg_path)


if __name__ == "__main__":
    main()
