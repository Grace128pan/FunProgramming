import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FONT_SIZE = CELL_SIZE // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sum to 10 Game")

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE)
big_font = pygame.font.SysFont(None, FONT_SIZE * 2)
instruction_font = pygame.font.SysFont(None, FONT_SIZE // 3)
button_font = pygame.font.SysFont(None, FONT_SIZE // 3)

# Game state
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 0  # 0 for player, 1 for computer
game_over = False
winner = None
input_active = False
current_input = ""
current_cell = (0, 0)
show_instructions = False

# Draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT), 2)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), 2)

# Draw numbers in the grid
def draw_numbers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is not None:
                color = BLUE if (row + col) % 2 == 0 else RED
                text = font.render(str(grid[row][col]), True, color)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))

# Check for a winning condition
def check_winner():
    global winner, game_over
    lines = []

    # Rows and columns
    for i in range(GRID_SIZE):
        lines.append(grid[i])  # Rows
        lines.append([grid[j][i] for j in range(GRID_SIZE)])  # Columns

    # Diagonals
    lines.append([grid[i][i] for i in range(GRID_SIZE)])
    lines.append([grid[i][GRID_SIZE - i - 1] for i in range(GRID_SIZE)])

    for line in lines:
        if None not in line and sum(line) == 10:
            winner = current_player + 1
            game_over = True
            return

# Draw instructions button
def draw_instructions_button():
    pygame.draw.rect(screen, GREEN, (10, SCREEN_HEIGHT - 60, 150, 50))
    text = button_font.render("Instructions", True, BLACK)
    screen.blit(text, (20, SCREEN_HEIGHT - 50))

# Show instructions window
def show_instructions_window():
    instructions = [
        "Sum to 10 Game",
        "1. Click on a cell to select it.",
        "2. Enter a number (0-9) to fill the cell.",
        "3. The computer will then place a random number.",
        "4. First to complete a row, column, or diagonal",
        "   with a sum of 10 wins!",
        "5. Click anywhere to close this window."
    ]
    instruction_screen = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
    instruction_screen.fill(WHITE)
    y_offset = 20
    for line in instructions:
        text = instruction_font.render(line, True, BLACK)
        instruction_screen.blit(text, (20, y_offset))
        y_offset += 30

    return instruction_screen

# Main game loop
def game_loop():
    global current_player, game_over, winner, input_active, current_input, current_cell, show_instructions

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if show_instructions:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_instructions = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 10 <= x <= 160 and SCREEN_HEIGHT - 60 <= y <= SCREEN_HEIGHT - 10:
                        show_instructions = True
                    elif current_player == 0 and not game_over:
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE

                        if grid[row][col] is None:
                            current_cell = (row, col)
                            input_active = True
                            current_input = ""

                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        if current_input.isdigit() and 0 <= int(current_input) <= 9:
                            grid[current_cell[0]][current_cell[1]] = int(current_input)
                            check_winner()
                            current_player = 1
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    elif event.unicode.isdigit() and len(current_input) < 1:
                        current_input += event.unicode

        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_instructions_button()

        if current_player == 1 and not game_over:
            empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] is None]
            if empty_cells:
                row, col = random.choice(empty_cells)
                grid[row][col] = random.randint(0, 9)
                check_winner()
                current_player = 0

        if input_active:
            text = font.render(current_input, True, BLACK)
            screen.blit(text, (current_cell[1] * CELL_SIZE + CELL_SIZE // 4, current_cell[0] * CELL_SIZE + CELL_SIZE // 4))

        if game_over:
            text = big_font.render(f"{'Player' if winner == 1 else 'Computer'} wins!", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 2))

        if show_instructions:
            instruction_screen = show_instructions_window()
            screen.blit(instruction_screen, (50, 50))

        pygame.display.flip()

game_loop()
