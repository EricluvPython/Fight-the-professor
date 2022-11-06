# Game Engine
# Game: a class that represents the state and progress of the game
# it contains all players and their cards, and the cards played on field
# initialize game -> shuffle deck -> distribute card -> choose landlord -> {{check validity -> play card} -> check if anyone won -> next player}

import random
import utils


class Game:
    def __init__(self, p1id, p2id, p3id):
        # for generating and comparing cards
        self.colors = ['heart', 'spade', 'diamond', 'club']
        self.nums = ['A', '2', '3', '4', '5', '6',
                     '7', '8', '9', '10', 'J', 'Q', 'K']
        self.specials = ['X', 'D']
        self.cardOrder = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                          'J': 9, 'Q': 10, 'K': 11, 'A': 12, '2': 13, 'X': 14, 'D': 15}
        # player objects and dictionary
        self.p1 = player(p1id)
        self.p2 = player(p2id)
        self.p3 = player(p3id)
        self.playerDict = {p1id: self.p1, p2id: self.p2, p3id: self.p3}
        # some game states
        self.currentPlayer = ''
        self.prevPlayer = ''
        self.prevPlay = ['', []]
        self.playOrder = []
        self.landLordCards = []
    # helper function for sorting card

    def sortHelper(self, x):
        if x[-1] == '0':
            return self.cardOrder['10']
        return self.cardOrder[x[-1]]
    # encode game to a message

    def encodeGame(self, mod=0):
        return f'''#{str(mod)}#{self.p1.name}#{self.p1.identity}#{self.p1.cards}
        #{self.p2.name}#{self.p2.identity}#{self.p2.cards}
        #{self.p3.name}#{self.p3.identity}#{self.p3.cards}
        #{self.currentPlayer}#{self.prevPlay}#{self.playOrder}#{self.landLordCards}'''
    # generate and distribute the initial cards

    def shuffleDeck(self):
        self.deck = []
        for i in self.colors:
            for j in self.nums:
                self.deck.append(i+' '+j)
        self.deck.append(self.specials[0])
        self.deck.append(self.specials[1])
        random.shuffle(self.deck)
    # deal the initial cards randomly

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

    def chooseLandlord(self, name):
        self.playerDict[name].identity = 'p'
        for card in self.landLordCards:
            self.playerDict[name].cards.append(card)
        self.playerDict[name].cards.sort(key=lambda x: self.sortHelper(x))
    # assign play sequence

    def assignPlayOrder(self):
        if self.p1.identity == 'p':
            self.playOrder = [self.p2.name, self.p3.name]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0, self.p1.name)
        elif self.p2.identity == 'p':
            self.playOrder = [self.p1.name, self.p3.name]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0, self.p2.name)
        elif self.p3.identity == 'p':
            self.playOrder = [self.p1.name, self.p2.name]
            random.shuffle(self.playOrder)
            self.playOrder.insert(0, self.p3.name)
        else:
            self.playOrder = [self.p1.name, self.p2.name, self.p3.name]
            random.shuffle(self.playOrder)
        self.currentPlayer = self.playOrder[0]
    # identify pattern of played card

    def whichPattern(self, selectedCards):
        cardValues = []
        for i in selectedCards:
            if i[-1] == '0':  # special case of 10
                cardValues.append(self.cardOrder['10'])
            else:
                cardValues.append(self.cardOrder[i[-1]])
        pattern = utils.get_move_type(cardValues)
        return pattern
    # check play validity

    def isValidPlay(self, selected):
        selectedCards = sorted(selected,key=lambda x: self.sortHelper(x))
        if self.prevPlay[0] == self.currentPlayer:
            return True
        pattern1 = self.whichPattern(self.prevPlay[1])
        pattern2 = self.whichPattern(selectedCards)
        if pattern2['type'] == 15 or pattern1['type'] == 5:
            return False  # previous kingbomb or current invalid
        elif pattern2['type'] == 5 or pattern1['type'] == 0:
            return True  # current kingbomb or previous pass
        else:
            if pattern1['type'] == pattern2['type'] and\
                    pattern1['rank'] < pattern2['rank']:
                return True
            else:
                return False
    # make a play

    def makePlay(self, selectedCards):
        if selectedCards == [] and self.prevPlay != []:
            pass
        else:
            self.playerDict[self.currentPlayer].playCard(selectedCards)
            self.prevPlay = [self.currentPlayer, selectedCards]
        self.prevPlayer = self.currentPlayer
        playerIndex = self.playOrder.index(self.currentPlayer)
        if playerIndex == 2:
            self.currentPlayer = self.playOrder[0]
        else:
            self.currentPlayer = self.playOrder[playerIndex+1]
    # check who wins

    def checkWin(self):
        if self.playerDict[self.prevPlayer].cards == []:
            if self.playerDict[self.prevPlayer].identity == 'p':
                return 1  # player wins as professor
            else:
                return 2  # player wins as students
        else:
            return 0  # not ended yet

    def createAI(self,name2,name3):
        self.p2 = AI(name2)
        self.p3 = AI(name3)
        self.playerDict[name2] = self.p2
        self.playerDict[name3] = self.p3

    def AIMakePlay(self,name,chosenLandLord):
        AIplayer = self.playerDict[name]
        if chosenLandLord:
            moves = AIplayer.getAllMoves()
            possibleMoves = []
            for move in moves:
                realcards = []
                for card in move:
                    for hand in AIplayer.cards:
                        if hand[-1] == card[-1] and hand not in realcards:
                            realcards.append(hand)
                if self.isValidPlay(realcards):
                    possibleMoves.append(realcards)
            try:
                move = random.choice(possibleMoves)
            except IndexError:
                move = []
            self.makePlay(move)
        else:
            self.chooseLandlord(name)
            self.assignPlayOrder()

class player:
    def __init__(self, name):
        self.name = name
        self.identity = 's'
        self.cards = []
    # make a play

    def playCard(self, selectedCards):
        for i in selectedCards:
            self.cards.remove(i)

class AI:
    def __init__(self, name):
        self.name = name
        self.identity = 's'
        self.cards = []
    # make a play

    def playCard(self, selectedCards):
        for i in selectedCards:
            self.cards.remove(i)
    
    def getAllMoves(self):
        envmoves = utils.MovesGener(self.cards).gen_moves()
        EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
                    13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}
        realmoves = []
        for move in envmoves:
            realmove = []
            for card in move:
                realmove.append(EnvCard2RealCard[card])
            realmoves.append(realmove)
        return realmoves