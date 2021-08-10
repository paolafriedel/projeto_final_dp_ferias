import pygame
from os import path
from config import IMG_DIR, BLACK, FPS, QUIT, INIT2, WIDTH, HEIGHT


def elem_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'elementos.jpg')).convert()
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
                state = INIT2
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(image, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state