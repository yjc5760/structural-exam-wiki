# 剪力強度特性

**分類 ID：** shear-strength-properties
**知識層：** Layer 6 材料行為

---

## 範疇

土壤抵抗剪力破壞的能力，是承載力、土壓力、邊坡穩定三大類分析共同的力學基礎，依土壤種類與排水條件呈現截然不同的行為。

## 行為特性對照

- **砂土：** 強度幾乎全來自摩擦角 $\phi'$（$c'\approx0$），密度愈高（$D_r$愈大）$\phi'$愈大，且可能出現剪脹（dilatancy）現象；一般用直接剪力試驗或三軸 CD 試驗量測。
- **飽和黏土（短期）：** 施工期不排水，以 $\phi=0$、不排水剪力強度 $S_u$ 描述（見 [[UNDRAINED-SHEAR-STRENGTH]]），$S_u$ 隨深度（有效覆土應力）增加而增加，並受擾動後靈敏度影響大幅降低。
- **飽和黏土（長期）：** 排水完成後以有效應力參數 $c', \phi'$ 描述（CD 或 CU+孔隙水壓量測試驗求得），見 [[MOHR-COULOMB-FAILURE-CRITERION]]。

## 常見陷阱

對黏土短期問題誤用有效應力參數（忽略孔隙水壓來不及消散）；正常壓密黏土 $S_u$ 誤用定值而非隨深度變化；三軸試驗類型（UU/CU/CD）與分析情境不對應（見 [[TRIAXIAL-TEST-TYPES]]）。

## 相關概念與方法

[[MOHR-COULOMB-FAILURE-CRITERION]]、[[UNDRAINED-SHEAR-STRENGTH]]、[[TRIAXIAL-TEST-TYPES]]

## 案例對應題目

- [[SM-2025-2]]
- [[SM-2024-1]]
- [[SM-2018-2]]
- [[SM-2013-3]]
- [[SM-2012-1]]
- [[SM-2010-1]]
