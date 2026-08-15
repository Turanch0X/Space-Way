class Strike:
    def __init__(self, win, img, sou, fon, ship):
        self.screen = win
        self.images = img
        self.sounds = sou
        self.fonts = fon
        self.spaceship = ship

        self.strike_active = False
        self.strike_timer = 0
        self.strike_duration = 5 * 50

        self.ammos = []
        self.ammo_left = 10

    def ulta_timer(self): #cause 1
            strike_time_left = (self.strike_duration - self.strike_timer) / 50  # Convert frames to seconds
            strike_timer_label = self.fonts.ammo_label.render(f'{strike_time_left}', False, (205, 255, 80))
            self.screen.blit(strike_timer_label, (300, 600))

    def timer_tick(self): #cause 2
        if self.strike_active:
            self.strike_timer += 1
            if self.strike_timer >= self.strike_duration:
                self.strike_active = False

    def double_strike(self):
        self.ammos.append(self.images.ammo.get_rect(topleft=(self.spaceship.x + 20, self.spaceship.y)))
        self.sounds.shot.play()
        self.ammos.append(self.images.ammo.get_rect(topleft=(self.spaceship.x + 60, self.spaceship.y)))
        self.sounds.shot.play()

    def ordinary_strike(self):
        self.ammos.append(self.images.ammo.get_rect(topleft=(self.spaceship.x + 40, self.spaceship.y)))
        self.sounds.shot.play()
        self.ammo_left -= 1

    def ammo_strike(self, count, enemies):
        for i, el_am in enumerate(self.ammos):
            self.screen.blit(self.images.ammo, el_am)
            el_am.y -= 5

            if el_am.y < -10:
                self.ammos.pop(i)
            
            if enemies:
                for index, (meteor_image, meteor_rect) in enumerate(enemies):

                    if el_am.colliderect(meteor_rect):
                        try:
                            enemies.pop(index)
                            self.ammos.pop(i)
                            count += 1
                            self.sounds.boom.play()
                            break  # Avoiding list mutation issues during iteration
                        
                        except IndexError:
                            print('Shit happened') #just for hint
                            pass
        return count