import pygame
from common import *
from event_manager import EventManager

class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.events = EventManager()

    def Press(self, event, data):
        self.events.Notify(event, data)

    def Collide(self, pos):
        return self.rect.collidepoint(pos)
