#!/usr/bin/python3

import array
import collections
import functools
import os
import pprint
import webbrowser

import numpy as np
import scipy.sparse
from sklearn import linear_model
from sklearn import metrics
from sklearn.feature_extraction import text


PARAMS = {
    # TU(6): Wybrać zbiór danych.
    'dataset': 'products.text',
    # TU(9): Próbować różnych wartości.
    'penalty': 'elasticnet',
    'solver': 'saga',
    # TU(18): Próbować różnych wartości.
    'negative_word_coefficient': -1,
}

# TU(11): Wkleić wyrazy z https://pl.wikipedia.org/wiki/Wikipedia:Stopwords
STOP_WORDS = """a, aby, ach, acz, aczkolwiek, aj, albo, ale, ależ, ani, aż, bardziej, bardzo, bo, bowiem, by, byli, bynajmniej, być, był, była,
było, były, będzie, będą, cali, cała, cały, ci, cię, ciebie, co, cokolwiek, coś, czasami, czasem, czemu, czy, czyli, daleko, dla, dlaczego,
dlatego, do, dobrze, dokąd, dość, dużo, dwa, dwaj, dwie, dwoje, dziś, dzisiaj, gdy, gdyby, gdyż, gdzie, gdziekolwiek, gdzieś, i, ich, ile, im,
inna, inne, inny, innych, iż, ja, ją, jak, jaka, jakaś, jakby, jaki, jakichś, jakie, jakiś, jakiż, jakkolwiek, jako, jakoś, je, jeden, jedna,
jedno, jednak, jednakże, jego, jej, jemu, jest, jestem, jeszcze, jeśli, jeżeli, już, ją, każdy, kiedy, kilka, kimś, kto, ktokolwiek, ktoś, która,
które, którego, której, który, których, którym, którzy, ku, lat, lecz, lub, ma, mają, mało, mam, mi, mimo, między, mną, mnie, mogą, moi, moim,
moja, moje, może, możliwe, można, mój, mu, musi, my, na, nad, nam, nami, nas, nasi, nasz, nasza, nasze, naszego, naszych, natomiast, natychmiast,
nawet, nią, nic, nich, nie, niech, niego, niej, niemu, nigdy, nim, nimi, niż, no, o, obok, od, około, on, ona, one, oni, ono, oraz, oto, owszem,
pan, pana, pani, po, pod, podczas, pomimo, ponad, ponieważ, powinien, powinna, powinni, powinno, poza, prawie, przecież, przed, przede, przedtem,
przez, przy, roku, również, sama, są, się, skąd, sobie, sobą, sposób, swoje, ta, tak, taka, taki, takie, także, tam, te, tego, tej, temu, ten,
teraz, też, to, tobą, tobie, toteż, trzeba, tu, tutaj, twoi, twoim, twoja, twoje, twym, twój, ty, tych, tylko, tym, u, w, wam, wami, was, wasz,
wasza, wasze, we, według, wiele, wielu, więc, więcej, wszyscy, wszystkich, wszystkie, wszystkim, wszystko, wtedy, wy, właśnie, z, za, zapewne,
zawsze, ze, zł, znowu, znów, został, żaden, żadna, żadne, żadnych, że, żeby
""".split(',')
STOP_WORDS = [w.strip() for w in STOP_WORDS if w.strip()]


def jednoznaczna_forma_podstawowa(wyraz):
    # TU(15): skopiować treść funkcji z laboratorium 1.
    return wyraz


TRAIN_DATASET = f'dataset/{PARAMS["dataset"]}.train.txt'
TEST_DATASET = f'dataset/{PARAMS["dataset"]}.test.txt'
DEV_DATASET = f'dataset/{PARAMS["dataset"]}.dev.txt'

LABEL_TO_Y = {
    '__label__meta_minus_m': 0,
    '__label__meta_minus_s': 0,
    '__label__meta_amb': None,
    '__label__meta_zero': None,
    '__label__meta_plus_s': 1,
    '__label__meta_plus_m': 1,

    '__label__z_minus_m': 0,
    '__label__z_minus_s': 0,
    '__label__z_amb': None,
    '__label__z_zero': None,
    '__label__z_plus_s': 1,
    '__label__z_plus_m': 1,
}

Y_TO_CLASS = {
    0: 'negative',
    1: 'positive',
}

HTML_FILE = 'misclassifications.html'

# TU(8): Studenci-daltoniści są proszeni o zmianę
# poniższych wartości tak, by móc odróżnić podświetlenia
# wyrazów o wydźwięku dodatnim i ujemnym.
GREEN = [0x85, 0x99, 0x00]
RED = [0xdc, 0x32, 0x2f]


NEGATION_START = {
    # TU(12): Wpisać wyrazy, które zmieniają
    # wydźwięk swoich następników na przeciwny.
    'nie', 'bez', 'oprócz', 'prócz', 'poza', 'źle'
}


def preprocess_tokens(tokens):
    # TU(12): Usunąć powyższy wiersz i zaimplementować
    # wstępne przetwarzanie tokenów zgodnie z instrukcją.
    negate = False
    result = []
    for token in tokens:
        if negate:
            result.append(token.upper())
        else:
            result.append(token)
        if token in NEGATION_START:
            negate = not negate
        if not token.isalnum():
            negate = False
    return result


