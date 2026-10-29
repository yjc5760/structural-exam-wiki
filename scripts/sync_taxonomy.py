#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_taxonomy.py — 把根目錄 syllabus_taxonomy.json（唯一正本）同步到各科 XX/raw/json/

為什麼要副本：unit-exam-intel、unit-formula-map、subject-frequency-map 等 skill 以
「科目資料夾」為工作目錄，預設讀 raw/json/syllabus_taxonomy.json。副本只為相容，
**改分類一律改根目錄正本，再執行本腳本**；不要手改副本。

用法（在知識庫根目錄執行）：
    python scripts/sync_taxonomy.py          # 同步所有已存在的科目資料夾
    python scripts/sync_taxonomy.py --check  # 只檢查副本是否與正本一致
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "syllabus_taxonomy.json")
NOTICE = ("本檔為副本，正本在知識庫根目錄 syllabus_taxonomy.json。"
          "請勿修改本檔；改正本後執行 python scripts/sync_taxonomy.py")


def render():
    with open(MASTER, encoding="utf-8") as f:
        d = json.load(f)
    d["_meta"] = dict(d.get("_meta", {}), source="命題大綱.pdf（知識庫根目錄）", copyNotice=NOTICE)
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def main():
    check = "--check" in sys.argv
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    text = render()
    with open(MASTER, encoding="utf-8") as f:
        ids = [s["id"] for s in json.load(f)["subjects"]]
    bad = 0
    for sid in ids:
        jdir = os.path.join(ROOT, sid, "raw", "json")
        if not os.path.isdir(jdir):
            continue
        p = os.path.join(jdir, "syllabus_taxonomy.json")
        cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if cur == text:
            print(f"[{sid}] 一致")
            continue
        bad += 1
        if check:
            print(f"[{sid}] ⚠️ 副本與正本不一致（或不存在）")
        else:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print(f"[{sid}] 已同步")
    sys.exit(1 if (check and bad) else 0)


if __name__ == "__main__":
    main()
