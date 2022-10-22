# Client GUI
# loginGUI: class for logging into the server and going to mainGUI
# gameGUI: class for the visualization of gaming

import tkinter
import pygame
from chatComm import *
import tkinter.messagebox
from pygameWidgets import *
from GameEngine import *
import ast

class loginGUI:
    def __init__(self,parent):
        # tkinter gui initialization
        self.parent = parent
        self.mainFrame = tkinter.Frame(parent)
        self.mainFrame.pack()
        # connection class initialization
        self.chatComm = chatComm("86.36.42.136", 15112)
        self.chatComm.startConnection()
        self.loggedin = False
        # title label
        titleLab = tkinter.Label(self.mainFrame,text="FIGHT THE PROFESSOR! presented by Eric Gao",font=30)
        titleLab.pack()
        # username field
        lab1 = tkinter.Label(self.mainFrame,text='Username')
        lab1.pack()
        self.nameBox = tkinter.Entry(self.mainFrame)
        self.nameBox.pack()
        # password field
        lab2 = tkinter.Label(self.mainFrame,text='Password')
        lab2.pack()
        self.passwordBox = tkinter.Entry(self.mainFrame,show="*")
        self.passwordBox.pack()
        # ok button
        ok = tkinter.Button(self.mainFrame,text="OK",command=self.verifyLogin)
        ok.pack()
        
    # try to login with username and password
    def verifyLogin(self):
        # get information from entry fields
        self.username = self.nameBox.get()
        password = self.passwordBox.get()
        # login to server
        status = self.chatComm.login(self.username,password)
        if status:
            # go to main indow
            tkinter.messagebox.showinfo("Status","Waiting for game to be established, please wait.")
            self.checkForGame()
        else:
            # destroy the login window and exit
            self.parent.destroy()
    # decode game
    def decodeGame(self,gameInfo):
        newGame = Game(gameInfo[1],gameInfo[4],gameInfo[7])
        newGame.p1.identity = gameInfo[2]
        newGame.p2.identity = gameInfo[5]
        newGame.p3.identity = gameInfo[8]
        newGame.p1.cards = gameInfo[3]
        newGame.p2.cards = gameInfo[6]
        newGame.p3.cards = gameInfo[9]
        newGame.currentPlayer = gameInfo[10]
        newGame.prevPlay = gameInfo[11]
        newGame.playOrder = gameInfo[12]      
        return newGame
    # create the main gui
    def checkForGame(self):
        messages = self.chatComm.getMail()[0]
        for i in messages:
            print(i)
            info = i[1].replace('\n','').replace(' ','').split('#')
            info = info[1:]
            info[3] = ast.literal_eval(info[3])
            info[6] = ast.literal_eval(info[6])
            info[9] = ast.literal_eval(info[9])
            info[12] = ast.literal_eval(info[12])
            if len(info) == 13 and info[0] in ['0','1','2']:
                self.Game = self.decodeGame(info)
                gameGUIObj = clientGUI(self.Game,self.chatComm,self.username)
                self.parent.destroy()
                return
        self.parent.after(5000,self.checkForGame)
        

