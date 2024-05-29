from manim import *
import numpy as np
import math

class CircleArea(Scene):
    def construct(self):
        color_purple = "#947BD3"
        color_blue = "#5E4AE3"
        color_pink = "#F26CA7"
        radius = 3
        
        circle_path = ParametricFunction(
            lambda t: radius * np.array([np.cos(t), np.sin(t), 0]), t_range=np.array([0, 2 * PI])
        )
        circle_path.set_stroke(WHITE, width=2)
        
        initial_radius_line = Line(start=ORIGIN, end=[radius, 0, 0]).set_stroke(width=2)
        self.play(Create(initial_radius_line), run_time=2)
        self.wait()
        
        horizontal_top = Line(start=[0.5 * PI * radius, 1.5, 0], end=[-0.5 * PI * radius, 1.5, 0])
        horizontal_bottom = Line(start=[-0.5 * PI * radius, -1.5, 0], end=[0.5 * PI * radius, -1.5, 0])
        vertical_left = Line(start=[-0.5 * PI * radius, -1.5, 0], end=[-0.5 * PI * radius, 1.5, 0])
        vertical_right = Line(start=[0.5 * PI * radius, -1.5, 0], end=[0.5 * PI * radius, 1.5, 0])
        
        upper_semi_circle = ParametricFunction(
            lambda t: radius * np.array([np.cos(t), np.sin(t), 0]), t_range=np.array([0, PI])
        )
        upper_semi_circle.set_stroke(WHITE, width=2)
        
        lower_semi_circle = ParametricFunction(
            lambda t: radius * np.array([np.cos(t), np.sin(t), 0]), t_range=np.array([PI, 2 * PI])
        )
        lower_semi_circle.set_stroke(WHITE, width=2)
        
        vertical_radius = Line(start=ORIGIN, end=[0, radius, 0]).set_stroke(WHITE, width=2)
        
        top_brace = Brace(horizontal_top, UP)
        semi_circumference_label = MathTex(r"\pi r")
        semi_circumference_label.next_to(top_brace, UP)
        
        left_brace = Brace(vertical_left, LEFT)
        radius_label = MathTex(r"r")
        radius_label.next_to(left_brace, LEFT)
        
        def rotate_circle_line(mob):
            mob.become(Line(start=ORIGIN, end=circle_path.get_end()).set_stroke(width=2))
        
        initial_radius_line.add_updater(rotate_circle_line)
        self.play(Create(circle_path), run_time=2)
        initial_radius_line.remove_updater(rotate_circle_line)
        self.play(FadeOut(initial_radius_line))
        self.wait(2)
        
        for num_sections in [4, 8, 20, 50, 100, 200]:
            if num_sections > 4:
                circle_path.set_fill(color_purple, opacity=1)
                self.play(FadeIn(circle_path))
            if num_sections == 4:
                self.play(circle_path.animate.set_fill(color_purple, opacity=1))
                self.wait()
                circle_copy = circle_path.copy()
                circle_copy.set_fill(color_purple)
                final_group = VGroup(
                    MathTex("Area(", font_size=40),
                    circle_copy.scale(0.075),
                    MathTex(")"),
                    MathTex("="),
                    semi_circumference_label.copy(),
                    MathTex(r"\cdot "),
                    radius_label.copy(),
                    MathTex(r"\pi r^2")
                )
                final_group.arrange(RIGHT)
                final_group.to_edge(DOWN, buff=0.25)
                self.play(Write(final_group[0]), Write(final_group[2]))
                self.play(Transform(circle_path.copy(), final_group[1]), run_time=2)
                self.play(Write(final_group[3]), run_time=0.5)
                question_mark = MathTex("?")
                question_mark.next_to(final_group[3], RIGHT)
                self.play(Write(question_mark))
                self.wait()
                
            self.wait(0.5)
            sectors = [
                AnnularSector(inner_radius=0, outer_radius=radius, angle=2 * PI / num_sections, start_angle=2 * PI * i / num_sections, fill_opacity=1, stroke_width=0, color=color_purple) 
                for i in range(num_sections)
            ]
            if num_sections < 100:
                VGroup(*sectors).set_stroke(WHITE, width=0.75)
            else:
                VGroup(*sectors).set_stroke(WHITE, width=0.01)
            self.play(FadeIn(VGroup(*sectors)))
            top_sectors = []
            bottom_sectors = []
            animations = []
            for i in range(num_sections):
                temp_sector = sectors[i].copy()
                if i < math.floor(num_sections / 2):
                    temp_sector.rotate(-2 * PI * i / num_sections, about_point=[0, 0, 0])
                    temp_sector.rotate(PI / 2 - PI / num_sections, about_point=[0, 0, 0])
                    temp_sector.set_fill(color_pink, opacity=1)
                    top_sectors.append(temp_sector)
                    animations.append(sectors[i].animate.set_fill(color_pink, opacity=1))
                else:
                    temp_sector.rotate(-2 * PI * i / num_sections, about_point=[0, 0, 0])
                    temp_sector.rotate(3 * PI / 2 - PI / num_sections, about_point=[0, 0, 0])
                    bottom_sectors.append(temp_sector)
                    
            self.remove(circle_path)
            self.wait(0.5)
            self.play(*animations)
            top_group = VGroup(*top_sectors)
            top_group.arrange(RIGHT, buff=0)
            top_group.shift(0.5 * radius * UP)
            bottom_group = VGroup(*bottom_sectors)
            bottom_group.arrange(RIGHT, buff=0)
            bottom_group.shift(0.5 * radius * DOWN)
            self.play(
                ReplacementTransform(VGroup(*sectors[:math.floor(num_sections / 2)]), top_group),
                ReplacementTransform(VGroup(*sectors[math.floor(num_sections / 2):]), bottom_group),
                run_time=2
            )
            self.wait(0.5)
            self.play(
                top_group.animate.shift(0.5 * math.cos(PI / num_sections) * radius * DOWN + 0.5 * sectors[0].get_width() * RIGHT),
                bottom_group.animate.shift(0.5 * math.cos(PI / num_sections) * radius * UP),
                run_time=2
            )
            self.wait(0.5)
            self.play(
                top_group.animate.set_stroke(color_purple, width=0).set_fill(color_purple, opacity=1),
                bottom_group.animate.set_stroke(color_purple, width=0)
            )
            self.wait(3)
            if num_sections != 200:
                self.play(FadeOut(VGroup(top_group, bottom_group)))
                
        self.play(FadeOut(question_mark))
        self.play(FadeIn(VGroup(upper_semi_circle, lower_semi_circle, vertical_radius)))
        self.wait()
        self.play(
            upper_semi_circle.animate.shift(0.75 * UP),
            lower_semi_circle.animate.shift(0.75 * DOWN),
            vertical_radius.animate.shift(1.5 * DOWN),
            run_time=2
        )
        self.play(
            ReplacementTransform(upper_semi_circle, horizontal_top),
            ReplacementTransform(lower_semi_circle, horizontal_bottom),
            ReplacementTransform(vertical_radius.copy(), vertical_left),
            ReplacementTransform(vertical_radius, vertical_right),
            run_time=2
        )
        self.wait()
        self.play(GrowFromCenter(top_brace), Write(semi_circumference_label), run_time=2)
        self.wait(0.5)
        self.play(GrowFromCenter(left_brace), Write(radius_label), run_time=2)
        self.wait()
        self.play(TransformMatchingShapes(semi_circumference_label.copy(), final_group[4]), run_time=2)
        self.play(Write(final_group[5]), run_time=0.25)
        self.play(TransformMatchingShapes(radius_label.copy(), final_group[6]), run_time=2)
        self.wait()
        final_group[-1].move_to(final_group[4].get_center())
        final_group[-1].shift(0.1 * UP + 0.1 * RIGHT)
        self.play(TransformMatchingShapes(VGroup(*final_group[-4:-1]), final_group[-1]), run_time=1.5)
        self.wait(1)
        self.play(VGroup(*final_group[:-4], final_group[-1]).animate.next_to(horizontal_bottom, 2 * DOWN))
        self.wait()
        final_rect = SurroundingRectangle(VGroup(final_group[0], final_group[-1]), color=WHITE)
        self.play(Create(final_rect))
        self.wait(5)

if __name__ == "__main__":
    from manim import config
    config.background_color = WHITE
    scene = CircleArea()
    scene.render()
