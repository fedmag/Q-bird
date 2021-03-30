import pygame
class Bird():
    
    def __init__(self) -> None:
        # parameters
        self.INITIAL_X = 50
        self.INITIAL_Y = 200
        self.x = self.INITIAL_X
        self.y = self.INITIAL_Y
        self.FLY_DISTANCE = 20
        self.mov_speed = 0
        # sprites
        self.sprite_w = 34
        self.sprite_h = 24
        self.MID_FLAP = "data/sprites/bluebird-midflap.png"
        self.DOWN_FLAP = "data/sprites/bluebird-downflap.png"
        self.UP_FLAP = "data/sprites/bluebird-upflap.png"
        # hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.sprite_w -2 , self.sprite_h -2) # -2 is being more forgiving

    
    def fall(self, gravity):
        self.mov_speed += gravity
        # print(self.mov_speed)
        self.y += self.mov_speed
        self.hitbox.centery += self.mov_speed

    def fly(self):
        self.mov_speed = -1.5 # giving an initial boost to improve the animation
        self.y -= self.FLY_DISTANCE
        self.hitbox.centery -= self.FLY_DISTANCE

    def relocate(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.centery = self.y

    def restart(self):
        self.relocate(self.INITIAL_X, self.INITIAL_Y)
        self.mov_speed = 0