import pygame as pg
from definitions import *

class Button:
    def __init__(self, w, h, text, position, bg='white'):
        self.x, self.y = position
        self.rect = pg.Rect(position[0], position[1], w, h)
        self.font = pg.font.Font('CaviarDreams.ttf', 20)
        self.text = text
        self.color = RED
    
    def mouse_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                return 1
        return 0
    
    def clicked(self):
        x, y = pg.mouse.get_pos()
        if self.rect.collidepoint(x,y):
            return 1
        return 0
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)