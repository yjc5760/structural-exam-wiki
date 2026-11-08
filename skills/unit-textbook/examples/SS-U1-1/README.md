# 範例：SS-U1-1 拉力及壓力桿件（上冊：拉力篇 第 0～2 章）

完整成品在 exam-wiki-SS：`study/textbook-SS-U1-1-tension.html`、`textbook-SS-U1-1-compression.html`（共 13 章、57 張圖）。
這裡只放第 0～2 章的原始碼，示範：

- `textbook.json`：分冊設定（上冊 tension、下冊 compression；章號跨冊連續）
- `calcs.py`：所有數值（第 1 章 H100 拉／壓對照、第 2～5 章貫穿全冊的角鋼範例、柱曲線、殘留應力…）
- `ch0.html`＋`figs_ch0.py`：讀法、種子表、種子家族樹
- `ch1.html`＋`figs_ch1.py`：拉與壓的差別（向量合成 → 彈簧模型 → 柱即彈簧推出 \(L^2\)）
- `ch2.html`＋`figs_ch2.py`：GSY／NSF 與 φ、ASD ＝ LRFD ÷ 1.5、臨界比 \(1.2F_y/F_u\)

試跑：把 `scripts/lib.py`、`plot.py`、`build.py`、`render_check.py` 複製進來，
在 `textbook.json` 把 tension 的 chapters 改成 `["ch0","ch1","ch2"]`，
放到某個 `study/figs-src/xxx/` 底下（`study/assets/katex/` 要存在）後執行 `python3 build.py tension`。
