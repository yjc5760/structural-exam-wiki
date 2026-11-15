# -*- coding: utf-8 -*-
"""FIX SM-2011-3：「平均新增鉛垂應力」改為沿黏土層厚的 2:1 積分平均（原為中點值）。在 SM/ 下執行；可重複執行。"""
p = "raw/solutions/SM-2011-3/SM-2011-3.md"
t = open(p, encoding="utf-8").read()
if "FIX：平均應力改積分平均" in t:
    raise SystemExit("already fixed")
R = [
("| 單位重 | 砂土、黏土都沒給單位重，須由 $e$、$G_s$、$S$ 換算（#7、#8） | 直接假設 $\\gamma=18$ |",
 "| 單位重 | 砂土、黏土都沒給單位重，須由 $e$、$G_s$、$S$ 換算（#7、#8） | 直接假設 $\\gamma=18$ |\n| 所求「平均」應力 | ㈠問黏土層的**平均**新增應力（#11）：2:1 公式沿層厚取平均，$\\Delta\\sigma_{av}=55.56$ kPa | 只取黏土中點一點的 49.38 kPa 當平均（本解 2026-11-15 前即如此，沉陷因而少算 25%） |"),
("並理解「平均新增應力」在實務上的簡化取法（通常取黏土層中央深度）。",
 "並依題意求整個黏土層的「平均」新增應力——沿層厚平均，不是中點一點的值。"),
("3. **計算平均新增應力 $\\Delta\\sigma_{avg}$**：採用 2:1 應力分布法，計算黏土層中央深度之新增應力作為平均值。",
 "3. **計算平均新增應力 $\\Delta\\sigma_{avg}$**：採用 2:1 應力分布法，沿黏土層厚度（基底下 $z_t$ = 1.2 m 到 $z_b$ = 4.2 m）積分取平均，再以辛普森法則交叉驗算。"),
("- **陷阱三：沉陷量公式錯用**。",
 "- **陷阱四：把中點值當平均**。題目明問「平均」新增應力；黏土頂、中、底的增量為 111.11、49.38、27.78 kPa，分布上凹，中點值比層厚平均低約 11%。\n- **陷阱三：沉陷量公式錯用**。"),
("- 2:1 應力分布（黏土層中央新增應力）：\n  $$ \\Delta\\sigma_{avg} = \\frac{Q}{(B+z_m)(L+z_m)} $$",
 "- 2:1 應力分布（沿黏土層厚取平均，$B=L$）：\n  $$ \\Delta\\sigma_{avg} = \\frac{1}{H}\\int_{z_t}^{z_b}\\frac{Q}{(B+z)^2}\\,dz = \\frac{Q}{H}\\left(\\frac{1}{B+z_t}-\\frac{1}{B+z_b}\\right) $$"),
("| $\\Delta\\sigma_{avg}$ | $Q / [(B+z_m)(L+z_m)]$ | |",
 "| $\\Delta\\sigma_{avg}$ | $\\frac{Q}{H}\\left(\\frac{1}{B+z_t}-\\frac{1}{B+z_b}\\right)$（2:1 積分平均） | |"),
("| **平均應力選取法** | 實務上 2:1 法的「黏土層平均新增應力」多直接取中央深度 $z_m$ 計算。 | |",
 "| **平均應力選取法** | 題目問「平均」時要沿層厚平均（積分或辛普森法則）；中點值只是近似。本題 $p_0'+\\Delta\\sigma$ 恰在 $p_c'$ 附近，平均值差 11% 就讓沉陷差約 33%。 | |"),
]
for a, b in R:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
# Step 3
i = t.index("### Step 3. 基礎中心下方黏土層之平均新增鉛垂向應力")
j = t.index("### Step 4. 黏土層之壓密沉陷量計算")
t = t[:i] + r"""### Step 3. 基礎中心下方黏土層之平均新增鉛垂向應力 ($\Delta\sigma_{avg}$)
> 💡 策略註解：題目問的是黏土層的「平均」新增應力，所以把 2:1 公式沿黏土層厚度取平均，而不是只取中點一點。

載重 $Q = 1 \text{ MN} = 1000 \text{ kN}$，基礎尺寸 $B \times L = 1.8 \text{ m} \times 1.8 \text{ m}$。深度 $z$ 由基礎底面起算：黏土頂 $z_t = 1.2 \text{ m}$、黏土底 $z_b = 1.2 + 3.0 = 4.2 \text{ m}$。

2:1 法任一深度的新增應力：
$$ \Delta\sigma_z = \frac{Q}{(B+z)(L+z)} $$
黏土頂、中、底分別為 $\Delta\sigma_t = \frac{1000}{3.0^2} = 111.11 \text{ kPa}$、$\Delta\sigma_m = \frac{1000}{4.5^2} = 49.38 \text{ kPa}$、$\Delta\sigma_b = \frac{1000}{6.0^2} = 27.78 \text{ kPa}$。

沿層厚積分取平均（$B = L$）：
$$ \Delta\sigma_{avg} = \frac{1}{H}\int_{z_t}^{z_b}\frac{Q}{(B+z)^2}\,dz = \frac{Q}{H}\left(\frac{1}{B+z_t}-\frac{1}{B+z_b}\right) = \frac{1000}{3.0}\left(\frac{1}{3.0}-\frac{1}{6.0}\right) = \mathbf{55.56 \text{ kPa}} $$

交叉驗算（辛普森法則）：$\Delta\sigma_{avg} \approx \frac{1}{6}(\Delta\sigma_t + 4\Delta\sigma_m + \Delta\sigma_b) = \frac{1}{6}(111.11 + 4 \times 49.38 + 27.78) = 56.07 \text{ kPa}$，與積分值差 0.9%。

**(一) 基礎中心下方黏土層之平均新增鉛垂向應力解答：**
$$ \boxed{\Delta\sigma_{avg} = 55.56 \text{ kPa}} $$

""" + t[j:]
R2 = [
("$$ p_f' = p_0' + \\Delta\\sigma_{avg} = 53.20 + 49.38 = \\mathbf{102.58 \\text{ kPa}} $$",
 "$$ p_f' = p_0' + \\Delta\\sigma_{avg} = 53.20 + 55.56 = \\mathbf{108.76 \\text{ kPa}} $$"),
("  $$ S_{c2} = \\frac{0.25 \\times 3000 \\text{ mm}}{1 + 0.68} \\log\\left(\\frac{102.58}{100}\\right) = 446.43 \\times \\log(1.0258) = 446.43 \\times 0.01106 \\approx 4.94 \\text{ mm} $$",
 "  $$ S_{c2} = \\frac{0.25 \\times 3000 \\text{ mm}}{1 + 0.68} \\log\\left(\\frac{108.76}{100}\\right) = 446.43 \\times \\log(1.0876) = 446.43 \\times 0.03647 \\approx 16.28 \\text{ mm} $$"),
("$$ S_c = 29.37 + 4.94 = \\mathbf{34.31 \\text{ mm}} $$", "$$ S_c = 29.37 + 16.28 = \\mathbf{45.65 \\text{ mm}} $$"),
("$$ \\boxed{S_c = 34.31 \\text{ mm}} $$",
 "$$ \\boxed{S_c \\approx 45.6 \\text{ mm}} $$\n\n交叉驗算：把黏土層切成薄層，各層用該深度的 $p_0'(z)$ 與 $\\Delta\\sigma_z$ 分別判斷 OC／NC 段後積分，得 $S_c = 46.5 \\text{ mm}$，與上式差 2%。"),
]
for a, b in R2:
    assert t.count(a) == 1, a[:50]
    t = t.replace(a, b)
