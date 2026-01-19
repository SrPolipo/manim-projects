from manim import *
from examples import *

class Testing_Vicsek(MovingCameraScene):
    def construct(self):
        thing = vicsek(num_points = 20000, colors = [BLUE,WHITE,BLUE,RED,RED], stroke_width = 3, noise = 0.02)
        self.add(thing)
        self.camera.frame.set(height = thing.height*1.4)
        self.wait()
        for _ in range(7):
            self.play(thing.animate.iterate())
            self.wait(0.3)
        self.wait(2)

class Testing_Barnsley(MovingCameraScene):
    def construct(self):
        thing = barnsley(num_points = 40000, colors = [GREEN], stroke_width = 2, noise = 0.06)
        self.add(thing)
        self.camera.frame.shift(3*UP).scale(1.4)
        self.wait()
        for i in range(20):
            self.play(thing.animate.iterate(), self.camera.frame.animate.shift(0.4/(i+1)*UP), run_time = 0.7, rate_func = rate_functions.linear)
        self.wait(2)