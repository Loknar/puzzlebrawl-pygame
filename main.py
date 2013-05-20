## Puzzle Brawl (a Puzzle Attack / Panel De Pon / Puzzle Challenge clone)
## "Swap and Match" tile-based puzzle gameplay style
## http://www.notendur.hi.is/sfg6/puzzlebrawl/
## By Sveinn Floki Gudmundsson - svefgud@gmail.com

import sys, pygame
from pygame.locals import *
from GameLogic import *

FPS = 60
WINDOWWIDTH = 720
WINDOWHEIGHT = 560
BLOCKIMAGESIZE = 40
BOARDWIDTH = 6
BOARDHEIGHT = 12

LIGHTBLUE = (83, 161, 255)

backgroundImage = pygame.image.load('images/bg01.png')

POINTERIMAGE = []
POINTERIMAGE.append(pygame.image.load('images/pointer01.png'))
POINTERIMAGE.append(pygame.image.load('images/pointer02.png'))

BLOCKIMAGES = []
BLOCKIMAGES.append(pygame.image.load('images/block1trans.png'))
BLOCKIMAGES.append(pygame.image.load('images/block2trans.png'))
BLOCKIMAGES.append(pygame.image.load('images/block3trans.png'))
BLOCKIMAGES.append(pygame.image.load('images/block4trans.png'))
BLOCKIMAGES.append(pygame.image.load('images/block5trans.png'))
BLOCKIMAGES.append(pygame.image.load('images/block6trans.png'))

darkBLOCKIMAGES = []
darkBLOCKIMAGES.append(pygame.image.load('images/block1transDark.png'))
darkBLOCKIMAGES.append(pygame.image.load('images/block2transDark.png'))
darkBLOCKIMAGES.append(pygame.image.load('images/block3transDark.png'))
darkBLOCKIMAGES.append(pygame.image.load('images/block4transDark.png'))
darkBLOCKIMAGES.append(pygame.image.load('images/block5transDark.png'))
darkBLOCKIMAGES.append(pygame.image.load('images/block6transDark.png'))

BLOCKIMAGESblink = []
BLOCKIMAGESblink.append(pygame.image.load('images/block1trans_blink.png'))
BLOCKIMAGESblink.append(pygame.image.load('images/block2trans_blink.png'))
BLOCKIMAGESblink.append(pygame.image.load('images/block3trans_blink.png'))
BLOCKIMAGESblink.append(pygame.image.load('images/block4trans_blink.png'))
BLOCKIMAGESblink.append(pygame.image.load('images/block5trans_blink.png'))
BLOCKIMAGESblink.append(pygame.image.load('images/block6trans_blink.png'))

BLOCKIMAGESnaked = []
BLOCKIMAGESnaked.append(pygame.image.load('images/block1trans_naked.png'))
BLOCKIMAGESnaked.append(pygame.image.load('images/block2trans_naked.png'))
BLOCKIMAGESnaked.append(pygame.image.load('images/block3trans_naked.png'))
BLOCKIMAGESnaked.append(pygame.image.load('images/block4trans_naked.png'))
BLOCKIMAGESnaked.append(pygame.image.load('images/block5trans_naked.png'))
BLOCKIMAGESnaked.append(pygame.image.load('images/block6trans_naked.png'))

BLINGIMAGES = []
BLINGIMAGES.append(pygame.image.load('images/bling01.png'))
BLINGIMAGES.append(pygame.image.load('images/bling02.png'))
BLINGIMAGES.append(pygame.image.load('images/bling03.png'))
BLINGIMAGES.append(pygame.image.load('images/bling04.png'))
BLINGIMAGES.append(pygame.image.load('images/bling05.png'))
BLINGIMAGES.append(pygame.image.load('images/bling06.png'))
BLINGIMAGES.append(pygame.image.load('images/bling07.png'))
BLINGIMAGES.append(pygame.image.load('images/bling08.png'))
BLINGIMAGES.append(pygame.image.load('images/bling09.png'))
BLINGIMAGES.append(pygame.image.load('images/bling10.png'))
BLINGIMAGES.append(pygame.image.load('images/bling11.png'))
BLINGIMAGES.append(pygame.image.load('images/bling12.png'))
BLINGIMAGES.append(pygame.image.load('images/bling13.png'))
BLINGIMAGES.append(pygame.image.load('images/bling14.png'))

