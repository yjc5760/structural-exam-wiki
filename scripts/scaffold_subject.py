#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaffold_subject.py — 依 SS 的架構建立新科目資料夾骨架

科目名稱／單元／子項取自根目錄 syllabus_taxonomy.json；科目專屬設定（考卷檔名、
designMethod 允許值、互動圖內容碼、wiki 第 5–7 層類別、題型診斷頁）取自
scripts/subject_profiles.json。

只建立不存在的檔案，**絕不覆蓋既有檔案**（可安全重跑，用來補齊缺漏）。

用法（在知識庫根目錄執行）：
    python scripts/scaffold_subject.py RC
    python scripts/scaffold_subject.py RC SA SD SM
    python scripts/scaffold_subject.py RC --dry-run
"""
import argparse, datetime, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
REF = "SS"  # 架構範本科目（katex 等共用資源從這裡複製）

DIRS = [
    "raw/exams", "raw/json", "raw/solutions/methods",
    "wiki/problems", "wiki/concepts", "wiki/methods", "wiki/philosophy", "wiki/traps",
    "wiki/topics", "wiki/diagnosis", "wiki/failure-modes", "wiki/materials", "wiki/code-ref",
    "wiki/queries", "study/problems-view", "study/figs-src", "scripts",
]
KEEP = ["raw/exams", "raw/solutions/methods", "wiki/problems", "wiki/methods",
        "study/problems-view", "study/figs-src"]

# ---------------------------------------------------------------- 設計哲學框架（起始版）
PHILO = {
"RC": r"""
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
""",
"SA": r"""
**穩定性與靜不定度（SA-U1-1）**
```
平面剛架：r = (3m + R) − 3j − (內部釋放數)；平面桁架：r = (m + R) − 2j
r < 0 → 不穩定；r ≥ 0 仍須檢查幾何不穩定（反力共點、平行、機構）
```

**力法：諧合變位／最小功（SA-U2-1、SA-U2-2）**
```
步驟：① 選多餘力 X，得到靜定的釋放結構
      ② 求 δ10（外載）與 δ11（單位多餘力），可用虛功或單位載重法
      ③ 諧合方程 δ10 + δ11·X = Δ（支承沉陷、溫度時 Δ 不為 0）
      ④ 疊加求全部內力；最小功法 ∂U/∂X = 0 與此等價
```

**位移法：傾角變位（SA-U2-3）**
```
M_AB = (2EI/L)(2θA + θB − 3ψ) + FEM_AB
未知數：節點轉角 θ ＋ 側移 Δ；方程式：節點彎矩平衡 ＋ 層剪力平衡
```

**彎矩分配法（SA-U2-5）**
```
DF = k / Σk；遠端固定 k = 4EI/L、傳遞係數 1/2；遠端鉸接 k = 3EI/L、不傳遞
有側移：先鎖住側移分配，再以假設側移的修正彎矩疊加
```

**矩陣分析（SA-U2-4）**
```
{F} = [K]{D}；構件勁度由局部座標轉整體座標 [T]ᵀ[k][T]，組裝後依邊界條件劃分求解
```

**影響線（SA-U1-3）**
```
Müller-Breslau 原理：解除欲求量對應的束制、施加單位變位，變形形狀即影響線
靜定結構 → 直線段；靜不定結構 → 曲線（需先求變形形狀）
```
""",
"SD": r"""
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
""",
"SM": r"""
**土壤基本性質（SM-U1-1）**
```
S·e = w·Gs；γ = (Gs + S·e) γw / (1 + e)；γ' = γsat − γw
先畫三相圖，再用已知量逐一補齊
```

**有效應力與滲流（SM-U1-2）**
```
σ' = σ − u；Darcy：q = k·i·A
流線網：q = k·H·Nf / Nd；臨界水力坡降 icr = γ' / γw（砂湧／管湧檢核）
```

**壓密（SM-U1-3）**
```
正常壓密：Sc = Cc·H / (1 + e0) · log(σ'f / σ'0)
過壓密：先以 Cs 算到 σ'c，再以 Cc 算超過的部分
時間：Tv = cv·t / Hdr²（雙向排水 Hdr = H/2）
```

