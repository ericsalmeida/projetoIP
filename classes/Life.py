import pygame
from constants import RED

class Life(pygame.sprite.Sprite):
    # Vida extra que um fantasma derruba no chão ao ser comido.

    def __init__(self, x, y, size=20):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)