CHAINIMAGES = []
CHAINIMAGES.append(pygame.image.load('images/chain02.png'))
CHAINIMAGES.append(pygame.image.load('images/chain03.png'))
CHAINIMAGES.append(pygame.image.load('images/chain04.png'))
CHAINIMAGES.append(pygame.image.load('images/chain05.png'))
CHAINIMAGES.append(pygame.image.load('images/chain06.png'))
CHAINIMAGES.append(pygame.image.load('images/chain07.png'))
CHAINIMAGES.append(pygame.image.load('images/chain08.png'))
CHAINIMAGES.append(pygame.image.load('images/chain09.png'))
CHAINIMAGES.append(pygame.image.load('images/chain10.png'))
CHAINIMAGES.append(pygame.image.load('images/chain11.png'))
CHAINIMAGES.append(pygame.image.load('images/chain12.png'))
CHAINIMAGES.append(pygame.image.load('images/chain13.png'))
CHAINIMAGES.append(pygame.image.load('images/chain14.png'))
CHAINIMAGES.append(pygame.image.load('images/chain15.png'))

COMBOIMAGES = []
COMBOIMAGES.append(pygame.image.load('images/combo04.png'))
COMBOIMAGES.append(pygame.image.load('images/combo05.png'))
COMBOIMAGES.append(pygame.image.load('images/combo06.png'))
COMBOIMAGES.append(pygame.image.load('images/combo07.png'))
COMBOIMAGES.append(pygame.image.load('images/combo08.png'))
COMBOIMAGES.append(pygame.image.load('images/combo09.png'))
COMBOIMAGES.append(pygame.image.load('images/combo10.png'))
COMBOIMAGES.append(pygame.image.load('images/combo11.png'))
COMBOIMAGES.append(pygame.image.load('images/combo12.png'))
COMBOIMAGES.append(pygame.image.load('images/combo13.png'))
COMBOIMAGES.append(pygame.image.load('images/combo14.png'))
COMBOIMAGES.append(pygame.image.load('images/combo15.png'))
COMBOIMAGES.append(pygame.image.load('images/combo16.png'))
COMBOIMAGES.append(pygame.image.load('images/combo17.png'))
COMBOIMAGES.append(pygame.image.load('images/combo18.png'))
COMBOIMAGES.append(pygame.image.load('images/combo19.png'))
COMBOIMAGES.append(pygame.image.load('images/combo20.png'))
COMBOIMAGES.append(pygame.image.load('images/combo21.png'))
COMBOIMAGES.append(pygame.image.load('images/combo22.png'))
COMBOIMAGES.append(pygame.image.load('images/combo23.png'))
COMBOIMAGES.append(pygame.image.load('images/combo24.png'))
COMBOIMAGES.append(pygame.image.load('images/combo25.png'))
COMBOIMAGES.append(pygame.image.load('images/combo26.png'))
COMBOIMAGES.append(pygame.image.load('images/combo27.png'))
COMBOIMAGES.append(pygame.image.load('images/combo28.png'))
COMBOIMAGES.append(pygame.image.load('images/combo29.png'))
COMBOIMAGES.append(pygame.image.load('images/combo30.png'))
COMBOIMAGES.append(pygame.image.load('images/combo31.png'))
COMBOIMAGES.append(pygame.image.load('images/combo32.png'))
COMBOIMAGES.append(pygame.image.load('images/combo33.png'))
COMBOIMAGES.append(pygame.image.load('images/combo34.png'))
COMBOIMAGES.append(pygame.image.load('images/combo35.png'))
COMBOIMAGES.append(pygame.image.load('images/combo36.png'))

BOARDRECTS = []
for k in range(20):
    BOARDRECTS.append([])
    for x in range(BOARDWIDTH):
        BOARDRECTS[k].append([])
        for y in range(BOARDHEIGHT):
            r = pygame.Rect((240 + (x * BLOCKIMAGESIZE),
                             480 - (y * BLOCKIMAGESIZE) - 2*k,
                             240 + (x * BLOCKIMAGESIZE)+ 40,
                             480 - (y * BLOCKIMAGESIZE) - 2*k + 40))
            BOARDRECTS[k][x].append(r)

