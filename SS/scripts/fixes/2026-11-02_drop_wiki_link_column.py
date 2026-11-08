# 刪除解析 VHA 表中「補強頁」「概念連結」欄（指向 2026-11-01 已封存的 archive/wiki/ 頁，連結已失效）
# 用法：python3 scripts/fixes/2026-11-02_drop_wiki_link_column.py [--write]
import re, sys, glob
WRITE = "--write" in sys.argv
DROP = {"補強頁", "概念連結"}

def cells(line):
    s = line.strip()
    assert s.startswith("|"), line
    out, cur, math, i = [], "", False, 1
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            cur += s[i:i+2]; i += 2; continue
        if c == "$": math = not math
        if c == "|" and not math:
            out.append(cur); cur = ""
        else:
            cur += c
        i += 1
    if cur.strip(): out.append(cur)
    return out

tot_files = tot_rows = 0; problems = []
for p in sorted(glob.glob("raw/solutions/SS-*/SS-*.md")):
    if p.endswith("-problem.md"): continue
    L = open(p, encoding="utf-8").read().split("\n")
    changed = False; i = 0
    while i < len(L):
        if L[i].lstrip().startswith("|") and any(c.strip() in DROP for c in cells(L[i])):
            hdr = cells(L[i]); n = len(hdr)
            k = [j for j, c in enumerate(hdr) if c.strip() in DROP][0]
            j = i
            while j < len(L) and L[j].lstrip().startswith("|"):
                c = cells(L[j])
                if len(c) != n:
                    problems.append(f"{p}:{j+1} 欄數 {len(c)}≠{n}")
                    j += 1; continue
                del c[k]
                L[j] = "|" + "|".join(c) + "|"
                tot_rows += 1; j += 1
            changed = True; i = j
        else:
            i += 1
    if changed:
        tot_files += 1
        if WRITE: open(p, "w", encoding="utf-8").write("\n".join(L))
print("files", tot_files, "rows", tot_rows, "write" if WRITE else "dry-run")
print("\n".join(problems) or "欄數全部一致")
