#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_knowledge_graph.py — exam-wiki-RC 知識圖譜產生器

⚠️ 2026-11-01 wiki 已封存至 archive/wiki/、不再維護；本腳本路徑已改指封存處，僅供參考，
   knowledge_graph.html 不再重新產生。

用途：
    重新掃描 raw/json/question_index.json、raw/json/concepts.json 以及
    wiki/{methods,philosophy,diagnosis,code-ref,failure-modes,materials,traps}/*.md，
    重建節點/邊資料，輸出自包含的 cytoscape.js 互動知識圖譜 knowledge_graph.html
    （存於專案根目錄，與 index.html 同層，深連結格式一致：
    index.html#md=<relpath>&t=<title>）。

使用時機：
    - 新增了考題（question_index.json 多了 moduleId）
    - 新增了概念（concepts.json 多了 concept_id）
    - 新增/修改了 wiki/methods, philosophy, diagnosis, code-ref, failure-modes,
      materials, traps 下的 .md 檔案，且想反映到圖譜連結上

注意：
    - 本腳本第一版是在沙盒（bash）不可用的情況下，依據 2026-07-08 當時的
      exam-wiki-RC 內容「手動推導」出資料模型後，回頭寫成腳本，尚未實際執行過。
      第一次執行後請打開 knowledge_graph.html 檢查節點/邊數量是否合理
      （對照終端機印出的摘要），有異常請回報。
    - FAILUREMODES / MATERIALS 兩層，以及 traps 對應到 concept/method 的連結，
      原始 .md 內文並未提供機器可解析的明確連結（無 [[wikilink]]），是依標題
      語意人工歸類，寫在下方 THEMATIC_* 常數裡。新增 failure-modes/materials
      檔案時，請一併在該常數補一筆。
    - DIAGNOSIS_TOPIC_OVERRIDE：少數 diagnosis 頁面（prestress.md、
      shear-torsion.md）內文只有「見 wiki/index.md §x.x」這種自然語言指向，
      無法穩定解析出完整 topicId 清單，因此用常數手動補上。

執行方式：
    python3 generate_knowledge_graph.py
    （於專案根目錄執行，或用 --root 指定 exam-wiki-RC 資料夾路徑）
"""
import json
import re
import sys
import argparse
from pathlib import Path

TOPICS = [
    ("RC-U1-1", "RC 梁彎矩強度分析與設計"),
    ("RC-U1-2", "RC 柱強度分析與設計"),
    ("RC-U1-3", "細長柱"),
    ("RC-U1-4", "柱設計圖之應用"),
    ("RC-U2-1", "RC 剪力強度分析與設計"),
    ("RC-U2-2", "RC 扭力強度設計"),
    ("RC-U2-3", "鋼筋錨定長度與斷點計算"),
    ("RC-U3-1", "梁工作性要求（含撓度、裂縫）"),
    ("RC-U3-2", "樓版與基腳設計"),
    ("RC-U3-3", "韌性要求與耐震設計"),
    ("RC-U4-1", "預力梁斷面應力分析"),
    ("RC-U4-2", "預力量與偏心量設計"),
    ("RC-U4-3", "預力損失"),
    ("RC-U4-4", "預力梁剪力分析與設計"),
]

# ---- 無法從檔案內容機器解析、需人工維護的主題式對應 ----------------------
# method id -> 適用題型 topicId 清單（若 .md 內有「**適用題型：**」行會優先動態解析，
# 這裡僅作為解析失敗時的備援）
METHOD_TOPIC_FALLBACK = {
    "PM-INTERACTION-DIAGRAM": ["RC-U1-2", "RC-U1-4"],
    "WHITNEY-STRESS-BLOCK-METHOD": ["RC-U1-1", "RC-U1-2"],
}
METHOD_CONCEPT_MAP = {
    "effective-inertia-deflection": ["EFFECTIVE-MOMENT-OF-INERTIA"],
    "FRICTION-LOSS-METHOD": ["PRESTRESS-LOSS"],
    "moment-magnifier-method": ["LONG-COLUMN-MOMENT-MAGNIFIER"],
    "PM-INTERACTION-DIAGRAM": ["PM-INTERACTION-DIAGRAM"],
    "prestress-loss-calculation": ["PRESTRESS-LOSS"],
    "SEISMIC-CAPACITY-METHOD": ["SEISMIC-DESIGN", "STRONG-COLUMN-WEAK-BEAM"],
    "T-BEAM-ANALYSIS": ["WHITNEY-STRESS-BLOCK"],
    "WHITNEY-STRESS-BLOCK-METHOD": ["WHITNEY-STRESS-BLOCK", "BETA1-FACTOR"],
}
# 已標註「（已整併）」的舊 stub 檔案，產生圖譜時略過
METHOD_SKIP_STUBS = {"EFFECTIVE-INERTIA", "MOMENT-MAGNIFIER", "PRESTRESS-LOSS-CALC"}

PHILOSOPHY_CONCEPT_MAP = {
    "deflection-crack": ["EFFECTIVE-MOMENT-OF-INERTIA", "DEFLECTION-CONTROL"],
    "prestress-philosophy": ["PRESTRESS-LOSS", "EFFECTIVE-PRESTRESS"],
    "seismic-philosophy": ["SEISMIC-DESIGN", "STRONG-COLUMN-WEAK-BEAM"],
    "slender-column": ["LONG-COLUMN-MOMENT-MAGNIFIER"],
    "usd-beam-flexure": ["DUCTILE-FAILURE", "WHITNEY-STRESS-BLOCK"],
    "usd-column-pm": ["PM-INTERACTION-DIAGRAM", "BALANCED-POINT"],
    "usd-shear": ["SHEAR-STRENGTH"],
}
PHILOSOPHY_METHOD_MAP = {
    "t-beam-design": ["T-BEAM-ANALYSIS"],
}

DIAGNOSIS_TOPIC_OVERRIDE = {
    "prestress": ["RC-U4-1", "RC-U4-2", "RC-U4-3", "RC-U4-4"],
    "shear-torsion": ["RC-U2-1", "RC-U2-2"],
}

# failure-modes / materials：原始 .md 無機器可解析連結，人工依標題語意歸類
THEMATIC_FAILUREMODES = {
    "flexure":    {"topics": ["RC-U1-1"], "concepts": ["WHITNEY-STRESS-BLOCK", "DUCTILE-FAILURE"]},
    "shear":      {"topics": ["RC-U2-1"], "concepts": ["SHEAR-STRENGTH", "STIRRUP-DESIGN"]},
    "deflection": {"topics": ["RC-U3-1"], "concepts": ["EFFECTIVE-MOMENT-OF-INERTIA", "DEFLECTION-CONTROL"]},
    "cracking":   {"topics": ["RC-U3-1"], "concepts": ["CRACK-WIDTH", "CRACKING-MOMENT"]},
    "crushing":   {"topics": ["RC-U1-1"], "concepts": ["WHITNEY-STRESS-BLOCK", "BALANCED-REINFORCEMENT-RATIO"]},
}
THEMATIC_MATERIALS = {
    "concrete-stress-strain": {"topics": ["RC-U1-1"], "concepts": ["WHITNEY-STRESS-BLOCK"]},
    "creep-shrinkage":        {"topics": ["RC-U4-3"], "concepts": ["CREEP-SHRINKAGE"]},
    "prestress-strand":       {"topics": ["RC-U4-1"], "concepts": ["EFFECTIVE-PRESTRESS", "PRESTRESS-LOSS"]},
    "steel-yielding":         {"topics": ["RC-U1-1"], "concepts": ["DUCTILE-FAILURE"]},
}
# trap id -> 相關 concept / method（原始 .md 無明確連結，依標題語意歸類）
TRAP_RELATION = {
    "BALANCED-RATIO-BOUNDARY": ("concept", "BALANCED-REINFORCEMENT-RATIO"),
    "COMPRESSION-STEEL-YIELDING": ("concept", "WHITNEY-STRESS-BLOCK"),
    "DEFLECTION-EFFECTIVE-INERTIA": ("concept", "EFFECTIVE-MOMENT-OF-INERTIA"),
    "JOINT-SHEAR-EFFECTIVE-AREA": ("concept", "SEISMIC-DESIGN"),
    "LONG-COLUMN-SLENDERNESS": ("concept", "LONG-COLUMN-MOMENT-MAGNIFIER"),
    "PHI-FACTOR-TRANSITION": ("concept", "DUCTILE-FAILURE"),
    "PRESTRESS-FPS-FORMULA": ("concept", "EFFECTIVE-PRESTRESS"),
    "PRESTRESS-LOSS-SEQUENCE": ("concept", "PRESTRESS-LOSS"),
    "PUNCHING-SHEAR-CRITICAL": ("concept", "PUNCHING-SHEAR"),
    "SEISMIC-BEAM-VE": ("concept", "SPECIAL-MOMENT-FRAME-BEAM"),
    "SHEAR-CRITICAL-SECTION": ("concept", "SHEAR-STRENGTH"),
    "T-BEAM-EFFECTIVE-WIDTH": ("method", "T-BEAM-ANALYSIS"),
    "TORSION-THRESHOLD": ("concept", "TORSION-DESIGN"),
}

RE_H1 = re.compile(r'^#\s+(.+)$', re.M)
RE_TOPIC = re.compile(r'RC-U\d-\d+')
RE_PROBLEM_BRACKET = re.compile(r'\[\[(RC-\d{4}-\d+)\]\]')
RE_PROBLEM_PLAIN = re.compile(r'RC-\d{4}-\d+(?:/\d+)*')
RE_MD_PROBLEM_LINK = re.compile(r'\]\(\.\./problems/(RC-\d{4}-\d+)\.md\)')
RE_WIKILINK = re.compile(r'\[\[([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\]\]')


def expand_shorthand(token):
    """把 'RC-2012-2/3/4' 展開成 ['RC-2012-2','RC-2012-3','RC-2012-4']"""
    m = re.match(r'(RC-\d{4})-(\d+(?:/\d+)*)', token)
    if not m:
        return [token]
    prefix, nums = m.group(1), m.group(2).split('/')
    return [f"{prefix}-{n}" for n in nums]


def read(path):
    return path.read_text(encoding='utf-8')


def h1_title(text, fallback):
    m = RE_H1.search(text)
    return m.group(1).strip() if m else fallback


def load_json_problems(root):
    data = json.loads(read(root / "raw/json/question_index.json"))
    out = []
    for q in data["questions"]:
        out.append({
            "id": q["moduleId"], "y": q["year"], "pt": q["primaryTopicId"],
            "st": q.get("secondaryTopicIds", []), "dm": q.get("designMethod", ""),
            "tags": q.get("tags", []),
        })
    return out


def load_json_concepts(root):
    data = json.loads(read(root / "raw/json/concepts.json"))
    concepts = []
    known_ids = set()
    for c in data["concepts"]:
        concepts.append({
            "id": c["concept_id"], "name": c["concept_name"], "cls": c["classification"],
            "rel": c.get("related_concept_ids", []),
            "formula": c.get("key_formula", ""), "desc": c.get("description", ""),
        })
        known_ids.add(c["concept_id"])
    return concepts, known_ids


def scan_concept_problems(root, known_concept_ids):
    """掃 wiki/concepts/*.md 的『出現題目』表格，抓 [[RC-YYYY-N]]"""
    out = {cid: [] for cid in known_concept_ids}
    d = root / "archive/wiki/concepts"
    if not d.exists():
        return out
    for f in sorted(d.glob("*.md")):
        cid = f.stem
        if cid not in known_concept_ids:
            continue
        text = read(f)
        seen = []
        for pid in RE_PROBLEM_BRACKET.findall(text):
            if pid not in seen:
                seen.append(pid)
        out[cid] = seen
    return out


def scan_methods(root, known_concept_ids):
    d = root / "archive/wiki/methods"
    out = []
    if not d.exists():
        return out
    for f in sorted(d.glob("*.md")):
        mid = f.stem
        if mid in METHOD_SKIP_STUBS or mid == "index":
            continue
        text = read(f)
        name = h1_title(text, mid)
        topic_m = re.search(r'\*\*適用題型：\*\*\s*(.+)', text)
        topics = RE_TOPIC.findall(topic_m.group(1)) if topic_m else []
        if not topics:
            topics = METHOD_TOPIC_FALLBACK.get(mid, [])
        problems = []
        for _, pid in [(g, g) for g in RE_MD_PROBLEM_LINK.findall(text)]:
            if pid not in problems:
                problems.append(pid)
        concepts = METHOD_CONCEPT_MAP.get(mid, [])
        out.append({"id": mid, "name": name, "topics": sorted(set(topics)),
                     "problems": problems, "concepts": concepts})
    return out


def scan_philosophy(root):
    d = root / "archive/wiki/philosophy"
    out = []
    if not d.exists():
        return out
    for f in sorted(d.glob("*.md")):
        pid = f.stem
        if pid == "index":
            continue
        text = read(f)
        name = h1_title(text, pid)
        problems = []
        for m in RE_MD_PROBLEM_LINK.finditer(text):
            p = m.group(1)
            if p not in problems:
                problems.append(p)
        # philosophy 檔沒有顯式 topicId 標記，topics 由對應 problems 的 primaryTopicId 推得
        # （呼叫端會用 PROBLEMS 資料回填，這裡先留空由 main() 處理）
        out.append({"id": pid, "name": name, "problems": problems,
                     "concepts": PHILOSOPHY_CONCEPT_MAP.get(pid, []),
                     "methods": PHILOSOPHY_METHOD_MAP.get(pid, [])})
    return out


def scan_diagnosis(root, known_concept_ids):
    d = root / "archive/wiki/diagnosis"
    out = []
    if not d.exists():
        return out
    for f in sorted(d.glob("*.md")):
        did = f.stem
        if did == "index":
            continue
        text = read(f)
        name = h1_title(text, did)
        topics = sorted(set(RE_TOPIC.findall(name)))
        if not topics:
            head_m = re.search(r'##\s*相關題目[（(]([^）)]+)[）)]', text)
            if head_m:
                topics = sorted(set(RE_TOPIC.findall(head_m.group(1))))
        if not topics:
            topics = DIAGNOSIS_TOPIC_OVERRIDE.get(did, [])
        concepts = []
        for cid in RE_WIKILINK.findall(text):
            if cid in known_concept_ids and cid not in concepts:
                concepts.append(cid)
        problems = []
        line_m = re.search(r'歷屆題目.*', text)
        if line_m:
            for tok in RE_PROBLEM_PLAIN.findall(line_m.group(0)):
                for p in expand_shorthand(tok):
                    if p not in problems:
                        problems.append(p)
        out.append({"id": did, "name": name, "topics": topics,
                     "problems": problems, "concepts": concepts})
    return out


def scan_coderef(root):
    d = root / "archive/wiki/code-ref"
    out = []
    if not d.exists():
        return out
    for f in sorted(d.glob("*.md")):
        cid = f.stem
        if cid == "index":
            continue
        text = read(f)
        name = h1_title(text, cid)
        # 抓所有「對應考點：」開頭那一行內的 topicId
        topics = []
        for line in text.splitlines():
            if '對應考點' in line:
                topics.extend(RE_TOPIC.findall(line))
        out.append({"id": cid, "name": name, "topics": sorted(set(topics))})
    return out


def scan_traps(root):
    d = root / "archive/wiki/traps"
    out = []
    if not d.exists():
        return out
    problems_by_trap = {}
    prob_dir = root / "archive/wiki/problems"
    trap_ids = {f.stem for f in d.glob("*.md") if f.stem != "index"}
    if prob_dir.exists():
        for pf in prob_dir.glob("*.md"):
            text = read(pf)
            for tid in RE_WIKILINK.findall(text):
                if tid in trap_ids:
                    problems_by_trap.setdefault(tid, [])
                    if pf.stem not in problems_by_trap[tid]:
                        problems_by_trap[tid].append(pf.stem)
    for f in sorted(d.glob("*.md")):
        tid = f.stem
        if tid == "index":
            continue
        text = read(f)
        name = h1_title(text, tid)
        rel_kind, rel_id = TRAP_RELATION.get(tid, (None, None))
        out.append({
            "id": tid, "name": name,
            "problems": problems_by_trap.get(tid, []),
            "concept": rel_id if rel_kind == "concept" else None,
            "method": rel_id if rel_kind == "method" else None,
        })
    return out


def build(root: Path):
    problems = load_json_problems(root)
    concepts, known_concept_ids = load_json_concepts(root)
    concept_problems = scan_concept_problems(root, known_concept_ids)
    methods = scan_methods(root, known_concept_ids)
    philosophy = scan_philosophy(root)
    diagnosis = scan_diagnosis(root, known_concept_ids)
    coderef = scan_coderef(root)
    failuremodes = [{"id": k, "name": k, **v} for k, v in THEMATIC_FAILUREMODES.items()]
    materials = [{"id": k, "name": k, **v} for k, v in THEMATIC_MATERIALS.items()]
    traps = scan_traps(root)

    # 用 problems 的 primaryTopicId 回填 philosophy 的 topics（philosophy 檔本身無顯式標記）
    prob_topic = {p["id"]: p["pt"] for p in problems}
    for ph in philosophy:
        topics = set()
        for pid in ph["problems"]:
            if pid in prob_topic:
                topics.add(prob_topic[pid])
        ph["topics"] = sorted(topics)

    # 讀真正的標題（failure-modes / materials 用檔案 H1，覆蓋掉暫用的 id 當 name）
    for lst, subdir in [(failuremodes, "archive/wiki/failure-modes"), (materials, "archive/wiki/materials")]:
        for item in lst:
            f = root / subdir / f"{item['id']}.md"
            if f.exists():
                item["name"] = h1_title(read(f), item["id"])

    warnings = []
    all_concept_ids = known_concept_ids
    for cid in concept_problems:
        if cid not in all_concept_ids:
            warnings.append(f"[警告] concept_problems 內 {cid} 不在 concepts.json 中")

    bundle = {
        "topics": TOPICS, "problems": problems, "concepts": concepts,
        "concept_problems": concept_problems, "methods": methods,
        "philosophy": philosophy, "diagnosis": diagnosis, "coderef": coderef,
        "failuremodes": failuremodes, "materials": materials, "traps": traps,
    }
    return bundle, warnings


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RC 知識庫｜知識圖譜</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
<style>
  :root{
    --c-topic:#EC4899; --c-problem:#3B82F6; --c-concept:#10B981; --c-method:#8B5CF6;
    --c-philosophy:#F97316; --c-diagnosis:#06B6D4; --c-trap:#EF4444; --c-coderef:#6B7280;
    --c-failuremode:#9F1239; --c-material:#92400E;
    --bg:#0f1420; --panel:#161d2e; --panel2:#1d2740; --text:#e6ebf5; --muted:#93a0c2; --line:#2a3654;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;height:100%;background:var(--bg);color:var(--text);font-family:-apple-system,"Segoe UI","Noto Sans TC",sans-serif;}
  #app{display:flex;height:100vh;width:100vw;overflow:hidden;}
  #sidebar{width:340px;min-width:340px;background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column;overflow:hidden;}
  #cy{flex:1;position:relative;background:radial-gradient(ellipse at 30% 20%, #131a2b 0%, #0b0f18 70%);}
  .sb-section{padding:14px 16px;border-bottom:1px solid var(--line);}
  h1{font-size:16px;margin:0 0 2px;font-weight:700;}
  .sub{color:var(--muted);font-size:11.5px;margin:0 0 10px;}
  input#search{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;}
  input#search:focus{outline:2px solid #3b82f680;}
  .legend-item{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:12.5px;cursor:pointer;user-select:none;}
  .legend-item:hover{color:#fff;}
  .dot{width:11px;height:11px;border-radius:50%;flex:0 0 auto;box-shadow:0 0 0 2px rgba(255,255,255,.08);}
  .legend-item.off{opacity:.35;}
  .legend-item .cnt{margin-left:auto;color:var(--muted);font-size:11px;}
  .edge-toggle{display:flex;align-items:center;gap:7px;padding:4px 0;font-size:12px;color:var(--muted);cursor:pointer;}
  .edge-toggle input{accent-color:#3b82f6;}
  #detail{flex:1;overflow-y:auto;padding:14px 16px;}
  #detail.empty{display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:12.5px;text-align:center;}
  .d-type{display:inline-block;font-size:10.5px;padding:2px 8px;border-radius:20px;color:#0b0f18;font-weight:700;margin-bottom:8px;}
  .d-title{font-size:15px;font-weight:700;margin:0 0 6px;line-height:1.4;}
  .d-meta{font-size:12px;color:var(--muted);margin-bottom:10px;line-height:1.7;}
  .d-meta b{color:var(--text);font-weight:600;}
  .tag{display:inline-block;background:var(--panel2);border:1px solid var(--line);color:var(--muted);font-size:11px;padding:2px 7px;border-radius:5px;margin:0 4px 4px 0;}
  .d-link{display:inline-block;margin-top:10px;padding:8px 12px;background:#3b82f6;color:#fff;text-decoration:none;font-size:12.5px;border-radius:7px;font-weight:600;}
  .d-link:hover{background:#2563eb;}
  .d-rel-h{font-size:11.5px;color:var(--muted);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.04em;}
  .d-rel{display:block;width:100%;text-align:left;background:var(--panel2);border:1px solid var(--line);color:var(--text);padding:7px 9px;border-radius:6px;font-size:12px;margin-bottom:5px;cursor:pointer;}
  .d-rel:hover{border-color:#3b82f6;}
  .d-rel .rt{color:var(--muted);font-size:10.5px;margin-left:6px;}
  #topbar{position:absolute;top:12px;left:12px;right:12px;display:flex;gap:8px;z-index:5;pointer-events:none;}
  #topbar>*{pointer-events:auto;}
  .btn{background:var(--panel);border:1px solid var(--line);color:var(--text);padding:7px 12px;border-radius:8px;font-size:12.5px;cursor:pointer;}
  .btn:hover{border-color:#3b82f6;}
  #stats{margin-left:auto;color:var(--muted);font-size:11.5px;background:var(--panel);border:1px solid var(--line);padding:7px 12px;border-radius:8px;}
  #hint{position:absolute;bottom:12px;left:12px;font-size:11px;color:var(--muted);background:rgba(22,29,46,.85);padding:6px 10px;border-radius:6px;z-index:5;}
  ::-webkit-scrollbar{width:8px;}
  ::-webkit-scrollbar-thumb{background:#2a3654;border-radius:4px;}
</style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <div class="sb-section">
      <h1>RC 知識庫｜知識圖譜</h1>
      <p class="sub">鋼筋混凝土設計與預力 · 考題 / 概念 / 方法 / 診斷全景圖</p>
      <input id="search" placeholder="搜尋題號、概念、標籤…" autocomplete="off">
    </div>
    <div class="sb-section" id="legendBox">
      <div class="d-rel-h" style="margin-top:0">節點類型（點擊切換顯示）</div>
      <div id="legend"></div>
    </div>
    <div class="sb-section">
      <div class="d-rel-h" style="margin-top:0">連結類型</div>
      <div id="edgeToggles"></div>
    </div>
    <div id="detail" class="empty">點選一個節點查看詳情</div>
  </div>
  <div id="cy">
    <div id="topbar">
      <button class="btn" id="btnFit">重置視圖</button>
      <button class="btn" id="btnLayout">重新排版</button>
      <div id="stats"></div>
    </div>
    <div id="hint">滾輪縮放 · 拖曳平移 · 點節點看詳情 · 點空白處清除選取</div>
  </div>
</div>

<script>
/* ===================== 資料層（由 generate_knowledge_graph.py 產生） ===================== */
const BUNDLE = __BUNDLE_JSON__;
const TOPICS = BUNDLE.topics;
const PROBLEMS = BUNDLE.problems;
const CONCEPTS = BUNDLE.concepts;
const CONCEPT_PROBLEMS = BUNDLE.concept_problems;
const METHODS = BUNDLE.methods;
const PHILOSOPHY = BUNDLE.philosophy.map(x=>({id:x.id,name:x.name,topics:x.topics,problems:x.problems,concepts:x.concepts||[],methods:x.methods||[]}));
const DIAGNOSIS = BUNDLE.diagnosis;
const CODEREF = BUNDLE.coderef;
const FAILUREMODES = BUNDLE.failuremodes;
const MATERIALS = BUNDLE.materials;
const TRAPS = BUNDLE.traps;

