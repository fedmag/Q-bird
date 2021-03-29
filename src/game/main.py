import pygame
import sys

from pygame.sprite import collide_rect
from bird import Bird
from world import World
from pipe import Pipe

 
SCREEN_SIZE = (288, 512)
MOV_SPEED = 1 

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE) # screen size
clock = pygame.time.Clock()
game_running = True
score = 0

world = World()
bird = Bird()
base_x = 0

def draw_base():
    screen.blit(pygame.image.load(world.BASE), (base_x, SCREEN_SIZE[1] - world.BASE_HEIGHT))
    screen.blit(pygame.image.load(world.BASE), (base_x + SCREEN_SIZE[0], SCREEN_SIZE[1] - world.BASE_HEIGHT))

def detect_collision():
    if(bird.hitbox.top <= 0  or bird.hitbox.bottom >= SCREEN_SIZE[1] - world.BASE_HEIGHT):
        return False
    for pipe in world.pipes:
        if bird.hitbox.colliderect(pipe.hitbox) == 1:
            return False
    return True

def draw_pipes():
    if game_running:
        for pipe in world.pipes:
            if pipe.cieling_pipe:
                screen.blit(pygame.image.load(pipe.GREEN_SPRITE_REVERSE),  (pipe.x, (pipe.y)))
            else:
                screen.blit(pygame.image.load(pipe.GREEN_SPRITE), (pipe.x, pipe.y))
            pipe.move(MOV_SPEED)

def draw_game_over():
    if not game_running:
        screen.blit(pygame.image.load("data/sprites/gameover.png"), (50, 100))

def wing_animation():
    screen.blit(pygame.image.load(bird.UP_FLAP).convert_alpha(), bird.hitbox)
    screen.blit(pygame.image.load(bird.DOWN_FLAP).convert_alpha(), bird.hitbox)

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1000)

while True: # game loop
    game_running = detect_collision()
    # event management
    for event in pygame.event.get():
        # quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_running:
                bird.fall(0)
                bird.fly()
                wing_animation()
            if event.key == pygame.K_SPACE and not game_running:  
                bird.restart()
                world.clear_pipes()
                game_running = True
        if event.type == SPAWN_PIPE and game_running:
            world.generate_pipes(SCREEN_SIZE )
            score += 1
            print(score)
    
    if game_running:
        bird.fall(world.GRAVITY) # the bird falls at each iteration
        base_x -= MOV_SPEED
        if base_x <= - SCREEN_SIZE[0]:
            base_x = 0
        
    else:
        draw_game_over()

    # redraw the screen
    screen.blit(pygame.image.load(world.BG_DAY), (0,0)) # bg -> this must be the first element
    draw_pipes() 
    draw_base()
    detect_collision()
    draw_game_over()
    screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird.hitbox) # bird -> convert_alpha is need for transparent bg 
    # pygame.draw.rect(screen, (255, 0, 0, 55), bird.hitbox)
    # for i, pipe in enumerate(world.pipes):
    #     print(pipe.hitbox)
    #     pygame.draw.rect(screen, (255,0, 0), pipe.hitbox)
    pygame.display.update() 
    clock.tick(120)

