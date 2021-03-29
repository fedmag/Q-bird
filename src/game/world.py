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

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def remove_unused_pipes(self):
        for pipe in self.pipes:
            if pipe.x < - pipe.PIPE_WIDTH:
                self.pipes.remove(pipe)

    def clear_pipes(self):
        self.pipes.clear()

    def generate_pipes (self, SCREEN_SIZE):
        pipe = Pipe(SCREEN_SIZE)
        self.add_pipe(pipe)
        if len(self.pipes) != 0: 
            self.remove_unused_pipes()