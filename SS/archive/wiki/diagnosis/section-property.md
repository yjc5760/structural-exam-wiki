# 題型診斷：斷面性質計算

---

## 辨識關鍵字

`慣性矩` `Ix` `Iy` `斷面模數` `Sx` `塑性斷面模數` `Zx` `形狀因子` `f = Zx/Sx` `塑性中性軸` `彈性中性軸` `ENA` `PNA` `迴轉半徑` `平行軸定理`

---

## 決策樹

```
看到「斷面性質」計算
    │
    ├─ 求 Ix（彈性，對 ENA）
    │       → 平行軸定理：I = Σ(Io + Adi²)
    │         各矩形：Io = bh³/12，di = 距 ENA 距離
    │         ENA 位置：Σ(Ai×yi) / ΣAi（面積矩法）
    │         對稱斷面：ENA 在幾何中心
    │
    ├─ 求 Sx（彈性斷面模數）
    │       → Sx = Ix / c（c = 最外緣到 ENA 距離）
    │         My = Fy × Sx
    │
    ├─ 求 Zx（塑性斷面模數）
    │       → Step 1: 找 PNA（等面積：A上 = A下 = A/2）
    │           對稱斷面：PNA = ENA = 幾何中心
    │           非對稱斷面：需解 PNA 位置
    │         Step 2: Zx = Q上 + Q下
    │           = Σ(Ai × ȳi)上 + Σ(Aj × ȳj)下
    │         對稱斷面：Zx = 2 × Q上
    │         Method: [[plastic-zx]]
    │
    ├─ 求形狀因子 f
    │       → f = Zx/Sx = Mp/My
    │         H型鋼 ≈ 1.12；矩形 = 1.5；圓形 = 1.70
    │         Concept: [[SHAPE-FACTOR]]
    │
    ├─ 求 ry 或 r（迴轉半徑）
    │       → r = √(I/A)
    │         用於計算 KL/r（壓力桿件）
    │
    └─ 複雜斷面（十字形、空心圓、非標準）
            → 分割為簡單幾何 → 平行軸定理疊加
              空心：外圓 - 內圓
              十字形：水平段 + 垂直段（扣重疊區）
```

---

## 常用斷面公式速查

| 斷面 | Ix | Sx | Zx |
|------|----|----|-----|
| 矩形 $b \times h$ | $bh^3/12$ | $bh^2/6$ | $bh^2/4$ |
| 實心圓 $D$ | $\pi D^4/64$ | $\pi D^3/32$ | $D^3/6$ |
| 空心圓管 $D,d$ | $\pi(D^4-d^4)/64$ | $(D^4-d^4)/(32c)$ | $(D^3-d^3)/6$ |
| H 型鋼 | 翼板 + 腹板疊加 | $I_x/c$ | 翼板 + 腹板各算 |

---

## 常見陷阱

- **Zx ≠ Ix/c**（後者是 Sx）
- **十字形分割注意重疊區**（中心 2×2 計算兩次需扣除）
- **對稱斷面 PNA = ENA**，不須另外解
- **半圓一次矩 Q = 2R³/3**（對直徑軸）
- **平行軸定理距離 di 是到整體 ENA**，非到自身形心

---

## 相關 Methods / Concepts / Traps

- Method: [[plastic-zx]]
- Concept: [[SHAPE-FACTOR]] [[PLASTIC-NEUTRAL-AXIS-PNA]] [[PLASTIC-MOMENT-MP]] [[YIELD-MOMENT-MY]]
- Traps: [[MATERIAL-TRAPS]]
- 歷屆題目: SS-2006-3, SS-2009-3, SS-2010-1, SS-2013-1