class PlusMinusVectorizer:

    def __init__(self, params, stop_words):
        self.negative_word_coefficient = params['negative_word_coefficient']
        self.stop_words = set(stop_words)

    def _count_vocab(self, raw_documents, fixed_vocab):
        if fixed_vocab:
            vocabulary = self.vocabulary_
        else:
            vocabulary = collections.defaultdict()
            vocabulary.default_factory = vocabulary.__len__
        j_indices = []
        values = array.array('f')
        indptr = [0]
        for doc in raw_documents:
            token_counter = collections.Counter()
            for token in doc.split():
                if token in self.stop_words:
                    continue
                try:
                    base = jednoznaczna_forma_podstawowa(token).lower()
                    base_idx = vocabulary[base]
                    if token.isupper():
                        token_counter[base_idx] += self.negative_word_coefficient
                    else:
                        token_counter[base_idx] += 1
                except KeyError:
                    # For fixed_vocab=True, ignore out-of-vocabulary items.
                    pass
            j_indices.extend(token_counter.keys())
            values.extend(token_counter.values())
            indptr.append(len(j_indices))
        if not fixed_vocab:
            vocabulary = dict(vocabulary)
        j_indices = np.asarray(j_indices, dtype=np.int32)
        indptr = np.asarray(indptr, dtype=np.int32)
        values = np.frombuffer(values, dtype=np.float32)
        X = scipy.sparse.csr_matrix(
            (values, j_indices, indptr),
            shape=(len(indptr) - 1, len(vocabulary)),
            dtype=np.float32)
        return vocabulary, X

    def fit_transform(self, raw_documents):
        self.vocabulary_, X = self._count_vocab(raw_documents, False)
        return X

    def transform(self, raw_documents):
        _, X = self._count_vocab(raw_documents, True)
        return X


def read_file(filename):
    with open(filename, 'rt', encoding='utf-8') as file:
        for line in file:
            tokens = line.lower().split()
            y = LABEL_TO_Y[tokens[-1]]
            if y is not None:
                yield tokens[:-1], y


def read_from_file(filename, X, Y):
    for tokens, y in read_file(filename):
        X.append(' '.join(preprocess_tokens(tokens)))
        Y.append(y)


def print_weights(header, token_weights):
    print(header, ', '.join(t.replace(' ', '#') for w, t in token_weights))


def get_token_weights(vectorizer, model):
    token_weights = []
    for token, index in vectorizer.vocabulary_.items():
        v = model.coef_[0][index]
        if v:
            token_weights.append((v, token))
    token_weights.sort()
    return token_weights


def print_token_info(token_weights):
    print('{} segmentów o niezerowych wagach'.format(len(token_weights)))
    print_weights('Dodatnie:', token_weights[-1:-20:-1])
    print_weights('Ujemne:', token_weights[:20])


def print_report(X_test, Y_test, vectorizer, model):
    X_counted = vectorizer.transform(X_test)
    print(metrics.classification_report(
        Y_test, model.predict(X_counted), digits=3))


def show_misclassifications_in_browser(X_test, Y_test, vectorizer, model):
    X_counted = vectorizer.transform(X_test)
    Y_predicted = model.predict(X_counted)
    html = open(HTML_FILE, 'wt')
    html.write('<html><body>\n')
    base_proba = model.predict_proba(vectorizer.transform(['']))[0][1]
    for x, y_real, y_predicted in zip(X_test, Y_test, Y_predicted):
        if y_real != y_predicted:
            html.write(f"""<p><b>Actual: {Y_TO_CLASS[not y_predicted]},
predicted: {Y_TO_CLASS[y_predicted]}</b><br>\n""")
            for token in x.split():
                token_counted = vectorizer.transform([token])
                token_score = model.predict_proba(token_counted)[0][1]
                if token_score < base_proba:
                    m = (base_proba - token_score) / base_proba
                    color = [255 - int((255 - c) * m) for c in RED]
                else:
                    m = (token_score - base_proba) / (1.0 - base_proba)
                    color = [255 - int((255 - c) * m) for c in GREEN]
                rgb = ','.join(str(c) for c in color)
                html.write(f'  <span title="{token_score:.2}" \
style="background-color:rgb({rgb});">{token}</span>\n')
            html.write('</p>\n')
    html.write('</body></html>')
    html.close()
    webbrowser.open_new_tab(f'file://{os.path.abspath(HTML_FILE)}')


def main():
    vectorizer = text.CountVectorizer(
        analyzer='word',
        stop_words=STOP_WORDS,
        lowercase=False)
    # TU(14): Zakomentować powyższe przypisanie,
    # a odkomentować poniższe.
    #vectorizer = PlusMinusVectorizer(PARAMS, stop_words=STOP_WORDS)
    X_train = []
    Y_train = []
    read_from_file(TRAIN_DATASET, X_train, Y_train)
    X_train = vectorizer.fit_transform(X_train)
    model = linear_model.LogisticRegression(
        penalty=PARAMS['penalty'],
        solver=PARAMS['solver'],
        l1_ratio=0.5,
        max_iter=1000,
        verbose=True
    )
    model.fit(X_train, Y_train)

    print('\n\n')
    pprint.pprint(PARAMS)
    token_weights = get_token_weights(vectorizer, model)
    print_token_info(token_weights)
    X_test = []
    Y_test = []
    read_from_file(TEST_DATASET, X_test, Y_test)
    read_from_file(DEV_DATASET, X_test, Y_test)
    print_report(X_test, Y_test, vectorizer, model)
    show_misclassifications_in_browser(X_test, Y_test, vectorizer, model)


if __name__ == '__main__':
    main()
