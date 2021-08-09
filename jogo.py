# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import WIDTH, HEIGHT, INIT, GAME, QUIT, END, INIT2
from init_screen import init_screen
from game_screen import game_screen
from end_screen import end_screen
from init2_screen import init2_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Navinha')

state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == INIT2:
        state = init2_screen(window)
    elif state == GAME:
        state, score = game_screen(window)
    elif state == END:
        state = end_screen(window, score)
        for event in pygame.event.get():
            if event.key == pygame.K_KP_ENTER:
                state == GAME
            else:
                state == QUIT
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados