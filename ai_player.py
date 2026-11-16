import pygame
import time
import BitVector as bv
from common import *
from bank import Bank

class AIPlayer:
    def __init__(self, tiles_placed_on_turn, discard_pile, placed_tiles, evaluator):
        self.bank = Bank()
        self.score = 0
        self.is_done = False
        self.state = PlayerState.WAITING
        self.highest_scoring_move = {}
        self.highest_score = 0
        self.can_handle_ui = False

        self.tiles_placed_on_turn = tiles_placed_on_turn
        self.discard_pile = discard_pile
        self.placed_tiles = placed_tiles
        self.evaluator = evaluator

        # Has shape:
        # {0, 0}: BitVector(intVal = 0, size = 26)
        self.across_checks = {}
        self.down_checks = {}
        self.across_anchors = []
        self.down_anchors = []

        # Tracking how long a move takes to generate (to be averaged later)
        self.move_gen_times = []

        self.InitCrossChecks()

    def InitCrossChecks(self):
        for y in range(0, 15):
            for x in range(0, 15):
                # All spaces are initially empty, therefore letter is technically playable at any space
                self.across_checks[(x,y)] = bv.BitVector(intVal = 0b11111111111111111111111111, size = 26)
                self.down_checks[(x,y)]   = bv.BitVector(intVal = 0b11111111111111111111111111, size = 26)

    def Draw(self):
        pass

    def Reset(self):
        for tile in self.tiles_placed_on_turn:
            index = self.bank.bank.index("")
            self.bank.bank[index] = self.tiles_placed_on_turn[tile]

        for tile in self.discard_pile:
            index = self.bank.bank.index("")
            self.bank.bank[index] = tile
        self.tiles_placed_on_turn.clear()
        self.discard_pile.clear()

    def PlayTurn(self):
        # Update cross checks and anchor squares after new tiles have been placed
        time0 = time.time()
        self.UpdateCrossChecksAndAnchors()
        if (self.evaluator.state.is_first_move):
            self.across_anchors.append((7, 7))
            self.down_anchors.append((7, 7))

        self.GenerateMoves()
        for tile in self.highest_scoring_move:
            self.tiles_placed_on_turn[tile] = self.highest_scoring_move[tile]
            index = self.bank.bank.index(self.highest_scoring_move[tile])
            self.bank.bank[index] = ""
        time1 = time.time()

        # Clean up
        self.state = PlayerState.DONE_MOVING
        self.across_anchors.clear()
        self.down_anchors.clear()
        self.highest_scoring_move.clear()
        self.highest_score = 0

        self.move_gen_times.append(time1-time0)

    def UpdateCrossChecksAndAnchors(self):
        for tile in self.placed_tiles:
            x, y = tile
            if ((x, y+1) not in self.placed_tiles and on_board((x, y+1))):
                if ((x, y+1) not in self.down_anchors):
                    self.down_anchors.append((x, y+1))
                for i in range(0, 26):
                    self.tiles_placed_on_turn[(x, y+1)] = letters[i]
                    if (self.evaluator.Evaluate()):
                        self.across_checks[(x, y+1)][i] = 1
                    else:
                        self.across_checks[(x, y+1)][i] = 0

                    self.tiles_placed_on_turn.clear()

            if ((x, y-1) not in self.placed_tiles and on_board((x, y-1))):
                if ((x, y-1) not in self.down_anchors):
                    self.down_anchors.append((x, y-1))
                for i in range(0, 26):
                    self.tiles_placed_on_turn[(x, y-1)] = letters[i]
                    if (self.evaluator.Evaluate()):
                        self.across_checks[(x, y-1)][i] = 1
                    else:
                        self.across_checks[(x, y-1)][i] = 0

                    self.tiles_placed_on_turn.clear()

            if ((x+1, y) not in self.placed_tiles and on_board((x+1, y))):
                if ((x+1, y) not in self.across_anchors):
                    self.across_anchors.append((x+1, y))
                for i in range(0, 26):
                    self.tiles_placed_on_turn[(x+1, y)] = letters[i]
                    if (self.evaluator.Evaluate()):
                        self.down_checks[(x+1, y)][i] = 1
                    else:
                        self.down_checks[(x+1, y)][i] = 0

                    self.tiles_placed_on_turn.clear()

            if ((x-1, y) not in self.placed_tiles and on_board((x-1, y))):
                if ((x-1, y) not in self.across_anchors):
                    self.across_anchors.append((x-1, y))
                for i in range(0, 26):
                    self.tiles_placed_on_turn[(x-1, y)] = letters[i]
                    if (self.evaluator.Evaluate()):
                        self.down_checks[(x-1, y)][i] = 1
                    else:
                        self.down_checks[(x-1, y)][i] = 0

                    self.tiles_placed_on_turn.clear()


    def GenerateMoves(self):
        for anchor in self.across_anchors:
            self.LeftPart("", self.evaluator.word_tree.head, anchor, 1, self.GetAnchorLimit(anchor, (-1, 0)))
        for anchor in self.down_anchors:
            self.UpPart("", self.evaluator.word_tree.head, anchor, 1, self.GetAnchorLimit(anchor, (0, -1)))


    def GetAnchorLimit(self, anchor, dir):
        count = 0
        x, y = anchor
        x += dir[0]
        y += dir[1]
        while ((x, y) not in self.placed_tiles and x >= 0 and y >= 0):
            if (dir[0] != 0 and (x, y) not in self.across_anchors):
                count += 1
            elif (dir[1] != 0 and (x, y) not in self.down_anchors):
                count += 1

            x += dir[0]
            y += dir[1]

        return count

    def LeftPart(self, part_word, node, anchor, anchor_offset, limit):
        self.ExtendRight(part_word, node, anchor)
        if (limit > 0):
            for letter in node.children:
                if (letter.letter in self.bank.bank):
                    self.tiles_placed_on_turn[(anchor[0]-anchor_offset, anchor[1])] = letter.letter
                    index = self.bank.bank.index(letter.letter)
                    self.bank.bank[index] = ""
                    part_word = letter.letter + part_word

                    self.LeftPart(part_word, letter, anchor, anchor_offset+1, limit-1)

                    self.bank.bank[index] = letter.letter
                    del self.tiles_placed_on_turn[(anchor[0]-anchor_offset, anchor[1])]

    def ExtendRight(self, part_word, node, square):
        if (square not in self.placed_tiles):
            if (node.is_word_end):
                self.LegalMove()
            for letter in node.children:
                if (letter.letter in self.bank.bank and self.LetterInCrossCheckSet(letter.letter, square, across=True)):
                    self.tiles_placed_on_turn[square] = letter.letter
                    index = self.bank.bank.index(letter.letter)
                    self.bank.bank[index] = ""

                    part_word += letter.letter
                    self.ExtendRight(part_word, letter, (square[0]+1, square[1]))

                    self.bank.bank[index] = letter.letter
                    del self.tiles_placed_on_turn[square]
        else:
            l = self.placed_tiles[square]
            result = list(filter(lambda x: x.letter == l, node.children))
            if (len(result)):
                part_word += node.letter
                self.ExtendRight(part_word, result[0], (square[0]+1, square[1]))

    def UpPart(self, part_word, node, anchor, anchor_offset, limit):
        self.ExtendDown(part_word, node, anchor)
        if (limit > 0):
            for letter in node.children:
                if (letter.letter in self.bank.bank):
                    self.tiles_placed_on_turn[(anchor[0], anchor[1]-anchor_offset)] = letter.letter
                    index = self.bank.bank.index(letter.letter)
                    self.bank.bank[index] = ""
                    part_word = letter.letter + part_word

                    self.UpPart(part_word, letter, anchor, anchor_offset+1, limit-1)

                    self.bank.bank[index] = letter.letter
                    del self.tiles_placed_on_turn[(anchor[0], anchor[1]-anchor_offset)]

    def ExtendDown(self, part_word, node, square):
        if (square not in self.placed_tiles):
            if (node.is_word_end):
                self.LegalMove()
            for letter in node.children:
                if (letter.letter in self.bank.bank and self.LetterInCrossCheckSet(letter.letter, square, across=False)):
                    self.tiles_placed_on_turn[square] = letter.letter
                    index = self.bank.bank.index(letter.letter)
                    self.bank.bank[index] = ""

                    part_word += letter.letter
                    self.ExtendDown(part_word, letter, (square[0], square[1]+1))

                    self.bank.bank[index] = letter.letter
                    del self.tiles_placed_on_turn[square]
        else:
            l = self.placed_tiles[square]
            result = list(filter(lambda x: x.letter == l, node.children))
            if (len(result)):
                part_word += node.letter
                self.ExtendDown(part_word, result[0], (square[0], square[1]+1))

    def LetterInCrossCheckSet(self, letter, square, across):
        index = letters.index(letter)
        if (square[0] < 0 or square[0] >= 15 or square[1] < 0 or square[1] >= 15):
            return False

        if (across):
            bit_vec = self.across_checks[square]
        else:
            bit_vec = self.down_checks[square]

        if (bit_vec[index]):
            return True
        else:
            return False

    def LegalMove(self):
        words = self.evaluator.Evaluate()

        if (words):
            score = self.evaluator.Score(words)
            if (score > self.highest_score):
                self.highest_scoring_move = self.tiles_placed_on_turn.copy()
                self.highest_score = score
