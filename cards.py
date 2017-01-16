# I got some help doing this game using the book python programming for absolute beginner
class Card(object):

    """ A playing card. """
    RANKS = ["Ace", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "Jack", "Queen", "King"]
    SUITS = ["Club", "Diamond", "Hearts", "Spades"]

    def __init__(self, rank, suit, is_face_up=True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = is_face_up

    def __str__(self):
        if self.is_face_up:
            display_card = self.rank + " of " + self.suit
        else:
            display_card = "Card Face Down"
        return display_card

    def flip(self):
        self.is_face_up = not self.is_face_up


class Hand(object):
    """ A hand of playing cards. """

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            playing_card = ""
            for card in self.cards:
                playing_card += str(card) + "\t"
        else:
            playing_card = "There is no cards left to be played"
        return playing_card

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)


class Deck(Hand):
    """ A deck of playing cards. """

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand=1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print("Can't continue deal. Out of cards!")

