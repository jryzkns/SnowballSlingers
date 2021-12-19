import pygame as pg
from definitions import *

class TextBox(pg.Rect):
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = RED
        self.text = text
        self.active = False

    def on_user_input(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    result = self.text
                    print(result)
                    self.text = ''
                    return result
                if event.key == pg.K_BACKSPACE:
                    self.text = self.txt[:-1]
                else:
                    self.text += event.unicode
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)