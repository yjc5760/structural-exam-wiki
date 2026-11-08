# 題型診斷：梁柱桿件

---

## 辨識關鍵字

`軸力 + 彎矩` `梁柱` `P-M 互制` `交互作用` `H1-1` `B1` `B2` `Mnt` `Mlt` `二階效應` `P-δ` `P-Δ` `有側移` `Cm`

---

## 決策樹

```
看到「梁柱桿件」或「軸力 + 彎矩共同作用」
    │
    Step 1：計算壓力設計強度 φcPn
    │   → 用 LRFD-Column 流程
    │     ┌ 需要 K → 有剛架：先查對位圖 [[effective-length-chart]]
    │     └ 無側移：K 由端點條件決定
    │
    Step 2：計算彎矩設計強度 φbMnx（φbMny）
    │   → 用 LTB-3Zone 流程 [[ltb-3zone]]
    │     單軸彎矩：只算 x 軸
    │     雙軸彎矩：x、y 軸各算
    │
    Step 3：計算二階設計彎矩 Mux
    │   ├─ 有側移框架（題目說「有側移」「無斜撐」「水平力」）
    │   │       Mux = B1×Mnt + B2×Mlt
    │   │       B1 = Cm/(1-Pu/Pe1)  [K=1]
    │   │       B2 = 1/(1-ΣPu/ΣPeK) [對位圖 K]
    │   │       Method: [[b1b2-amplification]]
    │   │
    │   └─ 無側移（有斜撐框架）
    │           Mux = B1×Mnt（只有構件彎曲放大）
    │           Mlt = 0
    │
    Step 4：P-M 互制方程式
    │   判斷 Pu/(φcPn)：
    │   ≥ 0.2 → Pu/(φcPn) + 8/9 × (Mux/φbMnx + Muy/φbMny) ≤ 1.0
    │   < 0.2 → Pu/(2φcPn) + (Mux/φbMnx + Muy/φbMny) ≤ 1.0
    │   Method: [[pm-interaction]]
    │
    └─ 若題目要求「繪 P-M 互制圖」
            → x 軸 M/φbMn，y 軸 P/φcPn
              折線：(0,1)→(1/9, 0.2)→(1,0)
              標示設計點
```

---

## ASD 梁柱（舊式題型）

```
兩個方程式均需滿足：
① fa/Fa + Cm×fbx/[(1-fa/F'ex)Fbx] + fby/[(1-fa/F'ey)Fby] ≤ 1.0
② fa/(0.6Fy) + fbx/Fbx + fby/Fby ≤ 1.0
```

---

## 常見陷阱

- **φc = 0.85（壓力），φb = 0.90（彎矩）**，不要混用
- **先判斷 Pu/(φcPn) ≥ 0.2 才選公式**
- **B1 用 K=1，B2 用對位圖 K**（不同！）
- **B1、B2 均 ≥ 1.0**（取 max 與 1）
- **Mux 是二階彎矩**，輸入 P-M 前須先做 B1B2 放大
- **ΣPeK 含整層所有柱**（B2 分母）

---

## 相關 Methods / Concepts / Traps

- Method: [[lrfd-column]] [[ltb-3zone]] [[b1b2-amplification]] [[pm-interaction]] [[effective-length-chart]]
- Concept: [[BEAM-COLUMN-INTERACTION]] [[MOMENT-AMPLIFICATION-B1-B2]] [[P-DELTA-EFFECT]] [[SECOND-ORDER-ANALYSIS]]
- Traps: [[BEAM-COLUMN-TRAPS]]
- 歷屆題目: SS-2012-3, SS-2013-4, SS-2014-4, SS-2019-3, SS-2020-3, SS-2022-1
