import pygame
import TextureLoader
import DrawHelper

class MovingBot:
    def __init__(self, north, east, south, west, x, y):
        self.north = north
        self.image = north
        self.east = east
        self.south = south
        self.west = west
        self.x = x
        self.y = y
        # 0 - north, 1 - east, 2 - south, 3 - west
        self.direction = 0
        self.xCoordinate = 4
        self.yCoordinate = 4

    # executes the passed in commands one by one
    def executeCommand(self,command):
        options = {
            'forward' : self.goForward,
            'turnleft' : self.turnLeft,
            'turnright' : self.turnRight,
        }
        # calls the correct function
        options[command]()
        self.updateDirection()

    def draw(self, screen):
        DrawHelper.drawCoor(screen,self.image,self.x,self.y)

    def updateDirection(self):
        if(self.direction == 0):
            self.image = self.north
        elif(self.direction == 1):
            self.image = self.east
        elif(self.direction == 2):
            self.image = self.south
        elif(self.direction == 3):
            self.image = self.west       

    def goForward(self):
        if(self.direction == 0):
            self.y -= 50
            self.yCoordinate -= 1
        if(self.direction == 1):
            self.x += 50
            self.xCoordinate += 1
        if(self.direction == 2):
            self.y += 50
            self.yCoordinate += 1
        if(self.direction == 3):
            self.x -= 50
            self.yCoordinate -= 1

    def turnLeft(self):
        self.direction -= 1
        if(self.direction < 0):
            self.direction = 3

    def turnRight(self):
        self.direction += 1
        if(self.direction > 3):
            self.direction = 0

    def reset(self):
        self.direction = 0
        self.x = 291
        self.y = 300
        self.xCoordinate = 4
        self.yCoordinate = 4
        self.updateDirection()