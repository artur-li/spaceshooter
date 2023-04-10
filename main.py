import pygame, sys, random
pygame.init()

# screen
screen = pygame.display.set_mode((500,700))
clock = pygame.time.Clock()

# score
score = 0
font = pygame.font.Font(None, 50)
def update_score():
    score_surf = font.render("SCORE: " + str(score), False, "grey", "black")
    score_rect = score_surf.get_rect(center=(250,100))
    screen.blit(score_surf,score_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(250,600))
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.centerx >= 25:
            self.rect.centerx -= 5
        elif keys[pygame.K_RIGHT] and self.rect.centerx <= 475:
            self.rect.centerx += 5
        elif keys[pygame.K_UP] and self.rect.centery >= 25:
            self.rect.centery -= 5
        elif keys[pygame.K_DOWN] and self.rect.centery <= 675:
            self.rect.centery += 5
    def collision(self):
        global game_state
        global over_state
        collided = pygame.sprite.spritecollide(player, obstacle_group, False)
        for i in collided:
            if i != None:
                game_state = False
                over_state = True
    def update(self):
        self.movement()
        self.collision()
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

class Obstacle1(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.Surface((400,20))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(x_pos,0))
    def movement(self):
        self.rect.centery += 2
    def destruction(self):
        global score
        if self.rect.centery > 710:
            pygame.sprite.Sprite.kill(self)
            score += 1
    def update(self):
        self.movement()
        self.destruction()
class Obstacle2(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(x_pos,0))
    def movement(self):
        self.rect.centery += 2
    def destruction(self):
        if self.rect.centery > 750:
            pygame.sprite.Sprite.kill(self)
    def update(self):
        self.movement()
        self.destruction()
timer = 180
def spawn_obstacles():
    global timer
    timer += 1
    if timer % 120 == 0:
        x_pos_list = [150, 350]
        obstacle = Obstacle1(random.choice(x_pos_list))
        obstacle_group.add(obstacle)
    elif timer % 60 == 0 and timer % 120 != 0:
        x_pos_list = [50,100,150,200,250,300,350,400,450]
        obstacle_a = Obstacle2(random.choice(x_pos_list))
        obstacle_group.add(obstacle_a)
        obstacle_b = Obstacle2(random.choice(x_pos_list))
        obstacle_group.add(obstacle_b)
        obstacle_c = Obstacle2(random.choice(x_pos_list))
        obstacle_group.add(obstacle_c)
obstacle_group = pygame.sprite.Group()

# start_game state
def start_game():
    global game_state
    global start_state
    play_surf = font.render("PLAY", False, "Blue", "black")
    play_rect = play_surf.get_rect(center=(250,350))
    screen.blit(play_surf,play_rect)
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() != (False, False, False):
        start_state = False
        game_state = True

# game_active state
def game():
    player_group.draw(screen)
    spawn_obstacles()
    obstacle_group.draw(screen)
    # update
    player_group.update()
    obstacle_group.update()
    # score
    update_score()

# game_over state
def game_over():
    global game_state
    global score
    score_surf = font.render("FINAL SCORE: " + str(score), False, "grey", "black")
    score_rect = score_surf.get_rect(center=(250,320))
    screen.blit(score_surf,score_rect)
    play_surf = font.render("PLAY AGAIN", False, "Blue", "black")
    play_rect = play_surf.get_rect(center=(250,380))
    screen.blit(play_surf,play_rect)
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() != (False, False, False):
        game_state = True
        score = 0
        obstacle_group.empty()

# state variables
start_state = True
game_state = False
over_state = False

# game loop
while True:
    screen.fill("black")

    for event in pygame.event.get():
        # close screen upon 'x'
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 

    if start_state:
        start_game()

    elif game_state:
        game()

    elif over_state:
        game_over()

    # update screen 60fps
    pygame.display.update()
    clock.tick(60)
