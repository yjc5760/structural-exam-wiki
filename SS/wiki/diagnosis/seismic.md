# 題型診斷：耐震設計

---

## 辨識關鍵字

`耐震` `韌性` `SMRF` `強柱弱梁` `Panel Zone` `節點域` `RBS` `犬骨` `EBF` `偏心斜撐` `連桿梁` `SN鋼材` `容量設計` `塑性轉角`

---

## 決策樹

```
看到「耐震設計」
    │
    ├─ 有「強柱弱梁」「梁柱彎矩強度比」
    │       → ΣφcMpc ≥ ΣφbMpb
    │         Mpc = Zx(Fy - Pu/Ag)（考量軸壓折減）
    │         比值 ≥ 1.0 → 強柱弱梁成立
    │         Concept: [[STRONG-COLUMN-WEAK-BEAM]]
    │
    ├─ 有「節點域」「Panel Zone」「腹板厚度 tz」
    │       → tz ≥ (dz + wz)/90（cm 單位）
    │         Concept: [[PANEL-ZONE]]
    │
    ├─ 有「RBS」「犬骨接頭」「縮翼」
    │       → RBS 目的：讓塑性鉸在梁端縮翼處形成
    │         距柱面距離、切削深度均有規定
    │         Concept: [[REDUCED-BEAM-SECTION]]
    │
    ├─ 有「EBF」「偏心斜撐」「連桿梁」「Link」
    │       → 連桿梁長度決定破壞模式：
    │           短連桿（e ≤ 1.6Mp/Vp）：剪力型，加勁多
    │           長連桿（e ≥ 2.6Mp/Vp）：彎矩型
    │         Concept: [[SEISMIC-DESIGN-PHILOSOPHY]]
    │
    ├─ 有「SN 鋼材」「SN400」「SN490」「Z向」
    │       → SN400B/SN490B：衝擊韌性要求
    │         SN400C/SN490C：額外 Z 向（厚度方向）韌性
    │         箱型柱板厚 ≥ 40 mm → 需 C 級
    │         Materials: [[fracture-toughness]]
    │
    ├─ 有「容量設計」「Capacity Design」「超強係數」
    │       → 強構材（柱）承擔弱構材（梁）超強後的力
    │         設計力 = 標稱強度 × 超強係數（1.1 或 1.25）
    │         Concept: [[CAPACITY-DESIGN]]
    │
    └─ 有「塑性轉角需求」「θp」「旋轉能力」
            → SMRF：梁端需提供 0.03 rad 以上塑性轉角
              需確認斷面結實 + 適當側撐間距
```

---

## 耐震設計階層

```
結構系統選擇（SMRF / IMRF / EBF / CBF）
    ↓
容量設計（Capacity Design）：決定強/弱構件
    ↓
強柱弱梁驗核（Strong Column Weak Beam）
    ↓
接頭設計（Panel Zone / RBS / 連續板）
    ↓
材料要求（SN 鋼材等級 / 降伏比 ≤ 0.80）
```

---

## 常見陷阱

- **Mpc 要扣除軸壓效應**：$M_{pc} = Z_x(F_y - P_u/A_g)$
- **Panel Zone tz 以 cm 為單位**（公式含 90 這個常數）
- **SN 鋼材 B vs C 級**：C 級有 Z 向韌性，B 級沒有
- **容量設計超強係數**：Ry = 1.1（A992），Ry = 1.25（A36）
- **EBF 連桿梁長度判斷**：e ≤ 1.6Mp/Vp 為剪力型

---

## 相關 Methods / Concepts / Traps

- Method: [[pm-interaction]]（強柱弱梁驗核需要）
- Concept: [[STRONG-COLUMN-WEAK-BEAM]] [[PANEL-ZONE]] [[REDUCED-BEAM-SECTION]] [[CAPACITY-DESIGN]] [[SEISMIC-DESIGN-PHILOSOPHY]]
- Traps: [[SEISMIC-TRAPS]]
- Materials: [[fracture-toughness]] [[stress-strain]]
- 歷屆題目: SS-2009-1/2, SS-2012-2, SS-2020-1, SS-2022-4
