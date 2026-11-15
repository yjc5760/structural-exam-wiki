#!/usr/bin/env python3
"""合併 2026-11-15 平行批次（G1–G9）的暫存片段到 SM 共用檔。
  python SM/scripts/fixes/2026-11-15_merge_staging.py [--dry]
- index-patch.json → raw/json/question_index.json（problemStatus、tags_add、tags_remove；不碰 verificationStatus）
- ledger.json      → wiki/queries/audit-ledger-SM.json（逐題整筆覆寫）
- log.md           → wiki/queries/log.md（append；已 append 過的組別以標記行跳過，可重複執行）
"""
import json, sys
from pathlib import Path
SM = Path(__file__).resolve().parents[2]
ST = SM / "wiki/queries/_staging"
dry = "--dry" in sys.argv
groups = sorted(p for p in ST.iterdir() if p.is_dir())

qp = SM / "raw/json/question_index.json"
q = json.loads(qp.read_text(encoding="utf-8"))
Q = q["questions"] if isinstance(q, dict) else q
byid = {x["moduleId"]: x for x in Q}
lp = SM / "wiki/queries/audit-ledger-SM.json"
led = json.loads(lp.read_text(encoding="utf-8"))
logp = SM / "wiki/queries/log.md"
log = logp.read_text(encoding="utf-8")

n_idx = n_led = 0; logs = []
for g in groups:
    ip = g / "index-patch.json"
    if ip.exists():
        for qid, p in json.loads(ip.read_text(encoding="utf-8")).items():
            x = byid[qid]
            assert "verificationStatus" not in p, (g.name, qid)
            if "problemStatus" in p: x["problemStatus"] = p["problemStatus"]
            tags = x.setdefault("tags", [])
            for t in p.get("tags_remove", []):
                if t in tags: tags.remove(t)
            for t in p.get("tags_add", []):
                if t not in tags: tags.append(t)
            for k, v in p.items():
                if k not in ("problemStatus", "tags_add", "tags_remove"):
                    x[k] = v
            n_idx += 1
    gp = g / "ledger.json"
    if gp.exists():
        for qid, e in json.loads(gp.read_text(encoding="utf-8")).items():
            assert qid in byid, qid
            led[qid] = e; n_led += 1
    mp = g / "log.md"
    mark = f"<!-- merged-staging 2026-11-15 {g.name} -->"
    if mp.exists() and mark not in log:
        logs.append("\n" + mark + "\n" + mp.read_text(encoding="utf-8").strip() + "\n")

print(f"index 題數 {n_idx}、ledger 題數 {n_led}、log 組數 {len(logs)}；ledger 總數 {len(led)}")
if not dry:
    qp.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lp.write_text(json.dumps(dict(sorted(led.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if logs: logp.write_text(log.rstrip("\n") + "\n" + "".join(logs), encoding="utf-8")
