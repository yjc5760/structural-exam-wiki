from lib import *
import math

# ---------------- 圖 3-3 塊狀剪力：範例 A 實尺寸 + 雙排示意 ----------------
def f33():
    p='f33'; b=[markers(p,{'r':RED,'k':EDGE})]
    s=1.2
    E=470; yh=270; yt=yh-125*s     # end x, heel (bottom) y, toe (top) y
    x_of=lambda mm: E-mm*s
    b.append(T(24,24,'(a) 範例 A：L125×125×12 的連接肢（攤平、實際比例）',13,INK,weight='700'))
    b.append(R(x_of(330),yt,330*s,125*s,'#fafafa',EDGE,1.6))
    b.append(L(x_of(330),yh,E,yh,BLUE,4))
    b.append(T(x_of(330)+4,yh+18,'肢背（外伸肢從這條邊長出去）',11.5,BLUE))
    b.append(T(x_of(330)+4,yt-8,'肢趾（自由邊）',11.5,MUT))
    yb=yh-45*s
    bolts=[40,110,180,250]
    # block
    b.append(R(E-250*s,yt,250*s,yb-yt,'#fff8e1','none',0))
    b.append(L(E-250*s,yb,E,yb,GREEN,3))
    b.append(L(E-250*s,yt,E-250*s,yb,RED,3))
    for mm in bolts: b.append(C(x_of(mm),yb,12.5*s,'#fff',EDGE,1.6))
    b.append(L(x_of(330),yb,E,yb,MUT,0.6,'4,3'))
    b.append(arrow(x_of(330)-2,(yt+yh)/2,x_of(330)-46,(yt+yh)/2,RED,3,p,'r'))
    b.append(T(x_of(330)-30,(yt+yh)/2-14,'T',14,RED,'middle','700'))
    # dims along bottom
    yd=yh+42
    prev=0
    for mm in bolts:
        b.append(dimh(x_of(mm),x_of(prev),yd,str(mm-prev),MUT,11.5)); prev=mm
    b.append(dimv(E+22,yb,yh,'45',MUT,11.5,'right'))
    b.append(dimv(E+22,yt,yb,'80',MUT,11.5,'right'))
    b.append(T(E+4,yd+4,'端部',11.5,MUT))
    # labels
    b.append(T(E-125*s,yb+34,'剪力面 L_{gv} = 4 + 3×7 = 25 cm',12.5,GREEN,'middle','700'))
    b.append(T(E-250*s-6,yt+26,'拉力面',12.5,RED,'end','700'))
    b.append(T(E-250*s-6,yt+44,'8.0 cm',12,RED,'end'))
    b.append(T(E-125*s,yt+28,'破壞塊（被整塊撕走）',12.5,ORG,'middle','700'))
    lines=['A_{gv} = 25 × 1.2 = 30.0 cm²','A_{nv} = (25 − 3.5×2.5) × 1.2 = 19.50 cm²','A_{nt} = (8.0 − 0.5×2.5) × 1.2 = 8.10 cm²']
    for i,t in enumerate(lines): b.append(T(24,yd+38+i*20,t,12.5,INK))
    b.append(T(24,yd+38+3*20,'孔徑 d_{h} = 2.5 cm；剪力面穿過 3.5 個孔（端孔算半個）',12,MUT))
    # (b) two rows schematic
    ox=560; b.append(T(ox-20,24,'(b) 雙排螺栓的板件',13,INK,weight='700'))
    W=270; yt2,yh2=60,240; E2=ox+W
    b.append(R(ox,yt2,W,yh2-yt2,'#fafafa',EDGE,1.6))
    rows=[105,195]; cols=[E2-35,E2-95,E2-155]
    b.append(R(cols[-1],rows[0],E2-cols[-1],rows[1]-rows[0],'#fff8e1','none',0))
    for y in rows: b.append(L(cols[-1],y,E2,y,GREEN,3))
    b.append(L(cols[-1],rows[0],cols[-1],rows[1],RED,3))
    for x in cols:
        for y in rows: b.append(C(x,y,10,'#fff',EDGE,1.6))
    b.append(arrow(ox-2,150,ox-40,150,RED,3,p,'r'))
    b.append(T(cols[-1]-8,154,'拉力面',12.5,RED,'end','700'))
    b.append(T((cols[-1]+E2)/2,rows[0]-10,'剪力面',12.5,GREEN,'middle','700'))
    b.append(T((cols[-1]+E2)/2,rows[1]+22,'剪力面',12.5,GREEN,'middle','700'))
    b.append(T(ox-20,290,'剪力面沿螺栓「中心線」走、穿過孔；',12.5,INK))
    b.append(T(ox-20,310,'不是貼著孔外緣走。',12.5,INK))
    b.append(T(ox-20,342,'剪（綠）→ ×0.6；拉（紅）→ 不乘',12.5,PUR,weight='700'))
    b.append(T(ox-20,364,'式A：0.6F_{u}A_{nv} + U_{bs}F_{u}A_{nt}',12.5,INK))
    b.append(T(ox-20,386,'式B：0.6F_{y}A_{gv} + U_{bs}F_{u}A_{nt}',12.5,INK))
    b.append(T(ox-20,412,'φR_{n} = 0.75 × min(式A, 式B)',13.5,RED,weight='700'))
    return svg(880,450,''.join(b),'塊狀剪力破壞塊：範例A實尺寸與雙排螺栓示意')

