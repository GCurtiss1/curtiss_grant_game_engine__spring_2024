# This file was created by: Grant Curtiss

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

#def draw_health_bar(surf, x, y, pct):
    #if pct < 0:
        #pct = 0
    #BAR_LENGTH = 100
    #BAR_HEIGHT = 10
    #fill = (pct / 100) * BAR_LENGTH
    #outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    #fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    #pg.draw.rect(surf, GREEN, fill_rect)
    #pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (health / 100) * BAR_LENGTH  # Calculate the filled length based on health percentage
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    

# Updating github for code because it wasn't updating
# def draw_health_bar(surf, x, y, pct):
    # in line 15 def draw healthbar and surf is surface, x and y are for the size, and pct is for the percentage of the healthbar
# if pct < 0:
# pct = 0
    # if the percentage is less than zero than the percentage is still 0
# BAR_LENGTH = 100
# BAR_HEIGHT = 10
    # l to determine the size of the bar
# outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
# fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # to determine how much health is left in the bar
    
# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.Sludge = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'S':
                    Sludge(self, col, row)
            
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()
        self.wait_for_key()

    # self.screen.fill(BGCOLOR)
        # This line fills the game screen with the background color
    # self.draw_text(self.screen, "This is the start screen", 24, WHITE, WIDTH/2 - 32, 2)
        # This line calls a method named draw_text to render text onto the screen
    # pg.display.flip()
        # This line updates the display to show the changes made to the screen
    # self.wait_for_key()
        # This line calls a method wait_for_key, which presumably waits for a key press event before proceeding

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        self.all_sprites.update()
        # Check for collision between player and Sludge
        hits = pg.sprite.spritecollide(self.player, self.Sludge, False)
        if hits:
            # Reduce player's health (adjust the damage as needed)
            self.player.health -= 20
        if self.player.health <= 0:
            # Game over logic, if player's health goes below or equal to 0
            self.game_over()
    
    def game_over(self):
    # Add game over logic here, such as displaying a game over screen
    # You might want to reset the game or go back to the main menu
    # For now, let's just quit the game
        self.playing = False  # Stop the game loop
        self.show_game_over_screen()

    def show_game_over_screen(self):
        # Display the game over screen
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        pg.time.wait(2500)  # Wait for 2.5 seconds before quitting
        self.quit()  # Quit the game

    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        draw_health_bar(self.screen, 5, 5, self.player.health)  
        # Pass player's health
        pg.display.flip()


    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)

# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
g.show_start_screen()
g.new()
g.run()
# g.show_go_screen()