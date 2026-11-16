import pygame
import os
import pickle
from dotenv import load_dotenv
from enum import Enum
from word_tree import *

load_dotenv()

SCALE = 0.75

SCREEN_WIDTH = SCALE * 2160
SCREEN_HEIGHT = SCALE * 1215

DEBOUNCE_TIME = 200

FONT_PATH = os.getenv("FONT_PATH")
LETTER_FONT_SIZE = int(SCALE * 80)
SMALL_FONT_SIZE = int(SCALE * 20)

TILE_SIZE = SCALE * 72
TILE_COLOR = (160, 120, 80)
BG_COLOR = (55, 57, 58)
BOARD_COLOR = (168, 157, 149)
BOARD_SIZE = SCALE * 1080
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = SCALE * 25
PLAY_BUTTON_X = SCREEN_WIDTH - SCREEN_WIDTH//8
PLAY_BUTTON_Y = SCREEN_HEIGHT - SCREEN_HEIGHT//6
RESET_BUTTON_X = PLAY_BUTTON_X + TILE_SIZE + TILE_SIZE*.25
RESET_BUTTON_Y = PLAY_BUTTON_Y
SKIP_BUTTON_X = RESET_BUTTON_X + TILE_SIZE + TILE_SIZE*.25
SKIP_BUTTON_Y = PLAY_BUTTON_Y
DONE_BUTTON_X = RESET_BUTTON_X
DONE_BUTTON_Y = RESET_BUTTON_Y + TILE_SIZE + TILE_SIZE*.25

SCORE1_X = SCALE * 10
SCORE1_Y = SCALE * 10
SCORE2_X = SCALE * 10
SCORE2_Y = SCALE * 80

ERR_MESSAGE_X = SCALE * 10
ERR_MESSAGE_Y = SCALE * 400

DISCARD_TEXT_X = BOARD_X + BOARD_SIZE + TILE_SIZE*.25
DISCARD_TEXT_Y = SCALE * 10

DISCARD_TILES_X = DISCARD_TEXT_X
DISCARD_TILES_Y = SCALE * 100

BANK_SIZE = 7
BINGO_BONUS = 50

PLAYER_BANK_PADDING = SCALE * TILE_SIZE * .25
PLAYER_BANK_WIDTH = (TILE_SIZE + PLAYER_BANK_PADDING) * 7 - PLAYER_BANK_PADDING
PLAYER_BANK_HEIGHT = TILE_SIZE
PLAYER_BANK_X = (BOARD_X + BOARD_SIZE / 2) - PLAYER_BANK_WIDTH / 2
PLAYER_BANK_Y = BOARD_Y + BOARD_SIZE + TILE_SIZE*.25

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

letter_distribution = {
    "A":     9,
    "B":     2,
    "C":     2,
    "D":     4,
    "E":     12,
    "F":     2,
    "G":     3,
    "H":     2,
    "I":     9,
    "J":     1,
    "K":     1,
    "L":     4,
    "M":     2,
    "N":     6,
    "O":     8,
    "P":     2,
    "Q":     1,
    "R":     6,
    "S":     4,
    "T":     6,
    "U":     4,
    "V":     2,
    "W":     2,
    "X":     1,
    "Y":     2,
    "Z":     1,
    " ":     0,
}

letter_values = {
    "A":     1,
    "B":     3,
    "C":     3,
    "D":     2,
    "E":     1,
    "F":     4,
    "G":     2,
    "H":     4,
    "I":     1,
    "J":     8,
    "K":     5,
    "L":     1,
    "M":     3,
    "N":     1,
    "O":     1,
    "P":     3,
    "Q":     10,
    "R":     1,
    "S":     1,
    "T":     1,
    "U":     1,
    "V":     4,
    "W":     4,
    "X":     8,
    "Y":     4,
    "Z":     10,
    " ":     0,
}


# This enum represents the score multiplier for a tile
class Space(Enum):
    SINGLE = 0
    DOUBLE_LETTER = 1
    TRIPLE_LETTER = 2
    DOUBLE_WORD = 3
    TRIPLE_WORD = 4

class PlayerState(Enum):
    WAITING = 0
    MOVING = 1
    DONE_MOVING = 2

spaces: Space = [
    [4,0,0,1,0,0,0,4,0,0,0,1,0,0,4],
    [0,3,0,0,0,2,0,0,0,2,0,0,0,3,0],
    [0,0,3,0,0,0,1,0,1,0,0,0,3,0,0],
    [1,0,0,3,0,0,0,1,0,0,0,3,0,0,1],
    [0,0,0,0,3,0,0,0,0,0,3,0,0,0,0],
    [0,2,0,0,0,2,0,0,0,2,0,0,0,2,0], 
    [0,0,1,0,0,0,1,0,1,0,0,0,1,0,0],
    [4,0,0,1,0,0,0,3,0,0,0,1,0,0,4],
    [0,0,1,0,0,0,1,0,1,0,0,0,1,0,0],
    [0,2,0,0,0,2,0,0,0,2,0,0,0,2,0],
    [0,0,0,0,3,0,0,0,0,0,3,0,0,0,0],
    [1,0,0,3,0,0,0,1,0,0,0,3,0,0,1],
    [0,0,3,0,0,0,1,0,1,0,0,0,3,0,0],
    [0,3,0,0,0,2,0,0,0,2,0,0,0,3,0],
    [4,0,0,1,0,0,0,4,0,0,0,1,0,0,4]
]

def get_letter(placed_tiles, tiles_placed_on_turn, cell):
    if (cell in placed_tiles):
        return placed_tiles[cell]
    return tiles_placed_on_turn[cell]

# Returns the cells of the word running through (x, y), in reading order.
# (dx, dy) must point in the reading direction: (1, 0) across or (0, 1) down
def get_word_cells(placed_tiles, tiles_placed_on_turn, x, y, dx, dy):
    def has_tile(cell):
        return cell in placed_tiles or cell in tiles_placed_on_turn

    while has_tile((x - dx, y - dy)):
        x -= dx
        y -= dy

    cells = []
    while has_tile((x, y)):
        cells.append((x, y))
        x += dx
        y += dy

    return cells

def draw_tile(screen, small_font, letter_font, color, letter, x, y):
    if (color != None):
        tile = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, tile)
    text = letter_font.render(letter, True, "black");
    screen.blit(text, (x+SCALE*17, y-SCALE*7))
    value = small_font.render(str(letter_values[letter]), True, "black")
    screen.blit(value, (x+TILE_SIZE-TILE_SIZE//6, y+TILE_SIZE-TILE_SIZE//3))

def cells_to_word(placed_tiles, tiles_placed_on_turn, cells):
    return "".join(get_letter(placed_tiles, tiles_placed_on_turn, cell) for cell in cells)

def get_board_pos_px(i, j):
    x = BOARD_X + i*TILE_SIZE
    y = BOARD_Y + j*TILE_SIZE

    return (x,y)

def on_board(pos):
    x, y = pos
    if (x >= 0 and x < 15 and y >= 0 and y < 15):
        return True

    return False
