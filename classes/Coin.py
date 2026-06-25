import pygame
from constants import PAO, ALFACE, CARNE, QUEIJO, TOMATE, MAIONESE
from classes.FloatingText import FloatingText, floating_texts

class Coin(pygame.sprite.Sprite):
    #classe dos sanduichinhos comuns
    def __init__(self, x, y):
        super().__init__()
        self.base_x = x
        self.base_y = y
        self.points = 10
        self.size = 16  
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_mini_sandwich()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.is_fading = False
        self.alpha = 255
        self.fade_speed = 15

    def draw_mini_sandwich(self):
            self.image.fill((0, 0, 0, 0))

            pygame.draw.rect(self.image, PAO,      (2, 3, 12, 3))
            pygame.draw.rect(self.image, ALFACE,   (1, 6, 14, 1))
            pygame.draw.rect(self.image, TOMATE,   (3, 7, 10, 1))
            pygame.draw.rect(self.image, QUEIJO,   (1, 8, 14, 1))
            pygame.draw.rect(self.image, MAIONESE, (3, 9, 10, 1))
            pygame.draw.rect(self.image, CARNE,    (2, 10, 12, 3))
            pygame.draw.rect(self.image, PAO,      (2, 13, 12, 2))

    def on_collide(self, pacman):
        new_text = FloatingText("+10", pacman.rect.centerx, pacman.rect.centery - 15, (50, 255, 50))
        floating_texts.add(new_text)
        return self.points, False  # retorna (pontos, power_activated)  