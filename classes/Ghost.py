import pygame
import random

class Ghost:
    def __init__(self, x, y, associated_key=None, tamanho=32, velocidade=3, color=(255, 0, 0)):
        """
        Inicializa o fantasma seguindo os padrões do PacIp.
        """
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.speed = velocidade
        self.color = color
        self.associated_key = associated_key
        
        # Direções: Cima, Baixo, Esquerda, Direita
        self.directions_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.direction = random.choice(self.directions_list)
        self.state = 'patrulha'

    def mudar_direcao_aleatoria(self):
        """Muda a direção evitando voltar pelo mesmo caminho imediatamente."""
        direcao_oposta = (-self.direction[0], -self.direction[1])
        opcoes_validas = [d for d in self.directions_list if d != direcao_oposta]
        
        if opcoes_validas:
            self.direction = random.choice(opcoes_validas)
        else:
            self.direction = random.choice(self.directions_list)

    def mover(self, walls):
        """
        Move nos eixos X e Y separadamente, checando colisões com as paredes (idêntico ao PacIp).
        """
        colidiu = False

        # Movimento e colisão no eixo X
        self.rect.x += self.direction[0] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= self.direction[0] * self.speed # Desfaz o movimento
                colidiu = True
                break

        # Movimento e colisão no eixo Y
        self.rect.y += self.direction[1] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.y -= self.direction[1] * self.speed # Desfaz o movimento
                colidiu = True
                break

        # Escolhe novo rumo ao bater na parede
        if colidiu:
            self.mudar_direcao_aleatoria()

    def desenhar(self, screen):
        """Desenha o fantasma na tela."""
        pygame.draw.rect(screen, self.color, self.rect)