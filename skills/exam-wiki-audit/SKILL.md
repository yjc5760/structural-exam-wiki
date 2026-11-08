---
name: "exam-wiki-audit"
description: "稽核 exam-wiki 五科（SS、RC、SA、SD、SM）既有題解：主副分類一致性、用考卷原圖盲解比對題解正確性、勘誤後落實檢查，產出報告與 ledger。使用者說掃描題解、驗證解題、盲解比對、稽核分類、落實檢查、複驗勘誤時使用。"
---

# exam-wiki-audit — 題解分類與正確性稽核（五科通用）

## 目的與原則

既有題解多由 Gemini 以 PDF 讀題產生。本庫考卷為 Adobe-CNS1 CID 字型，抽文字會漏中文，曾導致題目被「補全」成錯題；
8/22 抽查與 10/31 SS-U1-1 盲解比對顯示錯誤**主因是讀題與看圖（L1）**，不是算術。因此本 skill 的核心是：

1. **看原圖，不看 PDF 文字**：考卷一律以 PyMuPDF 轉圖（不可用 poppler／pdftotext）
2. **盲解**：寫完盲解紀錄之前，**絕不開啟舊題解**（`raw/solutions/<id>/<id>.md`、`archive/wiki/problems/`、`study/problems-view/`）。
   題目正本 `raw/solutions/<id>/<id>-problem.md` 不是題解（只有考卷原文與判讀，沒有解法），**可以讀**。
   **獨立性揭露**：工作階段會自動載入該科 `CLAUDE.md`，其 CHANGELOG 可能寫有舊勘誤的結論，盲解前無法避開。
   盲解前先掃過 CHANGELOG，把本批題目被洩漏的點逐題列在報告「方法」節；這些點雙方一致時標「一致但非獨立」，不算佐證。
   講義、log 等其他已讀過的文件若寫了某題的錯誤結論，同樣逐題揭露
3. **跨家族獨立**：Claude 盲解對照 Gemini 題解；分歧中屬看圖者交使用者判定，屬推理／規範者建議再請 GPT 系列解一次
4. **唯讀**：只新增報告與 ledger，不修改題解、索引或 wiki。修正由使用者依各科 CLAUDE.md 規則 1（勘誤條件各科不同）另行處理（exam-errata）。
   唯一例外：尚無題目正本的題目，可把盲解轉錄輸出成**題目正本草稿**（見 2-3）
5. **使用者自行 commit**：結束時列出新增檔案路徑，不執行 git commit

與其他 skill 的順序（見 exam-wiki-pipeline）：exam-problem-split 定題意 → 本 skill 盲解比對 → exam-errata 勘誤 → 本 skill 落實檢查 → struct-diagram 補圖解。

## 第 0 步：取得 repo 與規則

- 有連結使用者電腦時：用本機資料夾（如 `C:\Users\yjc57\Downloads\exam-wiki-XX`），只寫入 `wiki/queries/`
- 未連結時：`git clone --depth 1 https://github.com/yjc5760/exam-wiki-XX.git`（唯讀副本），報告以檔案交付；**不要 commit／push 到副本**，結束前刪掉副本中新增的檔案
- 讀該科 `CLAUDE.md` 的「命題大綱分類」「分類原則」「重要規則」，與 `raw/json/syllabus_taxonomy.json`
- 第一次使用時，把本檔末尾四支腳本寫到工作目錄（scratchpad）的 `audit-tools/`，`pip install pymupdf scipy`（如缺）
  - 使用者電腦上的 shell 可能沒有 PyMuPDF 且安裝逾時：stdlib 腳本（audit_classification、pending）在本機跑，考卷 PDF 用 device_stage_files 送到雲端再轉圖

## 第 1 層：分類一致性（機械檢查，全科一次跑完，幾秒）

