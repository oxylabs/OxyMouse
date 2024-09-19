import abc


class MouseMovement:
    @staticmethod
    @abc.abstractmethod
    def generate_coordinates(from_x: int, from_y: int, to_x: int, to_y: int) -> list[tuple[int, int]]:
        """
        Generate a list of coordinates from (from_x, from_y) to (to_x, to_y).
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def generate_random_coordinates(viewport_width: int, viewport_height: int) -> list[tuple[int, int]]:
        """
        Generate random coordinates within the given viewport dimensions.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def generate_scroll_coordinates(start_y: int, end_y: int) -> list[tuple[int, int]]:
        """
        Generate a list of y-coordinates for scrolling from start_y to end_y.
        """
        raise NotImplementedError
