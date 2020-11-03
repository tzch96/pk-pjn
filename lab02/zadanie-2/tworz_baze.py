#!/usr/bin/python3

import csv
import os
import sqlite3

import normalizacja
import utils


IGNORUJ_NAZWY_JEDNOSTEK = {
    'centrum',
    'dzial',
    'katedr',
}


def main():
    try:
        os.remove(utils.BAZA_DANYCH)
    except OSError:
        pass
    connection = sqlite3.connect(utils.BAZA_DANYCH)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE Pracownicy(
            docid INTEGER PRIMARY KEY
            , jednostka TEXT
            , pracownik TEXT
            , email TEXT
            , telefon TEXT
        )
        """)
    cursor.execute(
        """
        CREATE VIRTUAL TABLE PracownicyFTS USING fts4(dane)
        """)
    with open('pracownicy.csv', 'rt', encoding='utf-8') as pracownicy:
        for jednostka, pracownik, email, telefon in csv.reader(pracownicy):
            jednostka = normalizacja.normalizuj_kody_jednostek(jednostka)
            telefon = normalizacja.normalizuj_numery_telefonów(telefon)
            cursor.execute(
                """
                INSERT INTO Pracownicy(jednostka, pracownik, email, telefon)
                VALUES (?,?,?,?)
                """,
                (jednostka, pracownik, email, telefon))
            docid = cursor.lastrowid
            jednostka_fts = []
            for fragment in utils.podziel_i_odetnij_końcówki(jednostka):
                for element in fragment:
                    if element not in IGNORUJ_NAZWY_JEDNOSTEK:
                        jednostka_fts.append(element)
            pracownik_fts = []
            for fragment in utils.podziel_i_odetnij_końcówki(pracownik):
                pracownik_fts.extend(fragment)
            telefon_fts = []
            for fragment in utils.podziel_i_odetnij_końcówki(telefon):
                telefon_fts.extend(fragment)
            cursor.execute(
                """
                INSERT INTO PracownicyFTS(docid, dane)
                VALUES (?,?)
                """,
                (docid, ' '.join(jednostka_fts + pracownik_fts + telefon_fts)))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