/* ===================== 型別中繼資料 ===================== */
const TYPE_META = {
  topic:{color:"var(--c-topic)",label:"命題單元"},
  problem:{color:"var(--c-problem)",label:"考題"},
  concept:{color:"var(--c-concept)",label:"概念"},
  method:{color:"var(--c-method)",label:"解題方法"},
  philosophy:{color:"var(--c-philosophy)",label:"設計哲學"},
  diagnosis:{color:"var(--c-diagnosis)",label:"題型診斷"},
  trap:{color:"var(--c-trap)",label:"陷阱"},
  coderef:{color:"var(--c-coderef)",label:"規範條文"},
  failuremode:{color:"var(--c-failuremode)",label:"失敗模式"},
  material:{color:"var(--c-material)",label:"材料行為"}
};
const FILE_DIR = {
  problem:"archive/wiki/problems", concept:"archive/wiki/concepts", method:"archive/wiki/methods",
  philosophy:"archive/wiki/philosophy", diagnosis:"archive/wiki/diagnosis", coderef:"archive/wiki/code-ref",
  failuremode:"archive/wiki/failure-modes", material:"archive/wiki/materials", trap:"archive/wiki/traps"
};

/* ===================== 組裝節點與邊 ===================== */
const nodes = [];
const edgeSet = new Map();
function nid(type,id){return type+":"+id;}
function addNode(type,id,label,extra){
  nodes.push({data:Object.assign({id:nid(type,id),ntype:type,label:label,rawId:id,
    file: type==="topic"?null: FILE_DIR[type]+"/"+id+".md"}, extra||{})});
}
function addEdge(sType,sId,tType,tId,kind){
  const s=nid(sType,sId), t=nid(tType,tId);
  const key=[s,t,kind].sort().join("|")+"|"+kind;
  if(edgeSet.has(key))return;
  edgeSet.set(key,{data:{id:"e"+edgeSet.size,source:s,target:t,kind:kind}});
}

