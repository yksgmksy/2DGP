import random

from pico2d import *

import game_framework
import title_state
from Map import Map
from Hero import Hero
from Weapon import Bullet
from Monster import *
from Interface import *

name = "MainState"\


font = None
hero = None
slimes = None
bullets = None

first_time = 0
current_time = 0
slime_bool = False

font_X = 0
font_Y = 0
rand = 0

delcheck = False

RED , BLUE , YELLOW , PINK , STONE, METAL, SLIVER , GOLD ,WOOD, DIA  = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
WEAPON , NOT_WEAPON = 0, 1

def enter():
    global hero, slimes, image, font, bullets , first_time , slime_red , slime_blue , slime_yellow, slime_pink , interface
    global items
    items = [Item(0,0,0) for i in range(0)]
    hero = Hero()
    bullets = [Bullet() for i in range(0)]
    slimes = []
    slime_red = [Slime_red() for i in range(0)]
    slime_blue = [Slime_blue() for i in range(0)]
    slime_yellow = [Slime_yellow() for i in range(0)]
    slime_pink = [Slime_pink() for i in range(0)]
    slimes = slimes+slime_red+slime_blue+slime_yellow +slime_pink
    interface = Interface()
    image = load_image('res/title.png')
    first_time = get_time()

def exit():
    global hero, slimes, font, bullets, interface,items
    del(hero)
    del(bullets)
    del(slimes)
    del(font)
    del(items)
    del(interface)

def pause():
    pass


def resume():
    pass

def collide(a,b):
        left_a,bottom_a,right_a,top_a = a.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()
        if left_a > right_b : return False
        if right_a < left_b : return False
        if top_a < bottom_b : return False
        if bottom_a > top_b : return False
        return True

def handle_events(frame_time):
    # fill here
    global hero,slime,bullets,slimes , interface , rand
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                hero.handle_events(event)
            if event.type == SDL_MOUSEBUTTONDOWN:
                if hero.weaponstate == 2:
                    if hero.x > event.x:
                        bullets.append(Bullet(hero.x,hero.y,event.x,event.y,0))
                    else:
                        bullets.append(Bullet(hero.x,hero.y,event.x,event.y,1))
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                rand = random.randint(0,3)
                if rand == 0:
                    slimes.append(Slime_red())
                elif rand == 1:
                    slimes.append(Slime_blue())
                elif rand == 2:
                    slimes.append(Slime_pink())
                elif rand == 3:
                    slimes.append(Slime_yellow())

def removeItem():
        global items , hero
        for item in items:
            if item.x-5 < hero.x+12.5 and item.x+5 > hero.x-12.5 and item.y - 5 < hero.y+12.5 and item.y + 5 > hero.y-12.5:
                hero.inventory.get_item(item.itemstate, NOT_WEAPON)
                items.remove(item)

def mapmove():
    global delcheck
    if hero.mapchange == True:
        hero.mapchange = False
        delcheck = True
    if delcheck:
        if not slimes:
            delcheck = False
        for slime in slimes:
            slimes.remove(slime)

def get_info():
    global bullets,hero , interface,items
    interface.get_weapon(hero.weaponstate)
    for bullet in bullets:
        bullet.get_tilemap(hero.tile_map,hero.mapx,hero.mapy)
        if bullet.collide_tile():
            bullets.remove(bullet)
    for item in items:
        item.get_hero(hero.mapx,hero.mapy,hero.mapchange,hero.mapstate , hero.distance, hero.gravity , hero.state , hero.tileCollx, hero.tileColly, hero.x, hero.y)

def monster_move(slime):
    if 900 > hero.mapx > 0 and hero.state == hero.RIGHT_RUN and hero.tileCollx == False:
            slime.x -= hero.distance
    if 0 < hero.mapx < 900  and hero.state == hero.LEFT_RUN and hero.tileCollx == False:
            slime.x += hero.distance

    slime.get_hero(hero.mapx, hero.mapy, hero.tile_map)

def create_slime():
    global first_time , current_time , slime_bool
    current_time = (int)(get_time() - first_time)
    if (current_time+1) % 3 == 0 and slime_bool == False:
        slimes.append(Slime())
        slime_bool = True
    if (current_time+2) % 3 == 0 and slime_bool == True:
       slime_bool = False
    print(current_time)
    pass


def update(frame_time):
    removeItem()
    get_info()
    mapmove()
    hero.update(frame_time)
    for item in items:
        item.update()
    for bullet in bullets:
        bullet.update(frame_time)
        if bullet.travel_range > bullet.canmove:
            bullets.remove(bullet)
    for slime in slimes:
        slime.update(frame_time)
        monster_move(slime)
        if slime.hp < 0:
            items.append(Item(slime.x,slime.y,RED))
            slimes.remove(slime)
        if collide(hero,slime):
            if hero.invincible == False: #충돌처리
                if hero.x + hero.mapx-900 < slime.x:
                    hero.get_hit(7,1,0)
                elif hero.x + hero.mapx-900 >= slime.x:
                    hero.get_hit(7,1,1)
            slime.collcheck()
        for bullet in bullets:
            if collide(bullet,slime):
                slime.gethit(bullet.demage)
                bullets.remove(bullet)


def draw(frame_time):
    clear_canvas()
    hero.draw()
    #hero.draw_bb()
    for bullet in bullets:
        bullet.draw()
    for slime in slimes:
        slime.draw()
        #slime.draw_bb()

    for item in items:
        item.draw()
    interface.draw()
    update_canvas()







