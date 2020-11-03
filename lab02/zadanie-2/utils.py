#!/usr/bin/python3

import re

BAZA_DANYCH = 'pracownicy.sqlite3'

# \W pasuje do znaków, które nie wchodzą w skład wyrazów i liczb.
_NIEWYRAZY = re.compile(r'\W+')
_BEZ_ZNAKÓW_DIAKRYTYCZNYCH = dict(zip('ąćęłńóśźż', 'acelnoszz'))

# Miejscownik liczby pojedynczej rodzaju męskiego.
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_CI_T = re.compile('^(.+)cie$')
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_DZI_D = re.compile('^(.+d)zie$')
# Celownik i miejscownik liczby pojedynczej rodzaju żeńskiego.
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_CE_K = re.compile('^(.+)ce$')
# Miejscownik l.p. r.męskiego i mianownik liczby mnogiej rodzaju męskiego.
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_RZ_R = re.compile('^(.+r)z[ey]$')

# Nazwiska zakończone na -cień, -dziec, -dzień, -rzec, -rzeł.
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_CIE_T = re.compile('^(.+)cie(ń)$')
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_DZIE_D = re.compile('^(.+d)zie([cń])$')
_BEZ_KOŃCÓWKI_Z_WYMIANĄ_RZE_R = re.compile('^(.+r)ze([cł])$')

# Dwusylabowe i dłuższe nazwiska zakończone na -ie[ck].
_BEZ_RUCHOMEGO_IEC_IEK = re.compile('^(.*[aąeęioóuy].+)ie([ck])$')
# Dwusylabowe i dłuższe nazwiska zakończone na -e[ck].
_BEZ_RUCHOMEGO_EC_EK = re.compile('^(.*[aąeęioóuy].*[^i])e([ck])$')

# Dwusylabowe i dłuższe nazwiska zakończone na -ie[ćlłńr].
_BEZ_RUCHOMEGO_IE = re.compile('^(.*[aąeęioóuy].+)ie([ćlłńr])$')
# Nazwiska i imiona zakończone na -e[ćlłńr].
_BEZ_RUCHOMEGO_E = re.compile('^(.+[^i])e([ćlłńr])$')

# Regularne końcówki odmiany rzeczowników i przymiotników,
# oprócz końcówek złożonych z jednej samogłoski.
# TU(1): uzupełnić regexp.
_BEZ_DŁUŻSZEJ_KOŃCÓWKI = re.compile('^(.+)(a(ch|mi)|e(go|j|m|mu)|ie(j|m)|m|o(m|wi|wie)|ów)$')


def _bez_końcówki(wyraz):
    """Zwraca `wyraz` bez końcówki odmiany rzeczownika lub przymiotnika."""

    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_CI_T.match(wyraz);
    if m: return[m.group(1) + 't']
    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_DZI_D.match(wyraz)
    if m: return[m.group(1)]
    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_CE_K.match(wyraz)
    if m: return[m.group(1) + 'k']
    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_RZ_R.match(wyraz)
    if m: return[m.group(1), m.group(1) + 'z']

    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_CIE_T.match(wyraz)
    if m: return[wyraz, m.group(1) + 't' + m.group(2)]
    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_DZIE_D.match(wyraz)
    if m: return[wyraz, m.group(1) + m.group(2)]
    m = _BEZ_KOŃCÓWKI_Z_WYMIANĄ_RZE_R.match(wyraz)
    if m: return[wyraz,
                 m.group(1) + 'z' + m.group(2),
                 m.group(1) + m.group(2)]

    m = _BEZ_RUCHOMEGO_IEC_IEK.match(wyraz)
    if m: return[m.group(1) + m.group(2)]
    m = _BEZ_RUCHOMEGO_EC_EK.match(wyraz)
    if m: return[m.group(1) + m.group(2)]

    m = _BEZ_RUCHOMEGO_IE.match(wyraz)
    if m: return [wyraz, m.group(1) + m.group(2)]
    m = _BEZ_RUCHOMEGO_E.match(wyraz)
    if m: return [wyraz, m.group(1) + m.group(2)]

    m = _BEZ_DŁUŻSZEJ_KOŃCÓWKI.match(wyraz)
    if m: wyraz = m.group(1)
    return [wyraz.rstrip('aąeęiouy')]


