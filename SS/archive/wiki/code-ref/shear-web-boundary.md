# 腹板剪力強度三段式邊界值的來源

**Code-Ref ID：** shear-web-boundary
**對應概念頁：** [[SHEAR-BUCKLING-WEB]]
**對應題型：** SS-U1-2 梁桿件剪力強度檢核

---

## 一、三段式結構

腹板剪力強度依 $h/t_w$ 分三段，物理機制各不同：

| 段 | 條件 | 物理機制 | $V_n$ |
|----|------|---------|-------|
| **全斷面降伏段** | $\dfrac{h}{t_w} \leq 1.10\sqrt{\dfrac{k_v E}{F_y}}$ | 腹板在剪力挫屈前全面降伏 | $0.6 F_y A_w$ |
| **非彈性挫屈段** | $1.10 < \dfrac{h/t_w}{\sqrt{k_v E/F_y}} \leq 1.37$ | 腹板已局部降伏但未完全彈性挫屈 | $0.6 F_y A_w \cdot \dfrac{1.10\sqrt{k_v E/F_y}}{h/t_w}$ |
| **彈性挫屈段** | $\dfrac{h}{t_w} > 1.37\sqrt{\dfrac{k_v E}{F_y}}$ | 腹板在彈性範圍內發生剪力挫屈 | $\dfrac{0.9 k_v E}{(h/t_w)^2} A_w$ |

---

## 二、邊界值 1.10 和 1.37 的來源

### 邊界值 1.10√(kv E/Fy) — 全面降伏上限

板件純剪情況下的降伏條件：

$$\tau_{cr} = \tau_y = \frac{F_y}{\sqrt{3}} \approx 0.577 F_y$$

腹板純剪彈性挫屈臨界應力（對有加勁板的腹板）：

$$\tau_{cr} = k_v \frac{\pi^2 E}{12(1-\nu^2)} \cdot \frac{1}{(h/t_w)^2} \approx \frac{k_v E \pi^2}{10.9 (h/t_w)^2}$$

令 $\tau_{cr} = \tau_y$（剪力挫屈恰好在降伏點發生）：

$$\frac{k_v E}{(h/t_w)^2} \approx F_y \quad \Rightarrow \quad \frac{h}{t_w} = \sqrt{\frac{k_v E}{F_y}}$$

規範乘以約 1.10 的修正係數（考慮應力分布不均、端部支承效應等），得到：

$$\left(\frac{h}{t_w}\right)_{yld} = 1.10\sqrt{\frac{k_v E}{F_y}}$$

**台灣規範（tf/cm²）的等價表達：**
- 無加勁板（$k_v = 5.0$）：$\leq 50\sqrt{k_v/F_y}$（係數 50 對應 1.10√(E=2040/Fy)）
- 有加勁板（$k_v > 5$）：按實際 $k_v$ 計算

### 邊界值 1.37√(kv E/Fy) — 非彈性/彈性挫屈分界

取「剛好開始彈性挫屈」的位置為：

$$\left(\frac{h}{t_w}\right)_{elastic} = 1.37\sqrt{\frac{k_v E}{F_y}}$$

推導邏輯：在彈性挫屈段，$V_n$ 正比於 $1/(h/t_w)^2$；在全面降伏段，$V_n$ 是常數。兩者的交接使得在 1.10～1.37 之間線性過渡（保守）。

---

## 三、各段 Vn 公式的物理意義

### 全面降伏段：$V_n = 0.6 F_y A_w$

**來源：** 最大剪力應力 $\tau_{max} = V/A_w$（均勻化假設），降伏條件 $\tau_{max} = F_y/\sqrt{3} \approx 0.577 F_y$。

規範取 $0.6 F_y$ 而非 $0.577 F_y$，是**稍微偏保守的取整**：

$$\phi_v V_n = 0.9 \times 0.6 F_y A_w = 0.54 F_y A_w$$

### 非彈性挫屈段：線性折減

$$V_n = 0.6 F_y A_w \cdot \frac{C_v}{1} \quad \text{其中}\quad C_v = \frac{1.10\sqrt{k_v E/F_y}}{h/t_w}$$

$C_v$（剪力係數）在 1.10 分界點 = 1.0（與全面降伏接軌），隨 $h/t_w$ 增大線性下降。

### 彈性挫屈段：$V_n \propto 1/(h/t_w)^2$

$$V_n = \frac{0.9 k_v E}{(h/t_w)^2} A_w$$

這就是彈性板件剪力挫屈公式，直接從彈性板件理論推導。

---

## 四、$k_v$ 腹板剪力挫屈係數

| 條件 | $k_v$ 值 |
|------|---------|
| 無加勁板（或 $a/h > 3$） | **5.0**（最常考） |
| 有加勁板，$a/h \leq 1$ | $5.34 + 4/(a/h)^2$ |
| 有加勁板，$a/h > 1$ | $4 + 5.34/(a/h)^2$ |
| 端部加勁板 | 另有規定 |

**物理意義：** $k_v$ 越大，代表加勁板提供更多邊界束制，腹板抵抗剪力挫屈的能力越強（$V_{cr}$ 正比 $k_v$）。

---

## 五、台灣規範數值（LRFD，$F_y$ 單位 tf/cm²）

| 段 | 條件（無加勁板 $k_v = 5$） | $V_n$ |
|----|------------------------|-------|
| 降伏 | $h/t_w \leq 50\sqrt{k_v/F_y}$ | $0.6 F_y A_w$ |
| 非彈性 | $50\sqrt{k_v/F_y} < h/t_w \leq 62\sqrt{k_v/F_y}$ | $0.6 F_y A_w \cdot \dfrac{50\sqrt{k_v/F_y}}{h/t_w}$ |
| 彈性 | $h/t_w > 62\sqrt{k_v/F_y}$ | $\dfrac{1860 k_v}{(h/t_w)^2} A_w$ |

係數對應關係：$50 \approx 1.10\sqrt{2040}$，$62 \approx 1.37\sqrt{2040}$。

---

## 六、$A_w$ 的定義

$$A_w = d \times t_w$$

其中 $d$ = 梁**全深**（而非清淨高度 $h$）。

> ⚠️ 台灣規範 $A_w = d \times t_w$（包含翼板區），而非 $h_w \times t_w$（腹板清淨高度 × 腹板厚）。考試中常見陷阱。

## 相關頁面

- [[SHEAR-BUCKLING-WEB]] — 腹板剪力挫屈概念
- [[PLATE-GIRDER-DESIGN]] — 板梁：$h/t_w > 260$ 時的板梁設計
- [[TENSION-FIELD-ACTION]] — 張力場效應：可超過彈性挫屈後繼續承載
