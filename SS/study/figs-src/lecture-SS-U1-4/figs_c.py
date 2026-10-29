from lib import *
import math

# ---------------- 圖 6-1 範例 D：實尺寸幾何 + 向量合成 ----------------
def f61():
    p='f61'; b=[markers(p,{'r':RED,'b':BLUE,'o':ORG,'u':PUR,'k':EDGE})]
    g=8; X0,Y0=90,372
    X=lambda x: X0+x*g; Y=lambda y: Y0-y*g
    Ip=6816.7; e=31.0
    b.append(T(24,24,'(a) 幾何（比例 1 cm = 8 px）',13,INK,weight='700'))
    b.append(R(X(-5),Y(36),28*g,40*g,STEEL,'#b0bec5',1,extra=' fill-opacity="0.7"'))
    b.append(T(X(-4),Y(34.5),'柱翼板',11.5,MUT))
    b.append(R(X(0),Y(30),38*g,30*g,'#fffde7',ORG,1.4,extra=' fill-opacity="0.85"'))
    b.append(T(X(30),Y(27.5),'托架板',11.5,ORG,'middle'))
    b.append(L(X(0),Y(0),X(0),Y(30),ORG,6)); b.append(L(X(0),Y(0),X(20),Y(0),ORG,6))
    b.append(T(X(-1.2),Y(15),'d = 30',12,ORG,'end')); b.append(T(X(10),Y(0)+20,'b = 20',12,ORG,'middle'))
    cx,cy=X(4),Y(9)
    b.append(L(cx,cy,X(20),Y(0),MUT,1,'4,3')); b.append(L(cx,cy,X(0),Y(30),MUT,1,'4,3'))
    b.append(C(cx,cy,5,BLUE,BLUE)); b.append(T(cx+8,cy-4,'形心 (4, 9)',12,BLUE))
    b.append(T((cx+X(20))/2+4,(cy+Y(0))/2-6,'r = 18.36',11.5,MUT))
    b.append(T((cx+X(0))/2+6,(cy+Y(30))/2,'r = 21.38',11.5,MUT))
    # clockwise arc
    rr=34
    b.append(path(f'M{cx-rr},{cy} A{rr},{rr} 0 0 1 {cx},{cy-rr} A{rr},{rr} 0 0 1 {cx+rr*0.87:.1f},{cy-rr*0.5:.1f}',c=PUR,sw=1.8,marker={'end':f'{p}-u'}))
    b.append(T(cx+rr+4,cy-rr+2,'M = 31P（順）',12,PUR,weight='700'))
    # load
    b.append(arrow(X(35),Y(30)-48,X(35),Y(22),RED,3,p,'r')); b.append(T(X(35)+8,Y(30)-34,'P',15,RED,weight='700'))
    b.append(dimh(cx,X(35),Y(30)-60,'e = 35 − 4 = 31 cm',PUR,12.5))
    b.append(L(cx,cy-8,cx,Y(30)-56,PUR,0.7,'2,3'))
    # candidate points
    b.append(C(X(20),Y(0),6,RED,'#fff',1.5)); b.append(T(X(20)+10,Y(0)+18,'右下角 (20, 0) → 臨界',12,RED,weight='700'))
    b.append(C(X(0),Y(30),6,GREEN,'#fff',1.5)); b.append(T(X(0)+10,Y(30)+18,'左上角 (0, 30)：最遠但非臨界',12,GREEN,weight='700'))
    # (b) vector polygons
    k=1800  # px per P (tf/cm per P)
    b.append(L(450,40,450,430,'#cfd8dc',1.5,'6,5'))
    b.append(T(470,24,'(b) 兩點的向量合成（同一比例 0.01P = 18 px）',13,INK,weight='700'))
    fV=1/50
    def poly(sx,sy,rx,ry,title,col):
        fmx= e*ry/Ip; fmy=-e*rx/Ip
        o=[T(sx,sy-16,title,13,col,'middle','700')]
        x1,y1=sx,sy+fV*k
        o.append(arrow(sx,sy,x1,y1,BLUE,3,p,'b'))
        x2,y2=x1+fmx*k, y1-fmy*k
        o.append(arrow(x1,y1,x2,y2,ORG,3,p,'o'))
        o.append(arrow(sx,sy,x2,y2,PUR,3.4,p,'u'))
        o.append(C(sx,sy,4,col,col))
        fx,fy=fmx,fmy-fV; f=math.hypot(fx,fy)
        return o,(x1,y1,x2,y2,fmx,fmy,f)
    o,(x1,y1,x2,y2,fmx,fmy,f)=poly(560,84,16,-9,'右下角',RED); b+=o
    b.append(T(x1+8,(84+y1)/2+4,'f_{V} = 0.0200P',12,BLUE))
    b.append(T((x1+x2)/2-14,(y1+y2)/2+10,'f_{M} = 0.0835P',12,ORG,'end'))
    b.append(T((560+x2)/2+10,(84+y2)/2+30,f'合力 {f:.4f}P',13,PUR,'start','700'))
    b.append(T(560,y2+30,'兩分力都朝下 → 相加',12,RED,'middle'))
    o,(x1,y1,x2,y2,fmx,fmy,f2)=poly(670,330,-4,21,'左上角',GREEN); b+=o
    b.append(T(x1-8,(330+y1)/2+8,'f_{V} = 0.0200P',12,BLUE,'end'))
    b.append(T((x1+x2)/2,y2-14+(y1-y2)/2-6,f'f_{{M}} = {math.hypot(fmx,fmy):.4f}P',12,ORG,'middle'))
    b.append(T(665,392,f'合力 {f2:.4f}P（垂直分量只剩 −0.0018P，幾乎抵消）',12.5,PUR,'middle','700'))
    b.append(R(470,410,390,40,LORG,ORG,1.2,8))
    b.append(T(665,435,'0.1014P ≤ 1.565 tf/cm → P_{u} = 15.4 tf',13.5,RED,'middle','700'))
    return svg(880,460,''.join(b),'範例D偏心L形銲道的幾何與向量合成')

