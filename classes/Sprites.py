import pygame

class SpriteSheet:
    def __init__(self, caminho_arquivo):
        # convert_alpha() é crucial aqui para manter o fundo transparente
        self.sheet = pygame.image.load(caminho_arquivo).convert_alpha()

    def recortar(self, x, y, largura, altura):
        """Cria uma superfície vazia e 'cola' o pedaço da imagem nela"""
        frame = pygame.Surface((largura, altura), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), (x, y, largura, altura))
        return frame