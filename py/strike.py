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