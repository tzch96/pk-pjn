#!/usr/bin/python3

import collections
import sqlite3
import sys

import mwparserfromhell as mwp
import spacy


MODEL = 'pl_core_news_md'


def wypisz(typ, subj, pred, obj):
     # Interesują nas tylko relacje między rzeczownikami
     # (pospolitymi lub własnymi), a nie np. między zaimkami
     # rzeczownymi.
     if subj.pos_ not in {'NOUN', 'PROPN'}:
          return
     if obj.pos_ not in {'NOUN', 'PROPN'}:
          return
     print(typ, subj.text, pred.text, obj.text)
     sys.stdout.flush()


def znajdź_relacje_z_być_lub_to(token):
    if token.dep_ == 'nsubj':
        cop = [c for c in token.children if c.dep_ == 'cop']
        if not cop:
            return
        wypisz(1, token, cop[0], token.head)


def znajdź_relacje_z_innymi_czasownikami(token):
    if token.pos_ == 'VERB':
        # TU(5):
        #  * Stworzyć listę dzieci `tokenu`, będących z nim w relacji 'nsubj' (podmiot).
        #  * Jeśli lista podmiotów `tokenu` jest pusta, to wyjść z funkcji.
        #  * Stworzyć listę dzieci `tokenu`, będących z nim w relacji 'obj' (dopełnienie).
        #  * Jeśli lista dopełnień `tokenu` jest pusta, to wyjść z funkcji.
        #  * Wywołać `wypisz(2, subj[0], token, obj[0])`.
        subj = [c for c in token.children if c.dep_ == 'nsubj']
        obj = [c for c in token.children if c.dep_ == 'obj']
        if not subj or not obj:
            return
        wypisz(2, subj[0], token, obj[0])


def znajdź_relacje_w_stronie_biernej(token):
    if token.pos_ == 'VERB':
        # TU(6):
        #  * Znaleźć dzieci `tokenu`, będące z nim w relacji 'nsubj:pass'.
        #  * Jeśli nie ma takich dzieci, to wyjść z funkcji.
        #  * Znaleźć dzieci `tokenu`, będące z nim w relacji 'obl'
        #    i dodatkowo posiadające chociaż jedno własne dziecko,
        #    którego atrybut `.text` ma wartość 'przez'
        #    i atrybut `.dep_` ma wartość 'case'.
        #  * Jeśli nie ma takich dzieci, to wyjść z funkcji.
        #  * Wywołać `wypisz(3, obl[0], token, nsubj[0])`
        nsubj = [c for c in token.children if c.dep_ == 'nsubj:pass']
        obl = [c for c in token.children if c.dep_ == 'obl' and any(x.text == 'przez' and x.dep_ == 'case' for x in c.children)]
        if not nsubj or not obl:
            return
        wypisz(3, obl[0], token, nsubj[0])


def main():
    nlp = spacy.load(MODEL)
    # Żądamy łączenia wszystkich znalezionych jednostek nazewniczych
    # w pojedyncze segmenty (tokens), co ułatwia pisanie pozostałych
    # części programu.
    nlp.add_pipe(spacy.pipeline.merge_entities)
    connection = sqlite3.connect('artykuly.sqlite3')
    for title, text in connection.execute('SELECT title, text FROM Articles LIMIT 200'):
        text = mwp.parse(text).strip_code(keep_template_params=False)
        doc = nlp(text)
        for token in doc:
            # znajdź_relacje_z_być_lub_to(token)
            # znajdź_relacje_z_innymi_czasownikami(token)
            znajdź_relacje_w_stronie_biernej(token)


if __name__ == '__main__':
    main()
