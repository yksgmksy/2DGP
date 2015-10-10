import game_framework
import main_state
from pico2d import *



name = "TitleState"
image = None
title_time = 0

def enter():
    # fill here
    global image
    image = load_image('title.png')
    pass

def exit():
    # fill here
    global image
    del(image)
    pass


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    # fill here
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(main_state)


def update(frame_time):
    global title_time

    if(title_time > 0.1):
        title_time = 0
        #game_framework.quit()
        game_framework.push_state(main_state)
    title_time += frame_time


def draw(frame_time):
    # fill here
    global image
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass



