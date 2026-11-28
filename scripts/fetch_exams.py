#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從考選部「考畢試題查詢平臺」下載結構工程技師考卷到各科 raw/exams/

用法（在知識庫根目錄、用你自己電腦的終端機執行；Cowork／Claude 的沙盒連不到 moex.gov.tw）：
  python scripts/fetch_exams.py                  檢查「現有最新年度＋1」到今年，有新考卷就下載
  python scripts/fetch_exams.py --year 2026      只處理 2026（民國 115）年
  python scripts/fetch_exams.py --years 2002-2026 --subject SS,RC
  python scripts/fetch_exams.py --dry-run        只列出會下載什麼，不寫檔
  python scripts/fetch_exams.py --check          只檢查有沒有新考卷（有：結束碼 1，可給排程用）
  python scripts/fetch_exams.py --verify --years 2002-2025
                                                 比對既有考卷與官網檔案是否一致（不覆蓋）

規則：
  - raw/exams/ 是證據：既有檔一律不覆蓋；官網檔與既有檔不同時只回報，另存 *.moex-YYYYMMDD.pdf 供人工比對
  - 檔名照 scripts/subject_profiles.json 的 examFile：XX-YYYY_<examFile>.pdf（YYYY 為西元）
  - 每下載一份，在該科 wiki/queries/log.md append 一筆來源紀錄（考試代碼、類科、科目代碼、位元組數、MD5）
  - 材料力學（MM）目前沒有科目資料夾，預設略過；建好 MM/ 後加 --subject MM 即可

怎麼找到考卷（官網每年的考試代碼、類科代碼、科目代碼都不同，不能寫死）：
  1. GET wFrmExamQandASearch.aspx?y=<西元年>：該年所有考試的試題清單
  2. 找標籤含「結構工程技師」的類科（勾選框 id：chk_<考試代碼>_<類科>）；
     早年同一年還有檢覈考試（科目叫「結構分析」「基礎設計」…），以「科目名稱對得上幾科」挑出高考那一場
  3. 類科底下各科目（chk_<考試>_<類科>_<科目>）的試題連結 wHandExamQandA_File.ashx?t=Q&code=…&c=…&s=…&q=1
  2026-11-28 建立；HTML 結構以 2002、2010、2019、2024–2026 實頁驗證。
