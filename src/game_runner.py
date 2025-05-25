from game import VerbleGame
from constants import *
from ui.interface import UI

class GameRunner:
    def __init__(self, ui: UI):
        self.ui = ui

    def _handle_hint(self, game: VerbleGame):
        self.ui.display_text()
        self.ui.display_text(HINT_GREETING, INTERACT_COLOR)
        if game.hints == 0:
            self.ui.display_text(NO_HINT_TEXT + " " + HINT_BALANCE(game.hints), INTERACT_COLOR)
        elif game.hints == 1:
            self.ui.display_text(HINT_SMALL_PROMPT, INTERACT_COLOR)
            indices = game.get_hint_indices()
            self.ui.show_hint(indices, game.word)
        else:
            self.ui.display_text(PRICE_TEXT + " " + HINT_BALANCE(game.hints), INTERACT_COLOR)
            self.ui.display_text(HINT_PROMPT, INTERACT_COLOR, end=" ")
            choice = self.ui.get_input("").lower()
            kind = HintKind.big if choice == 'b' else HintKind.small
            indices = game.get_hint_indices(kind)
            self.ui.show_hint(indices, game.word)

    def run(self):
        replay = True
        while replay:
            game = VerbleGame()
            self.ui.reset()
            for msg in (WELCOME, WELCOME_QUESTION, HINT_INFO):
                self.ui.display_text(msg)

            # Main guessing loop
            while not game.is_lost():
                self.ui.display_text()
                guess = self.ui.get_input(GUESS_I(len(game.guesses))).upper()
                if guess == HINTER:
                    self._handle_hint(game)
                    continue

                if not game.is_valid_guess(guess):
                    msg = INVALID_GUESS_TEXT if len(guess) != NUM_LETTERS else UNRECOGNIZED_GUESS_TEXT
                    self.ui.display_text(msg)
                    continue

                validity = game.apply_guess(guess)
                self.ui.show_guess_result(guess, validity)
                if game.is_win(validity):
                    title, color = game.get_title_and_color()
                    for m in ('', WIN_TEXT, '', WIN_TITLE(title)):
                        self.ui.display_text(m, WIN_COLOR if m==WIN_TEXT else color)
                    break
            else:
                # Lost
                for m in ('', LOSE_TEXT, '', LOSE_REVEAL):
                    self.ui.display_text(m, LOSE_COLOR if m==LOSE_TEXT else None)
                self.ui.show_guess_result(game.get_answer(), [True]*NUM_LETTERS)

            # After game
            self.ui.display_text()
            self.ui.show_link(WIKI(game.get_answer()))
            self.ui.display_text()
            replay = self.ui.get_input(AGAIN).lower() == 'y'

        self.ui.display_text()
        self.ui.display_text(THANKS, INTERACT_COLOR)
        self.ui.pause()