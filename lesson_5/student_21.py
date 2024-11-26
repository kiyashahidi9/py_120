""" OO Twenty One Game"""
import random
import os
import sys

def clear_screen():
    """Clear screen """
    os.system('clear')

class Card:
    """Card Class"""
    SUITS = ("\u2663", "\u2665",
         "\u2666", "\u2660")
    RANKS = ('A', '2', '3', '4', '5',
         '6', '7', '8', '9', '10',
         'J', 'Q', 'K')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self._hidden = False

    def get_value(self):
        """Determine card value"""
        if self.is_face_card():
            return 10
        if self.is_ace():
            return 11
        return int(self.rank)

    def is_ace(self):
        """Determine card if ace"""
        return self.rank == 'A'

    def is_face_card(self):
        """Determine card if J, Q, K """
        return self.rank in ['J', 'Q', 'K']

    def hide(self):
        """Hide card"""
        self._hidden = True

    def reveal(self):
        """Reveal card"""
        self._hidden = False

    @property
    def hidden(self):
        """Getter for hidden variable"""
        return self._hidden

    def display(self):
        """Return visual representation of a single card"""
        if self.hidden:
            rank, suit = "?", "?"
        else:
            rank, suit = self.rank, self.suit

        space = ' ' * (6 if rank != '10' else 5)

        rank_line1 = f"| {rank}{space} |"
        empty_line = "|         |"
        suit_line = f"|    {suit}    |"
        empty_line = "|         |"
        rank_line2 = f"| {space}{rank} |"

        return rank_line1, empty_line, suit_line, empty_line, rank_line2

class Deck:
    """Deck Class"""
    def __init__(self):
        self.cards = [Card(rank, suit)
                for suit in Card.SUITS
                for rank in Card.RANKS]

        self.shuffle_deck()

    def shuffle_deck(self):
        """Shuffle deck"""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deal a card"""
        return self.cards.pop()

class Hand:
    """Hand Class"""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Add a card"""
        self.cards.append(card)

    def get_hand_total(self):
        """Get total of cards in hand"""
        total = sum(card.get_value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.is_ace())

        while total > TwentyOneGame.TARGET_SCORE and aces:
            total -= 10
            aces -= 1

        return total

    def is_busted(self):
        """Check if hand total is greater than target score"""
        return self.get_hand_total() > TwentyOneGame.TARGET_SCORE

    def reveal_cards(self):
        """Reveal card"""
        for card in self.cards:
            card.reveal()

    def reset(self):
        """Reset cards"""
        self.cards = []

    def __str__(self):
        return self.display_cards()

    def display_cards(self):
        """ Display cards in hand"""
        buffer = ' ' * 3
        card_line = (buffer + '+---------+') * len(self.cards)
        rank_line1 = empty_line1 = suit_line = empty_line2 = rank_line2 = ''

        for card in self.cards:
            r1, e1, s, e2, r2 = card.display()
            rank_line1 += buffer + r1
            empty_line1 += buffer + e1
            suit_line += buffer + s
            empty_line2 += buffer + e2
            rank_line2 += buffer + r2

        result = "\n".join([card_line, rank_line1,
                            empty_line1, suit_line,
                            empty_line2, rank_line2,
                            card_line])

        return result

class Participant:
    """Participant Class: Shared behavior between Player and Dealer"""
    def __init__(self):
        self.hand = Hand()

    def draw_card(self, deck):
        """Draw a card from the deck"""
        self.hand.add_card(deck.deal_card())

    def is_busted(self):
        """Check if participant busted"""
        return self.hand.is_busted()

    @property
    def hand_total(self):
        """Get total hand score"""
        return self.hand.get_hand_total()

    def show_hand(self):
        """Print the hand"""
        print(self.hand)

    def reveal_hand(self):
        """Reveal all hidden cards"""
        self.hand.reveal_cards()

    def reset_hand(self):
        """Reset the hand for a new round"""
        self.hand.reset()

class Wallet:
    """Wallet Class: Manages player's money. """
    INITIAL_AMOUNT = 5
    WINNING_AMOUNT = 10

    def __init__(self):
        self.money = Wallet.INITIAL_AMOUNT

    def adjust(self, amount):
        """Adjust player's money by a given amount."""
        self.money += amount

    def display(self):
        """Display player's current money."""
        print(f"\nYou have ${self.money}.")

    def is_bankrupt(self):
        """Check if player is bankrupt."""
        return self.money == 0

    def has_won(self):
        """Check if player has reached winning amount."""
        return self.money == Wallet.WINNING_AMOUNT

