# Zapoznanie z regexpami

1. Każdy autor dodaje do sprawozdania regexp,
który rozpoznaje jego imię w każdym przypadku
liczby pojedynczej. Uwagi:

    * Regexp ma być rozsądnie krótki, np.
    `^(Jan|Jana|Janowi|Janem|Janie)$` nie jest
    poprawnym rozwiązaniem.

    * Jeśli autorzy mają jednakowe pierwsze
    imiona, to któryś z nich powinien użyć
    drugiego imienia.

    * Imiona autorów, dla których polski nie
    jest językiem ojczystym, można odmieniać
    po ukraińsku lub rosyjsku.

    * Przypominam pytania, na które odpowiadają
    przypadki odmiany: kto? kogo? komu? kogo/co?
    (różnica z dopełniaczem zachodzi w odmianie
    imion zakończonych na -a) kim? o kim? hej!

2. Pobrać plik [slownik.zip](https://drive.google.com/file/d/1DPQ1Dx5-j6mt8x_vC-u22H-h-qzVDgfh/view?usp=sharing) i przejrzeć
treść rozpakowanego pliku `slownik.txt`, w którym
znajdują się ponad 4 miliony odmienionych wyrazów
polskich.

3. W pliku `rymy.py` poprawić napis, użyty
w stałej `RYM_ŻEŃSKI` tak, żeby program zliczał
rymy żeńskie, czyli ostatnie półtorej sylaby
wyrazów. Na potrzeby tego zadania uznajemy, że:

    * Pół przedostatniej sylaby zapisuje litera,
    oznaczająca samogłoskę, po której następuje
    co najmniej jedna litera, oznaczająca
    spółgłoskę.

    * Ostatnią sylabę zapisuje opcjonalna litera
    *i*, po której następuje litera, oznaczająca
    samogłoskę, następnie co najmniej zero liter,
    oznaczających spółgłoski, a następnie koniec
    wyrazu.

    * Pomijamy wyrazy zero- i jednosylabowe
    (*w*, *mieć*).

    * Pomijamy rzadkie rymy, które zawierają obok
    siebie dwie samogłoski (*idea*, *wideo*).

    * Ignorujemy to, że zbitki *au* i *eu* wymawia
    się często jako jedną sylabę (*hydraulik*,
    *terapeuta*).

    * Ignorujemy to, że wyrazy, w których akcent
    nie pada na przedostatnią sylabę (barach**ło**,
    mate**ma**tyka, ro**bi**libyście), nie tworzą
    rymów żeńskich.

    * Interesuje nas pisownia, a nie wymowa, np.
    nie utożsamiamy rymów w wyrazach *łódka*,
    *robótka*, *pobudka* i *zrzutka* oraz ignorujemy
    to, że nieprzyswojone wyrazy obcego pochodzenia
    (*business*, *messerschmitt*, *tournée*) wymawia
    się inaczej, niż na to wskazuje ich pisownia.

4. Przetestować program `rymy.py`:

```python
    python3 rymy.py < test_rymy.txt
```

5. Poprawne wyjście programu, gdy na wejście podamy
plik `test_rymy.txt` to:

```
    10.00% -amy
    10.00% -ewie
    10.00% -ewo
    10.00% -awka
    10.00% -acie
    10.00% -edźwiedź
    10.00% -edzia
    10.00% -edziem
    10.00% -ętość
    10.00% -ości
```

6. Jeśli wyniki programu `rymy.py` dla danych
z pliku `test_rymy.txt` są poprawne, dodać do
sprawozdania wynik działania tego programu
dla danych z pliku `slownik.txt`.
