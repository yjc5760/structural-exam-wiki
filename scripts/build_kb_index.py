#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""五科知識索引：由正本編譯「全站搜尋＋L3 深層知識索引＋陷阱字典＋信任標章＋概念反查」

用法（根目錄執行）：
  python scripts/build_kb_index.py            全部重建（kb/ 六頁＋題目瀏覽頁信任標章）
  python scripts/build_kb_index.py --check    只檢查（概念字典、跨科脈絡、抽取失敗的題目），不寫檔
  python scripts/build_kb_index.py --no-badges  不動 XX/study/problems-view/

只讀的來源（正本）：
  XX/raw/solutions/XX-YYYY-N/XX-YYYY-N.md          §2 核心觀念、§3 陷阱、§3.5 L3、頁尾修正日期
  XX/raw/solutions/XX-YYYY-N/XX-YYYY-N-problem.md  考卷原文（搜尋用摘要）
  XX/raw/json/question_index.json                  分類、標籤、verificationStatus、codeClauses
  XX/wiki/queries/audit-ledger-XX.json             盲解／勘誤／落實檢查 → 信任標章
  concept_vocabulary.json                          標籤同義詞與上位概念（根目錄）
  cross_subject_links.json                         跨科單元脈絡（根目錄）
  syllabus_taxonomy.json                           子項名稱

產出（全部可重跑覆寫，不手改）：
  kb/kb-data.js · kb/search.html · kb/traps.html · kb/l3.html · kb/trust.html · kb/concepts.html
  XX/study/problems-view/<id>.html 頁首 <!--trust-->…<!--/trust--> 一段（只動這一段）

信任標章（由 ledger 與 verificationStatus 推得，不另存狀態欄位）：
  ✅ 人工已核：verificationStatus = verified（只有使用者能改）
  🔵 盲解一致／勘誤已落實／分歧已裁定：AI 盲解或落實檢查通過，或使用者已裁定分歧
  🟠 盲解後有修改：盲解（或落實檢查）之後解析又改過，且頁尾修正紀錄沒寫「答案不變」
  🟠 勘誤後待複驗：依盲解結果勘誤了，還沒做落實檢查
  🟠 盲解不確定　🔴 分歧待處理：盲解與解析不同且尚未裁定　⚪ 未盲解
