import random
import math
import matplotlib.pyplot as plt

class Drzewo:
    # nr wejścia, które sprawdza gałąź
    nrWejscia = 0
    # nr cechy, którą zwraca ta gałąź, jeżeli jest ostatnia
    nrCechy = 0
    # wartość, dla której dokonujemy porównania, jeżeli jest mniejsza bądź równa to true, jak nie to false
    # przedstawiona jako kolumna i nr wartości rosnąco ze wszystkich wartości
    wartosc = [0 ,0]
    # jeżeli obydwie są None to gałąź jest końcowa
    # gałąź przy true
    prawdziwa = None
    # gałąź przy false
    falszywa = None
    # wartość gini dla gałęzi, jeżeli jest 0 to jest to końcowa
    gini = 0

def budowaDrzewa(wejscie, wyjscie, wartosci, ktoreWejscia, pozostalaWysokosc, unikalneCechy) -> Drzewo:
    # do zapisywania minimalnych wartości
    minGini = 10
    minKtoreWejscie = 0
    minKtoraWartoscWejscia = 0
    minCecha = 0
    # sprawdzamy dla każdej z kolumn z wejść
    for obecnaKolumna in ktoreWejscia:
        # i dla każdej kolumny sprawdzamy gini dla wszystkich cech
        for obecnaKtoraWartosc in range(obecnaKolumna[1], obecnaKolumna[2]):
            ileTrafienCech = [0 for n in range(unikalneCechy)]
            # sprawdzamy ile jest mniejszych bądź równych wartości dla danej kolumny i zliczamy które to cechy
            for wiersz in range(len(wejscie)):
                if wejscie[wiersz][obecnaKolumna[0]] <= wartosci[obecnaKolumna[0]][obecnaKtoraWartosc]:
                    ileTrafienCech[wyjscie[wiersz]] += 1
            # szukamy cechy z największą ilością trafień
            max = 0
            for n in range(1, len(ileTrafienCech)):
                if ileTrafienCech[n] > ileTrafienCech[max]:
                    max = n
            gini = 1 - (ileTrafienCech[max] / len(wejscie))
            if gini < minGini:
                minGini = gini
                minKtoreWejscie = obecnaKolumna[0]
                minKtoraWartoscWejscia = obecnaKtoraWartosc
                minCecha = max
                if gini == 0:
                    break
            if minGini == 0:
                break
        if minGini == 0:
            break

    # po sprawdzeniu możemy wreszcie stworzyć gałąź drzewa z najlepszą wartością
    rezultat = Drzewo()
    rezultat.gini = minGini
    rezultat.nrCechy = minCecha
    rezultat.wartosc = wartosci[minKtoreWejscie][minKtoraWartoscWejscia]
    rezultat.nrWejscia = minKtoreWejscie

    # gini to 0, trzeba stworzyć tylko gałąź dla sytuacji fałszywej
    if minGini == 0 and pozostalaWysokosc > 0:
        # dodawanie fałszywej jeżeli jeszcze można
        temp = [x for x in ktoreWejscia]
        temp[minKtoreWejscie][1] = minKtoraWartoscWejscia + 1
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        if mozna:
            rezultat.falszywa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)
    elif pozostalaWysokosc > 0:
        # dodawanie obu jeżeli można
        print("przed ", ktoreWejscia)
        temp = [x for x in ktoreWejscia]
        temp[minKtoreWejscie][2] = minKtoraWartoscWejscia
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        print("po ", ktoreWejscia)
        if mozna:
            rezultat.prawdziwa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)

        temp = [x for x in ktoreWejscia]
        temp[minKtoreWejscie][1] = minKtoraWartoscWejscia + 1
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        if mozna:
            rezultat.falszywa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)


    return rezultat

# przekazywać 0 : 1, numery w klasach
# funkcja ogólna
def runDTF(wejscie, wyniki, cechyNaDrzewo, maxWysokoscDrzewa):
    # inne zmienne kontrolne
    celnosc = []

    # tworzenie słownika z indeksami cechy i tworzenie tablicy z cechami dla indeksów
    indeksyWgCechy = {}
    for n in wyniki:
        indeksyWgCechy[n] = None
    temp = 0
    for n in indeksyWgCechy:
        indeksyWgCechy[n] = temp
        temp += 1

    cechyWgIndeksow = []
    for n in indeksyWgCechy:
        cechyWgIndeksow.append(n)

    # tworzenie tablicy wyników z indeksami
    wynikiNowe = [indeksyWgCechy[n] for n in wyniki]

    # przygotowywanie danych do tworzenia drzew
    # wartości występujące w danych wejściach posortowane potem rosnąco
    temp = [{} for n in range(len(wejscie[0]))]
    for n in range(len(wejscie)):
        for m in range(len(wejscie[n])):
            temp[m][wejscie[n][m]] = None

    wartosciWejsc = [[m for m in temp[n]] for n in range(len(temp))]
    for n in wartosciWejsc:
        n.sort()

    # na tym etapie mamy już przesortowaną tablicę z wartościami, według których będziemy iterować
    # następnie trzeba przygotować struktury drzew poprzez przechodzenie przez te wszystkie wartości
    # i sprawdzanie, która pierwsza zapewni nam gini = 0 (chyba tak to może działać a przyspieszy)

    drzewo = budowaDrzewa(wejscie, wynikiNowe, wartosciWejsc, [[0, 0, len(wartosciWejsc[0])], [1, 0, len(wartosciWejsc[1])]], 4, len(cechyWgIndeksow))






    print("koniec breakpoint")
