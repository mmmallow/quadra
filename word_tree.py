import pickle
import os
import sys

class LetterNode:
    def __init__(self, letter, is_word_end):
        self.letter = letter
        self.is_word_end = is_word_end
        self.children = []

class WordTree:
    def __init__(self, file_name):
        self.head = LetterNode("", False)

        with open(file_name, 'r') as f:
            for line in f:
                word = line.strip('\n')
                self.add_word(word.upper())

        with open("word_tree_obj.pkl", "wb") as f:
            pickle.dump(self, f)

    def add_word(self, word):
        cur_children = self.head.children
        i = 0
        while (i < len(word)):
            result = list(filter(lambda x: x.letter == word[i], cur_children))
            if (len(result)):
                if (i == len(word)-1):
                    result[0].is_word_end = True
                cur_children = result[0].children
                i += 1
            else:
                is_word_end = False
                if (i == len(word)-1):
                    is_word_end = True
                cur_children.append(LetterNode(word[i], is_word_end))

    # TODO: Change to recursive function and/or use queue to account for blank tiles
    def check_word(self, word):
        cur_children = self.head.children
        i = 0
        while (i < len(word) and len(cur_children) != 0):
            result = list(filter(lambda x: x.letter == word[i], cur_children))
            if (len(result)):
                cur_children = result[0].children
                if (i == len(word)-1):
                    if (result[0].is_word_end):
                        return True
                    else:
                        return False
                i += 1
            else:
                return False

    def print_tree(self):
        cur_children = self.head.children
        while (len(cur_children) != 0):
            print(cur_children[0].letter)
            cur_children = cur_children[0].children

    def get_sizeof_node(self, node):
        size = 0
        if (len(node.children) == 0):
            return sys.getsizeof(node)
        for child in node.children:
            size += self.get_sizeof_node(child)

        return size
