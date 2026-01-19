from manim import *
import numpy as np
from collections.abc import Callable

class Chaosgame(PMobject):
    def __init__(
            self, 
            functions: list[Callable[[np.ndarray], np.ndarray]], 
            vertices: list[np.ndarray], 
            num_points: int = 20000, 
            colors: list[ManimColor] | None = None, 
            noise: float = 0.04, 
            transition_probabilities: dict[int, list[float]] | None = None, 
            **kwargs
            ) -> None:
        """
        A subclass of PMobject, for working with iterated function systems.

        :param functions: Set of functions to be used when describing the IFS
        :param vertices: Set of initial points to which apply the functions.
        :param num_points: The number of points used to describe the animation. Rendering uses a probabilistic approach.
        :param colors: The colors of the points centered at each vertex.
        :param noise: The set of points are placed according to a normal distribution with this noise, centered at each vertex. 
        :param transition_probabilities: The dictionary for the transition probabilities between function compositions, leave this empty if all transitions are allowed and equiprobable.
        :param kwargs: Keyword arguments to be passed to PMobject.
        """
        super().__init__(**kwargs)
        self.functions = functions
        self.vertices = vertices
        self.num_points = num_points
        self.noise = noise
        self.num_functions = len(functions)

        if colors:
            self.colors = [color_to_rgba(color) for color in colors]
        else:
            self.colors = None

        if transition_probabilities:
            self.transition_probabilities = transition_probabilities
        else:
            self.transition_probabilities = {i: 1/self.num_functions * np.ones(shape = self.num_functions) for i in range(self.num_functions)}
        
        self.function_indices = np.array(sum([self.num_points//len(self.vertices) * [i%len(self.functions)] for i,vertex in enumerate(self.vertices)],[]))
        _points, colors_array = self._generate_initial_points()

        self.add_points(_points, rgbas = colors_array)

    def _generate_initial_points(self) -> tuple[np.ndarray, np.ndarray | None]:
        points_array = np.array(
            sum([self.num_points//len(self.vertices) * [vertex] for vertex in self.vertices], []),
            dtype=float 
        )
        if self.noise:
            points_array += np.random.normal(0, self.noise, points_array.shape)
        
        if self.colors:
            num_colors = len(self.colors)
            colors_array = np.array(sum([self.num_points//len(self.vertices) * [self.colors[i%num_colors]] for i,color in enumerate(self.vertices)],[]))
            return points_array, colors_array
        return points_array, None

    def transition_function(self) -> np.ndarray:
        new_indices = np.zeros_like(self.function_indices)
        for idx in range(self.num_functions):
            mask = self.function_indices == idx
            new_indices[mask] = np.random.default_rng().choice(
                a = range(self.num_functions),
                p = self.transition_probabilities[idx],
                size=np.sum(mask)
            )
        return new_indices

    
    def iterate(self) -> "Chaosgame":
        self.function_indices = self.transition_function()
        new_points = np.zeros_like(self.points)
        for idx, function in enumerate(self.functions):
            mask = self.function_indices == idx
            new_points[mask] = function(self.points[mask])
        self.points = new_points
        return self



