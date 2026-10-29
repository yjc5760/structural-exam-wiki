# φ 折減係數（Resistance Factors）的來源

**Code-Ref ID：** phi-resistance-factors
**規範來源：** AISC 360 / LRFD 可靠度理論

---

## 一、LRFD 設計方程式

$$\phi R_n \geq \sum \gamma_i Q_i$$

- $R_n$ = 標稱強度（Nominal Resistance）
- $\phi$ = 強度折減係數（Resistance Factor）
- $Q_i$ = 名義載重效應（Nominal Load Effect）
- $\gamma_i$ = 載重放大係數（$\gamma_D = 1.2$，$\gamma_L = 1.6$）

$\phi$ 的作用是**向強度側**引入保守性，抵消材料、製造、施工的不確定性。

---

## 二、各 φ 值的對照

| 設計項目 | $\phi$ 值 | 對應 ASD 安全係數 $\Omega$ | 說明 |
|---------|---------|----------------------|------|
| **彎矩強度**（$\phi_b M_n$） | **0.90** | 1.67 | 延性破壞，變形明顯，不確定性較低 |
| **軸壓強度**（$\phi_c P_n$） | **0.85** | 1.76 | 挫屈，二階效應不確定性較高 |
| **拉力降伏**（$\phi_t P_n = \phi_t F_y A_g$） | **0.90** | 1.67 | 延性降伏，不確定性低 |
| **拉力斷裂**（$\phi_t P_n = \phi_t F_u A_e$） | **0.75** | 2.00 | 脆性斷裂，無警示，保守 |
| **剪力強度**（$\phi_v V_n$） | **0.90** | 1.67 | 降伏控制段，延性 |
| **連接軸向**（$\phi = 0.75$） | **0.75** | 2.00 | 螺栓/銲道，局部脆性 |
| **承壓**（$\phi_{bf} = 0.75$） | **0.75** | 2.00 | 局部/脆性型失效 |

---

## 三、φ 值的決定邏輯

**LRFD 可靠度理論：**

$$\phi = \exp\left(-\beta_{target} \cdot \alpha_R \cdot V_R\right)$$

其中：
- $\beta_{target}$ = 目標可靠度指標（AISC 取 $\beta = 3.0$ 為一般構件目標）
- $\alpha_R$ = 強度的靈敏度係數（≈ 0.55 for strength）
- $V_R$ = 強度的變異係數（Coefficient of Variation）

**直觀理解：**

| 破壞模式 | 為何 φ 小 |
|---------|---------|
| 挫屈（壓力，$\phi_c = 0.85$） | 挫屈載重對幾何不完美、殘留應力極敏感，不確定性高 |
| 脆性斷裂（拉力斷裂，$\phi_t = 0.75$） | 無塑性警告，斷裂突然；且 $F_u$ 的離散性比 $F_y$ 大 |
| 延性降伏（彎矩/剪力，$\phi = 0.90$） | 材料降伏前有明顯變形警告，不確定性相對低 |

---

## 四、$\phi$ 與 ASD 安全係數 $\Omega$ 的關係

$$\phi \approx \frac{1}{\Omega \cdot \alpha} \quad \text{其中 } \alpha = 1.0 \text{（LRFD）}, 1.6 \text{（ASD 直接分析法）}$$

更精確地：

$$\phi \times \Omega \approx \frac{\text{載重因數}}{1.0} \approx 1.5 \sim 1.6$$

例如彎矩：$\phi_b = 0.90$，$\Omega_b = 1.67$，$\phi_b \times \Omega_b = 0.90 \times 1.67 \approx 1.50$

---

## 五、考試常見問法

| 問法 | 要點 |
|------|------|
| 「$\phi_c = 0.85$ 而非 $0.90$？」 | 壓力挫屈的不確定性比彎矩降伏高 |
| 「$\phi = 0.75$ 用在哪裡？」 | 脆性破壞：拉力斷裂、螺栓剪斷、銲道、承壓 |
| 「$\phi$ 的物理意義」 | 將標稱強度折減，使設計強度代表某目標可靠度水準下的承載力 |
| 「LRFD 與 ASD 對 φ 的等價概念」 | $\Omega = 1/\phi$ 的比值關係，兩法在相同假設下應給出接近結果 |

## 相關頁面

- [[column-buckling-lambda-boundary]] — 為何 $\phi_c = 0.85$ 在挫屈設計中的應用
- [[lrfd-load-factors]] — 載重放大係數 1.2D + 1.6L 的來源
- [[lrfd-column]] — $\phi_c P_n$ 計算流程
