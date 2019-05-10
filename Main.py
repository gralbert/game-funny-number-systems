from StartActivity import StartActivity
from GameActivity import GameActivity
from StaticObjects import *
from collections import defaultdict
from GameOver import GameOver


class Game:
    def __init__(self,
                 caption,
                 width,
                 height,
                 frame_rate):

        self.frame_rate = frame_rate
        self.game_over = False
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.font = pygame.font.Font(None, 40)

    def run(self):
        start = StartActivity(self.font, self.surface,
                              self.keydown_handlers, self.mouse_handlers)
        new_game = GameActivity(self.font, self.surface,
                                self.keydown_handlers, self.mouse_handlers,
                                'NoName', 1)
        game_over = GameOver(self.font, self.surface,
                              self.keydown_handlers, self.mouse_handlers, '', 2)

        interval = 0
        while not self.game_over:
            if start.status:
                start.show()
            else:
                new_game.show()
                interval += 1
                if interval == 250:
                    new_game.new_cloud()
                    interval = 0
                new_game.upd_lives()
                if new_game.lives <= 0:
                    game_over.show()

            pygame.display.update()
            self.clock.tick(self.frame_rate)


def main():
    game = Game('Funny number systems', 680, 628, 50)
    game.run()


if __name__ == '__main__':
    main()
