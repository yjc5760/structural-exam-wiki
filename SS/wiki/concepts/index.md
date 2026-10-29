# 概念索引（Concepts Index）

> 共 60 個概念頁，每頁含：定義、關鍵公式、常見陷阱、出現題目。
> 三種瀏覽方式：依知識分類 | 依出現頻率 | 依字母

---

## 依知識分類

### Part 1.1 拉力及壓力桿件

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 殘留應力 | [RESIDUAL-STRESS](RESIDUAL-STRESS.md) | 翼板端壓應力 ≈ 0.3Fy，使非彈性挫屈提前 |
| 切線模數理論 | [TANGENT-MODULUS-THEORY](TANGENT-MODULUS-THEORY.md) | Et < E → Fcr = π²Et/(KL/r)² |
| 柱強度曲線 | [COLUMN-STRENGTH-CURVE](COLUMN-STRENGTH-CURVE.md) | Fcr vs λc 三段式 |
| 歐拉彈性挫屈 | [EULER-BUCKLING](EULER-BUCKLING.md) | Pe = π²EI/(KL)² |
| 彎曲挫屈（一般） | [FLEXURAL-BUCKLING-GENERAL](FLEXURAL-BUCKLING-GENERAL.md) | 整體挫屈 vs 局部挫屈 |
| 扭轉挫屈 | [TORSIONAL-BUCKLING](TORSIONAL-BUCKLING.md) | 開口薄壁斷面特有 |
| 拉力構材設計 | [TENSION-MEMBER-DESIGN](TENSION-MEMBER-DESIGN.md) | GSY / NSF / BSR 三種失敗 |
| 有效淨面積 Ae | [EFFECTIVE-NET-AREA](EFFECTIVE-NET-AREA.md) | Ae = U·An |
| 剪力遲滯 | [SHEAR-LAG](SHEAR-LAG.md) | U = 1 - x̄/L |
| 塊狀剪力撕裂 | [BLOCK-SHEAR-RUPTURE](BLOCK-SHEAR-RUPTURE.md) | 剪力面 + 拉力面複合破壞 |
| 箱型柱 | [BOX-COLUMN](BOX-COLUMN.md) | 閉口截面，高扭轉剛度，無 LTB |
| 弱軸彎曲與挫屈 | [WEAK-AXIS-BEHAVIOR](WEAK-AXIS-BEHAVIOR.md) | 取兩軸 KL/r 大值；弱軸無 LTB |

### Part 1.2 撓曲桿件

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 結實斷面 / 寬厚比 | [COMPACT-SECTION](COMPACT-SECTION.md) | λ ≤ λp → 結實（可達 Mp），λ > λr → 細長 |
| 使用性撓度限制 | [SERVICEABILITY-DEFLECTION](SERVICEABILITY-DEFLECTION.md) | δL ≤ L/360（活載重，服務載重，不因數化） |
| 側向扭轉挫屈 LTB | [LATERAL-TORSIONAL-BUCKLING](LATERAL-TORSIONAL-BUCKLING.md) ⭐ | Lb → Lp/Lr → 三區段 Mn |
| 彎矩梯度係數 Cb | [BENDING-MODIFICATION-FACTOR-CB](BENDING-MODIFICATION-FACTOR-CB.md) | 四點法，均布彎矩 Cb=1 最保守 |
| 初始降伏彎矩 My | [YIELD-MOMENT-MY](YIELD-MOMENT-MY.md) | My = Fy·Sx |
| 塑性彎矩 Mp | [PLASTIC-MOMENT-MP](PLASTIC-MOMENT-MP.md) | Mp = Fy·Zx |
| 塑性中性軸 PNA | [PLASTIC-NEUTRAL-AXIS-PNA](PLASTIC-NEUTRAL-AXIS-PNA.md) | 等面積軸，非對稱≠ENA |
| 形狀因數 f | [SHAPE-FACTOR](SHAPE-FACTOR.md) | f = Zx/Sx，H型鋼≈1.12 |
| 張力場效應 | [TENSION-FIELD-ACTION](TENSION-FIELD-ACTION.md) | 腹板挫屈後斜向拉力帶承載 |
| 板梁設計 | [PLATE-GIRDER-DESIGN](PLATE-GIRDER-DESIGN.md) | h/tw > 5.70√(E/Fy)，需加勁 |
| 梁之剪力流 | [SHEAR-FLOW-BEAM](SHEAR-FLOW-BEAM.md) | q = VQ/I |
| 梁之雙軸彎曲 | [BIAXIAL-BENDING-BEAM](BIAXIAL-BENDING-BEAM.md) | 強軸 + 弱軸，弱軸無LTB |
| 腹板剪力挫屈 | [SHEAR-BUCKLING-WEB](SHEAR-BUCKLING-WEB.md) | h/tw 控制剪力強度 |
| 腹板局部降伏 | [WEB-LOCAL-YIELDING](WEB-LOCAL-YIELDING.md) | 集中力下腹板局部應力 |
| 腹板挫皺 | [WEB-CRIPPLING](WEB-CRIPPLING.md) | 集中力下腹板端部挫皺 |
| 承壓加勁板 | [BEARING-STIFFENER](BEARING-STIFFENER.md) | 防止腹板局部失穩 |

