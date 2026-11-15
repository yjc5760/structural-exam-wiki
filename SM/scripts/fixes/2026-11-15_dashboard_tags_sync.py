#!/usr/bin/env python3
"""只把 question_index.json 的 tags 同步到 dashboard-data.js 的 SM_QUESTIONS 第 5 欄（不跑 refresh_dashboard.py，見 SUBJECT.md §10）。可重複執行。"""
import json, re
from pathlib import Path
SM = Path(__file__).resolve().parents[2]
q = json.loads((SM/"raw/json/question_index.json").read_text(encoding="utf-8"))
tags = {x["moduleId"]: x.get("tags", []) for x in q["questions"]}
p = SM/"dashboard-data.js"; s = p.read_text(encoding="utf-8")
m = re.search(r"window\.SM_QUESTIONS = (\[.*?\]);\n", s, re.S)
rows = json.loads(m.group(1)); ch = []
for r in rows:
    if r[4] != tags[r[0]]: ch.append(r[0]); r[4] = tags[r[0]]
s = s[:m.start(1)] + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + s[m.end(1):]
p.write_text(s, encoding="utf-8"); print("updated", ch)
