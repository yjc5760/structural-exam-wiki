#!/usr/bin/env python3
"""SD-U1-3 批 3：audit-ledger-SD.json 寫入盲解比對、勘誤、落實檢查結果；question_index.json 追加勘誤題 tags。可重複執行。
用法：python3 <本檔> <SD 科目資料夾> <盲解結果 json>"""
import sys, re, json
from pathlib import Path
SD = Path(sys.argv[1]); R = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")); D = "2026-11-15"
FIXED = {"SD-2021-2", "SD-2021-3", "SD-2021-4", "SD-2022-3"}
lp = SD/"wiki/queries/audit-ledger-SD.json"; led = json.loads(lp.read_text(encoding="utf-8"))
for qid, r in R.items():
    e = led.get(qid) or {}
    e.update({"date": D, "model": "claude-opus-5-5", "result": r["result"], "source": r["source"],
              "report": "wiki/queries/盲解比對-SD-U1-3-批3-2026-11-15.md", "scope": "SD-U1-3 批 3（pipeline）",
              "human": r["human"], "fixed": D if qid in FIXED else ""})
    e["recheck"] = ({"date": D, "result": "落實", "report": "wiki/queries/落實檢查-SD-U1-3-批3-2026-11-15.md",
                     "note": "非獨立複核（勘誤與落實檢查同一工作階段）"} if qid in FIXED
                    else {"date": "", "result": "", "report": "", "note": ""})
    e.setdefault("history", []); led[qid] = e
assert all((led[q]["result"] != "一致") == (q in FIXED) for q in R)
lp.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
TAGS = {"SD-2021-2": ["阻尼脈衝反應", "分段閉合解", "題給阻尼比"],
        "SD-2021-3": ["初始變形形狀", "題意勘誤", "層剪力上確界"],
        "SD-2021-4": ["振幅判讀", "題意勘誤", "等能量法則", "彈塑性時間歷時"],
        "SD-2022-3": ["動力分析門檻", "規範條文"]}
ip = SD/"raw/json/question_index.json"; raw = ip.read_text(encoding="utf-8")
for qid, add in TAGS.items():
    m = re.search(r'\{\s*"moduleId": "%s",.*?"tags": \[(.*?)\]' % qid, raw, re.S); assert m, qid
    cur = json.loads("[" + m.group(1) + "]"); new = [t for t in add if t not in cur]
    if not new: continue
    body = m.group(1).rstrip(); ind = re.search(r'\n(\s*)"', m.group(1))
    sep = (",\n" + ind.group(1)) if ind else ", "
    ins = body + sep + sep.lstrip(",").join(json.dumps(t, ensure_ascii=False) for t in new) if False else body + "".join(sep + json.dumps(t, ensure_ascii=False) for t in new)
    raw = raw[:m.start(1)] + ins + m.group(1)[len(body):] + raw[m.end(1):]
d = json.loads(raw); Q = d["questions"] if isinstance(d, dict) else d
for x in Q:
    if x["moduleId"] in TAGS: assert all(t in x["tags"] for t in TAGS[x["moduleId"]]); assert x["verificationStatus"] != "verified"
ip.write_text(raw, encoding="utf-8"); print("ok", len(R))
