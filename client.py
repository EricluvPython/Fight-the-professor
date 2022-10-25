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
from utils import convertHelper

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
        titleLab = tkinter.Label(self.mainFrame,text="FIGHT THE PROFESSOR! presented by Eric Gao\n",font=30)
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
        self.ok = tkinter.Button(self.mainFrame,text="OK",command=self.verifyLogin)
        self.ok.pack()
    # try to login with username and password
    def verifyLogin(self):
        # get information from entry fields
        self.username = self.nameBox.get()
        password = self.passwordBox.get()
        # login to server
        status = self.chatComm.login(self.username,password)
        if status:
            # disable widgets
            self.nameBox.configure(state=tkinter.DISABLED)
            self.passwordBox.configure(state=tkinter.DISABLED)
            self.ok.configure(state=tkinter.DISABLED)
            tkinter.messagebox.showinfo("Status","Please wait for game to be started by host...")
            self.checkForGame()
        else:
            tkinter.messagebox.showerror("Error","Wrong username or password. You should be smarter than this to fight the professor.")
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
        def convertHelper(s):
            s = ast.literal_eval(s)
            for i in range(len(s)):
                if len(s[i]) > 1:
                    if s[i][-1] == '0':
                        s[i] = s[i][:-2]+' '+s[i][-2:]
                    else:
                        s[i] = s[i][:-1]+' '+s[i][-1]
            return s
        messages = self.chatComm.getMail()[0]
        for i in messages:
            info = i[1].replace('\n','').replace(' ','').split('#')
            info = info[1:]
            info[3] = convertHelper(info[3])
            info[6] = convertHelper(info[6])
            info[9] = convertHelper(info[9])
            info[11] = convertHelper(info[11])
            info[12] = ast.literal_eval(info[12])
            if len(info) == 13 and info[0] in ['0','1','2']:
                self.Game = self.decodeGame(info)
                self.parent.destroy()
                clientGUIObj = clientGUI(self.Game,self.chatComm,self.username)
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
    def sendGame(self,mod=0):
        encoded = self.Game.encodeGame(mod)
        target = [self.Game.p1.name,self.Game.p2.name,self.Game.p3.name]
        target.remove(self.name)
        for i in target:
            self.chatComm.sendMessage(i,encoded)
    def updateGame(self):
        messages = self.chatComm.getMail()[0]
        if messages != []:
            for i in messages:
                info = i[1].replace('\n','').replace(' ','').split('#')
                info = info[1:]
                print(info)
                info[3] = convertHelper(info[3])
                info[6] = convertHelper(info[6])
                info[9] = convertHelper(info[9])
                info[11] = convertHelper(info[11])
                info[12] = ast.literal_eval(info[12])
                if len(info) == 13 and info[0] in ['0','1','2']:
                    self.Game = self.decodeGame(info)
                    return
    def decodeGame(self,gameInfo):
        newGame = Game(gameInfo[1],gameInfo[4],gameInfo[7])
        newGame.p1.identity = gameInfo[2]
        newGame.p2.identity = gameInfo[5]
        newGame.p3.identity = gameInfo[8]
        if gameInfo[2] == 'p' or gameInfo[5] == 'p' or gameInfo[8] == 'p':
            self.chosenLandlord = True
        newGame.p1.cards = gameInfo[3]
        newGame.p2.cards = gameInfo[6]
        newGame.p3.cards = gameInfo[9]
        newGame.currentPlayer = gameInfo[10]
        newGame.prevPlay = gameInfo[11]
        newGame.playOrder = gameInfo[12]
        if newGame.p2.name == self.name:
            self.player = self.Game.p2
        else:
            self.player = self.Game.p3
        return newGame
    def confirmIdentity(self):
        self.Game.chooseLandlord(self.player)
        self.chosenLandlord = True
        self.Game.assignPlayOrder()
        self.sendGame()
    def passIdentity(self):
        self.Game.makePlay([])
        self.sendGame()
    def selectCard(self,cardVal):
        if cardVal not in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.append(cardVal)
    def deSelect(self,cardVal):
        if cardVal in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.remove(cardVal)
    def confirmCard(self):
        if self.selectedCards != [] and self.Game.isValidPlay(self.selectedCards):
            self.Game.makePlay(self.selectedCards)
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
    def passCard(self):
        if self.selectedCards == []:
            self.Game.makePlay([])
            self.sendGame()
    def updateScreen(self):
        # clear everything
        self.objs.clear()
        self.updateGame()
        # update hand cards
        for i in self.cardDict:
            if i not in self.player.cards:
                self.cardDict[i] = None
        xStart = 50
        cardCnt = len(self.player.cards)
        for card in self.player.cards:
            if card not in self.cardDict:
                cardObj = Card(self.screen,card,xStart,430,50,70,lambda x=card: self.selectCard(x),lambda x=card: self.deSelect(x))
                self.cardDict[card] = cardObj
            else:
                cardObj = self.cardDict[card]
                cardObj.x = xStart
            if cardObj not in self.objs:
                self.objs.append(cardObj)
            xStart += 700/cardCnt
        # update played cards
        xStart = 350
        cardCnt = len(self.Game.prevPlay)
        if cardCnt != 0:
            for card in self.Game.prevPlay:
                prevPlayObj = Card(self.screen,card,xStart,180,50,70)
                self.objs.append(prevPlayObj)
                xStart += 400/cardCnt
        # update avatars and positions
        myPos = self.Game.playOrder.index(self.name)
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
        # update buttons
        if self.chosenLandlord and self.Game.currentPlayer == self.name:
            self.passCardButton = Button(self.screen,100,350,100,50,'Pass turn', self.passCard)
            self.objs.append(self.passCardButton)
            self.confirmCardButton = Button(self.screen,600,350,100,50,'Confirm Play', self.confirmCard)
            self.objs.append(self.confirmCardButton)
        elif not self.chosenLandlord and self.Game.currentPlayer == self.name:
            self.passButton = Button(self.screen,100,350,100,50,'Pass', self.passIdentity)
            self.objs.append(self.passButton)
            self.confirmButton = Button(self.screen,600,350,100,50,'Be Professor', self.confirmIdentity)
            self.objs.append(self.confirmButton)
    def initGUI(self):
        # set basic variables
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bgColor)
        pygame.display.set_caption(self.title)
        # update screen
        self.updateScreen()
    def run(self):
        self.updateGame()
        self.initGUI()
        playing = True
        while playing:
            self.screen.fill(self.bgColor)
            self.clock.tick(self.fps)
            self.updateScreen()
            # to show the initial screen
            for obj in self.objs:
                obj.process()
            for event in pygame.event.get():
                if event.type in [pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP]:
                    for obj in self.objs:
                        obj.process()
                if event.type == pygame.QUIT:
                    playing = False
            for obj in self.objs:
                obj.process()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("Fight the Professor!")
    #wnd.resizable(0,0)
    loginGUIObj = loginGUI(wnd)
    wnd.mainloop()