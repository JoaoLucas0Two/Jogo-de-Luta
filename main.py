import pygame
from pygame import mixer
from Fighter import Fighter

# Inicializar o Pygame e o Mixer
pygame.init()  # Inicializa o módulo principal do Pygame
mixer.init()  # Inicializa o módulo de áudio do Pygame

# Configurações gerais
SCREEN_WIDTH = 1000  # Largura da tela
SCREEN_HEIGHT = 600  # Altura da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a tela do jogo
pygame.display.set_caption("Fight Game")  # Define o título da janela do jogo

# Cores definidas em formato RGB
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)

# Estados do jogo
INICIO = 1  # Tela inicial
JOGANDO = 2  # Jogo em andamento
FIM = 3  # Tela de fim do jogo
estado_jogo = INICIO  # Estado inicial

# Definir fontes
fonte = pygame.font.Font("assets/fonts/turok.ttf", 50)  # Fonte padrão
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)  # Fonte para contagem regressiva
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)  # Fonte para exibir placares

# Função para desenhar texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    textoobj = fonte.render(texto, True, cor)  # Renderiza o texto
    texto_rect = textoobj.get_rect()  # Obtém o retângulo do texto
    texto_rect.center = (x, y)  # Centraliza o texto nas coordenadas fornecidas
    superficie.blit(textoobj, texto_rect)  # Desenha o texto na superfície

# Funções para desenhar as diferentes telas
def tela_inicio():
    screen.fill(WHITE)  # Preenche a tela com a cor branca
    desenhar_texto("Bem-vindo ao Fight Game!", fonte, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    desenhar_texto("Pressione Enter para iniciar", fonte, BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

def tela_fim():
    screen.fill(BLACK)  # Preenche a tela com a cor preta
    desenhar_texto("Fim de Jogo!", fonte, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    desenhar_texto("Pressione R para reiniciar", fonte, BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

# Função para desenhar o fundo do jogo
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Ajusta o tamanho da imagem de fundo
    screen.blit(scaled_bg, (0, 0))  # Desenha o fundo na tela

# Função para desenhar a barra de vida
def draw_health_bar(health, x, y):
    ratio = health / 100  # Calcula o tamanho proporcional da barra de vida
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))  # Contorno da barra
    pygame.draw.rect(screen, RED, (x, y, 400, 30))  # Fundo da barra (vermelho)
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))  # Porção preenchida da barra (amarelo)

# Variáveis e carregamento de assets do jogo de luta
FPS = 60  # Taxa de quadros por segundo
clock = pygame.time.Clock()  # Relógio para controlar FPS
intro_count = 3  # Contagem regressiva inicial
last_count_update = pygame.time.get_ticks()  # Tempo desde a última atualização da contagem
score = [0, 0]  # Pontuação dos jogadores [P1, P2]
round_over = False  # Indica se a rodada terminou
ROUND_OVER_COOLDOWN = 2000  # Tempo de espera após o término da rodada

# Carregar imagens
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Dados dos personagens
WARRIOR_DATA = [162, 4, [72, 56]]  # Dados do guerreiro (altura, escala, deslocamento)
WIZARD_DATA = [250, 3, [112, 107]]  # Dados do mago
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]  # Passos de animação do guerreiro
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]  # Passos de animação do mago

# Carregar sons
pygame.mixer.music.load("assets/audio/music.mp3")  # Música de fundo
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)  # Reproduz indefinidamente com atraso de 5 segundos
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")  # Som da espada
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")  # Som de magia
magic_fx.set_volume(0.75)

# Criar lutadores
fighter_1 = Fighter(1, 200, 330, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 330, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Loop principal do jogo
rodando = True
while rodando:
    clock.tick(FPS)  # Garante que o jogo rode na taxa de quadros definida

    # Capturar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fechar o jogo
            rodando = False
        elif evento.type == pygame.KEYDOWN:  # Pressionar tecla
            if estado_jogo == INICIO and evento.key == pygame.K_RETURN:
                estado_jogo = JOGANDO
                intro_count = 4
            elif estado_jogo == FIM and evento.key == pygame.K_r:
                estado_jogo = INICIO
                score = [0, 0]  # Reinicia a pontuação
                # Reinicia os lutadores
                fighter_1 = Fighter(1, 200, 330, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 330, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # Gerenciar telas e estados do jogo
    if estado_jogo == INICIO:
        tela_inicio()
    elif estado_jogo == JOGANDO:
        draw_bg()  # Desenha o fundo do jogo
        draw_health_bar(fighter_1.health, 20, 20)  # Barra de vida do jogador 1
        draw_health_bar(fighter_2.health, 580, 20)  # Barra de vida do jogador 2
        desenhar_texto("P1: " + str(score[0]), score_font, RED, screen, 50, 60)  # Placar jogador 1
        desenhar_texto("P2: " + str(score[1]), score_font, RED, screen, 610, 60)  # Placar jogador 2

        if intro_count <= 0:  # Após contagem regressiva, os lutadores se movem
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:  # Exibe contagem regressiva
            desenhar_texto(str(intro_count), count_font, RED, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # Atualiza e desenha lutadores
        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Verifica o estado dos lutadores
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))  # Exibe imagem de vitória
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 4  # Reinicia contagem regressiva
                # Reinicia lutadores
                fighter_1 = Fighter(1, 200, 330, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 330, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    elif estado_jogo == FIM:
        tela_fim()  # Exibe tela de fim de jogo

    pygame.display.flip()  # Atualiza a tela

pygame.quit()  # Encerra o jogo