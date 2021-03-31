import sys
sys.path.append("/home/fedmag/Projects/Q-bird/src/game/")
sys.path.append("/home/fedmag/Projects/Q-bird/src/ai/")

# from agent import Agent
from flappy_bird import FlappyBird

# agent = Agent()

game = FlappyBird()
game.run()

print(sys.path)