__author__ = 'yang'

import random
from Hero import *
from Map import *
from pico2d import *

WORLD_GRAVITY = 9.8

class Slime:
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

    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND , LEFT_JUMP , RIGHT_JUMP = 0, 1, 2, 3, 4, 5

    def handle_left_run(self):
        self.randint = random.randint(1,2)
        if self.x > 0:
            self.x -= self.distance
        if self.current_time > self.randint:
            self.first_time = get_time()
            self.state = self.LEFT_STAND

    def handle_left_stand(self):
        self.randint = random.randint(0,1)
        if self.current_time > self.randint:
            self.randint = random.randint(0,3)
            self.first_time = get_time()
            if self.randint == 0:
                self.state = self.RIGHT_RUN
            elif self.randint == 1:
                self.state = self.LEFT_RUN
            elif self.randint == 2:
                self.state = self.LEFT_JUMP
            else:
                self.state = self.RIGHT_JUMP

    def handle_right_run(self):
        self.randint = random.randint(1,2)
        if self.x < 800 :
            self.x += self.distance
        if self.current_time >  self.randint:
            self.first_time = get_time()
            self.state = self.RIGHT_STAND
        pass

    def handle_right_stand(self):
        self.randint = random.randint(0,2)
        if self.current_time >  self.randint:
            self.randint = random.randint(0,3)
            self.first_time = get_time()
            if self.randint == 0:
                self.state = self.RIGHT_RUN
            elif self.randint == 1:
                self.state = self.LEFT_RUN
            elif self.randint == 2:
                self.state = self.LEFT_JUMP
            else:
                self.state = self.RIGHT_JUMP

    def handle_left_jump(self):
        if self.jumpCount >= 1:
            self.first_time = get_time()
            self.state = self.LEFT_RUN
            self.jumpCount = 0
        else:
            self.Jump_Check = True


        pass
    def handle_right_jump(self):

        if self.jumpCount >= 1:
            self.first_time = get_time()
            self.state = self.RIGHT_RUN
            self.jumpCount = 0
        else :
            self.Jump_Check = True




    handle_state = {
                LEFT_RUN: handle_left_run,
                RIGHT_RUN: handle_right_run,
                LEFT_STAND: handle_left_stand,
                RIGHT_STAND: handle_right_stand,
                LEFT_JUMP: handle_left_jump,
                RIGHT_JUMP: handle_right_jump
    }

    def __init__(self):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.sizex = 40
        self.jumpSpeed = 6
        self.jumpCount = 0
        self.myjump = False
        self.mapx = 0
        self.mapy = 0
        self.hp = 10
        self.tile_map = 0
        self.distance = 0
        self.gravity = 0
        self.x, self.y = random.randint(200, 800), 300
        self.jump = 0
        self.frame = random.randint(0, 2)
        self.total_frames = 0.0
        self.state = self.LEFT_RUN
        self.first_time = get_time()
        self.current_time = 0
        my_map = Map()
        tile_map = TileBackground()
        self.tile_map = tile_map

        if Slime.image == None:
            Slime.image = load_image('res/slime.png')

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        pass

    def gethit(self,demage):
        self.hp -= demage

    def get_bb(self):
        return self.x -20 , self.y -20 , self.x +20 , self.y+20

    def get_hero(self,map_x,map_y,tile_map):
        self.mapx = map_x
        self.mapy = map_y
        self.tile_map = tile_map

    def collide_tiley(self):
        if tile_map.mapstate == 1:
            if (int)(self.tile_map.mapChange[(int)((self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x + self.sizex/2 )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                self.step = True
                self.Jump_Check = False
                return True
            else :
                self.step = False
        elif tile_map.mapstate == 2:
            if (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y-self.gravity)/25)][(int)((-self.mapx+900+self.x + self.sizex/2 )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                self.step = True
                self.Jump_Check = False
                return True
            else :
                self.step = False
        return False

    def collide_tilex(self):
        if tile_map.mapstate == 1:
            if (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x-self.distance)/25)] / 10) == 2:
                self.x += self.distance
                return True
            if (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x+self.distance + self.sizex )/25)] / 10) == 2:
                self.x -= self.distance
                return True
        elif tile_map.mapstate == 2:
            if (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y)/25)][(int)((-self.mapx+900+self.x-self.distance)/25)] / 10) == 2:
                self.x += self.distance
                return True
            if (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y)/25)][(int)((-self.mapx+900+self.x+self.distance + self.sizex )/25)] / 10) == 2:
                self.x -= self.distance
                return True
            return False

    def collcheck(self):
        pass

    def update(self, frame_time):
        pass

    def draw(self):
        pass

class Slime_red(Slime):

    image = None

    def __init__(self):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.sizex = 30
        self.jumpSpeed = 6
        self.jumpCount = 0
        self.myjump = False
        self.mapx = 900
        self.mapy = 0
        self.hp = 10
        self.tile_map = 0
        self.distance = 0
        self.gravity = 0
        self.x, self.y = random.randint(200, 1600), 300
        self.jump = 0
        self.frame = random.randint(0, 2)
        self.total_frames = 0.0
        self.state = random.randint(0, 3)
        self.first_time = get_time()
        self.current_time = 0
        my_map = Map()
        tile_map = TileBackground()
        self.tile_map = tile_map

        if Slime_red.image == None:
            Slime_red.image = load_image('res/red.png')

    def update(self, frame_time):
        self.distance = Slime.RUN_SPEED_PPS/3 * frame_time
        self.total_frames += Slime.FRAMES_PER_ACTION * Slime.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.current_time = (int)(get_time()-self.first_time)

        self.handle_state[self.state](self)

        self.collide_tiley()
        self.collide_tilex()
        if self.Jump_Check:
            self.jump = self.jumpSpeed - self.gravity
            self.y += self.jump
            self.step = False
            self.jumpCount+=1
        if self.step == False:
            self.y -= self.gravity

        if self.collide_tiley() == False:
            self.gravity += (WORLD_GRAVITY/Slime.RUN_SPEED_PPS*2)

    def draw(self):
        self.image.opacify(0.8)
        self.image.clip_draw(0, self.frame * 50, 60, 50, self.x, self.y)

