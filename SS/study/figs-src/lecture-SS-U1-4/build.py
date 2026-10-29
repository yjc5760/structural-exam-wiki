import re, sys
sys.path.insert(0,'/home/claude/work')
from figs_a import *; from figs_b import *; from figs_c import *; from figs_d import *

src=open('/home/claude/work/orig.html',encoding='utf-8').read()

caps={
1:('圖 1-1',f11,'圖 1-1　螺栓搭接的六個關卡（上：平面；下：立面）。⓪ 是唯一的延性項；① 淨斷面要在 A、B 各自「力量還沒交出去的那一排孔」驗（圖示 B 板）；② 破壞塊兩側是被<b>剪</b>的面、後方是被<b>拉</b>的面；③④⑤ 只有在立面才看得到。注意承壓貼住的孔壁永遠是朝<b>板端</b>那一側 —— 這就是 §4.3 撕裂公式要用淨邊距 \\(L_c\\) 的原因。'),
2:('圖 2-1',f21,None),
3:('圖 3-1',f31,'圖 3-1　剪力遲滯，以範例 A 的 L125×125×12 實尺寸繪製。(a) \\(\\bar x\\) 是形心到<b>連接面</b>（肢背貼接合板的那一面）的距離 35.3 mm，不是到螺栓線；(b) 斷裂發生在連接肢先到 \\(F_u\\) 的瞬間，此時全斷面平均應力只有 \\(U F_u\\) —— 所以 \\(U\\) 就是「實際分佈面積」佔「均勻 \\(F_u\\) 面積」的比例。'),
4:('圖 3-2',f32,'圖 3-2　\\(U = 1-\\bar x/L\\) 的精確曲線（標記點均落在曲線上）。曲線很快就趨近 1，代表<b>把接合做長一點是消除剪力遲滯最便宜的手段</b>；反過來說，短接合（\\(L/\\bar{x} < 3\\)）的懲罰非常重。橘色虛線是角鋼的查表值：範例 A 算得 0.832，高於查表 0.80 —— 查表值是保守下限。'),
5:('圖 3-3',f33,'圖 3-3　(a) 範例 A 的破壞塊，依實際尺寸繪製：<b>一條</b>剪力面（綠，沿螺栓中心線從端部量到最內側螺栓，25 cm）＋<b>一條</b>拉力面（紅，從螺栓線量到肢趾，8.0 cm）。(b) 雙排螺栓則是<b>兩條</b>剪力面＋<b>一條</b>拉力面（兩排之間）。兩種情況剪力面都<b>穿過孔中心</b>，所以 \\(A_{nv}\\) 要扣孔、\\(A_{gv}\\) 不扣。'),
6:('圖 4-1',f41,'圖 4-1　同一顆螺栓的兩個世界與它們的載重—位移關係。上排：摩阻型靠<b>夾緊力產生的摩擦</b>，桿與孔壁之間仍有間隙；承壓型的板已錯開一個孔隙，孔壁貼住後<b>螺栓桿才受剪</b>。下排：摩阻型的極限是「滑動門檻」，滑過之後並沒有崩塌，而是進入承壓型的世界 —— 這正是 §4.2 \\(\\phi\\) 可以取 1.0 的理由。兩條水平線取自範例 B。'),
8:('圖 6-1',f61,'圖 6-1　範例 D，依實際尺寸（1 cm = 8 px）與同一向量比例尺繪製。左上角離形心較遠（21.38 &gt; 18.36），但它的扭矩分力幾乎水平，垂直分量 +0.0182P 與直接剪力 −0.0200P 相互抵消；右下角的扭矩分力斜向下，與直接剪力同向疊加。<b>臨界點取決於「方向是否同向」，不是「距離是否最遠」。</b>'),
9:('圖 7-1',f71,'圖 7-1　梁端彎矩的兩條路。接頭面應力：翼板近乎均勻 → 合成一對力偶 \\(T = C = M_f/d\\)；腹板為三角形 → 彎矩 \\(M_w\\)，再加上全部剪力 \\(V\\)。右側是範例 E 腹板銲道最上端的應力向量（同一比例尺）：合力 1.137 落在容許應力圓弧 1.476 之內。翼板銲實際是 CJP 還是填角銲，要先看圖上的銲接符號（見上方 SS-2018-3 警語）。'),
10:('圖 7-2',f72,'圖 7-2　側移（地震）下的節點域。兩根梁的彎矩<b>同向</b>，所以上翼板的兩個力都向右、下翼板都向左，在柱腹板上疊加成剪力，把節點域剪成平行四邊形（紅虛線）。\\(V_{pz}\\) 要<b>扣掉</b>柱剪力 \\(V_c\\)（方向與翼板力相反）—— 忘記扣就過度保守。連續板（綠）的作用不是抗剪，是把梁翼板的<b>集中力</b>接續到柱的另一側，避免柱翼板局部彎曲、柱腹板局部降伏。'),
11:('圖 7-3',f73,'圖 7-3　兩條路的目標完全相同：<b>讓塑性鉸離開銲道</b>。補強式把接頭加強到「塑鉸只能長在補強端之外」；RBS 在指定位置把<b>翼板寬度</b>削成圓弧（只有平面圖看得到），讓塑鉸「只能」長在削弱段中央。右圖平面與立面同比例。出自 <a class="qlink" href="problems-view/SS-2020-1.html" target="_blank">SS-2020-1</a>。'),
12:('圖 9-1',f91,'圖 9-1　三種常見開槽型式，以板厚 25 mm 依同一比例繪製。<b>選型的兩個依據：板厚（決定要不要開、開多大）與可及性（能不能翻面／兩面施銲）。</b>T 型接頭（梁翼板對柱翼板）只能從一側開槽 → Single Bevel，常加背墊板 —— 耐震接頭須移除背墊板並背剷回銲（§7.4）；對接厚板且可翻面 → Double V，本圖尺寸下銲道面積約為單 V 的 42%。'),
13:('圖 10-1',f101,None),
}

