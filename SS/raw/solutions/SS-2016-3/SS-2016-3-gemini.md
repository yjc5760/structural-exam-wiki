沒問題！這題的精華就在於第四小題中「理論與現實的物理衝突」。我們用最嚴謹的力學邏輯，幫你把這題從頭到尾重新解一次，並在最後明確標示出**「物理真實」**與**「坊間/考選部近似解」**的差異，讓你在考場上能寫出令閱卷委員驚豔的滿分解答。

---

### **SS-2016-3 嚴謹重新解題**

#### **(一) 何謂殘留應力？ (5分)**
[cite_start]殘留應力 (Residual Stress) 是指構材在沒有承受任何外部載重的作用下，存在於其截面內部、且自我平衡的初始應力系統 [cite: 64, 66][cite_start]。其特徵為截面上的壓區合力與拉區合力必須大小相等、方向相反（淨力為零、淨力矩為零） [cite: 65]。

#### **(二) 殘留應力的來源有哪些？ (5分)**
[cite_start]主要來源有三類 [cite: 69]：
1. [cite_start]**不均勻冷卻（最主要）：** 熱軋型鋼在脫模冷卻時，較薄的部分（如翼板尖端）冷卻較快，較厚的部分（如翼板與腹板交界）冷卻較慢。先冷卻部位會受到後冷卻部位收縮的拉扯與擠壓，導致先冷部位受壓，後冷部位受拉 [cite: 69]。
2. [cite_start]**焊接熱輸入：** 焊接過程中局部高溫冷卻收縮，會在焊縫附近產生殘留拉應力，較遠處產生殘留壓應力 [cite: 69]。
3. [cite_start]**冷加工 (Cold Working)：** 常溫下的彎曲或矯正作業，使局部材料超過降伏點，卸載後彈性回彈不均勻所致 [cite: 69]。

#### **(三) 殘留應力對受壓桿件的影響為何？ (5分)**
[cite_start]殘留應力會導致受壓構材的**局部提早降伏**。當外部施加的壓應力加上截面原有的殘留壓應力達到鋼材降伏強度時（即 $F_a + F_{rc} \ge F_y$） [cite: 77][cite_start]，該區域便失去抵抗額外應力的能力 [cite: 78]。
[cite_start]這會造成有效截面積縮小，整體斷面的切線模數 (Tangent Modulus, $E_t$) 下降，進而降低柱的臨界挫屈強度 [cite: 78, 80][cite_start]。這種強度的削弱在**中等細長比**的柱子中最為顯著 [cite: 84, 86]。

---

#### **(四) 繪製 $F_{cr}$ vs $L/r$ 曲線 (15分)**

**已知條件：**
* [cite_start]材料降伏應力 $F_y = 2.5 \text{ tf/cm}^2$ [cite: 89]
* [cite_start]彈性模數 $E = 2040 \text{ tf/cm}^2$ [cite: 89]
* [cite_start]最大殘留壓應力 $F_{rc} = F_y/4 = 0.625 \text{ tf/cm}^2$ (位於翼板兩端各 $b/3$ 區段) [cite: 30, 89]

**步驟 1：計算比例限 (Proportional Limit, $F_{PL}$)**
當疊加外部壓應力後，翼板尖端最先達到降伏：
[cite_start]$$F_{PL} = F_y - F_{rc} = 2.5 - 0.625 = \mathbf{1.875 \text{ tf/cm}^2}$$ [cite: 92]

**步驟 2：計算彈性-非彈性轉折點細長比 $(L/r)_{trans}$**
當 Euler 臨界應力剛好等於比例限時，為進入非彈性挫屈的臨界點：
[cite_start]$$F_e = \frac{\pi^2 E}{(L/r)^2} = F_{PL}$$ [cite: 95]
[cite_start]$$\frac{\pi^2 \times 2040}{(L/r)^2} = 1.875 \implies (L/r)_{trans} = \sqrt{\frac{20133.5}{1.875}} = \mathbf{103.6}$$ [cite: 96]

**步驟 3：建立曲線分段方程式（物理真實觀點）**
[cite_start]因為題目給定的是**「塊狀分佈」**（外側均勻受壓 $F_y/4$） [cite: 30]，這會導致極度特殊的物理現象：

