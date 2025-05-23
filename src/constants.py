import json
import sys
from pathlib import Path
from random import choice
from enum import Enum

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
HINT_GREETING = "KONNICHIWA!"
NO_HINT_TEXT = f"IYA, {HINTER} can't HELP!"
PRICE_TEXT = "[PRICE: Big : 2 , Small : 1]"
HintKind = Enum('Hint', ['small', 'big'])
HINT_TYPE_BIG = "big"
HINT_PROMPT = f"HAI, {HINTER} can HELP! Big HINT [b] / Small HINT [s]? [b/s]"
HINT_SMALL_PROMPT = f"HAI, {HINTER} can HELP with Small HINT!"
WELCOME = "Welcome to VERBLE, the ultimate verb guessing game!"
WELCOME_QUESTION = f"Can you guess the {NUM_LETTERS}-letter verb in {NUM_GUESSES} shots?"
HINT_INFO = f"Call {HINTER} for Hints!"
INVALID_GUESS_TEXT = f"Nope! Please enter a {NUM_LETTERS}-letter VERB!"
UNRECOGNIZED_GUESS_TEXT = "That's obscure! Please enter a VERB."
LOSE_REVEAL = "The word was: "
WIN_TEXT = "YOU WIN!"
LOSE_TEXT = "YOU LOSE!"
AGAIN = "Play again? [y/n] "
THANKS = "Thanks for playing VERBLE!"
HINT_BALANCE = lambda hints: f"[hints left: {hints}]"
GUESS_I = lambda i: f"Guess {i+1}:"
WIN_TITLE = lambda title: f"Congrats! You're a {title} of VERBLE!"
WIKI = lambda word: f"https://en.wiktionary.org/wiki/{word.lower()}#Verb"

TITLE_BY_GUESSES = { 1: "Master", 2: "Wizard", 3: "Mage", 4: "Warrior", 5: "Knight", 6: "Journeyman" }

# 0 guesses = win, -1 guesses = lose
COLOR_BY_GUESSES = { -1: 'red', 0: 'blue', 1: 'cyan', 2: 'orange', 3: 'purple', 4: 'lightseagreen', 5: 'green', 6: 'snow' }    
COLOR_BY_VALIDITY = { True: 'green', False: 'yellow', None: 'red' }
WIN_COLOR = COLOR_BY_GUESSES[0]
LOSE_COLOR = COLOR_BY_GUESSES[-1]
INTERACT_COLOR = 'magenta'
HIGHLIGHT = 'yellow'