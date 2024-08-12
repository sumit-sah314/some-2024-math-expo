from manim import *
import numpy as np

class NEqualVectors(Scene):
    def construct(self):
        # Set the number of vectors
        n = 9  # Change this value to the desired number of vectors

        tex_lines = [
            "If n equal vectors are lined up",
            "making an angle of $\\frac{2\pi}{n}$ to each",
            "other, then the resultant is 0.",
        ]
        
        # Create text objects
        text_group = VGroup(*[Tex(line) for line in tex_lines if line])
        text_group.arrange(DOWN, aligned_edge=LEFT)
        text_group.move_to(3*RIGHT + UP)  # Move text group to desired position

        formula = MathTex(r"\sum_{n=0}^{k-1}\vec{v}_k = 0").next_to(text_group, DOWN, buff=0.8)
        
        # Create the central object
        obj = Dot(ORIGIN, color=WHITE).scale(2)
        
        # Angle between the vectors
        angle = 2 * PI / n
        
        # Create and display the vectors
        vectors = [
            Arrow(
                start=obj.get_center(), 
                end=obj.get_center() + np.array([np.cos(k * angle), np.sin(k * angle), 0]) * 2.5, 
                buff=0, 
                color=BLUE,
                stroke_width=2
            ) for k in range(n)
        ]
        forces = VGroup(*vectors)

        # Create arcs and angle labels between vectors, but only show one at a time
        arc = Arc(
            radius=1, 
            start_angle=0, 
            angle=angle, 
            color=YELLOW,
            stroke_width=2
        ).move_arc_center_to(obj.get_center())
        angle_label = MathTex(r"\frac{2\pi}{n}").scale(0.6)
        angle_label.move_to(arc.point_from_proportion(0.5) + 0.5 * UP)

        # Group for initial arc and label
        arc_angle_group = VGroup(arc, angle_label)

        self.play(Create(obj))
        self.play(Create(forces))
        self.wait(1)

        # Animate each arc and label one by one
        for k in range(n):
            new_arc = Arc(
                radius=1,
                start_angle=k * angle,
                angle=angle,
                color=YELLOW,
                stroke_width=2
            ).move_arc_center_to(obj.get_center())

            new_angle_label = MathTex(r"\frac{2\pi}{n}").scale(0.6)
            new_angle_label.move_to(new_arc.point_from_proportion(0.5) + 0.5 * UP)

            new_arc_angle_group = VGroup(new_arc, new_angle_label)
        
            self.play(Transform(arc_angle_group, new_arc_angle_group))
        
        self.wait(1)
        self.play(FadeOut(arc_angle_group))
        self.play(VGroup(obj,forces).animate.shift(LEFT*3.5))
        self.wait(1)
        self.play(Write(text_group))
        self.wait(1)
        self.play(Write(formula))
        self.wait(1)

        # Shift the vectors to form a closed polygon
        closed_polygon_vectors = VGroup()
        for i in range(n):
            if i == 0:
                start = obj.get_center() + np.array([np.cos(i * angle), np.sin(i * angle), 0]) * 2.5
            else:
                start = end
            end = obj.get_center() + np.array([np.cos((i + 1) * angle), np.sin((i + 1) * angle), 0]) * 2.5
            closed_polygon_vectors.add(Arrow(start=start, end=end, buff=0, color=BLUE, stroke_width=2))

        self.play(Transform(forces, closed_polygon_vectors))
        self.wait(2)

        # Fade out text and elements
        self.play(FadeOut(text_group), FadeOut(formula))
        self.wait(1)
        self.play(FadeOut(forces), FadeOut(obj))
        self.wait(1)
