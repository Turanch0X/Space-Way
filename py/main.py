import pygame, random

from assets import Sounds, Image_Load, Fonts
from moves import Spaceship, Sky
from json_logic import JSON_Handler
from strike import Strike

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()

timer_list = [1000, 2000, 3000]
count = 0

images = Image_Load()
sounds = Sounds()
fonts = Fonts()

pygame.display.set_icon(images.logo)
pygame.display.set_caption('Space Way')

spaceship = Spaceship(160, 500, 10)
sky = Sky(screen, images, 0)
strike = Strike(screen, images, sounds, fonts, spaceship)
JSON = JSON_Handler(0)

health_idx, shield_idx = 0, 0

bust_list = []
bust_timer = pygame.USEREVENT + 5
pygame.time.set_timer(bust_timer, 10000)

enemy_list = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.choice(timer_list))

running, gaming = True, True
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

        if enemy_list:
            for i, (meteor_image, meteor_rect) in enumerate(enemy_list):
                screen.blit(meteor_image, meteor_rect)
                meteor_rect.y += 5
                if meteor_rect.y > 730:
                    enemy_list.pop(i)
                if spaceship_rect.colliderect(meteor_rect):
                    sounds.boom.play()
                    if shield_idx <= 0:
                        if meteor_image == images.meteors[0]:
                            health_idx += 1
                        if meteor_image == images.meteors[1]:
                            health_idx += 2
                        if meteor_image == images.meteors[2]:
                            health_idx += 3
                        if health_idx >= len(images.lives) - 1:
                            gaming = False
                    else:
                        shield_idx -= 1
                    enemy_list.pop(i)
                    count += 1
        
        if strike.ammos:
            for i, el_am in enumerate(strike.ammos):
                screen.blit(images.ammo, el_am)
                el_am.y -= 5

                if el_am.y < -10:
                    strike.ammos.pop(i)
                
                if enemy_list:
                    for index, (meteor_image, meteor_rect) in enumerate(enemy_list):
                        if el_am.colliderect(meteor_rect):
                            try:
                                enemy_list.pop(index)
                                strike.ammos.pop(i)
                                count += 1
                                sounds.boom.play()
                                break  # Avoiding list mutation issues during iteration
                            except IndexError:
                                print('Shit happened') #just for hint
                                pass
        if bust_list:
            for i, (bust, bust_rect) in enumerate(bust_list):
                screen.blit(bust, bust_rect)
                bust_rect.y += 8
                if bust_rect.y > 730:
                    bust_list.pop(i)
                if spaceship_rect.colliderect(bust_rect):
                    if bust == images.busts[0]:
                        sounds.energy_up.play()
                        strike.ammo_left += 5
                    if bust == images.busts[1]:
                        if health_idx == 0:
                            pass
                        else:
                            sounds.heal_up.play()
                            health_idx -= 1
                    if bust == images.busts[2]:
                        if shield_idx >= 8:
                            pass
                        else:
                            sounds.shield_on.play()
                            shield_idx += 1
                    if bust == images.busts[3]:
                        sounds.energy_up.play()
                        strike.strike_active = True
                        strike.strike_timer = 0
                        
                    bust_list.pop(i)
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
            enemy_list.clear()
            strike.ammos.clear()
            bust_list.clear()
            count = 0
            strike.ammo_left = 10
            health_idx = 0
            shield_idx = 0
            strike.strike_active = False
            strike.strike_timer = 0
            strike.strike_duration = 5 * 50

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == enemy_timer:
            for _ in range(3):  # Ensure at least 3 meteors are added each timer event
                meteor_image = random.choice(images.meteors)
                max_x = 400 - meteor_image.get_width()
                meteor_rect = meteor_image.get_rect(topleft=(random.randint(5, max_x), -100))
                enemy_list.append((meteor_image, meteor_rect))
                pygame.time.set_timer(enemy_timer, random.choice(timer_list))
        
        if event.type == bust_timer:
            bust = random.choice(images.busts)
            bust_rect = bust.get_rect(topleft=(random.randint(5, 350), -100))
            bust_list.append((bust, bust_rect))

        if gaming and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if strike.strike_active:
                strike.double_strike()
            if not strike.strike_active and strike.ammo_left > 0:
                strike.ordinary_strike()
    
    clock.tick(50)