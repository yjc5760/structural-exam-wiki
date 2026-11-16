#!/usr/bin/env python3
"""SD-2013-3 解析標頭主副分類同步 question_index（主 SD-U1-2、副 SD-U1-3；非勘誤，答案不變）。
依據：盲解比對 B-U1-2-G2（2026-11-16）、SD/SUBJECT.md §2 同型題歸法。可重複執行。用法：python3 <本檔> <SD 科目資料夾>"""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "raw/solutions/SD-2013-3/SD-2013-3.md"; t = p.read_text(encoding="utf-8")
old = "**主分類：** `SD-U1-3` 單自由度、多自由度系統之動態分析及應用\n**副分類：** `SD-U1-2` 運動方程式推導"
new = "**主分類：** `SD-U1-2` 運動方程式推導\n**副分類：** `SD-U1-3` 單自由度、多自由度系統之動態分析及應用"
if new in t: print("skip"); sys.exit()
assert old in t
t = t.replace(old, new, 1).rstrip("\n") + "\n\n*修正日期：2026-11-16（非勘誤）分類標頭同步索引：主分類 SD-U1-2、副分類 SD-U1-3（原標頭主副對調；答案不變）*\n"
p.write_text(t, encoding="utf-8"); print("done")
