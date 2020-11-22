# Rozpoznawanie jednostek nazewniczych

1. Celem tego zadania jest napisanie programu,
który wyświetli najczęstsze jednostki nazewnicze
w danym dziele literackim. Należy je zliczać
na dwa sposoby:

    - w takiej postaci, w jakiej występują w tekście,

    - w postaci znormalizowanej.

2. Pobrać z serwisu https://wolnelektury.pl
plik tekstowy z treścią dowolnej książki.

3. Tym razem program należy napisać samodzielnie.
Wskazówki:

    - Kod do wczytywania modelu spaCy i pliku tekstowego
    można zapożyczyć z [poprzedniego laboratorium](https://github.com/PK-PJN/laboratorium04).

    - Należy utworzyć dwa obiekty typu `collections.Counter`
    do zliczania obu postaci jednostek nazewniczych.

    - Iterowanie po jednostkach nazewniczych dokumentu
    `doc` robi się tak:

    ```python
    for ent in doc.ents:
        ...
    ```

    - Napis bezpośrednio odpowiadający treści jednostki
    nazewniczej `ent` otrzymuje się przez `ent.text`

    - Napis w przybliżeniu odpowiadający znormalizowanej
    jednostce nazewniczej `ent` można otrzymać na przykład tak:

    ```python
    ''.join(t.lemma_.title() + t.whitespace_ for t in ent).strip()
    ```

    - Dodanie napisu `'spam'` do licznika `licznik` robi się tak:

    ```python
    licznik['spam'] += 1
    ```

    - N najczęstszych elementów licznika `licznik` wraz z ich
    liczebnością otrzymuje się tak:

    ```python
    for tekst, ile in licznik.most_common(N):
        ...
    ```

4. W sprawozdaniu proszę zamieścić:

   - nazwę przetwarzanej książki;

   - cały kod programu;

   - listę 15 najczętszych jednostek nazewniczych
   w takiej postaci, w jakiej występują w tekście;

   - listę 15 najczęstszych jednostek nazewniczych
   w postaci znormalizowanej.
