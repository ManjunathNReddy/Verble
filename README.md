Verble is a basic command line version of Wordle with mostly verbs and a few nouns.

## Installation
- Clone the repo and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- In your terminal, run the command \
    `conda create --name <env> --file requirements.txt`
## Data
The complete list of verbs is derived from the website of [Ashley Bovan](http://www.ashley-bovan.co.uk/words/partsofspeech.html) and the most frequent list of verbs is derived from [Google's N-gram corpus](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html).

## How to play
- Run `python src/main.py` to play the game	
- You have six attempts to guess a five-letter verb which may have multiple instances of the same letter
- After every guess, each letter is marked as either green, yellow or red
    - Green  : letter is correct and in the correct position
    - Yellow : letter is in the answer but not in the right position
    - Red    : letter is not in the answer at all
