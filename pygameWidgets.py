# pygame widgets
# Button: class for creating an interactive button object that performs functions when clicked
# Card: class for creating an interactive card object that can be clicked and unclicked
# Deck: class for creating a container of a bunch of cards, while recording what each card is
# Player: class for creating a player avatar object that can be used to distinguish professor and student

import pygame

class Button():
    def __init__(self,screen, x, y, width, height, buttonText='Button', onclickFunction=lambda : 1, onePress=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        font = pygame.font.SysFont('Arial', 16)

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)
        pygame.draw.rect(self.screen, (0,0,0), self.buttonRect, 2)

class Card:
    def __init__(self,screen, cardType, x, y, width, height, onclickFunction=lambda : 1,cancelFuction=lambda : 1):
        self.screen = screen
        self.cardType = cardType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.cancelFunction = cancelFuction
        self.pressedCnt = 0
        self.newY = {
            'normal': self.y,
            'hover': self.y-2,
            'pressed': self.y-5,
        }
        self.cardImg = pygame.image.load(f"./imgs/pokers/{self.cardType}.png")
        self.cardImg = pygame.transform.scale(self.cardImg, (self.width, self.height))
        self.cardImg.convert()
        self.cardSurface = pygame.Surface((self.width, self.height))
        self.cardRect = pygame.Rect(self.x, self.y, self.width, self.height)
    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.cardRect.collidepoint(mousePos):
            self.cardRect = pygame.Rect(self.x,self.newY['hover'],self.width, self.height)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.pressedCnt = (self.pressedCnt+1)%2
                if self.pressedCnt == 1:
                    self.onclickFunction()
                else:
                    self.cancelFunction()
        if self.pressedCnt == 1:
            self.cardRect = pygame.Rect(self.x,self.newY['pressed'],self.width, self.height)
        else:
            self.cardRect = pygame.Rect(self.x, self.newY['normal'], self.width, self.height)
        self.cardSurface.blit(self.cardImg, [
            self.cardRect.width/2 - self.cardSurface.get_rect().width/2,
            self.cardRect.height/2 - self.cardSurface.get_rect().height/2
        ])
        self.screen.blit(self.cardSurface, self.cardRect)
        pygame.draw.rect(self.screen, (0,0,0), self.cardRect, 2)

class Player:
    def __init__(self,screen,playerObj, x, y, width, height,assignedIdentity=False):
        self.player = playerObj
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        font = pygame.font.SysFont('Arial', 16)
        self.playerSurface = pygame.Surface((self.width, self.height))
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if assignedIdentity:
            if self.player.identity == 's':
                self.playerSurf = font.render(self.player.name, True, (81, 4, 0))
            else:
                self.playerSurf = font.render(self.player.name, True, (2, 7, 93))
        else:
            self.playerSurf = font.render(self.player.name, True, (80, 80, 80))
    def process(self):
        self.playerSurface.blit(self.playerSurf, [
            self.playerRect.width/2 - self.playerSurf.get_rect().width/2,
            self.playerRect.height/2 - self.playerSurf.get_rect().height/2
        ])
        self.screen.blit(self.playerSurface, self.playerRect)