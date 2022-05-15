from manim import *

class Svt(Scene):
    def construct(self):
        formula = Tex("$s = vt$").scale(2)
        s = Tex("distance").shift(3*LEFT+1*DOWN)
        v = Tex("velocity").shift(1.5*DOWN)
        t = Tex("time").shift(3*RIGHT+1*DOWN)
        s_arrow = Arrow(start=s, end=formula)
        v_arrow = Arrow(start=v, end=0.5*RIGHT+0.2*DOWN)
        t_arrow = Arrow(start=t, end=formula)
        self.play(Write(formula))
        self.play(Write(s), Write(v), Write(t))
        self.play(Create(s_arrow), Create(v_arrow), Create(t_arrow))
        self.wait()


class ConstantSpeedWalk(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[-5, 10],
            include_numbers=True
        )
        alice = Dot(radius=DEFAULT_DOT_RADIUS*2, color=PINK).move_to(nl.n2p(0))
        alice_tex = Tex("Alice", color=PINK).next_to(alice, UP)
        nlgp = VGroup(nl, alice)

        speed = Tex("$v$ = \hspace{2em}units/second")
        speed_var = DecimalNumber(2).shift(LEFT)
        spgp = VGroup(speed_var, speed).next_to(nl, DOWN*3)

        self.add(nl, alice, spgp)
        self.play(Write(alice_tex))
        self.wait(0.5)
        self.play(FadeOut(alice_tex), run_time=0.5)

        alice_pos = ValueTracker(0.01)
        alice_line = Line(start=nl.n2p(0), end=nl.n2p(1), color=PINK)
        alice.add_updater(
            lambda m: m.move_to(nl.n2p(alice_pos.get_value()))
        )
        alice_line.add_updater(
            lambda m: m.put_start_and_end_on(
                nl.n2p(0), nl.n2p(alice_pos.get_value()))
        )

        def anim_walk(end):
            self.play(alice_pos.animate.set_value(end), run_time=0.75)
            t_tex = Tex("1 second").scale(0.8).next_to(nl.n2p(end - 1), UP)
            nlgp.add(t_tex)
            self.play(Write(t_tex), run_time=0.5)

        self.add(alice_line)
        anim_walk(2)
        anim_walk(4)
        anim_walk(6)
        self.wait()

        self.play(Uncreate(nlgp))
        self.play(spgp.animate.move_to(UP*2))
        self.wait()


class VelocityChangesOhno(Scene):
    def construct(self):
        speed = Tex("$v$ = \hspace{2em}units/second")
        speed_var = DecimalNumber(2).shift(LEFT)
        spgp = VGroup(speed, speed_var).shift(UP*2)
        self.add(spgp)
        self.wait(2)

        time = ValueTracker(0)
        speed_var.add_updater(
            lambda m: m.set_value(9.9*np.random.random()))

        def update_time():
            return time.animate.set_value(time.get_value() + 1)
        self.play(update_time())
        self.play(update_time())

        formula = Tex("$s = vt$").scale(2).shift(DOWN)
        self.play(update_time(), Write(formula))

        arrow = Arrow(
            start=speed.get_left()+0.1*DOWN,
            end=formula.get_center()+0.95*RIGHT+0.1*UP,
        )
        ques = Tex("?", color=RED, font_size=60).move_to(
            arrow, RIGHT).shift(LEFT+0.3*UP)
        self.play(update_time(), Write(arrow))
        self.play(update_time(), run_time=3)
        self.play(
            update_time(),
            Write(ques, lag_ratio=0.2, run_time=0.3),
            run_time=2,
        )
        self.play(update_time(), run_time=3)


class CalculusIsChange(Scene):
    def construct(self):
        tex = Tex("Calculus is fundamentally about studying changes")
        self.play(Write(tex), run_time=0.5)
        self.play(tex.animate.shift(2*UP))
        integ = Tex("$\int$").shift(2*LEFT).scale(2)
        deriv = Tex("$\\frac{\mathrm{d}}{\mathrm{d} x}$").shift(
            2*RIGHT).scale(2)
        self.play(Write(integ), run_time=0.5)
        self.wait(3)
        self.play(Write(deriv), run_time=0.5)
        self.wait(3)


class VelocityVsTime(Scene):
    def construct(self):
        tex = MathTex(r"""
            1~\mathrm{s} \to 2~\mathrm{m/s}\\
            2~\mathrm{s} \to 4~\mathrm{m/s}\\
            3~\mathrm{s} \to 6~\mathrm{m/s}\\
            \vdots
        """).shift(UP)
        fml = MathTex("2t = v", color=YELLOW).shift(DOWN)

        self.play(Write(tex))
        self.wait(2)
        self.play(Write(fml))
        self.wait(2)


