import pygame
import random
import noun # make this a pip package some day

pygame.init()

# Create a 15x15 grid, where each cell is 20x20 pixels
GRID_SIZE = 15
CELL_SIZE = 20
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize the snake and the food
snake = [(GRID_SIZE//2, GRID_SIZE//2)]
food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

# Initialize the direction of the snake
direction = 'RIGHT'

def draw_cell(pos, color):
    pygame.draw.rect(screen, color, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def game_over():
    pygame.quit()

while True:
    pygame.time.wait(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: direction = 'UP'
            if event.key == pygame.K_a: direction = 'LEFT'
            if event.key == pygame.K_s: direction = 'DOWN'
            if event.key == pygame.K_d: direction = 'RIGHT'

    # Move the snake
    if direction == 'UP': snake.insert(0, (snake[0][0], snake[0][1]-1))
    if direction == 'LEFT': snake.insert(0, (snake[0][0]-1, snake[0][1]))
    if direction == 'DOWN': snake.insert(0, (snake[0][0], snake[0][1]+1))
    if direction == 'RIGHT': snake.insert(0, (snake[0][0]+1, snake[0][1]))

    # Check if the snake is out of bounds or has eaten itself
    if (snake[0][0] < 0 or snake[0][0] >= GRID_SIZE or
        snake[0][1] < 0 or snake[0][1] >= GRID_SIZE or
        snake[0] in snake[1:]):
        game_over()

    # Check if the snake has eaten the food
    if snake[0] == food:
        food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    else:
        snake.pop()

    # Draw everything
    screen.fill((0, 0, 0))
    for cell in snake: draw_cell(cell, WHITE)
    draw_cell(food, RED)

    pygame.display.update()
