import cards


class BlackJackCards(cards.Card):
    """ BlackJack cards to be used in this game.
    This class inherits the Card class from the cards module
    """
    ACE_VALUE = 1  # Initial assignment of the Ace values

    @property
    def card_values(self):
        """A property that gets and sets the value of the Black Jack card between 1-10 """
        if self.is_face_up:
            value = BlackJackCards.RANKS.index(self.rank) + 1
            if value > 10:
                value = 10
        else:
            value = None
        return value


class BlackJackDeck(cards.Deck):
    """ A BlackJack Deck that populates the cards into the list from the cards class
        """
    def populate(self):
        """ A method that populates the cards list using the BlackJack Deck class"""
        for suit in BlackJackCards.SUITS:
            for rank in BlackJackCards.RANKS:
                self.cards.append(BlackJackCards(rank, suit))


class BlackJackHand(cards.Hand):
    """ Hand of cards based on the cards"""
    def __init__(self, name):
        super(BlackJackHand, self).__init__()
        self.name = name

    def __str__(self):

        player_total = self.name + ":\t" + super(BlackJackHand, self).__str__()
        if self.total:
            player_total += "(" + str(self.total) + ")"
        return player_total

    @property
    def total(self):
        """A property that get the total value of a card, If the value in the hand has the value of None
        that means the card is face-down, return None """
        for card in self.cards:
            if not card.card_values:
                return None
        # Add of sum of the cards in the if the card value is not None. Treat all Ace as value of 1
        sum_total = 0
        for card in self.cards:
            sum_total += card.card_values

        # Check to see if the hand contains an Ace
        is_ace_found = False
        for card in self.cards:
            if card.card_values == BlackJackCards.ACE_VALUE:
                is_ace_found = True
        # Check to see if sumTotal is less or equal to 11. If sumTotal is less or equal to 11, Treat a as 11
        if is_ace_found and sum_total <= 11:
            # Add only 10 since 1 was initially added as an Ace value
            sum_total += 10
        return sum_total

    def is_busted(self):
        return self.total > 21


class BlackJackPlayer(BlackJackHand):
    """A black jack player"""
    def is_hitting(self):
        answer = UserInput.ask_yes_no("\n" + self.name + ', do you want to hit (Y/N) ')
        return answer == 'y'

    def busted(self):
        print("{} busted".format(self.name))
        self.lose()

    def lose(self):
        print("{} loses".format(self.name))

    def win(self):
        print("{} wins".format(self.name))

    def push(self):
        print("{} pushes".format(self.name))


class BlackJackDealer(BlackJackHand):
    """ A  dealer for the Black Jack Game """
    def is_hitting(self):
        """ checks to see if the dealer is taking another card"""
        return self.total < 17

    def busted(self):
        """ print out a message if the dealer has been busted in the game"""
        print("{} busted".format(self.name))

    def show_first_card(self):
        """Display and flip the first card from the card list"""
        first_card = self.cards[0]
        first_card.flip()


class BlackJackGame(object):
    """A class that create a single object that represents the blackjack game"""
    def __init__(self, names):
        self.players = []
        for name in names:
            player = BlackJackPlayer(name)
            self.players.append(player)

        self.dealer = BlackJackDealer("Dealer")
        self.deck = BlackJackDeck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        """Return the list of players that are still playing. That's, the player has not been busted"""
        current_players = []
        for player in self.players:
            if not player.is_busted():
                current_players.append(player)
        return current_players

    def __add_another_card(self, player):
        """Adds additional cards to either the players or the dealers"""
        # deal the initial two cards to anyone
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.busted()

    def play(self):
        """Deal the first initial two cards to any player"""
        self.deck.deal(self.players+[self.dealer], per_hand=2)
        # Hide the first card in the dealer's hand
        self.dealer.show_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)

        # Deal additional cards to player

        for player in self.players:
            self.__add_another_card(player)
    # Flip the the dealer card to reveal dealer's first card
        self.dealer.show_first_card()

    # If all players have been busted, Show the cards in the dealer hands
        if not self.still_playing:
            print("Dealer wins! You guys are sucked at Black Jack {}".format(self.dealer))

        else:
            # Deal additional cards to dealer since the game is not over yet
            print(self.dealer)
            self.__add_another_card(self.dealer)
            # If the dealer is being busted, everyone wins
            if self.dealer.busted():
                # Because the dealer is being busted, everyone playing the blackjack game wins
                for player in self.still_playing:
                    player.win()
            else:
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        # Remove all cards from the hands of the players and dealers
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print("Welcome to the Black Jack Game!\n")
    names =[]
    number_of_players = UserInput.ask_number("How many players are playing?(2-7)", 2, 8)
    for i in range(number_of_players):
        name = input("Player {} Name : ".format((i+1)))
        names.append(name)
    game = BlackJackGame(names)

    play_again = None
    while play_again != 'n':
        game.play()
        play_again = UserInput.ask_yes_no("Do you want to play again?((Y/N ")


class UserInput(object):
    @staticmethod
    def ask_yes_no(question):
        """Ask a yes or no question."""
        response = None
        while response not in ("y", "n"):
            response = input(question).lower()
        return response

    @staticmethod
    def ask_number(question, low, high):
        """Ask for a number within a range."""
        response = None
        while response not in range(low, high):
            try:
                response = int(input(question))

            except ValueError:
                print("Please enter an integer")
                continue

        return response

if __name__ == '__main__':
    main()