2026-11-28 建立（知識庫升級第 1、2、4、5 步）。
"""
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUBJ = [("SS", "鋼結構設計", "#2563eb"), ("RC", "鋼筋混凝土設計與預力混凝土設計", "#d97706"),
        ("SA", "結構學", "#059669"), ("SD", "結構動力分析與耐震設計", "#7c3aed"),
        ("SM", "土壤力學與基礎設計", "#b45309")]
OUT = REPO / "kb"

TIERS = {  # key: (icon, label, color, 排序)
    "open": ("🔴", "分歧待處理", "#b91c1c", 0),
    "fixed-pending": ("🟠", "勘誤後待複驗", "#c2410c", 1),
    "uncertain": ("🟠", "盲解不確定", "#c2410c", 2),
    "changed": ("🟠", "盲解後有修改", "#c2410c", 3),
    "none": ("⚪", "未盲解", "#6b7280", 4),
    "ruled": ("🔵", "分歧已裁定", "#1d4ed8", 5),
    "fixed-ok": ("🔵", "勘誤已落實", "#1d4ed8", 6),
    "ai-ok": ("🔵", "盲解一致", "#1d4ed8", 7),
    "verified": ("✅", "人工已核", "#15803d", 8),
}
META_TAG = re.compile(r"規範|題意|勘誤|判讀|論述|名詞解釋|題目|單位換算|圖表|概念辨析|干擾|陷阱|錯誤診斷")
SAFE_EDIT = re.compile(r"答案不變|答案未變|內容與答案不變|不影響答案|數值不變|結果不變|僅格式|格式調整")
FOOT = re.compile(r"修正日期[：:]\s*(\d{4}-\d{2}-\d{2})")


# ───────────────────────── markdown 抽取 ─────────────────────────
def section(text, head_re, level=2):
    """取出標題符合 head_re 的段落（到下一個同級或更高級標題為止）"""
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if not m:
            continue
        lv = len(m.group(1))
        if start is None:
            if lv == level and re.search(head_re, m.group(2)):
                start = i + 1
        elif lv <= level:
            return "\n".join(lines[start:i])
    return "\n".join(lines[start:]) if start is not None else ""


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = s.replace("⚠️", "").replace("⚠", "")
    return re.sub(r"[ \t]+", " ", s).strip()


ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)、])\s+(.*)$")
TRAP_PREFIX = re.compile(r"^(?:⚠️?\s*)?(?:陷阱|易錯點|常見錯誤)\s*[0-9０-９①-⑳一二三四五六七八九十]*\s*[-–.：:、]?\s*")


def split_title(raw):
    """item 原文 → (標題, 內容)"""
    raw = raw.strip()
    m = re.match(r"^(?:⚠️?\s*)?\*\*(.+?)\*\*\s*[：:，,。]?\s*(.*)$", raw, re.S)
    if m:
        title, body = m.group(1), m.group(2)
    else:
        m = re.match(r"^(.{2,40}?)[：:]\s*(.+)$", raw, re.S)
        title, body = (m.group(1), m.group(2)) if m else (raw[:40], raw[40:] if len(raw) > 40 else "")
    title = TRAP_PREFIX.sub("", clean(title)).strip("：: ")
    body = clean(body)
    if not title and body:  # 「**陷阱 1：** 內容…」→ 以內容第一句當標題
        title = re.split(r"[，。；,;]|——", body, maxsplit=1)[0][:36]
    title = title or clean(raw)[:40]
    if title.count("$") % 2:  # 截斷在數學式中間 → 退到該式之前
        title = title[:title.rfind("$")].rstrip() or title.replace("$", "")
    return title, body


def is_header(line):
    """「**關鍵陷阱：**」這類只有標題、沒有內容的行"""
    t = clean(re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line))
    return bool(t) and len(t) <= 24 and t.endswith(("：", ":")) and "**" in line


SEP_ROW = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
TRAP_WORD = re.compile(r"陷阱|⚠|易錯|錯誤|誤")


def is_row(s):
    """表格列：| a | b |，或少數正本省略首尾直線的 a | b | c"""
    t = s.strip()
    if t.startswith("|"):
        return True
    return t.count("|") >= 2 and not t.startswith(("$", "-", "*", ">")) and "$|" not in t


TRAP_MARK = re.compile(r"陷阱|⚠|易錯|常見錯誤")


def split_cells(row):
    """表格列拆欄；$…$ 裡的 |（絕對值）先保護起來"""
    prot = re.sub(r"\$[^$\n]*\$", lambda m: m.group(0).replace("|", "‖"), row.strip().strip("|"))
    return [c.strip().replace("‖", "|") for c in prot.split("|")]


def parse_items(block, trap_mode=False):
    """把一段 markdown 拆成條目：表格列、引言群組、清單項目、粗體（或 ⚠）開頭的段落。

    trap_mode（§3 陷阱）：
      - 含「陷阱／⚠／易錯／常見錯誤」的小標題或粗體標題 → 進入陷阱區，其後條目都收
      - 其他小標題或粗體標題（如「子題(二) 戰略：」）→ 暫停收集，直到下一個陷阱標記
      - 只有標題、內容在下一段的（「**題(一)陷阱：**」換行接文字）→ 標題併入該段
    非 trap_mode（L3）：遇到小標題即結束。"""
    items, cur, quote, base = [], None, [], None
    para = False          # cur 是否為段落條目（空行即結束）
    skipping = False      # trap_mode：目前在非陷阱區
    pending = ""          # 只有標題、尚未接內容的陷阱標題
    infence = False
    lines = block.split("\n")

    def flush():
        nonlocal cur, quote, para
        if cur is not None:
            items.append(cur)
        if quote:
            items.append("\n".join(quote))
        cur, quote, para = None, [], False

    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if s.lstrip().startswith(("```", "~~~")):
            infence = not infence
            continue
        if infence:
            continue
        if not s.strip():
            if quote or para:
                flush()
            continue
        hm = re.match(r"^#{1,6}\s+(.*)$", s)
        if hm:
            if not trap_mode:
                break
            flush()
            skipping, pending = (False, "") if TRAP_MARK.search(hm.group(1)) else (True, "")
            continue
        if trap_mode and is_header(s):
            flush()
            if TRAP_MARK.search(s):
                skipping, pending = False, clean(s).rstrip("：:")
            else:
                skipping, pending = True, ""
            continue
        if not trap_mode and is_header(s):
            break
        bold_start = s.lstrip().startswith(("**", "⚠"))
        if trap_mode and skipping:
            if bold_start and TRAP_MARK.search(s):
                skipping = False
            elif s.lstrip().startswith(">") and TRAP_MARK.search(s):
                skipping = False
            elif ITEM.match(s) and TRAP_MARK.search(s):
                skipping = False
            else:
                continue
        if s.strip().startswith("|") or (not trap_mode and is_row(s)):
            flush()
            if SEP_ROW.match(s):
                continue
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if SEP_ROW.match(nxt):  # 下一列是分隔線 → 這列是表頭
                continue
            cells = split_cells(s)
            head = re.sub(r"\*\*(.+?)\*\*", r"\1", cells[0]) if cells else ""
            if head:
                items.append("**" + head + "**：" + "；".join(c for c in cells[1:] if c))
            pending = ""
            continue
        if s.lstrip().startswith(">"):
            if cur is not None:
                items.append(cur)
                cur, para = None, False
            quote.append(s.lstrip()[1:].strip())
            pending = ""
            continue
        if quote:
            flush()
        m = ITEM.match(s)
        if m:
            if para and trap_mode:  # 「**陷阱一：…**」下面緊接「- 描述／- 應對」→ 同一條
                cur += "\n" + m.group(2)
                continue
            if para:
                flush()
            ind = len(m.group(1).expandtabs(4))
            if base is None or ind <= base:
                base = ind
                if cur is not None:
                    items.append(cur)
                cur = m.group(2)
            else:
                cur = (cur + "\n" + m.group(2)) if cur is not None else m.group(2)
            pending = ""
            continue
        if bold_start and (cur is None or para):
            if trap_mode and not TRAP_MARK.search(s) and not pending and (items or cur is not None):
                flush()
                skipping = True
                continue
            flush()
            cur, para, pending = s.strip(), True, ""
            continue
        if cur is None and pending:  # 標題在上一行、內容在這段
            cur, para, pending = f"**{pending}**：{s.strip()}", True, ""
            continue
        if cur is not None:
            cur += "\n" + s.strip()
    flush()
    return [i for i in items if len(clean(i)) >= 2]


def extract_traps(md):
    sec = section(md, r"^3[.\s]")
    if not sec:
        return []
    lines = sec.split("\n")
    # 先找「像標題」的陷阱標記（粗體、⚠、小標題、清單、引言），找不到才退而求其次
    start = re.compile(r"^\s*(?:#{2,6}\s|>\s*|(?:[-*+]|\d+[.)、])\s+)?\s*(?:⚠️?\s*)?(?:\*\*)?[^\n]{0,20}?(?:陷阱|易錯|常見錯誤)")
    idx = next((i for i, ln in enumerate(lines) if start.match(ln) and (("**" in ln) or "⚠" in ln or ln.lstrip().startswith("#"))), None)
    if idx is None:
        idx = next((i for i, ln in enumerate(lines) if TRAP_MARK.search(ln)), None)
    if idx is None:
        return []
    first = lines[idx]
    out = []
    m = ITEM.match(first)
    if m and is_header(first):  # 「- **陷阱與常見錯誤：**」底下縮排子清單
        ind = len(m.group(1))
        sub = []
        for ln in lines[idx + 1:]:
            if ln.strip() and not ln.startswith(" " * (ind + 1)) and not ln.startswith("\t"):
                break
            sub.append(ln)
        raw = parse_items("\n".join(sub))
    else:
        raw = parse_items("\n".join(lines[idx:]), trap_mode=True)
    for r in raw:
        t, b = split_title(r)
        if t:
            out.append([t, b])
    return out


def extract_l3(md):
    lines = md.split("\n")
    start = next((i for i, ln in enumerate(lines) if re.match(r"^#{3,4}\s*L3[：:]\s*.*深", ln)), None)
    if start is None:
        return []
    body = []
    for ln in lines[start + 1:]:
        if re.match(r"^#{1,4}\s", ln) or ln.strip() == "---":
            break
        body.append(ln)
    out = []
    for r in parse_items("\n".join(body).replace("∣", "|")):
        t, b = split_title(r)
        if t and t not in ("知識點", "項目"):
            out.append([t, b])
    return out


def extract_core(md):
    sec = section(md, r"^2[.\s]")
    for ln in sec.split("\n"):
        if "核心" in ln and "**" in ln:
            return clean(ln)[:160]
    for ln in sec.split("\n"):
        if ln.strip() and not ln.startswith("#"):
            return clean(ln)[:160]
    return ""


def extract_problem(qdir, qid, md):
    p = qdir / f"{qid}-problem.md"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        sec = section(t, r"考卷原文")
        txt = " ".join(clean(ln.lstrip("> ")) for ln in sec.split("\n") if ln.strip().startswith(">"))
        if txt:
            return txt[:400]
    sec = section(md, r"^1[.\s]")
    return " ".join(clean(ln.lstrip("> ")) for ln in sec.split("\n") if ln.strip())[:400]


def footers(md):
    out = []
    for ln in md.split("\n"):
        for d in FOOT.findall(ln):
            out.append((d, ln))
    return out


# ───────────────────────── 信任標章 ─────────────────────────
def trust(q, ent, md):
    if q.get("verificationStatus") == "verified":
        return "verified", "使用者已人工複核（verificationStatus = verified）"
    if not ent or not ent.get("result"):
        return "none", "尚無盲解比對紀錄"
    res, d = ent["result"], ent.get("date", "")
    fixed = ent.get("fixed") or ""
    rc = ent.get("recheck") or {}
    rcd, rcr = rc.get("date") or "", rc.get("result") or ""
    human = ent.get("human") or ""
    note = [f"盲解 {d}：{res}"]
    if human:
        note.append(f"裁定：{human[:80]}")
    if fixed:
        note.append(f"勘誤 {fixed}")
    if rcd:
        note.append(f"落實檢查 {rcd}：{rcr}")
    if res.startswith("一致"):
        tier, base = "ai-ok", max(d, rcd)
    elif "不確定" in res:
        tier, base = ("ruled" if human else "uncertain"), d
    elif fixed:
        if rcd and rcd >= fixed and rcr.startswith("落實"):
            tier, base = "fixed-ok", rcd
        else:
            tier, base = "fixed-pending", fixed
    else:
        tier, base = ("ruled" if human else "open"), d
    if tier in ("ai-ok", "fixed-ok", "ruled"):
        later = sorted({dt for dt, ln in footers(md) if dt > base and not SAFE_EDIT.search(ln)})
        if later:
            tier = "changed"
            note.append(f"之後又修改 {'、'.join(later)}（頁尾未註明答案不變）")
    return tier, "；".join(note)


# ───────────────────────── 載入 ─────────────────────────
def load_taxonomy():
    d = json.loads((REPO / "syllabus_taxonomy.json").read_text(encoding="utf-8"))
    names = {}

    def walk(o):
        if isinstance(o, dict):
            if "id" in o and "name" in o:
                names[o["id"]] = o["name"]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    return names


def load_json(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def collect():
    topics = load_taxonomy()
    rows, problems = [], []
    for code, _, _ in SUBJ:
        idx = load_json(REPO / code / "raw/json/question_index.json", {"questions": []})["questions"]
        ledger = load_json(REPO / code / f"wiki/queries/audit-ledger-{code}.json", {})
        for q in idx:
            qid = q["moduleId"]
            qdir = REPO / code / "raw/solutions" / qid
            mdp = qdir / f"{qid}.md"
            md = mdp.read_text(encoding="utf-8") if mdp.exists() else ""
            if not md:
                problems.append(f"{qid}：找不到解析正本")
            traps, l3 = extract_traps(md), extract_l3(md)
            if md and not traps:
                s3 = section(md, r"^3[.\s]")
                problems.append(f"{qid}：§3 有「陷阱」字樣但格式抽不到" if re.search(r"陷阱|易錯|常見錯誤", s3)
                                else f"{qid}：正本沒有陷阱段落（§3{'不存在' if not s3 else '未寫陷阱'}）")
            if md and not l3:
                problems.append(f"{qid}：L3 格式抽不到" if re.search(r"^#{3,4}\s*L3", md, re.M)
                                else f"{qid}：正本沒有 L3 段落")
            tier, note = trust(q, ledger.get(qid), md)
            ent = ledger.get(qid) or {}
            rows.append({
                "id": qid, "s": code, "y": int(qid.split("-")[1]), "roc": q.get("year"),
                "t": q.get("primaryTopicId", ""), "st": q.get("secondaryTopicIds") or [],
                "tags": q.get("tags") or [], "cc": q.get("codeClauses") or [],
                "tr": tier, "tn": note, "rep": ent.get("report", ""),
                "prob": extract_problem(qdir, qid, md), "core": extract_core(md),
                "traps": traps, "l3": l3,
            })
    return topics, rows, problems


def check_vocab(vocab, rows, topics, links):
    errs, warns = [], []
    alltags = Counter(t for r in rows for t in r["tags"])
    seen, ids = {}, set()
    for c in vocab.get("concepts", []):
        if c["id"] in ids:
            errs.append(f"概念 id 重複：{c['id']}")
        ids.add(c["id"])
        for s in c["synonyms"]:
            if s in seen:
                errs.append(f"標籤「{s}」同時在 {seen[s]} 與 {c['id']}")
            seen[s] = c["id"]
            if s not in alltags:
                warns.append(f"{c['id']}：「{s}」目前沒有任何題目使用")
    for c in vocab.get("concepts", []):
        for b in c.get("broader", []):
            if b not in ids:
                errs.append(f"{c['id']} 的上位概念 {b} 不存在")
    for ch in links.get("chains", []):
        for u in ch["units"]:
            if u not in topics:
                errs.append(f"跨科脈絡 {ch['id']}：{u} 不是合法子項")
    return errs, warns


# ───────────────────────── 衍生：概念、熱點、跨科建議 ─────────────────────────
def derive(rows, vocab, links, topics):
    concepts = vocab.get("concepts", [])
    tag2c = {s: c["id"] for c in concepts for s in c["synonyms"]}
    cq = defaultdict(set)
    for r in rows:
        for t in r["tags"]:
            if t in tag2c:
                cq[tag2c[t]].add(r["id"])
    cout = [{"id": c["id"], "label": c["label"], "syn": c["synonyms"], "br": c.get("broader", []),
             "note": c.get("note", ""), "ok": bool(c.get("confirmed")), "q": sorted(cq[c["id"]])}
            for c in concepts]

    # L3 熱點：哪些概念（標籤／同義詞群）最常被寫成 L3「不懂就卡住」的知識點名稱
    # 只比對 L3 的知識點（第一欄），不比對說明；太短的中文標籤（翼板、內力…）太泛，略過
    def usable(t):
        if re.fullmatch(r"[\d.\s#\-]+", t) or META_TAG.search(t):
            return False
        return len(t) >= 3 or bool(re.search(r"[A-Za-zα-ωΑ-Ω]", t))

    keys = {}
    for c in concepts:
        vs = [s for s in c["synonyms"] if usable(s)]
        if vs:
            keys[c["label"]] = vs
    for r in rows:
        for t in r["tags"]:
            if t not in tag2c and usable(t):
                keys.setdefault(t, [t])
    pats = {k: re.compile("|".join(
        (r"(?<![A-Za-z])" + re.escape(v) + r"(?![A-Za-z])") if re.search(r"[A-Za-z]", v) else re.escape(v)
        for v in vs)) for k, vs in keys.items()}
    hot = defaultdict(list)
    for r in rows:
        names = " ／ ".join(a for a, _ in r["l3"])
        for k, p in pats.items():
            if p.search(names):
                hot[(r["s"], k)].append(r["id"])
    hotout = defaultdict(list)
    for (s, k), qs in hot.items():
        if len(qs) >= 3:
            hotout[s].append([k, sorted(qs)])
    for s in hotout:
        hotout[s].sort(key=lambda x: -len(x[1]))
        hotout[s] = hotout[s][:30]

    # 跨科：單元 → 概念（同義詞歸併後）
    unit_c = defaultdict(set)
    for r in rows:
        cs = {tag2c.get(t, "#" + t) for t in r["tags"]
              if not META_TAG.search(t) and not re.match(r"^(D\d|#\d|\d)", t)}
        for u in [r["t"]] + r["st"]:
            unit_c[u] |= cs
    chains = []
    for ch in links.get("chains", []):
        pairs = []
        us = ch["units"]
        for i in range(len(us)):
            for j in range(i + 1, len(us)):
                if us[i][:2] != us[j][:2]:
                    share = sorted(unit_c[us[i]] & unit_c[us[j]])
                    pairs.append([us[i], us[j], share[:12]])
        chains.append({**ch, "pairs": pairs})
    sugg = []
    units = sorted(unit_c)
    for i, a in enumerate(units):
        for b in units[i + 1:]:
            if a[:2] == b[:2]:
                continue
            share = unit_c[a] & unit_c[b]
            if len(share) >= 3:
                sugg.append([a, b, sorted(share)[:12], len(share)])
    sugg.sort(key=lambda x: -x[3])
    clabel = {c["id"]: c["label"] for c in concepts}

    def lab(x):
        return clabel.get(x, x[1:] if x.startswith("#") else x)
    for ch in chains:
        ch["pairs"] = [[a, b, [lab(x) for x in s]] for a, b, s in ch["pairs"]]
    sugg = [[a, b, [lab(x) for x in s], n] for a, b, s, n in sugg[:25]]

    # 規範條文反查（question_index 的 codeClauses，勘誤時逐步補）
    clauses = defaultdict(list)
    for r in rows:
        for c in r["cc"]:
            clauses[c].append(r["id"])
    return cout, dict(hotout), chains, sugg, {k: sorted(v) for k, v in sorted(clauses.items())}


# ───────────────────────── 頁面 ─────────────────────────
CSS = """:root{--bg:#f5f6f8;--card:#fff;--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--ac:#0f766e;--hl:#fef08a}
@media (prefers-color-scheme:dark){:root{--bg:#111827;--card:#1f2937;--ink:#e5e7eb;--mut:#9ca3af;--line:#374151;--ac:#2dd4bf;--hl:#854d0e}}
*{box-sizing:border-box}body{margin:0;font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;background:var(--bg);color:var(--ink);line-height:1.65;font-size:15px}
.wrap{max-width:1100px;margin:0 auto;padding:18px 14px 40px}
nav{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}nav a{padding:5px 11px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:inherit;text-decoration:none;font-size:.88rem}
nav a.on{background:var(--ac);color:#fff;border-color:var(--ac)}
h1{font-size:1.35rem;margin:4px 0}.sub{color:var(--mut);font-size:.87rem;margin:2px 0 14px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
input[type=search]{flex:1;min-width:220px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:1rem;background:var(--card);color:inherit}
select{padding:7px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:inherit}
.chip{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:999px;border:1.5px solid var(--c);color:var(--c);font-size:.83rem;cursor:pointer;user-select:none;background:var(--card)}
.chip.off{opacity:.35}
.card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--c,var(--ac));border-radius:10px;padding:10px 14px;margin:8px 0}
.qh{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}.qid{font-weight:800;color:var(--c);text-decoration:none}
.meta{color:var(--mut);font-size:.82rem}.badge{display:inline-block;padding:0 8px;border-radius:9px;border:1.5px solid var(--b);color:var(--b);font-size:.75rem;font-weight:700;white-space:nowrap;background:var(--card)}
.fld{font-size:.75rem;color:#fff;background:var(--mut);border-radius:4px;padding:0 5px;margin-right:4px}
.snip{margin:4px 0;font-size:.9rem}mark{background:var(--hl);color:inherit;border-radius:2px}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:8px 0;padding:6px 12px}
summary{cursor:pointer;font-weight:700}details details{border:none;border-left:3px solid var(--c,var(--line));border-radius:0;padding:2px 10px;margin:6px 0}
ul.items{margin:4px 0 6px;padding-left:20px}ul.items li{margin:3px 0}.t{font-weight:700}
table{border-collapse:collapse;width:100%;background:var(--card);font-size:.88rem}th,td{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}th{background:rgba(127,127,127,.08)}
.qlink{display:inline-block;margin:2px 4px 2px 0;font-size:.82rem;text-decoration:none;color:var(--c,var(--ac))}
.note{font-size:.82rem;color:var(--mut)}code{background:rgba(127,127,127,.15);padding:1px 5px;border-radius:4px}
.more{display:block;margin:10px auto;padding:8px 18px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:inherit;cursor:pointer}"""

NAV = [("search.html", "🔎 全站搜尋"), ("traps.html", "⚠️ 陷阱字典"), ("l3.html", "🧠 L3 深層知識"),
       ("concepts.html", "🏷️ 概念與跨科"), ("trust.html", "🛡️ 可信度"), ("../index.html", "🏠 五科首頁")]

COMMON_JS = r"""
const S=KB.subjects, T=KB.tiers;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const href=id=>`../${id.slice(0,2)}/study/problems-view/${id}.html`;
const col=id=>S[id.slice(0,2)].color;
const badge=r=>{const t=T[r.tr];return `<a class="badge" style="--b:${t[2]}" href="trust.html#${r.id}" title="${esc(r.tn)}">${t[0]} ${t[1]}</a>`};
const qlink=id=>`<a class="qlink" style="--c:${col(id)}" href="${href(id)}">${id}</a>`;
const topic=t=>esc(t)+' '+esc(KB.topics[t]||'');
function math(el){if(window.renderMathInElement)try{renderMathInElement(el,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})}catch(e){}}
function lazyMath(root){root.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open&&!d.dataset.m){d.dataset.m=1;math(d)}}))}
"""


def shell(fname, title, sub, body, script):
    nav = "".join(f'<a href="{h}"{" class=on" if h == fname else ""}>{t}</a>' for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}｜結構技師考試知識庫</title>
<!-- 由 scripts/build_kb_index.py 產生，請勿手改 -->
<link rel="stylesheet" href="../SS/study/assets/katex/katex.min.css">
<script defer src="../SS/study/assets/katex/katex.min.js"></script>
<script defer src="../SS/study/assets/katex/auto-render.min.js"></script>
<style>{CSS}</style></head><body><div class="wrap">
<nav>{nav}</nav><h1>{title}</h1><p class="sub">{sub}</p>
{body}
</div>
<script src="kb-data.js"></script>
<script>{COMMON_JS}
{script}</script>
</body></html>
"""


