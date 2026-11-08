"""由 segments.py 產生審閱用講稿 講稿.md（旁白＋估計秒數＋黑板分鏡）。
用法：python script_md.py
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from segments import SEGMENTS, CHAPTERS, BOARD
import segments

seg = dict(SEGMENTS)
lines, tot = [], 0
for _, name, keys in CHAPTERS:
    lines += [f"## {name}", ""]
    for k in keys:
        t = re.sub(r"\s*<[^>]+>\s*", "", seg[k]); s = len(t) / 4.6 + 0.6; tot += s
        lines += [f"**{k}**（約 {s:.0f} 秒）　{t}", "", f"　🖍 黑板：{BOARD.get(k, '')}", ""]
head = [f"# {getattr(segments, 'PROBLEM_ID', '')} 講稿（待確認）", "",
        "> 由 segments.py 產生，改稿請改 segments.py。估計時長以每秒 4.6 字計；實際配音通常再長 10–20%。", "",
        f"**合計約 {tot / 60:.1f} 分鐘（{tot:.0f} 秒）**", ""]
open(os.path.join(HERE, "講稿.md"), "w", encoding="utf-8").write("\n".join(head + lines))
print(f"講稿.md：{len(SEGMENTS)} 段，約 {tot / 60:.1f} 分鐘")
