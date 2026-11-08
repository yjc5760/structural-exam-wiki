# 規範條文對應層 — 鋼結構設計規範索引

> **核心功能：** 從設計公式反查規範來源，或從規範章節快速找到對應知識點。

---

## 規範體系說明

台灣鋼結構技師考試主要援引以下規範：

| 規範 | 全名 | 核心用途 |
|------|------|---------|
| **AISC 360** | Specification for Structural Steel Buildings | 主要設計規範（LRFD/ASD） |
| **AISC 341** | Seismic Provisions for Structural Steel Buildings | 耐震設計 |
| **AWS D1.1** | Structural Welding Code—Steel | 銲接規範 |
| **台灣鋼構規範** | 鋼構造建築物鋼結構設計技術規範 | 台灣版 AISC 改編 |
| **建築技術規則** | 建築技術規則結構篇 | 法規層級，載重、地震區劃 |

---

## 章節 × 知識點對應矩陣

### AISC 360（設計規範）章節

| 章節 | 主題 | 對應 Method/Concept |
|------|------|-------------------|
| **Chapter B** | 設計要求（LRFD vs ASD, 結實斷面） | [[lrfd-phi-values]] |
| **Chapter C** | 二階效應（B1-B2 放大法） | [[b1b2-amplification]] [[MOMENT-AMPLIFICATION-B1-B2]] [[b1-m1m2-sign-convention]] [[b1-amplification-derivation]] |
| **Chapter D** | 拉力桿件 | [[shear-lag-u]] [[block-shear]] [[EFFECTIVE-NET-AREA]] |
| **Chapter E** | 壓力桿件（柱挫曲） | [[lrfd-column]] [[effective-length-chart]] [[EULER-BUCKLING]] [[column-buckling-lambda-boundary]] |
| **Chapter F** | 梁桿件（撓曲） | [[ltb-3zone]] [[LATERAL-TORSIONAL-BUCKLING]] [[LATERAL-TORSIONAL-BUCKLING]] |
| **Chapter G** | 剪力強度（含腹板挫屈） | [[SHEAR-BUCKLING-WEB]] [[PLATE-GIRDER-DESIGN]] |
| **Chapter H** | 梁柱桿件（P-M 互制） | [[pm-interaction]] [[BEAM-COLUMN-INTERACTION]] [[pm-interaction-physical-meaning]] |
- [[b2-amplification-derivation]] — B2 放大係數分母推導：P-Δ 迭代幾何級數→1/(1-ΣPu/ΣPe2)
| **Chapter I** | 組合構材 | [[COMPOSITE-BEAM]] [[COMPOSITE-COLUMN]] |
| **Chapter J** | 接合設計 | [[eccentric-bolt]] [[eccentric-weld]] [[BOLTED-CONNECTION-DESIGN]] [[WELDED-CONNECTION-DESIGN]] |
| **Chapter K** | 管形構材接合（HSS） | （較少出題） |

### AISC 341（耐震規定）章節

| 章節 | 主題 | 對應 Concept |
|------|------|------------|
| **Chapter D** | 一般耐震規定（Ry, ductility） | [[CAPACITY-DESIGN]] [[SEISMIC-STEEL-SN]] |
| **Chapter E** | SMRF（特殊彎矩抵抗框架） | [[STRONG-COLUMN-WEAK-BEAM]] [[PANEL-ZONE]] |
| **Chapter F** | 偏心斜撐框架（EBF） | [[SEISMIC-DESIGN-PHILOSOPHY]] |
| **Chapter G** | 中心斜撐框架（CBF） | [[SEISMIC-DESIGN-PHILOSOPHY]] |

---

## 高頻考點的規範公式對應

### 拉力桿件（Chapter D）

| 失敗模式 | LRFD 設計強度 | ASD 容許強度 |
|---------|------------|-----------|
| 毛斷面降伏 | $\phi_t P_n = 0.90 F_y A_g$ | $P_n/\Omega_t = F_y A_g / 1.67$ |
| 淨斷面斷裂 | $\phi_t P_n = 0.75 F_u A_e$ | $P_n/\Omega_t = F_u A_e / 2.00$ |
| 塊狀剪力 | $\phi R_n = 0.75 R_n$ | $R_n/\Omega = R_n / 2.00$ |

