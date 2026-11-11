# SD 科目設定（SUBJECT.md）— 結構動力分析與耐震設計

> 本檔是 **SD 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md` 與根目錄 `skills/` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`SD`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。
> 原獨立 repo `exam-wiki-SD` 於 2026-11-11 搬入（見 §9）；原 repo 規則檔參考副本在 `archive/exam-wiki-SD-root/`。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `SD`（Structural Dynamics & Seismic Design） |
| 科目全名 | 結構動力分析與耐震設計 |
| 題號格式 | `SD-YYYY-N`（YYYY 為西元年，例 `SD-2015-1`） |
| 考卷檔名 | `raw/exams/SD-YYYY_結構動力分析與耐震設計.pdf` |
| 收錄範圍 | 2002–2025 年（民國 91–114 年）24 考年，共 **99 題**（2003、2004、2016 年各 5 題）；2026-08-22 起全庫重設為 unverified，人工驗算通過者再逐題改回 verified；題目正本（`-problem.md`）尚未建立 |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立，2026-10-29；2026-11-11 由原 repo 搬入內容 |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 | 主 | 副 |
|---------|------|------|:--:|:--:|
| `SD-U1-1` | 結構動力基本性質及原理 | 第一單元 | 2 | 20 |
| `SD-U1-2` | 運動方程式推導 | 第一單元 | 10 | 18 |
| `SD-U1-3` | 單自由度、多自由度系統之動態分析及應用 | 第一單元 | 43 | 22 |
| `SD-U2-1` | 地震力之設計規範 | 第二單元 | 1 | 9 |
| `SD-U2-2` | 建築耐震設計規範 | 第二單元 | 17 | 20 |
| `SD-U2-3` | 橋梁耐震設計規範 | 第二單元 | 4 | 1 |
| `SD-U3-1` | 結構耐震設計（含 RC 結構與鋼結構） | 第三單元 | 9 | 4 |
| `SD-U3-2` | 隔減震原理 | 第三單元 | 13 | 6 |

（題數為 2026-11-11 搬入時 `question_index.json` 的統計。）

**分類原則（五科一律）：** `primaryTopicId`、`secondaryTopicIds` **只能填本科子項**，不引用他科的單元。題目涉及他科觀念時，歸到本科最接近的子項（例：見根目錄 CLAUDE.md「命題大綱分類」）。
搬入時稽核（`audit_classification.py SD SD`）：**0 題指向他科**，無須改歸；索引名稱與解析標頭的不一致見 §10。

---

## 3. `designMethod` 欄位（本科分類軸：題型）

2026-11-11 經使用者決定，99 題歸併為四值，寫入索引 `designMethod`（單元總覽、共用樣板儀表板、稽核都讀這一欄）：

| 允許值 | 判準 | 題數 |
|--------|------|:---:|
| `動力分析` | 以結構動力學計算或推導為主：運動方程式、Lagrange／Ritz／Rayleigh、自由／強迫振動、特徵值、振態疊加、**題目給定反應譜**下的反應計算（含等位移法則）、消能元件以能量法求等效阻尼 | 58 |
| `規範計算` | 依規範公式或耐震實務的靜力程序計算／檢核：等效靜力法與豎向分配、規範週期公式（如橋梁規範 Rayleigh 式）、隔震設計位移程序（$D_D$、$T_{eD}$、$B$ 係數）、RC 耐震配筋檢核、側力分配近似法（懸臂梁法、短柱剪力分配） | 9 |
| `概念題` | 以說明、比較、繪圖為主，沒有數值計算（可含簡短公式說明） | 22 |
| `混合` | 同一題兩類以上各占相當配分，例：論述子題＋計算子題（SD-2008-3、2008-4、2016-5、2018-2、2022-3、2022-4、2023-3），動力分析＋規範程序（SD-2012-2、2024-4），動力分析＋靜力崩塌分析＋論述（SD-2010-4） | 10 |

> 判讀邊界：給的是規範型設計反應譜、但要做的是振態疊加或 SDOF 反應（SD-2002-4、2012-1、2016-4、2019-3）→ 動力分析；
> 只要套規範程序（隔震 $D_D$、FPS 設計，SD-2014-2、2018-4）→ 規範計算。
> SD-2015-4（懸臂梁法求構件彎矩）、SD-2017-3（短柱剪力分配）是靜力側力分配，不屬動力分析，暫歸規範計算。
>
> **`analysisMethod` 保留不刪**：原 repo 的方法長描述（75 種寫法，例「MDOF模態疊加法（第一模態基底剪力推導 + 倒三角豎向分配）」），
> 解析標頭 `**分析方法：**` 對應的是這一欄（99 份中 90 份有標頭；SD-2011-1、2011-2、2011-4、2012-1、2012-2、2012-4、2013-4、2016-4、2016-5 沒有）。
> 原 repo 的儀表板（`index.html` 的 `categorizeMethod`）與命題分析頁 `study-SD-*.html` 都由 `analysisMethod` 即時歸類，所以照舊可用。
> 根目錄 `audit_classification.py`：索引兩欄都有時，解析標頭與 `analysisMethod` 比對。
> 新題兩欄都要填：`designMethod` 填上表四值之一，`analysisMethod` 寫方法描述（與解析標頭一致）。

### 3.1 單位與符號慣例（本科特別容易出錯；原 repo `CLAUDE.md`）

結構動力學橫跨數個單位制，且同一符號在不同章節意義不同，撰寫解析與方法論時務必標註：

| 項目 | 常見表示 | 注意 |
|------|---------|------|
| 質量 $m$ | tf·s²/cm、kg、N·s²/m | **重量 $W$ 與質量 $m$ 差一個 $g$**，本科最常見的錯 |
| 勁度 $k$ | tf/cm、kN/m | $k = cEI/L^3$ 的係數（3／12／48…）取決於邊界條件，不可套錯 |
| 圓頻率 $\omega$ | rad/s | 與頻率 $f$ (Hz) 差 $2\pi$；週期 $T = 2\pi/\omega$ |
| 阻尼比 $\xi$ | 無因次 | 題目給「5%」時代入 0.05，不是 5 |
| 反應譜加速度 $S_a$ | $g$ 的倍數 或 cm/s² | 以 $g$ 表示時要乘回 $g$ 才能與質量相乘得力 |

> 撰寫方法論與解析時，係數一律附上單位制標註，並盡量同時給出無因次形式。
> 本科解析慣用 $\xi$ 表示阻尼比（§8 起始版用 $\zeta$，兩者同義）。

### 3.2 標籤詞彙

原 repo `CLAUDE-SPEC.md` §8 的標準標籤表是從 RC 複製來沒改的（設計法 USD／WSD、板、柱帶…），**不適用本科、未搬入**。
目前索引 `tags` 為自由詞彙（651 種，前幾名：MDOF 26、SDOF 18、自然頻率 15、模態參與因子 12、特徵值問題 11、運動方程式 11）。

---

## 4. 圖解（struct-diagram）

解題或勘誤後需要圖解時，用 `struct-diagram` skill 以程式產生向量圖（SVG＋2× PNG），
腳本 `gen_SD-YYYY-N.py` 與 `figs/` 放在該題資料夾，`.md` 引用 SVG 相對路徑。
（互動圖 `*-viz.html` 功能已於 2026-10-29 停用；原 repo 的 24 份已於 11-01 刪除。）
搬入時已有 29 題有 `figs/` 與 `gen_*.py`。

本科常見圖解：

- 結構模型與自由度
- 振態形狀
- 反應譜／設計譜
- 時間歷程反應
- 動力放大係數曲線

---

## 5.（保留編號）wiki 已封存

原 repo 已於 2026-11-01 自行把 `wiki/` 除 `queries/` 外的各層移到 `archive/wiki/`（說明見 `archive/README.md`），
與根目錄 2026-11-08 的「wiki 封存」規則一致。七層（failure-modes、materials、code-ref…）不再維護。

---

## 6. 題型辨識

診斷頁已封存於 `archive/wiki/diagnosis/`（`sdof.md`、`mdof.md`、`spectrum.md`、`code-design.md`，未逐頁核對，僅供參考）。
解題時的題型辨識以 §8 的框架與 `skills/exam-solve` 的三層掃描為準：

| 題型 | 辨識關鍵字 |
|------|-----------|
| 單自由度自由振動 | 「自然頻率」「阻尼比」「對數遞減」 |
| 單自由度強制振動 | 「簡諧載重」「衝擊」「Duhamel」「動力放大」「基礎激振」「傳遞率」 |
| 運動方程式推導 | 「推導運動方程式」「廣義座標」「Lagrange」「Rayleigh 法」「形函數」 |
| 多自由度系統 | 「振態」「特徵值」「振態疊加」「參與因子」「有效質量」 |
| 建築耐震規範計算 | 「設計地震力」「V」「SDS」「SD1」「Fu」「Ra」 |
| 橋梁耐震規範 | 「橋梁」「橋墩」「支承」「落橋」 |
| 結構耐震設計 | 「韌性構架」「強柱弱梁」「容量設計」「短柱」 |
| 隔減震 | 「隔震」「消能」「阻尼器」「週期延長」「LRB」「FPS」 |

---

## 7. 主要規範／依據

- 建築物耐震設計規範及解說（內政部；以考卷年份適用版本為準）
- 公路橋梁耐震設計規範（交通部）
- 建築物隔震與消能相關章節

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。

---

## 8. 設計哲學框架（解題邏輯）

> SOLVE 時與 `skills/exam-solve` 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。
> 8.1 是 scaffold 起始版；8.2 是原 repo `CLAUDE-SOLVE.md`「設計哲學框架」原文（2026-11-11 搬入）。

### 8.1 起始版（scaffold）

**單自由度系統（SD-U1-1、SD-U1-3）**
```
運動方程式：m ü + c u̇ + k u = p(t)
ωn = √(k/m)；ζ = c / (2 m ωn)；ωD = ωn √(1 − ζ²)
簡諧載重：動力放大係數 Rd = 1 / √[(1 − r²)² + (2ζr)²]，r = ω/ωn
一般載重：Duhamel 積分；衝擊／脈衝載重：最大反應（衝擊譜）
```

**運動方程式推導（SD-U1-2）**
```
選廣義座標 → 寫出動能 T、位能 V、非保守力虛功 → Lagrange 方程或虛功原理
等效質量、等效勁度、等效載重要在同一個廣義座標上一致
```

**多自由度系統（SD-U1-3）**
```
(K − ω²M) φ = 0 → 振態頻率與振態；振態對 M、K 正交
振態疊加：Γn = φnᵀ M ι / φnᵀ M φn；反應譜各振態最大值以 SRSS／CQC 組合
```

**建築耐震設計規範（SD-U2-2）**
```
工址 → SDS、SD1（含場址放大）→ 基本振動週期 T → 設計譜 SaD
結構系統 → R → Ra → Fu；用途係數 I
V = (SaD·I / (1.4 αy Fu))m · W（依考卷年份規範版本的修正與下限規定）
→ 豎向分配 Fx → 層間變位、意外扭矩、垂直不規則等檢核
```

**隔減震（SD-U3-2）**
```
隔震：延長週期、增加阻尼 → 降低上部結構加速度，代價是隔震層位移變大
消能：以遲滯或黏滯元件吸收能量，提高等效阻尼比
```

### 8.2 原 repo 完整版（原文保留；⚠️ 標記處待核對）

> ⚠️ 搬入時讀到三處疑點，**未修改原文**，待使用者核對後再決定是否更正：
> 1. 「台灣建築耐震設計規範」一段是美國 ASCE 7 的寫法（SMS／SM1、R、Ie、TL、V ≥ 0.01W），與台灣規範的
>    $V = \dfrac{S_{aD} I}{1.4\alpha_y F_u}W$（8.1）不同；解台灣規範題請以 8.1 與考卷年份規範為準。
> 2. 「摩擦阻尼器（BRB）」：BRB（挫屈束制支撐）是金屬降伏型消能元件，不是摩擦型。
> 3. 「ξeq = W_D / (4π·Ke·u_max²)」：以應變能 $E_S = \tfrac12 K u^2$ 定義時應為 $\xi_{eq} = \dfrac{W_D}{4\pi E_S} = \dfrac{W_D}{2\pi K u^2}$（與同段隔震 βeff 式一致），原文少了 ½。

**SDOF 自由振動**
```
核心：ẍ + 2ξω₀ẋ + ω₀²x = 0
      ω₀ = √(k/m)，ξ = c/(2mω₀)，ωd = ω₀√(1−ξ²)
