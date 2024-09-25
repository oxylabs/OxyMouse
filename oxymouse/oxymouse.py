from oxymouse.algorithms.base import MouseMovement
from oxymouse.algorithms.bezier_mouse.bezier_mouse import BezierMouse
from oxymouse.algorithms.gaussian_mouse.gaussian_mouse import GaussianMouse
from oxymouse.algorithms.perlin_mouse.perlin_mouse import PerlinMouse


class OxyMouse:
    def __init__(self, algorithm: str) -> None:
        self.mouse: MouseMovement

        mouses = {
            "perlin": PerlinMouse(),
            "bezier": BezierMouse(),
            "gaussian": GaussianMouse()
        }

        self.mouse = mouses.get(algorithm)
        if not self.mouse:
            raise ValueError("Invalid algorithm")

    def generate_coordinates(
        self, from_x: int = 0, from_y: int = 0, to_x: int = 1000, to_y: int = 1000
    ) -> list[tuple[int, int]]:
        return self.mouse.generate_coordinates(from_x, from_y, to_x, to_y)

    def generate_random_coordinates(
        self, viewport_width: int = 1920, viewport_height: int = 1080
    ) -> list[tuple[int, int]]:
        return self.mouse.generate_random_coordinates(viewport_width, viewport_height)

    def generate_scroll_coordinates(self, start_y: int = 0, end_y: int = 1000) -> list[tuple[int, int]]:
        return self.mouse.generate_scroll_coordinates(start_y, end_y)
