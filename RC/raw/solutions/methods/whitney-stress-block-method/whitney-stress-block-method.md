# Whitney 等值矩形應力塊法

**方法 ID：** whitney-stress-block-method
**知識分類：** 解題工具
**適用題型：** RC-U1-1 梁彎矩強度、RC-U1-2 柱強度

---

## 核心原理

混凝土壓力區的非線性應力分布（拋物線-矩形）以均勻應力 $0.85f'_c$、深度 $a = \beta_1 c$ 的矩形等效取代，使壓力合力 $C = 0.85f'_c \cdot a \cdot b$ 可用代數直接計算。極限狀態時混凝土壓應變取 $\varepsilon_{cu} = 0.003$。

---

## 邊界條件／對應關係表

| 條件 | 取值 |
|------|------|
| $f'_c \leq 280 \text{ kgf/cm}^2$ | $\beta_1 = 0.85$ |
| $f'_c > 280 \text{ kgf/cm}^2$ | $\beta_1 = 0.85 - 0.05\,\dfrac{f'_c - 280}{70} \geq 0.65$ |
| 拉力控制（$\varepsilon_t \geq 0.005$） | $\phi = 0.90$ |
| 過渡區（$0.002 < \varepsilon_t < 0.005$）| $\phi = 0.65 + (\varepsilon_t - 0.002)\,\dfrac{0.25}{0.003}$（箍筋柱） |
| 壓力控制（$\varepsilon_t \leq 0.002$）| $\phi = 0.65$（箍筋柱），$0.75$（螺旋柱） |
| 依據 | 112 年版表 21.2.2：$\phi = 0.65 + 0.25(\varepsilon_t-\varepsilon_{ty})/0.003$，拉力控制 $\varepsilon_t \ge \varepsilon_{ty}+0.003$；§21.2.2.1 SD420 取 $\varepsilon_{ty} = 0.002$（上三列即此）；$f_y \ne 4200$ 時 $\varepsilon_{ty} = f_y/E_s$ |
| 非預力梁的延性要求 | §9.3.3.1：須拉力控制（SD420：$\varepsilon_t \ge 0.005$）；舊規範 $\varepsilon_t \ge 0.004$ 已取消 |

---

## 步驟流程

### 單筋矩形梁

**Step 1：計算等值應力塊深度**

$$a = \frac{A_s f_y}{0.85 f'_c b}$$

**Step 2：中性軸深度與淨拉應變**

$$c = \frac{a}{\beta_1}, \quad \varepsilon_t = 0.003\,\frac{d - c}{c}$$

**Step 3：強度折減係數**

依 $\varepsilon_t$ 查上表得 $\phi$。

**Step 4：標稱彎矩強度**

$$M_n = A_s f_y \left(d - \frac{a}{2}\right)$$

**Step 5：設計強度驗核**

$$\phi M_n \geq M_u \quad \checkmark$$

---

## 常用型式與結果表

| 梁型 | 壓力合力 C | 力臂 | 注意事項 |
|------|-----------|------|---------|
| 單筋矩形梁 | $0.85f'_c a b$ | $d - a/2$ | 最基本型 |
| 雙筋梁 | $0.85f'_c a b + A'_s f'_s$ | — | 先驗壓力筋是否降伏（$\varepsilon'_s \geq \varepsilon_y$） |
| T 形梁（a≤hf） | $0.85f'_c a b_e$ | $d - a/2$ | $b$ 取有效翼板寬 $b_e$ |
| T 形梁（a>hf） | 翼板 + 腹板兩部分相加 | 分別計算 | 見 [t-beam-analysis](t-beam-analysis.md) |

---

## 推導示範

**雙筋梁壓力筋是否降伏判斷：**

設壓力筋深度 $d'$，降伏條件為：

$$\varepsilon'_s = 0.003\,\frac{c - d'}{c} \geq \varepsilon_y = \frac{f_y}{E_s}$$

若 $\varepsilon'_s < \varepsilon_y$，則 $f'_s = E_s \varepsilon'_s < f_y$（不可假設降伏）。

---

## 出現題目（使用本方法的考題，依 question_index 標籤核實）

| 題號 | 核心應用 |
|------|---------|
| [RC-2002-4](../problems/RC-2002-4.md) | 雙筋梁，壓力筋恰降伏邊界，$\beta_1 = 0.80$ |
| [RC-2004-2](../problems/RC-2004-2.md) | 外伸梁單筋設計，過渡區 $\phi$ 值 |
| [RC-2007-1](../problems/RC-2007-1.md) | T 形梁，有效翼板寬，$a \leq h_f$ |
| [RC-2014-1](../problems/RC-2014-1.md) | 單筋過筋梁，雙 $f'_c$ 複合斷面 |
| [RC-2015-2](../problems/RC-2015-2.md) | 雙筋梁，最大設計彎矩在拉力控制界限 $\varepsilon_t = 0.005$ |
| [RC-2016-1](../problems/RC-2016-1.md) | 單筋矩形梁，地震彎矩組合 |
| [RC-2019-1](../problems/RC-2019-1.md) | 單筋梁，過渡區 $\phi$ 值 |
| [RC-2022-1](../problems/RC-2022-1.md) | 雙筋梁，壓力筋未降伏，有效深度求解 |
| [RC-2022-2](../problems/RC-2022-2.md) | 梁設計最經濟材料 |
| [RC-2023-1](../problems/RC-2023-1.md) | 曲率延展比，降伏曲率 $\phi_y$ |
| [RC-2023-2](../problems/RC-2023-2.md) | T 形梁雙筋，壓力鋼筋未降伏 |
| [RC-2024-1](../problems/RC-2024-1.md) | T 形梁最大/最小鋼筋量，高強度鋼筋 |
| [RC-2024-2](../problems/RC-2024-2.md) | 雙筋梁壓力筋未降伏，懸臂梁 |

*修正日期：2026-11-21（補 φ 依據表 21.2.2／§21.2.2.1 與非預力梁須拉力控制（§9.3.3.1）；RC-2015-2 說明改正）*
