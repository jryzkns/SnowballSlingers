import pygame as pg
import re
from definitions import *

from entity import Player, Snowball
from particles import Particles

player_dis_rgx = re.compile( r'([\da-f]{32})-player-disconn' )
player_hit_rgx = re.compile( r'([\da-f]{32})-player-hit' )
player_ack_rgx = re.compile( r'([\da-f]{32})-player-ack' )
player_pos_rgx = re.compile( r'([\da-f]{32})-player-\((\d{1,3}),\s+(\d{1,3})\)' )
snowball_pos_rgx = re.compile( r'([\da-f]{32})-snowball-\((\d{1,3}),\s+(\d{1,3})\)' )
snowball_ded_rgx = re.compile( r'([\da-f]{32})-snowball-gone' )

def gameSession( game_win, cm ):

    game_objs = {}
    particles = Particles()
    right_is_clicked = False

    game_clock, dt = pg.time.Clock(), 0
    game_clock.tick()

    cm.do_init_session()
    player_uuid = cm.pid

    should_stop = False
    while not should_stop:

        for msg in cm.do_subscribe():

            r = snowball_pos_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                p_x, p_y = int( r.group( 2 ) ), int( r.group( 3 ) )
                if p_name not in game_objs:
                    game_objs[ p_name ] = Snowball( p_name, p_x, p_y )
                game_objs[ p_name ].goto( p_x, p_y )
                continue

            r = snowball_ded_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                if p_name in game_objs:
                    sb = game_objs[ p_name ]
                    particles.emit( 50, sb.x, sb.y, sb.direction() )
                    del game_objs[ p_name ]
                continue

            r = player_ack_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                if p_name not in game_objs:
                    continue
                game_objs[ p_name ].cd_countdown = CD_DURATION
                continue

            r = player_dis_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                if p_name == player_uuid:
                    return
                if p_name in game_objs:
                    del game_objs[ p_name ]
                continue

            r = player_pos_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                p_x, p_y = int( r.group( 2 ) ), int( r.group( 3 ) )
                if p_name not in game_objs:
                    game_objs[ p_name ] = Player( p_name, p_x, p_y,
                                                  p_name == player_uuid )
                game_objs[ p_name ].goto( p_x, p_y )
                continue

            r = player_hit_rgx.match( msg )
            if r:
                p_name = r.group( 1 )
                if p_name not in game_objs:
                    continue
                game_objs[ p_name ].hit()
                continue

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL:
                    pg.event.set_grab( not pg.event.get_grab() )
                elif event.key == pg.K_SPACE:
                    cm.do_handle( 'cast', pg.mouse.get_pos() )
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == MOUSE_RIGHT_CLICK:
                    right_is_clicked = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == MOUSE_RIGHT_CLICK:
                    right_is_clicked = False

        if right_is_clicked:
            cm.do_handle( 'click', pg.mouse.get_pos() )

        game_win.fill( INDIGO )

        dt = game_clock.get_time()/1000.
        particles.update( dt )
        for entity in game_objs.values():
            if hasattr( entity, 'update' ):
                entity.update( dt )
            entity.draw( game_win )

        particles.draw( game_win )

        pg.display.flip()
        game_clock.tick()

