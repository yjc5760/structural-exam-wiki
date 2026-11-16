#!/usr/bin/env python3
"""SD-2025-4 勘誤驗證（2026-11-16）：論述題，無數值答案。檢查現行條文值是否寫入、舊觀念／舊值是否殘留，並做 Ra、Fu 的邊界代入。
條文來源：建築物耐震設計規範及解說（111 年版）第 2.3、2.9、2.10 節；建築物混凝土結構設計規範（112 年版）第 18.3.3、18.3.4、18.4.5 節。"""
import os, math
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2025-4", "SD-2025-4.md")
s = open(P, encoding="utf-8").read().replace("\r\n", "\n")
mm = []
# Ra、Fu 邊界：R=1 時 Ra=1、Fu=1；等能量式在 Ra=1 時亦為 1
Ra = lambda R: 1 + (R - 1)/1.5
for R in (1.0, 2.5, 4.0):
    ra = Ra(R); fe = math.sqrt(2*ra - 1)
    ok = (R > 1 and 1 < fe < ra) or (R == 1 and abs(ra - 1) < 1e-12 and abs(fe - 1) < 1e-12)
    print(("OK " if ok else "BAD"), f"R={R}: Ra={ra:.3f}, sqrt(2Ra-1)={fe:.3f}"); ok or mm.append(f"Ra R={R}")
body = s[s.index("\n## 2."):]
for t in ["30 年", "475 年", "2500 年", "4.2\\alpha_y", "R_a=1+", "\\sqrt{2R_a-1}", "F_{uM}", "S_{aM}", "6d_b", "15 cm", "0.3A_gf'_c", "1/4"]:
    ok = t in body; print(("OK " if ok else "BAD"), "出現", t); ok or mm.append("缺 " + t)
main = body[:body.index("### 5.4")]
for t in ["2475", "1/2.5", "× 1.5", "0.35", "Fu（= R）", "≥ 8", "300 mm", "8d_b", "24 倍箍筋", "50 年 |", "小震≈50"]:
    n = main.count(t); print(("OK " if n == 0 else "BAD"), "殘留", t, n); n and mm.append("殘留 " + t)
print("MISMATCHES:", len(mm), mm if mm else "")
