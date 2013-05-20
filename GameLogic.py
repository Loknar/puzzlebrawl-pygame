## Puzzle Brawl (a Puzzle Attack / Panel De Pon / Puzzle Challenge clone)
## "Swap and Match" tile-based puzzle gameplay style
## http://www.notendur.hi.is/sfg6/puzzlebrawl/
## By Sveinn Floki Gudmundsson - svefgud@gmail.com

INERTIA = 16 # the time it takes for block to start falling

import random

class PuzzleBrawlBoard:
    def __init__(self):
        self.hiscore = 0
        self.score = 0
        self.speedlvl = 1
        
        # True if board needs to be redrawn, else False
        self.RedrawBoard = True
        
        # True if certain sounds need to be played, else False
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
        self.MakeNewBlocks()
        
        # Couple of 12x6 matrices for storing state of the board
        # Note: perhaps using something else than lists could be better for performance
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
    
    # Adds n to current score
    def AddToScore(self, n):
        self.score += n
        self.RedrawBoard = True
    
    # Creates new blocks that are to spawn from bottom of the board
    def MakeNewBlocks(self):
        for x in range(6):
            self.NewBlocks[x] = random.randint(1,6)
            if x > 1:
                while self.NewBlocks[x] == self.NewBlocks[x-1] == self.NewBlocks[x-2]:
                    self.NewBlocks[x] = random.randint(1,6)
    
    # Moves pointer up
    def MovePointerUp(self):
        if self.pointerY < 10 or (self.pointerY == 10 and self.Elevation == 0):
            self.pointerY += 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Moves pointer down
    def MovePointerDown(self):
        if self.pointerY > 0:
            self.pointerY -= 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Moves pointer to the right
    def MovePointerRight(self):
        if self.pointerX < 4:
            self.pointerX += 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Moves pointer to the left
    def MovePointerLeft(self):
        if self.pointerX > 0:
            self.pointerX -= 1
            self.movePointerSoundPlay = True
            self.RedrawBoard = True
    
    # Starts a swap if there isn't one going on
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
                self.Counter[self.swapY][self.swapX] = INERTIA + 5 # plus frames until PointerSwapFinish is called
            if self.Blocks[self.swapY-1][self.swapX+1] == 0:
                self.States[self.swapY][self.swapX+1] = 4
                self.Counter[self.swapY][self.swapX+1] = INERTIA + 5 # plus frames until PointerSwapFinish is called
        self.SwitchBlocks(self.swapY, self.swapX, self.swapY, self.swapX + 1)
        if self.Blocks[self.swapY][self.swapX] == 0:
            self.States[self.swapY][self.swapX] = 0
        elif self.Blocks[self.swapY][self.swapX+1] == 0:
            self.States[self.swapY][self.swapX+1] = 0
        self.swapBlocksSoundPlay = True
    
    # When swap finishes this function is called to finish the deal
    def PointerSwapFinish(self):
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
            self.CheckForPop(self.swapY,self.swapX)
        if self.Blocks[self.swapY][self.swapX+1] != 0 and self.States[self.swapY][self.swapX+1] == 0:
            self.CheckForPop(self.swapY,self.swapX+1)
        self.swap = False
    
    # Help function for swapping places of two blocks
    def SwitchBlocks(self, Y1, X1, Y2, X2):
        self.Blocks[Y1][X1], self.Blocks[Y2][X2] = self.Blocks[Y2][X2], self.Blocks[Y1][X1]
    
    # Handles making blocks fall
    def Fall(self, y, x, state):
        if y > 0:
            if self.Blocks[y-1][x] == 0:
                self.SwitchBlocks(y, x, y - 1, x)
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
                if not self.CheckForPop(y,x):
                    self.States[y][x] = 3
                    self.Counter[y][x] = 3
        else:
            if not self.CheckForPop(y,x):
                self.States[y][x] = 3
                self.Counter[y][x] = 3
        self.RedrawBoard = True
    
    # Checks if a block fulfills requirements for popping and if so, changes the state of the board accordingly
    # Returns True if pop happened, else False
    def CheckForPop(self, blockY, blockX):
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
    
    # Checks if a block is in loose air and if so, changes state of the board accordingly
    def CheckForDrop(self, blockY, blockX):
        result = False
        if self.States[blockY][blockX] > 2 or self.Blocks[blockY][blockX] == 0:
            return result
        if blockY < 11:
            if self.Blocks[blockY + 1][blockX] == 0:
                self.States[blockY][blockX] = 3
                self.Counter[blockY][blockX] = 7
                result = True
        return result
    
    # Handles changing between tvisual states of the pointer
    def MakePointerTick(self):
        if self.pointerCount == 0:
            self.pointerTick = not self.pointerTick
            self.pointerCount = 15
            self.RedrawBoard = True
        else:
            self.pointerCount -= 1
    
    # Subtracts one from values greater than zero in the Counter matrix
    def CounterSubtractOne(self):
        for y in range(12):
            for x in range(6):
                if self.Counter[y][x] > 0:
                    self.Counter[y][x] -= 1
    
    # Counts blocks in the between state 8, and setus up a new pop accoringly
    def SetupNewPops(self):
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
                                self.AddToScore(20)
                            elif n == 5:
                                self.AddToScore(25)
                            elif n == 6:
                                self.AddToScore(40)
                            elif n == 7:
                                self.AddToScore(55)
                            elif n == 8:
                                self.AddToScore(70)
                            elif n == 9:
                                self.AddToScore(85)
                            elif n == 10:
                                self.AddToScore(100)
                            elif n == 11:
                                self.AddToScore(120)
                            elif n == 12:
                                self.AddToScore(140)
                            elif n == 13:
                                self.AddToScore(160)
                            elif n == 14:
                                self.AddToScore(180)
                            elif n == 15:
                                self.AddToScore(200)
                            elif n == 16:
                                self.AddToScore(220)
                            elif n == 17:
                                self.AddToScore(250)
                            elif n == 18:
                                self.AddToScore(300)
                            elif n == 19:
                                self.AddToScore(350)
                            elif n == 20:
                                self.AddToScore(400)
                            elif n == 21:
                                self.AddToScore(450)
                            elif n == 22:
                                self.AddToScore(500)
                            elif n == 23:
                                self.AddToScore(550)
                            elif n == 24:
                                self.AddToScore(600)
                            elif n == 25:
                                self.AddToScore(700)
                            elif n == 26:
                                self.AddToScore(800)
                            elif n == 27:
                                self.AddToScore(900)
                            elif n == 28:
                                self.AddToScore(1000)
                            elif n == 29:
                                self.AddToScore(1100)
                            elif n == 30:
                                self.AddToScore(1200)
                            elif n == 31:
                                self.AddToScore(1300)
                            elif n == 32:
                                self.AddToScore(1400)
                            elif n == 33:
                                self.AddToScore(1500)
                            elif n == 34:
                                self.AddToScore(1600)
                            elif n == 35:
                                self.AddToScore(1800)
                            elif n > 35:
                                self.AddToScore(2000)
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
                        self.AddToScore(50)
                    elif self.ChainCount == 2:
                        self.AddToScore(80)
                    elif self.ChainCount == 3:
                        self.AddToScore(150)
                    elif self.ChainCount == 4:
                        self.AddToScore(300)
                    elif self.ChainCount == 5:
                        self.AddToScore(450)
                    elif self.ChainCount == 6:
                        self.AddToScore(600)
                    elif self.ChainCount == 7:
                        self.AddToScore(800)
                    elif self.ChainCount == 8:
                        self.AddToScore(1000)
                    elif self.ChainCount == 9:
                        self.AddToScore(1200)
                    elif self.ChainCount == 10:
                        self.AddToScore(1450)
                    elif self.ChainCount == 11:
                        self.AddToScore(1700)
                    elif self.ChainCount == 12:
                        self.AddToScore(2000)
                    elif self.ChainCount == 13:
                        self.AddToScore(2400)
                    elif self.ChainCount == 14:
                        self.AddToScore(2500)
                    self.ChainNoteCounter[11 - y][x] = 40
                    self.isChainFirstBlock = False
        for y in range(12):
            for x in range(6):
                if self.States[y][x] == 8:
                    self.States[y][x] = 9
    
    # If requirements for a chain were not fulfilled in last cycle this function does nothing (if isChain is False function does nothing)
    # Else: Checks if requirements for a chain are still fulfilled, if not it sets isChain to False
    def CheckChainConditions(self):
        if self.isChain or self.ChainCount != 0: # ChainCount checked as a precaution, possibly not required
            if all(all(x == False for x in self.ChainMarks[y]) for y in range(12)):
                if all(all((x != 2 and x != 7) for x in self.States[y]) for y in range(12)):
                    self.isChain = False
                    self.ChainCount = 0
    
    # Handles state changes for falling blocks and popping blocks
    def PopAndFallHandling(self):
        for x in range(6):
            for y in range(12):
                if self.Blocks[y][x] != 0 and self.Counter[y][x] == 0:
                    if self.States[y][x] == 4:
                        self.Fall(y,x,4)
                    elif self.States[y][x] == 5:
                        self.Fall(y,x,5)
                    elif self.States[y][x] == 6:
                        self.Fall(y,x,6)
                    elif self.States[y][x] == 7:
                        self.Fall(y,x,7)
                    elif self.States[y][x] == 1:
                        self.Fall(y,x,1)
                    elif self.States[y][x] == 2:
                        self.Fall(y,x,2)
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
                            self.AddToScore(10)
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
    
    # Counts down state of the swap and when the swap is over PointerSwapFinish() is called to seal the deal
    def SwapHandling(self):
        if self.swap:
            if self.swapCounter > 0:
                self.swapCounter -= 1
            else:
                self.PointerSwapFinish()
    
    # Handles elevating the board when appropriate
    def ElevationHandling(self):
        if not self.swap and all(all(x == 0 for x in self.States[y]) for y in range(12)): # if not swapping and no pops or drops in progress
            if self.ElevateCounter == 0 or self.ElevatePress:
                self.ElevateCounter = 30
                if self.Elevation < 19:
                    self.Elevation += 1
                else:
                    self.Elevation = 0
                    self.ElevateBoard()
                    for x in range(6):
                        self.CheckForPop(0,x)
                    if self.pointerY < 11:
                        self.pointerY += 1
                self.RedrawBoard = True
            else:
                self.ElevateCounter -= 1
        if (self.ElevateCounter == 1 or self.ElevatePress) and self.pointerY == 11:
            self.pointerY -= 1
    
    # Moving blocks one step up in the Blocks matrix
    def ElevateBoard(self):
        for y in range(11):
            self.Blocks[11-y] = self.Blocks[10-y] # swapping inner lists, should be rather inexpensive
        self.Blocks[0] = list(self.NewBlocks) # copy blocks from NewBlocks into bottom shelf of the board
        self.MakeNewBlocks()
        self.AddToScore(1)
    
    # Functions to be executed in a tick
    def BoardTick(self):
        self.CheckChainConditions()
        self.MakePointerTick()
        self.CounterSubtractOne()
        self.ElevationHandling()
        self.PopAndFallHandling()  # Note to self:
        self.SetupNewPops()        # swapped these two because of isChain
        self.SwapHandling()
        if self.swap:
            self.RedrawBoard = True
    
    