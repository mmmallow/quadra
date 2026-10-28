import pygame
import random
from enum import Enum

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

PLAYER_BANK_PADDING = BOARD_SIZE // 7
PLAYER_BANK_Y = BOARD_Y + BOARD_SIZE + 20

class GameState:
    player_turn = 0
    err_message = ""
    # Stores all tiles placed by the players as index in spaces : letter
    # (0, 0): "A"
    placed_tiles = {}

    # Tiles placed during a player's turn. Temporary and is wiped after every turn
    tiles_placed_on_turn = {}

# This enum represents the score multiplier for a tile
class Space(Enum):
    SINGLE = 0
    DOUBLE_LETTER = 1
    TRIPLE_LETTER = 2
    DOUBLE_WORD = 3
    TRIPLE_WORD = 4

class Player:
    bank = ["", "", "", "", "", "", ""]
    held_letter = ""
    score = 0

    def __init__(self, screen, small_font, letter_font, tiles_placed_on_turn):
        self.screen = screen
        self.small_font = small_font
        self.letter_font = letter_font
        self.tiles_placed_on_turn = tiles_placed_on_turn

    def Update(self):
        right_mouse_pressed = pygame.mouse.get_pressed()[2]

        if (right_mouse_pressed):
            print("r")

    def Draw(self):
        for i in range(0, 7):
            if (self.bank[i] != ""):
                x = BOARD_X + i*(PLAYER_BANK_PADDING)+43
                y = PLAYER_BANK_Y
                draw_tile(self.screen, self.small_font, self.letter_font, TILE_COLOR, self.bank[i], x, y)

        if (self.held_letter != ""):
            mouse_pos = pygame.mouse.get_pos()
            pos = [0, 0]
            pos[0] = mouse_pos[0]-TILE_SIZE//2
            pos[1] = mouse_pos[1]-TILE_SIZE//2
            draw_tile(self.screen, self.small_font, self.letter_font, TILE_COLOR, self.held_letter, pos[0], pos[1])

    def handle_left_mouse_press(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.held_letter == ""):
            for i in range(0,7):
                tile = pygame.Rect(BOARD_X + i*(PLAYER_BANK_PADDING)+43, PLAYER_BANK_Y, TILE_SIZE, TILE_SIZE)
                if (tile.collidepoint(mouse_pos)):
                    if (self.held_letter != ""):
                        index = self.bank.index("")
                        self.bank[index] = self.held_letter
                    self.held_letter = self.bank[i]
                    self.bank[i] = ""
                    break

            if (self.held_letter == ""):
                for t in self.tiles_placed_on_turn:
                    pos = get_board_pos_px(t[0], t[1])
                    tile = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                    if (tile.collidepoint(mouse_pos)):
                        self.held_letter = self.tiles_placed_on_turn[t]
                        self.tiles_placed_on_turn.pop(t)
                        break
        else:
            board = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
            if (board.collidepoint(mouse_pos)):
                board_x = (mouse_pos[0] - BOARD_X) // TILE_SIZE
                board_y = (mouse_pos[1] - BOARD_Y) // TILE_SIZE
                if ((board_x, board_y) in self.tiles_placed_on_turn):
                    index = self.bank.index("")
                    self.bank[index] = self.tiles_placed_on_turn[(board_x, board_y)]
                self.tiles_placed_on_turn[(board_x, board_y)] = self.held_letter
                self.held_letter = ""
            else:
                index = self.bank.index("")
                self.bank[index] = self.held_letter
                self.held_letter = ""




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

letter_bag = []
for key in letter_distribution:
    for i in range(0, letter_distribution[key]):
        letter_bag.append(key)

random.shuffle(letter_bag)
current_letter = iter(letter_bag)

spaces: Space = [
    [4,0,0,1,0,0,0,4,0,0,0,1,0,0,4],
    [0,3,0,0,0,2,0,0,0,2,0,0,0,3,0],
    [0,0,3,0,0,0,1,0,1,0,0,0,3,0,0],
    [1,0,0,3,0,0,0,1,0,0,0,3,0,0,1],
    [0,0,0,0,3,0,0,0,0,0,3,0,0,0,0],
    [0,2,0,0,0,2,0,0,0,2,0,0,0,2,0], 
    [0,0,1,0,0,0,1,0,1,0,0,0,1,0,0],
    [4,0,0,1,0,0,0,0,0,0,0,1,0,0,4],
    [0,0,1,0,0,0,1,0,1,0,0,0,1,0,0],
    [0,2,0,0,0,2,0,0,0,2,0,0,0,2,0],
    [0,0,0,0,3,0,0,0,0,0,3,0,0,0,0],
    [1,0,0,3,0,0,0,1,0,0,0,3,0,0,1],
    [0,0,3,0,0,0,1,0,1,0,0,0,3,0,0],
    [0,3,0,0,0,2,0,0,0,2,0,0,0,2,0],
    [4,0,0,1,0,0,0,4,0,0,0,1,0,0,4]
]



def init_player(player):
    for i in range(0,7):
        player.bank[i] = next(current_letter)

def get_board_pos_px(i, j):
    x = BOARD_X + i*TILE_SIZE
    y = BOARD_Y + j*TILE_SIZE

    return (x,y)

############################### Draw Code ###############################