figs=list(re.finditer(r'<div class="fig">\s*(<svg.*?</svg>)\s*(<div class="cap">.*?</div>)',src,re.S))
assert len(figs)==14, len(figs)
out=[]; last=0
for i,m in enumerate(figs):
    out.append(src[last:m.start(1)])
    if i in caps:
        _,fn,cap=caps[i]
        out.append(fn()); out.append('\n')
        out.append(f'<div class="cap">{cap}</div>' if cap else m.group(2))
    else:
        out.append(m.group(1)); out.append('\n'); out.append(m.group(2))
    last=m.end(2)
out.append(src[last:])
s=''.join(out)

def ins_after(s, anchor, block):
    assert s.count(anchor)==1, anchor
    return s.replace(anchor, anchor+block)
def ins_before(s, anchor, block):
    assert s.count(anchor)==1, anchor
    return s.replace(anchor, block+anchor)

fig42=('\n\n<div class="fig">\n'+f42()+'\n<div class="cap">圖 4-2　承壓強度的兩段式。(a) \\(L_c\\) 是孔<b>邊緣</b>到板端（或到下一個孔邊）的淨距離，不是孔中心距；'
       '(b) \\(L_c < 2d\\) 時由撕裂控制（斜線段 \\(1.2F_uL_ct\\)），\\(L_c \\geq 2d\\) 後由孔變形封頂在 \\(2.4F_udt\\) —— 兩段的交點就是「2.4 = 1.2 × 2」的由來。</div>\n</div>')
s=ins_after(s,'反過來，題目若給的邊距很小（\\(L_c < 2d\\)），就必須用 \\(1.2F_u L_c t\\)，不能直接套 2.4。\n</div>',fig42)

ver=('\n\n<div class="trap">\n<b>版本提醒（2026-10 補註）：</b>上表的 \\(\\phi = 1.0/0.85\\)＋\\(h_{sc}\\) 是 <b>AISC 360-05</b> 的寫法，也是考題最常沿用的版本。'
     'AISC 360-10 起改為：A 級接觸面 \\(\\mu = 0.30\\)、\\(\\phi\\) 依孔型取 1.00（標準孔）／0.85（過大孔、短槽孔）／0.70（長槽孔），\\(h_f\\) 改為<b>填板係數</b>。'
     '台灣容許應力設計法則以表列容許剪應力處理摩阻型（A325 標準孔 1.19 tf/cm²、A490 標準孔 1.47 tf/cm²），並要求滑動係數 ≥ 0.33。'
     '<b>考試照題目指定的規範與係數走</b>；題目沒指定時，寫明採用哪一版即可（詳見 <a class="qlink" href="problems-view/SS-2017-2.html" target="_blank">SS-2017-2</a> 勘誤後的 §6）。\n</div>')