SEARCH_JS = r"""
const syn={},orig={};KB.concepts.forEach(c=>{const all=[...new Set([...c.syn,c.label])];all.forEach(s=>{orig[s.toLowerCase()]=s;(syn[s.toLowerCase()]=syn[s.toLowerCase()]||new Set());all.forEach(x=>syn[s.toLowerCase()].add(x.toLowerCase()))})});
const rx={};const R=v=>rx[v]||(rx[v]=new RegExp(/[a-z]/.test(v)?'(?<![a-z])'+v.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![a-z])':v.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'));
const has=(txt,v)=>/[a-z]/.test(v)?R(v).test(txt)&&(R(v).lastIndex=0,true):txt.includes(v);
const FIELDS={prob:'題意',core:'核心',traps:'陷阱',l3:'L3',tags:'標籤',cc:'條文'};
const docs=KB.q.map(r=>({r,f:{prob:r.prob,core:r.core,traps:r.traps.map(x=>x.join('：')).join('\n'),l3:r.l3.map(x=>x.join('：')).join('\n'),tags:r.tags.join(' '),cc:r.cc.join(' ')},low:null}));
docs.forEach(d=>{d.low={};for(const k in d.f)d.low[k]=d.f[k].toLowerCase()});
const on=new Set(Object.keys(S));
document.getElementById('subs').innerHTML=Object.entries(S).map(([k,v])=>`<span class="chip" data-s="${k}" style="--c:${v.color}">${k} ${v.name.slice(0,6)}</span>`).join('');
document.getElementById('tier').innerHTML='<option value="">全部可信度</option>'+Object.entries(T).sort((a,b)=>a[1][3]-b[1][3]).map(([k,v])=>`<option value="${k}">${v[0]} ${v[1]}</option>`).join('');
document.querySelectorAll('#subs .chip').forEach(c=>c.onclick=()=>{const s=c.dataset.s;on.has(s)?on.delete(s):on.add(s);c.classList.toggle('off');run()});
const qi=document.getElementById('q'),fi=document.getElementById('field'),ti=document.getElementById('tier'),out=document.getElementById('out'),info=document.getElementById('info');
let shown=40,last=[];
function terms(){return qi.value.trim().toLowerCase().split(/\s+/).filter(Boolean).map(t=>[...(syn[t]||new Set([t]))])}
function snip(text,vars){const low=text.toLowerCase();let pos=-1,len=0;for(const v of vars){const re=R(v);re.lastIndex=0;const m=re.exec(low);const p=m?m.index:-1;if(p>=0&&(pos<0||p<pos)){pos=p;len=v.length}}
 if(pos<0)return null;const line0=text.lastIndexOf('\n',pos)+1,line1=(text.indexOf('\n',pos)+1||text.length+1)-1;let a=Math.max(line0,pos-70),b=Math.min(line1,pos+len+110);
 let s=esc(text.slice(a,b));for(const v of vars){if(!v)continue;s=s.replace(R(v),m=>`<mark>${m}</mark>`)}return (a>line0?'…':'')+s+(b<line1?'…':'')}
function run(){const ts=terms(),fld=fi.value,tier=ti.value;location.hash=qi.value?('q='+encodeURIComponent(qi.value)):'';
 if(!ts.length){out.innerHTML='';info.textContent=`共 ${KB.q.length} 題；輸入關鍵字開始搜尋（空白分隔＝且；同義詞自動展開，例：Mp、block shear、剪力屋架）`;return}
 last=docs.filter(d=>on.has(d.r.s)&&(!tier||d.r.tr===tier)&&ts.every(vs=>(fld?[fld]:Object.keys(FIELDS)).some(k=>vs.some(v=>has(d.low[k],v)))));
 shown=40;render(ts)}
function render(ts){ts=ts||terms();const vars=ts.flat();
 info.textContent=`找到 ${last.length} 題`+(ts.some(v=>v.length>1)?'（含同義詞：'+ts.filter(v=>v.length>1).map(v=>v.map(x=>orig[x]||x).join('／')).join('；')+'）':'');
 out.innerHTML=last.slice(0,shown).map(({r,f})=>{const sn=Object.keys(FIELDS).map(k=>{const s=snip(f[k],vars);return s?`<div class="snip"><span class="fld">${FIELDS[k]}</span>${s}</div>`:''}).filter(Boolean).slice(0,3).join('');
  return `<div class="card" style="--c:${col(r.id)}"><div class="qh"><a class="qid" href="${href(r.id)}">${r.id}</a><span class="meta">${topic(r.t)}・民國 ${r.roc ?? ''}</span>${badge(r)}</div>${sn}</div>`}).join('')+(last.length>shown?'<button class="more" id="more">顯示更多</button>':'');
 const m=document.getElementById('more');if(m)m.onclick=()=>{shown+=60;render()};math(out)}
qi.oninput=()=>{clearTimeout(window._t);window._t=setTimeout(run,180)};fi.onchange=run;ti.onchange=run;
const h=decodeURIComponent((location.hash.match(/q=([^&]*)/)||[])[1]||'');if(h)qi.value=h;run();
"""