**剪力強度（SM-U1-5）**
```
τf = c' + σ' tan φ'；三軸試驗依 UU／CU／CD 區分總應力與有效應力路徑
```

**淺基礎（SM-U2-1）**
```
qu = c·Nc·sc·dc·ic + q·Nq·sq·dq·iq + 0.5γ·B·Nγ·sγ·dγ·iγ
偏心：有效寬度 B' = B − 2e；地下水位修正 γ 與 q；FS = qu / q
```

**側向土壓與擋土結構（SM-U3-1、SM-U3-2）**
```
Rankine：Ka = tan²(45° − φ/2)、Kp = tan²(45° + φ/2)；Coulomb 考慮牆背摩擦
擋土牆：滑動 FS、傾倒 FS、基底承載力三項檢核
```

**邊坡（SM-U3-3）**
```
無限邊坡（無凝聚、無滲流）FS = tan φ / tan β；有限邊坡用切片法（Fellenius／Bishop）
```
""",
}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def wr(path, text, made, dry):
    if os.path.exists(path):
        return
    made.append(path)
    if dry:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.lstrip("\n"))


def scaffold(code, dry=False):
    tax = load(os.path.join(ROOT, "syllabus_taxonomy.json"))
    subj = next((s for s in tax["subjects"] if s["id"] == code), None)
    if subj is None:
        sys.exit(f"錯誤：syllabus_taxonomy.json 沒有科目 {code}")
    prof = load(os.path.join(ROOT, "scripts", "subject_profiles.json"))["subjects"].get(code)
    if prof is None:
        sys.exit(f"錯誤：scripts/subject_profiles.json 沒有科目 {code}，請先補上設定")
    name, units = subj["name"], subj["units"]
    items = [(it["id"], it["name"], u) for u in units for it in u["items"]]
    base = os.path.join(ROOT, code)
    made = []
    for d in DIRS:
        if not dry:
            os.makedirs(os.path.join(base, d), exist_ok=True)
    for d in KEEP:
        wr(os.path.join(base, d, ".gitkeep"), "", made, dry)
    P = lambda *a: os.path.join(base, *a)
    lay = prof["layers"]
    exam = f"raw/exams/{code}-YYYY_{prof['examFile']}.pdf"

    # ---------------------------------------------------------- SUBJECT.md
    unit_rows = "\n".join(f"| `{i}` | {n} | {u['name']} |" for i, n, u in items)
    meth_rows = "\n".join(f"| `{m}` |" for m in prof["methods"])
    viz_rows = "\n".join(f"| `{k}` | {v} | `{code}-YYYY-N-{k}-viz.html` |" for k, v in prof["viz"].items())
    lrows = []
    for n, key in [(5, "failure-modes"), (6, "materials"), (7, "code-ref")]:
        L = lay[key]
        pages = "<br>".join(f"`{p}` {t}" for p, t in L["pages"].items()) or "（index.md 單頁）"
        lrows.append(f"| Layer {n} | `wiki/{key}/` | **{L['title']}** | {pages} |")
    diag_rows = "\n".join(f"| {v[0]} | {v[1]} | `wiki/diagnosis/{k}.md` |" for k, v in prof["diagnosis"].items())
    codes = "\n".join(f"- {c}" for c in prof["codes"])
    rel = "、".join(f"`{t}`" for t in prof.get("relatedTopics", [])) or "（無）"
    wr(P("SUBJECT.md"), f"""
# {code} 科目設定（SUBJECT.md）— {name}

> 本檔是 **{code} 科的科目層設定**。工作流程、重要規則、指令與格式規範一律以知識庫根目錄的
> `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SOLVE.md`／`CLAUDE-SPEC.md` 為準；
> 根目錄文件中的 `XX` 在本科一律代換成 **`{code}`**。
> 科目名稱與單元劃分以根目錄 `syllabus_taxonomy.json` 為唯一依據；本檔的科目專屬設定與
> `scripts/subject_profiles.json` 同步維護。

---

## 1. 基本資料

