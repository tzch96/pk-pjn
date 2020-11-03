# Odpowiadanie na pytania

## Treść zadania

Celem tego zadania jest opracowanie programu,
który odpowiada na pytania o pracowników
Wydziału Informatyki i Telekomunikacji,
czerpiąc odpowiedzi z niewielkiej bazy danych.
Program powinien sensownie odpowiadać np.
na takie pytania:

```
    W której katedrze pracuje doktor Ciura?
    Jaki jest adres email pana dziekana?
    Jacy profesorowie są pracownikami F-3?
    Kto ma telefon o numerze 26-66?
    Czy znasz kogoś o imieniu Filip?
    Parlez-vous français ?
```

Oczywiście gdzieś trzeba postawić granicę,
bo od żadnego programu nie można się spodziewać
zadowalających odpowiedzi na wszelkie możliwe
pytania:

```
    Jakie było najgłupsze pytanie, które ci kiedykolwiek zadano?
```

Sztuka polega na rozsądnym odpowiadaniu na jak
najwięcej pytań bez nadmiernego komplikowania
programu. Zakładamy, że użytkownik programu ma
niewielkie doświadczenie z komputerami i nie
chce czytać podręcznika ani uczyć się reguł
zadawania pytań. Wiemy o nim tylko to, że zna
język polski i umie pisać na klawiaturze.

Nie należy zakładać, że użytkownik będzie się
starał wywieść program w pole. Dialog między
użytkownikiem a programem można raczej porównać
do próby porozumienia się w języku, który słabo
rozumiemy. Ludzie w takich sytuacjach zawsze
znajdą sposób, żeby przekazać sobie, o co chodzi.

## Podejście

Dane o pracownikach będziemy przechowywać w tabeli
bazy danych SQLite o następującym schemacie:

```sql
    CREATE TABLE Pracownicy(
        docid       INTEGER PRIMARY KEY
        , jednostka TEXT
        , pracownik TEXT
        , email     TEXT
        , telefon   TEXT
    );
```

Do wyszukiwania danych w tabeli `Pracownicy`
posłuży wirtualna tabela `PracownicyFTS`
(FTS = Full-Text Search). Zawiera ona pozbawione
końcówek odmiany i polskich znaków diakrytycznych
oraz sprowadzone do małych liter wyrazy, służące
do wyszukiwania:

```sql
    CREATE VIRTUAL TABLE PracownicyFTS USING fts4(dane);
```

Na przykład temu wierszowi tabeli `Pracownicy`:

```sql
    INSERT INTO Pracownicy(
        docid
        , jednostka
        , pracownik
        , email
        , telefon
    ) VALUES (
        77
        , 'Katedra Teleinformatyki (F-3)'
        , 'dr inż. Marcin Ciura'
        , 'marcin.ciura@pk.edu.pl'
        , ''
    );
```

odpowiada następujący wiersz tabeli
`PracownicyFTS`:

```sql
    INSERT INTO PracownicyFTS(docid, dane)
    VALUES(77, 'teleinformatyk f3 dr inz marcin ciur');
```

Olbrzymia większość pytań do naszego programu
zawiera określenie *wartości* pewnych kolumn,
być może wyszczególnienie innych **kolumn**,
których wartość interesuje użytkownika, oraz
„szum”, czyli wyrazy, które nie wpływają na
interpretację pytania, np.

W której **katedrze** pracuje *doktor Ciura*?

Jaki jest adres **email** pana *dziekana*?

Jacy **profesorowie** są pracownikami *F-3*?

Kto ma **telefon** o numerze *26-66*?

Czy znasz kogoś o imieniu *Filip*?

Powyższym pytaniom odpowiadają następujące
zapytania SQL:

