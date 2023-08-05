import pygame
from sys import exit
from random import randint, choice
global game
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dino_run_1 = pygame.image.load('graphics/dino/DinoRun1.png').convert_alpha()
        dino_dead =pygame.image.load('graphics/dino/DinoDead.png').convert_alpha()
        dino_run_2 = pygame.image.load('graphics/dino/DinoRun2.png').convert_alpha()
        self.dino_run = [dino_run_1, dino_run_2, dino_dead]
        self.dino_index = 0
        self.dino_jump = pygame.image.load('graphics/dino/DinoJump.png').convert_alpha()
        dino_duck_1 = pygame.image.load('graphics/dino/DinoDuck1.png').convert_alpha()
        dino_duck_2 = pygame.image.load('graphics/dino/DinoDuck2.png').convert_alpha()
        self.dino_duck = [dino_duck_1, dino_duck_2]
        self.dino_duck_index = 0
        self.image = self.dino_run[self.dino_index]
        self.rect = self.image.get_rect(midbottom=(150, 331))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def dino_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not key[pygame.K_DOWN] and self.rect.bottom >= 331 or key[pygame.K_UP] and self.rect.bottom >= 331 and not key[pygame.K_DOWN]:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 331: self.rect.bottom = 331

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom < 331:
            self.image = self.dino_jump
            return 5
        elif keys[pygame.K_DOWN]:
            self.dino_index += 0.1
            self.rect.y = 275
            if self.dino_index >= len(self.dino_duck): self.dino_index = 0
            self.image = self.dino_duck[int(self.dino_index)]
            return 1
        else:
            self.dino_index += 0.1
            if self.dino_index >= 2: self.dino_index = 0
            self.image = self.dino_run[int(self.dino_index)]
            if done == 1:
                self.dino_index = 2
                self.image = dino_dead

    def dead(self):
        global counter
        self.image = pygame.image.load('graphics/dino/DinoDead.png')
        if counter == 0 and self.animation_state() == 5:
            self.rect.move_ip(0,-10)
            counter += 1


    def update(self):
        if done == 0:
            self.dino_input()
            self.apply_gravity()
            self.animation_state()
        elif done == 1 and self.animation_state() == 5:
           self.dead()
        else:
            self.dead()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        global game_speed
        if type == 'fly':
            bird_fly = pygame.image.load('graphics/bird/bird1.png').convert_alpha()
            bird_fly_2 = pygame.image.load('graphics/bird/Bird2.png').convert_alpha()
            self.frames = [bird_fly, bird_fly_2]
            y_pos = 250
        elif type == '1':
            small_cactus = pygame.image.load('graphics/cactus/SmallCactus1.png').convert_alpha()
            self.frames = [small_cactus]
            y_pos = 324
        elif type == '2':
            small_cactus_2 = pygame.image.load('graphics/cactus/SmallCactus2.png').convert_alpha()
            self.frames = [small_cactus_2]
            y_pos = 324
        elif type == '3':
            small_cactus_3 = pygame.image.load('graphics/cactus/SmallCactus3.png').convert_alpha()
            self.frames = [small_cactus_3]

            y_pos = 324
        elif type == '4':
            large_cactus = pygame.image.load('graphics/cactus/LargeCactus1.png').convert_alpha()
            self.frames = [large_cactus]
            y_pos = 324
        elif type == '5':
            large_cactus_2 = pygame.image.load('graphics/cactus/LargeCactus2.png').convert_alpha()
            self.frames = [large_cactus_2]
            y_pos = 324
        elif type == '6':
            large_cactus_3 = pygame.image.load('graphics/cactus/LargeCactus3.png').convert_alpha()
            self.frames = [large_cactus_3]
            y_pos = 324

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_pos))
        self.mask = pygame.mask.from_surface(self.image)
    def obs_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.obs_animation()
        self.rect.x -= game_speed
        if  324 < self.rect.y <270 :
            self.rect.x -= game_speed + 3
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + randint(800, 1000)
        self.y = randint(50, 100)
        self.image = cloud
        self.width = self.image.get_width()

    def update(self):
        global game_speed
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + randint(2500, 3000)
            self.y = randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def score():
     zeroes = "000"
     current_time = int(pygame.time.get_ticks()/100) - start_time
     score_surf = game_font.render(f"{0}{0}{0}{current_time}", False, '#787878')
     if 100 <= current_time < 1000:
         score_surf = game_font.render(f"{0}{0}{current_time}", False, '#787878')
     if 1000 <= current_time < 10000:
         score_surf = game_font.render(f"{0}{current_time}", False, '#787878')
     if current_time >= 10000:
         score_surf = game_font.render(f"{current_time}", False, '#787878')
     if int(current_time) % 100 == 0 and current_time != 0:
         score_sound.play()
     elif int(current_time) % 500 == 0 and current_time != 0:
         game_speed += 1
     screen.blit(score_surf, (890,10))

