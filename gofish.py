# Original Code Source: https://rosettacode.org/wiki/Go_Fish/Python
# Modified by Derek Stratton on 4/17/2022 for Python 3

import random
from collections import defaultdict

""" Human Player object for Go Fish """
class HumanPlayer(object):
    """ Initializes the human player object. """
    def __init__(self, deck):
        self.hand = defaultdict(int)
        self.book = []
        self.deck = deck  # making a copy of deck, all changes within
        # this class should affect the global deck
        self.score = 0
        self.name = 'Player'

    """ Draws a card from the deck into the player's hand"""
    def Draw(self):  # assuming that deck is a global
        cardDrawn = self.deck.pop()  # removes the last card from deck
        self.hand[cardDrawn] += 1  # adds card to hand
        print('%s drew %s.' % (self.name, cardDrawn))
        self.checkForBooks()

    """ Checks if there are any 4 of a kinds (books) """
    def checkForBooks(self):
        #       Removes all items of which are 4.
        for key, val in list(self.hand.items()):  # can't use iteritems() because we are modifying hand in loop
            if val == 4:  # completed a book
                self.book.append(key)
                print('%s completed the book of %s\'s.' % (self.name, key))
                self.score += 1
                del self.hand[key]
        self.emptyCheck()

    """ Checks if the hand is empty, and draws a card if it is"""
    def emptyCheck(self):
        if len(self.deck) != 0 and len(self.hand) == 0:  # checks if deck/hand is empty
            self.Draw()

    """ Returns a string for displaying the current hand """
    def displayHand(self):  # Displays current hand, cards separated by spaces
        return ' '.join(key for key, val in self.hand.items()
                        for i in range(val))  # meh, make it prettier

    """ Does the player's turn by asking for input """
    def makeTurn(self):
        print('%s\'s hand: %s\nWhat card do you ask for?' % (self.name, self.displayHand()))
        chooseCard = input().strip()
        if chooseCard not in self.hand:
            print('You don\'t have that card. Try again! (or enter quit to exit)')
            chooseCard = self.makeTurn()
        return chooseCard

    """ Gives card if its in the hand, otherwise returns false """
    def fishFor(self, card):
        if card in self.hand:  # if card in hand, returns count and removes the card from hand
            val = self.hand.pop(card)
            self.emptyCheck()
            return val
        else:
            return False

    """ Receives a card and checks for a 4 of a kind """
    def gotCard(self, card, amount):
        self.hand[card] += amount
        self.checkForBooks()


""" Computer Player object for Go Fish """
class Computer(HumanPlayer):
    """ Initializes the cpu object"""
    def __init__(self, deck):
        self.name = 'Computer'
        self.hand = defaultdict(int)
        self.book = []
        self.deck = deck
        self.opponentHas = set()
        self.score = 0

    """ Draws a card from the deck """
    def Draw(self):  # assuming that deck is a global
        cardDrawn = self.deck.pop()  # removes the last card from deck
        self.hand[cardDrawn] += 1  # adds card to hand
        print('%s drew a card.' % (self.name))
        self.checkForBooks()

    """ Makes the computer player's turn by picking a randomly known card """
    def makeTurn(self):
        ##AI: guesses cards that knows you have, then tries cards he has at random.
        ##Improvements: remember if the card was rejected before, guess probabilities
        #        print self.displayHand(),self.opponentHas
        candidates = list(
            self.opponentHas & set(self.hand.keys()))  # checks for cards in hand that computer knows you have
        if not candidates:
            candidates = list(self.hand.keys())  # if no intersection between those two, random guess
        move = random.choice(candidates)
        print('%s fishes for %s.' % (self.name, move))
        return move

    """ Gives card if in the player's hand, otherwise returns false. Updates information for decision making """
    def fishFor(self, card):  # Same as for humans players, but adds the card fished for to opponentHas list.
        self.opponentHas.add(card)
        if card in self.hand:  # if card in hand, returns count and removes the card from hand
            val = self.hand.pop(card)
            self.emptyCheck()
            return val
        else:
            return False

    """ Receives cards from the player """
    def gotCard(self, card, amount):
        self.hand[card] += amount
        self.opponentHas.discard(card)
        self.checkForBooks()



""" Game class that has the main loop for Go Fish """
class PlayGoFish(object):
    """ Initializes the game with the deck and the players """
    def __init__(self):
        self.deck = ('2 3 4 5 6 7 8 9 10 J Q K A ' * 4).split(' ')
        self.deck.remove('')
        random.shuffle(self.deck)
        self.player = [HumanPlayer(self.deck), Computer(self.deck)]  # makes counting turns easier

    """ Checks if the game has ended, based on if there are any cards left in play """
    def endOfPlayCheck(self):  # checks if hands/decks are empty using the any method
        return self.deck or self.player[0].hand or self.player[1].hand

    """ Deals cards to the players """
    def deal_cards(self):
        for i in range(9):  # Deal the first cards
            self.player[0].Draw()
            self.player[1].Draw()

    """ Determines the winner based on the players' scores """
    def determine_winner(self):
        print('\nScores: \n%s: %d\n%s: %d\n' % (self.player[0].name, self.player[0].score,
                                                self.player[1].name, self.player[1].score))
        if self.player[0].score > self.player[1].score:
            print(self.player[0].name, 'won!')
            return 0
        elif self.player[0].score == self.player[1].score:
            print('Draw!')
            return -1
        else:
            print(self.player[1].name, 'won!')
            return 1

    """ The interactions between the two players for fishing for a card """
    def card_interaction(self, whoseTurn, otherPlayer, cardFished):
        result = self.player[otherPlayer].fishFor(cardFished)
        if not result:  # Draws and ends turn
            self.player[whoseTurn].Draw()
            return False
        print('%s got %d more %s.' % (self.player[whoseTurn].name, result, cardFished))
        self.player[whoseTurn].gotCard(cardFished, result)
        return True

    """ The main gameplay loop """
    def play(self):
        self.deal_cards()
        turn = 0
        while self.endOfPlayCheck():
            print('\nTurn %d (%s:%d %s:%d) %d cards remaining.' % (turn, self.player[0].name,
                                                             self.player[0].score, self.player[1].name,
                                                             self.player[1].score, len(self.deck)))
            whoseTurn = turn % 2
            otherPlayer = (turn + 1) % 2
            while True:  # loop until player finishes turn
                cardFished = self.player[whoseTurn].makeTurn()
                if not self.card_interaction(whoseTurn, otherPlayer, cardFished): break
                if not self.endOfPlayCheck(): break
            turn += 1
        self.determine_winner()


if __name__ == "__main__":
    game = PlayGoFish()
    game.play()