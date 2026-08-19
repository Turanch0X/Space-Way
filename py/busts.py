import pygame

class Bust:
    def __init__(self, screen, images, sounds, strike):
        self.screen = screen
        self.images = images
        self.sounds = sounds
        self.strike = strike

        self.bust_list = []
        self.bust_timer = pygame.USEREVENT + 5
        pygame.time.set_timer(self.bust_timer, 10000)

    def check_for_bust(self, health_idx, shield_idx, ship):
        for i, (bust, bust_rect) in enumerate(self.bust_list):

            self.screen.blit(bust, bust_rect)
            bust_rect.y += 8

            if bust_rect.y > 730:
                self.bust_list.pop(i)

            if ship.colliderect(bust_rect):

                if bust == self.images.busts[0]:
                    self.sounds.energy_up.play()
                    self.strike.ammo_left += 5

                if bust == self.images.busts[1]:
                    if health_idx >= 8:
                        pass
                    else:
                        self.sounds.heal_up.play()
                        health_idx += 1

                if bust == self.images.busts[2]:
                    if shield_idx >= 8:
                        pass
                    else:
                        self.sounds.shield_on.play()
                        shield_idx += 1
                        
                if bust == self.images.busts[3]:
                    self.sounds.energy_up.play()
                    self.strike.strike_active = True
                    self.strike.strike_timer = 0
                    
                self.bust_list.pop(i)

        return health_idx, shield_idx