# GUI
# loginGUI: class for logging into the server and going to mainGUI
# mainGUI: class for choosing players and go to gameGUI
# gameGUI: class for the visualization of gaming

import tkinter
import pygame
from pygameWidgets import *
from GameEngine import *


class gameGUI:
    def __init__(self,Game):
        self.width = 800
        self.height = 600
        self.fps = 20
        self.title = "Fight the Professor! By Eric Gao"
        self.bgColor = (255,255,255)
        self.Game = Game
        self.objs = []
        self.chosenLandlord = False
        pygame.init()
        self.run()
    def decodeGame(self,gameInfo):
        newGame = Game(gameInfo[1],gameInfo[4],gameInfo[7])
        newGame.p1.identity = gameInfo[2]
        newGame.p2.identity = gameInfo[5]
        newGame.p3.identity = gameInfo[8]
        newGame.p1.cards = gameInfo[3]
        newGame.p1.cards = gameInfo[6]
        newGame.p1.cards = gameInfo[9]
        newGame.currentPlayer = gameInfo[10]
        newGame.prevPlay = gameInfo[11]
        newGame.playOrder = gameInfo[12]
        return newGame
    def initGUI(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bgColor)
        # set the title of the window
        pygame.display.set_caption(self.title)
        # call for landlord
        self.passButton = Button(self.screen,100,350,100,50,'Pass', self.passIdentity)
        self.objs.append(self.passButton)
        self.confirmButton = Button(self.screen,600,350,100,50,'Be Professor', self.confirmIdentity)
        self.objs.append(self.confirmButton)
        self.Game.assignPlayOrder()
        myPos = self.Game.playOrder.index(self.Game.p1.name)
        if myPos == 0:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[2]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[1]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        elif myPos == 1:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[0]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[2]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        else:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[1]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[0]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        self.Game.shuffleDeck()
        self.Game.dealCard()
        xStart = 50
        cardCnt = len(self.Game.p1.cards)
        for card in self.Game.p1.cards:
            cardObj = Card(self.screen,card,xStart,430,50,70)
            self.objs.append(cardObj)
            xStart += 700/cardCnt
    def confirmIdentity(self):
        self.Game.chooseLandlord(self.Game.p1)
        self.Game.assignPlayOrder()
        self.objs.remove(self.confirmButton)
        self.objs.remove(self.passButton)
        self.objs.remove(self.prevPlayer)
        self.objs.remove(self.nextPlayer)
        self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[2]],50,50,50,50)
        self.objs.append(self.prevPlayer)
        self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[1]],700,50,50,50)
        self.objs.append(self.nextPlayer)
        self.initMainGameGUI()
    def passIdentity(self):
        self.Game.makePlay('')
        self.objs.remove(self.confirmButton)
        self.objs.remove(self.passButton)
    def selectCard(self,cardVal):
        if cardVal not in self.selectedCards and cardVal in self.Game.p1.cards:
            self.selectedCards.append(cardVal)
            print(f"Selected: {cardVal}")
    def deSelect(self,cardVal):
        if cardVal in self.selectedCards and cardVal in self.Game.p1.cards:
            self.selectedCards.remove(cardVal)
            print(f"Deselected: {cardVal}")
    def confirmCard(self):
        self.Game.makePlay(self.selectedCards)
        self.updateScreen()
        self.objs.remove(self.confirmButton)
        self.selectedCards = []
        mod = self.Game.checkWin()
        if mod == 1: # current player wins as professor
            tkinter.Tk().wm_withdraw() #to hide the main window
            tkinter.messagebox.showinfo('Winner','CONGRATS PROFESSOR! KEEP OPPRESSING YOUR STUDENTS!')
            pygame.quit()
        elif mod == 2: # current player wins as student
            tkinter.Tk().wm_withdraw() #to hide the main window
            tkinter.messagebox.showinfo('Winner','CONGRATS STUDENTS! KILL MORE PROFESSORS!')
            pygame.quit()
    def updateScreen(self):
        for i in self.objs:
            if type(i).__name__ == 'Card':
                del i
        self.cardDict.clear()
        xStart = 50
        cardCnt = len(self.Game.p1.cards)
        for card in self.Game.p1.cards:
            cardObj = Card(self.screen,card,xStart,430,50,70,lambda x=card: self.selectCard(x),lambda x=card: self.deSelect(x))
            self.objs.append(cardObj)
            self.cardDict[card] = cardObj
            xStart += 700/cardCnt
        xStart = 350
        for card in self.Game.prevPlay:
            prevPlayObj = Card(self.screen,card,xStart,180,50,70)
            self.objs.append(prevPlayObj)
            xStart += 400/cardCnt
    def initMainGameGUI(self):
        self.objs.clear()
        self.selectedCards = []
        self.confirmButton = Button(self.screen,600,350,100,50,'Confirm Play', self.confirmCard)
        self.objs.append(self.confirmButton)
        myPos = self.Game.playOrder.index(self.Game.p1.name)
        if myPos == 0:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[2]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[1]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        elif myPos == 1:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[0]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[2]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        else:
            self.prevPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[1]],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playerDict[self.Game.playOrder[0]],700,50,50,50)
            self.objs.append(self.nextPlayer)
        xStart = 50
        cardCnt = len(self.Game.p1.cards)
        self.cardDict = {}
        for card in self.Game.p1.cards:
            cardObj = Card(self.screen,card,xStart,430,50,70,lambda x=card: self.selectCard(x),lambda x=card: self.deSelect(x))
            self.cardDict[card] = cardObj
            self.objs.append(cardObj)
            xStart += 700/cardCnt
    def run(self):
        self.initGUI()
        playing = True
        while playing:
            time = self.clock.tick(self.fps)
            #self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in self.objs:
                        obj.process()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for obj in self.objs:
                        obj.process()
                elif event.type == pygame.QUIT:
                    playing = False
            if self.chosenLandlord:
                self.initMainGameGUI()
            
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game('human','ai1','ai2')
    gameGUI(game)