import random
from typing import Any

import numpy as np
from scipy.special import comb

from oxymouse.algorithms.base import MouseMovement


class BezierMouse(MouseMovement):
    @staticmethod
    def bernstein_poly(
        i: int, n: int, t: np.ndarray[Any, np.dtype[np.float64]]
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        """
        The Bernstein polynomial of n, i as a function of t
        """
        return comb(n, i) * (t**i) * (1 - t) ** (n - i)

    @staticmethod
    def bezier_curve(points: list[tuple[int, int]], num_steps: int = 1000) -> list[tuple[int, int]]:
        """
        Given a set of control points, return the
        bezier curve defined by the control points.
        points should be a list of lists, or list of tuples
        such as [ [1,1], [2,3], [4,5], [3,5] ]
        """
        n_points = len(points)
        xpoints = np.array([p[0] for p in points])
        ypoints = np.array([p[1] for p in points])

        t = np.linspace(0.0, 1.0, num_steps)

        polynomial_array = np.array([BezierMouse.bernstein_poly(i, n_points - 1, t) for i in range(n_points)])

        xvals = np.dot(xpoints, polynomial_array)
        yvals = np.dot(ypoints, polynomial_array)

        return list(zip(xvals.astype(int), yvals.astype(int)))

    @staticmethod
    def generate_bezier_mouse_movements(  # pylint: disable=too-many-positional-arguments
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float = 1.0,
        complexity: int = 4,
        randomness: float = 1.0,
    ) -> list[tuple[int, int]]:
        """
        Generate mouse movements using Bézier curves.

        :param start_x: Starting x-coordinate
        :param start_y: Starting y-coordinate
        :param end_x: Ending x-coordinate
        :param end_y: Ending y-coordinate
        :param duration: Duration of the movement in seconds
        :param complexity: Number of control points (minimum 4, includes start and end points)
        :param randomness: Controls the randomness of control points (0.0 to 1.0)
        """
        complexity = max(4, complexity)  # Ensure at least 4 control points for a cubic Bézier curve

        control_points = [(start_x, start_y)]
        for i in range(complexity - 2):
            cx = random.randint(min(start_x, end_x), max(start_x, end_x))
            cy = random.randint(min(start_y, end_y), max(start_y, end_y))
            control_points.append((cx, cy))
        control_points.append((end_x, end_y))

        for i in range(1, len(control_points) - 1):
            control_points[i] = (
                int(control_points[i][0] + random.uniform(-randomness * 100, randomness * 100)),
                int(control_points[i][1] + random.uniform(-randomness * 100, randomness * 100)),
            )

        num_steps = int(duration * 60)  # Assuming 60 fps
        curve_points = BezierMouse.bezier_curve(control_points, num_steps)

        return curve_points

    @staticmethod
    def generate_coordinates(
        from_x: int = 0, from_y: int = 0, to_x: int = 1000, to_y: int = 1000
    ) -> list[tuple[int, int]]:
        """
        Generate a list of coordinates from (from_x, from_y) to (to_x, to_y) using Bézier curves.
        """
        return BezierMouse.generate_bezier_mouse_movements(from_x, from_y, to_x, to_y)

    @staticmethod
    def generate_random_coordinates(viewport_width: int = 1920, viewport_height: int = 1080) -> list[tuple[int, int]]:
        """
        Generate random coordinates within the given viewport dimensions using Bézier curves.
        """
        start_x, start_y = 0, 0
        end_x = random.randint(0, viewport_width)
        end_y = random.randint(0, viewport_height)
        movements = BezierMouse.generate_bezier_mouse_movements(start_x, start_y, end_x, end_y)
        return movements

    @staticmethod
    def generate_scroll_coordinates(start_y: int = 0, end_y: int = 1000) -> list[tuple[int, int]]:
        """
        Generate a list of y-coordinates for scrolling from start_y to end_y using Bézier curves.
        """
        movements = BezierMouse.generate_bezier_mouse_movements(0, start_y, 0, end_y)
        y_coords = [m[1] for m in movements]

        y_coords.append(end_y)
        x_coords = [0] * len(y_coords)

        return list(zip(x_coords, y_coords))
