import pygame
import random
import os
import sys
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
                        # The middle square shows the star instead
                        text = "" if (x,y) == (7,7) else "Double\n Word"
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

    color = "white" if state.player_turn else "blue"
    text = letter_font.render(score1, True, color)
    screen.blit(text, (10, 10))

    color = "blue" if state.player_turn else "white"
    text = letter_font.render(score2, True, color)
    screen.blit(text, (10, 80))

    pygame.draw.rect(screen, "grey45", (PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    pygame.draw.polygon(screen, "white", [[PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//4], [PLAY_BUTTON_X+TILE_SIZE-TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//2], [PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE-TILE_SIZE//4]])

    pygame.draw.rect(screen, "grey45", (RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    text = small_font.render("RESET", True, "white")
    screen.blit(text, (RESET_BUTTON_X+TILE_SIZE//6, RESET_BUTTON_Y+TILE_SIZE//3))

    pygame.draw.rect(screen, "grey45", (SKIP_BUTTON_X, SKIP_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    text = small_font.render("SKIP", True, "white")
    screen.blit(text, (SKIP_BUTTON_X+TILE_SIZE//6, SKIP_BUTTON_Y+TILE_SIZE//3))

    if (state.err_message != ""):
        msg = letter_font.render(state.err_message, True, "red")
        screen.blit(msg, (10, 400))

def draw_discard_pile(screen, small_font, letter_font):
    text = letter_font.render("Discard Pile:", True, "white")
    screen.blit(text, (BOARD_X+BOARD_SIZE+20, 10))

    x_offset = BOARD_X + BOARD_SIZE + 10
    y_offset = 100
    for tile in state.discard_pile:
        if (x_offset >= SCREEN_WIDTH):
            x_offset = BOARD_X + BOARD_SIZE + 10
            y_offset += TILE_SIZE+TILE_SIZE*.25

        draw_tile(screen, small_font, letter_font, TILE_COLOR, tile, x_offset, y_offset)

        x_offset += TILE_SIZE+TILE_SIZE*.25

##############################################################################

############################### UI Interaction ###############################
def handle_element_clicked():
    play_button = pygame.Rect(PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE)
    reset_button = pygame.Rect(RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE)
    skip_button = pygame.Rect(SKIP_BUTTON_X, SKIP_BUTTON_Y, TILE_SIZE, TILE_SIZE)
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
    elif (skip_button.collidepoint(pos) and state.player_turn == 0):
        skip_turn(player1)
        is_player_event = False
    elif (skip_button.collidepoint(pos) and state.player_turn == 1):
        skip_turn(player2)
        is_player_event = False

    return is_player_event

##############################################################################

################################## Gameplay ##################################

def skip_turn(player):
    state.discard_pile.clear()
    init_player(player)
    state.player_turn = 0 if state.player_turn else 1

def play_turn():
    words = check_valid()

    if (words):
        # Valid move. Score before the tiles are committed, since premium
        # squares only count for tiles placed this turn
        player = player1 if state.player_turn == 0 else player2
        player.score += score_move(words)
        init_player(player)

        for tile in state.tiles_placed_on_turn:
            state.placed_tiles[(tile)] = state.tiles_placed_on_turn[tile]

        print([cells_to_word(word) for word in words])

        state.tiles_placed_on_turn.clear()
        state.is_first_move = False

        state.player_turn = 1 if state.player_turn == 0 else 0
        state.err_message = ""


def get_letter(cell):
    if (cell in state.placed_tiles):
        return state.placed_tiles[cell]
    return state.tiles_placed_on_turn[cell]


# Returns the cells of the word running through (x, y), in reading order.
# (dx, dy) must point in the reading direction: (1, 0) across or (0, 1) down
def get_word_cells(x, y, dx, dy):
    def has_tile(cell):
        return cell in state.placed_tiles or cell in state.tiles_placed_on_turn

    while has_tile((x - dx, y - dy)):
        x -= dx
        y -= dy

    cells = []
    while has_tile((x, y)):
        cells.append((x, y))
        x += dx
        y += dy

    return cells


def cells_to_word(cells):
    return "".join(get_letter(cell) for cell in cells)


# Returns every word formed this turn as a list of cells, with the main word
# first. Returns [] and sets the error message if the move isn't legal
def check_valid():
    if (len(state.tiles_placed_on_turn) == 0):
        state.err_message = "Must play a\nword"
        return []
    if (state.is_first_move and (7, 7) not in state.tiles_placed_on_turn):
        state.err_message = "Middle tile\nmust be used\non first turn"
        return []

    tiles = sorted(state.tiles_placed_on_turn)

    if (any(tile in state.placed_tiles for tile in tiles)):
        state.err_message = "Space already\ntaken"
        return []

    # Check if the placed tiles are in a line
    horiz = 0
    vert  = 0
    if (len(tiles) > 1):
        horiz = 1 if all(tile[1] == tiles[0][1] for tile in tiles) else 0
        vert  = 1 if all(tile[0] == tiles[0][0] for tile in tiles) else 0

        if (horiz == 0 and vert == 0):
            state.err_message = "Tiles must be\nin a straight\nline"
            return []
    else:
        x, y = tiles[0]
        if (((x+1, y) in state.placed_tiles) or ((x-1, y) in state.placed_tiles)):
            horiz = 1
        elif (((x, y+1) in state.placed_tiles) or ((x, y-1) in state.placed_tiles)):
            vert = 1
        else:
            state.err_message = "Must use\ntiles already\nplaced"
            return []

    main_word = get_word_cells(tiles[0][0], tiles[0][1], horiz, vert)

    if (any(tile not in main_word for tile in tiles)):
        state.err_message = "Tiles must\nnot have gaps"
        return []

    if (len(main_word) < 2):
        state.err_message = "Words must\nbe at least\n2 letters\nlong"
        return []

    words = [main_word]

    # Check that tiles placed this turn form words with any other placed tiles
    for x, y in tiles:
        cross_word = get_word_cells(x, y, vert, horiz)
        if (len(cross_word) > 1):
            words.append(cross_word)

    # The move can connect through the main word or through any cross word
    connected = any(cell in state.placed_tiles for word in words for cell in word)
    if (not state.is_first_move and not connected):
        state.err_message = "Must use\ntiles already\nplaced"
        return []

    for cells in words:
        word = cells_to_word(cells)
        if (not state.word_tree.check_word(word)):
            state.err_message = f"Invalid word:\n{word}"
            return []

    return words


# Every letter in a word counts, but premium squares only apply to tiles placed
# this turn. A new tile's premium applies to each word it's part of
def score_word(cells):
    score = 0
    multiplier = 1
    for cell in cells:
        value = letter_values[get_letter(cell)]
        if (cell in state.tiles_placed_on_turn):
            x, y = cell
            match (Space(spaces[y][x])):
                case Space.DOUBLE_LETTER:
                    value *= 2
                case Space.TRIPLE_LETTER:
                    value *= 3
                case Space.DOUBLE_WORD:
                    multiplier *= 2
                case Space.TRIPLE_WORD:
                    multiplier *= 3
        score += value

    return score * multiplier


def score_move(words):
    score = sum(score_word(cells) for cells in words)
    if (len(state.tiles_placed_on_turn) == BANK_SIZE):
        score += BINGO_BONUS
    return score


def init_player(player):
    for i in range(0,BANK_SIZE):
        if (player.bank[i] == ""):
            player.bank[i] = next(state.current_letter, "")


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
        state = GameState(current_letter, "dictionary.txt")

    global player1
    player1 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn, state.discard_pile)
    global player2
    player2 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn, state.discard_pile)

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

                if (right_mouse_pressed and state.player_turn == 0 and is_player_event):
                    player1.handle_right_mouse_press()
                elif (right_mouse_pressed and state.player_turn == 1 and is_player_event):
                    player2.handle_right_mouse_press()

        screen.fill(BG_COLOR)
        
        draw_board(screen, small_font, letter_font)
        draw_ui(screen, small_font, letter_font)
        draw_discard_pile(screen, small_font, letter_font)
        if (state.player_turn == 0):
            player1.Draw()
        else:
            player2.Draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
