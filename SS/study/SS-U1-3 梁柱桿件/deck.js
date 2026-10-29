const { newPres, titleSlide, topicMapSlide, formulaSlide, flowchartSlide, flowMapSlide,
        diagramSlide, cheatSheetSlide, trapSlide, tableSlide, closingSlide } = require("./lib.js");

const pres = newPres();
const FOOT = "鋼結構設計「梁柱桿件 Beam-Column」觀念講義｜原理 · 公式 · 向量圖解";

/* 1 */
titleSlide(pres, {
  kicker: "SS · 鋼結構設計｜觀念講義",
  title: "梁柱桿件 Beam-Column",
  subtitle: "全鋼結構唯一「內力會自己長大」的構材 —— 掌握兩條腿的解題骨架，規範公式就不會迷路",
  tag: "核心考點",
  footer: FOOT,
});

/* 2 */
topicMapSlide(pres, {
  eyebrow: "TOPIC MAP",
  title: "本單元的四個區塊",
  topics: [
    { title: "一、物理本質", desc: "P 與 δ 同時存在 → 額外彎矩 P·δ → 回饋迴圈 → 收斂成放大係數 1/(1−P/Pcr)。" },
    { title: "二、左腿：需求側", desc: "一階內力 Mnt、Mlt 經 B₁（構件自彎）與 B₂（整層側移）放大，得到 Mu。" },
    { title: "三、右腿：強度側", desc: "φcPn、φbMnx、φbMny 全部複用壓桿與梁桿單元的成果，不教新觀念。" },
    { title: "四、兩腿會合", desc: "P-M 互制式計算「斷面能力被吃掉幾成」；ASD 走同一骨架但要驗兩條式子。" },
  ],
});

/* 3 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "為什麼只有梁柱需要「放大」，純柱與純梁不用？",
  diagram: "bc-fig-1-three-members",
  insights: [
    "純柱只有 P，桿身保持直線，δ = 0 → P×δ = 0，內力不會自我增長。",
    "純梁只有 δ，沒有軸力可乘 → P×δ = 0，一階彎矩就是最終答案。",
    "梁柱同時有 P 與 δ，乘積不為零：彎矩造成變形、變形又回餵更多彎矩。",
    "所以本單元真正的新東西只有一個 —— 把一階彎矩放大的係數。",
  ],
  note: "記住這張圖，就不會再問「這題到底要不要算 B₁」——只要柱子同時受壓又有彎矩，就要。",
});

/* 4 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 二階效應的本質",
  title: "放大係數不是規範硬塞的，而是一個級數的和",
  formulas: [
    { label: "軸力乘上側向位移，產生額外彎矩", math: "f_dm" },
    { label: "每一圈的增量都是前一圈的 α = P/Pcr 倍，形成幾何級數", math: "f_series" },
    { label: "級數收斂的結果，就是二階放大係數", math: "f_amp" },
  ],
  note: "因為 α ≥ 0，級數各項皆為正，放大只會往上不會往下 —— 這就是規範規定 B₁、B₂ 恆 ≥ 1.0 的原因。",
});

/* 5 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "無窮迴圈怎麼會收斂成一個乾淨的分式？",
  diagram: "bc-fig-2-amplification",
  insights: [
    "左圖：每疊代一圈，增量縮小為前一圈的 α 倍，四圈後已逼近 1.667 Mnt。",
    "右圖：α → 1（軸力逼近挫屈載重）時分母趨近 0，放大係數發散 → 這就是挫屈的數學形式。",
    "α = 0.8 時彎矩已被放大 5 倍：軸力比是梁柱題最敏感的輸入。",
    "考場檢查：算出的 B 若小於 1.0 或為負，必定是 Pu/Pe 代錯或超過 1。",
  ],
});

/* 6 */
diagramSlide(pres, {
  eyebrow: "SOLVING FRAMEWORK · 解題骨架",
  title: "進考場的第一個動作：在紙上畫出左右兩欄",
  diagram: "bc-fig-3-two-legs",
  note: "兩欄法的價值在於「不會漏」：左欄漏了 B₂、右欄漏了弱軸上限，在會合前就會看出缺格。",
});

