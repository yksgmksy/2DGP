__author__ = 'yang'
import math
from pico2d import *

class Inventory:
    image = None

    LEFT, RIGHT = 0, 1
    RED , BLUE , YELLOW , PINK , STONE, METAL, SLIVER , GOLD ,WOOD, DIA , ARROW_ITEM, DOK2_ITEM, GOK_ITEM, GUN_ITEM, SWORD_ITEM , ROKET_ITEM, POTION, CANDY , PUMPKIN ,BULLET  = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
    WEAPON , NOT_WEAPON = 0, 1
    def __init__(self):
        global  font
        self.x = 200
        self.y = 300
        self.item_num = [[0]*15 for i in range(15)] #갯수
        self.item_state = [[self.NOT_WEAPON]*15 for i in range(15)]
        self.item_kind = [[-1]*15 for i in range(15)]
        self.image = load_image('res/Inventory.png')
        self.state = 0
        self.item_imagelist  = [[] for i in range(20)]
        font = load_font('ENCR10B.TTF')

        self.item_imagelist[self.RED] = load_image('res/item/jelly_red.png')
        self.item_imagelist[self.BLUE] = load_image('res/item/jelly_blue.png')
        self.item_imagelist[self.YELLOW] = load_image('res/item/jelly_yellow.png')
        self.item_imagelist[self.PINK] = load_image('res/item/jelly_pink.png')
        self.item_imagelist[self.STONE] = load_image('res/item/break_item.png')
        self.item_imagelist[self.METAL] = load_image('res/item/fe.png')
        self.item_imagelist[self.SLIVER] = load_image('res/item/sliver.png')
        self.item_imagelist[self.GOLD] = load_image('res/item/gold.png')
        self.item_imagelist[self.WOOD] = load_image('res/item/wood.png')
        self.item_imagelist[self.DIA] = load_image('res/item/dia.png')

        self.item_imagelist[self.ARROW_ITEM] = load_image('res/item/arrow_item.png')
        self.item_imagelist[self.DOK2_ITEM] = load_image('res/item/dok2_item.png')
        self.item_imagelist[self.GOK_ITEM] = load_image('res/item/gokgang_item.png')
        self.item_imagelist[self.GUN_ITEM] = load_image('res/item/gun_item.png')
        self.item_imagelist[self.SWORD_ITEM] = load_image('res/item/sword_item.png')
        self.item_imagelist[self.ROKET_ITEM] = load_image('res/item/roket_item.png')
        self.item_imagelist[self.POTION] = load_image('res/item/potion_item.png')
        self.item_imagelist[self.CANDY] = load_image('res/item/candy.png')
        self.item_imagelist[self.PUMPKIN] = load_image('res/item/pumpkin.png')
        self.item_imagelist[self.BULLET] = load_image('res/item/bullet.png')

        self.item_kind[0][0] = self.SWORD_ITEM
        self.item_num[0][0] = 1
        self.item_state[0][0] = self.WEAPON
        self.item_kind[0][1] = self.DOK2_ITEM
        self.item_num[0][1] = 1
        self.item_state[0][1] = self.WEAPON
        self.item_kind[0][2] = self.GOK_ITEM
        self.item_num[0][2] = 1
        self.item_state[0][2] = self.WEAPON
        self.item_kind[0][3] = self.POTION
        self.item_num[0][3] = 2
        self.item_state[0][3] = self.NOT_WEAPON

        self.show = False

    def get_tilemap(self,tile_map , mapx,mapy):
        self.tile_map = tile_map
        self.mapx = mapx
        self.mapy = mapy

    def get_item(self,item_kind,item_state):
        for i in range(0,15):
            for j in range(0,15):
                if self.item_kind[i][j] == item_kind:
                    self.item_num[i][j] += 1
                    return
                elif self.item_kind[i][j] == -1:
                    self.item_kind[i][j] = item_kind
                    self.item_num[i][j] += 1
                    return

    def update(self,itemlist,item_num,item_state):
        self.item_kind = itemlist
        self.item_num = item_num
        self.item_state = item_state
        pass

    def draw(self):
        #print(self.list[0][0])
        if self.show:
            self.image.opacify(0.5)
            self.image.draw(self.x,self.y)
            font.draw(140,160,"inventory")
            for i in range(0,15):
                for j in range(0,15):
                    if self.item_kind[i][j] == -1:
                        continue
                    else:
                        self.item_imagelist[self.item_kind[i][j]].draw(50+ j*20+10, 600-(self.y/2 + i*40+10) )
                        font.draw(40+ j*20+10, 600-(self.y/2 + i*40+30),'%d'%(self.item_num[i][j]))
