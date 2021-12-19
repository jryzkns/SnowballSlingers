from definitions import *
import pygame as pg

from buttonPress import Button
from textBox import TextBox

def loginPage(login):
    # screen = pg.display.set_mode((300, 200))
    login.fill(INDIGO)
    # input_box = TextBox(50, 100, 200, 32)
    # input_box.draw(screen)
    # button = Button(50, 20, "Click here", (50,50), 30, "white")
    # button.draw_button(screen)
    pg.draw.circle(login, (0,0,0), (150,150), (5))
    pg.display.flip()

    # done = False
    # while not done:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             sys.exit(0)
            