GROUPED_JS = r"""
const KEY=PAGE_KEY;
function build(filter){const f=filter.trim().toLowerCase();let n=0,nq=0;const html=Object.entries(S).map(([s,sv])=>{
  const units={};KB.q.filter(r=>r.s===s&&r[KEY].length).forEach(r=>{(units[r.t]=units[r.t]||[]).push(r)});
  const ublocks=Object.keys(units).sort().map(u=>{const qs=units[u].map(r=>{const its=r[KEY].filter(([a,b])=>!f||(a+b+r.id).toLowerCase().includes(f));if(!its.length)return '';n+=its.length;nq++;
     return `<li><a class="qid" style="--c:${sv.color}" href="${href(r.id)}">${r.id}</a> ${badge(r)}<ul class="items">${its.map(([a,b])=>`<li><span class="t">${esc(a)}</span>${b?'：'+esc(b):''}</li>`).join('')}</ul></li>`}).join('');
     return qs?`<details style="--c:${sv.color}"${f?' open':''}><summary>${topic(u)}（${units[u].length} 題）</summary><ul class="items" style="list-style:none;padding-left:0">${qs}</ul></details>`:''}).join('');
  return ublocks?`<details style="--c:${sv.color}"${f?' open':''}><summary style="color:${sv.color}">${s} ${sv.name}</summary>${ublocks}</details>`:''}).join('');
 document.getElementById('out').innerHTML=html;document.getElementById('info').textContent=`${nq} 題、${n} 條`+(f?`（篩選「${filter}」）`:'');
 lazyMath(document.getElementById('out'));if(f)math(document.getElementById('out'))}
const fi=document.getElementById('f');fi.oninput=()=>{clearTimeout(window._t);window._t=setTimeout(()=>build(fi.value),200)};build('');
"""