欠阻尼（ξ < 1）：x(t) = e^(−ξω₀t)[A cos(ωd·t) + B sin(ωd·t)]
初始條件：x(0) = x₀，ẋ(0) = v₀
          A = x₀，B = (v₀ + ξω₀x₀)/ωd
週期：T = 2π/ω₀（無阻尼）；Td = 2π/ωd（有阻尼）
對數衰減率：δ = ln(xn/x_{n+1}) = 2πξ/√(1−ξ²) ≈ 2πξ（輕阻尼）
```

**SDOF 強迫振動（穩態）**
```
核心：mẍ + cẋ + kx = F₀ sin(Ωt)
穩態解：x(t) = X sin(Ωt − φ)
動力放大係數：D = 1/√[(1−r²)² + (2ξr)²]
      r = Ω/ω₀（頻率比）
      φ = arctan[2ξr/(1−r²)]
共振（r ≈ 1）：D_max ≈ 1/(2ξ)（輕阻尼）
最大靜變位：x_st = F₀/k
最大動態位移：X = D·x_st
```

**Duhamel 積分（任意激振）**
```
核心：x(t) = (1/mωd)∫₀ᵗ F(τ)·e^[−ξω₀(t−τ)]·sin[ωd(t−τ)]dτ
地震激振（地盤加速度 üg(t)）：
  相對位移 u(t) = −(1/ωd)∫₀ᵗ üg(τ)·e^[−ξω₀(t−τ)]·sin[ωd(t−τ)]dτ
