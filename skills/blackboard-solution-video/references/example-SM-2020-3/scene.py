"""SM-2020-3 黑板講解影片（範例：整題 22 段、6 章，約 6 分鐘）
講稿／章節／分鏡：segments.py；底座：board_scene.py
  manim -qm scene.py Full   # 720p 審閱
  manim -qh scene.py Full   # 1080p 成片
"""
from board_scene import *


class Full(BoardScene):
    # ---------- 場景 ----------
    def construct(self):
        self.intro()
        self.c0()
        self.c1()
        self.c2()
        self.c3()
        self.c4()
        self.c5()
        self.wait(1.0)

    # ===== c0 題目 =====
    def c0(self):
        self.begin("s01")
        lines = [
            "欲了解某工址現地土壤之緊密程度，以取樣器取得",
            "500 ml 之砂土，其重量為 900 克，烘乾後重量為 850 克。",
            "將此砂土置於夯實模內，最緊密狀態體積為 440 ml，",
            "最疏鬆狀態體積為 640 ml；現地砂土飽和度為 27%。",
            "請求得此砂土之相對密度。",
        ]
        marks = [[], ["500 ml", "900", "850"], ["440 ml"], ["640 ml", "27%"], ["相對密度"]]
        txt = VGroup(*[T(s, 34) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        txt.move_to(DOWN * 0.1)
        self.play(LaggedStart(*[Write(l) for l in txt], lag_ratio=0.85), run_time=6.5)
        hl = []
        for i, words in enumerate(marks):
            flat = lines[i].replace(" ", "")
            for w in words:
                a = flat.find(w.replace(" ", ""))
                seg = txt[i][a:a + len(w.replace(" ", ""))]
                u = Line(seg.get_corner(DL), seg.get_corner(DR), color=YELLOW_C,
                         stroke_width=3).shift(DOWN * 0.07)
                hl.append((seg, u))
        for seg, u in hl:
            self.play(seg.animate.set_color(YELLOW_C), Create(u), run_time=0.45)
        goal = row(T("求", 36, YELLOW_C), M(r"D_r", 48, YELLOW_C))
        goal.next_to(txt[4], RIGHT, buff=0.6)
        self.play(Write(goal), Create(SurroundingRectangle(goal, color=YELLOW_C, buff=0.15)),
                  run_time=0.9)
        self.end()

    # ===== c1 方法一（沿用試片） =====
    def c1(self):
        self.begin("s02")
        self.clear_board()
        quote = T("「將此砂土置於夯實模內」", 46).move_to(UP * 2.3)
        self.play(Write(quote), run_time=1.8)
        ci = quote[2]
        ring = Ellipse(width=ci.width + 0.45, height=ci.height + 0.4,
                       color=YELLOW_C, stroke_width=4).move_to(ci)
        self.play(Create(ring), ci.animate.set_color(YELLOW_C), run_time=0.8)
        chain = VGroup(
            T("同一堆土", 38), M(r"\Rightarrow"),
            M(r"W_s=850\,\mathrm{g}", 46), T("固定", 38), M(r"\Rightarrow"),
            M(r"V_s", 50, YELLOW_C), T("固定", 38, YELLOW_C),
        ).arrange(RIGHT, buff=0.22).next_to(quote, DOWN, buff=0.55)
        for m in chain:
            self.play(Write(m), run_time=0.45)
        self.end()

        # --- s03 三根柱子 ---
        self.begin("s03")
        top_grp = VGroup(quote, ring, chain)
        self.play(top_grp.animate.scale(0.58).to_corner(UR, buff=0.5).shift(DOWN * 0.05),
                  run_time=0.8)
        k, base_y, Vs, w = 0.0058, -2.35, 314.8, 1.1
        self.k, self.base_y, self.w = k, base_y, w
        data = [("最疏鬆", 640, -5.6), ("現地", 500, -3.9), ("最緊密", 440, -2.2)]
        bars, tops = VGroup(), {}
        for name, V, x in data:
            soil = Rectangle(width=w, height=Vs * k, stroke_color=CHALK, stroke_width=3,
                             fill_color=SOIL_C, fill_opacity=0.35)
            soil.move_to([x, base_y + Vs * k / 2, 0])
            voids = Rectangle(width=w, height=(V - Vs) * k, stroke_color=CHALK,
                              stroke_width=3, fill_opacity=0).next_to(soil, UP, buff=0)
            dots = VGroup(*[Dot(radius=0.035, color=SOIL_C).move_to(
                soil.get_center() + [((i * 37) % 9 - 4) * 0.11, ((i * 53) % 7 - 3) * 0.13, 0])
                for i in range(14)])
            lab = T(name, 30).next_to(soil, DOWN, buff=0.18)
            num = M(str(V), 34).move_to(voids)
            bars.add(VGroup(soil, dots, voids, lab, num))
            tops[V] = voids.get_top()[1]
        self.tops = tops
        for g in bars:
            soil, dots, voids, lab, num = g
            self.play(GrowFromEdge(soil, DOWN), FadeIn(dots), GrowFromEdge(voids, DOWN),
                      Write(lab), run_time=0.9)
            self.play(Write(num), run_time=0.35)
        solid_y = base_y + Vs * k
        dash = DashedLine([-6.4, solid_y, 0], [-1.5, solid_y, 0], color=YELLOW_C,
                          stroke_width=3, dash_length=0.12)
        vs_lab = M(r"V_s=314.8", 32, YELLOW_C).next_to(dash, RIGHT, buff=0.15)
        self.play(Create(dash), run_time=0.7)
        self.play(Write(vs_lab), run_time=0.6)
        void_lab = T("孔隙在變", 30, BLUE_C).move_to([-3.9, tops[640] + 0.4, 0])
        self.play(Indicate(VGroup(*[g[2] for g in bars]), color=BLUE_C, scale_factor=1.04),
                  Write(void_lab), run_time=1.0)
        self.bars, self.dash, self.vs_lab, self.void_lab = bars, dash, vs_lab, void_lab
        self.end()

        # --- s04 為何能用體積算：V_s 約掉 ---
        self.begin("s04")
        x0 = 0.3
        d1 = M(r"D_r=\frac{e_{max}-e}{e_{max}-e_{min}}", 40)
        d2 = M(r"e=\frac{V-V_s}{V_s}", 40)
        d1.move_to([0, 1.3, 0]).align_to([x0, 0, 0], LEFT)
        d2.next_to(d1, RIGHT, buff=0.55)
        self.play(Write(d1), run_time=1.4)
        self.play(Write(d2), run_time=1.2)
        d3 = M(r"D_r=\frac{\dfrac{V_{max}-V}{V_s}}{\dfrac{V_{max}-V_{min}}{V_s}}", 38)
        d3.next_to(d1, DOWN, buff=0.45).align_to(d1, LEFT)
        self.play(Write(d3), run_time=1.6)
        vs1, vs2 = d3[0][10:12], d3[0][23:25]
        self.play(vs1.animate.set_color(YELLOW_C), vs2.animate.set_color(YELLOW_C), run_time=0.5)
        s1 = Line(vs1.get_corner(DL), vs1.get_corner(UR), color=RED_C, stroke_width=5)
        s2 = Line(vs2.get_corner(DL), vs2.get_corner(UR), color=RED_C, stroke_width=5)
        self.play(Create(s1), Create(s2), run_time=0.6)
        d4 = M(r"=\frac{V_{max}-V}{V_{max}-V_{min}}", 38).next_to(d3, RIGHT, buff=0.2)
        self.play(Write(d4), run_time=1.2)
        self.play(Circumscribe(d4, color=YELLOW_C), run_time=0.9)
        self.deriv = VGroup(d1, d2, d3, s1, s2)
        self.d4 = d4
        self.end()

        # --- s05 代數字（沿用試片 S3） ---
        self.begin("s05")
        f1 = M(r"D_r=\frac{V_{max}-V}{V_{max}-V_{min}}", 56).move_to([3.3, 1.05, 0])
        self.play(FadeOut(self.deriv), ReplacementTransform(self.d4, f1), run_time=1.0)
        top640, top500, top440 = tops[640], tops[500], tops[440]
        xr = -2.2 + w / 2 + 0.3
        g640 = DashedLine([-5.6 + w / 2, top640, 0], [xr + 0.55, top640, 0],
                          color=CHALK, stroke_width=2, dash_length=0.08)
        g500 = DashedLine([-3.9 + w / 2, top500, 0], [xr + 0.15, top500, 0],
                          color=PINK_C, stroke_width=2, dash_length=0.08)
        g440 = DashedLine([-2.2 + w / 2, top440, 0], [xr + 0.55, top440, 0],
                          color=BLUE_C, stroke_width=2, dash_length=0.08)
        num_br = DoubleArrow([xr, top640, 0], [xr, top500, 0], buff=0, color=PINK_C,
                             stroke_width=5, tip_length=0.15)
        den_br = DoubleArrow([xr + 0.4, top640, 0], [xr + 0.4, top440, 0], buff=0, color=BLUE_C,
                             stroke_width=5, tip_length=0.15)
        n_lab = M("140", 30, PINK_C).next_to(num_br, LEFT, buff=0.08)
        d_lab = M("200", 30, BLUE_C).next_to(den_br, RIGHT, buff=0.1)
        f2 = M(r"=\frac{640-500}{640-440}", 56).next_to(f1, DOWN, buff=0.35).align_to(f1[0][2], LEFT)
        self.play(Write(f2), run_time=1.4)
        self.play(Create(g640), Create(g500), GrowFromCenter(num_br), FadeIn(n_lab),
                  f2[0][1:8].animate.set_color(PINK_C), run_time=0.9)
        self.play(Create(g440), GrowFromCenter(den_br), FadeIn(d_lab),
                  f2[0][9:].animate.set_color(BLUE_C), run_time=0.9)
        self.measure = VGroup(g640, g500, g440, num_br, den_br, n_lab, d_lab)
        self.f = [f1, f2]
        self.end()

        # --- s06 答案（沿用試片 S4） ---
        self.begin("s06")
        f3 = M(r"=\frac{140}{200}", 56).next_to(f2, DOWN, buff=0.35).align_to(f2, LEFT)
        f3[0][1:4].set_color(PINK_C)
        f3[0][5:].set_color(BLUE_C)
        self.play(Write(f3), run_time=1.0)
        ans = M(r"D_r=70\%", 60, YELLOW_C).scale(0.9).next_to(f3, RIGHT, buff=0.6)
        box = SurroundingRectangle(ans, color=YELLOW_C, buff=0.2, stroke_width=4)
        self.play(Write(ans), run_time=0.8)
        self.play(Create(box), run_time=0.6)
        self.f += [f3]
        self.ans = VGroup(ans, box)
        self.top_grp = top_grp
        self.end()

    # ===== c2 陷阱一 =====
    def c2(self):
        tops, w = self.tops, self.w
        self.begin("s07")
        self.play(FadeOut(VGroup(*self.f, self.measure, self.void_lab, self.top_grp)),
                  self.ans.animate.scale(0.8).to_corner(UR, buff=0.55), run_time=0.8)
        b640, b440 = self.bars[0], self.bars[2]
        loose = VGroup(T("最疏鬆", 28, BLUE_C), M(r"D_r=0\%", 36, BLUE_C)).arrange(DOWN, buff=0.1)
        dense = VGroup(T("最緊密", 28, PINK_C), M(r"D_r=100\%", 36, PINK_C)).arrange(DOWN, buff=0.1)
        loose.next_to(b640[2], UP, buff=0.15)
        dense.next_to(b440[2], UP, buff=0.15)
        self.play(Indicate(b640[4], color=BLUE_C, scale_factor=1.3), run_time=0.7)
        self.play(Write(loose), run_time=0.9)
        self.play(Indicate(b440[4], color=PINK_C, scale_factor=1.3), run_time=0.7)
        self.play(Write(dense), run_time=0.9)
        big = T("體積最大 ＝ 最疏鬆", 34, YELLOW_C).move_to([3.3, 1.9, 0])
        self.play(Write(big), run_time=1.0)
        self.end_labels = VGroup(loose, dense)
        self.end()

        self.begin("s08")
        wrong = M(r"\frac{500-440}{640-440}=\frac{60}{200}=30\%", 50, RED_C).move_to([3.3, 0.6, 0])
        self.play(Write(wrong), run_time=1.6)
        cr = xmark(wrong)
        self.play(Create(cr), run_time=0.5)
        # 數線 440 —— 500 —— 640
        y = -1.3
        X = lambda v: 0.6 + (v - 440) / 200 * 5.4
        axis = Line([X(440), y, 0], [X(640), y, 0], color=CHALK, stroke_width=3)
        ticks = VGroup(*[Line([X(v), y - 0.12, 0], [X(v), y + 0.12, 0], color=CHALK, stroke_width=3)
                         for v in (440, 500, 640)])
        tl = VGroup(*[M(str(v), 32).next_to([X(v), y, 0], DOWN, buff=0.2) for v in (440, 500, 640)])
        ends = VGroup(T("緊", 30, PINK_C).next_to([X(440), y, 0], LEFT, buff=0.25),
                      T("鬆", 30, BLUE_C).next_to([X(640), y, 0], RIGHT, buff=0.25))
        self.play(Create(axis), Create(ticks), Write(tl), Write(ends), run_time=1.2)
        br1 = BraceBetweenPoints([X(440), y + 0.2, 0], [X(500), y + 0.2, 0], UP, color=PINK_C)
        br2 = BraceBetweenPoints([X(500), y + 0.2, 0], [X(640), y + 0.2, 0], UP, color=BLUE_C)
        l1 = M("60", 30, PINK_C).next_to(br1, UP, buff=0.08)
        l2 = M("140", 30, BLUE_C).next_to(br2, UP, buff=0.08)
        self.play(GrowFromCenter(br1), Write(l1), run_time=0.7)
        self.play(GrowFromCenter(br2), Write(l2), run_time=0.7)
        concl = row(T("現地靠近緊密端", 30, YELLOW_C), M(r"\Rightarrow D_r>50\%", 38, YELLOW_C))
        concl.next_to(tl, DOWN, buff=0.35).set_x(X(540))
        self.play(Write(concl), run_time=1.2)
        self.trap = VGroup(big, wrong, cr, axis, ticks, tl, ends, br1, br2, l1, l2, concl)
        self.end()

        self.begin("s09")
        self.play(FadeOut(self.trap), FadeOut(self.end_labels), run_time=0.6)
        xr = -1.05
        yl, yd = tops[640], tops[440]
        ruler = Line([xr, yl, 0], [xr, yd, 0], color=CHALK, stroke_width=4)
        tk = VGroup()
        for i in range(11):
            yy = yl + (yd - yl) * i / 10
            L = 0.22 if i % 5 == 0 else 0.12
            tk.add(Line([xr, yy, 0], [xr + L, yy, 0], color=CHALK, stroke_width=3))
        tlab = VGroup(M(r"0\%", 30, BLUE_C).next_to([xr + 0.25, yl, 0], RIGHT, buff=0.1),
                      M(r"100\%", 30, PINK_C).next_to([xr + 0.25, yd, 0], RIGHT, buff=0.1))
        guides = VGroup(
            DashedLine([-5.6 + w / 2, yl, 0], [xr, yl, 0], color=BLUE_C, stroke_width=2, dash_length=0.08),
            DashedLine([-2.2 + w / 2, yd, 0], [xr, yd, 0], color=PINK_C, stroke_width=2, dash_length=0.08))
        self.play(Create(guides), run_time=0.7)
        self.play(Create(ruler), Create(tk), Write(tlab), run_time=1.2)
        y70 = tops[500]
        g500 = DashedLine([-3.9 + w / 2, y70, 0], [xr, y70, 0], color=YELLOW_C, stroke_width=3,
                          dash_length=0.08)
        arr = Arrow([xr + 1.6, y70, 0], [xr + 0.05, y70, 0], buff=0, color=YELLOW_C, stroke_width=5)
        l70 = M(r"70\%", 40, YELLOW_C).next_to(arr, RIGHT, buff=0.1)
        self.play(Create(g500), GrowArrow(arr), Write(l70), run_time=1.1)
        self.play(Indicate(self.ans, color=YELLOW_C), run_time=0.8)
        self.end()

    # ===== c3 方法二 =====
    def c3(self):
        self.mini = VGroup(self.bars, self.dash, self.vs_lab).copy()
        self.begin("s10")
        self.clear_board()
        given = VGroup(M(r"W=900\,\mathrm{g}", 40), M(r"W_s=850\,\mathrm{g}", 40),
                       M(r"V=500\,\mathrm{ml}", 40), M(r"S=27\%", 40))
        given.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_corner(UL, buff=0.5).shift(DOWN * 1.35)
        gl = T("已知", 28, YELLOW_C).next_to(given, UP, buff=0.25).align_to(given, LEFT)
        self.play(Write(gl), run_time=0.4)
        for g in given:
            self.play(Write(g), run_time=0.6)
        self.play(Indicate(VGroup(given[0], given[3]), color=YELLOW_C), run_time=0.9)
        self.given = VGroup(gl, given)
        self.end()

        # 三相柱（右側）
        k2, by, cx, cw = 0.0095, -3.1, 5.6, 1.5
        hs, hw, ha = 314.8 * k2, 50 * k2, 135.2 * k2
        soil = Rectangle(width=cw, height=hs, stroke_color=CHALK, stroke_width=3,
                         fill_color=SOIL_C, fill_opacity=0.4).move_to([cx, by + hs / 2, 0])
        water = Rectangle(width=cw, height=hw, stroke_color=CHALK, stroke_width=3,
                          fill_color=BLUE_C, fill_opacity=0.45).next_to(soil, UP, buff=0)
        air = Rectangle(width=cw, height=ha, stroke_color=CHALK, stroke_width=3,
                        fill_opacity=0).next_to(water, UP, buff=0)
        ls = T("土粒", 26).move_to(soil)
        lw = row(T("水", 24), M(r"50", 28), buff=0.12).move_to(water)
        la = row(T("空氣", 24), M(r"135.2", 28), buff=0.12).move_to(air)
        xL = 0.2  # 計算欄左緣

        self.begin("s11")
        l1 = M(r"W_w=W-W_s=900-850=50\,\mathrm{g}", 38).move_to([0, 2.3, 0]).align_to([-4.1, 0, 0], LEFT)
        self.play(Write(l1), run_time=1.8)
        l2 = M(r"V_w=\frac{W_w}{\gamma_w}=\frac{50}{1}=50\,\mathrm{ml}", 38)
        l2.next_to(l1, DOWN, buff=0.35).align_to(l1, LEFT)
        self.play(Write(l2), run_time=1.6)
        self.play(GrowFromEdge(soil, DOWN), Write(ls), run_time=0.8)
        self.play(GrowFromEdge(water, DOWN), Write(lw), run_time=0.7)
        self.end()

        self.begin("s12")
        l3 = M(r"V_v=\frac{V_w}{S}=\frac{50}{0.27}=185.19\,\mathrm{ml}", 38)
        l3.next_to(l2, DOWN, buff=0.35).align_to(l1, LEFT)
        self.play(Write(l3), run_time=1.8)
        self.play(Circumscribe(l3[0][3:7], color=YELLOW_C), run_time=0.8)
        self.play(GrowFromEdge(air, DOWN), Write(la), run_time=0.8)
        vbr = BraceBetweenPoints(air.get_corner(UL), water.get_corner(DL), LEFT, color=YELLOW_C)
        vlab = M(r"V_v=185.19", 30, YELLOW_C).next_to(vbr, LEFT, buff=0.1)
        self.play(GrowFromCenter(vbr), Write(vlab), run_time=0.8)
        self.end()

        self.begin("s13")
        l4 = M(r"V_v=V_w\times S=50\times0.27=13.5<V_w", 38, RED_C)
        l4.next_to(l3, DOWN, buff=0.35).align_to(l1, LEFT)
        self.play(Write(l4), run_time=1.8)
        c4 = xmark(l4)
        self.play(Create(c4), run_time=0.5)
        note = T("S＝27%：孔隙只有兩成七裝水 ⇒ 孔隙＞水", 28, YELLOW_C)
        note.next_to(l4, DOWN, buff=0.3).align_to(l1, LEFT)
        self.play(Write(note), run_time=1.4)
        self.end()

        self.begin("s14")
        self.play(FadeOut(VGroup(l4, c4, note, self.given)), run_time=0.6)
        l5 = M(r"V_s=V-V_v=500-185.19=314.8\,\mathrm{ml}", 38, YELLOW_C)
        l5.next_to(l3, DOWN, buff=0.35).align_to(l1, LEFT)
        self.play(Write(l5), run_time=1.8)
        self.play(soil.animate.set_stroke(YELLOW_C, 5), ls.animate.set_color(YELLOW_C), run_time=0.5)
        mini = self.mini.scale(0.5).to_corner(DL, buff=0.5).shift(UP * 0.35)
        self.play(FadeIn(mini), run_time=0.7)
        self.play(ShowPassingFlash(mini[1].copy().set_stroke(YELLOW_C, 8), time_width=0.6),
                  Indicate(mini[2], color=YELLOW_C), run_time=1.2)
        self.end()

        self.begin("s15")
        self.play(FadeOut(mini), run_time=0.5)
        l6 = M(r"G_s=\frac{W_s}{V_s\gamma_w}=\frac{850}{314.8}=2.70", 38)
        l6.next_to(l5, DOWN, buff=0.35).align_to(l1, LEFT)
        self.play(Write(l6), run_time=1.6)
        ok = T("✓ 砂土常見值", 30, GREEN_C).next_to(l6, RIGHT, buff=0.3)
        self.play(Write(ok), run_time=0.6)
        bad = row(T("若乘除顛倒：", 28, RED_C), M(r"G_s=\frac{850}{486.5}=1.75", 38, RED_C))
        bad.next_to(l6, DOWN, buff=0.3).align_to(l1, LEFT)
        self.play(Write(bad), run_time=1.4)
        self.play(Create(xmark(bad[1])), run_time=0.5)
        self.end()

        self.begin("s16")
        self.clear_board(keep=[l5, l6])
        vs = l5
        self.play(vs.animate.scale(0.9).move_to([0, 2.35, 0]).align_to([-6.3, 0, 0], LEFT),
                  l6.animate.scale(0.8).move_to([0, 2.35, 0]).align_to([6.6, 0, 0], RIGHT),
                  run_time=0.8)
        e0 = M(r"e=\frac{V_v}{V_s}=\frac{185.19}{314.8}=0.5882", 44)
        e0.move_to([0, 1.2, 0]).align_to([-6.3, 0, 0], LEFT)
        self.play(Write(e0), run_time=1.8)
        self.end()

        self.begin("s17")
        e1 = M(r"e_{max}=\frac{V_{max}-V_s}{V_s}=\frac{640-314.8}{314.8}=1.0329", 44)
        e2 = M(r"e_{min}=\frac{V_{min}-V_s}{V_s}=\frac{440-314.8}{314.8}=0.3976", 44)
        e1.next_to(e0, DOWN, buff=0.35).align_to(e0, LEFT)
        e2.next_to(e1, DOWN, buff=0.35).align_to(e0, LEFT)
        self.play(Write(e1), run_time=2.2)
        self.play(Write(e2), run_time=2.2)
        self.end()

        self.begin("s18")
        dr = M(r"D_r=\frac{1.0329-0.5882}{1.0329-0.3976}=\frac{0.4447}{0.6353}=70\%", 46)
        dr.next_to(e2, DOWN, buff=0.45).align_to(e0, LEFT)
        self.play(Write(dr[0][:44]), run_time=2.4)
        dr[0][45:].set_color(YELLOW_C)
        self.play(Write(dr[0][44:]), run_time=0.7)
        self.play(Create(SurroundingRectangle(dr[0][45:], color=YELLOW_C, buff=0.08)), run_time=0.6)
        same = row(T("方法一", 32, YELLOW_C), M(r"=", 40, YELLOW_C), T("方法二", 32, YELLOW_C))
        same.next_to(dr, RIGHT, buff=0.5)
        self.play(Write(same), run_time=0.9)
        self.end()

    # ===== c4 乾單位重 =====
    def c4(self):
        self.begin("s19")
        self.clear_board()
        gd = M(r"\gamma_d=\frac{W_s}{V}\times9.81=\frac{850}{V}\times9.81", 40)
        gd.move_to([0, 2.35, 0]).align_to([-6.3, 0, 0], LEFT)
        self.play(Write(gd), run_time=1.8)
        rows = [("狀態", r"V\ (\mathrm{ml})", r"\gamma_d\ (\mathrm{kN/m^3})"),
                ("最疏鬆", "640", "13.03"), ("現地", "500", "16.68"), ("最緊密", "440", "18.95")]
        colx = [-5.4, -3.4, -1.1]
        cells = VGroup()
        for i, r in enumerate(rows):
            y = 1.35 - i * 0.62
            c = VGroup(T(r[0], 30, YELLOW_C if i == 0 else CHALK).move_to([colx[0], y, 0]),
                       M(r[1], 34, YELLOW_C if i == 0 else CHALK).move_to([colx[1], y, 0]),
                       M(r[2], 34, YELLOW_C if i == 0 else CHALK).move_to([colx[2], y, 0]))
            cells.add(c)
        hline = Line([-6.4, 1.05, 0], [0.2, 1.05, 0], color=CHALK, stroke_width=2)
        self.play(Write(cells[0]), Create(hline), run_time=0.9)
        for c in cells[1:]:
            self.play(Write(c), run_time=0.9)
        self.table = VGroup(cells, hline)
        self.end()

        self.begin("s20")
        pa = M(r"D_r=\frac{\gamma_d-\gamma_{d,min}}{\gamma_{d,max}-\gamma_{d,min}}", 38)
        pb = M(r"\times\frac{\gamma_{d,max}}{\gamma_d}", 38)
        fm = row(pa, pb, buff=0.12).move_to([0, 1.75, 0]).align_to([0.9, 0, 0], LEFT)
        self.play(Write(pa), run_time=1.6)
        self.play(Write(pb), run_time=0.9)
        pbox = SurroundingRectangle(pb, color=YELLOW_C, buff=0.1)
        plab = T("修正項", 26, YELLOW_C).next_to(pbox, UP, buff=0.1)
        self.play(Create(pbox), Write(plab), run_time=0.7)
        n1 = M(r"=\frac{16.68-13.03}{18.95-13.03}\times\frac{18.95}{16.68}", 36)
        n1.next_to(fm, DOWN, buff=0.25).align_to(pa[0][2], LEFT)
        n2 = M(r"=0.616\times1.136=0.70", 36)
        n2.next_to(n1, DOWN, buff=0.2).align_to(n1, LEFT)
        self.play(Write(n1), run_time=1.8)
        self.play(Write(n2), run_time=1.3)
        n2[0][-4:].set_color(YELLOW_C)
        self.end()

        self.begin("s21")
        miss = row(T("漏修正項", 30, RED_C), M(r"\Rightarrow 0.616=61.6\%", 38, RED_C))
        miss.next_to(n2, DOWN, buff=0.2).align_to(n1, LEFT)
        self.play(Write(miss), run_time=1.2)
        self.play(Create(xmark(miss)), run_time=0.5)
        # 兩支標尺：e 等距 vs γd 不等距
        x0, x1 = -4.2, 4.2
        def ruler(y, lab, marks, col):
            ax = Line([x0, y, 0], [x1, y, 0], color=CHALK, stroke_width=3)
            name = lab.next_to(ax, LEFT, buff=0.3)
            g = VGroup(ax, name)
            for f, top, bot, c in marks:
                x = x0 + f * (x1 - x0)
                g.add(Line([x, y - 0.14, 0], [x, y + 0.14, 0], color=c, stroke_width=4))
                g.add(M(top, 28, c).next_to([x, y, 0], UP, buff=0.18))
                g.add(M(bot, 26, CHALK).next_to([x, y, 0], DOWN, buff=0.18))
            return g
        r1 = ruler(-1.75, M(r"e", 36, YELLOW_C),
                   [(0, "1.033", r"0\%", BLUE_C), (0.7, "0.588", r"70\%", YELLOW_C), (1, "0.398", r"100\%", PINK_C)], None)
        f616 = (16.677 - 13.029) / (18.951 - 13.029)
        r2 = ruler(-2.85, M(r"\gamma_d", 36, YELLOW_C),
                   [(0, "13.03", r"0\%", BLUE_C), (f616, "16.68", r"70\%", YELLOW_C), (1, "18.95", r"100\%", PINK_C)], None)
        self.play(Create(r1), run_time=1.3)
        self.play(Create(r2), run_time=1.3)
        x70 = x0 + 0.7 * (x1 - x0)
        ghost = DashedLine([x70, -1.75, 0], [x70, -2.85, 0], color=YELLOW_C, stroke_width=2, dash_length=0.08)
        self.play(Create(ghost), run_time=0.6)
        tag1 = T("線性（等距）", 26, GREEN_C).next_to(r1[0], RIGHT, buff=0.2)
        tag2 = T("不線性", 26, RED_C).next_to(r2[0], RIGHT, buff=0.2)
        self.play(Write(tag1), Write(tag2), run_time=0.9)
        self.end()

    # ===== c5 總結 =====
    def c5(self):
        self.begin("s22")
        self.clear_board()
        pts = VGroup(
            row(T("①", 34, YELLOW_C), T("「此砂土」", 34), M(r"\Rightarrow V_s", 40), T("固定，直接用體積算", 34)),
            row(T("②", 34, YELLOW_C), T("體積最大＝最疏鬆", 34), M(r"(D_r=0\%)", 40), T("，別搞反", 34)),
            row(T("③", 34, YELLOW_C), M(r"V_v=V_w\,/\,S", 42), T("（除，不是乘）", 34)),
            row(T("④", 34, YELLOW_C), T("乾單位重公式別漏", 34), M(r"\gamma_{d,max}/\gamma_d", 42)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-0.3, 0.7, 0])
        for p in pts:
            self.play(Write(p), run_time=1.6)
            self.wait(0.8)
        ans = M(r"D_r=70\%", 72, YELLOW_C).next_to(pts, DOWN, buff=0.6)
        self.play(Write(ans), run_time=0.9)
        self.play(Create(SurroundingRectangle(ans, color=YELLOW_C, buff=0.22, stroke_width=5)), run_time=0.6)
        self.end()