# ---------------- 圖 4-1 摩阻型 vs 承壓型 + 載重-滑移 ----------------
def f41():
    p='f41'; b=[markers(p,{'r':RED,'k':EDGE,'o':ORG,'g':GREEN,'b':BLUE})]
    def joint(cx,slipped):
        o=[]
        yT0,yT1,yB1=120,150,180
        dT=-10 if slipped else 0; dB=10 if slipped else 0
        o.append(R(cx-170+dT,yT0,300,30,LBLUE,BLUE,1.6))
        o.append(R(cx-130+dB,yT1,300,30,LRED if slipped else LBLUE,RED if slipped else BLUE,1.6))
        hw=15; sw=11
        # holes
        if slipped:
            o.append(R(cx+sw-2*hw,yT0+1,2*hw,28,'#fff','none',0))  # top plate moved left: right wall touches
            o.append(R(cx-sw,yT1+1,2*hw,28,'#fff','none',0))       # bottom moved right: left wall touches
        else:
            o.append(R(cx-hw,yT0+1,2*hw,58,'#fff','none',0))
        o.append(R(cx-sw,yT0-8,2*sw,yB1-yT0+16,'#cfd8dc',EDGE,1.5))
        o.append(R(cx-26,yT0-20,52,12,'#90a4ae',EDGE,1.4)); o.append(R(cx-26,yB1+8,52,12,'#90a4ae',EDGE,1.4))
        return o
    # left: slip-critical
    cx=210
    b.append(T(cx,28,'摩阻型（Slip-Critical）',15,BLUE,'middle','700'))
    b+=joint(cx,False)
    b.append(arrow(cx,64,cx,96,RED,2.5,p,'r')); b.append(arrow(cx,238,cx,206,RED,2.5,p,'r'))
    b.append(T(cx+10,72,'夾緊力 T_{b}（預拉力反力）',12.5,RED,weight='700'))
    b.append(arrow(cx-160,135,cx-206,135,EDGE,2.4,p,'k')); b.append(arrow(cx+170,165,cx+214,165,EDGE,2.4,p,'k'))
    b.append(L(cx-130,150,cx+130,150,ORG,3))
    b.append(arrow(cx-110,145,cx-60,145,ORG,1.8,p,'o')); b.append(arrow(cx+110,155,cx+60,155,ORG,1.8,p,'o'))
    b.append(T(cx-160,250,'接觸面摩擦 μ·T_{b}：桿與孔壁之間仍有間隙',12,ORG))
    # right: bearing
    cx=650
    b.append(T(cx,28,'承壓型（Bearing-Type）',15,RED,'middle','700'))
    b+=joint(cx,True)
    b.append(arrow(cx-180,135,cx-224,135,EDGE,2.4,p,'k')); b.append(arrow(cx+180,165,cx+224,165,EDGE,2.4,p,'k'))
    b.append(L(cx-11,150,cx+11,150,PUR,3,'4,2'))
    b.append(T(cx+30,146,'剪力面',12.5,PUR,'start','700'))
    b.append(L(cx+11,122,cx+11,148,ORG,3.5)); b.append(L(cx-11,152,cx-11,178,ORG,3.5))
    b.append(T(cx+22,112,'孔壁承壓（上板孔右壁）',11.5,ORG))
    b.append(T(cx-22,206,'孔壁承壓（下板孔左壁）',11.5,ORG,'end'))
    b.append(T(cx-150,250,'板已錯開一個孔隙，孔壁貼住才傳力',12,RED))
    # load-slip curve
    ox,oy,W,H=110,490,700,190
    b.append(arrow(ox,oy,ox+W+20,oy,EDGE,1.5,p,'k')); b.append(arrow(ox,oy,ox,oy-H-24,EDGE,1.5,p,'k'))
    b.append(T(ox+W+18,oy+20,'接合相對位移 δ',12.5,MUT,'end')); b.append(T(ox+6,oy-H-20,'每顆螺栓傳的力',12.5,MUT))
    ys=oy-H*139.2/180; yb=oy-H*158.4/180
    xs1=ox+40; xs2=ox+40+150
    pts=[(ox,oy),(xs1,ys),(xs2,ys)]
    for k in range(1,31):
        t=k/30; pts.append((xs2+t*470, ys-(ys-(oy-H*0.97))*(1-(1-t)**2.2)))
    b.append(P(pts,'none',INK,2.6,close=False))
    b.append(L(ox,ys,ox+W,ys,BLUE,1.3,'6,4')); b.append(T(ox+250,ys+18,'滑動門檻：範例 B 摩阻型 φR_{n} = 139.2 kN（φ = 1.0）',12,BLUE,'start','700'))
    b.append(L(ox,yb,ox+W,yb,RED,1.3,'6,4')); b.append(T(ox+50,yb-8,'範例 B 承壓型 φR_{n} = 158.4 kN（承壓控制）',12,RED,'start','700'))
    b.append(dimh(xs1,xs2,oy-20,'滑移 ≈ 孔隙（標準孔 d_{b}+2 mm）',ORG,12))
    b.append(T(ox+30,oy-H*0.5+40,'① 摩擦傳力',12,BLUE))
    b.append(T(xs2+60,oy-H*0.5+60,'③ 桿貼孔壁 → 剪力＋承壓',12,RED))
    b.append(T((xs1+xs2)/2,ys+20,'② 滑動',12,ORG,'middle'))
    return svg(880,520,''.join(b),'摩阻型與承壓型螺栓的傳力機制與載重滑移曲線')

