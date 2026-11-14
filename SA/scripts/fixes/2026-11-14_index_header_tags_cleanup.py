import json,re,os,collections
os.chdir(os.path.expanduser('~/mnt/structural-exam-wiki/SA'))
IDX='raw/json/question_index.json'
raw=open(IDX,encoding='utf-8').read()
d=json.loads(raw); Q={q['moduleId']:q for q in d['questions']}
NAMES={'SA-U1-1':'靜不定度與穩定性之判斷','SA-U1-2':'靜定結構之分析','SA-U1-3':'靜定及靜不定結構影響線','SA-U2-1':'靜不定結構最小功法','SA-U2-2':'靜不定結構諧合變位','SA-U2-3':'靜不定結構之傾角變位法','SA-U2-4':'靜不定結構之矩陣分析法','SA-U2-5':'彎矩分配法','SA-U3-1':'建築結構系統之使用','SA-U3-2':'建築結構系統分析'}
STD=['moduleId','year','rocYear','questionNumber','primaryTopicId','primaryTopicName','secondaryTopicIds','verificationStatus','problemStatus','hasSolution','hasHandwritten','tags']
LOG=collections.defaultdict(list)
# ---- item 1: strip legacy fields
for i,q in Q.items():
    extra=[k for k in q if k not in STD]
    if extra: LOG[i].append('idx 刪舊欄位 '+','.join(extra))
    for k in extra: del q[k]
# ---- items 2/3: final tag lists
FINAL={
 'SA-2025-2':None,'SA-2022-3':None,'SA-2019-4':None,'SA-2017-1':None,'SA-2015-2':None,
 'SA-2010-1':None,'SA-2002-1':None,'SA-2011-3':None,'SA-2016-1':None}
DROP={'SA-2022-3':{'細長拉桿'},'SA-2010-1':{'零力桿件'},'SA-2025-2':{'內鉸接'},'SA-2016-1':{'靜定剛架','靜力平衡'}}
TAGRE=re.compile(r'^(\*\*標籤：\*\*\s*)(.*)$',re.M)
def mdtags(t):
    m=TAGRE.search(t); return (re.findall(r'`([^`]+)`',m.group(2)),m) if m else (None,None)
MD={}
def md(i):
    if i not in MD: MD[i]=open(f'raw/solutions/{i}/{i}.md',encoding='utf-8').read()
    return MD[i]
for i in FINAL:
    mt,_=mdtags(md(i)); it=Q[i]['tags']
    fin=[x for x in mt]+[x for x in it if x not in mt]
    fin=[x for x in fin if x not in DROP.get(i,set())]
    FINAL[i]=fin
# ---- item 4 + tags: rebuild header block
METHOD={'SA-2008-1':'諧合變位法（力法，取 D 點水平反力為贅力）','SA-2008-2':'傾角變位法','SA-2008-3':'最小功法','SA-2008-4':'矩陣勁度法（直接勁度法）','SA-2019-3':'傾角變位法','SA-2019-4':'矩陣勁度法（直接勁度法，柱 CD、梁 DE 用修正勁度）'}
def sec_line(q):
    s=q['secondaryTopicIds']
    return '無' if not s else '、'.join(f'`{x}` {NAMES[x]}' for x in s)
def fmt_tags(lst,old):
    sep=', ' if old and re.search(r'`\s*,\s*`',old) else ' '
    return sep.join(f'`{x}`' for x in lst)
changed=[]
for i,q in Q.items():
    t=md(i); orig=t; notes=[]
    # YAML frontmatter files
    if t.startswith('---\n'):
        end=t.index('\n---\n',4)
        body=t[end+5:]
        body=re.sub(r'^\s*# [^\n]*\n','',body,count=1)
        hdr=(f"# 考題編號：{i}\n\n**主分類：** `{q['primaryTopicId']}` {NAMES[q['primaryTopicId']]}\n**副分類：** {sec_line(q)}\n"
             f"**分析法：** {METHOD[i]}\n**標籤：** {fmt_tags(q['tags'],None)}\n\n---\n\n")
        t=hdr+body.lstrip('\n'); notes.append('YAML frontmatter 改為標準標頭（主分類、副分類、分析法、標籤）')
    else:
        head,rest=t[:2000],t[2000:]
        lines=head.split('\n')
        # locate header lines
        def find(k): 
            for n,l in enumerate(lines[:15]):
                if l.startswith(f'**{k}：**'): return n
            return None
        pn=find('主分類')
        newp=f"**主分類：** `{q['primaryTopicId']}` {NAMES[q['primaryTopicId']]}"
        if lines[pn]!=newp: notes.append(f'主分類行改為大綱名稱（原：{lines[pn][8:].strip()}）'); lines[pn]=newp
        sn=find('副分類'); news=f"**副分類：** {sec_line(q)}"
        if sn is None: lines.insert(pn+1,news); notes.append('補副分類行')
        elif lines[sn].rstrip()!=news:
            old=lines[sn]; lines[sn]=news
            if set(re.findall(r'SA-U\d-\d',old))!=set(q['secondaryTopicIds']): raise SystemExit('sec mismatch '+i)
            if re.sub(r'\s','',old)!=re.sub(r'\s','',news): notes.append('副分類行格式統一')
        if find('分析法') is None:
            n=find('副分類'); lines.insert(n+1,f'**分析法：** {METHOD[i]}'); notes.append('補分析法行')
        head='\n'.join(lines); t=head+rest
    # tags
    if i in FINAL:
        mt,m=mdtags(t)
        if mt!=FINAL[i]:
            t=t[:m.start(2)]+fmt_tags(FINAL[i],m.group(2))+t[m.end(2):]
            notes.append('標籤與索引對齊')
        if Q[i]['tags']!=FINAL[i]: LOG[i].append(f"idx tags {Q[i]['tags']} → {FINAL[i]}"); Q[i]['tags']=FINAL[i]
    if t!=orig:
        t=t.rstrip('\n')+f"\n\n*修正日期：2026-11-14（格式整理：{'；'.join(notes)}。解題內容與答案不變）*\n"
        MD[i]=t; changed.append(i); LOG[i].append('md: '+'；'.join(notes))
# primaryTopicName sanity
for i,q in Q.items(): assert q['primaryTopicName']==NAMES[q['primaryTopicId']],i
# write
for i in changed: open(f'raw/solutions/{i}/{i}.md','w',encoding='utf-8').write(MD[i])
d['questions']=[{k:q[k] for k in STD if k in q} for q in d['questions']]
json.dump(d,open(IDX,'w',encoding='utf-8'),ensure_ascii=False,indent=2); open(IDX,'a').write('\n')
json.dump(dict(LOG),open(os.path.expanduser('~/chk/fixlog.json'),'w'),ensure_ascii=False,indent=1)
print('md changed',len(changed),changed)
for i,v in LOG.items(): print(i,'|',' || '.join(v)[:300])
