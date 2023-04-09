import pygame, sys, random
pygame.init()

# display screen set up
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# game loop
while True:

    # for event in events
    for event in pygame.event.get():
        # close if event == "x" 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # update the screen 60fps
    pygame.display.update()
    clock.tick(60)
