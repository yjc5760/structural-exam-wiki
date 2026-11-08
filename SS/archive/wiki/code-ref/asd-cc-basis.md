# ASD 柱設計臨界細長比 Cc 的來源

**Code-Ref ID：** asd-cc-basis
**對應方法頁：** [[asd-column]]（`wiki/methods/asd-column.md`）

---

## 一、Cc 的定義

$$\boxed{C_c = \sqrt{\frac{2\pi^2 E}{F_y}}}$$

$C_c$ 是 ASD 柱設計中**非彈性挫屈 / 彈性挫屈的分界細長比**。

---

## 二、推導

ASD 柱設計以「Euler 彈性挫屈應力 = 降伏強度」作為分界：

$$F_e = F_y \quad \Rightarrow \quad \frac{\pi^2 E}{(KL/r)^2} = F_y$$

解出分界細長比：

$$\left(\frac{KL}{r}\right)^2 = \frac{\pi^2 E}{F_y} \quad \Rightarrow \quad \frac{KL}{r} = \pi\sqrt{\frac{E}{F_y}}$$

**ASD 規範（AISC ASD 9th Ed.）取 2 倍安全考量（考慮殘留應力等因素），定義 $C_c$ 為：**

$$C_c = \sqrt{\frac{2\pi^2 E}{F_y}}$$

即：$C_c = \sqrt{2} \times \pi\sqrt{\frac{E}{F_y}} \approx \sqrt{2} \times \frac{KL}{r}\big|_{F_e = F_y}$

---

## 三、$C_c$ 的物理意義

| 條件 | 物理意義 |
|------|---------|
| $KL/r \leq C_c$ | 非彈性挫屈段：細長比不太大，Euler 公式不適用（已有殘留應力效應） |
| $KL/r > C_c$ | 彈性挫屈段：細長比大，Euler 公式適用（全截面尚在彈性） |

> ⚠️ **重要：$C_c$ ≠ 最大容許細長比（200）**。  
> $C_c$ 是「設計段落分界」，最大容許細長比（$KL/r \leq 200$）是另一個限制。

---

## 四、常用數值

| 鋼材 | $F_y$（tf/cm²） | $C_c$ | $F_y$（ksi） |
|------|---------------|-------|------------|
| A36 | 2.52 | ≈ 126 | 36 ksi |
| A572 Gr.50 | 3.52 | ≈ 107 | 50 ksi |
| A572 Gr.60 | 4.22 | ≈ 97 | 60 ksi |

$C_c$ 對應公式：$C_c = \sqrt{2\pi^2 \times 2040/F_y}$ (tf/cm² 系統)

---

## 五、ASD 容許應力公式的推導邏輯

### 非彈性段（$KL/r \leq C_c$）

SSRC 柱強度曲線的 ASD 近似：

$$F_a = \frac{\left[1 - \dfrac{(KL/r)^2}{2C_c^2}\right]F_y}{\text{FS}}$$

括號中的 $1 - (KL/r)^2/(2C_c^2)$ 是 Rankine-Gordon 公式的近似，反映殘留應力影響。

安全係數（隨細長比變化，1.67 → 1.92）：
$$\text{FS} = \frac{5}{3} + \frac{3(KL/r)}{8C_c} - \frac{(KL/r)^3}{8C_c^3}$$

**為何 FS 不是常數？** 非彈性挫屈段，不完美和殘留應力的影響隨細長比增大而增大，安全係數也相應提高。

### 彈性段（$KL/r > C_c$）

直接套 Euler 公式，但加保守安全係數 23/12（≈1.92）：

$$F_a = \frac{12\pi^2 E}{23(KL/r)^2}$$

（$12/23 = 1/1.917$，對應 FS = 23/12）

---

## 六、LRFD 對應

| ASD | LRFD |
|-----|------|
| $KL/r \leq C_c$（非彈性） | $\lambda_c \leq 1.5$（非彈性） |
| $KL/r > C_c$（彈性） | $\lambda_c > 1.5$（彈性） |
| $F_a$ | $\phi_c F_{cr}$ |

$C_c$ 與 LRFD 的 $\lambda_c = 1.5$ 分界相對應（見 [[column-buckling-lambda-boundary]]）。

## 相關頁面

- [[asd-column]] — ASD 柱設計計算流程
- [[column-buckling-lambda-boundary]] — LRFD 版本 λc = 1.5 的來源
- [[RESIDUAL-STRESS]] — 殘留應力對非彈性挫屈的影響