def _bez_znaków_diakrytycznych(wyraz):
    """Zwraca `wyraz` bez polskich znaków diakrytycznych.

    >>> _bez_znaków_diakrytycznych('kowalski')
    'kowalski'
    >>> _bez_znaków_diakrytycznych('żabińska')
    'zabinska'
    """
    return ''.join(_BEZ_ZNAKÓW_DIAKRYTYCZNYCH.get(c, c) for c in wyraz)


def _minuskułą_i_podzielone(pytanie):
    """Dzieli `pytanie` na wyrazy i zamienia je na małe litery.

    >>> _minuskułą_i_podzielone('Kto ma na imię Paweł?')
    ['kto', 'ma', 'na', 'imię', 'paweł']
    """
    return [w.lower() for w in _NIEWYRAZY.split(pytanie) if w]


def podziel_i_odetnij_końcówki(pytanie):
    """Dzieli `pytanie` na wyrazy i odcina ich końcówki.

    >>> podziel_i_odetnij_końcówki('Kowalski Kowalskiego Kowalskiemu Kowalskim')
    [['kowalsk'], ['kowalsk'], ['kowalsk'], ['kowalsk']]
    >>> podziel_i_odetnij_końcówki('Kowalska Kowalskiej Kowalską')
    [['kowalsk'], ['kowalsk'], ['kowalsk']]
    >>> podziel_i_odetnij_końcówki('Szczęsny Szczęsnego Szczęsnemu Szczęsnym')
    [['szczesn'], ['szczesn'], ['szczesn'], ['szczesn']]
    >>> podziel_i_odetnij_końcówki('Szczęsna Szczęsnej Szczęsną')
    [['szczesn'], ['szczesn'], ['szczesn']]
    >>> podziel_i_odetnij_końcówki('Nowak Nowaka Nowakowi Nowakiem Nowaku')
    [['nowak'], ['nowak'], ['nowak'], ['nowak'], ['nowak']]
    >>> podziel_i_odetnij_końcówki('doktor doktora doktorowi doktorem')
    [['doktor'], ['doktor'], ['doktor'], ['doktor']]
    >>> podziel_i_odetnij_końcówki('profesorowie profesorów profesorom profesorami profesorach')
    [['profesor'], ['profesor'], ['profesor'], ['profesor'], ['profesor']]

    >>> podziel_i_odetnij_końcówki('doktorze doktorzy Jerzy Zygmuncie Dawidzie Magdzie jednostce')
    [['doktor', 'doktorz'], ['doktor', 'doktorz'], ['jer', 'jerz'], ['zygmunt'], ['dawid'], ['magd'], ['jednostk']]
    >>> podziel_i_odetnij_końcówki('Marzec Kwiecień Grudzień')
    [['marzec', 'marzc', 'marc'], ['kwiecien', 'kwietn'], ['grudzien', 'grudn']]

    >>> podziel_i_odetnij_końcówki('Niemiec Niemca Bieniek Bieńka')
    [['niemc'], ['niemc'], ['bienk'], ['bienk']]
    >>> podziel_i_odetnij_końcówki('Pawelec Pawelca Dudek Dudka')
    [['pawelc'], ['pawelc'], ['dudk'], ['dudk']]
    >>> podziel_i_odetnij_końcówki('Dec Piec Ćwiek Skrzek')
    [['dec'], ['piec'], ['cwiek'], ['skrzek']]

    >>> podziel_i_odetnij_końcówki('Dziegieć Grygiel Szczygieł Stępień Węgier')
    [['dziegiec', 'dziegc'], ['grygiel', 'grygl'], ['szczygiel', 'szczygl'], ['stepien', 'stepn'], ['wegier', 'wegr']]
    >>> podziel_i_odetnij_końcówki('Kopeć Wróbel Gaweł Styczeń Majcher')
    [['kopec', 'kopc'], ['wrobel', 'wrobl'], ['gawel', 'gawl'], ['styczen', 'styczn'], ['majcher', 'majchr']]
    >>> podziel_i_odetnij_końcówki('Kmieć Chmiel Kieł Bień Sier')
    [['kmiec'], ['chmiel'], ['kiel'], ['bien'], ['sier']]

    >>> podziel_i_odetnij_końcówki('Maria Marii')
    [['mar'], ['mar']]
    """
    wynik = []
    for wyraz in _minuskułą_i_podzielone(pytanie):
        wynik.append([_bez_znaków_diakrytycznych(rdzeń) for rdzeń in _bez_końcówki(wyraz)])
    return wynik


if __name__ == '__main__':
    import doctest
    doctest.testmod()
