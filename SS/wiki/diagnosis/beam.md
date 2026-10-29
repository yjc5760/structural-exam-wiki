# 題型診斷：梁桿件

---

## 辨識關鍵字

`鋼梁` `受彎` `彎矩強度` `Lb` `無束制長度` `LTB` `側扭挫屈` `Cb` `Lp` `Lr` `φbMn` `撓度` `使用性` `L/360` `斷面選擇` `最輕斷面`

---

## 決策樹

```
看到「梁桿件」或「受彎構材」
    │
    ├─ 有「無束制長度 Lb」或「側向支撐」
    │       → LTB 三區段判斷
    │         Step 1: 確認結實斷面
    │         Step 2: 算 Mp, Mr
    │         Step 3: 算 Lp, Lr（需 X1, X2）
    │         Step 4: 判斷 Lb 落哪區段 → Mn
    │         Method: [[ltb-3zone]]
    │
    ├─ 有「完全側撐」「上翼板埋入混凝土」「Lb=0」
    │       → Mn = Mp = FyZx（直接）
    │         只需確認結實斷面
    │
    ├─ 有「撓度」「L/360」「使用性」
    │       → δ = 5wL⁴/(384EI) ≤ L/360
    │         注意：撓度用「活載重」計算
    │         若同時有強度需求：先設計斷面再驗撓度
    │
    ├─ 有「Cb」「彎矩修正係數」
    │       → Cb = 12.5Mmax/(2.5Mmax+3MA+4MB+3MC)
    │         均勻彎矩 Cb=1；雙曲率 Cb>1
    │         Concept: [[BENDING-MODIFICATION-FACTOR-CB]]
    │
    ├─ 有「斷面選擇」「最經濟」「最輕」
    │       → 先求需要 Zx = Mu/(φbFy)
    │         查表選最輕滿足條件斷面
    │         再驗撓度（若有使用性要求）
    │
    ├─ 有「剪力強度」「Vn」
    │       → 腹板不挫屈：Vn = 0.6FyAw = 0.6Fy(dtw)
    │         有剪力挫屈（h/tw 大）：參見[[SHEAR-BUCKLING-WEB]]
    │
    └─ 有「板梁」「加勁板」「張力場」
            → Concept: [[PLATE-GIRDER-DESIGN]] [[TENSION-FIELD-ACTION]]
```

---

## 全側撐 vs 部分側撐快速判斷

| 情況 | 判斷 | Mn |
|------|------|-----|
| 上翼板埋入RC板 | 全側撐，Lb=0 | $M_p$ |
| 樓板以剪力釘連接 | 全側撐 | $M_p$ |
| 側撐間距 ≤ Lp | 塑性區 | $M_p$ |
| Lp < Lb ≤ Lr | 非彈性 LTB | 內插公式 |
| Lb > Lr | 彈性 LTB | $C_b M_{cr}$ |

---

## 常見陷阱

- **全側撐時 Mn = Mp，用 Zx 不用 Sx**
- **撓度只用活載重**（L/360 規定）
- **Mn ≤ Mp 上限**（乘 Cb 後仍要截斷）
- **各無束制段各自算 Cb**（多段梁）
- **Fr 只影響 Mr 和 Lr，不影響 Mp**

---

## 相關 Methods / Concepts / Traps

- Method: [[ltb-3zone]] [[plastic-zx]]
- Concept: [[LATERAL-TORSIONAL-BUCKLING]] [[BENDING-MODIFICATION-FACTOR-CB]] [[PLASTIC-MOMENT-MP]] [[SHEAR-BUCKLING-WEB]]
- Traps: [[LTB-BEAM-TRAPS]] [[WEAK-AXIS-BENDING-LIMIT]]
- 歷屆題目: SS-2007-3, SS-2008-1/3, SS-2010-4, SS-2011-1/3, SS-2021-3
