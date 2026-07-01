import pygame
import random
from constants import TILE_SIZE

class Ghost:
    # Adicionamos as três spritesheets como parâmetros obrigatórios e mudamos o tamanho para 40
    def __init__(self, x, y, ghost_id, matrix, spritesheet_main, spritesheet_cyan_right, spritesheet_scared, tamanho=40, velocidade=2, color=(255, 0, 0), raio_patrulha=4):
        
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

        self.tile_col = self.rect.centerx // TILE_SIZE
        self.tile_row = self.rect.centery // TILE_SIZE

        self.home_col = self.tile_col
        self.home_row = self.tile_row
        self.raio_patrulha = raio_patrulha  # em blocos

        
        def pegar_e_aumentar(sheet, pos_x, pos_y, largura, altura):
            # Recorta e força o tamanho para 40x40 (mesmo os assustados que são grandões)
            pedaco = sheet.recortar(pos_x, pos_y, largura, altura)
            return pygame.transform.scale(pedaco, (tamanho, tamanho))

        # FANTASMAS ASSUSTADOS (Pegando do spritesheet_scared)
        self.sprites_assustados = {
            (0, -1): pegar_e_aumentar(spritesheet_scared, 380, 373, 95, 99), # Cima
            (0, 1):  pegar_e_aumentar(spritesheet_scared, 177, 381, 94, 90), # Baixo
            (-1, 0): pegar_e_aumentar(spritesheet_scared, 274, 375, 93, 99), # Esquerda
            (1, 0):  pegar_e_aumentar(spritesheet_scared, 481, 373, 90, 98)  # Direita
        }

        # FANTASMAS NORMAIS (Mapeados pelo ghost_id)
        self.sprites_normais = {}
        
        # VERMELHO (Pode ser ID 1 ou 'red')
        if self.ghost_id == 1 or self.ghost_id == 'red':
            self.sprites_normais = {
                (0, -1): pegar_e_aumentar(spritesheet_main, 66, 128, 26, 28),
                (0, 1):  pegar_e_aumentar(spritesheet_main, 94, 128, 29, 28),
                (-1, 0): pegar_e_aumentar(spritesheet_main, 9, 161, 24, 26),
                (1, 0):  pegar_e_aumentar(spritesheet_main, 39, 162, 25, 25)
            }
        # LARANJA (Pode ser ID 2 ou 'orange')
        elif self.ghost_id == 2 or self.ghost_id == 'orange':
            self.sprites_normais = {
                (0, -1): pegar_e_aumentar(spritesheet_main, 195, 128, 23, 28),
                (0, 1):  pegar_e_aumentar(spritesheet_main, 223, 128, 23, 28),
                (-1, 0): pegar_e_aumentar(spritesheet_main, 138, 160, 25, 27),
                (1, 0):  pegar_e_aumentar(spritesheet_main, 167, 160, 28, 29)
            }
        # ROXO (Pode ser ID 3 ou 'purple')
        elif self.ghost_id == 3 or self.ghost_id == 'purple':
            self.sprites_normais = {
                (0, -1): pegar_e_aumentar(spritesheet_main, 65, 194, 27, 28),
                (0, 1):  pegar_e_aumentar(spritesheet_main, 94, 195, 25, 27),
                (-1, 0): pegar_e_aumentar(spritesheet_main, 8, 228, 23, 26),
                (1, 0):  pegar_e_aumentar(spritesheet_main, 37, 224, 26, 27)
            }
        # CIANO (Pode ser ID 4 ou 'cyan')
        elif self.ghost_id == 4 or self.ghost_id == 'cyan':
            self.sprites_normais = {
                (0, -1): pegar_e_aumentar(spritesheet_main, 193, 194, 28, 29),
                (0, 1):  pegar_e_aumentar(spritesheet_main, 221, 194, 28, 28),
                (-1, 0): pegar_e_aumentar(spritesheet_main, 136, 224, 26, 27),
                # Atenção: O Ciano pra Direita usa a spritesheet separada!
                (1, 0):  pegar_e_aumentar(spritesheet_cyan_right, 67, 224, 27, 26) 
            }
        else:
            # Prevenção de erro: Se vier um ID desconhecido, usa o Vermelho como padrão
            self.sprites_normais = {
                (0, -1): pegar_e_aumentar(spritesheet_main, 66, 128, 26, 28),
                (0, 1):  pegar_e_aumentar(spritesheet_main, 94, 128, 29, 28),
                (-1, 0): pegar_e_aumentar(spritesheet_main, 9, 161, 24, 26),
                (1, 0):  pegar_e_aumentar(spritesheet_main, 39, 162, 25, 25)
            }

        # Define a imagem inicial
        self.image = self.sprites_normais[self.direction]

    # Coloca o fantasma no estado em que pode ser comido
    def tornar_vulneravel(self, pontos):
        self.vulnerable = True
        self.bonus_points = pontos

    # Marca o fantasma como comido
    def ser_comido(self):
        self.eaten = True
        self.vulnerable = False

    def get_direcoes_validas(self, tile_row, tile_col):
        direcao_oposta = (-self.direction[0], -self.direction[1])
        validas = []

        for d in self.directions_list:
            nova_col = tile_col + d[0]
            nova_row = tile_row + d[1]

            dentro_do_mapa = 0 <= nova_row < len(self.matrix) and 0 <= nova_col < len(self.matrix[0])
            if dentro_do_mapa and self.matrix[nova_row][nova_col] == 0:
                if d != direcao_oposta:
                    validas.append(d)

        if not validas:
            nova_col = tile_col + direcao_oposta[0]
            nova_row = tile_row + direcao_oposta[1]
            dentro_do_mapa = 0 <= nova_row < len(self.matrix) and 0 <= nova_col < len(self.matrix[0])
            if dentro_do_mapa and self.matrix[nova_row][nova_col] == 0:
                validas.append(direcao_oposta)

        return validas

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
            if mais_perto:
                candidatos = mais_perto

        pesos = []
        for d in candidatos:
            nova_col = tile_col + d[0]
            nova_row = tile_row + d[1]
            distancia = abs(nova_col - self.home_col) + abs(nova_row - self.home_row)
            peso = 1 / ((distancia + 1) ** 2)
            pesos.append(peso)

        return random.choices(candidatos, weights=pesos, k=1)[0]

    def mover(self, walls):
        if self.eaten:
            return

        colidiu = False

        self.rect.x += self.direction[0] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= self.direction[0] * self.speed
                colidiu = True
                break

        self.rect.y += self.direction[1] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.y -= self.direction[1] * self.speed
                colidiu = True
                break

        novo_tile_col = self.rect.centerx // TILE_SIZE
        novo_tile_row = self.rect.centery // TILE_SIZE

        entrou_bloco_novo = (novo_tile_col != self.tile_col) or (novo_tile_row != self.tile_row)

        if colidiu or entrou_bloco_novo:
            self.tile_col, self.tile_row = novo_tile_col, novo_tile_row
            centro_x = self.tile_col * TILE_SIZE + TILE_SIZE // 2
            centro_y = self.tile_row * TILE_SIZE + TILE_SIZE // 2
            self.rect.center = (centro_x, centro_y)
            opcoes = self.get_direcoes_validas(self.tile_row, self.tile_col)
            if opcoes:
                self.direction = self.escolher_direcao(opcoes, self.tile_row, self.tile_col)

        # Atualiza a imagem com base na direção atual e se está assustado
        if self.vulnerable:
            # Adiciona o efeito piscando (some e aparece) pouco antes de acabar
            piscando = (pygame.time.get_ticks() // 200) % 2
            if piscando == 0:
                self.image = self.sprites_assustados[self.direction]
            else:
                # Quando pisca, mostra a cor base original só pra dar um aviso
                self.image = self.sprites_normais[self.direction] 
        else:
            self.image = self.sprites_normais[self.direction]

    # Desenha o fantasma na tela
    def desenhar(self, screen):
        if self.eaten:
            return

        # Desenha a imagem (o sprite) em vez do quadrado colorido!
        screen.blit(self.image, self.rect)