# Narrative
# o3 mini promt: me a complex game of snake on python? should have levels difficulty settings and obstacles. Think of what could make the game more fun and add it in query. Ensure it runs in one go.

import pygame
import sys
import random

# Initialize pygame
pygame.init()

# --- Configuration Constants ---
WIDTH, HEIGHT = 1000, 600  # Screen dimensions (pixels)
CELL_SIZE = 20  # Size of each grid cell (pixels)
GRID_WIDTH = WIDTH // CELL_SIZE  # Number of cells horizontally
GRID_HEIGHT = HEIGHT // CELL_SIZE  # Number of cells vertically

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")
clock = pygame.time.Clock()

# Fonts for text display
font_small = pygame.font.SysFont("comicsansms", 25)
font_medium = pygame.font.SysFont("comicsansms", 35)
font_large = pygame.font.SysFont("comicsansms", 50)


# --- Helper Functions ---
def draw_text(surface, text, color, rect, font, center=True):
    """Helper function to draw text on a given surface."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = rect.center
    else:
        text_rect.topleft = rect.topleft
    surface.blit(text_surface, text_rect)


def random_position(exclude_positions):
    """
    Returns a random grid position (tuple) that is not in the exclude_positions list.
    """
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in exclude_positions:
            return pos


def show_start_screen():
    """
    Displays the start screen and waits for the player to select a difficulty.
    Returns a starting speed based on the difficulty:
      - 1: Easy (10 FPS)
      - 2: Medium (15 FPS)
      - 3: Hard (20 FPS)
    """
    while True:
        screen.fill(BLACK)
        title_text = font_large.render("Advanced Snake Game", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        instructions = [
            "Select Difficulty:",
            "1 - Easy",
            "2 - Medium",
            "3 - Hard",
            "Press the corresponding key; play with arrow keys"
        ]
        for i, line in enumerate(instructions):
            line_surface = font_medium.render(line, True, WHITE)
            screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, HEIGHT // 2 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10  # Easy speed
                elif event.key == pygame.K_2:
                    return 15  # Medium speed
                elif event.key == pygame.K_3:
                    return 20  # Hard speed


def game_over_screen(score):
    """
    Displays the Game Over screen with the final score.
    Allows the player to retry (press R) or quit (press Q).
    """
    while True:
        screen.fill(BLACK)
        over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        retry_text = font_small.render("Press R to Retry or Q to Quit", True, YELLOW)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# --- Main Game Function ---
def main():
    # Show start screen and get the base speed from difficulty selection
    base_speed = show_start_screen()

    # Initialize game state
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Snake starts at center
    direction = (0, 0)  # No movement until a key is pressed
    snake_length = 1
    score = 0
    level = 1
    food = random_position(snake)
    obstacles = []  # List to hold obstacle positions

    # Level settings: Every 5 foods eaten, the level increases
    level_up_threshold = 5
    foods_eaten = 0
    speed = base_speed  # Starting FPS (frames per second)

    # Main game loop
    while True:
        clock.tick(speed)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Change snake direction (prevent reversing directly)
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Don't move the snake until a direction is chosen
        if direction == (0, 0):
            continue

        # Calculate new head position
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # --- Collision Checks ---
        # Check for collision with walls (game over if the snake leaves the grid)
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            game_over_screen(score)
        # Check for collision with itself
        if new_head in snake:
            game_over_screen(score)
        # Check for collision with obstacles
        if new_head in obstacles:
            game_over_screen(score)

        # Insert new head (snake moves forward)
        snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == food:
            score += 10
            foods_eaten += 1
            snake_length += 1
            # Place new food ensuring it doesn't appear on the snake or obstacles
            occupied = snake + obstacles
            food = random_position(occupied)
        else:
            # Remove the tail segment if no food was eaten
            if len(snake) > snake_length:
                snake.pop()

        # Level Up: Increase level, speed, and add obstacles after threshold foods
        if foods_eaten >= level_up_threshold:
            level += 1
            foods_eaten = 0
            speed += 2  # Increase the game speed (FPS)
            # Add obstacles: add 3 new obstacles per level, avoiding snake and food positions
            for _ in range(3):
                occupied = snake + obstacles + [food]
                new_obstacle = random_position(occupied)
                obstacles.append(new_obstacle)

        # --- Drawing Section ---
        screen.fill(BLACK)

        # Draw food (as a red square)
        food_rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        # Draw obstacles (as purple squares)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, PURPLE, obs_rect)

        # Draw the snake (as green squares)
        for segment in snake:
            seg_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, seg_rect)

        # Display score and level
        score_surface = font_small.render(f"Score: {score}", True, WHITE)
        level_surface = font_small.render(f"Level: {level}", True, WHITE)
        screen.blit(score_surface, (10, 10))
        screen.blit(level_surface, (10, 40))

        pygame.display.flip()


# --- Run the Game ---
if __name__ == "__main__":
    main()