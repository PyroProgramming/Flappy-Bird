import pygame, random

pygame.init()

# -- images --
icon = pygame.image.load('data\images\icon.png')

sky = pygame.transform.scale_by(pygame.image.load('data\images\sky.png'), 0.65)
ground = pygame.transform.scale_by(pygame.image.load('data\images\ground.png'), 0.25)

birdimage = pygame.transform.scale(pygame.image.load('data\images\icon.png'), (75, 75))
bird = pygame.transform.rotate(birdimage, ((0 / 5) * 45))

pipe = pygame.transform.scale(pygame.image.load('data\images\pipes.png'), (400, 600))
pipe2 = pygame.transform.flip(pipe, 0, 1)

# -- masks --
pipeMask = pygame.mask.from_surface(pipe)
pipe2Mask = pygame.mask.from_surface(pipe2)

birdMask = pygame.mask.from_surface(bird)

groundMask = pygame.mask.from_surface(ground)

# -- fonts/text --
font = pygame.font.Font('data\Fonts\Blacknorthdemo-mLE25.otf', 75)
restartfont = pygame.font.Font('data\Fonts\Blacknorthdemo-mLE25.otf', 35)

restart = restartfont.render('Press "r" \n to restart', True, 'black', 'white')
score = font.render(f'0', True, 'black')

# -- window --
screen = pygame.display.set_mode((400, 750))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# -- variables --
run = True

skyX = - 20
groundX = 0

birdX, birdY = 10, 300
alive = False
playerVelocity = 0
gravity = 0.2
playerScore = 0

pipeX, pipeY = 100, 300

pipe2offset = pipe2.get_height() + 140

# -- functions --
def enactgravity():
    global birdY
    global playerVelocity

    playerVelocity += gravity

    print(playerVelocity)

    birdY += playerVelocity

def pipespawn():
    global pipeY

    pipeY = random.randrange(175, 600)

def movement():
    global pipeX
    global run
    global skyX
    global groundX
    global playerScore
    global score

    enactgravity()
    
    if pipeX == birdX - 150:
        playerScore += 1
        score = font.render(f'{playerScore}', True, 'black')

    if skyX > - sky.get_width() - 20:
        skyX -= 1
    else:
        skyX = - 30

    if groundX > - ground.get_width():
        groundX -= 3
    else:
        groundX = - 30

    if pipeX > 0 - pipe.get_width() + 75:
        pipeX -= 5
    else:
        pipeX = screen.get_width() - 75
        pipespawn()

def draw():
    global alive
    global playerScore
    global bird
    global birdMask

    if pipeMask.overlap(birdMask, (birdX - pipeX, birdY - pipeY)):
        alive = False

    if pipe2Mask.overlap(birdMask, (birdX - pipeX, birdY - pipeY + pipe2offset)):
        alive = False

    if groundMask.overlap(birdMask, (birdX - groundX, birdY - (screen.get_height() - ground.get_height()))):
        alive = False

    if alive:
        bird = pygame.transform.rotate(birdimage, - ((playerVelocity / 5) * 45))
        birdMask = pygame.mask.from_surface(bird)
        movement()

    screen.blit(sky, (skyX, - 10))
    screen.blit(sky, (skyX + sky.get_width() - 10, - 10))

    screen.blit(ground, (groundX, screen.get_height() - ground.get_height()))
    screen.blit(ground, (groundX + ground.get_width() - 1, screen.get_height() - ground.get_height()))
    screen.blit(ground, (groundX + ground.get_width() * 2 - 2, screen.get_height() - ground.get_height()))

    screen.blit(pipe, (pipeX, pipeY))
    screen.blit(pipe2, (pipeX, pipeY - pipe2offset))

    screen.blit(bird, (birdX, birdY))
    
    screen.blit(score, (screen.get_width() / 2 - score.get_width() / 2, 10))

    if not alive and playerScore >= 1:
        screen.blit(restart, (screen.get_width() / 2 - restart.get_width() / 2, screen.get_height() / 2 - restart.get_height() / 2))

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if gravity > 0:
                    gravity = - 0.2
                else:
                    gravity = 0.2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                alive = True
                if gravity > 0:
                    gravity = - 0.2
                else:
                    gravity = 0.2
            if event.key == pygame.K_r:
                if alive == False:
                    birdX, birdY = 10, 300
                    alive = False
                    playerVelocity = 0
                    gravity = 0.2
                    playerScore = 0
                    pipeX, pipeY = 150, 300
                    score = font.render(f'0', True, 'black')

    # -- background --
    screen.fill('light blue')

    # -- use functions --
    draw()

    # -- update display and set tick speed --
    pygame.display.update()

    clock.tick(60)

pygame.quit()