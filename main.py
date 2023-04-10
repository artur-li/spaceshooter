import pygame, sys, random
from datetime import datetime

# general 
pygame.init()
font = pygame.font.Font(None, 50)
count = 0

# display screen set up
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# spaceship class(sprite + movement + shooting)
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = font.render("A", False, "Green")
        self.rect = self.image.get_rect(center=(400, 380))
    def update(self):
        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.centerx < 790:
            self.rect.centerx += 5
        elif keys[pygame.K_LEFT] and self.rect.centerx > 10:
            self.rect.centerx -= 5
        # shooting
        global count 
        if count != 0:
            count -= 1
        if keys[pygame.K_SPACE]:
                if count == 0:
                    bullet = Bullet(self.rect.centerx, self.rect.centery)
                    spaceship_group.add(bullet)
                    count = 60

# bullet class(sprite + movement)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.surface.Surface((5, 10))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
    def update(self):
        self.rect.centery -= 5

# (group and sprites) -init
spaceship = Spaceship()
spaceship_group = pygame.sprite.Group()
spaceship_group.add(spaceship)

# game loop
while True:

    # for event in events
    for event in pygame.event.get():
        # close if event == "x" 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw to screen
    screen.fill("black")
    spaceship_group.draw(screen)

    # update the screen 60fps
    spaceship_group.update()
    pygame.display.update()
    clock.tick(60)
