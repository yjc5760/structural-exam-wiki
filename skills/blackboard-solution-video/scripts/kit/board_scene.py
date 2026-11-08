"""黑板講解影片共用底座（Manim）。題目專屬的 scene.py 只要：

    from board_scene import *
    class Full(BoardScene):
        def construct(self):
            self.intro()                 # 左上角題號＋主題（來自 segments.py）
            self.begin("s01"); ...動畫...; self.end()
            ...

- begin(key)：段落開始；章節換了會自動換左上角章名
- end()：補 wait 到該段配音長度（durations.json 真實秒數 +0.6 s；沒有就以每秒 4.6 字估），
         並把 (key, 開始, 結束) 寫進 timeline.json（配音合成與字幕都靠它對位）
- clear_board(keep=[...])：換板，保留標題列與章名
渲染：manim -qm scene.py Full（720p 審閱）／ manim -qh scene.py Full（1080p60 成片）
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from manim import *
import segments as _seg

SEGMENTS = _seg.SEGMENTS
CHAPTERS = _seg.CHAPTERS
PROBLEM_ID = getattr(_seg, "PROBLEM_ID", "")
TOPIC = getattr(_seg, "TOPIC", "")

# 粉筆色系（同一個量全片用同一色：分子粉紅、分母藍、答案黃、錯誤紅、正確綠）
CHALK = "#F2F0E6"
YELLOW_C = "#F4D35E"
PINK_C = "#F28DA6"
BLUE_C = "#8ECAE6"
SOIL_C = "#C9A27A"
RED_C = "#F07167"
GREEN_C = "#9BE39B"
FONT = "Iansui"          # 芫荽（github.com/ButTaiwan/iansui），手寫感；沒裝會退回系統字型

SEG = dict(SEGMENTS)
CHAP_OF = {k: name for _, name, keys in CHAPTERS for k in keys}


def spoken(t):
    return re.sub(r"\s*<[^>]+>\s*", "", t)


def load_durations():
    p = os.path.join(HERE, "durations.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        return {k: v + 0.6 for k, v in d.items()}
    return {k: len(spoken(t)) / 4.6 + 0.6 for k, t in SEGMENTS}


def T(s, size=40, color=CHALK):
    """中文字（Iansui）。注意：Text 的子物件不含空白，用索引取字時要先去掉空白再算位置。"""
    return Text(s, font=FONT, font_size=size, color=color)


def M(s, size=48, color=CHALK):
    """LaTeX 公式。不要在 MathTex 裡放中文（會 LaTeX Unicode 錯誤）——中文用 T() 再 row() 併排。"""
    return MathTex(s, font_size=size, color=color)


def row(*items, buff=0.18):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def xmark(m, color=RED_C):
    return Cross(m, stroke_color=color, stroke_width=5, scale_factor=0.9)


class BoardScene(Scene):
    def setup(self):
        bg = ImageMobject(os.path.join(HERE, "board.png"))
        bg.height = config.frame_height
        self.add(bg)
        self.dur = load_durations()
        self.timeline = []
        self.chap = None
        self.title = None

    def intro(self):
        s = "　".join(x for x in (PROBLEM_ID, TOPIC) if x)
        self.title = T(s, 30, YELLOW_C).to_corner(UL, buff=0.45)
        self.ul = Line(self.title.get_corner(DL), self.title.get_corner(DR), color=YELLOW_C,
                       stroke_width=2).shift(DOWN * 0.08)
        self.add(self.title, self.ul)

    # ---------- 計時 ----------
    def begin(self, key):
        if self.title is None:
            self.intro()
        self._key, self._t0 = key, self.renderer.time
        name = CHAP_OF.get(key)
        if name and name != getattr(self.chap, "chap_name", None):
            new = T(name, 26, CHALK).set_opacity(0.8)
            new.next_to(self.title, RIGHT, buff=0.5).align_to(self.title, DOWN)
            new.chap_name = name
            if self.chap is None:
                self.play(FadeIn(new), run_time=0.4)
            else:
                self.play(FadeOut(self.chap, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.4)
            self.chap = new

    def end(self):
        used = self.renderer.time - self._t0
        rest = self.dur[self._key] - used
        if rest > 0.05:
            self.wait(rest)
        self.timeline.append((self._key, self._t0, self.renderer.time))
        with open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8") as f:
            json.dump(self.timeline, f)

    def clear_board(self, keep=(), run_time=0.6):
        keep = set(keep) | {self.title, self.ul, self.chap}
        gone = [m for m in self.mobjects if m not in keep and not isinstance(m, ImageMobject)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)
