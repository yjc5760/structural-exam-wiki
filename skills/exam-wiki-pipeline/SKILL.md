---
name: "exam-wiki-pipeline"
description: "exam-wiki 五科題庫的總控流程：一批題目依序定題意（題目正本＋附圖重繪）→盲解比對→勘誤→落實檢查→補向量圖解→收尾，判斷每題進度並在兩個人工關卡停下。說「跑 XX-Un-m 第 n 批」「題庫流程」「pipeline」「這批做到哪了」時使用。"
---

# exam-wiki-pipeline — 題庫總控流程（五科通用：SS／RC／SA／SD／SM）

本 skill 不自己解題或改檔，而是**決定下一步該跑哪個 skill、跑哪幾題、何時停下等使用者**。
各階段的細節以被呼叫的 skill 為準：exam-problem-split、exam-wiki-audit、exam-errata、struct-diagram，以及各科 `CLAUDE.md`。

## 核心原則：題意 → 答案 → 圖

1. **題意先凍結**：錯誤主因是讀題與看圖（L1），題目正本確認後，盲解與勘誤才有可靠輸入。
2. **答案再驗證**：盲解比對找分歧，勘誤只改有分歧的題，再做落實檢查。
3. **解題圖解最後畫**：BMD、變形圖、自由體圖畫的是答案；數值未驗證就畫，答案一改圖就要重畫。
   （題目附圖重繪只依賴題意，屬於階段 A。）
4. **整批只有兩個人工關卡**：關卡一確認題目正本，關卡二人工複核改 verified。中間階段連續跑，不要逐題停下來問。
5. **使用者自己 commit**：每個階段結束列出動到的檔案路徑，不執行 git commit／push。

## 批次的定義

- 一批＝同一子項（`XX-Un-m`）約 10–15 題，依年份切。例：SA-U2-3 第一批 2002–2013、第二批 2014–2025。
- 使用者沒指定時：用 exam-wiki-audit 的 `pending.py` 取出題數最多、尚未處理的子項，問一次範圍；無人回應就取該子項最早的 12 題。

## 階段總覽

| 階段 | 內容 | 執行 | 完成判定 |
|---|---|---|---|
| 0 | 全科分類一致性稽核（全科一次，之後每次大改分類才重跑） | exam-wiki-audit 第 1 層 | 報告 0 筆，或問題已列給使用者 |
| **A 定題意** | 盲讀考卷 → 判讀清單 → `<id>-problem.md` 草稿 → 比對解析 §1 → **關卡一** → 凍結 → 重繪題目附圖 → 改寫解析 §1 | exam-problem-split | `-problem.md` 判讀狀態「已確認」且附圖已重繪 |
| **B 驗答案** | 以凍結題目正本盲解、比對舊解 | exam-wiki-audit 第 2–3 層 | ledger 有該題紀錄 |
| B' 判分歧 | 看圖／題意類分歧交使用者判定，填 ledger `human` | 使用者 | 分歧題 `human` 已填，或屬推導類證據明確 |
| **C 改錯** | 只改 ledger 結果為分歧的題 | exam-errata | ledger `fixed` ≥ `date` |
| **D 驗改錯** | 落實檢查：勘誤是否改到、有無殘留 | exam-wiki-audit `--recheck` | `recheck.result` = 落實 |
| **E 補圖解** | 只為數值已驗證（一致或已落實）的題目補向量圖解 | struct-diagram | 解析 .md 已嵌入解題圖 |
| **F 收尾** | 一次重建重下游 → **關卡二** → 使用者複核改 verified | 各科腳本；使用者 | `verificationStatus` = verified |

## 每次啟動時：先盤點進度

1. 讀該科 `CLAUDE.md`（規則 1 可改範圍、資料流、CHANGELOG）。
2. 跑本檔附錄的 `pipeline_status.py` 列出這批每題目前在哪個階段（腳本只讀不寫）。
3. 依「階段總覽」找出**最前面還沒完成的階段**，對該階段所有未完成的題目一起處理；不要在同一批裡讓題目各自跑到不同階段太遠。
4. 開工前用一句話告訴使用者：這批幾題、目前卡在哪個階段、這次要做到哪裡、在哪個關卡停下。

## 各階段要點

