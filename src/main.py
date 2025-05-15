from game import VerbleGame
from constants import *
from ui.cli import CLI

def play():
    ui = CLI()
    replay = True

    while replay:
        game = VerbleGame()

        ui.display_text(WELCOME)
        ui.display_text(WELCOME_QUESTION)
        ui.display_text(HINT_INFO)
        ui.display_text("")

        while not game.is_lost():
            guess = ui.get_input(GUESS_I(len(game.guesses))).upper()

            if guess == HINTER:
                ui.display_text(HINT_GREETING, INTERACT_COLOR)
                if game.hints == 0:
                    ui.display_text(NO_HINT_TEXT + " " + HINT_BALANCE(game.hints), INTERACT_COLOR)
                elif game.hints == 1:
                    ui.display_text(HINT_SMALL_PROMPT, INTERACT_COLOR)
                    indices, _ = game.get_hint()
                    ui.show_hint(indices, game.word)
                else:
                    ui.display_text(PRICE_TEXT + " " + HINT_BALANCE(game.hints), INTERACT_COLOR)
                    ui.display_text(HINT_PROMPT, INTERACT_COLOR)
                    hint_type = ui.get_input("").lower()
                    indices, _ = game.get_hint("big" if hint_type == "b" else "small")
                    ui.show_hint(indices, game.word)
                continue

            if not game.is_valid_guess(guess):
                msg = INVALID_GUESS_TEXT if len(guess) != NUM_LETTERS else UNRECOGNIZED_GUESS_TEXT
                ui.display_text(msg)
                continue

            validity = game.apply_guess(guess)
            ui.show_guess_result(guess, validity)

            if game.is_win(validity):
                title, color = game.get_title_and_color()
                ui.display_text("")
                ui.display_text(WIN_TEXT, WIN_COLOR)
                ui.display_text("")
                ui.display_text(WIN_TITLE(title), color)
                break

        else:
            ui.display_text("")
            ui.display_text(LOSE_TEXT, LOSE_COLOR)
            ui.display_text("")
            ui.display_text(LOSE_REVEAL)
            ui.show_guess_result(game.get_answer(), [True] * NUM_LETTERS)

        ui.display_text("")
        ui.show_link(WIKI(game.get_answer()))
        ui.display_text("")

        replay = ui.get_input(AGAIN).lower() == "y"

    ui.display_text("")
    ui.display_text(THANKS, INTERACT_COLOR)
    ui.pause()

if __name__ == "__main__":
    play()