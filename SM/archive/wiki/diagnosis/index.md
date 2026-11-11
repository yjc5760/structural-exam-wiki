# 題型診斷決策樹（Layer 4）

> 拿到一道 SM 考題後，用來快速判斷「這是哪種題型、該用哪套邏輯解」的決策樹索引。
> 由 Cowork 直接維護，內容隨解題累積逐步充實。

---

## 診斷頁清單

> 採「跨題型判斷點」而非「逐一對應命題大綱子項」的方式組織，因為實際解題時的第一個分岔（例如「這題該用總應力法還是有效應力法」）往往橫跨多個 SM-Un-n 子項，比單一子項各自建一頁更貼近實際解題流程。

| 判斷點 | 診斷頁 | 對應單元 |
|--------|--------|---------|
| 總應力法 vs 有效應力法選擇 | [analysis-method-diagnosis.md](analysis-method-diagnosis.md) | [[SM-U1-5]]、跨單元 |
| 淺基礎 vs 深基礎判斷與計算項目 | [foundation-type-diagnosis.md](foundation-type-diagnosis.md) | [[SM-U2-1]]、[[SM-U2-2]] |
| Rankine vs Coulomb、主動 vs 被動判斷 | [earth-pressure-theory-diagnosis.md](earth-pressure-theory-diagnosis.md) | [[SM-U3-1]]、[[SM-U3-2]] |
| 邊坡穩定分析方法選擇 | [slope-analysis-method-diagnosis.md](slope-analysis-method-diagnosis.md) | [[SM-U3-3]] |
| 開挖破壞模式判斷 | [excavation-failure-diagnosis.md](excavation-failure-diagnosis.md) | [[SM-U2-3]] |
| 「承載力」vs「沉陷量」題型判斷 | [settlement-vs-bearing-diagnosis.md](settlement-vs-bearing-diagnosis.md) | [[SM-U2-1]]、[[SM-U2-2]] |

> 六頁已建立初版內容。若未來發現特定命題大綱子項（如 [[SM-U1-1]] 土壤分類、[[SM-U2-5]] 地層改良）需要獨立診斷頁，可再依 CLAUDE-CODE.md 的通用格式擴充。

---

## 診斷頁通用格式

```markdown
# [判斷點名稱]

## 決策樹
（流程圖文字化：先問什麼問題，依答案分支）

## 延伸閱讀
（連結至 wiki/philosophy/ 或 wiki/concepts/ 中的深入說明）

## 範例題目
（連結至 wiki/problems/）
```
