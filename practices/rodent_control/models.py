import dataclasses
import math

import numpy as np


class Env2D:
    """
    Defines a 2D environment where the mice and the catcher will be located.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def valid_x(self, x: float) -> bool:
        return 0 < x < self.width

    def valid_y(self, y: float) -> bool:
        return 0 < y < self.height


class KalmanFilter2D:
    """
    Implements the Kalman Filter for continuous 2D movement.
    """

    def __init__(
        self,
        initial: np.ndarray = None,
        dt: float = 1.0,
        u: tuple[float, float] = (0.0, 0.0),
        uncertainty: np.ndarray = None,
        z_var: tuple[float, float] = (1e-9, 1e-9),
    ) -> None:
        """
        :param initial:  Initial position measurement.
        :param dt: Time frame between each measurement.
        :param u: Position uncertainty.
        :param uncertainty: Observation uncertainty.
        :param z_var: Measurement variance.
        """
        # Guard conditions.
        if initial is None:
            initial = np.zeros((4, 1), np.float32)
        if uncertainty is None:
            uncertainty = np.array([1000.0, 1000.0, 1000.0, 1000.0])
        # Constructor "injection".
        self._x: np.ndarray = initial
        self._p: np.ndarray = np.array(
            [
                [uncertainty[0], 0.0, 0.0, 0.0],
                [0.0, uncertainty[1], 0.0, 0.0],
                [0.0, 0.0, uncertainty[2], 0.0],
                [0.0, 0.0, 0.0, uncertainty[3]],
            ]
        )
        self._f: np.ndarray = np.array(
            [
                [1.0, 0.0, dt, 0.0],
                [0.0, 1.0, 0.0, dt],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        self._h: np.ndarray = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])
        self._u: np.ndarray = np.array([[u[0]], [u[1]], [0.0], [0.0]])
        self._r: np.ndarray = np.array([[z_var[0], 0.0], [0.0, z_var[1]]])
        self._eye: np.ndarray = np.eye(4)

    # PROPERTIES

    @property
    def x(self) -> np.ndarray:
        """
        Current estimated position.
        """
        return self._x[:2].flatten().T

    @property
    def v(self) -> np.ndarray:
        """
        Current estimated velocity.
        """
        return self._x[2:].flatten().T

    # INSTANCE METHODS

    def measure(self, z: np.ndarray) -> "KalmanFilter2D":
        """
        Incorporates a new measurement into the model.
        """
        s = self._h @ self._p @ self._h.T + self._r
        k: np.ndarray = self._p @ self._h.T @ np.linalg.inv(s)
        e: np.ndarray = z.reshape(-1, 1) - self._h @ self._x
        # State update.
        self._x = self._x + k @ e
        self._p = (self._eye - k @ self._h) @ self._p
        return self

    def predict(self, n: int) -> list[np.ndarray]:
        """
        Predicts the next `n` positions according to the current model, without
        modifying it.
        """
        pred: list[np.ndarray] = []
        x: np.ndarray = self._x.copy()
        for _ in range(n):
            x = self._f @ x + self._u
            pred.append(self._h @ x)
        return pred

    def predict_update(self) -> "KalmanFilter2D":
        """
        Predicts the next state according to the current model, and updates it
        according to such prediction.
        """
        self._x = self._f @ self._x + self._u
        self._p = self._f @ self._p @ self._f.T
        return self

    def __repr__(self) -> str:
        return f"({self.x}, {self.v})"


class Mouse:
    """
    Defines a moving mouse.
    """

    def __init__(
        self,
        id_,
        env: Env2D,
        initial_state: np.ndarray,
        # Optional parameters.
        dt: float = 1.0,
        noise: float = 0.0,
    ) -> None:
        """
        :param id_: Unique identifier (uniqueness not enforced).
        :param env: Environment that the mouse will navigate.
        :param initial_state: Initial position and velocity.
        :param dt: Time frame between each movement.
        :param noise: Motion noise.
        """
        self.id = id_
        self._env: Env2D = env
        self._x: np.ndarray = initial_state
        self._u: float = noise
        self._f: np.ndarray = np.array(
            [
                [1.0, 0.0, dt, 0.0],
                [0.0, 1.0, 0.0, dt],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    # PROPERTIES

    @property
    def x(self) -> np.ndarray:
        """
        Current position.
        """
        return self._x[:2].flatten().T

    @property
    def v(self) -> np.ndarray:
        """
        Current velocity.
        """
        return self._x[2:].flatten().T

    # INSTANCE METHODS

    def move(self) -> "Mouse":
        """
        Produces noisy movement for the mouse.
        """
        u: np.ndarray = np.random.normal(self._u, self._u / 3, 2)
        self._x = self._f @ self._x + np.array([[u[0]], [u[1]], [0.0], [0.0]])
        return self._correct_state()

    # PRIVATE METHODS

    def _correct_state(self) -> "Mouse":
        """
        Corrects the position and velocity of the mouse according to the
        environment restrictions, like changing velocity when hitting a border
        or disallowing going outside its dimensions, etc.
        """
        x, y = self.x
        if not self._env.valid_x(x):
            self._x[2] *= -1
        if not self._env.valid_y(y):
            self._x[3] *= -1
        self._x[0] = min(max(x, 0), self._env.width)
        self._x[1] = min(max(y, 0), self._env.height)
        self._x[0] += self._u if (self._x[2] >= 0) else -self._u
        self._x[1] += self._u if (self._x[3] >= 0) else -self._u
        return self


@dataclasses.dataclass
class Plan:
    """
    Encapsulates the information necessary to catch a mouse.
    """

    wait_time: int
    hit_time: int
    trap: KalmanFilter2D
    mouse_id: any = None
    x_pred: list[tuple] = None


class MouseCatcher:
    """
    Defines an agent in charge of catching all mice in the given environment.
    """

    def __init__(
        self,
        initial: np.ndarray,
        ids: list,
        # Optional parameters.
        dt: float = 1.0,
        missteps: int = 5,
        misstep_margin: float = 0.5,
        n_steps: int = 10,
        shooting_range: float = 400.0,
        shooting_speed: float = 100.0,
        trap_radius: float = 10.0,
        v_tol: float = 1e-2,
    ) -> None:
        """
        :param initial: Initial position.
        :param ids: IDs of the mice needed to be caught.
        :param dt: Time frame between each update.
        :param missteps: Maximum number of consecutive mis-predictions allowed,
        before dropping the current predictor for a particular mouse.
        :param misstep_margin: Maximum difference between position and
        estimated position to consider a misstep.
        :param n_steps: Number of states it can predict in the future for
        each mouse.
        :param shooting_range: Maximum distance the mice traps can reach.
        :param shooting_speed: Constant shooting speed in units per second.
        :param trap_radius: Size of the mice traps.
        :param v_tol: Maximum velocity change to declare "certainty".
        """
        self._x: np.ndarray = initial
        self._dt: float = dt
        self._missteps: int = missteps
        self._misstep_margin: float = misstep_margin
        self._n_steps: int = n_steps
        self._s_range: float = shooting_range
        self._s_speed: float = shooting_speed
        self._radius: float = trap_radius
        self._v_tol: float = v_tol
        # Additional properties.
        self._data: dict = {}
        [self._reset_data(id_) for id_ in ids]
        # Currently active plan.
        self._plan: Plan | None = None

    @property
    def pred(self):
        return self._plan.x_pred if self._plan else []

    @property
    def trap_x(self) -> np.ndarray:
        if self._plan:
            return self._plan.trap.x

    # INSTANCE METHODS

    def update(self, positions: dict[any, np.ndarray]) -> any:
        """
        Update the estimations for all mice, given its measured positions, and
        acts accordingly in order to catch all mice (eventually).
        """
        for id_, z in positions.items():
            if mouse_id := self._update_plan(id_, z):
                return mouse_id
            # Updates the prediction for the current mouse.
            predictor: KalmanFilter2D = self._get_predictor(id_)
            # Evaluates missteps before updating estimate.
            self._update_missteps(id_, z)
            predictor.measure(z).predict_update()
            # Determines if able to track the mouse. Ignore if active plan.
            if self._is_trackable(id_, predictor) and not self._plan:
                if plan := self._formulate_plan(predictor):
                    plan.mouse_id = id_
                    self._plan = plan
            self._set_last_v(id_, predictor.v)

    # PRIVATE METHODS

    @staticmethod
    def _dist(x: np.ndarray, y: np.ndarray) -> float:
        """
        Euclidean distance between `x` and `y`.
        """
        return float(np.sqrt(np.sum((x - y) ** 2)))

    @staticmethod
    def _enumerate(x_pred: list) -> list[tuple]:
        """
        Adds the "number of steps ahead" to each prediction in `x_pred`.
        """
        return [(i + 1, x_i) for i, x_i in enumerate(x_pred)]

    def _formulate_plan(self, predictor: KalmanFilter2D) -> Plan:
        """
        Formulates a plan to catch the mouse followed by the given `predictor`.
        """
        # Removes infeasible future states.
        x_pred: list[tuple] = self._enumerate(predictor.predict(self._n_steps))
        original_x_pred: list[tuple] = x_pred[:]
        x_pred = self._remove_off_steps(self._remove_off_range(x_pred))
        # Creates action plans for the remaining states, if any.
        plans = filter(lambda plan: plan, [self._get_plan(x) for x in x_pred])
        plans = sorted(plans, key=lambda p_dist: p_dist[1])
        # Returns the best plan, if any.
        if not plans or not plans[0]:
            return None
        best_plan: Plan = plans[0][0]
        best_plan.x_pred = [x[1].flatten().T.tolist() for x in original_x_pred]
        return best_plan

    def _get_plan(self, x_pred: tuple) -> tuple[Plan, float] | None:
        """
        Computes the plan to catch the mouse tracked by `x_pred`, returning,
        also, how close would the mouse be to the trap's center.
        """
        hit_steps, t_ahead, x = x_pred
        speed: float = self._s_speed
        delta: np.ndarray = x - self._x
        theta: float = float(np.arctan2(delta[1], delta[0]))
        d_hit: float = speed * hit_steps * self._dt
        x_hit: np.ndarray = d_hit * np.cos(theta) + self._x[0]
        y_hit: np.ndarray = d_hit * np.sin(theta) + self._x[1]
        # Determines viability if mouse will probably be inside the trap.
        x_trap: np.ndarray = np.array([x_hit, y_hit])
        dist: float = self._dist(x, x_trap)
        if dist <= self._radius:
            v = np.array([[speed * np.cos(theta)], [speed * np.sin(theta)]])
            start = np.concatenate([self._x, v], axis=0)
            trap: KalmanFilter2D = KalmanFilter2D(start, self._dt)
            return Plan(t_ahead, hit_steps, trap), dist
        else:
            return None

    def _get_predictor(self, id_) -> KalmanFilter2D:
        """
        Gets the movement predictor for the mouse with the given `id`.
        """
        return self._data[id_]["predictor"]

    def _get_last_v(self, id_) -> np.ndarray:
        """
        Gets the last estimated velocity for the mouse with the given `id`.
        """
        return self._data[id_]["last_v"]

    def _hit_steps(self, x_pred: list[tuple]) -> list[int]:
        """
        Computes the number of time steps needed to hit each `x_pred`.
        """
        all_hit_steps: list[int] = []
        for i, x in x_pred:
            # Time to hit target, discretized by time steps.
            hit_time: float = self._dist(x, self._x) / self._s_speed
            hit_steps: int = int(round(hit_time / self._dt))
            all_hit_steps.append(hit_steps)
        return all_hit_steps

    def _is_trackable(self, id_, predictor: KalmanFilter2D) -> bool:
        """
        Determines whether the catcher has enough certainty about predicting
        a mouse's future movements.
        """
        last_v: np.ndarray = self._get_last_v(id_)
        current_v: np.ndarray = predictor.v
        # Certainty is measured by closeness in two consecutive velocities.
        return self._dist(last_v, current_v) <= self._v_tol

    def _reset_data(self, id_, initial: np.ndarray = None) -> None:
        """
        Resets the data cache for the given mouse estimator.
        """
        self._data[id_] = {
            "predictor": KalmanFilter2D(initial, self._dt),
            "last_v": np.full((2, 1), np.inf),
            "pred": [],
            "missteps": 0,
        }
        self._get_predictor(id_).predict_update()

    def _remove_off_range(self, x_pred: list[tuple]) -> list[tuple]:
        """
        Removes the `x_pred`s that are out from the shooting range.
        """
        return [
            (i, x)
            for i, x in x_pred
            if np.all(x >= 0) and self._dist(self._x, x) <= self._s_range
        ]

    def _remove_off_steps(self, x_pred: list[tuple]) -> list[tuple]:
        """
        Removes the `x_pred`s that are not reachable to trap in the time steps
        it takes for the trap to hit them.
        """
        steps: list[int] = self._hit_steps(x_pred)
        return [
            (steps[i], n_ahead - steps[i], x)
            for i, (n_ahead, x) in enumerate(x_pred)
            if steps[i] <= n_ahead
        ]

    def _set_last_v(self, id_, v: np.ndarray) -> None:
        """
        Sets the "last_v" for the mouse with the given `id`.
        """
        self._data[id_]["last_v"] = v

    def _update_missteps(self, id_, z: np.ndarray) -> None:
        """
        Performs the misstep logic to consider dropping a current predictor.
        """
        predictor: KalmanFilter2D = self._get_predictor(id_)
        if self._dist(predictor.x, z) > self._misstep_margin:
            self._data[id_]["missteps"] += 1
        else:
            self._data[id_]["missteps"] = 0
        if self._data[id_]["missteps"] >= self._missteps:
            initial = np.array([[z[0]], [z[1]], [0.0], [0.0]])
            self._reset_data(id_, initial)

    def _update_plan(self, id_, z: np.ndarray) -> any:
        """
        Executes the current plan, if any.
        """
        # No active plan for the mouse with the given `id_`.
        if not self._plan or id_ != self._plan.mouse_id:
            return
        # Does nothing while waiting to execute the plan.
        if self._plan.wait_time >= 0:
            self._plan.wait_time -= 1
        else:
            # Shoots the trap and updates its position.
            self._plan.hit_time -= 1
            self._plan.trap.predict_update()
            # By now, the trap should have caught the expected mouse.
            if self._plan.hit_time <= 0:
                plan: Plan = self._plan
                self._plan = None
                # Was the mouse actually trapped?
                if self._dist(z, plan.trap.x) <= self._radius:
                    return plan.mouse_id