| 項目 | 內容 |
|------|------|
| 科目代碼 | `{code}`（{subj.get('nameEn', '')}） |
| 科目全名 | {name} |
| 題號格式 | `{code}-YYYY-N`（YYYY 為西元年，例 `{code}-2015-1`） |
| 考卷檔名 | `{exam}` |
| 收錄範圍 | 尚未收錄（考卷放入 `raw/exams/` 後開始） |
| 架構範本 | 依 `SS/`（鋼結構設計）的架構建立，{TODAY} |

---

## 2. 命題大綱子項（primaryTopicId／secondaryTopicIds 的合法值）

| topicId | 子項 | 單元 |
|---------|------|------|
{unit_rows}

他科常見副考點：{rel}

---

## 3. `designMethod` 欄位（本科分類軸：{prof['methodAxis']}）

| 允許值 |
|--------|
{meth_rows}

> {prof.get('methodNotes', '')}
>
> `unit-exam-intel` 的「設計法走向」區塊在本科改用上表的分類軸；儀表板篩選選項亦依此順序。

---

## 4. 互動圖內容碼（`*-viz.html`）

| 內容碼 | 圖形 | 檔名範例 |
|--------|------|---------|
{viz_rows}

---

## 5. wiki 七層的本科解讀

Layer 1–4（concepts＋problems／philosophy／methods／diagnosis）五科相同；Layer 5–7 依科目性質調整，
**資料夾名稱維持不變**（skills 與 LINT 依資料夾名稱運作），只改顯示名稱與類別頁：

| 層 | 目錄 | 本科名稱 | 類別頁 |
|----|------|---------|--------|
{chr(10).join(lrows)}

> LINT 第 14、15 項（類別頁齊全）以本表為準。

---

## 6. 題型診斷入口（`wiki/diagnosis/`）

| 題型 | 辨識關鍵字 | 診斷頁 |
|------|-----------|--------|
{diag_rows}

---

## 7. 主要規範／依據（Layer 7 的來源）

{codes}

> ⚠️ 規範版本以「考卷年份當時適用的版本」為準；新舊版差異在解析 §5 或 §6 註明。

---

## 8. 設計哲學框架（解題邏輯起始版）

> 起始版只列各子項的主幹流程，隨題目解析累積後擴充；SOLVE 時與根目錄 `CLAUDE-SOLVE.md`
> 的三層掃描法一起使用。內容若與考卷所附公式或適用規範牴觸，以考卷與規範為準。
{PHILO.get(code, chr(10) + '（待補）' + chr(10))}
---

## 9. CHANGELOG（{code} 科）

| 日期 | 變更 | 原因 |
|------|------|------|
| {TODAY} | 依 SS 架構建立科目骨架（`scripts/scaffold_subject.py`） | 五科合併為單一知識庫，架構統一 |
""", made, dry)

    # ---------------------------------------------------------- README.md
    wr(P("README.md"), f"""
# {code} — {name}考古題知識庫

**科目：** 專門職業及技術人員高等考試結構工程技師 — {name}
**收錄範圍：** 尚未收錄
**題目編號：** `{code}-YYYY-N`（如 `{code}-2015-1` = 2015 年第 1 題）

> 本資料夾是「結構技師考試知識庫」五科之一，架構與 `SS/` 相同。
> 流程與規則見根目錄 `CLAUDE.md`；本科專屬設定見 **`SUBJECT.md`**。

---

## 如何開始

```
1. 把考卷 PDF 放進 raw/exams/，命名 {code}-YYYY_{prof['examFile']}.pdf
2. 對 Cowork 說：「解析 YYYY 年 {code} 考卷」
3. 依提醒截圖題目附圖，存入 raw/solutions/{code}-YYYY-N/{code}-YYYY-N-fig-1.png
4. 告知 Cowork「截圖完成，請開始解題」（一次解一題）
5. 人工驗算後：「將 {code}-YYYY-N 的 verificationStatus 改為 verified」
6. 「ingest {code}-YYYY-N」→ wiki 自動更新
7. 「更新儀表板資料」→ index.html 題庫同步
```

