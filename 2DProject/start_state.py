import game_framework
import title_state
from pico2d import *


# fill here
name = "StartState"
image = None
logo_time = 0.0

def enter():
    # fill here
    global image
    open_canvas()#sync = True)
    image = load_image('kpu_credit.png')
    pass


def exit():
    # fill here
    global image
    del(image)
    close_canvas()
    pass

def update(frame_time):
    # fill here
    global logo_time

    if(logo_time > 0.1):
        logo_time = 0
        #game_framework.quit()
        game_framework.push_state(title_state)
    logo_time += frame_time

def draw(frame_time):
    # fill here
    global image
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass

def handle_events(frame_time):
    events = get_events()

def pause(): pass
def resume(): pass




