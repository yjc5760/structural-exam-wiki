# 設計哲學總覽

**來源：** CLAUDE-SOLVE.md「設計哲學框架」章節（原 design_philosophy.json 已整合）

| 哲學 ID | 設計法 | 命題大綱 | 核心原則 |
|--------|--------|---------|---------|
| [lrfd-beam](lrfd-beam.md) | LRFD | SS-U1-2 梁桿件 | φbMn 取所有極限狀態最脆弱一環 |
| [lrfd-column](lrfd-column.md) | LRFD | SS-U1-1 壓力桿件 | λc 兩段式 Fcr |
| [asd-column](asd-column.md) | ASD | SS-U1-1 壓力桿件 | fa ≤ Fa，Cc 判斷 |
| [lrfd-tension](lrfd-tension.md) | LRFD | SS-U1-1 拉力桿件 | 三種極限狀態取最小值 |
| [lrfd-connection](lrfd-connection.md) | LRFD | SS-U1-4 接合設計 | 填角銲 + 高拉力螺栓 |
| [lrfd-beam-column-box](lrfd-beam-column-box.md) | LRFD | SS-U1-3 梁柱桿件 | BOX 斷面 P-M 互制 |
| [asd-pin-tension](asd-pin-tension.md) | ASD | SS-U1-1 插銷拉力構件 | 四種破壞模式 |
| [probability-analysis](probability-analysis.md) | — | SD-U3-1 耐震 | 強柱弱梁機率分析 |
| [lrfd-phi-values](lrfd-phi-values.md) | LRFD | 通用 | φ 值三維度邏輯：延性/不確定性/後果，φ×Ω≈1.5 |
| [b1-b2-amplification](b1-b2-amplification.md) | LRFD | SS-U1-3 梁柱桿件 | B1/B2 分別放大 P-δ 與 P-Δ；Pe1 不側移 K、PeK 側移 K |
