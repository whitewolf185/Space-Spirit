# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:36:03 2019

@author: МЫ
"""

import time
import random
import math
import sys
import pygame
LENGTH = 1200
WIDTH = 600
center=(LENGTH/2,WIDTH/2)
    
FPS=30

def gr(x,y,x0,y0,G,M):
    r = ((x-x0)**2 + (y-y0)**2)**0.5
    g_x=-(G*M/r**2)*(x-x0)/r
    g_y=-(G*M/r**2)*(y-y0)/r
    return (g_x, g_y)

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100,100))
        self.surf.fill((8,23,43))
        self.rect =self.surf.get_rect(center=(LENGTH/2,WIDTH/2))
        pygame.draw.circle(self.surf,(243,165,5),(50,50),50)
        self.Mass=0
        
    def gravity(self,x,y):
        G=1.0
        return gr(x, y, self.rect.x, self.rect.y, G, self.Mass)
    
def gameOver(player):
#                player.surf =pygame.Surface((1,1))
#                player.surf.fill((8,23,43))
#                player.original_surf=player.surf;
                player.gameover = True
                player.kill()
                

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,flag):
        
        super().__init__()
        self.surf = pygame.Surface((4,4)) 
        self.surf.fill((255,255,255))
        if flag:
            pygame.draw.circle(self.surf,(89, 255, 235),(4,4),50)        
        else:
            pygame.draw.circle(self.surf,(244, 199, 102),(4,4),50)
        self.original_surf=self.surf;
        self.vel_x = 0
        self.vel_y = 0
        self.player_vel_x = player.vel_x
        self.player_vel_y = player.vel_y
        x = (player.rect.left + player.rect.right)/2 + 10*math.cos((player.angle)*math.pi/180)
        y = (player.rect.bottom + player.rect.top)/2 - 10*math.sin((player.angle)*math.pi/180)
        self.rect = self.surf.get_rect(center=(x + 2, y + 2))
        self.angle = player.angle
        
    def update(self):
        self.vel_x = 10*math.cos((self.angle)*math.pi/180) + self.player_vel_x
        self.vel_y = 10*math.sin((self.angle)*math.pi/180) - self.player_vel_y
        self.rect.x += self.vel_x
        self.rect.y -= self.vel_y
        
        if (self.rect.x < 0) or (self.rect.x > LENGTH):# убивает пульку
            pass
        
class Player(pygame.sprite.Sprite,):
    
    def __init__(self,go_left,go_right,go_stright,pl_fire,position,angle,ship,ship_thrust):       
        super().__init__()
        self.ship = pygame.image.load(ship)
        self.surf = self.ship
        self.thrust = pygame.image.load(ship_thrust)
        self.engine_vel=0.5
        self.engine=0
        self.surf.set_colorkey((255,255,255))
        self.thrust.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect(center=position)
        self.original_surf=self.surf
        self.vel_x=0
        self.vel_y=0
        self.angle= angle
        self.gameover=False
        self.go_left = go_left
        self.go_right = go_right
        self.go_stright = go_stright
        self.pl_fire = pl_fire
        
        
    def povorot(self,key):
        ship1=self.original_surf;
        if key == self.go_left:    
            self.angle=self.angle+5
        elif key == self.go_right:
            self.angle=self.angle-5
        angle=self.angle
        ship2=pygame.transform.rotate(ship1,angle)
        return ship2
    
    
    def update(self,SUN):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[self.go_left]:
            self.surf=self.povorot(self.go_left)
        if pressed_key[self.go_right]:
            self.surf=self.povorot(self.go_right)
        if pressed_key[self.go_stright]:
            self.surf = pygame.transform.rotate(self.thrust,self.angle)
            self.engine=1
        else:
            self.engine=0
            self.surf = pygame.transform.rotate(self.ship,self.angle)
        
        (gx_save,gy_save)=SUN.gravity(self.rect.x,self.rect.y)
        x_save = self.rect.x+self.vel_x
        y_save = self.rect.y + self.vel_y
        gx = 0.5*(gx_save + SUN.gravity(x_save,y_save)[0])
        gy = 0.5*(gy_save + SUN.gravity(x_save, y_save)[1])
        
        
        self.rect.x += self.vel_x + gx*0.5
        self.rect.y += self.vel_y + gy*0.5
        self.vel_x += 0.5*(gx +self.engine*self.engine_vel*math.cos((self.angle)*math.pi/180))
        self.vel_y += 0.5*(gy -self.engine*self.engine_vel*math.sin((self.angle)*math.pi/180))
        if self.rect.left > LENGTH: self.rect.right=0
        if self.rect.right<0: self.rect.left=LENGTH
        if self.rect.top>WIDTH:self.rect.bottom=0
        if self.rect.bottom<0:self.rect.top=WIDTH
        
class Game:
    def main(self,screen):
        main_game = Game()
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        background.fill((8,23,43))
        players = pygame.sprite.Group()        
                
        SUN=Star()
        player1 = Player(
                go_left = pygame.K_a,
                go_right = pygame.K_d,            #Управление
                go_stright = pygame.K_w,
                pl_fire = pygame.K_SPACE,
                position = [100, WIDTH/2 - 100],
                angle = 180,
                ship = 'ship.gif',
                ship_thrust = 'ship_thrust.gif'
                )
        players.add(player1)
        player2 = Player(
                go_left = pygame.K_LEFT,
                go_right = pygame.K_RIGHT,            #Управление
                go_stright = pygame.K_UP,
                pl_fire = pygame.K_RSHIFT,
                position = [LENGTH-100, WIDTH/2 - 100],
                angle = 0,
                ship = 'ship_2.gif',
                ship_thrust = 'ship_2_thrust.gif'
                )
        
        
        players.add(player2)
        bullets = pygame.sprite.Group()
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main_game.main(screen)   #Restart
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit() 
                        
#                for player in players:        
                if event.type == pygame.KEYDOWN and (player1.gameover == False  and  player2.gameover == False):#стреляю
                    if event.key == player1.pl_fire:
                        
                        new_bullet1 = Bullet(player1,True)
                        bullets.add(new_bullet1)
                    elif event.key == player2.pl_fire:
                        new_bullet2 = Bullet(player2,False)
                        bullets.add(new_bullet2)
                        
            screen.blit(background, (0,0))
            screen.blit(SUN.surf,SUN.rect) 
            
            
            
            
                    
                    
            for bullet in bullets:
                        
                        bullet.update()
            
            
            
            for player in players:
                screen.blit(player.surf,player.rect)
                collision=pygame.sprite.collide_circle_ratio(0.8)
                if collision(player,SUN):
                        print('Gameover((')
                        gameOver(player)
                for bullet in bullets:
                    screen.blit(bullet.surf,bullet.rect)
                    
                    collision=pygame.sprite.collide_circle_ratio(0.8)
                    
                    if collision(player,bullet):
                        print('Gameover((')
                        gameOver(player)
                        bullet.kill()   #Пулька исчезает
                        
            
                        
            if not player1.gameover and not player2.gameover:
                    player1.update(SUN)
                    player2.update(SUN)
               
            if player1.gameover and player2.gameover:
                
                player1.surf = pygame.Surface((1,1))
                player1.surf.fill((0,0,0))
                
                player2.surf = pygame.Surface((1,1))
                player2.surf.fill((0,0,0))
                
                font = pygame.font.Font(None, 50)
                text = font.render('Lol, you both DIE ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
                player1.original_surf = player1.surf
                
                
                
                
            elif player1.gameover :
                player1.surf = pygame.Surface((1,1))
                player1.surf.fill((0,0,0))
                font = pygame.font.Font(None, 50)
                text = font.render('Lol, player2 WINS ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
                player1.original_surf = player1.surf
                
            
            elif player2.gameover :
                player2.surf = pygame.Surface((1,1))
                player2.surf.fill((0,0,0))
                font = pygame.font.Font(None, 50)
                text = font.render('Lol, player 1 WINS ',True,(255,255,0))
                text_length, text_width = text.get_size()
                screen.blit(text,(LENGTH/2 - text_length/2 + 1 , WIDTH/2- text_width/2 + 100))
                player2.original_surf = player2.surf
            
            
                
            pygame.display.flip()
                

pygame.init()
screen = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption('Space spirit: matvey edition')
game=Game()
game.main(screen)


    
    
        
    

  