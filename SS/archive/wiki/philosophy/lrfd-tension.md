# LRFD 拉力桿件設計哲學（SS-U1-1）

**哲學 ID：** lrfd-tension
**適用規範：** 鋼結構極限設計法（LRFD）
**命題大綱：** SS-U1-1 拉力及壓力桿件
**核心原則：** $\phi_t P_n$ 取三種極限狀態最小值

---

## 設計邏輯

```
① GSY 全斷面降伏（Gross Section Yielding）
   φt = 0.90
   Pn = Fy × Ag

② NSF 淨斷面斷裂（Net Section Fracture）
   φt = 0.75
   Pn = Fu × Ae，Ae = U × An
   U 值：查表（0.9/0.85/0.75）或公式 U = 1 - x̄/L

③ BSR 塊狀剪力撕裂（Block Shear Rupture）
   φ = 0.75
   當 FuAnt ≥ 0.6FuAnv：Rn = 0.6FyAgv + FuAnt
   當 0.6FuAnv > FuAnt ：Rn = 0.6FuAnv + FyAgt
   上限：φ[0.6FuAnv + FuAnt]

φtPn = min(①, ②, ③)
```

## 關鍵判斷：U 值

| 接合情況 | U 值 |
|---------|------|
| 所有元件均連接 | 1.00 |
| 翼板 + 腹板連接（W 型鋼） | 0.90 |
| 僅翼板連接（W 型鋼） | 0.85 |
| 僅腹板連接（W 型鋼） | 0.70 |
| 單角鋼（長肢連接） | 0.80 |
| 單角鋼（短肢連接） | 0.60 |
| 或用公式 $U = 1 - \bar{x}/L$ | — |

## 常見陷阱

1. **三種極限狀態缺一**：BSR 最常被遺漏
2. **An vs Ae**：$A_e = U \times A_n$，U 值與連接型式有關
3. **BSR 判斷條件**：$F_u A_{nt}$ 與 $0.6 F_u A_{nv}$ 比較，而非面積

## 出現題目

| 題目 | 年份 | 核心考點 |
|------|------|---------|
| [SS-2025-2](../problems/SS-2025-2.md) | 114年 | ASD 拉力、剪力遲滯 |
| [SS-2024-2](../problems/SS-2024-2.md) | 113年 | 圓管 HSS、縱向銲、U 值 |
| [SS-2023-1](../problems/SS-2023-1.md) | 112年 | 壓/拉力桿件 |
| [SS-2022-2](../problems/SS-2022-2.md) | 111年 | 插銷接合 ASD |
| [SS-2021-2](../problems/SS-2021-2.md) | 110年 | 拉力構材、塊狀剪力 |
| [SS-2015-2](../problems/SS-2015-2.md) | 104年 | 剪力遲滯、U 值、BSR |
| [SS-2014-2](../problems/SS-2014-2.md) | 103年 | SN 耐震鋼材、容量設計 |
| [SS-2005-1](../problems/SS-2005-1.md) | 94年 | 角鋼拉力、螺栓群 |
