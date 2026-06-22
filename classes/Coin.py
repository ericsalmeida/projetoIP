# Categoria: classes/Coin.py
import pygame
from constants import TILE_SIZE, PAO, ALFACE, CARNE, QUEIJO

floating_texts = pygame.sprite.Group()


class FloatingText(pygame.sprite.Sprite):
    # Classe que cria o texto animado (+10) que sobe e some
    def __init__(self, text, x, y, color):
        super().__init__()

        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.y_float = float(y)
        self.alpha = 255
        self.speed = 0.8

    def update(self):
        self.y_float -= self.speed
        self.rect.centery = int(self.y_float)

        self.alpha -= 5
        if self.alpha <= 0:
            self.kill()
        else:
            alpha_image = self.image.copy()
            alpha_surface = pygame.Surface(alpha_image.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, self.alpha))
            alpha_image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = alpha_image


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_x = x
        self.base_y = y
        self.animation_time = x + y
        self.points = 10
        self.size = 16
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_mini_sandwich()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_mini_sandwich(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, PAO, (2, 2, 12, 3))
        pygame.draw.rect(self.image, ALFACE, (1, 5, 14, 2))
        pygame.draw.rect(self.image, QUEIJO, (2, 7, 12, 2))
        pygame.draw.rect(self.image, CARNE, (3, 9, 10, 2))
        pygame.draw.rect(self.image, PAO, (2, 11, 12, 3))

    def update(self):
        self.animation_time += 0.05

        if int(self.animation_time) % 4 == 0:
            self.image.set_alpha(170)
        else:
            self.image.set_alpha(255)


def generate_coins(matrix):
    coins_group = pygame.sprite.Group()
    reserved_positions = { #reserva as posições dos cantos para não colocar moedas lá, porque é onde as espadas ficam
        (1, 1),
        (1, 18),
        (13, 1),
        (13, 18),
    }

    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == 0 and (row_idx, col_idx) not in reserved_positions:
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2
                coins_group.add(Coin(x, y))

    return coins_group


def update_coin_collisions(pacman, coins_group):
    points_earned = 0

    hits = pygame.sprite.spritecollide(pacman, coins_group, True)

    for coin in hits:
        points_earned += coin.points
        new_text = FloatingText("+10", pacman.rect.centerx, pacman.rect.centery - 15, (50, 255, 50))
        floating_texts.add(new_text)

    return points_earned
