import pygame
from pygame.constants import QUIT
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, END
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, SCORE_FONT
from sprites import Ship, Meteor, Explosion, Coracao, Bomb, Mais_bullets, Escudo    


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de meteoros
    all_sprites = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_bombs = pygame.sprite.Group()
    all_cora = pygame.sprite.Group()
    all_mais_bullets = pygame.sprite.Group()
    all_shields = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_meteors'] = all_meteors
    groups['all_bullets'] = all_bullets
    groups['all_cora'] = all_cora
    groups['all_bombs'] = all_bombs
    groups['all_mais_bullets'] = all_mais_bullets
    groups['all_shields'] = all_shields

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)
    # Criando os meteoros
    for i in range(6):
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3
    shield = 3

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
                return QUIT, score
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_UP:
                        player.speedy -= 8
                    if event.key == pygame.K_DOWN:
                        player.speedy += 8
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8
                        if event.key == pygame.K_UP:
                            player.speedy += 8
                        if event.key == pygame.K_DOWN:
                            player.speedy -= 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True, pygame.sprite.collide_mask)#aqui
            for meteor in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                m = Meteor(assets)
                all_sprites.add(m)
                all_meteors.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(meteor.rect.center, assets)
                all_sprites.add(explosao)

                # Ganhou pontos!
                score += 100
                if score % 1000 == 0:
                    lives += 1
                if score % 500 == 0:
                    met = 3
                    for i in range(met):
                        meteor = Meteor(assets)
                        all_sprites.add(meteor)
                        all_meteors.add(meteor)
                if score % 1200 == 0:
                    bo = 1
                    for i in range(bo):
                        bomb = Bomb(assets)
                        all_sprites.add(bomb)
                        all_bombs.add(bomb)
                if score % 800 == 0:
                    co = 1
                    for i in range(co):
                        coracao = Coracao(assets)
                        all_sprites.add(coracao)
                        all_cora.add(coracao)
                if score % 1100 == 0:
                    bala = 1
                    for i in range(bala):
                        bala = Mais_bullets(assets)
                        all_sprites.add(bala)
                        all_mais_bullets.add(bala)
                if score % 2000 == 0:
                    escudo = 1
                    for i in range(escudo):
                        escudo = Escudo(assets)
                        all_sprites.add(escudo)
                        all_shields.add(escudo)

            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                player.kill()
                lives -= 1
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

            hits_bombs = pygame.sprite.spritecollide(player, all_bombs, True, pygame.sprite.collide_mask)
            if len(hits_bombs) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                player.kill()
                shield -= 1
                if shield<=0:
                    lives-=2
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

            hits_balls = pygame.sprite.groupcollide(all_cora, all_bullets, True, True, pygame.sprite.collide_mask)
            if len(hits_balls) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                lives += 1
                for bola in hits_balls:
                    explosao = Explosion(bola.rect.center, assets)
                    all_sprites.add(explosao)
                
                # player.start_multi_shots()
            hits_mais_bullets = pygame.sprite.groupcollide(all_mais_bullets, all_bullets, True, True, pygame.sprite.collide_mask)
            if len(hits_mais_bullets) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                for bala in hits_mais_bullets:
                    player.start_multi_shots()   
                    explosao = Explosion(bala.rect.center, assets)
                    all_sprites.add(explosao)
            hits_escudos = pygame.sprite.groupcollide(all_shields, all_bullets, True, True, pygame.sprite.collide_mask)
            if len(hits_escudos) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                shield+=1
                for bala in hits_mais_bullets:
                    player.start_multi_shots()   
                    explosao = Explosion(bala.rect.center, assets)
                    all_sprites.add(explosao)
            

        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives <= 0:
                    state = DONE
                    return END, score
                else:
                    state = PLAYING
                    player = Ship(groups, assets)
                    all_sprites.add(player)

        # ----- Gera saídas
        window.fill(BLACK)  # Preenche com a cor branca
        window.blit(assets[BACKGROUND], (0, 0))
        # Desenhando meteoros
        all_sprites.draw(window)

        # Desenhando o score
        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)

        # Desenhando as vidas
        text_surface = assets[SCORE_FONT].render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        # Desenhando os escudos
        text_surface = assets[SCORE_FONT].render(chr(9829) * shield, True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (WIDTH, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador
