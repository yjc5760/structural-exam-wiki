#!/usr/bin/env python3
"""SD 組 U3-1-G2 階段 C 勘誤（2026-11-16）：SD-2022-2、SD-2022-4、SD-2025-4；SD-2019-4 只改標頭副分類（非勘誤）。
新內容放在同名資料夾 2026-11-16_errata_U3-1-G2/。可重複執行（已處理者略過）；保留原檔換行格式。
用法：在 SD/ 目錄執行  python scripts/fixes/2026-11-16_errata_U3-1-G2.py"""
import os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "2026-11-16_errata_U3-1-G2")
SOL = os.path.join(HERE, "..", "..", "raw", "solutions")
TAG = "2026-11-16（勘誤："

def load(qid):
    p = os.path.join(SOL, qid, f"{qid}.md")
    raw = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    return p, raw.replace("\r\n", "\n"), nl
def save(p, s, nl):
    open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))
def rep1(s, old, new, qid):
    assert s.count(old) == 1, f"{qid}: 找不到或不唯一：{old[:40]}"
    return s.replace(old, new)
def replace_sec2_to_footer(s, newbody, qid):
    a = s.index("\n## 2.")
    b = s.index("\n*修正日期：", a)
    return s[:a+1] + newbody.rstrip("\n") + "\n" + s[b:]

FOOT = {
"SD-2022-2": "*修正日期：2026-11-16（勘誤：改依現行台灣規範（建築物混凝土結構設計規範 112 年版第 18.3 節）——梁寬上限 b_c＋1.5h 改為 c2＋2min(c2, 0.75c1)；淨跨 4h 改為 4d；搭接禁區與閉合箍筋區 2d 改為 2h；閉合箍筋間距 min(d/4, 8db, 24dh, 300 mm) 改為 min(d/4, 6db, 15 cm)；補 1/4 彎矩強度規則、縱筋側向支撐間距 35 cm、搭接區箍筋間距 min(d/4, 10 cm)；改寫 §2–§5，舊答降為 §5.5 對照。錯誤類型：規範版本＋條文誤記（2d）。證據：2022 年考卷第 1 頁第二題（題目未指定規範）；條文依國土管理署公布之 112 年版規範 PDF 第 18.3.2–18.3.4 節。驗證：scripts/fixes/2026-11-16_verify_SD-2022-2.py MISMATCHES: 0）*",
"SD-2022-4": "*修正日期：2026-11-16（勘誤：依題目正本判讀 #1、#4 改寫——經驗分布由一階振態分布 90／210／300 kN 改為規範豎向分配式（Ft＝0.07TV＝105 kN）82.5／165.0／352.5 kN；振態組合法（SRSS）由多次側推組合需求量（無數值）改為振態層剪力 SRSS 後差分的單一分布 121.4／165.3／313.3 kN；粗估振態 {0.3, 0.7, 1.0}／{1.0, 0.3, −0.7}（不正交）改為精確振態；刪除自我更正亂句、修正 Σm·H 單位；改寫 §2–§5 與比較表，舊答降為 §5.7 對照。錯誤類型：L1 讀題（未依已確認題目正本）＋觀念模型（振態）。證據：2022 年考卷第 2 頁第四題；Ft 式依建築物耐震設計規範第 2.11 節。驗證：scripts/fixes/2026-11-16_verify_SD-2022-4.py（numpy 特徵值、兩路層剪力）MISMATCHES: 0）*",
"SD-2025-4": "*修正日期：2026-11-16（勘誤：改依現行建築物耐震設計規範及解說（111 年版）與建築物混凝土結構設計規範（112 年版）——三級地震由小震 50 年／設計地震 ×1/2.5、大震 2475 年／×1.5 改為中小度地震約 30 年（4.2αy 檢核）、設計地震 475 年、最大考量地震 2500 年（SaM、FuM）；「Fu（＝R）」改為 R → Ra＝1＋(R−1)/1.5 → 依週期得 Fu；刪除 Fu＝8／5／3 韌性等級表；梁箍筋間距 8db／24dh／300 mm 改為 d/4、6db、15 cm；柱軸力比上限 0.35 改為 0.3Ag·fc′ 加嚴圍束門檻；補正負彎矩強度比規定。錯誤類型：觀念模型＋規範版本。證據：2025 年考卷第 2 頁第四題；條文依國土管理署公布之耐震規範第 2 章、混凝土規範第 18.3–18.4 節。驗證：scripts/fixes/2026-11-16_verify_SD-2025-4.py 殘留與條文值檢查 MISMATCHES: 0）*",
}

