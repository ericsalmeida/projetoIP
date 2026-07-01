import pygame
from constants import YELLOW

class PacIp:
    # Adicionamos 'spritesheet' como um parâmetro obrigatório ao criar o jogador
    def __init__(self, x, y, spritesheet, tamanho=32, velocidade=4):
        # Posição inicial do PacIp
        self.start_x = x
        self.start_y = y

        # Retângulo usado para colisões
        self.rect = pygame.Rect(x, y, tamanho, tamanho)

        # Atributo de movimento do personagem
        self.speed = velocidade

        # Atributo da direção atual
        self.direction = (0, 0)

        # Atributo da próxima direção desejada
        self.next_direction = (0, 0)

        self.lives = 3 # Qtd. de vidas do PacIp

        self.score = 0 # Pontuação do jogador

        self.keys_collected = [] # Armazenamento das chaves especiais que foram coletadas

        # Mantido por compatibilidade
        self.color = YELLOW 

        # Atributos relacionados as moedas
        self.total_coins = 0        # total de moedas de moedas que tem no mapa (os hamburguer)
        self.half_life_given = False  # Registro se já deu a vida pela metade dos hamburguer coletados
        self.full_life_given = False  # Registro se já deu a vida por todos os hamburguer coletados
        self.coins_eaten = 0          # registro de quantas moedas já foram comidas pelo pacip

    
        self.spritesheet = spritesheet
        
        # Dicionário que usa as tuplas de direção do seu jogo como chaves.
        def pegar_e_aumentar(x, y, largura, altura):
            # Recorta exatamente no X, Y, Largura e Altura que você mediu!
            pedaco = self.spritesheet.recortar(x, y, largura, altura)
            # Estica para o tamanho da colisão (40x40) para não ficar pequeno na tela
            return pygame.transform.scale(pedaco, (tamanho, tamanho))
            
        self.animacoes = {
            # DIREITA: Fechada (68,38 a 95,63) | Aberta (97,37 a 124,62)
            (1, 0):  [pegar_e_aumentar(68, 38, 27, 25), pegar_e_aumentar(97, 37, 27, 25)],
            
            # ESQUERDA: Fechada (165,38 a 193,63) | Aberta (135,37 a 161,62)
            (-1, 0): [pegar_e_aumentar(165, 38, 28, 25), pegar_e_aumentar(135, 37, 26, 25)],
            
            # CIMA: Fechada (35,38 a 65,65) | Aberta (36,68 a 64,96)
            (0, -1): [pegar_e_aumentar(35, 38, 30, 27), pegar_e_aumentar(36, 68, 28, 28)],
            
            # BAIXO: Fechada (68,70 a 94,95) | Aberta (97,70 a 123,94)
            (0, 1):  [pegar_e_aumentar(68, 70, 26, 25), pegar_e_aumentar(97, 70, 26, 24)],
            
            # PARADO: Usa a animação "Direita Boca Fechada" repetida
            (0, 0):  [pegar_e_aumentar(68, 38, 27, 25), pegar_e_aumentar(68, 38, 27, 25)]
        }
        
        self.frame_index = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade_animacao = 150 # tempo em milissegundos para alternar a boca
        
        # Define a imagem inicial (boca fechada parado)
        self.image = self.animacoes[self.direction][self.frame_index]

    #  Método que define a direção do PacIp
    def definir_direcao(self, key):
        if key == pygame.K_UP:
            self.direction = (0, -1)
        elif key == pygame.K_DOWN:
            self.direction = (0, 1)
        elif key == pygame.K_LEFT:
            self.direction = (-1, 0)
        elif key == pygame.K_RIGHT:
            self.direction = (1, 0)

    def mover(self, walls):
        # PacIp tenta mover no eixo X isso é, na direcao horizontal
        self.rect.x += self.direction[0] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                # Se colidiu, desfaz o passo no eixo X e faz o PacIp parar totalmente
                self.rect.x -= self.direction[0] * self.speed
                self.direction = (0, 0)
                break

        # PacIp tenta mover no eixo Y --> isso é, na direcao vevrtical
        self.rect.y += self.direction[1] * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                # Se colidiu, desfaz o passo no eixo Y e faz o PacIp parar totalmente
                self.rect.y -= self.direction[1] * self.speed
                self.direction = (0, 0)
                break
                
        # Atualiza qual frame da boca deve ser renderizado baseado no movimento
        self.atualizar_animacao()

    # Método focado em controlar a velocidade da batida de boca
    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        
        # Se ele estiver se movendo, alternamos entre o frame 0 e 1
        if self.direction != (0, 0):
            if agora - self.ultimo_update > self.velocidade_animacao:
                self.ultimo_update = agora
                self.frame_index = (self.frame_index + 1) % 2
        else:
            # Se ele bateu na parede ou parou, fica de boca fechada
            self.frame_index = 0
            
        # Aplica a imagem correspondente à direção e ao frame atual
        if self.direction in self.animacoes:
            self.image = self.animacoes[self.direction][self.frame_index]

    # Função que desenha o PacIp na tela
    def desenhar(self, tela):
        # Substituído o desenho antigo do círculo pela textura recortada da SpriteSheet
        tela.blit(self.image, self.rect)

    # Função para vida extra
    def verificar_vida_extra(self):
        if self.total_coins == 0:
            return
        # Verifica se o pacip comeu mais das metades ou a metade das moedas e dá mais uma vida apenas uma vez por essa condicao
        if not self.half_life_given and self.coins_eaten >= self.total_coins // 2:
            self.lives += 1
            self.half_life_given = True
        # Verifica se o pacip comeu todas as moedas e dá mais uma vida apenas uma vez por essa condicao
        if not self.full_life_given and self.coins_eaten >= self.total_coins:
            self.lives += 1
            self.full_life_given = True