from lib import *
import math

# ---------------- 新圖 8-1 剪力流與斷續銲（範例 F） ----------------
def f81():
    p='f81'; b=[markers(p,{'k':EDGE,'r':RED})]
    s=4.2  # px/cm
    b.append(T(24,24,'(a) 斷面：Q 只算「被這條銲道連過去」的蓋板',13,INK,weight='700'))
    cx=170; ytop=60
    # cover plate 20x1.2 on top, beam H500x200 (flange 1.6 approx, web 1.0) schematic but scaled depth
    d=50; bf=30; tf=1.6; tw=1.0
    yb0=ytop+1.2*s
    b.append(R(cx-10*s,ytop,20*s,1.2*s,'#ffcc80',ORG,1.6))
    b.append(R(cx-bf/2*s,yb0,bf*s,tf*s,'#cfd8dc',EDGE,1.4))
    b.append(R(cx-tw/2*s,yb0+tf*s,tw*s,(d-2*tf)*s,'#cfd8dc',EDGE,1.2))
    b.append(R(cx-bf/2*s,yb0+(d-tf)*s,bf*s,tf*s,'#cfd8dc',EDGE,1.4))
    # welds at plate edges (on flange top? plate same width as flange -> fillet at plate side edges)
    for sx in (-1,1):
        x=cx+sx*10*s
        b.append(P([(x,ytop),(x,yb0),(x+sx*1.2*s,yb0)],ORG,ORG,1))
    # neutral axis: plate centroid 26 cm above NA
    yna=ytop+0.6*s+26*s
    b.append(L(cx-bf/2*s-30,yna,cx+bf/2*s+30,yna,MUT,1,'5,3')); b.append(T(cx+bf/2*s+34,yna+4,'中性軸',11.5,MUT))
    b.append(L(cx+10*s+12,ytop+0.6*s,cx+10*s+40,ytop+0.6*s,ORG,0.8))
    b.append(dimv(cx+10*s+30,ytop+0.6*s,yna,'ȳ = 26 cm',ORG,12,'right'))
    b.append(T(cx,ytop-8,'PL 200×12（橘色 = Q 的面積）',11.5,ORG,'middle'))
    b.append(T(cx-bf/2*s-4,yb0+tf*s+14,'H 梁上翼板',10.5,MUT,'start'))
    b.append(T(24,yb0+d*s+40,'Q = (20 × 1.2) × 26 = 624 cm³',12.5,INK))
    b.append(T(24,yb0+d*s+60,'q = VQ / I = 40 × 624 / 200,000 = 0.1248 tf/cm',12.5,INK))
    b.append(T(24,yb0+d*s+80,'兩側分擔 → 每側 0.0624 tf/cm',12.5,PUR,weight='700'))
    # (b) elevation of plate length with intermittent welds, scale 2.6 px/cm
    k=2.6; x0=410; yy=110
    b.append(T(x0-10,24,'(b) 側面（沿梁長，比例 1 cm = 2.6 px）',13,INK,weight='700'))
    Lshow=170
    b.append(R(x0,yy-10,Lshow*k,10,'#ffcc80',ORG,1.2)); b.append(R(x0,yy,Lshow*k,8,'#cfd8dc',EDGE,1.2))
    b.append(T(x0+Lshow*k,yy-16,'蓋板（橘塊 = 6 cm 銲段）',11.5,ORG,'end'))
    pitch=28; seg=6
    xs=[]
    pos=0
    while pos+seg<=Lshow:
        b.append(R(x0+pos*k,yy-3,seg*k,6,ORG,ORG,0)); xs.append(pos); pos+=pitch
    b.append(dimh(x0+xs[1]*k,x0+xs[2]*k,yy+30,'s = 28 cm（構造控制）',GREEN,12,ty=yy+50))
    b.append(dimh(x0+xs[0]*k,x0+(xs[0]+seg)*k,yy-26,'6',ORG,11.5))
    # comparison bars
    yc=200
    b.append(T(x0-10,yc,'同一段 6 cm 銲道，兩種上限：',12.5,INK,weight='700'))
    b.append(R(x0,yc+14,90*k,14,'#e3f2fd',BLUE,1.2)); b.append(T(x0+90*k+8,yc+26,'強度需求只要 s ≤ 90 cm',12,BLUE))
    b.append(R(x0,yc+40,28.8*k,14,'#c8e6c9',GREEN,1.2)); b.append(T(x0+28.8*k+8,yc+52,'構造規定 s ≤ 24t = 28.8 cm（受壓）、≤ 300 mm',12,GREEN,'start','700'))
    b.append(T(x0-10,yc+90,'銲道只需 6.6% 的長度（0.0624 / 0.939），',12,MUT))
    b.append(T(x0-10,yc+110,'所以間距幾乎永遠是構造規定說了算：',12,MUT))
    b.append(T(x0-10,yc+130,'防鏽、防止板件在兩段銲道之間局部挫屈。',12,MUT))
    return svg(880,400,''.join(b),'蓋板剪力流與斷續銲間距')

