import random
import os
import time

class Score:
    WINNING_SCORE = 5

    def __init__(self):
        self._player = 0
        self._computer = 0

    def player_won_game(self):
        return self._player == self.WINNING_SCORE

    def computer_won_game(self):
        return self._computer == self.WINNING_SCORE
    
    def increment_player(self):
        self._player += 1

    def increment_computer(self):
        self._computer += 1

class RPSGame:
    def __init__(self):
        self._human = Human()
        self._computer = None
        self._robot_name = None
        self._score = Score()
        self._robots = (R2D2(), HAL(), Daneel(self._human))
        self._moves = (Rock(), Paper(), Scissors(), Spock(), Lizard())
        self._round_history = []

    def _choose_robot(self):
        self._display_robots()
        choice = input()
        while choice not in [robot.OPTION for robot in self._robots]:
            os.system('clear')
            self._display_robots()
            choice = input('Please enter one of the valid choices: ')

        for robot in self._robots:
            if choice == robot.OPTION:
                self._computer = robot
                self._robot_name = robot.__class__.__name__
                os.system('clear')
                print(f'You are playing against: {self._robot_name}')
                print(f'- {robot.info}')
                time.sleep(4)
                os.system('clear')

    def _display_robots(self):
        for robot in self._robots:
            print(f'Enter "{robot.OPTION}" to play against '
                  f'{robot.__class__.__name__}')

    def _display_welcome_message(self):
        print('Welcome to Rock Paper Scissors!\n')

    def _display_goodbye_message(self):
        os.system('clear')
        print('\nThanks for playing Rock Paper Scissors. Goodbye!')

    def _human_won_round(self):

        human_move = self._human.move
        computer_move = self._computer.move

        for choice in self._moves:
            if human_move == choice and computer_move in choice._wins_against:
                return True

    def _display_scoreboard(self):
        print(f'\nTotal player wins: {self._score._player}\n'
              f'Total {self._robot_name} wins: {self._score._computer}\n')

    def _display_round_winner(self):
        human_move = self._human.move
        computer_move = self._computer.move

        os.system('clear')

        print(f'\nYou chose: {human_move}\n'
              f'{self._robot_name} chose: {computer_move}\n')

        if self._human_won_round():
            self._score.increment_player()
            round_result = f'(You) {human_move.title()} beat {computer_move}'
            print(round_result)
            print('You win the round!')
        elif self._human.move == self._computer.move:
            round_result = 'It\'s a tie.'
            print(round_result)
        else:
            self._score.increment_computer()
            round_result = f'({self._robot_name[0]}) {computer_move.title()} beat {human_move}'
            print(round_result)
            print(f'{self._robot_name} wins the round!')

        self._round_history.append(round_result)
        self._display_scoreboard()
        time.sleep(2)

    def _play_again(self):
        play_again = input('\nEnter "y" if you would like to play again.'
                           ' Press "Enter" if not. ')
        os.system('clear')
        return play_again.lower() == 'y'

    def _game_was_won(self):
        return self._score.player_won_game() or self._score.computer_won_game()
    
    def _display_game_winner(self):
        os.system('clear')
        self._display_scoreboard()

        if self._score.player_won_game():
            print('You won the game!')
        elif self._score.computer_won_game():
            print(f'{self._robot_name} won the game!')
        else:
            print("It's a tie!")

    def _display_move_history(self):
        print('\nWould you like to see the move history?')
        choice = input('Enter "y" to see. Press "Enter" to skip.')
        if choice in ['y', 'Y']:
            os.system('clear')
            counter = 1
            for round in self._round_history:
                print(f'Round {counter}: {round}')
                counter += 1

    def play(self):
        self._display_welcome_message()
        while True:
            self.__init__()
            self._choose_robot()
            while True:
                self._human.choose()
                self._computer.choose()
                self._display_round_winner()
                if self._game_was_won():
                    self._display_game_winner()
                    break
            
            self._display_move_history()
            if not self._play_again():
                break

        self._display_goodbye_message()

class Player:

    def __init__(self):
        self.move = None
        self.move_history = []

class Computer(Player):

    def __init__(self):
        super().__init__()

    def choose(self):
        self.move = random.choice(Move.CHOICES)

class R2D2(Computer):
    OPTION = '1'

    def choose(self):
        self.move = 'rock'

    @property
    def info(self):
        return 'Always chooses rock...'

class HAL(Computer):
    OPTION = '2'

    def choose(self):
        more_scissors = ('scissors', 'scissors', 'scissors', 'scissors')
        self.move = random.choice((Move.CHOICES + more_scissors))

    @property
    def info(self):
        return 'Mostly chooses scissors...'

class Daneel(Computer):
    OPTION = '3'

    def __init__(self, human):
        super().__init__()
        self._human = human

    @property
    def info(self):
        return 'Chooses your last move...'

    def choose(self):
        if len(self._human.move_history) <= 1:
            super().choose()
        else:
            self.move = self._human.move_history[-2]

class Human(Player):
    def __init__(self):
        super().__init__()

    def choose(self):
        while True:
            choice = input(f'Choose {', '.join(Move.CHOICES)}:\n')

            if choice.isalpha():
                choice = choice.lower()
                if choice in Move.CHOICES:
                    break

            print(f'Sorry, {choice} is not valid.')

        self.move = choice
        self.move_history.append(self.move)

class Move:

    CHOICES = ('rock', 'paper', 'scissors', 'lizard', 'spock')

    def __init__(self, wins_against):
        self._wins_against = wins_against

    def __eq__(self, other):
        return other == self.__class__.__name__.lower()

class Rock(Move):
    def __init__(self):
        super().__init__(['scissors', 'lizard'])

class Scissors(Move):
    def __init__(self):
        super().__init__(['paper', 'lizard'])

class Paper(Move):
    def __init__(self):
        super().__init__(['rock', 'spock'])

class Lizard(Move):
    def __init__(self):
        super().__init__(['spock', 'paper'])

class Spock(Move):
    def __init__(self):
        super().__init__(['scissors', 'rock'])

RPSGame().play()

