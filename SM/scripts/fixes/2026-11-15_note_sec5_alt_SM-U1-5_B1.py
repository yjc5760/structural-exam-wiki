# -*- coding: utf-8 -*-
"""SM-U1-5 批 1 階段 B'：題目資訊不足的兩題，在 §5 補替代解讀（非勘誤，答案不變）。可重複執行。在 SM/ 下執行。
數值：σ'v0 與 S_u = σ'v0·sinφ'/[1+(2A_f−1)sinφ']，2003-4：92.28 kPa、φ'=30°；2010-1：111.90 kPa、φ'=28°。"""
import math
def su(sv, A, phi):
    s = math.sin(math.radians(phi)); return sv*s/(1+(2*A-1)*s)
sv3 = (17.5-9.81)*12; sv10 = 17.5*12-9.81*10
V = dict(a=su(sv3,1,30), b=su(sv3,.5,30), c=su(sv3,0,30), d=.22*sv3, e=su(sv10,1,28), f=su(sv10,.5,28), g=.22*sv10)
assert ("%.2f %.2f %.2f %.1f %.2f %.2f %.1f" % tuple(V[k] for k in "abcdefg")) == "30.76 46.14 92.28 20.3 35.75 52.53 24.6"
N = {
 "SM-2003-4": ("\n*修正日期：2026-11-15（§1 改為指向題目正本",
  "3. **$A_f$ 未給的替代解讀（⚠ 待使用者複核）**：考卷只寫「未受解壓影響」、沒有給 $A_f$。本解依題目正本 #1 定案取完美取樣 $A_s = A_f = 1$，"
  "$S_u = \\sigma'_{v0}\\sin\\phi'/[1+(2A_f-1)\\sin\\phi']$ 對 $A_f$ 很敏感：$A_f = 1$ → 30.76 kPa（主答）；$A_f = 0.5$ → 46.14 kPa；"
  "$A_f = 0$（不產生超額孔隙水壓，$\\sigma'_{3f} = \\sigma'_{v0}$）→ 92.28 kPa；經驗式 Mesri $S_u \\approx 0.22\\sigma'_{v0}$ → 20.3 kPa。"
  "考場作答宜寫明 $A_f = 1$ 的假設。（2026-11-15 盲解比對補註）\n"),
 "SM-2010-1": ("\n---\n\n*解析日期：",
  "4. **題目資訊不足處的替代解讀（⚠ 待使用者複核）**：① 考卷**沒寫**正常壓密，本解依題目正本 #1 假設 NC、$c'$ = 0；"
  "② 未給 $A_f$，主答取完美取樣 $A_s = A_f = 1$（35.75 kPa），若取 $A_f = 0.5$ 則 $S_u$ = 52.53 kPa，Mesri $0.22\\sigma'_{v0}$ 為 24.6 kPa；"
  "③ ㈡ 若讀成試體內絕對孔隙水壓，施加圍壓後為 $-111.9 + 50 = -61.9$ kPa（見 Step 3 表）。（2026-11-15 盲解比對補註）\n"),
}
for q, (anchor, block) in N.items():
    p = "raw/solutions/%s/%s.md" % (q, q)
    t = open(p, encoding="utf-8").read()
    if "（2026-11-15 盲解比對補註）" in t:
        print("skip", q); continue
    assert t.count(anchor) == 1, (q, anchor)
    t = t.replace(anchor, block + anchor)
    lines = t.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith("*修正日期：2026-11-15（§1 改為指向題目正本")]
    assert len(k) == 1, q
    lines[k[0]] = lines[k[0]].replace("；非勘誤）*", "；§5 補題目資訊不足的替代解讀；非勘誤）*")
    data = "\n".join(lines).encode("utf-8")
    with open(p, "r+b") as fh:   # 掛載磁碟不允許 O_TRUNC，改用覆寫（新內容較長）
        fh.seek(0); fh.write(data)
        try: fh.truncate()
        except OSError: pass
    print("done", q)
