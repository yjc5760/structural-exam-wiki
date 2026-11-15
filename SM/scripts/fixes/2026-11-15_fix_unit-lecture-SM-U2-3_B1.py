# -*- coding: utf-8 -*-
"""同步 SM-U2-3 批 1 勘誤到單元資料與講義：
  study/data/unit-SM-U2-3.json（隆起 2D 卡 meta、2017 年註、SM-2010-3 題目摘要）→ 之後跑 python3 ../scripts/build_unit_page.py SM-U2-3
  study/lecture-SM-U2-3.html（隆起比較表、圖 6-3 隆起方塊、SM-2017-4 手算 (3)）
在 SM/ 下執行；可重複執行。"""
def W(p, s):
    with open(p, "r+b") as f:
        f.seek(0); f.write(s.encode("utf-8")); f.truncate()
def R(t, a, b):
    assert t.count(a) == 1, (a[:60], t.count(a)); return t.replace(a, b)
p = "study/data/unit-SM-U2-3.json"
t = open(p, encoding="utf-8").read()
if "2026-11-15 勘誤同步" not in t:
    t = R(t, "106 年（2017-4）把整條式子連 \\\\(N_c=\\\\pi+2\\\\) 印出，是唯一一次。",
          "106 年（2017-4）印出的是圓弧力矩法形式 \\\\(FS=S_u(\\\\pi+2\\\\alpha)/(\\\\gamma H+q)\\\\)（以最下階支撐為圓心、半徑 \\\\(X\\\\) 到壁底，\\\\(\\\\alpha=\\\\cos^{-1}(\\\\ell/X)\\\\)；不是 \\\\(N_c=\\\\pi+2\\\\) 的誤植，2026-11-15 勘誤同步，FS 2.13），是唯一一次印隆起式。")
    t = R(t, "FS=Su(π+2)/(γH+q)——", "FS=Su(π+2α)/(γH+q)（圓弧力矩法，α 未定義）——")
    t = R(t, "檢核開挖底面管湧（FS=1.11，不到規範 1.5）", "檢核開挖底面管湧（FS=1.11 > 1 但不符現行規範砂湧要求 → 有管湧之虞）")
    W(p, t); print("ok", p)
else:
    print("skip", p)
p = "study/lecture-SM-U2-3.html"
t = open(p, encoding="utf-8").read()
if "2026-11-15 勘誤同步" not in t:
    t = R(t, '<a class="qlink" href="problems-view/SM-2017-4.html" target="_blank">SM-2017-4</a>（用 \\(\\pi+2\\)）',
          '<a class="qlink" href="problems-view/SM-2017-4.html" target="_blank">SM-2017-4</a>（考卷給圓弧力矩法 \\(S_u(\\pi+2\\alpha)\\)，\\(\\alpha=\\cos^{-1}(\\ell/X)\\)）')
    t = R(t, '>③ 隆起（Terzaghi，π+2）<', '>③ 隆起（圓弧力矩法，π+2α）<')
    t = R(t, '>FS = 6.078×5.142/15.392 = 2.03<', '>FS = 6.078×5.397/15.392 = 2.13<')
    t = R(t, '=2.50 → 0.84</text>', '=2.50 → 0.88</text>')
    t = R(t, """$$FS=\\frac{S_u(\\pi+2)}{\\gamma H+q}=\\frac{6.078\\times5.1416}{14.392+1}=\\mathbf{2.03}\\ \\checkmark$$""",
          """考卷給的是 \\(FS=S_u(\\pi+2\\alpha)/(\\gamma H+q)\\)：以最下一段支撐（GL−3.5 m）為圓心、半徑 \\(X=\\ell+D=4.5+6.0=10.5\\) m 的圓弧，\\(\\alpha=\\cos^{-1}(\\ell/X)=64.62^\\circ\\)，\\(\\pi+2\\alpha=5.3974\\)（2026-11-15 勘誤同步：舊版把 \\(2\\alpha\\) 當誤植用 \\(\\pi+2\\)，得 2.03）。
$$FS=\\frac{S_u(\\pi+2\\alpha)}{\\gamma H+q}=\\frac{6.078\\times5.3974}{14.392+1}=\\mathbf{2.13}\\ \\checkmark$$""")
    t = R(t, "\\(S_u=2.50\\)、\\(FS=\\mathbf{0.84}\\)，結論相反。", "\\(S_u=2.50\\)、\\(FS=\\mathbf{0.88}\\)，結論相反。")
    t = R(t, "管湧 2.33、隆起 2.03 都很安全", "管湧 2.33、隆起 2.13 都很安全")
    W(p, t); print("ok", p)
else:
    print("skip", p)