# ---------------- 圖 7-1 梁端彎矩分兩路 + 腹板銲道應力向量 ----------------
def f71():
    p='f71'; b=[markers(p,{'r':RED,'b':BLUE,'o':ORG,'u':PUR,'k':EDGE})]
    # elevation
    yt,yb,tf=70,290,14
    b.append(R(50,30,36,300,STEEL,EDGE,1.5)); b.append(T(68,24,'柱',12,MUT,'middle'))
    b.append(R(90,yt,240,tf,'#cfd8dc',EDGE,1.4)); b.append(R(90,yb-tf,240,tf,'#cfd8dc',EDGE,1.4))
    b.append(R(90,yt+tf,240,yb-yt-2*tf,'#f5f5f5',EDGE,1.2))
    b.append(T(210,186,'腹板',12,MUT,'middle'))
    # flange welds (groove symbol) and web fillet
    b.append(P([(86,yt),(98,yt),(90,yt+tf),(86,yt+tf)],RED,RED,1))
    b.append(P([(86,yb-tf),(90,yb-tf),(98,yb),(86,yb)],RED,RED,1))
    b.append(L(89,yt+tf+8,89,yb-tf-8,ORG,4))
    b.append(T(104,yt-8,'翼板銲（實務多為 CJP）',11.5,RED))
    b.append(T(100,yt+tf+30,'腹板填角銲',11.5,ORG))
    # stress diagram at column face
    sx=430; mid=(yt+yb)/2; sm=90
    b.append(L(sx,yt-10,sx,yb+10,EDGE,1.2)); b.append(L(sx-8,mid,sx+130,mid,MUT,1,'4,3'))
    b.append(T(sx+132,mid+4,'中性軸',11.5,MUT))
    sig=lambda y: sm*(mid-y)/(mid-yt)
    # flange blocks
    for y0,y1,c,fill in [(yt,yt+tf,RED,'#ffcdd2'),(yb-tf,yb,BLUE,'#bbdefb')]:
        b.append(P([(sx,y0),(sx+sig(y0),y0),(sx+sig(y1),y1),(sx,y1)],fill,c,1.2))
    b.append(P([(sx,yt+tf),(sx+sig(yt+tf),yt+tf),(sx,mid)],'#ffe0b2',ORG,1.2))
    b.append(P([(sx,mid),(sx+sig(yb-tf),yb-tf),(sx,yb-tf)],'#ffe0b2',ORG,1.2))
    b.append(arrow(sx+sm+6,yt+7,sx+sm+56,yt+7,RED,2.6,p,'r')); b.append(T(sx+sm+60,yt+11,'T = M_{f}/d',12.5,RED,weight='700'))
    b.append(arrow(sx+sm+56,yb-7,sx+sm+6,yb-7,BLUE,2.6,p,'b'))
    b.append(T(sx+sm+60,yb-3,'C = M_{f}/d',12.5,BLUE,weight='700'))
    b.append(T(sx+30,mid-36,'M_{w}',13,ORG,'start','700'))
    b.append(T(sx,yb+30,'接頭面應力：翼板≈均勻 → 力偶；腹板三角形 → 彎矩',11.5,MUT,'middle'))
    b.append(T(sx,yb+48,'SS-2018-3：M_{f} : M_{w} = 124.5 : 25.5（83% : 17%）',11.5,MUT,'middle'))
    # stress element vectors (Example E) scale 100 px per tf/cm²
    k=120; ex,ey=672,160
    b.append(T(ex+90,128,'範例 E：腹板銲道最上端的應力',12.5,INK,'middle','700'))
    sM,tV=1.102,0.279; f=math.hypot(sM,tV); fa=1.476
    b.append(path(f'M{ex+fa*k:.1f},{ey} A{fa*k:.1f},{fa*k:.1f} 0 0 1 {ex+fa*k*math.cos(math.radians(24)):.1f},{ey+fa*k*math.sin(math.radians(24)):.1f}',c=GREEN,sw=1.6,dash='6,4'))
    b.append(T(ex+fa*k+4,ey-8,'容許 f_{a} = 1.476',12,GREEN,'end'))
    b.append(arrow(ex,ey,ex+sM*k,ey,ORG,3,p,'o'))
    b.append(T(ex+42,ey-8,'σ_{M} = 1.102',12,ORG,'middle'))
    b.append(arrow(ex+sM*k,ey,ex+sM*k,ey+tV*k,BLUE,3,p,'b'))
    b.append(T(ex+sM*k-6,ey+tV*k+18,'τ_{V} = 0.279',12,BLUE,'end'))
    b.append(arrow(ex,ey,ex+sM*k,ey+tV*k,PUR,3.2,p,'u'))
    y=ey+tV*k+46
    b.append(T(ex-10,y,f'f = √(σ² + τ²) = {f:.3f}',12.5,PUR,'start','700'))
    b.append(T(ex-10,y+20,f'f / f_{{a}} = {f/fa:.2f} < 1.0 → OK',12.5,GREEN,'start','700'))
    b.append(T(ex-10,y+40,'（單位 tf/cm²，三向量同一比例尺）',11.5,MUT))
    b.append(T(ex-10,y+60,'直接相加 1.381 → 把向量當純量，錯',11.5,RED))
    return svg(880,380,''.join(b),'梁端彎矩分為翼板力偶與腹板彎曲')

