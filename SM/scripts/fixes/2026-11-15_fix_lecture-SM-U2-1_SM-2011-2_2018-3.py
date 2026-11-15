# -*- coding: utf-8 -*-
"""同步 FIX SM-2011-2、SM-2018-3 到 study/lecture-SM-U2-1.html（§5.2、§5.3、速查表、FAQ 11、練習 ⑥）。
在 SM/ 下執行；可重複執行。"""
p = "study/lecture-SM-U2-1.html"
t = open(p, encoding="utf-8").read()
if "2026-11-15 勘誤同步" in t:
    raise SystemExit("already patched")
R = [
# §5.2 trap
("""<b>兩個投影，方向相反，很容易只做一半。</b><br>
① <b>流徑長度</b>：沿流線量，不是垂直高差 → \\(L=\\Delta Z/\\sin\\theta\\)（<b>除以</b> \\(\\sin\\theta\\)，變<b>長</b>）。<br>
② <b>截面積</b>：達西定律的 \\(A\\) 必須<b>垂直於流向</b> → \\(A_\\perp=A_{\\text{水平}}\\sin\\theta\\)（<b>乘以</b> \\(\\sin\\theta\\)，變<b>小</b>）。<br>
<a class="qlink" href="problems-view/SM-2011-2.html" target="_blank">SM-2011-2</a>（\\(\\theta=53^\\circ\\)，\\(\\sin\\theta=0.8\\)）：
\\(L=5/0.8=6.25\\) m、\\(A_\\perp=4\\times0.8=3.2\\) m²。
只做流徑不做面積，流量會多算 25%。""",
"""<b>流徑要投影，截面積要先看「給的是哪個面」。</b><br>
① <b>流徑長度</b>：沿流線量，不是垂直高差 → \\(L=\\Delta Z/\\sin\\theta\\)（<b>除以</b> \\(\\sin\\theta\\)，變<b>長</b>）。<br>
② <b>截面積</b>：達西定律的 \\(A\\) 必須<b>垂直於流向</b>。題目給的若是水平面積才要投影 \\(A_\\perp=A_{\\text{水平}}\\sin\\theta\\)；給的面若本來就垂直於流向，直接用。<br>
<a class="qlink" href="problems-view/SM-2011-2.html" target="_blank">SM-2011-2</a>（\\(\\theta=53^\\circ\\)，\\(\\sin\\theta=0.8\\)）：開挖底面在 d（B 層頂），圍堰內積水到地表，
B 層頂、底面垂直於圍堰壁 → \\(L_{bd}=3/0.8=3.75\\) m、\\(A=2\\times2=4\\) m²（不再乘 \\(\\sin\\theta\\)），\\(h_b=8\\)、\\(h_d=6\\) m，\\(i_{bd}=0.533\\)、\\(Q=9.22\\) m³/day。
把 2 m × 2 m 當水平面積再乘 0.8，或把開挖底面讀成 e 的高程，都會算錯（2026-11-15 勘誤前的解析即如此，得 6.64 m³/day）。"""),
("""<b>驗算法：換一條路走。</b>SM-2011-2 也可以用「垂直方向的流速分量 × 水平面積」計算：
\\(v_z=(ki)\\sin\\theta=1.92\\times10^{-5}\\) m/s，\\(Q=v_z\\times4=7.68\\times10^{-5}\\) m³/s ——
與 \\(kiA_\\perp\\) 完全一致。<b>兩條路殊途同歸，就代表兩個投影都做對了。</b>""",
"""<b>驗算法：換一條路走。</b>SM-2011-2 也可以用流網公式：B 層內是一維平行流，取 1 m 方格，\\(N_f=2\\)、\\(N_d=3.75\\)，
\\(Q=k\\,\\Delta h\\,\\frac{N_f}{N_d}\\times\\) 寬 \\(=5\\times10^{-5}\\times2\\times\\frac{2}{3.75}\\times2=1.067\\times10^{-4}\\) m³/s ——
與 \\(kiA\\) 完全一致。<b>兩條路殊途同歸，就代表流徑與斷面都取對了。</b>"""),
# §5.3 svg
("""  <line x1="30" y1="150" x2="320" y2="150" stroke="#455a64" stroke-width="1.8"/>
  <text x="40" y="145" font-size="11" fill="#607d8b">上游海床</text>""",
"""  <line x1="30" y1="150" x2="320" y2="150" stroke="#455a64" stroke-width="1.8"/>
  <text x="40" y="145" font-size="11" fill="#607d8b">上游地表</text>"""),
("""  <line x1="620" y1="180" x2="850" y2="180" stroke="#455a64" stroke-width="1.8"/>
  <text x="760" y="174" font-size="11.5" fill="#1565c0">下游水面＝海床</text>""",
"""  <line x1="620" y1="150" x2="850" y2="150" stroke="#455a64" stroke-width="1.8"/>
  <text x="740" y="144" font-size="11.5" fill="#1565c0">下游水面＝地表</text>"""),
("""  <path d="M200 152 Q 300 200 357 262 Q 430 300 700 182" fill="none" stroke="#00838f" stroke-width="1.8"/>
  <path d="M170 152 Q 280 220 357 276 Q 440 316 700 182" fill="none" stroke="#00838f" stroke-width="1.5" opacity=".75"/>
  <path d="M140 152 Q 260 240 357 288 Q 450 324 700 182" fill="none" stroke="#00838f" stroke-width="1.5" opacity=".55"/>""",
"""  <path d="M200 152 Q 300 200 357 266 Q 430 300 700 152" fill="none" stroke="#00838f" stroke-width="1.8"/>
  <path d="M150 152 Q 270 236 357 286 Q 450 324 760 152" fill="none" stroke="#00838f" stroke-width="1.5" opacity=".7"/>"""),
("""  <text x="40" y="374" font-size="12" font-weight="bold" fill="#00838f">Nf = 4 個流槽（青線之間的「道」）</text>""",
"""  <text x="40" y="374" font-size="12" font-weight="bold" fill="#00838f">Nf = 3 個流槽（含壩底＋牆面、不透水層兩條邊界流線）</text>"""),
("""  <text x="452" y="358" font-size="12.5" font-weight="bold" fill="#e65100">總水頭差不是圖上最大的那個數字</text>
  <text x="452" y="380" font-size="12" fill="#37474f">ΔH = 6.3（上游水深）+ 1.6（壩底埋深）= 7.9 m</text>
  <text x="452" y="400" font-size="12" fill="#607d8b">因為下游水面比上游海床還低 1.6 m</text>""",
"""  <text x="452" y="358" font-size="12.5" font-weight="bold" fill="#e65100">ΔH 看水面差，埋深算進壓力水頭</text>
  <text x="452" y="380" font-size="12" fill="#37474f">上下游地表同高 → ΔH = 6.3 m（上游水深）</text>
  <text x="452" y="400" font-size="12" fill="#607d8b">1.6 m 是壩底埋深：u = (h + 1.6)γw</text>"""),
# hand calc
("""<b>手算：SM-2018-3</b>（\\(k=3.5\\times10^{-6}\\) m/s，\\(N_f=4\\)，\\(N_d=10\\)）
$$\\Delta H=6.3+1.6=7.9\\ \\text{m},\\qquad \\Delta h=\\frac{7.9}{10}=0.79\\ \\text{m}$$
$$q=kH\\frac{N_f}{N_d}=3.5\\times10^{-6}\\times7.9\\times\\frac{4}{10}=\\boxed{1.106\\times10^{-5}\\ \\text{m}^3/\\text{s/m}}$$
以壩底為基準面（各點 \\(z=0\\)，故 \\(u_i=h_i\\gamma_w\\)），從上游算起累積降數：""",
"""<b>手算：SM-2018-3</b>（\\(k=3.5\\times10^{-6}\\) m/s，\\(N_f=3\\)，\\(N_d=10\\)；2026-11-15 勘誤同步）
$$\\Delta H=6.3\\ \\text{m},\\qquad \\Delta h=\\frac{6.3}{10}=0.63\\ \\text{m}$$
$$q=kH\\frac{N_f}{N_d}=3.5\\times10^{-6}\\times6.3\\times\\frac{3}{10}=\\boxed{6.62\\times10^{-6}\\ \\text{m}^3/\\text{s/m}}$$
以下游水面為基準面，壩底各點 \\(z=-1.6\\) m，故 \\(u_i=(h_i+1.6)\\gamma_w\\)；從上游算起累積降數（a 在牆與壩底交角，介於第 4、5 條等勢線之間）："""),
("""<thead><tr><th>點</th><th>累積降數 \\(n\\)</th><th>\\(h=7.9-0.79n\\) (m)</th><th>\\(u=h\\gamma_w\\) (kPa)</th></tr></thead>
<tbody>
<tr><td>a</td><td>6</td><td>3.16</td><td>31.00</td></tr>
<tr><td>b</td><td>7</td><td>2.37</td><td>23.25</td></tr>
<tr><td>c</td><td>8</td><td>1.58</td><td>15.50</td></tr>
<tr><td>d</td><td>9</td><td>0.79</td><td>7.75</td></tr>
<tr><td>e</td><td>10</td><td>0</td><td>0</td></tr>
</tbody>
</table>
<b>自我檢查</b>：① e 點是下游出口，總水頭必須為 0、上揚壓力必須為 0 ✓；
② 相鄰兩點差恰好 \\(0.79\\times9.81=7.75\\) kPa，等差 ✓。<b>只要末點歸零、間距等差，這一整組數字就不會錯。</b>""",
"""<thead><tr><th>點</th><th>累積降數 \\(n\\)</th><th>\\(h=6.3-0.63n\\) (m)</th><th>\\(u=(h+1.6)\\gamma_w\\) (kPa)</th></tr></thead>
<tbody>
<tr><td>a</td><td>≈4.5</td><td>3.465</td><td>49.7</td></tr>
<tr><td>b</td><td>5</td><td>3.15</td><td>46.6</td></tr>
<tr><td>c</td><td>6</td><td>2.52</td><td>40.4</td></tr>
<tr><td>d</td><td>7</td><td>1.89</td><td>34.2</td></tr>
<tr><td>e</td><td>8</td><td>1.26</td><td>28.1</td></tr>
</tbody>
</table>
<b>自我檢查</b>：① e 點不是出口（之後還有 2 降），而且壩底埋在下游水面下 1.6 m，上揚壓力不會是 0 ✓；
② 相鄰兩點差恰好 \\(0.63\\times9.81=6.18\\) kPa，等差 ✓。<b>壩底在水面下時，每一點都另有 \\(1.6\\gamma_w=15.7\\) kPa 的靜水部分。</b>"""),
("""<b>陷阱：總水頭差要從圖面幾何推，不能照抄標註。</b>
SM-2018-3 圖上印了 6.3、1.6、9.4、17.2 四個數字。
驗證方法：截水牆長 \\(9.4-1.6=7.8\\) m、牆底至不透水層 \\(17.2-9.4=7.8\\) m —— <b>兩者相等，證明所有尺寸都自上游海床起算</b>。
因此 \\(\\Delta H=6.3+1.6=7.9\\) m，而非 6.3 m。<b>看到一組尺寸，先找「能互相驗證」的那兩個。</b>""",
"""<b>陷阱：先看清每條尺寸線量的是什麼。</b>
SM-2018-3 圖上印了 6.3、1.6、9.4、17.2 四個數字，都由地表量起：6.3 m 是上游水深，1.6 m 是壩底埋深，9.4 m、17.2 m 是截水牆底與不透水層深度。
左右地表是同一條水平線、下游水位在地表，所以 \\(\\Delta H=6.3\\) m；1.6 m 不進 \\(\\Delta H\\)，而是進壓力水頭。
（2026-11-15 勘誤前的解析把下游地表讀成與壩底同高，取 \\(\\Delta H=7.9\\) m、\\(N_f=4\\)，e 點上揚壓力算成 0。）"""),
# summary svg
("""  <text x="332" y="210" font-size="13" font-weight="bold" fill="#2e7d32">斜向：兩個投影</text>
  <text x="332" y="232" font-size="12" fill="#37474f">流徑 L = ΔZ / sinθ（變長）</text>
  <text x="332" y="252" font-size="12" fill="#37474f">面積 A⊥ = A水平 · sinθ（變小）</text>
  <text x="332" y="274" font-size="11.5" fill="#c62828">只做一個 → 流量錯 25%</text>
  <text x="332" y="294" font-size="11.5" fill="#607d8b">驗算：改用 vz × A水平，須相同</text>""",
"""  <text x="332" y="210" font-size="13" font-weight="bold" fill="#2e7d32">斜向：流徑投影、斷面看清</text>
  <text x="332" y="232" font-size="12" fill="#37474f">流徑 L = ΔZ / sinθ（變長）</text>
  <text x="332" y="252" font-size="12" fill="#37474f">A 要垂直流向；給水平面積才乘 sinθ</text>
  <text x="332" y="274" font-size="11.5" fill="#c62828">開挖面邊界水頭＝積水面高程</text>
  <text x="332" y="294" font-size="11.5" fill="#607d8b">驗算：流網 Nf/Nd 公式須相同</text>"""),
("""  <text x="632" y="294" font-size="11.5" fill="#c62828">ΔH 要由圖面幾何推，勿照抄</text>""",
"""  <text x="632" y="294" font-size="11.5" fill="#c62828">ΔH 看水面差；埋深進壓力水頭</text>"""),
# tables
("""<td>斜向滲流、水頭三兄弟、流徑與截面積兩個投影</td>""",
 """<td>斜向滲流、水頭三兄弟、開挖面邊界水頭、流徑投影與垂直斷面</td>"""),
("""<td>流網 \\(N_f/N_d\\)、上揚壓力、由圖面幾何推總水頭差</td>""",
 """<td>流網 \\(N_f/N_d\\)、上揚壓力、尺寸線判讀（埋深進壓力水頭）</td>"""),
("""<tr><td>20</td><td>同上，算流量</td><td>截面積用水平投影面積</td><td>\\(A_\\perp=A_{\\text{水平}}\\sin\\theta\\)（變小）。兩個投影都要做，只做一個會錯 25%</td></tr>""",
 """<tr><td>20</td><td>同上，算流量</td><td>截面積沒看清是哪個面</td><td>\\(A\\) 要垂直於流向：給水平面積才乘 \\(\\sin\\theta\\)；SM-2011-2 的 2 m × 2 m 本身就垂直於流向，直接用</td></tr>"""),
("""<td>要找能互相驗證的尺寸推基準。SM-2018-3 是 \\(6.3+1.6=7.9\\) m 不是 6.3 m</td>""",
 """<td>先看每條尺寸線量的是什麼。SM-2018-3 上下游地表同高，\\(\\Delta H=6.3\\) m；1.6 m 是壩底埋深，進壓力水頭</td>"""),
("""<details><summary>11　斜向滲流的兩個投影，為什麼一個乘 \\(\\sin\\theta\\) 一個除 \\(\\sin\\theta\\)？</summary>
<p>流徑是沿流線量的<b>斜邊</b>，比垂直高差長，所以 \\(L=\\Delta Z/\\sin\\theta\\)；截面積必須<b>垂直於流速向量</b>，水平面積投影過去會變小，所以 \\(A_\\perp=A_{\\text{水平}}\\sin\\theta\\)。驗算：改用「垂直流速分量 × 水平面積」應得到相同流量。（§5.2）</p></details>""",
 """<details><summary>11　斜向滲流的兩個投影，為什麼一個乘 \\(\\sin\\theta\\) 一個除 \\(\\sin\\theta\\)？</summary>
<p>流徑是沿流線量的<b>斜邊</b>，比垂直高差長，所以 \\(L=\\Delta Z/\\sin\\theta\\)；截面積必須<b>垂直於流速向量</b>，若題目給的是水平面積，投影過去會變小，所以 \\(A_\\perp=A_{\\text{水平}}\\sin\\theta\\)。但先確認給的是哪個面：SM-2011-2 的開挖底面（B 層頂）垂直於圍堰壁，本身就是垂直斷面，不必再乘。（§5.2；2026-11-15 勘誤同步）</p></details>"""),
("""更重要的是<b>總水頭差要自己從圖面幾何推出來</b>（用「截水牆長 7.8 m ＝ 牆底至不透水層 7.8 m」的對稱性驗證基準面），""",
 """更重要的是<b>每條尺寸線量的是什麼要自己看清</b>（四個尺寸都由地表量起；上下游地表同高，1.6 m 是壩底埋深），"""),
("""② 為什麼 \\(\\Delta H=7.9\\) 而不是 6.3？③ e 點的上揚壓力為什麼一定是 0？""",
 """② 為什麼 \\(\\Delta H=6.3\\) 而不是 7.9？③ e 點的上揚壓力為什麼不是 0？"""),
("""<tr><td>斜向滲流的兩個投影</td><td style="color:#e65100"><b>△</b></td>""",
 """<tr><td>斜向滲流：流徑投影與垂直斷面</td><td style="color:#e65100"><b>△</b></td>"""),
("""— 斜向滲流的兩個投影，補齊上表第 10 列。</li>""",
 """— 斜向滲流的流徑投影與開挖面邊界水頭，補齊上表第 10 列。</li>"""),
]
for a, b in R:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
with open(p, "r+b") as f:
    f.seek(0); f.write(t.encode("utf-8")); f.truncate()
print("patched")