newBLOCKSRECTS = []
for k in range(20):
    newBLOCKSRECTS.append([])
    for x in range(BOARDWIDTH):
        r = pygame.Rect((240 + (x * BLOCKIMAGESIZE),
                         480 + 40 - 2*k,
                         240 + (x * BLOCKIMAGESIZE)+ 40,
                         480 + 40))
        newBLOCKSRECTS[k].append(r)

cutNewBLOCKS = []
for k in range(20):
    r = pygame.Rect((0,0,40,2*k))
    cutNewBLOCKS.append(r)

BLINGRECTS = []
for k in range(20):
    BLINGRECTS.append([])
    for x in range(BOARDWIDTH):
        BLINGRECTS[k].append([])
        for y in range(BOARDHEIGHT):
            r = pygame.Rect((240 + (x * BLOCKIMAGESIZE) - 40,
                             480 - (y * BLOCKIMAGESIZE) - 2*k - 40,
                             240 + (x * BLOCKIMAGESIZE) + 40 + 40,
                             480 - (y * BLOCKIMAGESIZE) - 2*k + 40 + 40))
            BLINGRECTS[k][x].append(r)

pointerRECTS = []
for k in range(20):
    pointerRECTS.append([])
    for x in range(BOARDWIDTH):
        pointerRECTS[k].append([])
        for y in range(BOARDHEIGHT):
            r = pygame.Rect((236 + (x * BLOCKIMAGESIZE),
                             476 - (y * BLOCKIMAGESIZE) - 2*k,
                             236 + (x * BLOCKIMAGESIZE) + 88,
                             476 - (y * BLOCKIMAGESIZE) - 2*k + 48))
            pointerRECTS[k][x].append(r)

swapRECTS = []
for k in range(20):
    swapRECTS.append([])
    for x in range(BOARDWIDTH-1):
        swapRECTS[k].append([])
        for y in range(BOARDHEIGHT):
            swapRECTS[k][x].append([])
            for z in range(3):
                r = pygame.Rect((240 + (x * BLOCKIMAGESIZE) + (z+1)*10,
                                 480 - (y * BLOCKIMAGESIZE) - 2*k,
                                 240 + (x * BLOCKIMAGESIZE) + 40 + (z+1)*10,
                                 480 - (y * BLOCKIMAGESIZE) - 2*k + 40))
                swapRECTS[k][x][y].append(r)


class Keystate:
    def __init__(self):
        self.RCMD = False
        self.LCMD = False
        self.R = False
        self.Q = False
        self.Z = False
        self.A = False
        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False

def eventHandler():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYDOWN):
        if event.key == K_RMETA: # right cmd on mac
            keystate.RCMD = True
        if event.key == K_LMETA: # left cmd on mac
            keystate.LCMD = True
        if event.key == K_r:
            keystate.R = True
            setupBoard(board)
        if event.key == K_z:
            keystate.Z = True
            board.PointerSwap()
        if event.key == K_a:
            keystate.A = True
        if event.key == K_q:
            if keystate.RCMD or keystate.LCMD:
                terminate() # quit if cmd + q is pressed
            keystate.Q = True
        if event.key == K_UP:
            keystate.UP = True
            board.MovePointerUp()
        if event.key == K_DOWN:
            keystate.DOWN = True
            board.MovePointerDown()
        if event.key == K_RIGHT:
            keystate.RIGHT = True
            board.MovePointerRight()
        if event.key == K_LEFT:
            keystate.LEFT = True
            board.MovePointerLeft()
    for event in pygame.event.get(KEYUP):
        if event.key == K_RMETA:
            keystate.RCMD = False
        if event.key == K_LMETA:
            keystate.LCMD = False
        if event.key == K_r:
            keystate.R = False
        if event.key == K_z:
            keystate.Z = False
        if event.key == K_a:
            keystate.A = False
        if event.key == K_q:
            keystate.Q = False
        if event.key == K_UP:
            keystate.UP = False
        if event.key == K_DOWN:
            keystate.DOWN = False
        if event.key == K_RIGHT:
            keystate.RIGHT = False
        if event.key == K_LEFT:
            keystate.LEFT = False
    pygame.event.get() # throws away any pending events that won't be used
    if keystate.A:
        board.ElevatePress = True
    else:
        board.ElevatePress = False

