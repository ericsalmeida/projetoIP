import pygame
import random
from constants import TILE_SIZE

class Ghost:
    def __init__(self, x, y, ghost_id, matrix, tamanho=32, velocidade=2, color=(255, 0, 0), raio_patrulha=4):
        # Cria o rect e centraliza ele no ponto (x, y) — que é o centro do
        # bloco do mapa. Antes o (x, y) virava o canto superior esquerdo,
        # fazendo o fantasma nascer meio bloco fora do lugar e preso na parede.
        self.rect = pygame.Rect(0, 0, tamanho, tamanho)
        self.rect.center = (x, y)

        self.matrix = matrix
        self.speed = velocidade  # mais devagar que o PacIp, pra dar chance de fuga
        self.color = color
        self.base_color = color  # cor original, quando ele NÃO está vulnerável

        self.ghost_id = ghost_id
        self.bonus_points = 0
        self.vulnerable = False
        self.eaten = False

        # Direções: Cima, Baixo, Esquerda, Direita
        self.directions_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.direction = random.choice(self.directions_list)
        self.state = 'patrulha'

        # Guarda em qual bloco (tile) o fantasma está agora. Usado pra
        # detectar quando ele realmente atravessa pra um bloco novo
        # (é isso que evita ele travar tremendo no lugar).
        self.tile_col = self.rect.centerx // TILE_SIZE
        self.tile_row = self.rect.centery // TILE_SIZE

        # Ponto de origem (o bloco onde ele nasceu). O fantasma tende a
        # rondar perto daqui em vez de vagar pelo mapa inteiro.
        self.home_col = self.tile_col
        self.home_row = self.tile_row
        self.raio_patrulha = raio_patrulha  # em blocos

        self.vulnerable_colors = [(30, 30, 255), (255, 255, 255)]

    # Coloca o fantasma no estado em que o fantasma pode ser comido pelo jogador
    def tornar_vulneravel(self, pontos):
        self.vulnerable = True
        self.bonus_points = pontos

    # Marca o fantasma como comido
    def ser_comido(self):
        self.eaten = True
        self.vulnerable = False

    # Descobre quais direções podem ser utilizadas a partir do bloco atual
    # Apenas posições com valor 0 (caminho livre) são consideradas
    def get_direcoes_validas(self, tile_row, tile_col):
        direcao_oposta = (-self.direction[0], -self.direction[1])
        validas = []

        for d in self.directions_list:
            nova_col = tile_col + d[0]
            nova_row = tile_row + d[1]

            dentro_do_mapa = 0 <= nova_row < len(self.matrix) and 0 <= nova_col < len(self.matrix[0])
            if dentro_do_mapa and self.matrix[nova_row][nova_col] == 0:
                # Evita voltar pelo mesmo caminho, a menos que seja a única opção (beco sem saída)
                if d != direcao_oposta:
                    validas.append(d)

        if not validas:
            # Beco sem saída: a única saída é voltar
            nova_col = tile_col + direcao_oposta[0]
            nova_row = tile_row + direcao_oposta[1]
            dentro_do_mapa = 0 <= nova_row < len(self.matrix) and 0 <= nova_col < len(self.matrix[0])
            if dentro_do_mapa and self.matrix[nova_row][nova_col] == 0:
                validas.append(direcao_oposta)

        return validas

    # Escolhe qual direção seguir
    # O algoritmo favorece movimentos que mantêm o fantasma próximo do ponto onde nasceu
    def escolher_direcao(self, opcoes, tile_row, tile_col):
        if len(opcoes) == 1:
            return opcoes[0]

        distancia_atual = abs(tile_col - self.home_col) + abs(tile_row - self.home_row)
        candidatos = opcoes

        if distancia_atual >= self.raio_patrulha:
            mais_perto = []
            for d in opcoes:
                nova_col = tile_col + d[0]
                nova_row = tile_row + d[1]
                nova_distancia = abs(nova_col - self.home_col) + abs(nova_row - self.home_row)
                if nova_distancia < distancia_atual:
                    mais_perto.append(d)
            # Só troca pra lista restrita se existir alguma opção que
            # realmente aproxime; senão (beco sem saída) mantém as normais.
            if mais_perto:
                candidatos = mais_perto

        # Sorteio ponderado: direções que aproximam mais do home pesam mais.
        pesos = []
        for d in candidatos:
            nova_col = tile_col + d[0]
            nova_row = tile_row + d[1]
            distancia = abs(nova_col - self.home_col) + abs(nova_row - self.home_row)
            peso = 1 / ((distancia + 1) ** 2)
            pesos.append(peso)

        return random.choices(candidatos, weights=pesos, k=1)[0]

    # Move o fantasma pelo mapa.
    # Sempre que entra em um novo tile ou colide com uma parede, decide uma nova direção.
    def mover(self, walls):
        if self.eaten:
            return

        colidiu = False

        # Move no eixo X e trava se bater em parede
        self.rect.x += self.direction[0] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= self.direction[0] * self.speed
                colidiu = True
                break

        # Move no eixo Y e trava se bater em parede
        self.rect.y += self.direction[1] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.y -= self.direction[1] * self.speed
                colidiu = True
                break

        novo_tile_col = self.rect.centerx // TILE_SIZE
        novo_tile_row = self.rect.centery // TILE_SIZE

        # Só decide nova direção quando bate numa parede OU quando de fato
        # entrou em um bloco diferente do que estava antes.
        entrou_bloco_novo = (novo_tile_col != self.tile_col) or (novo_tile_row != self.tile_row)

        if colidiu or entrou_bloco_novo:
            self.tile_col, self.tile_row = novo_tile_col, novo_tile_row
            centro_x = self.tile_col * TILE_SIZE + TILE_SIZE // 2
            centro_y = self.tile_row * TILE_SIZE + TILE_SIZE // 2
            self.rect.center = (centro_x, centro_y)
            opcoes = self.get_direcoes_validas(self.tile_row, self.tile_col)
            if opcoes:
                self.direction = self.escolher_direcao(opcoes, self.tile_row, self.tile_col)

    # Desenha o fantasma na tela
    def desenhar(self, screen):
        if self.eaten:
            return

        if self.vulnerable:
            piscando = (pygame.time.get_ticks() // 200) % 2
            cor_atual = self.vulnerable_colors[piscando]
        else:
            cor_atual = self.base_color

        pygame.draw.rect(screen, cor_atual, self.rect)