TOPICS.forEach(([id,name])=>addNode("topic",id,name,{}));

PROBLEMS.forEach(pr=>{
  addNode("problem",pr.id,pr.id,{year:pr.y,pt:pr.pt,st:pr.st,dm:pr.dm,tags:pr.tags});
  addEdge("problem",pr.id,"topic",pr.pt,"primary-topic");
  (pr.st||[]).forEach(s=>addEdge("problem",pr.id,"topic",s,"secondary-topic"));
});

CONCEPTS.forEach(cn=>{
  addNode("concept",cn.id,cn.name,{cls:cn.cls,formula:cn.formula,desc:cn.desc});
  addEdge("concept",cn.id,"topic",cn.cls,"classification");
  (cn.rel||[]).forEach(r=>addEdge("concept",cn.id,"concept",r,"concept-relation"));
});
Object.keys(CONCEPT_PROBLEMS).forEach(cid=>{
  CONCEPT_PROBLEMS[cid].forEach(pid=>addEdge("concept",cid,"problem",pid,"appears-in"));
});

METHODS.forEach(mt=>{
  addNode("method",mt.id,mt.name,{});
  (mt.topics||[]).forEach(t=>addEdge("method",mt.id,"topic",t,"applies-to"));
  (mt.problems||[]).forEach(pid=>addEdge("method",mt.id,"problem",pid,"appears-in"));
  (mt.concepts||[]).forEach(cid=>addEdge("method",mt.id,"concept",cid,"uses-concept"));
});

