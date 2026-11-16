import pygame
import time
from common import *
from event_listener import EventListener
from bank import Bank

class Player(EventListener):
    def __init__(self, screen, small_font, letter_font, tiles_placed_on_turn, discard_pile, placed_tiles):
        self.bank = Bank()
        self.held_letter = ""
        self.score = 0
        self.is_done = False
        self.state = PlayerState.WAITING
        self.debounce_time = 0

        self.screen = screen
        self.small_font = small_font
        self.letter_font = letter_font
        self.tiles_placed_on_turn = tiles_placed_on_turn
        self.discard_pile = discard_pile
        self.placed_tiles = placed_tiles

    def Draw(self):
        self.bank.Draw(self.screen, self.small_font, self.letter_font)

        if (self.held_letter != ""):
            mouse_pos = pygame.mouse.get_pos()
            pos = [0, 0]
            pos[0] = mouse_pos[0]-TILE_SIZE//2
            pos[1] = mouse_pos[1]-TILE_SIZE//2
            draw_tile(self.screen, self.small_font, self.letter_font, TILE_COLOR, self.held_letter, pos[0], pos[1])

    def Listen(self, event, data):
        match (event):
            case "play_press":
                self.state = PlayerState.DONE_MOVING
            case "reset_press":
                self.Reset()
            case "bank_left_mouse":
                self.HandleLeftMousePress()
            case "bank_right_mouse":
                self.HandleRightMousePress()
            case "board_press":
                self.HandleLeftMousePress()

    def PlayTurn(self):
        pass

    def Reset(self):
        for tile in self.tiles_placed_on_turn:
            if ("" in self.bank.bank):
                index = self.bank.bank.index("")
                self.bank.bank[index] = self.tiles_placed_on_turn[tile]

        for tile in self.discard_pile:
            if ("" in self.bank.bank):
                index = self.bank.bank.index("")
                self.bank.bank[index] = tile
        self.tiles_placed_on_turn.clear()
        self.discard_pile.clear()

    def HandleLeftMousePress(self):
        '''
        if (self.debounce_time == 0):
            self.debounce_time = time.time()
        else:
            if (time.time()-self.debounce_time <= DEBOUNCE_TIME):
                self.debounce_time = 0
            else:
                return
        '''

        mouse_pos = pygame.mouse.get_pos()
        if (self.held_letter == ""):
            for i in range(0,7):
                tile = self.bank.GetTile(i)
                if (tile.collidepoint(mouse_pos)):
                    if (self.held_letter != ""):
                        index = self.bank.bank.index("")
                        self.bank.bank[index] = self.held_letter
                    self.held_letter = self.bank.bank[i]
                    self.bank.bank[i] = ""
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
                    index = self.bank.bank.index("")
                    self.bank.bank[index] = self.tiles_placed_on_turn[(board_x, board_y)]
                if ((board_x, board_y) not in self.placed_tiles):
                    self.tiles_placed_on_turn[(board_x, board_y)] = self.held_letter
                    self.held_letter = ""
            else:
                index = self.bank.bank.index("")
                self.bank.bank[index] = self.held_letter
                self.held_letter = ""

    def HandleRightMousePress(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.held_letter == ""):
            for i in range(0, 7):
                tile = self.bank.GetTile(i)
                if (tile.collidepoint(mouse_pos)):
                    self.discard_pile.append(self.bank.bank[i])
                    self.bank.bank[i] = ""
                    break

