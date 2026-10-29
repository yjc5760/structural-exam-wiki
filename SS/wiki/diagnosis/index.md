# 題型診斷層 — 考題進入點地圖

> **用法：** 拿到考題後，先對照下表找到題型，再按診斷頁的決策樹決定「用哪個 Method、需要哪些 Concept、注意哪些 Trap」。

---

## 快速分類表

| 題型 | 關鍵辨識特徵 | 診斷頁 |
|------|------------|--------|
| 拉力桿件 | 「拉力」「拉桿」「承拉」「接合長度」「U 值」 | [[tension-member]] |
| 壓力桿件 | 「受壓柱」「有效長度」「KL/r」「λc」「Cc」 | [[compression-member]] |
| 梁桿件 | 「受彎」「彎矩強度」「無束制長度 Lb」「撓度」 | [[beam]] |
| 梁柱桿件 | 「軸力 + 彎矩」「互制」「B1B2」「梁柱」 | [[beam-column]] |
| 接合設計 | 「螺栓」「銲縫」「填角銲」「開槽銲」「偏心接合」 | [[connection]] |
| 斷面性質 | 「慣性矩」「斷面模數」「Zx」「形狀因子」「塑性中性軸」 | [[section-property]] |
| 耐震設計 | 「耐震」「強柱弱梁」「Panel Zone」「SMRF」「EBF」 | [[seismic]] |
| 概念／規範題 | 「說明」「比較」「依規範」「定義」「差異」 | [[conceptual]] |

---

## 跨題型組合（複合題型）

歷屆常見複合組合：

| 組合 | 典型題目 | 主要 Method |
|------|---------|------------|
| 壓力 + 彎矩 | 梁柱桿件 | lrfd-column → pm-interaction → b1b2 |
| LTB + 使用性 | 梁設計 | ltb-3zone → 撓度公式 |
| 拉力 + 接合 | 拉力構材設計 | block-shear + shear-lag-u |
| 挫屈 + 對位圖 | 剛架穩定 | effective-length-chart → lrfd-column |
| 強柱弱梁 + P-M | 耐震梁柱 | pm-interaction + 耐震規定 |

---

## 各診斷頁

- [[tension-member]] — 拉力桿件
- [[compression-member]] — 壓力桿件
- [[beam]] — 梁桿件
- [[beam-column]] — 梁柱桿件
- [[connection]] — 接合設計
- [[section-property]] — 斷面性質
- [[seismic]] — 耐震設計
- [[conceptual]] — 概念／規範題
