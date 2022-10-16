# pygame widgets
# Button: class for creating an interactive button object that performs functions when clicked
# Card: class for creating an interactive card object that can be clicked and unclicked
# Deck: class for creating a container of a bunch of cards, while recording what each card is
# Player: class for creating a player avatar object that can be used to distinguish professor and student

import pygame

class Button():
    def __init__(self,screen, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        font = pygame.font.SysFont('Arial', 40)

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

class Card:
    def __init__(self,screen, cardType, x, y, width, height, onclickFunction=None):
        self.screen = screen
        self.cardType = cardType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.cardImg = pygame.image.load(f"./imgs/pokers/{self.cardType}.img")
        self.cardImg.convert()
        self.cardSurface = pygame.Surface((self.width, self.height))
        self.cardRect = pygame.Rect(self.x, self.y, self.width, self.height)
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.cardSurface.fill(self.fillColors['normal'])
        if self.cardRect.collidepoint(mousePos):
            self.cardSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.cardSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.cardSurface.blit(self.cardImg, [
            self.cardRect.width/2 - self.cardSurface.get_rect().width/2,
            self.cardRect.height/2 - self.cardSurface.get_rect().height/2
        ])
        self.screen.blit(self.cardSurface, self.cardRect)

class Player:
    def __init__(self,screen,playerObj, x, y, width, height):
        self.player = playerObj
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        font = pygame.font.SysFont('Arial', 40)
        self.playerSurface = pygame.Surface((self.width, self.height))
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.player.identity == 's':
            self.playerSurf = font.render(self.player.name, True, (81, 4, 0))
        else:
            self.playerSurf = font.render(self.player.name, True, (2, 7, 93))
    def process(self):
        self.playerSurface.blit(self.playerSurf, [
            self.playerRect.width/2 - self.playerSurf.get_rect().width/2,
            self.playerRect.height/2 - self.playerSurf.get_rect().height/2
        ])
        self.screen.blit(self.handSurface, self.handRect)