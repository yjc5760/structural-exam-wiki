#!/usr/bin/env python3
"""SD-2009-4 勘誤驗算（2026-11-16）：圓柱螺箍筋體積比與構造檢核（現行混凝土結構設計規範 112 年版）。
路徑 1 精確體積式 π(Dc−db)Asp/(Ach s)；路徑 2 近似式 4Asp/(Dc s)。最後印 MISMATCHES。"""
import sys, math
from pathlib import Path
SD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
md = (SD/"raw/solutions/SD-2009-4/SD-2009-4.md").read_text(encoding="utf-8")
D,cv,fc,fy,s=55.,4.,350.,4200.,7.5; dsp,Asp=1.27,1.267; db,Ab=2.54,5.067
mm=0
def chk(n,a,b,tol):
    global mm; ok=abs(a-b)<=tol; mm+=(not ok); print(("OK " if ok else "BAD"),n,round(a,5),"vs",b)
Dc=D-2*cv; Ag=math.pi*D**2/4; Ach=math.pi*Dc**2/4
chk("Dc",Dc,47,0); chk("Ag",Ag,2375.8,0.1); chk("Ach",Ach,1734.9,0.1); chk("Ag/Ach",Ag/Ach,1.3693,1e-4)
req=0.45*(Ag/Ach-1)*fc/fy; chk("ρs,req",req,0.01385,1e-5)
act=math.pi*(Dc-dsp)*Asp/(Ach*s); chk("ρs 精確",act,0.01399,1e-5)
app=4*Asp/(Dc*s); chk("ρs 近似（路徑 2）",app,0.01438,1e-5); chk("近似亦 ≥ req",float(app>=req),1,0)
chk("裕度",act/req,1.010,1e-3); chk("0.12f'c/fyt",0.12*fc/fy,0.0100,1e-5)
chk("淨螺距",s-dsp,6.23,0.005); chk("ρg",9*Ab/Ag,0.0192,1e-4); chk("D/4",D/4,13.75,0); chk("6db",6*db,15.24,0)
chk("ρs@8cm（§5.2）",math.pi*(Dc-dsp)*Asp/(Ach*8),0.01312,1e-5)
chk("dagg 上限 6.23×3/4",(s-dsp)*0.75,4.67,0.01)
fl=act*fy/2; chk("f_l",fl,29.4,0.05); chk("f'cc",fc+4.1*fl,470.5,0.3)
for t in ["Step 6：構造檢核","25.7.3.1","25.7.3.2","10.7.3.1","10.6.1.1","18.4.5.3","0.0100","6.23","1.92\\%"]:
    if t not in md: mm+=1; print("BAD 正本缺",t)
print("MISMATCHES:",mm)
