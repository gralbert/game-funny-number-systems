from StaticObjects import *
import sys

class StartActivity:
    def __init__(self, font, surface, keydown_handlers, mouse_handlers):
        self.__status = True
        self.surface = surface
        self.font = font
        self.keydown_handlers = keydown_handlers
        self.mouse_handlers = mouse_handlers
        self.background_image = \
            pygame.image.load('img/bg-1.jpg')
        self.objects = [InputBox(220, 250, 140, 32, self.font),
                        ButtonChoose(220, 350, 200, 32, self.font, '       EASY', False),
                        ButtonChoose(220, 400, 200, 32, self.font, '      MEDIUM', True),
                        ButtonChoose(220, 450, 200, 32, self.font, '       HARD', False),
                        ButtonStart(130, 530, 400, 32, self.font, '                   START', True),
                        TextObject(220, 200, lambda: 'Your name: ', (0, 0, 150), 'Impact', 30),
                        TextObject(220, 300, lambda: 'Number systems: ', (0, 0, 150), 'Impact', 30)]

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

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
                if self.objects[4].rect.collidepoint(event.pos):
                    self.status = False
            for o in self.objects:
                o.handle_event(event)

    def show(self):
        self.surface.blit(self.background_image, (0, 0))
        self.handle_events()
        self.update()
        self.draw()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value