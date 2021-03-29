import pygame
import sys
from bird import Bird
from world import World
from pipe import Pipe

 
SCREEN_SIZE = (288, 512)
MOV_SPEED = 1 

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE) # screen size
clock = pygame.time.Clock()
game_running = True

world = World()
bird = Bird()
bird_rect = pygame.Rect(bird.x, bird.y, bird.sprite_w, bird.sprite_h)
base_x = 0

def draw_base():
    screen.blit(pygame.image.load(world.BASE), (base_x, SCREEN_SIZE[1] - world.BASE_HEIGHT))
    screen.blit(pygame.image.load(world.BASE), (base_x + SCREEN_SIZE[0], SCREEN_SIZE[1] - world.BASE_HEIGHT))

def detect_collision():
    if(bird_rect.top <= 0  or bird_rect.bottom >= SCREEN_SIZE[1] - world.BASE_HEIGHT):
        return False
    return True

def draw_pipes():
    if game_running:
        for pipe in world.pipes:
            screen.blit(pygame.image.load(pipe.GREEN_SPRITE), (pipe.x, pipe.y))
            pipe.move(MOV_SPEED)

def draw_game_over():
    if not game_running:
        screen.blit(pygame.image.load("data/sprites/gameover.png"), (50, 100))

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)


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
                # bird.fall(0)
                bird.fly()

            if event.key == pygame.K_SPACE and not game_running:
                bird.x, bird.y = 50, 200
                game_running = True
        if event.type == SPAWN_PIPE and game_running:
            pipe = Pipe(SCREEN_SIZE)
            world.generate_pipes(pipe)
    
    if game_running:
        bird.fall(world.GRAVITY) # the bird falls at each iteration
        bird_rect.topleft = (bird.x, bird.y) # rectangle always coincide with the position of the bird
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
    screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird_rect) # bird -> convert_alpha is need for transparent bg 
    # pygame.draw.rect(screen, (255, 0, 0, 55), bird_rect)
    pygame.display.update() 
    clock.tick(120)

