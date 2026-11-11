# 開挖破壞模式判斷

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
開挖題目要求檢核哪一種破壞？
├─ 題目問「基盤隆起」或給定黏土不排水強度 Su → 基盤隆起分析（[[EXCAVATION-STABILITY]]，Nc 依開挖形狀查表）
├─ 題目問「砂湧/管湧」或給定滲透係數、水位差 → 流網分析（[[flow-net-method]]），求 icr/iexit
├─ 題目問「擋土結構本身」（貫入深度、支撐反力、彎矩）→ 屬 [[retaining-wall-stability-check]] 範疇，非地層破壞
└─ 題目問「整體穩定」（含擋土結構在內的大範圍滑動）→ 用邊坡穩定法（[[fellenius-method]]/[[bishop-simplified-method]]）檢核含開挖在內的滑動面
```
五大失敗模式總覽見 [failure-modes/index.md](../failure-modes/index.md)。

## 延伸閱讀

[[EXCAVATION-STABILITY]]、[[seepage-failure]]、[[retaining-structure-failure]]

## 範例題目

- [[SM-2017-4]]
- [[SM-2015-3]]
- [[SM-2003-3]]