## 快速導航

| 我想找... | 去哪找 |
|----------|-------|
| 視覺化瀏覽 | 雙擊 `index.html` |
| 科目設定（單元、設計法欄位、七層解讀） | `SUBJECT.md` |
| 題目解析 | `raw/solutions/{code}-YYYY-N/{code}-YYYY-N.md` |
| wiki 主導航 | `wiki/index.md` |
| 命題大綱分類 | `wiki/topics/index.md` |
| 題型診斷 | `wiki/diagnosis/index.md` |
| 操作紀錄 | `wiki/log.md` |
""", made, dry)

    # ---------------------------------------------------------- 檔案架構索引表.md
    wr(P("檔案架構索引表.md"), f"""
# {code}　檔案架構索引表

> 即時統計請對 Cowork 說 `status {code}`。目錄結構與 `SS/` 相同，說明見根目錄 `CLAUDE.md`。

```
{code}/
├── SUBJECT.md          ← 科目層設定（單元表、designMethod、七層解讀、設計哲學、CHANGELOG）
├── README.md
├── index.html          ← 儀表板（五科共用樣板 scripts/templates/dashboard-index.html）
├── dashboard-data.js   ← python scripts/refresh_dashboard.py {code}
├── scripts/build_frequency.py
├── raw/
│   ├── exams/          ← {code}-YYYY_{prof['examFile']}.pdf
│   ├── json/           ← question_index.json ✏️、concepts.json、syllabus_taxonomy.json（副本，勿改）
│   └── solutions/      ← {code}-YYYY-N/（🔒 證據）、methods/（✏️ 方法論）
├── study/              ← lecture-／formula-given-／study-／frequency- 教材；assets/katex/（勿刪）
└── wiki/               ← problems / concepts / methods / philosophy / traps / topics /
                           diagnosis / failure-modes / materials / code-ref / queries
```
""", made, dry)

    # ---------------------------------------------------------- raw/json
    wr(P("raw/json/question_index.json"), json.dumps({
        "description": f"{code} {name} 考題總索引（v3 格式，與 SS 相同）。verificationStatus 和 tags 是主要人工維護欄位。topicId 格式為 syllabus_taxonomy.json 的 XX-Un-m 代號。",
        "tagSystem": {
            "primaryTopicId": "命題大綱主分類（依 syllabus_taxonomy.json，格式：XX-Un-m）",
            "secondaryTopicIds": "命題大綱副分類（跨主題時使用）",
            "designMethod": f"{prof['methodAxis']}：" + " / ".join(prof["methods"]),
            "tags": "自由標籤，描述核心考點、概念、陷阱類型",
        },
        "questions": [],
    }, ensure_ascii=False, indent=2) + "\n", made, dry)
    wr(P("raw/json/concepts.json"), json.dumps({"concepts": []}, ensure_ascii=False, indent=2) + "\n", made, dry)

    # ---------------------------------------------------------- wiki/index.md
    sec = []
    for u in units:
        sec.append(f"### {u['id']}：{u['name']}\n")
        for it in u["items"]:
            sec.append(f"- [[{it['id']}]] [{it['name']}](topics/{it['id']}.md) — 尚無題目")
        sec.append("")
    wr(P("wiki/index.md"), f"""
# {name}考古題知識庫

**科目代碼：** {code}（{subj.get('nameEn', '')}）
**考試名稱：** 專門職業及技術人員高等考試結構工程技師 — {name}
**題目總數：** 0 題
**已驗證：** 0 題

> ⚠️ = 尚未驗證（unverified）；驗證後執行 `ingest {code}-XXXX-N` 即可生成題目頁。

---

## 快速導航

- [依年份瀏覽 →](by-year.md)
- [命題大綱分類 →](topics/index.md)
- [設計哲學 →](philosophy/index.md)
- [陷阱總表 →](traps/index.md)
- [題型診斷 →](diagnosis/index.md)
- [{lay['failure-modes']['title']} →](failure-modes/index.md)
- [{lay['materials']['title']} →](materials/index.md)
- [{lay['code-ref']['title']} →](code-ref/index.md)
- [術語速查 GLOSSARY →](concepts/GLOSSARY.md)
- [科目設定 SUBJECT.md →](../SUBJECT.md)

