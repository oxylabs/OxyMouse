import random
from enum import Enum

import numpy as np
from noise import pnoise2

from oxymouse.algorithms.base import MouseMovement


class MouseState(Enum):
    ACCELERATING = 1
    PRECISE_MOVEMENT = 2
    DECELERATING = 3


class OxyMouse(MouseMovement):
    @staticmethod
    def _generate_movements(
        duration: float = 1.0,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
        seed: int | None = None,
        max_velocity: float = 10000.0,
        step_interval: float = 0.01,
    ) -> list[tuple[int, int]]:
        """
        Generate mouse movements with realistic acceleration patterns and corrective movements.
        """
        if seed is None:
            seed = random.randint(0, 100000)
        random.seed(seed)
        coordinates = []

        phases = [
            (MouseState.ACCELERATING, 0.2),  # Initial burst
            (MouseState.PRECISE_MOVEMENT, 0.3),  # Careful adjustments
            (MouseState.DECELERATING, 0.2),  # Slowdown
            (MouseState.PRECISE_MOVEMENT, 0.2),  # Final adjustments
            (MouseState.DECELERATING, 0.1),  # Final positioning
        ]

        last_x, last_y = 0, 0
        current_velocity = 0

        # Simulation time variables
        sim_time = 0.0
        last_time = 0.0
        phase_start_time = 0.0
        current_phase_idx = 0

        while sim_time < duration and current_phase_idx < len(phases):
            current_time = sim_time
            dt = current_time - last_time if sim_time != 0 else step_interval  # Use step_interval for first iteration
            phase_elapsed = current_time - phase_start_time

            current_state, phase_duration = phases[current_phase_idx]
            phase_total_time = phase_duration * duration
            phase_progress = phase_elapsed / phase_total_time if phase_total_time > 0 else 1.0

            if phase_progress >= 1.0:
                current_phase_idx += 1
                phase_start_time = current_time
                # Skip further processing if phase index changed
                last_time = current_time
                sim_time += step_interval
                continue

            t = current_time / duration
            x_noise = pnoise2(t * 3, seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            y_noise = pnoise2(t * 3, seed + 1, octaves=octaves, persistence=persistence, lacunarity=lacunarity)

            if current_state == MouseState.ACCELERATING:
                # Rapid acceleration with some overshooting
                target_velocity = max_velocity * (1 - np.exp(-phase_progress * 5))
                jitter = random.uniform(-0.1, 0.1) * target_velocity
                current_velocity = target_velocity + jitter

            elif current_state == MouseState.PRECISE_MOVEMENT:
                # Small corrective movements with reduced speed
                target_velocity = max_velocity * 0.2 * (np.sin(phase_progress * 4 * np.pi) * 0.5 + 0.5)
                current_velocity = target_velocity * random.uniform(0.8, 1.2)

            elif current_state == MouseState.DECELERATING:
                # Smooth deceleration with micro-adjustments
                target_velocity = max_velocity * np.exp(-phase_progress * 3)
                current_velocity = target_velocity * random.uniform(0.9, 1.1)

            max_movement = current_velocity * dt
            movement_angle = np.arctan2(y_noise, x_noise) + random.uniform(-0.1, 0.1)

            dx = np.cos(movement_angle) * max_movement
            dy = np.sin(movement_angle) * max_movement

            # Add micro-corrections (tremor)
            if current_state == MouseState.PRECISE_MOVEMENT:
                tremor_amplitude = 2.0
                dx += random.uniform(-tremor_amplitude, tremor_amplitude)
                dy += random.uniform(-tremor_amplitude, tremor_amplitude)

            new_x = int(last_x + dx)
            new_y = int(last_y + dy)

            coordinates.append((new_x, new_y))

            last_x, last_y = new_x, new_y
            last_time = current_time
            sim_time += step_interval

        return coordinates

    @staticmethod
    def generate_coordinates(
        from_x: int = 0, from_y: int = 0, to_x: int = 1000, to_y: int = 1000
    ) -> list[tuple[int, int]]:
        """
        Generate a list of coordinates from (from_x, from_y) to (to_x, to_y) using Perlin noise.
        """
        movements = OxyMouse._generate_movements()

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
        Generate random coordinates within the given viewport dimensions.
        """

        movements = OxyMouse._generate_movements()
        return movements

    @staticmethod
    def generate_scroll_coordinates(start_y: int = 0, end_y: int = 1000) -> list[tuple[int, int]]:
        """
        Generate a list of y-coordinates for scrolling from start_y to end_y.
        """
        movements = OxyMouse._generate_movements()

        y_coords = [int(start_y + (m[1] / 1080) * (end_y - start_y)) for m in movements]

        y_coords.append(end_y)
        x_coords = [0] * len(y_coords)
        return list(zip(x_coords, y_coords))