"""
import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "https://wwwq.moex.gov.tw/exam/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) structural-exam-wiki/fetch_exams.py"
PAUSE = 1.0  # 每個請求間隔秒數，避免對官網造成負擔

# 現行科目名稱（官網類科底下的科目標籤）→ 本庫科目代碼
SUBJECT_NAMES = {
    "SS": ["鋼結構設計"],
    "RC": ["鋼筋混凝土設計與預力混凝土設計"],
    "SA": ["結構學"],
    "SD": ["結構動力分析與耐震設計"],
    "SM": ["土壤力學與基礎設計"],
    "MM": ["材料力學"],
}


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"[\s（）()〔〕【】、，,]", "", s)


# ───────────────────────── HTTP ─────────────────────────
def get(url, binary=False, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            time.sleep(PAUSE)
            return data if binary else data.decode("utf-8", errors="replace")
        except urllib.error.URLError as e:  # 含 SSL 錯誤
            last = e
            time.sleep(2 * (i + 1))
    msg = f"連線失敗：{url}\n  {last}"
    if "CERTIFICATE" in str(last).upper():
        msg += "\n  （SSL 憑證驗證失敗：請更新 Python 或執行 pip install --upgrade certifi 後再試）"
    raise SystemExit(msg)


# ───────────────────────── 解析 ─────────────────────────
OPT = re.compile(r'<option[^>]*value="(\d+)"[^>]*>(.*?)</option>', re.S)
CAT = re.compile(r'<label for="ctl00_holderContent_chk_(\d+)_([A-Za-z0-9]+)"\s*>(.*?)</label>', re.S)
SUB = re.compile(r'<label for="ctl00_holderContent_chk_(\d+)_([A-Za-z0-9]+)_([A-Za-z0-9]+)"[^>]*>(.*?)</label>', re.S)
LINK = re.compile(r'href="wHandExamQandA_File\.ashx\?t=Q&(?:amp;)?code=(\d+)&(?:amp;)?c=([A-Za-z0-9]+)&(?:amp;)?s=([A-Za-z0-9]+)&(?:amp;)?q=(\d+)"')


def parse_year_page(text):
    """回傳 [{code, exam, c, cat, subjects: {name: [(s, q), ...]}}]，只含類科名稱有「結構工程技師」者"""
    sel = re.search(r'<select[^>]*id="ctl00_holderContent_ddlExamCode".*?</select>', text, re.S)
    exams = {v: html.unescape(re.sub(r"<[^>]+>", "", n)).strip() for v, n in OPT.findall(sel.group(0))} if sel else {}
    cats = {}
    for code, c, name in CAT.findall(text):
        if "結構工程技師" in norm(name):
            cats[(code, c)] = {"code": code, "exam": exams.get(code, ""), "c": c, "cat": norm(name), "subjects": {}}
    subname = {}
    for code, c, s, name in SUB.findall(text):
        if (code, c) in cats:
            subname[(code, c, s)] = norm(name)
    for code, c, s, q in LINK.findall(text):
        key = (code, c, s)
        if key in subname:
            lst = cats[(code, c)]["subjects"].setdefault(subname[key], [])
            if (s, q) not in lst:
                lst.append((s, q))
    return list(cats.values())


def pick_exam(cands):
    """同一年有多場含結構工程技師的考試（早年有檢覈）時，挑現行六科名稱對得最多的那場"""
    targets = {norm(n) for ns in SUBJECT_NAMES.values() for n in ns}

    def score(x):
        hit = sum(1 for n in x["subjects"] if n in targets)
        return (hit, "檢覈" not in x["exam"], "高等考試" in x["exam"] or "高考" in x["cat"])
    ranked = sorted(cands, key=score, reverse=True)
    if not ranked or score(ranked[0])[0] == 0:
        return None, ranked
    return ranked[0], ranked


def match_subject(subjects, code):
    want = {norm(n) for n in SUBJECT_NAMES[code]}
    for name, links in subjects.items():
        if name in want:
            return name, links
    return None, []


# ───────────────────────── 本庫狀態 ─────────────────────────
def profiles():
    d = json.loads((REPO / "scripts/subject_profiles.json").read_text(encoding="utf-8"))
    return d.get("subjects", d)


def exam_path(code, year, prof):
    stem = prof.get(code, {}).get("examFile") or SUBJECT_NAMES[code][0]
    return REPO / code / "raw/exams" / f"{code}-{year}_{stem}.pdf"


def latest_year(codes):
    ys = []
    for c in codes:
        for p in (REPO / c / "raw/exams").glob(f"{c}-*_*.pdf"):
            m = re.match(rf"{c}-(\d{{4}})_", p.name)
            if m:
                ys.append(int(m.group(1)))
    return max(ys) if ys else 2002


def append_log(code, line):
    p = REPO / code / "wiki/queries/log.md"
    if not p.exists():
        return
    with p.open("a", encoding="utf-8") as f:
        f.write("\n" + line + "\n")


# ───────────────────────── 主流程 ─────────────────────────
def parse_years(a):
    if a.year:
        return [a.year]
    if a.years:
        lo, _, hi = a.years.partition("-")
        return list(range(int(lo), int(hi or lo) + 1))
    this = dt.date.today().year
    return list(range(latest_year(a.subjects) + 1, this + 1)) or [this]


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):  # Windows 主控台或導向檔案時是 cp950，✔ ⚠ 之類符號改以 ? 顯示，不讓程式中斷
        try:
            stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description="下載結構工程技師考卷（考選部考畢試題查詢平臺）")
    ap.add_argument("--year", type=int, help="單一西元年，如 2026")
    ap.add_argument("--years", help="西元年範圍，如 2002-2026")
    ap.add_argument("--subject", default="SS,RC,SA,SD,SM", help="科目代碼，逗號分隔（預設五科；MM 需先建資料夾）")
    ap.add_argument("--dry-run", action="store_true", help="只列出，不下載")
    ap.add_argument("--check", action="store_true", help="只檢查是否有新考卷；有則結束碼 1")
    ap.add_argument("--verify", action="store_true", help="比對既有考卷與官網檔案是否一致")
    a = ap.parse_args(argv)
    a.subjects = [s.strip().upper() for s in a.subject.split(",") if s.strip()]
    for s in a.subjects:
        if s not in SUBJECT_NAMES:
            raise SystemExit(f"未知科目代碼：{s}")
    prof = profiles()
    years = parse_years(a)
    today = dt.date.today().isoformat()
    print(f"檢查 {years[0]}–{years[-1]} 年，科目 {','.join(a.subjects)}")
    new, done, missing, differ = [], [], [], []

    for y in years:
        page = get(f"{BASE}wFrmExamQandASearch.aspx?y={y}")
        exam, ranked = pick_exam(parse_year_page(page))
        if not exam:
            print(f"  {y}（民國 {y - 1911}）：官網尚無結構工程技師試題")
            missing.extend((s, y, "官網尚未公布") for s in a.subjects)
            continue
        others = [r["code"] for r in ranked if r is not exam]
        print(f"  {y}（民國 {y - 1911}）：{exam['code']} {exam['exam'][:40]}…（類科 {exam['c']}）"
              + (f"；略過同年 {', '.join(others)}" if others else ""))
        for s in a.subjects:
            dest = exam_path(s, y, prof)
            if not (REPO / s).is_dir():
                print(f"    {s}：本庫沒有 {s}/ 資料夾，略過")
                continue
            name, links = match_subject(exam["subjects"], s)
            if not links:
                print(f"    {s}：該場考試找不到科目「{SUBJECT_NAMES[s][0]}」")
                missing.append((s, y, "找不到科目"))
                continue
            sid, q = links[0]
            if len(links) > 1:
                print(f"    {s}：⚠ 官網有 {len(links)} 份試題檔（{links}），只取第一份，其餘請人工確認")
            url = f"{BASE}wHandExamQandA_File.ashx?t=Q&code={exam['code']}&c={exam['c']}&s={sid}&q={q}"
            src = f"moex code={exam['code']} c={exam['c']} s={sid} q={q}"
            if dest.exists() and not a.verify:
                done.append((s, y))
                continue
            if a.check or (a.dry_run and not dest.exists()):
                print(f"    {s}：可下載 → {dest.relative_to(REPO)}（{src}）")
                new.append((s, y))
                continue
            if a.dry_run:
                continue
            data = get(url, binary=True)
            if not data.startswith(b"%PDF"):
                print(f"    {s}：⚠ 下載內容不是 PDF（{len(data)} bytes），略過：{url}")
                missing.append((s, y, "下載內容不是 PDF"))
                continue
            md5 = hashlib.md5(data).hexdigest()
            if dest.exists():  # --verify
                old = dest.read_bytes()
                if old == data:
                    print(f"    {s}：與官網一致（{len(data):,} bytes）")
                else:
                    alt = dest.with_name(dest.stem + f".moex-{today.replace('-', '')}.pdf")
                    alt.write_bytes(data)
                    print(f"    {s}：⚠ 與官網不同（本庫 {len(old):,}／官網 {len(data):,} bytes），官網版另存 {alt.name}，原檔不動")
                    differ.append((s, y))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(".part")
            tmp.write_bytes(data)
            tmp.replace(dest)
            print(f"    {s}：✔ 下載 {dest.relative_to(REPO)}（{len(data):,} bytes）")
            append_log(s, f"- {today}｜FETCH-EXAM｜{s}-{y}：考卷原件由 `scripts/fetch_exams.py` 下載至 "
                          f"`raw/exams/{dest.name}`；來源考選部考畢試題查詢平臺（{src}；{exam['exam']}），"
                          f"{len(data):,} bytes，MD5 {md5}")
            new.append((s, y))

    print()
    if a.check:
        print(f"可下載的新考卷：{len(new)} 份" + ("" if new else "（沒有新考卷）"))
        return 1 if new else 0
    if new and not a.dry_run:
        print(f"已下載 {len(new)} 份：" + "、".join(f"{s}-{y}" for s, y in new))
        print("下一步（在 Cowork）：對每科說「解析 YYYY 年 XX 考卷」（exam-solve：擷取附圖 → 題目正本 → 判讀確認 → 解題）。")
        print("考卷檔寫入 raw/exams/、來源記在各科 wiki/queries/log.md；git commit 由你自己做。")
    elif not a.dry_run and not a.verify:
        print("沒有新考卷。" + (f"（{len(done)} 份已在本庫）" if done else ""))
    if differ:
        print(f"⚠ {len(differ)} 份既有考卷與官網不同，請人工比對：" + "、".join(f"{s}-{y}" for s, y in differ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
