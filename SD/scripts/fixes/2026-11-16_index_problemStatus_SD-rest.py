"""2026-11-16 SD 其餘 6 子項（59 題）題目正本確認 → question_index problemStatus=confirmed（只改此欄，保留格式）"""
import json,re,pathlib
root=pathlib.Path(__file__).resolve().parents[2]
p=root/'raw/json/question_index.json'
raw=p.read_text(encoding='utf-8')
q=json.loads(raw);Q=q['questions'] if isinstance(q,dict) else q
units={'SD-U1-1','SD-U1-2','SD-U2-2','SD-U2-3','SD-U3-1','SD-U3-2'}
n=0;miss=[]
for x in Q:
    if x.get('primaryTopicId') in units:
        pm=root/f"raw/solutions/{x['moduleId']}/{x['moduleId']}-problem.md"
        if pm.exists() and '已確認' in (re.search(r'判讀狀態[^\n]*',pm.read_text(encoding='utf-8')) or [''])[0]:
            if x.get('problemStatus')!='confirmed': x['problemStatus']='confirmed';n+=1
        else: miss.append(x['moduleId'])
ind=2
p.write_text(json.dumps(q,ensure_ascii=False,indent=ind)+('\n' if raw.endswith('\n') else ''),encoding='utf-8')
print('updated',n,'missing',miss)
