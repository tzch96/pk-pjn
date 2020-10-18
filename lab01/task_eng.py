#!/usr/bin/python3

"""Natural Language Processing, lesson 1."""

import collections
import functools

import matplotlib.pyplot as plt

import Stemmer

STEMMER = Stemmer.Stemmer('english')

BOOK = 'the-history-of-don-quixote.txt'

def get_words(file_name):
    with open(file_name, 'rt', encoding='utf-8') as book_file:
        for part in book_file.read().split():
            word = part.strip(",;.“”(?)’‘!:_—-*>#[]/%$")
            if word not in ['']:
                yield word

def get_words_outer_chars(file_name):
    chars = collections.Counter()
    for word in get_words(file_name):
        chars[word[0]] += 1
        chars[word[-1]] += 1
    for char, num_occurrences in chars.most_common():
        if not char.isalnum():
            print(char, num_occurrences)

def single_basic_form(word):
    return STEMMER.stemWord(word)

def main():
    # get_words_outer_chars(BOOK)
    # return
    words = collections.Counter(get_words(BOOK))
    text_length = sum(words.values())
    print(words.most_common(10))
    
    plt.xscale('log')
    plt.yscale('log')
    y = []
    for _, num_occurrences in words.most_common():
        y.append(num_occurrences / text_length)
    plt.plot(y)
    plt.title(f'Number of occurrences for {len(words)} words\nin book {BOOK}')
    plt.show()

    plt.xscale('log')
    plt.yscale('linear')
    y = []
    total = 0
    for _, num_occurrences in words.most_common():
        total += num_occurrences
        y.append(total)
    
    plt.plot(y)
    plt.title(f'Coverage of text for {len(words)} words\nin book {BOOK}')
    plt.show()

    forms = collections.Counter()
    for word in get_words(BOOK):
        form = single_basic_form(word)
        forms[form] += 1

    # number of occurrences - basic forms
    plt.xscale('log')
    plt.yscale('log')
    y = []

    for _, num_occurrences in forms.most_common():
        y.append(num_occurrences / text_length)
    plt.plot(y)
    plt.title(f'Number of occurrences for {len(forms)} basic word forms\nin book {BOOK}')
    plt.show()

    # text coverage - basic forms
    plt.xscale('log')
    plt.yscale('linear')
    y = []

    total = 0
    for _, num_occurrences in forms.most_common():
        total += num_occurrences
        y.append(total)
    plt.plot(y)
    plt.title(f'Coverage of text for {len(forms)} basic word forms\nin book {BOOK}')
    plt.show()


if __name__ == '__main__':
    main()
