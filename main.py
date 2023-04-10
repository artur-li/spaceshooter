import pygame, sys, random
from datetime import datetime

# general 
pygame.init()
font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 30)
start_screen = True
game = False
game_over = False
score = 0

# display screen set up
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# play screen
play_surf = font.render("PLAY", False, "Grey")
play_rect = play_surf.get_rect(center=(400,200))

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
        global score
        for bullet in bullets_shot:
            collided = pygame.sprite.spritecollide(bullet, enemy_group, True)
            for i in collided:
                score += 1

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
        global game_over
        self.rect.y += 2
        if self.rect.y > 380:
            game_over = True
# (enemy spawning)
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

    # start_screen state
    if start_screen:
        screen.blit(play_surf, play_rect)
        if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() != (False, False, False):
            start_screen = False
            game = True

    # game_running state
    elif game:

        # if game over then end game
        if game_over:
            game = False

        # enemy spawning function
        enemy_spawning()

        # draw to screen
        screen.fill("black")
        score_surf = font2.render("Score: " + str(score), False, "Grey")
        score_rect = score_surf.get_rect(center=(400,50))
        screen.blit(score_surf, score_rect)
        spaceship_group.draw(screen)
        enemy_group.draw(screen)

        # update the screen 60fps
        spaceship_group.update()
        enemy_group.update()

    # game_over state
    elif game_over:
        screen.fill("black")
        score2_surf = font.render("Final Score: " + str(score), False, "Grey")
        score2_rect = score2_surf.get_rect(center=(400,180))
        screen.blit(score2_surf, score2_rect)
        play_again_surf = font.render("play again", False, "Blue")
        play_again_rect = play_again_surf.get_rect(center=(400,220))
        screen.blit(play_again_surf, play_again_rect)
        if play_again_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() != (False, False, False):
            enemy_group.empty()
            game_over = False
            game = True
            score = 0


    pygame.display.update()
    clock.tick(60)