### Part 1.3 梁柱桿件

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 梁柱互制行為 | [BEAM-COLUMN-INTERACTION](BEAM-COLUMN-INTERACTION.md) ⭐ | P-M 互制：H1-1a/b |
| P-Δ 效應 | [P-DELTA-EFFECT](P-DELTA-EFFECT.md) | 側移引起附加彎矩 |
| 彎矩放大 B1/B2 | [MOMENT-AMPLIFICATION-B1-B2](MOMENT-AMPLIFICATION-B1-B2.md) | B1 放大構件曲率，B2 放大層間漂移 |
| 彎矩放大 Cm | [MOMENT-AMPLIFICATION-CM](MOMENT-AMPLIFICATION-CM.md) | 端部彎矩比對 B1 的修正 |
| 二階分析 | [SECOND-ORDER-ANALYSIS](SECOND-ORDER-ANALYSIS.md) | 含幾何非線性的分析 |
| 塑性鉸 | [PLASTIC-HINGE](PLASTIC-HINGE.md) | M = Mp 且允許相對轉動 |
| 構架穩定性（進階） | [FRAME-STABILITY-ADVANCED](FRAME-STABILITY-ADVANCED.md) | 整體結構二階效應 |
| 靠桿效應 | [LEANER-COLUMN-EFFECT](LEANER-COLUMN-EFFECT.md) | 無抵抗側移能力的柱增加 ΣPu |

### Part 1.4 接合設計

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 接合設計概論 | [CONNECTION-DESIGN](CONNECTION-DESIGN.md) | 強接合弱構材原則 |
| 螺栓接合設計 | [BOLTED-CONNECTION-DESIGN](BOLTED-CONNECTION-DESIGN.md) | 剪斷/承壓/滑動三種模式 |
| 摩阻型接合 | [SLIP-CRITICAL-CONNECTION](SLIP-CRITICAL-CONNECTION.md) | 夾緊力×摩擦係數×接觸面數 |
| 承壓型螺栓接合 | [BEARING-TYPE-CONNECTION](BEARING-TYPE-CONNECTION.md) | 螺栓桿承剪，板面承壓 |
| 高拉力螺栓施工 | [HIGH-STRENGTH-BOLT-PRACTICE](HIGH-STRENGTH-BOLT-PRACTICE.md) | 預拉力、摩擦面、施工順序 |
| 銲接接合設計 | [WELDED-CONNECTION-DESIGN](WELDED-CONNECTION-DESIGN.md) | 填角銲/開槽銲強度 |
| 填角銲設計 | [FILLET-WELD-DESIGN](FILLET-WELD-DESIGN.md) | 0.707w 有效喉厚 × 0.6FEXX 設計 |
| 偏心接合 | [ECCENTRIC-CONNECTION](ECCENTRIC-CONNECTION.md) | 剪力 + 扭矩，彈性向量法，Jp = Σr² |
| 銲接施工實務 | [WELDING-PRACTICE](WELDING-PRACTICE.md) | 最小/最大銲腳、最小長度 |
| 銲接方法 | [WELDING-PROCESSES](WELDING-PROCESSES.md) | SMAW/GMAW/SAW/FCAW |
| 銲道瑕疵 | [WELD-DEFECTS](WELD-DEFECTS.md) | 裂縫/氣孔/夾渣/未熔合 |
| 銲道 NDT | [WELD-INSPECTION-NDT](WELD-INSPECTION-NDT.md) | VT/MT/PT/UT/RT 選擇 |
| 剪力釘 | [SHEAR-CONNECTOR](SHEAR-CONNECTOR.md) | 組合梁界面剪力傳遞 |

### Part 2：組合構件

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 合成梁 | [COMPOSITE-BEAM](COMPOSITE-BEAM.md) | 鋼梁 + 混凝土板，有效寬度 be |
| 合成柱 | [COMPOSITE-COLUMN](COMPOSITE-COLUMN.md) | 包覆型 or 填充型 |
| 包覆型 SRC 梁 | [CONCRETE-ENCASED-BEAM](CONCRETE-ENCASED-BEAM.md) | 混凝土包覆鋼梁 |

### Part 2.1 耐震設計