反應譜：
  Sd(T,ξ) = max|u(t)|        ← 位移反應譜
  Sv(T,ξ) = max|u̇(t)|        ← 速度反應譜（偽速度）
  Sa(T,ξ) = ω₀²·Sd(T,ξ)     ← 加速度反應譜（偽加速度）
  PSv ≈ ω₀·Sd（偽速度）；PSa ≈ ω₀²·Sd（偽加速度）
```

**MDOF 系統自由振動（模態分析）**
```
核心：[M]{ẍ} + [C]{ẋ} + [K]{x} = {0}
特徵值問題：([K] − ω²[M]){φ} = {0}
  → 求解 n 個自然頻率 ω₁ < ω₂ < ... < ωₙ
  → 對應 n 個振態向量 {φ}₁, {φ}₂, ..., {φ}ₙ
正規化：{φ}ᵢᵀ[M]{φ}ⱼ = δᵢⱼ（正交性）
模態參與因子：Γᵢ = {φ}ᵢᵀ[M]{1} / ({φ}ᵢᵀ[M]{φ}ᵢ)
有效質量：mᵢ* = Γᵢ²·mᵢ**；Σmᵢ* = 總質量（驗算）
```

**模態疊加法（反應譜分析）**
```
各模態最大反應：Xᵢ = Γᵢ·Sd(Tᵢ,ξᵢ)·{φ}ᵢ
SRSS 組合：X_total = √[ΣXᵢ²]（各模態頻率相差 > 10%）
CQC 組合：X_total = √[ΣΣρᵢⱼ·Xᵢ·Xⱼ]
  相關係數：ρᵢⱼ = 8ξ²(1+r)r^(3/2) / [(1−r²)² + 4ξ²r(1+r)²]
  r = ωⱼ/ωᵢ