→ 詳見 [[tension-member]]（診斷）、[[block-shear]]（方法）

### 壓力桿件（Chapter E）

| 細長比 | Fcr 公式 |
|--------|---------|
| $\lambda_c = \frac{KL}{r\pi}\sqrt{F_y/E} \leq 1.5$ | $F_{cr} = 0.658^{\lambda_c^2} F_y$ |
| $\lambda_c > 1.5$ | $F_{cr} = \frac{0.877}{\lambda_c^2} F_y$ |

$$\phi_c P_n = 0.85 F_{cr} A_g$$

→ 詳見 [[compression-member]]（診斷）、[[lrfd-column]]（方法）

### 梁桿件（Chapter F）

| 區段 | 條件 | Mn |
|------|------|-----|
| 塑性 | $L_b \leq L_p$ | $M_p = F_y Z_x$ |
| 非彈性 LTB | $L_p < L_b \leq L_r$ | 線性內插 |
| 彈性 LTB | $L_b > L_r$ | $F_{cr} S_x \leq M_p$ |

$$\phi_b M_n = 0.90 M_n$$

→ 詳見 [[beam]]（診斷）、[[ltb-3zone]]（方法）

### 梁柱桿件（Chapter H）

H1-1a（$P_r/P_c \geq 0.2$）：
$$\frac{P_r}{P_c} + \frac{8}{9}\left(\frac{M_{rx}}{M_{cx}} + \frac{M_{ry}}{M_{cy}}\right) \leq 1.0$$

H1-1b（$P_r/P_c < 0.2$）：
$$\frac{P_r}{2P_c} + \left(\frac{M_{rx}}{M_{cx}} + \frac{M_{ry}}{M_{cy}}\right) \leq 1.0$$

→ 詳見 [[beam-column]]（診斷）、[[pm-interaction]]（方法）

### 接合設計（Chapter J）

| 接合型式 | 設計強度 | 規範 |
|---------|---------|------|
| 填角銲（LRFD） | $0.75 \times 0.6F_{EXX} \times 0.707w$ | J2.4 |
| 填角銲（ASD） | $0.30F_{EXX} \times 0.707w$ | J2.4 |
| 螺栓剪力 | $0.75 F_{nv} A_b$ | J3.6 |
| 螺栓承壓 | $0.75 \times 2.4 F_u d t$ | J3.10 |

→ 詳見 [[connection]]（診斷）、[[eccentric-bolt]]、[[eccentric-weld]]（方法）

---

## 施工規定速查（高頻填空）

### 螺栓施工規定（Chapter J, Section J3）

| 規定項目 | 數值 |
|---------|------|
| 最小螺栓間距 | 2.67d（建議 3d） |
| 最小邊距 | 依板厚與螺栓直徑查表（最小 1.25d） |
| 最大邊距（受力） | 12t 或 150mm（取小） |
| 預拉力 A325 | 依螺栓直徑查表（20mm：142 kN） |
| 預拉力 A490 | 依螺栓直徑查表（20mm：179 kN） |

### 銲接施工規定（AWS D1.1 / Chapter J）

| 規定項目 | 數值 |
|---------|------|
| 最小填角銲腳 | 依較厚板厚查表 |
| 最大填角銲腳（板緣） | t - 1/16"（t ≥ 1/4"） |
| 最小銲道長度 | 4w 或 1.5" |
| CJP 開槽銲 NDT | UT 或 RT |

→ 詳見 [[weldability]]、[[HIGH-STRENGTH-BOLT-PRACTICE]]、[[WELDING-PRACTICE]]

---

## ASD vs. LRFD 安全係數對應

| 失敗模式 | LRFD φ | ASD Ω | φ × Ω 乘積 |
|---------|--------|--------|-----------|
| 降伏 | 0.90 | 1.67 | 1.503 |
| 挫屈（壓） | 0.85 | 1.765 | 1.500 |
| 斷裂 | 0.75 | 2.00 | 1.500 |
| 接合 | 0.75 | 2.00 | 1.500 |
| 銲縫剪力 | 0.75 | 2.00 | 1.500 |

→ 注意：φ × Ω ≈ 1.5，這是 AISC 設計的一致性

→ 詳見 [[lrfd-phi-values]]（哲學）

