# 題型診斷：概念／規範題

---

## 辨識關鍵字

`說明` `比較` `定義` `依規範` `敘述` `差異` `原理` `為什麼` `圖示` `繪圖說明` `列舉`

---

## 決策樹

```
看到「說明…」「比較…」「依規範…」「定義…」
    │
    ├─ 比較兩種設計法
    │       ASD vs LRFD
    │       → Philosophy: [[lrfd-phi-values]]
    │         重點：安全係數方式、載重組合、可靠度基礎
    │
    ├─ 解釋某個現象
    │       「說明 LTB 的發生原因」
    │       「說明殘留應力的影響」
    │       「說明剪力遲滯」
    │       → 找對應 Concept 頁
    │         說明：定義 → 公式 → 物理意義 → 影響
    │
    ├─ 比較兩個類似概念
    │       「Single V vs Single Bevel」
    │       「結實斷面 vs 非結實斷面」
    │       「側移框架 vs 無側移框架」
    │       → 用表格對比：
    │         | 項目 | A | B |
    │         答題格式：定義各自 → 差異點 → 適用場合
    │
    ├─ 規範施工規定（填空型）
    │       「螺栓間距不得小於？」
    │       「預拉力應達幾倍 Fu？」
    │       → Concept: [[HIGH-STRENGTH-BOLT-PRACTICE]]
    │         [[WELDING-PRACTICE]] [[WELD-INSPECTION-NDT]]
    │
    ├─ 耐震規定（條文型）
    │       「說明如何滿足強柱弱梁」
    │       「Panel Zone 最小厚度規定」
    │       → Diagnosis: [[seismic]]
    │         Concept: [[STRONG-COLUMN-WEAK-BEAM]] [[PANEL-ZONE]]
    │
    └─ 繪圖說明
            「繪出 P-M 互制曲線」
            「繪出 φbMn vs Lb 曲線」
            「繪出柱強度曲線 Fcr/Fy vs λc」
            → 對應 Concept/Method 頁的圖形部分
              P-M：[[pm-interaction]]
              LTB：[[ltb-3zone]]
              柱曲線：[[lrfd-column]]
```

---

## 概念題答題格式指南

**說明題（「說明 XX」）**
```
① 定義：XX 是指…
② 發生條件：當…時發生
③ 規範處理方式：依規範，以…公式計算
④ 對設計的影響：XX 會使…降低/增加
```

**比較題（「比較 A 與 B」）**
```
① 各自定義（1-2 句）
② 表格對比（3-5 個比較面向）
③ 結論：適用場合各異
```

**繪圖題**
```
① 標示座標軸（含單位）
② 畫出曲線（折線/曲線，標關鍵點）
③ 標注區段（塑性區/非彈性/彈性）
④ 標注公式或數值（Lp, Lr 或 λc=1.5 等）
```

---

## 高頻概念題彙整（依出現次數）

| 主題 | 典型題型 | 對應頁面 |
|------|---------|---------|
| 強柱弱梁 | 說明如何驗核 | [[seismic]] |
| LTB 三區段 | 繪 φbMn vs Lb | [[ltb-3zone]] |
| P-M 互制 | 繪互制曲線 | [[pm-interaction]] |
| 柱強度曲線 | 繪 Fcr/Fy vs λc | [[lrfd-column]] |
| 殘留應力 | 說明來源與影響 | [[residual-stress]] |
| ASD vs LRFD | 比較兩種設計法 | [[lrfd-phi-values]] |
| 銲接規定 | 填空式條文 | [[WELDING-PRACTICE]] |
| SN 鋼材 | 說明分級與用途 | [[fracture-toughness]] |

---

## 相關 Methods / Concepts / Traps

- Philosophy: wiki/philosophy/
- Materials: wiki/materials/
- 歷屆題目: SS-2009-2, SS-2009-4, SS-2010-2, SS-2016-2, SS-2017-1