PHILOSOPHY.forEach(phl=>{
  addNode("philosophy",phl.id,phl.name,{});
  (phl.topics||[]).forEach(t=>addEdge("philosophy",phl.id,"topic",t,"applies-to"));
  (phl.problems||[]).forEach(pid=>addEdge("philosophy",phl.id,"problem",pid,"discusses"));
  (phl.concepts||[]).forEach(cid=>addEdge("philosophy",phl.id,"concept",cid,"uses-concept"));
  (phl.methods||[]).forEach(mid=>addEdge("philosophy",phl.id,"method",mid,"uses-method"));
});

DIAGNOSIS.forEach(dgn=>{
  addNode("diagnosis",dgn.id,dgn.name,{});
  (dgn.topics||[]).forEach(t=>addEdge("diagnosis",dgn.id,"topic",t,"covers"));
  (dgn.problems||[]).forEach(pid=>addEdge("diagnosis",dgn.id,"problem",pid,"references"));
  (dgn.concepts||[]).forEach(cid=>addEdge("diagnosis",dgn.id,"concept",cid,"uses-concept"));
});

CODEREF.forEach(cr=>{
  addNode("coderef",cr.id,cr.name,{});
  (cr.topics||[]).forEach(t=>addEdge("coderef",cr.id,"topic",t,"covers"));
});

