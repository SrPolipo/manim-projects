import numpy as np
from matplotlib import pyplot as plt
from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22 
config.frame_width = 8.0   

class Testing(Scene):
    def construct(self):           
        N = 1000
        number = 100
        frequencies = np.linspace(start = 0, stop = 1,num = number, endpoint=True)
        x = np.arange(1,N+1)

        plane = NumberPlane(
            x_range = [0, N, N//10],
            x_length = config.frame_width*0.85,
            y_range = [-20,20,5],
            y_length = config.frame_height*0.7,
            ).add_coordinates().to_edge(DOWN)
        
        

        frequency = frequencies[0]
        f = lambda t: (frequency*t)%1
        mean = np.average(f(x))
        y = np.cumsum(f(x)-mean)
        points = [plane.c2p(a,b) for a,b in zip(x,y)]

        point_object = PMobject(stroke_width= 6, color = RED).add_points(points)
        
        frequency_tracker = ValueTracker(frequency)
        frequency_label = DecimalNumber(frequency).move_to(plane,UR).shift(1.5*LEFT)
        frequency_label.add_updater(
            lambda m: m.set_value(
                frequency_tracker.get_value()
            )
        )
        label_text = Text(f"Frequência:", font_size=24).next_to(frequency_label,LEFT)

        self.add(plane)
        self.add(point_object)
        self.add(label_text,frequency_label)
        anim = []
        
        for i in range(1,number):
            frequency = frequencies[i]

            f = lambda t: (frequency*t)%1   
            mean = np.average(f(x))
            y = np.cumsum(f(x)-mean)
            points = [plane.c2p(a,b) for a,b in zip(x,y)]
            
            temp_object = PMobject(stroke_width=6).add_points(points)
            temp_object.match_color(point_object)

            anim.append(AnimationGroup(
                frequency_tracker.animate.set_value(frequency),
                point_object.animate.become(temp_object)
            ))

        self.play(Succession(*anim), run_time = 30, rate_func = smoothstep)
  
        self.wait(2)