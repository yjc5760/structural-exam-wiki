#!/usr/bin/env python3
"""U3-2-G4 階段 E（2026-11-16）：把解題圖解插回解析（非勘誤）。圖由 gen_SD-2018-1.py、gen_SD-2023-3.py 產生（先執行 render.py 出 2× PNG）。
可重複執行（已插入者略過）。用法：python3 <本檔> <SD 科目資料夾>"""
import sys
from pathlib import Path
SD = Path(sys.argv[1]); D = "2026-11-16"
def load(qid):
    p = SD/f"raw/solutions/{qid}/{qid}.md"
    with open(p, encoding="utf-8", newline="") as f: raw = f.read()
    return p, raw.replace("\r\n", "\n"), ("\r\n" in raw)
def save(p, t, crlf):
    if crlf: t = t.replace("\n", "\r\n")
    with open(p, "w", encoding="utf-8", newline="") as f: f.write(t)
def ins_after(t, anchor, add, qid):
    assert t.count(anchor) == 1, (qid, anchor[:50], t.count(anchor)); return t.replace(anchor, anchor + add)
def run(qid, inserts, figs, footer):
    p, t, crlf = load(qid)
    if f"figs/{figs[0]}" in t: print(qid, "skip"); return
    for f in figs: assert (SD/f"raw/solutions/{qid}/figs/{f}").exists() and (SD/f"raw/solutions/{qid}/figs/{f[:-4]}.png").exists(), f
    for a, add in inserts: t = ins_after(t, a, add, qid)
    t = t.rstrip("\n") + "\n\n" + footer + "\n"
    save(p, t, crlf); print(qid, "inserted", len(inserts))

run("SD-2018-1", [
 ("故等效水平阻尼係數 c_eff = C·cos²θ。*\n",
  "\n![SD-2018-1 對角阻尼器幾何：樓層側移 u 時，斜撐由左柱底伸到右柱頂，伸長量 δ＝u·cosθ；θ＝26.6°、cosθ＝0.8944，等效水平阻尼係數 c_eff＝0.80 C](figs/SD-2018-1-fig-2-damper-geometry.svg)\n"
  "*圖 2　對角阻尼器的兩次 cosθ：伸長速度是樓層速度的 cosθ 倍，軸力的水平分量再乘一次 cosθ，所以 c_eff＝C cos²θ＝0.80 C。可攔下「阻尼器當水平裝設（cosθ＝1）」與「只乘一次 cosθ」兩種錯。*\n"),
 ("$$S_a = 0.3g = 0.3 \\times 9.8 = 2.94 \\text{ m/s}^2$$\n",
  "\n![SD-2018-1 加速度反應譜：T 小於 0.5 s 為 0.3g 平台、之後 0.15g/T 下降；本題 T＝0.252 s 落在平台段，Sa＝2.94 m/s²](figs/SD-2018-1-fig-3-spectrum.svg)\n"
  "*圖 3　反應譜轉折點 T*＝0.5 s，本題 T＝0.252 s 在平台段取 0.3g（不是 0.15g/T＝0.595g）；圖下列出 Sd＝4.725 mm、Sv＝0.1179 m/s、F_d＝2.35 kN。*\n"),
], ["SD-2018-1-fig-2-damper-geometry.svg", "SD-2018-1-fig-3-spectrum.svg"],
 f"*修正日期：{D}（非勘誤）標頭主／副分類改為與索引一致（主 SD-U3-2、副 SD-U1-3）；圖解補繪：figs/SD-2018-1-fig-2-damper-geometry.svg（對角阻尼器幾何與 cos²θ）、figs/SD-2018-1-fig-3-spectrum.svg（反應譜平台段取值），腳本 gen_SD-2018-1.py，答案不變*")

run("SD-2023-3", [
 ("$\\beta_{eff} = 50/(4\\pi \\times 80) = 50/1005.3 = 4.97\\%$ ✓\n",
  "\n![SD-2023-3 等效阻尼比的能量意義：割線勁度 K_eff＝1000 kN/m 通過頂點 (0.4 m, 400 kN)，紅色三角形為 E_S0＝80 kN·m，綠色迴圈面積 E_D＝50 kN·m（形狀示意），ξ＝50/(4π×80)＝4.97%](figs/SD-2023-3-fig-1-energy.svg)\n"
  "*圖 1　等效阻尼比＝迴圈面積 ÷（4π × 割線三角形面積）。三角形是 K_eff 割線下的彈性應變能 E_S0＝K_eff D²/2＝80 kN·m，不是迴圈面積；分母漏 2π 會得 31%，誤用 4πK_eff D² 會得 2.5%。迴圈形狀為示意（考卷只給面積）。*\n"),
], ["SD-2023-3-fig-1-energy.svg"],
 f"*修正日期：{D}（非勘誤）圖解補繪：figs/SD-2023-3-fig-1-energy.svg（割線勁度、E_S0 三角形與遲滯迴圈面積），腳本 gen_SD-2023-3.py，答案不變*")
