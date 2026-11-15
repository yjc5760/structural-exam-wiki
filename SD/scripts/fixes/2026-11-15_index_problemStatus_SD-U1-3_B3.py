#!/usr/bin/env python3
"""SD-U1-3 批 3（2017–2025，16 題）題目正本確認後：question_index.json 寫入 problemStatus: confirmed。可重複執行。
用法：python3 <本檔> <SD 科目資料夾>"""
import sys, re, json
from pathlib import Path
SD = Path(sys.argv[1])
IDS = ["SD-2017-1","SD-2019-1","SD-2019-2","SD-2019-3","SD-2020-2","SD-2020-3","SD-2021-1","SD-2021-2",
       "SD-2021-3","SD-2021-4","SD-2022-1","SD-2022-3","SD-2023-2","SD-2024-1","SD-2025-2","SD-2025-3"]
p = SD/"raw/json/question_index.json"; raw = p.read_text(encoding="utf-8")
for qid in IDS:
    assert "判讀狀態 | **已確認**" in (SD/f"raw/solutions/{qid}/{qid}-problem.md").read_text(encoding="utf-8"), qid
    pat = re.compile(r'(\{\s*"moduleId": "%s",.*?"verificationStatus": "[^"]*")(,\s*"problemStatus": "[^"]*")?' % qid, re.S)
    m = pat.search(raw); assert m, qid
    ind = re.search(r'\n(\s*)"verificationStatus"', m.group(1)).group(1)
    raw = raw[:m.start()] + m.group(1) + f',\n{ind}"problemStatus": "confirmed"' + raw[m.end():]
d = json.loads(raw)
Q = d["questions"] if isinstance(d, dict) else d
assert sum(1 for x in Q if x.get("moduleId") in IDS and x.get("problemStatus") == "confirmed") == 16
p.write_text(raw, encoding="utf-8"); print("ok")
