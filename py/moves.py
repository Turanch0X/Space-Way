import pygame

class Spaceship:
    def __init__(self, x, y, step):
        self.x = x
        self.y = y
        self.step = step

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.y > -5:
            self.y -= self.step
        if keys[pygame.K_s] and self.y < 620:
            self.y += self.step
        if keys[pygame.K_a] and self.x > -10:
            self.x -= self.step
        if keys[pygame.K_d] and self.x < 310:
            self.x += self.step

class Sky:
    def __init__(self, win, img, y):
        self.window = win
        self.images = img
        self.y = y

    def move(self):
        self.window.blit(self.images.sky, (0, self.y))
        self.window.blit(self.images.sky, (0, self.y - 700))
        self.y += 2

        if self.y == 700:
                self.y = 0