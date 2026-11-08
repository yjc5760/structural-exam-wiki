#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2003-1/2/3 勘誤（2026-11-01）下游同步：索引標籤、儀表板、單元總覽資料檔、概念／方法／索引頁、講義、教科書。
在 repo 根目錄執行：python3 sync_2003.py   （每處替換都 assert 命中一次，未命中即中止）"""
import json, re
from pathlib import Path

R = Path(".")
TAGS = {
    "SS-2003-1": ["塊狀剪力", "block shear", "腹板承壓降伏", "web yielding", "Cc臨界細長比", "ASD",
                  "受拉構材安全係數", "局部挫屈", "斷面分類", "結實斷面", "承壓加勁板"],
    "SS-2003-2": ["SRC複合柱", "包覆型複合柱", "有效降伏強度Fmy", "修正彈性模數Em", "整體挫屈", "非彈性挫屈",
                  "λc", "Fcr", "φcPn", "H型鋼", "A572", "SD420", "rm下限", "0.3倍全厚"],
    "SS-2003-3": ["接合設計", "剪力遲滯", "U值", "螺栓接合", "A325X", "淨斷面斷裂", "WT斷面", "承壓型螺栓",
                  "有效淨面積", "雙角鋼", "雙剪", "拉剪互制", "螺栓數量設計"],
}


def sub1(path, old, new):
    p = R / path
    t = p.read_text(encoding="utf-8")
    n = t.count(old)
    assert n == 1, f"{path}: 預期命中 1 次，實際 {n} 次：{old[:60]}"
    p.write_text(t.replace(old, new), encoding="utf-8")


# 1) question_index.json（indent=2、保留結尾換行）
p = R / "raw/json/question_index.json"
raw = p.read_text(encoding="utf-8")
d = json.loads(raw)
for x in d["questions"]:
    if x["moduleId"] in TAGS:
        x["tags"] = TAGS[x["moduleId"]]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + raw[len(raw.rstrip()):], encoding="utf-8")

# 2) dashboard-data.js
p = R / "dashboard-data.js"
t = p.read_text(encoding="utf-8")
for q, tags in TAGS.items():
    rx = re.compile(r'(\["' + q + r'",[^\[\]]*\[[^\]]*\],[^\[\]]*\[[^\]]*\],)\[[^\]]*\]')
    assert len(rx.findall(t)) == 1, q
    t = rx.sub(lambda m: m.group(1) + json.dumps(tags, ensure_ascii=False, separators=(",", ":")), t)
p.write_text(t, encoding="utf-8")

# 3) 單元總覽資料檔（indent=1）
def edit_unit(u, fn):
    p = R / f"study/data/unit-{u}.json"
    raw = p.read_text(encoding="utf-8")
    d = json.loads(raw)
    fn(d)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + raw[len(raw.rstrip()):], encoding="utf-8")

def q_of(d, qid):
    return next(x for x in d["Q"] if x["id"] == qid)

def rep(s, old, new):
    assert s.count(old) == 1, old[:50]
    return s.replace(old, new)

def u11(d):
    q = q_of(d, "SS-2003-1"); q["sum"] = "塊狀剪力、腹板局部降伏改善、受拉安全係數、局部挫屈斷面分類、Cc（概念五小題）"; q["f"] = [7, 10, 22, 27, 29]
    q = q_of(d, "SS-2003-2"); q["sum"] = "SRC 包覆型合成柱：Fmy／Em 與 r_m ≥ 0.3 全厚的整體挫屈強度"; q["f"] = [0, 1, 5, 16, 30]
    q = q_of(d, "SS-2003-3"); q["sum"] = "雙角鋼夾 WT 腹板（雙剪）的螺栓數量設計與柱面拉剪互制"; q["f"] = [18, 20, 21, 24]
    F = d["F"]
    F[3]["meta"] = rep(F[3]["meta"], "用到它的 <code>SS-2003-2</code>（SRC 柱 \\(\\lambda_c=2.405\\)）、<code>SS-2010-3</code>", "用到它的 <code>SS-2010-3</code>")
    F[16]["meta"] = ("92 年 <code>SS-2003-2</code> 把「\\(A_s\\) 代替 \\(A_g\\)、\\(r_m\\) 代替 \\(r\\)、\\(F_{my},E_m\\) 代替 \\(F_y,E\\)」連同"
                     "「\\(r_m\\) 不應小於挫屈平面全厚度之 30%」全部印出——<b>給了也要讀到</b>，漏掉這條會把弱軸 \\(KL/r\\) 由 80 算成 156、誤判彈性挫屈。"
                     "100 年 <code>SS-2011-4</code> 要做非彈性 \\(G\\) 值折減，沒給 \\(\\tau_a\\) 的定義也沒給修正式。")
    if 2003 not in F[16]["ok"]:
        F[16]["ok"] = sorted(F[16]["ok"] + [2003])
    F[22]["meta"] = rep(F[22]["meta"], "<code>SS-2003-1</code>①、<code>SS-2003-3</code> 與 94 年", "<code>SS-2003-1</code>① 與 94 年")
    F[24]["meta"] = rep(F[24]["meta"], "本單元用到它的 <code>SS-2003-3</code>、<code>SS-2005-1</code> 當年都有印",
                        "本單元用到它的 <code>SS-2003-3</code>（92 年表列「變形非考量」對應 \\(2.4dtF_u\\)，與 AISC 條件相反）、<code>SS-2005-1</code> 當年都有印")

def u12(d):
    q = q_of(d, "SS-2003-1"); q["sum"] = "梁支承處腹板局部降伏的改善措施＋局部挫屈四種斷面分類（五小題之二）"; q["f"] = [5, 6]

def u14(d):
    q = q_of(d, "SS-2003-3"); q["sum"] = "雙角鋼—WT 雙剪螺栓數量；WT—柱 8 栓拉剪互制"; q["f"] = [0, 2, 6, 7, 8, 12]
    q = q_of(d, "SS-2003-1"); q["sum"] = "塊狀剪力撕裂說明（五小題之一）"
    F = d["F"]
    F[5]["meta"] = rep(F[5]["meta"], "<code>SS-2003-1</code>①／<code>SS-2003-3</code>、94 年", "<code>SS-2003-1</code>①、94 年")

edit_unit("SS-U1-1", u11); edit_unit("SS-U1-2", u12); edit_unit("SS-U1-4", u14)

# 4) 概念頁、方法頁（raw 來源與 wiki 同步）、索引頁
sub1("wiki/concepts/BLOCK-SHEAR-RUPTURE.md", "| [[SS-2003-3]] | 92 | 拉力及壓力桿件 | 接合設計, 剪力遲滯, U值 |\n", "")
sub1("wiki/concepts/COMPACT-SECTION.md", "|------|------|--------|----------|\n| [[SS-2002-2]]",
     "|------|------|--------|----------|\n| [[SS-2003-1]] | 92 | 拉力及壓力桿件 | 局部挫屈, 斷面分類, 結實斷面 |\n| [[SS-2002-2]]")
sub1("wiki/concepts/TENSION-MEMBER-DESIGN.md", "|------|------|--------|----------|\n| [[SS-2005-1]]",
     "|------|------|--------|----------|\n| [[SS-2003-1]] | 92 | 拉力及壓力桿件 | 受拉構材安全係數, 塊狀剪力 |\n| [[SS-2003-3]] | 92 | 拉力及壓力桿件 | 雙角鋼, 剪力遲滯, U值 |\n| [[SS-2005-1]]")
sub1("wiki/concepts/BOLTED-CONNECTION-DESIGN.md", "| [[SS-2002-4]] | 91 | 接合之分析與設計 | 接合設計, 偏心螺栓群, 彈性分析法 |\n",
     "| [[SS-2002-4]] | 91 | 接合之分析與設計 | 接合設計, 偏心螺栓群, 彈性分析法 |\n| [[SS-2003-3]] | 92 | 拉力及壓力桿件 | 雙剪, 螺栓數量設計, 拉剪互制 |\n")
for f in ("wiki/methods/block-shear.md", "raw/solutions/methods/block-shear/block-shear.md"):
    sub1(f, "| [[SS-2003-1]] | 92年 | 腹板加勁板，Block Shear |\n| [[SS-2003-3]] | 92年 | WT 斷面，Block Shear + NSF |\n",
         "| [[SS-2003-1]] | 92年 | 簡答（一）：塊狀剪力撕裂的定義與擇式原則 |\n")
for f in ("wiki/methods/shear-lag-u.md", "raw/solutions/methods/shear-lag-u/shear-lag-u.md"):
    sub1(f, "| [[SS-2003-3]] | 92年 | WT 斷面，x̄ 計算 + U + Block Shear |",
         "| [[SS-2003-3]] | 92年 | 長肢背對背雙角鋼，角鋼尺寸未給 → 表列 U = 0.85（每列 ≥ 3 栓） |")
sub1("wiki/index.md", "| 92年 | 概念題 | 塊狀剪力、block shear、腹板承壓降伏、web yielding |",
     "| 92年 | 概念題 | 塊狀剪力、腹板局部降伏改善、受拉安全係數、局部挫屈斷面分類、Cc |")
sub1("wiki/index.md", "| 92年 | LRFD | SRC複合柱、包覆型複合柱、有效降伏強度Fmy、修正彈性模數Em |",
     "| 92年 | LRFD | SRC複合柱、包覆型複合柱、有效降伏強度Fmy、修正彈性模數Em、rm下限 |")
sub1("wiki/index.md", "| 92年 | LRFD | 剪力遲滯、螺栓接合、塊狀剪力、WT斷面 |", "| 92年 | LRFD | 雙角鋼、雙剪、剪力遲滯、拉剪互制 |")
sub1("wiki/by-year.md", "| 拉力及壓力桿件 | LRFD | 接合設計、剪力遲滯、U值 |", "| 拉力及壓力桿件 | LRFD | 雙角鋼、雙剪、拉剪互制 |")

# 5) 講義與教科書
sub1("study/lecture-SS-U1-1.html", "<li>迴轉半徑 \\(r_m\\) 規範規定不得小於 \\(0.3\\times\\) 混凝土斷面在挫屈方向的全深。</li>",
     "<li>迴轉半徑 \\(r_m\\) 規範規定不得小於 \\(0.3\\times\\) 混凝土斷面在挫屈方向的全深。"
     "<b>SS-2003-2 的分水嶺就在這裡</b>：弱軸 \\(r_m=\\max(7.7,\\,0.3\\times50)=15\\) cm，\\(\\lambda_c=1.235\\)（非彈性），\\(\\phi_cP_n\\approx513\\) t；"
     "漏用而直接取 \\(r_y=7.7\\) 會變成 \\(\\lambda_c=2.405\\)、147 t，低估約 3.5 倍。</li>")
sub1("study/lecture-SS-U1-1.html", "<td>塊狀剪力機制 / 腹板承壓降伏 / 複合柱 \\(F_{my},E_m\\) / \\(C_c\\) 意義</td><td>§3, §7.3, §8.2</td>",
     "<td>塊狀剪力機制 / 腹板局部降伏改善 / 受拉構材兩種安全係數 / 局部挫屈斷面分類 / \\(C_c\\) 意義</td><td>§3, §7.3</td>")
sub1("study/lecture-SS-U1-1.html", "<td>\\(\\lambda_c\\) 用 \\(F_{my}/E_m\\)；最後乘 \\(A_s\\)</td>",
     "<td>\\(r_m\\ge0.3\\times\\)挫屈平面全厚；\\(\\lambda_c\\) 用 \\(F_{my}/E_m\\)；最後乘 \\(A_s\\)</td>")
sub1("study/lecture-SS-U1-1.html", "<td>WT 斷面以莖部螺栓接合：剪力遲滯 \\(U\\)、淨斷面斷裂、塊狀剪力</td><td>§1, §2, §3</td><td>翼板未直接傳力 → \\(U\\) 折減；塊狀剪力要畫出剪力面與拉力面</td>",
     "<td>雙角鋼夾 WT 腹板：雙剪螺栓數量設計；WT 與柱 8 栓拉剪互制</td><td>§1, §2</td><td>沒給外力 → 以構材 \\(\\phi_tP_n\\) 為設計力；雙角鋼夾板是雙剪；題目明示不必考慮塊狀剪力</td>")
sub1("study/lecture-SS-U1-2.html", "<td>子題(二)：梁無承壓加勁板時的<b>腹板承壓降伏</b>發生條件與檢核</td>",
     "<td>子題(二)：梁支承處<b>腹板局部降伏</b>的改善措施；子題(四)：依局部挫屈特性的四種斷面</td>")
sub1("study/lecture-SS-U1-4.html", "<td>WT 斷面螺栓接合：剪力遲滯 U、淨斷面斷裂、塊狀剪力、承壓型螺栓</td><td>§3、§4.3</td>",
     "<td>雙角鋼夾 WT 腹板的雙剪螺栓數量；WT 與柱 8 栓的承壓型螺栓拉剪互制</td><td>§3、§4.3</td>")
sub1("study/lecture-SS-U1-4.html", "<td>SS-2021-2、SS-2003-3</td>", "<td>SS-2021-2</td>")
sub1("study/textbook-SS-U1-1-tension.html",
     "（各題慣例略不同，例如 <a href=\"problems-view/SS-2003-3.html\">SS-2003-3</a> 用「孔徑 + 2 mm」）。",
     "（各題慣例略不同）。若題目已寫明「計算時必須扣除之螺栓孔徑」，就直接用，例如 <a href=\"problems-view/SS-2003-3.html\">SS-2003-3</a> 指定扣 22 mm，不要再加。")
print("sync ok")
