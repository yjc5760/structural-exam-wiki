# 總應力法 vs 有效應力法 判斷

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
題目土壤是黏土還是砂土？
├─ 砂土 → 一律用有效應力法（c'=0, φ'）。結束。
└─ 黏土 → 問：分析的是「施工期/短期」還是「使用期/長期」行為？
    ├─ 短期（快速施工、開挖、剛完工） → 用總應力法（φ=0, Su），見 [[UNDRAINED-SHEAR-STRENGTH]]
    │      └─ 若題目要求「隨時間變化」的行為 → 需另外結合 [[CONSOLIDATION-THEORY]] 判斷孔隙水壓消散進度
    └─ 長期（孔隙水壓已消散、穩態滲流） → 用有效應力法（c', φ'），見 [[MOHR-COULOMB-FAILURE-CRITERION]]
           └─ 題目若同時問「施工期」與「長期」兩種情況 → designMethod 應標為「混合」，兩者都要算
```
詳細判斷邏輯與範例見 [[total-vs-effective-stress]]。

## 延伸閱讀

[[total-vs-effective-stress]]、[[drainage-condition-philosophy]]

## 範例題目

- [[SM-2010-4]]
- [[SM-2024-4]]
- [[SM-2013-4]]
