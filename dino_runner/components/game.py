from tkinter import END
import pygame
import time
from dino_runner.components import text_utils
from dino_runner.components.cloud import Cloud
from dino_runner.components.dino import Dino
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


from dino_runner.utils.constants import BG, DINO_DEAD, DINO_START, GAME_OVER, ICON, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    START = 0
    END = 0
    COLORS = [
        (255, 255, 255),
        (0, 0, 0)
    ]
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.cloud = Cloud()
        self.player = Dino()
        self.obstacle_manager = ObstacleManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
        self.high_score = 0
        self.count = 0

    def run(self):
        # Game loop: events - update - draw
        self.START_TIME = time.time()
        self.create_components()
        self.playing = True
        self.points = 0
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.cloud.update(self)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player, self)

    def draw(self):
        self.END = time.time() - self.START_TIME
        
        if self.END > 10:
            if self.count == 0:
                
                self.count = 1
            else:
                self.count = 0
            self.START_TIME = time.time()
        

        self.clock.tick(FPS)
        self.screen.fill(self.COLORS[self.count])
        self.draw_background()
        self.cloud.draw(self.screen)
        self.player.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score()
        self.obstacle_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
        

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
    
    def show_menu(self):
        self.running = True
        white_color = (255,255,255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()

    def print_menu_elements(self):
        
        if self.death_count == 0:
            text, text_rect = text_utils.get_centered_message("PRESS ANY KEY TO START")
            self.screen.blit(text, text_rect)
            self.screen.blit(DINO_START, (80, 310))
        else:
            if self.points > self.high_score:
                self.high_score = self.points
            text_death, text_death_rect = text_utils.get_centered_message(f" Deaths:  {self.death_count}",font_size=16)
            text_points, text_points_rect = text_utils.get_centered_message(f" Points: {self.points}",font_size=16)
            text_round, text_round_rect = text_utils.get_centered_message(f" Round: {self.death_count}",font_size=16)
            text_hi, text_hi_rect = text_utils.get_centered_message(f" HI: {self.high_score}",font_size=16)
            text, text_rect = text_utils.get_centered_message("PRESS ANY KEY TO START AGAIN")
            self.screen.blit(text_death, (text_death_rect.x, 150))
            self.screen.blit(text_points, (text_points_rect.x, 180 ))
            self.screen.blit(text_round, (text_round_rect.x, 210))
            self.screen.blit(text_hi, (text_hi_rect.x, 240))
            self.screen.blit(text, (text_rect.x, 300))
            self.screen.blit(DINO_DEAD, (80, 310)) 
            self.screen.blit(RESET, (520, 350))
            self.screen.blit(GAME_OVER, (350, 100))

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element("Points: ",self.points, color=self.count)  
        self.screen.blit(text, text_rect)
        text, text_rect = text_utils.get_score_element("HI: ", self.high_score, 900, color=self.count)  
        self.screen.blit(text, text_rect)
        self.player.check_invincibility(self.screen)

    def create_components(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points)

            
                   