# 題型診斷：壓力桿件

---

## 辨識關鍵字

`受壓` `軸壓` `壓力桿件` `鋼柱` `有效長度` `KL/r` `λc` `Cc` `挫屈` `對位圖` `Fcr` `Fa` `φcPn` `容許壓力` `設計壓力強度`

---

## 決策樹

```
看到「壓力桿件」或「受壓鋼柱」
    │
    ├─ 題目要求 LRFD
    │       → λc = (KL/rπ)√(Fy/E)
    │         λc ≤ 1.5 → Fcr = 0.658^(λc²) Fy
    │         λc > 1.5 → Fcr = 0.877/λc² × Fy
    │         φcPn = 0.85 FcrA
    │         Method: [[lrfd-column]]
    │
    ├─ 題目要求 ASD
    │       → Cc = √(2π²E/Fy)
    │         KL/r ≤ Cc → 非彈性，用 Fa 公式含 FS
    │         KL/r > Cc → 彈性長柱，Fa = 12π²E/[23(KL/r)²]
    │         Pa = FaA
    │         Method: [[asd-column]]
    │
    ├─ 有「對位圖」「剛架」「有側移」「G值」
    │       → 先查 G → 對位圖查 K → 再進 LRFD/ASD 流程
    │         Method: [[effective-length-chart]]
    │
    ├─ 有「LeMessurier」「層間穩定」「臨界載重」
    │       → 層間穩定：ΣPu ≥ ΣPeK 時失穩
    │         ΣPeK = Σ[π²EI/(KL)²]（含所有柱）
    │         Method: [[effective-length-chart]]
    │
    ├─ 有「分段側撐」「分兩段」「弱軸有支撐」
    │       → 分段計算各段 KL/r，取最大值控制
    │         強軸：全柱 KxLx/rx
    │         弱軸：各段各自 KyLy/ry
    │
    └─ 有「組合柱」「四角鋼」「組合斷面」
            → 計算組合斷面 I、A → r = √(I/A)
              注意控制 r 方向（通常弱軸最小）
```

---

## K 值速查

| 端點條件 | 理論 K | 設計建議 K |
|---------|--------|----------|
| 兩端鉸接 | 1.0 | 1.0 |
| 一端固、一端鉸 | 0.707 | 0.8 |
| 兩端固定（無側移） | 0.5 | 0.65 |
| 一端固、一端自由 | 2.0 | 2.1 |
| 有側移框架（查對位圖） | > 1.0 | ≥ 1.2 |

---

## 常見陷阱

- **λc 公式含 π**：$\lambda_c = \frac{KL}{r\pi}\sqrt{F_y/E}$，π 在分母
- **φc = 0.85**，不是 0.9
- **0.658 的指數是 λc²**：先算 λc²，再算指數
- **強弱軸分開計算，取最大 KL/r**
- **固接 G=1，鉸接 G=10**（設計值，非理論值）

---

## 相關 Methods / Concepts / Traps

- Method: [[lrfd-column]] [[asd-column]] [[effective-length-chart]]
- Concept: [[FLEXURAL-BUCKLING-GENERAL]] [[COLUMN-STRENGTH-CURVE]] [[EULER-BUCKLING]] [[RESIDUAL-STRESS]] [[TANGENT-MODULUS-THEORY]]
- Traps: [[COLUMN-BUCKLING-TRAPS]] [[HIGH-STRENGTH-STEEL-SLENDER-COLUMN]]
- 失敗模式: [[stability-failure]]
- 歷屆題目: SS-2002-3, SS-2013-3, SS-2018-2, SS-2024-1
