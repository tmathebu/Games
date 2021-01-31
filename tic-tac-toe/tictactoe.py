import pygame
import sys
import numpy as np

pygame.init()

#Constants
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE//4

CIRCLE_COLOR = (239,231,200)
CROSS_COLOR = (66,66,66)
RED = (255,0,255)
BACKGROUND_COLOR = (28,170,156)
LINE_COLOR = (23,145,135)

#creating the screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# setting title and color
pygame.display.set_caption('TIC & TAC & TOE')
screen.fill(BACKGROUND_COLOR)

# board
board = np.zeros((BOARD_ROWS,BOARD_COLS))

def drawlines():
    """
    DRaws The lines that's shows/demacates the Grid
    """
    #1 horizontal line
    pygame.draw.line(screen,LINE_COLOR,(0,SQUARE_SIZE),(HEIGHT,SQUARE_SIZE),LINE_WIDTH)
    #2 horizontal line
    pygame.draw.line(screen,LINE_COLOR,(0,SQUARE_SIZE*2),(HEIGHT,SQUARE_SIZE*2),LINE_WIDTH)
    
    #1 vertical line
    pygame.draw.line(screen,LINE_COLOR,(SQUARE_SIZE,0),(SQUARE_SIZE,HEIGHT),LINE_WIDTH)
    #2 vertical line 
    pygame.draw.line(screen,LINE_COLOR,(SQUARE_SIZE*2,0),(SQUARE_SIZE*2,HEIGHT),LINE_WIDTH)


def draw_figures():
    """Draws figures X and O when screen is clicked
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen,CIRCLE_COLOR,(int(col * SQUARE_SIZE + SQUARE_SIZE/2),int(row* SQUARE_SIZE +SQUARE_SIZE/2)),CIRCLE_RADIUS,CIRCLE_WIDTH)
            if board[row][col] == 2:
                pygame.draw.line(screen,CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),(col*SQUARE_SIZE+SQUARE_SIZE - SPACE,row * SQUARE_SIZE + SPACE),CROSS_WIDTH)
                pygame.draw.line(screen,CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),(col*SQUARE_SIZE + SQUARE_SIZE - SPACE,row * SQUARE_SIZE + SQUARE_SIZE - SPACE),CROSS_WIDTH)

def mark_square(row,col,player):
    """MArks A square in the board of arrays

    Args:
        row ([int]): row in grid
        col ([int]): column in grid
        player ([type]): either player 1 or player 2
    """
    board[row][col] = player


def available_square(row,col):
    """CHecks for available Square and returns true if square is available and false if not

    Args:
        row ([int]): row in grid
        col ([int]): column in grid

    Returns:
        [bool]: True if square is availabe and false if not
    """
    return board[row][col] == 0


def is_board_full():
    """CHecks if the grid is full,i.e to check for a drawn game

    Returns:
        [bool]: true if board is full and false if not
    """
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    """Checks which player won

    Args:
        player ([int]): The player to be checked
    """    
    #Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col,player)
            return True
    #Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row,player)
            return True
    #Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_ascending_diagonal(player)
        return True
    #Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_descending_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(col,player):
    """draws vertical line on column that matched 3 times

    Args:
        col ([int]): [the matched column]
        player ([int]): Player who won by matching correctly
    """
    pos_X = col * SQUARE_SIZE + SQUARE_SIZE/2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color,(pos_X,15),(pos_X,HEIGHT-15),15)

def draw_horizontal_winning_line(row,player):
    """draws horizontal line on row that matched 3 times

    Args:
        row ([int]): [the matched row]
        player ([int]): Player who won by matching correctly
    """
    pos_Y = row * SQUARE_SIZE + SQUARE_SIZE/2
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    
    pygame.draw.line(screen,color,(15,pos_Y),(WIDTH-15,pos_Y),15)

def draw_ascending_diagonal(player):
    """Draws ascending diagonal line

    Args:
        player ([int]): Player who won by matching correctly
    """
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen,color,(15,HEIGHT-15),(WIDTH-15,15),15)

def draw_descending_diagonal(player):
    """Draws descending diagonal line

    Args:
        player ([int]): Player who won by matching correctly
    """
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR
    
    pygame.draw.line(screen,color,(15,15),(WIDTH-15,HEIGHT-15),15)


def restart():
    """restarts the game to give a clean sheet
    """
    screen.fill(BACKGROUND_COLOR)
    drawlines()
    player = 1
    for col in range(BOARD_COLS):
        for row in range(BOARD_COLS):
            board[row][col] = 0


drawlines()

player = 1
game_over = False

#mainloop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouse_X = event.pos[0] #X
            mouse_Y = event.pos[1] #Y

            clicked_row = int(mouse_Y // SQUARE_SIZE)
            clicked_col = int(mouse_X // SQUARE_SIZE)

            if available_square( clicked_row, clicked_col ):
                if player == 1:
                    mark_square(clicked_row, clicked_col,1)
                    if check_win(player):
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col,2)
                    if check_win(player):
                        game_over = True
                    player = 1 
                
                draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False

    pygame.display.update()