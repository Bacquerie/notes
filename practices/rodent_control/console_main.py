import time

import numpy as np

import models


np.set_printoptions(precision=3)

# Simulation configuration.
_frame_rate: int = 10
_dt: float = 1.0 / _frame_rate
_motion_noise: float = 2 / _frame_rate

if __name__ == "__main__":
    env: models.Env2D = models.Env2D(500, 500)
    # Mice initialization.
    initial: np.ndarray = np.array([[479.0], [150.0], [3.0], [-6.0]])
    initial_b: np.ndarray = np.array([[100.0], [400.0], [2.0], [-5.0]])
    mice: dict[any, models.Mouse] = {
        "A": models.Mouse("A", env, initial, _dt, _motion_noise),
        "B": models.Mouse("B", env, initial_b, _dt, _motion_noise),
    }

    # Catcher initialization.
    initial: np.ndarray = np.array([[env.width // 2], [0]])
    catcher: models.MouseCatcher = models.MouseCatcher(
        initial=initial,
        ids=list(mice.keys()),
        dt=_dt,
        misstep_margin=4 / _frame_rate,
        n_steps=int(_frame_rate * 5),
        v_tol=0.2 / _frame_rate,
    )

    # Simulation.
    t: float = 0.0
    while mice:
        t += _dt
        mice_positions = {id_: mouse.move().x for id_, mouse in mice.items()}
        print(f"t={t:0.2f} ->", mice_positions)

        if id_ := catcher.update(mice_positions):
            print(f"===== Mouse {id_} caught at position", mice_positions[id_])
            del mice[id_]
            print("===== Remaining mice:", list(mice.keys()))
        time.sleep(0.1)
