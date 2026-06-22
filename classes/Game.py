import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
from classes.Ghost import Ghost
from classes.Coin import generate_coins, update_coin_collisions, floating_texts
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

        #Fantasma temporário pra testes

        self.ghost_teste = Ghost(x=364, y=100)

        # Gera as moedas no mapa
        self.coins = generate_coins(self.mapa.matrix)

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

            # Move o fantasma e verifica as colisões com as paredes do mapa
            self.ghost_teste.mover(self.mapa.walls)

            update_coin_collisions(self.pacip, self.coins) # Detecta colisão
            self.coins.update()                            # Faz a espada flutuar e sanduíches piscarem
            floating_texts.update()      

            # Desenha a tela do jogo
            self.screen.fill(BLACK)

            self.mapa.draw(self.screen)  # Desenha o labirinto 
            self.pacip.desenhar(self.screen) # Desenha o PacIp dentro do labrinto
            self.coins.draw(self.screen)  # Desenha as moedas

            # Renderiza o fantasma na tela
            self.ghost_teste.desenhar(self.screen)
            
            floating_texts.draw(self.screen) 

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

        sys.exit()