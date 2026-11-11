# 邊坡穩定分析方法選擇

**知識層：** Layer 4 題型診斷

---

## 決策樹

```
邊坡的滑動面幾何形狀？
├─ 均質無限延伸的淺層土坡（厚度遠小於坡長）→ 無限邊坡分析（見 [[SLOPE-STABILITY-ANALYSIS]] 公式庫）
├─ 均質土坡、假設圓弧滑動面 → 切片法
│      ├─ 快速估算或手算驗證 → [[fellenius-method]]（偏保守，忽略切片間作用力）
│      └─ 需要較精確結果、允許疊代計算 → [[bishop-simplified-method]]
└─ 有明顯弱面（頁岩層理、節理、既有滑動面）→ 平面滑動分析（沿弱面直接列力平衡，非圓弧法）

排水條件判斷（見 [[drainage-condition-philosophy]]）：
├─ 剛開挖/剛加載完成 → 短期不排水分析（Su, φ=0）
└─ 長期穩態滲流 → 長期有效應力分析（c', φ'，需先繪流網或給定水位求孔隙水壓）
```

## 延伸閱讀

[[fellenius-method]]、[[bishop-simplified-method]]、[[SLOPE-STABILITY-ANALYSIS]]

## 範例題目

- [[SM-2023-2]]
- [[SM-2021-4]]
- [[SM-2014-1]]
