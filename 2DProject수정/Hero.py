import random
from Weapon import Weapon
from Map import *
from pico2d import *
from Monster import Slime
import copy
font = None
slime = None
my_map = None
my_mapLayer = None
tile_map = None
#my_weapon = None

WORLD_GRAVITY = 9.8

class Hero:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    SHOW_MAP_SIZE = 20 #화면에보여지는 크기
    SHOW_MAP_SIZEY = 10
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND, LEFT_KNOCK_BACK , RIGHT_KNOCK_BACK = 0, 1, 2, 3, 4, 5

    def handle_left_run(self):
        #왼쪽 오른쪽 움직임(맵)
        if self.Left_Check == True and self.x > 0:
            if my_map.x >= 900 or self.x >= 400:
                self.x -= self.distance
            elif my_map.x < 900:
                my_map.x += self.distance
                my_mapLayer.x += self.distance/4
                my_mapLayer.x2 += self.distance/2
                for i in range((tile_map.mapSizeY)):
                    for j in range((72)):
                        tile_map.x[i][j] += self.distance
        else:
            self.state = self.LEFT_STAND

    def handle_left_stand(self):
        if self.Right_Check == True:
            self.state = self.RIGHT_RUN
        if self.Left_Check == True:
            self.state = self.LEFT_RUN
        pass

    def handle_right_run(self):
        if self.Right_Check == True:
            if self.x <= 400 or my_map.x <= 0 : #화면 반이상
                self.x += self.distance
            elif my_map.x > 0:
                my_map.x -= self.distance
                my_mapLayer.x -= self.distance/4
                my_mapLayer.x2 -= self.distance/2
                for i in range((tile_map.mapSizeY)):
                    for j in range((72)):
                        tile_map.x[i][j] -= self.distance
        else:
            self.state = self.RIGHT_STAND
        pass

    def handle_right_stand(self):
        if self.Right_Check == True:
            self.state = self.RIGHT_RUN
        if self.Left_Check == True:
            self.state = self.LEFT_RUN
        pass

    def handle_left_knock(self,knockback):
        pass

    def handle_right_knock(self):
        pass

    handle_state = {
                LEFT_RUN: handle_left_run,
                RIGHT_RUN: handle_right_run,
                LEFT_STAND: handle_left_stand,
                RIGHT_STAND: handle_right_stand,
                LEFT_KNOCK_BACK : handle_left_knock,
                RIGHT_KNOCK_BACK : handle_right_knock
    }

    def __init__(self):
        global font,my_map,tile_map,my_mapLayer , slime
        self.Left_Check = False
        self.Right_Check = False
        self.Jump_Check = False
        self.mouse_Check = False
        #self.mouse_RCheck = False
        self.tileColly = False
        self.tileCollx = False
        self.step = False
        self.jumpSpeed = 5
        self.weaponstate = -1
        self.hp = 10
        self.mouseX = 0
        self.mouseY = 0
        self.saveY = 0
        self.saveY2 = 0
        self.saveX = 0
        self.distance = 0
        self.showSize = 0
        self.gravity = 0
        self.mapstate = 0
        self.invincible = False
        self.knockbackdir = 0
        self.knockback = 0
        self.x, self.y = 100, 300
        self.test = 0
        self.jump = 0
        self.herojump = False
        self.firstjump = 0
        self.frame = random.randint(0, 7)
        self.total_frames = 0.0
        self.state = self.RIGHT_STAND
        self.mapx,self.mapy=0,0
        self.mapchange = False
        self.showinventory = False
        self.inventory = 0

        slime = Slime()
        my_mapLayer = MapLayer()
        tile_map = TileBackground()
        self.tile_map = tile_map
        tile_map.showSize(self.x / 25 - Hero.SHOW_MAP_SIZE-10, 0, self.x / 25 + Hero.SHOW_MAP_SIZE, 24)
        my_map = Map()
        #my_weapon = Weapon()
        font = load_font('ENCR10B.TTF')
        if Hero.image == None:
            Hero.image = load_image('res/Hero.png')

    def get_hit(self,knockback,demage,dir):
        #self.knockbackdir = dir
        #self.knockback = knockback
        #self.hp -= demage
        #self.invincible = True
        pass

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x -11 , self.y -17 , self.x +11 , self.y+8


    def changestage(self,stageFrom,stageTo):
        if stageTo == 1:
            my_map.changeMap(1, 450*2, 350)
            my_mapLayer.changeMap(stageTo)
            tile_map.changeStage(tile_map.map_01, 24)
            self.x ,self.y = 100,100
            self.mapchange = True
        if stageTo == 2:
            my_map.changeMap(2,450*2,450*2)
            my_mapLayer.changeMap(stageTo)
            tile_map.map_02 = copy.deepcopy(tile_map.info_map_02)
            tile_map.tilehp_2 = copy.deepcopy(tile_map.info_map_02hp)
            tile_map.changeStage(tile_map.map_02, 72)
            self.x, self.y = 100, 100
            self.mapchange = True


    def collide_tiley(self):
        if tile_map.mapstate == 1:
            if (int)(tile_map.mapChange[(int)((self.y-self.gravity-5)/25)][(int)((-self.mapx+900+self.x + 25/2 )/25)] / 10) == 2:
                self.y += self.gravity
                self.gravity = 0
                self.Jump_Check = False
                self.tileColly = True
                self.step = True
                return True
            elif (int)(tile_map.mapChange[(int)((self.y+self.jump+17)/25)][(int)((-self.mapx+900+self.x + 25/2 )/25)] / 10) == 2:
                self.y -= self.jump
                self.gravity = 0
                self.Jump_Check = False
                self.tileColly = True
                self.step = True
                return True
            else :
                self.step = False
        elif tile_map.mapstate == 2: #
            print(self.gravity , self.saveY2 , self.saveY)
            if (int)(tile_map.mapChange[(int)((-self.mapy+900+self.y-self.gravity-5)/25)][(int)((-self.mapx+900+self.x + 25/2 )/25)] / 10) == 2:
                if 0 <= self.y < 300 or my_map.y > 900:
                    if self.herojump == True and self.firstjump == 0:
                        self.y += self.gravity
                        my_map.y -= self.saveY2
                        my_mapLayer.y -= self.saveY2/4
                        my_mapLayer.y2 -= self.saveY2/2
                        for i in range((tile_map.mapSizeY)):
                                for j in range((72)):
                                    tile_map.y[i][j] -= self.saveY2
                        self.herojump = False
                    elif self.herojump == True and self.firstjump == 1:
                        self.y += self.jump
                        my_map.y += ( self.jump)
                        my_mapLayer.y += ( self.jump)/4
                        my_mapLayer.y2 += (self.jump)/2
                        for i in range((tile_map.mapSizeY)):
                                for j in range((72)):
                                    tile_map.y[i][j] +=( self.jump)
                        self.herojump = False
                else: # self.y >= 300 and  my_map.y <= 900:
                    my_map.y -= self.gravity
                    my_mapLayer.y -= self.gravity/4
                    my_mapLayer.y2 -= self.gravity/2
                    self.y = 300
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]-= self.gravity
                self.saveY = 0
                self.saveY2 = 0
                self.gravity = 0
                self.Jump_Check = False
                self.tileColly = True
                self.step = True
                self.firstjump = 0
                return True
            elif (int)(tile_map.mapChange[(int)((-self.mapy+900+self.y+self.jump+17)/25)][(int)((-self.mapx+900+self.x + 25/2 )/25)] / 10) == 2:
                if 0 <= self.y < 300 or my_map.y >= 900: #올라갈때
                    self.y -= self.jump
                    self.saveY = 0
                else: # self.y > 300 and  my_map.y <= 900:
                    my_map.y += self.jump
                    my_mapLayer.y += self.jump/4
                    my_mapLayer.y2 += self.jump/2
                    self.y = 300
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]+= self.jump

                self.gravity = 0
                self.Jump_Check = False
                self.tileColly = True
                self.step = True
                self.saveY = 0
                return True
            else :
                self.step = False
        return False

    def collide_tilex(self):
        if tile_map.mapstate == 1:
            if (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x+self.distance +11 )/25)] / 10) == 3:
                self.changestage(1,2)
            if (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x-self.distance +8)/25)] / 10) == 2:
                self.x += self.distance
                self.tileCollx = True
                return True
            elif (int)(self.tile_map.mapChange[(int)((self.y)/25)][(int)((-self.mapx+900+self.x+self.distance + 17 )/25)] / 10) == 2:
                self.x -= self.distance
                self.tileCollx = True
                return True
            else:
                self.tileCollx = False
        elif tile_map.mapstate == 2:
            if (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y)/25)][(int)((-self.mapx+900+self.x-self.distance +8)/25)] / 10) == 2:
                self.x += self.distance
                self.tileCollx = True
                return True
            elif (int)(self.tile_map.mapChange[(int)((-self.mapy+900+self.y)/25)][(int)((-self.mapx+900+self.x+self.distance +17 )/25)] / 10) == 2:
                self.x -= self.distance
                self.tileCollx = True
                return True
            else:
                self.tileCollx = False
            return False

    def heroMove(self):
        self.mapx,self.mapy = my_map.x, my_map.y
        self.tile_map = tile_map

        if my_map.change == True:
            self.changestage(0,1)
            my_map.change = False
        #넉백
        if self.knockbackdir == 0:
            if self.x >= 400:
                self.mapx -= self.knockback
            else:
                self.x -= self.knockback
        elif self.knockbackdir == 1:
            if self.x >= 400:
                self.mapx += self.knockback
            else:
                self.x += self.knockback
        if self.knockback < 0:
            self.invincible = False
            self.knockback = 0
        if self.invincible == True:
            self.knockback -= 1
        #


        #점프
        if my_map.mapState == 1:
            if self.Jump_Check:
                 self.jump = self.jumpSpeed - self.gravity
                 self.y += self.jump
                 self.step = False
            if self.step == False:
                 self.y -= self.gravity

        elif my_map.mapState == 2: # 300넘어가면 맵을 움직인다
            if self.Jump_Check:
                self.jump = self.jumpSpeed - self.gravity
                if 0 <= self.y < 300 or my_map.y > 900: #올라갈때
                    self.y += self.jump
                    my_map.y = 900
                    self.herojump = True
                else: # self.y >= 300 and  my_map.y <= 900:
                    my_map.y -= self.jump
                    my_mapLayer.y -= self.jump/4
                    my_mapLayer.y2 -= self.jump/2
                    self.y = 300
                    self.saveY += self.jump
                    self.saveY2 -= self.jump
                    self.herojump = False
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]-= self.jump
                self.step = False
            if self.step == False: # 점프하지않았을때 중력받게
                if 0 <= self.y < 300 or my_map.y >= 900:
                    self.y -= self.gravity
                    my_map.y = 900
                else: # self.y > 300 and  my_map.y <= 900:
                    my_map.y += self.gravity
                    my_mapLayer.y += self.gravity/4
                    my_mapLayer.y2 += self.gravity/2
                    self.y = 300
                    self.saveY2 += self.gravity
                    for i in range((tile_map.mapSizeY)):
                            for j in range((72)):
                                tile_map.y[i][j]+= self.gravity



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

        self.collide_tilex()
        self.collide_tiley()



        if self.collide_tiley() == False:
            self.gravity += (WORLD_GRAVITY/Slime.RUN_SPEED_PPS*2)


    def handle_events(self,event):
            global  items
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_0:
                    self.weaponstate = 0
                if event.key == SDLK_1:
                    self.weaponstate = 1
                if event.key == SDLK_2:
                    self.weaponstate = 2
                if event.key == SDLK_3:
                    self.weaponstate = 3
                if event.key == SDLK_4:
                    self.weaponstate = 4
                if event.key == SDLK_5:
                    self.weaponstate = 5
                if event.key == SDLK_6:
                    self.weaponstate = 6
                if event.key == SDLK_i:
                    if self.showinventory == False:
                        self.showinventory = True
                    elif self.showinventory == True:
                        self.showinventory = False
                if event.key == SDLK_a:
                    self.Left_Check = True
                if event.key == SDLK_d:
                    self.Right_Check = True
                if event.key == SDLK_w and self.Jump_Check == False:
                    self.Jump_Check = True
                    self.gravity = 0
                    if self.y >= 300 and  my_map.y <= 900:
                        self.firstjump = 1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_a:
                    self.Left_Check = False
                if event.key == SDLK_d:
                    self.Right_Check = False
                if event.key == SDLK_w and self.y <= 90:
                    self.Jump_Check = False
            if event.type == SDL_MOUSEBUTTONDOWN:
                self.mouseX = event.x
                self.mouseY = abs(event.y-600)
                self.mouse_Check = True
            elif event.type == SDL_MOUSEBUTTONUP:
                self.mouse_Check = False
                self.mouseX = -10
                self.mouseY = -10

    def update(self, frame_time):
        self.distance = Hero.RUN_SPEED_PPS * frame_time
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME * frame_time
        self.frame = (self.frame + 1) % 8
        self.mapstate = my_map.mapState
        self.handle_state[self.state](self)
        self.heroMove()
        self.inventory = tile_map.inventory
        #my_weapon.state = self.weaponstate
        my_map.get_hero_hp(self.hp)
        tile_map.getHeroSize(self.x, self.y,self.mouseX,self.mouseY,self.distance, self.gravity ,self.state , self.tileCollx, self.tileColly , self.showinventory)
        tile_map.getMapSize(my_map.x, my_map.y, my_map.mapState)
        if self.mouse_Check == True:
            tile_map.blockControl(self.mouse_Check,self.weaponstate)
            self.mouse_Check = tile_map.breakblock(self.mouse_Check,self.weaponstate)
        #my_weapon.update()
        my_map.update()
        tile_map.update()


    def draw(self):
        my_mapLayer.draw()
        tile_map.draw()
        tile_map.draw_bb()
        my_map.draw()
        #if self.weaponstate == 0:
        #    font.draw(self.x-50, self.y+50, 'Destroy')
        #elif self.weaponstate == 1:
        #    font.draw(self.x-50, self.y+50, 'Make block')
        #elif self.weaponstate == 2:
        #    font.draw(self.x-50, self.y+50, 'GUN')
        #else:
        #    font.draw(self.x-50, self.y+50, 'no Weapon')
        self.image.opacify(1)#random.random()+10) #이미지 투명
        self.image.clip_draw(self.frame * 60, self.state * 60, 60, 60, self.x, self.y)


    def get_XY(self):
        _x = self.x
        _y = self.y
        return _x,_y