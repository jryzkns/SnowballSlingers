import pygame as pg
import zmq
import re
from definitions import *

from entity import Player, Snowball
from particles import Particles

class GameSession:
    def run_session(zmq_ctx, game_win, player_uuid):

        game_objs = {}

        particles = Particles()

        right_is_clicked = False

        player_dis_regex = re.compile(r'([\da-f]{32})-player-disconn')
        player_hit_regex = re.compile(r'([\da-f]{32})-player-hit')
        player_ack_regex = re.compile(r'([\da-f]{32})-player-ack')
        player_pos_regex = re.compile(r'([\da-f]{32})-player-\((\d{1,3}),\s+(\d{1,3})\)')
        snowball_pos_regex = re.compile(r'([\da-f]{32})-snowball-\((\d{1,3}),\s+(\d{1,3})\)')
        snowball_ded_regex = re.compile(r'([\da-f]{32})-snowball-gone')

        skt_hand = zmq_ctx.socket(zmq.PUSH)
        skt_hand.connect(f"tcp://{ADDRESS}:{PORT_HAND}")

        skt_subs = zmq_ctx.socket(zmq.SUB)
        skt_subs.setsockopt(zmq.SUBSCRIBE, b"U")
        skt_subs.connect(f"tcp://{ADDRESS}:{PORT_SUBS}")

        game_clock, dt = pg.time.Clock(), 0
        game_clock.tick()

        should_stop = False
        while not should_stop:

            incoming = []
            while True:
                try:
                    incoming += skt_subs.recv(zmq.NOBLOCK).decode(UTF8)[2:],
                except:
                    break

            for msg in incoming:

                r = snowball_pos_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    p_x, p_y = int(r.group(2)), int(r.group(3))
                    if p_name not in game_objs:
                        game_objs[p_name] = Snowball(p_name, p_x, p_y)
                    game_objs[p_name].goto(p_x, p_y)
                    continue

                r = snowball_ded_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    if p_name in game_objs:
                        particles.emit(30, game_objs[p_name].x, game_objs[p_name].y)
                        del game_objs[p_name]
                    continue

                r = player_ack_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    if p_name not in game_objs:
                        continue
                    game_objs[p_name].cd_countdown = CD_DURATION

                r = player_dis_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    if p_name == player_uuid:
                        return not SHOULD_STOP_GAME
                    if p_name in game_objs:
                        del game_objs[p_name]
                    continue

                r = player_pos_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    p_x, p_y = int(r.group(2)), int(r.group(3))
                    if p_name not in game_objs:
                        game_objs[p_name] = Player(p_name, p_x, p_y, p_name == player_uuid)
                    game_objs[p_name].goto(p_x, p_y)
                    continue
                
                r = player_hit_regex.match(msg)
                if r is not None:
                    p_name = r.group(1)
                    if p_name not in game_objs:
                        continue
                    game_objs[p_name].hit()
                    continue

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return SHOULD_STOP_GAME
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LCTRL:
                        pg.event.set_grab(not pg.event.get_grab())
                    elif event.key == pg.K_SPACE:
                        skt_hand.send(f"{player_uuid}-cast-{pg.mouse.get_pos()}".encode(UTF8))
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == MOUSE_RIGHT_CLICK:
                        right_is_clicked = True
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == MOUSE_RIGHT_CLICK:
                        right_is_clicked = False

            if right_is_clicked:
                skt_hand.send(f"{player_uuid}-click-{pg.mouse.get_pos()}".encode(UTF8))             

            game_win.fill(INDIGO)

            dt = game_clock.get_time()/1000.
            particles.update(dt)
            for _, entity in game_objs.items():
                if hasattr(entity, 'update'):
                    entity.update(dt)
                entity.draw(game_win)

            particles.draw(game_win)

            pg.display.flip()
            game_clock.tick()

        return SHOULD_STOP_GAME