```
python audit-tools/audit_classification.py <repo> <科目> --out <報告.md>
```
以 `question_index.json` 為準，比對：索引自身（代號不存在／指向他科／名稱與大綱不符／副分類重複）與題解正本標頭。
支援三種標頭格式（`**主分類：**`、YAML、表格「科目分類」），主分類只寫到單元層級（如 `SD-U1`）會另外標出。
設計法只在短固定值（LRFD／ASD／USD／概念題…）時比對。
wiki 各層（problems、topics…）已於 2026-11 封存到 `archive/wiki/`，不再維護，不比對。

## 第 2 層：盲解（分批，每次對話 10–20 題）

### 2-1 選題
```
python audit-tools/pending.py <repo> <科目> [--unit XX-Un-m] [--limit 15]
```
輸出含 `problemStatus` 欄（confirmed／draft／—），有已確認題目正本的題目讀題可省力。自動略過 ledger 已記錄與**已勘誤**的題目；預設依單元出題數多者優先。

「已勘誤」的判定（三者任一）：ledger 該題 `fixed` 有值；`wiki/queries/log.md` 中標題含 `FIX-` 的段落提到該題號；
解析 .md 有「依最新規範」，或有一行「修正日期」不屬於非勘誤修改。
**非勘誤修改**（題目正本拆分、重繪附圖、補圖解）的頁尾修正日期，括號內必須以「§1 改為指向題目正本」開頭，或含「圖解補繪」「（非勘誤）」字樣——
否則 pending.py 會把它當成已勘誤而跳過盲解。exam-problem-split、struct-diagram 寫頁尾時都要遵守。

使用者未指定時：先問一次範圍；無人回應則取出題最多的單元。

**複驗**（勘誤之後）：
```
python audit-tools/pending.py <repo> <科目> --recheck [--unit XX-Un-m] [--limit 15]
```
列出兩類題目，處理方式不同：
- **落實檢查**：ledger 有 `fixed` ≥ `date`（依盲解結果勘誤過），且還沒做過落實檢查。
  盲解紀錄已經存在，**不必重新盲解**，直接做第 3 層：拿既有盲解紀錄與 ledger `human` 的判定，對照勘誤後的正本，
  確認數值、結論都改到了，且 §1、§3、§3.5、§4、§5、圖說沒有殘留舊值或舊觀念（勘誤殘留）。
  勘誤與落實檢查在同一工作階段完成時，於報告與 ledger `recheck.note` 註明「非獨立複核」。
- **重新盲解**：題解已勘誤但 ledger 無紀錄（勘誤版從未盲解）→ 照第 2 層完整盲解。

### 2-2 轉圖
```
python audit-tools/pages.py render <考卷.pdf> <輸出資料夾> 300
python audit-tools/pages.py crop <考卷.pdf> <頁> x0 y0 x1 y1 <out.png> 400
```
先看整頁圖找到該題，再把**附圖、尺寸標註、支承符號**放大到 400–450 dpi 逐一確認。題目文字與附圖都從圖讀。

### 2-3 每題依序做三件事（寫入盲解紀錄）

**先看有沒有題目正本 `<id>-problem.md`**（題意與解答已拆開的科目／單元才有；格式見 exam-problem-split「題目正本」結構）：

- **已確認**：以它的 §1 原文、§2 公式與附表、§4 判讀清單作為 (a)(b) 的輸入，不必重新轉錄；
  仍要開考卷原圖核對附圖與判讀清單，看到不一致就記為「❓ 題目正本疑義」並寫出頁碼位置（不要自行修改題目正本）。
- **待確認或沒有**：照下列 (a)(b) 做，並把轉錄＋判讀表依題目正本格式另存草稿（判讀狀態「待確認」）：
  該科 `CLAUDE.md` 規則 1 已把 `-problem.md` 列為例外時（SS 自 2026-11-02、SA 自 2026-11-04 起）寫到 `raw/solutions/<id>/<id>-problem.md`；
  否則寫到 `wiki/queries/題目正本草稿-<科目>/<id>-problem.md`。草稿交使用者確認，不算稽核結論。

