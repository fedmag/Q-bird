import pygame
import sys

from pygame.sprite import collide_rect
from bird import Bird
from world import World
from pipe import Pipe

 
SCREEN_SIZE = (288, 512)
MOV_SPEED = 1 

class MySprite(pygame.sprite.Sprite):
    def __init__(self, bird) -> None:
        super(MySprite, self).__init__()
        self.images = [screen.blit(pygame.image.load(bird.UP_FLAP).convert_alpha(), bird.hitbox), 
                       screen.blit(pygame.image.load(bird.DOWN_FLAP).convert_alpha(), bird.hitbox),
                       screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird.hitbox)]
        self.index = 0
        self.rect = pygame.Rect(bird.hitbox)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE) # screen size
clock = pygame.time.Clock()
game_running = True
score = 0 

world = World()
bird = Bird()
bird_icon = bird.MID_FLAP
base_x = 0

my_sprite = MySprite(bird)
my_group = pygame.sprite.Group(my_sprite)

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
    if bird_icon == bird.MID_FLAP:
        screen.blit(pygame.image.load(bird.UP_FLAP).convert_alpha(), bird.hitbox)
    if bird_icon == bird.UP_FLAP:
        screen.blit(pygame.image.load(bird.DOWN_FLAP).convert_alpha(), bird.hitbox)
    if bird_icon == bird.DOWN_FLAP:
        screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird.hitbox)

def draw_score():
    # font = pygame.font.Font(pygame.font.match_font('arial'), 30)
    font = pygame.font.SysFont("ubuntu", 30)
    text_surface = font.render(str(score), True, (255, 0 , 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (SCREEN_SIZE[0] - 50, 20)
    screen.blit(text_surface, text_rect)

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
                score = 0
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
    draw_score()
    draw_game_over()
    my_group.draw(screen)
    screen.blit(pygame.image.load(bird_icon).convert_alpha(), bird.hitbox) # bird -> convert_alpha is need for transparent bg 
    pygame.display.update() 
    clock.tick(120)