```sql
    SELECT pracownik, jednostka
    FROM Pracownicy JOIN PracownicyFTS USING(docid)
    WHERE PracownicyFTS MATCH 'dr ciur';

    SELECT pracownik, email
    FROM Pracownicy JOIN PracownicyFTS USING(docid)
    WHERE PracownicyFTS MATCH 'dziekan';

    SELECT pracownik, jednostka
    FROM Pracownicy JOIN PracownicyFTS USING(docid)
    WHERE PracownicyFTS MATCH 'prof f3';

    SELECT pracownik, telefon
    FROM Pracownicy JOIN PracownicyFTS USING(docid)
    WHERE PracownicyFTS MATCH '2666';

    SELECT pracownik
    FROM Pracownicy JOIN PracownicyFTS USING(docid)
    WHERE PracownicyFTS MATCH 'filip';
```

## Implementacja

W ramach zadania należy zaimplementować:

1. Podział wczytanego z klawiatury pytania
na wyrazy i usuwanie znaków przestankowych,
np. `'Gdzie pracuje dr Kowalska-Wójcik?'` →
`['Gdzie', 'pracuje', 'dr', 'Kowalska', 'Wójcik']` (✅).

2. Usuwanie znaków diakrytycznych, np.
`'Wójcik'` → `'Wojcik'` (✅).

3. Zamianę liter na małe, np. `'Wojcik'` →
`'wojcik'` (✅).

4. Usuwanie końcówek odmiany, czasem z wariantami,
np. `'profesorowie'` → `['profesor']`, `'jednostce'`
→ `['jednostk']`, `'Kowalskiego'` → `['kowalsk']`,
`'Grygiel'` → `['grygiel', 'grygl']` (¾✅¼❌).

5. Normalizowanie kodów jednostek organizacyjnych, np.
`'F-1'` -> `'f1'` (❌).

6. Normalizowanie numerów telefonów, np. `'21 02'`,
`'628-21-02'` → `'2102'` (❌).

