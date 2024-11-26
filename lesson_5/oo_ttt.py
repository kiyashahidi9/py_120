import random
import os

class DisplayMixin:

    @staticmethod
    def join_or(elements, sep=', ', last_word='or'):
        elements = [str(element) for element in elements]
        if len(elements) > 1:
            return f'{sep.join(elements[0:-1])} {last_word} {elements[-1]}'
        elif len(elements) == 1:
            return elements[0]
        else:
            return ""
        
    @staticmethod
    def clear_screen():
        os.system('clear')

class Square:
    INITIAL_MARKER = ' '
    HUMAN_MARKER = 'X'
    COMPUTER_MARKER = 'O'

    def __init__(self, marker=INITIAL_MARKER):
        self.marker = marker

    @property
    def marker(self):
        return self._marker 
    
    @marker.setter
    def marker(self, marker):
        self._marker = marker

    def is_unused(self):
        return self.marker == Square.INITIAL_MARKER

    def __str__(self):
        return self.marker

class Board:
    def __init__(self):
        self.squares = {key: Square() for key in range(1, 10)}

    def unused_squares(self):
        return [key for key, square in self.squares.items()
                if square.is_unused()]

    def display(self):
        empty_line = f'     |     |     '
        horizontal_line = f'-----+-----+-----'

        print()
        print(empty_line)
        print(f'  {self.squares[1]}  |'
              f'  {self.squares[2]}  |'
              f'  {self.squares[3]}  ')
        print(empty_line)
        print(horizontal_line)
        print(empty_line)
        print(f'  {self.squares[4]}  |'
              f'  {self.squares[5]}  |'
              f'  {self.squares[6]}  ')
        print(empty_line)
        print(horizontal_line)
        print(empty_line)
        print(f'  {self.squares[7]}  |'
              f'  {self.squares[8]}  |'
              f'  {self.squares[9]}  ')
        print(empty_line)
        print()

    def mark_square_at(self, key, marker):
        self.squares[key].marker = marker

    def is_full(self):
        return self.unused_squares() == []
    
    def count_markers_for(self, player, keys):
        markers = [self.squares[key].marker for key in keys]
        return markers.count(player.marker)

class Player:
    def __init__(self, marker):
        self.marker = marker

    @property
    def marker(self):
        return self._marker
    
    @marker.setter
    def marker(self, marker):
        self._marker = marker

class Human(Player):
    def __init__(self):
        super().__init__(Square.HUMAN_MARKER)

class Computer(Player):
    def __init__(self):
        super().__init__(Square.COMPUTER_MARKER)

class TTTGame(DisplayMixin):

    POSSIBLE_WINNING_ROWS = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    )

    def __init__(self):
        self.board = Board()
        self.human = Human()
        self.computer = Computer()

    def play(self):
        # SPIKE
        self.display_welcome_message()

        while True:
            self.board.display()

            self.human_moves()
            self.clear_screen()
            if self.is_game_over():
                break

            self.computer_moves()
            self.clear_screen()
            if self.is_game_over():
                break
        
        self.board.display()
        self.display_results()
        self.display_goodbye_message()
    
    def display_welcome_message(self):
        self.clear_screen()
        print('Welcome to Tic Tac Toe!')

    def display_goodbye_message(self):
        print('Thanks for playing Tic Tac Toe! Goodbye :)')

    def display_results(self):
        if self.is_winner(self.human):
            print('You won! Congratulations!')
        elif self.is_winner(self.computer):
            print('I won! I won! Take that, human!')
        else:
            print('A tie game. How boring.')

    def is_winner(self, player):
        for row in TTTGame.POSSIBLE_WINNING_ROWS:
            if self.three_in_a_row(player, row):
                return True
        
        return False

    def human_moves(self):
        while True:
            valid_choices = self.board.unused_squares()
            choices_list = self.join_or([str(num) for num in valid_choices])
            choice = input(f'Choose a square: ({choices_list}) ')

            try:
                choice = int(choice)
            except ValueError:
                pass
            else:
                if choice in valid_choices:
                    break

            print('Sorry, that\'s not a valid choice\n')

        self.board.mark_square_at(choice, self.human.marker)

    def computer_moves(self):
        valid_choices = self.board.unused_squares()
        choice = random.choice(valid_choices)
        self.board.mark_square_at(choice, self.computer.marker)

    def is_game_over(self):
        return self.board.is_full() or self.someone_won()
    
    def someone_won(self):
        return (self.is_winner(self.human) or 
                self.is_winner(self.computer))
    
    def three_in_a_row(self, player, row):
        return self.board.count_markers_for(player, row) == 3

game = TTTGame()
game.play()