FAILUREMODES.forEach(fm=>{
  addNode("failuremode",fm.id,fm.name,{});
  (fm.topics||[]).forEach(t=>addEdge("failuremode",fm.id,"topic",t,"relates-to"));
  (fm.concepts||[]).forEach(cid=>addEdge("failuremode",fm.id,"concept",cid,"relates-to"));
});

MATERIALS.forEach(mat=>{
  addNode("material",mat.id,mat.name,{});
  (mat.topics||[]).forEach(t=>addEdge("material",mat.id,"topic",t,"relates-to"));
  (mat.concepts||[]).forEach(cid=>addEdge("material",mat.id,"concept",cid,"relates-to"));
});

TRAPS.forEach(t=>{
  addNode("trap",t.id,t.name,{});
  (t.problems||[]).forEach(pid=>addEdge("trap",t.id,"problem",pid,"trap-in"));
  if(t.concept) addEdge("trap",t.id,"concept",t.concept,"relates-to");
  if(t.method) addEdge("trap",t.id,"method",t.method,"relates-to");
});

const edges = Array.from(edgeSet.values());
const elements = nodes.concat(edges);

/* ===================== Cytoscape ===================== */
const EDGE_KIND_META = {
  "primary-topic":{label:"主分類 → 命題單元",color:"#3B82F680",width:2.4},
  "secondary-topic":{label:"副分類 → 命題單元",color:"#3B82F640",width:1.2,dashed:true},
  "classification":{label:"概念 → 命題單元",color:"#10B98180",width:1.6},
  "concept-relation":{label:"概念關聯",color:"#10B98160",width:1.4,dashed:true},
  "appears-in":{label:"出現於考題",color:"#93a0c260",width:1.2},
  "applies-to":{label:"方法/哲學 → 命題單元",color:"#8B5CF680",width:1.6},
  "discusses":{label:"哲學討論考題",color:"#F9731660",width:1.2},
  "uses-concept":{label:"引用概念",color:"#10B98150",width:1,dashed:true},
  "uses-method":{label:"引用方法",color:"#8B5CF650",width:1,dashed:true},
  "covers":{label:"診斷/規範 → 命題單元",color:"#06B6D480",width:1.6},
  "references":{label:"診斷引用考題",color:"#06B6D460",width:1.2},
  "relates-to":{label:"主題關聯（推論）",color:"#93a0c240",width:1,dashed:true},
  "trap-in":{label:"陷阱出現於考題",color:"#EF444470",width:1.3}
};

