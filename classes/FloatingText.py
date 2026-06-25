import pygame

# O grupo global
floating_texts = pygame.sprite.Group()

class FloatingText(pygame.sprite.Sprite):
    #Classe que cria o texto animado (+10) que sobe e some
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