# 淺基礎 vs 深基礎 判斷與計算項目

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
題目問的是哪一種基礎？
├─ 明確提及「連續/方形/矩形/筏式基腳」，或載重直接由基礎底面傳遞 → 淺基礎
│      └─ 問法是「承載力/容許承載力」→ 用 [[bearing-capacity-method]]（見 [[BEARING-CAPACITY-THEORY]]）
│      └─ 問法是「沉陷量」→ 用 [[SETTLEMENT-COMPONENTS]]（瞬時+壓密+次壓縮）
│      └─ 問法是「地下水位變化對承載力/沉陷的影響」→ 需重算 [[EFFECTIVE-STRESS-PRINCIPLE]] 修正後的 γ 與 u
└─ 明確提及「樁、basement、深基礎」 → 深基礎
       └─ 問法是「單樁承載力」→ 用 [[pile-capacity-method]]（α法/β法，見 [[PILE-CAPACITY-COMPONENTS]]）
       └─ 問法是「群樁」→ 需另檢核 [[PILE-GROUP-EFFICIENCY]]（效率與群樁沉陷）
       └─ 題目描述「上方新填土」或「地下水位下降」造成黏土層持續壓密 → 檢查是否為負摩擦力（down-drag）情境
```

## 延伸閱讀

[[BEARING-CAPACITY-THEORY]]、[[PILE-CAPACITY-COMPONENTS]]

## 範例題目

- [[SM-2010-4]]
- [[SM-2024-4]]
- [[SM-2021-3]]