class Player(Participant):
    """Player Class: Inherits Participant with wallet management."""
    def __init__(self):
        super().__init__()
        self.wallet = Wallet()

    def adjust_money(self, amount):
        """Delegate money adjustment to Wallet."""
        self.wallet.adjust(amount)

    def display_money(self):
        """Delegate display of money to Wallet."""
        self.wallet.display()

    def is_bankrupt(self):
        """Delegate bankrupt check to Wallet."""
        return self.wallet.is_bankrupt()

    def has_won(self):
        """Delegate win check to Wallet."""
        return self.wallet.has_won()

class Dealer(Participant):
    """Dealer Class: Extends Participant with specific dealer logic"""
    DEALER_MUST_STAY_SCORE = 17

    def should_hit(self):
        """Determine if dealer should hit based on hand score"""
        return self.hand_total < Dealer.DEALER_MUST_STAY_SCORE

    def hide_second_card(self):
        """Hide dealer's second card"""
        if len(self.hand.cards) > 1:
            self.hand.cards[1].hide()

class Scoreboard:
    """Scoreboard Class"""
    def __init__(self):
        self.scores = {'You': 0, 'Dealer': 0}

    def update_score(self, winner):
        """Update the score for the winner"""

        if winner in self.scores:
            self.scores[winner] += 1

    def __str__(self):
        return '\n'.join([f"{key}: {value}" for key, value in self.scores.items()])

class UserInterface:
    """Handles displaying messages, menus, and input."""
    @staticmethod
    def display_welcome_message():
        """Display welcome message"""
        clear_screen()
        print(f"Welcome to {TwentyOneGame.TARGET_SCORE}! Let's get started!")

    @staticmethod
    def display_goodbye_message():
        """Display goodbye message when exiting the game"""
        print("Thanks for playing! Goodbye.")

    @staticmethod
    def display_instructions():
        """Display game instructions"""
        clear_screen()
        print(f"The goal is to get as close to "
              f"{TwentyOneGame.TARGET_SCORE} as possible without going over.")
        print("Each player starts with 2 cards. "
              "One of the dealer's cards will be hidden.")
        print("On your turn, you can choose:")
        print("  - 'Hit' to get another card.")
        print("  - 'Stay' to keep your current hand.")
        print(f"If your total exceeds {TwentyOneGame.TARGET_SCORE}, "
              f"you 'bust' and lose automatically.")        
        print(f"The dealer will hit until reaching "
              f"at least {Dealer.DEALER_MUST_STAY_SCORE}.\n")
        print(f"Each bet costs $1. You start with ${Wallet.INITIAL_AMOUNT}.")
        print("Try to manage your money and avoid losing everything.")
        print("Game ends when you have no money left or you have $10.\n")
        print("Good luck!")