def setupBoard(board):
    for y in range(12):
        for x in range(6):
            board.Blocks[y][x] = 0
            board.States[y][x] = 0
            board.PopStates[y][x] = 0
            board.ChainStates[y][x] = 0
            board.Counter[y][x] = 0
            board.PopStateCounter1[y][x] = 0
            board.PopStateCounter2[y][x] = 0
    
    board.Blocks[0][0] = 0
    board.Blocks[0][1] = 3
    board.Blocks[0][2] = 5
    board.Blocks[0][3] = 5
    board.Blocks[0][4] = 1
    board.Blocks[0][5] = 5
    
    board.Blocks[1][0] = 0
    board.Blocks[1][1] = 2
    board.Blocks[1][2] = 2
    board.Blocks[1][3] = 1
    board.Blocks[1][4] = 3
    board.Blocks[1][5] = 1
    
    board.Blocks[2][0] = 0
    board.Blocks[2][1] = 3
    board.Blocks[2][2] = 2
    board.Blocks[2][3] = 5
    board.Blocks[2][4] = 1
    board.Blocks[2][5] = 3
    
    board.Blocks[3][0] = 0
    board.Blocks[3][1] = 3
    board.Blocks[3][2] = 4
    board.Blocks[3][3] = 5
    board.Blocks[3][4] = 1
    board.Blocks[3][5] = 0
    
    board.Blocks[4][0] = 0
    board.Blocks[4][1] = 0
    board.Blocks[4][2] = 4
    board.Blocks[4][3] = 0
    board.Blocks[4][4] = 3
    board.Blocks[4][5] = 0
    
    board.Blocks[5][0] = 0
    board.Blocks[5][1] = 0
    board.Blocks[5][2] = 5
    board.Blocks[5][3] = 0
    board.Blocks[5][4] = 5
    board.Blocks[5][5] = 0
    
    board.Blocks[6][0] = 0
    board.Blocks[6][1] = 0
    board.Blocks[6][2] = 4
    board.Blocks[6][3] = 0
    board.Blocks[6][4] = 3
    board.Blocks[6][5] = 0
    
    board.Blocks[7][0] = 0
    board.Blocks[7][1] = 0
    board.Blocks[7][2] = 0
    board.Blocks[7][3] = 0
    board.Blocks[7][4] = 3
    board.Blocks[7][5] = 0

def terminate():
    pygame.quit()
    sys.exit()

