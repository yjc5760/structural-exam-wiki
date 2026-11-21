#!/usr/bin/env python3
"""從影片資料夾產生 YouTube 章節時間碼。

用法：python yt_chapters.py <video 資料夾>
讀取：講稿.md（"## 章名" 之後第一個 "**sNN**" 為該章起點）＋ timeline.json（[[段號, 起, 訖], ...]）
輸出：章節清單（m:ss 章名），第一章強制 0:00；並印出影片總長供核對。
"""
import json, re, sys, pathlib

def fmt(t):
    t = int(t)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main(folder):
    d = pathlib.Path(folder)
    tl = {seg: start for seg, start, _ in json.loads((d / "timeline.json").read_text(encoding="utf-8"))}
    end = max(e for _, _, e in json.loads((d / "timeline.json").read_text(encoding="utf-8")))
    chapters, pending = [], None
    for line in (d / "講稿.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            pending = m.group(1).replace("　", " ").strip()
            continue
        m = re.match(r"^\*\*(s\d+)\*\*", line)
        if m and pending:
            chapters.append((tl.get(m.group(1), 0.0), pending))
            pending = None
    if not chapters:
        sys.exit("找不到章節：講稿.md 需有 '## 章名' 與 '**sNN**' 段落")
    chapters[0] = (0.0, chapters[0][1])
    for t, name in chapters:
        print(f"{fmt(t)} {name}")
    print(f"# 配音總長 {fmt(end)}（成片若有片頭，章節時間要加上片頭秒數）", file=sys.stderr)
    if len(chapters) < 3:
        print("# 注意：YouTube 章節至少要 3 個、每段至少 10 秒", file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
