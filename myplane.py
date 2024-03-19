import pygame
#玩家飞机
class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        self.image1 = pygame.image.load('images/me1.png').convert_alpha()
        self.image2 = pygame.image.load('images/me2.png').convert_alpha()
        self.destory_images = []
        self.destory_images.extend([
            pygame.image.load('images/me_destroy_1.png').convert_alpha(),
            pygame.image.load('images/me_destroy_2.png').convert_alpha(),
            pygame.image.load('images/me_destroy_3.png').convert_alpha(),
            pygame.image.load('images/me_destroy_4.png').convert_alpha()
            ])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect = self.image1.get_rect()
        #飞机的初始化位置
        self.rect.left, self.rect.top = (self.width-self.rect.width)/2, self.height-self.rect.height-60
        #设置飞机移动速度
        self.speed = 10
        self.active = True
        #是否处于无敌状态
        self.invincible = False
        # 飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image1)

    #向上移动
    def moveUp(self):
        if self.rect.top>0:
            self.rect.top -= self.speed
        else:
            self.rect.top=0

    # 向下移动
    def moveDown(self):
        if self.rect.bottom < self.height-60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height-60

    #向左移动
    def moveLeft(self):
        if self.rect.left>0:
            self.rect.left -= self.speed
        else:
            self.rect.left=0

    #向右移动
    def moveRight(self):
        if self.rect.right<self.width:
            self.rect.right += self.speed
        else:
            self.rect.right=self.width

    #玩家飞机重生
    def reset(self):
        self.active = True
        #重生时处于无敌状态
        self.invincible = True
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60