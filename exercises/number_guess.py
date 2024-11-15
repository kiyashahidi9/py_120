import random
import math

class GuessingGame:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.num_range = range(start, stop + 1)
        self.correct_num = random.choice(self.num_range)
        self.guesses_remaining = int(math.log2(stop - start + 1)) + 1
        self.is_correct_guess = False

    def play(self):
        self.__init__(self.start, self.stop)

        while True:

            if self.guesses_remaining == 0:
                self._game_lost()
                break

            self._display_remaining_guesses()

            guess = self._user_guess()

            if self._determine_if_correct(guess):
                print("That's the number!")
                self._game_won()
                break

            self._lost_round(guess)
            

    def _user_guess(self):

        while True:
            guess = input(f'Enter a number between {self.num_range[0]} and {self.num_range[-1]}: ')

            if guess.isdigit() and int(guess) in self.num_range:
                return int(guess)
            else:
                print('Invalid Guess.')

    def _display_remaining_guesses(self):
        print(f'\nYou have {self.guesses_remaining} guesses remaining.')

    def _determine_if_correct(self, guess):
        if guess == self.correct_num:
            return True

        return False

    def _display_comparison(self, guess):
        if guess > self.correct_num:
            print('Your guess is too high')
        else:
            print('Your guess is too low')

    def _lost_round(self, guess):
        self.guesses_remaining -= 1
        self._display_comparison(guess)

    def _game_lost(self):
        print('\nYou have no more guesses. You lost!')

    def _game_won(self):
        print('\nYou won!')

game = GuessingGame(501, 1500)
game.play()