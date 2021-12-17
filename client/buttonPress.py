import pygame as pg

pg.init()
COLOR = pg.Color('red')

class Button:
    def __init__(self, w, h, text, position, font, bg='white'):
        self.x, self.y = position
        self.rect = pg.Rect(position[0], position[1], w, h)
        self.font = pg.font.SysFont("Arial", font)
        self.text = text
        self.color = COLOR
    
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
    
    def draw_button(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)