const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: elements,
  style: [
    {selector:'node', style:{
      'background-color': ele=>getComputedColor(ele.data('ntype')),
      'label':'data(label)','color':'#e6ebf5','font-size':9,'text-wrap':'wrap','text-max-width':'90px',
      'text-valign':'bottom','text-margin-y':4,'text-outline-width':2,'text-outline-color':'#0b0f18',
      'width': ele=>nodeSize(ele), 'height': ele=>nodeSize(ele),
      'border-width':1.5,'border-color':'rgba(255,255,255,.25)'
    }},
    {selector:'node[ntype="topic"]', style:{'font-size':11,'font-weight':700,'border-width':2.5,'border-color':'#fff','text-outline-width':3}},
    {selector:'edge', style:{
      'width': e=>(EDGE_KIND_META[e.data('kind')]||{}).width||1,
      'line-color': e=>(EDGE_KIND_META[e.data('kind')]||{}).color||'#3a4666',
      'curve-style':'haystack','haystack-radius':0.2,
      'line-style': e=>(EDGE_KIND_META[e.data('kind')]||{}).dashed?'dashed':'solid',
      'opacity':0.85
    }},
    {selector:'.faded', style:{'opacity':0.06}},
    {selector:'.highlighted', style:{'opacity':1}},
    {selector:'node.highlighted', style:{'border-width':3,'border-color':'#fff'}},
    {selector:'node.selected', style:{'border-width':4,'border-color':'#fff','background-color':'#fff'}}
  ],
  layout:{name:'cose', animate:false, nodeRepulsion:9000, idealEdgeLength:70, nestingFactor:1.2, gravity:45, numIter:1200, componentSpacing:110}
});
function getComputedColor(t){
  const v = getComputedStyle(document.documentElement).getPropertyValue('--c-'+t).trim();
  return v || '#888';
}
function nodeSize(ele){
  if(ele.data('ntype')==='topic') return 34;
  const deg = ele.degree ? ele.degree() : 0;
  return Math.max(10, Math.min(28, 8 + deg*1.6));
}

