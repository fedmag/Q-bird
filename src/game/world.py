class World():

    def __init__(self) -> None:
        # sprites
        self.BG_DAY = "data/sprites/background-day.png" #background
        self.BG_NIGHT = "data/sprites/background-night.png"
        self.BASE = "data/sprites/base.png"
        self.BASE_HEIGHT = 112 
        # variables
        self.GRAVITY = 1.7
        self.pipes = []

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def remove_unused_pipes(self):
        for pipe in self.pipes:
            if pipe.x < - pipe.PIPE_WIDTH:
                self.pipes.remove(pipe)

    def generate_pipes (self, pipe):
        self.add_pipe(pipe)
        self.remove_unused_pipes()