from StartActivity import StartActivity
import pygame
import sys


class GameActivity(StartActivity):
    def __init__(self, font, surface, keydown_handlers, mouse_handlers, name, speed):
        super().__init__(font, surface, keydown_handlers, mouse_handlers)
        self.name = name
        self.speed = speed
        self.background_image = \
            pygame.image.load('img/bg-2.jpg')
        self.objects = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)
            for o in self.objects:
                o.handle_event(event)