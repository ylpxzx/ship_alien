# coding:utf-8
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        # 飞船矩形
        self.rect = self.image.get_rect()
        # 屏幕矩形
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        # 飞船矩形的y位置，用于上下移动
        self.rect.centery = self.screen_rect.centery
        # 飞船矩形的x位置，用于左右移动
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船 的属性center中存储小数值，，可在后面加快游戏节奏时更细致地控制飞船速度
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # 根据移动标志调整飞船位置

        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < 800:
            self.centery += self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象，即更新飞船的位置
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # 让飞船在屏幕上居中
        self.center = self.screen_rect.centerx
