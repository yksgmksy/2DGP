__author__ = 'yang'

import math
from pico2d import *

class Interface:
    image = None

    LEFT, RIGHT = 0, 1
    ARROW , CANDY , DOK2, GOKGANG , GUN , POTION , ROCKET , SWORD = 0,1,2,3,4,5,6,7

    def __init__(self):
        self.x = 210
        self.y = 565
        self.list = [-1]*6
        self.image = load_image('res/interface.png')
        self.state = 0
        self.item_imagelist  = [[] for i in range(8)]
        self.select = 0

        self.list[1] = self.GUN


        self.item_imagelist[self.ARROW] = load_image('res/weapon/arrow.png')
        self.item_imagelist[self.CANDY] = load_image('res/weapon/candy.png')
        self.item_imagelist[self.DOK2] = load_image('res/weapon/dok2.png')
        self.item_imagelist[self.GOKGANG] = load_image('res/weapon/gokgang.png')
        self.item_imagelist[self.GUN] = load_image('res/weapon/gun.png')
        self.item_imagelist[self.POTION] = load_image('res/weapon/potion.png')
        self.item_imagelist[self.ROCKET] = load_image('res/weapon/Rocket.png')
        self.item_imagelist[self.SWORD] = load_image('res/weapon/sword.png')
        self.show = False

    def get_weapon(self,weaponstate):
        self.select = weaponstate

    def update(self, frame_time):
        pass

    def draw(self):
            self.image.opacify(0.5)
            self.image.draw(self.x,self.y)
            for i in range(0,6):
                    if self.list[i] == -1:
                        continue
                    else:
                        self.item_imagelist[self.list[i]].draw( i*70+35, 565)
            draw_rectangle(self.select*70-35 - 35 , 565+35 , self.select*70-35 + 35 , 565-35)
