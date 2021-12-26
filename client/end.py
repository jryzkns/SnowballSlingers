from definitions import *
import pygame as pg

from buttonPress import Button

def endScreen(screen):
    button_rejoin = Button(90, 30, "Rejoin", (50,130))
    back_to_login = Button(200, 30, "Return to Login Screen", (50,180))
    
    done = False
    REJOIN = True
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rejoin.collidepoint(event.pos):
                    button_rejoin.active = True
                    if button_rejoin.on_mousebuttondown(event.pos):
                        return REJOIN
                elif back_to_login.collidepoint(event.pos):
                    back_to_login.active = True
                    if back_to_login.on_mousebuttondown(event.pos):
                        return not REJOIN
        screen.fill(INDIGO)
        button_rejoin.draw(screen)
        back_to_login.draw(screen)
        pg.display.flip()
