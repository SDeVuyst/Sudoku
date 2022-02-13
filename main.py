import math
import pygame
from time import perf_counter

# Constants
WIDTH = 1000
BACKGROUND_COLOR = (38, 38, 38)
CONTRAST_COLOR = (255, 255, 255)

# Main Sudoku grid (0 is considered empty)
GRID  = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def main():   
    
    # Setting up the basics in pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))  
    pygame.display.set_caption("Sudoku")            
    win.fill(BACKGROUND_COLOR)                      
    creategrid(win)                              
    

    # Key events
    while True:
        for event in pygame.event.get():

            # User want to solve 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('Solving...')
                    t1 = perf_counter()
                    solve()
                    t2 = perf_counter()
                    print(f"Solved in {round(t2-t1,3)} Seconds")
                    print(GRID)
                    creategrid(win)
            # User wants to insert number
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert_number(win, pos)

            # User wants to clear board
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Print current board before clearing
                    print(GRID)
                    # Clear board
                    for y in range(len(GRID)):
                        for x in range(len(GRID)):
                            GRID[y][x] = 0
                    # Refresh window
                    creategrid(win)

            # user wants to quit game
            if event.type == pygame.QUIT:
                print(GRID)
                pygame.quit()
                

# Lets user input values into the grid
def insert_number(win, pos):
    
    # Which square did user select
    x, y = get_square(pos[0], pos[1])
    
    # Wait for user to type in number
    while True:
        for event in pygame.event.get():
            # User wants to quit
            if event.type == pygame.QUIT:
                return

            # User gave input, display onto screen
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                # User can only input number from 1-9 and check if legal move
                if key.isnumeric() and valid(int(key), (y, x)):
                    # Insert input into grid
                    GRID[y][x] = int(key)
                    # Display number 
                    creategrid(win)
                    return



def display_number(win, x, y, number):
    font = pygame.font.SysFont('Comic Sans MS',  int(WIDTH/10))

    number = font.render(number, False, CONTRAST_COLOR)
    x_visual = x*(WIDTH/9) + WIDTH/36
    y_visual = y*(WIDTH/9) - WIDTH/72
    win.blit(number, (x_visual, y_visual))

    pygame.display.update()
    


# Get square in grid based on x and y coordinates
def get_square(x, y):
    spacing = WIDTH/9
    c = math.floor(x / spacing) 
    r = math.floor(y / spacing)
    return(c, r)



# Creates the visual sudoku grid
def creategrid(win):
    win.fill(BACKGROUND_COLOR)
    spacing = WIDTH/9
    
    # Create Grid
    for i in range(9):
        if (i == 2 or i == 5):
            # drawing vertical lines
            pygame.draw.line(win, CONTRAST_COLOR, (spacing+spacing*i, 0), (spacing+spacing*i, WIDTH), 4)
            # drawing horizontal lines
            pygame.draw.line(win, CONTRAST_COLOR, (0, spacing+spacing*i), (WIDTH, spacing+spacing*i), 4)
        # drawing vertical lines
        pygame.draw.line(win, CONTRAST_COLOR, (spacing+spacing*i, 0), (spacing+spacing*i, WIDTH))
        # drawing horizontal lines
        pygame.draw.line(win, CONTRAST_COLOR, (0, spacing+spacing*i), (WIDTH, spacing+spacing*i))
        
            
    # Fill grid with values in GRID 
    for y in range(9):
        for x in range(9):
            if GRID[y][x] != 0:
                display_number(win, x, y, str(GRID[y][x]))

    pygame.display.update()
   


# Adapted from https://www.youtube.com/watch?v=eqUwSA0xI-s&ab_channel=TechWithTim
def solve():
    find = find_empty()
    if not find:  # if find is None or False
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if valid(num, (row, col)):
            GRID[row][col] = num

            if solve():
                return True

            GRID[row][col] = 0

    return False

def valid(num, pos):
    # User want to remove number
    if num == 0:
        return True
    # Check row
    for i in range(len(GRID[0])):
        if GRID[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(GRID)):
        if GRID[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if GRID[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty():
    for i in range(len(GRID)):
        for j in range(len(GRID[0])):
            if GRID[i][j] == 0:
                return i, j  # row, column

    return None



if __name__ == '__main__':
    main()