def do_2022_2():
    q = "SD-2022-2"; p, s, nl = load(q)
    if TAG in s: print(q, "已處理，略過"); return
    s = rep1(s, "| 規範與構架類別 | 依現行建築物混凝土結構設計規範（2023 年版）耐震特別規定的**特殊抗彎矩構架梁**作答（判讀 #1） | 引用 ACI 318-99 或舊版規範數值 |",
               "| 規範與構架類別 | 依現行建築物混凝土結構設計規範（2023 年版）耐震特別規定的**特殊抗彎矩構架梁**作答（判讀 #1） | 引用舊版數值：梁寬「柱寬＋1.5 倍梁深」、箍筋間距 8 倍主筋徑／24 倍箍筋徑／30 cm（本庫舊解） |\n| 閉合箍筋區、搭接禁區 | 量 **2 倍梁深 $2h$**（18.3.3.3、18.3.4.1） | 寫成 $2d$（本庫舊解） |", q)
    s = rep1(s, "**本解記號：** $b_w$ 梁寬、$h$ 梁深、$d$ 有效深度、$b_c$ 支承柱寬、$\\rho$ 縱向拉力鋼筋比、$d_{bl}$ 縱筋直徑、$d_{bh}$ 箍筋直徑、$s$ 箍筋間距。",
               "**本解記號：** $b_w$ 梁寬、$h$ 梁深、$d$ 有效深度、$c_1$／$c_2$ 支承柱沿梁跨／垂直梁跨方向尺寸、$\\rho$ 縱向拉力鋼筋比、$d_b$ 最小主要撓曲鋼筋直徑、$s$ 箍筋間距。", q)
    s = replace_sec2_to_footer(s, open(os.path.join(DATA, f"{q}_sec2-5.md"), encoding="utf-8").read(), q)
    s = s.rstrip("\n") + "\n" + FOOT[q] + "\n"
    save(p, s, nl); print(q, "已勘誤")

def do_2022_4():
    q = "SD-2022-4"; p, s, nl = load(q)
    if TAG in s: print(q, "已處理，略過"); return
    s = rep1(s, "| 「經驗分布」 | 考卷未定義；題目正本定案解讀為規範等值靜力法豎向分配式（含頂層集中力 $F_t$）；作答須先寫明所採定義（判讀 #1） | 不寫定義直接套用某一式 |",
               "| 「經驗分布」 | 考卷未定義；題目正本定案解讀為規範等值靜力法豎向分配式（含頂層集中力 $F_t$）；作答須先寫明所採定義（判讀 #1） | 不寫定義直接套用一階振態分布（本庫舊解） |", q)
    s = rep1(s, "| 振態組合法（SRSS） | 是**一種側力豎向分布**：各振態側力（或層剪力）以 SRSS 組合成單一分布再側推（判讀 #4） | 與其他方法結果再做 SRSS 組合 |",
               "| 振態組合法（SRSS） | 是**一種側力豎向分布**：各振態層剪力以 SRSS 組合後差分成單一分布再側推（判讀 #4） | 每個振態各做一次 Pushover 再組合需求量（MPA，本庫舊解）；或與其他方法結果再做 SRSS 組合 |\n| 振態形狀 | 等質量等勁度 3 層：$\\phi_1=\\{0.445,\\ 0.802,\\ 1\\}$ | 粗估 $\\{0.3,\\ 0.7,\\ 1\\}$（與第二振態不正交，本庫舊解） |", q)
    s = replace_sec2_to_footer(s, open(os.path.join(DATA, f"{q}_sec2-5.md"), encoding="utf-8").read(), q)
    s = s.rstrip("\n") + "\n" + FOOT[q] + "\n"
    save(p, s, nl); print(q, "已勘誤")

def do_2025_4():
    q = "SD-2025-4"; p, s, nl = load(q)
    if TAG in s: print(q, "已處理，略過"); return
    spec = importlib.util.spec_from_file_location("reps", os.path.join(DATA, f"{q}_reps.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for old, new in m.REPS: s = rep1(s, old, new, q)
    s = rep1(s, "| 三級地震 | 小震、中震、大震宜對應規範的中小度地震、設計地震（回歸期 475 年）、最大考量地震（回歸期 2500 年）（判讀 #1） | 自創回歸期或地震倍數 |",
               "| 三級地震 | 小震、中震、大震宜對應規範的中小度地震（約 30 年）、設計地震（回歸期 475 年）、最大考量地震（回歸期 2500 年）（判讀 #1） | 套用美國分級：小震 50 年、設計地震 ×1/2.5，大震 2475 年、×1.5（本庫舊解） |\n| $F_u$ 與 $R$ | $R\\to R_a=1+(R-1)/1.5\\to$ 依週期得 $F_u$ | 「$F_u=R$」並列 8／5／3（本庫舊解，實為 ASCE 7 的 R 值） |", q)
    a = s.index("\n*修正日期：")
    s = s[:a].rstrip("\n") + "\n" + m.APPEND5 + s[a:]
    s = s.rstrip("\n") + "\n" + FOOT[q] + "\n"
    save(p, s, nl); print(q, "已勘誤")

def do_2019_4():
    q = "SD-2019-4"; p, s, nl = load(q)
    mark = "標頭副分類改為與 question_index 一致"
    if mark in s: print(q, "已處理，略過"); return
    s = rep1(s, "**副分類：** `SD-U2-1` 地震力之設計規範", "**副分類：** 無", q)
    s = s.rstrip("\n") + "\n" + f"*修正日期：2026-11-16（非勘誤）{mark}（索引 secondaryTopicIds 為空；舊標頭 SD-U2-1）*" + "\n"
    save(p, s, nl); print(q, "標頭已改")

if __name__ == "__main__":
    do_2022_2(); do_2022_4(); do_2025_4(); do_2019_4()
