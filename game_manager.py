import pygame
from common import *
from button import Button
from game_state import GameState
from evaluator import Evaluator
from event_listener import EventListener

class GameManager(EventListener):
    def __init__(self, current_letter, dict_file):
        self.state = GameState(current_letter, dict_file)
        self.evaluator = Evaluator(self.state, dict_file)

        self.play_button = Button(PLAY_BUTTON_X, PLAY_BUTTON_Y, TILE_SIZE, TILE_SIZE)
        self.reset_button = Button(RESET_BUTTON_X, RESET_BUTTON_Y, TILE_SIZE, TILE_SIZE)
        self.skip_button = Button(SKIP_BUTTON_X, SKIP_BUTTON_Y, TILE_SIZE, TILE_SIZE)
        self.done_button = Button(DONE_BUTTON_X, DONE_BUTTON_Y, TILE_SIZE, TILE_SIZE)

    def PlayerIsDone(self):
        player = self.state.GetCurrentPlayer()
        self.state.discard_pile.clear()
        self.state.SwitchPlayer()
        self.state.turns_without_move += 1
        player.is_done = True
        player.state = PlayerState.WAITING
        self.CheckGameOver()

    def Update(self):
        if (not self.state.game_over):
            player = self.state.GetCurrentPlayer()
            if (player.state == PlayerState.DONE_MOVING):
                self.PlayTurn()
            elif (player.state == PlayerState.WAITING):
                player.state = PlayerState.MOVING
            elif (player.state == PlayerState.MOVING):
                player.PlayTurn()

    def BoardCollide(self, pos):
        board = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
        return board.collidepoint(pos)

    def Listen(self, event, data):
        match (event):
            case "skip_press":
                self.SkipTurn()
            case "done_press":
                self.PlayerIsDone()

    def SkipTurn(self):
        player = self.state.GetCurrentPlayer()
        self.state.discard_pile.clear()
        self.state.err_message = ""
        self.InitPlayer(player)
        self.state.SwitchPlayer()
        player.state = PlayerState.WAITING
        self.state.turns_without_move += 1
        self.CheckGameOver()

    def PlayTurn(self):
        words = []

        if (len(self.state.tiles_placed_on_turn) == 0):
            self.SkipTurn()
            return
        else:
            self.state.display_err_message = True
            words = self.evaluator.Evaluate()

        player = self.state.GetCurrentPlayer()
        if (words):
            # Valid move. Score before the tiles are committed, since premium
            # squares only count for tiles placed this turn
            player.score += self.evaluator.Score(words)
            if (len(self.state.discard_pile) > 0):
                for tile in self.state.discard_pile:
                    index = player.bank.bank.index("")
                    player.bank.bank[index] = tile
                self.state.discard_pile.clear()
            self.InitPlayer(player)

            for tile in self.state.tiles_placed_on_turn:
                self.state.placed_tiles[(tile)] = self.state.tiles_placed_on_turn[tile]

            print([cells_to_word(self.state.placed_tiles, self.state.tiles_placed_on_turn, word) for word in words])

            self.state.tiles_placed_on_turn.clear()
            self.state.is_first_move = False

            self.state.SwitchPlayer()

            player.state = PlayerState.WAITING
            self.state.err_message = ""
            self.state.turns_without_move = 0
        else:
            player.state = PlayerState.MOVING

        self.CheckGameOver()

    def InitPlayer(self, player):
        for i in range(0,BANK_SIZE):
            if (player.bank.bank[i] == ""):
                try:
                    player.bank.bank[i] = next(self.state.current_letter)
                except:
                    self.state.letter_bag_empty = True

    def CheckGameOver(self):
        if (self.state.turns_without_move >= 6):
            self.EndGame()
        elif (self.state.players[0].is_done and self.state.players[1].is_done):
            self.EndGame()
        elif (self.state.letter_bag_empty and all(c == "" for c in self.state.players[0].bank.bank) and all(c == "" for c in self.state.players[1].bank.bank)):
            self.EndGame()

    def EndGame(self):
        self.state.game_over = True
        self.state.err_message = ""
        winner = "Player 1" if self.state.players[0].score > self.state.players[1].score else "Player 2"
        self.state.win_message = winner + " wins!"