/* 7 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 需求側總式",
  title: "左腿的終點：設計需求內力",
  formulas: [
    { label: "設計彎矩 —— 兩個放大係數各自作用在對應的一階彎矩上", math: "f_mu" },
    { label: "設計軸力 —— 側移分量同樣要被 B₂ 放大", math: "f_pu" },
  ],
  note: "Mnt = no translation（節點不平移時的一階彎矩）；Mlt = lateral translation（側移造成的一階彎矩）。"
      + "兩者的來源不同，放大係數當然也不同 —— 這是整個單元的分水嶺。",
});

/* 8 */
flowchartSlide(pres, {
  eyebrow: "OVERVIEW · 構架型式判斷",
  title: "先判構架行為，才知道 K 值怎麼取、要不要算 B₂",
  stages: [
    { type: "step", text: "① 讀題：這個構架有沒有斜撐／剪力牆／核心筒？" },
    {
      type: "decision", question: "節點能不能相對側移？",
      branches: [
        { label: "不能（有斜撐．無側移構架）", text: "M_lt = 0，整題只需要 B₁\n有效長度 K = 1.0（非側移模式）\nB₂ 完全用不到" },
        { label: "能（無斜撐．有側移構架）", text: "把一階內力拆成 M_nt 與 M_lt\nB₁ 仍用 K = 1.0\nB₂ 用對位圖查得的側移 K（> 1.0）" },
      ],
    },
    { type: "result", text: "得到 Mu = B₁·Mnt + B₂·Mlt，左腿完成" },
  ],
  note: "「一支柱同時有兩個 K」不是矛盾，而是兩種二階效應各自對應一種變形模式。",
});

