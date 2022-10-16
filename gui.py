# GUI
# loginGUI: class for logging into the server and going to mainGUI
# mainGUI: class for choosing players and go to gameGUI
# gameGUI: class for the visualization of gaming

import tkinter
import pygame
from chatComm import *
import tkinter.messagebox
from pygameWidgets import *
from GameEngine import Game

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
            # destroy login window and go to main indow
            self.parent.destroy()
            self.createMainGUI()
        else:
            # destroy the login window and exit
            self.parent.destroy()
            
    # create the main gui
    def createMainGUI(self):
        mainwnd = tkinter.Tk()
        mainwnd.title("Chat Client")
        mainwnd.geometry("450x300")
        mainwnd.resizable(0,0) # makes window size static
        mainGUIObj = mainGUI(mainwnd,self.chatComm,self.username)
        mainwnd.mainloop()

# class for the main window
class mainGUI:
    def __init__(self,parent,chatComm,username):
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
        # labels of respective field
        self.friendsLab = tkinter.Label(self.mainFrame,text="Choose 2 players to play with")
        # label layout
        self.friendsLab.grid(row=0,column=0)
        # three listboxes for respective fields
        self.friendsList = tkinter.Listbox(self.mainFrame,
                                           selectmode=tkinter.MULTIPLE,
                                           height=10)
        # listbox layout
        self.friendsList.grid(row=1,column=0)
        # put all of the data in each field
        for i in self.friends: self.friendsList.insert(tkinter.END,i)
        # buttons for each field
        self.startGameBtn = tkinter.Button(self.mainFrame,
                                           text="Start Game",
                                           command=self.startGame)
        # buttons layout
        self.startGameBtn.grid(row=2,column=0)
    
    # select 2 people to play with
    def startGame(self):
        selected = self.friendsList.get(self.friendsList.curselection())
        if len(selected) == 3:
            player1 = self.username
            player2 = selected[0]
            player3 = selected[1]
            game = Game(player1,player2,player3)
            gameGUIObj = gameGUI(game,self.chatComm,self.chatObjs)
            self.chatObjs[selected] = gameGUIObj
        else:
            tkinter.messagebox.showerror("Error","Can't you find 2 friends to fight the professor with you?")


class gameGUI:
    def __init__(self,Game,chatComm):
        self.chatComm = chatComm
        self.width = 800
        self.height = 600
        self.fps = 24
        self.title = "Fight the Professor! By Eric Gao"
        self.bgColor = (255,255,255)
        self.Game = Game
        self.objs = []
        pygame.init()
    def initGUI(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        self.confirmButton = Button(self.screen,30, 30, 400, 100, 'Confirm', self.confirmPlay)
        self.objs.append(self.confirmButton)
        self.prevPlayer = Player
        self.objs.append(self.prevPlayer)
        self.nextPlayer = Player
        self.objs.append(self.nextPlayer)
        self.Game.shuffleDeck()
    def run(self):
        self.initGUI()
        playing = True
        while playing:
            time = self.clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
            for obj in self.objs:
                obj.process()
            self.screen.fill(self.bgColor)
            pygame.display.flip()

        pygame.quit()