class clientGUI:
    def __init__(self,Game,chatComm,name):
        self.chatComm = chatComm
        self.name = name
        self.width = 800
        self.height = 600
        self.fps = 20
        self.title = "Fight the Professor! By Eric Gao"
        self.bgColor = (255,255,255)
        self.Game = Game
        if self.Game.p1.name == self.name:
            self.player = self.Game.p1
        elif self.Game.p2.name == self.name:
            self.player = self.Game.p2
        else:
            self.player = self.Game.p3
        self.objs = []
        self.chosenLandlord = False
        pygame.init()
        self.run()
    def sendGame(self,mod=0):
        encoded = self.Game.encodeGame(mod)
        for i in [self.Game.p1.name,self.Game.p2.name,self.Game.p3.name]-[self.name]:
            self.chatComm.sendMessage(i,encoded)
    def updateGame(self):
        updates = self.chatComm.getMail()[0]
        for i in updates:
            if i[0] in [self.Game.p1.name,self.Game.p2.name,self.Game.p3.name]-[self.name]:
                newInfo = i[1].split('#')
                if newInfo[0] in ['0','1','2']:
                    self.Game = self.decodeGame(newInfo)
                    break
    def decodeGame(self,gameInfo):
        newGame = Game(gameInfo[1],gameInfo[4],gameInfo[7])
        newGame.p1.identity = gameInfo[2]
        newGame.p2.identity = gameInfo[5]
        newGame.p3.identity = gameInfo[8]
        if gameInfo[2] == 'p' or gameInfo[5] == 'p' or gameInfo[8] == 'p':
            self.chosenLandlord = True
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
        self.updateGame()
        xStart = 50
        cardCnt = len(self.player.cards)
        for card in self.player.cards:
            cardObj = Card(self.screen,card,xStart,430,50,70)
            self.objs.append(cardObj)
            xStart += 700/cardCnt
        # call for landlord
        if self.Game.currentPlayer == self.name and self.playOrder.index(self.Game.currentPlayer) == 2:
            self.confirmIdentity()
        if self.Game.currentPlayer == self.name:
            self.passButton = Button(self.screen,100,350,100,50,'Pass', self.passIdentity)
            self.objs.append(self.passButton)
            self.confirmButton = Button(self.screen,600,350,100,50,'Be Professor', self.confirmIdentity)
            self.objs.append(self.confirmButton)
            myPos = self.Game.playOrder.index(self.Game.p1)
            if myPos == 0:
                self.prevPlayer = Player(self.screen,self.Game.playOrder[2],50,50,50,50)
                self.objs.append(self.prevPlayer)
                self.nextPlayer = Player(self.screen,self.Game.playOrder[1],700,50,50,50)
                self.objs.append(self.nextPlayer)
            elif myPos == 1:
                self.prevPlayer = Player(self.screen,self.Game.playOrder[0],50,50,50,50)
                self.objs.append(self.prevPlayer)
                self.nextPlayer = Player(self.screen,self.Game.playOrder[2],700,50,50,50)
                self.objs.append(self.nextPlayer)
            else:
                self.prevPlayer = Player(self.screen,self.Game.playOrder[1],50,50,50,50)
                self.objs.append(self.prevPlayer)
                self.nextPlayer = Player(self.screen,self.Game.playOrder[0],700,50,50,50)
                self.objs.append(self.nextPlayer)
    def confirmIdentity(self):
        self.Game.chooseLandlord(self.player)
        self.Game.assignPlayOrder()
        self.objs.remove(self.confirmButton)
        self.objs.remove(self.passButton)
        self.objs.remove(self.prevPlayer)
        self.objs.remove(self.nextPlayer)
        self.prevPlayer = Player(self.screen,self.Game.playOrder[2],50,50,50,50)
        self.objs.append(self.prevPlayer)
        self.nextPlayer = Player(self.screen,self.Game.playOrder[1],700,50,50,50)
        self.objs.append(self.nextPlayer)
        self.sendGame()
        self.initMainGameGUI()
    def passIdentity(self):
        self.Game.makePlay('')
        self.objs.remove(self.confirmButton)
        self.objs.remove(self.passButton)
        self.sendGame()
    def selectCard(self,cardVal):
        if cardVal not in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.append(cardVal)
            print(f"Selected: {cardVal}")
    def deSelect(self,cardVal):
        if cardVal in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.remove(cardVal)
            print(f"Deselected: {cardVal}")
    def confirmCard(self):
        if self.Game.isValidPlay(self.selectedCards):
            self.Game.makePlay(self.selectedCards)
            self.updateScreen()
            self.objs.remove(self.confirmButton)
            self.selectedCards = []
            mod = self.Game.checkWin()
            if mod == 1: # current player wins as professor
                self.sendGame(1)
                tkinter.Tk().wm_withdraw() #to hide the main window
                tkinter.messagebox.showinfo('Winner','CONGRATS PROFESSOR! KEEP OPPRESSING YOUR STUDENTS!')
                pygame.quit()
            elif mod == 2: # current player wins as student
                self.sendGame(2)
                tkinter.Tk().wm_withdraw() #to hide the main window
                tkinter.messagebox.showinfo('Winner','CONGRATS STUDENTS! KILL MORE PROFESSORS!')
                pygame.quit()
            else:
                self.sendGame(0)
        else:
            tkinter.Tk().wm_withdraw() 
            tkinter.messagebox.showwarning('Warning','Invalid play!')
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
        myPos = self.Game.playOrder.index(self.player)
        if myPos == 0:
            self.prevPlayer = Player(self.screen,self.Game.playOrder[2],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playOrder[1],700,50,50,50)
            self.objs.append(self.nextPlayer)
        elif myPos == 1:
            self.prevPlayer = Player(self.screen,self.Game.playOrder[0],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playOrder[2],700,50,50,50)
            self.objs.append(self.nextPlayer)
        else:
            self.prevPlayer = Player(self.screen,self.Game.playOrder[1],50,50,50,50)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(self.screen,self.Game.playOrder[0],700,50,50,50)
            self.objs.append(self.nextPlayer)
        xStart = 50
        cardCnt = len(self.player.cards)
        self.cardDict = {}
        for card in self.player.cards:
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