import re
from pathlib import Path
ROOT=Path('.')
def sec(md, start_rx, end_rx):
    m=re.search(start_rx+r'.*?\n(.*?)(?='+end_rx+r')', md, re.S); return m.group(1).strip() if m else ''
CFG={
 'SS-2003-1':dict(no='第一題', figs=[], concepts='[[BLOCK-SHEAR-RUPTURE]] | [[WEB-LOCAL-YIELDING]] | [[WEB-CRIPPLING]] | [[TENSION-MEMBER-DESIGN]] | [[COMPACT-SECTION]] | [[COLUMN-STRENGTH-CURVE]] | [[RESIDUAL-STRESS]] | [[FLEXURAL-BUCKLING-GENERAL]]',
   ans='（一）塊狀剪力撕裂：剪力面＋拉力面一起撕出；（二）改善：加長支承長度、設承壓加勁板、加厚腹板／補強板；（三）降伏屬延性、有預警，斷裂屬脆性 → $\\phi_t$ 0.90 vs 0.75（ASD $0.6F_y$ vs $0.5F_u$）；（四）塑性設計、結實、半結實、細長肢四種；（五）$C_c = \\sqrt{2\\pi^2E/F_y}$，$F_e = F_y/2$ 的細長比，源自殘留應力約 $0.5F_y$。',
   rel=[('SS-2015-2','中度相關','同主分類；共同標籤：塊狀剪力'),('SS-2023-2','中度相關','同主分類；共同考點：$C_c$ 判斷挫屈型態'),('SS-2016-3','中度相關','同主分類；共同考點：殘留應力與柱強度曲線'),('SS-2024-1','中度相關','同主分類；共同考點：殘留應力與柱強度曲線')]),
 'SS-2003-2':dict(no='第二題', figs=['SS-2003-2-fig-1.png'], concepts='[[COLUMN-STRENGTH-CURVE]] | [[EULER-BUCKLING]] | [[FLEXURAL-BUCKLING-GENERAL]]',
   ans='$r_m = \\max(r_{型鋼},\\ 0.3\\times$挫屈平面全厚$)$：弱軸 15.0 cm、強軸 18.0 cm → $KL/r_m = 80$（弱軸控制）→ $\\lambda_c = 1.235$（非彈性）→ $F_{cr} = 3.661$ t/cm² → **$\\phi_cP_n \\approx 513$ t**。',
   rel=[('SS-2018-2','高度相關','同主分類；共同標籤：Fcr、λc、φcPn'),('SS-2002-3','高度相關','同主分類；共同標籤：Fcr、λc、φcPn'),('SS-2023-2','中度相關','同主分類；共同標籤：整體挫屈、非彈性挫屈'),('SS-2014-1','中度相關','同主分類；共同標籤：整體挫屈')]),
 'SS-2003-3':dict(no='第三題', figs=['SS-2003-3-fig-1.png','SS-2003-3-fig-2.png'], concepts='[[BOLTED-CONNECTION-DESIGN]] | [[BEARING-TYPE-CONNECTION]] | [[CONNECTION-DESIGN]] | [[TENSION-MEMBER-DESIGN]] | [[EFFECTIVE-NET-AREA]] | [[SHEAR-LAG]]',
   ans='（一）構材 $\\phi_tP_n = 77.51$ t（降伏控制）；雙角鋼夾 WT 腹板為雙剪 17.96 t/顆 → **5 顆**。（二）WT 與柱 8 顆螺栓受 3:4 斜向力：每栓 $t_u = 7.75$、$v_u = 5.81$ t；考卷表 $F_t = 8.2 - 1.9f_v = 4.32$ t/cm² → $\\phi R_t = 9.24$ t ≥ 7.75 t → **足夠**。',
   rel=[('SS-2005-1','高度相關','同主分類；共同標籤：U值、剪力遲滯、有效淨面積'),('SS-2015-2','高度相關','同主分類；共同標籤：U值、剪力遲滯'),('SS-2025-2','中度相關','同主分類；共同標籤：U值、剪力遲滯'),('SS-2002-4','中度相關','共同標籤：A325X、承壓型螺栓')]),
}
def build(q, mdtext, header_lines):
    c=CFG[q]; md=mdtext.replace('\x00','')
    s1=sec(md, r'## 1\. 原始題目重述[^\n]*', r'\n---\n\n## 2\.')
    s2=sec(md, r'## 2\. 考題核心精神[^\n]*', r'\n---\n\n## 3\.')
    s3=sec(md, r'## 3\. 解題戰略地圖[^\n]*', r'\n---\n\n## 3\.5')
    s1=re.sub(r'\]\(('+q+r'-[^)]+)\)', r'](../../raw/solutions/'+q+r'/\1)', s1)
    first=re.sub(r'\s+',' ',re.sub(r'[*$\\]','',s1.split('\n\n')[0])).strip()
    if first.startswith('一、簡答題'): first='簡答題五小題：塊狀剪力、腹板局部降伏改善、受拉安全係數、局部挫屈斷面分類、Cc'
    title=first[:48]+('…' if len(first)>48 else '')
    L=[f'# {q} — {title}','']+header_lines+['','---','','## 題幹摘要','',s1,'','---','','## 核心考點','',s2,'','---','','## 解題關鍵步驟','',s3,'','---','','## 答案摘要','',c['ans'],'','---','']
    if c['figs']:
        L+=['## 圖形','','| 檔案 | 類型 | 內容 |','|------|------|------|']+[f'| [{f}](../../raw/solutions/{q}/{f}) | PNG 附圖 | 題目附圖 |' for f in c['figs']]+['','']
    L+=['## 相關概念','',c['concepts'],'','## 相關題目','','| 題目 | 關聯性 | 說明 |','|------|--------|------|']+[f'| ⚠️ [[{a}]] | {b} | {d} |' for a,b,d in c['rel']]+['',f'*（請參閱 [原始解析](../../raw/solutions/{q}/{q}.md) 取得完整計算內容）*','']
    return '\n'.join(L)
if __name__=='__main__':
    import sys
    root=Path(sys.argv[1])
    for q in CFG:
        md=(root/f'raw/solutions/{q}/{q}.md').read_text(encoding='utf-8')
        old=(root/f'wiki/problems/{q}.md').read_text(encoding='utf-8').splitlines()
        hdr=[l for l in old[1:12] if l.startswith('**')]
        tags=re.search(r'\*\*標籤：\*\*.*',md).group(0)
        hdr=[tags if l.startswith('**標籤') else l for l in hdr]
        (root/f'wiki/problems/{q}.md').write_text(build(q,md,hdr),encoding='utf-8'); print('wrote',q, len(hdr))
