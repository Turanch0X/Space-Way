import pygame

from assets import Sounds, Images, Fonts
from moves import Spaceship, Sky
from json_logic import JSON_Handler
from strike import Strike
from enemies import Enemy
from busts import Bust
from events import Events

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()

health_idx, shield_idx, count = 8, 0, 0
running, gaming = True, True

images = Images()
sounds = Sounds()
fonts = Fonts()

pygame.display.set_icon(images.logo)
pygame.display.set_caption('Space Way')

spaceship = Spaceship(160, 500, 10)
sky = Sky(screen, images, 0)
strike = Strike(screen, images, sounds, fonts, spaceship)
enemies = Enemy(screen, images, sounds)
busts = Bust(screen, images, sounds, strike)
events = Events(images)

JSON = JSON_Handler()
JSON.read_json()

while running:
    
    spaceship.move()
    sky.move()

    if gaming:
        info = fonts.ammo_label.render(f'{strike.ammo_left}', False, (205, 255, 80))
        screen.blit(info, (350, 600))
        screen.blit(images.spaceship, (spaceship.x, spaceship.y))
        spaceship_rect = images.spaceship.get_rect(topleft=(spaceship.x, spaceship.y))

        screen.blit(images.lives[health_idx], (300, 650))
        screen.blit(images.shields[shield_idx], (300, 680))

        if strike.strike_active:
            strike.ulta_timer()

        if enemies.enemy_list:
            health_idx, shield_idx, count, gaming = enemies.check_for_enemies(
                health_idx,
                shield_idx,
                count,
                gaming,
                spaceship_rect
            )
        
        if strike.ammos:
            count = strike.ammo_strike(count, enemies.enemy_list)
        
        if busts.bust_list:
            health_idx, shield_idx, = busts.check_for_bust(
                        health_idx,
                        shield_idx,
                        spaceship_rect,
                )
            
        strike.timer_tick()

    else:
        screen.blit(fonts.finish_label, (125, 250))
        screen.blit(fonts.restart_label, (130, 350))

        result_text = f'Result: {count}'
        result = fonts.label.render(result_text, False, (255, 255, 0))
        screen.blit(result, (135, 450))

        record_text = f'Your record: {JSON.record}'
        record_display = fonts.rec_label.render(record_text, False, (255, 255, 0))
        screen.blit(record_display, (300, 650))
        JSON.write_json(count=count)

        mouse = pygame.mouse.get_pos()
        if fonts.restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gaming = True
            spaceship.x = 160
            spaceship.y = 500
            screen.blit(images.spaceship, (spaceship.x, spaceship.y))
            enemies.enemy_list.clear()
            strike.ammos.clear()
            busts.bust_list.clear()
            count = 0
            strike.ammo_left = 10
            health_idx = 8
            shield_idx = 0
            strike.strike_active = False
            strike.strike_timer = 0
            strike.strike_duration = 5 * 50

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.quit(running)

        if event.type == enemies.enemy_timer:
            events.enemy_encounter(enemies)
        
        if event.type == busts.bust_timer:
            events.bust_catch(busts)

        if gaming and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            events.double_catch(strike)
    
    clock.tick(50)