def collision_sprite():
    if pygame.sprite.spritecollide(dino, obstacle_group, False, pygame.sprite.collide_mask):
        obstacle_group.empty()
        die_sound.play()
        return False
    else:
        return True


def move_ground():
    if surf_rect.x <= 2404:
        screen.blit(ground_copy, copy_rect)
    if surf_rect.x <= -2404:
        surf_rect.x = 0
        copy_rect.x = 2404
        screen.blit(ground_surface, surf_rect)


pygame.init() #initializles the screen
screen = pygame.display.set_mode((1000, 400))
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 1000
pygame.display.set_caption('Dino Game')
clock = pygame.time.Clock()
replay = pygame.image.load('graphics/other/Reset.png')
replay_rect = replay.get_rect(midbottom=(480,260))
score_sound = pygame.mixer.Sound('audio/point.mp3')
score_sound.set_volume(0.1)
game_font = pygame.font.Font('font/PressStart2p.ttf', 20)
game = True
game_speed = 10
start_time = 00000
background_color = pygame.Surface((1000,400))
background_color.fill('#FFFFFF')
global done
done = 0
cloud = pygame.image.load('graphics/other/cloud.png').convert_alpha()
ground_surface = pygame.image.load('graphics/other/Track.png').convert_alpha()
ground_copy = ground_surface
copy_rect = ground_copy.get_rect(midbottom=(2404, 328))
surf_rect = ground_surface.get_rect(midbottom=(0, 328))
counter = 0

text_surface = game_font.render('00000', False, '#787878')
mouse_pos = pygame.mouse.get_pos()

#Groups
dino = Dino()

dino_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group.add(dino)
die_sound = pygame.mixer.Sound('audio/die.mp3')

cloud = Cloud()

dino_dead = pygame.image.load('graphics/dino/DinoDead.png')

bird_animation_timer = pygame.USEREVENT + 8
pygame.time.set_timer(bird_animation_timer, 15000)


gameover = pygame.image.load('graphics/other/GameOver.png')

keys = pygame.key.get_pressed()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #does the opposite of initializing the screen
            exit() #stops the while true statement
        if game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONUP and replay_rect.collidepoint(mouse_pos):
                game = True
                counter = 0
                done = 0
                start_time = int(pygame.time.get_ticks()/100)

        if event.type == obstacle_timer and game or event.type == bird_animation_timer:
            obstacle_group.add(Obstacle(choice(['fly', 'fly', '1', '1','1','1', '2', '2', '3', '3', '3', '4', '4','4','5','5','6'])))

    if game:
        screen.blit(background_color, (0,0))
        screen.blit(ground_surface, surf_rect)
        screen.blit(ground_copy, copy_rect)
        score()
        move_ground()
        surf_rect.x -= game_speed
        copy_rect.x -= game_speed
        dino_group.draw(screen)
        dino_group.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        cloud.draw(screen)
        cloud.update()

        game = collision_sprite()
    if not game:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(gameover, (300, 100))
        screen.blit(replay, replay_rect)
        done = 1
        clock.tick(100)
        dino_group.draw(screen)
        dino_group.update()
        gravity = 0
        surf_rect.x = 0
        copy_rect.x = 2404


    pygame.display.update()
    clock.tick(60)
