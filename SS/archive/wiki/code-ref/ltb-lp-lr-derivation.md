# LTB 邊界長度 Lp / Lr 的來源

**Code-Ref ID：** ltb-lp-lr-derivation
**對應方法頁：** [[ltb-3zone]]（`wiki/methods/ltb-3zone.md`）
**對應概念頁：** [[LATERAL-TORSIONAL-BUCKLING]]

---

## 一、三段式結構的物理根據

LTB 強度被分成三段，是因為「側扭挫屈何時發生、如何發生」在不同無支撐長度 $L_b$ 下物理機制不同：

| 區段 | $L_b$ 範圍 | 控制機制 | 可達強度 |
|------|-----------|---------|---------|
| **塑性段** | $L_b \leq L_p$ | 翼板先局部降伏，LTB 無法在達 $M_p$ 前發生 | $M_n = M_p$ |
| **非彈性段** | $L_p < L_b \leq L_r$ | 部分截面降伏（翼板端因殘留應力已降伏），線性折減 | $M_r \leq M_n < M_p$ |
| **彈性段** | $L_b > L_r$ | 全截面在彈性範圍內側扭挫屈 | $M_n < M_r$ |

---

## 二、Lp 的推導

**$L_p$ 定義：** 無側撐長度不超過 $L_p$ 時，可達完全塑性彎矩 $M_p$，不受 LTB 限制。

**理論基礎：** 對 I 形斷面，彈性 LTB 臨界彎矩為：

$$M_{cr} = \frac{\pi}{L_b}\sqrt{EI_y GJ} \cdot \sqrt{1 + \frac{\pi^2 EC_w}{GJ L_b^2}}$$

當 $L_b$ 短時，$M_{cr}$ 很高，不是控制因素。但 AISC 的 $L_p$ 定義採**簡化公式**，以 $r_y$（弱軸迴轉半徑）為基礎：

$$\boxed{L_p = 1.76\,r_y\sqrt{\frac{E}{F_y}}}$$

**推導邏輯：**
- 令 $r_y$ 對應的細長比 $L_p/r_y = 1.76\sqrt{E/F_y}$
- 對 A36 鋼（$F_y = 36$ ksi，$E = 29000$ ksi）：$L_p/r_y \approx 1.76\sqrt{29000/36} \approx 50$
- 此係數使「大多數常見 I 形斷面在 $L_b = L_p$ 時恰好能完整發展 $M_p$」
- 實質上是**校準值**（calibrated value），而非純解析推導

**台灣規範換算（tf/cm² 系統）：**

$$L_p[\text{cm}] = \frac{80\,r_y}{\sqrt{F_y[\text{tf/cm}^2]}}$$

（係數 80 是從 1.76√E/Fy 在 tf/cm² 單位下的換算結果：$1.76\sqrt{2040} \approx 79.5 \approx 80$）

---

## 三、Lr 的推導

**$L_r$ 定義：** 無側撐長度超過 $L_r$ 時，全截面均在彈性範圍內發生 LTB（截面有殘留應力，但挫屈在彈性範圍）。

**理論基礎：** $L_r$ 是令彈性 LTB 臨界彎矩 $M_{cr}$ = **初始降伏彎矩 $M_r$** 時的 $L_b$：

$$M_r = (F_y - F_r)S_x \quad \text{（含殘留應力折減：}F_r \approx 0.3F_y\text{）}$$

令 $M_{cr} = M_r$，解出 $L_b = L_r$：

$$\boxed{L_r = 1.95\,r_{ts}\frac{E}{F_y - F_r}\sqrt{\frac{J}{S_x h_o} + \sqrt{\left(\frac{J}{S_x h_o}\right)^2 + 6.76\left(\frac{F_y - F_r}{E}\right)^2}}}$$

其中：
- $r_{ts}^2 = \frac{\sqrt{I_y C_w}}{S_x}$（有效迴轉半徑，比 $r_y$ 略大）
- $h_o$ = 翼板形心距（約 $\approx d - t_f$）
- $F_r = 0.3 F_y$（翼板殘留應力）

**簡化認知：** 記不住推導也能考試，關鍵是理解 $L_r$ 的物理意義：**超過 $L_r$ 後，彈性 LTB 公式適用**。

---

## 四、非彈性段的線性內插

$L_p < L_b \leq L_r$ 之間採**線性內插**，而非另一個複雜公式：

$$M_n = C_b\left[M_p - (M_p - M_r)\frac{L_b - L_p}{L_r - L_p}\right] \leq M_p$$

**為何線性？** 非彈性 LTB 的精確行為複雜（翼板逐步降伏），但試驗與數值分析顯示在 $[L_p, L_r]$ 之間強度下降近似線性，規範採線性內插作為**保守下包絡線**。

---

## 五、彈性段

$$M_n = F_{cr} S_x \leq M_p \quad \text{（AISC 360 F2-3）}$$

$$F_{cr} = \frac{C_b \pi^2 E}{(L_b/r_{ts})^2}\sqrt{1 + 0.078\frac{J}{S_x h_o}\left(\frac{L_b}{r_{ts}}\right)^2}$$

**物理意義：** 這就是含翹曲剛度的彈性 LTB 公式。$\sqrt{1+0.078\cdots}$ 修正項考慮了翹曲勁度 $C_w$ 的貢獻（短柱 → 翹曲重要，長柱 → 純 Saint-Venant 扭轉控制）。

---

## 六、常見考試問法

| 考法 | 答題要點 |
|------|---------|
| 「Lp 的物理意義」 | $L_b \leq L_p$ 時斷面能完全塑性化（$M_n = M_p$），無 LTB 限制 |
| 「為何三段」 | 因殘留應力，截面在 $L_p < L_b \leq L_r$ 時部分提前降伏，強度介於 $M_p$ 和 $M_r$ 之間 |
| 「$L_p$ 公式中 1.76 怎來」 | 以 $r_y$ 校準的近似值，確保大多數 I 形斷面在此長度下可達 $M_p$ |
| 「$M_r$ 中為何有 $F_r$」 | 殘留應力使翼板端提前降伏，初始降伏彎矩降低至 $(F_y - F_r)S_x$ |

## 相關頁面

- [[ltb-3zone]] — 計算流程（方法頁）
- [[LATERAL-TORSIONAL-BUCKLING]] — LTB 物理機制（概念頁）
- [[cb-formula-derivation]] — Cb 係數來源（此目錄）
- [[RESIDUAL-STRESS]] — 殘留應力對 $F_r$、$L_r$ 的影響
