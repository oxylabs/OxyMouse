import random
import time

from noise import pnoise2

from oxymouse.algorithms.base import MouseMovement


class PerlinMouse(MouseMovement):
    @staticmethod
    def generate_perlin_mouse_movements(
        duration: float = 1.0,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
        seed: int = random.randint(0, 100000),
    ) -> list[tuple[int, int]]:
        """
        Generate mouse movements using Perlin noise.

        :param duration: Duration of the movement in seconds
        :param octaves: Number of octaves for the noise
        :param persistence: Persistence for the noise
        :param lacunarity: Lacunarity for the noise
        :param seed: Seed for reproducible results
        """
        start_time = time.time()
        screen_width, screen_height = 1920, 1080

        coordinates = []

        while time.time() - start_time < duration:
            # Generate noise values
            t = (time.time() - start_time) / duration
            x_noise = pnoise2(t, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            y_noise = pnoise2(t, seed + 1, octaves=octaves, persistence=persistence, lacunarity=lacunarity)

            # Map noise to screen coordinates
            x = int((x_noise + 1) / 2 * screen_width)
            y = int((y_noise + 1) / 2 * screen_height)

            coordinates.append((x, y))

            time.sleep(0.01)
        return coordinates

    @staticmethod
    def generate_coordinates(
        from_x: int = 0, from_y: int = 0, to_x: int = 1000, to_y: int = 1000
    ) -> list[tuple[int, int]]:
        """
        Generate a list of coordinates from (from_x, from_y) to (to_x, to_y) using Perlin noise.
        """
        movements = PerlinMouse.generate_perlin_mouse_movements()

        # Scale and translate the movements to fit the desired start and end points
        x_scale = (to_x - from_x) / (max(m[0] for m in movements) - min(m[0] for m in movements))
        y_scale = (to_y - from_y) / (max(m[1] for m in movements) - min(m[1] for m in movements))

        scaled_movements = [
            (int(from_x + (m[0] - movements[0][0]) * x_scale), int(from_y + (m[1] - movements[0][1]) * y_scale))
            for m in movements
        ]

        return scaled_movements

    @staticmethod
    def generate_random_coordinates(viewport_width: int = 1920, viewport_height: int = 1080) -> list[tuple[int, int]]:
        """
        Generate random coordinates within the given viewport dimensions using Perlin noise.
        """

        movements = PerlinMouse.generate_perlin_mouse_movements()
        return movements

    @staticmethod
    def generate_scroll_coordinates(start_y: int = 0, end_y: int = 1000) -> list[tuple[int, int]]:
        """
        Generate a list of y-coordinates for scrolling from start_y to end_y using Perlin noise.
        """
        movements = PerlinMouse.generate_perlin_mouse_movements()

        y_coords = [int(start_y + (m[1] / 1080) * (end_y - start_y)) for m in movements]

        y_coords.append(end_y)
        x_coords = [0] * len(y_coords)
        return list(zip(x_coords, y_coords))
