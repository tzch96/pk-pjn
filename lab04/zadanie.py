#!/usr/bin/python3

import colorama
import spacy


BOOK_FILE = 'ogniem-i-mieczem-tom-pierwszy.txt'  # TU(4): wpisać nazwę pliku z tekstem książki.
MODEL = 'pl_core_news_md'


def main():
    colorama.init()
    with open(BOOK_FILE, 'rt', encoding='utf-8') as book:
        text = book.read()
    nlp = spacy.load(MODEL)
    doc = nlp(text)
    for sentence in doc.sents:
        left, right = set(), set()
        for token in sentence:
            # TU(5, 6): uzupełnić dodawanie indeksów
            # do zbiorów `left` i `right`.
            if token.dep_ == 'aux:pass':
                l, r = sorted([token.i, token.head.i])
                left.add(l)
                right.add(r)
        if left:
            for token in sentence:
                # TU(7): uzupełnić wypisywanie zdania
                # z podświetleniami.
                if token.i in left:
                    print(colorama.Fore.BLACK + colorama.Back.GREEN + '[', end='')
                    print(token.text, end='')
                    print(token.whitespace_, end='')
                elif token.i in right:
                    print(token.whitespace_, end='')
                    print(token.text, end='')
                    print(']' + colorama.Fore.RESET + colorama.Back.RESET, end='')
            print()


if __name__ == '__main__':
    main()
