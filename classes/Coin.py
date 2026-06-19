# Categoria: classes/Coin.py
import pygame
import math
from constants import (TILE_SIZE, PAO, ALFACE, CARNE, QUEIJO, TOMATE, MAIONESE, SWORD_BLADE, SWORD_GUARD, SWORD_EYE, SWORD_PUPIL, SWORD_HILT, SWORD_SKULL)

floating_texts = pygame.sprite.Group()

class FloatingText(pygame.sprite.Sprite):
    #Classe que cria o texto animado (+10 / +50) que sobe e some
    def __init__(self, text, x, y, color):
        super().__init__()
      
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.y_float = float(y)
        self.alpha = 255  # Opacidade inicial (totalmente visível)
        self.speed = 0.8  # Velocidade com que o texto sobe

    def update(self):
        # Faz o texto subir
        self.y_float -= self.speed
        self.rect.centery = int(self.y_float)
        
        # Diminui a opacidade (efeito fade out)
        self.alpha -= 5
        if self.alpha <= 0:
            self.kill()  # Remove o texto do jogo quando sumir por completo
        else:
            # Cria uma cópia da imagem para aplicar a nova transparência
            alpha_image = self.image.copy()
            alpha_surface = pygame.Surface(alpha_image.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, self.alpha))
            alpha_image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = alpha_image


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, is_power_pellet=False):
        super().__init__()
        self.is_power_pellet = is_power_pellet
        self.base_x = x
        self.base_y = y
        self.animation_time = x + y

        if self.is_power_pellet:
            self.points = 50
            self.size = 24  
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.draw_sound_sword()
        else:
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
        
        if self.is_power_pellet:
            offset_y = math.sin(self.animation_time) * 4
            self.rect.centery = self.base_y + int(offset_y)
            
            self.draw_sound_sword()
            if math.sin(self.animation_time * 2.5) > 0:
                pygame.draw.rect(self.image, (200, 240, 255), (0, 0, self.size, self.size), 1)
        else:
            if int(self.animation_time) % 4 == 0:
                self.image.set_alpha(170)
            else:
                self.image.set_alpha(255)


def generate_coins(matrix):
    coins_group = pygame.sprite.Group()

    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == 0:
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2

                if (row_idx == 1 and col_idx == 1) or \
                   (row_idx == 1 and col_idx == 18) or \
                   (row_idx == 13 and col_idx == 1) or \
                   (row_idx == 13 and col_idx == 18):
                    coin = Coin(x, y, is_power_pellet=True)
                else:
                    coin = Coin(x, y, is_power_pellet=False)
                
                coins_group.add(coin)

    return coins_group

def update_coin_collisions(pacman, coins_group):
    points_earned = 0
    power_activated = False

    hits = pygame.sprite.spritecollide(pacman, coins_group, True)
    
    for coin in hits:
        points_earned += coin.points
        if coin.is_power_pellet:
            power_activated = True
            # COR MUDADA: Roxo/Rosa Neon (+50)
            new_text = FloatingText("+50", pacman.rect.centerx, pacman.rect.centery - 15, (255, 80, 255))
            floating_texts.add(new_text)
        else:
            # COR MUDADA: Verde Limão/Alface (+10)
            new_text = FloatingText("+10", pacman.rect.centerx, pacman.rect.centery - 15, (50, 255, 50))
            floating_texts.add(new_text)

    return points_earned, power_activated