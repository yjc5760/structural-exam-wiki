# 「承載力」vs「沉陷量」題型判斷

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
題目問的最終目標是什麼？
├─ 問「容許承載力 qa / Qa」或「安全係數 FS」 → 承載力題型
│      └─ 用 [[bearing-capacity-method]] 或 [[pile-capacity-method]]，結果單位為應力(kPa)或力(kN)
├─ 問「沉陷量 S / ΔH」或「多久沉陷到某程度」 → 沉陷題型
│      └─ 瞬時沉陷用彈性理論（[[BOUSSINESQ-STRESS-INCREASE]]）；長期沉陷用 [[consolidation-settlement-method]]
└─ 兩者都問（常見於「先求容許承載力，再求此載重下的沉陷量」）→ 先做承載力題型求出設計載重，再以此載重作為沉陷題型的輸入
       （見 [[SM-2017-3]] 承載力控制 vs 沉陷量控制對照）
```

## 延伸閱讀

[[BEARING-CAPACITY-THEORY]]、[[SETTLEMENT-COMPONENTS]]

## 範例題目

- [[SM-2017-3]]
- [[SM-2010-4]]