**(a) 題目逐字轉錄**：看不清處寫「〔無法判讀〕」並放大重看；仍不清楚就標註後跳過該處，**禁止依題型脈絡補全**。

**(b) 判讀表**（錯誤最多的地方，逐項寫明）：
- 每個節點的支承／接合：固接、鉸支、滾支、滑動束制（可平移不轉動）、梁柱鉸接（圖上小圓圈）
- 每個尺寸標註量到哪裡（形心？外緣？腹板高？虛線？）、側撐位置
- 構件、斷面、材料、載重（大小、方向、作用點）
- 題目給的公式、係數、表格、指定方法與規範版本（考卷附的參考公式以原文為準）
- 每小題實際問什麼（逐小題列出；標稱或設計強度、哪一個強度）
- 題目**已給定、不需自算**的參數（如 $L_p$、$L_r$、$C_b$、斷面性質表）

**(c) 盲分類**：只依轉錄與判讀，從該科大綱選主分類與副分類（此時才可對照 `pending.py` 列出的索引主分類，並記錄是否同意）。

### 2-4 解題
- 數值一律以 Python 計算並保留式子；單位統一後再算
- 剛架、連續梁可用平面剛架勁度法（EA 取 10⁸·EI 模擬不計軸向變形）一次解出所有桿端彎矩；有側移的傾角變位題，另以手列傾角變位式（sympy）交叉驗算側移式的符號
- 對位圖 K 值用方程式精確解：`python audit-tools/align.py sway|brace GA GB`（查圖讀值只作參考）
- 說明題：列出得分要點清單，供比對覆蓋度與事實錯誤
- 有多種合理解讀時，主解採最符合題意者，並寫「不確定處」與替代解讀的數值
- 解完一題就把結果 append 到 `盲解紀錄-<科目>-<範圍>-<日期>.md`

## 第 3 層：比對

全部題目的盲解紀錄寫完後，才逐題打開舊題解，讀 §1 題目重述、§3.5 VHA、§4 計算、§5 彙整、`\boxed{}` 結果，比對：
1. **題意**：舊解用的題意（§1 重述、§3.5 L1 給定值、計算中引用的參數）是否與題目正本或盲解轉錄一致——特別注意「依題意補全」「掃描不清」等字樣、**題給參數被自行重算**、**所求的量答錯**（標稱答成設計強度等）、**重述中多出考卷沒有的條件**
2. **判讀**：支承、尺寸、側撐、銲道／螺栓數量、開孔扣除是否一致
3. **最終答案**：數值差 > 2%，或結論（OK/NG、控制模式、挫屈型態）不同即為分歧
4. **分類**：盲分類與索引是否一致
5. **觀念作圖**：彎矩圖受拉側、反曲點、變形方向的文字描述是否與數值相符（數值一致也要看）
6. **勘誤殘留**（題解含「修正日期」時）：結論改了但前面步驟、§3.5 L3、§5 彙整、圖說仍是舊值或舊觀念

結果分級：
- ✅ 一致
- ❌ 分歧-答案改變
- ⚠️ 分歧-觀念作圖（數值不受影響，但圖形、觀念或題意解讀有誤）
- ❓ 盲解不確定（題目本身有缺陷或多解）

錯誤來源標籤：`L1 讀題`、`L1 看圖`、`L1 漏抄題給`、`L1 答非所問`、`規範條文漏用`、`查圖誤差`、`觀念模型`、`單位換算`、`算術`、`分類`、`勘誤殘留`。

**禁止**為了一致而改動盲解結論；若比對後發現盲解自己錯了，在報告中照實寫明。

## 輸出

1. `wiki/queries/盲解比對-<科目>-<範圍>-<日期>.md`：
   - 方法、版本（commit 日期）、獨立性揭露、總覽表（一致／分歧題號）、錯誤來源分布
   - 分歧明細依嚴重度排序，每題含：舊解、盲解、**「回考卷看：第幾頁哪個位置」**
   - 一致題清單、建議下一步
