import pygame
import sys
from classes.PacIp import PacIp
from classes.Map import Map
from classes.FloatingText import floating_texts
from classes.Key import Key
from classes.Life import Life
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE

class Game:
    # Inicializa todo o jogo
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PacIp")

        self.clock = pygame.time.Clock()
        self.running = True

        self.mapa = Map()
        self.pacip = PacIp(x=364, y=324)

        # Agora o mapa devolve moedas, espadas E os 4 fantasmas
        self.coins, self.keys, self.ghosts = self.mapa.generate_items()

        # Grupo das vidas que os fantasmas derrubam no chão
        self.lives_drop = pygame.sprite.Group()

        self.pacip.total_coins = len(self.coins)

        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 36, bold=True)

        # Estado de fim de jogo
        self.game_over = False
        self.won = False

        # Estado geral do jogo: começa no menu, so depois vira "jogo"
        self.estado = "menu"
        self.menu_opcoes = ["Começar Jogo", "Sair"]
        self.menu_selecionado = 0

    # Desenha a interface do jogo, exibindo a pontuação e as vidas restantes
    def draw_hud(self):
        score_surf = self.font.render(f"Pontos: {self.pacip.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))

        for i in range(self.pacip.lives):
            pygame.draw.circle(self.screen, (255, 80, 80), (SCREEN_WIDTH - 20 - i * 28, 20), 10)

    # Desenha a tela de vitória ou derrota 
    def draw_end_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        if self.won:
            texto = "VOCE VENCEU!"
            cor = (80, 255, 80)
        else:
            texto = "GAME OVER"
            cor = (255, 80, 80)

        texto_surf = self.big_font.render(texto, True, cor)
        rect = texto_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(texto_surf, rect)

        score_surf = self.font.render(f"Pontuacao final: {self.pacip.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(score_surf, score_rect)

    # Desenha o menu principal do jogo
    def draw_menu(self):
        # Desenha o mapa de verdade (chão + paredes) no fundo do menu
        self.mapa.draw(self.screen)

        # Escurece por cima do mapa pra dar destaque ao texto do menu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        titulo_surf = self.big_font.render("PacIp", True, (255, 255, 0))
        titulo_rect = titulo_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(titulo_surf, titulo_rect)

        for i, opcao in enumerate(self.menu_opcoes):
            selecionado = (i == self.menu_selecionado)
            cor = (255, 255, 0) if selecionado else WHITE
            texto = f"> {opcao} <" if selecionado else opcao

            opcao_surf = self.menu_font.render(texto, True, cor)
            opcao_rect = opcao_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(opcao_surf, opcao_rect)

        dica_surf = self.font.render("Use as setas para navegar e ENTER para confirmar", True, (180, 180, 180))
        dica_rect = dica_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(dica_surf, dica_rect)

    # Processa o tratamento da navegação do menu
    def processar_menu(self, event):
        if event.key in (pygame.K_UP, pygame.K_w):
            self.menu_selecionado = (self.menu_selecionado - 1) % len(self.menu_opcoes)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.menu_selecionado = (self.menu_selecionado + 1) % len(self.menu_opcoes)
        elif event.key == pygame.K_RETURN:
            opcao_escolhida = self.menu_opcoes[self.menu_selecionado]
            if opcao_escolhida == "Começar Jogo":
                self.estado = "jogo"
            elif opcao_escolhida == "Sair":
                self.running = False

    # Coloca o PacIp pra posicao inicial depois de ser pego por um fantasma
    def resetar_pacip(self):
        self.pacip.rect.x = self.pacip.start_x
        self.pacip.rect.y = self.pacip.start_y
        self.pacip.direction = (0, 0)

    # Vence o jogo ao coletar tudo do mapa e comer todos os fantasmas
    def verificar_vitoria(self):
        todos_fantasmas_mortos = all(g.eaten for g in self.ghosts)
        if len(self.coins) == 0 and len(self.keys) == 0 and todos_fantasmas_mortos:
            self.won = True

    # Loop principal do jogo
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.estado == "menu":
                        self.processar_menu(event)
                    elif not (self.game_over or self.won):
                        self.pacip.definir_direcao(event.key)

            # Enquanto está no menu, só desenha o menu e pula toda a lógica do jogo
            if self.estado == "menu":
                self.draw_menu()
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            # Só roda a lógica do jogo se ele ainda não acabou
            if not (self.game_over or self.won):

                self.pacip.mover(self.mapa.walls)

                for ghost in self.ghosts:
                    ghost.mover(self.mapa.walls)

                # PacIp x moedas
                coin_hits = pygame.sprite.spritecollide(self.pacip, self.coins, True)
                for coin in coin_hits:
                    coin.on_collide(self.pacip)
                    self.pacip.score += coin.points
                    self.pacip.coins_eaten += 1

                self.pacip.verificar_vida_extra()

                # PacIp x espadas -> libera o fantasma ligado, ainda sem pontos
                key_hits = pygame.sprite.spritecollide(self.pacip, self.keys, True)
                for key in key_hits:
                    key.on_collect(self.pacip)
                    self.pacip.keys_collected.append(key.key_id)

                    if key.linked_ghost_id is not None:
                        for ghost in self.ghosts:
                            if ghost.ghost_id == key.linked_ghost_id:
                                ghost.tornar_vulneravel(key.points)
                                break

                # PacIp x fantasmas
                for ghost in self.ghosts:
                    if ghost.eaten:
                        continue
                    if self.pacip.rect.colliderect(ghost.rect):
                        if ghost.vulnerable:
                            # Come o fantasma: pontos da espada entram agora
                            self.pacip.score += ghost.bonus_points
                            drop_x = ghost.rect.centerx + ghost.direction[0] * 40
                            drop_y = ghost.rect.centery + ghost.direction[1] * 40
                            self.lives_drop.add(Life(drop_x, drop_y))
                            ghost.ser_comido()
                        else:
                            # Fantasma pega o PacIp: perde 1 vida
                            self.pacip.lives -= 1
                            self.resetar_pacip()
                            if self.pacip.lives <= 0:
                                self.game_over = True

                # PacIp x vida dropada no chão
                life_hits = pygame.sprite.spritecollide(self.pacip, self.lives_drop, True)
                for _ in life_hits:
                    self.pacip.lives += 1

                self.coins.update()
                self.keys.update()
                self.lives_drop.update()
                floating_texts.update()

                self.verificar_vitoria()

            # Desenho
            self.screen.fill(BLACK)

            self.mapa.draw(self.screen)
            self.pacip.desenhar(self.screen)

            for ghost in self.ghosts:
                ghost.desenhar(self.screen)

            self.coins.draw(self.screen)
            self.keys.draw(self.screen)
            for life in self.lives_drop:
                life.desenhar(self.screen)
            floating_texts.draw(self.screen)

            self.draw_hud()

            if self.game_over or self.won:
                self.draw_end_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()