# ---------------- 新圖 4-2 承壓 R_n 與 L_c ----------------
def f42():
    p='f42'; b=[markers(p,{'k':EDGE,'r':RED})]
    # left: geometry
    b.append(T(24,24,'(a) 承壓幾何：力朝板端',13,INK,weight='700'))
    s=4.0  # px/mm, bolt d=22, dh=24
    E=330; cy=150; cxh=E-38*s   # Le = 38 mm
    b.append(R(30,70,E-30,160,'#fafafa',EDGE,1.6))
    b.append(L(E,70,E,230,EDGE,2.4))
    r=12*s
    b.append(R(cxh,cy-r,E-cxh,2*r,'#fff3e0','none',0))
    b.append(L(cxh,cy-r,E,cy-r,ORG,2.4,'5,3')); b.append(L(cxh,cy+r,E,cy+r,ORG,2.4,'5,3'))
    b.append(C(cxh,cy,r,'#fff',EDGE,1.6)); b.append(C(cxh+1*s,cy,11*s,'#cfd8dc',EDGE,1.4))
    b.append(arrow(cxh-10,cy,cxh+40,cy,RED,2.5,p,'r'))
    b.append(T(cxh-r-6,cy+5,'螺栓推板',11.5,RED,'end'))
    b.append(dimh(cxh,E,58,'L_{e}（中心到板端）',MUT,12))
    b.append(L(cxh,62,cxh,cy,MUT,0.8,'2,2'))
    b.append(dimh(cxh+r,E,246,'L_{c} = L_{e} − d_{h}/2',ORG,12,ty=264))
    b.append(L(cxh+r,cy,cxh+r,250,ORG,0.8,'2,2'))
    b.append(T(40,290,'L_{c} 很小 → 孔前那塊板沿兩條橘線被「犁」出去',12,INK))
    b.append(T(40,308,'抗力 ∝ 兩條剪切面長 2L_{c} → 1.2F_{u}L_{c}t',12,INK))
    b.append(T(40,326,'（0.6F_{u} × 2L_{c} × t = 1.2F_{u}L_{c}t）',12,PUR,weight='700'))
    # right: graph
    ox,oy,W,H=440,270,380,210
    b.append(T(ox-20,24,'(b) 標稱承壓強度 vs 淨邊距',13,INK,weight='700'))
    X=lambda v: ox+v/3.5*W; Y=lambda v: oy-v/3.0*H
    for v in [0,0.6,1.2,1.8,2.4,3.0]:
        b.append(L(ox,Y(v),ox+W,Y(v),'#eceff1',1)); b.append(T(ox-8,Y(v)+4,f'{v:.1f}',11.5,MUT,'end'))
    for v in [0,0.5,1,1.5,2,2.5,3,3.5]:
        b.append(T(X(v),oy+18,f'{v:g}',11.5,MUT,'middle'))
    b.append(L(ox,oy,ox+W+6,oy,EDGE,1.5)); b.append(L(ox,oy,ox,Y(3.1),EDGE,1.5))
    b.append(T(ox+W/2,oy+40,'L_{c} / d',13,INK,'middle'))
    b.append(T(ox-40,Y(3.1)-8,'R_{n} / (F_{u}dt)',12.5,INK))
    b.append(P([(X(0),Y(0)),(X(2),Y(2.4)),(X(3.5),Y(2.4))],'none',BLUE,3,close=False))
    b.append(L(X(2),Y(2.4),X(2),oy,MUT,1,'3,3'))
    b.append(C(X(2),Y(2.4),5,RED,RED))
    b.append(T(X(2)+6,Y(2.4)-10,'L_{c} = 2d：1.2×2 = 2.4',12.5,RED,'start','700'))
    b.append(T(X(0.85),Y(1.75),'撕裂控制',12.5,BLUE,'end','700'))
    b.append(T(X(0.85),Y(1.75)+18,'1.2F_{u}L_{c}t',12.5,BLUE,'end'))
    b.append(T(X(2.75),Y(2.4)+22,'孔變形控制 2.4F_{u}dt',12.5,BLUE,'middle','700'))
    b.append(T(X(2.75),Y(2.4)+40,'（變形 ≈ 6 mm 封頂）',11.5,MUT,'middle'))
    return svg(880,340,''.join(b),'孔壁承壓：撕裂與孔變形兩種破壞')

