from blessed import Terminal
from constants import COLOR_BY_VALIDITY, NUM_LETTERS, HIGHLIGHT
from os import name, system
from ui.interface import UI

class CLI(UI):
    def __init__(self):
        self.term = Terminal()

    def display_text(self, text="", color=None, end="\n"):
        if color:
            bg_attr = f'on_{color.lower()}'
            bg = getattr(self.term, bg_attr, None)
            if bg:
                fg = self.term.black
                print(fg + bg + text + self.term.normal, end=end)
                return
        print(text, end=end)

    def get_input(self, prompt):
        return input(prompt)

    def show_guess_result(self, guess, validity):
        print()
        for i in range(len(guess)):
            color = COLOR_BY_VALIDITY.get(validity[i])
            self.display_text(f" {guess[i]} ", color, end="")
        print()

    def show_hint(self, indices, word):
        display = ["?" for _ in range(NUM_LETTERS)]
        validity = [None] * NUM_LETTERS
        for i in indices:
            display[i] = word[i]
            validity[i] = True
        self.show_guess_result(display, validity)

    def show_link(self, url):
        self.display_text(url, HIGHLIGHT)

    def pause(self):
        input()

    def reset(self):
        system('cls' if name == 'nt' else 'clear')