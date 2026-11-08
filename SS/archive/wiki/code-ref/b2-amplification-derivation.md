# B2 放大係數分母「1 - ΣPu/ΣPe2」的來源

**Code-Ref ID：** b2-amplification-derivation
**規範來源：** AISC 360 Appendix 8 / Chapter C
**對應概念頁：** [[SECOND-ORDER-ANALYSIS]]
**對應方法頁：** [[b1b2-amplification]]

---

## 一、問題背景

AISC 360 B2 放大係數用於放大側移引起的彎矩（$M_{lt}$）：

$$B_2 = \frac{1}{1 - \frac{\sum P_u}{\sum P_{e2}}} \geq 1.0$$

考試常直接問：「分母 $1 - \sum P_u / \sum P_{e2}$ 是怎麼推導出來的？」

---

## 二、推導

### 物理模型：單層側移構架

考慮一個側移構架，在水平力 $H$ 作用下產生側移 $\Delta$。樓層內各柱的軸力合計為 $\sum P_u$。

### 虛功原理推導

設樓層側移為 $\Delta$，水平力 $H$ 引起的初始側移為 $\Delta_0$：

**一階側移（無 P-Δ）：**
$$\Delta_0 = \frac{H \cdot L}{\sum (\text{層剪力剛度})}$$

**P-Δ 效應的附加水平力等效：**

側移 $\Delta$ 使樓層的軸力 $\sum P_u$ 產生等效水平力：

$$H_{P\Delta} = \frac{\sum P_u \cdot \Delta}{L}$$

**迭代收斂（幾何級數）：**

$$\Delta = \Delta_0 + \frac{\sum P_u}{P_{e2,\text{story}}} \Delta_0 + \left(\frac{\sum P_u}{P_{e2,\text{story}}}\right)^2 \Delta_0 + \cdots$$

其中 $P_{e2,\text{story}} = \sum P_{e2}$ 是整層的彈性側移挫屈載重。

幾何級數求和：

$$\Delta = \frac{\Delta_0}{1 - \dfrac{\sum P_u}{\sum P_{e2}}}$$

### 從側移到彎矩放大

因為彎矩與側移成正比：

$$M_{2nd} = \frac{M_{1st}}{1 - \dfrac{\sum P_u}{\sum P_{e2}}} = B_2 \cdot M_{lt}$$

$$\boxed{B_2 = \frac{1}{1 - \dfrac{\sum P_u}{\sum P_{e2}}}}$$

---

## 三、ΣPe2 的計算

$$\sum P_{e2} = R_M \frac{\sum H \cdot L}{\Delta_H}$$

其中：
- $R_M$：側移剛度修正係數（純框架 = 1.0；有剪力牆 = 0.85）
- $\sum H$：樓層總水平力
- $\Delta_H$：對應的樓層側移
- $L$：樓層高度

---

## 四、物理意義

$\sum P_u / \sum P_{e2}$ 是「二階效應嚴重程度指標」：
- 趨近 0 → 側移構架很穩，$B_2 \approx 1$，二階效應可忽略
- 趨近 1 → 接近側移挫屈，$B_2 \to \infty$（不穩定）
- AISC 360 規定 $\sum P_u / \sum P_{e2} \leq 0.6$（即 $B_2 \leq 2.5$）

---

## 五、常見考試問法

| 問法 | 要點 |
|------|------|
| 「B2 公式分母是怎麼來的」 | 側移構架 P-Δ 迭代幾何級數收斂，等比級數求和得到 1/(1-Pu/Pe2) |
| 「ΣPe2 是什麼」 | 整層的彈性側移挫屈載重，由 ΣH·L/ΔH 計算（非單柱 Pe） |
| 「B2 與 B1 的差別」 | B1 放大 Mnt（無側移彎矩，P-δ 效應）；B2 放大 Mlt（側移彎矩，P-Δ 效應） |
| 「B2 ≥ 1 的意義」 | 側移只會讓彎矩增大，不會減小，故 B2 下限為 1.0 |

---

## 相關頁面

- [[SECOND-ORDER-ANALYSIS]] — 二階分析概念
- [[b1b2-amplification]] — B1/B2 完整計算方法（方法頁）
- [[b1-amplification-derivation]] — B1 推導（P-δ 效應）
- [[MOMENT-AMPLIFICATION-B1-B2]] — B1/B2 概念頁
