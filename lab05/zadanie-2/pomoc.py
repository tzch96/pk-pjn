#!/usr/bin/python3

import os.path
import webbrowser
import spacy


MODEL = 'pl_core_news_md'


def main():
    nlp = spacy.load(MODEL)
    while True:
        doc = nlp(input('Wprowadź zdanie: '))
        with open('output.html', 'w') as file:
            file.write(spacy.displacy.render(doc, style='dep'))
        webbrowser.open_new_tab('file://' + os.path.abspath('output.html'))


if __name__ == '__main__':
    main()
