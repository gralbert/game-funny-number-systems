from StartActivity import StartActivity
import pygame
import sys
from MovingObjects import Cloud
from StaticObjects import InputBox, TextObject
import random


class GameActivity(StartActivity):
    def __init__(self, font, surface, keydown_handlers, mouse_handlers, name, speed):
        super().__init__(font, surface, keydown_handlers, mouse_handlers)
        self.name = name
        self.score = 0
        self.lives = 6
        self.speed = speed
        self.background_image = \
            pygame.image.load('img/bg-2.jpg')
        self.objects = [TextObject(300, 555, lambda: 'Lives: '+ str(self.lives),
                                   (0, 0, 150), 'Calibri', 28),
                        TextObject(450, 555, lambda: 'Score: ' + str(self.score),
                                   (0, 0, 150), 'Calibri', 28),
                        InputBox(50, 550, 140, 32, self.font,),
                        Cloud(200, 'img/cloud_1.png')]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
                if event.key == pygame.K_RETURN:
                    for o in self.objects:
                        try:
                            if self.objects[2].get_text() == o.right_answer:
                                self.objects.remove(o)
                                self.set_score()
                        except AttributeError:
                            pass
            elif event.type == pygame.KEYUP:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

            for o in self.objects:
                o.handle_event(event)

    def new_cloud(self):
        x = random.randrange(100, 600)
        self.objects.append(Cloud(x, 'img/cloud_1.png'))

    def set_score(self):
        self.score += 1

    def upd_lives(self):
        for o in self.objects:
            try:
                if o.rect.y > 660:
                    self.objects.remove(o)
                    self.lives -= 1
            except AttributeError:
                pass
