import pygame as pg
from definitions import *

class Button(pg.Rect):
    def __init__(self, w, h, text, position):
        pg.Rect.__init__(self, *position, w, h)
        self.font = pg.font.Font(asset('CaviarDreams.ttf'), 18)
        self.text = self.font.render(text, True, BLACK)
        self.active = False
    
    def on_mousebuttondown(self, position):
        return self.active and pg.mouse.get_pressed()[0] and self.collidepoint(*position)
    
    def draw(self, screen):
        screen.blit(self.text, self.topleft)
        pg.draw.rect(screen, (ORANGE if self.active else BANANA), self, 2)
