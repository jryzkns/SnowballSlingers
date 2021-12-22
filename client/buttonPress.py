import pygame as pg
from definitions import *

class Button(pg.Rect):
    def __init__(self, w, h, text, position):
        pg.Rect.__init__(self, *position, w, h)
        self.font = pg.font.Font(asset('CaviarDreams.ttf'), 18)
        self.text = self.font.render(text, True, BLACK)
        self.color_inactive = BANANA
        self.color_active = ORANGE
        self.active = False
    
    def on_mousebuttondown(self, position):
        return self.active and pg.mouse.get_pressed()[0] and self.collidepoint(*position)
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.text, self.topleft)
            pg.draw.rect(screen, self.color_inactive, self, 2)