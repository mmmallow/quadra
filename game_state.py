from common import *

class GameState:
    def __init__(self, current_letter, dict_file):
        self.players = []
        self.player_turn = 0
        self.err_message = ""
        self.display_err_message = False
        self.win_message = ""
        self.is_first_move = True
        self.letter_bag_empty = False
        self.turns_without_move = 0
        self.game_over = False
        # Stores all tiles placed by the players as index in spaces : letter
        # (0, 0): "A"
        self.placed_tiles = {}
        # Tiles placed during a player's turn. Temporary and is wiped after every turn
        self.tiles_placed_on_turn = {}

        # Tiles in to be removed from player's letter bank
        self.discard_pile = []
        self.current_letter = current_letter

    def GetCurrentPlayer(self):
        return self.players[self.player_turn]

    def SwitchPlayer(self):
        if (self.player_turn == 0 and not self.players[1].is_done):
            self.player_turn = 1
        elif (self.player_turn == 1 and not self.players[0].is_done):
            self.player_turn = 0

        self.players[self.player_turn].state = PlayerState.MOVING
        self.display_err_message = False

