import pygame
from constants import TILE_SIZE, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from classes.Coin import Coin
from classes.Key import Key

class Map:
    def __init__(self):
        # Matriz de 15 linhas por 20 colunas
        # 1 = Parede, 0 = Caminho livre
        self.matrix = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
            [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
            [1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1],
            [1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
            [1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
        self.walls = []
        self.generate_walls()

        # Traz pro jogo a imagem do chão do mapa
        self.chao_image = pygame.image.load('assets/images/mapa_chão.png').convert()       
        # Garante a imagem no tamanho certo
        self.chao_image = pygame.transform.scale(self.chao_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Traz pro jogo a imagem das paredes do mapa
        self.parede_image = pygame.image.load('assets/images/mapa_parede.png').convert()       
        # Garante a imagem no tamanho certo
        self.parede_image = pygame.transform.scale(self.parede_image, (TILE_SIZE, TILE_SIZE))

    def generate_walls(self):
        for row_idx, row in enumerate(self.matrix):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    # Calcula a posição X e Y baseada na linha/coluna e tamanho do bloco
                    rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.walls.append(rect)

    def generate_items(self):
        coins_group = pygame.sprite.Group()
        keys_group = pygame.sprite.Group()

        # Coordenadas exatas dos 4 cantos para as espadas (Key)
        key_positions = {
            (1, 1),
            (1, 18),
            (13, 1),
            (13, 18)
        }

        # Contador manual para definir o ID de cada chave criada
        key_id_counter = 0

        for row_idx, row in enumerate(self.matrix):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    # Calcula o pixel central do bloco para o item não ficar torto
                    x = col_idx * TILE_SIZE + TILE_SIZE // 2
                    y = row_idx * TILE_SIZE + TILE_SIZE // 2

                    # Se a posição atual for um dos 4 cantos, gera uma chave
                    if (row_idx, col_idx) in key_positions:
                        keys_group.add(Key(x, y, key_id_counter))
                        key_id_counter += 1
                    else:
                        # Caso contrário, gera uma moeda (sanduíche) comum
                        coins_group.add(Coin(x, y))

        return coins_group, keys_group

    def draw(self, screen):
        # Desenho do chão na tela
        screen.blit(self.chao_image, (0, 0))
        
        # Desenho das paredes na tela
        for wall in self.walls:
            screen.blit(self.parede_image, (wall.x, wall.y))
