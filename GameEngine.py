# Game Engine
# Game: a class that represents the state and progress of the game
# it contains all players and their cards, and the cards played on field
# initialize game -> shuffle deck -> distribute card -> choose landlord -> {{check validity -> play card} -> check if anyone won -> next player}

import random
import utils

class Game:
    def __init__(self,p1id,p2id,p3id):
        self.colors = ['heart','spade','diamond','club']
        self.nums = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.specials = ['X','D']
        self.cardOrder = {'3':1,'4':2,'5':3,'6':4,'7':5,'8':6,'9':7,'10':8,
        'J':9,'Q':10,'K':11,'A':12,'2':13,'X':14,'D':15}
        self.p1 = player(p1id)
        self.p2 = player(p2id)
        self.p3 = player(p3id)
        self.currentPlayer = ''
        self.prevPlay = ''
        self.playOrder = []
    # helper function for sorting card
    def sortHelper(self,x):
            if x[-1] == '0':
                return self.cardOrder['10']
            return self.cardOrder[x[-1]]
    # encode game to a message
    def encodeGame(self,mod=0):
        return f'''@{str(mod)}@{self.p1.name}@{self.p1.identity}@{self.p1.cards}
        @{self.p2.name}@{self.p2.identity}@{self.p2.cards}
        @{self.p3.name}@{self.p3.identity}@{self.p3.cards}
        @{self.currentPlayer}@{self.prevPlay}@{self.playOrder}'''
    # distribute the initial card
    def shuffleDeck(self):
        self.deck = []
        for i in self.colors:
            for j in self.nums:
                self.deck.append(i+' '+j)
        self.deck.append(self.specials[0])
        self.deck.append(self.specials[1])
        random.shuffle(self.deck)
    # deal the cards
    def dealCard(self):
        self.landLordCards = []
        for i in range(3):
            choice = random.choice(self.deck)
            self.landLordCards.append(choice)
            self.deck.remove(choice)
        self.p1Card = []
        for i in range(17):
            choice = random.choice(self.deck)
            self.p1Card.append(choice)
            self.deck.remove(choice)
        self.p2Card = []
        for i in range(17):
            choice = random.choice(self.deck)
            self.p2Card.append(choice)
            self.deck.remove(choice)
        self.p3Card = []
        for i in range(17):
            choice = random.choice(self.deck)
            self.p3Card.append(choice)
            self.deck.remove(choice)
        self.p1.cards = self.p1Card
        self.p2.cards = self.p2Card
        self.p3.cards = self.p3Card
        self.p1.cards.sort(key=lambda x: self.sortHelper(x))
        self.p2.cards.sort(key=lambda x: self.sortHelper(x))
        self.p3.cards.sort(key=lambda x: self.sortHelper(x))
    # assign landlord
    def chooseLandlord(self,player):
        player.identity = 'p'
        for card in self.landLordCards:
            player.cards.append(card)
        player.cards.sort(key=lambda x: self.sortHelper(x))
    # assign play sequence
    def assignPlayOrder(self):
        if self.p1.identity == 'p':
            self.playOrder = [self.p2,self.p3]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0,self.p1)
        elif self.p2.identity == 'p':
            self.playOrder = [self.p1,self.p3]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0,self.p2)
        elif self.p3.identity == 'p':
            self.playOrder = [self.p1,self.p2]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0,self.p3)
        else:
            self.playOrder = [self.p1,self.p2,self.p3]
            random.shuffle(self.playOrder)
        self.currentPlayer = self.playOrder[0]
    # identify pattern of played card
    def whichPattern(self,selectedCards):
        cardValues = []
        for i in selectedCards:
            cardValues.append(self.cardOrder[i[-1]])
        pattern = utils.get_move_type(cardValues)
        return pattern
    # check play validity
    def isValidPlay(self,prevPlay,selected):
        pattern1 = self.whichPattern(prevPlay)
        pattern2 = self.whichPattern(selected)
        if pattern2['type'] == 15 or pattern1['type'] == 5:
            return False
        elif pattern2['type'] == 5:
            return True
        else:
            if pattern1['type'] == pattern2['type'] and\
                 pattern1['rank'] < pattern2['rank']:
                 return True
            else:
                return False
    # make a play
    def makePlay(self,selectedCards):
        self.currentPlayer.playCard(selectedCards)
        self.prevPlay = self.currentPlayer
        playerIndex = self.playOrder.index(self.currentPlayer)
        if playerIndex == 2:
            self.currentPlayer = self.playOrder[0]
        else:
            self.currentPlayer = self.playOrder[playerIndex+1]
    # check who wins
    def checkWin(self):
        if self.currentPlayer.cards == []:
            if self.currentPlayer.identity == 'p':
                return 1 # player wins as professor
            else:
                return 2 # player wins as students
        else:
            return 0 # not ended yet

class player:
    def __init__(self,name):
        self.name = name
        self.identity = 's'
        self.cards = []
    # make a play
    def playCard(self,selectedCards):
        print(self.cards,selectedCards)
        for i in selectedCards:
            self.cards.remove(i)