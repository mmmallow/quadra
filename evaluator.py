import os
from common import *
from word_tree import *

class Evaluator:
    def __init__(self, tiles_placed_on_turn, placed_tiles, dict_file, state):
        self.tiles_placed_on_turn = tiles_placed_on_turn
        self.placed_tiles = placed_tiles
        self.state = state

        extension = os.path.splitext(dict_file)[1]
        if (extension == ".txt"):
            self.word_tree = WordTree(dict_file)
        elif (extension == ".pkl"):
            with open(dict_file, 'rb') as f:
                self.word_tree = pickle.load(f)

    # Returns every word formed this turn as a list of cells, with the main word
    # first. Returns [] and sets the error message if the move isn't legal
    def Evaluate(self):
        if (len(self.tiles_placed_on_turn) == 0):
            self.state.err_message = "Must play a\nword"
            return []
        if (self.state.is_first_move and (7, 7) not in self.tiles_placed_on_turn):
            self.state.err_message = "Middle tile\nmust be used\non first turn"
            return []

        tiles = sorted(self.tiles_placed_on_turn)

        if (any(tile in self.placed_tiles for tile in tiles)):
            self.state.err_message = "Space already\ntaken"
            return []

        # Check if the placed tiles are in a line
        horiz = 0
        vert  = 0
        if (len(tiles) > 1):
            horiz = 1 if all(tile[1] == tiles[0][1] for tile in tiles) else 0
            vert  = 1 if all(tile[0] == tiles[0][0] for tile in tiles) else 0

            if (horiz == 0 and vert == 0):
                self.state.err_message = "Tiles must be\nin a straight\nline"
                return []
        else:
            x, y = tiles[0]
            if (((x+1, y) in self.placed_tiles) or ((x-1, y) in self.placed_tiles)):
                horiz = 1
            elif (((x, y+1) in self.placed_tiles) or ((x, y-1) in self.placed_tiles)):
                vert = 1
            else:
                self.state.err_message = "Must use\ntiles already\nplaced"
                return []

        main_word = get_word_cells(self.placed_tiles, self.tiles_placed_on_turn, tiles[0][0], tiles[0][1], horiz, vert)

        if (any(tile not in main_word for tile in tiles)):
            self.state.err_message = "Tiles must\nnot have gaps"
            return []

        if (len(main_word) < 2):
            self.state.err_message = "Words must\nbe at least\n2 letters\nlong"
            return []

        words = [main_word]

        # Check that tiles placed this turn form words with any other placed tiles
        for x, y in tiles:
            cross_word = get_word_cells(self.placed_tiles, self.tiles_placed_on_turn, x, y, vert, horiz)
            if (len(cross_word) > 1):
                words.append(cross_word)

        # The move can connect through the main word or through any cross word
        connected = any(cell in self.placed_tiles for word in words for cell in word)
        if (not self.state.is_first_move and not connected):
            self.state.err_message = "Must use\ntiles already\nplaced"
            return []

        for cells in words:
            word = cells_to_word(self.placed_tiles, self.tiles_placed_on_turn, cells)
            if (not self.word_tree.check_word(word)):
                self.state.err_message = f"Invalid word:\n{word}"
                return []

        return words

    def Score(self, words):
        score = sum(self.score_word(cells) for cells in words)
        if (len(self.tiles_placed_on_turn) == BANK_SIZE):
            score += BINGO_BONUS
        return score

    # Every letter in a word counts, but premium squares only apply to tiles placed
    # this turn. A new tile's premium applies to each word it's part of
    def score_word(self, cells):
        score = 0
        multiplier = 1
        for cell in cells:
            value = letter_values[get_letter(self.placed_tiles, self.tiles_placed_on_turn, cell)]
            if (cell in self.tiles_placed_on_turn):
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
