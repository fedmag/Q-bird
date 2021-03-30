import pygame
import sys

from bird import Bird
from world import World
from pipe import Pipe

class Game():

    def __init__(self) -> None:
        self.SCREEN_SIZE = (288, 512)
        self.MOV_SPEED = 1 
        # FIXME: fix the animation
        # class MySprite(pygame.sprite.Sprite):
        #     def __init__(self, bird) -> None:
        #         super(MySprite, self).__init__()
        #         self.images = [self.screen.blit(pygame.image.load(bird.UP_FLAP).convert_alpha(), bird.hitbox), 
        #                        self.screen.blit(pygame.image.load(bird.DOWN_FLAP).convert_alpha(), bird.hitbox),
        #                        self.screen.blit(pygame.image.load(bird.MID_FLAP).convert_alpha(), bird.hitbox)]
        #         self.index = 0
        #         self.rect = pygame.Rect(bird.hitbox)

        #     def update(self):
        #         if self.index >= len(self.images):
        #             self.index = 0
        #         self.image = self.images[self.index]
        #         self.index += 1
        
        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE) # self.screen size
        pygame.display.set_caption("q-bird")
        self.clock = pygame.time.Clock()
        # variables
        self.game_running = True
        self.score = 0 
        self.world = World()
        self.bird = Bird()
        self.bird_icon = self.bird.MID_FLAP
        self.base_x = 0
        # spawns
        self.SPAWN_PIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWN_PIPE, 1000)

        # TODO: fix the animation
        # my_sprite = MySprite(bird)
        # my_group = pygame.sprite.Group(my_sprite)

    def draw_base(self):
        self.screen.blit(pygame.image.load(self.world.BASE), (self.base_x, self.SCREEN_SIZE[1] - self.world.BASE_HEIGHT))
        self.screen.blit(pygame.image.load(self.world.BASE), (self.base_x + self.SCREEN_SIZE[0], self.SCREEN_SIZE[1] - self.world.BASE_HEIGHT))

    def detect_collision(self):
        if(self.bird.hitbox.top <= 0  or self.bird.hitbox.bottom >= self.SCREEN_SIZE[1] - self.world.BASE_HEIGHT):
            return False
        for pipe in self.world.pipes:
            if self.bird.hitbox.colliderect(pipe.hitbox) == 1:
                return False
        return True

    def draw_pipes(self):
        if self.game_running:
            for pipe in self.world.pipes:
                if pipe.cieling_pipe:
                    self.screen.blit(pygame.image.load(pipe.GREEN_SPRITE_REVERSE),  (pipe.x, (pipe.y)))
                else:
                    self.screen.blit(pygame.image.load(pipe.GREEN_SPRITE), (pipe.x, pipe.y))
                pipe.move(self.MOV_SPEED)

    def draw_game_over(self):
        if not self.game_running:
            self.screen.blit(pygame.image.load("data/sprites/gameover.png"), (50, 100))

    # FIXME
    def wing_animation(self):
        if self.bird_icon == self.bird.MID_FLAP:
            self.screen.blit(pygame.image.load(self.bird.UP_FLAP).convert_alpha(), self.bird.hitbox)
        if self.bird_icon == self.bird.UP_FLAP:
            self.screen.blit(pygame.image.load(self.bird.DOWN_FLAP).convert_alpha(), self.bird.hitbox)
        if self.bird_icon == self.bird.DOWN_FLAP:
            self.screen.blit(pygame.image.load(self.bird.MID_FLAP).convert_alpha(), self.bird.hitbox)

    def draw_score(self):
        # font = pygame.font.Font(pygame.font.match_font('arial'), 30)
        font = pygame.font.SysFont("ubuntu", 30)
        text_surface = font.render(str(self.score), True, (255, 0 , 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.SCREEN_SIZE[0] - 50, 20)
        self.screen.blit(text_surface, text_rect)

    def get_state(self):
        top_distance = self.bird.hitbox.top
        bot_distance = (self.SCREEN_SIZE[1] - self.world.BASE_HEIGHT) - self.bird.hitbox.bottom
        closest_pipe_top = None
        closest_pipe_bot = None
        for pipe in self.world.pipes:
            if pipe != None:
                if pipe.cieling_pipe: # top pipes
                    if closest_pipe_top == None:
                        closest_pipe_top = pipe
                    else: 
                        _, current_pipe_dist = self.get_distances(closest_pipe_top)
                        _, candidate_pipe_dist = self.get_distances(pipe)
                        if candidate_pipe_dist < current_pipe_dist:
                            closest_pipe_top = pipe
                else: # bot pipes
                    if closest_pipe_bot == None:
                        closest_pipe_bot = pipe
                    else: 
                        _, current_pipe_dist = self.get_distances(closest_pipe_bot)
                        _, candidate_pipe_dist = self.get_distances(pipe)
                        if candidate_pipe_dist < current_pipe_dist:
                            closest_pipe_bot = pipe
        if closest_pipe_bot != None and closest_pipe_top != None:
            top_v_dist, top_h_dist = self.get_distances(closest_pipe_top)
            bot_v_dist, bot_h_dist = self.get_distances(closest_pipe_bot)
            print(f"top: v {top_v_dist}, h {top_h_dist}")
            print(f"bot: v {bot_v_dist}, h {bot_h_dist}")
            print("====================")


    def get_distances(self, pipe):
        if pipe != None:
            if pipe.cieling_pipe: # top_pipe
                v_dist = self.bird.hitbox.top - pipe.hitbox.bottom
            else: # bot pipe
                v_dist = pipe.hitbox.bottom - self.bird.hitbox.top
            h_dist = pipe.hitbox.left - self.bird.hitbox.right
            return v_dist, h_dist

    def run(self):
        while True: # game loop
            self.game_running = self.detect_collision()
            # event management
            for event in pygame.event.get():
                # quitting
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_running:
                        self.bird.fall(0)
                        self.bird.fly()
                        self.wing_animation()
                    if event.key == pygame.K_SPACE and not self.game_running:  
                        self.score = 0
                        self.bird.restart()
                        self.world.clear_pipes()
                        self.game_running = True
                if event.type == self.SPAWN_PIPE and self.game_running:
                    self.world.generate_pipes(self.SCREEN_SIZE )
                    self.score += 1
                    print(self.score) 
            if self.game_running:
                self.bird.fall(self.world.GRAVITY) # the bird falls at each iteration
                self.base_x -= self.MOV_SPEED
                if self.base_x <= - self.SCREEN_SIZE[0]:
                    self.base_x = 0  
            else:
                self.draw_game_over()

            # redraw the self.screen
            self.screen.blit(pygame.image.load(self.world.BG_DAY), (0,0)) # bg -> this must be the first element
            self.draw_pipes() 
            self.draw_base()
            self.detect_collision()
            self.draw_score()
            self.draw_game_over()
            self.get_state()
            # TODO: fix the animation
            # my_group.draw(self.screen)
            self.screen.blit(pygame.image.load(self.bird_icon).convert_alpha(), self.bird.hitbox) # bird -> convert_alpha is need for transparent bg 
            pygame.display.update() 
            self.clock.tick(120)


if __name__ == "__main__":
    game = Game()
    game.run()