### A 定題意（exam-problem-split）
- 已有盲解或稽核產生的題目正本草稿（`wiki/queries/題目正本草稿-XX/`，或 `raw/solutions/<id>/<id>-problem.md` 判讀狀態「待確認」）時，以草稿為起點，仍要回考卷原圖核對。
- **關卡一**：把整批的判讀清單一次交給使用者確認（列出每題的疑點與考卷頁碼位置），不要逐題問。
  使用者確認後才凍結（判讀狀態改「已確認」，同步 `question_index.json` 的 `problemStatus`）。
- 凍結後重繪題目附圖、把解析 §1 改寫為「指向題目正本＋常見誤讀＋本解記號」。§1 與考卷不符的題目（例：虛構條件）在這一步一併修正，並在 log 記一筆。

### B 驗答案（exam-wiki-audit）
- **與階段 A 分開在不同對話執行**：A 會讀舊解析 §1，同一對話接著盲解就不算獨立。若不得不同一對話，在比對報告的獨立性揭露中寫明。
- 題目正本已確認時，盲解直接用它的 §1／§2／§4，不重新轉錄，但仍開考卷原圖核對附圖。
- B'：分歧屬 `L1 看圖`、`L1 讀題`、`L1 漏抄題給` 時，交使用者回考卷判定；屬觀念、推導、算術且證據明確（有兩條獨立計算路徑一致）時，可直接進 C，在報告寫明理由。

### C 改錯（exam-errata）
- 只處理 ledger 結果為「分歧-答案改變」「分歧-觀念作圖」的題目；「一致」的題目不跑 errata。
- 每題仍完整走 errata 步驟 2–7（回考卷、獨立重算 MISMATCHES: 0、清殘留、log、ledger `fixed`）。
- 勘誤時發現**其他題有同類錯誤**：先列出，同一批內可順手勘誤（另記一筆 log）；不在這批的題目列入下一批。
- 重下游（單元總覽、講義 PDF、儀表板）延到 F 一次重建；problems-view 由 errata 逐題重產即可。

### D 驗改錯（exam-wiki-audit `--recheck`）
- 依既有盲解紀錄與 ledger `human` 對照勘誤後正本，檢查數值、結論與 §1、§3、§3.5、§4、§5、圖說是否還有舊值或舊觀念。
- 結果為「殘留」或「新分歧」→ 回到 C 處理該題，再做一次 D。

### E 補圖解（struct-diagram）
- 前提：該題 ledger 為「一致」，或 recheck 為「落實」。數值未驗證的題目不畫。
- 優先順序：
  1. 考卷要求繪 SFD／BMD／變形曲線的繪圖題
  2. 這批錯在判讀或觀念作圖的題目（受拉側、反曲點、側移方向、支承判讀）——畫一張能攔下同類錯誤的圖
  3. 其餘計算題（時間允許才補）
- 圖中數值一律取自已驗證的解析正本；畫完目視檢查受拉側、反曲點位置、側移方向與正本文字一致。

### F 收尾
- 一次重建：`study/problems-view/`（該批題目）、單元總覽（`build_unit_page.py` 該子項）、引用這批題目的講義與 PDF、頻率熱圖與儀表板（有異動才重跑）。
- 檢查：KaTeX 錯誤 0、PDF 頁數與版面合理。
- 更新 `wiki/queries/log.md` 一筆批次摘要；影響答案者在該科 `CLAUDE.md` CHANGELOG 加一列。
- **關卡二**：列出這批每題的最終狀態（一致／已勘誤落實／圖解已補）與複核重點，請使用者人工複核後說「將 XX-YYYY-N 的 verificationStatus 改為 verified」；本 skill 不自行改 verified。

## 停止條件

- 到達關卡一或關卡二。
- 題目本身有缺陷或多解（盲解 ❓），需使用者決定採用哪種解讀。
- 要改的檔案不在該科 `CLAUDE.md` 規則 1 允許的範圍內。
- 使用者電腦未連結、考卷或 repo 讀不到。

## 每次結束時回報

1. 這批目前進度表（題號 × 階段）
2. 本次完成的事與最重要的發現（最多 3 點）
3. 動到的檔案路徑清單（交給使用者自行 commit）
4. 下一步：下一個階段，或要使用者做的關卡動作

---

## 附錄：pipeline_status.py（唯讀，第一次使用時寫到工作目錄 `audit-tools/`）

