# Rankine vs Coulomb、主動 vs 被動 判斷

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
題目擋土結構的牆背與填土條件？
├─ 牆背垂直、填土水平、光滑牆面（忽略牆土摩擦） → Rankine 理論（見 [[RANKINE-EARTH-PRESSURE]]）
├─ 牆背傾斜、填土有坡度、或明確給定牆土摩擦角 δ → Coulomb 理論（見 [[COULOMB-EARTH-PRESSURE]]）
└─ 懸臂式擋土牆（L型/倒T型）→ 先建立「虛擬牆背」再套用 Rankine（見 [[lateral-earth-pressure-method]]）

牆體運動方向決定主動或被動：
├─ 牆體遠離填土方向變形/位移 → 主動土壓力 Ka（土體卸壓）
└─ 牆體推向填土方向變形/位移（如被動抵抗、開挖擋土結構的貫入段）→ 被動土壓力 Kp（土體受壓）
```

## 延伸閱讀

[[RANKINE-EARTH-PRESSURE]]、[[COULOMB-EARTH-PRESSURE]]、[[lateral-earth-pressure-method]]

## 範例題目

- [[SM-2018-4]]
- [[SM-2019-4]]
- [[SM-2016-4]]
