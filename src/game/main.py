import pygame
import sys
from bird import Bird
from world import World


SCREEN_SIZE = (288, 512)

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

def draw_game_over():
    if not game_running:
        screen.blit(pygame.image.load("data/sprites/gameover.png"), (50, 100))


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

            if event.key == pygame.K_SPACE and not game_running:
                bird.x, bird.y = 50, 200
                game_running = True
    
    if game_running:
        bird.fall(world.GRAVITY) # the bird falls at each iteration
        bird_rect.topleft = (bird.x, bird.y) # rectangle always coincide with the position of the bird
        base_x -=1
        if base_x <= - SCREEN_SIZE[0]:
            base_x = 0
    else:
        draw_game_over()

    # redraw the screen
    screen.blit(pygame.image.load(world.BG_DAY), (0,0)) # bg -> this must be the first element
    draw_base()
    detect_collision()
    draw_game_over()
    screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird_rect) # bird -> convert_alpha is need for transparent bg 
    # pygame.draw.rect(screen, (255, 0, 0, 55), bird_rect)
    pygame.display.update() 
    clock.tick(120)

