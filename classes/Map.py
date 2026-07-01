import pygame
from constants import TILE_SIZE, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from classes.Coin import Coin
from classes.Key import Key
from classes.Ghost import Ghost

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

    # Criação das paredes no mapa
    def generate_walls(self):
        for row_idx, row in enumerate(self.matrix):
            for col_idx, cell in enumerate(row):
                if cell == 1:
                    # Calcula a posição X e Y baseada na linha/coluna e tamanho do bloco
                    rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.walls.append(rect)


    # Cria todos os objetos existentes no mapa, ou seja, as moedas, espadas e fantasmas
    def generate_items(self):
        coins_group = pygame.sprite.Group()
        keys_group = pygame.sprite.Group()
        ghosts = []

        # Lista pra garantir que a ordem case com o id do fantasma
        key_positions = [
            (1, 1),
            (1, 18),
            (13, 1),
            (13, 18)
        ]

        # Posições de spawn dos 4 fantasmas, uma pra cada espada (mesma ordem = mesmo id)
        ghost_positions = [
            (4, 4),
            (4, 15),
            (10, 4),
            (10, 15)
        ]
        ghost_colors = [(255, 0, 0), (255, 128, 0), (255, 0, 255), (0, 200, 200)]

        # 
        for ghost_id, (row, col) in enumerate(ghost_positions):
            x = col * TILE_SIZE + TILE_SIZE // 2
            y = row * TILE_SIZE + TILE_SIZE // 2
            ghosts.append(Ghost(x, y, ghost_id=ghost_id, matrix=self.matrix, color=ghost_colors[ghost_id]))

        key_id_counter = 0
        for row_idx, row in enumerate(self.matrix):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    x = col_idx * TILE_SIZE + TILE_SIZE // 2
                    y = row_idx * TILE_SIZE + TILE_SIZE // 2

                    if (row_idx, col_idx) in key_positions:
                        # o id da espada é igual ao id do fantasma que ela liberta
                        keys_group.add(Key(x, y, key_id_counter, linked_ghost_id=key_id_counter))
                        key_id_counter += 1
                    else:
                        coins_group.add(Coin(x, y))

        return coins_group, keys_group, ghosts

    # Desenho o mapa completo
    def draw(self, screen):
        screen.blit(self.chao_image, (0, 0))
        for wall in self.walls:
            screen.blit(self.parede_image, (wall.x, wall.y))