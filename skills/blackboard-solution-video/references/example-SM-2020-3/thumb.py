"""YouTube 封面範例（1280×720）：manim -s -r 1280,720 --format png thumb.py Thumb"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from manim import *
from board_scene import T, M, CHALK, YELLOW_C, PINK_C, BLUE_C, SOIL_C, RED_C


class Thumb(Scene):
    def construct(self):
        bg = ImageMobject(os.path.join(HERE, "board.png")); bg.height = config.frame_height
        self.add(bg)

        # 左上標籤
        tag = T("土壤力學｜SM-2020-3", 34, CHALK).to_corner(UL, buff=0.5)
        tag_ul = Line(tag.get_corner(DL), tag.get_corner(DR), color=CHALK, stroke_width=2).shift(DOWN * 0.1)

        # 主標
        l1 = T("一個「此」字", 92, CHALK)
        ci = l1[3]
        ci.set_color(YELLOW_C)
        ring = Ellipse(width=ci.width + 0.55, height=ci.height + 0.5, color=YELLOW_C,
                       stroke_width=7).move_to(ci)
        l2 = T("相對密度秒解", 92, YELLOW_C)
        head = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        head.next_to(tag, DOWN, buff=0.55).align_to(tag, LEFT)
        ring.move_to(ci)

        sub = VGroup(T("三種算法都是", 40, CHALK), M(r"D_r=70\%", 56, YELLOW_C)).arrange(RIGHT, buff=0.25)
        traps = T("＋ 三個常見陷阱", 40, PINK_C)
        subs = VGroup(sub, traps).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        subs.next_to(head, DOWN, buff=0.6).align_to(head, LEFT)

        # 右側三根柱子
        k, base_y, Vs, w = 0.0078, -3.1, 314.8, 1.05
        bars = VGroup()
        tops = {}
        for name, V, x in [("鬆", 640, 2.35), ("現地", 500, 3.75), ("緊", 440, 5.15)]:
            soil = Rectangle(width=w, height=Vs * k, stroke_color=CHALK, stroke_width=4,
                             fill_color=SOIL_C, fill_opacity=0.4).move_to([x, base_y + Vs * k / 2, 0])
            voids = Rectangle(width=w, height=(V - Vs) * k, stroke_color=CHALK, stroke_width=4,
                              fill_opacity=0).next_to(soil, UP, buff=0)
            dots = VGroup(*[Dot(radius=0.04, color=SOIL_C).move_to(
                soil.get_center() + [((i * 37) % 9 - 4) * 0.1, ((i * 53) % 7 - 3) * 0.17, 0]) for i in range(14)])
            num = M(str(V), 44).move_to(voids)
            bars.add(VGroup(soil, dots, voids, num))
            tops[V] = voids.get_top()[1]
        sy = base_y + Vs * k
        dash = DashedLine([1.6, sy, 0], [5.9, sy, 0], color=YELLOW_C, stroke_width=4, dash_length=0.14)
        vs = VGroup(M(r"V_s", 40, YELLOW_C), T("固定", 32, YELLOW_C)).arrange(RIGHT, buff=0.1)
        vs.next_to(dash, LEFT, buff=0.15)
        # 70% 標記
        arr = Arrow([6.2, tops[500] + 1.0, 0], [3.75 + w / 2 + 0.05, tops[500] + 0.02, 0], buff=0,
                    color=YELLOW_C, stroke_width=7, max_tip_length_to_length_ratio=0.2)
        ans = M(r"70\%", 64, YELLOW_C).next_to(arr.get_start(), UP, buff=0.05)

        self.add(tag, tag_ul, head, ring, subs, bars, dash, vs, arr, ans)
