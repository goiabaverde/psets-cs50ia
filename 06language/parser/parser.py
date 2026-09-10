import nltk
import sys

nltk.download('punkt_tab')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


NONTERMINALS = """
S -> NP VP | S Conj S

PP -> P NP

NP -> N | Det N | Det AdjP N | AdjP N | NP Conj NP

AdjP -> Adj | Adj AdjP

VP -> V| V NP| V PP| V Adv| Adv V| V NP PP | V Adv PP | VP Conj VP |
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Tokenize the sentence
    list_sentence = nltk.word_tokenize(sentence)
    to_remove = [] # Iniciate the list with the words that will be removed

    # Do a for loop cleaning the list_sentence, removing all word that have any alphabetic character
    for word in list_sentence:
        for letter in word:
            if letter.isalpha():
                break
            to_remove.append(word)
    # Remove the words
    for word in to_remove:
        n = list_sentence.count(word)
        for i in range(n):
            list_sentence.remove(word)

    process_list = [] # Iniciate the list with processed words
    for word in list_sentence:
        process_list.append(word.lower())

    return process_list






def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    np_chunk_list = [] # Iniciate the list with chunk np

    # Do the for loop in all the subtrees of the tree
    for subtree in tree.subtrees():
        add_subtree = True
        # If a subtree is a NP, check if there is no more NP as subtress
        if subtree.label() == "NP":
            # Remove the first item, because the first item is the own subtree
            for subsubtree in list(subtree.subtrees())[1:]:
                if subsubtree.label() == "NP":
                    add_subtree = False
                    break
            if add_subtree:
                np_chunk_list.append(subtree)

    return np_chunk_list







if __name__ == "__main__":
    main()
