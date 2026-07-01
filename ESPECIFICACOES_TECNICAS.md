# Especificações Técnicas - Jogo PacIp "Hora de Aventura"

## 1. TAMANHO DA GRADE E RESOLUÇÃO

### Dimensões da Tela
- **Resolução**: 800 × 600 pixels
- **Cálculo**: 20 colunas × 15 linhas de tiles

### Tamanho dos Tiles (Blocos)
- **Tamanho do bloco**: 40 × 40 pixels
- **Constante**: `TILE_SIZE = 40` em `constants.py`

### Mapeamento de Coordenadas
```
Posição do bloco (col, row) → Coordenada em pixels:
- X = col * 40
- Y = row * 40
- Centro do bloco = (col * 40 + 20, row * 40 + 20)
```

**Exemplo**: Um sprite no bloco (5, 3) está na posição pixel (200, 120), com centro em (220, 140)

---

## 2. ESTRUTURA DOS SPRITES

### A. JOGADOR (PacIp)

#### Atributos
```python
self.rect = pygame.Rect(x, y, tamanho, tamanho)  # Tamanho padrão: 32×32 pixels
self.speed = 4  # velocidade padrão
self.direction = (dx, dy)  # Tupla: (0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)
self.next_direction = (dx, dy)  # Próxima direção desejada
```

#### Controle de Direção
```python
# Mapeamento de teclas
pygame.K_UP    → direction = (0, -1)   # Cima
pygame.K_DOWN  → direction = (0, 1)    # Baixo
pygame.K_LEFT  → direction = (-1, 0)   # Esquerda
pygame.K_RIGHT → direction = (1, 0)    # Direita
```

#### Movimento
- Movimento separado por eixos (X e Y)
- Colisão com paredes (`self.walls`) faz reverter movimento
- O movimento atual é `direction * speed` por frame

#### Renderização Atual
```python
# Desenho simples (círculo amarelo)
pygame.draw.circle(tela, self.color, self.rect.center, self.rect.width // 2)
# Será substituído por sprite animado
```

#### Especificação para Sprite
- **Dimensões sugeridas**: 32 × 32 pixels por frame
- **Animações necessárias**: 
  - Andar para cima (3-4 frames)
  - Andar para baixo (3-4 frames)
  - Andar para esquerda (3-4 frames)
  - Andar para direita (3-4 frames)
  - Idle/parado (1-2 frames)