2. `wiki/queries/盲解紀錄-<科目>-<範圍>-<日期>.md`：每題轉錄、判讀表、算式與結果
3. `wiki/queries/分類稽核-<科目>-<日期>.md`：第 1 層報告（有問題時）
3a. 題目正本草稿（見 2-3；尚無題目正本的題目才有）
4. 更新 `wiki/queries/audit-ledger-<科目>.json`：
   ```json
   {"SS-2003-2": {"date": "2026-10-31", "model": "claude-opus-5-5", "result": "分歧-答案改變",
                  "source": "規範條文漏用", "report": "wiki/queries/盲解比對-SS-U1-1-2026-10-31.md",
                  "scope": "", "human": "", "fixed": "",
                  "recheck": {"date": "", "result": "", "report": "", "note": ""},
                  "history": []}}
   ```
   各欄由誰寫：

   | 欄位 | 寫入者 | 內容 |
   |---|---|---|
   | `date` `model` `result` `source` `report` `scope` | 本 skill（盲解比對） | `scope` 可選，標批次性質（如「已勘誤題抽樣」「單題補登」） |
   | `human` | 使用者（或依使用者明說的判定代填） | 「舊解對／盲解對／皆錯」或使用者的決定原文 |
   | `fixed` | exam-errata | 依本筆結果完成勘誤的日期 |
   | `recheck` | 本 skill（落實檢查） | `result`：`落實`／`殘留`／`新分歧`；有問題時 `note` 寫哪一節殘留什麼 |
   | `history` | 本 skill（重新盲解） | 重新盲解時，把舊的整筆（不含 `history`）移入陣列，再寫新結果 |

   只改本次動到的欄位，其他欄位原樣保留；不要刪除舊紀錄。

落實檢查只產出 `wiki/queries/落實檢查-<科目>-<範圍>-<日期>.md`（每題：勘誤日期、該改的點、是否改到、殘留位置），並更新 ledger `recheck`。

最後回覆：一致／分歧題數（落實檢查則為落實／殘留題數）、最嚴重的 3 題（一句話說明錯在哪）、新增檔案路徑清單、建議下一批範圍。

## 注意

- 盲解本身也會錯；報告每項都要能讓使用者回考卷原圖快速判定
- 不要把 `verificationStatus` 改為 `verified`；「AI 盲解一致」只寫在 ledger
- 各科 CLAUDE.md 規則 1 對題解正本可否修改規定不同（SS、SA 可勘誤；SD 等仍唯讀），本 skill 一律不改
- 規模參考：五科約 440 題待驗；每次對話以一個單元或 15 題為宜，靠 ledger 接續

---

## 附錄：腳本（第一次使用時寫入 `audit-tools/`）

### audit_classification.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exam-wiki 分類一致性稽核（六科通用，唯讀）
用法：python audit_classification.py <repo根目錄> <科目代號> [--out 報告.md]
以 raw/json/question_index.json 為準，比對：
  A 索引自身：主分類代號不存在於大綱、指向他科、名稱與大綱不符、副分類含主分類或他科代號、有題解資料夾但索引無此題
  B 題解正本 raw/solutions/<id>/<id>.md 標頭（主分類／副分類／設計法）
