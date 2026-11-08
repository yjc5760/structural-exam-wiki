# -*- coding: utf-8 -*-
"""本單元教科書講義的所有數值（圖與內文共用，先算再寫）。單位請在此註明。

規則：
  * 講義內文、圖、範例出現的每一個數字都要能在這裡找到來源。
  * 考題數字一律取自 raw/solutions/XX-YYYY-N/XX-YYYY-N.md（勘誤後版本）。
  * 寫完執行 `python3 calcs.py`，把印出的數字和內文逐一對照。
"""
import math

E = 2040.0   # 範例：tf/cm²


def example():
    d = dict(A=19.0, Fy=2.52)
    d['P'] = 0.9 * d['Fy'] * d['A']
    return d


if __name__ == '__main__':
    for k, v in example().items():
        print(k, round(v, 4) if isinstance(v, float) else v)