---

## Part 1：命題大綱分類

{chr(10).join(sec)}
---

## Part 2：設計哲學（philosophy/）

（compile-all 後生成）

## Part 3：解題方法論（methods/）

（compile-all 後生成）

## 概念索引

（compile-all 後生成）
""", made, dry)
    wr(P("wiki/by-year.md"), f"""
# 依考年分類

> 總題數：0 題
> ✅ = verified｜⚠️ = unverified

---

（尚未收錄題目；每次 ingest 時依考年由新到舊追加）
""", made, dry)
    wr(P("wiki/log.md"), f"""
# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## {TODAY} — 依 SS 架構建立 {code} 科目骨架

**操作類型：** 初始化

### 完成事項
- 以 `scripts/scaffold_subject.py {code}` 建立目錄結構、`SUBJECT.md`、空的 `question_index.json`／`concepts.json`。
- 建立 wiki 導航頁：`index.md`、`by-year.md`、`topics/`（{len(items)} 個子項）、`diagnosis/`、`failure-modes/`、`materials/`、`code-ref/` 的索引與類別頁。
- 複製共用資源：`study/assets/katex/`、`scripts/build_frequency.py`；`index.html` 使用五科共用樣板。

### 下一步
- 將歷年考卷放入 `raw/exams/`（命名 `{exam}`），開始「解析 YYYY 年 {code} 考卷」。
""", made, dry)

    # ---------------------------------------------------------- topics
    tlines = [f"# 命題大綱分類索引 — {code} {name}\n",
              "依考選部公告命題大綱建立的題目分類導航。\n",
              "**格式：** `XX-Un-m`（XX 科目代號 · Un 單元 · m 子項）｜完整分類見根目錄 `syllabus_taxonomy.json`\n",
              "---\n"]
    for u in units:
        tlines.append(f"## {u['id']}：{u['name']}\n")
        tlines += [f"- [[{it['id']}]] {it['name']}" for it in u["items"]]
        tlines.append("")
    wr(P("wiki/topics/index.md"), "\n".join(tlines) + "\n", made, dry)
    for i, n, u in items:
        wr(P("wiki/topics", f"{i}.md"), f"""
# {i} — {n}

**所屬科目：** {name}（{code}）
**命題大綱：** {u['name']}／{n}

---

## 主分類題目（0 題）

（尚無）

## 副分類題目（0 題）

（尚無）

---

*出處：[命題大綱](../../../命題大綱.pdf)*
""", made, dry)

    # ---------------------------------------------------------- Layer 2–4
    wr(P("wiki/philosophy/index.md"), f"""
# 設計哲學總覽 — {code}

**來源：** `SUBJECT.md` §8「設計哲學框架」（compile-all 時展開為各哲學頁）

| 哲學 ID | {prof['methodAxis']} | 命題大綱 | 核心原則 |
|--------|------|---------|---------|
| （待 compile-all） | | | |
""", made, dry)
    wr(P("wiki/traps/index.md"), f"""
# 陷阱總覽（Traps Index）— {code}

> 從各題解析的「解題戰略地圖與陷阱分析」區段萃取，按命題大綱子項分組。
> 每個陷阱頁包含：觸發信號、錯誤思維、正確認知、出現題目。

---

（尚無題目，compile-all 後生成）
""", made, dry)
    wr(P("wiki/concepts/GLOSSARY.md"), f"""
# {name}術語速查表（GLOSSARY）

> 考試常見符號與術語的快速定義，附公式與規範來源。
> 詳細概念說明見各 `wiki/concepts/[CONCEPT-ID].md`。

---

## 符號索引

| 符號 | 名稱 | 定義 / 說明 |
|------|------|------------|
| （待補） | | |
""", made, dry)
    drows = "\n".join(f"| {v[0]} | {v[1]} | [[{k}]] |" for k, v in prof["diagnosis"].items())
    wr(P("wiki/diagnosis/index.md"), f"""
