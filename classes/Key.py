import pygame
from constants import SWORD_BLADE, SWORD_GUARD, SWORD_EYE, SWORD_PUPIL, SWORD_HILT, SWORD_SKULL
from classes.Coin import FloatingText, floating_texts


# Essa classe representa a espada especial do jogo.
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, key_id, linked_ghost_id=None, size=24):
        super().__init__()

        # Cada espada tem seu proprio id.
        self.key_id = key_id

        # Aqui fica o id do fantasma que vai ser ligado a essa espada depois.
        self.linked_ghost_id = linked_ghost_id

        # Quando virar True, a espada some do mapa.
        self.collected = False

        # Quantos pontos essa espada vale.
        self.points = 50

        # Area usada para desenhar a espada.
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        # Caixa usada para posicao e colisao.
        self.rect = self.image.get_rect(center=(x, y))

        # Desenha a espada logo na criacao.
        self.draw()

    def link_to_ghost(self, ghost_id):
        # Guarda qual fantasma vai ficar ligado a essa espada.
        self.linked_ghost_id = ghost_id

    def collect(self):
        # Marca a espada como coletada.
        self.collected = True

    def on_collect(self, pacman):
        # Quando o PacIp pega a espada, ela some e mostra +50.
        self.collect()
        floating_texts.add(
            FloatingText("+50", pacman.rect.centerx, pacman.rect.centery - 15, (255, 80, 255))
        )

    def draw(self):
        # Limpa a imagem antes de desenhar de novo.
        self.image.fill((0, 0, 0, 0))

        # Aqui a espada eh desenhada com formas simples.
        pygame.draw.rect(self.image, SWORD_BLADE, (4, 10, 10, 4))
        pygame.draw.rect(self.image, SWORD_BLADE, (4, 8, 2, 2))
        pygame.draw.rect(self.image, SWORD_BLADE, (8, 8, 2, 2))
        pygame.draw.rect(self.image, SWORD_BLADE, (12, 8, 2, 2))
        pygame.draw.rect(self.image, SWORD_GUARD, (14, 7, 4, 10))
        pygame.draw.rect(self.image, SWORD_EYE, (15, 10, 2, 4))
        pygame.draw.rect(self.image, SWORD_PUPIL, (15, 11, 2, 2))
        pygame.draw.rect(self.image, SWORD_HILT, (18, 11, 4, 2))
        pygame.draw.rect(self.image, SWORD_SKULL, (22, 10, 2, 4))

    def update(self):
        # A espada ainda nao tem animacao.
        pass

    def desenhar(self, tela):
        # So desenha se ela ainda nao foi coletada.
        if not self.collected:
            tela.blit(self.image, self.rect)


def create_keys(positions):
    # Cria todas as espadas do mapa.
    keys = pygame.sprite.Group()

    # Cada posicao vira uma espada com seu proprio id.
    for key_id, (x, y) in enumerate(positions):
        keys.add(Key(x, y, key_id))

    return keys


def update_key_collisions(pacman, keys_group):
    # Guarda os resultados da coleta.
    points_earned = 0
    collected_key_ids = []
    linked_ghost_ids = []

    # Se o PacIp encostar em alguma espada, ela sai do grupo.
    hits = pygame.sprite.spritecollide(pacman, keys_group, True)

    for key in hits:
        # Faz a espada sumir e mostra o texto de pontos.
        key.on_collect(pacman)

        # Soma os pontos da espada.
        points_earned += key.points

        # Registra qual espada foi pega.
        collected_key_ids.append(key.key_id)

        # Se essa espada ja estiver ligada a um fantasma, guardamos o id.
        if key.linked_ghost_id is not None:
            linked_ghost_ids.append(key.linked_ghost_id)

    # Devolve tudo para o Game usar depois.
    return points_earned, collected_key_ids, linked_ghost_ids
