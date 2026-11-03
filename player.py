import pygame
from common import *

class Player:
    def __init__(self, screen, small_font, letter_font, tiles_placed_on_turn):
        self.bank = ["", "", "", "", "", "", ""]
        self.held_letter = ""
        self.score = 0

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

    def Reset(self):
        for tile in self.tiles_placed_on_turn:
            index = self.bank.index("")
            self.bank[index] = self.tiles_placed_on_turn[tile]
        self.tiles_placed_on_turn.clear()

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


