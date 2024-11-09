#Débora Cardoso

import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

principal_directory = os.path.dirname(__file__)
images_directory = os.path.join(principal_directory, 'image')
sound_directory = os.path.join(principal_directory, 'sound')

WIDTH = 640
HIGHT = 480
    
WHITE = (255,255,255)

display = pygame.display.set_mode((WIDTH, HIGHT))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(images_directory, 'Spritesheet.png')).convert_alpha()

clash_sound = pygame.mixer.Sound(os.path.join(sound_directory, 'death_sound.wav'))
clash_sound.set_volume(1)

score_sound = pygame.mixer.Sound(os.path.join(sound_directory, 'score_sound.wav'))
score_sound.set_volume(1)

collided = False

choose_obstacle = choice([0, 1])

points = 0

game_speed = 10

def show_message(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    message = f'{msg}' 
    texto_formatado = fonte.render(message, True, cor)
    return texto_formatado

def restart_game():
    global points, game_speed, collided, choose_obstacle
    points = 0
    game_speed = 10
    collided = False
    dino.rect.y = (HIGHT - 64 - 96)//2
    dino.jump = False
    flying_dino.rect.x = WIDTH
    cactus.rect.x = WIDTH
    choose_obstacle = choice([0, 1])

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sound_jump = pygame.mixer.Sound(os.path.join(sound_directory, 'jump_sound.wav'))
        self.sound_jump.set_volume(1)
        self.image_dinossaur = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.image_dinossaur.append(img)
        
        self.index_lista = 0
        self.image = self.image_dinossaur[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 370
        self.rect.center = (100, self.pos_y_inicial) 
        self.jump = False

    def jumping(self):
        self.jump = True
        self.sound_jump.play()

    def update(self):

        if self.jump == True:
            if self.rect.y <= self.pos_y_inicial - 150:
                self.jump = False
            self.rect.y -= 15

        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += 15
        
 
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.image_dinossaur[int(self.index_lista)]

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = WIDTH - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= game_speed

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y =  415
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
        self.rect.x -= 10
    
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.choose = choose_obstacle
        self.rect.center = (WIDTH,  HIGHT - 64)
        self.rect.x = WIDTH

    def update(self):
        if self.choose == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH
            self.rect.x -= game_speed

class FlyingDino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_dinossaur = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.image_dinossaur.append(img)

        self.index_lista = 0
        self.image = self.image_dinossaur[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.choose = choose_obstacle
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 300)
        self.rect.x = WIDTH
    
    def update(self):
        if self.choose == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH
            self.rect.x -= game_speed

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.image_dinossaur[int(self.index_lista)]

sprites = pygame.sprite.Group()
dino = Dino()
sprites.add(dino)

for i in range(4):
    cloud = Clouds()
    sprites.add(cloud)

for i in range(WIDTH*2//64):
    floor = Floor(i)
    sprites.add(floor)

cactus = Cactus()
sprites.add(cactus)

flying_dino = FlyingDino()
sprites.add(flying_dino)

group_obstacles = pygame.sprite.Group()
group_obstacles.add(cactus)
group_obstacles.add(flying_dino)

timer = pygame.time.Clock()
while True:
    timer.tick(30)
    display.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and collided == False:
                dino.jumping()
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.jumping()

            if event.key == K_SPACE and collided == True:
                restart_game()

    collisions = pygame.sprite.spritecollide(dino, group_obstacles, False, pygame.sprite.collide_mask)

    sprites.draw(display)

    if cactus.rect.topright[0] <= 0 or flying_dino.rect.topright[0] <= 0:
        choose_obstacle = choice([0, 1])
        cactus.rect.x = WIDTH
        flying_dino.rect.x = WIDTH
        cactus.choose = choose_obstacle
        flying_dino.choose = choose_obstacle

    if collisions and collided == False:
        clash_sound.play()
        collided = True

    if collided == True:
        if points % 100 == 0:
            points += 1
        game_over = show_message('G A M E  O V E R', 40, (0,0,0))
        display.blit(game_over, (120, (HIGHT//2)))
        restart = show_message('Press space to restart!', 20, (0,0,0))
        display.blit(restart, (180, (HIGHT//2) + 60))

    else:
        points += 1
        sprites.update()
        text_points = show_message(points, 40, (0,0,0))

    if points % 100 == 0:
        score_sound.play()
        if game_speed >= 23:
            game_speed += 0
        else:
            game_speed += 1
        
    display.blit(text_points, (520, 30))

    pygame.display.flip()