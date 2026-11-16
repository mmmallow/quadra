import pygame
import random
import os
import inquirer
from player       import *
from ai_player    import *
from game_manager import *
from common       import *



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

    if (game.state.is_first_move):
        draw_star(screen)

    for y in range(0, 15):
        for x in range(0, 15):
            text_color = "black"
            text = ""
            text_bottom = ""
            pos = get_board_pos_px(x,y)
            if (x,y) in game.state.placed_tiles:
                draw_tile(screen, small_font, letter_font, None, game.state.placed_tiles[(x,y)], pos[0], pos[1])
            elif (x,y) in game.state.tiles_placed_on_turn:
                draw_tile(screen, small_font, letter_font, TILE_COLOR, game.state.tiles_placed_on_turn[(x,y)], pos[0], pos[1])
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

                draw_text(screen, small_font, SMALL_FONT_SIZE, text, text_color, (pos[0]+SCALE*7,pos[1]+SCALE*10))

def draw_text(screen, font, font_size, text, text_color, pos):
    split = text.split('\n')
    for i in range(0, len(split)):
        top = font.render(split[i], True, text_color)
        screen.blit(top, (pos[0], pos[1]+(i*font_size+font_size*.25)))

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

    color = "white" if game.state.player_turn else "blue"
    draw_text(screen, letter_font, LETTER_FONT_SIZE, score1, color, (SCORE1_X, SCORE1_Y))

    color = "blue" if game.state.player_turn else "white"
    draw_text(screen, letter_font, LETTER_FONT_SIZE, score2, color, (SCORE2_X, SCORE2_Y))

    pygame.draw.rect(screen, "grey45", (PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    pygame.draw.polygon(screen, "white", [[PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//4], [PLAY_BUTTON_X+TILE_SIZE-TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE//2], [PLAY_BUTTON_X+TILE_SIZE//4, PLAY_BUTTON_Y+TILE_SIZE-TILE_SIZE//4]])

    pygame.draw.rect(screen, "grey45", (RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    draw_text(screen, small_font, SMALL_FONT_SIZE, "RESET", "white", (RESET_BUTTON_X+TILE_SIZE//6, RESET_BUTTON_Y+TILE_SIZE//3))

    pygame.draw.rect(screen, "grey45", (SKIP_BUTTON_X, SKIP_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    draw_text(screen, small_font, SMALL_FONT_SIZE, "SKIP", "white", (SKIP_BUTTON_X+TILE_SIZE//6, SKIP_BUTTON_Y+TILE_SIZE//3))

    pygame.draw.rect(screen, "grey45", (DONE_BUTTON_X, DONE_BUTTON_Y, TILE_SIZE, TILE_SIZE))
    draw_text(screen, small_font, SMALL_FONT_SIZE, "DONE", "white", (DONE_BUTTON_X+TILE_SIZE//6, DONE_BUTTON_Y+TILE_SIZE//3))

    if (game.state.err_message != "" and game.state.display_err_message):
        draw_text(screen, letter_font, LETTER_FONT_SIZE, game.state.err_message, "red", (ERR_MESSAGE_X, ERR_MESSAGE_Y))

    if (game.state.game_over):
        draw_text(screen, letter_font, LETTER_FONT_SIZE, game.state.win_message, "white", (ERR_MESSAGE_X, ERR_MESSAGE_Y))

def draw_discard_pile(screen, small_font, letter_font):
    text = letter_font.render("Discard Pile:", True, "white")
    screen.blit(text, (DISCARD_TEXT_X, DISCARD_TEXT_Y))

    x_offset = DISCARD_TILES_X
    y_offset = DISCARD_TILES_Y
    for tile in game.state.discard_pile:
        if (x_offset >= SCREEN_WIDTH):
            x_offset = BOARD_X + BOARD_SIZE + 10
            y_offset += TILE_SIZE+TILE_SIZE*.25

        draw_tile(screen, small_font, letter_font, TILE_COLOR, tile, x_offset, y_offset)

        x_offset += TILE_SIZE+TILE_SIZE*.25

##############################################################################

############################### UI Interaction ###############################

def handle_element_clicked():
    pos = pygame.mouse.get_pos();
    player = game.state.GetCurrentPlayer()
    if (game.play_button.Collide(pos)):
        game.play_button.Press("play_press", pos)

    elif (game.reset_button.Collide(pos)):
        game.reset_button.Press("reset_press", pos)

    elif (game.skip_button.Collide(pos)):
        game.skip_button.Press("skip_press", pos)

    elif (game.done_button.Collide(pos)):
        game.done_button.Press("done_press", pos)

    elif (player.bank.Collide(pos)):
        left_mouse_pressed = pygame.mouse.get_pressed()[0]
        right_mouse_pressed = pygame.mouse.get_pressed()[2]
        if (left_mouse_pressed):
            player.bank.Press("bank_left_mouse", pos)
        elif (right_mouse_pressed):
            player.bank.Press("bank_right_mouse", pos)

    elif (game.BoardCollide(pos)):
        player.HandleLeftMousePress()

##############################################################################

player_options = ['Human Player', 'AI Player']
player1_question = [
    inquirer.List('player1',
                  message="Player 1",
                  choices=player_options)
]
player2_question = [
    inquirer.List('player2',
                  message="Player 2",
                  choices=player_options)
]

def main():
    player1_choice = inquirer.prompt(player1_question)
    player2_choice = inquirer.prompt(player2_question)


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quadra')

    small_font = pygame.font.Font(FONT_PATH, SMALL_FONT_SIZE)
    letter_font = pygame.font.Font(FONT_PATH, LETTER_FONT_SIZE)

    global letter_bag
    letter_bag = []
    for key in letter_distribution:
        for i in range(0, letter_distribution[key]):
            letter_bag.append(key)

    random.shuffle(letter_bag)
    current_letter = iter(letter_bag)

    global game
    if (os.path.exists("word_tree_obj.pkl")):
        game = GameManager(current_letter, "word_tree_obj.pkl")
    else:
        game = GameManager(current_letter, "dictionary.txt")

    global player1
    match (player1_choice['player1']):
        case "Human Player":
            player1 = Player(screen, small_font, letter_font, game.state.tiles_placed_on_turn, game.state.discard_pile, game.state.placed_tiles)
            player1.bank.events.Subscribe("bank_left_mouse", player1)
            player1.bank.events.Subscribe("bank_right_mouse", player1)
            game.skip_button.events.Subscribe("skip_press", player1)
            game.done_button.events.Subscribe("done_press", player1)
            game.play_button.events.Subscribe("play_press", player1)
            game.reset_button.events.Subscribe("reset_press", player1)
        case "AI Player":
            player1 = AIPlayer(game.state.tiles_placed_on_turn, game.state.discard_pile, game.state.placed_tiles, game.evaluator)

    global player2
    match (player2_choice['player2']):
        case "Human Player":
            player2 = Player(screen, small_font, letter_font, game.state.tiles_placed_on_turn, game.state.discard_pile, game.state.placed_tiles)
            player2.bank.events.Subscribe("bank_left_mouse", player2)
            player2.bank.events.Subscribe("bank_right_mouse", player2)
            game.skip_button.events.Subscribe("skip_press", player2)
            game.done_button.events.Subscribe("done_press", player2)
            game.play_button.events.Subscribe("play_press", player2)
            game.reset_button.events.Subscribe("reset_press", player2)
        case "AI Player":
            player2 = AIPlayer(game.state.tiles_placed_on_turn, game.state.discard_pile, game.state.placed_tiles, game.evaluator)

    running = True
    clock = pygame.time.Clock()

    game.state.players.append(player1)
    game.state.players.append(player2)
    game.InitPlayer(player1)
    game.InitPlayer(player2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.MOUSEBUTTONDOWN and not game.state.game_over):
                handle_element_clicked()

        game.Update()

        screen.fill(BG_COLOR)
        
        draw_board(screen, small_font, letter_font)
        draw_ui(screen, small_font, letter_font)
        draw_discard_pile(screen, small_font, letter_font)
        if (game.state.player_turn == 0):
            player1.Draw()
        else:
            player2.Draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