class ElementaryApproach(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-2, 11],
            y_range=[-5, 100],
            tips=True,
        )
        ax.add_coordinates(range(-2, 11, 1), range(-5, 100, 10))
        t_alice = ValueTracker(0)
        alice = Dot(radius=DEFAULT_DOT_RADIUS, color=PINK)
        alice.add_updater(
            lambda m: m.move_to(ax.c2p(t_alice.get_value()))
        )
        self.add(ax, alice)

        # vdots = VGroup()
        dxdots = VGroup()
        all_points = VGroup()

        def move(pos, dt, group=False):
            t = t_alice.get_value()
            t_new = t + dt

            v = t_new * 2
            x_new = pos + v * dt
            # vdot = Dot(color=GREEN).move_to(ax.c2p(t_new, t_new * 2))
            dxdot = Dot(color=BLUE).move_to(ax.c2p(t_new, x_new))
            if group:
                t_alice.set_value(t_new)
                # vdots.add(vdot)
                dxdots.add(dxdot)
            else:
                # all_points.add(vdot, dxdot)
                all_points.add(dxdot)
                self.play(
                    t_alice.animate.set_value(t_new),
                    # Create(vdot),
                    Create(dxdot),
                    run_time=dt
                )
            return x_new

        def loop(cnt, target=10, group=False):
            prev_pos = 0
            for _ in range(cnt):
                prev_pos = move(prev_pos, target / cnt, group)
            if group:
                self.play(
                    t_alice.animate.set_value(target),
                    # Create(vdots),
                    Create(dxdots),
                )

        def reset():
            self.play(
                Uncreate(all_points),
                # Uncreate(vdots),
                Uncreate(dxdots),
                t_alice.animate.set_value(0),
                run_time=0.5
            )

        loop(5)
        reset()
        self.wait(2)
        loop(20, group=True)
        reset()
        self.wait(2)
        loop(100, group=True)
        self.wait(2)

        g_x_2 = ax.plot(lambda x: x ** 2, color=BLUE)
        # g_2x = ax.plot(lambda x: 2 * x, color=GREEN)

        self.play(
            # Uncreate(vdots),
            Uncreate(dxdots),
            Uncreate(alice),
            Write(g_x_2),
            # Write(g_2x),
        )
        self.wait(2)

        g_x_2_tex = MathTex(r"\int 2x~\mathrm{d}x = x^2", color=BLUE).move_to(
            g_x_2.get_right() + 4.3 * LEFT + UP)
        # g_2x_tex = MathTex("y = 2x", color=GREEN)
        self.play(Write(g_x_2_tex))
        self.wait(2)


class DerivativeSalvation(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-2, 11, 1],
            y_range=[-5, 100, 10],
            tips=True,
        )
        def func(x): return x ** 2
        ax.add_coordinates()
        g_x_2 = ax.plot(func, color=BLUE)
        g_x_2_tex = MathTex("\int 2x~\mathrm{d}x = x^2", color=BLUE).move_to(
            g_x_2.get_right() +4.3 * LEFT + UP)
        self.add(ax, g_x_2, g_x_2_tex)

        def plot_derivs(verts, subdivs, start=-2, end=10, erase_final=True):
            group = VGroup()
            lines = VGroup()

            delta = (end - start) / subdivs
            x = start
            for _ in range(subdivs):
                x += delta
                pos = ax.c2p(x, func(x))
                dx = 1e-06
                dpos = ax.c2p(x+dx, func(x+dx))
                deriv = (func(x + dx) - func(x)) / dx

                angle = angle_of_vector(dpos - pos)
                line = Line(color=GREEN, stroke_width=3) \
                    .scale(0.45) \
                    .set_angle(angle) \
                    .move_to(pos)

                corner = line.get_end()
                corner[1] = line.get_start()[1]

                nstart = corner.copy()
                nstart[1] = ax.c2p(0)[1]

                verts.add(Line(
                    start=nstart,
                    end=[nstart[0], ax.c2p(0, deriv)[1], 0],
                    color=GREEN,
                    stroke_width=3
                ))

                x_line = Line(
                    color=RED,
                    start=line.get_start(),
                    end=corner,
                    stroke_width=2,
                )
                z_line = Line(
                    color=BLUE,
                    start=corner,
                    end=line.get_end(),
                    stroke_width=2,
                )

                dot = Dot(color=GREEN).scale(0.7).move_to(pos)
                group.add(line, dot, x_line, z_line)
                lines.add(line)
            self.play(Create(group))
            self.wait()
            self.play(
                Uncreate(group-lines),
                Transform(lines, verts),
                run_time=0.5
            )
            self.wait()
            if erase_final:
                self.play(Uncreate(verts), run_time=0.5)
                print(verts)

        verts = VGroup()
        plot_derivs(verts, 5)
        plot_derivs(verts, 10)
        plot_derivs(verts, 20, erase_final=False)

        v_graph = ax.plot_derivative_graph(g_x_2)
        self.play(Write(v_graph))
        v_tex = MathTex(
            r"\frac{\mathrm{d}}{\mathrm{d}x}\int 2x~\mathrm{d}x = 2x",
            color=GREEN
        ).next_to(v_graph.get_end(), LEFT+0.5*UP)
        self.play(Write(v_tex))
        self.wait()

        second_ftc = MathTex(
            r"\frac{\mathrm{d}}{\mathrm{d}x}\int f(x)~\mathrm{d}x = f(x)",
        )
        self.play(
            FadeOut(ax, g_x_2, g_x_2_tex, v_graph, verts),
            Transform(v_tex, second_ftc)
        )
        self.wait(3)
