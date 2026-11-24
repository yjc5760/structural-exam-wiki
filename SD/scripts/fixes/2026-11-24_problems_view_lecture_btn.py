"""problems-view 頁首「講義」鈕同步（2026-11-24，新增 lecture-SD-U2-3、U3-1 後）。
規則沿用 UNIT-OVERVIEW-SD：主分類有講義就連主分類，否則連第一個有講義的副分類；都沒有就不放。可重跑。"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
qs = json.load(open(os.path.join(ROOT, 'raw/json/question_index.json'), encoding='utf-8'))['questions']
tax = json.load(open(os.path.join(ROOT, '..', 'syllabus_taxonomy.json'), encoding='utf-8'))
names = {}
def walk(o):
    if isinstance(o, dict):
        if 'id' in o and 'name' in o and str(o['id']).startswith('SD-U'): names[o['id']] = o['name']
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(tax)
have = {u for u in names if os.path.exists(os.path.join(ROOT, 'study', f'lecture-{u}.html'))}
changed = 0
for q in qs:
    p = os.path.join(ROOT, 'study/problems-view', q['moduleId'] + '.html')
    if not os.path.exists(p): continue
    cands = [q.get('primaryTopicId')] + list(q.get('secondaryTopicIds') or [])
    tgt = next((u for u in cands if u in have), None)
    s = open(p, encoding='utf-8').read(); s0 = s
    s = re.sub(r'\n<a class="lect"  id="btnLect"[^\n]*</a>', '', s)
    if tgt:
        short = tgt.replace('SD-', '')
        btn = (f'\n<a class="lect"  id="btnLect"  href="../lecture-{tgt}.html" title="{tgt} {names[tgt]} 觀念講義">'
               f'&#128218; {short} {names[tgt]} 講義</a>')
        m = re.search(r'<a class="quick" id="btnStudy"[^\n]*</a>', s)
        if not m: raise SystemExit('no btnStudy in ' + p)
        s = s[:m.end()] + btn + s[m.end():]
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s); changed += 1
print('lectures:', sorted(have)); print('changed pages:', changed)
