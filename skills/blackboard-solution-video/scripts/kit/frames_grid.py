"""版面檢查：擷取每段結束前的畫格，拼成 2×3 格狀圖 frames_grid_N.png，一眼看出文字重疊、出界。
用法：python frames_grid.py [影片路徑]   （預設 media/videos/scene/ 底下最新的 Full.mp4）
"""
import glob, json, os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
if len(sys.argv) > 1:
    video = sys.argv[1]
else:
    c = [x for x in glob.glob("media/videos/**/Full.mp4", recursive=True) if "partial" not in x]
    video = max(c, key=os.path.getmtime)
tl = json.load(open("timeline.json", encoding="utf-8"))
os.makedirs("frames", exist_ok=True)
paths = []
for k, a, b in tl:
    p = f"frames/{k}.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(max(b - 0.15, 0)), "-i", video,
                    "-frames:v", "1", "-vf", "scale=854:-2", p], check=True)
    paths.append(p)
for n in range(0, len(paths), 6):
    ims = [Image.open(p) for p in paths[n:n + 6]]
    W, H = ims[0].size
    g = Image.new("RGB", (W * 2, H * 3))
    for i, im in enumerate(ims):
        g.paste(im, ((i % 2) * W, (i // 2) * H))
    out = f"frames_grid_{n // 6 + 1}.png"
    g.save(out)
    print(out, "←", ", ".join(os.path.basename(p)[:-4] for p in paths[n:n + 6]))
