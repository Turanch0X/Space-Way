import pygame, random, json

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

timer_list = [1000, 2000, 3000]

shot = pygame.mixer.Sound('sounds\\shot.mp3')
boom = pygame.mixer.Sound('sounds\\boom.mp3')
energy_up = pygame.mixer.Sound('sounds\\energy_up.mp3')
heal_up = pygame.mixer.Sound('sounds\\health_up.wav')
shield_on = pygame.mixer.Sound('sounds\\shield_on.ogg')

pygame.mixer.music.load('music\\oblivion.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

logo = pygame.image.load('images\\logo.ico')
extra_logo = pygame.image.load('images\\round_logo.ico')

screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption('Space Way')
pygame.display.set_icon(logo)

sky = pygame.image.load('images\\sky.jpg').convert_alpha()
sky = pygame.transform.scale(sky, (400, 700)).convert_alpha()
sky_y = 0

label = pygame.font.Font('fonts\\title_font.ttf', 32)
rec_label = pygame.font.Font('fonts\\title_font.ttf', 12)
ammo_label = pygame.font.Font('fonts\\title_font.ttf', 18)

finish_label = label.render('Game over', False, (255, 255, 0))
restart_label = label.render('New game', False, (255, 255, 0))
restart_label_rect = restart_label.get_rect(topleft=(130, 350))

spaceship = pygame.image.load('images\\spaceship.png').convert_alpha()
space_step = 10
space_x = 160
space_y = 500

ammo = pygame.image.load('images\\ammo.png')
ammos = []
ammo_left = 10
strike_active = False
strike_timer = 0
strike_duration = 5 * 50

lives = [
    pygame.image.load('images\\lives\\8.png'),
    pygame.image.load('images\\lives\\7.png'),
    pygame.image.load('images\\lives\\6.png'),
    pygame.image.load('images\\lives\\5.png'),
    pygame.image.load('images\\lives\\4.png'),
    pygame.image.load('images\\lives\\3.png'),
    pygame.image.load('images\\lives\\2.png'),
    pygame.image.load('images\\lives\\1.png'),
    pygame.image.load('images\\lives\\0.png')
]
health_index = 0

shields = [
    pygame.image.load('images\\shields\\0.png'),
    pygame.image.load('images\\shields\\1.png'),
    pygame.image.load('images\\shields\\2.png'),
    pygame.image.load('images\\shields\\3.png'),
    pygame.image.load('images\\shields\\4.png'),
    pygame.image.load('images\\shields\\5.png'),
    pygame.image.load('images\\shields\\6.png'),
    pygame.image.load('images\\shields\\7.png'),
    pygame.image.load('images\\shields\\8.png')
]
shield_index = 0

busts = [
    pygame.image.load('images\\busts\\ammo+.png').convert_alpha(),
    pygame.image.load('images\\busts\\health+.png').convert_alpha(),
    pygame.image.load('images\\busts\\shield+.png').convert_alpha(),
    pygame.image.load('images\\busts\\strike.png').convert_alpha()
]

bust_list = []
bust_timer = pygame.USEREVENT + 5
pygame.time.set_timer(bust_timer, 10000)

meteors = [
    pygame.image.load('images\\meteorits\\S.png').convert_alpha(),
    pygame.image.load('images\\meteorits\\M.png').convert_alpha(),
    pygame.image.load('images\\meteorits\\L.png').convert_alpha()
]
met_step = 10
enemy_list = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.choice(timer_list))
max_meteor_width = max(meteor.get_width() for meteor in meteors)

running = True
gaming = True
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
        screen.blit(spaceship, (space_x, space_y))
        spaceship_rect = spaceship.get_rect(topleft=(space_x, space_y))

        screen.blit(lives[health_index], (300, 650))
        screen.blit(shields[shield_index], (300, 680))

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
                    boom.play()
                    if shield_index <= 0:
                        if meteor_image == meteors[0]:
                            health_index += 1
                        if meteor_image == meteors[1]:
                            health_index += 2
                        if meteor_image == meteors[2]:
                            health_index += 3
                        if health_index >= len(lives) - 1:
                            gaming = False
                    else:
                        shield_index -= 1
                    enemy_list.pop(i)
                    count += 1
        
        if ammos:
            for i, el_am in enumerate(ammos):
                screen.blit(ammo, el_am)
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
                                boom.play()
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
                    if bust == busts[0]:
                        energy_up.play()
                        ammo_left += 5
                    if bust == busts[1]:
                        if health_index == 0:
                            pass
                        else:
                            heal_up.play()
                            health_index -= 1
                    if bust == busts[2]:
                        if shield_index >= 8:
                            pass
                        else:
                            shield_on.play()
                            shield_index += 1
                    if bust == busts[3]:
                        energy_up.play()
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
            screen.blit(spaceship, (space_x, space_y))
            enemy_list.clear()
            ammos.clear()
            bust_list.clear()
            count = 0  # Reset the count for the new game
            ammo_left = 10
            health_index = 0
            shield_index = 0
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
                meteor_image = random.choice(meteors)
                max_x = 400 - meteor_image.get_width()
                meteor_rect = meteor_image.get_rect(topleft=(random.randint(5, max_x), -100))
                enemy_list.append((meteor_image, meteor_rect))
                pygame.time.set_timer(enemy_timer, random.choice(timer_list))
        
        if event.type == bust_timer:
            bust = random.choice(busts)
            bust_rect = bust.get_rect(topleft=(random.randint(5, 350), -100))
            bust_list.append((bust, bust_rect))

        if gaming and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if strike_active:
                ammos.append(ammo.get_rect(topleft=(space_x + 20, space_y)))
                shot.play()
                ammos.append(ammo.get_rect(topleft=(space_x + 60, space_y)))
                shot.play()

            if not strike_active and ammo_left > 0:
                ammos.append(ammo.get_rect(topleft=(space_x + 40, space_y)))
                shot.play()
                ammo_left -= 1
    
    clock.tick(50)