HOT_JS = r"""
document.getElementById('hot').innerHTML=Object.entries(S).map(([s,sv])=>{const h=KB.hot[s]||[];if(!h.length)return '';
 return `<details style="--c:${sv.color}"><summary style="color:${sv.color}">${s} L3 熱點（前 ${h.length} 名）</summary><table><tr><th>觀念</th><th>題數</th><th>題目</th></tr>${h.map(([k,qs])=>`<tr><td>${esc(k)}</td><td>${qs.length}</td><td>${qs.map(qlink).join('')}</td></tr>`).join('')}</table></details>`}).join('');
"""

TRUST_JS = r"""
const order=Object.entries(T).sort((a,b)=>a[1][3]-b[1][3]).map(x=>x[0]);
const cnt={};KB.q.forEach(r=>{cnt[r.s]=cnt[r.s]||{};cnt[r.s][r.tr]=(cnt[r.s][r.tr]||0)+1});
document.getElementById('sum').innerHTML=`<table><tr><th>科目</th>${order.map(k=>`<th style="color:${T[k][2]}">${T[k][0]} ${T[k][1]}</th>`).join('')}<th>合計</th></tr>`+
 Object.keys(S).map(s=>`<tr><td><b style="color:${S[s].color}">${s}</b></td>${order.map(k=>`<td>${cnt[s]?.[k]||''}</td>`).join('')}<td>${KB.q.filter(r=>r.s===s).length}</td></tr>`).join('')+
 `<tr><td><b>五科</b></td>${order.map(k=>`<td><b>${KB.q.filter(r=>r.tr===k).length||''}</b></td>`).join('')}<td><b>${KB.q.length}</b></td></tr></table>`;
document.getElementById('lists').innerHTML=order.filter(k=>k!=='verified').map(k=>{const qs=KB.q.filter(r=>r.tr===k);if(!qs.length)return '';
 return `<details${T[k][3]<=3?' open':''}><summary style="color:${T[k][2]}">${T[k][0]} ${T[k][1]}（${qs.length} 題）— ${DESC[k]}</summary><table><tr><th>題號</th><th>單元</th><th>紀錄</th></tr>${qs.map(r=>`<tr id="${r.id}"><td>${qlink(r.id)}</td><td class="note">${topic(r.t)}</td><td class="note">${esc(r.tn)}${r.rep?`<br>報告：<code>${r.s}/${esc(r.rep.replace(/^wiki\/queries\//,'wiki/queries/'))}</code>`:''}</td></tr>`).join('')}</table></details>`}).join('');
if(location.hash){const el=document.getElementById(location.hash.slice(1));if(el){el.closest('details').open=true;el.style.background='rgba(250,204,21,.25)';setTimeout(()=>el.scrollIntoView({block:'center'}),50)}}
"""

