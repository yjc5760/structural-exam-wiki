# RC 科目設定（SUBJECT.md）— 鋼筋混凝土設計與預力混凝土設計

> 本檔是 **RC 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SOLVE.md`／`CLAUDE-SPEC.md` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`RC`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `RC`（RC & Prestressed Concrete Design） |
| 科目全名 | 鋼筋混凝土設計與預力混凝土設計 |
| 題號格式 | `RC-YYYY-N`（YYYY 為西元年，例 `RC-2015-1`） |
| 考卷檔名 | `raw/exams/RC-YYYY_鋼筋混凝土設計與預力混凝土設計.pdf` |
| 收錄範圍 | 尚未收錄（考卷放入 `raw/exams/` 後開始） |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立，2026-10-29 |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 |
|---------|------|------|
| `RC-U1-1` | RC 梁彎矩強度分析與設計 | 第一單元 |
| `RC-U1-2` | RC 柱強度分析與設計 | 第一單元 |
| `RC-U1-3` | 細長柱 | 第一單元 |
| `RC-U1-4` | 柱設計圖之應用 | 第一單元 |
| `RC-U2-1` | RC 剪力強度分析與設計 | 第二單元 |
| `RC-U2-2` | RC 扭力強度設計 | 第二單元 |
| `RC-U2-3` | 鋼筋錨定長度與斷點計算 | 第二單元 |
| `RC-U3-1` | 梁工作性要求（含撓度、裂縫） | 第三單元 |
| `RC-U3-2` | 樓版與基腳設計 | 第三單元 |
| `RC-U3-3` | 韌性要求與耐震設計 | 第三單元 |
| `RC-U4-1` | 預力梁斷面應力分析 | 第四單元 |
| `RC-U4-2` | 預力量與偏心量設計 | 第四單元 |
| `RC-U4-3` | 預力損失 | 第四單元 |
| `RC-U4-4` | 預力梁剪力分析與設計 | 第四單元 |

他科常見副考點：`SD-U3-1`、`SM-U2-1`

---

## 3. `designMethod` 欄位（本科分類軸：設計法）

| 允許值 |
|--------|
| `USD` |
| `WSD` |
| `概念題` |
| `混合` |

> USD＝強度設計法（含預力梁極限強度）；WSD＝工作應力法（含預力梁傳遞／使用階段之容許應力檢核）；概念題＝說明／比較題
>
> `unit-exam-intel` 的「設計法走向」區塊在本科改用上表的分類軸；儀表板篩選選項亦依此順序。

---

## 4. 圖解（struct-diagram）

解題或勘誤後需要圖解時，用 `struct-diagram` skill 以程式產生向量圖（SVG＋2× PNG），
腳本 `gen_RC-YYYY-N.py` 與 `figs/` 放在該題資料夾，`.md` 引用 SVG 相對路徑。
（互動圖 `*-viz.html` 功能已於 2026-10-29 停用。）

本科常見圖解：

- RC 斷面／應變／應力三聯圖
- P-M 交互曲線
- 梁三聯圖（載重／SFD／BMD）
- 預力斷面應力分佈與 Magnel 圖
- 鋼腱線形與偏心量

---

## 5. wiki 七層的本科解讀

Layer 1–4（concepts＋problems／philosophy／methods／diagnosis）五科相同；Layer 5–7 依科目性質調整，
**資料夾名稱維持不變**（skills 與 LINT 依資料夾名稱運作），只改顯示名稱與類別頁：

| 層 | 目錄 | 本科名稱 | 類別頁 |
|----|------|---------|--------|
| Layer 5 | `wiki/failure-modes/` | **失敗模式** | `flexural-failure` 撓曲破壞（拉力控制／過渡區／壓力控制）<br>`shear-torsion-failure` 剪力與扭力破壞<br>`bond-anchorage-failure` 握裹與錨定破壞<br>`serviceability-failure` 使用性失效（撓度／裂縫）<br>`prestress-failure` 預力構材應力超限與損失 |
| Layer 6 | `wiki/materials/` | **材料行為** | `concrete` 混凝土（應力應變、Whitney 應力塊、彈性模數）<br>`reinforcing-steel` 鋼筋（降伏、應變硬化、竹節與握裹）<br>`prestressing-steel` 預力鋼材（鋼絞線、鬆弛）<br>`time-dependent` 時間相依行為（潛變、乾縮） |
| Layer 7 | `wiki/code-ref/` | **規範條文對應** | （index.md 單頁） |

> LINT 第 14、15 項（類別頁齊全）以本表為準。

---

## 6. 題型診斷入口（`wiki/diagnosis/`）

| 題型 | 辨識關鍵字 | 診斷頁 |
|------|-----------|--------|
| 梁撓曲 | 單筋／雙筋、T 形梁、εt、φ 過渡區 | `wiki/diagnosis/beam-flexure.md` |
| 柱與細長柱 | P-M 互制、平衡點、彎矩放大 δns／δs | `wiki/diagnosis/column.md` |
| 剪力與扭力 | Vc、Vs、箍筋間距、Tth、閉合箍筋 | `wiki/diagnosis/shear-torsion.md` |
| 錨定與斷筋 | ld、彎鉤、搭接、斷點 | `wiki/diagnosis/development.md` |
| 使用性 | Ie、長期撓度 λΔ、裂縫控制鋼筋間距 | `wiki/diagnosis/serviceability.md` |
| 樓版與基腳 | 雙向版、穿孔剪力、單向剪力、基腳尺寸 | `wiki/diagnosis/slab-footing.md` |
| 耐震韌性 | 特殊抗彎矩構架、強柱弱梁、圍束箍筋、接頭剪力 | `wiki/diagnosis/seismic.md` |
| 預力梁 | 傳遞／使用階段應力、Magnel 圖、預力損失、fps | `wiki/diagnosis/prestressed.md` |

---

## 7. 主要規範／依據（Layer 7 的來源）

- 混凝土結構設計規範（內政部；以考卷年份適用版本為準，並對照 ACI 318）
- 建築物耐震設計規範及解說（韌性設計相關）
- 建築技術規則建築構造編

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。

---

## 8. 設計哲學框架（解題邏輯起始版）

> 起始版只列各子項的主幹流程，隨題目解析累積後擴充；SOLVE 時與根目錄 `CLAUDE-SOLVE.md`
> 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。

**USD 梁撓曲強度（RC-U1-1）**
```
核心：φMn ≥ Mu，先由應變相容判斷破壞型態，再決定 φ
步驟：① 假設拉力筋降伏，由 C = T 求 a = As·fy / (0.85 f'c b)
      ② c = a / β1；εt = 0.003 (dt − c) / c
      ③ εt ≥ 0.005 拉力控制（φ = 0.90）；εt ≤ εy 壓力控制；其間為過渡區（φ 線性內插）
      ④ Mn = As·fy (d − a/2)；雙筋梁另判斷壓力筋是否降伏
      ⑤ 檢核最少鋼筋量與最小 εt 規定
T 形梁：先判斷 a ≤ hf（矩形梁行為）或 a > hf（翼板＋腹板分開算）
```

**RC 柱與細長柱（RC-U1-2、RC-U1-3）**
```
核心：P-M 互制——在 εcu = 0.003 下改變中性軸深度 c，逐點求 (Mn, Pn)
關鍵點：純壓、平衡點（εs = εy）、拉力控制點（εt = 0.005）、純彎
細長柱：k·lu / r 判斷可否忽略細長效應 → 不可忽略時以彎矩放大法
        無側移 δns = Cm / (1 − Pu / 0.75Pc) ≥ 1.0；Pc = π²(EI)eff / (k lu)²
```

**剪力與扭力（RC-U2-1、RC-U2-2）**
```
核心：φVn = φ(Vc + Vs) ≥ Vu，φ = 0.75
步驟：① Vu 取支承面 d 處  ② Vc（依考卷年份規範版本；新版含尺寸效應與 ρw）
      ③ Vs = Av·fyt·d / s，並檢核 Vs 上限與最大箍筋間距  ④ 最少剪力筋
扭力：先比 Tu 與門檻扭力 Tth，超過才需設計；閉合箍筋 + 縱向扭力筋
```

**預力梁應力檢核（RC-U4-1、RC-U4-2）**
```
核心：f = −P/A ± P·e·y/I ∓ M·y/I，頂／底纖維 × 傳遞／使用兩階段 = 4 個不等式
傳遞階段：Pi + 自重；使用階段：Pe（= R·Pi）+ 全部載重
Magnel 圖：把 4 個不等式寫成 1/P 對 e 的直線，可行區即容許的 (P, e) 組合
```

**預力損失（RC-U4-3）**
```
瞬時損失：彈性縮短、錨碇滑動、摩擦（曲率＋擺動）
長期損失：潛變、乾縮、鋼材鬆弛
```

---

## 9. CHANGELOG（RC 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-10-29 | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
| 2026-10-29 | 停用互動圖（`*-viz.html`）；§4 改為 struct-diagram 圖解 | 靜態向量圖可重跑、可審核，與互動圖功能重疊 |
