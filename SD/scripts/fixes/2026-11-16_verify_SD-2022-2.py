#!/usr/bin/env python3
"""SD-2022-2 勘誤驗證（2026-11-16）：§5.1 數值示例獨立重算＋現行條文值出現檢查＋舊值殘留檢查。
條文來源：建築物混凝土結構設計規範 112 年版 18.3.2.1、18.3.3.1–3、18.3.4.1–6（國土管理署 PDF）。"""
import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2022-2", "SD-2022-2.md")
s = open(P, encoding="utf-8").read().replace("\r\n", "\n")
mm = []
def chk(name, got, exp, tol=0.051):
    ok = abs(got - exp) <= tol; print(f"{'OK ' if ok else 'BAD'} {name}: {got:.4g} vs {exp}"); ok or mm.append(name)
# 示例：柱 c1=c2=60 cm，梁 h=70、d=64 cm，主筋 D25 db=2.54 cm，箍筋 D13 dh=1.27 cm
c1 = c2 = 60.0; h = 70.0; d = 64.0; db = 2.54; dh = 1.27
chk("梁寬上限 現行", c2 + 2*min(c2, 0.75*c1), 150)
chk("梁寬上限 舊式", c2 + 1.5*h, 165)
chk("間距 現行", min(d/4, 6*db, 15.0), 15)
chk("6db", 6*db, 15.24, 0.005)
chk("間距 舊式", min(d/4, 8*db, 24*dh, 30.0), 16)
chk("8db", 8*db, 20.3, 0.05); chk("24dh", 24*dh, 30.5, 0.05)
chk("2h", 2*h, 140); chk("2d", 2*d, 128)
chk("ρ 材料式 (fc'+100)/(4fy)", (280 + 100)/(4*4200), 0.0226, 0.00005)
# 條文值必須出現在正本（§2 以後）
body = s[s.index("\n## 2."):]
for t in ["c_2 + 2\\min(c_2,\\ 0.75c_1)", "\\ell_n \\geq 4d", "0.3h", "0.025", "1/4", "2h", "6d_b", "15\\,\\text{cm}", "10\\,\\text{cm}", "35 cm", "d/2", "5 cm"]:
    ok = t in body; print(("OK " if ok else "BAD"), "出現", t); ok or mm.append("缺 " + t)
# 舊值殘留：只准在 §5.1 對照表、§5.5 舊解對照
a = body.index("### 5.1"); b = body.index("### 5.2"); c = body.index("### 5.5")
main = (body[:a] + body[b:c]).replace("不是 $2d$", "").replace("舊解的 $2d=128$ cm 偏短", "").replace("$2d$／$2h$ 混淆", "")   # 陷阱提示與圖說點名舊錯，允許
for t in ["1.5h", "8d_{bl}", "24d_{bh}", "300\\,\\text{mm}", "2d", "4h", "b_c"]:
    n = main.count(t); print(("OK " if n == 0 else "BAD"), "殘留", t, n); n and mm.append("殘留 " + t)
print("MISMATCHES:", len(mm), mm if mm else "")
