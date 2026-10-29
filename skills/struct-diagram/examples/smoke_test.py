#!/usr/bin/env python3
"""
smoke_test.py — 安裝驗證：把每個 recipe 各跑一次

用法：
    python3 smoke_test.py [輸出目錄]
    python3 ../scripts/render.py <輸出目錄>      # 應回報 0 個需要修正

若某張圖的中文變成方框，代表本機缺 Noto Sans CJK；
這只影響 PNG 預覽，SVG 進瀏覽器仍正常。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from structdraw import C, column_shape, beam_shape
from recipes import beam_vm, mohr2, mohr3, rc_flexure, pm_interaction, truss_forces, bar_compare

O = sys.argv[1] if len(sys.argv) > 1 else "smoke"
os.makedirs(O, exist_ok=True)

# 1) 簡支梁承受均佈載重
L, w = 8.0, 10.0
xs = [i*L/80 for i in range(81)]
beam_vm(L, xs, [w*L/2 - w*x for x in xs], [w*L/2*x - w*x*x/2 for x in xs],
        supports=[(0, 'pin'), (L, 'roller')], udls=[(0, L, 'w')],
        title="簡支梁承受均佈載重", v_unit="kN", m_unit="kN·m",
        key_V=[(0, '+wL/2', -14), (L, '−wL/2', 18)], key_M=[(L/2, 'wL^{2}/8', -16)],
        note="剪力零點即彎矩極值位置——最快的自我檢核", path=f"{O}/1_beam_vm.svg")

# 2) 三向應力莫爾圓
mohr3(40, 0, -20, title="三向應力 σ_x=40, σ_z=0, σ_y=−20 MPa", path=f"{O}/2_mohr3.svg")

# 3) 平面應力莫爾圓
mohr2(80, -20, 30, title="平面應力 σ_x=80, σ_y=−20, τ_xy=30 MPa", path=f"{O}/3_mohr2.svg")

# 4) RC 撓曲三聯圖
rc_flexure(b=300, h=600, d=540, c=120, a=102,
           title="RC 梁撓曲（b=300, h=600, d=540, c=120, a=102 mm）", path=f"{O}/4_rc.svg")

# 5) P-M 交互曲線
pm_interaction([0, 120, 190, 215, 180, 90, 0], [3200, 2400, 1500, 780, 300, -200, -600],
               marks=[(0, 3200, '純壓 P_{0}'), (215, 780, '平衡點'), (90, -200, '拉力控制')],
               title="柱 P-M 交互曲線", path=f"{O}/5_pm.svg")

# 6) 桁架力流圖
truss_forces({'A': (0, 0), 'B': (2, 0), 'C': (1, 1), 'D': (2, 1)},
             [('A', 'B', -1.0), ('A', 'C', 1.414), ('B', 'C', -1.414), ('C', 'D', 2.0)],
             supports=[('B', 'pin'), ('D', 'roller', 90)], loads=[('A', (0, 0.55), 'P')],
             title="桁架力流圖（桿力以 P 為單位）",
             note="受壓桿 AB、BC 才需檢核挫屈；受拉桿以降伏控制", path=f"{O}/6_truss.svg")

# 7) 量級比較
def sk(mini, i):
    D = 0.30; th = (0.0, -0.6*D, -1.5*D)[i]; col = ("#1D4ED8", "#B45309", "#94A3B8")[i]
    for s, e in (((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))):
        mini.line(s, e, C["ghost"], 2.2, dash="4 4", cap="butt")
    mini.poly(column_shape((0, 0), 1.0, D, th), col, 3.2)
    mini.poly(column_shape((1, 0), 1.0, D, th), col, 3.2)
    mini.poly(beam_shape((D, 1), 1.0, th, th), col, 3.2)

bar_compare([("梁無限剛　EI_{b} → ∞", "θ_{B} = θ_{C} = 0", 24.0, "24EI/L^{3}", "#1D4ED8"),
             ("梁柱同 EI/L", "θ = 3Δ/5L", 16.8, "84EI/5L^{3}", "#B45309"),
             ("梁無勁度　EI_{b} → 0", "兩根獨立懸臂柱", 6.0, "6EI/L^{3}", "#94A3B8")],
            title="側向勁度光譜", sub="答案必落在此區間，否則量級就錯了",
            sketch=sk, path=f"{O}/7_bars.svg")

print(f"7 張圖已輸出至 {O}/　接著執行： python3 ../scripts/render.py {O}")
