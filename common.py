import pygame
import os
import pickle
from enum import Enum
from word_tree import *

SCREEN_WIDTH = 2160
SCREEN_HEIGHT = 1215

FONT_PATH = '/home/evan/.local/share/fonts/InconsolataNerdFont-Regular.ttf'

TILE_SIZE = 72
TILE_COLOR = (160, 120, 80)
BG_COLOR = (55, 57, 58)
BOARD_COLOR = (168, 157, 149)
BOARD_SIZE = 1080
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 25
PLAY_BUTTON_X = SCREEN_WIDTH - SCREEN_WIDTH//8
PLAY_BUTTON_Y = SCREEN_HEIGHT - SCREEN_HEIGHT//6
RESET_BUTTON_X = PLAY_BUTTON_X + TILE_SIZE + TILE_SIZE*.25
RESET_BUTTON_Y = PLAY_BUTTON_Y
SKIP_BUTTON_X = RESET_BUTTON_X + TILE_SIZE + TILE_SIZE*.25
SKIP_BUTTON_Y = PLAY_BUTTON_Y
DONE_BUTTON_X = RESET_BUTTON_X
DONE_BUTTON_Y = RESET_BUTTON_Y + TILE_SIZE + TILE_SIZE*.25

BANK_SIZE = 7
BINGO_BONUS = 50

PLAYER_BANK_PADDING = BOARD_SIZE // 7
PLAYER_BANK_Y = BOARD_Y + BOARD_SIZE + 20

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
    " ":     2,
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

class GameState:
    player_turn = 0
    err_message = ""
    win_message = ""
    is_first_move = True
    letter_bag_empty = False
    turns_without_move = 0
    game_over = False
    # Stores all tiles placed by the players as index in spaces : letter
    # (0, 0): "A"
    placed_tiles = {}

    # Tiles placed during a player's turn. Temporary and is wiped after every turn
    tiles_placed_on_turn = {}

    # Tiles in to be removed from player's letter bank
    discard_pile = []

    def __init__(self, current_letter, dict_file):
        self.current_letter = current_letter

        extension = os.path.splitext(dict_file)[1]
        if (extension == ".txt"):
            self.word_tree = WordTree(dict_file)
        elif (extension == ".pkl"):
            with open(dict_file, 'rb') as f:
                self.word_tree = pickle.load(f)

# This enum represents the score multiplier for a tile
class Space(Enum):
    SINGLE = 0
    DOUBLE_LETTER = 1
    TRIPLE_LETTER = 2
    DOUBLE_WORD = 3
    TRIPLE_WORD = 4


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


def draw_tile(screen, small_font, letter_font, color, letter, x, y):
    if (color != None):
        tile = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, tile)
    text = letter_font.render(letter, True, "black");
    screen.blit(text, (x+17, y-7))
    value = small_font.render(str(letter_values[letter]), True, "black")
    screen.blit(value, (x+TILE_SIZE-TILE_SIZE//6, y+TILE_SIZE-TILE_SIZE//3))

def get_board_pos_px(i, j):
    x = BOARD_X + i*TILE_SIZE
    y = BOARD_Y + j*TILE_SIZE

    return (x,y)
