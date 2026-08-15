import pygame, random

class Events:
    def __init__(self, img):
        self.images = img

    def quit(self, running):
        running = False
        pygame.quit()

    def enemy_encounter(self, enemy):        
        for _ in range(3):  # Ensure at least 3 meteors are added each timer event
            meteor_image = random.choice(self.images.meteors)
            max_x = 400 - meteor_image.get_width()
            meteor_rect = meteor_image.get_rect(topleft=(random.randint(5, max_x), -100))
            enemy.enemy_list.append((meteor_image, meteor_rect))
            pygame.time.set_timer(enemy.enemy_timer, random.choice(enemy.timer_list))

    def bust_catch(self, bustic):
        bust = random.choice(self.images.busts)
        bust_rect = bust.get_rect(topleft=(random.randint(5, 350), -100))
        bustic.bust_list.append((bust, bust_rect))

    def double_catch(self, strike):
        if strike.strike_active:
            strike.double_strike()
        if not strike.strike_active and strike.ammo_left > 0:
            strike.ordinary_strike()