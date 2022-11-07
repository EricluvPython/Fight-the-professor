# Host GUI
# loginGUI: class for logging into the server and going to mainGUI
# mainGUI: class for choosing players and go to gameGUI
# gameGUI: class for the visualization of gaming

import tkinter
from tkinter.tix import IMAGE
import pygame
from chatComm import *
import tkinter.messagebox
from pygameWidgets import *
from GameEngine import *
import ast
from utils import convertHelper, anotherConvertHelper
import time


class loginGUI:
    def __init__(self, parent):
        # tkinter gui initialization
        self.parent = parent
        self.mainFrame = tkinter.Frame(parent)
        self.mainFrame.pack()
        # connection class initialization
        self.chatComm = chatComm("86.36.42.136", 15112)
        self.chatComm.startConnection()
        self.loggedin = False
        # title label
        titleLab = tkinter.Label(
            self.mainFrame, text="FIGHT THE PROFESSOR! presented by Eric Gao", font=30)
        titleLab.pack()
        # username field
        lab1 = tkinter.Label(self.mainFrame, text='Username')
        lab1.pack()
        self.nameBox = tkinter.Entry(self.mainFrame)
        self.nameBox.pack()
        # password field
        lab2 = tkinter.Label(self.mainFrame, text='Password')
        lab2.pack()
        self.passwordBox = tkinter.Entry(self.mainFrame, show="*")
        self.passwordBox.pack()
        # ok button
        ok = tkinter.Button(self.mainFrame, text="OK",
                            command=self.verifyLogin)
        ok.pack()

    # try to login with username and password
    def verifyLogin(self):
        # get information from entry fields
        self.username = self.nameBox.get()
        password = self.passwordBox.get()
        # login to server
        status = self.chatComm.login(self.username, password)
        if status:
            # destroy login window and go to main indow
            self.parent.destroy()
            self.createMainGUI()
        else:
            # destroy the login window and exit
            self.parent.destroy()

    # create the main gui
    def createMainGUI(self):
        mainwnd = tkinter.Tk()
        mainwnd.title("Choose 2 players to play with")
        mainwnd.geometry("450x300")
        mainwnd.resizable(0, 0)  # makes window size static
        mainGUIObj = mainGUI(mainwnd, self.chatComm, self.username)
        mainwnd.mainloop()

# class for the main window


class mainGUI:
    def __init__(self, parent, chatComm, username):
        # tkinter gui initialization
        self.parent = parent
        self.chatComm = chatComm
        self.username = username
        self.mainFrame = tkinter.Frame(parent)
        self.mainFrame.pack()
        # list of active chats
        self.gameObjs = {}
        # lists of users, friends, and requests
        self.friends = self.chatComm.getFriends()
        # labels of respective field and layout
        self.friendsLab = tkinter.Label(
            self.mainFrame, text="Choose 2 players to play with")
        self.friendsLab.grid(row=0, column=0)
        # listbox of friends and layout
        self.friendsList = tkinter.Listbox(self.mainFrame,
                                           selectmode=tkinter.MULTIPLE,
                                           height=10)
        self.friendsList.grid(row=1, column=0)
        for i in self.friends:
            self.friendsList.insert(tkinter.END, i)
        # button for starting game and layout
        self.startGameBtn = tkinter.Button(self.mainFrame,
                                           text="Start Game",
                                           command=self.startGame)
        self.startGameBtn.grid(row=2, column=0)

    # select 2 people to play with
    def startGame(self):
        selected = []
        # get selected people
        for i in self.friendsList.curselection():
            selected.append(self.friendsList.get(i))
        # start the game
        if len(selected) == 2:
            player1 = self.username
            player2 = selected[0]
            player3 = selected[1]
            self.parent.destroy()
            game = Game(player1, player2, player3)
            gameGUIObj = gameGUI(game, self.chatComm)
            # not sure why I didn't delete this
            self.gameObjs[''.join(selected)] = gameGUIObj
        else:  # show error message
            tkinter.messagebox.showerror(
                "Error", "Can't you find 2 friends to fight the professor with you?")


