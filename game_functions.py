# coding:utf-8
import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    # 空格操作子弹发射
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    # 按键q退出游戏
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # 响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # 响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pygame.mouse.get_pos()返回一个元组，包含玩家单击时鼠标的x和y坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # 在玩家单击play按钮时开始新游戏
    # collidepoint(mouse_x,mouse_y)检查鼠标单击的位置是否在play按钮的rect内
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 玩家每次单击play按钮时都重置游戏
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()

        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # 更新屏幕上的图像，并切换到新的屏幕
    # 每次循环时重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 绘制飞船
    ship.blitme()

    # 自动绘制外星人元素
    aliens.draw(screen)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    sb.show_score()
    if not stats.game_active:
        # 如果游戏处于非活动状态。就绘制play按钮
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 更新子弹的位置，并删除已消失的子弹
    bullets.update()

    # 在for循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本，copy()副本
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


# 创建新子弹并将其加入到编组bullest中
def fire_bullet(ai_settings, screen, ship, bullets):
    # 限制子弹数量，如果还没有到达限制，就发射一颗子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 调用create_alien()
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # 计算一行可容纳多少个外星人
    # available_space_x=ai_settings.screen_width-2*alien_width
    # number_aliens_x=int(available_space_x/(2*alien_width))
    # 'Generating random numbers'
    random_number = randint(5, 10)
    number_aliens_x = random_number
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # 计算屏幕可容纳多少行外星人
    # available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    # number_rows=int(available_space_y/(2*alien_height))
    # Generating random rows
    random_number = randint(1, 5)
    number_rows = random_number
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建第一个外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    # 创建好后加入到编组
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    # 有外星人到达边缘时采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # 将外星人群下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 调用check_fleet_edges()检查外星人是否撞到屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞，spritecollideany()接受两个实参：一个精灵和一个编组，当发生碰撞时停止遍历编组
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检测碰撞
    # 方法sprite.groupcollide（）将每颗子弹的rect同外星人的rect进行比较，并返回一个字典，其中包含发生碰撞的子弹和外星人
    # 同时遍历bullets和aliens两个编组，当两个rect重叠时，groupcollide（）就返回一个字典
    # 两个实参True，表示是否删除碰撞后的两个rect
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # 如果外星人群全被消灭，删除现有的子弹并建立一群外星人
    if len(aliens) == 0:
        bullets.empty()

        # 加快游戏节奏
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 响应被外星人撞到的飞船
    if stats.ships_left > 0:

        stats.ships_left -= 1
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停3秒
        sleep(3.0)
    else:
        # 将游戏设为非活动状态
        stats.game_active = False
        # 显示光标
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()