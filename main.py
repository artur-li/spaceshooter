import pygame, sys, random
from datetime import datetime

# general 
pygame.init()
font = pygame.font.Font(None, 50)

# display screen set up
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# spaceship class(sprite + movement + shooting)
count = 0
bullets_shot = []
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = font.render("A", False, "Green")
        self.rect = self.image.get_rect(center=(400, 380))
    def update(self):
        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.centerx < 790:
            self.rect.centerx += 7.5
        elif keys[pygame.K_LEFT] and self.rect.centerx > 10:
            self.rect.centerx -= 7.5
        # shooting
        global count 
        if count != 0:
            count -= 1
        if keys[pygame.K_SPACE]:
                if count == 0:
                    bullet = Bullet(self.rect.centerx, self.rect.centery)
                    bullets_shot.append(bullet)
                    spaceship_group.add(bullet)
                    count = 30
        # collisions with enemy
        for bullet in bullets_shot:
            pygame.sprite.spritecollide(bullet, enemy_group, True)


# bullet class(sprite + movement)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.surface.Surface((5, 10))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
    def update(self):
        self.rect.centery -= 5

# enemy class(sprite + movement)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(random.randint(20,780),0))
    def update(self):
        self.rect.y += 2
# (enemy spawining)
spawn_amount = random.randint(1,2)
count2 = 0
interval = random.randint(120,300)
def enemy_spawning():
    global spawn_amount
    global count2
    global interval
    count2 += 1
    if count2 % interval == 0:
        if spawn_amount == 1:
            enemy = Enemy()
            enemy_group.add(enemy)
            count2 = 0
            interval = random.randint(120,300)
            spawn_amount = random.randint(1,2)
        elif spawn_amount == 2:
            enemy = Enemy()
            enemy2 = Enemy()
            enemy_group.add(enemy)
            enemy_group.add(enemy2)
            count2 = 0
            interval = random.randint(120,300)
            spawn_amount = random.randint(1,2)

# (groups and sprites) -init
# spaceship
spaceship = Spaceship()
spaceship_group = pygame.sprite.Group()
spaceship_group.add(spaceship)
# enemies
enemy = Enemy()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

# game loop
while True:

    # for event in events
    for event in pygame.event.get():
        # close if event == "x" 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # enemy spawning function
    enemy_spawning()

    # draw to screen
    screen.fill("black")
    spaceship_group.draw(screen)
    enemy_group.draw(screen)

    # update the screen 60fps
    spaceship_group.update()
    enemy_group.update()
    pygame.display.update()
    clock.tick(60)
