# 題型診斷：接合設計

---

## 辨識關鍵字

`螺栓` `銲接` `填角銲` `開槽銲` `CJP` `高拉力螺栓` `A325` `A490` `偏心接合` `托架` `牛腿` `剪力板` `翼板連接` `E70XX`

---

## 決策樹

```
看到「接合設計」
    │
    ├─ 螺栓接合
    │       │
    │       ├─ 有「偏心」「托架」「扭矩」「偏心距」
    │       │       → 彈性向量法
    │       │         Ip = Σ(xi²+yi²)
    │       │         RM = M×r/Ip，方向垂直半徑
    │       │         合力 R = √(Rx²+Ry²)
    │       │         Method: [[eccentric-bolt]]
    │       │
    │       ├─ 有「摩阻型」「Slip-critical」「預拉力」
    │       │       → 摩阻型螺栓設計
    │       │         φRn = φ × μ × Du × hsc × Pt × ns
    │       │         Concept: [[SLIP-CRITICAL-CONNECTION]]
    │       │
    │       ├─ 有「承壓型」「A325-X」「A490-X」
    │       │       → 承壓剪力：φRn = φ×0.5FuAb（單剪）
    │       │         承壓強度：φRn = φ×2.4Fudt
    │       │         Concept: [[BEARING-TYPE-CONNECTION]]
    │       │
    │       └─ 一般螺栓群（直接剪力，無偏心）
    │               → 每根螺栓剪力 = V/n
    │                 驗核剪力 + 承壓
    │
    ├─ 銲縫接合
    │       │
    │       ├─ 有「偏心」「牛腿」「扭矩」
    │       │       → 彈性向量法（銲縫線圖）
    │       │         Ip（線圖），f = M×r/Ip（每單位長度）
    │       │         Method: [[eccentric-weld]]
    │       │
    │       ├─ 有「填角銲」「角銲」
    │       │       → φRn = 0.75×0.6FEXX×0.707w×L
    │       │         Concept: [[WELDED-CONNECTION-DESIGN]]
    │       │
    │       ├─ 有「開槽銲」「CJP」「PJP」
    │       │       → CJP：φRn = φFuABM（母材控制）
    │       │         PJP：φRn = 0.75×0.6FEXX×Aeff
    │       │
    │       └─ 有「剪力流」「組合梁腹板」「水平剪力」
    │               → q = VQ/I（每單位長度剪力流）
    │                 Concept: [[SHEAR-FLOW-BEAM]]
    │
    └─ 接合施工規定（概念題）
            → 螺栓間距、端距、預拉力、NDT
              Concept: [[HIGH-STRENGTH-BOLT-PRACTICE]] [[WELD-INSPECTION-NDT]]
```

---

## 銲道強度速查

| 型式 | φ | 容許/設計強度 |
|------|---|-------------|
| 填角銲（LRFD） | 0.75 | $0.75 \times 0.6 F_{EXX} \times 0.707w$ |
| 填角銲（ASD） | — | $0.3 F_{EXX} \times 0.707w$ |
| E70XX | — | $F_{EXX} = 490$ MPa = 49 tf/cm² |
| E70XX 容許（ASD） | — | $f_w = 0.3 \times 49 \approx 14.7$ tf/cm² |

---

## 常見陷阱

- **0.707 是有效喉深係數**（45° 填角銲）
- **偏心銲縫 Ip 用線圖計算**（單位 cm³，非 cm⁴）
- **摩阻型 φ = 1.0（SLS）or 0.85（ULS）** 依滑動定義
- **接合最少強度規定**：不得少於 120 kN 或構材強度 50%

---

## 相關 Methods / Concepts / Traps

- Method: [[eccentric-bolt]] [[eccentric-weld]] [[block-shear]] [[shear-lag-u]]
- Concept: [[WELDED-CONNECTION-DESIGN]] [[BOLTED-CONNECTION-DESIGN]] [[SLIP-CRITICAL-CONNECTION]] [[CONNECTION-DESIGN]]
- Traps: [[CONNECTION-TRAPS]]
- 歷屆題目: SS-2002-4, SS-2004-3, SS-2005-3, SS-2017-4, SS-2021-2
