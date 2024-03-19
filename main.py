import pygame
import sys
import traceback
from pygame.locals import *
from random import *
import myplane
import enemy
import bullet
import supply
import background
from background import *
#初始化
pygame.init()
#初始化混音器模块
pygame.mixer.init()
#设置窗口大小
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")
#加载背景图片

bg1 = Background()
bg2 = Background(True)
back_group = pygame.sprite.Group(bg1,bg2)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#载入游戏音乐
pygame.mixer.music.load('sound/game_music.ogg')
#设置音量，取值范围为0-1.0的浮点数。0为最小值，1为最大值
pygame.mixer.music.set_volume(0.2)
#打子弹的声音
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#炸弹爆炸的声音
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
#出现补给的声音
supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
#吃到补给-炸弹的声音
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
#吃到补给-子弹的声音
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
#升级的声音
upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)
#大飞机飞的声音
enemy3_flying_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_flying_sound.set_volume(0.2)
#大飞机被击毙的声音
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
#中型飞机被击毙的声音
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
#小飞机被击毙的声音
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)
#玩家被击毙的声音
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

#生成小型飞机
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

#生成中型飞机
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

#生成大型飞机
def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

#增加敌机速度
def add_enemy_speed(targets, inc):
    for ei in targets:
        ei.speed += inc

