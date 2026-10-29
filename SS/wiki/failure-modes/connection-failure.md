# 接合失敗模式

> **核心問題：** 接合處是整體鏈中最薄弱的一環，且通常是脆性失敗。設計原則：接合強度 ≥ 構材強度。

---

## 接合失敗的設計哲學

**「強接合弱構材」原則**（Capacity Design of Connections）：

```
失敗序列（設計目標）：
    構材降伏（延性，可接受）
        ↓
    接合保持完整（強度不折減）
        ↓ 避免
    接合先行破壞（脆性，不可接受）
```

耐震設計更嚴格：接合需能承受構材**超強後**的最大力量（× Ry 或 × 1.25）。

---

## 螺栓接合失敗模式

### 四種失敗模式

| 序號 | 失敗模式 | 英文 | φRn 計算 |
|------|---------|------|---------|
| ① | 螺栓剪斷 | Bolt Shear Fracture | $\phi R_n = \phi \cdot F_{nv} \cdot A_b$ |
| ② | 螺栓承壓（板件） | Bearing | $\phi R_n = \phi \cdot 2.4 F_u d t$ |
| ③ | 淨截面斷裂 | Net Section Fracture | $\phi P_n = 0.75 F_u A_e$ |
| ④ | 塊狀剪力 | Block Shear | $\phi R_n = \phi (0.6F_u A_{nv} + U_{bs} F_u A_{nt})$ |

**控制模式** = 四者中最小值。

### 各模式說明

#### ① 螺栓剪斷

$$\phi R_n = \phi \cdot F_{nv} \cdot A_b \cdot n_s$$

- $F_{nv}$：螺栓標稱剪力強度（A325: 330 MPa；A490: 414 MPa）
- $A_b$：螺栓標稱面積
- $n_s$：剪力面數（單剪 = 1；雙剪 = 2）
- $\phi = 0.75$

| 螺栓 | 承壓型 Fnv | 摩阻型（滑動強度） |
|------|-----------|-------------|
| A325 | 330 MPa（單剪）、414 MPa（雙剪） | 依接觸面狀況 |
| A490 | 414 MPa（單剪）、517 MPa（雙剪） | 依接觸面狀況 |

#### ② 承壓破壞

$$\phi R_n = \phi \cdot 2.4 F_u d t \quad (\phi = 0.75)$$

- 適用條件：邊距 $L_c \geq 1.5d$，螺栓間距 $s \geq 3d$
- 近邊螺栓（邊距不足）：$\phi R_n = \phi \cdot 1.2 F_u L_c t$

#### ③ 淨截面斷裂

$$\phi P_n = 0.75 F_u A_e, \quad A_e = U \cdot A_n$$

- 剪力遲滯 U < 1.0（非全斷面連接時）
- Method: [[shear-lag-u]]

#### ④ 塊狀剪力

$$\phi R_n = 0.75 \min \begin{cases} 0.6F_u A_{nv} + U_{bs} F_u A_{nt} \\ 0.6F_y A_{gv} + U_{bs} F_u A_{nt} \end{cases}$$

- Method: [[block-shear]]

---

## 摩阻型螺栓失敗（Slip-Critical）

摩阻型螺栓有**兩種失敗狀態**：

| 狀態 | 失敗定義 | φ | 用途 |
|------|---------|---|------|
| SLS 滑動 | 接觸面滑動（功能失效） | 1.0 | 反覆載重、精密接合 |
| ULS 強度 | 螺栓剪斷（如承壓型） | 0.75 | 最終破壞 |

**SLS 滑動設計強度：**

$$\phi R_n = \phi \mu D_u h_{sc} P_t n_s$$

- $\mu$：摩擦係數（A級：0.35；B級：0.50）
- $D_u$：1.13
- $h_{sc}$：1.0（標準孔）；0.85（超大孔）
- $P_t$：預拉力（A325: 142 kN；A490: 179 kN，20mm螺栓）

---

## 銲縫接合失敗模式

### 三種失敗模式

