import json
import os
from collections import defaultdict
from colorama import Fore, Back, Style
from random import choice
# Encase letter in a box
def encase_letter(letter):
    return " " + letter + " "

# Check the validity of the input word
def validate_word(word):
    all_verbs = {}
    with open("words/verbs.txt", "r") as verb_file:
        all_verbs=verb_file.read().splitlines()
    valid = word.lower() in all_verbs
    return valid

def get_random_word():
    freq_verbs = {}
    with open("words/top_verbs.json", "r") as frequent_verbs:
        freq_verbs = json.load(frequent_verbs)
    return choice(list(freq_verbs.keys()))

# Check the validity of the guess
# Letter validity is a list of values that indicate whether each letter in the guess.
# If a letter is in 
#   correct position: True; incorrect position: False; not in the word: None
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

def print_formatted_text(text, letter_validity):
    print()
    for i in range(len(text)):
        if letter_validity[i] == True:
            print(Fore.BLACK + Back.GREEN + encase_letter(text[i]) + Style.RESET_ALL,end="")
        elif letter_validity[i] == False:
            print(Fore.BLACK + Back.YELLOW + encase_letter(text[i]) + Style.RESET_ALL,end="")
        else:
            print(Fore.BLACK + Back.RED + encase_letter(text[i]) + Style.RESET_ALL,end="")
    else:
        print()

def main():
    replay = True
    while replay:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to VERBLE!")
        print("You have 6 attempts to guess the 5-letter verb.")
        word = get_random_word().upper()
        i = 0
        while i < 6:
            guess = input("\nGuess " + str(i+1) + ":").upper()
            if len(guess) != 5:
                print("Invalid guess. Please enter a 5-letter verb.")
                continue
            elif not validate_word(guess):
                print("Invalid guess. Please enter a valid verb.")
                continue
            else:
                i += 1

            validity = check_guess(guess, word)
            print_formatted_text(guess,validity)
            if (all(validity)) == True:
                print("\n"+Fore.BLACK + Back.CYAN +"YOU \nWIN!"+ Style.RESET_ALL+"\n")
                break
        else: 
            print("\n"+Fore.BLACK + Back.MAGENTA +"YOU  \nLOSE!"+ Style.RESET_ALL+"\n")
            print("The word was: ")
            print_formatted_text(word, [True]*len(word))
        replay = input("\nPlay again? (y/n)").lower() == "y"
if __name__ == "__main__":
    main()