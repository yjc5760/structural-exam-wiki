# 題型診斷：拉力桿件

---

## 辨識關鍵字

`拉力` `承拉` `拉桿` `拉力構材` `淨截面` `有效淨面積` `U值` `剪力遲滯` `塊狀剪力` `block shear` `GSY` `NSF` `BSR`

---

## 決策樹

```
看到「拉力桿件」或「拉力構材」
    │
    ├─ 有「接合」（螺栓孔 or 銲縫）
    │       │
    │       ├─ 有「U值」「剪力遲滯」「只連一肢/腹板」
    │       │       → ① 計算 U = 1 - x̄/L
    │       │         ② Ae = U × An
    │       │         ③ 淨斷面斷裂 φtFuAe
    │       │         Method: [[shear-lag-u]]
    │       │
    │       ├─ 有「塊狀剪力」「block shear」「角隅撕裂」
    │       │       → 畫塊體 → Anv/Ant → φ[0.6FuAnv + UbsFuAnt]
    │       │         Method: [[block-shear]]
    │       │
    │       └─ 一般拉力接合（三種破壞模式並列）
    │               → ① 毛斷面降伏 φtFyAg
    │                 ② 淨斷面斷裂 φtFuAe（含 U）
    │                 ③ 塊狀剪力 φRn
    │                 取三者最小值
    │
    └─ 無接合（純拉力桿件強度）
            → φtPn = min(φtFyAg, φtFuAe)
              Concept: [[TENSION-MEMBER-DESIGN]]
```

---

## 三種破壞模式速查

| 破壞模式 | 英文縮寫 | 公式 | φ |
|---------|---------|------|---|
| 毛斷面降伏 | GSY | $\phi_t F_y A_g$ | 0.90 |
| 淨斷面斷裂 | NSF | $\phi_t F_u A_e = \phi_t F_u U A_n$ | 0.75 |
| 塊狀剪力 | BSR | $\phi[0.6F_u A_{nv} + U_{bs} F_u A_{nt}]$ | 0.75 |

---

## 常見陷阱

- **U 值忘記乘**：$A_e = U \times A_n$，不是 $A_n$
- **孔徑加 3mm**：計算淨面積用 $d_b + 3$ mm
- **Block Shear 取兩公式最小值**
- **φ = 0.75 vs 0.90**：斷裂型用 0.75，降伏型用 0.90

---

## 相關 Methods / Concepts / Traps

- Method: [[shear-lag-u]] [[block-shear]]
- Concept: [[TENSION-MEMBER-DESIGN]] [[EFFECTIVE-NET-AREA]] [[SHEAR-LAG]] [[BLOCK-SHEAR-RUPTURE]]
- Traps: [[TENSION-MEMBER-TRAPS]]
- 歷屆題目: SS-2003-3, SS-2005-1, SS-2015-2, SS-2024-2, SS-2025-2
