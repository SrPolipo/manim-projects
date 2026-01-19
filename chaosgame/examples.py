from manim import *
from main import *

def sierpinski_triangle(
        **kwargs
    ) -> Chaosgame:
    """
    Creates an equilateral Sierpinski triangle centered at (0,0) with width 1.
    
    :param kwargs: Arguments to pass to Chaosgame, and by proxy to PMobject / Mobject.
    """

    sierpinski_vertices: list[np.ndarray] = [
    np.array([-0.5,-0.25*np.sqrt(3),0]),
    np.array([ 0.5,-0.25*np.sqrt(3),0]),
    np.array([   0, 0.25*np.sqrt(3),0])
    ]

    sierpsinski_functions: list[Callable[[np.ndarray], np.ndarray]] = [
        lambda x: 0.5*(x + sierpinski_vertices[0]),
        lambda x: 0.5*(x + sierpinski_vertices[1]),
        lambda x: 0.5*(x + sierpinski_vertices[2]),
    ]

    default_colors: list[ManimColor] = [GREEN, ORANGE,PURPLE]

    return Chaosgame(
        functions = sierpsinski_functions,
        vertices= sierpinski_vertices,
        colors = default_colors,
        **kwargs,
    )

def vicsek(
    **kwargs
    )-> Chaosgame:
    """
    Creates a two dimensional Vicsek fractal centered at (0,0) with width 1
    
    :param kwargs: Arguments to pass to Chaosgame, and by proxy to PMobject / Mobject.
    """
    vertices = [
        np.array([-1/3,0,0]),
        np.array([0,0,0]),
        np.array([1/3,0,0]),
        np.array([0,1/3,0]),
        np.array([0,-1/3,0]),
    ]

    function_generator = lambda vertex: lambda x: 1/3*x + vertex

    function_list = [
        function_generator(vertex) for vertex in vertices
    ]

    return Chaosgame(
        functions=function_list,
        vertices = vertices,
        **kwargs
        )

def barnsley(
        **kwargs
    )-> Chaosgame:
    """
    Creates a Barnsley fern
    
    :param kwargs: Arguments to pass to Chaosgame, and by proxy to PMobject / Mobject.
    """

    function_generator = lambda a,b,c,d,e,f: lambda x: x @ np.array([[a,c,0],[b,d,0],[0,0,0]]) + np.array([e,f,0])
    list_inputs = [
        (0,0,0,0.16,0,0),
        (0.85,0.04,-0.04,0.85,0,1.60),
        (0.20,-0.26,0.23,0.22,0,1.60),
        (-0.15,0.28,0.26,0.24,0,0.44)
    ]
    function_list = [
        function_generator(*g) for g in list_inputs
    ]
    probabilities = {
        i: [0.01,0.85,0.07,0.07] for i in range(4)
    }
    vertices = [
        np.array([0,0,0])
    ]
    return Chaosgame(function_list, vertices = vertices, transition_probabilities=probabilities, **kwargs)

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