# ---------------- 圖 7-2 節點域（側移下的正確受力方向） ----------------
def f72():
    p='f72'; b=[markers(p,{'r':RED,'b':BLUE,'k':EDGE,'u':PUR})]
    cl,cr,tf=330,450,12
    yt,yb,ft=130,250,10
    b.append(R(cl,20,tf,330,STEEL,EDGE,1.4)); b.append(R(cr-tf,20,tf,330,STEEL,EDGE,1.4))
    b.append(R(cl+tf,20,cr-cl-2*tf,330,'#f5f5f5',EDGE,1))
    for x0,x1 in [(60,cl),(cr,720)]:
        b.append(R(x0,yt,x1-x0,ft,'#cfd8dc',EDGE,1.3)); b.append(R(x0,yb-ft,x1-x0,ft,'#cfd8dc',EDGE,1.3))
        b.append(R(x0,yt+ft,x1-x0,yb-yt-2*ft,'#fafafa','#b0bec5',0.8))
    b.append(T(160,196,'左梁',12.5,MUT,'middle')); b.append(T(620,196,'右梁',12.5,MUT,'middle'))
    # panel zone
    b.append(R(cl+tf,yt+ft,cr-cl-2*tf,yb-yt-2*ft,'#fff9c4',ORG,2))
    d=14
    b.append(P([(cl+tf+d,yt+ft),(cr-tf+d,yt+ft),(cr-tf-d,yb-ft),(cl+tf-d,yb-ft)],'none',RED,2,dash='6,4'))
    b.append(T((cl+cr)/2,(yt+yb)/2+5,'節點域',14,ORG,'middle','700'))
    # continuity plates
    for y in [yt+ft/2,yb-ft/2]: b.append(L(cl+tf,y,cr-tf,y,GREEN,5))
    # flange forces (all on the joint): top → right, bottom → left
    yT=yt+ft/2; yB=yb-ft/2
    b.append(arrow(cl-110,yT,cl-6,yT,RED,3,p,'r')); b.append(T(cl-110,yT-10,'C_{1} = M_{b1}/d_{b}（壓，推入）',12,RED))
    b.append(arrow(cr+6,yT,cr+110,yT,RED,3,p,'r')); b.append(T(cr+10,yT-10,'T_{2} = M_{b2}/d_{b}（拉，拉出）',12,RED))
    b.append(arrow(cl-6,yB,cl-110,yB,BLUE,3,p,'b')); b.append(T(cl-110,yB+22,'T_{1}（拉，拉出）',12,BLUE))
    b.append(arrow(cr+110,yB,cr+6,yB,BLUE,3,p,'b')); b.append(T(cr+10,yB+22,'C_{2}（壓，推入）',12,BLUE))
    # column shears
    b.append(arrow((cl+cr)/2+40,40,(cl+cr)/2-40,40,PUR,2.6,p,'u')); b.append(T((cl+cr)/2+46,44,'V_{c}',13,PUR,weight='700'))
    b.append(arrow((cl+cr)/2-40,330,(cl+cr)/2+40,330,PUR,2.6,p,'u')); b.append(T((cl+cr)/2-46,334,'V_{c}',13,PUR,'end','700'))
    # notes
    b.append(T(40,380,'側移（地震）時兩根梁的彎矩同向 → 上翼板兩個力都向右、下翼板都向左 → 在柱腹板疊加成剪力。',12.5,INK))
    b.append(T(40,400,'（若畫成上翼板兩力「相對」，那是對稱重力載重：兩力抵消，節點域幾乎不受剪。）',12,MUT))
    b.append(R(560,20,300,96,LBLUE,BLUE,1.2,8))
    b.append(T(574,44,'需求：V_{pz} = M_{b1}/d_{b} + M_{b2}/d_{b} − V_{c}',12.5,'#0d47a1',weight='700'))
    b.append(T(574,68,'強度：φ_{v}V_{n} = 0.9 × 0.6F_{y}d_{c}t_{w}',12.5,'#0d47a1'))
    b.append(T(574,92,'綠＝連續板（傳翼板集中力，不抗剪）',11.5,GREEN))
    b.append(T(574,108,'紅虛線＝剪切後的節點域',11.5,RED))
    return svg(880,415,''.join(b),'節點域剪力的正確受力方向')

