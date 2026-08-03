import pygame
from enum import Enum

SCREEN_WIDTH = 2160
SCREEN_HEIGHT = 1215

FONT_PATH = '/home/evan/.local/share/fonts/InconsolataNerdFont-Regular.ttf'

TILE_SIZE = 72
TILE_COLOR = (160, 120, 80)
BG_COLOR = (55, 57, 58)
BOARD_COLOR = (168, 157, 149)
BOARD_SIZE = 1080
board_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
board_y = 25

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
    [4,0,0,1,0,0,0,0,0,0,0,1,0,0,4],
    [0,0,1,0,0,0,1,0,1,0,0,0,1,0,0],
    [0,2,0,0,0,2,0,0,0,2,0,0,0,2,0],
    [0,0,0,0,3,0,0,0,0,0,3,0,0,0,0],
    [1,0,0,3,0,0,0,1,0,0,0,3,0,0,1],
    [0,0,3,0,0,0,1,0,1,0,0,0,3,0,0],
    [0,3,0,0,0,2,0,0,0,2,0,0,0,2,0],
    [4,0,0,1,0,0,0,4,0,0,0,1,0,0,4]
]

# Stores all tiles placed by the players as index in spaces : letter
# (0, 0): "A"
placed_tiles = {}

def get_board_pos_px(i, j):
    x = board_x + i*TILE_SIZE
    y = board_y + j*TILE_SIZE

    return (x,y)

def draw_board(screen, small_font, letter_font):
    pygame.draw.rect(screen, BOARD_COLOR, (board_x, board_y, BOARD_SIZE, BOARD_SIZE))

    # Draw outline
    pygame.draw.rect(screen, (0,0,0), (board_x, board_y, BOARD_SIZE+3, BOARD_SIZE+3), 3)

    # Draw vertical lines
    for i in range(0, 15):
        vert_x_pos = board_x + i*TILE_SIZE
        hor_y_pos = board_y + i*TILE_SIZE
        # Draw vertical lines
        pygame.draw.line(screen, (0,0,0), (vert_x_pos, board_y), (vert_x_pos, board_y+BOARD_SIZE), 2)

        #Draw horizontal lines
        pygame.draw.line(screen, (0,0,0), (board_x, hor_y_pos), (board_x+BOARD_SIZE, hor_y_pos), 2)

    for i in range(0, 15):
        for j in range(0, 15):
            text_color = "black"
            text_top = ""
            text_bottom = ""
            pos = get_board_pos_px(i,j)
            if (i,j) in placed_tiles:
                letter = letter_font.render(placed_tiles[(i,j)], True, "black")
                screen.blit(letter, (pos[0]+17, pos[1]-7))
            else:
                space = Space(spaces[i][j])
                match (space):
                    case Space.DOUBLE_LETTER:
                        text_color = "cadetblue1"
                        text_top = "Double"
                        text_bottom = "Letter"
                    case Space.TRIPLE_LETTER:
                        text_color = "aqua"
                        text_top = "Triple"
                        text_bottom = "Letter"
                    case Space.DOUBLE_WORD:
                        text_color = "lightpink"
                        text_top = "Double"
                        text_bottom = "Word"
                    case Space.TRIPLE_WORD:
                        text_color = "indianred2"
                        text_top = "Triple"
                        text_bottom = "Word"

                top = small_font.render(text_top, True, text_color)
                bottom = small_font.render(text_bottom, True, text_color)
                screen.blit(top, (pos[0]+7,pos[1]+10))
                screen.blit(bottom, (pos[0]+7, pos[1]+35))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Scrabble')

    small_font = pygame.font.Font(FONT_PATH, 20)
    letter_font = pygame.font.Font(FONT_PATH, 80)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw content that adapts to window size
        screen.fill(BG_COLOR)
        
        # Draw a rectangle that scales with window size
        draw_board(screen, small_font, letter_font)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