#主入口
def main():
    #播放音乐，参数表示播放次数，如果是-1表示循环播放
    pygame.mixer.music.play(-1)
    # 创建时钟对象 (可以控制游戏循环频率)
    clock = pygame.time.Clock()

    #生成玩家飞机
    me = myplane.MyPlane(bg_size)
    #放所有敌方飞机
    enemies = pygame.sprite.Group()
    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成子弹
    bullet1s = []
    bullet1_index = 0
    BULLET1_NUM = 100
    for i in range(BULLET1_NUM):
        bullet1s.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2s = []
    bullet2_index = 0
    BULLET2_NUM = 100
    for i in range(BULLET2_NUM//2):
        bullet2s.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2s.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    #控制玩家飞机图片切换，展示突突突的效果
    switch_image = True
    #切换延时
    delay = 20

    #飞机撞击爆炸的图片下标
    e1_destory_index = 0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0

    #玩家分数显示
    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)

    #超级炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font.ttf', 48)
    bomb_num = 3

    #初始化补给对象
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    #设置定时器，30秒钟发放一次补给
    pygame.time.set_timer(SUPPLY_TIME, 5 * 1000)

    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    #标志是否使用超级子弹
    is_double_bullet = False

    #玩家的生命次数
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    #玩家三条命
    life_num = 3
    #无敌的时间3秒
    INVINCIBLE_TIME = USEREVENT + 2

    #分数文件是否被打开
    RECORDED = False

    #游戏结束界面
    gameover_font = pygame.font.Font('font/font.TTF', 48)
    #重新开始按钮图片
    again_image = pygame.image.load('images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    #游戏结束按钮图片
    gameover_image = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    #设置游戏难度级别
    level = 1


    #游戏暂停
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    #设置默认图片
    paused_image = pause_nor_image
    #暂停按钮位置
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width-paused_rect.width-10, 10



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                #如果是鼠标点击事件
            elif event.type == MOUSEBUTTONDOWN:
                #如果是左键，并且鼠标在矩形框内
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                if paused:
                    #暂停定时器
                    pygame.time.set_timer(SUPPLY_TIME, 0)
                    #停止播放背景音乐
                    pygame.mixer.music.pause()
                    #大飞机飞行额音效停止
                    pygame.mixer.pause()
                else:
                    pygame.time.set_timer(SUPPLY_TIME, 5 * 1000)
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
                #鼠标移动事件
            elif event.type == MOUSEMOTION:
                #鼠标在矩形框内
                if paused_rect.collidepoint(event.pos):
                    #如果是暂停状态
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
                #如果是按键操作
            elif event.type == KEYDOWN:
                #如果按下空格键，放大招，清空全部敌机
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for ei in enemies:
                            if ei.rect.bottom > 0:
                                ei.active = False
                #触发补给事件
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
                #超级子弹使用时间18秒后触发
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
                #重生3秒后触发
            elif event.type == INVINCIBLE_TIME:
                #解除无敌状态
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        #检测用户键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        #在屏幕上面绘制图像，并指定位置
        back_group.update()
        back_group.draw(screen)


        if level == 1 and score > 5000:
            level = 2
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
        elif level == 2 and score > 30000:
            level = 3
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 3 and score > 60000:
            level = 4
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 4 and score > 100000:
            level = 5
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 5 and score > 200000:
            level = 6
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 7)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 3)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 6 and score > 500000:
            level = 7
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 7)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 3)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 7 and score > 1000000:
            level = 8
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 7)
            add_mid_enemies(mid_enemies, enemies, 5)
            add_big_enemies(big_enemies, enemies, 3)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        elif level == 8 and score > 2000000:
            level = 9
            upgrade_sound.play()
            # 增加敌机数量
            add_small_enemies(small_enemies, enemies, 9)
            add_mid_enemies(mid_enemies, enemies, 7)
            add_big_enemies(big_enemies, enemies, 5)
            # 增加敌机速度
            add_enemy_speed(small_enemies, 1)
            add_enemy_speed(mid_enemies, 1)
        if not paused and life_num:

            #绘制子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                #补给和玩家飞机碰撞检测
                if pygame.sprite.collide_mask(bullet_supply, me):
                    bullet_supply.active = False
                    #使用超级子弹
                    is_double_bullet = True
                    #超级子弹使用时间是18秒
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
            #绘制炸弹补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                # 补给和玩家飞机碰撞检测
                if pygame.sprite.collide_mask(bomb_supply, me):
                    bomb_supply.active = False
                    if bomb_num < 3:
                        bomb_num += 1

            #10个时间单位发射一颗子弹
            if not(delay % 5):
                bullet_sound.play()
                #如果是发射超级子弹
                if is_double_bullet:
                    bullets = bullet2s
                    bullets[bullet2_index].reset((me.rect.centerx-95, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx-30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1s
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            #绘制子弹并做碰撞检测
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    #做子弹和敌机的碰撞检测
                    enemy_hits = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hits:
                        b.active = False
                        for ei in enemy_hits:
                            if ei in mid_enemies or ei in big_enemies:
                                ei.hited = True
                                ei.emergy -= 1
                                if ei.emergy == 0:
                                    ei.active = False
                            else:
                                ei.active = False

            #绘制大型机
            for ei in big_enemies:
                # 如果飞机是活的
                if ei.active:
                    ei.move()
                    if ei.hited:
                        screen.blit(ei.image_hit, ei.rect)
                        ei.hited = False
                    else:
                        if switch_image:
                            screen.blit(ei.image1, ei.rect)
                        else:
                            screen.blit(ei.image2, ei.rect)
                    #绘制血槽
                    pygame.draw.line(screen, BLACK, (ei.rect.left, ei.rect.top-5), (ei.rect.right, ei.rect.top-5), 2)
                    #当生命值小于20%时显示红色，否则显示绿色
                    emergy_remain = ei.emergy / enemy.BigEnemy.emergy
                    if emergy_remain > 0.2:
                        emergy_color = GREEN
                    else:
                        emergy_color = RED
                    pygame.draw.line(screen, emergy_color, (ei.rect.left, ei.rect.top-5),\
                                     (ei.rect.left+ei.rect.width*emergy_remain, ei.rect.top-5), 2)

                    #提前播放出场音效
                    if ei.rect.bottom == -50:
                        enemy3_flying_sound.play(-1)
                    #停止播放声音
                    if ei.rect.top >= (ei.height-ei.speed):
                        enemy3_flying_sound.stop()

                else:
                    if not(delay % 3):
                        #只播放一次声音
                        if e3_destory_index == 0:
                            enemy3_down_sound.play()
                            enemy3_flying_sound.stop()
                        #画撞击爆炸画面
                        screen.blit(ei.destory_images[e3_destory_index],ei.rect)
                        e3_destory_index = (e3_destory_index+1) % 6
                        #爆炸画面播放完之后飞机重生
                        if e3_destory_index == 0:
                            ei.reset()
                            score += 10000

            # 绘制中型机
            for ei in mid_enemies:
                # 如果飞机是活的
                if ei.active:
                    ei.move()
                    if ei.hited:
                        screen.blit(ei.image_hit, ei.rect)
                        ei.hited = False
                    else:
                        screen.blit(ei.image, ei.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (ei.rect.left, ei.rect.top - 5), (ei.rect.right, ei.rect.top - 5), 2)
                    # 当生命值小于20%时显示红色，否则显示绿色
                    emergy_remain = ei.emergy / enemy.MidEnemy.emergy
                    if emergy_remain > 0.25:
                        emergy_color = GREEN
                    else:
                        emergy_color = RED
                    pygame.draw.line(screen, emergy_color, (ei.rect.left, ei.rect.top - 5),\
                                     (ei.rect.left + ei.rect.width * emergy_remain,  ei.rect.top - 5), 2)
                else:
                    if not(delay % 3):
                        #只播放一次声音
                        if e2_destory_index == 0:
                            enemy2_down_sound.play()
                        #画撞击爆炸画面
                        screen.blit(ei.destory_images[e2_destory_index],ei.rect)
                        e2_destory_index = (e2_destory_index+1) % 4
                        #爆炸画面播放完之后飞机重生
                        if e2_destory_index == 0:
                            ei.reset()
                            score += 5000

            #绘制小型机
            for ei in small_enemies:
                #如果飞机是活的
                if ei.active:
                    ei.move()
                    screen.blit(ei.image, ei.rect)
                else:
                    if not(delay % 3):
                        #只播放一次声音
                        if e1_destory_index == 0:
                            enemy1_down_sound.play()
                        #画撞击爆炸画面
                        screen.blit(ei.destory_images[e1_destory_index],ei.rect)
                        e1_destory_index = (e1_destory_index+1) % 4
                        #爆炸画面播放完之后飞机重生
                        if e1_destory_index == 0:
                            ei.reset()
                            score += 1000

            #做碰撞检测
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            #不是无敌状态
            if enemies_down and not me.invincible:
                me.active = False
                for ei in enemies_down:
                    ei.active = False

            #绘制玩家飞机
            if me.active:
                # 在屏幕上绘制玩家飞机
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not (delay % 3):
                    # 只播放一次声音
                    if me_destory_index == 0:
                        me_down_sound.play()
                    # 画撞击爆炸画面
                    screen.blit(me.destory_images[me_destory_index], me.rect)
                    me_destory_index = (me_destory_index + 1) % 4
                    # 爆炸画面播放完之后飞机重生
                    if me_destory_index == 0:
                        life_num -= 1
                        me.reset()
                        #无敌时间设置3秒
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制暂停按钮图片
            screen.blit(paused_image, paused_rect)

            # 绘制分数文字
            score_text = score_font.render('Score : %s' % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制超级炸弹
            bomb_text = bomb_font.render('* %d' % bomb_num, True, WHITE)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - bomb_text_rect.height))

            #绘制剩余生命次数
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i+1)*life_rect.width, height - 10 - life_rect.height))

            delay -= 1
            if delay == 0:
                delay = 100
            if delay % 5 == 0:
                switch_image = not switch_image


        elif life_num == 0:
            #停止播放背景音乐
            pygame.mixer.music.stop()
            #停止播放音效，包括飞机飞行声音、补给发放声音
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not RECORDED:
                RECORDED = True
                #读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())
                #如果玩家分数大于历史最高分，则写入
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))

            #绘制结束界面
            #历史最高分数
            record_text_score = score_font.render('Best : %d' % record_score, True, WHITE)
            screen.blit(record_text_score, (50, 50))

            #本次游戏分数
            gameover_text1 = gameover_font.render('Your Score', True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, (height // 2 - 100)
            screen.blit(gameover_text1, gameover_text1_rect)
            #分数显示
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2,\
                                                                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            #绘制重新开始
            again_rect.left, again_rect.top = (width - again_rect.width)//2,\
                                                            gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            #绘制结束游戏
            gameover_rect.left, gameover_rect.top = (width - gameover_rect.width)//2,\
                                                            again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            #检测用户的鼠标操作
            #如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                #获取鼠标坐标
                pos = pygame.mouse.get_pos()
                #如果用户点击重新开始
                if again_rect.left < pos[0] < again_rect.right and\
                    again_rect.top < pos[1] < again_rect.bottom:
                    #重新开始游戏
                    main()
                #如果用户点击结束游戏
                elif gameover_rect.left < pos[0] < gameover_rect.right and\
                    gameover_rect.top < pos[1] < gameover_rect.bottom:
                    #结束游戏
                    pygame.quit()
                    sys.exit()


        #更新整个待显示的  Surface 对象到屏幕上，将内存中的内容显示到屏幕上
        pygame.display.flip()
        # 通过时钟对象指定循环频率，每秒循环60次
        # 帧速率是指程序每秒在屏幕山绘制图
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print('正常退出游戏')
        pass
    except:
        traceback.print_exc()
        pygame.quit()



