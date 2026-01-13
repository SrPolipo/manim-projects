from manim import *

class Sierpisnki_Triangle(MovingCameraScene):
    def construct(self):
        v = {
            0:np.array([0,0,0]),
            1:np.array([1,0,0]),
            2:np.array([0.5, 0.5*np.sqrt(3),0])
        }
        F = {
            0: lambda x: 0.5*(x+v[0]),
            1: lambda x: 0.5*(x+v[1]),
            2: lambda x: 0.5*(x+v[2])
        }

        num_points = 8000
        limit = 20
        #I want to build a sample
        def random_walk(limit):
            #returns a random walk with size limit on the symbols 0,1,2
            return [np.random.randint(0,3) for _ in range(limit)]
        
        def _point(arr):
            #returns the location of the point
            position = v[arr[0]]
            for i in arr[1:]:
                position = F[i](position)
            return position, arr[-1]
        
        colors = [RED, GREEN, BLUE]
        
        random_bernoulli = [random_walk(limit) for _ in range(num_points)]

        random_points = np.array([_point(vec)[0] for vec in random_bernoulli])

        
        random_indices = np.array([_point(vec)[1] for vec in random_bernoulli])
        random_colors = np.array([color_to_rgba(colors[idx]) for idx in random_indices])

        points = PMobject(stroke_width = 2)
        points.add_points(points = random_points, rgbas=random_colors)
        self.add(points)
        self.camera.frame.move_to(points).set(width=points.height * 2)
        """
        for point in random_points:
            points.add(Point(point[0], color = colors[point[1]], stroke_width = 1))
        
        self.add(points)
        
        """

class animated_sierpinski_triangle(MovingCameraScene):
    def construct(self):
        v = {
            0:np.array([0,0,0]),
            1:np.array([1,0,0]),
            2:np.array([0.5, 0.5*np.sqrt(3),0])
        }
        F = {
            0: lambda x: 0.5*(x+v[0]),
            1: lambda x: 0.5*(x+v[1]),
            2: lambda x: 0.5*(x+v[2])
        }
        random_function = lambda x: F[np.random.randint(0,3)](x)

        num_points = 20000       

        points_array = np.array(
            [v[0] for _ in range(num_points//3)] + [v[1] for _ in range(num_points//3)] + [v[2] for _ in range(num_points//3)]
            )
        # Add small error/noise to the points
        noise_scale = 0.04  # Adjust this to control the amount of noise
        points_array = points_array + np.random.normal(0, noise_scale, points_array.shape)
        
        colors = [RED, GREEN, BLUE]
        colors_RGBA = [color_to_int_rgba(elem) for elem in colors]
        colors_array = np.array(
            [colors_RGBA[0] for _ in range(num_points//3)] + [colors_RGBA[1] for _ in range(num_points//3)] + [colors_RGBA[2] for _ in range(num_points//3)]
        )
        points = PMobject(stroke_width = 6)
        points.add_points(points = points_array, rgbas = colors_array)
        self.add(points)
        self.camera.frame.move_to(points).set(width=points.height * 2)
        self.wait(1)
        for _ in range(7):
            self.wait(0.3)
            self.play(points.animate.apply_function(random_function))
        self.wait(2)
        """
        for point in random_points:
            points.add(Point(point[0], color = colors[point[1]], stroke_width = 1))
        
        self.add(points)
        
        """