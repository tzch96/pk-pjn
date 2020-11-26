#!/usr/bin/python3

import logging
import pickle
import re
import sqlite3

import mwparserfromhell as mwp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import functools
import morfeusz2

# TU(10a): Wkleić wyrazy z https://pl.wikipedia.org/wiki/Wikipedia:Stopwords
# TU(11b): Dopisać wyrazy specyficzne dla haseł Wikipedii.
STOP_WORDS = """a, aby, ach, acz, aczkolwiek, aj, albo, ale, ależ, ani, aż, bardziej, bardzo, bo, bowiem, by, byli, bynajmniej, być, był, była, było, były,
będzie, będą, cali, cała, cały, ci, cię, ciebie, co, cokolwiek, coś, czasami, czasem, czemu, czy, czyli, daleko, dla, dlaczego, dlatego, do, dobrze, dokąd,
dość, dużo, dwa, dwaj, dwie, dwoje, dziś, dzisiaj, gdy, gdyby, gdyż, gdzie, gdziekolwiek, gdzieś, i, ich, ile, im, inna, inne, inny, innych, iż, ja, ją,
jak, jaka, jakaś, jakby, jaki, jakichś, jakie, jakiś, jakiż, jakkolwiek, jako, jakoś, je, jeden, jedna, jedno, jednak, jednakże, jego, jej, jemu, jest,
jestem, jeszcze, jeśli, jeżeli, już, ją, każdy, kiedy, kilka, kimś, kto, ktokolwiek, ktoś, która, które, którego, której, który, których, którym, którzy,
ku, lat, lecz, lub, ma, mają, mało, mam, mi, mimo, między, mną, mnie, mogą, moi, moim, moja, moje, może, możliwe, można, mój, mu, musi, my, na, nad, nam,
nami, nas, nasi, nasz, nasza, nasze, naszego, naszych, natomiast, natychmiast, nawet, nią, nic, nich, nie, niech, niego, niej, niemu, nigdy, nim, nimi, niż,
no, o, obok, od, około, on, ona, one, oni, ono, oraz, oto, owszem, pan, pana, pani, po, pod, podczas, pomimo, ponad, ponieważ, powinien, powinna, powinni,
powinno, poza, prawie, przecież, przed, przede, przedtem, przez, przy, roku, również, sama, są, się, skąd, sobie, sobą, sposób, swoje, ta, tak, taka, taki,
takie, także, tam, te, tego, tej, temu, ten, teraz, też, to, tobą, tobie, toteż, trzeba, tu, tutaj, twoi, twoim, twoja, twoje, twym, twój, ty, tych, tylko,
tym, u, w, wam, wami, was, wasz, wasza, wasze, we, według, wiele, wielu, więc, więcej, wszyscy, wszystkich, wszystkie, wszystkim, wszystko, wtedy, wy,
właśnie, z, za, zapewne, zawsze, ze, zł, znowu, znów, został, żaden, żadna, żadne, żadnych, że, żeby, kategoria, przypisy, wydane, zewnętrzne, linki, single,
the, utwór, singel, utworów, wydany, lista, utwory, bibliografia, literackie, piosenki, została, utworu, pierwszy, powieści, kategoria, s1, rok, wydać, utwór,
przypis, zostać, v1, zewnętrzny, link, singel, the, s2, album, piosenka, lista, swój, napisać, list, literacki, autor, mieć, of, in, tytuł, okładka, tekst,
strona, autor, wersja, pierwsza, sam, powieścić, książka, film, www, http, en, https, wydawnictwo, records
""".split(',')
STOP_WORDS = [w.strip() for w in STOP_WORDS if w.strip()]

# TU(11c): Nie likwidować liczb.
NONLETTERS_RE = re.compile(
    r'[0-9’“„”«»…–—!"#$%&\'()*+,\-./:;?@\[\\\]^_`{|}~<=>]')

MORFEUSZ = morfeusz2.Morfeusz(praet='composite')

@functools.lru_cache(maxsize=None)
def formy_podstawowe(wyraz):
    formy = []
    for interpretacja in MORFEUSZ.analyse(wyraz):
        formy.append(interpretacja[2][1])
    return sorted(formy)


def jednoznaczna_forma_podstawowa(wyraz):
    formy = formy_podstawowe(wyraz)
    # TU(7): uzupełnić zgodnie z instrukcją.
    if not formy:
        return wyraz
    if len(formy) == 1:
        return formy[0]
    
    return min(formy, key=len)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    logging.info('Wczytywanie danych. To potrwa do dwóch minut.')
    connection = sqlite3.connect('artykuly.sqlite3')
    titles = []
    texts = []
    for row in connection.execute('SELECT title, text FROM Articles'):
        titles.append(row[0])
        # TU(11d): zmienić keep_template_params na True.
        text = mwp.parse(row[1]).strip_code(keep_template_params=True)
        text = NONLETTERS_RE.sub(' ', text)
        # TU(11a): zamiast poniższego wiersza zapisać dodawanie do `texts`
        # ' '.join(jednoznaczna_forma_podstawowa(w) for w in text.split())
        texts.append(' '.join(jednoznaczna_forma_podstawowa(w) for w in text.split()))
    logging.info('Tworzenie modelu. To potrwa do pół minuty.')
    # TU(10b): Zamienić na TfidfVectorizer.
    vectorizer = TfidfVectorizer(
        analyzer='word',
        min_df=3,
        stop_words=STOP_WORDS
        # TU(10a): Dopisać stop_words=STOP_WORDS.
    )
    X = vectorizer.fit_transform(texts)
    logging.info(
            'Model gotowy. Korzysta z %d cech.',
            len(vectorizer.get_feature_names()))
    if type(vectorizer) is TfidfVectorizer:
        idfs = []
        for feature, idf in zip(
                vectorizer.get_feature_names(),
                vectorizer.idf_):
            idfs.append((idf, feature))
        logging.info(
            'Najczęstsze wyrazy: %s.',
            ', '.join(feature for idf, feature in sorted(idfs)[:20]))
    with open('model.pickle', 'wb') as file:
        pickle.dump(titles, file, pickle.HIGHEST_PROTOCOL)
        pickle.dump(X, file, pickle.HIGHEST_PROTOCOL)
    logging.info('Model zapisany.')


if __name__ == '__main__':
    main()