def draw_tile(screen, small_font, letter_font, color, letter, x, y):
    if (color != None):
        tile = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, tile)
    text = letter_font.render(letter, True, "black");
    screen.blit(text, (x+17, y-7))
    value = small_font.render(str(letter_values[letter]), True, "black")
    screen.blit(value, (x+TILE_SIZE-TILE_SIZE//6, y+TILE_SIZE-TILE_SIZE//3))

def draw_board(screen, small_font, letter_font):
    pygame.draw.rect(screen, BOARD_COLOR, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE))

    # Draw outline
    pygame.draw.rect(screen, (0,0,0), (BOARD_X, BOARD_Y, BOARD_SIZE+3, BOARD_SIZE+3), 3)

    # Draw vertical lines
    for i in range(0, 15):
        vert_x_pos = BOARD_X + i*TILE_SIZE
        hor_y_pos = BOARD_Y + i*TILE_SIZE
        # Draw vertical lines
        pygame.draw.line(screen, (0,0,0), (vert_x_pos, BOARD_Y), (vert_x_pos, BOARD_Y+BOARD_SIZE), 2)

        #Draw horizontal lines
        pygame.draw.line(screen, (0,0,0), (BOARD_X, hor_y_pos), (BOARD_X+BOARD_SIZE, hor_y_pos), 2)

    draw_star(screen)

    for y in range(0, 15):
        for x in range(0, 15):
            text_color = "black"
            text = ""
            pos = get_board_pos_px(x,y)
            if (x,y) in state.placed_tiles:
                draw_tile(screen, small_font, letter_font, None, state.placed_tiles[(x,y)], pos[0], pos[1])
            elif (x,y) in state.tiles_placed_on_turn:
                draw_tile(screen, small_font, letter_font, TILE_COLOR, state.tiles_placed_on_turn[(x,y)], pos[0], pos[1])
            else:
                space = Space(spaces[y][x])
                match (space):
                    case Space.DOUBLE_LETTER:
                        text_color = "cadetblue1"
                        text = "Double\nLetter"
                    case Space.TRIPLE_LETTER:
                        text_color = "aqua"
                        text = "Triple\nLetter"
                    case Space.DOUBLE_WORD:
                        text_color = "lightpink"
                        text = "Double\n Word"
                    case Space.TRIPLE_WORD:
                        text_color = "indianred2"
                        text = "Triple\n Word"

                top = small_font.render(text, True, text_color)
                screen.blit(top, (pos[0]+7,pos[1]+10))

def draw_star(screen):
    middle_tile = pygame.Rect(BOARD_X - TILE_SIZE//2 + BOARD_SIZE//2, BOARD_Y - TILE_SIZE//2 + BOARD_SIZE//2, TILE_SIZE, TILE_SIZE)
    top_point = (middle_tile.x + TILE_SIZE//2, middle_tile.y+5)
    bottom_left = (middle_tile.x + TILE_SIZE//8, middle_tile.y + TILE_SIZE//2 + TILE_SIZE//4 + TILE_SIZE//8)
    right = (middle_tile.x+TILE_SIZE-5, middle_tile.y - 10 + TILE_SIZE//2)
    left = (middle_tile.x+5, middle_tile.y - 10 + TILE_SIZE//2)
    bottom_right = (middle_tile.x + TILE_SIZE//2 + TILE_SIZE//4 + TILE_SIZE//8, middle_tile.y + TILE_SIZE//2 + TILE_SIZE//4 + TILE_SIZE//8)
    pygame.draw.lines(screen, "black", True, [top_point, bottom_left, right, left, bottom_right])

def draw_ui(screen, letter_font):
    score1 = f"Player 1: {player1.score}"
    text = letter_font.render(score1, True, "white")
    screen.blit(text, (10, 10))
    pygame.draw.rect(screen, "grey45", (PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    pygame.draw.polygon(screen, "white", [[PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//4], [PLAY_BUTTON_X+TILE_SIZE-TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//2], [PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE-TILE_SIZE//4]])

    if (state.err_message != ""):
        msg = letter_font.render(state.err_message, True, "red")
        screen.blit(msg, (10, 400))

###################################################################################

############################### UI Interaction Code ###############################
def handle_element_clicked():
    play_button = pygame.Rect(PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE)
    pos = pygame.mouse.get_pos();
    is_player_event = True
    if (play_button.collidepoint(pos)):
        play_turn()
        is_player_event = False

    return is_player_event

###################################################################################

################################## Gameplay Code ##################################

def play_turn():
    valid = score()

    if (valid):
        state.player_turn = 1 if state.player_turn == 0 else 0
        state.err_message = ""

def score():
    tiles = []
    for tile in state.tiles_placed_on_turn:
        tiles.append((pygame.Vector2(tile), state.tiles_placed_on_turn[tile]))

    prev_tile = tiles[0]
    for tile in tiles:
        if (tile[0].x == prev_tile[0].x):
            vert = True




###################################################################################

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Scrabble')

    small_font = pygame.font.Font(FONT_PATH, 20)
    letter_font = pygame.font.Font(FONT_PATH, 80)

    global state
    state = GameState()

    global player1
    player1 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn)

    running = True
    clock = pygame.time.Clock()

    init_player(player1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.MOUSEBUTTONDOWN):
                is_player_event = handle_element_clicked()
                left_mouse_pressed = pygame.mouse.get_pressed()[0]
                right_mouse_pressed = pygame.mouse.get_pressed()[2]
                if (left_mouse_pressed and state.player_turn == 0 and is_player_event):
                    player1.handle_left_mouse_press()

        player1.Update()
        
        screen.fill(BG_COLOR)
        
        draw_board(screen, small_font, letter_font)
        draw_ui(screen, letter_font)
        player1.Draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
