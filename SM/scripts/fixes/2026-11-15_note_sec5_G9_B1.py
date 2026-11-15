# -*- coding: utf-8 -*-
"""G9（SM-U2-1 批 1）盲解比對後補註：SM-2009-2、SM-2020-4 §5 補方法敏感度（答案不變；非勘誤）。
可重複執行（已補者跳過）。在 SM/ 下執行。數值來源：盲解紀錄-SM-U2-1-B1-2026-11-15.md 與比對時 Python 重算。"""
NOTE = {
 "SM-2009-2": "\n3. **承載力與隆起公式的敏感度（2026-11-15 盲解比對補註）**：考卷沒有指定公式，答案隨方法變動，作答時寫明所採公式即可。㈠ $D_f$：Terzaghi（$N_c$ = 5.7、形狀 $1+0.3B/L$，本解）6.34 m；Skempton 6.51 m；Meyerhof／Hansen 型（$N_c$ = 5.14、$s_c=1+0.195B/L$、$d_c=1+0.4D_f/B$）5.87 m。㈡ 抗隆起 FS：本解 Terzaghi 形式 2.58、Bjerrum–Eide 2.13；獨立盲解取 $D_f$ = 5.87 m 時 Bjerrum–Eide 2.28、Terzaghi 標準式 $FS=\\frac{5.7c_u}{H(\\gamma-c_u/0.7B)}$ 3.16。各法 FS 2.1～3.2，皆高於一般要求 1.5～2.0，結論相同；上舉 FS 對 $D_f$ 敏感（$D_f$ = 5.87 m 時 1.18、6.34 m 時 1.09、6.51 m 時 1.06），都低於 1.2，降壓建議不變。\n",
 "SM-2020-4": "\n4. **結論對承載力公式敏感（2026-11-15 盲解比對補註）**：FS 落在 3 附近，換公式可能翻轉結論。以淨施加壓力 98.6 kPa 計：Terzaghi $N_c$ = 5.7（本解）2.89；Meyerhof $d_c=1+0.2D_f/B$ = 1.08 → 2.82；Skempton $N_c=5(1+0.2D_f/B)$ = 5.4 → 2.74；$N_c$ = 5.14 不計深度因數 → 2.61；Hansen／Vesic 型 $d_c=1+0.4D_f/B$ = 1.16 → $q_{ult,net}$ = 298.1 kPa、**FS = 3.02**（獨立盲解主線，剛好滿足）。五法中四法 < 3，本解維持「不安全」；若採 Hansen 深度因數，應寫成「FS ≈ 3.0，臨界、無餘裕」。另若 120 kN/m 已含基礎重，Terzaghi FS = 285/96 = 2.97，Hansen 型 3.11。作答時寫明所採公式、FS 要求與自重假設。\n",
}
DESC = {"SM-2009-2": "§5 補註承載力與隆起公式敏感度", "SM-2020-4": "§5 補註承載力公式敏感度（FS 在 3 附近）"}
TAG = "盲解比對後補充"
for q in DESC:
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if TAG in t:
        print("skip", q); continue
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    j = k[0]
    while lines[j - 1].strip() == "": j -= 1
    lines[j:j] = NOTE[q].rstrip("\n").split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；%s（%s，答案未變）；非勘誤）*" % (DESC[q], TAG))
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("done", q)
