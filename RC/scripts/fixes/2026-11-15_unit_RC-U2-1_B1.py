#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""study/data/unit-RC-U2-1.json：依 RC-U2-1／U2-2 批 1 勘誤（現行規範 Vc 式）同步公式卡與題目摘要（2026-11-15，階段 F）
F1–F4：舊規範詳細式／140Ag／35Ag／Mm 改為現行式（考卷印過的仍是舊式，meta 保留紀錄並加警示）
F16：瓶形無分布筋 βs 0.40（舊版 0.60λ）；Q RC-2014-3、RC-2010-3 摘要改寫
用法：python RC/scripts/fixes/2026-11-15_unit_RC-U2-1_B1.py"""
import json
from pathlib import Path
p = Path(__file__).resolve().parents[2] / "study" / "data" / "unit-RC-U2-1.json"
d = json.loads(p.read_text(encoding="utf-8"))
F = d["F"]
assert F[1]["sh"] == "Vc 詳細式" and F[2]["sh"] == "Vc 軸壓" and F[3]["sh"] == "Vc 軸拉" and F[4]["sh"] == "Mm"
W = "⚠️ 現行規範（2023）"
F[1]["nm"] = "Vc 第二式（含 ρw；現行 2.1ρw^(1/3)）"
F[1]["sh"] = "Vc 第二式"
F[1]["eq"] = r"$$V_c=\max\left\{\left[0.53\sqrt{f'_c}+\frac{N_u}{6A_g}\right]b_wd,\ \left[2.1\rho_w^{1/3}\sqrt{f'_c}+\frac{N_u}{6A_g}\right]b_wd\right\}\le1.33\sqrt{f'_c}\,b_wd$$"
F[1]["meta"] = W + r"已刪除舊詳細式 \((0.50\sqrt{f'_c}+175\rho_wV_ud/M_u)\le0.93\sqrt{f'_c}b_wd\)，改為此式與簡化式取大，作答依現行式。考卷紀錄：" + F[1]["meta"]
F[2]["nm"] = "軸力項 Nu/6Ag（軸壓）"
F[2]["eq"] = r"$$V_c = \left[0.53\sqrt{f'_c}+\frac{N_u}{6A_g}\right]b_wd,\qquad \frac{N_u}{6A_g}\le0.05f'_c\quad(N_u\text{ 壓為正})$$"
F[2]["meta"] = W + r"以 \(N_u/6A_g\) 取代舊式 \(1+N_u/140A_g\)。考卷紀錄（印的是舊式）：" + F[2]["meta"]
F[3]["nm"] = "軸力項 Nu/6Ag（軸拉）"
F[3]["eq"] = r"$$V_c = \left[0.53\sqrt{f'_c}+\frac{N_u}{6A_g}\right]b_wd \ge 0\qquad(N_u \text{ 取負})$$"
F[3]["meta"] = W + r"壓、拉用同一個 \(N_u/6A_g\) 項，取代舊式 \(1+N_u/35A_g\)；仍要記得拉力代負號、\(V_c\) 不得小於零。考卷紀錄：" + F[3]["meta"]
F[4]["nm"] = "等效彎矩 Mm（舊規範，現行已刪除）"
F[4]["meta"] = W + "已刪除 \\(M_m\\) 法；考卷若印出，數據照用、公式改用現行式（RC-2014-3）。考卷紀錄：" + F[4]["meta"]
assert "0.60\\lambda" in F[16]["eq"]
F[16]["eq"] = F[16]["eq"].replace(r"0.60\lambda\ (\text{瓶形無腹筋})", r"0.40\ (\text{瓶形無分布筋；舊版 }0.60\lambda)")
assert "0.40" in F[16]["eq"]
for q in d["Q"]:
    if q["id"] == "RC-2014-3":
        q["sum"] = "三種軸力條件下求臨界斷面 Vc：現行表列兩式＋Nu/6Ag（考卷印 401-100 詳細式／Mm 法，為舊規範）"
    if q["id"] == "RC-2010-3":
        q["sum"] = "軸力對剪力開裂與裂縫形態的影響（軸壓裂縫較平緩），並以現行簡化式＋Nu/6Ag 求 φVc"
d["date"] = "2026-11-15"
p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("OK", p)
