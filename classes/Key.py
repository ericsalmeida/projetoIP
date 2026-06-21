# Categoria: key/sword.py
import pygame
import math
from constants import (TILE_SIZE, SWORD_BLADE, SWORD_GUARD, SWORD_EYE, SWORD_PUPIL, SWORD_HILT, SWORD_SKULL)
from classes.Coin import FloatingText, floating_texts  # Reaproveita o texto flutuante

class Sword(pygame.sprite.Sprite):
    """Classe exclusiva da Espada de Som do Jake"""
    def __init__(self, x, y):
        super().__init__()
        self.base_x = x
        self.base_y = y
        self.animation_time = x + y
        self.points = 50
        self.size = 24  
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_sound_sword()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_sound_sword(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, SWORD_BLADE, (4, 10, 10, 4))
        pygame.draw.rect(self.image, SWORD_BLADE, (4, 8, 2, 2))  
        pygame.draw.rect(self.image, SWORD_BLADE, (8, 8, 2, 2))  
        pygame.draw.rect(self.image, SWORD_BLADE, (12, 8, 2, 2)) 
        pygame.draw.rect(self.image, SWORD_GUARD, (14, 7, 4, 10))
        pygame.draw.rect(self.image, SWORD_EYE, (15, 10, 2, 4))
        pygame.draw.rect(self.image, SWORD_PUPIL, (15, 11, 2, 2))
        pygame.draw.rect(self.image, SWORD_HILT, (18, 11, 4, 2))
        pygame.draw.rect(self.image, SWORD_SKULL, (22, 10, 2, 4))

    def update(self):
        self.animation_time += 0.05
        offset_y = math.sin(self.animation_time) * 4
        self.rect.centery = self.base_y + int(offset_y)
        
        self.draw_sound_sword()
        if math.sin(self.animation_time * 2.5) > 0:
            pygame.draw.rect(self.image, (200, 240, 255), (0, 0, self.size, self.size), 1)


def generate_swords(matrix):
    """Gera o grupo contendo apenas as espadas nos 4 cantos do mapa"""
    keys_group = pygame.sprite.Group()

    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == 0:
                # Verifica se é uma das 4 posições dos cantos
                if (row_idx == 1 and col_idx == 1) or \
                   (row_idx == 1 and col_idx == 18) or \
                   (row_idx == 13 and col_idx == 1) or \
                   (row_idx == 13 and col_idx == 18):
                    x = col_idx * TILE_SIZE + TILE_SIZE // 2
                    y = row_idx * TILE_SIZE + TILE_SIZE // 2
                    sword = Sword(x, y)
                    keys_group.add(sword)

    return keys_group

def update_sword_collisions(pacman, keys_group):
    """Detecta colisão apenas com as espadas"""
    points_earned = 0
    power_activated = False

    hits = pygame.sprite.spritecollide(pacman, keys_group, True)
    for sword in hits:
        points_earned += sword.points
        power_activated = True
        new_text = FloatingText("+50", pacman.rect.centerx, pacman.rect.centery - 15, (255, 80, 255))
        floating_texts.add(new_text)

    return points_earned, power_activated