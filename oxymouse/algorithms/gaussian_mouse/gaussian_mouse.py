import random
from typing import Any

import numpy as np
from scipy.ndimage import gaussian_filter1d

from oxymouse.algorithms.base import MouseMovement


class GaussianMouse(MouseMovement):
    @staticmethod
    def random_walk(length: int, stddev: float) -> np.ndarray[Any, np.dtype[np.float64]]:
        return np.cumsum(np.random.normal(0, stddev, length))

    @staticmethod
    def gaussian_smooth(
        data: np.ndarray[Any, np.dtype[np.float64]], sigma: float
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        return gaussian_filter1d(data, sigma)

    @staticmethod
    def morph_distribution(
        data: np.ndarray[Any, np.dtype[np.float64]], target_mean: float, target_std: float
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        return (data - np.mean(data)) / np.std(data) * target_std + target_mean

    @staticmethod
    def bezier_curve(p0: float, p1: float, p2: float, t: float) -> float:
        return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

    @staticmethod
    def generate_gaussian_mouse_movements(  # pylint: disable=too-many-locals, too-many-positional-arguments
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float = 1.0,
        smoothness: float = 2.0,
        randomness: float = 1.0,
    ) -> list[tuple[int, int]]:
        """
        Generate mouse movements using Gaussian random walk and Bezier curves.

        :param start_x: Starting x-coordinate
        :param start_y: Starting y-coordinate
        :param end_x: Ending x-coordinate
        :param end_y: Ending y-coordinate
        :param duration: Duration of the movement in seconds
        :param smoothness: Controls the smoothness of the path (higher value = smoother)
        :param randomness: Controls the randomness of the path (higher value = more random)
        """
        num_points = int(duration * 60)

        stddev = randomness * 10
        random_x = GaussianMouse.random_walk(num_points, stddev)
        random_y = GaussianMouse.random_walk(num_points, stddev)

        smooth_x = GaussianMouse.gaussian_smooth(random_x, sigma=smoothness)
        smooth_y = GaussianMouse.gaussian_smooth(random_y, sigma=smoothness)

        human_mean_x, human_std_x = (end_x - start_x) / 2, (end_x - start_x) / 6
        human_mean_y, human_std_y = (end_y - start_y) / 2, (end_y - start_y) / 6
        morphed_x = GaussianMouse.morph_distribution(smooth_x, human_mean_x, human_std_x)
        morphed_y = GaussianMouse.morph_distribution(smooth_y, human_mean_y, human_std_y)

        control_x = random.uniform(start_x, end_x)
        control_y = random.uniform(start_y, end_y)

        t_values = np.linspace(0, 1, num_points)
        bezier_x = [GaussianMouse.bezier_curve(start_x, control_x, end_x, t) for t in t_values]
        bezier_y = [GaussianMouse.bezier_curve(start_y, control_y, end_y, t) for t in t_values]

        final_x = [int(bx + mx) for bx, mx in zip(bezier_x, morphed_x)]
        final_y = [int(by + my) for by, my in zip(bezier_y, morphed_y)]

        final_x[0], final_y[0] = start_x, start_y
        final_x[-1], final_y[-1] = end_x, end_y

        mouse_path = list(zip(final_x, final_y))
        return mouse_path

    @staticmethod
    def generate_coordinates(
        from_x: int = 0, from_y: int = 0, to_x: int = 1000, to_y: int = 1000
    ) -> list[tuple[int, int]]:
        """
        Generate a list of coordinates from (from_x, from_y) to (to_x, to_y) using Gaussian random walk.
        """
        return GaussianMouse.generate_gaussian_mouse_movements(from_x, from_y, to_x, to_y)

    @staticmethod
    def generate_random_coordinates(viewport_width: int = 1920, viewport_height: int = 1080) -> list[tuple[int, int]]:
        """
        Generate random coordinates within the given viewport dimensions using Gaussian random walk.
        """
        start_x, start_y = 0, 0
        end_x = random.randint(0, viewport_width)
        end_y = random.randint(0, viewport_height)
        movements = GaussianMouse.generate_gaussian_mouse_movements(start_x, start_y, end_x, end_y)
        return movements

    @staticmethod
    def generate_scroll_coordinates(start_y: int = 0, end_y: int = 1000) -> list[tuple[int, int]]:
        """
        Generate a list of y-coordinates for scrolling from start_y to end_y using Gaussian random walk.
        """
        movements = GaussianMouse.generate_gaussian_mouse_movements(0, start_y, 0, end_y)
        y_coords = [m[1] for m in movements]

        y_coords.append(end_y)
        x_coords = [0] * len(y_coords)

        return list(zip(x_coords, y_coords))