# ---------------- 圖 7-3 補強式 vs RBS（平面＋立面） ----------------
def f73():
    p='f73'; b=[markers(p,{'k':EDGE,'r':RED})]
    b.append(L(440,20,440,505,'#cfd8dc',1.5,'6,5'))
    # left reinforced (elevation)
    b.append(T(220,28,'補強式：把接頭做強（立面）',14,BLUE,'middle','700'))
    b.append(R(30,60,30,300,STEEL,EDGE,1.4))
    yt,yb=140,280
    b.append(R(60,yt,360,10,'#cfd8dc',EDGE,1.3)); b.append(R(60,yb-10,360,10,'#cfd8dc',EDGE,1.3))
    b.append(R(60,yt+10,360,yb-yt-20,'#fafafa','#b0bec5',0.8))
    Lc=150
    b.append(R(60,yt-10,Lc,10,'#90caf9',BLUE,1.4)); b.append(R(60,yb,Lc,10,'#90caf9',BLUE,1.4))
    b.append(T(64,yt-16,'蓋板',11.5,BLUE))
    hx=60+Lc+35
    b.append(R(hx-22,yt-2,44,yb-yt+4,'#ffcdd2','none',0,extra=' fill-opacity="0.6"'))
    b.append(T(hx,(yt+yb)/2+5,'塑鉸區',12.5,RED,'middle','700'))
    b.append(dimh(60,60+Lc,yb+34,'補強長度',BLUE,11.5))
    b.append(T(70,340,'塑鉸被「推」到補強端之外、遠離柱面銲道',12,INK))
    b.append(T(70,360,'代價：柱、節點域、銲道需求都隨 M_{pr} 移出去而變大',12,MUT))
    # right RBS: plan of top flange (scale 0.5 px/mm, bf=300, d=600)
    sc=0.36; bf=300; dd=600; a=0.625*bf; bb=0.75*dd; c=0.2*bf
    R_=(4*c*c+bb*bb)/(8*c)
    x0=470; yc=112
    b.append(T(660,28,'削弱式 RBS：把梁做弱',14,RED,'middle','700'))
    
    b.append(R(x0-14,yc-bf*sc/2-20,14,bf*sc+40,STEEL,EDGE,1.4))
    xa=x0+a*sc; xb=xa+bb*sc; xm=(xa+xb)/2
    top=yc-bf*sc/2; bot=yc+bf*sc/2
    # arc points
    def arc(sign):
        pts=[]
        for k in range(41):
            x=xa+(xb-xa)*k/40; u=(x-xm)/sc
            dep=c-(R_-math.sqrt(R_*R_-u*u))
            pts.append((x, (top+dep*sc) if sign<0 else (bot-dep*sc)))
        return pts
    up=arc(-1); lo=arc(1)
    outline=[(x0,top),(xa,top)]+up+[(860,top),(860,bot),(xb,bot)]+lo[::-1]+[(xa,bot),(x0,bot)]
    b.append(P(outline,'#ffebee',RED,1.6))
    b.append(P([(xa,top)]+up+[(xb,top)],'#ffffff','none',0))
    b.append(L(xa,top,xb,top,RED,0.8,'3,3')); b.append(L(xa,bot,xb,bot,RED,0.8,'3,3'))
    b.append(dimh(x0,xa,top-10,'a',MUT,12))
    b.append(dimh(xa,xb,top-10,'b',MUT,12))
    b.append(L(xm,top,xm,top+c*sc,RED,1.4)); b.append(T(xm+5,top+c*sc-6,'c',12,RED))
    b.append(T(x0,bot+18,'上翼板平面（俯視）',11.5,MUT))
    b.append(L(xm,bot+6,xm,212,RED,1,'3,3'))
    # elevation below
    ey0,ey1=212,212+dd*sc
    b.append(T(x0+4,ey1+18,'立面（與平面同比例）',11.5,MUT))
    b.append(R(x0-14,ey0-14,14,ey1-ey0+28,STEEL,EDGE,1.4))
    b.append(R(x0,ey0,390,8,'#cfd8dc',EDGE,1.2)); b.append(R(x0,ey1-8,390,8,'#cfd8dc',EDGE,1.2))
    b.append(R(x0,ey0+8,390,ey1-ey0-16,'#fafafa','#b0bec5',0.8))
    b.append(R(xa,ey0-2,xb-xa,ey1-ey0+4,'#ffcdd2','none',0,extra=' fill-opacity="0.6"'))
    b.append(T(xm,(ey0+ey1)/2+5,'塑鉸區（削弱段中央）',12,RED,'middle','700'))
    b.append(T(x0-10,460,'AISC 358：a = 0.5～0.75b_{f}、b = 0.65～0.85d、c ≤ 0.25b_{f}',11.5,INK))
    b.append(T(x0-10,480,'圖以 b_{f} = 300、d = 600 mm，取 a = 0.625b_{f}、b = 0.75d、c = 0.2b_{f} 繪製',11.5,MUT))
    b.append(T(x0-10,500,'削的是翼板「寬度」—— 立面上看不到凹口',11.5,RED,weight='700'))
    return svg(880,515,''.join(b),'補強式與削弱式RBS耐震接頭')
