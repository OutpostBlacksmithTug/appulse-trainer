import math
from typing import Tuple

def world_to_screen(
    wx: float, wy: float, wz: float,
    vx: float, vy: float, vz: float,
    yaw: float, pitch: float,
    fov: float, screen_w: int, screen_h: int,
) -> Tuple[float, float, bool]:
    """Very rough world-space -> screen-space projection."""
    dx, dy, dz = wx - vx, wy - vy, wz - vz
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    x = dx * cy - dy * sy
    y = dx * sy + dy * cy
    z = dz * cp - y * sp

    if z <= 0.01:
        return 0.0, 0.0, False

    f = (screen_h / 2.0) / math.tan(math.radians(fov / 2.0))
    sx = screen_w / 2.0 + (x * f) / z
    sy_screen = screen_h / 2.0 - (y * f) / z
    return sx, sy_screen, True