```python
#!/usr/bin/env python3
"""列出一批題目目前在題庫流程的哪個階段（唯讀）
  python pipeline_status.py <repo根目錄> <科目> --unit XX-Un-m [--years 2002-2013]
判定（啟發式，結果有疑時以實際檔案為準）：
  A  題目正本 raw/solutions/<id>/<id>-problem.md 存在且判讀狀態含「已確認」；附圖重繪：figs/ 下有 <id>-fig-*-problem.svg
  B  wiki/queries/audit-ledger-XX.json 有該題
  C  ledger 結果為一致（不需勘誤），或 fixed >= date
  D  不需勘誤，或 recheck.date >= fixed 且 recheck.result == 落實
  E  解析 .md 引用 figs/ 下的解題圖 svg：不是 -problem.svg，也不是早期題目重繪 <id>-fig-1-{beam,frame,truss,grid}.svg
     （解題圖依 struct-diagram 命名一律為 <id>-fig-N-<語意>.svg，舊判定「不含 -fig-」會把全科判成沒有圖）
  F  question_index.json verificationStatus == verified"""
import argparse, json, re
from pathlib import Path

PROBLEM_REDRAW = re.compile(r"-fig-\d+[a-z]?-problem\.svg$|-fig-1-(beam|frame|truss|grid)\.svg$")

ap = argparse.ArgumentParser()
ap.add_argument("root"); ap.add_argument("subject")
ap.add_argument("--unit", required=True); ap.add_argument("--years")
a = ap.parse_args()
root, S = Path(a.root), a.subject
q = json.loads((root / "raw/json/question_index.json").read_text(encoding="utf-8"))
Q = [x for x in (q["questions"] if isinstance(q, dict) else q)
     if (x.get("moduleId") or "").startswith(S + "-") and x.get("primaryTopicId") == a.unit]
if a.years:
    y0, y1 = map(int, a.years.split("-"))
    Q = [x for x in Q if y0 <= int(x["moduleId"].split("-")[1]) <= y1]
Q.sort(key=lambda x: (int(x["moduleId"].split("-")[1]), int(x["moduleId"].split("-")[2])))
lp = root / f"wiki/queries/audit-ledger-{S}.json"
led = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {}

rows = []
for x in Q:
    qid = x["moduleId"]; d = root / f"raw/solutions/{qid}"
    pm = d / f"{qid}-problem.md"
    ptxt = pm.read_text(encoding="utf-8", errors="replace") if pm.exists() else ""
    m = re.search(r"判讀狀態[^\n]*", ptxt)
    pstat = "—" if not pm.exists() else ("已確認" if m and "已確認" in m.group(0) else "待確認")
    figs = list((d / "figs").glob("*.svg")) if (d / "figs").exists() else []
    redraw = any(f.name.endswith("-problem.svg") for f in figs)
    stxt = (d / f"{qid}.md").read_text(encoding="utf-8", errors="replace") if (d / f"{qid}.md").exists() else ""
    diag = any(f.name in stxt for f in figs if not PROBLEM_REDRAW.search(f.name))
    e = led.get(qid, {}); res = e.get("result", "")
    need_fix = bool(e) and not res.startswith("一致")
    fixed = bool(e) and (not need_fix or (e.get("fixed") or "") >= e.get("date", "9"))
    rc = e.get("recheck") or {}
    landed = bool(e) and (not need_fix or (fixed and rc.get("date", "") >= (e.get("fixed") or "") and rc.get("result") == "落實"))
    ver = x.get("verificationStatus") == "verified"
    A = pstat == "已確認" and redraw
    stage = next((s for s, ok in [("A", A), ("B", bool(e)), ("C", fixed), ("D", landed), ("E", diag), ("F", ver)] if not ok), "完成")
    rows.append((qid, pstat, "✓" if redraw else "—", res or "—", "✓" if fixed else "—",
                 "✓" if landed else "—", "✓" if diag else "—", "✓" if ver else "—", stage))

print(f"{S} {a.unit} {a.years or ''}：{len(rows)} 題")
print("題號\t題目正本\t附圖重繪\t盲解結果\t勘誤\t落實\t圖解\tverified\t卡在")
for r in rows:
    print("\t".join(r))
from collections import Counter
print("各階段題數：", dict(Counter(r[-1] for r in rows)))
```