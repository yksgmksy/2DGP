__author__ = 'yang'
from pico2d import *

class Weapon:

    def __init__(self):
        self.state = -1

    def update(self):
        pass


    def draw(self):
        pass

class Bullet:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 100.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    SHOW_MAP_SIZE = 15 #화면에보여지는 크기
    SHOW_MAP_SIZEY = 10
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None

    LEFT, RIGHT = 0, 1

    def handle_left(self):
        self.x -= self.distance
        self.travel_range += self.distance

    def handle_right(self):
        self.x += self.distance
        self.travel_range += self.distance

    handle_state = {
                LEFT: handle_left,
                RIGHT: handle_right
    }

    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.first_x = x
        self.first_y = y
        self.canmove = 300
        self.distance = 0
        self.demage = 1
        self.travel_range = 0
        self.state = state
        self.tile_map = 0
        self.mapx = 0
        self.mapy = 0

        if Bullet.image == None:
            Bullet.image = load_image('res/item/bullet.png')

    def get_tilemap(self,tile_map , mapx,mapy):
        self.tile_map = tile_map
        self.mapx = mapx
        self.mapy = mapy

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -10 , self.y -10 , self.x +10 , self.y+10

    def collide_tile(self):
        if self.tile_map.mapstate == 1:
            if (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x)/25)] / 10) != 1:
                return True
        elif self.tile_map.mapstate == 2:
            if (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y)/25)][(int)((-self.mapx+900+self.x)/25)] / 10) != 1:
                return True

    def update(self, frame_time):
        self.distance = Bullet.RUN_SPEED_PPS * frame_time
        self.handle_state[self.state](self)

    def draw(self):
        self.image.draw(self.x,self.y)