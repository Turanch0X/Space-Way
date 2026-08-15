import pygame, random

class Enemy:
    def __init__(self, screen, images, sounds):
        self.screen = screen
        self.images = images
        self.sounds = sounds

        self.timer_list = [1000, 2000, 3000]
        self.enemy_list = []
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, random.choice(self.timer_list))

    def check_for_enemies(self, health_idx, shield_idx, count, gaming, ship):
        for i in range(len(self.enemy_list) - 1, -1, -1):

            meteor_image, meteor_rect = self.enemy_list[i]
            self.screen.blit(meteor_image, meteor_rect)
            meteor_rect.y += 5

            if meteor_rect.y > 730:
                self.enemy_list.pop(i)

            if ship.colliderect(meteor_rect):
                self.sounds.boom.play()

                if shield_idx <= 0:

                    if meteor_image == self.images.meteors[0]:
                        health_idx += 1
                    if meteor_image == self.images.meteors[1]:
                        health_idx += 2
                    if meteor_image == self.images.meteors[2]:
                        health_idx += 3
                    if health_idx >= len(self.images.lives) - 1:
                        gaming = False

                else:
                    shield_idx -= 1

                self.enemy_list.pop(i)
                count += 1

        return health_idx, shield_idx, count, gaming