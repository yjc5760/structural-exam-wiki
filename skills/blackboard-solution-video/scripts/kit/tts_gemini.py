"""Gemini TTS 配音（在自己電腦上跑；雲端沙箱通常連不到 Google API）
讀本資料夾 segments.py → audio/s*.wav ＋ durations.json（每段秒數，渲染與字幕都靠它）

用法（Windows cmd，於本資料夾，或雙擊 run_tts.bat）：
  python tts_gemini.py                         全部段落配音
  python tts_gemini.py --only s05,s12          只重配某幾段（其他段秒數保留）
  python tts_gemini.py --audition Charon,Sadaltager,Iapetus
                                               用第一段講稿試聽多個聲音 → audition/*.wav
  python tts_gemini.py --list-voices           列出聲音庫的台灣華語男聲
需求：pip install -U "google-genai>=2.25.0"
金鑰：.env 內 GEMINI_API_KEY=...（依序找：本資料夾、往上三層資料夾、目前資料夾；或設成環境變數）
"""
import argparse, base64, json, os, re, sys, time, wave
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from segments import SEGMENTS, GEMINI_MODEL, GEMINI_VOICE, GEMINI_STYLE


def load_env():
    cands, d = [], HERE
    for _ in range(4):
        cands.append(os.path.join(d, ".env")); d = os.path.dirname(d)
    cands.append(os.path.join(os.getcwd(), ".env"))
    for p in cands:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    if v.strip().strip('"'):
                        os.environ.setdefault(k.strip(), v.strip().strip('"'))


def synth(client, text, voice, path, retries=4):
    content = {"type": "text", "text": text}
    if GEMINI_STYLE:
        content["annotations"] = [{"type": "speech_metadata", "style": GEMINI_STYLE}]
    for i in range(retries):
        try:
            it = client.interactions.create(
                model=GEMINI_MODEL,
                input=[{"type": "user_input", "content": [content]}],
                response_format={"type": "audio"},            # 回傳含 RIFF 標頭的 WAV
                generation_config={"speech_config": [{"voice": voice}]},
            )
            with open(path, "wb") as f:
                f.write(base64.b64decode(it.output_audio.data))
            with wave.open(path) as w:
                return round(w.getnframes() / w.getframerate(), 3)
        except Exception as e:                                # 429／暫時性錯誤：退避重試
            if i == retries - 1:
                raise
            wait = 5 * 2 ** i
            print(f"  重試（{e.__class__.__name__}），{wait}s 後…")
            time.sleep(wait)


def list_voices(client):
    r = client.voices.list(language_code=["zh-TW", "cmn-TW", "cmn-Hant-TW", "zh-Hant-TW"],
                           gender=["male"], page_size=200)
    vs = r.voices or []
    if not vs:
        vs = client.voices.list(search="Mandarin", gender=["male"], page_size=200).voices or []
    for v in vs:
        print(f"{v.id:28} {v.display_name} | {v.language_code} {v.accent} pitch={v.pitch} | {v.description}")
    print(f"共 {len(vs)} 個")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--audition", help="逗號分隔的聲音名稱／ID")
    ap.add_argument("--only", help="只重配指定段落，逗號分隔，例如 s05,s12")
    a = ap.parse_args()
    load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("找不到 GEMINI_API_KEY（放在 .env 或環境變數）")
    from google import genai
    client = genai.Client()
    os.chdir(HERE)

    if a.list_voices:
        return list_voices(client)
    if a.audition:
        os.makedirs("audition", exist_ok=True)
        for v in [x.strip() for x in a.audition.split(",") if x.strip()]:
            safe = re.sub(r"[^\w.-]", "_", v)
            d = synth(client, SEGMENTS[0][1], v, f"audition/{safe}.wav")
            print(f"{v:24} {d:6.2f}s → audition/{safe}.wav")
        return

    os.makedirs("audio", exist_ok=True)
    durations = {}
    if a.only and os.path.exists("durations.json"):
        durations = json.load(open("durations.json", encoding="utf-8"))
    only = set(x.strip() for x in a.only.split(",")) if a.only else None
    for key, text in SEGMENTS:
        if only and key not in only:
            continue
        durations[key] = synth(client, text, GEMINI_VOICE, f"audio/{key}.wav")
        print(f"{key}  {durations[key]:6.2f}s")
    json.dump(durations, open("durations.json", "w", encoding="utf-8"), indent=1)
    json.dump({"model": GEMINI_MODEL, "voice": GEMINI_VOICE, "style": GEMINI_STYLE},
              open("audio/tts_meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"完成 → audio/*.wav、durations.json（合計 {sum(durations.values()) / 60:.1f} 分鐘）")


if __name__ == "__main__":
    main()
