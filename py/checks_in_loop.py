import pygame
from assets import Sounds, Image_Load

enemy_list = []
health_idx, shield_idx = 0, 0

class Enemy_Check():
    def __init__(self, scr, ship, game, count):
        sounds = Sounds()
        if enemy_list:
            for i, (meteor_image, meteor_rect) in enumerate(enemy_list):
                scr.blit(meteor_image, meteor_rect)
                meteor_rect.y += 5
                if meteor_rect.y > 730:
                    enemy_list.pop(i)
                if ship.colliderect(meteor_rect):
                    sounds.boom.play()
                    if shield_idx <= 0:
                        if meteor_image == Image_Load.meteors[0]:
                            heal += 1
                        if meteor_image == Image_Load.meteors[1]:
                            heal += 2
                        if meteor_image == Image_Load.meteors[2]:
                            heal += 3
                        if heal >= len(Image_Load.lives) - 1:
                            game = False
                    else:
                        shield_idx -= 1
                    enemy_list.pop(i)
                    count += 1