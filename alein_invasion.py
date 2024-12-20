import pygame as game
from settings import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard



def Run_game():
    game.init()
    ai_settings=Setting()
    screen=game.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship=Ship(screen,ai_settings)
    game.display.set_caption("Alein invasion game")
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    bullets=Group()
    aleins=Group()
    play_button=Button(ai_settings,screen,"PLAY")
    
    gf.create_fleet(ai_settings,screen,ship,aleins)
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aleins,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aleins)
            gf.update_aleins(ai_settings,stats,sb,screen,ship,aleins,bullets)
        gf.update_screen(screen,ai_settings,stats,sb,ship,bullets,aleins,play_button)
       
Run_game()