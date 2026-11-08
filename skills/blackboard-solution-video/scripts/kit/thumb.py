"""YouTube 封面（1280×720 PNG，黑板風）
  manim -s -r 1280,720 --format png --disable_caching thumb.py Thumb
  → media/images/thumb/Thumb_ManimCE_*.png（複製成 <題號>_thumbnail.png）
改下面「文字」區；右半邊 figure() 換成這題最有辨識度的圖（柱子、彎矩圖、莫爾圓…），
左半邊留給大字。手機上封面只有郵票大小：主標 ≤ 2 行、每行 ≤ 6 字，最多 3 種顏色。
"""
from board_scene import *

# ── 文字 ──
TAG = f"科目｜{PROBLEM_ID}"              # 左上小標，例：土壤力學｜SM-2020-3
LINE1 = "一句抓住人的"                    # 主標第一行（白）
LINE2 = "結論或關鍵字"                    # 主標第二行（黃）
RING_CHAR = None                          # 主標第一行要圈起來的字的索引（不含空白），例：3；不要就 None
SUB1 = [("答案是", "t"), (r"D_r=70\%", "m")]   # 副標第一行：("文字","t") 或 ("LaTeX","m")
SUB2 = "＋ 常見陷阱"                        # 副標第二行（粉紅），不要就 ""


def figure():
    """右半邊的圖。回傳一個 VGroup，會自動縮放放進 x∈[1.5,6.7]、y∈[-3.3,3]。"""
    ans = M(r"D_r=70\%", 96, YELLOW_C)
    box = SurroundingRectangle(ans, color=YELLOW_C, buff=0.35, stroke_width=8)
    return VGroup(ans, box)


class Thumb(Scene):
    def construct(self):
        bg = ImageMobject(os.path.join(HERE, "board.png")); bg.height = config.frame_height
        self.add(bg)
        tag = T(TAG, 34, CHALK).to_corner(UL, buff=0.5)
        tag_ul = Line(tag.get_corner(DL), tag.get_corner(DR), color=CHALK, stroke_width=2).shift(DOWN * 0.1)
        l1 = T(LINE1, 92, CHALK)
        l2 = T(LINE2, 92, YELLOW_C)
        head = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        head.next_to(tag, DOWN, buff=0.55).align_to(tag, LEFT)
        extra = []
        if RING_CHAR is not None:
            ci = l1[RING_CHAR]; ci.set_color(YELLOW_C)
            extra.append(Ellipse(width=ci.width + 0.55, height=ci.height + 0.5, color=YELLOW_C,
                                 stroke_width=7).move_to(ci))
        s1 = row(*[T(x, 40, CHALK) if k == "t" else M(x, 56, YELLOW_C) for x, k in SUB1], buff=0.25)
        subs = VGroup(s1, *([T(SUB2, 40, PINK_C)] if SUB2 else [])).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        subs.next_to(head, DOWN, buff=0.6).align_to(head, LEFT)
        fig = figure()
        fig.scale_to_fit_width(min(fig.width, 5.2))
        if fig.height > 6.2:
            fig.scale_to_fit_height(6.2)
        fig.move_to([4.1, -0.1, 0])
        left = max(1.5, head.get_right()[0] + 0.4)      # 不壓到主標
        if fig.get_left()[0] < left:
            fig.scale((6.7 - left) / fig.width).move_to([(left + 6.7) / 2, -0.1, 0])
        self.add(tag, tag_ul, head, *extra, subs, fig)
