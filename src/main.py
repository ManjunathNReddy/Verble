import json
import os
import sys
from collections import defaultdict
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from random import choice, randrange
from pathlib import Path
colorama_init(autoreset=True)

# |CONSTANTS| #

WORDS_PATH = None
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    WORDS_PATH = Path(sys._MEIPASS) / "words"
else:
    # Running in a normal Python environment
    WORDS_PATH = Path(__file__).resolve().parent.parent / "words"


# Load words : top verbs for choosing and all verbs for checking
TOP_VERBS, VERBS = [], []
with open(WORDS_PATH /"top_verbs.json", "r") as frequent_verbs:
    freq_verbs = json.load(frequent_verbs)
    TOP_VERBS = list(freq_verbs.keys())
with open(WORDS_PATH / "verbs.txt", "r") as verb_file:
        VERBS=verb_file.read().splitlines()

# |SETTINGS| #

# NUM_LETTERS must match length of words in the verb list
NUM_LETTERS = 5
NUM_GUESSES = NUM_LETTERS + 1
NUM_HINTS = NUM_LETTERS//2

NAMES = ['KENTO', 'TOSHY', 'TATSO', 'SHINO', 'AKIYO', 'KYOKO', 'EMIKO', 'YUKIY', 'RIEKO', 'KAORY']
HINTER = choice(NAMES)
END_T = HINTER[-1]
HINT_GREETING = "KONNICHIWA!"
HINT_ANGRY = f"NANI? {HINTER} angry!"
NO_HINT_TEXT = f"IYA, {HINTER} no HELP-{END_T}!"
PRICE_TEXT = "[PRICE: Big : 2 , Small : 1]"
HINT_PROMPT = f"HAI, {HINTER} HELP-{END_T}! Big HINT-{END_T} [b] / Small HINT-{END_T} [s]? [b/s]"
WELCOME = "Welcome to VERBLE, the ultimate verb guessing game!"
WELCOME_QUESTION = f"Can you guess the {NUM_LETTERS}-letter verb in {NUM_GUESSES} shots?"
HINT_INFO = f"Call {HINTER} for Hints!"
INVALID_GUESS_TEXT = f"Nope! Please enter a {NUM_LETTERS}-letter VERB."
UNRECOGNIZED_GUESS_TEXT = "That's obscure! Please enter a VERB."
LOSE_REVEAL = "The word was: "
WIN_TEXT = "YOU WIN!"
LOSE_TEXT = "YOU LOSE!"
AGAIN = "Play again? [y/n]"
THANKS = "Thanks for playing VERBLE!"
HINT_BALANCE = lambda hints: f"[hints left: {hints}]"
GUESS_I = lambda i: f"Guess {i+1}:"
WIN_TITLE = lambda title: f"Congrats! You're a {title} of VERBLE!"
WIKI = lambda word: f"https://en.wiktionary.org/wiki/{word.lower()}#Verb"

TITLE_BY_GUESSES = { 1: "Master", 2: "Wizard", 3: "Mage", 4: "Warrior", 5: "Knight", 6: "Journeyman" }

# 0 guesses = win, -1 guesses = lose
COLOR_BY_GUESSES = { -1: Back.RED, 0: Back.BLUE, 1: Back.MAGENTA, 2: Back.CYAN, 3: Back.CYAN, 4: Back.GREEN, 5: Back.GREEN, 6: Back.WHITE }
COLOR_BY_VALIDITY = { True: Back.GREEN, False: Back.YELLOW, None: Back.RED }
WIN_COLOR = COLOR_BY_GUESSES[0]
LOSE_COLOR = COLOR_BY_GUESSES[-1]
INTERACT_COLOR = Fore.MAGENTA
FORE_COLOR = Fore.BLACK
HIGHLIGHT = Fore.YELLOW

# |HELPERS| #

def get_random_word():
    return choice(TOP_VERBS)

def get_hint_balance(hints):
    return HINT_BALANCE(hints)

def encase_letter(letter):
    return f" {letter} " 

def print_color_text(text, color, end="\n"):
    print(FORE_COLOR + color + text, end=end)

