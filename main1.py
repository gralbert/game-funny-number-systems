import pygame
import sys

from collections import defaultdict


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
                                'gg', 1)

        while not self.game_over:
            if start.status:
                start.show()
            else:
                new_game.show()
            pygame.display.update()
            self.clock.tick(self.frame_rate)


class StartActivity:
    def __init__(self, font, surface, keydown_handlers, mouse_handlers):
        self.__status = True
        self.surface = surface
        self.font = font
        self.keydown_handlers = keydown_handlers
        self.mouse_handlers = mouse_handlers
        self.background_image = \
            pygame.image.load('img/bg-1.jpg')
        self.objects = [InputBox(200, 250, 140, 32, self.font),
                        ButtonChoose(200, 350, 200, 32, self.font, '       EASY', False),
                        ButtonChoose(200, 400, 200, 32, self.font, '      MEDIUM', True),
                        ButtonChoose(200, 450, 200, 32, self.font, '       HARD', False),
                        ButtonStart(100, 530, 400, 32, self.font, '                   START', True),
                        TextObject(200, 200, lambda: 'Your name: ', (0, 0, 150), 'Impact', 30),
                        TextObject(200, 300, lambda: ' Difficult: ', (0, 0, 150), 'Impact', 30)]

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


class InputBox:

    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 0, 150)
        self.color_tx = (0, 60, 150)
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color_tx)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = (0, 0, 150)

    def __init__(self, x, y, w, h, font, text, status):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Button.COLOR_ACTIVE if status else Button.COLOR_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = status
        self.width = w

    def handle_event(self, event):
        pass

    def update(self):
        self.rect.w = self.width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class ButtonStart(Button):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print('tu')


class ButtonChoose(Button):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = Button.COLOR_ACTIVE if self.active \
                else Button.COLOR_INACTIVE
            self.txt_surface = self.font.render(self.text, True, self.color)


class TextObject:
    def __init__(self,
                 x,
                 y,
                 text_func,
                 color,
                 font_name,
                 font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = \
            self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text,
                                        True,
                                        self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

    def handle_event(self, event):
        pass


def main():
    game = Game('Funny number systems', 680, 628, 50)
    game.run()


if __name__ == '__main__':
    main()
