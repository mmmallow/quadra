import pygame
from common import *
from event_manager import EventManager

class Bank:
    def __init__(self):
        self.bank = ["", "", "", "", "", "", ""]
        self.rect = pygame.Rect(PLAYER_BANK_X, PLAYER_BANK_Y, PLAYER_BANK_WIDTH, PLAYER_BANK_HEIGHT)
        self.events = EventManager()

    def Draw(self, screen, small_font, letter_font):
        orig_x = self.rect.x
        y = self.rect.y
        x = orig_x
        for i in range(0, 7):
            x = orig_x + i * (TILE_SIZE + PLAYER_BANK_PADDING)
            if (self.bank[i] != ""):
                draw_tile(screen, small_font, letter_font, TILE_COLOR, self.bank[i], x, y)

    def Press(self, event, data):
        self.events.Notify(event, data)

    def Collide(self, pos):
        return self.rect.collidepoint(pos)

    def GetTile(self, index):
        return pygame.Rect(self.rect.x + index*(TILE_SIZE + PLAYER_BANK_PADDING)-PLAYER_BANK_PADDING, PLAYER_BANK_Y, TILE_SIZE, TILE_SIZE)
