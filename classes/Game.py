import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
from classes.Ghost import Ghost
from classes.Coin import generate_coins, update_coin_collisions, floating_texts
from classes.Key import create_keys, update_key_collisions
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK


# Classe principal que controla o jogo inteiro
class Game:
    def __init__(self):
        # Liga o pygame
        pygame.init()

        # Prepara a musica do jogo
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # Cria a janela do jogo.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PacIp")

        # Controle de tempo para o jogo rodar numa velocidade constante
        self.clock = pygame.time.Clock()

        # Controle simples para manter ou encerrar o jogo.
        self.running = True

        # Cria o mapa, o PacIp e um fantasma de teste.
        self.mapa = Map()
        self.pacip = PacIp(x=364, y=324)
        self.ghost_teste = Ghost(x=364, y=100)

        # Cria todas as moedas normais do mapa.
        self.coins = generate_coins(self.mapa.matrix)

        # Cria as 4 espadas especiais do jogo
        self.keys = create_keys([
            (60, 60),
            (740, 60),
            (60, 540),
            (740, 540),
        ])

        # Guarda futuramente os ids dos fantasmas ligados a cada espada.
        self.pending_ghost_ids = []

    def run(self):
        # Loop principal do jogo.
        while self.running:
            # Le tudo que o jogador faz no teclado e na janela.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Quando aperta uma seta, o PacIp muda de direcao.
                    self.pacip.definir_direcao(event.key)

            # Move o PacIp seguindo a direcao escolhida.
            self.pacip.mover(self.mapa.walls)

            # Move o fantasma de teste pelo mapa.
            self.ghost_teste.mover(self.mapa.walls)

            # Verifica se o PacIp encostou em alguma moeda.
            points_earned = update_coin_collisions(self.pacip, self.coins)
            self.pacip.score += points_earned

            # Verifica se o PacIp encostou em alguma espada.
            key_points, collected_key_ids, linked_ghost_ids = update_key_collisions(self.pacip, self.keys)
            self.pacip.score += key_points

            # Guarda quais espadas ja foram coletadas.
            self.pacip.keys_collected.extend(collected_key_ids)

            # Guarda os ids dos fantasmas que depois vao ser ligados.
            self.pending_ghost_ids.extend(linked_ghost_ids)

            # Atualiza a animacao das moedas, das espadas e dos textos flutuantes.
            self.coins.update()
            self.keys.update()
            floating_texts.update()

            # Limpa a tela antes de desenhar tudo de novo.
            self.screen.fill(BLACK)

            # Desenha o mapa, o personagem e o fantasma.
            self.mapa.draw(self.screen)
            self.pacip.desenhar(self.screen)
            self.ghost_teste.desenhar(self.screen)

            # Desenha moedas, espadas e textos de pontos.
            self.coins.draw(self.screen)
            self.keys.draw(self.screen)
            floating_texts.draw(self.screen)

            # Mostra o que foi desenhado na tela.
            pygame.display.flip()

            # Mantem o jogo na velocidade definida em FPS.
            self.clock.tick(FPS)

        # Fecha o pygame e encerra o programa.
        pygame.quit()
        sys.exit()
