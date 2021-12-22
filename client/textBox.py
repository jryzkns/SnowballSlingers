import pygame as pg
from definitions import *

class TextBox(pg.Rect):
    def __init__(self, x, y, w, h, matcher = None):
        pg.Rect.__init__(self, x, y, w, h)
        self.font = pg.font.Font(asset('CaviarDreams.ttf'), 18)
        self.text_input = ''
        self.text = self.font.render(self.text_input, True, BLACK)
        self.active = False
        self.matcher = matcher
        self.valid = False

    def on_mousebuttondown(self, position):
        self.active = self.collidepoint(position)

    def on_keydown(self, key):
        if key == pg.K_RETURN:
            if self.valid:
                pass
        else:
            if key == pg.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            else:
                self.text_input += pg.key.name(key)
            self.text = self.font.render(self.text_input, True, BLACK)
            self.valid = self.matcher.match(self.text_input) is not None
    
    def draw(self, screen):
        screen.blit(self.text, self.topleft)
        pg.draw.rect(screen, (ORANGE if self.active else BANANA), self, 2)
