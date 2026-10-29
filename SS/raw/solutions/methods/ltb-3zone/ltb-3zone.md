# LTB 側扭挫屈三區段判斷流程

**方法 ID：** ltb-3zone
**知識分類：** 解題工具 / 梁設計
**適用題型：** SS-U1-2 梁桿件、SS-U1-3 梁柱桿件
**出現題數：** 18 題（最高頻，幾乎每年必考）

---

## 核心原理

梁在彎矩作用下可能發生「側向扭轉挫屈（LTB）」——壓力翼板側移、梁體扭轉，導致彎矩強度低於塑性彎矩 $M_p$。LRFD 規範以無束制長度 $L_b$（梁側撐點間距）分三段判斷：

$$M_n = \begin{cases}
M_p & L_b \leq L_p \quad \text{（塑性區，LTB 不控制）}\\
C_b \left[ M_p - (M_p - M_r)\dfrac{L_b - L_p}{L_r - L_p} \right] \leq M_p & L_p < L_b \leq L_r \quad \text{（非彈性 LTB）}\\
C_b \cdot M_{cr} \leq M_p & L_b > L_r \quad \text{（彈性 LTB）}
\end{cases}$$

---

## 關鍵參數速查

| 符號 | 意義 | 公式 |
|------|------|------|
| $M_p$ | 塑性彎矩 | $F_y Z_x$ |
| $M_r$ | 殘留應力修正彎矩 | $(F_y - F_r) S_x$，$F_r = 1.16\ \text{tf/cm}^2$（焊接型） / $0.7\ \text{tf/cm}^2$（輾軋型）|
| $L_p$ | 塑性區上限長度 | $1.76\,r_y\sqrt{\dfrac{E}{F_y}}\;=\;\dfrac{80\,r_y}{\sqrt{F_y}}$（$F_y$ 單位 **tf/cm²**，$E=2040$ tf/cm²）|
| $L_r$ | 非彈性 LTB 上限長度 | $\dfrac{r_y X_1}{F_y - F_r}\sqrt{1 + \sqrt{1 + X_2(F_y-F_r)^2}}$ |
| $X_1$ | LTB 輔助參數 | $\dfrac{\pi}{S_x}\sqrt{\dfrac{EGJA}{2}}$ |
| $X_2$ | LTB 輔助參數 | $4\dfrac{C_w}{I_y}\left(\dfrac{S_x}{GJ}\right)^2$ |
| $M_{cr}$ | 彈性 LTB 臨界彎矩 | $\dfrac{\pi}{L_b}\sqrt{EI_y GJ + \left(\dfrac{\pi E}{L_b}\right)^2 I_y C_w}$ 或 $\dfrac{C_b S_x X_1 \sqrt{2}}{L_b/r_y}\sqrt{1 + \dfrac{X_1^2 X_2}{2(L_b/r_y)^2}}$ |
| $C_b$ | 彎矩修正係數 | $\dfrac{12.5 M_{max}}{2.5M_{max}+3M_A+4M_B+3M_C}$ |

**記憶口訣：**
- $L_p$：小 $L_b$ → 全塑（Plastic）
- $L_r$：大 $L_b$ → 彈性（Elastic 'r' for residual stress boundary）
- $C_b \geq 1$，均勻彎矩時 $C_b = 1$，中間高兩端低時 $C_b > 1$

---

## 解題步驟

```
Step 1  確認斷面結實（Compact Section）
        ※ 以下係數為 tf/cm² 制（Fy 用 tf/cm²）；括號內為 ksi 制對應係數
        翼板：λf = bf/(2tf) ≤ λpf = 0.38√(E/Fy) = 17/√Fy   （ksi 制：65/√Fy）
        腹板：λw = h/tw  ≤ λpw = 3.76√(E/Fy) = 170/√Fy  （ksi 制：640/√Fy）
        → 結實斷面才能達到 Mp，否則用非結實斷面公式

Step 2  計算塑性/彈性彎矩
        Mp = Fy × Zx
        Mr = (Fy - Fr) × Sx
        （Fr = 1.16 tf/cm² 焊接型；0.70 tf/cm² 輾軋型）

Step 3  計算 LTB 輔助參數（若未給 Lp、Lr 需自行算）
        X1 = (π/Sx)√(EGJA/2)
        X2 = 4(Cw/Iy)(Sx/GJ)²
        Lp = 1.76·ry·√(E/Fy) = 80ry/√Fy   [cm, tf/cm², E=2040]
             ↳ 心算門檻：Fy=2.5 時 Lp ≈ 50ry；Fy=3.3 時 Lp ≈ 44ry
        Lr = ry·X1/(Fy-Fr) × √(1 + √(1 + X2(Fy-Fr)²))

Step 4  計算每個無束制段的 Cb
        Cb = 12.5Mmax / (2.5Mmax + 3MA + 4MB + 3MC)
        （MA=1/4點, MB=1/2點, MC=3/4點彎矩絕對值）
        → 均勻彎矩 Cb = 1.0；雙曲率 Cb 較大

Step 5  判斷 Lb 落在哪個區段（每個無束制段各自判斷）
        ① Lb ≤ Lp → Mn = Mp（最強）
        ② Lp < Lb ≤ Lr → 非彈性 LTB 線性內插公式
        ③ Lb > Lr  → 彈性 LTB，Mn = Cb × Mcr ≤ Mp

Step 6  套用對應公式，注意 Mn ≤ Mp 上限
        各段 φbMn = 0.9 × Mn

Step 7  與彎矩需求 Mu 比較，找控制段
        設計強度 = min(φbMn) 跨各無束制段
```

