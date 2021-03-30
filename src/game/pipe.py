import random
import pygame
class Pipe():

    def __init__(self, SCREEN_SIZE) -> None:
        self.cieling_pipe = bool(random.getrandbits(1))
        self.GREEN_SPRITE = "data/sprites/pipe-green.png"
        self.GREEN_SPRITE_REVERSE = "data/sprites/pipe-green-reverse.png"
        self.RED_SPRITE = "data/sprites/pipe-red.png"
        self.PIPE_HEIGHT = 320
        self.PIPE_WIDTH = 52
        self.TOP_POS = [ -250, -200, -150, -100 ]
        self.BOT_POS = [SCREEN_SIZE[1] - 250, SCREEN_SIZE[1] - 230, SCREEN_SIZE[1] -200, SCREEN_SIZE[1] - 180, SCREEN_SIZE[1] - 150]
        if self.cieling_pipe:
            self.x = random.randint(SCREEN_SIZE[0], SCREEN_SIZE[0] + 70)
            self.y = random.choice(self.TOP_POS)
        else:
            self.x = random.randint(SCREEN_SIZE[0], SCREEN_SIZE[0] + 70)
            self.y = random.choice(self.BOT_POS)
        # hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.PIPE_WIDTH - 2, self.PIPE_HEIGHT - 2) # -2 is being more forgiving

    def move(self, mov_speed):
        self.x -= mov_speed
        self.hitbox.centerx -= mov_speed

    def relocate(self, x, y):
        self.y = y
        self.x = x
        self.hitbox.centery = self.y
        self.hitbox.centerx = self.x