wiki 各層（problems、topics 等）已於 2026-11 封存到 archive/wiki/，不再維護，故不比對。
"""
import argparse, json, re
from collections import defaultdict
from pathlib import Path

UID = re.compile(r"\b([A-Z]{2}-U\d+-\d+)\b")
UNIT = re.compile(r"\b([A-Z]{2}-U\d+)\b(?!-)")
ALIAS = {"主分類": "主分類|科目分類", "副分類": "副分類", "設計法": "設計法|分析方法"}
HDR = {k: re.compile(rf"(?m)^(?:\*\*(?:{a})[：:]\*\*|(?:{a})\s*[:：]|\|\s*(?:{a})\s*\|)\s*(.+)") for k, a in ALIAS.items()}


def load(root, subj):
    q = json.loads((root / "raw/json/question_index.json").read_text(encoding="utf-8"))
    Q = q["questions"] if isinstance(q, dict) else q
    tax = json.loads((root / "raw/json/syllabus_taxonomy.json").read_text(encoding="utf-8"))
    names = {i["id"]: i["name"] for s in tax["subjects"] for u in s["units"] for i in u["items"]}
    qs = {}
    for x in Q:
        mid = x.get("moduleId") or x.get("id") or x.get("questionId")
        if mid and mid.startswith(subj + "-"):
            qs[mid] = x
    return qs, names


def method(x):
    return x.get("designMethod") or x.get("analysisMethod")


def header(path):
    if not path.exists():
        return None
    head = "\n".join(path.read_text(encoding="utf-8", errors="replace").replace("\x00", "").splitlines()[:25])
    out = {}
    for k, rx in HDR.items():
        m = rx.search(head)
        out[k] = (UID.findall(m.group(1)) if k != "設計法" else m.group(1).strip()) if m else None
        if k == "主分類" and m and not out[k] and UNIT.search(m.group(1)):
            out["unit_only"] = UNIT.search(m.group(1)).group(1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("subject"); ap.add_argument("--out")
    a = ap.parse_args()
    root, S = Path(a.root), a.subject
    qs, names = load(root, S)
    iss = defaultdict(list)
    norm = lambda s: re.sub(r"[\s（）()]", "", s or "")

    for qid, x in qs.items():
        p, sec = x.get("primaryTopicId"), list(x.get("secondaryTopicIds") or [])
        if p not in names:
            iss[qid].append(("A 索引", f"主分類 {p} 不在命題大綱"))
        elif not p.startswith(S + "-"):
            iss[qid].append(("A 索引", f"主分類 {p} 指向他科"))
        elif x.get("primaryTopicName") and norm(x["primaryTopicName"]) != norm(names[p]):
            iss[qid].append(("A 索引", f"primaryTopicName「{x['primaryTopicName']}」≠ 大綱「{names[p]}」"))
        for s in sec:
            if s == p: iss[qid].append(("A 索引", f"副分類重複列入主分類 {s}"))
            elif not s.startswith(S + "-"): iss[qid].append(("A 索引", f"副分類 {s} 指向他科"))
            elif s not in names: iss[qid].append(("A 索引", f"副分類 {s} 不在命題大綱"))
        lab, path = "B 題解正本", root / f"raw/solutions/{qid}/{qid}.md"
        h = header(path)
        if h is None:
            iss[qid].append((lab, "檔案不存在")); continue
        if not h["主分類"]:
            if h.get("unit_only"):
                iss[qid].append((lab, f"主分類只寫到單元層級 {h['unit_only']}（索引為 {p}）"))
            else:
                iss[qid].append((lab, "標頭缺主分類"))
            continue
        if h["主分類"][:1] != [p]:
            iss[qid].append((lab, f"主分類 {h['主分類']} ≠ 索引 {p}"))
        if h["副分類"] is not None and sorted(h["副分類"]) != sorted(sec):
            iss[qid].append((lab, f"副分類 {h['副分類']} ≠ 索引 {sorted(sec)}"))
        if h["設計法"] and method(x) and len(norm(method(x))) <= 8 and norm(h["設計法"]).split("（")[0] != norm(method(x)):
            if norm(method(x)) not in norm(h["設計法"]):
                iss[qid].append((lab, f"設計法「{h['設計法']}」≠ 索引「{method(x)}」"))

    for d in sorted((root / "raw/solutions").glob(f"{S}-*")):
        if d.is_dir() and re.fullmatch(rf"{S}-\d{{4}}-\d+", d.name) and d.name not in qs:
            iss[d.name].append(("A 索引", "有題解資料夾但索引無此題"))

    cnt = defaultdict(int)
    for v in iss.values():
        for c, _ in v: cnt[c] += 1
    L = [f"# 分類一致性稽核 — {S}", "", f"索引 {len(qs)} 題；有問題 {len(iss)} 題、{sum(cnt.values())} 筆", "",
         "| 檢查 | 筆數 |", "|---|---|"] + [f"| {c} | {n} |" for c, n in sorted(cnt.items())] + [""]
    for q in sorted(iss):
        x = qs.get(q, {})
        L.append(f"## {q}　索引：{x.get('primaryTopicId','—')} 主／{x.get('secondaryTopicIds','—')} 副")
        L += [f"- **{c}**　{d}" for c, d in iss[q]] + [""]
    rep = "\n".join(L)
    if a.out: Path(a.out).write_text(rep, encoding="utf-8")
    print("\n".join(L[:7 + len(cnt)]))


if __name__ == "__main__":
    main()
```

### pending.py
```python
#!/usr/bin/env python3
"""列出待盲解的題目（唯讀）
  python pending.py <repo根目錄> <科目> [--unit XX-Un-m] [--limit N] [--all | --recheck]