/* 9 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 左腿（一）",
  title: "B₁：構件自彎的 P-δ 效應",
  formulas: [
    { label: "構件放大係數（恆 ≥ 1.0）", math: "f_b1" },
    { label: "構件的尤拉載重 —— 有效長度一律取非側移模式", math: "f_pe1" },
  ],
  note: "Pe1 的 K₁ 一律取 1.0。把對位圖查來的側移 K 代進 Pe1 是本單元最高頻的失分點。",
});

/* 10 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "B₁ 在放大什麼？——桿件相對「自己的弦線」鼓出來的量",
  diagram: "bc-fig-4-b1-member",
  insights: [
    "δ 的定義是「桿身相對兩端連線（弦線）的偏移」，與弦線本身有沒有傾斜無關。",
    "所以即使整層完全不側移（有斜撐），B₁ 仍然存在、仍然要算。",
    "因為端點不平移，Pe1 的有效長度用非側移模式：K = 1.0。",
    "有斜撐構架 Mlt = 0，整題只要 B₁；這是最好拿分的題型。",
  ],
});

/* 11 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 左腿（一）",
  title: "Cm：等值均勻彎矩係數，決定 B₁ 折不折減",
  formulas: [
    { label: "兩端有彎矩、桿間無橫向載重時", math: "f_cm" },
    { label: "桿間有橫向載重時（依端部束制狀況取用）", math: "f_cm2" },
  ],
  note: "符號規則：單曲率（C 型）M₁/M₂ 取負 → Cm 變大（最危險，不折減）；雙曲率（S 型）取正 → Cm 變小（可大幅折減）。",
});

/* 12 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "為什麼雙曲率可以折減？Cm 其實在問「同不同步」",
  diagram: "bc-fig-5-cm-curvature",
  insights: [
    "單曲率：彎矩全段同號，最大 δ 恰好落在彎矩也大的位置 → P·δ 完全疊加，不折減。",
    "雙曲率：彎矩沿桿變號、中央過零，而 δ 最大的地方彎矩接近 0 → 兩者不同步，可折減。",
    "同一支桿、同一個 Pu，Cm 從 1.0 變成 0.2，B₁ 直接差 5 倍。",
    "判斷訣竅：畫出變形形狀，C 型取負、S 型取正，不要背符號表。",
  ],
});

/* 13 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 左腿（二）",
  title: "B₂：整層側移的 P-Δ 效應",
  formulas: [
    { label: "樓層放大係數 —— 注意 Σ 是「整個樓層」", math: "f_b2" },
    { label: "側移模式的尤拉載重（K₂ 由對位圖查得，恆 > 1.0）", math: "f_pe2" },
    { label: "等效寫法：用一階側移量 Δoh 與樓層剪力直接算", math: "f_b2alt" },
  ],
  note: "B₁ 的 Pu、Pe1 屬於「這一支桿」；B₂ 的 ΣPu、ΣPe2 屬於「這一層樓」。層與桿混用是本單元最大宗的失分點。",
});

/* 14 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "靠桿（重力柱）為什麼只進分子、不進分母？",
  diagram: "bc-fig-6-b2-story-leaning",
  insights: [
    "靠桿兩端鉸接，提供不了任何抗側勁度 → 不列入分母 ΣPe2。",
    "但它的重力必須由抗側系統拉住才不會倒 → 重量要算進分子 ΣPu。",
    "本例漏算靠桿，B₂ 從 1.171 掉到 1.091，彎矩低估 6.8%，而且是偏不安全的方向。",
    "考場檢查：分子的柱數應該等於整層柱數，分母只數抗側構架的柱。",
  ],
});

/* 15 */
tableSlide(pres, {
  eyebrow: "KNOWLEDGE CARD · 對照表",
  title: "B₁ 與 B₂ 的七個關鍵差異（背這張就夠）",
  header: ["比較項目", "B₁（P-δ．構件自彎）", "B₂（P-Δ．整層側移）"],
  colW: [2.1, 5.0, 5.0],
  rows: [
    ["作用對象", "單一構件，相對自身弦線的鼓出", "整個樓層，所有柱一起側移"],
    ["有效長度 K", "非側移模式，實務一律取 K = 1.0", "側移模式，由對位圖查得，K > 1.0"],
    ["分子軸力", "該支桿自己的 Pu", "ΣPu：全樓層柱的軸力，含鉸接靠桿"],
    ["分母尤拉載重", "Pe1 = π²EI /(1.0·L)²，單桿", "ΣPe2：只計抗側系統提供的勁度"],
    ["折減係數", "有 Cm = 0.6 − 0.4(M₁/M₂)", "無 Cm，整層一起放大"],
    ["何時不必算", "恆須計算（只要有 Pu 與 M）", "無側移構架 Mlt = 0 時用不到"],
    ["常見錯誤", "誤用側移 K 去算 Pe1", "漏算靠桿重量；把單桿當成整層"],
  ],
});

