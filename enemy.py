import pygame
from random import *
#小型敌机
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemy1.png').convert_alpha()
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load('images/enemy1_down1.png').convert_alpha(),\
            pygame.image.load('images/enemy1_down2.png').convert_alpha(),\
            pygame.image.load('images/enemy1_down3.png').convert_alpha(),\
            pygame.image.load('images/enemy1_down4.png').convert_alpha()\
            ])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = randint(0, self.width-self.rect.width), randint(-5*self.height, 0)
        self.speed = 2
        self.active = True
        #飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image)
    #敌机向下移动
    def move(self):
        if self.rect.top<self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    #重置敌机位置
    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)

#中型敌机
class MidEnemy(pygame.sprite.Sprite):
    emergy = 4
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemy2.png').convert_alpha()
        # 被击中时的图片
        self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.destory_images = []
        self.destory_images.extend([ \
            pygame.image.load('images/enemy2_down1.png').convert_alpha(), \
            pygame.image.load('images/enemy2_down2.png').convert_alpha(), \
            pygame.image.load('images/enemy2_down3.png').convert_alpha(), \
            pygame.image.load('images/enemy2_down4.png').convert_alpha() \
            ])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = randint(0, self.width-self.rect.width), randint(-10*self.height, -self.height)
        self.speed = 1
        self.active = True
        #飞机的血量
        self.emergy = MidEnemy.emergy
        #是否被击中
        self.hited = False
        # 飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image)
    #敌机向下移动
    def move(self):
        if self.rect.top<self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    #重置敌机位置
    def reset(self):
        self.active = True
        # 飞机的血量
        self.emergy = MidEnemy.emergy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10 * self.height, -self.height)

    # 中型敌机

#大型敌机
class BigEnemy(pygame.sprite.Sprite):
    emergy = 8
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
        self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
        #被击中时的图片
        self.image_hit = pygame.image.load('images/enemy3_hit.png').convert_alpha()
        self.destory_images = []
        self.destory_images.extend([ \
            pygame.image.load('images/enemy3_down1.png').convert_alpha(), \
            pygame.image.load('images/enemy3_down2.png').convert_alpha(), \
            pygame.image.load('images/enemy3_down3.png').convert_alpha(), \
            pygame.image.load('images/enemy3_down4.png').convert_alpha(), \
            pygame.image.load('images/enemy3_down5.png').convert_alpha(), \
            pygame.image.load('images/enemy3_down6.png').convert_alpha() \
            ])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image1.get_rect()
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5 * self.height,-1*self.height)
        self.speed = 1
        self.active = True
        # 飞机的血量
        self.emergy = BigEnemy.emergy
        # 是否被击中
        self.hited = False
        # 飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image1)

    # 敌机向下移动
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    # 重置敌机位置
    def reset(self):
        self.active = True
        # 飞机的血量
        self.emergy = BigEnemy.emergy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-5 * self.height,
                                                                                          -1*self.height)

