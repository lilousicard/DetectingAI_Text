import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Map NLTK's POS tags to a more readable format or type
pos_map = {
    'NN': 'Noun', 'NNS': 'Noun', 'NNP': 'Proper noun', 'NNPS': 'Proper noun',
    'VB': 'Verb', 'VBD': 'Verb', 'VBG': 'Verb', 'VBN': 'Verb', 'VBP': 'Verb', 'VBZ': 'Verb',
    'JJ': 'Adjective', 'JJR': 'Adjective', 'JJS': 'Adjective',
    'RB': 'Adverb', 'RBR': 'Adverb', 'RBS': 'Adverb',
    'IN': 'Preposition', 'DT': 'Determiner', 'PRP': 'Pronoun', 'PRP$': 'Possessive pronoun',
    'CC': 'Conjunction', 'CD': 'Cardinal number', 'EX': 'Existential there', 'FW': 'Foreign word',
    'MD': 'Modal', 'PDT': 'Predeterminer', 'POS': 'Possessive ending', 'RP': 'Particle',
    'SYM': 'Symbol', 'TO': 'To', 'UH': 'Interjection', 'WDT': 'Wh-determiner',
    'WP': 'Wh-pronoun', 'WP$': 'Possessive wh-pronoun', 'WRB': 'Wh-adverb',
    ',': 'Comma', '.': 'Dot', ':': 'Colon', ';': 'Semicolon', '``': 'DoubleQuote',
    "''": 'DoubleQuote', '`': 'Quote', "'": 'Quote',
    '-LRB-': 'Punctuation', '-RRB-': 'Punctuation',  # These are for '(' and ')'
    '-LSB-': 'Punctuation', '-RSB-': 'Punctuation',  # These are for '[' and ']'
    '-LCB-': 'Punctuation', '-RCB-': 'Punctuation',  # These are for '{' and '}'
    'OTHER': 'Other'
}

index_map = {
    'Noun': 0, 'Proper noun': 1, 'Verb': 2, 'Adjective': 3, 'Adverb': 4,
    'Preposition': 5, 'Determiner': 6, 'Pronoun': 7, 'Possessive pronoun': 8,
    'Conjunction': 9, 'Cardinal number': 10, 'Existential there': 11, 'Foreign word': 12,
    'Modal': 13, 'Predeterminer': 14, 'Possessive ending': 15, 'Particle': 16,
    'Symbol': 17, 'To': 18, 'Interjection': 19, 'Wh-determiner': 20,
    'Wh-pronoun': 21, 'Possessive wh-pronoun': 22, 'Wh-adverb': 23,
    'Comma': 24, 'Dot': 25, 'Colon': 26, 'Semicolon': 27, 'DoubleQuote': 28,
    'Quote': 29, 'Punctuation': 30, 'Other': 31
}

num_categories = len(index_map)

# Function to convert words to their POS types
def words_to_pos_types(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Tag each word with its part of speech
    tagged_words = nltk.pos_tag(words)

    # Replace each word with its POS type based on the mapping
    pos_types = [pos_map.get(tag, 'Other') for word, tag in tagged_words]
    return ', '.join(pos_types)


def words_to_pos_vector(pos_sentence):
    # Split the input string into tags
    tags = pos_sentence.split(", ")

    # Initialize the vector with zeros
    vector = [0] * num_categories

    # Increment the corresponding index for each tag
    for tag in tags:
        tag = tag.strip()  # Strip whitespace
        if tag in index_map:
            index = index_map[tag]
            vector[index] += 1

    # Normalize the vector by the total number of tags to make it a frequency vector
    total = sum(vector)
    if total > 0:
        vector = [x / total for x in vector]

    return vector

