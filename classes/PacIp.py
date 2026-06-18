import pygame
from constants import YELLOW

class PacIp:
    def __init__(self, x, y, tamanho=32, velocidade=4):
        # Posição inicial do PacIp
        self.start_x = x
        self.start_y = y

        # Retângulo usado para colisões
        self.rect = pygame.Rect(x, y, tamanho, tamanho)

        # Atributo de movimento do personagem
        self.speed = velocidade

        # Atributo da direção atual
        self.direction = (0, 0)

        # Atributo da próxima direção desejada
        self.next_direction = (0, 0)

        self.lives = 3 # Qtd. de vidas do PacIp

        self.score = 0 # Pontuação do jogador

        self.keys_collected = [] # Armazenamento das chaves especiais que foram coletadas

        # Representação inicial do personagem: círculo amarelo no mapa
        self.color = YELLOW 

    #  Método que define a direção do PacIp
    def definir_direcao(self, key):

        if key == pygame.K_UP:
            self.direction = (0, -1)

        elif key == pygame.K_DOWN:
            self.direction = (0, 1)

        elif key == pygame.K_LEFT:
            self.direction = (-1, 0)

        elif key == pygame.K_RIGHT:
            self.direction = (1, 0)
    def mover(self, walls):
        # PacIp tenta mover no eixo X --> isso é, na direcao horizontal
        self.rect.x += self.direction[0] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                # Se colidiu, desfaz o passo no eixo X e faz o PacIp parar totalmente
                self.rect.x -= self.direction[0] * self.speed
                self.direction = (0, 0)
                break

        # PacIp tenta mover no eixo Y --> isso é, na direcao vevrtical
        self.rect.y += self.direction[1] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                # Se colidiu, desfaz o passo no eixo Y e faz o PacIp parar totalmente
                self.rect.y -= self.direction[1] * self.speed
                self.direction = (0, 0)
                break

    # Função que desenha o PacIp na tela
    def desenhar(self, tela):

        pygame.draw.circle(
            tela,
            self.color,
            self.rect.center,
            self.rect.width // 2
        )