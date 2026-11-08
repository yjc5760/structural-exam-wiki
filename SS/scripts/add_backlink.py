#!/usr/bin/env python3
"""在 exam-wiki-SS 的學習頁頂部插入「← 從這裡開始」返回列。
用法：python add_backlink.py <repo 根目錄>
- 處理 study/*.html 與 影片講義/*.html
- 已插入過的頁面會跳過（以 id="start-backlink" 判斷），可重複執行
"""
import re
import sys
from pathlib import Path

BAR = ('<style>@media print{#start-backlink{display:none}}</style>'
       '<div id="start-backlink" style="font:14px/1.6 \'Noto Sans TC\',system-ui,sans-serif;padding:8px 16px;background:#2f4a5e;color:#fff"><a href="{href}" style="color:#fff;text-decoration:none">← 從這裡開始（SS 學習路徑）</a></div>')

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
changed = []
for sub in ("study", "影片講義"):
    for f in sorted((root / sub).glob("*.html")):
        s = f.read_text(encoding="utf-8")
        if 'id="start-backlink"' in s:
            continue
        m = re.search(r"<body[^>]*>", s, re.I)
        if not m:
            print("略過（找不到 <body>）:", f)
            continue
        s = s[:m.end()] + "\n" + BAR.replace("{href}", "../start.html") + s[m.end():]
        f.write_text(s, encoding="utf-8")
        changed.append(f)
for f in changed:
    print(f.relative_to(root))
print(f"共 {len(changed)} 個檔案")
