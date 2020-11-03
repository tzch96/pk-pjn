#!/usr/bin/python3

import collections
import logging
import math
import os
import re
import string
import unicodedata

from matplotlib import animation
from matplotlib import patches
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from sklearn import manifold

DIRNAME = 'teksty'

ALPHANUMERIC = ''.join(
    chr(x) for x in range(0x250)
    if unicodedata.category(chr(x)) in ('Lu', 'Ll', 'Nd'))

TOKENIZE_RE = re.compile(
    r'[{0}]+(?:-[{0}]+)*|[.,;:!?]+'.format(ALPHANUMERIC),
    re.MULTILINE | re.UNICODE)

INTERESTING_TOKEN_SET = frozenset("""
    . ? ! ,
    a aby albo ale ani aż bo choć czy i jeśli lecz ni niech niż więc że żeby
    bez dla do ku jako na nad o od po pod przed przez przy u w we wkoło z ze za
    bardzo coraz dotąd dziś gdy jak kiedy kiedyś niegdyś nieraz nigdy potem
    razem sam stąd teraz tu tuż tyle tym tymczasem wnet wszystko wtem wtenczas
    się nie by co gdyby gdzie jakby jeszcze już ledwie może nawet niby
    przecież tak tam też to tylko właśnie zaraz znowu
""".split())

INTERESTING_TOKEN_LIST = sorted(INTERESTING_TOKEN_SET)

# Solarized palette, https://ethanschoonover.com/solarized/
COLORS = [
    '#b58900',  # Yellow.
    '#dc322f',  # Red.
    '#6c71c4',  # Violet.
    '#2aa198',  # Cyan.
    '#859900',  # Green.
    '#cb4b16',  # Orange.
    '#d33682',  # Magenta.
    '#268bd2',  # Blue.
]


def analyze(filename):
    counter = collections.Counter()
    with open(filename, 'rt', encoding='utf-8') as file:
        logging.info('Processing %s', filename)
        contents = file.read().split(u'-----\r\nTa lektura,')[0]
        tokens = TOKENIZE_RE.findall(contents)
        # TU(5): Uzupełnić zgodnie z instrukcją.
        for t in [token.lower() for token in tokens]:
            if t in INTERESTING_TOKEN_SET:
                counter[t] += 1
    # TU(6): Uzupełnić zgodnie z instrukcją.
    result = []
    for token in INTERESTING_TOKEN_LIST:
        result.append(counter[token] / len(tokens))

    return result


def split_filename(filename, colors):
    filename = filename.split('.txt')[0]
    author, book = filename.split('-', 1)
    book = book.replace('-', ' ')
    book = book[0].title() + book[1:]
    author = author.title()
    if author not in colors:
        colors[author] = COLORS[len(colors)]
    return author, colors[author], book


def plot(filenames, X, title):
    colors = {}
    fig = plt.figure(figsize=(6.4, 4.8))
    ax = fig.add_subplot(111)
    for filename, (x, y) in zip(filenames, X):
        author, color, book = split_filename(filename, colors)
        ax.plot(x, y, marker='o', color=color, label=author)
        ax.annotate(xy=(x, y), s=book, color=color)
    legend_handles = [
        patches.Circle((0.5, 0.5), color=x) for x in colors.values()]
    ax.legend(legend_handles, colors.keys(), loc='upper left')
    plt.title(title)
    plt.show()


def plot3d(filenames, X, title, gif_name):
    # TU(12): Wpisać wybrane przez siebie wartości.
    NUM_FRAMES = 0
    ELEVATION_ZERO = 0.0
    ELEVATION_SPEED = 0.0
    AZIMUTH_ZERO = 0.0
    AZIMUTH_SPEED = 0.0

    def draw_frame(frame_num):
        logging.info('Drawing frame %d of %s', frame_num, title)
        plt.clf()
        ax = fig.add_subplot(111, projection='3d')
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.zaxis.set_ticklabels([])
        colors = {}
        for filename, (x, y, z) in zip(filenames, X):
            author, color, book = split_filename(filename, colors)
            ax.plot([x], [y], [z], marker='o', color=color, label=author)
            ax.text(x, y, z, s=book, color=color)
        if frame_num <= NUM_FRAMES:
            # TU(12): Obliczyć `elev` i `azim` zgodnie z instrukcją.
            pass
        else:
            # TU(12): Obliczyć `elev` i `azim` zgodnie z instrukcją.
            pass
        ax.view_init(elev=elev, azim=azim)
        legend_handles = [
            patches.Circle((0.5, 0.5), color=x) for x in colors.values()]
        ax.legend(legend_handles, colors.keys(), loc='upper left')
        plt.title(title, loc='right')

    fig = plt.figure(figsize=(6.4, 4.8))
    anim = animation.FuncAnimation(fig, draw_frame, frames=2 * NUM_FRAMES)
    anim.save(gif_name, writer='imagemagick', fps=12.5)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    filenames = []
    X = []
    for filename in os.listdir(DIRNAME):
        filenames.append(filename)
        X.append(analyze(os.path.join(DIRNAME, filename)))

    plot(
        filenames,
        decomposition.PCA(n_components=2).fit_transform(X),
        'Principal component analysis')

    # TU(9): Narysować analogiczny do powyższego diagram
    # wyników analizy czynnikowej (n_components=2).
    plot(
        filenames,
        decomposition.FactorAnalysis(n_components=2).fit_transform(X),
        'Factor analysis')

    # TU(10): Narysować analogiczny do powyższych diagram
    # wyników skalowania wielowymiarowego (n_components=2).
    plot(
        filenames,
        manifold.MDS(n_components=2).fit_transform(X),
        'Multidimensional scaling')


if __name__ == '__main__':
    main()