def print_formatted_text(text, letter_validity):
    print()
    for i in range(len(text)):
        print_color_text(encase_letter(text[i]), COLOR_BY_VALIDITY[letter_validity[i]],end="")
    else:
        print()

def print_formatted_hint(expose_indices,word):
    letter_validity = [True if i in expose_indices else None for i in range(NUM_LETTERS) ]
    text = [word[i] if i in expose_indices else "?" for i in range(NUM_LETTERS)]
    print_formatted_text(text, letter_validity)

def print_small_hint(hint_index,word):
    index = hint_index.pop(randrange(len(hint_index)))
    print_formatted_hint([index], word)

def print_big_hint(hint_index,word):
    first, last = hint_index.pop(0), hint_index.pop(-1)
    print_formatted_hint([first,last], word)

# Check validity of the guess
# Letter validity indicates how each letter corresponds to the guess:
#   correct position: True, incorrect position: False, not in the word: None
def check_guess(guess, word):
    letter_validity = []
    # Dictionary with number of matches per letter
    matched_by_letter = defaultdict(lambda: 0)
    for i in range(len(word)):
        if guess[i] == word[i]:
            letter_validity.append(True)
            matched_by_letter[word[i]] +=1
        else:
            letter_validity.append(None)

    # Set the letter validity for wrongly placed letters
    for i in range(len(word)):
        if letter_validity[i] == None and guess[i] in word:
            if matched_by_letter[guess[i]] < word.count(guess[i]):
                letter_validity[i] = False
                matched_by_letter[guess[i]] +=1
    return letter_validity

def ask_hinter(hints, hint_index, word): 
    print_color_text(HINT_GREETING,INTERACT_COLOR, end=" ")     
    if hints == 0:
        print_color_text(NO_HINT_TEXT+" "+get_hint_balance(hints), INTERACT_COLOR)
    else:
        print_color_text(PRICE_TEXT+" "+get_hint_balance(hints), INTERACT_COLOR)
        print_color_text(HINT_PROMPT, INTERACT_COLOR, end=" ")
        hint_type = input().lower()
        if hint_type == "b":
            hints -= 2
            if hints < 0:
                hints = 0
                print_color_text(HINT_ANGRY+" "+get_hint_balance(hints), INTERACT_COLOR)
            else:
                print_big_hint(hint_index, word)          
        else:
            hints -= 1
            print_small_hint(hint_index, word)
    return hints

# |GAME LOOP| #
def play():
    replay = True
    while replay:
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print welcome message
        for prompt in [WELCOME, WELCOME_QUESTION, HINT_INFO]:
            print(prompt)
        print()
        hint_index = list(range(NUM_LETTERS))
        word = get_random_word().upper()
        i = 0
        hints = NUM_HINTS
        while i < NUM_GUESSES:
            print()
            guess = input(GUESS_I(i)).upper()
            if guess == HINTER:
                hints = ask_hinter(hints,hint_index,word)               
                continue

            if len(guess) != NUM_LETTERS:
                print(INVALID_GUESS_TEXT)
                continue
            elif not guess.lower() in VERBS:
                print(UNRECOGNIZED_GUESS_TEXT)
                continue
            else:
                i += 1
            
            validity = check_guess(guess, word)
            print_formatted_text(guess,validity)
            if (all(validity)) == True:
                title = TITLE_BY_GUESSES.get(i, TITLE_BY_GUESSES[6])
                color = COLOR_BY_GUESSES.get(i, TITLE_BY_GUESSES[6])
                print()
                print_color_text(WIN_TEXT,WIN_COLOR)
                print()
                print_color_text(WIN_TITLE(title),color)
                break
        else: 
            print()
            print_color_text(LOSE_TEXT,LOSE_COLOR)
            print()
            print(LOSE_REVEAL)
            print_formatted_text(word, [True]*len(word))
        print()
        print_color_text(WIKI(word), HIGHLIGHT)
        print()
        replay = input(AGAIN).lower() == "y"
    print()
    print_color_text(THANKS, INTERACT_COLOR)
    input()

if __name__ == "__main__":
    play()