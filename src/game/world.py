import pygame
from pipe import Pipe
class World():

    def __init__(self) -> None:
        # sprites
        self.BG_DAY = "data/sprites/background-day.png" #background
        self.BG_NIGHT = "data/sprites/background-night.png"
        self.BASE = "data/sprites/base.png"
        self.BASE_HEIGHT = 112 
        # variables
        self.GRAVITY = 0.08
        self.pipes = []

    def add_pipes(self, pipe1, pipe2):
        self.pipes.extend([pipe1, pipe2])

    def remove_unused_pipes(self):
        for pipe in self.pipes:
            if pipe.x < - pipe.PIPE_WIDTH:
                self.pipes.remove(pipe)

    def clear_pipes(self):
        self.pipes.clear()

    def generate_pipes (self, SCREEN_SIZE):
        pipe1 = Pipe(SCREEN_SIZE)
        pipe2 = Pipe(SCREEN_SIZE, pipe1.x, pipe1.y)
        self.add_pipes(pipe1, pipe2)
        if len(self.pipes) != 0: 
            self.remove_unused_pipes()