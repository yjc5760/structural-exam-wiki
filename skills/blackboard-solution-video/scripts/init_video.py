"""建立一題的影片工作資料夾：把 kit/ 的底座、工具、黑板底圖複製過去，並填好題號與主題。
用法：python init_video.py <目標資料夾> --id SM-2020-3 --topic 相對密度 [--force]
已存在的檔案不覆蓋（segments.py、scene.py 是你改過的東西），除非加 --force。
"""
import argparse, os, re, shutil

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit")

SCENE_TEMPLATE = '''"""{pid} 黑板講解影片
講稿／章節／分鏡：segments.py（唯一改稿處）；底座：board_scene.py
  manim -qm scene.py Full   # 720p 審閱（無聲、估計時長）
  manim -qh scene.py Full   # 1080p 成片（有 durations.json 就對齊真實配音）
每段：self.begin("sXX") → 動畫 → self.end()；換章前 self.clear_board()
"""
from board_scene import *


class Full(BoardScene):
    def construct(self):
        self.intro()
        self.begin("s01")
        q = T("題目原文……", 34).move_to(UP * 0.5)
        self.play(Write(q), run_time=3)
        self.end()
        # …依 segments.BOARD 逐段寫動畫…
        self.wait(1.0)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dest")
    ap.add_argument("--id", required=True)
    ap.add_argument("--topic", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.dest, exist_ok=True)
    done = []
    for f in sorted(os.listdir(KIT)):
        src = os.path.join(KIT, f)
        if not os.path.isfile(src) or f.endswith(".pyc"):
            continue
        dst = os.path.join(a.dest, f)
        if os.path.exists(dst) and not a.force:
            continue
        shutil.copyfile(src, dst)
        done.append(f)
    seg = os.path.join(a.dest, "segments.py")
    if "segments.py" in done:
        s = open(seg, encoding="utf-8").read()
        s = re.sub(r'PROBLEM_ID = ".*?"', f'PROBLEM_ID = "{a.id}"', s)
        s = re.sub(r'TOPIC = ".*?"', f'TOPIC = "{a.topic}"', s)
        open(seg, "w", encoding="utf-8").write(s)
    scene = os.path.join(a.dest, "scene.py")
    if not os.path.exists(scene) or a.force:
        open(scene, "w", encoding="utf-8").write(SCENE_TEMPLATE.format(pid=a.id))
        done.append("scene.py")
    print(f"{a.dest}：新增 {len(done)} 個檔案 → {', '.join(done) or '（無，全都已存在）'}")


if __name__ == "__main__":
    main()
