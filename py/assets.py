import pygame

class Sounds():
    def __init__(self):
        self.shot = pygame.mixer.Sound('sounds\\shot.mp3')
        self.boom = pygame.mixer.Sound('sounds\\boom.mp3')
        self.energy_up = pygame.mixer.Sound('sounds\\energy_up.mp3')
        self.heal_up = pygame.mixer.Sound('sounds\\health_up.wav')
        self.shield_on = pygame.mixer.Sound('sounds\\shield_on.ogg')

        pygame.mixer.music.load('music\\oblivion.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)


class Images():
    def __init__(self):
        self.logo = pygame.image.load('images\\logo.ico')
        sky = pygame.image.load('images\\sky.jpg').convert()
        self.sky = pygame.transform.scale(sky, (400, 700)).convert_alpha()
        self.spaceship = pygame.image.load('images\\spaceship.png').convert_alpha()
        self.ammo = pygame.image.load('images\\ammo.png').convert_alpha()

        self.lives = [
            pygame.image.load('images\\lives\\0.png').convert_alpha(),
            pygame.image.load('images\\lives\\1.png').convert_alpha(),
            pygame.image.load('images\\lives\\2.png').convert_alpha(),
            pygame.image.load('images\\lives\\3.png').convert_alpha(),
            pygame.image.load('images\\lives\\4.png').convert_alpha(),
            pygame.image.load('images\\lives\\5.png').convert_alpha(),
            pygame.image.load('images\\lives\\6.png').convert_alpha(),
            pygame.image.load('images\\lives\\7.png').convert_alpha(),
            pygame.image.load('images\\lives\\8.png').convert_alpha()
            ]

        self.shields = [
            pygame.image.load('images\\shields\\0.png').convert_alpha(),
            pygame.image.load('images\\shields\\1.png').convert_alpha(),
            pygame.image.load('images\\shields\\2.png').convert_alpha(),
            pygame.image.load('images\\shields\\3.png').convert_alpha(),
            pygame.image.load('images\\shields\\4.png').convert_alpha(),
            pygame.image.load('images\\shields\\5.png').convert_alpha(),
            pygame.image.load('images\\shields\\6.png').convert_alpha(),
            pygame.image.load('images\\shields\\7.png').convert_alpha(),
            pygame.image.load('images\\shields\\8.png').convert_alpha()
        ]

        self.busts = [
            pygame.image.load('images\\busts\\ammo+.png').convert_alpha(),
            pygame.image.load('images\\busts\\health+.png').convert_alpha(),
            pygame.image.load('images\\busts\\shield+.png').convert_alpha(),
            pygame.image.load('images\\busts\\strike.png').convert_alpha()
        ]

        self.meteors = [
            pygame.image.load('images\\meteorits\\S.png').convert_alpha(),
            pygame.image.load('images\\meteorits\\M.png').convert_alpha(),
            pygame.image.load('images\\meteorits\\L.png').convert_alpha()
        ]


class Fonts():
    def __init__(self):
        self.label = pygame.font.Font('fonts\\title_font.ttf', 32)
        self.rec_label = pygame.font.Font('fonts\\title_font.ttf', 12)
        self.ammo_label = pygame.font.Font('fonts\\title_font.ttf', 18)

        self.finish_label = self.label.render('Game over', False, (255, 255, 0))
        self.restart_label = self.label.render('New game', False, (255, 255, 0))
        self.restart_label_rect = self.restart_label.get_rect(topleft=(130, 350))