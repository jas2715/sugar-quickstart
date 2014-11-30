import pygame
import TextureLoader
import DrawHelper
import MouseMethodHelper
import math
import os
from GameTile import GameTile
from MovingBot import MovingBot

tileImages = []
tiles = []

class GameScreen:
    # Load all of the textures, fonts, titles, etc.
    def __init__(self):
        self.bgImage = TextureLoader.load(os.path.join('assets', 'game-bg.png'), (800,600))
        self.botImage = TextureLoader.load(os.path.join('assets', 'bot.png'), (37,49))
        self.mainImage = TextureLoader.load(os.path.join('assets', 'main.png'), (151,151))
        self.funcImage = TextureLoader.load(os.path.join('assets', 'func.png'), (151,101))
        self.goButton = TextureLoader.load(os.path.join('assets', 'button-go.png'), (69,27))
        self.clearButton = TextureLoader.load(os.path.join('assets', 'button-clear.png'), (69,27))

        self.botRunning = False
        self.currentCommand = 0
        self.commands = []

        self.bot = MovingBot(self.botImage, 91, 100)

        # Load tile images
        for i in range(0, 5):
            tileImages.append(TextureLoader.load(os.path.join('assets', 'tile' + str(i+1) + '.png'), (47,47) ))
        # constant for keeping track of tile width and spawner placement
        self.TILEWIDTH = 47;

        # The selected tile is the one being dragged
        self.selectedTile = None

        # The two grids - represented by 2d arrays 
        self.mainMethod = [[0 for x in range(3)] for x in range(3)] 
        self.secondaryMethod = [[0 for x in range(2)] for x in range(3)]

        # Two sizes of the same font to use
        self.titleFont =  pygame.font.SysFont('ActionIsShaded', 48)
        self.labelFont = pygame.font.SysFont('ActionIsShaded', 24)

    # Update the game logic
    def update(self):
        if self.selectedTile:
            self.selectedTile.move(self.mouseX,self.mouseY,self.TILEWIDTH);

        # Move Robobuddy
        if self.botRunning:
            cmd = self.commands[self.currentCommand]
            print(self.commands)
            if(cmd == "grab"):
                #add the current number the robot is standing on to the equation
            elif(cmd == "function"):
                #run the commands from the secondary function
            elif(cmd == "turnleft" or cmd == "turnright" or cmd == "forward"):
                self.bot.executeCommand(cmd)

    # Spawns a new tile, moves a current one, clears the methods, or compiels the methods
    def pressMouse(self):
        # Wont even bother to check for collision unless the player is clicking on the right side of the screen
        # Trades a few extra lines for a little bit of optimization
        if(self.mouseX > 500):
            # Is the user clicking an already placed tile
            for t in tiles:
                if((self.mouseX > t.x and self.mouseX < t.x+self.TILEWIDTH) and (self.mouseY > t.y and self.mouseY < t.y+self.TILEWIDTH)):
                        self.selectedTile = t
                        self.removeFromGrid(self.selectedTile.gridX,self.selectedTile.gridY,self.selectedTile.grid)
                        return

            # Is the user is clicking on a tile spawner
            tempX = 550
            actions = ["forward","turnleft","turnright","function","grab"]
            for i in range(0,5):
                if((self.mouseX > tempX and self.mouseX < tempX+self.TILEWIDTH) and (self.mouseY > 500 and self.mouseY < 500+self.TILEWIDTH)):
                    self.selectedTile = GameTile(tileImages[i], self.mouseX, self.mouseY, actions[i])
                    tiles.append(self.selectedTile)
                    return
                tempX += 50

            # Is the user clicking on the Clear button?
            tempX = 599
            tempY = 420
            if(self.mouseX > tempX) and (self.mouseX < tempX + 69) and (self.mouseY > tempY) and (self.mouseY < tempY + 69):
                # Clear tiles and grids
                global tiles
                tiles = []
                for i in range(0, 3):
                    for j in range(0, 3):
                        self.removeFromGrid(i,j,"main")
                for i in range(0, 3):
                    for j in range(0, 2):
                        self.removeFromGrid(i,j,"secondary")
                return

            # Is the user clicking on the Go button?
            tempX = 682
            if(self.mouseX > tempX) and (self.mouseX < tempX + 69) and (self.mouseY > tempY) and (self.mouseY < tempY + 69):

                if not self.botRunning:
                    # Start the run process
                    self.botRunning = True

                    #http://stackoverflow.com/questions/24591917/nested-loop-python

                    #We need to work a nested for loop in here so we can get the filtered array of commands

                    # Build list of commands
                    #self.commands = []
                    #for i in self.mainMethod:
                    #    for j in self.mainMethod[i]:
                            # Grab the commands that exist from the grid
                    #        if self.mainMethod[i][j] != 0:
                    #            self.commands.append(self.mainMethod[i][j])
                    
                    #for cell in self.mainMethod:
                    #    if cell != 0:
                    #        self.commands.append(cell)
                    #FIX COMMANDS TO BE ONLY THE GOOD STUFF

                    # TODO: include the "F" in here somehow
                return

    # The mouse button was released and a tile is selected. kill whatever isn't in an appropriate location
    def releaseMouse(self):
        if(self.selectedTile != None):
            # if the mouse is released somewhere inside the main grid (hardcoded coords for grid)
            if((self.mouseX > 600 and self.mouseX < 600+151) and (self.mouseY > 120 and self.mouseY < 120+151)):
                MouseMethodHelper.releaseInMainGrid(self.mouseX,self.mouseY,self.selectedTile,self.mainMethod,tiles)
                self.logInfoForTesting()
                return
            # if the mouse is released somewhere inside the secondary function grid (again, hardcoded)
            if((self.mouseX > 600 and self.mouseX < 600+151) and (self.mouseY > 300 and self.mouseY < 300+101)):
                MouseMethodHelper.releaseInSecondaryGrid(self.mouseX,self.mouseY,self.selectedTile,self.secondaryMethod,tiles)
                self.logInfoForTesting()
                return
            #removes the tile from existance if it wasn't dropped on a grid
            tiles.remove(self.selectedTile)
            self.logInfoForTesting()

    # Removes a tiles influence on its respective grid
    def removeFromGrid(self,xCord,yCord,grid):
        if(grid == None):
            return
        elif(grid == "main"):
            self.mainMethod[xCord][yCord] = 0
            return
        elif(grid == "secondary"):
            self.secondaryMethod[xCord][yCord] = 0
            return

    # Self explanatory...
    def logInfoForTesting(self):
        print("Total tiles: ", len(tiles))
        print("Main List of Commands: ")
        for i in range(3):
            for j in range(3):
                print '{:3}'.format(self.mainMethod[j][i]),
            print
        print("Secondary List of Commands:")
        for i in range(2):
            for j in range(3):
                print '{:3}'.format(self.secondaryMethod[j][i]),
            print

    # Draw all screen elements here!
    def draw(self, screen):
    	if screen != 0:
            # Images
            DrawHelper.drawAspect(screen,self.bgImage, 0,0)
            DrawHelper.drawAspect(screen,self.mainImage, 0.75,0.2)
            DrawHelper.drawAspect(screen,self.funcImage, 0.75,0.5)
            #DrawHelper.drawAspect(screen,self.botImage, 0.365,0.835)
            self.bot.draw(screen)

             # Text blocks
            title1 = self.titleFont.render("Robobuddy", 1, (10,10,10))
            title1pos = title1.get_rect()
            title1pos.centerx = 675
            title1pos.centery = 50
            screen.blit(title1, title1pos)

            labelMain = self.labelFont.render("main:", 1, (10,10,10))
            labelFunc = self.labelFont.render("f:", 1, (10,10,10))
            mainPos = labelMain.get_rect()
            funcPos = labelFunc.get_rect()
            mainPos.centerx = 570
            funcPos.centerx = 585
            mainPos.centery = 140
            funcPos.centery = 325
            screen.blit(labelMain, mainPos)
            screen.blit(labelFunc, funcPos)

            labelEq = self.labelFont.render("<insert equation here>", 1, (10,10,10))
            eqPos = labelEq.get_rect()
            eqPos.centerx = 200
            eqPos.centery = 50
            screen.blit(labelEq, eqPos)

            # Buttons
            DrawHelper.drawCoor(screen,self.goButton,682, 420)
            DrawHelper.drawCoor(screen,self.clearButton,599, 420)

            # Draw the tile spawners (just images) with a 3 pixel gap
            for i in range(0, 5):
                DrawHelper.drawCoor(screen,tileImages[i],(550 + i*(self.TILEWIDTH+3)),500)
            # Draw any dragged out tiles
            for t in tiles:
                t.draw(screen)