/* ===================== 互動：篩選 / 圖例 ===================== */
const activeTypes = new Set(Object.keys(TYPE_META));
const activeKinds = new Set(Object.keys(EDGE_KIND_META));

function countByType(t){ return nodes.filter(n=>n.data.ntype===t).length; }

function renderLegend(){
  const box = document.getElementById('legend');
  box.innerHTML='';
  Object.keys(TYPE_META).forEach(t=>{
    const meta = TYPE_META[t];
    const div = document.createElement('div');
    div.className='legend-item';
    div.innerHTML = `<span class="dot" style="background:${meta.color}"></span><span>${meta.label}</span><span class="cnt">${countByType(t)}</span>`;
    div.onclick = ()=>{
      if(activeTypes.has(t)) activeTypes.delete(t); else activeTypes.add(t);
      div.classList.toggle('off');
      applyFilter();
    };
    box.appendChild(div);
  });
}
function renderEdgeToggles(){
  const box = document.getElementById('edgeToggles');
  box.innerHTML='';
  const seen = new Set();
  edges.forEach(e=>seen.add(e.data.kind));
  Array.from(seen).forEach(k=>{
    const meta = EDGE_KIND_META[k]||{label:k};
    const id='ek_'+k;
    const div = document.createElement('label');
    div.className='edge-toggle';
    div.innerHTML = `<input type="checkbox" id="${id}" checked><span>${meta.label}</span>`;
    div.querySelector('input').onchange = (ev)=>{
      if(ev.target.checked) activeKinds.add(k); else activeKinds.delete(k);
      applyFilter();
    };
    box.appendChild(div);
  });
}
function applyFilter(){
  cy.batch(()=>{
    cy.nodes().forEach(n=>{
      const show = activeTypes.has(n.data('ntype'));
      n.style('display', show?'element':'none');
    });
    cy.edges().forEach(e=>{
      const kindOk = activeKinds.has(e.data('kind'));
      const endsOk = e.source().style('display')!=='none' && e.target().style('display')!=='none';
      e.style('display', (kindOk && endsOk) ? 'element':'none');
    });
  });
  document.getElementById('stats').textContent =
    cy.nodes(':visible').length + ' 節點 · ' + cy.edges(':visible').length + ' 連結';
}

