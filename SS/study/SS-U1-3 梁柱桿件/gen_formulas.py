#!/usr/bin/env python3
"""TEMPLATE — copy this file into your job's working directory and fill in FORMULAS below
with every formula used across all decks in this batch (one shared dict/manifest, reused by
every deckN.js via lib.js's mathImg()).

Renders each formula as true LaTeX typesetting via matplotlib's mathtext engine — this gives
proper math typesetting (fractions, subscripts, square roots, Greek letters, etc.) without
needing a full TeX/LaTeX install. Writes transparent PNGs + a manifest.json mapping
id -> {file, ar (aspect ratio = width/height)} that lib.js's formulaSlide/cheatSheetSlide
read to size and place the image.

Run with: python3 gen_formulas.py    (produces formula_imgs/*.png + formula_manifest.json)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json, os

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"   # match lib.js's C.navy so formula images blend with the deck's ink color
DPI = 400
FONTSIZE = 30

# matplotlib mathtext (mathtext.fontset='cm') renders proper LaTeX-typeset math without
# requiring a full TeX install. Gotcha: mathtext supports a subset of real LaTeX — commands
# like \textstyle, \begin{aligned}, or anything requiring a package will throw a
# ParseSyntaxException. Stick to: \frac, \sqrt, super/subscripts (^ _), \sum, \left/\right,
# Greek letters (\lambda, \phi, \pi...), \leq/\geq/\times/\cdot, and plain multi-part strings
# joined with \quad for "formula, with a side condition" layouts.
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

# ---------------------------------------------------------------------------------------
# Fill this in. Use one short mnemonic id per formula (e.g. "d1_f1_1" = deck 1, formula
# group 1, item 1) — deckN.js will reference these ids by name in formulaSlide/cheatSheetSlide
# calls, so keep them stable once you start wiring up the decks.
#
# Wrap every entry in raw-string $...$ so backslashes aren't mangled by Python, e.g.:
#   "example_1": r"$F_{cr} = \left(0.658^{\lambda_c^2}\right) F_y$",
# ---------------------------------------------------------------------------------------
FORMULAS = {
    # --- 1. 二階效應的本質 ---
    "f_dm":     r"$\Delta M = P \cdot \delta$",
    "f_series": r"$1 + \alpha + \alpha^2 + \alpha^3 + \cdots = \frac{1}{1-\alpha} \quad , \quad \alpha = P/P_{cr}$",
    "f_amp":    r"$M_{2nd} = \frac{1}{1 - P/P_{cr}} \, M_{1st}$",

    # --- 2. 設計需求內力 ---
    "f_mu":     r"$M_u = B_1 M_{nt} + B_2 M_{lt}$",
    "f_pu":     r"$P_u = P_{nt} + B_2 P_{lt}$",

    # --- 3. B1 (P-delta) ---
    "f_b1":     r"$B_1 = \frac{C_m}{1 - P_u/P_{e1}} \geq 1.0$",
    "f_pe1":    r"$P_{e1} = \frac{\pi^2 E I}{(K_1 L)^2} \quad , \quad K_1 = 1.0$",
    "f_cm":     r"$C_m = 0.6 - 0.4 \left( \frac{M_1}{M_2} \right)$",
    "f_cm2":    r"$C_m = 0.85 \,\, \mathrm{(restrained)} \quad , \quad C_m = 1.0 \,\, \mathrm{(unrestrained)}$",

    # --- 4. B2 (P-Delta) ---
    "f_b2":     r"$B_2 = \frac{1}{1 - \frac{\sum P_u}{\sum P_{e2}}} \geq 1.0$",
    "f_pe2":    r"$P_{e2} = \frac{\pi^2 E I}{(K_2 L)^2} \quad , \quad K_2 > 1.0$",
    "f_b2alt":  r"$B_2 = \frac{1}{1 - \frac{\sum P_u \, \Delta_{oh}}{\sum H \cdot L}}$",

    # --- 5. 強度側：軸壓 ---
    "f_pn":     r"$\phi_c P_n = \phi_c F_{cr} A_g \quad , \quad \phi_c = 0.85$",
    "f_lamc":   r"$\lambda_c = \frac{K L}{r \pi} \sqrt{\frac{F_y}{E}}$",
    "f_fcr1":   r"$F_{cr} = \left( 0.658^{\lambda_c^2} \right) F_y \quad (\lambda_c \leq 1.5)$",
    "f_fcr2":   r"$F_{cr} = \left( \frac{0.877}{\lambda_c^2} \right) F_y \quad (\lambda_c > 1.5)$",

    # --- 6. 強度側：彎曲 ---
    "f_mp":     r"$\phi_b M_{nx} = \phi_b M_p = \phi_b Z_x F_y \quad (L_b \leq L_p)$",
    "f_mltb":   r"$M_n = C_b \left[ M_p - (M_p - M_r) \frac{L_b - L_p}{L_r - L_p} \right] \leq M_p$",
    "f_mny":    r"$\phi_b M_{ny} = \phi_b \, \mathrm{min} \left( F_y Z_y \, , \, 1.5 F_y S_y \right)$",

    # --- 7. P-M 互制 ---
    "f_h1a":    r"$\frac{P_u}{\phi_c P_n} + \frac{8}{9} \left( \frac{M_{ux}}{\phi_b M_{nx}} + \frac{M_{uy}}{\phi_b M_{ny}} \right) \leq 1.0$",
    "f_h1b":    r"$\frac{P_u}{2 \phi_c P_n} + \left( \frac{M_{ux}}{\phi_b M_{nx}} + \frac{M_{uy}}{\phi_b M_{ny}} \right) \leq 1.0$",
    "f_h1cond": r"$\frac{P_u}{\phi_c P_n} \geq 0.2 \, \rightarrow \, \mathrm{H1-1a} \quad ; \quad < 0.2 \, \rightarrow \, \mathrm{H1-1b}$",

    # --- 8. ASD ---
    "f_asd1":   r"$\frac{f_a}{F_a} + \frac{C_m f_b}{\left( 1 - \frac{f_a}{F'_e} \right) F_b} \leq 1.0$",
    "f_asd2":   r"$\frac{f_a}{0.6 F_y} + \frac{f_b}{F_b} \leq 1.0$",
    "f_fe":     r"$F'_e = \frac{12 \pi^2 E}{23 \left( K L / r_b \right)^2}$",
    "f_asd3":   r"$\frac{f_a}{F_a} + \frac{f_b}{F_b} \leq 1.0 \quad \left( \frac{f_a}{F_a} \leq 0.15 \right)$",

    # --- 9. 自我檢查 ---
    "f_check":  r"$\frac{P_{e1y}}{P_{e1x}} = \frac{I_y}{I_x}$",
}

manifest = {}
errors = []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
        # pad_inches gives a small safety margin — formulas with sqrt/fraction stacks can
        # clip at the top/bottom if this is too tight (0.08 has proven safe in practice).
        fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.08)
        plt.close(fig)
        from PIL import Image
        im = Image.open(path)
        w, h = im.size
        manifest[fid] = {"file": path, "ar": w / h}
    except Exception as e:
        errors.append((fid, str(e)))
        plt.close(fig)

with open("formula_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Rendered {len(manifest)} formulas, {len(errors)} errors")
for fid, err in errors:
    print("ERROR", fid, err)
