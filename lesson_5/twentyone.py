import random
import os
import time

def clear_screen():
    os.system('clear')

def short_wait():
    time.sleep(1.5)

class Card:
    SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    RANKS = {
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10, 
        'Jack': 10,
        'Queen': 10,
        'King': 10,
        'Ace': [1, 11]
    }

    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = self._initialize_deck()

    def _initialize_deck(self):
        return ([Card(rank, suit, value) 
                    for suit in Card.SUITS 
                    for rank, value in Card.RANKS.items()])

    def deal(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

class Player:

    START_MONEY = 5
    RICH = 10
    POOR = 0
    money = START_MONEY

    def __init__(self):
        self.hand = []

    def busted(self):
        return self.score() > TwentyOneGame.TARGET_SCORE

    def score(self):
        return sum([card.value for card in self.hand])
    
    def calculate_aces_in_hand(self):
        ace_cards = [card for card in self.hand if card.rank == 'Ace']
        for card in ace_cards:
            card.value = 11
        for card in ace_cards:
            if self.score() > TwentyOneGame.TARGET_SCORE:
                card.value = 1

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.card_hidden = True

    def display_hand(self):
        if self.card_hidden:

            plural = 's' if len(self.hand) > 2 else ''
            return (f'{self.hand[0].__str__()}' 
                    f' and unknown card{plural}')
        
        return f'{' '.join([str(card) for card in self.hand])}: {self.score()}'

    def reveal_card(self):
        self.card_hidden = False

class Human(Player):
    def __init__(self):
        super().__init__()
    
    def display_hand(self):
        return ', '.join(str(card) for card in self.hand) + f': {self.score()}'

class TwentyOneGame:

    TARGET_SCORE = 21

    def __init__(self):
        self.human = Human()
        self.dealer = Dealer()
        self.deck = Deck()
        self.winner = None

    def start(self):
        self.display_welcome_message()

        while True:

            self.__init__()
            self.deal_initial_cards()
            self.player_turn()
            if self.human.busted():
                print('You busted!')
                self.winner = self.dealer
                short_wait()
            else:
                self.dealer_turn()

            if self.dealer.busted():
                print('Dealer busted!')
                self.winner = self.human
                short_wait()

            self.determine_winner()
            self.pay_up()
            self.display_results()

            if self.reached_money_limit() or not self.play_again():
                break

        self.display_goodbye_message()

    def reached_money_limit(self):
        return self.too_rich() or self.too_poor()

    def too_rich(self):
        return self.human.money == Player.RICH

    def too_poor(self):
        return self.human.money == Player.POOR

    def pay_up(self):
        if self.winner == self.human:
            self.human.__class__.money += 1
        elif self.winner == self.dealer:
            self.human.__class__.money -= 1

    def play_again(self):
        choice = input('\nEnter "y" to play again. Press "Enter" to quit: ')
        if choice.lower() == 'y':
            return True
        else:
            return False

    def display_welcome_message(self):
        clear_screen()
        print('Welcome to Twenty One!\n')
        self.display_money()
        short_wait()

    def display_goodbye_message(self):
        print()
        if self.too_poor():
            print("You don't have enough money to keep playing :(")
        elif self.too_rich():
            print("You're rich enough! Enough playing!")
        else:
            print('Thanks for playing! Bye bye :)')

    def deal_initial_cards(self):
        for _ in range(0, 2):
            for player in [self.human, self.dealer]:
                self.deal_card(player)
    
    def deal_card(self, player):
        card = self.deck.deal()
        player.hand.append(card)
        player.calculate_aces_in_hand()
        return card

    def display_cards(self):
        clear_screen()
        print(f'You have: {self.human.display_hand()}')
        print(f'Dealer has: {self.dealer.display_hand()}')

    def player_turn(self):
        while True:
            self.display_cards()
            choice = input('\nWould you like to hit or stay? (h/s): ')

            if choice.lower() in ['h', 's']:
                match choice.lower():
                    case 'h':
                        print('You hit!\n')
                        print(f'You drew: {self.deal_card(self.human)}')
                        short_wait()

                    case 's':
                        print('You stayed...')
                        short_wait()
                        break

                if self.human.busted():
                    break
            else:
                print('Sorry, that is not a valid choice')
                short_wait()

    def dealer_turn(self):
        self.dealer.reveal_card()
        clear_screen()
        print('Dealer\'s turn...\n')
        short_wait()

        while True:
            self.display_cards()
            print()
            short_wait()

            if self.dealer.score() < 17:
                print('Dealer Hit!\n')
                print(f'Dealer drew: {self.deal_card(self.dealer)}')
                short_wait()
                
            else:
                break
    
    def someone_busted(self):
        return self.dealer.busted() or self.human.busted()

    def determine_winner(self):
        if not self.someone_busted():
            if self.human.score() > self.dealer.score():
                self.winner = self.human
            elif self.human.score() < self.dealer.score():
                self.winner = self.dealer
            else:
                self.winner = None

    def display_results(self):
        self.dealer.reveal_card()
        self.display_cards()

        print()
        if self.winner == self.human:
            print('You won!')
        elif self.winner == self.dealer:
            print('Dealer won!')
        else:
            print('It\'s a tie.')
        
        self.display_money()

    def display_money(self):
        print(f'You have ${self.human.__class__.money}.')

game = TwentyOneGame()
game.start()