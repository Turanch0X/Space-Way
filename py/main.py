import pygame, random, json
from assets import Sounds, Image_Load

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()

timer_list = [1000, 2000, 3000]

images = Image_Load()
sounds = Sounds()

pygame.display.set_icon(images.logo)
pygame.display.set_caption('Space Way')

sky = pygame.transform.scale(images.sky, (400, 700)).convert_alpha()
sky_y = 0

label = pygame.font.Font('fonts\\title_font.ttf', 32)
rec_label = pygame.font.Font('fonts\\title_font.ttf', 12)
ammo_label = pygame.font.Font('fonts\\title_font.ttf', 18)

finish_label = label.render('Game over', False, (255, 255, 0))
restart_label = label.render('New game', False, (255, 255, 0))
restart_label_rect = restart_label.get_rect(topleft=(130, 350))

space_step = 10
space_x = 160
space_y = 500

ammos = []
ammo_left = 10
strike_active = False
strike_timer = 0
strike_duration = 5 * 50

health_idx, shield_idx = 0, 0

bust_list = []
bust_timer = pygame.USEREVENT + 5
pygame.time.set_timer(bust_timer, 10000)

enemy_list = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.choice(timer_list))

running, gaming = True, True
count = 0

with open('data.json', 'r') as file:
    data = json.load(file)
    record = data.get("Your record", 0)

while running:
    keys = pygame.key.get_pressed()
    
    screen.blit(sky, (0, sky_y))
    screen.blit(sky, (0, sky_y - 700))
    sky_y += 2
    if sky_y == 700:
        sky_y = 0

    if keys[pygame.K_w] and space_y > -5:
        space_y -= space_step
    if keys[pygame.K_s] and space_y < 620:
        space_y += space_step
    if keys[pygame.K_a] and space_x > -10:
        space_x -= space_step
    if keys[pygame.K_d] and space_x < 310:
        space_x += space_step
    
    if gaming:
        info = ammo_label.render(f'{ammo_left}', False, (205, 255, 80))
        screen.blit(info, (350, 600))
        screen.blit(images.spaceship, (space_x, space_y))
        spaceship_rect = images.spaceship.get_rect(topleft=(space_x, space_y))

        screen.blit(images.lives[health_idx], (300, 650))
        screen.blit(images.shields[shield_idx], (300, 680))

        if strike_active:
            strike_time_left = (strike_duration - strike_timer) / 50  # Convert frames to seconds
            strike_timer_label = ammo_label.render(f'{strike_time_left}', False, (205, 255, 80))
            screen.blit(strike_timer_label, (300, 600))

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
        
        if ammos:
            for i, el_am in enumerate(ammos):
                screen.blit(images.ammo, el_am)
                el_am.y -= 5

                if el_am.y < -10:
                    ammos.pop(i)
                
                if enemy_list:
                    for index, (meteor_image, meteor_rect) in enumerate(enemy_list):
                        if el_am.colliderect(meteor_rect):
                            try:
                                enemy_list.pop(index)
                                ammos.pop(i)
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
                        ammo_left += 5
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
                        strike_active = True
                        strike_timer = 0
                        
                    bust_list.pop(i)
        if strike_active:
            strike_timer += 1
            if strike_timer >= strike_duration:
                strike_active = False
    else:
        screen.blit(finish_label, (125, 250))
        screen.blit(restart_label, (130, 350))

        result_text = f'Result: {count}'
        result = label.render(result_text, False, (255, 255, 0))
        screen.blit(result, (135, 450))

        # Display record text
        record_text = f'Your record: {record}'
        record_display = rec_label.render(record_text, False, (255, 255, 0))
        screen.blit(record_display, (300, 650))

        if count > record:
            record = count  # Update record
            with open('data.json', 'w') as file:
                json.dump({'Your record': record}, file)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gaming = True
            space_x = 160
            space_y = 500
            screen.blit(images.spaceship, (space_x, space_y))
            enemy_list.clear()
            ammos.clear()
            bust_list.clear()
            count = 0  # Reset the count for the new game
            ammo_left = 10
            health_idx = 0
            shield_idx = 0
            strike_active = False
            strike_timer = 0
            strike_duration = 5 * 50

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
            if strike_active:
                ammos.append(images.ammo.get_rect(topleft=(space_x + 20, space_y)))
                sounds.shot.play()
                ammos.append(images.ammo.get_rect(topleft=(space_x + 60, space_y)))
                sounds.shot.play()

            if not strike_active and ammo_left > 0:
                ammos.append(images.ammo.get_rect(topleft=(space_x + 40, space_y)))
                sounds.shot.play()
                ammo_left -= 1
    
    clock.tick(50)