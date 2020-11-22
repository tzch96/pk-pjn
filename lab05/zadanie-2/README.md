# Wydobywanie informacji

1. Program, którego opracowanie jest celem tego zadania,
ma demonstrować wydobywanie informacji z tekstów w postaci
trójek semantycznych (podmiot, predykat, dopełnienie).

2. Pobrać i rozpakować jeden z plików, zawierający bazę
danych SQLite z treścią artykułów polskiej Wikipedii na temat
[dzieł literackich](https://drive.google.com/open?id=1gTd7BCxM_C9aPAmvfVO9F3uCi875fBEL)
albo [filmów](https://drive.google.com/open?id=18amHXSBYJupR6drnVhjS8qYzf3VHVVlS).

3. Zainstalować `mwparserfromhell` — pakiet do obróbki
tekstów korzystających ze znaczników MediaWiki.

    ```
    pip install mwparserfromhell
    ```

4. W zrozumieniu działań wykonywanych w punktach
5 i 6 może pomóc uruchomienie programu `pomoc.py`
i wprowadzenie do niego zdań zawierających
odpowiednie relacje. Oto przykłady zdań, które
warto wpisać:

    * Politechnika Krakowska to uczelnia wyższa w Krakowie.

    * Politechnika Krakowska jest uczelnią wyższą w Krakowie.

    * Studenci pilnie robią ciekawe zadanie.

    * Ciekawe zadanie jest pilnie robione przez studentów.

5. Odkomentować fragment funkcji `main()`, w którym
wywołuje się `znajdź_relacje_z_innymi_czasownikami(token)`
i wykonać instrukcje zapisane w ciele funkcji
`znajdź_relacje_z_innymi_czasownikami()`. Wskazówka:
znajdowanie wszystkich dzieci `tokenu`, które są z nim
w odpowiedniej relacji, można odpisać z ciała funkcji
`znajdź_relacje_z_być_lub_to()`.

6. Odkomentować fragment funkcji `main()`, w którym
wywołuje się `znajdź_relacje_w_stronie_biernej(token)`
i wykonać instrukcje zapisane w ciele funkcji
`znajdź_relacje_w_stronie_biernej()`. Wskazówka:
funkcja wbudowana `any()` zwraca wartość logiczną
`True` jeśli istnieje chociaż jeden element spełniający
zadany warunek. Można z niej korzystać mniej więcej tak:

    ```python
    any(x.spam == 42 for x in y.children)
    ```

7. W sprawozdaniu zamieścić cały kod programu `zadanie.py`
oraz po 3 przykładowych relacje z "być lub to", z innymi
czasownikami i w stronie biernej.
