# -*- coding: utf-8 -*-
"""SM-2021-4 獨立重算（勘誤 2026-11-15）：由題目正本的量測幾何重算解析中每個數值，並檢查正本 .md 內的數值字串。
用法：python 2026-11-15_verify_SM-2021-4.py <SM-2021-4.md 路徑>；最後印 MISMATCHES: n。
幾何：題目正本 #3–#5、#8（5 m = 292.5 px，58.5 px/m，坡趾原點），圓弧中間點為同一量測框架的像素描點。"""
import sys, numpy as np
gw=9.81; g=18.; gs=20.; c=10.; phi=np.radians(36)
sl=0.684; ycr=13.92; ywt=4.77
xb=[0,5.25,10.38,15.34,20.35,25.8]
surf=lambda x: np.minimum(sl*x, ycr)
wt=lambda x: np.minimum(ywt, surf(x))
P=np.array([(480,1292),(560,1306),(640,1312),(720,1316),(760,1316),(840,1312),(920,1306),(1000,1296),(1040,1289),(1120,1269),(1160,1256),(1200,1246),(1240,1232),(1320,1201),(1360,1182),(1400,1164),(1440,1141),(1480,1113),(1560,1064),(1600,1031),(1680,961),(1720,919),(1760,872),(1800,816),(1840,756),(1880,686)],float)
s=58.5; X0,Y0=441.8,1283.9
ax=np.r_[0,(P[:,0]-X0)/s,25.8]; ay=np.r_[0,(Y0-P[:,1])/s,13.92]
arc=lambda X: np.interp(X,ax,ay)
ALPHA=[60,42,30,13,0]
def slices(base=arc, alph=ALPHA, gw=gw, useL='b/cos'):
    out=[]
    for k in range(5):
        x0,x1=xb[4-k],xb[5-k]; X=np.linspace(x0,x1,4001); ys=surf(X); yw=wt(X); yB=base(X)
        Ad=np.trapezoid(np.clip(ys-np.maximum(yw,yB),0,None),X); As=np.trapezoid(np.clip(np.minimum(yw,ys)-yB,0,None),X)
        W=g*Ad+gs*As; b=x1-x0; xm=(x0+x1)/2; a=np.radians(alph[k])
        hw=max(0.,float(wt(xm))-float(base(xm))); u=gw*hw
        L=b/np.cos(a) if useL=='b/cos' else float(np.hypot(b,base(x1)-base(x0)))
        out.append(dict(b=b,Ad=Ad,As=As,W=W,L=L,hw=hw,u=u,yb=float(base(xm)),cL=c*L,Wc=W*np.cos(a),uL=u*L,
                        N=W*np.cos(a)-u*L,fr=(W*np.cos(a)-u*L)*np.tan(phi),dr=W*np.sin(a)))
    return out
def FS(**kw):
    r=slices(**kw); return sum(x['cL']+x['fr'] for x in r)/sum(x['dr'] for x in r)
R=slices()
# 第二路徑：多邊形面積（shapely，折線幾何的精確面積）
from shapely.geometry import Polygon, box
xs=np.unique(np.r_[ax, xb, 6.96/1.0, ycr/sl, 40]); xs=xs[xs<=40]
ground=Polygon([(x,float(surf(x))) for x in np.linspace(0,40,4001)]+[(40,-5),(0,-5)])
above=Polygon([(x,float(arc(x))) for x in np.linspace(0,25.8,4001)]+[(25.8,30),(0,30)])
soil=ground.intersection(above)
dry=soil.intersection(Polygon([(0,ywt),(40,ywt),(40,30),(0,30)])); 
# 坡面段水位沿地表：水位以下＝ y<min(4.77, surf) 即 y<4.77 的土體
sat=soil.intersection(Polygon([(0,-5),(40,-5),(40,ywt),(0,ywt)]))
mis=[]
def chk(name, v, ref, tol):
    if abs(v-ref)>tol: mis.append((name,v,ref))
for k,r in enumerate(R):
    x0,x1=xb[4-k],xb[5-k]; bx=box(x0,-5,x1,30)
    chk('A_dry%d poly'%(k+1), dry.intersection(bx).area, r['Ad'], 0.02)
    chk('A_sat%d poly'%(k+1), sat.intersection(bx).area, r['As'], 0.02)
fs=FS(); print('FS main %.4f'%fs)
md=open(sys.argv[1],encoding='utf-8').read() if len(sys.argv)>1 else ''
def inmd(s_):
    if md and s_ not in md: mis.append(('md missing',s_,''))
vals=[]
for k,r in enumerate(R):
    for key,fmt in [('b','%.2f'),('Ad','%.2f'),('As','%.2f'),('W','%.1f'),('L','%.2f'),('u','%.1f'),('Wc','%.1f'),('uL','%.1f'),('N','%.1f'),('cL','%.1f'),('fr','%.1f'),('dr','%.1f')]:
        v=r[key]; 
        if key in('Ad','As') and v<1e-9: continue
        if key in('u','uL','dr') and v<1e-9: continue
        vals.append(fmt%v)
S=dict(cL=sum(r['cL'] for r in R),fr=sum(r['fr'] for r in R),dr=sum(r['dr'] for r in R))
vals += ['%.1f'%S['cL'],'%.1f'%S['fr'],'%.1f'%S['dr'],'%.1f'%(round(S['cL'],1)+round(S['fr'],1)),'%.3f'%fs,'%.4f'%np.tan(phi)]
for v in vals: inmd(v)
# 交叉值（§4 Step 5 文字）
cross={'shift-0.2':FS(base=lambda X: arc(X)-0.2),'shift+0.2':FS(base=lambda X: arc(X)+0.2),'chordL':FS(useL='ch'),'gw10':FS(gw=10.)}
ang=[float(np.degrees(np.arctan2(arc(xb[5-k])-arc(xb[4-k]),xb[5-k]-xb[4-k]))) for k in range(5)]
cross['chord-angles']=FS(alph=ang); cross['a5=-6']=FS(alph=ALPHA[:4]+[ang[4]]); cross['a5=-5']=FS(alph=ALPHA[:4]+[-5])
for k_,v in cross.items(): print(k_,'%.3f'%v)
for s_ in ['0.965','0.986','0.983','0.969','1.37','0.987']: inmd(s_)
chk('chord angles',ang[1],33,1.0); print('chord angles',np.round(ang,1))
n=len(vals)+10+len(cross)
print('checked values:',len(vals),'+ poly areas 10')
print('MISMATCHES:',len(mis))
for m in mis: print('  ',m)
