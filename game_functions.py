import pygame as game
import sys
from bullet import Bullet
from pygame.sprite import Sprite
from aleinn import Alein
from time import sleep


def check_events(ai_settings,screen,stats,sb,play_button,ship,aleins,bullets):
    for event in game.event.get():
        if event.type == game.QUIT:
            sys.exit()
                
        elif event.type == game.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type ==game.KEYUP:
            check_keyup_events(event,ship)
            
        elif event.type ==game.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=game.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aleins,bullets,mouse_x,mouse_y)
            
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aleins,bullets,mouse_x,mouse_y):
    button_clicked= play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        game.mouse.set_visible(False)
        stats.reset_stats()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        stats.game_active=True
        
        aleins.empty()
        bullets.empty()
        
        create_fleet(ai_settings,screen,ship,aleins)
        ship.center_ship()
                
                    
                
def update_screen(screen,ai_settings,stats,sb,ship,bullets,aleins,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aleins.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    game.display.flip()
    
        



def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key==game.K_RIGHT:
        ship.moving_right=True
    elif event.key==game.K_LEFT:
        ship.moving_left=True
    elif event.key==game.K_SPACE:
        fire_bullets(bullets,ai_settings,screen,ship)
    
    
        
def check_keyup_events(event,ship):
    if event.key==game.K_RIGHT:
        ship.moving_right=False
    elif event.key==game.K_LEFT:
        ship.moving_left=False
        
def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aleins):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullets_aleins_collisions(ai_settings,screen,stats,sb,ship,aleins,bullets)
    
        
def check_bullets_aleins_collisions(ai_settings,screen,stats,sb,ship,aleins,bullets):
    collisions=game.sprite.groupcollide(bullets,aleins,True,True)
    if collisions:
        for aleins in collisions.values():
            
            stats.score +=ai_settings.alein_points
            sb.prep_score()
        check_high_scores(stats,sb)
    if len(aleins)==0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level +=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aleins)
    


def fire_bullets(bullets,ai_settings,screen,ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet=Bullet(ai_settings,ship,screen)
        bullets.add(new_bullet)
    print(len(bullets))
    
            
def create_alein(ai_settings,screen,aleins,alein_number,row_number):
    alein=Alein(ai_settings,screen)
    alein_width=alein.rect.width
    alein.x=alein_width+2*alein_width*alein_number
    alein.rect.x=alein.x
    alein.rect.y=alein.rect.height+2*alein.rect.height*row_number
    aleins.add(alein)
    
        
def create_fleet(ai_settings,screen,ship,aleins):
    alein=Alein(ai_settings,screen)
    number_aleins_x=get_number_aleinss(ai_settings,alein.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alein.rect.height)
    for row in range(number_rows):
        for alein_number in range(number_aleins_x):
            create_alein(ai_settings,screen,aleins,alein_number,row)
    
        
    
    
def get_number_rows(ai_settings,ship_height,alein_height):
    avilable_space_y=(ai_settings.screen_height-(3*alein_height)-ship_height)
    number_rows=int(avilable_space_y/(2*alein_height))
    return number_rows


def get_number_aleinss(ai_settings,alein_width):
    avilable_space_x=ai_settings.screen_width-2*alein_width
    number_aleins_x=int(avilable_space_x/(2*alein_width))
    return number_aleins_x


def update_aleins(ai_settings,stats,sb,screen,ship,aleins,bullets):
    check_fleet_edges(ai_settings,aleins)
    aleins.update()
    if game.sprite.spritecollideany(ship,aleins):
        ship_hit(ai_settings,stats,sb,screen,ship,aleins,bullets)
    check_aleins_bottom(ai_settings,stats,sb,screen,ship,aleins,bullets)
    
    
def check_fleet_edges(ai_settiings,aleins):
    for alein in aleins.sprites():
        if alein.check_edges():
            change_fleet_direction(ai_settiings,aleins)
            break
        
        
def change_fleet_direction(ai_settings,aleins):
    for alien in aleins.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *=-1
    
        
        
def ship_hit(ai_settings,stats,sb,screen,ship,aleins,bullets):
    if stats.ships_left >0:
        stats.ships_left -=1
        sb.prep_ships()
        aleins.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aleins)
        ship.center_ship()
        #pause
        sleep(0.5)
    else:
        stats.game_active=False
        game.mouse.set_visible(True)
    
    
    
def check_aleins_bottom(ai_settings,stats,sb,screen,ship,aleins,bullets):
    screen_rect=screen.get_rect()
    for alein in aleins.sprites():
        if alein.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aleins,bullets)
            break
    
    
def check_high_scores(stats,sb):
    if stats.score >=stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()