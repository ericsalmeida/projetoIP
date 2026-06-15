import pygame
import sys
from classes.PacIp import PacIp

class Game:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("PacIp")

        self.clock = pygame.time.Clock()

        self.running = True

        # Cria do PacIp
        self.pacip = PacIp(
            x=self.width // 2,
            y=self.height // 2
        )

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
            self.pacip.mover()

            # Desenha a tela do jogo
            self.screen.fill((0, 0, 0))

            self.pacip.desenhar(
                self.screen
            )

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

        sys.exit()