# ---------------- 圖 9-1 開槽型式（實尺寸，t = 25 mm） ----------------
def f91():
    b=[]
    s=2.4; t=25*s
    tan30=math.tan(math.radians(30))
    WM='#ffcc80'
    def plate(pts): return P(pts,STEEL,EDGE,1.5)
    # single V
    cx=150; yb=170; yt=yb-t
    R_=6*s; op=t*tan30
    b.append(T(cx,28,'單 V（Single V）',14,BLUE,'middle','700'))
    b.append(plate([(30,yt),(cx-R_/2-op,yt),(cx-R_/2,yb),(30,yb)]))
    b.append(plate([(270,yt),(cx+R_/2+op,yt),(cx+R_/2,yb),(270,yb)]))
    b.append(P([(cx-R_/2,yb),(cx-R_/2-op,yt),(cx+R_/2+op,yt),(cx+R_/2,yb)],WM,ORG,1.6))
    b.append(path(f'M{cx-R_/2-op:.1f},{yt} Q{cx},{yt-10} {cx+R_/2+op:.1f},{yt}',WM,ORG,1.4))
    b.append(R(cx-15*s,yb,30*s,8*s,'#b0bec5',EDGE,1.2))
    b.append(T(cx,yb+8*s+16,'背墊板',11,MUT,'middle'))
    b.append(path(f'M{cx-R_/2-op*0.55:.1f},{yt+t*0.45:.1f} A40,40 0 0 1 {cx+R_/2+op*0.55:.1f},{yt+t*0.45:.1f}',c=PUR,sw=1))
    b.append(T(cx,yt+t*0.45-8+40-40,'60°',11.5,PUR,'middle'))
    b.append(dimv(26,yt,yb,'t',MUT,11.5))
    b.append(T(cx,yb+8*s+34,'R = 6、開槽角 60°',11.5,MUT,'middle'))
    b.append(T(cx,250,'對接、單面施銲；中厚板',12,INK,'middle'))
    # single bevel T-joint (beam flange to column flange)
    cx=440; yb=170; yt=yb-t
    b.append(T(cx,28,'單斜（Single Bevel）',14,BLUE,'middle','700'))
    cf=30*s
    b.append(plate([(cx-cf,40),(cx,40),(cx,215),(cx-cf,215)]))
    b.append(T(cx-cf/2,52,'柱翼板',10.5,MUT,'middle'))
    gap=6*s
    b.append(plate([(cx+gap,yb),(cx+gap+t,yt),(cx+130,yt),(cx+130,yb)]))
    b.append(T(cx+100,yt-6,'梁翼板',10.5,MUT,'middle'))
    b.append(P([(cx,yb),(cx,yt),(cx+gap+t,yt),(cx+gap,yb)],WM,ORG,1.6))
    b.append(R(cx,yb,gap+20*s,8*s,'#ef9a9a',RED,1.2))
    b.append(T(cx+gap+22*s,yb+8*s+14,'背墊板 = 人造裂縫',11,RED,'middle','700'))
    b.append(T(cx+gap+22*s,yb+8*s+30,'（耐震接頭須移除＋背剷回銲）',10.5,RED,'middle'))
    b.append(path(f'M{cx+gap:.1f},{yb-30:.1f} A30,30 0 0 1 {cx+gap+21.2:.1f},{yb-21.2:.1f}',c=PUR,sw=1))
    b.append(T(cx+gap+24,yb-30,'45°',11.5,PUR))
    b.append(T(cx,250,'T 型接頭（梁翼對柱）；只能從一側開槽',12,INK,'middle'))
    # double V
    cx=720; yb=170; yt=yb-t; f=3*s; R2=3*s; hseg=(t-f)/2; op=hseg/s*tan30*s
    b.append(T(cx,28,'雙 V（Double V）',14,BLUE,'middle','700'))
    ym1=yt+hseg; ym2=yb-hseg
    b.append(plate([(600,yt),(cx-R2/2-op,yt),(cx-R2/2,ym1),(cx-R2/2,ym2),(cx-R2/2-op,yb),(600,yb)]))
    b.append(plate([(840,yt),(cx+R2/2+op,yt),(cx+R2/2,ym1),(cx+R2/2,ym2),(cx+R2/2+op,yb),(840,yb)]))
    b.append(P([(cx-R2/2-op,yt),(cx+R2/2+op,yt),(cx+R2/2,ym1),(cx+R2/2,ym2),(cx+R2/2+op,yb),(cx-R2/2-op,yb),(cx-R2/2,ym2),(cx-R2/2,ym1)],WM,ORG,1.6))
    b.append(T(cx+38,(ym1+ym2)/2+4,'根面 f = 3',10.5,MUT))
    b.append(L(cx+4,(ym1+ym2)/2,cx+34,(ym1+ym2)/2,MUT,0.8))
    b.append(T(cx,yb+34,'R = 3、上下各 60°',11.5,MUT,'middle'))
    b.append(T(cx,250,'兩面施銲，銲料約省一半；可翻面時',12,INK,'middle'))
    b.append(T(440,282,'三圖皆以板厚 t = 25 mm 依同一比例繪製；R = 根部間隙。',11.5,MUT,'middle'))
    return svg(880,295,''.join(b),'開槽銲三種坡口實尺寸')

