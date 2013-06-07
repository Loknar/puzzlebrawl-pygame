## Puzzle Brawl (a Puzzle Attack / Panel De Pon / Puzzle Challenge clone)
## "Swap and Match" tile-based puzzle gameplay style
## http://www.notendur.hi.is/sfg6/puzzlebrawl/
## By Sveinn Floki Gudmundsson - svefgud@gmail.com

INERTIA = 16 # the time it takes for block to start falling

import random

# Descr:  Holds the state of the board and has accessible functions for legal actions
# Usage:  board = PuzzlebrawlBoard()
# Before: Nothing
# After:  board is a new puzzlebrawl board
class PuzzleBrawlBoard:
    def __init__(self):
        self.hiscore = 0
        self.score = 0
        self.speedlvl = 1
        
        # True if board needs to be redrawn, else False
        self.RedrawBoard = True
        
        # True if certain sounds are to be played, else False
        self.movePointerSoundPlay = False
        self.swapBlocksSoundPlay = False
        self.popBlocksSoundPlay = False
        self.gutWrenchingScreamPlay = False
        
        # Placement of pointer
        self.pointerX = 2
        self.pointerY = 6
        
        # Pointer has two visual states and 'ticks' between the states
        self.pointerTick = False
        # Countdown for pointer to change state
        self.pointerCount = 10
        
        # True if swap is being executed
        self.swap = False
        # Place of current swap
        self.swapX = 0
        self.swapY = 0
        # State/counter for swap
        self.swapCounter = 0
        
        # True if chain requirements for a chain are met
        self.isChain = False
        # Helping variable for choosing highest block to the left in chain, possibly unnecessary
        self.isChainFirstBlock = False
        # Current chain count
        self.ChainCount = 0
        
        # True if board is supposed to take a step up
        self.Elevate = False
        # True if board is forced to take a step up
        self.ElevatePress = False
        # Blocks rise in 20 steps to higher floor, 0 <= Elevation <= 19
        self.Elevation = 0
        # Countdown to next elevation step up
        self.ElevateCounter = 30
        # Delay countdown before losing when blocks reach the ceiling
        self.ElevateTopDelayer = 180
        
        # Holds the new blocks spawning from the bottom
        self.NewBlocks = [0,0,0,0,0,0]
        self.__MakeNewBlocks()
        
        # Couple of 12x6 matrices for storing state of the board
        # Note to self: perhaps using something else than lists could be better for performance
        self.ChainMarks = []
        self.Blocks = [] # Blocks
        self.States = [] # States of blocks in corresponding place
        self.PopStates = [] # Current pop state of a block
        self.ChainStates = [] # Current chain state of a block
        self.Counter = [] # countdown for states in corresponding place
        self.PopStateCounter1 = [] # time from last blink of a popping block until it pops
        self.PopStateCounter2 = [] # time from pop until the space becomes accessible by other blocks
        self.ComboNote = [] # boolean matrix for whether or not a combo note is in corresponding place
        self.ComboNoteCounter = [] # state counter for combo note
        self.ChainNote = [] # boolean matrix for whether or not a chain note is in corresponding place
        self.ChainNoteCounter = [] # state counter for chain note
        for i in range(12):
            self.Blocks.append([0] * 6)
            self.States.append([0] * 6)
            self.PopStates.append([0] * 6)
            self.ChainStates.append([0] * 6)
            self.Counter.append([0] * 6)
            self.PopStateCounter1.append([0] * 6)
            self.PopStateCounter2.append([0] * 6)
            self.ComboNote.append([0] * 6)
            self.ComboNoteCounter.append([0] * 6)
            self.ChainNote.append([0] * 6)
            self.ChainNoteCounter.append([0] * 6)
            self.ChainMarks.append([False] * 6)
    
    # Private
    # Descr:  Adds n to current score
    # Before: n is a positive integer
    # After:  n has been added to the score of the board
    def __AddToScore(self, n):
        self.score += n
        self.RedrawBoard = True
    
    # Private
    # Descr:  Creates new blocks that are to spawn from bottom of the board
    # Before: Nothing
    # After:  New blocks to be spawned from bottom created
    def __MakeNewBlocks(self):
        for x in range(6):
            self.NewBlocks[x] = random.randint(1,6)
            if x > 1:
                while self.NewBlocks[x] == self.NewBlocks[x-1] == self.NewBlocks[x-2]:
                    self.NewBlocks[x] = random.randint(1,6)
    
    # Descr:  Moves pointer up
    # Usage:  board.MovePointerUp()
    # Before: board is a puzzlebrawl board
    # After:  If pointer is not in highest position it is moved up
    def MovePointerUp(self):
        if self.pointerY < 10 or (self.pointerY == 10 and self.Elevation == 0):
            self.pointerY += 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Descr:  Moves pointer down
    # Usage:  board.MovePointerDown()
    # Before: board is a puzzlebrawl board
    # After:  If pointer is not in lowest position it is moved down
    def MovePointerDown(self):
        if self.pointerY > 0:
            self.pointerY -= 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Descr:  Moves pointer to the right
    # Usage:  board.MovePointerRight()
    # Before: board is a puzzlebrawl board
    # After:  If pointer is not in completely right position it is moved to the right
    def MovePointerRight(self):
        if self.pointerX < 4:
            self.pointerX += 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Descr:  Moves pointer to the left
    # Usage:  board.MovePointerLeft()
    # Before: board is a puzzlebrawl board
    # After:  If pointer is not in completely left position it is moved to the left
    def MovePointerLeft(self):
        if self.pointerX > 0:
            self.pointerX -= 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Descr:  Starts a swap if there isn't one going on
    # Usage:  board.PointerSwap()
    # Before: board is a puzzlebrawl board
    # After:  if legal, we start a swap in the current pointer position
    def PointerSwap(self):
        if self.swap:
            return
        if self.Blocks[self.pointerY][self.pointerX] == 0 and self.Blocks[self.pointerY][self.pointerX + 1] == 0:
            return
        if self.States[self.pointerY][self.pointerX] > 3 or self.States[self.pointerY][self.pointerX + 1] > 3:
            return
        if self.pointerY < 11:
            if self.States[self.pointerY + 1][self.pointerX] == 1 or self.States[self.pointerY + 1][self.pointerX + 1] == 1:
                return
            if self.States[self.pointerY + 1][self.pointerX] == 2 or self.States[self.pointerY + 1][self.pointerX + 1] == 2:
                return
            if self.States[self.pointerY + 1][self.pointerX] == 4 or self.States[self.pointerY + 1][self.pointerX + 1] == 4:
                return
            if self.States[self.pointerY + 1][self.pointerX] == 5 or self.States[self.pointerY + 1][self.pointerX + 1] == 5:
                return
            if self.States[self.pointerY + 1][self.pointerX] == 6 or self.States[self.pointerY + 1][self.pointerX + 1] == 6:
                return
            if self.States[self.pointerY + 1][self.pointerX] == 7 or self.States[self.pointerY + 1][self.pointerX + 1] == 7:
                return
        self.swap = True
        self.swapX = self.pointerX
        self.swapY = self.pointerY
        self.swapCounter = 4
        if self.swapY > 0:
            if self.Blocks[self.swapY-1][self.swapX] == 0:
                self.States[self.swapY][self.swapX] = 4
                self.Counter[self.swapY][self.swapX] = INERTIA + 5 # plus frames until __PointerSwapFinish is called
            if self.Blocks[self.swapY-1][self.swapX+1] == 0:
                self.States[self.swapY][self.swapX+1] = 4
                self.Counter[self.swapY][self.swapX+1] = INERTIA + 5 # plus frames until __PointerSwapFinish is called
        self.__SwitchBlocks(self.swapY, self.swapX, self.swapY, self.swapX + 1)
        if self.Blocks[self.swapY][self.swapX] == 0:
            self.States[self.swapY][self.swapX] = 0
        elif self.Blocks[self.swapY][self.swapX+1] == 0:
            self.States[self.swapY][self.swapX+1] = 0
        self.swapBlocksSoundPlay = True
    
    # Private
    # Descr:  Counts down state of the swap and when the swap is over __PointerSwapFinish() is called to seal the deal
    # Before: Nothing
    # After:  see description
    def __SwapHandling(self):
        if self.swap:
            if self.swapCounter > 0:
                self.swapCounter -= 1
            else:
                self.__PointerSwapFinish()
    
    # Private
    # Descr:  When swap finishes this function is called to finish the deal
    # Before: swap in process
    # After:  finished swapping
    def __PointerSwapFinish(self):
        if self.swapY < 11:
            if self.Blocks[self.swapY][self.swapX+1] == 0 and self.Blocks[self.swapY+1][self.swapX+1] != 0:
                if self.States[self.swapY+1][self.swapX+1] == 0 or self.States[self.swapY+1][self.swapX+1] == 3:
                    self.States[self.swapY+1][self.swapX+1] = 4
                    self.Counter[self.swapY+1][self.swapX+1] = INERTIA
            if self.Blocks[self.swapY][self.swapX] == 0 and self.Blocks[self.swapY+1][self.swapX] != 0:
                if self.States[self.swapY+1][self.swapX] == 0 or self.States[self.swapY+1][self.swapX] == 3:
                    self.States[self.swapY+1][self.swapX] = 4
                    self.Counter[self.swapY+1][self.swapX] = INERTIA
        if self.Blocks[self.swapY][self.swapX] != 0 and self.States[self.swapY][self.swapX] == 0:
            self.__CheckForPop(self.swapY,self.swapX)
        if self.Blocks[self.swapY][self.swapX+1] != 0 and self.States[self.swapY][self.swapX+1] == 0:
            self.__CheckForPop(self.swapY,self.swapX+1)
        self.swap = False
    
    # Private
    # Descr:  Help function for swapping places of two blocks
    # Before: (Y1, X1) and (Y2, X2) are positions in the board
    # After:  blocks in (Y1, X1) and (Y2, X2) have switched places
    def __SwitchBlocks(self, Y1, X1, Y2, X2):
        self.Blocks[Y1][X1], self.Blocks[Y2][X2] = self.Blocks[Y2][X2], self.Blocks[Y1][X1]
    
    # Private
    # Descr:  Handles making blocks fall
    # Before: block in place (y, x) is in one of the falling states and the blocks counter is at zero
    # After:  appropriate changes made regarding the block
    def __Fall(self, y, x, state):
        if y > 0:
            if self.Blocks[y-1][x] == 0:
                self.__SwitchBlocks(y, x, y - 1, x)
                self.States[y][x] = 0
                if state == 4:
                    self.States[y-1][x] = 5
                elif state == 5 or state == 1:
                    self.States[y-1][x] = 1
                elif state == 6:
                    self.States[y-1][x] = 7
                elif state == 7 or state == 2:
                    self.States[y-1][x] = 2
                self.Counter[y-1][x] = 2
                if y < 11:
                    if self.Blocks[y+1][x] != 0:
                        if state == 0 or state == 1 or state == 4 or state == 5:
                            if self.States[y+1][x] == 0 or self.States[y+1][x] == 3:
                                self.States[y+1][x] = 1
                                self.Counter[y+1][x] = 0
                        elif state == 2 or state == 6 or state == 7:
                            if self.States[y+1][x] == 0 or self.States[y+1][x] == 3:
                                self.States[y+1][x] = 2
                                self.Counter[y+1][x] = 0
            elif self.States[y-1][x] == 4 or self.States[y-1][x] == 5 or (self.swap and self.swapY == (y-1) and (self.swapX == x or self.swapX == (x-1))):
                if self.Counter[y-1][x] == 1:
                    if self.States[y][x] == 2 or self.States[y][x] == 7:
                        self.States[y-1][x] = 7
                    elif self.States[y][x] == 1 or self.States[y][x] == 5:
                        self.States[y-1][x] = 5
            else:
                if not self.__CheckForPop(y,x):
                    self.States[y][x] = 3
                    self.Counter[y][x] = 3
        else:
            if not self.__CheckForPop(y,x):
                self.States[y][x] = 3
                self.Counter[y][x] = 3
        self.RedrawBoard = True
    
    # Private
    # Descr:  Checks if a block fulfills requirements for popping and if so, changes the state of the board accordingly
    # Before: Nothing
    # After:  marks blocks that fulfill requirements for poppping, returns True if pop happened, else False
    def __CheckForPop(self, blockY, blockX):
        result = False
        blockType = self.Blocks[blockY][blockX]
        blockState = self.States[blockY][blockX]
        if blockType == 0:
            return result
        a = False
        b = False
        c = False
        d = False
        e = False
        f = False
        g = False
        h = False
        if blockY > 1:
            if self.States[blockY-2][blockX] == 0 or self.States[blockY-2][blockX] == 3 or self.States[blockY-2][blockX] == 8:
                a = blockType == self.Blocks[blockY-2][blockX]
        if blockY > 0:
            if self.States[blockY-1][blockX] == 0 or self.States[blockY-1][blockX] == 3 or self.States[blockY-1][blockX] == 8:
                b = blockType == self.Blocks[blockY-1][blockX]
        if blockX > 1:
            if self.States[blockY][blockX-2] == 0 or self.States[blockY][blockX-2] == 3 or self.States[blockY][blockX-2] == 8:
                c = blockType == self.Blocks[blockY][blockX-2]
        if blockX > 0:
            if self.States[blockY][blockX-1] == 0 or self.States[blockY][blockX-1] == 3 or self.States[blockY][blockX-1] == 8:
                d = blockType == self.Blocks[blockY][blockX-1]
        if blockY < 10:
            if self.States[blockY+2][blockX] == 0 or self.States[blockY+2][blockX] == 3 or self.States[blockY+2][blockX] == 8:
                h = blockType == self.Blocks[blockY+2][blockX]
        if blockY < 11:
            if self.States[blockY+1][blockX] == 0 or self.States[blockY+1][blockX] == 3 or self.States[blockY+1][blockX] == 8:
                g = blockType == self.Blocks[blockY+1][blockX]
        if blockX < 4:
            if self.States[blockY][blockX+2] == 0 or self.States[blockY][blockX+2] == 3 or self.States[blockY][blockX+2] == 8:
                f = blockType == self.Blocks[blockY][blockX+2]
        if blockX < 5:
            if self.States[blockY][blockX+1] == 0 or self.States[blockY][blockX+1] == 3 or self.States[blockY][blockX+1] == 8:
                e = blockType == self.Blocks[blockY][blockX+1]
        if a and b:
            self.States[blockY - 2][blockX] = 8
            self.Counter[blockY - 2][blockX] = 0
            self.States[blockY - 1][blockX] = 8
            self.Counter[blockY - 1][blockX] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if b and g:
            self.States[blockY - 1][blockX] = 8
            self.Counter[blockY - 1][blockX] = 0
            self.States[blockY + 1][blockX] = 8
            self.Counter[blockY + 1][blockX] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if c and d:
            self.States[blockY][blockX - 2] = 8
            self.Counter[blockY][blockX - 2] = 0
            self.States[blockY][blockX - 1] = 8
            self.Counter[blockY][blockX - 1] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if d and e:
            self.States[blockY][blockX - 1] = 8
            self.Counter[blockY][blockX - 1] = 0
            self.States[blockY][blockX + 1] = 8
            self.Counter[blockY][blockX + 1] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if e and f:
            self.States[blockY][blockX + 2] = 8
            self.Counter[blockY][blockX + 2] = 0
            self.States[blockY][blockX + 1] = 8
            self.Counter[blockY][blockX + 1] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if g and h:
            self.States[blockY + 2][blockX] = 8
            self.Counter[blockY + 2][blockX] = 0
            self.States[blockY + 1][blockX] = 8
            self.Counter[blockY + 1][blockX] = 0
            self.States[blockY][blockX] = 8
            self.Counter[blockY][blockX] = 0
            result = True
        if result:
            if blockState == 7 or blockState == 2:
                if not self.isChainFirstBlock:
                    if 0 <= self.ChainCount < 14:
                        self.ChainCount += 1
                self.isChain = True
                self.isChainFirstBlock = True
            self.popBlocksSoundPlay = True
        return result
    
    # Private
    # Descr:  Handles changing between two visual states of the pointer
    # Before: Nothing
    # After:  changes visual state if pointer counter is zero and sets pointer counter to 15,
    #         else subtracts one from pointer counter
    def __MakePointerTick(self):
        if self.pointerCount == 0:
            self.pointerTick = not self.pointerTick
            self.pointerCount = 15
            self.RedrawBoard = True
        else:
            self.pointerCount -= 1
    
    # Private
    # Descr:  Subtracts one from values greater than zero in the Counter matrix
    # Before: Nothing
    # After:  all values greater than zero in the Counter matrix have been subtracted by one
    def __CounterSubtractOne(self):
        for y in range(12):
            for x in range(6):
                if self.Counter[y][x] > 0:
                    self.Counter[y][x] -= 1
    
    # Private
    # Descr:  Counts blocks in the between state 8, and setus up a new pop accoringly
    # Before: Nothing
    # After:  see description
    def __SetupNewPops(self):
        n = 0 # number of pops
        for y in range(12):
            for x in range(6):
                if self.States[y][x] == 8:
                    n = n + 1
        if n > 0:
            k = 0 # pop number
            for y in range(12):
                for x in range(6):
                    if self.States[11 - y][x] == 8:
                        if k == 0 and n > 3:
                            self.ComboNote[11 - y][x] = n
                            self.ComboNoteCounter[11 - y][x] = 40
                            if n == 4:
                                self.__AddToScore(20)
                            elif n == 5:
                                self.__AddToScore(25)
                            elif n == 6:
                                self.__AddToScore(40)
                            elif n == 7:
                                self.__AddToScore(55)
                            elif n == 8:
                                self.__AddToScore(70)
                            elif n == 9:
                                self.__AddToScore(85)
                            elif n == 10:
                                self.__AddToScore(100)
                            elif n == 11:
                                self.__AddToScore(120)
                            elif n == 12:
                                self.__AddToScore(140)
                            elif n == 13:
                                self.__AddToScore(160)
                            elif n == 14:
                                self.__AddToScore(180)
                            elif n == 15:
                                self.__AddToScore(200)
                            elif n == 16:
                                self.__AddToScore(220)
                            elif n == 17:
                                self.__AddToScore(250)
                            elif n == 18:
                                self.__AddToScore(300)
                            elif n == 19:
                                self.__AddToScore(350)
                            elif n == 20:
                                self.__AddToScore(400)
                            elif n == 21:
                                self.__AddToScore(450)
                            elif n == 22:
                                self.__AddToScore(500)
                            elif n == 23:
                                self.__AddToScore(550)
                            elif n == 24:
                                self.__AddToScore(600)
                            elif n == 25:
                                self.__AddToScore(700)
                            elif n == 26:
                                self.__AddToScore(800)
                            elif n == 27:
                                self.__AddToScore(900)
                            elif n == 28:
                                self.__AddToScore(1000)
                            elif n == 29:
                                self.__AddToScore(1100)
                            elif n == 30:
                                self.__AddToScore(1200)
                            elif n == 31:
                                self.__AddToScore(1300)
                            elif n == 32:
                                self.__AddToScore(1400)
                            elif n == 33:
                                self.__AddToScore(1500)
                            elif n == 34:
                                self.__AddToScore(1600)
                            elif n == 35:
                                self.__AddToScore(1800)
                            elif n > 35:
                                self.__AddToScore(2000)
                        self.PopStateCounter1[11 - y][x] = 16 + k*8
                        self.PopStateCounter2[11 - y][x] = (n - k)*8
                        k = k + 1
            self.RedrawBoard = True
        for y in range(12):
            for x in range(6):
                if self.ComboNoteCounter[11 - y][x] > 0:
                    self.ComboNoteCounter[11 - y][x] -= 1
                else:
                    self.ComboNote[11 - y][x] = 0
                if self.ChainNoteCounter[11 - y][x] > 0:
                    self.ChainNoteCounter[11 - y][x] -= 1
                else:
                    self.ChainNote[11 - y][x] = 0
                if self.isChain and self.States[11 - y][x] == 8:
                    self.ChainMarks[11 - y][x] = True
                if self.isChainFirstBlock and self.States[11 - y][x] == 8:
                    self.ChainNote[11 - y][x] = self.ChainCount
                    if self.ChainCount == 1:
                        self.__AddToScore(50)
                    elif self.ChainCount == 2:
                        self.__AddToScore(80)
                    elif self.ChainCount == 3:
                        self.__AddToScore(150)
                    elif self.ChainCount == 4:
                        self.__AddToScore(300)
                    elif self.ChainCount == 5:
                        self.__AddToScore(450)
                    elif self.ChainCount == 6:
                        self.__AddToScore(600)
                    elif self.ChainCount == 7:
                        self.__AddToScore(800)
                    elif self.ChainCount == 8:
                        self.__AddToScore(1000)
                    elif self.ChainCount == 9:
                        self.__AddToScore(1200)
                    elif self.ChainCount == 10:
                        self.__AddToScore(1450)
                    elif self.ChainCount == 11:
                        self.__AddToScore(1700)
                    elif self.ChainCount == 12:
                        self.__AddToScore(2000)
                    elif self.ChainCount == 13:
                        self.__AddToScore(2400)
                    elif self.ChainCount == 14:
                        self.__AddToScore(2500)
                    self.ChainNoteCounter[11 - y][x] = 40
                    self.isChainFirstBlock = False
        for y in range(12):
            for x in range(6):
                if self.States[y][x] == 8:
                    self.States[y][x] = 9
    
    # Private
    # Descr:  If requirements for a chain were not fulfilled in last cycle this function does nothing (if isChain is False function does nothing)
    #         Else: Checks if requirements for a chain are still fulfilled, if not it sets isChain to False
    # Before: Nothing
    # After:  see description
    def __CheckChainConditions(self):
        if self.isChain or self.ChainCount != 0: # ChainCount checked as a precaution, most likely not required
            if all(all(x == False for x in self.ChainMarks[y]) for y in range(12)):
                if all(all((x != 2 and x != 7) for x in self.States[y]) for y in range(12)):
                    self.isChain = False
                    self.ChainCount = 0
    
    # Private
    # Descr:  Handles state changes for falling blocks and popping blocks
    # Before: Nothing
    # After:  see description
    def __PopAndFallHandling(self):
        for x in range(6):
            for y in range(12):
                if self.Blocks[y][x] != 0 and self.Counter[y][x] == 0:
                    if self.States[y][x] == 4:
                        self.__Fall(y,x,4)
                    elif self.States[y][x] == 5:
                        self.__Fall(y,x,5)
                    elif self.States[y][x] == 6:
                        self.__Fall(y,x,6)
                    elif self.States[y][x] == 7:
                        self.__Fall(y,x,7)
                    elif self.States[y][x] == 1:
                        self.__Fall(y,x,1)
                    elif self.States[y][x] == 2:
                        self.__Fall(y,x,2)
                    elif self.States[y][x] == 3:
                        self.States[y][x] = 0 # block has finished bouncing after landing and state becomes idle
                if self.States[y][x] == 9:
                    if self.Counter[y][x] == 0:
                        if self.PopStates[y][x] < 38:
                            if self.PopStates[y][x]%2 == 0:
                                self.Counter[y][x] = 1
                            else:
                                self.Counter[y][x] = 2
                            self.PopStates[y][x] += 1
                        elif self.PopStates[y][x] == 38:
                            if self.PopStateCounter1[y][x] == 0:
                                self.PopStates[y][x] += 1
                                self.Counter[y][x] = 3
                            else:
                                self.PopStateCounter1[y][x] -= 1
                        elif self.PopStates[y][x] == 39:
                            self.PopStates[y][x] = 40
                            self.Counter[y][x] = 2
                        elif self.PopStates[y][x] == 40:
                            self.PopStates[y][x] = 41
                            self.Counter[y][x] = 2
                            self.__AddToScore(10)
                        elif 40 < self.PopStates[y][x] < 48:
                            self.PopStates[y][x] += 1
                            self.Counter[y][x] = 1
                        elif self.PopStates[y][x] == 48:
                            self.PopStates[y][x] = 49
                            self.Counter[y][x] = 2
                        elif self.PopStates[y][x] == 49:
                            self.PopStates[y][x] = 50
                            self.Counter[y][x] = 1
                        elif self.PopStates[y][x] == 50:
                            self.PopStates[y][x] = 51
                            self.Counter[y][x] = 1
                        elif self.PopStates[y][x] == 51:
                            self.PopStates[y][x] = 52
                            self.Counter[y][x] = 2
                        elif self.PopStates[y][x] == 52:
                            self.PopStates[y][x] = 53
                            self.Counter[y][x] = 1
                        elif self.PopStates[y][x] == 53:
                            self.PopStates[y][x] = 54
                            self.Counter[y][x] = 4
                        elif self.PopStates[y][x] == 54:
                            self.PopStates[y][x] = 55
                            self.Counter[y][x] = 4
                        elif self.PopStates[y][x] == 55:
                            self.PopStates[y][x] = 56
                        elif self.PopStates[y][x] == 56:
                            if self.PopStateCounter2[y][x] == 0:
                                self.Blocks[y][x] = 0
                                self.States[y][x] = 0
                                self.ChainMarks[y][x] = False
                                self.PopStates[y][x] = 0
                                if y < 11 and self.Blocks[y+1][x] != 0:
                                    if self.States[y+1][x] == 0 or self.States[y+1][x] == 3:
                                        self.States[y+1][x] = 6
                                        self.Counter[y+1][x] = 12
                            else:
                                self.PopStateCounter2[y][x] -= 1
                        self.RedrawBoard = True
    
    # Private
    # Descr:  Handles elevating the board when appropriate
    # Before: Nothing
    # After:  see description
    def __ElevationHandling(self):
        if not self.swap and all(all(x == 0 for x in self.States[y]) for y in range(12)): # if not swapping and no pops or drops in progress
            if self.ElevateCounter == 0 or self.ElevatePress:
                self.ElevateCounter = 30
                if self.Elevation < 19:
                    self.Elevation += 1
                else:
                    self.Elevation = 0
                    self.__ElevateBoard()
                    for x in range(6):
                        self.__CheckForPop(0,x)
                    if self.pointerY < 11:
                        self.pointerY += 1
                self.RedrawBoard = True
            else:
                self.ElevateCounter -= 1
        if (self.ElevateCounter == 1 or self.ElevatePress) and self.pointerY == 11:
            self.pointerY -= 1
    
    # Private
    # Descr:  Moves blocks one step up in the Blocks matrix
    # Before: Nothing
    # After:  see description
    def __ElevateBoard(self):
        for y in range(11):
            self.Blocks[11-y] = self.Blocks[10-y] # swapping inner lists, should be rather inexpensive
        self.Blocks[0] = list(self.NewBlocks) # copy blocks from NewBlocks into bottom shelf of the board
        self.__MakeNewBlocks()
        self.__AddToScore(1)
    
    # Functions to be executed in a tick
    def BoardTick(self):
        self.__CheckChainConditions()
        self.__MakePointerTick()
        self.__CounterSubtractOne()
        self.__ElevationHandling()
        self.__PopAndFallHandling()
        self.__SetupNewPops()
        self.__SwapHandling()
        if self.swap:
            self.RedrawBoard = True
    

