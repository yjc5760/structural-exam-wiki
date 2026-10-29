# 陷阱總覽（Traps Index）

> 從 98 道解析的「解題戰略地圖與陷阱分析」區段萃取，按主題分組。
> 每個陷阱頁包含：觸發信號、錯誤思維、正確認知、出現題目。

---

## 依主題分組

### 拉力及壓力桿件（SS-U1-1）

- [壓力桿件挫屈陷阱](COLUMN-BUCKLING-TRAPS.md) — 對位圖版本、K值、ASD安全係數、柱曲線繪圖
  - **8 個陷阱** | SS-2013-2, SS-2013-3, SS-2016-3, SS-2017-3, SS-2023-1, SS-2023-2

- [高強度鋼對細長壓力桿件無效](HIGH-STRENGTH-STEEL-SLENDER-COLUMN.md) — 細長柱 Fcr 與 Fy 完全無關

- [拉力桿件陷阱](TENSION-MEMBER-TRAPS.md) — U值L認定、插銷接合、塊狀剪力Ubs
  - **7 個陷阱** | SS-2021-2, SS-2022-2, SS-2024-2, SS-2025-2

### 撓曲桿件（SS-U1-2）

- [梁桿件 LTB 陷阱](LTB-BEAM-TRAPS.md) — 弱軸無LTB、Mn上限=Mp、Sx/Zx混用、局部挫屈分類
  - **11 個陷阱** | SS-2016-1, SS-2016-4, SS-2021-3, SS-2023-3, SS-2024-3, SS-2025-1, SS-2025-3

- [弱軸彎曲強度上限（1.5 FySy）](WEAK-AXIS-BENDING-LIMIT.md) — W型鋼弱軸 Mny 上限陷阱

### 梁柱桿件（SS-U1-3）

- [梁柱桿件 P-M 互制陷阱](BEAM-COLUMN-TRAPS.md) — B2全層柱、Pe1/PeK的K值差異、Mnt/Mlt識別
  - **7 個陷阱** | SS-2013-4, SS-2019-3, SS-2020-3, SS-2022-1

### 接合設計（SS-U1-4）

- [接合設計陷阱](CONNECTION-TRAPS.md) — 偏心銲縫Ip單位cm³、形心位置、摩阻型不共用銲縫
  - **9 個陷阱** | SS-2003-3, SS-2017-2, SS-2017-4, SS-2020-4, SS-2021-4, SS-2023-4

### 塑性分析（SS-U2-1）

- [塑性分析陷阱](PLASTIC-ANALYSIS-TRAPS.md) — 塑性鉸≠一般鉸、崩塌鉸數=n+1、PNA≠ENA
  - **7 個陷阱** | SS-2005-4, SS-2020-2, SS-2023-3, SS-2025-4

### 耐震設計（SD-U3-1）

- [耐震設計陷阱](SEISMIC-TRAPS.md) — RBS削翼板非腹板、SN鋼材降伏比方向、側撐位置
  - **8 個陷阱** | SS-2012-2, SS-2020-1, SS-2021-3, SS-2022-4

### 材料與施工（SS-U2-2 / SS-U2-3）

- [材料性質與施工陷阱](MATERIAL-TRAPS.md) — BH/RH差異、NDT方法選擇、回銲最小長度
  - **8 個陷阱** | SS-2015-4, SS-2016-2, SS-2016-5, SS-2018-4, SS-2021-1, SS-2022-3

---

## 依危險程度排序（⭐ 最常犯）

| 陷阱 | 危險程度 | 涵蓋頁面 |
|------|---------|---------|
| Zx ≠ Ix/c（Zx 與 Sx 混用） | ⭐⭐⭐⭐⭐ | [LTB-BEAM-TRAPS](LTB-BEAM-TRAPS.md) |
| 弱軸彎曲套 LTB 公式 | ⭐⭐⭐⭐⭐ | [LTB-BEAM-TRAPS](LTB-BEAM-TRAPS.md) |
| Mn 超過 Mp 未截頂 | ⭐⭐⭐⭐⭐ | [LTB-BEAM-TRAPS](LTB-BEAM-TRAPS.md) |
| 對位圖版本選錯（有/無側移） | ⭐⭐⭐⭐⭐ | [COLUMN-BUCKLING-TRAPS](COLUMN-BUCKLING-TRAPS.md) |
| B2 只算一根柱的 ΣPeK | ⭐⭐⭐⭐ | [BEAM-COLUMN-TRAPS](BEAM-COLUMN-TRAPS.md) |
| 偏心銲縫 Ip 單位（cm³ 非 cm⁴） | ⭐⭐⭐⭐ | [CONNECTION-TRAPS](CONNECTION-TRAPS.md) |
| 塑性鉸仍承受 Mp，不是 M=0 | ⭐⭐⭐⭐ | [PLASTIC-ANALYSIS-TRAPS](PLASTIC-ANALYSIS-TRAPS.md) |
| RBS 削翼板，不是腹板 | ⭐⭐⭐⭐ | [SEISMIC-TRAPS](SEISMIC-TRAPS.md) |
| ASD FS 不是固定 12/5 | ⭐⭐⭐ | [COLUMN-BUCKLING-TRAPS](COLUMN-BUCKLING-TRAPS.md) |
| 銲接接合 An = Ag，但 Ae = UAg | ⭐⭐⭐ | [TENSION-MEMBER-TRAPS](TENSION-MEMBER-TRAPS.md) |

---

*每次 ingest 含新陷阱的題目時自動更新*