| 序號 | 失敗模式 | 發生位置 | φRn 計算 |
|------|---------|---------|---------|
| ① | 銲喉剪斷 | 銲縫有效喉深 | $\phi \cdot 0.6F_{EXX} \cdot 0.707w \cdot L$ |
| ② | 母材剪斷 | 熔合線附近母材 | $\phi \cdot 0.6F_u \cdot A_{BM}$ |
| ③ | 熱影響區脆裂 | HAZ | 材料韌性不足時 |

**控制模式** = 銲喉強度與母材強度的較小值。

### 填角銲（Fillet Weld）強度

$$\phi R_n = 0.75 \times 0.6 F_{EXX} \times (0.707w) \times L$$

- $F_{EXX}$：銲條強度（E70XX: 490 MPa = 49 tf/cm²）
- $w$：銲腳尺寸
- $0.707w$：有效喉深（45° 填角銲）
- ASD：$R_n = 0.3 F_{EXX} \times 0.707w \times L$

### 開槽銲（Groove Weld）強度

| 類型 | 適用 | φRn |
|------|------|-----|
| CJP（完全滲透） | 完全連接 | 母材控制：$\phi F_u A_{BM}$ |
| PJP（部分滲透） | 壓力連接 | $0.75 \times 0.6F_{EXX} \times A_{eff}$ |

### 偏心銲縫（Eccentric Weld）

$$f_{resultant} = \sqrt{f_d^2 + f_M^2 + 2 f_d f_M \cos\theta}$$

- Method: [[eccentric-weld]]（銲縫線圖法）
- $I_p$（線圖）：單位 cm³（非 cm⁴）—— **常見錯誤**

---

## 接合設計快速檢查流程

### 螺栓接合（直接剪力）

```
① 所需螺栓數 n = V / φRn,bolt
② 驗核承壓：φRn,bearing ≥ 每根螺栓實際力
③ 驗核淨截面：φPn = 0.75FuAe ≥ Pu
④ 驗核塊狀剪力：φRn,block ≥ Pu
⑤ 驗核間距與端距（規範施工規定）
```

### 銲縫接合（直接剪力）

```
① 需求銲道長度 L = V / (φ × 0.6FEXX × 0.707w)
② 驗核母材剪斷
③ 最小銲腳 w_min（依板厚查表）
④ 最大銲腳 w_max = t - 1/16 in（翼板邊緣）
```

---

## 接合施工規定（概念題高頻）

### 螺栓施工規定

| 規定項目 | 數值 |
|---------|------|
| 最小螺栓間距 | 2.67d（建議 3d） |
| 最小邊距 | 1.5d（建議 1.75d） |
| 最大邊距 | 12t 或 150 mm |
| 最大間距（拉力） | 24t 或 300 mm |
| 預拉力（A325, d=20mm） | 142 kN |

### 銲接施工規定

| 規定項目 | 數值 |
|---------|------|
| 最小填角銲尺寸 | 依板厚：t≤6mm → 3mm；t≤12mm → 5mm |
| 最大填角銲尺寸（板緣） | t - 1/16 in（≥ 6mm 板） |
| 最小銲道長度 | 4w 或 38mm |
| CJP 銲接後熱 | 需 NDT 檢測（UT 或 RT） |

---

## 常見陷阱

- **偏心銲縫 Ip 用線圖（cm³）**，不是面積慣性矩（cm⁴）
- **填角銲有效喉深 = 0.707w**，不是 w
- **摩阻型 φ = 1.0（SLS滑動）or 0.75（ULS強度）** 是兩種不同狀態
- **CJP 開槽銲強度由母材控制**，不由銲條控制
- **塊狀剪力 Ubs = 1.0（均勻拉力）**，L 型角鋼連接用 0.5

---

## 相關頁面

- [[strength-failure]] — 構材強度失敗（塊狀剪力是強度也是接合）
- [[stability-failure]] — 板件局部挫屈（影響接合板）
- Concepts: [[WELDED-CONNECTION-DESIGN]] [[BOLTED-CONNECTION-DESIGN]] [[SLIP-CRITICAL-CONNECTION]] [[BLOCK-SHEAR-RUPTURE]]
- Methods: [[eccentric-bolt]] [[eccentric-weld]] [[block-shear]] [[shear-lag-u]]
- Diagnosis: [[connection]]