7. Przypisanie niektórym wyrazom odpowiadających im
synonimów, używanych w tabeli PracownicyFTS, np.
`'doktor'` → '`dr'`, `'habilitowan'` → `'hab'` (❌).

8. Przypisanie niektórym wyrazom odpowiadających im
kolumn tabeli Pracownicy, np. `'gd'` (z `'gdzie'`),
`'jednostk'`, `'katedr'` → `jednostka`;
`'numer'`, `'telefon'` → `telefon` (❌).

9. Ekstrakcję z pytania tych kolumn tabeli `Pracownicy`,
które mają się znaleźć w odpowiedzi (kolumna
`pracownik` zawsze się tam znajdzie), oraz tekstu
warunku, który zostanie użyty w zapytaniu SQL, np.
`'Gdzie pracuje doktor Grygiel?'` →
`[['gd'], ['pracuj'], ['dr'], ['grygiel', 'grygl']]` →
`(kolumny={'pracownik', 'jednostka'}), tekst_warunku='dr grygiel OR grygl')`
(❌).

10. Zbudowanie i wykonanie zapytania SQL
oraz prezentację jego wyniku (❌);

## Podzadania do wykonania

W pliku `utils.py`:

1. Dopisać do regexpu `_BEZ_DŁUŻSZEJ_KOŃCÓWKI`
rozpoznawanie końcówek odmiany rzeczowników
i przymiotników. Uwagi:

    * W tematach rzeczowników występują cztery
    regularne wymiany samogłosek:
    ą:ę, ó:o, e:∅, ie:∅.

    * Wymiana ą:ę nie występuje w odmianie
    nazwisk: *pan Gołąb*:*pana Gołąba*.

    * Nie występuje w niej też wyjątkowa
    wymiana io:∅: *pan Kozioł*:*pana Kozioła*.

    * Wymianę ó:o obsługuje usuwanie znaków
    diakrytycznych: *pan Mróz*:*pana Mroza*.

    * Pozostają wymiany e:∅: *pan Mazurek*:*pana Mazurka*
    oraz ie:∅, w której obsłudze trochę pomaga
    usuwanie znaków diakrytycznych:
    *pan Maciek*:*pana Maćka*.

2. Plik `utils.py` zawiera testy do podzadania
opisanego w powyższym punkcie. Do dalszych podzadań
można przejść, jeśli jego wykonanie przebiegnie
bez błędów:

    ```
    python3 utils.py
    ```

W pliku `normalizacja.py`:

1. Uzupełnić funkcję `normalizuj_kody_jednostek()`
tak, żeby zamieniała:

    * wystąpienia od jednej do dwóch liter,
    ciągu białych znaków lub znaków minus
    i od jednej do dwóch cyfr na:

    * litery, po których bezpośrednio następują cyfry,
    np. `'Kto pracuje w Ś 2?'` → `'Kto pracuje w Ś2?'`,
    `'Podaj mi pracowników PN-5.'` → `'Podaj mi pracowników PN5.'`,
    `'I - 01'` → `'I01'`.

2. Uzupełnić funkcję `normalizuj_numery_telefonów()`
tak, żeby zamieniała:

   * wystąpienia dwóch cyfr, ciągu białych znaków
   lub znaków minus i dwóch cyfr, opcjonalnie
   poprzedzonych przez znaki `'628'`, `'12 628'`,
   `'+48 12 628'` itp., na:

   * cztery cyfry, np. `'21 05'`, `'21-05'`,
   `'628 - 21 - 05'` → `'2105'`.

3. Plik `normalizacja.py` zawiera testy do podzadań
opisanych w powyższych dwóch punktach. Do dalszych
podzadań można przejść, jeśli jego wykonanie
przebiegnie bez błędów:

    ```
    python3 normalizacja.py
    ```

4. Stworzyć plik z bazą danych poprzez wydanie polecenia

    ```
    python3 tworz_baze.py
    ```

W pliku `odpowiedz.py`:

1. Jeśli pracujemy pod Windows, zainstalować pakiet `pyreadline`:

    ```
    pip install pyreadline
    ```

2. Dopisać synonimy do słownika `SYNONIMY`.

3. Dopisać synonimy do słownika `KOLUMNY`.

4. Uzupełnić funkcję `odpowiedz()`.
Pod żadnym pozorem nie należy wstawiać tekstu
warunku do zapytania SQL, bo ten paskudny zwyczaj
otwiera drogę do ataków, znanych jako *SQL injection*
(więcej wiadomości o *SQL injection*
[tu](https://xkcd.com/327/)
i [tu](https://prod.ceidg.gov.pl/CEIDG/ceidg.public.ui/SearchDetails.aspx?Id=e82735cd-bc2b-4ac0-8bac-a1dc54d8c013);
z kolumnami nie da się tak zrobić,
trzeba wkleić ich nazwy do napisu `zapytanie_sql`).
Zamiast tego należy użyć parametru:

```python
    zapytanie_sql = '…WHERE PracownicyFTS MATCH ?'
    connection.execute(zapytanie_sql, [tekst_warunku])
```

W sprawozdaniu zamieścić:

1. Regexp `_BEZ_DŁUŻSZEJ_KOŃCÓWKI` z pliku `utils.py`;

2. Regexpy `_JEDNOSTKA_RE` i `_TELEFON_RE` z pliku `normalizacja.py`;

3. Funkcję `odpowiedz()` z pliku `odpowiedz.py`;

4. Pięć przykładowych pytań użytkownika
(innych niż w tej instrukcji)
i odpowiedzi na nie.

Opracowano na podstawie zadania 5.
z seminarium programowania i rozwiązywania zadań,
prowadzonego w roku 1981 na Uniwersytecie Stanforda
przez Donalda E. Knutha i Josepha S. Weeninga:
[CS-TR-83-989](http://i.stanford.edu/pub/cstr/reports/cs/tr/83/989/CS-TR-83-989.pdf#page=71).
