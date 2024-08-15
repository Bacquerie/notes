import sys
import uuid

import numpy as np
import pygame
from pygame import draw
from pygame import transform

import models
import util


np.set_printoptions(precision=3)

# Initialize Pygame.
pygame.init()
clock = pygame.time.Clock()


class Simulation:
    def __init__(self):
        # Graphics initialization.
        self.height: int = 800
        self.width: int = 1200
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rodent Control")

        self.mouse_sprite = pygame.image.load("resources/img/mouse.png")#.convert_alpha()
        self.robot_sprite = pygame.image.load("resources/img/robot.png")#.convert_alpha()

        # Graphical properties.
        self.background_color: tuple[int, int, int] = (255, 255, 255)
        self.frame_rate: int = 30
        self.range_color: tuple[int, int, int] = (240, 255, 250)
        self.sampling_rate: int = 1
        self.track_color: tuple[int, int, int] = (128, 192, 192)
        self.track_size: int = 1
        self.trap_color: tuple[int, int, int] = (255, 0, 0)

        # Mice and catcher properties.
        self.n_mice: int = 15
        self.dt: float = 0.2
        self.missteps: int = 10
        self.motion_noise: float = 1.0
        self.shooting_range: float = 550.0
        self.shooting_speed: float = 120.0
        self.steps_per_second: int = 5
        self.trap_radius: float = 10.0

        self.env: models.Env2D = models.Env2D(self.width, self.height)

    def run(self) -> None:
        # Mice initialization.
        mice: dict[any, models.Mouse] = self._init_mice()

        # Catcher initialization.
        initial_position: np.ndarray = np.array([[self.env.width // 2], [0]])
        catcher: models.MouseCatcher = models.MouseCatcher(
            initial=initial_position,
            ids=list(mice.keys()),
            dt=self.dt,
            missteps=self.missteps,
            misstep_margin=self.motion_noise,
            n_steps=int(self.frame_rate * self.steps_per_second),
            shooting_range=self.shooting_range,
            shooting_speed=self.shooting_speed,
            trap_radius=self.trap_radius,
        )

        # Main game loop.
        self.catcher_xy: list[int] = initial_position.flatten().tolist()
        self.robot_xy: list[int] = self.catcher_xy

        input()

        # Main simulation loop.
        while mice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._draw_static()

            # Logic.
            mouse_states: dict = {
                id_: {"position": mouse.move().x, "velocity": mouse.v}
                for id_, mouse in mice.items()
            }

            # Draw the mice.
            self._draw_mice(mouse_states)

            # Mouse ID empty if trapped.
            positions = {id_: state["position"] for id_, state in mouse_states.items()}
            if id_ := catcher.update(positions):
                del mice[id_]

            # Draw sub-sampled predicted tracks for the mouse planned to be caught.
            for pos in catcher.pred[::self.sampling_rate]:
                pygame.draw.circle(
                    self.screen,
                    self.track_color,
                    pos,
                    self.track_size,
                )

            # Update and draw the trap.
            if catcher.trap_x is not None:
                trap_position = util.update_trap_position(catcher.trap_x)
                pygame.draw.circle(
                    self.screen,
                    self.trap_color,
                    trap_position,
                    self.trap_radius)

            pygame.display.flip()
            clock.tick(self.frame_rate)

    # PRIVATE METHODS

    def _draw_mice(self, mouse_states: dict) -> None:
        for state in mouse_states.values():
            x, y = state["position"]
            velocity: np.ndarray = state["velocity"]
            self.draw_sprite(self.mouse_sprite, x, y, util.angle(*velocity))

    def __draw_range(self) -> None:
        """
        Draws the shooting range on screen.
        """
        s_range: float = self.shooting_range
        draw.circle(self.screen, self.range_color, self.catcher_xy, s_range)

    def _draw_robot(self) -> None:
        """
        Draws the robot sprite on screen.
        """
        x = self.catcher_xy[0]
        y = self.catcher_xy[1] + self.robot_sprite.get_rect().height / 2
        self.draw_sprite(self.robot_sprite, x, y, 0)

    def draw_sprite(self, image, x, y, angle):
        """
        Draws a sprite on screen.
        """
        rotated_image = transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=(x, y))
        self.screen.blit(rotated_image, new_rect)

    def _draw_static(self) -> None:
        """
        Draws the static elements on the screen.
        """
        self.screen.fill(self.background_color)
        self.__draw_range()
        self._draw_robot()

    def _init_mice(self) -> dict[uuid.UUID, models.Mouse]:
        """
        Creates n new random mice.
        """
        return {
            id_: util.create_mouse(id_, self.env, self.dt, self.motion_noise)
            for id_ in [uuid.uuid4() for _ in range(self.n_mice)]
        }


if __name__ == "__main__":
    while True:
        Simulation().run()
