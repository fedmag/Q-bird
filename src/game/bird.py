
class Bird():
    
    def __init__(self) -> None:
        # parameters
        self.x = 50
        self.y = 200
        self.FLY_DISTANCE = 100

        # sprites
        self.sprite_w = 34
        self.sprite_h = 24
        self.MID_FLAP = "data/sprites/bluebird-midflap.png"
        self.DOWN_FLAP = "data/sprites/bluebird-downflap.png"
        self.UP_FLAP = "data/sprites/bluebird-upflap.png"

    
    def fall(self, gravity):
        self.y += gravity

    def fly(self):
        self.y -= self.FLY_DISTANCE