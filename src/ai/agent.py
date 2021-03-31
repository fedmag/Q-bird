from flappy_bird import FlappyBird
from q_net import Q_net
class Agent():
    def __init__(self) -> None:
        self.q_net = Q_net()