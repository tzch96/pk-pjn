#!/usr/bin/python3

import collections
import re
import sys

# IMIĘ: [Tt]omasz(\b|a|u|em|owi)\b
# (?:...) oznacza grupę, której nie zostanie nadany numer.
SPÓŁGŁOSKA = '(?:ch|cz|dz|dź|dż|rz|sz|[^aęeęioóuy])'
SAMOGŁOSKA = '[aąeęioóuy]'

# Wewnątrz tzw. f-napisów można używać wyrażeń w nawiasach klamrowych.
# Zostaną one zastąpione przez wartości tych wyrażeń.
RYM_ŻEŃSKI = re.compile(
    f'.*({SAMOGŁOSKA}{SPÓŁGŁOSKA}+i?{SAMOGŁOSKA}{SPÓŁGŁOSKA}*)$')


def main():
    licznik_wyrazów = 0
    licznik_rymów = collections.Counter()
    for wyraz in sys.stdin:
        # Usuń końcowy znak nowego wiersza.
        wyraz = wyraz.strip()
        m = RYM_ŻEŃSKI.match(wyraz)
        if m:
             licznik_wyrazów += 1
             licznik_rymów[m.group(1)] += 1
    for rym, ile_razy in licznik_rymów.most_common(25):
        # :5.2f oznacza "typ float, 5 znaków, 2 cyfry po przecinku".
        print(f'{100*ile_razy/licznik_wyrazów:5.2f}% -{rym}')


if __name__ == '__main__':
    main()
