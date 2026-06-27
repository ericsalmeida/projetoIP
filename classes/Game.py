import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
from classes.Ghost import Ghost
from classes.FloatingText import floating_texts
from classes.Key import Key 
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE

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
        self.ghost_teste = Ghost(x=364, y=160)

        # a partir do método interno dele.
        self.coins, self.keys = self.mapa.generate_items()

        # Guarda futuramente os ids dos fantasmas ligados a cada espada.
        self.pending_ghost_ids = []

        # Envia a qtd total de hamburguer no mapa para a classe do pacio
        self.pacip.total_coins = len(self.coins)  

        # Define a fonte do HUD
        self.font = pygame.font.SysFont("arial", 20, bold=True) 

    # Função que coloca a qtd de pontos e de vidas na tela
    def draw_hud(self):
        score_surf = self.font.render(f"Pontos: {self.pacip.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))

        for i in range(self.pacip.lives):
            pygame.draw.circle(self.screen, (255, 80, 80), (SCREEN_WIDTH - 20 - i * 28, 20), 10)

    def run(self):
        tempo_ultimo_dano = 0
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

        ##############################################
            tempo_atual = pygame.time.get_ticks()
        
            if self.pacip.rect.colliderect(self.ghost_teste.rect):
            # Só tira vida se já tiverem passado 2000 milissegundos (2 segundos) desde o último hit
                if tempo_atual - tempo_ultimo_dano > 2000:
                    self.pacip.lives -= 1
                    tempo_ultimo_dano = tempo_atual # Reseta o cronômetro do dano
                    
                    # Condição de Game Over
                    if self.pacip.lives <= 0:
                        self.running = False


            #########################################

            # Verifica se o PacIp encostou em alguma moeda.
            coin_hits = pygame.sprite.spritecollide(self.pacip, self.coins, True)
            for coin in coin_hits:
                #Dispara os pontos e o texto flutuante da moeda coletada
                coin.on_collide(self.pacip) 
                self.pacip.score += coin.points
                # Soma 1 na qtd de hamburguer comido
                self.pacip.coins_eaten += 1
            
            # Verifica se o PacIp precisa ou não receber uma ivda extra. Podia ser no loop, mas aqui fica melhor p economiazr tempo no laço for
            self.pacip.verificar_vida_extra()  


            # Verifica se o PacIp encostou em alguma espada.
            key_hits = pygame.sprite.spritecollide(self.pacip, self.keys, True)
            for key in key_hits:
                # Dispara os pontos e o texto flutuante da espada coletada
                key.on_collect(self.pacip)
                
                self.pacip.score += key.points
                self.pacip.keys_collected.append(key.key_id)
                if key.linked_ghost_id is not None:
                    self.pending_ghost_ids.append(key.linked_ghost_id)

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

            # Chamada da função do hub
            self.draw_hud() 

            # Mostra o que foi desenhado na tela.
            pygame.display.flip()

            # Mantem o jogo na velocidade definida em FPS.
            self.clock.tick(FPS)

        # Fecha o pygame e encerra o programa.
        pygame.quit()
        sys.exit()