```

**台灣建築耐震設計規範（設計地震力）**　⚠️ 見上方疑點 1
```
核心：設計水平地震力 V = Sa(T)·W / g
反應譜（SMS/SM1 為最大考量地震）：
  設計地震：SDS = (2/3)·SMS，SD1 = (2/3)·SM1
  短週期加速度：SMS = Fa·Ss
  長週期加速度：SM1 = Fv·S1（1秒週期）
  放大係數 Fa、Fv 依場址類別（SA~SF）查表
反應譜形狀：
  T ≤ T₀：Sa = SDS·[0.4 + 0.6T/T₀]
  T₀ ≤ T ≤ Ts：Sa = SDS
  Ts < T ≤ TL：Sa = SD1/T
  T > TL：Sa = SD1·TL/T²
  T₀ = 0.2·Ts，Ts = SD1/SDS
設計地震力：
  V = (SDS/R)·Ie·W（短週期控制）
  最小地震力：V ≥ (SD1·Ie)/(T·R)·W
  最大地震力：V ≤ (SDS·Ie)/(R)·W（T < Ts 時控制）
  極低地震力下限：V ≥ 0.01W
週期計算（建築）：
  T_a = Ct·hₙˣ（經驗公式）
  RC剪力牆：Ct=0.0488，x=0.75
  鋼筋混凝土：Ct=0.0466，x=0.9
