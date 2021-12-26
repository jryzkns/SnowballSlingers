from definitions import *
import pygame as pg

from buttonPress import Button

SHOULD_REJOIN = True

def endScreen(screen):
    print("hello world")
    button_rejoin = Button(90, 30, "Rejoin", (50,130))
    backToLogin = Button(200, 30, "Return to Login Screen", (50,180))
    
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.MOUSEBUTTONDOWN:
                button_rejoin.active = button_rejoin.collidepoint(*event.pos)
                backToLogin.active = backToLogin.collidepoint(*event.pos)
                if button_rejoin.on_mousebuttondown(event.pos):
                    return SHOULD_REJOIN
                elif backToLogin.on_mousebuttondown(event.pos):
                    return not SHOULD_REJOIN
        screen.fill(INDIGO)
        button_rejoin.draw(screen)
        backToLogin.draw(screen)
        pg.display.flip()