---

## 耐震規定速查（AISC 341）

| 規定 | 數值/公式 | 章節 |
|------|---------|------|
| 強柱弱梁 | $\Sigma \phi_c M_{pc} \geq \Sigma \phi_b M_{pb}$ | E3 |
| Mpc 折減 | $M_{pc} = Z_x(F_y - P_u/A_g)$ | E3 |
| Panel Zone 厚度 | $t_z \geq (d_z + w_z)/90$（cm 單位） | E3.6 |
| 超強係數 Ry | A992: 1.1；A36: 1.5 | A3.2 |
| 梁端塑性轉角要求 | ≥ 0.03 rad（SMRF） | E2.6 |

→ 詳見 [[seismic]]（診斷）

---

## 快速索引

- [[tension-member]] — 拉力桿件（Chapter D）
- [[compression-member]] — 壓力桿件（Chapter E）
- [[beam]] — 梁桿件（Chapter F）
- [[beam-column]] — 梁柱桿件（Chapter H）
- [[connection]] — 接合設計（Chapter J）
- [[seismic]] — 耐震規定（AISC 341）
- [[lrfd-phi-values]] — 設計哲學（Chapter B）
## 推導頁目錄（code-ref/ 完整列表）

### 原有推導頁
- [[b1-m1m2-sign-convention]] — B1 放大係數：M1/M2 符號規則（單曲率=負、雙曲率=正）
- [[b1-amplification-derivation]] — B1 放大係數完整推導：Pe1物理意義、Dm微分方程推導、Cm由來
- [[column-buckling-lambda-boundary]] — λ_c = 1.5 分界點：0.658^λc² 與 0.877/λc² 推導
- [[pm-interaction-physical-meaning]] — P-M 互制 H1-1 物理意義：8/9 係數、0.2 門檻、幾何解讀

### 本次新增推導頁
- [[asd-cc-basis]] — ASD 柱臨界細長比 Cc 推導：Euler 分界 + 殘留應力修正
- [[asd-1.6-coefficient]] — ASD 1.6 折減係數：組合載重與 LRFD 等效換算
- [[b2-amplification-derivation]] — B2 放大係數分母推導：P-Δ 迭代幾何級數→1/(1-ΣPu/ΣPe2)

### ASD 容許應力推導頁（新增）
- [[asd-fa-formula-basis]] — ASD 壓力桿件 Fa 公式推導：非彈性拋物線 + 彈性 Euler 段 + 非均一 FS
- [[asd-beam-fb-derivation]] — ASD 梁容許彎曲應力 Fb 推導：三段 LTB + rT 物理意義 + Cb 應用

### 其他推導頁
- [[block-shear-formula-basis]] — 塊狀剪力公式的來源
- [[cb-formula-derivation]] — Cb 彎矩梯度係數的來源
- [[fillet-weld-0707]] — 填角銲有效厚度 0.707w 的來源
- [[lrfd-load-factors]] — LRFD 載重係數 1.2D + 1.6L 的來源
- [[ltb-lp-lr-derivation]] — LTB 邊界長度 Lp / Lr 的來源
- [[phi-resistance-factors]] — φ 折減係數（Resistance Factors）的來源
- [[seismic-ry-factor]] — 耐震超強係數 Ry 的來源
- [[shear-lag-u-basis]] — 剪力遲滯 U 值公式的來源
- [[shear-web-boundary]] — 腹板剪力強度三段式邊界值的來源
### 其他推導頁
- [[block-shear-formula-basis]] — 塊狀剪力公式的來源
- [[cb-formula-derivation]] — Cb 彎矩梯度係數的來源
- [[fillet-weld-0707]] — 填角銲有效厚度 0.707w 的來源
- [[lrfd-load-factors]] — LRFD 載重係數 1.2D + 1.6L 的來源
- [[ltb-lp-lr-derivation]] — LTB 邊界長度 Lp / Lr 的來源
- [[phi-resistance-factors]] — φ 折減係數（Resistance Factors）的來源
- [[seismic-ry-factor]] — 耐震超強係數 Ry 的來源
- [[shear-lag-u-basis]] — 剪力遲滯 U 值公式的來源
- [[shear-web-boundary]] — 腹板剪力強度三段式邊界值的來源
