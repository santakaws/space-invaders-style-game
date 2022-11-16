import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.settings.initialize_speed_settings()
    
    def highscores(self):
        while True:
            f = open('highscores.txt', 'r')
            score_list = f.readlines()
            font = pg.font.SysFont('arial', 30)
            self.screen.fill((0,0,0))
            for i in range(len(score_list)):
                play_text = font.render(score_list[i], True, (255,255,255))
                self.screen.blit(play_text, ((self.settings.screen_width/2)-(play_text.get_width()/2),i*30))
            pg.display.flip()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN:
                    self.menu()


    def menu(self):
        while True:
            black = (0,0,0)
            white = (255,255,255)
            green = (0,255,0)
            button_font = pg.font.SysFont('arial', 30)
            title_font = pg.font.SysFont('arial', 100, True)
            play_text = button_font.render('PLAY', True, black)
            hs_text = button_font.render('HIGHSCORES', True, black)
            title_text = title_font.render('SPACE', True, white), title_font.render('INVADERS', True, green)
            self.screen.fill(black)
            play_rect = pg.draw.rect(self.screen,white,[self.settings.pb_posn[0],self.settings.pb_posn[1],self.settings.button_width,self.settings.button_height])
            hs_rect = pg.draw.rect(self.screen,white,[self.settings.hsb_posn[0],self.settings.hsb_posn[1],self.settings.button_width,self.settings.button_height])
            self.screen.blit(play_text, play_rect)
            self.screen.blit(hs_text, hs_rect)
            self.screen.blit(title_text[0], ((self.settings.screen_width/2)-(title_text[0].get_width()/2),5))
            self.screen.blit(title_text[1], ((self.settings.screen_width/2)-(title_text[1].get_width()/2),90))
            pg.display.flip()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if ev.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pos()[0] > self.settings.pb_posn[0] and pg.mouse.get_pos()[0] < self.settings.pb_posn[0]+self.settings.button_width:
                        if pg.mouse.get_pos()[1] > self.settings.pb_posn[1] and pg.mouse.get_pos()[1] < self.settings.pb_posn[1]+self.settings.button_height:
                            self.play()
                    if pg.mouse.get_pos()[0] > self.settings.hsb_posn[0] and pg.mouse.get_pos()[0] < self.settings.hsb_posn[0]+self.settings.button_width:
                        if pg.mouse.get_pos()[1] > self.settings.hsb_posn[1] and pg.mouse.get_pos()[1] < self.settings.hsb_posn[1]+self.settings.button_height:
                            self.highscores()
                    

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()
        #self.barriers.reset()
        self.ship.reset()
        #self.aliens.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.scoreboard.store_score()
        self.sound.gameover()
        #self.sound.stop_bg()
        self.__init__()
        self.menu()

    def play(self):
        self.sound.play_bg()
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.fill(self.settings.bg_color)
            self.barriers.update()
            self.ship.update()
            self.aliens.update()
            # self.lasers.update()
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.menu()


if __name__ == '__main__':
    main()