- **Cor base**: Amarelo (#FFFF00)

---

### B. FANTASMAS (Ghost)

#### Atributos
```python
self.rect = pygame.Rect(0, 0, tamanho, tamanho)  # Tamanho padrão: 32×32 pixels
self.speed = 2  # Mais lento que o PacIp
self.color = color  # Cor do fantasma (cada um tem uma)
self.base_color = color  # Cor original
self.direction = (dx, dy)  # Mesmas tuplas que o PacIp
self.state = 'patrulha'  # Estado atual
self.vulnerable = False  # Pode ser comido?
self.vulnerable_colors = [(30, 30, 255), (255, 255, 255)]  # Cores piscando quando vulnerável
```

#### Cores dos 4 Fantasmas
```python
ghost_colors = [
    (255, 0, 0),        # Fantasma 0: Vermelho
    (255, 128, 0),      # Fantasma 1: Laranja
    (255, 0, 255),      # Fantasma 2: Magenta/Rosa
    (0, 200, 200)       # Fantasma 3: Ciano/Azul-turquesa
]
```

#### Movimento e IA
- Navega pela matriz do mapa (values 0 = caminho, 1 = parede)
- Detecta mudança de bloco via `tile_col` e `tile_row`
- Escolhe direção válida automaticamente
- Tenta ficar próximo ao seu ponto de origem (`home_col`, `home_row`)
- Raio de patrulha: 4 blocos (padrão)

#### Posições de Spawn
```python
ghost_positions = [
    (4, 4),      # Fantasma 0: linha 4, coluna 4
    (4, 15),     # Fantasma 1: linha 4, coluna 15
    (10, 4),     # Fantasma 2: linha 10, coluna 4
    (10, 15)     # Fantasma 3: linha 10, coluna 15
]
# Conversão: x = col * 40 + 20, y = row * 40 + 20
```

#### Especificação para Sprite
- **Dimensões**: 32 × 32 pixels por frame
- **Animações necessárias** (por fantasma):
  - Andar para cima (2-3 frames)
  - Andar para baixo (2-3 frames)
  - Andar para esquerda (2-3 frames)
  - Andar para direita (2-3 frames)
  - Vulnerável (piscando entre azul e branco, 2-3 frames)
  - Comido/Ghost (apenas cabeça/olhos, 1 frame)

---

## 3. ESTRUTURA DO LABIRINTO (MAPA)

### Matriz de Blocos
```python
self.matrix = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # Linha 0
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],  # Linha 1
    # ... (15 linhas no total)
]

# Dimensões: 15 linhas × 20 colunas
# Valor 0 = caminho livre (o personagem pode passar)
# Valor 1 = parede (bloqueio)
```

### Sistema de Paredes
```python
# Geração automática de paredes
def generate_walls(self):
    for row_idx, row in enumerate(self.matrix):
        for col_idx, cell in enumerate(row):
            if cell == 1:
                rect = pygame.Rect(
                    col_idx * TILE_SIZE,      # x
                    row_idx * TILE_SIZE,      # y
                    TILE_SIZE,                # width (40)
                    TILE_SIZE                 # height (40)
                )
                self.walls.append(rect)  # Lista de retângulos para colisão
```

### Posições de Itens Especiais
```python
# Espadas (4 unidades, uma em cada canto):
key_positions = [
    (1, 1),       # Canto superior-esquerdo
    (1, 18),      # Canto superior-direito
    (13, 1),      # Canto inferior-esquerdo
    (13, 18)      # Canto inferior-direito
]

# Todos os outros caminhos (0s) contêm moedas (sanduíches)
```

### Coleta de Dados do Mapa
```python
# O mapa percorre a matriz e cria:
# 1. walls[] → Lista de Rect para colisão
# 2. coins_group → Sprite.Group com Coin objects
# 3. keys_group → Sprite.Group com Key objects (espadas)
# 4. ghosts → Lista com 4 Ghost objects
```

---

## 4. INTEGRAÇÃO DE SPRITES (SUBSURFACE)

### Estrutura Recomendada de Folha de Sprites

#### Arquivo: `assets/images/pacip_spritesheet.png`
Sugestão de layout:
```
[IDLE] [UP 1] [UP 2] [UP 3]
[DOWN 1] [DOWN 2] [DOWN 3] [RIGHT 1]
[RIGHT 2] [RIGHT 3] [LEFT 1] [LEFT 2]
[LEFT 3] [MORTE 1] [MORTE 2] [VAZIO]

Tamanho total: 4 colunas × 4 linhas = 128 × 128 pixels (se cada frame for 32×32)
```

#### Arquivo: `assets/images/fantasma_spritesheet.png` (um arquivo por cor, OU um único com variações)
```
[UP 1] [UP 2] [DOWN 1] [DOWN 2]
[LEFT 1] [LEFT 2] [RIGHT 1] [RIGHT 2]
[VULN 1] [VULN 2] [COMIDO 1] [COMIDO 2]

Tamanho total: 4 colunas × 3 linhas = 128 × 96 pixels
```

### Implementação em Código

#### 1. **Carregar a folha de sprites** (em `PacIp.__init__()` ou `Game.__init__()`)
```python
class PacIp:
    def __init__(self, x, y, tamanho=32, velocidade=4):
        # ... código existente ...
        
        # NOVO: Carregar spritesheet
        self.spritesheet = pygame.image.load('assets/images/pacip_spritesheet.png').convert_alpha()
        self.frame_size = 32
        self.current_frame = 0
        self.animation_speed = 6  # Frames para trocar de sprite
        self.frame_counter = 0
        
        # Dicionário de frames por direção
        self.frames = {
            'idle': [self.get_frame(0, 0)],
            'up': [self.get_frame(0, 1), self.get_frame(0, 2), self.get_frame(0, 3)],
            'down': [self.get_frame(1, 0), self.get_frame(1, 1), self.get_frame(1, 2)],
            'right': [self.get_frame(1, 3), self.get_frame(2, 0), self.get_frame(2, 1)],
            'left': [self.get_frame(2, 2), self.get_frame(2, 3), self.get_frame(3, 0)]
        }
        self.current_animation = 'idle'
        self.current_image = self.frames['idle'][0]
```

#### 2. **Método para extrair frames com subsurface** (em `PacIp`)
```python
def get_frame(self, row, col):
    """
    Extrai um frame da spritesheet usando subsurface.
    
    Args:
        row: Linha do frame (0, 1, 2, 3, ...)
        col: Coluna do frame (0, 1, 2, 3, ...)
    
    Returns:
        pygame.Surface com o frame recortado
    """
    x = col * self.frame_size
    y = row * self.frame_size
    
    # subsurface cria uma view sem copiar a memória (mais eficiente)
    frame = self.spritesheet.subsurface(
        pygame.Rect(x, y, self.frame_size, self.frame_size)
    )
    return frame.copy()  # Faz uma cópia para evitar problemas de referência
```

#### 3. **Atualizar animação no método `mover()` ou novo método `update()`** (em `PacIp`)
```python
def update(self):
    """Atualiza a animação baseada na direção"""
    
    # Mapa de direção para chave de animação
    if self.direction == (0, 0):
        anim_key = 'idle'
    elif self.direction == (0, -1):
        anim_key = 'up'
    elif self.direction == (0, 1):
        anim_key = 'down'
    elif self.direction == (-1, 0):
        anim_key = 'left'
    elif self.direction == (1, 0):
        anim_key = 'right'
    
    # Troca animação se mudou a direção
    if anim_key != self.current_animation:
        self.current_animation = anim_key
        self.current_frame = 0
        self.frame_counter = 0
    
    # Incrementa contador de frames
    self.frame_counter += 1
    
    # Troca de sprite
    if self.frame_counter >= self.animation_speed:
        self.frame_counter = 0
        frames = self.frames[self.current_animation]
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.current_image = frames[self.current_frame]

def desenhar(self, tela):
    """Desenha o sprite animado em vez do círculo"""
    tela.blit(self.current_image, self.rect)
```

#### 4. **Para Fantasmas** (em `Ghost`)
```python
class Ghost:
    def __init__(self, x, y, ghost_id, matrix, tamanho=32, velocidade=2, color=(255, 0, 0), raio_patrulha=4):
        # ... código existente ...
        
        # NOVO: Carregar spritesheet
        self.spritesheet = pygame.image.load(f'assets/images/ghost_{ghost_id}_spritesheet.png').convert_alpha()
        # OU usar um único arquivo com variações de cor e aplicar colorkey/tinting
        
        self.frame_size = 32
        self.current_frame = 0
        self.animation_speed = 8
        self.frame_counter = 0
        
        self.frames = {
            'up': [self.get_ghost_frame(0, 0), self.get_ghost_frame(0, 1)],
            'down': [self.get_ghost_frame(0, 2), self.get_ghost_frame(0, 3)],
            'left': [self.get_ghost_frame(1, 0), self.get_ghost_frame(1, 1)],
            'right': [self.get_ghost_frame(1, 2), self.get_ghost_frame(1, 3)],
            'vulnerable': [self.get_ghost_frame(2, 0), self.get_ghost_frame(2, 1)],
            'eaten': [self.get_ghost_frame(2, 2)]
        }
        self.current_animation = 'down'
        self.current_image = self.frames['down'][0]
    
    def get_ghost_frame(self, row, col):
        x = col * self.frame_size
        y = row * self.frame_size
        frame = self.spritesheet.subsurface(
            pygame.Rect(x, y, self.frame_size, self.frame_size)
        )
        return frame.copy()
    
    def update(self):
        """Atualiza animação do fantasma"""
        
        if self.vulnerable:
            anim_key = 'vulnerable'
        elif self.eaten:
            anim_key = 'eaten'
        elif self.direction == (0, -1):
            anim_key = 'up'
        elif self.direction == (0, 1):
            anim_key = 'down'
        elif self.direction == (-1, 0):
            anim_key = 'left'
        elif self.direction == (1, 0):
            anim_key = 'right'
        else:
            anim_key = 'down'
        
        if anim_key != self.current_animation:
            self.current_animation = anim_key
            self.current_frame = 0
            self.frame_counter = 0
        
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            frames = self.frames[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.current_image = frames[self.current_frame]
```

#### 5. **Chamar `update()` no loop do jogo** (em `Game.run()`)
```python
def run(self):
    while self.running:
        # ... tratamento de eventos ...
        
        # Atualizar animações
        self.pacip.update()
        for ghost in self.ghosts:
            ghost.update()
        
        # ... resto da lógica do jogo ...
```

---

## 5. RESUMO: ONDE INTEGRAR A LÓGICA DE SPRITES

| Componente | Arquivo | Método | O que fazer |
|---|---|---|---|
| **Jogador** | `classes/PacIp.py` | `__init__()` | Carregar spritesheet, criar dicionário de frames |
| | | `get_frame()` | Novo método para extrair frames com subsurface |
| | | `update()` | Novo método para animar baseado na direção |
| | | `desenhar()` | Substituir círculo por `tela.blit(self.current_image, self.rect)` |
| **Fantasmas** | `classes/Ghost.py` | `__init__()` | Carregar spritesheet, criar frames |
| | | `get_ghost_frame()` | Novo método para extrair frames |
| | | `update()` | Novo método para animar baseado no estado (direção, vulnerable, eaten) |
| | | `desenhar()` | Adicionar método para desenhar sprite (chamar em Game.run) |
| **Jogo** | `classes/Game.py` | `run()` | Chamar `pacip.update()` e `ghost.update()` em cada frame |

---

## 6. CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Criar spritesheet do PacIp (32×32 por frame, múltiplas linhas/colunas)
- [ ] Criar spritesheets dos 4 fantasmas (32×32 por frame)
- [ ] Adicionar atributos de spritesheet em `PacIp.__init__()`
- [ ] Adicionar atributos de spritesheet em `Ghost.__init__()`
- [ ] Implementar `get_frame()` em `PacIp`
- [ ] Implementar `get_ghost_frame()` em `Ghost`
- [ ] Implementar `update()` em `PacIp`
- [ ] Implementar `update()` em `Ghost`
- [ ] Modificar `desenhar()` em `PacIp` para usar sprite
- [ ] Adicionar `desenhar()` em `Ghost` para usar sprite
- [ ] Chamar `update()` no loop principal (`Game.run()`)
- [ ] Testar animações e velocidade

---

## 7. DICAS IMPORTANTES

1. **subsurface() vs copy()**:
   - `subsurface()` é mais rápido (não copia dados)
   - Mas pode causar bugs se o spritesheet for modificado
   - Use `.copy()` para segurança

2. **Velocidade de Animação**:
   - `animation_speed = 6` significa trocar de frame a cada 6 frames do jogo
   - Com FPS=60, isso é ~10 mudanças por segundo
   - Ajuste conforme necessário

3. **Orientação dos Sprites**:
   - Certifique-se que os sprites estão olhando para a direção correta
   - Pode ser necessário usar `pygame.transform.flip()` se recortar errado

4. **Cores dos Fantasmas**:
   - Se usar um único arquivo para todos, considere adicionar uma camada de tint
   - Ou crie 4 spritesheets separados (recomendado)

5. **Memória**:
   - Carregue spritesheet uma única vez (em `__init__()`)
   - Use `convert_alpha()` para melhor performance
   - `subsurface()` sem `.copy()` poupa memória, mas `.copy()` é mais seguro