# §5 item 1
i = t.index("1. **關於 2:1 法「平均應力」的三種解讀方式**")
j = t.index("2. **基礎自重與開挖解壓的考量**")
t = t[:i] + r"""1. **2:1 法「平均應力」的三種算法與差異**：
   - **積分平均（本解主線）**：$\Delta\sigma_{avg} = \frac{Q}{H}\left(\frac{1}{B+z_t}-\frac{1}{B+z_b}\right) = 55.56 \text{ kPa}$，是 2:1 分布沿層厚的精確平均，$S_c = 45.6 \text{ mm}$。
   - **辛普森法則**：$\frac{1}{6}(\Delta\sigma_t + 4\Delta\sigma_m + \Delta\sigma_b) = 56.07 \text{ kPa}$，與積分值幾乎相同，$S_c = 46.6 \text{ mm}$；手算時較快。
   - **中點值（對照，不是平均）**：只取黏土中點 $\Delta\sigma_m = 49.38 \text{ kPa}$，$p_f' = 102.58 \text{ kPa}$ 僅略超過 $p_c'$，$S_c = 34.3 \text{ mm}$。本解 2026-11-15 前以此為答案；題目明問「平均」新增應力，且 2:1 分布上凹，中點值必然低於層厚平均。
   - 為什麼差這麼多：$p_0' = 53.2 \text{ kPa}$ 到 $p_c' = 100 \text{ kPa}$ 的回脹段兩法相同（29.37 mm），差別全在越過 $p_c'$ 後的 $C_c$ 段：$\log(108.76/100)$ 與 $\log(102.58/100)$ 相差 3.3 倍。終應力落在 $p_c'$ 附近時，平均應力的取法對答案非常敏感。

""" + t[j:]
t = t.rstrip("\n") + "\n\n*修正日期：2026-11-15（FIX：平均應力改積分平均——㈠ 平均新增應力 49.38 → 55.56 kPa（原為黏土中點值，非平均）、㈡ 沉陷 34.31 → 45.6 mm；§1 常見誤讀、§2、§3、§3.5、§4 Step 3–4、§5 同步。驗證：腳本重算 14 個數值 MISMATCHES: 0，辛普森法則 56.07 kPa 與分層積分 46.5 mm 交叉驗算；依 2026-11-15 獨立盲解比對）*\n"
open(p, "w", encoding="utf-8").write(t)
print("fixed")
