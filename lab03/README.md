# Przetwarzanie języka naturalnego
# Laboratorium 3: stylometria i redukcja wymiarowości

1. Skopiować zawartość niniejszego repozytorium
na dysk lokalny. Pobrać i rozpakować plik [teksty.zip](https://drive.google.com/file/d/1kHEp0gL8gDlIA7YBifO6vP3gMJLhaWN2/view?usp=sharing).

    ```
    git clone https://github.com/PK-PJN-NS/laboratorium-3.git
    cd laboratorium-3
    unzip teksty.zip
    ```

2. Zainstalować `matplotlib` — zewnętrzną bibliotekę Pythona,
która służy do tworzenia wykresów, oraz `scikit-learn` —
bibliotekę z narzędziami do uczenia maszynowego.

    ```
    pip install matplotlib
    pip install sklearn
    ```

3. Pobrać z serwisu https://wolnelektury.pl co najmniej
trzy pliki tekstowe z książkami autorstwa co najmniej dwóch
polskich pisarzy lub pisarek innych niż Prus i Sienkiewicz.
Zapisać je wewnątrz folderu `teksty` pod nazwami
*nazwisko-tytuł-połączony-minusami.txt*.

4. *Stylometria* polega na stosowaniu narzędzi statystycznych
do badania stylu tekstów. W ramach laboratorium użyjemy
częstości końcowych znaków przestankowych, przecinków i tzw.
*wyrazów funkcyjnych* w tekstach polskich (zobacz stałą
`INTERESTING_TOKEN_SET` w pliku `zadanie.py`).

5. Uzupełnić funkcję `analyze()`: iterować po liście `tokens`,
zamieniając każdy segment (ang. *token*) na małe litery. Jeśli
wynik zamiany należy do zbioru `INTERESTING_TOKEN_SET`,
zwiększyć odpowiedni element licznika `counter` o 1.

6. Uzupełnić funkcję `analyze()`: iterując po liście
`INTERESTING_TOKEN_LIST`, dodawać do zmiennej `result`
wynik dzielenia odpowiedniego elementu licznika `counter`
przez `len(tokens)`.

7. W wyniku wywołania funkcji `analyze()` otrzymujemy
dla każdego pliku z folderu `teksty` 90-wymiarowy wektor
(nazwa jest trochę myląca; w programie te liczby są
przechowywane w tablicy jednowymiarowej o 90 elementach)
częstości interesujących nas segmentów w tekście. Żeby
porównać wzrokiem wektory, które odpowiadają poszczególnym
książkom, zastosujemy metody *redukcji wymiarowości*.

8. Pierwsza z zastosowanych metod redukcji wymiarowości
to *analiza składowych głównych* (*Principal Component
Analysis*). W bibliotece `scikit-learn` odpowiada za nią
klasa `decomposition.PCA`. Za pomocą tej metody zrzutowaliśmy
90-wymiarową przestrzeń na 2 kierunki. Metoda wybiera je tak,
żeby w układzie współrzędnych opartym na tych kierunkach
zmienność (wariancja) danych była jak największa. Innymi
słowy: w pozostałych, niewidocznych kierunkach dane różnią
się jak najmniej.

9. Kolejna metoda redukcji wymiarowości to *analiza
czynnikowa* (*Factor Analysis*). W bibliotece `scikit-learn`
odpowiada za nią klasa `decomposition.FactorAnalysis`.
Za pomocą analizy czynnikowej można znaleźć niewielką liczbę
czynników (kierunków), które stoją za danymi, przy założeniu,
że kombinacje liniowe tych czynników są zaburzane przez szum
o rozkładzie normalnym. Uzupełnić funkcję `main()` o rysowanie
diagramu wyników analizy czynnikowej.

10. Kolejna metoda redukcji wymiarowości to *skalowanie
wielowymiarowe* (*Multidimensional Scaling*). W biliotece
`scikit-learn` odpowiada za nią klasa `manifold.MDS`.
Za pomocą skalowania wielowymiarowego znajduje się
takie położenie punktów w przestrzeni o niskiej liczbie
wymiarów, że odległości między tymi punktami dobrze
przybliżają odległości między ich odpowiednikami
w wejściowej przestrzeni o wysokiej liczbie wymiarów.
Uzupełnić funkcję `main()` o rysowanie diagramu wyników
skalowania wielowymiarowego.

11. W sprawozdaniu zamieścić autorów i tytuły książek
pobranych zgodnie z punktem 3, treść funkcji `analyze()`
i `main()` oraz trzy diagramy, przedstawiające wyniki
analizy składowych głównych, analizy czynnikowej
i skalowania wielowymiarowego danych stylometrycznych
wszystkich książek z folderu `teksty`.

12. Zadanie nadobowiązkowe: ruchome wykresy trójwymiarowe.
Wymagane jest zainstalowanie programu [ImageMagick](https://imagemagick.org/)
(to jest osobny program, niezwiązany z Pythonem).

    * Rysowanie poszczególnych punktów odbywa się
    podobnie, jak przy wykresach dwuwymiarowych.
    Należy tylko podawać trzy współrzędne punktów
    zamiast dwóch.

    * Żeby wykres się poruszał, trzeba w funkcji
    `draw_frame()` zmieniać *azymut* (`azim`),
    czyli kąt między punktem widzenia a południkiem
    zerowym, oraz *wysokość* (`elev`), czyli kąt
    między punktem widzenia a płaszczyzną horyzontu.

    * Uzupełnić wartości stałych `NUM_FRAMES`,
    `ELEVATION_ZERO`, `ELEVATION_SPEED`,
    `AZIMUTH_ZERO`, `AZIMUTH_SPEED` w funkcji
    `plot3d()`. Kąty podać w mierze stopniowej,
    czyli nie w radianach. Wskazówka 1: całkiem
    niezłe wyniki można otrzymać przy
    `ELEVATION_SPEED = 0`. Wskazówka 2:
    wartość `AZIMUTH_SPEED` powinna być niewielka,
    żeby ruch wydawał się płynny. Wskazówka 3:
    najlepiej wszystko widać, kiedy punkt widzenia
    jest wzniesiony mniej więcej 30°–45° ponad horyzont.

    * Obliczyć `elev` i `azim` w funkcji `draw_frame()`
    tak, by w pierwszej połowie klatek punkt widzenia
    przemieszczał się od punktu (`AZIMUTH_ZERO`, `ELEVATION_ZERO`)
    z prędkością (`AZIMUTH_SPEED`, `ELEVATION_SPEED`)
    na klatkę.

    * Obliczyć `elev` i `azim` w funkcji `draw_frame()`
    tak, by w drugiej połowie klatek punkt widzenia
    przemieszczał się od punktu
    (`AZIMUTH_ZERO + NUM_FRAMES * AZIMUTH_SPEED`,
    `ELEVATION_ZERO + NUM_FRAMES * ELEVATION_SPEED`)
    w kierunku punktu (`AZIMUTH_ZERO`, `ELEVATION_ZERO`)
    z prędkością (`-AZIMUTH_SPEED`, `-ELEVATION_SPEED`)
    na klatkę.

    * Dodać do funkcji `main()` odpowiednie wywołania
    funkcji `plot3d()`. Pamiętać o zmianie `n_components`
    na 3 i o podawaniu różnych parametrów `gif_name`
    z rozszerzeniem `.gif`.

    * Dołączyć do sprawozdania treść funkcji `plot3d()`
    oraz przesłać jako osobne pliki otrzymane GIF-y.
    (O ile mi wiadomo, w PDF-ach byłoby widać tylko
    pierwsze klatki ruchomych GIF-ów). Ewentualnie
    skorzystać z usługi https://cloudconvert.com/gif-to-mp4,
    żeby skonwertować GIF-y na pliki wideo, które
    widać w PDF-ach jako ruchome obrazki. (Wada:
    plików wideo nie da się zapętlić).
