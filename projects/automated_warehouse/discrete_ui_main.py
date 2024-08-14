import pygame
import sys
import random
import util

# Initialize Pygame
pygame.init()

# Define constants
CELL_SIZE = 40
WIDTH = 10
HEIGHT = 10
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE
FRAME_RATE = 5  # frames per second

# Load images
wall_image = pygame.image.load("resources/img/wall.png")
free_space_image = pygame.image.load("resources/img/wall.png")
package_image = pygame.image.load("resources/img/wall.png")
band_image = pygame.image.load("resources/img/wall.png")
robot_image = pygame.image.load("resources/img/wall.png")

# Scale images to fit the cell size
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
free_space_image = pygame.transform.scale(
    free_space_image,
    (CELL_SIZE, CELL_SIZE))
package_image = pygame.transform.scale(package_image, (CELL_SIZE, CELL_SIZE))
band_image = pygame.transform.scale(band_image, (CELL_SIZE, CELL_SIZE))
robot_image = pygame.transform.scale(robot_image, (CELL_SIZE, CELL_SIZE))


# Create a map with different cell types
def create_map():
    util.read_map("resources/mazes/warehouse_medium")
    return [[random.choice(['wall', 'free_space', 'package', 'band']) for _ in
             range(WIDTH)] for _ in range(HEIGHT)]


# Draw the map
def draw_map(screen, map, robot_position):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if map[y][x] == 'wall':
                screen.blit(wall_image, (x * CELL_SIZE, y * CELL_SIZE))
            #elif map[y][x] == 'free_space':
            #    screen.blit(free_space_image, (x * CELL_SIZE, y * CELL_SIZE))
            elif map[y][x] == 'package':
                screen.blit(package_image, (x * CELL_SIZE, y * CELL_SIZE))
            elif map[y][x] == 'band':
                screen.blit(band_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Draw the robot
    screen.blit(
        robot_image,
        (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))


# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Discrete Environment")

    clock = pygame.time.Clock()

    map = create_map()
    robot_position = [0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Randomly move the robot for demonstration purposes
        robot_position[0] = (robot_position[0] + random.choice(
            [-1, 0, 1])) % WIDTH
        robot_position[1] = (robot_position[1] + random.choice(
            [-1, 0, 1])) % HEIGHT

        # Draw everything
        screen.fill((255, 255, 255))
        draw_map(screen, map, robot_position)
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FRAME_RATE)


if __name__ == "__main__":
    main()
