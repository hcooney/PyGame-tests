# Thanks to N. Yergler. teaching-python-with-pygame
#!/usr/bin/python

# Squarify, 5x5 grid
# pyGame Demo
# Harry Cooney
# March 2018

# import necessary modules
import pygame
from pygame.locals import *

# declare our global variables for the game
player   = "R"   # track whose turn it is; R(ed) or B(lue)
grid = [ [ None, None, None, None, None ], \
         [ None, None, None, None, None ], \
         [ None, None, None, None, None ], \
         [ None, None, None, None, None ], \
         [ None, None, None, None, None ] ]
winner = None

# declare our support functions

def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board
    # ---------------------------------------------------------------
    # board : the initialized game board surface where the status will
    #         be drawn

    # gain access to global variables
    global player, winner

    # determine the status message
    if (winner is None):
        message = player + "'s turn"
    else:
        message = winner + " won!"
        
    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill ((250, 250, 250), (0, 500, 500, 25))
    board.blit(text, (10, 500))


def showBoard (squ, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # squ   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    squ.blit (board, (0, 0))
    pygame.display.flip()


def resetGame(squ):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    global  winner
    global  grid
    global  player
        
    # set up the background surface
    background = pygame.Surface (squ.get_size())
    background = background.convert()
    background.fill (pygame.color.Color('WHEAT'))
    #background.fill ((250, 250, 250))
    
    # draw the marker dots
    for xpos in range(50, 500, 100):
        for ypos in range(50, 500, 100):
            pygame.draw.circle (background, pygame.color.Color('BLACK'), (xpos, ypos), 4)
    
    winner = None
    player   = "R"   # track whose turn it is; R(ed) or B(lue)

    grid = [ [ None, None, None, None, None ], \
             [ None, None, None, None, None ], \
             [ None, None, None, None, None ], \
             [ None, None, None, None, None ], \
             [ None, None, None, None, None ] ]

    # return the board
    return background

   
def boardPos (mouseX, mouseY):
    # given a set of coordinates from the mouse, determine which board space
    # (row, column) the user clicked in.
    # ---------------------------------------------------------------
    # mouseX : the X coordinate the user clicked
    # mouseY : the Y coordinate the user clicked

    # determine the row the user clicked
    row = int (mouseY / 100)
    
    # determine the column the user clicked
    col = int(mouseX / 100)

    # return the tuple containg the row & column
    return (row, col)

  
def clickBoard(board):
    # determine where the user clicked and if the space is not already
    # occupied, draw the appropriate piece there (Red or Blue)
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, player
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos (mouseX, mouseY)

    # make sure no one's used this space
    if ((grid[row][col] == "R") or (grid[row][col] == "B")):
        # this space is in use
        return

    # draw a coloured dot
    drawMove (board, row, col, player)

    # toggle XO to the other player's move
    if (player == "R"):
        player = "B"
    else:
        player = "R"


def drawMove (board, boardRow, boardCol, player):
    # draw an Red or Blue dot on the board in boardRow, boardCol
    # ---------------------------------------------------------------
    # board     : the game board surface
    # boardRow,
    # boardCol  : the Row & Col in which to draw the piece (0 based)
    # Player    : Player colour R or B
    
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    # draw the appropriate piece
    if (player == 'R'): playerColor = pygame.color.Color('RED')
    if (player == 'B'): playerColor = pygame.color.Color('TURQUOISE')
    pygame.draw.circle (board, playerColor, (centerX, centerY), 6)

    # mark the space as used
    grid [boardRow][boardCol] = player


def drawLine(fromX, fromY, toX, toY, board):
    # draw a line between two dots on the board
    # ---------------------------------------------------------------
    # board     : the game board surface
    # fromX,
    # fromY     : the Row & Col of the starting dot (0 based)
    # toX, toY  : the Row & Col of the ending dot (0 based)
    
    # check for winning rows
    lineColor = pygame.color.Color('BLACK')
    pygame.draw.line (board, lineColor, (fromX*100 + 50, fromY*100 + 50), \
                                        (toX*100 +50,    toY*100 + 50), 2)


def findSquare(ax, ay, bx, by):
    # given 2 dots locate and return the coordinates of 2 other dots that could form a square 
    # ---------------------------------------------------------------
    # ax, ay    : the coordinates of dot A
    # bx, by    : the coordinates of dot B
    
    winner = None 
    cx, cy = 2, 0
    dx, dy = 2, 2

    if ((grid [ax][ay] == grid[bx][by] == grid[cx][cy] == grid[dx][dy]) and \
           (grid[ax][ay] is not None)):
            # this is a square

            winner = grid[ax][ay]

    # return the coordinates of the 2 dots that were identified
    return (winner, cx, cy, dx, dy)

def gameWon(board):
    # determine if anyone has won the game
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global grid, winner

    # Locate 2 spots with the same colour and the the other 2 corners to see if it is a square

    # Check square with corners a, b
    ax, ay = 0, 0
    bx, by = 0, 2
    (winner, cx, cy, dx, dy) = findSquare(ax, ay, bx, by)
    
    # If we have a winner draw the box
    if winner is not None:
            drawLine(ax, ay, bx, by, board)
            drawLine(bx, by, dx, dy, board)
            drawLine(dx, dy, cx, cy, board)
            drawLine(cx, cy, ax, ay, board)
    

# --------------------------------------------------------------------
# initialize pygame and our window
pygame.init()
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
squ = pygame.display.set_mode ((500, 525))
pygame.display.set_caption ('Squarify 5x5')

# create the game board
board = resetGame (squ)
showBoard (squ, board)

# main event loop
running = 1
while (running == 1):
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            running = 0
        elif winner is not None:
        # if we have a winner reset the board
            board = resetGame (squ)
        elif event.type is pygame.MOUSEBUTTONDOWN:
            # the user clicked; update the  board
            clickBoard(board)

        # check for a winner
        gameWon (board)

        # update the display
        showBoard (squ, board)