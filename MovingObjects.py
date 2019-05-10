import pygame
import random


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, -50))
        self.font = pygame.font.Font(None, 23)
        self.number = self.new_number()
        self.right_answer = self.answer(self.number)

    def update(self):
        self.rect.y += 1

    def draw(self, screen):

        text_surface = self.font.render(self.number,
                                        True,
                                        (0, 0, 0))
        screen.blit(self.image, (self.rect.x-43, self.rect.y-43))
        screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))

    @staticmethod
    def new_number():
        n = '1'
        for i in range(random.randint(5, 7)):
            n += str(random.randint(0, 1))
        return n

    def answer(self, num, to_base=10, from_base=2):
        # first convert to decimal number
        if isinstance(num, str):
            n = int(num, from_base)
        else:
            n = int(num)
        # now convert decimal to 'to_base' base
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < to_base:
            return alphabet[n]
        else:
            return self.answer(n // to_base, to_base) + alphabet[n % to_base]

    def handle_event(self, event):
        pass
