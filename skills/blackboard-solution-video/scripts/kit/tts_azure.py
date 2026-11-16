"""Azure TTS 配音（備用）：讀本資料夾 segments.py → audio/s*.wav ＋ durations.json
用法：python tts_azure.py [--only s05,s12] [--resume]
需求：pip install azure-cognitiveservices-speech
金鑰：.env 內 AZURE_SPEECH_KEY、AZURE_SPEECH_REGION（找法同 tts_gemini.py）
"""
import argparse, json, os, sys, time, wave
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from segments import SEGMENTS, AZURE_VOICE, AZURE_RATE
from tts_gemini import load_env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--resume", action="store_true", help="略過已用同一聲音配好的段落（中斷後續跑）")
    a = ap.parse_args()
    load_env()
    import azure.cognitiveservices.speech as sdk
    cfg = sdk.SpeechConfig(subscription=os.environ["AZURE_SPEECH_KEY"], region=os.environ["AZURE_SPEECH_REGION"])
    cfg.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    os.chdir(HERE)
    os.makedirs("audio", exist_ok=True)
    stamp = os.path.join("audio", ".azure_voice")
    same_voice = os.path.exists(stamp) and open(stamp, encoding="utf-8").read().strip() == AZURE_VOICE + AZURE_RATE
    durations = json.load(open("durations.json", encoding="utf-8")) if (a.only or a.resume) and os.path.exists("durations.json") else {}
    only = set(a.only.split(",")) if a.only else None
    log = open("tts_azure.log", "a", encoding="utf-8")
    for key, text in SEGMENTS:
        if only and key not in only:
            continue
        wav = f"audio/{key}.wav"
        if a.resume and not only and same_voice and os.path.exists(wav) and os.path.getsize(wav) > 1000:
            with wave.open(wav) as w:
                durations[key] = round(w.getnframes() / w.getframerate(), 3)
            continue
        text = text.replace("<short pause>", '<break time="300ms"/>').replace("<long pause>", '<break time="700ms"/>')
        ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">'
                f'<voice name="{AZURE_VOICE}"><prosody rate="{AZURE_RATE}">{text}</prosody></voice></speak>')
        for attempt in range(5):
            out = sdk.audio.AudioOutputConfig(filename=wav)
            syn = sdk.SpeechSynthesizer(speech_config=cfg, audio_config=out)
            r = syn.speak_ssml_async(ssml).get()
            del syn, out
            if r.reason == sdk.ResultReason.SynthesizingAudioCompleted:
                break
            msg = f"{key} 第 {attempt + 1} 次失敗：{r.cancellation_details.error_details}"
            print(msg); log.write(msg + "\n"); log.flush()
            time.sleep(5 * 2 ** attempt)
        else:
            raise SystemExit(f"{key} 配音失敗，見 tts_azure.log")
        with wave.open(wav) as w:
            durations[key] = round(w.getnframes() / w.getframerate(), 3)
        print(key, durations[key], "s"); log.write(f"{key} {durations[key]}\n"); log.flush()
        open(stamp, "w", encoding="utf-8").write(AZURE_VOICE + AZURE_RATE)
        same_voice = True
        json.dump(durations, open("durations.json", "w", encoding="utf-8"), indent=1)
    json.dump(durations, open("durations.json", "w", encoding="utf-8"), indent=1)
    print("完成 → audio/*.wav、durations.json")


if __name__ == "__main__":
    main()
