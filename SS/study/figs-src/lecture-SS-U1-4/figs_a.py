from lib import *
import math

# ---------------- 圖 1-1 螺栓搭接五關卡（平面＋立面） ----------------
def f11():
    p='f11'; b=[markers(p,{'r':RED,'k':EDGE})]
    b.append(T(30,26,'平面圖（俯視；B 板疊在 A 板上，以半透明表示）',13,MUT))
    # plates
    yA0,yA1=60,180
    b.append(R(70,yA0,450,120,LBLUE,BLUE,1.8))
    b.append(R(340,yA0,450,120,'#fff8e1',ORG,1.8,extra=' fill-opacity="0.72"'))
    b.append(T(110,yA0-8,'母材 A',13,BLUE,weight='700'))
    b.append(T(780,yA0-8,'母材 B',13,ORG,'end','700'))
    cols=[370,430,490]; rows=[90,150]
    # GSY
    b.append(L(190,yA0-4,190,yA1+4,GREEN,1.6,'4,3'))
    # NSF on B through column nearest B body (x=490)
    b.append(L(490,yA0-4,490,yA1+4,RED,2,'6,3'))
    # Block shear in A: tension plane at x=370 between rows, shear planes along rows to A end (x=520)
    b.append(P([(370,90),(520,90),(520,150),(370,150)],'#ce93d8',PUR,2.2,dash='7,3',extra=' fill-opacity="0.25"'))
    for x in cols:
        for y in rows:
            b.append(C(x,y,8.5,'#fff',EDGE,1.6))
    b.append(L(520,yA0,520,yA1,BLUE,1.2,'3,3'))
    b.append(T(524,yA1+16,'A 端',11,BLUE))
    b.append(T(336,yA1+16,'B 端',11,ORG,'end'))
    # loads
    b.append(arrow(68,120,22,120,RED,3,p,'r')); b.append(T(30,110,'T',14,RED,weight='700'))
    b.append(arrow(792,120,850,120,RED,3,p,'r')); b.append(T(842,110,'T',14,RED,'end','700'))
    # number tags plan
    b.append(num(190,yA1+22,'0',GREEN)); b.append(num(445,yA1+30,'2',PUR)); b.append(num(490,yA0-16,'1',RED))
    b.append(L(445,yA1+20,445,152,PUR,1))
    # ---- elevation
    b.append(T(30,232,'立面圖（側視；承壓型已滑移、孔壁貼住螺栓）',13,MUT))
    yB0,yB1,yAa,yAb=290,312,312,334   # B on top, A below
    b.append(R(70,yAa,450,22,LBLUE,BLUE,1.8))
    b.append(R(340,yB0,450,22,'#fff8e1',ORG,1.8))
    for x in cols:
        # holes (white gaps), A hole shifted left: right wall touches shank; B hole shifted right
        b.append(R(x+8-22,yAa+0.9,22,20.2,'#fff','none',0))
        b.append(R(x-8,yB0+0.9,22,20.2,'#fff','none',0))
        b.append(R(x-8,yB0-6,16,yAb-yB0+12,'#cfd8dc',EDGE,1.5))
        b.append(R(x-15,yB0-15,30,9,'#90a4ae',EDGE,1.4))
        b.append(R(x-15,yAb+6,30,9,'#90a4ae',EDGE,1.4))
        # bearing contact highlight
        b.append(L(x+8,yAa+2,x+8,yAb-2,ORG,3.2))
        b.append(L(x-8,yB0+2,x-8,yB1-2,ORG,3.2))
    # shear plane & faying surface
    b.append(L(340,yB1,520,yB1,TEAL,2.4,'2,0'))
    for x in cols: b.append(L(x-11,yB1,x+11,yB1,PUR,2.6,'4,2'))
    b.append(arrow(68,323,22,323,RED,3,p,'r')); b.append(arrow(792,301,850,301,RED,3,p,'r'))
    # tags elevation
    b.append(num(430,372,'3',PUR)); b.append(L(430,362,430,yB1+1,PUR,1))
    b.append(num(510,372,'4',ORG)); b.append(L(503,364,498,326,ORG,1))
    b.append(num(330,372,'5',TEAL)); b.append(L(337,363,355,yB1+1,TEAL,1))
    # legend
    leg=[('0',GREEN,'全斷面降伏 GSY（孔外，φ=0.90）'),('1',RED,'淨斷面斷裂 NSF（過孔斷面；A、B 各驗）'),
         ('2',PUR,'塊狀剪力 BSR（A 板端被撕下的塊）'),('3',PUR,'螺栓剪斷（A／B 交界的剪力面）'),
         ('4',ORG,'孔壁承壓／撕裂（孔壁朝板端那一側）'),('5',TEAL,'接觸面滑動（僅摩阻型）')]
    for i,(n,c,t) in enumerate(leg):
        x=40+(i%2)*420; y=410+(i//2)*26
        b.append(num(x,y-4,n,c,9)); b.append(T(x+16,y,t,12.5,INK))
    return svg(880,480,''.join(b),'螺栓搭接接合的六個極限狀態位置')

# ---------------- 圖 2-1 延性 vs 脆性 ----------------
def f21():
    p='f21'; b=[markers(p,{'k':EDGE})]
    ox,oy,W,H=80,290,500,240
    b.append(arrow(ox,oy,ox+W+20,oy,EDGE,1.6,p,'k')); b.append(arrow(ox,oy,ox,oy-H-20,EDGE,1.6,p,'k'))
    b.append(T(ox+W+18,oy+20,'伸長量 Δ',12.5,MUT,'end')); b.append(T(ox-8,oy-H-24,'載重 P',12.5,MUT,'start'))
    X=lambda u: ox+u*W; Y=lambda v: oy-v*H
    # ductile: elastic to (0.06,0.60), plateau to 0.18, hardening to peak (0.62,0.86), necking to (0.84,0.74)
    pts=[(0,0),(0.06,0.60),(0.18,0.60)]
    for k in range(1,41):
        t=k/40; u=0.18+t*0.44; v=0.60+0.26*(1-(1-t)**2); pts.append((u,v))
    for k in range(1,21):
        t=k/20; u=0.62+t*0.22; v=0.86-0.12*t**1.6; pts.append((u,v))
    b.append(P([(X(u),Y(v)) for u,v in pts],'none',GREEN,3,close=False))
    b.append(C(X(0.84),Y(0.74),5,GREEN,GREEN))
    b.append(T(X(0.84)+8,Y(0.74)+4,'斷',12,GREEN))
    b.append(L(X(0.06),Y(0.60),X(0.06),oy,GREEN,1,'3,3'))
    b.append(T(X(0.06),oy+16,'Δ_{y}',12,GREEN,'middle'))
    b.append(T(X(0.40),Y(0.92),'延性（降伏 F_{y}·A_{g}）：降伏後還走很長一段',13,GREEN,'middle','700'))
    b.append(L(ox,Y(0.60),X(0.06),Y(0.60),GREEN,1,'3,3')); b.append(T(ox-6,Y(0.60)+4,'P_{y}',12,GREEN,'end'))
    # brittle: same stiffness to (0.07,0.70) then sudden drop
    b.append(P([(X(0),Y(0)),(X(0.07),Y(0.70))],'none',RED,3,close=False))
    b.append(L(X(0.07),Y(0.70),X(0.075),oy,RED,2,'5,3'))
    b.append(C(X(0.07),Y(0.70),5,RED,RED))
    b.append(T(X(0.09),Y(0.42),'脆性（斷裂 F_{u}·A_{n}）：到頂就掉',13,RED,'start','700'))
    b.append(T(X(0.09),Y(0.42)+20,'可用變形 ≈ 0，沒有警告',12,RED,'start'))
    # boxes
    b.append(R(612,52,250,104,LGRN,GREEN,1.5,10))
    b.append(T(628,78,'變形大、看得見、可預警',13,GREEN)); b.append(T(628,100,'F_{y} 離散小 → 不確定性小',13,GREEN))
    b.append(T(628,132,'φ = 0.90（Ω = 1.67）',16,GREEN,weight='700'))
    b.append(R(612,176,250,104,LRED,RED,1.5,10))
    b.append(T(628,202,'無預警、F_{u} 離散較大',13,RED)); b.append(T(628,224,'→ 必須更保守',13,RED))
    b.append(T(628,256,'φ = 0.75（Ω = 2.00）',16,RED,weight='700'))
    return svg(880,320,''.join(b),'延性降伏與脆性斷裂的載重-變形曲線')

# ---------------- 圖 3-1 剪力遲滯：斷面（範例 A 比例）＋應力分佈 ----------------
def f31():
    p='f31'; b=[markers(p,{'k':EDGE,'b':BLUE})]
    s=1.45  # px per mm
    # cross-section L125x125x12, heel at (x0,y0) ; connected leg vertical (against gusset at its back face)
    x0,y0=150,240   # heel (outside corner) bottom-left
    t=12; Lg=125
    # gusset plate to the left of connected leg back face
    b.append(T(30,24,'(a) 斷面 L125×125×12（比例 1:1 縮放）',13,INK,weight='700'))
    b.append(R(x0-14*s,y0-Lg*s-24,14*s,Lg*s+34,'#cfd8dc',EDGE,1.4))
    b.append(T(x0-14*s-6,y0+4,'接合板',11.5,MUT,'end'))
    pts=[(x0,y0),(x0,y0-Lg*s),(x0+t*s,y0-Lg*s),(x0+t*s,y0-t*s),(x0+Lg*s,y0-t*s),(x0+Lg*s,y0)]
    b.append(P(pts,LBLUE,BLUE,1.8))
    # bolt line at 45 mm from heel along connected leg
    yb=y0-45*s
    b.append(R(x0-14*s-8,yb-11*s,14*s+t*s+16,22*s,'#b0bec5',EDGE,1.2))
    b.append(L(x0-14*s-16,yb,x0+t*s+16,yb,MUT,0.8,'6,3'))
    b.append(T(x0-14*s-14,yb-18,'螺栓線',11.5,MUT,'end')); b.append(T(x0-14*s-14,yb-4,'（距肢背 45）',11.5,MUT,'end'))
    # centroid x̄=35.3 mm from connection plane (back face of connected leg), same ȳ
    xc=x0+35.3*s; yc=y0-35.3*s
    b.append(C(xc,yc,5,RED,RED)); b.append(T(xc+8,yc+18,'形心 C',12,RED))
    b.append(L(x0,yc,xc,yc,RED,1,'3,2'))
    b.append(dimh(x0,xc,y0+22,'~{x̄} = 35.3 mm',RED,12.5,ty=y0+40))
    b.append(L(x0,y0+4,x0,y0+28,RED,0.8)); b.append(L(xc,yc+6,xc,y0+28,RED,0.8,'2,2'))
    b.append(T(x0+t*s/2+4,y0-Lg*s-8,'連接肢',12,BLUE,'start'))
    b.append(T(x0+Lg*s,y0-t*s-8,'外伸肢',12,BLUE,'end'))
    b.append(T(30,312,'~{x̄}：形心到「連接面」（肢背貼接合板的那一面）',12,MUT))
    b.append(T(30,330,'的垂直距離 —— 不是到螺栓線。',12,MUT))
    # (b) stress distribution on unfolded section at critical section
    b.append(T(400,24,'(b) 最後一排螺栓處的斷面應力（攤平兩肢）',13,INK,weight='700'))
    ox,oy=430,250; Wl=190; H=160
    b.append(arrow(ox,oy,ox+2*Wl+30,oy,EDGE,1.4,p,'k'))
    b.append(L(ox,oy,ox,oy-H-14,EDGE,1.4))
    b.append(L(ox+Wl,oy+4,ox+Wl,oy-H-6,MUT,1,'2,3'))
    b.append(T(ox+Wl/2,oy+20,'連接肢（125）',12,BLUE,'middle'))
    b.append(T(ox+1.5*Wl,oy+20,'外伸肢（125）',12,BLUE,'middle'))
    b.append(T(ox+Wl,oy+38,'角隅',11,MUT,'middle'))
    k=0.328
    actual=[(ox,oy-H),(ox+Wl,oy-H),(ox+2*Wl,oy-H*k),(ox+2*Wl,oy),(ox,oy)]
    b.append(P(actual,'#bbdefb',BLUE,2))
    ua=0.832
    b.append(L(ox,oy-H,ox+2*Wl+16,oy-H,RED,1.4,'6,3'))
    b.append(T(ox-6,oy-H+4,'F_{u}',13,RED,'end'))
    b.append(L(ox,oy-H*ua,ox+2*Wl+16,oy-H*ua,PUR,1.8,'8,4'))
    b.append(T(ox-6,oy-H*ua+4,'U·F_{u}',13,PUR,'end'))
    b.append(T(ox+2*Wl+20,oy-H*ua+4,'平均',12,PUR))
    b.append(T(ox+2*Wl+6,oy-H*k-8,'≈0.33F_{u}',12,BLUE,'end'))
    # lag annotation
    b.append(T(ox+1.5*Wl+6,oy-H*0.88,'外伸肢「來不及」分到力',12,ORG,'middle','700'))
    b.append(T(ox+0.5*Wl,oy-H*0.5,'連接肢先到 F_{u}',12.5,'#0d47a1','middle','700'))
    b.append(T(400,300,'斷裂的定義是「最大應力點到 F_{u}」。此時全斷面平均只有 U·F_{u}，',12,MUT))
    b.append(T(400,318,'故 P_{n} = F_{u}·(U·A_{n})。圖以範例 A 的 U = 0.832、外伸肢線性遞減反推，',12,MUT))
    b.append(T(400,336,'屬示意分佈（真實分佈還受孔位應力集中影響）。',12,MUT))
    return svg(880,350,''.join(b),'剪力遲滯：角鋼斷面與應力分佈')

# ---------------- 圖 3-2 U 曲線（精確） ----------------
def f32():
    p='f32'; b=[markers(p,{'k':EDGE})]
    ox,oy,W,H=90,270,640,230
    xmin,xmax=1,12
    X=lambda r: ox+(r-xmin)/(xmax-xmin)*W; Y=lambda u: oy-u*H
    for u in [0,0.2,0.4,0.6,0.8,1.0]:
        b.append(L(ox,Y(u),ox+W,Y(u),'#eceff1',1))
        b.append(T(ox-8,Y(u)+4,f'{u:.1f}',12,MUT,'end'))
    for r in range(1,13):
        b.append(L(X(r),oy,X(r),oy+5,EDGE,1)); b.append(T(X(r),oy+20,str(r),12,MUT,'middle'))
    b.append(L(ox,oy,ox+W+8,oy,EDGE,1.6)); b.append(L(ox,oy,ox,Y(1.08),EDGE,1.6))
    b.append(T(ox+W/2,oy+42,'接合長度比 L / ~{x̄}（無因次）',13,INK,'middle'))
    b.append(T(ox-56,Y(0.5),'U',15,INK,'middle',extra=f' font-family={SERIF!r} font-style="italic"'.replace("'",'"')))
    b.append(L(ox,Y(1),ox+W,Y(1),MUT,1.4,'6,4')); b.append(T(ox+W,Y(1)-6,'U = 1（無遲滯）',12,MUT,'end'))
    # table values for angles
    b.append(L(ox,Y(0.8),ox+W,Y(0.8),ORG,1.2,'3,4')); b.append(T(ox+W,Y(0.8)+15,'查表 0.80（角鋼，≥4 顆）',11.5,ORG,'end'))
    b.append(L(ox,Y(0.6),ox+W,Y(0.6),ORG,1.2,'3,4')); b.append(T(ox+W,Y(0.6)+15,'查表 0.60（角鋼，2～3 顆）',11.5,ORG,'end'))
    pts=[]
    n=220
    for k in range(n+1):
        r=xmin+(xmax-xmin)*k/n; pts.append((X(r),Y(1-1/r)))
    b.append(P(pts,'none',BLUE,3,close=False))
    marks=[(2,'(2, 0.50) 嚴重遲滯',RED,10,18),(4,'(4, 0.75)',ORG,8,18),(21/3.53,'範例 A：(5.95, 0.832)',PUR,-10,-12),(10,'(10, 0.90)',GREEN,0,-12)]
    for r,lab,c,dx,dy in marks:
        u=1-1/r; b.append(C(X(r),Y(u),5.5,c,'#fff',1.5))
        b.append(T(X(r)+dx,Y(u)+dy,lab,12.5,c,'start' if dx>=0 else 'end','700'))
    b.append(R(ox+330,Y(0.42)-6,300,62,LPUR,'#ce93d8',1.2,8))
    b.append(T(ox+344,Y(0.42)+14,'U = 1 − ~{x̄}/L = 1 − 1/(L/~{x̄})',13,PUR,weight='700'))
    b.append(T(ox+344,Y(0.42)+36,'範例 A 算得 0.832 ＞ 查表 0.80 → 能算就用算的',12,PUR))
    return svg(820,330,''.join(b),'U 隨接合長度比變化的精確曲線')
