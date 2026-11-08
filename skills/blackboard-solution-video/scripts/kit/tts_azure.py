"""Azure TTS 配音（備用）：讀本資料夾 segments.py → audio/s*.wav ＋ durations.json
用法：python tts_azure.py [--only s05,s12]
需求：pip install azure-cognitiveservices-speech
金鑰：.env 內 AZURE_SPEECH_KEY、AZURE_SPEECH_REGION（找法同 tts_gemini.py）
"""
import argparse, json, os, sys, wave
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from segments import SEGMENTS, AZURE_VOICE, AZURE_RATE
from tts_gemini import load_env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    load_env()
    import azure.cognitiveservices.speech as sdk
    cfg = sdk.SpeechConfig(subscription=os.environ["AZURE_SPEECH_KEY"], region=os.environ["AZURE_SPEECH_REGION"])
    cfg.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    os.chdir(HERE)
    os.makedirs("audio", exist_ok=True)
    durations = json.load(open("durations.json", encoding="utf-8")) if a.only and os.path.exists("durations.json") else {}
    only = set(a.only.split(",")) if a.only else None
    for key, text in SEGMENTS:
        if only and key not in only:
            continue
        text = text.replace("<short pause>", '<break time="300ms"/>').replace("<long pause>", '<break time="700ms"/>')
        ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">'
                f'<voice name="{AZURE_VOICE}"><prosody rate="{AZURE_RATE}">{text}</prosody></voice></speak>')
        out = sdk.audio.AudioOutputConfig(filename=f"audio/{key}.wav")
        r = sdk.SpeechSynthesizer(speech_config=cfg, audio_config=out).speak_ssml_async(ssml).get()
        if r.reason != sdk.ResultReason.SynthesizingAudioCompleted:
            raise SystemExit(f"{key} 配音失敗：{r.cancellation_details.error_details}")
        with wave.open(f"audio/{key}.wav") as w:
            durations[key] = round(w.getnframes() / w.getframerate(), 3)
        print(key, durations[key], "s")
    json.dump(durations, open("durations.json", "w", encoding="utf-8"), indent=1)
    print("完成 → audio/*.wav、durations.json")


if __name__ == "__main__":
    main()