```

**橋梁耐震設計規範（α法）**
```
核心：水平地震力 = α·W
設計地震加速度係數 A（依地震分區）
場址類別修正係數 S
等效靜力法：
  P = A·S·C·W
  C = 1.2S/T^(2/3)（慣性力係數）
  最大值：C ≤ 2.5A
  最小值：C ≥ 0.4A·S（長週期）
  橋梁重要性因子 I（生命線 = 1.5；主要 = 1.25；一般 = 1.0）
基礎液化評估：
  剪應力比 τ/σ'v vs 液化阻抗 CRR
  安全係數 FL = CRR/CSR
```

**隔震設計**
```
核心：延長週期，遠離地盤卓越週期；增加阻尼，減小反應
隔震系統等效線性化：
  等效剛度：Keff = F_max / D_max（割線剛度）
  等效阻尼比：βeff = W_D / (2π·Keff·D_max²)
  W_D = 遲滯迴圈面積（消散能量）
隔震週期：TIS = 2π√(W/(g·Keff))
設計位移：DD = g·SD1·TIS / (4π²·BD)
  BD = 阻尼修正係數（查表，βeff 函數）
最大位移（含扭轉）：DM = DD·(1 + y·12e/(b²+d²))
  y = 偏心方向距離，e = 偏心距
隔震層剪力（設計地震）：Vs = Keff·DD
上部結構設計：使用放大係數 Ω₀
```

**消能減震（被動控制）**　⚠️ 見上方疑點 2、3
```
粘滯阻尼器：F = C·|u̇|^α（α=1線性，α<1非線性）
摩擦阻尼器（BRB）：消散能量 = 降伏力×塑性變形×2
  等效黏滯阻尼比：ξeq = W_D / (4π·Ke·u_max²)
系統等效阻尼：ξtotal = ξstructure + ξadded
  → 反應由修正阻尼反應譜計算
