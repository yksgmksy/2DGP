import random

from pico2d import *

import game_framework
import title_state
from Map import Map
from Hero import Hero

name = "MainState"\

font = None
hero = None
#my_map = None
font_X = 0
font_Y = 0

def enter():
    global hero, my_map, image, font
    hero = Hero()
    #my_map = Map()
    image = load_image('title.png')


def exit():
    global hero, my_map, tile_map, font
    del(hero)
    #del(my_map)
    del(font)

def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    # fill here
    global hero
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                pass
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT:
                    hero.Left_Check = True
                if event.key == SDLK_RIGHT:
                    hero.Right_Check = True
                if event.key == SDLK_UP and hero.Jump_Check == False and hero.herojump == True:
                    hero.Jump_Check = True
                    hero.herojump = False
                    hero.gravity = 0
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_LEFT:
                    hero.Left_Check = False
                if event.key == SDLK_RIGHT:
                    hero.Right_Check = False
                if event.key == SDLK_UP and hero.y <= 90:
                    hero.Jump_Check = False

def update(frame_time):
    hero.update(frame_time)

def draw(frame_time):
    clear_canvas()
    #my_map.draw()
    hero.draw()
    hero.draw_bb()
    update_canvas()







