import pygame
import random
from player import *
from common import *

letter_bag = []
for key in letter_distribution:
    for i in range(0, letter_distribution[key]):
        letter_bag.append(key)

random.shuffle(letter_bag)
current_letter = iter(letter_bag)

def init_player(player):
    for i in range(0,7):
        player.bank[i] = next(current_letter)

############################### Draw Code ###############################

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

    if (state.is_first_move):
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

def draw_ui(screen, small_font, letter_font):
    score1 = f"Player 1: {player1.score}"
    text = letter_font.render(score1, True, "white")
    screen.blit(text, (10, 10))

    pygame.draw.rect(screen, "grey45", (PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    pygame.draw.polygon(screen, "white", [[PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//4], [PLAY_BUTTON_X+TILE_SIZE-TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//2], [PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE-TILE_SIZE//4]])

    pygame.draw.rect(screen, "grey45", (RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    text = small_font.render("RESET", True, "white")
    screen.blit(text, (RESET_BUTTON_X+TILE_SIZE//6, RESET_BUTTON_Y+TILE_SIZE//3))

    if (state.err_message != ""):
        msg = letter_font.render(state.err_message, True, "red")
        screen.blit(msg, (10, 400))

##############################################################################

############################### UI Interaction ###############################
def handle_element_clicked():
    play_button = pygame.Rect(PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE)
    reset_button = pygame.Rect(RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE)
    pos = pygame.mouse.get_pos();
    is_player_event = True
    if (play_button.collidepoint(pos) and state.player_turn == 0):
        play_turn()
        is_player_event = False
    elif (reset_button.collidepoint(pos) and state.player_turn == 0):
        player1.Reset()
        is_player_event = False

    return is_player_event

##############################################################################

################################## Gameplay ##################################

def play_turn():
    valid = score()

    if (valid):
        state.player_turn = 1 if state.player_turn == 0 else 0
        state.err_message = ""

def score():
    if (len(state.tiles_placed_on_turn) == 0):
        state.err_message = "Must play a\nword"
        return False

    if (state.is_first_move and (7, 7) not in state.tiles_placed_on_turn):
        state.err_message = "Middle tile\nmust be used\non first turn"
        return False

    tiles = []
    for tile in state.tiles_placed_on_turn:
        tiles.append((pygame.Vector2(tile), state.tiles_placed_on_turn[tile]))

    # Check if the placed tiles are in a line
    horiz = 0
    vert  = 0
    if (len(tiles) > 1):
        horiz = 1 if all(item[0].y == tiles[0][0].y for item in tiles) else 0
        vert  = 1 if all(item[0].x == tiles[0][0].x for item in tiles) else 0

        if (horiz == 0 and vert == 0):
            state.err_message = "Tiles must be\nin a straight\nline"
            return False

    if (horiz):
        tiles.sort(key=lambda x: x[0].x)
    else:
        tiles.sort(key=lambda x: x[0].y)

    score = 0
    word = []

    # Find the first overall letter in the word
    x = tiles[0][0].x
    y = tiles[0][0].y
    first_tile = None
    while (True):
        neighbor = (x-horiz, y-vert)
        if (neighbor in state.placed_tiles):
            x = neighbor[0]
            y = neighbor[1]
        else:
            first_tile = pygame.Vector2(x, y)
            break

    i = 0
    counter = 0
    x = first_tile.x
    y = first_tile.y
    while (True):
        if ((x, y) in state.placed_tiles):
            word.append(state.placed_tiles[(x, y)])
        elif (i < len(tiles) and x == tiles[i][0].x and y == tiles[i][0].y):
            word.append(tiles[i][1])
            i += 1
        else:
            break

        x += horiz
        y += vert
        counter += 1
        if (counter == 8):
            break


    for tile in tiles:
        state.placed_tiles[(tile[0].x, tile[0].y)] = tile[1]

    state.tiles_placed_on_turn.clear()
    state.is_first_move = False
    print(word)

    return True


##############################################################################

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
        draw_ui(screen, small_font, letter_font)
        player1.Draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