CONCEPT_JS = r"""
function cbuild(f){f=f.trim().toLowerCase();const cs=KB.concepts.filter(c=>!f||(c.label+c.syn.join(' ')).toLowerCase().includes(f));
 const lab={};KB.concepts.forEach(c=>lab[c.id]=c.label);
 document.getElementById('cinfo').textContent=`${cs.length} 個概念`;
 document.getElementById('cout').innerHTML=`<table><tr><th>概念</th><th>同義標籤</th><th>上位概念</th><th>題目</th></tr>`+cs.map(c=>`<tr><td><b>${esc(c.label)}</b>${c.ok?'':' <span class="note">（待確認）</span>'}${c.note?`<div class="note">${esc(c.note)}</div>`:''}</td><td class="note">${c.syn.map(esc).join('、')}</td><td class="note">${c.br.map(b=>esc(lab[b]||b)).join('、')}</td><td>${c.q.length} 題<br>${c.q.map(qlink).join('')}</td></tr>`).join('')+'</table>'}
const cf=document.getElementById('cf');cf.oninput=()=>cbuild(cf.value);cbuild('');
const ul=u=>`<b style="color:${S[u.slice(0,2)].color}">${u}</b> ${esc(KB.topics[u]||'')}`;
document.getElementById('chains').innerHTML=KB.chains.map(ch=>`<div class="card"><div class="qh"><b>${esc(ch.name)}</b>${ch.confirmed?'':'<span class="note">（待確認）</span>'}</div><div>${ch.units.map(ul).join(' ↔ ')}</div><div class="note">${esc(ch.why)}</div>${ch.pairs.map(([a,b,s])=>`<div class="note">${a} × ${b} 共同概念：${s.length?s.map(esc).join('、'):'（目前標籤沒有交集）'}</div>`).join('')}</div>`).join('');
document.getElementById('sugg').innerHTML=`<table><tr><th>單元 A</th><th>單元 B</th><th>共同概念數</th><th>共同概念（前 12）</th></tr>`+KB.sugg.map(([a,b,s,n])=>`<tr><td>${ul(a)}</td><td>${ul(b)}</td><td>${n}</td><td class="note">${s.map(esc).join('、')}</td></tr>`).join('')+'</table>';
const cl=Object.entries(KB.clauses);document.getElementById('clauses').innerHTML=cl.length?`<table><tr><th>條文</th><th>題目</th></tr>${cl.map(([k,qs])=>`<tr><td><code>${esc(k)}</code></td><td>${qs.map(qlink).join('')}</td></tr>`).join('')}</table>`:'<p class="note">尚無題目標註 <code>codeClauses</code>。勘誤或依現行規範改寫解析時，於 question_index.json 補上（格式見 CLAUDE-SPEC.md），重跑本腳本即出現在這裡。</p>';
"""

