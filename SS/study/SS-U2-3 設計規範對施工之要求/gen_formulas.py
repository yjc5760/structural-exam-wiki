#!/usr/bin/env python3
"""SS-U2-3 觀念講義 — 公式 PNG 渲染（matplotlib mathtext）

注意（踩過的坑）：
  * mathtext 只支援 LaTeX 子集：\\frac \\sqrt ^ _ \\sum \\left \\right 希臘字母
    \\leq \\geq \\times \\cdot \\quad；**不支援** \\le \\ge \\tfrac \\text \\begin。
  * `$...$` 內絕對不能放中文 —— cm 字型無 CJK 字面。中文一律寫在 deck.js 的
    label / note / insights。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json, os, re

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"
DPI, FONTSIZE = 400, 30
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

FORMULAS = {
    # --- 填角銲 ---
    "f_weld":    r"$\phi R_n = \phi \, (0.6 F_{EXX}) \, (0.707\,w) \, L \quad , \quad \phi = 0.75$",
    "f_throat":  r"$t_e = w \sin 45^\circ = \frac{w}{\sqrt{2}} = 0.707\,w$",
    "f_vm":      r"$\tau_y = \frac{F_y}{\sqrt{3}} = 0.577 F_y \; \longrightarrow \; 0.6 F_y$",
    "f_wcheck":  r"$1.25 \; \mathrm{kN/mm} \quad (w = 8\,\mathrm{mm},\; \mathrm{E70})$",
    # --- 銲腳與回銲 ---
    "f_wmin":    r"$w_{min} : \; t \leq 6 \rightarrow 3 \,;\; \leq 13 \rightarrow 5 \,;\; \leq 19 \rightarrow 6 \,;\; > 19 \rightarrow 8 \;\mathrm{mm}$",
    "f_wmax":    r"$w_{max} = t - 2\,\mathrm{mm} \quad (t \geq 6\,\mathrm{mm}) \; ; \quad w_{max} = t \quad (t < 6\,\mathrm{mm})$",
    "f_return":  r"$2w \leq \ell_{return} \leq 4w$",
    # --- 碳當量與預熱 ---
    "f_ce":      r"$C_{eq} = C + \frac{Mn}{6} + \frac{Cr+Mo+V}{5} + \frac{Ni+Cu}{15}$",
    "f_celim":   r"$C_{eq} \leq 0.44 \quad (\mathrm{SN490B})$",
    "f_preheat": r"$T_{preheat} \uparrow \;\Rightarrow\; \dot{T}_{cool} \downarrow \;,\; t_{H\,diffusion} \uparrow \;,\; \sigma_{residual} \downarrow$",
    # --- 韌性與 Z 向 ---
    "f_cvn":     r"$CVN \geq 27\,\mathrm{J} \quad @ \; 0^\circ \mathrm{C}$",
    "f_ra":      r"$RA_z \geq 25\% \quad (\mathrm{SN\!-\!C})$",
    # --- 高拉力螺栓 ---
    "f_tb":      r"$T_b = 0.7 F_u A_s \approx 0.88 F_y A_s$",
    "f_slip":    r"$\phi R_n = \phi \, \mu \, D_u \, h_{sc} \, T_b \, n_s$",
    "f_bear":    r"$\phi R_n = \phi \, (2.4 \, d \, t \, F_u) \quad , \quad \phi = 0.75$",
    "f_torque":  r"$T = K \, d \, T_b$",
    # --- 耐震加嚴 ---
    "f_tz":      r"$t_z \geq \frac{d_z + w_z}{90}$",
    "f_tzdef":   r"$d_z = d_{beam} - t_{f,beam} \quad , \quad w_z = d_{col} - t_{f,col}$",
    "f_yr":      r"$\frac{F_y}{F_u} \leq 0.80$",
    "f_capacity": r"$\sum M_{pc}^{*} \; > \; \sum M_{pb}^{*}$",
    # --- 防蝕 ---
    "f_emf":     r"$E_{Zn} = -0.76\,\mathrm{V} \; < \; E_{Fe} = -0.44\,\mathrm{V}$",
}

CJK = re.compile(r"[　-〿一-鿿＀-￯]")
bad = {k: v for k, v in FORMULAS.items() if CJK.search(v)}
if bad:
    raise SystemExit(f"CJK leaked into mathtext: {list(bad)}")
for k, v in FORMULAS.items():
    if re.search(r"\\le[^qf]|\\ge[^q]|\\tfrac", v):
        raise SystemExit(f"unsupported macro in {k}: {v}")

manifest, errors = {}, []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
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

print(f"Rendered {len(manifest)} formulas, {len(errors)} errors")
for fid, err in errors:
    print("ERROR", fid, err)
