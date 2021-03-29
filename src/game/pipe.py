from pygame import init


import random
class Pipe():

    def __init__(self, SCREEN_SIZE) -> None:
        self.GREEN_SPRITE = "data/sprites/pipe-green.png"
        self.RED_SPRITE = "data/sprites/pipe-red.png"
        self.PIPE_HEIGHT = 320
        self.PIPE_WIDTH = 52
        self.x = random.randint(SCREEN_SIZE[0], SCREEN_SIZE[0] * 2)
        self.y = random.randint( 200 , SCREEN_SIZE[1] + 100)

    def move(self, mov_speed):
        self.x -= mov_speed