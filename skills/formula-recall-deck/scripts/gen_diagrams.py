#!/usr/bin/env python3
"""觀念圖渲染（範本 — 複製到工作目錄後換成自己的圖）

下面的字型與色盤 boilerplate 直接可用，不要動；把最底下的示範圖換成
`references/deck-blueprint.md`「觀念圖四種原型」裡對應的圖。
完整可執行的六張實例見 `references/example-gen_diagrams-SS-U1-1.py`。

輸出 diagram_imgs/*.png 與 diagram_manifest.json，供 lib.js 的 diagramSlide 讀取。
執行：python3 gen_diagrams.py

每加一兩張就跑一次，並且**一定要把 PNG 讀出來實際看過**——標籤重疊在程式碼裡看不出來。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np
import json, os

OUT_DIR = "diagram_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

# 對齊 lib.js 的色盤，圖表才會跟簡報融為一體
NAVY = "#1B2A41"
STEEL = "#4C6B8A"
ACCENT = "#E8734A"
ICE = "#DCE6F0"
SUB = "#5C7A99"
GRID = "#E3E9F0"
GREEN = "#1E8449"

# --- CJK 字型：一定要先 addfont 再設 rcParams，且內部名稱是 JP（見 pitfalls #2）---
import matplotlib.font_manager as fm
fm.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.color"] = NAVY
plt.rcParams["axes.edgecolor"] = SUB
plt.rcParams["axes.labelcolor"] = NAVY
plt.rcParams["xtick.color"] = SUB
plt.rcParams["ytick.color"] = SUB

manifest = {}


def save(fig, fid, pad=0.12):
    path = os.path.join(OUT_DIR, f"{fid}.png")
    fig.savefig(path, dpi=220, transparent=True, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(path).size
    manifest[fid] = {"file": path, "ar": w / h}


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(SUB)
    ax.spines["bottom"].set_color(SUB)
    ax.grid(True, color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)


# ===================================================================
# 原型①：設計曲線疊圖 — 把理想曲線、設計曲線、舊版寫法疊在一起，
# 標出轉折點，並用箭頭說明兩條線之間的差距代表什麼物理現象。
# ===================================================================
fig, ax = plt.subplots(figsize=(7.6, 5.0))
style_axes(ax)
x = np.linspace(0.01, 2.4, 400)
ideal = 1.0 / x**2
ax.plot(x, np.where(ideal <= 1.25, ideal, np.nan), color=SUB, linestyle="--",
        linewidth=1.8, label="理想曲線")
design = np.where(x <= 1.5, 0.658**(x**2), 0.877 / x**2)
ax.plot(x, design, color=NAVY, linewidth=3.4, zorder=5, label="設計曲線")
ax.axvline(1.5, color=ACCENT, linestyle=":", linewidth=1.5)
ax.plot([1.5], [0.658**2.25], "o", color=ACCENT, markersize=8, zorder=8)
ax.annotate("轉折點\n（標出座標值）", xy=(1.5, 0.39), xytext=(1.62, 0.62),
            fontsize=10.5, color=ACCENT, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, linewidth=1.4))
ax.fill_between(x, 0, design, color=ICE, alpha=0.55, zorder=0)
ax.set_xlim(0, 2.4); ax.set_ylim(0, 1.25)
ax.set_xlabel("（無因次參數）", fontsize=12)
ax.set_ylabel("（強度比）", fontsize=12)
ax.legend(fontsize=9.5, loc="upper right", frameon=True, framealpha=0.95)
save(fig, "example_curve")


# ===================================================================
# 原型④：取小／取大長條圖 — 三根長條加一條控制值虛線。
# 比任何文字說明都有效，適合「N 個都要算然後取極值」的題型。
# ===================================================================
fig, ax = plt.subplots(figsize=(7.6, 4.4))
style_axes(ax)
labels = ["情況一\n（公式）", "情況二\n（公式）", "情況三\n（公式）"]
vals = [100, 86, 78]
bars = ax.bar(labels, vals, color=[STEEL, STEEL, ACCENT], width=0.55, zorder=3)
ax.axhline(min(vals), color=ACCENT, linestyle="--", linewidth=2)
ax.text(0.42, min(vals) + 4, "控制值＝三者最小", fontsize=12, color=ACCENT,
        fontweight="bold", ha="center")
ax.set_ylim(0, 120); ax.set_yticks([])
ax.set_ylabel("設計強度（示意）", fontsize=12)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 3, str(v), ha="center",
            fontsize=11, color=NAVY, fontweight="bold")
save(fig, "example_minmax")


# ===================================================================
# 原型②③（標註幾何草圖 / 破壞面圖）請參考
# references/example-gen_diagrams-SS-U1-1.py 的 net_area、shear_lag、block_shear。
# 要點：ax.axis("off") + 資料座標畫圖，尺寸線用
# ax.annotate("", xy=..., xytext=..., arrowprops=dict(arrowstyle="<->"))
# ===================================================================

with open("diagram_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"完成 {len(manifest)} 張圖　→ 請逐張讀出 PNG 目視檢查標籤是否重疊")