| 概念 | 頁面 | 核心一句話 |
|------|------|----------|
| 耐震設計哲學 | [SEISMIC-DESIGN-PHILOSOPHY](SEISMIC-DESIGN-PHILOSOPHY.md) | 容量設計，延性耗能 |
| 耐震鋼材 SN 系列 | [SEISMIC-STEEL-SN](SEISMIC-STEEL-SN.md) | SN490B：Fy上下限 + 降伏比≤0.80 |
| 容量設計法 | [CAPACITY-DESIGN](CAPACITY-DESIGN.md) | 強構材承擔弱構材超強後的力 |
| 強柱弱梁 | [STRONG-COLUMN-WEAK-BEAM](STRONG-COLUMN-WEAK-BEAM.md) | ΣφcMpc ≥ ΣφbMpb |
| 節點域 Panel Zone | [PANEL-ZONE](PANEL-ZONE.md) | tz ≥ (dz + wz)/90 |
| RBS 犬骨接頭 | [REDUCED-BEAM-SECTION](REDUCED-BEAM-SECTION.md) | 翼板削弱 → 塑性鉸遠離接頭 |
| 耐震接頭細部 | [SEISMIC-CONNECTION-DETAILS](SEISMIC-CONNECTION-DETAILS.md) | 背銲條、全滲透銲道 |
| 連續板 | [CONTINUITY-PLATE](CONTINUITY-PLATE.md) | 梁翼板力傳入柱腹板 |

---

## 依出現頻率排序（前 15 高頻概念）

| 排名 | 概念 | 出現題數 | 頁面 |
|------|------|---------|------|
| 1 | 側向扭轉挫屈 LTB | 13+ 題 | [LATERAL-TORSIONAL-BUCKLING](LATERAL-TORSIONAL-BUCKLING.md) |
| 2 | 梁柱互制行為 | 9 題 | [BEAM-COLUMN-INTERACTION](BEAM-COLUMN-INTERACTION.md) |
| 3 | 殘留應力 | 7 題 | [RESIDUAL-STRESS](RESIDUAL-STRESS.md) |
| 4 | 塊狀剪力撕裂 | 7 題 | [BLOCK-SHEAR-RUPTURE](BLOCK-SHEAR-RUPTURE.md) |
| 5 | 彎矩放大 B1/B2 | 6 題 | [MOMENT-AMPLIFICATION-B1-B2](MOMENT-AMPLIFICATION-B1-B2.md) |
| 6 | 塑性彎矩 Mp | 6 題 | [PLASTIC-MOMENT-MP](PLASTIC-MOMENT-MP.md) |
| 7 | 強柱弱梁 | 5 題 | [STRONG-COLUMN-WEAK-BEAM](STRONG-COLUMN-WEAK-BEAM.md) |
| 8 | 銲接施工實務 | 5 題 | [WELDING-PRACTICE](WELDING-PRACTICE.md) |
| 9 | 剪力遲滯 | 5 題 | [SHEAR-LAG](SHEAR-LAG.md) |
| 10 | 柱強度曲線 | 5 題 | [COLUMN-STRENGTH-CURVE](COLUMN-STRENGTH-CURVE.md) |
| 11 | P-Δ 效應 | 5 題 | [P-DELTA-EFFECT](P-DELTA-EFFECT.md) |
| 12 | 彎矩梯度係數 Cb | 4 題 | [BENDING-MODIFICATION-FACTOR-CB](BENDING-MODIFICATION-FACTOR-CB.md) |
| 13 | 容量設計法 | 4 題 | [CAPACITY-DESIGN](CAPACITY-DESIGN.md) |
| 14 | 銲道 NDT | 4 題 | [WELD-INSPECTION-NDT](WELD-INSPECTION-NDT.md) |
| 15 | 歐拉彈性挫屈 | 4 題 | [EULER-BUCKLING](EULER-BUCKLING.md) |

---

## 依字母排序（全部 58 概念）

