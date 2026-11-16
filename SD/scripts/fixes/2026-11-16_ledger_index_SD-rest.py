"""2026-11-16 SD 其餘 6 子項 59 題 pipeline：寫入 audit-ledger（B 結果＋C fixed＋D recheck）與 question_index tags（只增不刪）"""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[2]; W=pathlib.Path.home()/'sdwork'; D='2026-11-16'
U={'U3-2':'SD-U3-2','U2-2':'SD-U2-2','U1-2':'SD-U1-2','U3-1':'SD-U3-1','X':'SD-U2-3與U1-1'}
FIXED={'SD-2013-3','SD-2002-3','SD-2002-4','SD-2004-1','SD-2004-2','SD-2005-1','SD-2005-3','SD-2006-3','SD-2006-4','SD-2007-1','SD-2007-4','SD-2008-2','SD-2008-4','SD-2009-3','SD-2009-4','SD-2010-3','SD-2010-4','SD-2012-4','SD-2013-2','SD-2014-3','SD-2014-4','SD-2015-4','SD-2017-3','SD-2018-2','SD-2020-4','SD-2022-2','SD-2022-4','SD-2023-3','SD-2023-4','SD-2024-3','SD-2024-4','SD-2025-4','SD-2003-4','SD-2004-3'}
lp=root/'wiki/queries/audit-ledger-SD.json'; led=json.loads(lp.read_text(encoding='utf-8'))
n=0
for f in sorted(W.glob('B-*-ledger.json')):
    g=f.name[2:-12]; u=U[g.split('-G')[0] if not g.startswith('X') else 'X']
    for qid,v in json.loads(f.read_text(encoding='utf-8')).items():
        res=re.sub(r'^[✅⚠️❌❓\s]+','',v.get('result','')).strip()
        e={'date':D,'model':'claude-opus-5-5','result':res,'source':v.get('source',''),
           'report':f'wiki/queries/盲解比對-{u}-{D}.md','scope':f'{u}（pipeline，組 {g}）','human':v.get('human',''),
           'fixed':D if qid in FIXED else '',
           'recheck':({'date':D,'result':'落實','report':f'wiki/queries/落實檢查-{u}-{D}.md','note':'非獨立複核（勘誤與落實檢查同一工作階段）'} if qid in FIXED else {'date':'','result':'','report':'','note':''}),
           'history':[]}
        if qid in led: e['history']=led[qid].get('history',[])+[{k:vv for k,vv in led[qid].items() if k!='history'}]
        led[qid]=e; n+=1
lp.write_text(json.dumps(led,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
TAGS={"SD-2004-2":["隔震層變形分配","上部結構變形"],"SD-2005-1":["等效阻尼比","割線勁度","遲滯迴圈","調整後強度","容量設計"],"SD-2008-4":["DD修正","動力分析"],
"SD-2012-4":["串聯模型","動力分析位移下限","規範9.3.4","隔震元件穩定性","隔震間隙"],
"SD-2014-4":["狀態組合係數","CF1／CF2","相位差","最大加速度狀態","殘餘變形"],
"SD-2018-1":["擬速度","反應譜平台段"],"SD-2018-4":["表3-1","長週期阻尼修正係數B1"],"SD-2023-3":["靜力分析適用條件9.2.1","抗傾倒9.4.2.7","傾倒力矩","現行規範"],"SD-2023-4":["被動消能系統第十章","消能元件數量","剛心兩側配置","最大考量地震位移"],
"SD-2005-3":["頂層集中力Ft","經驗週期公式","現行規範改寫"],"SD-2004-1":["現行規範改寫","中小度地震"],"SD-2002-4":["絕對值和","建築物間隔"],
"SD-2006-3":["近斷層效應","地盤分類","震區係數","設計譜形"],"SD-2007-1":["最大考量地震","臺北盆地"],"SD-2007-4":["容量設計","機率彎矩強度","圍束箍筋","短柱效應"],"SD-2008-2":["強度需求比","非結構牆","弱層"],
"SD-2009-3":["中小度地震30年","50年超越機率80%","V*","VM","現行規範111年版"],"SD-2014-3":["總橫力調整","規則性90%","不規則性100%","3.3節"],
"SD-2020-4":["最大考量地震檢核","設計力取最大值"],"SD-2024-3":["一般工址","中小度地震分母","起始降伏地震力放大倍數","系統超強","設計力取最大值"],
"SD-2003-4":["角點自由度","座標轉換","非對角質量矩陣","影響向量"],"SD-2004-3":["鉸支承剛性桿","轉動慣量","讀圖錯誤"],
"SD-2010-1":["幾何負勁度"],"SD-2016-2":["彈簧清點"],"SD-2017-4":["上界","自然邊界條件"],"SD-2024-2":["虛功原理","廣義力"],
"SD-2010-4":["崩塌機構","塑鉸順序","柱剪力不均","虛功法","推覆曲線","題意勘誤"],"SD-2017-3":["可變形段","牆高判讀","題意勘誤"],"SD-2015-4":["傾覆力矩","柱軸力拉壓"],"SD-2013-2":["實配鋼筋Mpr","現行規範18章","2h外剪力"],"SD-2009-4":["構造檢核","螺箍筋淨間距","特殊抗彎矩構架柱"],
"SD-2022-2":["112年版混凝土規範","2h閉合箍筋區","梁寬上限c2+0.75c1","1/4彎矩強度","規範版本勘誤"],"SD-2022-4":["規範豎向分配Ft","振態層剪力SRSS","題意判讀勘誤"],"SD-2025-4":["中小度地震","最大考量地震","容許韌性容量Ra","地震力折減係數Fu","規範版本勘誤"],"SD-2019-4":["短柱勁度1/L^3"],
"SD-2002-3":["施加載重與質量權重","Rayleigh下限","公式修正","題意勘誤"],"SD-2010-3":["縱向振動單元","滾支承與鉸支承","雙鉸墩","題意勘誤"],"SD-2018-2":["三軸座標軸向","常數位移段","規範譜對應"],"SD-2024-4":["形狀比較","Rayleigh商誤差"]}
ip=root/'raw/json/question_index.json'; q=json.loads(ip.read_text(encoding='utf-8')); m=0
for x in q['questions']:
    i=x['moduleId']
    if i in TAGS:
        t=x.setdefault('tags',[])
        for tg in TAGS[i]:
            if tg not in t: t.append(tg); m+=1
    if i in FIXED: x['verificationStatus']='unverified'
q['_meta']['updatedAt']=D
ip.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ledger',n,'tags added',m)