class TwentyOneGame:
    """Twenty One Game Class"""
    TARGET_SCORE = 21
    BUST_MSG = "You busted!"
    DEALER_BUSTS_MSG = "Dealer busted! You win!"
    DEALER_WINS_MSG = "Dealer wins!"
    PLAYER_WINS_MSG = "You win!"
    TIE_MSG = "It's a tie!"

    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.scoreboard = Scoreboard()
        self.ui = UserInterface()

    def start(self):
        """Start the game loop"""
        self.ui.display_welcome_message()
        self.display_main_menu()
        while not self.is_game_over():
            self.play_one_round()
            if self.is_game_over():
                break
            if not self.play_again():
                break
        self.ui.display_goodbye_message()

    def play_one_round(self):
        """Play a single round"""
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.deck = Deck()
        self.deal_initial_cards()
        clear_screen()
        self.player_turn()

        if not self.player.is_busted():
            self.dealer_turn()

        self.display_round_result()
        self.display_scoreboard()

    def deal_initial_cards(self):
        """Deal 2 cards to both player and dealer"""
        for _ in range(2):
            self.player.draw_card(self.deck)
            self.dealer.draw_card(self.deck)
        self.dealer.hide_second_card()

    def show_cards(self):
        """Show both player's and dealer's hands"""
        print(f"Dealer's hand: ({self.display_dealer_total()})")
        print(self.dealer.hand)

        print(f"\nYour hand: ({self.display_player_total()})")
        print(self.player.hand)

    def player_turn(self):
        """Handle player's turn"""
        while True:
            clear_screen()
            self.show_cards()
            self.player.display_money()
            print()

            choice = self.get_player_choice()

            if choice == 'q':
                self.ui.display_goodbye_message()
                sys.exit()
            elif choice == 'h':
                self.player.draw_card(self.deck)
                if self.player.is_busted():
                    self.handle_bust(self.player)
                    break
            elif choice == 's':
                break

    def get_player_choice(self):
        """Get the player's selection (hit, stay, quit)"""
        while True:
            choice = input("Press (H) for hit, "
                               "(S) for stay, or (Q) to quit: ").lower()
            if choice in ['h', 's', 'q']:
                return choice
            input("Invalid choice. Press Enter to try again: ")

    def dealer_turn(self):
        """Handle the dealer's turn"""
        clear_screen()
        print("Dealer's turn... ")
        self.dealer.reveal_hand()
        self.dealer.show_hand()

        while self.dealer.should_hit():
            print("Dealer hits...")
            self.dealer.draw_card(self.deck)
            self.dealer.show_hand()

            if self.dealer.is_busted():
                self.handle_bust(self.dealer)
                return

        print("Dealer stays.")

    def handle_bust(self, participant):
        """Handle bust scenario"""
        if isinstance(participant, Player):
            print("\nYou busted! Dealer wins.")
        elif isinstance(participant, Dealer):
            print("\nDealer busted! You win.")

    def display_dealer_total(self):
        """Display the total for dealer's revealed cards"""
        revealed_cards = [card for card in self.dealer.hand.cards if not card.hidden]
        total = sum(card.get_value() for card in revealed_cards)
        return str(total)

    def display_player_total(self):
        """Display the total of the player's hand"""
        return f"{self.player.hand_total}"

    def display_round_result(self):
        """Display the result of the current round"""
        clear_screen()
        self.show_cards()

        if self.player.is_busted():
            print(f"\n{self.BUST_MSG}")
            self.player.adjust_money(-1)
            self.scoreboard.update_score('Dealer')
        elif self.dealer.is_busted():
            print(f"\n{self.DEALER_BUSTS_MSG}")
            self.player.adjust_money(1)
            self.scoreboard.update_score('You')
        elif self.dealer.hand_total > self.player.hand_total:
            print(f"\n{self.DEALER_WINS_MSG}")
            self.player.adjust_money(-1)
            self.scoreboard.update_score('Dealer')
        elif self.player.hand_total > self.dealer.hand_total:
            print(f"\n{self.PLAYER_WINS_MSG}")
            self.player.adjust_money(1)
            self.scoreboard.update_score('You')
        else:
            print(f"\n{self.TIE_MSG}")

        self.player.display_money()

    def play_again(self):
        """Ask the player if they want to play another round"""
        print()
        while True:
            choice = input("Do you want to play again (y/n): ").lower()
            if choice in ['y', 'yes']:
                return True
            if choice in ['n', 'no']:
                return False
            print("Invalid input. Please press 'y' for yes or 'n' for no.")

    def is_game_over(self):
        """check if the game should end"""
        if self.player.is_bankrupt():
            print("\nYou have no money left! Game over.")
            return True
        if self.player.has_won():
            print("\nYou reached $10! You win!")
            return True
        return False

    def display_main_menu(self):
        """Display main menu for game"""
        while True:
            options = [
            "(S) Start Game",
            "(I) Instructions", 
            "(Q) Quit"
        ]

            banner_width = max(len(option) for option in options) + 4

            print(f"\n+{'-' * banner_width}+")
            print(f"| Menu{' ' * (banner_width - len('Menu') - 1)}|")
            print(f"+{'-' * banner_width}+")
            for option in options:
                print(f"| {option.ljust(banner_width - 2)} |")
            print(f"+{'-' * banner_width}+")

            answer = input("\nChoose an option: ").lower()
            if answer == 's':
                return
            if answer == 'i':
                self.ui.display_instructions()
                continue
            if answer == 'q':
                self.ui.display_goodbye_message()
                sys.exit()

            print("\nInvalid choice, please try again.")

    def display_scoreboard(self):
        """Display the scoreboard"""
        print("\n+--------------------+")
        print(f"| Scoreboard{' ' * (19 - len('Scoreboard'))}|")
        print("+--------------------+")
        for key, value in self.scoreboard.scores.items():
            print(f"| {key}: {value}{' ' * (19 - len(f'{key}: {value}'))}|")
        print("+--------------------+")

game = TwentyOneGame()
game.start()