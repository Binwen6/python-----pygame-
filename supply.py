import pygame
from random import *
#子弹补给
class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self, bgsize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bgsize[0], bgsize[1]
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100
        self.active = False
        self.speed = 5
        #忽略掉图片中白色背景的部分
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100

#炸弹补给
class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self, bgsize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bgsize[0], bgsize[1]
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100
        self.active = False
        self.speed = 4
        #忽略掉图片中白色背景的部分
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100