class gameGUI:
    def __init__(self, Game, chatComm):
        # main objects initialization
        self.chatComm = chatComm
        self.width = 800
        self.height = 600
        self.fps = 40
        self.title = "Fight the Professor! By Eric Gao"
        self.bgColor = (255, 255, 255)
        self.bg = pygame.image.load('./imgs/bg/tartanbg.png')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        # game objects initialization
        self.Game = Game
        self.objs = []
        self.chosenLandlord = False
        self.cardDict = {}
        self.selectedCards = []
        pygame.init()
        self.run()
    # send the game to clients, mod indicates whether game ended

    def sendGame(self, mod=0):
        encoded = self.Game.encodeGame(mod)
        self.chatComm.sendMessage(self.Game.p2.name, encoded)
        self.chatComm.sendMessage(self.Game.p3.name, encoded)
    # update current game from received game (if any)

    def updateGame(self):
        messages = self.chatComm.getMail()[0]
        if messages != []:
            for i in messages:
                info = i[1].replace('\n', '').replace(' ', '').split('#')
                info = info[1:]
                info[3] = convertHelper(info[3])
                info[6] = convertHelper(info[6])
                info[9] = convertHelper(info[9])
                info[11] = anotherConvertHelper(info[11])
                info[12] = ast.literal_eval(info[12])
                info[13] = convertHelper(info[13])
                if info[0] in ['0', '1', '2']:
                    self.Game = self.decodeGame(info)
    # decode info to a new game object

    def decodeGame(self, gameInfo):
        newGame = Game(gameInfo[1], gameInfo[4], gameInfo[7])
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
        newGame.landLordCards = gameInfo[13]
        if gameInfo[0] == '1':
            if newGame.p1.name == 'p':
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {newGame.prevPlayer}', 'CONGRATS PROFESSOR! KEEP OPPRESSING YOUR STUDENTS!')
                pygame.quit()
            else:
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {newGame.prevPlayer}', 'YOU LOST! FIGHT HARDER AGAINST YOUR PROFESSOR!')
                pygame.quit()
        elif gameInfo[0] == '2':
            if newGame.p1.identity == 's':
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {newGame.prevPlayer}', 'CONGRATS STUDENTS! KILL MORE PROFESSORS!')
                pygame.quit()
            else:
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {newGame.prevPlayer}', 'YOU LOST! BECOME BETTER AT BEING AN EVIL PROFESSOR!')
                pygame.quit()
        return newGame
    # confirm professor identity

    def confirmIdentity(self):
        self.Game.chooseLandlord(self.Game.p1.name)
        self.chosenLandlord = True
        self.Game.assignPlayOrder()
        self.updateScreen()
        self.sendGame()
    # pass professor identity

    def passIdentity(self):
        self.Game.makePlay([])
        self.updateScreen()
        self.sendGame()
    # select cards

    def selectCard(self, cardVal):
        if cardVal not in self.selectedCards and cardVal in self.Game.p1.cards:
            self.selectedCards.append(cardVal)
    # deselect cards

    def deSelect(self, cardVal):
        if cardVal in self.selectedCards and cardVal in self.Game.p1.cards:
            self.selectedCards.remove(cardVal)
    # confirm card play

    def confirmCard(self):
        if self.selectedCards != [] and self.Game.isValidPlay(self.selectedCards):
            self.Game.makePlay(self.selectedCards)
            self.selectedCards = []
            mod = self.Game.checkWin()
            if mod == 1:  # current player wins as professor
                self.sendGame(1)
                if self.Game.p1.identity == 'p':
                    tkinter.Tk().wm_withdraw()  # to hide the main window
                    tkinter.messagebox.showinfo(
                        f'Winner is: {self.Game.prevPlayer}', 'CONGRATS PROFESSOR! KEEP OPPRESSING YOUR STUDENTS!')
                    pygame.quit()
                else:
                    tkinter.Tk().wm_withdraw()  # to hide the main window
                    tkinter.messagebox.showinfo(
                        f'Winner is: {self.Game.prevPlayer}', 'YOU LOST! FIGHT HARDER AGAINST YOUR PROFESSOR!')
                    pygame.quit()
            elif mod == 2:  # current player wins as student
                self.sendGame(2)
                if self.Game.p1.identity == 's':
                    tkinter.Tk().wm_withdraw()  # to hide the main window
                    tkinter.messagebox.showinfo(
                        f'Winner is: {self.Game.prevPlayer}', 'CONGRATS STUDENTS! KILL MORE PROFESSORS!')
                    pygame.quit()
                else:
                    tkinter.Tk().wm_withdraw()  # to hide the main window
                    tkinter.messagebox.showinfo(
                        f'Winner is: {self.Game.prevPlayer}', 'YOU LOST! BECOME BETTER AT BEING AN EVIL PROFESSOR!')
                    pygame.quit()
            else:
                self.sendGame(0)  # game continues
        elif self.Game.prevPlay == []:  # show error message
            tkinter.Tk().wm_withdraw()
            tkinter.messagebox.showwarning('Warning', 'Invalid play!')
        self.updateScreen()
    # pass the turn

    def passCard(self):
        if self.selectedCards == []:
            self.Game.makePlay([])
            self.updateScreen()
            self.sendGame()
    # update screen from current game object

    def updateScreen(self):
        # clear everything
        self.objs.clear()
        self.updateGame()
        # update hand cards
        for i in self.cardDict:
            if i not in self.Game.p1.cards:
                self.cardDict[i] = None
        xStart = 50
        cardCnt = len(self.Game.p1.cards)
        for card in self.Game.p1.cards:
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
        # update avatars
        myPos = self.Game.playOrder.index(self.Game.p1.name)
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
            self.prevCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[2]].cards)),70,90,20,20)
            self.objs.append(self.prevCardCnt)
            self.afterCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[1]].cards)),720,90,20,20)
            self.objs.append(self.afterCardCnt)
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
            self.prevCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[0]].cards)),70,90,20,20)
            self.objs.append(self.prevCardCnt)
            self.afterCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[2]].cards)),720,90,20,20)
            self.objs.append(self.afterCardCnt)
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
            self.prevCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[1]].cards)),70,90,20,20)
            self.objs.append(self.prevCardCnt)
            self.afterCardCnt = Text(
                self.screen,str(len(self.Game.playerDict[self.Game.playOrder[0]].cards)),720,90,20,20)
            self.objs.append(self.afterCardCnt)
        # update buttons
        if self.chosenLandlord and self.Game.currentPlayer == self.Game.p1.name:
            self.passCardButton = Button(
                self.screen, 100, 350, 100, 50, 'Pass turn', self.passCard)
            self.objs.append(self.passCardButton)
            self.confirmCardButton = Button(
                self.screen, 600, 350, 100, 50, 'Confirm Play', self.confirmCard)
            self.objs.append(self.confirmCardButton)
        elif not self.chosenLandlord and self.Game.currentPlayer == self.Game.p1.name:
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
        # initialize game engine
        self.Game.assignPlayOrder()
        self.Game.shuffleDeck()
        self.Game.dealCard()
        self.sendGame()
        # update screen
        self.updateScreen()
    # the main function to be called

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


# start game as host
if __name__ == "__main__":
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("Fight the Professor!")
    #wnd.resizable(0, 0)
    loginGUIObj = loginGUI(wnd)
    wnd.mainloop()
