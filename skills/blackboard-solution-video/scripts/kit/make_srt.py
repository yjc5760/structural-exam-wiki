"""字幕：segments.py ＋ timeline.json（渲染產生）＋ audio/*.wav → <PROBLEM_ID>.srt（YouTube 另傳用）
- 國字數字轉阿拉伯數字、口語符號轉回符號（V s → Vs、伽瑪 d → γd …）
- 每段依標點切成子句，以 TTS 實際念的字數估長度（數字念成國字，比阿拉伯數字長），
  再用 DP 把子句邊界對到實際語音停頓（silencedetect）：字幕從停頓結束（開口）才出現
用法：python make_srt.py            產生字幕
      python make_srt.py --preview  只預覽字幕切句與數字轉換（不需音檔），檢查有沒有誤轉
"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import segments
from segments import SEGMENTS
PID = getattr(segments, "PROBLEM_ID", "video")

# ---------- 國字數字 → 阿拉伯 ----------
D = {"零": 0, "一": 1, "二": 2, "兩": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
U = {"十": 10, "百": 100, "千": 1000}
# 含數字但不是數值的常用詞（不轉阿拉伯數字）；題目專屬的放 segments.SUB_KEEP
KEEP = ["一大堆", "一堆", "一端", "一個", "一件", "一樣", "一約", "一看", "一次", "一半", "一致", "一下",
        "一條", "一點都", "一定", "一起", "一般", "一直", "一邊", "一種", "一項", "一步", "一律", "同一",
        "方法一", "方法二", "方法三", "第一", "第二", "第三", "第四", "第五",
        "三根", "三種", "三個", "三相", "兩種", "兩支", "一支", "兩個", "兩邊", "兩端", "四個", "千牛頓", "千牛",
        "十分", "萬一", "唯一", "統一", "一百對齊"] + list(getattr(segments, "SUB_KEEP", []))
SYMBOLS = sorted(getattr(segments, "SUB_SYMBOLS", []), key=lambda x: -len(x[0]))
UNITS = list(getattr(segments, "SUB_UNITS", [("毫升", "ml"), ("克", "g")]))


def cn_int(s):
    if not s:
        return 0
    if all(c in D for c in s) and len(s) > 1:          # 逐位念法：三一四 → 314
        return int("".join(str(D[c]) for c in s))
    total, num = 0, 0
    for c in s:
        if c in D:
            num = D[c]
        elif c in U:
            total += (num or 1) * U[c]
            num = 0
    return total + num


def cn_num(s):
    if "點" in s:
        a, b = s.split("點", 1)
        return f"{cn_int(a)}." + "".join(str(D[c]) for c in b)
    return str(cn_int(s))


NUM_RE = re.compile(r"(百分之)?([零一二兩三四五六七八九十百千]+(?:點[零一二三四五六七八九]+)?)")


def to_display(t):
    t = re.sub(r"\s*<[^>]+>\s*", "", t)
    for a, b in SYMBOLS:
        t = t.replace(a, b)
    guard = {}
    for i, k in enumerate(sorted(KEEP, key=len, reverse=True)):
        tok = f"{i}"
        if k in t:
            guard[tok] = k
            t = t.replace(k, tok)

    def rep(m):
        pct, body = m.group(1), m.group(2)
        if body in ("千",) or (len(body) == 1 and body in "十百"):
            return m.group(0)
        n = cn_num(body)
        return f"{n}%" if pct else n
    t = NUM_RE.sub(rep, t)
    for a, b in UNITS:                       # 只換「數字後面」的單位
        t = re.sub(rf"(\d)\s*{re.escape(a)}", rf"\1 {b}", t)
    for tok, k in guard.items():
        t = t.replace(tok, k)
    return t


# ---------- 停頓偵測 ----------
def silences(wav, db=-38, dur=0.18):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=n={db}dB:d={dur}",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return list(zip(st, en))


def wav_len(wav):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                 "csv=p=0", wav], capture_output=True, text=True).stdout)


def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


SPLIT = re.compile(r"(?<=[。：，；？！、])")


def clauses(t):
    return [p for p in SPLIT.split(t) if p.strip()]


def spoken_weight(c):
    """以 TTS 實際念的字估長度：國字 1、英文字母 0.6（V s、e max）、標點 0"""
    c = re.sub(r"<[^>]+>", "", c)
    return sum(1 if "\u4e00" <= ch <= "\u9fff" else 0.6 if ch.isalnum() else 0 for ch in c) or 0.5


def group(parts, lo=8, hi=24):
    """把子句併成字幕條，回傳每條包含的子句索引"""
    out, buf, idx = [], "", []
    for i, p in enumerate(parts):
        if buf and len(buf) + len(p) > hi:
            out.append(idx); buf, idx = "", []
        buf += p; idx.append(i)
        if len(buf) >= lo or (len(buf) >= 5 and buf[-1] in "。？！"):
            out.append(idx); buf, idx = "", []
    if idx:
        if out and len("".join(parts[j] for j in out[-1])) + len(buf) <= hi + 6:
            out[-1] += idx
        else:
            out.append(idx)
    return out


def align(fr, pauses, speech):
    """子句邊界（預期語音時間比例 fr）對到實際停頓（DP，單調）。
    pauses: [(start, end, 語音時間比例)]；回傳每個邊界對到的停頓索引或 None"""
    n, m = len(fr), len(pauses)
    INF = float("inf")
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    bk = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            c = dp[i][j]
            if c == INF:
                continue
            if j < m:                                   # 略過停頓 j（長停頓略過要付代價）
                d = pauses[j][1] - pauses[j][0]
                v = c + 1.5 * min(d, 0.8)
                if v < dp[i][j + 1]:
                    dp[i][j + 1], bk[i][j + 1] = v, (i, j, None)
            if i < n and j < m:                         # 邊界 i 對到停頓 j
                err = abs(fr[i] - pauses[j][2]) * speech  # 秒
                v = c + (err / 1.2) ** 2
                if v < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1], bk[i + 1][j + 1] = v, (i, j, j)
            if i < n:                                   # 邊界 i 不對停頓（句中無停頓）
                v = c + 1.2
                if v < dp[i + 1][j]:
                    dp[i + 1][j], bk[i + 1][j] = v, (i, j, "none")
    res, i, j = [None] * n, n, m
    while (i, j) != (0, 0):
        pi, pj, what = bk[i][j]
        if isinstance(what, int):
            res[pi] = what
        i, j = pi, pj
    return res


def main():
    tl = {k: a for k, a, b in json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))}
    n, out, report = 1, [], []
    for key, text in SEGMENTS:
        wav = os.path.join(HERE, "audio", f"{key}.wav")
        L = wav_len(wav)
        sil = silences(wav, db=-38, dur=0.12)
        s0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
        s1 = sil[-1][0] if sil and sil[-1][1] > L - 0.05 else L
        inner = [(a, b) for a, b in sil if a > s0 + 0.05 and b < s1 - 0.05]
        speech = (s1 - s0) - sum(b - a for a, b in inner)

        def sp_frac(t):  # 真實時間 → 語音時間比例
            v = t - s0 - sum(min(b, t) - a for a, b in inner if a < t)
            return v / speech

        def at(frac):
            need, t = frac * speech, s0
            for a, b in inner:
                if t + need <= a:
                    return t + need
                need -= a - t; t = b
            return min(t + need, s1)

        sp_parts = clauses(re.sub(r"\s*<[^>]+>\s*", "", text))
        dp_parts = clauses(to_display(text))
        assert len(sp_parts) == len(dp_parts), (key, sp_parts, dp_parts)
        w = [spoken_weight(c) for c in sp_parts]
        tot, acc, fr = sum(w), 0, []
        for x in w[:-1]:
            acc += x; fr.append(acc / tot)
        pauses = [(a, b, sp_frac(a)) for a, b in inner]
        match = align(fr, pauses, speech)
        # 子句起訖：對到停頓 → 前句結束於停頓開始、後句開始於停頓結束；否則按比例內插
        starts, ends = [s0], []
        for f, mj in zip(fr, match):
            if mj is None:
                t = at(f); ends.append(t); starts.append(t)
            else:
                ends.append(pauses[mj][0]); starts.append(pauses[mj][1])
        ends.append(s1)
        base = tl[key]
        for g in group(dp_parts):
            a, b = starts[g[0]], ends[g[-1]]
            txt = "".join(dp_parts[i] for i in g).strip().rstrip("，。：；、")
            out.append((base + a, base + b, txt))
        report.append(f"{key}: {sum(m is not None for m in match)}/{len(match)} 個子句邊界對到停頓")
    # 相鄰字幕：前一條延到下一條開始（最多延 0.8 s），避免閃爍
    lines = []
    for i, (a, b, t) in enumerate(out):
        if i + 1 < len(out):
            b = min(max(b, min(out[i + 1][0], b + 0.8)), out[i + 1][0])
        lines.append(f"{i + 1}\n{fmt(a)} --> {fmt(b)}\n{t}\n")
    p = os.path.join(HERE, f"{PID}.srt")
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(report))
    print(f"{len(lines)} 條字幕 → {p}")


if __name__ == "__main__":
    if "--preview" in sys.argv:
        for k, t in SEGMENTS:
            parts = clauses(to_display(t))
            print(k, " | ".join("".join(parts[i] for i in g) for g in group(parts)))
    else:
        main()
