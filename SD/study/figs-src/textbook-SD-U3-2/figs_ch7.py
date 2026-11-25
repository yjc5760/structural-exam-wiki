# -*- coding: utf-8 -*-
from sdfig import *  # noqa
from figs_ch0 import fig0_1


def fig7_1():
    return fig0_1()


def fig7_2():
    rows = [
        ('1', '問題：力太大（加速度、內力）→ 隔震（S1）；位移太大 → 加阻尼（S3）', AC),
        ('2', '隔震器 → 迴圈：鉛心橡膠 *Q*、*k*_{d}、*D*_{y}；FPS μ*W*、*W*/*R*（S4、S5）', KEY),
        ('3', '割線 *K*_{eD}、迴圈面積 *A*_{TD} → ξ_{eD} = *A*_{TD}/(2π*K*_{eD}*D*²)', TEN),
        ('4', '*T*_{eD} → 查 *B* → *D*_{D} = *gS*_{aD}*T*_{eD}²/(4π²*B*)，迭代', WARN),
        ('5', '最大考量地震 *D*_{M} × 扭轉 → *D*_{TM}；上部柔性 → *D*′_{D}（S2）', COMP),
        ('6', '阻尼器：*c*_{eff} = *C*cos²θ → ξ_{d} → *S*_{a}/*B* → 位移、出力 *C*cosθ·ω*S*_{d}（S6）', TEN),
        ('7', '構材設計：速度型三種情況包絡；多振態用複合阻尼比', KEY),
    ]
    return flow(rows, W=900, bh=44, gap=12, title='隔減震題的解題流程')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
