# This file was created by: Grant Curtiss
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        # number the moneybag starts
        self.health = 100 
        # amount of health the healthbar starts with
        self.speed = 300
        # The speed of the character
        
        
       
    #def take_damage(self, damage):
        #self.health -= damage
        #if self.health >= 0:
            # self.health = 0
        
            # Player dies or any other game over logic
        
        
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        # initializes the two attributes
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        # check if left arrow key is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        # check if right arrow was pressed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        # check if up arrow was pressed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        # check if down arrow was pressed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        # help with diagonal velocity movement
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
                # detects if collsion is horizonatal and stops movement sideways
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                    # detects if collsion is vertical and stops movement that is vertical
                self.vy = 0
                self.rect.y = self.y
                self.take_damage_from_wall()  
                # Call method to take damage

    def take_damage_from_wall(self):
        # Define how much damage the player takes when hitting a wall
        damage = 10  # Example damage value, adjust as needed
        #self.game.player.take_damage(damage)  
        # Assuming self.game.player refers to the player instance
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                # if player hits coin moneybag is +1
            if str(hits[0].__class__.__name__) == "Sludge":
                self.health -= 20
                # if str hits sludge takes -20 health
                print ("sludge")
            if str(hits[0].__class__.__name__) == "Elixir":
                self.health += 20
                # if str hits sludge takes -20 health
            if str(hits[0].__class__.__name__) == "Lightning":
                print(hits[0].__class__.__name__)
                self.speed += 100
                # if player 


    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.walls, False)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.Sludge, True)
        # Defines is player hits the object
          
        #coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        #if coin_hits:
        #     print("I got a coin")
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # represents the walls in the game, image of the wall is blue

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # is the behavior and attriubutes of coins in the game rendering, positioning, and interaction

class Sludge(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # provides a blueprint for creating and managing sludge within the game environment 

class Elixir(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # provides blueprint for creating and managing elixir within game environment


class Lightning(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        # provides blueprint for creating and managing lightning within game environment

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        # shows enemies in envrironment

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx = 1  # Initial velocity of the enemy

    def update(self):
        # Move the enemy horizontally
        self.rect.x += self.vx
        # Check for collisions with walls
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        for hit in hits:
            # Reverse direction if colliding with a wall
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
            self.vx *= -1  # Reverse velocity
        

        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # stops moving if you hit a wall