# ---------------- 圖 10-1 決策流程（重排） ----------------
def f101():
    p='f101'; b=[markers(p,{'k':EDGE})]
    def box(cx,cy,w,h,title,lines,fill,stroke,tc):
        o=[R(cx-w/2,cy-h/2,w,h,fill,stroke,1.8,10)]
        n=len(lines); y0=cy-h/2+24
        o.append(T(cx,y0,title,13.5,tc,'middle','700'))
        for i,l in enumerate(lines): o.append(T(cx,y0+20+i*19,l,12,INK,'middle'))
        return ''.join(o)
    def dia(cx,cy,w,h,title,sub=None,fill='#fff9c4',stroke=ORG):
        o=[P([(cx,cy-h/2),(cx+w/2,cy),(cx,cy+h/2),(cx-w/2,cy)],fill,stroke,1.8)]
        o.append(T(cx,cy+(0 if sub else 5),title,13.5,INK,'middle','700'))
        if sub: o.append(T(cx,cy+19,sub,11.5,MUT,'middle'))
        return ''.join(o)
    def ar(pts,lab=None,lp=None,lc=INK):
        o=[P(pts[:-1]+[pts[-1]],'none',EDGE,1.8,close=False,extra=f' marker-end="url(#{p}-k)"')]
        if lab: o.append(T(lp[0],lp[1],lab,12.5,lc,'middle','700'))
        return ''.join(o)
    b.append(box(440,38,520,46,'先列傳力路徑：外力 → 母材 A → 緊結物 → 母材 B',[],LBLUE,BLUE,'#0d47a1'))
    b.append(ar([(440,61),(440,88)]))
    b.append(dia(440,130,400,84,'外力通過緊結物群形心？','（托架／牛腿／偏心 = 否）'))
    b.append(ar([(240,130),(140,130),(140,246)],'否',(190,121),RED))
    b.append(box(140,300,240,110,'彈性向量法（§6）',['① 形心（銲道長度加權）','② I_{p}（螺栓 cm²／銲道 cm³）','③ M = P·e（e 到形心）','④ 向量相加找臨界點'],LORG,ORG,'#e65100'))
    b.append(ar([(440,172),(440,258)],'是',(456,220),GREEN))
    b.append(dia(440,300,300,80,'緊結物是螺栓還是銲道？'))
    b.append(ar([(260,300),(288,300)]))
    b.append(T(274,290,'R_{max}',10.5,ORG,'middle'))
    b.append(ar([(440,340),(440,368),(250,368),(250,396)],'螺栓',(330,360),BLUE))
    b.append(ar([(590,300),(690,300),(690,396)],'銲道',(640,291),RED))
    b.append(dia(250,432,300,72,'不准滑動（摩阻型）？',fill=LBLUE,stroke=BLUE))
    b.append(dia(690,432,280,72,'填角銲還是開槽銲？',fill=LRED,stroke=RED))
    b.append(ar([(250,468),(250,486),(140,486),(140,508)],'是',(186,480),GREEN))
    b.append(ar([(250,486),(360,486),(360,508)],'否',(316,480),RED))
    b.append(ar([(690,468),(690,486),(610,486),(610,508)],'填角',(644,480),ORG))
    b.append(ar([(690,486),(785,486),(785,508)],'開槽',(742,480),EDGE))
    b.append(box(140,544,220,72,'滑動強度（§4.2）',['φ μ D_{u} h_{sc} T_{b} n_{s}','φ = 1.0／0.85'],LBLUE,BLUE,'#0d47a1'))
    b.append(box(362,544,210,72,'承壓型（§4.3）',['min( F_{nv}A_{b}n_{s} ,','2.4F_{u}dt 或 1.2F_{u}L_{c}t )'],LRED,RED,RED))
    b.append(box(610,544,170,72,'填角銲（§5）',['1.565 wL（LRFD）','1.043 wL（ASD）'],LORG,ORG,'#e65100'))
    b.append(box(785,544,160,72,'CJP／PJP（§5.3）',['CJP → 驗母材','PJP → A_{eff}'],STEEL,EDGE,INK))
    for x in (140,362,610,785): b.append(L(x,580,x,602,EDGE,1.8))
    b.append(L(140,602,785,602,EDGE,1.8))
    b.append(ar([(440,602),(440,622)]))
    b.append(box(440,656,600,64,'母材端一律再驗三項（§3）—— 最常漏掉的一格',['GSY 0.9F_{y}A_{g}　｜　NSF 0.75F_{u}UA_{n}　｜　BSR 0.75·min(式A, 式B)'],LGRN,GREEN,GREEN))
    b.append(ar([(440,688),(440,712)]))
    b.append(dia(440,750,340,76,'梁柱接頭／續接／耐震？'))
    b.append(ar([(610,750),(650,750)],'是',(630,741),GREEN))
    b.append(box(760,750,220,96,'加做這些（§7、§1.3）',['M_{f}／M_{w} 分配、腹板組合應力','節點域 V_{pz}、連續板','最小接合強度、×R_{y} 超強'],LPUR,PUR,PUR))
    b.append(ar([(440,788),(440,822)],'否',(456,808),RED))
    b.append(ar([(760,798),(760,850),(672,850)]))
    b.append(box(440,850,460,54,'設計強度 = 清單中所有項目的最小值',['最後回頭檢查構造規定（間距、邊距、w 上下限）'],LRED,RED,RED))
    return svg(880,890,''.join(b),'接合題解題決策流程')
