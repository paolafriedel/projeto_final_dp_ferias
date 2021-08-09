import pygame
from os import path
from assets import load_assets, SCORE_FONT
from config import IMG_DIR, BLACK, FPS, QUIT, YELLOW, WIDTH, INIT, HEIGHT, GAME


def end_screen(screen, score):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    assets = load_assets()
    # Carrega o fundo da tela final
    background = pygame.image.load(path.join(IMG_DIR, 'gameover.jpg')).convert()
    image = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = image.get_rect()

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    state = INIT
                    running = False
                else:
                    state = QUIT
                    running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(image, background_rect)

        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        screen.blit(text_surface, text_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state