```

---

## 9. CHANGELOG（SD 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
| 2026-10-29 | 停用互動圖（`*-viz.html`）；§4 改為 struct-diagram 圖解 | 靜態向量圖可重跑、可審核，與互動圖功能重疊 |
| 2026-11-11 | **由獨立 repo `exam-wiki-SD` 搬入本資料夾**（只搬檔案，不含 git 歷史）：先刪 10-29 scaffold 骨架（七層 wiki 空殼、空索引、共用樣板儀表板、KaTeX 副本、`.gitkeep`），再搬入 `raw/`（24 份考卷＋命題大綱副本、99 題解析、`methods/`、`pdf_*.txt`）、`study/`（命題分析 5 頁、給／背 5 頁＋PDF、觀念講義 5 份＋PDF、記憶片 `recall-decks/` 5 組 pptx＋PDF＋旁白稿、頻率熱圖、99 頁 problems-view、原 repo 的 `assets/katex/`）、`wiki/queries/`（含 `log.md`）、`archive/`（原 repo 11-01 已封存的舊 wiki 與其 README）、`影片講義/`（5 單元 HTML＋mp4）、儀表板 `index.html`／`dashboard-data.js`；`scripts/` 只留講義附圖產生器（`build_figs_SD-U2-2.py`、`build_figs_SD-U3-2.py`、`lecture_U1_1_figs.py`、`lecture_U1-2_figs.py`、`lecture_U1-3_figs.py`＋其依賴 `structdraw.py`）與 SD 版儀表板產生器 `refresh-dashboard.ps1`；原 repo 根目錄 CLAUDE*.md、`README.md`、`xcheck.py` 存參考副本於 `archive/exam-wiki-SD-root/`；README、檔案架構索引表、知識庫使用說明書改寫為合併後路徑與現況；`syllabus_taxonomy.json` 副本以 `sync_taxonomy.py` 重新同步（只差 `_meta`）；§1 補收錄範圍、§2 補題數、§3 記錄分類軸現況（`analysisMethod` 自由文字，待決）、§3.1 單位與符號慣例（原 CLAUDE.md）、§5～§6 改指封存、§8 補原 repo 完整框架（三處疑點加註） | 五科合一，SD 不再在原 repo 分岔維護。原 repo 與 GitHub Pages 舊網址維持上線不動，git 歷史保留在原 repo。未搬：`.claude/`（本機設定）、`.github/workflows/static.yml`（根目錄已有 deploy-pages.yml）、`.gitignore`／`.gitattributes`／`.nojekyll`（根目錄已涵蓋）、gitignore 的 `*.bak`（根目錄 2 份、study 5 份）與 `raw/solutions/SD-2023-4/_to_delete/`、`scripts/build_frequency.py`（v1.1 加 recall-decks 在地修改；根目錄 v1.2）、`scripts/render_problem_view.py`（根目錄版為超集）、`unit-exam-intel.skill`（已於 11-11 停用）、空的 `解題過程影片/`（gitignore） |
| 2026-11-11 | 共用腳本相容性檢查（不重產）：`render_problem_view.py` 抽 `SD-2016-4`、`SD-2003-2` 重產後比對——SD-2016-4 完全相同；SD-2003-2 只差兩處「文字後緊接清單」由 `<br />` 純文字改為真正的 `<ul>`（SA 搬入時併入的改進）；比對後還原原頁，99 頁維持原 repo 版。`build_frequency.py --check` 對帳通過（99 題）；`xcheck.py SD` A=0、B=0、C=0（根目錄版未掃封存區，見 §10）；站內相對連結 121 頁 2 處失效（原 repo 即缺圖，見 §10）；根目錄 `index.html` 五科入口讀得到 SD 99 題 | 根目錄 v1.2 頻率熱圖只認單元總覽 `unit-*.html`，SD 尚無，現在重產會拿掉「命題分析／講義／給背／記憶片」教材連結（見 §10） |
| 2026-11-11 | 分類稽核（`audit_classification.py SD SD`）：0 題指向他科；15 題 22 筆其他不一致（索引 `primaryTopicName` 舊名 7 筆、解析標頭主分類只寫到單元層級 13 份、缺主分類 2 份），未改，列 §10 | 主副分類全部是 SD 子項，無須改歸 |
| 2026-11-11 | **分類軸定案（使用者決定）**：99 題歸併為四值寫入 `question_index.json` 新欄位 `designMethod`（動力分析 58、概念題 22、混合 10、規範計算 9；判準與邊界題見 §3），`analysisMethod` 長描述保留；`scripts/subject_profiles.json` 的 SD `methodNotes` 同步改為判準全文；根目錄 `audit_classification.py` 改為索引兩欄都有時標頭對照 `analysisMethod`（其餘四科稽核結果逐字不變） | 單元總覽、共用樣板儀表板、稽核都要固定的分類軸；原 75 種自由文字無法篩選。保留長描述是因為解析標頭、原 repo 儀表板、命題分析頁都依它 |
| 2026-11-11 | **移除已停用的記憶片教材（`study/recall-decks/` 5 組 pptx＋PDF＋旁白稿）**：比照 SS 清理已停用 skill 產出物；同步更新 `README.md`、`檔案架構索引表.md`、`知識庫使用說明書.md` 與 §10 單元教材說明 | 停用教材已無維護價值，清理以精簡專案體積（~40 MB） |

### 獨立 repo 時期的變更紀錄（2026-10-29～11-11，原 exam-wiki-SD/CLAUDE.md CHANGELOG，原樣保留）

> 2026-10-29 以前的紀錄見 `archive/exam-wiki-SD-root/CLAUDE.md`；11-07 的 study 清理（刪 5 個單元舊版簡報與圖檔目錄）只記在 `wiki/queries/log.md`。

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-11-01 | **wiki 封存**：wiki/ 只保留 queries/，其餘（problems、concepts、methods、traps、philosophy、diagnosis、failure-modes、materials、code-ref、index.md、by-year.md）移至 `archive/wiki/`；`wiki/log.md` 移為 `wiki/queries/log.md`；ingest／compile-all／lint／add-concept 停用；方法論只在 raw/solutions/methods/ 維護 | wiki 為早期 AI 編譯之摘要、未逐頁核對（SS 科掃描 84 頁發現 45 項錯誤），且與 raw/solutions、study/ 重複，增加同步負擔 |
| 2026-11-01 | **廢止互動圖、移除補充筆記 PDF、儀表板優化、公式渲染修正**（比照 SS）：刪除 `raw/solutions/` 下 24 份 `*-viz.html` 與 1 份題目補充 PDF，清除 .md／problems-view 引用；`question_index.json` 移除 `hasViz`；`dashboard-data.js` 改 5 欄（`refresh-dashboard.ps1` 同步）；`index.html`「完整解析」改連 problems-view、刪「指令速查」分頁；新增 `scripts/render_problem_view.py` 並重新渲染 99 頁 problems-view | 互動圖與正本易不同步；problems-view 停在 09-02 版、10-05 勘誤未反映，且舊渲染吞掉 `\\`、`_`、`<` 等 |

---

## 10. 本科與根目錄規則的差異

> 原 repo 的規則在 11-01 已跟上 wiki 封存，但沒有跟上 11-02 以後的題目正本、解析勘誤例外與單元總覽。搬入時逐項比對，SD 規則多數已被根目錄涵蓋，或比根目錄窄（以根目錄為準）。
> 原 repo 規則原文見 `archive/exam-wiki-SD-root/`。以下只列仍屬 SD 專屬、待決或待辦的項目：

| 項目 | 根目錄 | SD |
|------|--------|----|
| 規則 1 例外範圍 | 五處例外（含解析勘誤四條件、題目正本） | 原 repo 只有兩處（`question_index.json`、methods），比根目錄窄，以根目錄為準 |
| 分類軸 | `designMethod`，各科固定幾個值 | 2026-11-11 已定四值並寫入索引（見 §3）；SD 另保留 `analysisMethod` 長描述（解析標頭 `**分析方法：**` 對應此欄，9 份缺標頭）。原 repo SPEC 的「設計法 USD／WSD」是 RC 殘留，不適用 |
| `raw/solutions/methods/` | 本科方法論 | **待使用者決定**：8 份全是 RC 方法論（effective-inertia-deflection、friction-loss-method、moment-magnifier-method、pm-interaction-diagram、prestress-loss-calculation、seismic-capacity-method、t-beam-analysis、whitney-stress-block-method），5 份與 `RC/raw/solutions/methods/` 完全相同、3 份是 RC 較舊版本；SD 解析與講義沒有任何一處引用。應是當初由 RC 複製建庫的殘留。建議刪除（RC 已有正本），SD 方法論日後再依 add method 補；決定前原樣保留 |
| 標籤詞彙 | 各科在 `SUBJECT.md` 列標準標籤 | 原 repo 標籤表是 RC 的，未搬入；SD 目前無標準詞彙（§3.2） |
| 分類稽核遺留 | 索引名稱＝大綱名稱；解析標頭主分類寫到子項 | 索引 `primaryTopicName` 7 筆是舊名（SD-2003-2～2003-5、2005-1、2005-2、2005-4，例「多自由度系統之動態分析及應用」≠ 大綱名）——屬索引欄位，**待使用者確認**後可直接改成大綱名；解析標頭只寫到單元層級 13 份（SD-2002-1～2005-4）、缺主分類 2 份（SD-2016-4、2016-5）——屬受保護的解析正本，等勘誤或補題目正本時一併處理 |
| 缺圖 | — | 解析引用但資料夾沒有：`SD-2008-3-chart-1.png`、`SD-2017-4-fig-1.png`（原 repo 即缺）；補圖時用 `scripts/extract_figure.py` 從考卷擷取 |
| 題目正本 | 解題前先寫 `-problem.md`、確認後凍結 | **待辦**：SD 99 題都還沒有題目正本；要補時用 exam-problem-split |
| 單元教材 | 單元總覽 `unit-SD-Un-m.html`（unit-overview） | **待使用者決定**：SD 仍是舊式——命題分析 `study-SD-*.html` 5 頁、給／背 `formula-given-SD-*.html` 5 頁（＋PDF）、觀念講義 `lecture-SD-*.html` 5 份（＋PDF），子項 U1-1、U1-2、U1-3、U2-2、U3-2；原已停用 skill 產出的記憶片 `study/recall-decks/` 5 組已於同日清理移除。要改成單元總覽時，逐子項建 `study/data/unit-SD-*.json` 後產生 |
| 頻率熱圖 | `build_frequency.py` v1.2（教材欄只認 `unit-*.html`） | 保留原 repo v1.1 頁（教材欄列命題分析／講義／給背／記憶片；記憶片偵測 `recall-decks/` 是原 repo 在地修改）。改成單元總覽**之前不要重產** `frequency-SD.html`；`--check` 可照常跑 |
| 題目瀏覽頁 | `render_problem_view.py` 由正本產生 | 99 頁保留原 repo 版（11-01 同一管線重生）。根目錄腳本已抽查相容（見 §9），勘誤後重產單題沒問題 |
| xcheck 封存區 | 根目錄 `scripts/xcheck.py` 註解說「舊目錄不存在時改掃封存處」，但判斷以執行目錄（根目錄）為準，五科在合併後**實際都沒掃到** `XX/archive/wiki/` | 原 repo 版（`archive/exam-wiki-SD-root/xcheck.py`）以科目資料夾為準，實測 SD A=3、SM A=2、SA A=7、RC A=23、SS A=0。**待使用者決定（五科通用）**：要不要掃已凍結的封存區；要掃就把 SD 版那三行併入根目錄，不掃就把根目錄註解改正 |
| 儀表板 | 五科共用樣板＋`scripts/refresh_dashboard.py`（`KB_*`） | **待辦**：暫用原 repo 的 `index.html`／`dashboard-data.js`（`SD_*`、5 欄格式，篩選選單由 `analysisMethod` 即時歸成 9 類）。要更新資料時在 `SD/` 下執行 `scripts/refresh-dashboard.ps1`（PowerShell，讀 `raw\json\` 相對路徑，優先讀 `analysisMethod`）；改回共用樣板前**不要**對 SD 執行 `refresh_dashboard.py`。分類軸已於 11-11 定案（§3），改用共用樣板的前提已具備，篩選會改成四值。根目錄 `index.html` 讀 `window[code+'_QUESTIONS']`，五科入口讀得到 SD 99 題 |
| 網站網址 | — | **待辦**：舊站 `yjc5760.github.io/exam-wiki-SD` 維持上線；新站上線後在舊站加轉址 |
| 起點頁 | `start.html`（exam-start-page） | 尚未建立 |
| 一次性腳本 | 共用腳本在根目錄 `scripts/` | `scripts/` 的 5 支講義附圖產生器＋`structdraw.py`（struct-diagram 的 primitives 副本，被 `lecture_*` 以同目錄 import）；在 `SD/` 下執行 |
| 影片 | — | `影片講義/` 5 份圖文講義（`video/` 約 199 MB，原 repo 即納入 git）；`解題過程影片/` 為 gitignore 的本機資料夾，原 repo 是空的，未建立 |
| `raw/exams/命題大綱.pdf`、`raw/json/pdf_*.txt` | 命題大綱正本在根目錄 | 原 repo 的副本與考卷文字抽取，屬 raw 證據，保留不動 |