s=ins_before(s,'\n\n<h3>4.3 承壓型',ver)

fig52=('\n<div class="fig">\n'+f52()+'\n<div class="cap">圖 5-2　填角銲方向性強度倍數 \\(1+0.5\\sin^{1.5}\\theta\\)。θ = 90°（橫向銲）多 50%，45° 約多 30%；'
       '規範預設一律取紅線 1.0，等於主動放棄曲線與紅線之間的那塊強度，換取「整條銲道一個數字」的簡單。</div>\n</div>\n')
s=ins_before(s,'\n<h3>5.3 填角銲 vs 開槽銲',fig52)

fig81=('<div class="fig">\n'+f81()+'\n<div class="cap">圖 8-1　範例 F 的斷面與斷續銲配置。(a) \\(Q\\) 只取蓋板本身的 \\(A\\bar y\\)；'
       '(b) 依比例畫出 6 cm 銲段、間距 28 cm。強度只要求 \\(s \\le 90\\) cm，構造規定把它壓到 28.8 cm —— 兩條橫條的長度差，就是「構造控制」的意思。</div>\n</div>\n\n')
s=ins_before(s,'<div class="trap">\n<b>陷阱：\\(Q\\) 用錯部位。',fig81)

# weld size table: AISC vs Taiwan
old_tab='''<tr><th>板厚 \\(t\\)</th><th>\\(w_{min}\\)</th></tr>
<tr><td>\\(t \\leq 6\\) mm</td><td>3 mm</td></tr>
<tr><td>\\(6 < t \\leq 13\\)</td><td>5 mm</td></tr>
<tr><td>\\(13 < t \\leq 19\\)</td><td>6 mm</td></tr>
<tr><td>\\(t > 19\\)</td><td>8 mm</td></tr>
</table>'''
new_tab='''<tr><th>\\(w_{min}\\)</th><th>AISC 360 表 J2.4</th><th>台灣規範表 10.2-4</th></tr>
<tr><td>3 mm</td><td>\\(t \\leq 6\\)</td><td>\\(t \\leq 6\\)</td></tr>
<tr><td>5 mm</td><td>\\(6 < t \\leq 13\\)</td><td>\\(6 < t \\leq 12\\)</td></tr>
<tr><td>6 mm</td><td>\\(13 < t \\leq 19\\)</td><td>\\(12 < t \\leq 19\\)</td></tr>
<tr><td>8 mm</td><td>\\(t > 19\\)</td><td>\\(19 < t \\leq 38\\)</td></tr>
</table>
<span style="font-size:.86em;color:#607d8b">兩者只差在 12～13 mm 的分界。台灣級距以 113 年考卷所附表格（轉圖目視確認）為準；作答以題目附表優先。</span><br>'''
assert s.count(old_tab)==1
s=s.replace(old_tab,new_tab)

# header + footer notes
s=s.replace('觀念圖解 ＋ 六個完整手算範例。</p>','觀念圖解 ＋ 六個完整手算範例。圖解以程式依實際尺寸與範例數值繪製（2026-10 改版）。</p>')
s=s.replace('<code>wiki/failure-modes/connection-failure.md</code>\n</footer>','<code>wiki/failure-modes/connection-failure.md</code><br>\n  2026-10-23 圖解改版：12 張圖重繪並新增圖 4-2、5-2、8-1，全部依座標與範例數值計算繪製（圖 0-1、5-1 沿用），並修正圖 3-2 標記點偏離曲線、圖 7-2 右梁翼板力方向相反、圖 7-3 RBS 誤畫於立面等問題。\n</footer>')
open('/home/claude/work/lecture-SS-U1-4.html','w',encoding='utf-8').write(s)
print('svgs:',s.count('<svg'),'ids unique check')
ids=re.findall(r'id="(f\d+-\w+)"',s); print(len(ids),len(set(ids)))
