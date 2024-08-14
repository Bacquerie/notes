import dataclasses
from typing import Callable

from problems import Action
from problems import Location2D


@dataclasses.dataclass(frozen=True)
class Package:
    """
    Abstract representation of a warehouse package that must be transported
    from an initial `location` (its rack) into a target conveyor belt
    (abstracted as another location in the map).
    """

    location: Location2D
    destination: Location2D


@dataclasses.dataclass
class Robot:
    """
    Represents an automated warehouse robot, used to help in the package
    picking process.
    """

    location: Location2D
    package: Package | None = None
    rest: Location2D | None = None

    def __post_init__(self) -> None:
        self._delivery_policy: dict[Location2D, Action] = {}
        self._pickup_policy: dict[Location2D, Action] = {}
        self._rest_policy: dict[Location2D, Action] = {}
        # Whether the robot is navigating to the package's location.
        self.is_picking_up: bool = False
        # Whether the robot is navigating to the package's destination.
        self.is_delivering: bool = False
        # Stop functions
        self._stop_delivery = lambda cur, new: not self._delivery_policy[new]
        self._stop_pickup = lambda cur, new: new == self.package.location
        self._stop_rest = lambda cur, new: cur == self.rest

    @property
    def is_free(self) -> bool:
        """
        Determines whether the robot is not currently transporting a package.
        """
        return self.package is None

    @property
    def is_going_to_rest(self) -> bool:
        """
        Determines whether the robot is currently going to a resting location.
        """
        return self.rest is not None

    def step(self) -> Package:
        """
        Performs a step in the navigation process to pick `package` from its
        rack and place it into its designed conveyor belt according to
        `pickup_policy` and `deliver_policy`.
        """
        if self.is_picking_up:
            return self.policy_step(self._pickup_policy, self._stop_pickup)
        elif self.is_delivering:
            return self.policy_step(self._delivery_policy, self._stop_delivery)
        elif self.is_going_to_rest:
            return self.policy_step(self.rest_policy, self._stop_rest)

    def policy_step(
        self,
        policy: dict[Location2D, Action],
        stop_condition: Callable[[Location2D, Location2D], bool],
    ) -> Package:
        """
        Follows `policy` from the start until `stop_condition` is met.
        """
        if action := policy[self.location]:
            new_location: Location2D = action.apply(self.location)
            # Stop before stepping on the conveyor belt.
            if stop_condition(self.location, new_location):
                if self.is_picking_up:
                    self.is_picking_up = False
                    self.is_delivering = True
                    return self.package
                elif self.is_delivering:
                    self.is_delivering = False
                    self.package = None
                elif self.is_going_to_rest:
                    self.rest = None
                    self.rest_policy = {}
            else:
                self.location = new_location
            return None

    def prepare(
        self,
        package: Package,
        pickup_policy: dict[Location2D, Action],
        delivery_policy: dict[Location2D, Action],
    ) -> None:
        self.package = package
        self.rest = None
        self._delivery_policy = delivery_policy
        self._pickup_policy = pickup_policy
        self.rest_policy = {}
        self.is_picking_up = True
        self.is_delivering = False

    def set_rest(
        self,
        rest: Location2D,
        rest_policy: dict[Location2D, Action],
    ) -> None:
        self.is_picking_up = False
        self.is_delivering = False
        self.rest = rest
        self.rest_policy = rest_policy
