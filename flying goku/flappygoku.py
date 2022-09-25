
import pygame
import random  # for generating random number
import sys  # we will use sys.exit to exit program
from pygame.locals import *  # basic pyame imports
from pygame import mixer
mixer.init()

# global variable for game
FPS = 32
SCREENWIDTH = 649
SCREENHEIGHT = 461
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
GOKU_HEIGHT ,GOKU_WIDTH =50 ,65
PLAYER = 'photo removed/goku_flying-removebg-preview.png'
BACKGROUND = 'photo removed/background1.png'
PIPE = 'gallery/sprites/pipe.png'
mixer.music.load("y2mate.com - ReZERO  Starting Life in Another World  Ending.mp3")
mixer.music.play(-1)


def welcomeScreen():
    # shows welcome image on screen
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex =  0  # int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = 0  # int(SCREENHEIGHT*0.13)
    basex = 0
    while True:

        for event in pygame.event.get():
            # if user click on cross button,close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses space or up key,start game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    # create 2 pipes for bliting
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 3), 'y': newPipe2[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 1.5), 'y': newPipe3[0]['y']},
    ]
    # list o flower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 3), 'y': newPipe2[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 1.5), 'y': newPipe3[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes,
                              score)  # this function return true if you are crashed
        if crashTest:
            return

        # check for score
        playerMIDPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMIDPos < pipeMidPos + 4:
                score += 1
                print(f"your score is  {score}")
                GAME_SOUNDS['point'].play()

        finalscore = score
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):  # make upper pipe and lower pipe in same group
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a new pipe when the first pipe is about to leave the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if pipe out of screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):  # make upper pipe and lower pipe in same group
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes, score):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            mixer.music.load("Jine Mera Dil Luteya.mp3")
            mixer.music.play(-1)
            print(f"your score is{score}")
            return True
        return False

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) <  GAME_SPRITES['pipe'][0].get_width():

            GAME_SOUNDS['hit'].play()
            mixer.music.load("Jine Mera Dil Luteya.mp3")
            mixer.music.play(-1)
            return True
        return False


# offset=a random length with trial and error
# PH=pipe height
# Sh screen height
# B=base height
# y2=random(offset,SH-B-1.2*offset)
# y1=PH-y2+offset
def getRandomPipe():  # generate position of two pipes(one bottom straight and other top rotated) blitting pn the screen
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipe
        {'x': pipeX, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == "__main__":
    # this will be the main poit from where our game will start
    pygame.init()  # initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('FLAPPY GOKU')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),

    )

    GAME_SPRITES['message'] = pygame.image.load('photo removed/intro.webp').convert_alpha()

    GAME_SPRITES['base'] = pygame.transform.scale(pygame.image.load('gallery/sprites/base.png').convert_alpha(),
                                                  (SCREENWIDTH, 100))
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), pygame.image.load(PIPE).convert_alpha()
    )

    # game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    GAME_SPRITES['background'] = pygame.transform.scale(pygame.image.load(BACKGROUND).convert(),
                                                        (SCREENWIDTH, SCREENHEIGHT))

    GAME_SPRITES['player'] = pygame.transform.scale(pygame.image.load(PLAYER).convert_alpha(),(GOKU_WIDTH, GOKU_HEIGHT))


    while True:
        welcomeScreen()  # show welcome screen to user until he presses a button
        mainGame()  # main game function
