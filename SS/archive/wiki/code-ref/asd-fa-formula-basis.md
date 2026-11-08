# ASD 壓力桿件容許應力 Fa 公式推導

**Code-Ref ID：** asd-fa-formula-basis
**對應方法頁：** [[asd-column]]（`wiki/methods/asd-column.md`）
**前置推導：** [[asd-cc-basis]]（Cc 的來源）

---

## 一、公式全覽

ASD（AISC ASD 9th Edition）依細長比分兩段：

### 非彈性挫屈段（$KL/r \leq C_c$）

$$\boxed{F_a = \frac{\left[1 - \dfrac{(KL/r)^2}{2C_c^2}\right]F_y}{\text{FS}}}$$

$$\text{FS} = \frac{5}{3} + \frac{3(KL/r)}{8C_c} - \frac{(KL/r)^3}{8C_c^3}$$

### 彈性挫屈段（$KL/r > C_c$）

$$\boxed{F_a = \frac{12\pi^2 E}{23(KL/r)^2}}$$

---

## 二、非彈性段公式推導

### 步驟一：SSRC 柱強度基礎

CRC（Column Research Council）考慮殘留應力後，提出理想化柱強度公式：

$$\frac{F_{cr}}{F_y} = 1 - \frac{\lambda_c^2}{4}, \quad \lambda_c \leq \sqrt{2}$$

其中 $\lambda_c = \frac{KL}{r\pi}\sqrt{\frac{F_y}{E}}$（無因次細長比）

### 步驟二：換算為 ASD 形式

代入 $\lambda_c^2 = \frac{(KL/r)^2 F_y}{\pi^2 E}$ 及 $C_c^2 = \frac{2\pi^2 E}{F_y}$，得：

$$F_{cr} = F_y\left[1 - \frac{(KL/r)^2}{2C_c^2}\right]$$

此即非彈性段強度的名義值（無安全係數）。

### 步驟三：安全係數

ASD 規範採用**非均一安全係數**，在 $KL/r = 0$ 時 FS = 5/3（≈1.67），在 $KL/r = C_c$ 時 FS = 23/12（≈1.92）：

$$\text{FS} = \frac{5}{3} + \frac{3}{8}\frac{KL/r}{C_c} - \frac{1}{8}\left(\frac{KL/r}{C_c}\right)^3$$

**為何 FS 隨細長比增大？**

- 短柱（$KL/r \to 0$）：失效模式為材料強度，不確定性低 → FS = 1.67
- 中長柱（$KL/r \to C_c$）：挫屈特性更複雜，殘留應力與初始彎曲影響更顯著 → FS → 1.92
- 連續性：在 $KL/r = C_c$ 與彈性段 FS = 23/12 接續，確保無跳躍

### 步驟四：完整容許應力

$$F_a = \frac{F_{cr}}{\text{FS}} = \frac{\left[1 - \dfrac{(KL/r)^2}{2C_c^2}\right]F_y}{\dfrac{5}{3} + \dfrac{3(KL/r)}{8C_c} - \dfrac{(KL/r)^3}{8C_c^3}}$$

---

## 三、彈性段公式推導

### Euler 公式 + 固定安全係數

當 $KL/r > C_c$，全截面維持彈性，套用 Euler 挫屈公式：

$$F_e = \frac{\pi^2 E}{(KL/r)^2}$$

規範取 FS = 23/12（≈1.917）：

$$F_a = \frac{F_e}{\text{FS}} = \frac{\pi^2 E}{(KL/r)^2} \times \frac{12}{23} = \frac{12\pi^2 E}{23(KL/r)^2}$$

**為何固定 FS = 23/12？**

彈性段挫屈受幾何不完美控制，不確定性主要來自初始彎曲量，此不確定性與細長比關係較小，故採固定值。

---

## 四、ASD 與 LRFD 對照

| 項目 | ASD（9th Ed.） | LRFD（360-10） |
|------|--------------|--------------|
| 分界 | $KL/r = C_c$ | $\lambda_c = 1.5$ |
| 非彈性公式 | $F_a = F_{cr}/\text{FS}$，FS 非均一 | $\phi_c F_{cr} = 0.85 \times 0.658^{\lambda_c^2} F_y$ |
| 彈性公式 | $F_a = 12\pi^2E/[23(KL/r)^2]$ | $\phi_c F_{cr} = 0.85 \times 0.877/\lambda_c^2 \times F_y$ |
| 安全哲學 | 隱含於 FS 中 | 顯式 $\phi = 0.85$ |

> **記憶要點：** LRFD 的 $0.877/\lambda_c^2$ 即相當於 Euler 公式 × 0.877（考慮初始彎曲）；ASD 彈性段 12/23 ≈ 0.522，已包含初始彎曲的等效折減。

---

## 五、常見考題應用

| 題型 | 關鍵步驟 |
|------|---------|
| 計算柱容許軸力 | ① 算 KL/r → ② 比較 Cc → ③ 選公式算 Fa → ④ $P_a = F_a \times A_g$ |
| ASD vs LRFD 比較 | 轉換關係：$F_a \approx \phi F_{cr}/1.5$（近似） |
| 驗核細長比上限 | $KL/r \leq 200$（構材）；$KL/r \leq 300$（次要構材） |

---

## 相關頁面

- [[asd-cc-basis]] — Cc 的推導與物理意義
- [[asd-column]] — ASD 柱設計計算流程（含範例）
- [[column-buckling-lambda-boundary]] — LRFD λc = 1.5 分界推導
- [[EULER-BUCKLING]] — Euler 挫屈公式基礎
- [[RESIDUAL-STRESS]] — 殘留應力對柱強度影響