TIER_DESC = {
    "open": "盲解與解析不同、尚未勘誤也未裁定，最優先處理",
    "fixed-pending": "已依盲解勘誤，待跑落實檢查",
    "uncertain": "盲解自己沒把握，需要人看",
    "changed": "通過盲解後解析又改過，建議重新盲解或落實檢查",
    "none": "還沒做盲解比對",
    "ruled": "盲解有分歧，使用者已裁定（可安排人工複核）",
    "fixed-ok": "勘誤後落實檢查通過（可安排人工複核）",
    "ai-ok": "AI 盲解與解析一致（可安排人工複核）",
}


def write_pages(data):
    OUT.mkdir(exist_ok=True)
    (OUT / "kb-data.js").write_text(
        "// 由 scripts/build_kb_index.py 產生，請勿手改\nwindow.KB=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")
    pages = {
        "search.html": shell("search.html", "全站搜尋", "五科題意、核心觀念、陷阱、L3 深層知識、標籤一次搜；同義詞自動展開（依 concept_vocabulary.json）。資料由正本編譯，勘誤後重跑 <code>python scripts/build_kb_index.py</code>。",
                             '<div class="bar"><input type="search" id="q" placeholder="例：Lb Lp、剪力遲滯、block shear、穿孔剪力、SRSS" autofocus>'
                             '<select id="field"><option value="">全部欄位</option><option value="prob">題意</option><option value="core">核心觀念</option><option value="traps">陷阱</option><option value="l3">L3</option><option value="tags">標籤</option><option value="cc">規範條文</option></select>'
                             '<select id="tier"></select></div><div class="bar" id="subs"></div><p class="note" id="info"></p><div id="out"></div>', SEARCH_JS),
        "traps.html": shell("traps.html", "全庫陷阱字典", "從每題解析 §3「陷阱分析」自動抽出，依科目 → 單元 → 題目排列。考前衝刺看這頁；點題號回到完整解析。",
                            '<div class="bar"><input type="search" id="f" placeholder="篩選陷阱文字或題號，例：寬厚比、單位、臨界斷面、SS-U1-2"></div><p class="note" id="info"></p><div id="out"></div>',
                            "const PAGE_KEY='traps';" + GROUPED_JS),
        "l3.html": shell("l3.html", "L3 深層知識索引", "從每題 §3.5「L3：深層知識（不懂就卡住）」自動抽出。上方「L3 熱點」列出同一觀念在 3 題以上被列為卡關點的項目——最值得先補、也最適合做講義或影片。",
                         '<h2 style="font-size:1.05rem">L3 熱點</h2><div id="hot"></div><h2 style="font-size:1.05rem">逐題 L3</h2>'
                         '<div class="bar"><input type="search" id="f" placeholder="篩選 L3 文字或題號"></div><p class="note" id="info"></p><div id="out"></div>',
                         "const PAGE_KEY='l3';" + GROUPED_JS + HOT_JS),
        "trust.html": shell("trust.html", "可信度總覽", "標章由各科 <code>wiki/queries/audit-ledger-XX.json</code>（盲解／勘誤／落實檢查）與 <code>verificationStatus</code> 推得，不另存狀態。✅ 只有使用者人工複核後才會出現；其餘清單就是人工驗算的待辦。",
                            '<div id="sum"></div><h2 style="font-size:1.05rem">清單（依處理優先順序）</h2><div id="lists"></div>',
                            "const DESC=" + json.dumps(TIER_DESC, ensure_ascii=False) + ";" + TRUST_JS),
        "concepts.html": shell("concepts.html", "概念與跨科脈絡", "概念字典 <code>concept_vocabulary.json</code> 把同義標籤歸成一個概念；跨科脈絡 <code>cross_subject_links.json</code> 只記單元層連結，共同概念由標籤自動算出。標「待確認」者請審閱後把 confirmed 改 true。",
                               '<h2 style="font-size:1.05rem">跨科脈絡（已整理）</h2><div id="chains"></div>'
                               '<h2 style="font-size:1.05rem">跨科共同概念最多的單元組合（自動偵測，未確認）</h2><div id="sugg"></div>'
                               '<h2 style="font-size:1.05rem">規範條文反查</h2><div id="clauses"></div>'
                               '<h2 style="font-size:1.05rem">概念字典</h2><div class="bar"><input type="search" id="cf" placeholder="篩選概念或標籤"></div><p class="note" id="cinfo"></p><div id="cout"></div>',
                               CONCEPT_JS),
    }
    for name, txt in pages.items():
        (OUT / name).write_text(txt, encoding="utf-8")


