# 壓密特性

**分類 ID：** consolidation-properties
**知識層：** Layer 6 材料行為

---

## 範疇

飽和黏土在附加應力下隨時間排水、體積縮小的行為，決定長期沉陷量與沉陷速率，是淺基礎設計不可或缺的一環。

## 行為特性對照

- **正常壓密黏土（NC）：** 目前有效覆土應力即為歷史最大值（OCR=1），沉陷對附加應力較敏感，需用較大的壓縮指數 $C_c$。
- **過壓密黏土（OC）：** 歷史曾承受更大應力（OCR>1），若附加應力後總應力仍小於過壓密應力 $p_c'$，僅產生較小的回彈/再壓縮沉陷（用 $C_r \ll C_c$）；一旦超過 $p_c'$ 則需分段計算（見 [[PRECONSOLIDATION-PRESSURE]]）。
- **壓密速率：** 由壓密係數 $C_v$ 與排水路徑長 $H_{dr}$ 共同決定（見 [[COEFFICIENT-OF-CONSOLIDATION]]），雙向排水的壓密速率遠快於單向排水（時間需求為 4 倍差異，因 $T_v \propto 1/H_{dr}^2$）。

## 常見陷阱

正常壓密與過壓密段落誤用同一壓縮指數；忽略取樣擾動會使實驗室量測的 $p_c'$ 偏低、$C_c$ 曲線圓弧段不明顯；壓密度 $U\ge60\%$ 時仍誤用拋物線近似公式。

## 相關概念與方法

[[CONSOLIDATION-THEORY]]、[[PRECONSOLIDATION-PRESSURE]]、[[COEFFICIENT-OF-CONSOLIDATION]]、[[consolidation-settlement-method]]

## 案例對應題目

- [[SM-2025-1]]
- [[SM-2024-3]]
- [[SM-2018-1]]
- [[SM-2016-1]]
- [[SM-2012-2]]
