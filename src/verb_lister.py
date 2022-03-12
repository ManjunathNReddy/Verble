# Create verb files to be used by the game

import json
from operator import itemgetter

verb_list = []
with open("words/31K verbs.txt", "r") as all_verbs:
    verb_list = all_verbs.read().splitlines()

# Only keep 5 letter words
verb_list = [verb for verb in verb_list if len(verb) == 5]
# Remove the words with dashes and apostrophes
verb_list = [verb for verb in verb_list if '-' not in verb and "'" not in verb]

# Save the list to txt file
with open("words/verbs.txt", "w") as verbs_file:
    verbs_file.write('\n'.join(verb_list))

freq_verbs = {}
with open("words/frequent.json", "r") as frequent_verbs:
    freq_verbs = json.load(frequent_verbs)

# Get common words
common_words = list(set(freq_verbs.keys()) & set(verb_list))

# Save top 500 common words sorted by frequencies to a file
common_word_dict = dict((k, freq_verbs[k]) for k in common_words if k in freq_verbs)
common_word_dict = dict(sorted(common_word_dict.items(), key=itemgetter(1), reverse=True)[:500])

with open("words/top_verbs.json", "w") as common_words_file:
    json.dump(common_word_dict, common_words_file)
