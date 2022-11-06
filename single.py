# Single Player GUI
# loginGUI: class for logging into the server and going to mainGUI
# gameGUI: class for the visualization of gaming

import tkinter
import pygame
from chatComm import *
import tkinter.messagebox
from pygameWidgets import *
from GameEngine import *


class singleGUI:
    def __init__(self, Game, name):
        # initialize main parameters
        self.name = name
        self.width = 800
        self.height = 600
        self.fps = 20
        self.title = "Fight the Professor! By Eric Gao"
        self.bgColor = (255, 255, 255)
        self.bg = pygame.image.load('./imgs/bg/tartanbg.png')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        # initialize game object
        self.Game = Game
        if self.Game.p2.name == self.name:
            self.player = self.Game.p2
        else:
            self.player = self.Game.p3
        self.objs = []
        self.cardDict = {}
        self.selectedCards = []
        self.chosenLandlord = False
        pygame.init()
        self.run()
    # confirm proofessor identity

    def confirmIdentity(self):
        self.Game.chooseLandlord(self.name)
        self.chosenLandlord = True
        self.Game.assignPlayOrder()
        self.updateScreen()
    # pass professor identity

    def passIdentity(self):
        self.Game.makePlay([])
        self.updateScreen()
    # select cards

    def selectCard(self, cardVal):
        if cardVal not in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.append(cardVal)
    # deselect cards

    def deSelect(self, cardVal):
        if cardVal in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.remove(cardVal)
    # confirm card play

    def confirmCard(self):
        if self.selectedCards != [] and self.Game.isValidPlay(self.selectedCards):
            self.Game.makePlay(self.selectedCards)
            self.selectedCards = []
            mod = self.Game.checkWin()
            if mod == 1:  # current player wins as professor
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {self.Game.prevPlayer}', 'CONGRATS PROFESSOR! KEEP OPPRESSING YOUR STUDENTS!')
                pygame.quit()
            elif mod == 2:  # current player wins as student
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {self.Game.prevPlayer}', 'CONGRATS STUDENTS! KILL MORE PROFESSORS!')
                pygame.quit()
            self.updateScreen()
        elif self.Game.prevPlay == []:  # show error
            tkinter.Tk().wm_withdraw()
            tkinter.messagebox.showwarning('Warning', 'Invalid play!')
    # pass turn

    def passCard(self):
        if self.selectedCards == []:
            self.Game.makePlay([])
            self.updateScreen()
    # update screen from game object

    def updateScreen(self):
        # clear everything
        self.objs.clear()
        # update hand cards
        for i in self.cardDict:
            if i not in self.player.cards:
                self.cardDict[i] = None
        xStart = 50
        cardCnt = len(self.player.cards)
        for card in self.player.cards:
            if card not in self.cardDict:
                cardObj = Card(self.screen, card, xStart, 430, 50, 70, lambda x=card: self.selectCard(
                    x), lambda x=card: self.deSelect(x))
                self.cardDict[card] = cardObj
            else:
                cardObj = self.cardDict[card]
                cardObj.x = xStart
            if cardObj not in self.objs:
                self.objs.append(cardObj)
            xStart += 700/cardCnt
        # update played cards
        xStart = 350
        cardCnt = len(self.Game.prevPlay[1])
        if cardCnt != 0:
            for card in self.Game.prevPlay[1]:
                prevPlayObj = Card(self.screen, card, xStart, 180, 50, 70)
                self.objs.append(prevPlayObj)
                xStart += 200/cardCnt
        # update landlord cards
        if self.chosenLandlord == True:
            xStart = 320
            for card in self.Game.landLordCards:
                landlordCardObj = Card(self.screen, card, xStart, 40, 50, 70)
                self.objs.append(landlordCardObj)
                xStart += 200/3
        # update current player
        text = f"Current playing: {self.Game.currentPlayer}"
        currentPlayerTextObj = Text(self.screen, text, 230, 120, 350, 50)
        self.objs.append(currentPlayerTextObj)
        # update avatars and positions
        myPos = self.Game.playOrder.index(self.name)
        if myPos == 0:
            self.prevPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[2]], 50, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 700, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.nextPlayer)
            self.myPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[0]], 370, 570, 60, 20, self.chosenLandlord)
            self.objs.append(self.myPlayer)
            self.prevImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[2]],50,10,60,60)
            self.objs.append(self.prevImg)
            self.afterImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[1]],700,10,60,60)
            self.objs.append(self.afterImg)
            self.myImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[0]],370,510,60,60)
            self.objs.append(self.myImg)
        elif myPos == 1:
            self.prevPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[0]], 50, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[2]], 700, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.nextPlayer)
            self.myPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 370, 570, 60, 20, self.chosenLandlord)
            self.objs.append(self.myPlayer)
            self.prevImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[0]],50,10,60,60)
            self.objs.append(self.prevImg)
            self.afterImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[2]],700,10,60,60)
            self.objs.append(self.afterImg)
            self.myImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[1]],370,510,60,60)
            self.objs.append(self.myImg)
        else:
            self.prevPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 50, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[0]], 700, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.nextPlayer)
            self.myPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[2]], 370, 570, 60, 20, self.chosenLandlord)
            self.objs.append(self.myPlayer)
            self.prevImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[1]],50,10,60,60)
            self.objs.append(self.prevImg)
            self.afterImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[0]],700,10,60,60)
            self.objs.append(self.afterImg)
            self.myImg = Img(
                self.screen,self.Game.playerDict[self.Game.playOrder[2]],370,510,60,60)
            self.objs.append(self.myImg)
        # update buttons
        if self.chosenLandlord and self.Game.currentPlayer == self.name:
            self.passCardButton = Button(
                self.screen, 100, 350, 100, 50, 'Pass turn', self.passCard)
            self.objs.append(self.passCardButton)
            self.confirmCardButton = Button(
                self.screen, 600, 350, 100, 50, 'Confirm Play', self.confirmCard)
            self.objs.append(self.confirmCardButton)
        elif not self.chosenLandlord and self.Game.currentPlayer == self.name:
            self.passButton = Button(
                self.screen, 100, 350, 100, 50, 'Pass', self.passIdentity)
            self.objs.append(self.passButton)
            self.confirmButton = Button(
                self.screen, 600, 350, 100, 50, 'Be Professor', self.confirmIdentity)
            self.objs.append(self.confirmButton)
    # initialize game GUI

    def initGUI(self):
        # set basic variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bgColor)
        pygame.display.set_caption(self.title)
        # update screen
        self.updateScreen()
    # main function to be called

    def run(self):
        self.initGUI()
        playing = True
        while playing:
            self.screen.fill(self.bgColor)
            self.screen.blit(self.bg, (0,0))
            self.clock.tick(self.fps)
            self.updateScreen()
            # to show the initial screen
            for obj in self.objs:
                obj.process()
            for event in pygame.event.get():
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                    for obj in self.objs:
                        obj.process()
                if event.type == pygame.QUIT:
                    playing = False
            for obj in self.objs:
                obj.process()
            pygame.display.flip()
        pygame.quit()


# start game as client
if __name__ == "__main__":
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("Fight the Professor!")
    wnd.resizable(0, 0)
    singleGUIObj = singleGUI(wnd)
    wnd.mainloop()
