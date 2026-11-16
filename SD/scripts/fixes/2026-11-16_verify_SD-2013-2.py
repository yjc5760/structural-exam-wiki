#!/usr/bin/env python3
"""SD-2013-2 勘誤驗算（2026-11-16）：韌性抗彎構架梁撓曲與容量設計剪力（現行混凝土結構設計規範 112 年版）。
單位 kgf、cm；Tf-m＝1e5 kgf-cm。路徑 1 疊代 a；路徑 2 二次式 ρ。V_e 另以對 A 端取彎矩交叉。最後印 MISMATCHES。"""
import sys, math
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
md = (SD/"raw/solutions/SD-2013-2/SD-2013-2.md").read_text(encoding="utf-8")
fc,fy,b,d=280.,4200.,40.,53.; Ab25,db25=5.067,2.54; Av=2*1.267; ln=6.40
mm=0
def chk(n,a,b,tol=0.01):
    global mm; ok=abs(a-b)<=tol; mm+=(not ok); print(("OK " if ok else "BAD"),n,round(a,3),"vs",b)
def As_it(Mu):
    a=10.
    for _ in range(60): As=Mu*1e5/(0.9*fy*(d-a/2)); a=As*fy/(0.85*fc*b)
    return As
def As_q(Mu):
    Rn=Mu*1e5/(0.9*b*d*d); return 0.85*fc/fy*(1-math.sqrt(1-2*Rn/(0.85*fc)))*b*d
for Mu,v in ((40,21.98),(20,10.44),(19,9.89),(17,8.81),(48,26.99)):
    chk(f"As(Mu={Mu}) 疊代",As_it(Mu),v); chk(f"As(Mu={Mu}) 二次式",As_q(Mu),v)
chk("As,min",max(14/fy,0.8*math.sqrt(fc)/fy)*b*d,7.07)
def sec(n):
    As=n*Ab25; a=As*fy/(0.85*fc*b); c=a/0.85; et=0.003*(d-c)/c; Mn=As*fy*(d-a/2)/1e5
    ap=1.25*As*fy/(0.85*fc*b); Mpr=As*1.25*fy*(d-ap/2)/1e5; return As,a,et,Mn,ap,Mpr
for n,phiMn,et,Mpr,ap in ((5,45.40,0.0091,61.20,13.97),(6,53.20,0.0071,71.21,16.77),(3,28.53,0.0172,38.95,8.38),(2,19.45,0.0272,None,None)):
    As,a,e,Mn,a2,M2=sec(n); chk(f"{n}-D25 φMn",0.9*Mn,phiMn); chk(f"{n}-D25 εt",e,et,1e-4)
    if Mpr: chk(f"{n}-D25 Mpr",M2,Mpr); chk(f"{n}-D25 a_pr",a2,ap)
Mn6=sec(6)[3]; Mn5=sec(5)[3]; Mn3=sec(3)[3]; Mn2=sec(2)[3]
chk("B 柱面 Mn+ ≥ ½Mn-",float(Mn3>=0.5*Mn6),1); chk("A 柱面 Mn+ ≥ ½Mn-",float(Mn3>=0.5*Mn5),1); chk("¼Mn,max ≤ 頂連續 2-D25",float(Mn2>=Mn6/4),1)
chk("2-D25 Mn",Mn2,21.61); chk("½×59.11",0.5*Mn6,29.56,0.05)
chk("6-D25 淨距",(40-8-2*1.27-6*db25)/5,2.84)
wu=1.2*2.7+1.0*1.4; chk("wu",wu,4.64)
Veq=(38.95+71.21)/ln; Vg=wu*ln/2; Ve=Veq+Vg
chk("Veq2",Veq,17.21); chk("Veq1",(61.20+38.95)/ln,15.65); chk("Vg",Vg,14.85); chk("Ve",Ve,32.06)
chk("Ve 對 A 取彎矩",(38.95+71.21+wu*ln**2/2)/ln,32.06); chk("Veq/Ve",Veq/Ve,0.537,1e-3)
Vs=32.06/0.75; chk("Vs",Vs,42.75); chk("s_req",Av*fy*d/(Vs*1000),13.2,0.05); chk("Vs,max",2.12*math.sqrt(fc)*b*d/1000,75.2,0.05)
chk("s_max",min(d/4,15,6*db25),13.25); chk("φVs@12",0.75*Av*fy*d/12/1000,35.25); chk("φVs@13（舊配）",0.75*Av*fy*d/13/1000,32.54)
Vx=32.06-wu*1.2; Vc=0.53*math.sqrt(fc)*b*d/1000; chk("Vu@2h",Vx,26.49); chk("Vc",Vc,18.80); chk("Vs2",Vx/0.75-Vc,16.52); chk("s2",Av*fy*d/((Vx/0.75-Vc)*1000),34.1,0.05)
chk("Av,min@25",max(0.2*math.sqrt(fc)*b*25/fy,3.5*b*25/fy),0.83)
wu5=1.2*2.7+0.5*1.4; Ve5=Veq+wu5*ln/2; chk("0.5L Ve",Ve5,29.82); chk("0.5L 比值",Veq/Ve5,0.577,1e-3)
for s in ["5-D25","6-D25","3-D25","61.20","71.21","38.95","32.06","@12 cm","@25 cm","min\\!\\left(\\frac{d}{4},\\; 15\\text{ cm},\\; 6 d_b\\right)"]:
    if s not in md: mm+=1; print("BAD 正本缺",s)
body=md.split("### 5.4")[0].split("## 2.")[1]
for s in ["54.17","64.57","34.93","29.44","26.98","24 d_{b,","30 \\text{ cm}\\right)","@13 cm","@26 cm","8 d_{b"]:
    if s in body: mm+=1; print("BAD §2–§5.3 殘留舊值",s)
print("MISMATCHES:",mm)
