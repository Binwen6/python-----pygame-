import pygame
#子弹1
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.active = True
        self.speed = 12
        # 子弹和飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image)

    #子弹移动
    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    #子弹重置
    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

#子弹2
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/wsparticle_super01.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.active = True
        self.speed = 14
        # 子弹和飞机碰撞检测，会忽略掉图片中白色的背景部分
        self.mask = pygame.mask.from_surface(self.image)

    #子弹移动
    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    #子弹重置
    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True