「已勘誤」的判定（三者任一）：
  (1) ledger 該題 fixed 有值
  (2) wiki/queries/log.md 中標題含 FIX- 的段落提到該題號
  (3) 解析 .md 有「依最新規範」，或有一行「修正日期」不屬於非勘誤修改
      非勘誤修改＝題目正本拆分／重繪附圖／補圖解：修正日期括號內以「§1 改為指向題目正本」開頭，
      或含「圖解補繪」「（非勘誤）」字樣（exam-problem-split、struct-diagram 寫頁尾時須遵守）
預設：排除 ledger 已記錄與已勘誤者。--all：不排除。
--recheck：只列需要「複驗」的題目——
   (a) 落實檢查：ledger 有 fixed ≥ date（依盲解結果勘誤），且尚無 recheck.date ≥ fixed
       → 只需拿既有盲解紀錄對照勘誤後正本（第 3 層），不必重新盲解
   (b) 重新盲解：已勘誤但 ledger 無紀錄（勘誤版從未盲解）
排序：單元主分類題數多者優先 → 同單元依年份。ledger：wiki/queries/audit-ledger-<科目>.json"""
import argparse, json, re
from collections import Counter
from pathlib import Path

NONFIX = re.compile(r"修正日期：[^（(]*[（(]\s*§1 改為指向題目正本|圖解補繪|（非勘誤）")


def errata_in_md(t):
    if "依最新規範" in t:
        return True
    return any(not NONFIX.search(l) for l in t.splitlines() if "修正日期" in l)


ap = argparse.ArgumentParser()
ap.add_argument("root"); ap.add_argument("subject")
ap.add_argument("--unit"); ap.add_argument("--limit", type=int, default=0)
g = ap.add_mutually_exclusive_group()
g.add_argument("--all", action="store_true"); g.add_argument("--recheck", action="store_true")
a = ap.parse_args()
root, S = Path(a.root), a.subject
q = json.loads((root / "raw/json/question_index.json").read_text(encoding="utf-8"))
Q = [x for x in (q["questions"] if isinstance(q, dict) else q) if (x.get("moduleId") or "").startswith(S + "-")]
led_p = root / f"wiki/queries/audit-ledger-{S}.json"
ledger = json.loads(led_p.read_text(encoding="utf-8")) if led_p.exists() else {}
log_p = root / "wiki/queries/log.md"
log = log_p.read_text(encoding="utf-8", errors="replace") if log_p.exists() else ""
fix_ids = set()
for sec in re.split(r"\n(?=## )", log):
    if "FIX-" in sec.split("\n", 1)[0]:
        fix_ids.update(re.findall(rf"{S}-\d{{4}}-\d+", sec))
freq = Counter(x.get("primaryTopicId") for x in Q)
rows, skipped = [], Counter()
for x in Q:
    qid, u = x["moduleId"], x.get("primaryTopicId")
    if a.unit and u != a.unit:
        continue
    f = root / f"raw/solutions/{qid}/{qid}.md"
    t = f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
    ent = ledger.get(qid)
    corrected = bool((ent or {}).get("fixed")) or qid in fix_ids or errata_in_md(t)
    note = ""
    if a.recheck:
        if ent:
            fx = ent.get("fixed") or ""
            rc = (ent.get("recheck") or {}).get("date", "")
            if not (fx and fx >= ent.get("date", "")):
                skipped["盲解後未勘誤"] += 1; continue
            if rc and rc >= fx:
                skipped["已做落實檢查"] += 1; continue
            note = f"落實檢查（勘誤 {fx}）"
        elif corrected:
            note = "重新盲解（已勘誤、從未盲解）"
        else:
            skipped["未勘誤"] += 1; continue
    elif not a.all:
        if ent: skipped["ledger 已記錄"] += 1; continue
        if corrected: skipped["已勘誤"] += 1; continue
    rows.append((-freq[u], u, qid, x.get("verificationStatus"), note or ("已勘誤" if corrected else ""),
                 (ent or {}).get("result", ""), x.get("problemStatus", "—")))
rows.sort()
if a.limit: rows = rows[: a.limit]
label = "待複驗" if a.recheck else "待盲解"
print(f"{S}：{label} {len(rows)} 題（略過 {dict(skipped)}）")
for _, u, qid, vs, c, r, ps in rows:
    print(f"{qid}\t{u}\t{vs}\tproblem:{ps}\t{c}\t{r}")
```

### pages.py
```python
#!/usr/bin/env python3
"""考卷轉圖（PyMuPDF；勿用 poppler，缺 Adobe-CNS1 字型包會漏中文）
  python pages.py render <pdf> <outdir> [dpi=300]          → outdir/p1.png, p2.png …
  python pages.py crop <pdf> <頁碼> x0 y0 x1 y1 <out.png> [dpi=400]
     x0..y1 為 0–1 的頁面比例座標（先看整頁圖估位置，再放大附圖）"""
import sys, warnings
warnings.filterwarnings("ignore")
try:
    import pymupdf as fitz
except ImportError:
    import fitz

cmd, pdf = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
if cmd == "render":
    import os
    out = sys.argv[3]; dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    os.makedirs(out, exist_ok=True)
    for i, p in enumerate(doc):
        p.get_pixmap(dpi=dpi).save(f"{out}/p{i+1}.png")
    print(f"{len(doc)} 頁 → {out}")
elif cmd == "crop":
    pg = int(sys.argv[3]); x0, y0, x1, y1 = map(float, sys.argv[4:8]); out = sys.argv[8]
    dpi = int(sys.argv[9]) if len(sys.argv) > 9 else 400
    p = doc[pg - 1]; r = p.rect
    p.get_pixmap(dpi=dpi, clip=fitz.Rect(r.width * x0, r.height * y0, r.width * x1, r.height * y1)).save(out)
    print(out)
```

### align.py
```python
#!/usr/bin/env python3
"""對位圖 K 值精確解（取代目視查圖）
  python align.py sway GA GB      有側移（Sidesway uninhibited）
  python align.py brace GA GB     無側移（Sidesway inhibited）"""
import sys
from math import pi, tan
from scipy.optimize import brentq
mode, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
if mode == "sway":
    f = lambda K: (a * b * (pi / K) ** 2 - 36) / (6 * (a + b)) - (pi / K) / tan(pi / K)
    K = brentq(f, 1.0001, 50)
else:
    def f(K):
        x = pi / K
        return a * b / 4 * x ** 2 + (a + b) / 2 * (1 - x / tan(x)) + 2 * tan(x / 2) / x - 1
    try:
        K = brentq(f, 0.50001, 0.99999)
    except ValueError:
        K = 0.5 if a + b < 1 else 1.0   # 兩端趨近固接或鉸接的極限
print(f"K = {K:.3f}")
```