/* 16 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 右腿（一）",
  title: "強度側：軸壓強度 φcPn（完全複用壓桿單元）",
  formulas: [
    { label: "設計軸壓強度", math: "f_pn" },
    { label: "細長參數 —— 強弱軸各算一次，取較大的 KL/r 控制", math: "f_lamc" },
    { label: "非彈性挫屈（含殘留應力效應）", math: "f_fcr1" },
    { label: "彈性挫屈（Euler）", math: "f_fcr2" },
  ],
  note: "右腿不教新觀念，只是把 U1-1（壓桿）與 U1-2（梁桿）的成果搬過來用。時間不足時，右腿要算得又快又穩。",
});

/* 17 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "柱曲線的兩段式從哪裡分界？λc = 1.5",
  diagram: "bc-fig-7-column-curve",
  insights: [
    "λc ≤ 1.5：短粗柱，殘留應力使斷面提早局部降伏 → 用 0.658 的指數式。",
    "λc > 1.5：細長柱，破壞前仍在彈性 → 回到 Euler 的 0.877/λc²（0.877 是初始偏心折減）。",
    "本例 Fy = 2.5 tf/cm² 時分界落在 KL/r ≈ 135，可當作快速判斷的心算值。",
    "強弱軸都要算 KL/r，但只有較大者控制 φcPn；另一軸的 I 會回頭決定 B₁ 的 Pe1。",
  ],
});

/* 18 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 右腿（二）",
  title: "強度側：強軸看 LTB，弱軸看形狀因數上限",
  formulas: [
    { label: "強軸．塑性區段（Lb ≤ Lp）", math: "f_mp" },
    { label: "強軸．非彈性 LTB（Lp < Lb ≤ Lr）直線內插", math: "f_mltb" },
    { label: "弱軸．沒有 LTB，但受矩形形狀因數上限控制", math: "f_mny" },
  ],
  note: "題目同時給你 Zy 與 Sy，就是在提示 1.5FySy 這個上限要檢查 —— 這是弱軸最常被漏掉的一刀。",
});

/* 19 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "Lb 落在哪一段，決定 Mn 用哪一條式子",
  diagram: "bc-fig-8-ltb-zones",
  insights: [
    "Lb ≤ Lp：側撐夠密，斷面可完全塑化 → Mn = Mp，與 Lb 無關（水平段）。",
    "Lp < Lb ≤ Lr：部分斷面已因殘留應力降伏 → 在 Mp 與 Mr 之間直線內插。",
    "Lb > Lr：彈性側向扭轉挫屈，Mn 隨 Lb 快速衰減（曲線段）。",
    "弱軸沒有這三段 —— 弱軸不會側傾，直接由 min(FyZy, 1.5FySy) 控制。",
  ],
});

/* 20 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 兩腿會合",
  title: "P-M 互制方程式：先判區間，再選式子",
  formulas: [
    { label: "第一步永遠是判斷軸力比落在哪一區", math: "f_h1cond" },
    { label: "軸力主控（彎矩項乘 8/9）", math: "f_h1a" },
    { label: "彎矩主控（軸力項乘 1/2）", math: "f_h1b" },
  ],
  note: "兩式在 Pu/φcPn = 0.2 處數值連續（皆為 0.90），是同一條包絡線的兩段，不是兩個獨立檢核。",
});

/* 21 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "互制式在量什麼？——斷面能力被吃掉的百分比",
  diagram: "bc-fig-9-pm-interaction",
  insights: [
    "縱軸是軸力用掉的比例，橫軸是彎矩用掉的比例；落在包絡線內就是安全。",
    "軸力大時彎矩項權重 8/9（較嚴），軸力小時軸力項權重只有 1/2（較寬）。",
    "選錯式子，彎矩項的權重會差 1.8 倍（8/9 對 1/2），答案直接錯一個量級。",
    "利用率正常落在 0.8 ~ 1.0；算出 0.2 或 3.0 幾乎都是單位或放大係數出錯。",
  ],
});

/* 22 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 自我檢查",
  title: "雙軸彎矩題：B₁x 與 B₁y 為什麼絕對不能共用？",
  diagram: "bc-fig-10-weak-vs-strong",
  insights: [
    "Pe1 正比於 I，所以弱軸的 Pe1 只有強軸的 Iy/Ix 倍（本例 0.336）。",
    "同樣的 Pu，弱軸的軸力比 0.743 遠高於強軸的 0.250 → B₁y = 3.90 vs B₁x = 1.33。",
    "1/(1−α) 是非線性的，軸力比差 3 倍，放大倍率會差得更多（本例 2.9 倍）。",
    "考場自我檢查：算完後確認 Pe1y / Pe1x 是否剛好等於 Iy / Ix，不等就是代錯 I。",
  ],
});

/* 23 */
formulaSlide(pres, {
  eyebrow: "FORMULA · ASD 對照",
  title: "ASD 走同一骨架，但必須驗兩條式子",
  formulas: [
    { label: "① 穩定式（中段控制）—— 放大倍率藏在分母裡", math: "f_asd1" },
    { label: "② 強度式（端部控制）—— 端部無二階彎矩，但要防斷面降伏", math: "f_asd2" },
    { label: "ASD 的尤拉應力（注意是 rb：彎曲平面內的迴轉半徑）", math: "f_fe" },
  ],
  note: "只驗穩定式而漏掉端部強度式，是 ASD 題最典型的扣分方式；fa/Fa ≤ 0.15 時才可用簡化式 fa/Fa + fb/Fb ≤ 1.0。",
});

