import random
from Map import *
from pico2d import *

font = None
my_map = None
tile_map = None

WORLD_GRAVITY = 9.8

class Hero:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    JUMP_SPEED = 7.0
    SHOW_MAP_SIZE = 15 #화면에보여지는 크기
    SHOW_MAP_SIZEY = 10
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    LEFT_RUN, RIGHT_RUN = 0, 1

    def __init__(self):
        global font,my_map,tile_map
        self.Left_Check = False
        self.Right_Check = False
        self.Jump_Check = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.saveY = 0
        self.saveX = 0
        self.distance = 0
        self.showSize = 0
        self.gravity = 0
        self.x, self.y = 100, 300
        self.test = 0
        self.jump = 0
        self.herojump = False
        self.frame = random.randint(0, 7)
        self.total_frames = 0.0
        self.state = self.RIGHT_RUN

        tile_map = TileBackground()
        tile_map.showSize(self.x / 25 - Hero.SHOW_MAP_SIZE-10, 0, self.x / 25 + Hero.SHOW_MAP_SIZE, 24)
        my_map = Map()
        font = load_font('ENCR10B.TTF')
        if Hero.image == None:
            Hero.image = load_image('animation_sheet.png')

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -10 , self.y -20 , self.x +10 , self.y+20

    def collide(a,b):
        left_a,bottom_a,right_a,top_a = a.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()
        if left_a > right_b : return False
        if right_a < left_b : return False
        if top_a < bottom_b : return False
        if bottom_a > top_b : return False
        return True

    def heroMove(self):
        if self.x > get_canvas_width():
            my_map.changeMap(2,450*2,450*2)
            tile_map.changeStage(tile_map.map_02, 72)
            self.x, self.y = 100, 100

        #왼쪽 오른쪽 움직임(맵)
        if self.Left_Check == True and self.x > 0:
            if my_map.x >= 900 or self.x >= 400:
                self.x -= self.distance
            elif my_map.x < 900:
                my_map.x += self.distance
                for i in range((tile_map.mapSizeY)):
                    for j in range((72)):
                        tile_map.x[i][j] += self.distance

        if self.Right_Check == True:
            if self.x <= 400 or my_map.x <= 0 : #화면 반이상
                self.x += self.distance
            elif my_map.x > 0:
                my_map.x -= self.distance
                for i in range((tile_map.mapSizeY)):
                    for j in range((72)):
                        tile_map.x[i][j] -= self.distance

        #점프
        if my_map.mapState == 1:
            if self.Jump_Check:
                 self.jump = Hero.JUMP_SPEED - self.gravity
                 self.y += self.jump
                 self.step = False
            if self.step == False:
                 self.y -= self.gravity

        elif my_map.mapState == 2: # 300넘어가면 맵을 움직인다
            if self.Jump_Check:
                self.jump = Hero.JUMP_SPEED - self.gravity
                if 0 <= self.y < 300 or my_map.y > 900: #올라갈때
                    self.y += self.jump
                    my_map.y = 900
                else: # self.y >= 300 and  my_map.y <= 900:
                    my_map.y -= self.jump
                    self.y = 300
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]-= self.jump
                self.step = False
            elif self.step == False: # 점프하지않았을때 중력받게
                if 0 <= self.y < 300 or my_map.y > 900: #올라갈때
                    self.y -= self.gravity
                    my_map.y = 900
                else: # self.y > 300 and  my_map.y <= 900:
                    my_map.y += self.gravity
                    self.y = 300
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]+= self.gravity


        print(my_map.mapState,my_map.x, my_map.y)
        if my_map.mapState == 1:
            if my_map.x < 0: #맨오른
                tile_map.showSize((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE+2, self.y/25 -Hero.SHOW_MAP_SIZEY-7, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE+12, self.y/25 +Hero.SHOW_MAP_SIZEY+15)
            elif my_map.x >= 900: #맨왠
                tile_map.showSize((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE-12, self.y/25 -Hero.SHOW_MAP_SIZEY-7, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE-2, self.y/25 +Hero.SHOW_MAP_SIZEY+15)
            elif -5 <= my_map.x < 905:
                tile_map.showSize((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE, self.y/25 -Hero.SHOW_MAP_SIZEY-7, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE, self.y/25 +Hero.SHOW_MAP_SIZEY+15)

        elif my_map.mapState == 2:
            if my_map.x < 0: #맨오른
                tile_map.showSizeX((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE+2, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE+12)
            elif my_map.x >= 900: #맨왠
                tile_map.showSizeX((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE-12, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE-2)
            elif -5 <= my_map.x < 905:
                tile_map.showSizeX((-my_map.x+1300) / 25 - Hero.SHOW_MAP_SIZE, (-my_map.x+1300) / 25 + Hero.SHOW_MAP_SIZE)
            if my_map.y < 0: #맨위
                tile_map.showSizeY((-my_map.y+1300) / 25 - Hero.SHOW_MAP_SIZE-2, (-my_map.y+1300) / 25 + Hero.SHOW_MAP_SIZE+12)
            elif my_map.y >= 900: #맨아래
                tile_map.showSizeY((-my_map.y+1300) / 25 - Hero.SHOW_MAP_SIZE-12, (-my_map.y+1300) / 25 + Hero.SHOW_MAP_SIZE-2)
            elif -5 <= my_map.y <= 905:
                tile_map.showSizeY((-my_map.y+1300) / 25 - Hero.SHOW_MAP_SIZE, (-my_map.y+1300) / 25 + Hero.SHOW_MAP_SIZE)

        #print(self.y)
        #타일충돌 함수

        self.tileColly, self.saveY, self.saveY2, self.herojump, self.Jump_Check = tile_map.collheroy(self.x, self.y,self.jump,self.gravity, self.herojump , self.Jump_Check)
        self.tileCollx, self.saveX = tile_map.collherox(self.x, self.y, self.distance)
        #    print("충돌")
        if self.tileColly == True:
            self.step = True
            if my_map.mapState == 1:
                if self.jump+3 > self.gravity:
                    self.y += self.saveY
                else:
                    self.y += self.saveY2
            elif my_map.mapState == 2: #충돌보정
                if self.jump+3 > self.gravity:
                    if 0 <= self.y < 300 or my_map.y > 900:
                        self.y += self.saveY
                    else:
                        my_map.y -= self.saveY
                        for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j] -= self.saveY
                else:
                    if 0 <= self.y < 300 or my_map.y > 900:
                        self.y += self.saveY2
                    else:
                        my_map.y -= self.saveY2
                        for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j] -= self.saveY2
                self.saveY = 0
                self.saveY2 = 0
            self.gravity = 0
            self.jump = 0
        else:
            self.step = False
            self.gravity += (WORLD_GRAVITY/Hero.RUN_SPEED_PPS*2)



        if self.tileCollx == True:
            if 0 <= self.x < 400 or my_map.x > 900 or my_map.x <= 0:
                self.x += self.saveX
            else:
                my_map.x -= self.saveX
                for i in range((tile_map.mapSizeY)):
                    for j in range((72)):
                        tile_map.x[i][j] -= self.saveX
            self.saveX = 0

    def update(self, frame_time):
        self.distance = Hero.RUN_SPEED_PPS * frame_time
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.heroMove()

    def draw(self):
        # fill here
        my_map.draw()
        tile_map.draw()
        tile_map.draw_bb()
        font.draw(self.x-50, self.y+50, 'Time: %3.2f' % get_time())
        self.image.opacify(0.5)#random.random()+10) #이미지 투명
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)

    def get_XY(self):
        _x = self.x
        _y = self.y
        return _x,_y