/* ===================== 詳情面板 ===================== */
function fileTitleFor(type,id,label){ return label || id; }
function openWiki(type,id,label){
  const file = type==='topic'? null : FILE_DIR[type]+'/'+id+'.md';
  if(!file) return;
  window.open('index.html#md='+encodeURIComponent(file)+'&t='+encodeURIComponent(fileTitleFor(type,id,label)), '_blank');
}
function neighborsOf(ele){
  const rel = [];
  ele.connectedEdges().forEach(e=>{
    const other = e.source().id()===ele.id()? e.target() : e.source();
    rel.push({node:other, kind:e.data('kind')});
  });
  return rel;
}
function renderDetail(ele){
  const d = ele.data();
  const meta = TYPE_META[d.ntype];
  const panel = document.getElementById('detail');
  panel.classList.remove('empty');
  let html = `<span class="d-type" style="background:${meta.color}">${meta.label}</span>`;
  html += `<div class="d-title">${d.label}</div>`;
  let metaLines = '';
  if(d.ntype==='problem'){
    metaLines += `<div><b>年度：</b>${d.year}</div><div><b>設計法：</b>${d.dm}</div>`;
    if(d.tags && d.tags.length){
      html += `<div style="margin:8px 0 4px">`+d.tags.map(t=>`<span class="tag">${t}</span>`).join('')+`</div>`;
    }
  }
  if(d.ntype==='concept'){
    if(d.formula) metaLines += `<div><b>公式：</b>${d.formula}</div>`;
    if(d.desc) metaLines += `<div style="margin-top:6px">${d.desc}</div>`;
  }
  if(metaLines) html += `<div class="d-meta">${metaLines}</div>`;
  if(d.file){
    html += `<a class="d-link" href="javascript:void(0)" onclick='openWikiFromPanel("${d.ntype}","${d.rawId}")'>📖 在題庫中開啟原始頁面</a>`;
  }
  const rel = neighborsOf(ele);
  if(rel.length){
    html += `<div class="d-rel-h">關聯節點（${rel.length}）</div>`;
    rel.sort((a,b)=> a.node.data('ntype').localeCompare(b.node.data('ntype')));
    rel.forEach(r=>{
      const rn = r.node.data();
      const rm = TYPE_META[rn.ntype];
      html += `<button class="d-rel" onclick='selectNodeById("${rn.id}")'><span class="dot" style="background:${rm.color};display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px"></span>${rn.label}<span class="rt">${rm.label}</span></button>`;
    });
  }
  panel.innerHTML = html;
}
window.openWikiFromPanel = function(type,id){
  const n = cy.getElementById(nid(type,id));
  openWiki(type,id,n.data('label'));
};
window.selectNodeById = function(id){
  const n = cy.getElementById(id);
  if(n && n.length){
    cy.elements().unselect();
    n.select();
    cy.animate({center:{eles:n}, duration:300});
    highlightNeighborhood(n);
    renderDetail(n);
  }
};

function highlightNeighborhood(node){
  cy.elements().removeClass('faded highlighted');
  const neighborhood = node.closedNeighborhood();
  cy.elements().difference(neighborhood).addClass('faded');
  neighborhood.addClass('highlighted');
}

cy.on('tap','node', evt=>{
  const n = evt.target;
  cy.elements().unselect();
  n.select();
  highlightNeighborhood(n);
  renderDetail(n);
});
cy.on('tap', evt=>{
  if(evt.target === cy){
    cy.elements().removeClass('faded highlighted').unselect();
    document.getElementById('detail').className='empty';
    document.getElementById('detail').textContent='點選一個節點查看詳情';
  }
});

/* ===================== 搜尋 ===================== */
document.getElementById('search').addEventListener('input', (e)=>{
  const q = e.target.value.trim().toLowerCase();
  cy.elements().removeClass('faded highlighted');
  if(!q){ return; }
  const matched = cy.nodes().filter(n=>{
    const d = n.data();
    if(d.label && d.label.toLowerCase().includes(q)) return true;
    if(d.tags && d.tags.some(t=>t.toLowerCase().includes(q))) return true;
    if(d.rawId && d.rawId.toLowerCase().includes(q)) return true;
    return false;
  });
  if(matched.length===0) return;
  const nb = matched.closedNeighborhood();
  cy.elements().difference(nb).addClass('faded');
  nb.addClass('highlighted');
});

/* ===================== 頂部工具列 ===================== */
document.getElementById('btnFit').onclick = ()=>{ cy.fit(undefined, 40); };
document.getElementById('btnLayout').onclick = ()=>{
  cy.layout({name:'cose', animate:true, nodeRepulsion:9000, idealEdgeLength:70, gravity:45, numIter:1200, componentSpacing:110}).run();
};

renderLegend();
renderEdgeToggles();
applyFilter();
setTimeout(()=>cy.fit(undefined,40), 300);
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="exam-wiki-RC 專案根目錄路徑")
    ap.add_argument("--out", default=None, help="輸出檔名（預設 <root>/knowledge_graph.html）")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.out).resolve() if args.out else root / "knowledge_graph.html"

    bundle, warnings = build(root)
    html = TEMPLATE.replace("__BUNDLE_JSON__", json.dumps(bundle, ensure_ascii=False))
    out_path.write_text(html, encoding="utf-8")

    n_nodes = (len(bundle["topics"]) + len(bundle["problems"]) + len(bundle["concepts"])
               + len(bundle["methods"]) + len(bundle["philosophy"]) + len(bundle["diagnosis"])
               + len(bundle["coderef"]) + len(bundle["failuremodes"]) + len(bundle["materials"])
               + len(bundle["traps"]))
    print(f"已產生 {out_path}")
    print(f"節點數（依類別加總，非去重後 cytoscape 節點數）：{n_nodes}")
    print(f"  topics={len(bundle['topics'])} problems={len(bundle['problems'])} "
          f"concepts={len(bundle['concepts'])} methods={len(bundle['methods'])} "
          f"philosophy={len(bundle['philosophy'])} diagnosis={len(bundle['diagnosis'])} "
          f"coderef={len(bundle['coderef'])} failuremodes={len(bundle['failuremodes'])} "
          f"materials={len(bundle['materials'])} traps={len(bundle['traps'])}")
    for w in warnings:
        print(w)
    if not warnings:
        print("無警告。")


if __name__ == "__main__":
    sys.exit(main())