/* 24 */
tableSlide(pres, {
  eyebrow: "KNOWLEDGE CARD · 對照表",
  title: "LRFD 與 ASD：同一個骨架的兩種寫法",
  header: ["比較項目", "LRFD（極限設計法）", "ASD（許用應力法）"],
  colW: [2.2, 4.9, 5.0],
  rows: [
    ["放大的對象", "放大彎矩：Mu = B₁Mnt + B₂Mlt", "放大應力項：Cm /(1 − fa/F'e)"],
    ["檢核式數量", "一式（H1-1a 或 H1-1b 擇一）", "兩式都要：穩定式 ＋ 強度式"],
    ["穩定（中段）", "已含在 H1-1 之中", "fa/Fa + Cm·fb /[(1 − fa/F'e)Fb] ≤ 1.0"],
    ["強度（端部）", "由放大後的 Mu 直接反映", "fa/(0.6Fy) + fb/Fb ≤ 1.0"],
    ["小軸力的處理", "Pu/φcPn < 0.2 改用 H1-1b", "fa/Fa ≤ 0.15 可用簡化式"],
    ["二階項的來源", "B₁（Pe1）、B₂（ΣPe2）", "F'e = 12π²E /[23(KL/rb)²]"],
  ],
});

/* 25 */
flowMapSlide(pres, {
  eyebrow: "SOLUTION FLOW",
  badge: "流",
  title: "實戰解題流：從題目到利用率",
  subtitle: "左腿與右腿平行推進，最後在 P-M 互制式會合",
  tag: "SS · Beam-Column",
  cols: 5,
  nodes: [
    { text: "梁柱題目", type: "start" },
    { text: "一階分析\nMnt, Mlt, Pu", type: "step" },
    { text: "有無側撐？", type: "decision" },
    { fork: [
      { text: "有撐：Mlt = 0\n只需要算 B₁", tint: "blue" },
      { text: "無撐：Mnt / Mlt 拆開\nB₁ 與 B₂ 都要算", tint: "pink" },
    ] },
    { text: "判單/雙曲率 → Cm\nPe1 (K=1.0) → B₁", type: "step" },
    { text: "ΣPu / ΣPe2\n（側移 K）→ B₂", type: "step" },
    { text: "Mu = B₁Mnt\n+ B₂Mlt", type: "step" },
    { text: "φcPn：KL/r\n取較大者控制", type: "step" },
    { text: "φbMnx（LTB 三段）\nφbMny（1.5FySy）", type: "step" },
    { text: "Pu/φcPn\n≥ 0.2 ？", type: "decision" },
  ],
  result: { text: "H1-1a 或 H1-1b\n利用率 ≤ 1.0" },
  sideNote: {
    title: "雙軸彎矩分支",
    text: "Mux 與 Muy 必須各自用 B₁x、B₁y 放大；弱軸 Pe1 小，放大倍率遠大於強軸，不可共用一個 B₁。",
    color: "pink",
  },
  checklist: {
    title: "交卷前的三個驗證",
    items: [
      { label: "K 值沒混用", detail: "Pe1 用 K=1.0，Pe2 才用側移 K" },
      { label: "靠桿有算進 ΣPu", detail: "分子含全樓層，分母只含抗側" },
      { label: "利用率量級合理", detail: "正常落在 0.8 ~ 1.0" },
    ],
  },
});

