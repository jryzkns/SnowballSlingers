from definitions import *
import pygame as pg

from buttonPress import Button

def endScreen(screen, address):
    print("hello world")
    button_rejoin = Button(90, 30, "Rejoin", (50,130))
    backToLogin = Button(200, 30, "Return to Login Screen", (50,180))
    
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                button_rejoin.active = True
                backToLogin.active = True
                print("mouse button down")
                if button_rejoin.on_mousebuttondown(event.pos):
                    print("rejoin pressed")
                    return address
                elif backToLogin.on_mousebuttondown(event.pos):
                    print("back to login")
                    return 0
        screen.fill(INDIGO)
        button_rejoin.draw(screen)
        backToLogin.draw(screen)
        pg.display.flip()