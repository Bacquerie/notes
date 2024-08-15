import math
import random

import numpy as np

import models


def update_trap_position(trap_position):
    new_x = trap_position[0]
    new_y = trap_position[1]
    return new_x, new_y


def angle(velocity_x, velocity_y):
    return math.degrees(math.atan2(-velocity_y, velocity_x)) - 90


def random_state(
    env: models.Env2D,
    min_v: int = -70,
    max_v: int = 70,
) -> np.ndarray:
    """
    Creates a new random state ``(position, velocity)`` with `env` limits.
    """
    x: int = random.randint(0, env.width)
    y: int = random.randint(0, env.height)
    vx: int = random.randint(min_v, max_v)
    vy: int = random.randint(min_v, max_v)
    while abs(vx) < 5.0:
        vx = random.randint(min_v, max_v)
    while abs(vy) < 5.0:
        vy = random.randint(min_v, max_v)
    return np.array([[x], [y], [vx], [vy]])


def create_mouse(
    id_,
    env: models.Env2D,
    dt: float,
    motion_noise: float,
) -> models.Mouse:
    """
    Creates a new mouse with an initial random state.
    """
    state: np.ndarray = random_state(env)
    return models.Mouse(id_, env, state, dt, motion_noise)
