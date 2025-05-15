from random import choice, randrange
from collections import defaultdict
from constants import TOP_VERBS, VERBS, NUM_LETTERS, NUM_HINTS, TITLE_BY_GUESSES, COLOR_BY_GUESSES

class VerbleGame:
    def __init__(self):
        self.word = choice(TOP_VERBS).upper()
        self.hints = NUM_HINTS
        self.hint_indices = list(range(NUM_LETTERS))
        self.guesses = []

    def is_valid_guess(self, guess):
        return len(guess) == NUM_LETTERS and guess.lower() in VERBS
    
    # Letter validity indicates how each letter corresponds to the guess:
    #   correct position: True, incorrect position: False, not in the word: None
    def check_guess(self, guess):
        guess = guess.upper()
        validity = [None] * NUM_LETTERS
        # number of matches per letter
        match_count = defaultdict(int)

        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                validity[i] = True
                match_count[letter] += 1

        for i, letter in enumerate(guess):
            if validity[i] is None and letter in self.word:
                if match_count[letter] < self.word.count(letter):
                    validity[i] = False
                    match_count[letter] += 1

        return validity

    def apply_guess(self, guess):
        guess = guess.upper()
        self.guesses.append(guess)
        return self.check_guess(guess)

    def is_win(self, validity):
        return all(v is True for v in validity)

    def is_lost(self):
        return len(self.guesses) >= NUM_LETTERS + 1

    def get_title_and_color(self):
        i = len(self.guesses)
        return TITLE_BY_GUESSES.get(i, TITLE_BY_GUESSES[6]), COLOR_BY_GUESSES.get(i, COLOR_BY_GUESSES[6])

    def get_hint(self, kind="small"):
        if not self.hint_indices or self.hints <= 0:
            return [], self.hints

        if kind == "big" and self.hints >= 2 and len(self.hint_indices) >= 2:
            self.hints -= 2
            return [self.hint_indices.pop(0), self.hint_indices.pop(-1)], self.hints
        else:
            self.hints -= 1
            index = self.hint_indices.pop(randrange(len(self.hint_indices)))
            return [index], self.hints

    def get_answer(self):
        return self.word