| 概念 | ID | 分類 |
|------|-----|------|
| P-Δ 效應 | P-DELTA-EFFECT | 梁柱 |
| RBS 犬骨接頭 | REDUCED-BEAM-SECTION | 耐震 |
| 二階分析 | SECOND-ORDER-ANALYSIS | 梁柱 |
| 包覆型 SRC 梁 | CONCRETE-ENCASED-BEAM | 組合 |
| 塊狀剪力撕裂 | BLOCK-SHEAR-RUPTURE | 拉力 |
| 切線模數理論 | TANGENT-MODULUS-THEORY | 壓力 |
| 合成梁 | COMPOSITE-BEAM | 組合 |
| 合成柱 | COMPOSITE-COLUMN | 組合 |
| 有效淨面積 Ae | EFFECTIVE-NET-AREA | 拉力 |
| 扭轉挫屈 | TORSIONAL-BUCKLING | 壓力 |
| 承壓加勁板 | BEARING-STIFFENER | 梁 |
| 承壓型螺栓 | BEARING-TYPE-CONNECTION | 接合 |
| 剪力遲滯 | SHEAR-LAG | 拉力 |
| 剪力釘 | SHEAR-CONNECTOR | 組合 |
| 初始降伏彎矩 My | YIELD-MOMENT-MY | 梁 |
| 容量設計法 | CAPACITY-DESIGN | 耐震 |
| 張力場效應 | TENSION-FIELD-ACTION | 梁 |
| 強柱弱梁 | STRONG-COLUMN-WEAK-BEAM | 耐震 |
| 梁之剪力流 | SHEAR-FLOW-BEAM | 梁 |
| 梁之雙軸彎曲 | BIAXIAL-BENDING-BEAM | 梁 |
| 梁柱互制行為 | BEAM-COLUMN-INTERACTION | 梁柱 |
| 接合設計概論 | CONNECTION-DESIGN | 接合 |
| 彎矩放大 B1/B2 | MOMENT-AMPLIFICATION-B1-B2 | 梁柱 |
| 彎矩放大 Cm | MOMENT-AMPLIFICATION-CM | 梁柱 |
| 彎矩梯度係數 Cb | BENDING-MODIFICATION-FACTOR-CB | 梁 |
| 彎曲挫屈（一般） | FLEXURAL-BUCKLING-GENERAL | 壓力 |
| 腹板剪力挫屈 | SHEAR-BUCKLING-WEB | 梁 |
| 腹板局部降伏 | WEB-LOCAL-YIELDING | 梁 |
| 腹板挫皺 | WEB-CRIPPLING | 梁 |
| 塑性中性軸 PNA | PLASTIC-NEUTRAL-AXIS-PNA | 梁 |
| 塑性彎矩 Mp | PLASTIC-MOMENT-MP | 梁 |
| 塑性鉸 | PLASTIC-HINGE | 梁柱 |
| 節點域 Panel Zone | PANEL-ZONE | 耐震 |
| 靠桿效應 | LEANER-COLUMN-EFFECT | 梁柱 |
| 摩阻型接合 | SLIP-CRITICAL-CONNECTION | 接合 |
| 耐震接頭細部 | SEISMIC-CONNECTION-DETAILS | 耐震 |
| 耐震設計哲學 | SEISMIC-DESIGN-PHILOSOPHY | 耐震 |
| 歐拉彈性挫屈 | EULER-BUCKLING | 壓力 |
| 構架穩定性（進階） | FRAME-STABILITY-ADVANCED | 梁柱 |
| 銲接接合設計 | WELDED-CONNECTION-DESIGN | 接合 |
| 銲接施工實務 | WELDING-PRACTICE | 接合 |
| 銲接方法 | WELDING-PROCESSES | 接合 |
| 銲道 NDT | WELD-INSPECTION-NDT | 接合 |
| 銲道瑕疵 | WELD-DEFECTS | 接合 |
| 螺栓接合設計 | BOLTED-CONNECTION-DESIGN | 接合 |
| 殘留應力 | RESIDUAL-STRESS | 壓力 |
| 形狀因數 f | SHAPE-FACTOR | 梁 |
| 板梁設計 | PLATE-GIRDER-DESIGN | 梁 |
| 柱強度曲線 | COLUMN-STRENGTH-CURVE | 壓力 |
| 連續板 | CONTINUITY-PLATE | 耐震 |
| 偏心接合 | ECCENTRIC-CONNECTION | 接合 |
| 填角銲設計 | FILLET-WELD-DESIGN | 接合 |
| 高拉力螺栓施工 | HIGH-STRENGTH-BOLT-PRACTICE | 接合 |
| 側向扭轉挫屈 LTB | LATERAL-TORSIONAL-BUCKLING | 梁 |
| 拉力構材設計 | TENSION-MEMBER-DESIGN | 拉力 |
| 使用性撓度限制 | SERVICEABILITY-DEFLECTION | 梁 |
| 弱軸彎曲與挫屈 | WEAK-AXIS-BEHAVIOR | 壓力/梁柱 |
| 結實斷面 / 寬厚比 | COMPACT-SECTION | 梁 |
| 耐震鋼材 SN 系列 | SEISMIC-STEEL-SN | 耐震/材料 |
| 箱型柱 | BOX-COLUMN | 壓力/梁柱 |

---

## 相關導航

- [術語速查 GLOSSARY →](GLOSSARY.md)（符號定義 · 公式 · 設計法對照）
- [方法論索引 →](../methods/index.md)（計算步驟層）
- [題型診斷 →](../diagnosis/index.md)（從題目出發）
- [陷阱總覽 →](../traps/index.md)（常見錯誤）
- [wiki 主索引 →](../index.md)

---

*每次 compile-all 或 ingest 後自動更新*