class Slime_blue(Slime):

    image = None

    def __init__(self):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.sizex = 30
        self.jumpSpeed = 6
        self.jumpCount = 0
        self.myjump = False
        self.mapx = 900
        self.mapy = 0
        self.hp = 10
        self.tile_map = 0
        self.distance = 0
        self.gravity = 0
        self.x, self.y = random.randint(200, 1600), 300
        self.jump = 0
        self.frame = random.randint(0, 2)
        self.total_frames = 0.0
        self.state = random.randint(0, 3)
        self.first_time = get_time()
        self.current_time = 0
        my_map = Map()
        tile_map = TileBackground()
        self.tile_map = tile_map

        if Slime_blue.image == None:
            Slime_blue.image = load_image('res/blue.png')

    def update(self, frame_time):
        self.distance = Slime.RUN_SPEED_PPS/3 * frame_time
        self.total_frames += Slime.FRAMES_PER_ACTION * Slime.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.current_time = (int)(get_time()-self.first_time)

        self.handle_state[self.state](self)

        self.collide_tiley()
        self.collide_tilex()
        if self.Jump_Check:
            self.jump = self.jumpSpeed - self.gravity
            self.y += self.jump
            self.step = False
            self.jumpCount+=1
        if self.step == False:
            self.y -= self.gravity

        if self.collide_tiley() == False:
            self.gravity += (WORLD_GRAVITY/Slime.RUN_SPEED_PPS*2)

    def draw(self):
        self.image.opacify(0.8)
        self.image.clip_draw(0, self.frame * 50, 60, 50, self.x, self.y)

class Slime_yellow(Slime):

    image = None

    def __init__(self):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.sizex = 30
        self.jumpSpeed = 6
        self.jumpCount = 0
        self.myjump = False
        self.mapx = 900
        self.mapy = 0
        self.hp = 10
        self.tile_map = 0
        self.distance = 0
        self.gravity = 0
        self.x, self.y = random.randint(200, 1600), 300
        self.jump = 0
        self.frame = random.randint(0, 2)
        self.total_frames = 0.0
        self.state = random.randint(0, 3)
        self.first_time = get_time()
        self.current_time = 0
        my_map = Map()
        tile_map = TileBackground()
        self.tile_map = tile_map

        if Slime_yellow.image == None:
            Slime_yellow.image = load_image('res/yellow.png')

    def update(self, frame_time):
        self.distance = Slime.RUN_SPEED_PPS/3 * frame_time
        self.total_frames += Slime.FRAMES_PER_ACTION * Slime.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.current_time = (int)(get_time()-self.first_time)

        self.handle_state[self.state](self)

        self.collide_tiley()
        self.collide_tilex()
        if self.Jump_Check:
            self.jump = self.jumpSpeed - self.gravity
            self.y += self.jump
            self.step = False
            self.jumpCount+=1
        if self.step == False:
            self.y -= self.gravity

        if self.collide_tiley() == False:
            self.gravity += (WORLD_GRAVITY/Slime.RUN_SPEED_PPS*2)

    def draw(self):
        self.image.opacify(0.8)
        self.image.clip_draw(0, self.frame * 50, 60, 50, self.x, self.y)

class Slime_pink(Slime):

    image = None

    def __init__(self):
        global font,my_map,tile_map,my_weapon,my_mapLayer
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.sizex = 30
        self.jumpSpeed = 6
        self.jumpCount = 0
        self.myjump = False
        self.mapx = 900
        self.mapy = 0
        self.hp = 10
        self.tile_map = 0
        self.distance = 0
        self.gravity = 0
        self.x, self.y = random.randint(200, 1600), 300
        self.jump = 0
        self.frame = random.randint(0, 2)
        self.total_frames = 0.0
        self.state = random.randint(0, 3)
        self.first_time = get_time()
        self.current_time = 0
        my_map = Map()
        tile_map = TileBackground()
        self.tile_map = tile_map

        if Slime_pink.image == None:
            Slime_pink.image = load_image('res/pink.png')

    def update(self, frame_time):
        self.distance = Slime.RUN_SPEED_PPS/3 * frame_time
        self.total_frames += Slime.FRAMES_PER_ACTION * Slime.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.current_time = (int)(get_time()-self.first_time)

        self.handle_state[self.state](self)

        self.collide_tiley()
        self.collide_tilex()
        if self.Jump_Check:
            self.jump = self.jumpSpeed - self.gravity
            self.y += self.jump
            self.step = False
            self.jumpCount+=1
        if self.step == False:
            self.y -= self.gravity

        if self.collide_tiley() == False:
            self.gravity += (WORLD_GRAVITY/Slime.RUN_SPEED_PPS*2)

    def draw(self):
        self.image.opacify(0.8)
        self.image.clip_draw(0, self.frame * 50, 60, 50, self.x, self.y)