---

## ASD 版本對照

ASD 規範（容許應力法）以容許彎曲應力 $F_b$ 取代 $\phi M_n$：

$$F_b = \begin{cases}
0.66 F_y & L_b \leq L_c \text{（全塑）} \\
\text{線性內插或 Fbx 公式} & L_c < L_b \leq L_u \\
\dfrac{170000 C_b}{(L_b/r_T)^2} & L_b/r_T > \sqrt{703000 C_b/F_y}
\end{cases}$$

> ⚠️ **單位警告**：上式的 170000、703000 是 **ksi 制**係數（$F_y$ 用 ksi、長度用 in）。
> 台灣教科書若改用 tf/cm² 或 kgf/cm²，係數完全不同。ASD 題目通常直接給 $L_c$、$L_u$ 或設計表；
> 若須自算，先確認題目的 $F_y$ 單位再選係數，並在答案卷上寫明採用的單位制。
> 詳見 [[asd-beam]] 與 [[asd-beam-fb-derivation]]。

---

## 常見陷阱彙整

| # | 陷阱 | 說明 | 對策 |
|---|------|------|------|
| 1 | **$M_n \leq M_p$ 忘記上限** | 非彈性/彈性段乘 $C_b$ 後若超過 $M_p$，必須截斷為 $M_p$ | 計算完永遠加一步：取 $\min(C_b \times \text{公式結果},\ M_p)$ |
| 2 | **每段各自計算 $C_b$** | 多段梁每個無束制段有自己的 $C_b$，不能用同一個 | 先標明所有側撐點，再逐段算 $C_b$ |
| 3 | **$M_r$ 含 $F_r$，$M_p$ 不含** | 殘留應力只影響 $M_r$、$L_r$，不影響 $M_p$ | $M_p = F_y Z_x$（無 $F_r$）；$M_r = (F_y - F_r)S_x$ |
| 4 | **$X_2$ 單位** | $X_2 = 4(C_w/I_y)(S_x/GJ)^2$，各項需同一單位制 | 統一用 cm, tf 制；$G = 800\ \text{tf/cm}^2$ |
| 5 | **$C_b$ 的 $M$ 取絕對值** | $M_A, M_B, M_C$ 均取絕對值，彎矩圖可能正負 | 畫彎矩圖後取各點絕對值 |
| 6 | **輾軋型 vs 焊接型 $F_r$** | 輾軋型 $F_r = 0.70\ \text{tf/cm}^2$，焊接型 $F_r = 1.16\ \text{tf/cm}^2$ | 題目給定型式確認，H 型鋼通常輾軋型 |

---

## 考試速查：Lb 判斷決策樹

```
給定 Lb（無束制長度）
    │
    ├─ Lb ≤ Lp ──→ Mn = Mp = FyZx  （最強，無折減）
    │
    ├─ Lp < Lb ≤ Lr ──→ Mn = Cb[Mp - (Mp-Mr)(Lb-Lp)/(Lr-Lp)] ≤ Mp
    │                      （線性內插，Cb > 1 時有加成）
    │
    └─ Lb > Lr ──→ Mn = Cb × Mcr ≤ Mp
                     （彈性，Mcr 用 Lx、X1、X2 計算）
```

---

## 出現題目

| 題號 | 考年 | 重點 |
|------|------|------|
| [[SS-2007-3]] | 96年 | LRFD 三區段完整計算，X1/X2 推導 |
| [[SS-2008-1]] | 97年 | ASD Fb 判斷，rT 迴轉半徑 |
| [[SS-2008-3]] | 97年 | 多側撐段各自計算 Cb，找控制段 |
| [[SS-2010-4]] | 99年 | 全側撐梁（Lb=0），直接 Mn=Mp |
| [[SS-2011-1]] | 100年 | Cb 修正係數計算，彎矩圖讀取 |
| [[SS-2011-3]] | 100年 | LTB + 斷面選擇 |
| [[SS-2012-1]] | 101年 | 非彈性 LTB 線性內插 |
| [[SS-2014-3]] | 103年 | Lp/Lr 計算 + 驗核 |
| [[SS-2015-1]] | 104年 | 三分點側撐，各段 Cb |
| [[SS-2016-4]] | 105年 | 彈性 LTB，Mcr 計算 |
| [[SS-2020-3]] | 109年 | LTB + P-M 互制複合題 |
| [[SS-2021-3]] | 110年 | 全側撐 + 使用性撓度 |
| [[SS-2022-1]] | 111年 | LTB + 雙軸彎矩 |
| [[SS-2024-3]] | 113年 | 完整三區段 |
| [[SS-2025-1]] | 114年 | 寬厚比確認 + Mn=Mp |
| [[SS-2025-3]] | 114年 | LTB + 撓度 |