# ---------------- 新圖 5-2 方向性 ----------------
def f52():
    p='f52'; b=[markers(p,{'k':EDGE,'r':RED})]
    ox,oy,W,H=90,250,420,200
    X=lambda d: ox+d/90*W; Y=lambda v: oy-(v-0.9)/0.7*H
    for v in [1.0,1.1,1.2,1.3,1.4,1.5]:
        b.append(L(ox,Y(v),ox+W,Y(v),'#eceff1',1)); b.append(T(ox-8,Y(v)+4,f'{v:.1f}',11.5,MUT,'end'))
    for d in [0,15,30,45,60,75,90]:
        b.append(T(X(d),oy+18,f'{d}°',11.5,MUT,'middle'))
    b.append(L(ox,oy,ox+W+6,oy,EDGE,1.5)); b.append(L(ox,oy,ox,Y(1.58),EDGE,1.5))
    b.append(T(ox+W/2,oy+40,'力與銲道軸線的夾角 θ',13,INK,'middle'))
    b.append(T(ox-60,Y(1.58)-10,'強度倍數 1 + 0.5 sin^{1.5}θ',12.5,INK))
    pts=[(X(d),Y(1+0.5*math.sin(math.radians(d))**1.5)) for d in range(0,91)]
    b.append(P(pts,'none',BLUE,3,close=False))
    b.append(L(ox,Y(1.0),ox+W,Y(1.0),RED,1.6,'6,4'))
    b.append(T(ox+W,Y(1.0)+16,'規範預設：一律取 1.0（θ = 0，純剪）',12,RED,'end','700'))
    for d,lab in [(0,'1.00'),(45,'1.30'),(90,'1.50')]:
        v=1+0.5*math.sin(math.radians(d))**1.5
        b.append(C(X(d),Y(v),5,BLUE,'#fff',1.5)); b.append(T(X(d)+(8 if d==0 else -8),Y(v)-8,lab,12.5,BLUE,'start' if d==0 else 'end','700'))
    b.append(T(X(52),Y(1.18),'被放棄的紅利',13,GREEN,'middle','700'))
    # sketches
    sx=600
    b.append(T(sx,40,'θ = 0°：縱向銲（平行受力）',12.5,INK,weight='700'))
    b.append(R(sx,56,120,40,STEEL,EDGE,1.4)); b.append(R(sx+60,64,140,24,LBLUE,BLUE,1.4))
    b.append(L(sx+60,64,sx+120,64,ORG,4)); b.append(L(sx+60,88,sx+120,88,ORG,4))
    b.append(arrow(sx+200,76,sx+240,76,RED,2.5,p,'r'))
    b.append(T(sx,150,'θ = 90°：橫向銲（垂直受力）',12.5,INK,weight='700'))
    b.append(R(sx,166,120,40,STEEL,EDGE,1.4)); b.append(R(sx+60,174,140,24,LBLUE,BLUE,1.4))
    b.append(L(sx+60,174,sx+60,198,ORG,4))
    b.append(arrow(sx+200,186,sx+240,186,RED,2.5,p,'r'))
    b.append(T(sx,240,'橘線 = 填角銲',11.5,ORG))
    b.append(T(sx,262,'同一條銲道上各點 θ 不同（偏心時）',11.5,MUT))
    b.append(T(sx,280,'→ 一律取 1.0 最省事也最保守',11.5,MUT))
    return svg(880,300,''.join(b),'填角銲方向性強度曲線')
