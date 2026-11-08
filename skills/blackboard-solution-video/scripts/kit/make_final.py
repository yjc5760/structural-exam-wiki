"""合成成片：Manim 影片 ＋ 各段配音（依 timeline.json 對位）→ <PROBLEM_ID>.mp4
前置：manim -qh scene.py Full（產生影片與 timeline.json）；要燒字幕另需 python make_srt.py
用法：python make_final.py [影片路徑] [--burn]
  影片路徑預設為 media/videos/scene/ 底下最新的 Full.mp4
  預設不燒字幕（YouTube 另傳 .srt）；加 --burn 才把字幕燒進畫面
  輸出 1080p30、CRF 28、tune stillimage：黑板片 6 分鐘約 18 MB（< 20 MB，方便傳檔）
"""
import glob, json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
import segments
PID = getattr(segments, "PROBLEM_ID", "video")

BURN = "--burn" in sys.argv
args = [a for a in sys.argv[1:] if a != "--burn"]
if args:
    video = args[0]
else:
    c = sorted(glob.glob(os.path.join("media", "videos", "**", "Full.mp4"), recursive=True), key=os.path.getmtime)
    c = [x for x in c if "partial_movie_files" not in x]
    if not c:
        sys.exit("找不到 Full.mp4，請先 manim -qh scene.py Full")
    video = c[-1]
print("影片：", video)

tl = json.load(open("timeline.json", encoding="utf-8"))
SR = 48000
vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                             video], capture_output=True, text=True).stdout)
track = np.zeros(int((vdur + 1) * SR), dtype=np.float32)
for key, a, b in tl:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join("audio", f"{key}.wav"), "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    i = int(round(a * SR))
    track[i:i + len(x)] += x[:len(track) - i]
track = track[:int(vdur * SR)]
pcm = (np.clip(track, -1, 1) * 32767).astype(np.int16)
with wave.open(f"{PID}_narration.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

style = ("FontName=Noto Sans CJK TC,FontSize=18,PrimaryColour=&H00F0F2F2,OutlineColour=&H00000000,"
         "BackColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=14")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", f"{PID}_narration.wav",
                *(["-vf", f"subtitles={PID}.srt:force_style='{style}'"] if BURN else []),
                "-r", "30", "-c:v", "libx264", "-crf", "28", "-preset", "slow", "-tune", "stillimage",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", "-shortest",
                f"{PID}.mp4"], check=True)
print(f"完成 → {PID}.mp4（{os.path.getsize(PID + '.mp4') / 1e6:.1f} MB）")
