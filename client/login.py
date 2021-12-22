from definitions import *
import pygame as pg
import re

from buttonPress import Button
from textBox import TextBox

def loginPage(screen):
    address_regex = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)$")
    input_box = TextBox(50, 80, 200, 32, address_regex)
    button = Button(90, 30, "Connect", (50,130))
    font = pg.font.Font(asset('CaviarDreams.ttf'), 18)
    text = font.render("Welcome to Snowball Slingers.", True, BLACK)
    text2 = font.render("Please enter the server IP address into the text box below.", True, BLACK)
    text3 = font.render("Click the Connect button after you have entered the IP address", True, BLACK)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                input_box.on_mousebuttondown(event.pos)
                if button.on_mousebuttondown(event.pos):
                    return input_box.text_input
            elif event.type == pg.KEYDOWN:
                if input_box.active:
                    input_box.on_keydown(event.key)
                    button.active = input_box.valid
        screen.fill(INDIGO)
        screen.blit(text, (20, 10))
        screen.blit(text2, (20, 30))
        screen.blit(text3, (20, 50))
        input_box.draw(screen)
        button.draw(screen)
        pg.display.flip()
        