# 題型診斷層 — 考題進入點地圖（{code}）

> **用法：** 拿到考題後，先對照下表找到題型，再按診斷頁的決策樹決定「用哪個 Method、需要哪些 Concept、注意哪些 Trap」。

---

## 快速分類表

| 題型 | 關鍵辨識特徵 | 診斷頁 |
|------|------------|--------|
{drows}
""", made, dry)
    for k, v in prof["diagnosis"].items():
        wr(P("wiki/diagnosis", f"{k}.md"), f"""
# 題型診斷：{v[0]}

**辨識特徵：** {v[1]}

---

## 決策樹

（待題目累積後補：題目給了什麼 → 走哪條路徑）

## 使用的方法論（Method）

## 需要的概念（Concept）

## 常見陷阱（Trap）

## 出現題目

| 題號 | 子題 | 判斷依據 |
|------|------|---------|
""", made, dry)

    # ---------------------------------------------------------- Layer 5–7
    for key in ["failure-modes", "materials", "code-ref"]:
        L = lay[key]
        rows = "\n".join(f"| {t} | [[{p}]] |" for p, t in L["pages"].items())
        extra = "" if key != "code-ref" else "\n## 規範體系\n\n" + "\n".join(f"- {c}" for c in prof["codes"]) + "\n\n## 條文 ↔ 知識點對照\n\n| 條文／定理 | 內容 | 相關 Concept／Method | 出現題目 |\n|-----------|------|---------------------|---------|\n"
        wr(P("wiki", key, "index.md"), f"""
# {L['title']}（{code}）

> 本層由 Cowork 直接維護，不走 ingest／compile 流程。類別定義見 `SUBJECT.md` §5。

---
{("" if not rows else chr(10) + "## 類別" + chr(10) + chr(10) + "| 類別 | 詳細頁面 |" + chr(10) + "|------|---------|" + chr(10) + rows + chr(10))}{extra}""", made, dry)
        for p, t in L["pages"].items():
            wr(P("wiki", key, f"{p}.md"), f"""
# {t}

> 所屬層：{L['title']}（`wiki/{key}/`）｜科目：{code}

---

## 核心觀念

（待補）

## 判斷條件／公式

## 出現題目

| 題號 | 說明 |
|------|------|
""", made, dry)

    wr(P("wiki/queries/index.md"), f"""
# 查詢結果目錄（{code}）

> 本目錄由 **Cowork** 直接存入，不走 ingest 流程。
> 命名規則：`[主題]-[YYYY-MM-DD].md`

---

## 查詢結果列表

| 日期 | 主題 | 格式 | 連結 |
|------|------|------|------|
""", made, dry)

    # ---------------------------------------------------------- 共用資源
    for rel_src, rel_dst in [("study/assets/katex", "study/assets/katex")]:
        src, dst = os.path.join(ROOT, REF, rel_src), P(rel_dst)
        if os.path.isdir(src) and not os.path.exists(dst):
            made.append(dst)
            if not dry:
                shutil.copytree(src, dst)
    for rel_src in ["scripts/build_frequency.py"]:
        src, dst = os.path.join(ROOT, REF, rel_src), P(rel_src)
        if os.path.isfile(src) and not os.path.exists(dst):
            made.append(dst)
            if not dry:
                shutil.copy2(src, dst)
    tpl, dst = os.path.join(ROOT, "scripts", "templates", "dashboard-index.html"), P("index.html")
    if not os.path.exists(dst):
        made.append(dst)
        if not dry:
            shutil.copy2(tpl, dst)

    print(f"[{code}] {name}：新建 {len(made)} 項" + ("（dry-run）" if dry else ""))
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subjects", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for c in a.subjects:
        scaffold(c, a.dry_run)
    if not a.dry_run:
        here = os.path.join(ROOT, "scripts")
        subprocess.run([sys.executable, os.path.join(here, "sync_taxonomy.py")], check=False)
        for c in a.subjects:
            subprocess.run([sys.executable, os.path.join(here, "refresh_dashboard.py"), c], check=False)


if __name__ == "__main__":
    main()