/* 26 */
cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查",
  title: "梁柱桿件｜全公式一頁速查",
  items: [
    { label: "設計彎矩", math: "f_mu" },
    { label: "B₁ 構件放大", math: "f_b1" },
    { label: "Pe1（K = 1.0）", math: "f_pe1" },
    { label: "Cm 係數", math: "f_cm" },
    { label: "B₂ 樓層放大", math: "f_b2" },
    { label: "Pe2（側移 K）", math: "f_pe2" },
    { label: "雙軸自我檢查", math: "f_check" },
    { label: "軸壓強度", math: "f_pn" },
    { label: "非彈性挫屈", math: "f_fcr1" },
    { label: "彈性挫屈", math: "f_fcr2" },
    { label: "強軸塑性", math: "f_mp" },
    { label: "非彈性 LTB", math: "f_mltb" },
    { label: "弱軸上限", math: "f_mny" },
    { label: "H1-1a 軸力主控", math: "f_h1a" },
    { label: "H1-1b 彎矩主控", math: "f_h1b" },
    { label: "ASD 穩定式", math: "f_asd1" },
  ],
});

/* 27 */
trapSlide(pres, {
  eyebrow: "REVIEW",
  title: "高頻陷阱精選：這六個一定要在考場上想起來",
  traps: [
    { title: "把側移 K 拿去算 Pe1", desc: "Pe1 一律取 K = 1.0（非側移模式）。對位圖查來的側移 K（> 1.0）只屬於 B₂ 的 Pe2。同一支柱有兩個 K 是正常的。" },
    { title: "Cm 的 M₁/M₂ 符號代反", desc: "單曲率（C 型）取負 → Cm 變大、不折減；雙曲率（S 型）取正 → Cm 變小。先畫變形形狀再判符號，不要背表。" },
    { title: "B₂ 的 Σ 只算了抗側柱", desc: "分子 ΣPu 必須含鉸接靠桿（重力柱）的軸力；分母 ΣPe2 才只計抗側系統。漏算靠桿會低估彎矩，方向偏不安全。" },
    { title: "弱軸忘了 1.5FySy 上限", desc: "弱軸沒有側向扭轉挫屈，但受矩形形狀因數上限控制。題目同時給 Zy 與 Sy，就是在提示你必須取 min(FyZy, 1.5FySy)。" },
    { title: "雙軸彎矩共用一個 B₁", desc: "弱軸 Pe1 小得多，同樣的 Pu 會吃掉更高比例，B₁y 往往是 B₁x 的好幾倍。務必分開算，並檢查 Pe1y/Pe1x = Iy/Ix。" },
    { title: "ASD 只驗了穩定式", desc: "端部強度式 fa/(0.6Fy) + fb/Fb ≤ 1.0 也必須檢核。端部雖無二階彎矩，但要防止端部斷面直接降伏。" },
  ],
});

/* 28 */
closingSlide(pres, {
  title: "梁柱桿件｜重點回顧",
  points: [
    "梁柱是全鋼結構唯一「內力會自己長大」的構材：P 與 δ 同時存在，一階彎矩不能直接用。",
    "左腿需求側：B₁ 管構件自彎（K = 1.0、有 Cm），B₂ 管整層側移（側移 K、Σ 含靠桿）。",
    "右腿強度側完全複用壓桿（φcPn）與梁桿（φbMnx、φbMny）單元，沒有新觀念，只求快而穩。",
    "兩腿只在 P-M 互制式會合：先判 Pu/φcPn 是否 ≥ 0.2，再選 H1-1a 或 H1-1b。",
    "ASD 骨架相同，但穩定式（中段）與強度式（端部）兩條都要驗，缺一不可。",
  ],
});

pres.writeFile({ fileName: "SS_梁柱桿件_Beam-Column_觀念講義.pptx" })
  .then(() => console.log("deck written"));
