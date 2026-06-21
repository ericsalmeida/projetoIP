import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
from classes.Coin import generate_coins, update_coin_collisions, floating_texts
from classes.Key import generate_swords, update_sword_collisions
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK

class Game:
    def __init__(self):
        pygame.init()

        # COnfiguracao da musica do jogo
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.2) # Volume aqui vavi de 0 a 1. deixei em 0.2 para ficar agradável
        pygame.mixer.music.play(-1) # Funcao p manter a música em um loop infinito, repetindo a música quantas vezes forem preciso

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("PacIp")

        self.clock = pygame.time.Clock()

        self.running = True
        # Inicializa o mapa estruturado
        self.mapa = Map()

        # Cria do PacIp
        self.pacip = PacIp(x=364, y=324)

        # Gera as moedas no mapa
        self.coins = generate_coins(self.mapa.matrix)
        
        # Gera as espadas no mapa
        self.keys = generate_swords(self.mapa.matrix)

    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:

                    self.pacip.definir_direcao(
                        event.key
                    )

            # Atualiza o personagem na tela
            self.pacip.mover(self.mapa.walls)  # o parâmetro passado é a lista das paredes do mapa

            update_coin_collisions(self.pacip, self.coins) # Detecta colisão
            update_sword_collisions(self.pacip, self.keys) # ADICIONADO: Detecta colisão com a espada da pasta key
            
            self.coins.update()                            # Faz a espada flutuar e sanduíches piscarem
            self.keys.update()                             # Atualiza a animação da espada
            floating_texts.update()      

            # Desenha a tela do jogo
            self.screen.fill(BLACK)

            self.mapa.draw(self.screen)  # Desenha o labirinto 
            self.pacip.desenhar(self.screen) # Desenha o PacIp dentro do labrinto
            self.coins.draw(self.screen)  # Desenha as moedas
            self.keys.draw(self.screen)   # Desenha as espadas da pasta key
            
            floating_texts.draw(self.screen) 

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

        sys.exit()