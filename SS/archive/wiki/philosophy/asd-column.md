# ASD 壓力桿件設計哲學（SS-U1-1）

**哲學 ID：** asd-column
**適用規範：** 容許應力設計法（ASD）
**命題大綱：** SS-U1-1 拉力及壓力桿件
**核心原則：** $f_a \leq F_a$（工作載重應力不超過容許應力）

---

## 設計邏輯

```
① 計算需求應力
   fa = P / A

② 計算 Cc（彈性/非彈性分界細長比）
   Cc = √(2π²E / Fy)

③ 判斷挫屈類型並計算容許應力 Fa
   KL/r ≤ Cc（非彈性）：
     Fa = [1 - (KL/r)² / 2Cc²] × Fy / FS
     FS = 5/3 + 3(KL/r)/8Cc - (KL/r)³/8Cc³

   KL/r > Cc（彈性）：
     Fa = 12π²E / [23(KL/r)²]

④ 檢核
   fa ≤ Fa → OK
```

## 關鍵公式

$$C_c = \sqrt{\frac{2\pi^2 E}{F_y}}$$

## 與 LRFD 的對應

| ASD | LRFD |
|-----|------|
| $C_c$（分界） | $\lambda_c = 1.5$ |
| $F_a$（容許應力） | $F_{cr}$（臨界應力）/ 安全係數 |
| $f_a \leq F_a$ | $P_u \leq \phi_c P_n$ |

## 出現題目

| 題目 | 年份 | 核心考點 |
|------|------|---------|
| [SS-2023-2](../problems/SS-2023-2.md) | 112年 | ASD 柱設計、Cc |
| [SS-2017-3](../problems/SS-2017-3.md) | 106年 | ASD 組合 H 型鋼柱 |
| [SS-2010-3](../problems/SS-2010-3.md) | 99年 | ASD + LRFD 組合柱 |
| [SS-2008-1](../problems/SS-2008-1.md) | 97年 | ASD 梁設計 |
| [SS-2007-2](../problems/SS-2007-2.md) | 96年 | ASD 梁柱互制 |
