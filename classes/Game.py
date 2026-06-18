import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
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

            # Desenha a tela do jogo
            self.screen.fill(BLACK)

            self.mapa.draw(self.screen)  # Desenha o labirinto 
            self.pacip.desenhar(self.screen) # Desenha o PacIp dentro do labrinto

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

        sys.exit()