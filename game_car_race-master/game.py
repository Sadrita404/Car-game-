
import random
from time import sleep

import pygame
from pathlib2 import Path


class CarRacing:
    def draw_switches(self):
        # Draw left and right control buttons on the game panel
        button_width, button_height = 80, 80
        left_rect = pygame.Rect(80, self.display_height - 120, button_width, button_height)
        right_rect = pygame.Rect(self.display_width - 160, self.display_height - 120, button_width, button_height)
        pygame.draw.rect(self.gameDisplay, (200, 200, 200), left_rect)
        pygame.draw.polygon(self.gameDisplay, (50, 50, 50), [
            (left_rect.x + 60, left_rect.y + 20),
            (left_rect.x + 20, left_rect.y + 40),
            (left_rect.x + 60, left_rect.y + 60)
        ])
        pygame.draw.rect(self.gameDisplay, (200, 200, 200), right_rect)
        pygame.draw.polygon(self.gameDisplay, (50, 50, 50), [
            (right_rect.x + 20, right_rect.y + 20),
            (right_rect.x + 60, right_rect.y + 40),
            (right_rect.x + 20, right_rect.y + 60)
        ])
        return left_rect, right_rect
    def front_page(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race -- Sadrita Neogi')
        font_title = pygame.font.SysFont("comicsansms", 60, True)
        font_button = pygame.font.SysFont("comicsansms", 40, True)
        title_text = font_title.render("Game By Sadrita Neogi", True, (255, 255, 255))
        button_text = font_button.render("Go", True, (0, 0, 0))
        button_rect = pygame.Rect((self.display_width//2 - 75, self.display_height//2 + 40, 150, 60))
        waiting = True
        while waiting:
            self.gameDisplay.fill((30, 30, 30))
            self.gameDisplay.blit(title_text, (self.display_width//2 - title_text.get_width()//2, self.display_height//2 - 100))
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), button_rect)
            self.gameDisplay.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width())//2, button_rect.y + (button_rect.height - button_text.get_height())//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False
            pygame.display.update()
            self.clock.tick(60)
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load(self.root_path + "/img/car.png")
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load(self.root_path + "/img/enemy_car_1.png")
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load(self.root_path + "/img/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race -- Sadrita Neogi')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            move_left = move_right = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    if event.key == pygame.K_RIGHT:
                        move_right = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    left_rect, right_rect = self.draw_switches()
                    if left_rect.collidepoint(mouse_pos):
                        move_left = True
                    if right_rect.collidepoint(mouse_pos):
                        move_right = True

            if move_left:
                self.car_x_coordinate -= 50
            if move_right:
                self.car_x_coordinate += 50

            self.gameDisplay.fill(self.black)
            self.back_ground_road()
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed
            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            if self.count % 100 == 0:
                self.enemy_car_speed += 1
                self.bg_speed += 1
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.game_over_page()
            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                self.game_over_page()
            # Draw switches every frame
            self.draw_switches()
            pygame.display.update()
            self.clock.tick(60)

    def game_over_page(self):
        font_title = pygame.font.SysFont("comicsansms", 72, True)
        font_score = pygame.font.SysFont("comicsansms", 48, True)
        font_button = pygame.font.SysFont("comicsansms", 40, True)
        title_text = font_title.render("Game Is Over", True, (255, 0, 0))
        score_text = font_score.render(f"Score: {self.count}", True, (255, 255, 255))
        button_text = font_button.render("Play Again", True, (0, 0, 0))
        button_rect = pygame.Rect((self.display_width//2 - 120, self.display_height//2 + 80, 240, 60))
        # Show the game over and score for 1 second before enabling the button
        self.gameDisplay.fill((30, 30, 30))
        self.gameDisplay.blit(title_text, (self.display_width//2 - title_text.get_width()//2, self.display_height//2 - 120))
        self.gameDisplay.blit(score_text, (self.display_width//2 - score_text.get_width()//2, self.display_height//2 - 30))
        self.display_credit()
        pygame.display.update()
        pygame.time.delay(1000)
        waiting = True
        while waiting:
            self.gameDisplay.fill((30, 30, 30))
            self.gameDisplay.blit(title_text, (self.display_width//2 - title_text.get_width()//2, self.display_height//2 - 120))
            self.gameDisplay.blit(score_text, (self.display_width//2 - score_text.get_width()//2, self.display_height//2 - 30))
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), button_rect)
            self.gameDisplay.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width())//2, button_rect.y + (button_rect.height - button_text.get_height())//2))
            self.display_credit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False
            pygame.display.update()
            self.clock.tick(60)
        self.initialize()
        self.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks & Regards,", True, self.white)
        self.gameDisplay.blit(text, (600, 520))
        text = font.render("Sadrita Neogi", True, self.white)
        self.gameDisplay.blit(text, (600, 540))
        text = font.render("sadritaneogi@gmail.com", True, self.white)
        self.gameDisplay.blit(text, (600, 560))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.front_page()
    car_racing.racing_window()
