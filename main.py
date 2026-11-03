import pygame
import random
import os
from player import *
from common import *



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
    score2 = f"Player 2: {player2.score}"
    text = letter_font.render(score1, True, "white")
    screen.blit(text, (10, 10))
    text = letter_font.render(score2, True, "white")
    screen.blit(text, (10, 80))

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
    if (play_button.collidepoint(pos)):
        play_turn()
        is_player_event = False
    elif (reset_button.collidepoint(pos) and state.player_turn == 0):
        player1.Reset()
        is_player_event = False
    elif (reset_button.collidepoint(pos) and state.player_turn == 1):
        player2.Reset()
        is_player_event = False

    return is_player_event

##############################################################################

################################## Gameplay ##################################

def play_turn():
    words = check_valid()

    if (words):
        # Valid move
        for tile in state.tiles_placed_on_turn:
            state.placed_tiles[(tile)] = state.tiles_placed_on_turn[tile]

        state.tiles_placed_on_turn.clear()
        state.is_first_move = False
        print(words)

        state.player_turn = 1 if state.player_turn == 0 else 0
        state.err_message = ""

        print(player1.bank)
        print(player2.bank)

# FIX: Sometimes words appear backwards when placing one tile above already placed tiles
#      Don't know if it is that way for any other orientations
def check_tiles(ox, oy, dx, dy, letter):
    # Find the first overall letter in the word
    x = ox
    y = oy
    first_tile = None
    while (True):
        neighbor = (x+dx, y+dy)
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
    word = ""
    while (True):
        if ((x, y) in state.placed_tiles):
            word += state.placed_tiles[(x, y)]
        elif (x == ox and y == oy):
            word += letter
            i += 1
        else:
            break

        x -= dx
        y -= dy
        counter += 1
        if (counter == 8):
            state.err_message = "An error occurred"
            return ""

    return word

def check_valid():
    if (len(state.tiles_placed_on_turn) == 0):
        state.err_message = "Must play a\nword"
        return []
    if (state.is_first_move and (7, 7) not in state.tiles_placed_on_turn):
        state.err_message = "Middle tile\nmust be used\non first turn"
        return []

    tiles = []
    for tile in state.tiles_placed_on_turn:
        tiles.append((pygame.Vector2(tile), state.tiles_placed_on_turn[tile]))

    # Check if the placed tiles are in a line
    horiz = 0
    vert  = 0
    if (len(tiles) > 1):
        horiz = 1 if all(tile[0].y == tiles[0][0].y for tile in tiles) else 0
        vert  = 1 if all(tile[0].x == tiles[0][0].x for tile in tiles) else 0

        if (horiz == 0 and vert == 0):
            state.err_message = "Tiles must be\nin a straight\nline"
            return []
    else:
        if (((tiles[0][0].x+1, tiles[0][0].y) in state.placed_tiles) or ((tiles[0][0].x-1, tiles[0][0].y) in state.placed_tiles)):
            horiz = 1
        elif (((tiles[0][0].x, tiles[0][0].y+1) in state.placed_tiles) or ((tiles[0][0].x, tiles[0][0].y-1) in state.placed_tiles)):
            vert = 1
        else:
            state.err_message = "Must use\ntiles already\nplaced"
            return []

    if (horiz):
        tiles.sort(key=lambda x: x[0].x)
    else:
        tiles.sort(key=lambda x: x[0].y)

    words = []
    word = ""

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
    used_placed_tiles = False
    while (True):
        if ((x, y) in state.placed_tiles):
            word += state.placed_tiles[(x, y)]
            used_placed_tiles = True
        elif (i < len(tiles) and x == tiles[i][0].x and y == tiles[i][0].y):
            word += tiles[i][1]
            i += 1
        else:
            break

        x += horiz
        y += vert
        counter += 1
        if (counter == 8):
            state.err_message = "An error occurred"
            return []

    print(word)
    if (not state.is_first_move and not used_placed_tiles):
        state.err_message = "Must use\ntiles already\nplaced"
        return []

    words.append(word)

    # Check that tiles placed this turn form words with any other placed tiles
    for tile in tiles:
        x = int(tile[0].x)
        y = int(tile[0].y)
        if ((x+1, y) in state.placed_tiles and not horiz):
            new_word = check_tiles(x, y, 1, 0, tile[1])
            if (new_word != ""):
                words.append(new_word)
            else:
                state.err_message = "Invalid move"
                return []
        if ((x-1, y) in state.placed_tiles and not horiz):
            new_word = check_tiles(x, y, -1, 0, tile[1])
            if (new_word != ""):
                words.append(new_word)
            else:
                state.err_message = "Invalid move"
                return []

        if ((x, y+1) in state.placed_tiles and not vert):
            new_word = check_tiles(x, y, 0, 1, tile[1])
            if (new_word != ""):
                words.append(new_word)
            else:
                state.err_message = "Invalid move"
                return []
        if ((x, y-1) in state.placed_tiles and not vert):
            new_word = check_tiles(x, y, 0, -1, tile[1])
            if (new_word != ""):
                words.append(new_word)
            else:
                state.err_message = "Invalid move"
                return []

    for w in words:
        valid = state.word_tree.check_word(w)
        if (not valid):
            state.err_message = f"Invalid word:\n{w}"
            return []

    score = 0
    multiplier = 1
    # Score words
    # First word in words will always be made of placed tiles
    for tile in tiles:
        x = int(tile[0].x)
        y = int(tile[0].y)
        space = Space(spaces[y][x])
        match (space):
            case Space.DOUBLE_LETTER:
                score += letter_values[tile[1]] * 2
            case Space.TRIPLE_LETTER:
                score += letter_values[tile[1]] * 3
            case Space.DOUBLE_WORD:
                score += letter_values[tile[1]]
                multiplier = 2
            case Space.TRIPLE_WORD:
                score += letter_values[tile[1]]
                multiplier = 3
            case _:
                score += letter_values[tile[1]]

    score *= multiplier
    if state.player_turn == 0:
        player1.score += score
        init_player(player1)
    else:
        player2.score += score
        init_player(player2)

    return words


def init_player(player):
    for i in range(0,7):
        if (player.bank[i] == ""):
            player.bank[i] = next(state.current_letter)


##############################################################################

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Scrabble')

    small_font = pygame.font.Font(FONT_PATH, 20)
    letter_font = pygame.font.Font(FONT_PATH, 80)

    letter_bag = []
    for key in letter_distribution:
        for i in range(0, letter_distribution[key]):
            letter_bag.append(key)

    random.shuffle(letter_bag)
    current_letter = iter(letter_bag)

    global state
    if (os.path.exists("word_tree_obj.pkl")):
        state = GameState(current_letter, "word_tree_obj.pkl")
    else:
        state = GameState(current_letter, "words.txt")

    global player1
    player1 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn)
    global player2
    player2 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn)

    running = True
    clock = pygame.time.Clock()

    init_player(player1)
    init_player(player2)

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
                elif (left_mouse_pressed and state.player_turn == 1 and is_player_event):
                    player2.handle_left_mouse_press()

        screen.fill(BG_COLOR)
        
        draw_board(screen, small_font, letter_font)
        draw_ui(screen, small_font, letter_font)
        if (state.player_turn == 0):
            player1.Draw()
        else:
            player2.Draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
