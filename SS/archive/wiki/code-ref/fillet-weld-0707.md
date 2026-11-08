# 填角銲有效厚度 0.707w 的來源

**Code-Ref ID：** fillet-weld-0707
**對應概念頁：** [[WELDED-CONNECTION-DESIGN]]

---

## 一、填角銲幾何

填角銲（Fillet Weld）的截面為等腰直角三角形：

```
    ←── w ──→
    ┌─────────┐ ← 翼板（被銲件）
    │  ╲      │
    │    ╲    │ ← 腹板（被銲件）
    │      ╲  │
    └─────────┘
          ↑
       銲腳尺寸 w（兩腳相等）
```

**銲喉（Throat，有效厚度）= 最薄弱截面**

破壞時，填角銲沿**最小截面**（45° 對角線方向的喉部）剪斷：

$$t_e = \text{有效喉厚} = w \times \cos 45° = w \times \frac{\sqrt{2}}{2} = 0.707\, w$$

---

## 二、幾何推導

等腰直角三角形，兩腰長各為 $w$：

$$t_e = \frac{w}{\sqrt{2}} = \frac{w \times \sqrt{2}}{2} = 0.707\, w$$

精確值：$\cos 45° = \sin 45° = 1/\sqrt{2} \approx 0.7071$

規範取 **0.707**（精確到三位有效數字）。

---

## 三、填角銲強度公式

$$R_n = 0.6 F_{EXX} \times t_e \times L_w = 0.6 F_{EXX} \times 0.707w \times L_w$$

$$\phi R_n = 0.75 \times 0.6 F_{EXX} \times 0.707w \times L_w$$

其中：
- $F_{EXX}$ = 銲材分類強度（如 E70XX → $F_{EXX} = 70$ ksi = 4.92 tf/cm²）
- $w$ = 銲腳尺寸（Weld Leg Size）
- $L_w$ = 有效銲縫長度

**台灣規範（kN-cm 系統，E70XX）常用簡化：**

$$\phi R_n \approx 0.75 \times 0.6 \times 4.92 \times 0.707 \times w \times L$$
$$\approx 1.565\, w\, L \quad \text{[tf/cm]}$$

---

## 四、0.6FEXX 的來源

**銲材的剪切強度取 $\tau_u = 0.6 F_{EXX}$**，與板件剪切強度 $0.6F_u$ 的邏輯一致：

$$\tau_{rupture} = \frac{F_{EXX}}{\sqrt{3}} \approx 0.577 F_{EXX} \approx 0.6 F_{EXX}$$

（Von Mises 條件，取整為 0.6）

---

## 五、FEXX 常見銲條等級

| 銲條分類 | $F_{EXX}$ | 說明 |
|---------|----------|------|
| E70XX | 70 ksi = 4.92 tf/cm² | 最常用（A36/A572 Gr.50 鋼材） |
| E80XX | 80 ksi | 高強度鋼用 |
| E100XX | 100 ksi | HSLA 鋼 |

**台灣考試常見：** E70XX（對應 43 級或 50 級鋼材）

---

## 六、最小銲腳尺寸規定（AISC Table J2.4）

| 較薄板件厚度 $t$ | 最小銲腳 $w_{min}$ |
|---------------|-----------------|
| $t \leq 6$ mm | 3 mm |
| $6 < t \leq 13$ mm | 5 mm |
| $13 < t \leq 19$ mm | 6 mm |
| $t > 19$ mm | 8 mm |

**最大銲腳尺寸：**
- 板厚 $\leq 6$ mm：$w_{max} = t$（板的全厚）
- 板厚 $> 6$ mm：$w_{max} = t - 2$ mm（留 2 mm 防熱影響區問題）

---

## 七、常見考試問法

| 問法 | 要點 |
|------|------|
| 「0.707 怎麼來」 | 等腰直角三角形的喉部 = $w\cos 45° = 0.707w$ |
| 「填角銲強度公式推導」 | $\phi R_n = 0.75 \times 0.6F_{EXX} \times 0.707w \times L$ |
| 「銲腳 w 與有效喉 te 的差別」 | $w$ 是外觀量測值，$t_e = 0.707w$ 是最小承力截面 |
| 「為何用 0.75 而非 0.9」 | 銲接屬局部/脆性型破壞，φ = 0.75 |

## 相關頁面

- [[WELDED-CONNECTION-DESIGN]] — 銲接接合設計概念
- [[phi-resistance-factors]] — φ = 0.75 的物理意義
- [[eccentric-weld]] — 偏心銲縫計算（使用此強度公式）