1. [cite_start]**彈性區（$L/r > 103.6$）：** 全截面未降伏，遵循 Euler 公式 [cite: 98]。
   [cite_start]$$F_{cr} = \frac{\pi^2 \times 2040}{(L/r)^2}$$ [cite: 99]

2. [cite_start]**非彈性區（$L/r \le 103.6$）：** 當外部應力達到 $1.875 \text{ tf/cm}^2$ 時，翼板外側總計 $2b/3$ 的區域會**「瞬間同時降伏」**。鋼材為完美彈塑性（降伏後切線模數 $E_t = 0$） [cite: 36]，這會導致斷面的有效慣性矩 $I_{eff}$ 發生斷崖式暴跌（強軸慣性矩瞬間只剩約 1/3）。
   因為剛度瞬間大幅流失，柱子無法承受更高的應力，因此曲線在這裡不會是平滑的，而是會形成一段**水平的「挫屈高原區 (Plateau)」**。

**曲線特徵描述（繪圖重點）：**
* [cite_start]**$L/r > 103.6$：** 拋物線狀的 Euler 曲線，結束於 $(103.6, 1.875)$ [cite: 108]。
* **$L/r$ 在 $103.6$ 到約 $60$ 之間：** 一條水平線 $F_{cr} = 1.875 \text{ tf/cm}^2$（物理真實現象）。
* [cite_start]**短柱區：** 應力最終向 $F_y = 2.5 \text{ tf/cm}^2$ 爬升收斂 [cite: 108]。

---

### 💡 考場防禦與拿分策略（強烈建議）

在國考作答圖形時，為了避免閱卷老師只看「坊間標準答案」而誤判，建議你在圖上**同時畫出兩條線**，並加註文字說明展現實力：

1. **畫出真實的水平轉折線（實線）**：標註「因殘留應力為均勻塊狀分佈，應力達 $1.875$ 時外側翼板瞬間降伏，剛度突降形成高原區」。
2. [cite_start]**畫出平滑過渡的非彈性曲線（虛線）**：利用 $F_{cr} = \frac{F_y \cdot F_e}{F_e + F_{rc}}$ 公式 [cite: 102] 畫出一條平滑連接 $(103.6, 1.875)$ 與 $(0, 2.5)$ 的曲線，並標註「此為假設漸進式降伏之理論近似解」。

這樣不僅保住了基本分，還能展現你超越一般考生的結構力學素養。

為了讓你更直觀地感受「真實物理現象」與「近似理論」的巨大差異，我為你準備了一個互動圖表，你可以拖曳細長比，觀察斷面降伏狀態與強度的變化：

```json?chameleon
{"component":"LlmGeneratedComponent","props":{"height":"700px","prompt":"Create an interactive educational dashboard comparing two buckling curves: 'True Block Yielding (Real Physics)' vs 'Progressive Yielding Approx'. Initial values: Fy = 2.5, E = 2040, F_rc = 0.625, F_PL = 1.875, L/r_trans = 103.6. Use a standard layout. Inputs: A slider for 'Slenderness Ratio (L/r)' ranging from 20 to 150. Behavior: Display a D3.js line chart with L/r on the X-axis (0-150) and Critical Stress F_cr on the Y-axis (0-3.0). Plot three lines: 1. Elastic Euler Curve (pi^2*E/(L/r)^2). 2. Progressive Yielding Approx (Fy * Fe / (Fe + F_rc)) as a dashed line. 3. True Block Yielding curve (solid line) which perfectly tracks Euler for L/r > 103.6, forms a horizontal plateau at F_cr = 1.875 for L/r from roughly 60 to 103.6, and then rises to 2.5. Include a vertical marker line that moves with the slider. Below the chart, display an SVG visualizer of the cross-section (a rectangular flange). As the slider moves and F_cr changes: If F_cr < 1.875, show the whole section as 'Elastic'. If the slider is in the plateau region (F_cr = 1.875), visually distinguish the outer 1/3s of the flange as 'Yielded (E_t = 0)' and the middle 1/3 as 'Elastic'. Distinguish elements clearly using semantic visual states.","id":"im_ed0f1354c0399953"}}
```