def drawBoard(b):
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            if b.Blocks[y][x] != 0:
                if b.swap and (x == b.swapX or x == (b.swapX+1)) and y == b.swapY:
                    if x == b.swapX:
                        if 3 < b.swapCounter <= 4:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x][y][2])
                        elif 2 < b.swapCounter <= 3:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x][y][1])
                        elif 1 < b.swapCounter <= 2:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x][y][0])
                        elif b.swapCounter <= 1:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
                    elif x == (b.swapX+1):
                        if 3 < b.swapCounter <= 4:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x-1][y][0])
                        elif 2 < b.swapCounter <= 3:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x-1][y][1])
                        elif 1 < b.swapCounter <= 2:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],swapRECTS[b.Elevation][x-1][y][2])
                        elif b.swapCounter <= 1:
                            DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
                elif b.States[y][x] == 9:
                    if b.PopStates[y][x] < 38 and b.PopStates[y][x]%2 == 1:
                        DISPLAYSURF.blit(BLOCKIMAGESblink[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] < 38 and b.PopStates[y][x]%2 == 0:
                        DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 38:
                        DISPLAYSURF.blit(BLOCKIMAGESnaked[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 42:
                        DISPLAYSURF.blit(BLINGIMAGES[0],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 43:
                        DISPLAYSURF.blit(BLINGIMAGES[1],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 44:
                        DISPLAYSURF.blit(BLINGIMAGES[2],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 45:
                        DISPLAYSURF.blit(BLINGIMAGES[3],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 46:
                        DISPLAYSURF.blit(BLINGIMAGES[4],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 47:
                        DISPLAYSURF.blit(BLINGIMAGES[5],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 48:
                        DISPLAYSURF.blit(BLINGIMAGES[6],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 49:
                        DISPLAYSURF.blit(BLINGIMAGES[7],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 50:
                        DISPLAYSURF.blit(BLINGIMAGES[8],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 51:
                        DISPLAYSURF.blit(BLINGIMAGES[9],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 52:
                        DISPLAYSURF.blit(BLINGIMAGES[10],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 53:
                        DISPLAYSURF.blit(BLINGIMAGES[11],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 54:
                        DISPLAYSURF.blit(BLINGIMAGES[12],BLINGRECTS[b.Elevation][x][y])
                    elif b.PopStates[y][x] == 55:
                        DISPLAYSURF.blit(BLINGIMAGES[13],BLINGRECTS[b.Elevation][x][y])
                    if b.ComboNoteCounter[y][x] > 0:
                        DISPLAYSURF.blit(COMBOIMAGES[b.ComboNote[y][x] - 4],BOARDRECTS[b.Elevation][x][y])
                        if b.ChainNoteCounter[y][x] > 0:
                            DISPLAYSURF.blit(CHAINIMAGES[b.ChainCount - 1],BOARDRECTS[b.Elevation][x][y+1])
                    elif b.ChainNoteCounter[y][x] > 0:
                        DISPLAYSURF.blit(CHAINIMAGES[b.ChainCount - 1],BOARDRECTS[b.Elevation][x][y])
                    
                else:
                    DISPLAYSURF.blit(BLOCKIMAGES[b.Blocks[y][x]-1],BOARDRECTS[b.Elevation][x][y])
    if b.Elevation != 0:
        for x in range(BOARDWIDTH):
            DISPLAYSURF.blit(darkBLOCKIMAGES[b.NewBlocks[x]-1],newBLOCKSRECTS[b.Elevation][x],cutNewBLOCKS[b.Elevation])

def drawPointer(b):
    if b.pointerTick:
        DISPLAYSURF.blit(POINTERIMAGE[1],pointerRECTS[b.Elevation][b.pointerX][b.pointerY])
    else:
        DISPLAYSURF.blit(POINTERIMAGE[0],pointerRECTS[b.Elevation][b.pointerX][b.pointerY])

def playSounds(b):
    if b.movePointerSoundPlay:
        movePointerSound.play()
        b.movePointerSoundPlay = False
    if b.swapBlocksSoundPlay:
        swapBlocksSound.play()
        b.swapBlocksSoundPlay = False
    if b.popBlocksSoundPlay:
        popBlocksSound.play()
        b.popBlocksSoundPlay = False
    if b.gutWrenchingScreamPlay:
        gutWrenchingScream.play()
        b.gutWrenchingScreamPlay = False

def runGame():
    while True:
        board.BoardTick()
        eventHandler()
        playSounds(board)
        if board.RedrawBoard:
            DISPLAYSURF.blit(backgroundImage,pygame.Rect(0,0,WINDOWWIDTH,WINDOWHEIGHT))
            myScore = myCourierNewFont.render(str(board.score), True, LIGHTBLUE)
            myScoreRect = myScore.get_rect()
            myScoreRect.right = WINDOWWIDTH
            myScoreRect.move_ip(-40,40)
            DISPLAYSURF.blit(myScore, myScoreRect)
            drawBoard(board)
            drawPointer(board)
            pygame.display.update()
            board.RedrawBoard = False
        FPSCLOCK.tick(FPS)

def main():
    global FPSCLOCK, DISPLAYSURF, keystate, board, movePointerSound, swapBlocksSound
    global popBlocksSound, myCourierNewFont, myScore, myScoreRect
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    pygame.mixer.set_num_channels(4)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Puzzle Brawl')
    
    pygame.mixer.music.load('sounds/savant_awsm01.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
    movePointerSound = pygame.mixer.Sound('sounds/movePointer2.wav')
    swapBlocksSound = pygame.mixer.Sound('sounds/swapBlocks2.wav')
    popBlocksSound = pygame.mixer.Sound('sounds/comboMade.wav')
    gutWrenchingScream = pygame.mixer.Sound('sounds/gutwrenching_scream.wav')
    
    keystate = Keystate()
    board = PuzzleBrawlBoard()
    
    setupBoard(board)
    
    DISPLAYSURF.blit(backgroundImage,pygame.Rect(0,0,WINDOWWIDTH,WINDOWHEIGHT))
    
    myCourierNewFont = pygame.font.Font('font/Courier_New.ttf', 26)
    myScore = myCourierNewFont.render(str(0), True, LIGHTBLUE)
    myScoreRect = myScore.get_rect()
    myScoreRect.right = WINDOWWIDTH
    myScoreRect.move_ip(-40,40)
    DISPLAYSURF.blit(myScore, myScoreRect)
    
    drawBoard(board)
    pygame.display.update()
    runGame()


if __name__ == '__main__':
    main()
