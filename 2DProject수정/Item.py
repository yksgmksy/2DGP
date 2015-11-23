__author__ = 'yang'
__author__ = 'yang'

import random
from pico2d import *

WORLD_GRAVITY = 9.8

class Item:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    SHOW_MAP_SIZE = 15 #화면에보여지는 크기
    SHOW_MAP_SIZEY = 10
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    LEFT_RUN , RIGHT_RUN = 0, 1
    RED , BLUE , YELLOW , PINK , STONE, METAL, SLIVER , GOLD ,WOOD, DIA  = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    def __init__(self , x,y, item):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.distance = 0
        self.gravity = 0

        self.first_time = get_time()
        self.current_time = 0;

        self.position = 0
        self.x = x
        self.y = y

        self.herox = 0
        self.heroy = 0
        self.heroTilex = 0
        self.heroTiley = 0
        self.herogravity = 0

        self.mapx = 0
        self.mapy = 0
        self.mapChange = None
        self.mapstate = 1

        self.itemstate = item

        if item == self.RED:
            self.image = load_image('res/item/jelly_red.png')
        if item == self.BLUE:
            self.image = load_image('res/item/jelly_blue.png')
        if item == self.YELLOW:
            self.image = load_image('res/item/jelly_yellow.png')
        if item == self.PINK:
            self.image = load_image('res/item/jelly_pink.png')
        if item == self.STONE:
            self.image = load_image('res/item/break_item.png')
        if item == self.METAL:
            self.image = load_image('res/item/fe.png')
        if item == self.SLIVER:
            self.image = load_image('res/item/sliver.png')
        if item == self.GOLD:
            self.image = load_image('res/item/gold.png')
        if item == self.WOOD:
            self.image = load_image('res/item/wood.png')
        if item == self.DIA:
            self.image = load_image('res/item/dia.png')

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x -10 , self.y -10 , self.x +10, self.y+10


    def collide(a,b):
        left_a,bottom_a,right_a,top_a = a.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()
        if left_a > right_b : return False
        if right_a < left_b : return False
        if top_a < bottom_b : return False
        if bottom_a > top_b : return False
        return True


    def get_hero(self,map_x,map_y,mapChange,mapstate , distance, herogravity , state , heroTilex, heroTiley, herox, heroy):
        self.mapx = map_x
        self.mapy = map_y
        self.mapChange = mapChange
        self.mapstate = mapstate
        self.distance = distance
        self.herogravity = herogravity
        self.state = state
        self.heroTilex = heroTilex
        self.heroTiley = heroTiley
        self.herox = herox
        self.heroy = heroy

    def collide_tiley(self):
        if self.mapstate == 1:
            if (int)(self.mapChange[(int)((self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x + self.sizex/2 )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                return True

        elif self.mapstate == 2:
            if (int)(self.mapChange[(int)((-self.mapy+900+self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x + self.sizex/2 )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                return True
        return False

    def collide_tilex(self):
        if self.mapstate == 1:
            if (int)(self.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x-self.distance)/25)] / 10) == 2:
                self.x += self.distance
                return True
            if (int)(self.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x+self.distance + self.sizex )/25)] / 10) == 2:
                self.x -= self.distance
                return True
        elif self.mapstate == 2:
            if (int)(self.mapChange[(int)((-self.mapy+900+self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x-self.distance)/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                return True
            if (int)(self.mapChange[(int)((-self.mapy+900+self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x+self.distance + self.sizex )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                return True
        return False

    def collcheck(self):
        self.x = self.x+((self.herox)-self.x)/30
        self.y = self.y+((self.heroy)-self.y)/30

            #rt[i].x = rt[i].x + (px - rt[i].x) / 20; //사각형대각선
			#rt[i].y = rt[i].y + (py - rt[i].y) / 20;
    def update(self):
        if 900 > self.mapx > 0 and self.state == self.RIGHT_RUN and self.heroTilex == False:
                self.x -= self.distance
        if 0 < self.mapx < 900  and self.state == self.LEFT_RUN and self.heroTilex == False:
                self.x += self.distance
        #if 900 > self.mapy > 0  and self.heroTiley == False:
        #        self.y -= self.distance
        #if 0 < self.mapy < 900   and self.heroTiley == False:
        #        self.y += self.distance

        self.collcheck()
        #self.collide_tiley()
        #self.y -= self.gravity
        #if self.collide_tiley() == False:
        #    self.gravity += (WORLD_GRAVITY/Item.RUN_SPEED_PPS*2)


    def draw(self):
        self.image.opacify(0.8)
        self.image.draw(self.x, self.y, 20, 20)