# ───────────────────────── 題目瀏覽頁標章 ─────────────────────────
BADGE_RE = re.compile(r"<!--trust-->.*?<!--/trust-->", re.S)


def badge_html(r):
    icon, label, color, _ = TIERS[r["tr"]]
    return (f'<!--trust--><a class="trust" href="../../../kb/trust.html#{r["id"]}" title="{html.escape(r["tn"])}" '
            f'style="display:inline-block;margin:0 8px;padding:1px 9px;border-radius:10px;background:#fff;color:{color};'
            f'border:1.5px solid {color};font-size:.78rem;font-weight:700;text-decoration:none;vertical-align:middle;white-space:nowrap">'
            f'{icon} {label}</a><!--/trust-->')


def apply_badges(rows):
    changed, missing = 0, []
    for r in rows:
        p = REPO / r["s"] / "study/problems-view" / f"{r['id']}.html"
        if not p.exists():
            missing.append(r["id"])
            continue
        t = p.read_text(encoding="utf-8")
        b = badge_html(r)
        if BADGE_RE.search(t):
            new = BADGE_RE.sub(lambda m: b, t, count=1)
        else:
            m = re.search(r"<header[^>]*>.*?</h1>", t, re.S)
            if not m:
                missing.append(r["id"])
                continue
            new = t[:m.end()] + b + t[m.end():]
        if new != t:
            p.write_text(new, encoding="utf-8")
            changed += 1
    return changed, missing


def main(argv):
    check = "--check" in argv
    topics, rows, problems = collect()
    vocab = load_json(REPO / "concept_vocabulary.json", {"concepts": []})
    links = load_json(REPO / "cross_subject_links.json", {"chains": []})
    errs, warns = check_vocab(vocab, rows, topics, links)
    for e in errs:
        print("✖", e)
    for w in warns:
        print("△", w)
    for pmsg in problems:
        print("△", pmsg)
    ntr, nl3 = sum(len(r["traps"]) for r in rows), sum(len(r["l3"]) for r in rows)
    print(f"題目 {len(rows)}；陷阱 {ntr} 條（{sum(1 for r in rows if r['traps'])} 題）；L3 {nl3} 條（{sum(1 for r in rows if r['l3'])} 題）")
    print("可信度：" + "、".join(f"{TIERS[k][1]} {n}" for k, n in sorted(Counter(r['tr'] for r in rows).items(), key=lambda x: TIERS[x[0]][3])))
    if errs:
        sys.exit("概念字典或跨科脈絡有錯誤，未寫檔")
    if check:
        return
    cout, hot, chains, sugg, clauses = derive(rows, vocab, links, topics)
    used = {t for r in rows for t in r["tags"]}
    data = {
        "built": date.today().isoformat(),
        "subjects": {c: {"name": n, "color": col} for c, n, col in SUBJ},
        "topics": {k: v for k, v in topics.items() if k[:2] in dict((c, 1) for c, _, _ in SUBJ)},
        "tiers": TIERS, "q": rows, "concepts": cout, "hot": hot, "chains": chains, "sugg": sugg, "clauses": clauses,
        "stats": {"tags": len(used), "conceptTags": sum(1 for t in used if any(t in c["syn"] for c in cout))},
    }
    write_pages(data)
    print(f"→ kb/（6 個檔，kb-data.js {(OUT / 'kb-data.js').stat().st_size / 1024:,.0f} KB）")
    if "--no-badges" not in argv:
        n, miss = apply_badges(rows)
        print(f"→ 題目瀏覽頁信任標章：更新 {n} 頁" + (f"；找不到頁面或頁首 {len(miss)} 題：{' '.join(miss[:10])}" if miss else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
