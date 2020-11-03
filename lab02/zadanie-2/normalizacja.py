#!/usr/bin/python3

import re

# TU(1): Uzupełnić regexp tak, żeby (grupa 1) + (grupa 2)
# dawała znormalizowany kod jednostki.
# Wskazówki:
# * \b pasuje do początku lub końca wyrazu, czyli granicy
#   między znakiem alfanumerycznym i nie-alfanumerycznym
# * [\s-]+ pasuje do ciągu białych znaków lub znaków minusa.
_JEDNOSTKA_RE = re.compile(r'\b([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{1,2})[\s-]+([0-9]{1,2})\b')

# TU(2): Uzupełnić regexp tak, żeby (grupa 1) + (grupa 2)
# dawała znormalizowany numer telefonu.
# Należy usuwać sprzed ciągów znaków,
# pasujących do regexpu r'([0-9]{2})[\s-]*([0-9]{2})'
# ciągi znaków, pasujące do regexpów:
# * r'628[\s-]*'
# * r'12[\s-]*628[\s-]*'
# * r'\+48[\s-]*12[\s-]*628[\s-]*'
# Wskazówki:
# * [\s-]+ pasuje do ciągu białych znaków lub znaków minusa.
# * (?:...) tworzy grupę, której nie zostanie nadany numer.
_TELEFON_RE = re.compile(
    r'(?:628[\s-]*)?(?:12[\s-]*628[\s-]*)?(?:\+48[\s-]*12[\s-]*628[\s-]*)?([0-9]{2})[\s-]*([0-9]{2})')


def normalizuj_kody_jednostek(tekst):
    """Zwraca `tekst` ze znormalizowanymi kodami jednostek.

    >>> normalizuj_kody_jednostek('F--3 ka  3 Ś-01 L 9a L a9')
    'F3 ka3 Ś01 L 9a L a9'
    """
    return _JEDNOSTKA_RE.sub(r'\1\2', tekst)


def normalizuj_numery_telefonów(tekst):
    """Zwraca `tekst` ze znormalizowanymi numerami telefonów.

    >>> normalizuj_numery_telefonów(
    ...     '21 04 21-05 628 - 21 - 06 126282107 +48 12 628 21 08')
    '2104 2105 2106 2107 2108'
    """
    return _TELEFON_RE.sub(r'\1\2', tekst)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
