import pygame
import random
import os
from player    import *
from ai_player import *
from common    import *



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

    pygame.draw.rect(screen, "grey45", (DONE_BUTTON_X, DONE_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    text = small_font.render("DONE", True, "white")
    screen.blit(text, (DONE_BUTTON_X+TILE_SIZE//6, DONE_BUTTON_Y+TILE_SIZE//3))

    if (state.err_message != ""):
        msg = letter_font.render(state.err_message, True, "red")
        screen.blit(msg, (10, 400))

    if (state.game_over):
        msg = letter_font.render(state.win_message, True, "white")
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
    done_button = pygame.Rect(DONE_BUTTON_X, DONE_BUTTON_Y, TILE_SIZE, TILE_SIZE)
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
    elif (done_button.collidepoint(pos) and state.player_turn == 0):
        player_is_done(player1)
        is_player_event = False
    elif (done_button.collidepoint(pos) and state.player_turn == 1):
        player_is_done(player2)
        is_player_event = False

    return is_player_event

##############################################################################

################################## Gameplay ##################################

def player_is_done(player):
    state.discard_pile.clear()
    state.player_turn = 0 if state.player_turn else 1
    state.turns_without_move += 1
    player.is_done = True
    check_game_over()

def skip_turn(player):
    state.discard_pile.clear()
    state.err_message = ""
    init_player(player)
    state.player_turn = 0 if state.player_turn else 1
    state.turns_without_move += 1
    check_game_over()

def play_turn():
    words = []

    if (len(state.tiles_placed_on_turn) == 0):
        skip_turn(player2 if state.player_turn else player1)
    else:
        words = state.evaluator.Evaluate()

    if (words):
        # Valid move. Score before the tiles are committed, since premium
        # squares only count for tiles placed this turn
        player = player1 if state.player_turn == 0 else player2
        player.score += state.evaluator.Score(words)
        if (len(state.discard_pile) > 0):
            for tile in state.discard_pile:
                index = player.bank.index("")
                player.bank[index] = tile
            state.discard_pile.clear()
        init_player(player)

        for tile in state.tiles_placed_on_turn:
            state.placed_tiles[(tile)] = state.tiles_placed_on_turn[tile]

        print([cells_to_word(state.placed_tiles, state.tiles_placed_on_turn, word) for word in words])

        state.tiles_placed_on_turn.clear()
        state.is_first_move = False

        if (player == player1 and not player2.is_done):
            state.player_turn = 1
        elif (player == player2 and not player1.is_done):
            state.player_turn = 0
            player2.state = AIState.WAITING

        state.err_message = ""
        state.turns_without_move = 0

    check_game_over()

def init_player(player):
    for i in range(0,BANK_SIZE):
        if (player.bank[i] == ""):
            try:
                player.bank[i] = next(state.current_letter)
            except:
                state.letter_bag_empty = True

def check_game_over():
    if (state.turns_without_move >= 6):
        end_game()
    elif (player1.is_done and player2.is_done):
        end_game()
    elif (state.letter_bag_empty and all(c == "" for c in player1.bank) and all(c == "" for c in player2.bank)):
        end_game()

def end_game():
    state.game_over = True
    state.err_message = ""
    winner = "Player 1" if player1.score > player2.score else "Player 2"
    state.win_message = winner + " wins!"


##############################################################################

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Scrabble')

    small_font = pygame.font.Font(FONT_PATH, 20)
    letter_font = pygame.font.Font(FONT_PATH, 80)

    global letter_bag
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
    player1 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn, state.discard_pile, state.placed_tiles)
    global player2
    #player2 = Player(screen, small_font, letter_font, state.tiles_placed_on_turn, state.discard_pile, state.placed_tiles)
    player2 = AIPlayer(state.tiles_placed_on_turn, state.discard_pile, state.placed_tiles, state.evaluator)

    running = True
    clock = pygame.time.Clock()

    init_player(player1)
    init_player(player2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.MOUSEBUTTONDOWN and not state.game_over):
                is_player_event = handle_element_clicked()
                left_mouse_pressed = pygame.mouse.get_pressed()[0]
                right_mouse_pressed = pygame.mouse.get_pressed()[2]
                if (left_mouse_pressed and state.player_turn == 0 and is_player_event):
                    player1.HandleLeftMousePress()
                elif (left_mouse_pressed and state.player_turn == 1 and is_player_event):
                    player2.HandleLeftMousePress()

                if (right_mouse_pressed and state.player_turn == 0 and is_player_event):
                    player1.HandleRightMousePress()
                elif (right_mouse_pressed and state.player_turn == 1 and is_player_event):
                    player2.HandleRightMousePress()

        if (state.player_turn == 1 and player2.state == AIState.WAITING):
            player2.PlayTurn()
        elif (state.player_turn == 1 and (player2.state == AIState.DONE_MOVING or player1.is_done)):
            play_turn()

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
