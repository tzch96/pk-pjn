#!/usr/bin/python3

import spacy
from collections import Counter

BOOK_FILE = 'ogniem-i-mieczem-tom-pierwszy.txt'
MODEL = 'pl_core_news_md'

def main():
  with open(BOOK_FILE, 'rt', encoding='utf-8') as book:
    text = book.read()

  nlp = spacy.load(MODEL)
  doc = nlp(text)

  original, normalized = Counter(), Counter()

  for ent in doc.ents:
    original[ent.text] += 1
    ent_norm = ''.join(t.lemma_.title() + t.whitespace_ for t in ent).strip()
    normalized[ent_norm] += 1

  print('Original forms\n==============')
  for word, n in original.most_common(15):
    print(word + ': ' + str(n))

  print('\n\nNormalized forms\n================')
  for word, n in normalized.most_common(15):
    print(word + ': ' + str(n))

if __name__ == '__main__':
  main()