#!/usr/bin/env python3
"""公式 LaTeX 渲染（範本 — 複製到工作目錄後填入 FORMULAS）

用 matplotlib 的 mathtext 引擎產生真正的 LaTeX 排版，不需要安裝完整 TeX。
輸出 formula_imgs/*.png 與 formula_manifest.json（id -> {file, ar}），
供 lib.js 的 formulaSlide / cheatSheetSlide 讀取尺寸並置入。

執行：python3 gen_formulas.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json, os, re

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"   # 對齊 lib.js 的 C.navy
DPI = 400
FONTSIZE = 30

plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

# ---------------------------------------------------------------------------
# 填這裡。id 用簡短好記的名字（lambda_c、fcr_new1、an…），deck.js 會直接引用。
# 每一條都用 raw string 包在 $...$ 裡。
#
# 可用：\frac \sqrt \sum \left \right \bar \max \min \leq \geq \times \cdot
#       \approx \quad 以及希臘字母。
# 不可用：\le \ge \tfrac \textstyle \begin{aligned}（下方會自動擋下）
# 中文一律不能出現在這裡，放到 deck.js 的 label / note / insights。
# ---------------------------------------------------------------------------
FORMULAS = {
    "example_1": r"$\lambda_c = \frac{KL}{r\,\pi}\sqrt{\frac{F_y}{E}}$",
    "example_2": r"$F_{cr} = \left(0.658^{\ \lambda_c^2}\right) F_y \qquad (\lambda_c \leq 1.5)$",
}

# --- 防呆：中文混入數學區塊、以及 mathtext 不支援的巨集 ---
for fid, s in FORMULAS.items():
    if re.findall(r"[\u4e00-\u9fff]", s):
        raise SystemExit(f"[中止] 中文出現在數學區塊：{fid}　→ 改放到 deck.js 的 label/note")
    for bad in [r"\le ", r"\ge ", r"\tfrac", r"\textstyle", r"\begin{"]:
        if bad in s:
            raise SystemExit(f"[中止] mathtext 不支援 {bad.strip()}：{fid}　→ 改寫成 \\leq / \\geq / \\frac")

manifest, errors = {}, []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
        # pad_inches 給根號／分式堆疊留安全邊界，太小會在某些尺寸被裁切
        fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.08)
        plt.close(fig)
        from PIL import Image
        w, h = Image.open(path).size
        manifest[fid] = {"file": path, "ar": w / h}
    except Exception as e:
        errors.append((fid, str(e)))
        plt.close(fig)

with open("formula_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"完成 {len(manifest)} 條，{len(errors)} 條失敗")
for fid, err in errors:
    print("  ERROR", fid, err)

# 提示哪些公式太寬，速查表要放在 cols:2 那一頁（見 references/pitfalls.md #3）
wide = [fid for fid, m in manifest.items() if m["ar"] > 8]
if wide:
    print("\n寬公式（ar>8，速查表請用 cols:2）：", ", ".join(wide))
