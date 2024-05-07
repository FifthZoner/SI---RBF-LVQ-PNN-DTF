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
    minIndeksTymczasowyWejscia = 0
    minKtoraWartoscWejscia = 0
    minCecha = 0
    # sprawdzamy dla każdej z kolumn z wejść
    for obecnaKolumna in ktoreWejscia:
        # i dla każdej kolumny sprawdzamy gini dla wszystkich cech
        for obecnaKtoraWartosc in range(obecnaKolumna[1], obecnaKolumna[2]):
            ileTrafienCech = [0 for n in range(unikalneCechy)]
            # sprawdzamy ile jest mniejszych bądź równych wartości dla danej kolumny i zliczamy które to cechy
            ileUjetychWejsc = 0
            for wiersz in range(len(wejscie)):
                # sprawdzanie czy dany wiersz może być sprawdzony
                czyLiczyc = True
                for n in range(len(ktoreWejscia)):
                    if wejscie[wiersz][obecnaKolumna[0]] < wartosci[obecnaKolumna[0]][obecnaKolumna[1]] or wejscie[wiersz][obecnaKolumna[0]] > wartosci[obecnaKolumna[0]][obecnaKolumna[2] - 1]:
                        czyLiczyc = False
                # sprawdzanie czy liczy się do trafionych
                if czyLiczyc:
                    ileUjetychWejsc += 1
                    if wejscie[wiersz][obecnaKolumna[0]] <= wartosci[obecnaKolumna[0]][obecnaKtoraWartosc]:
                        ileTrafienCech[wyjscie[wiersz]] += 1

            # szukamy cechy z największą ilością trafień
            max = 0
            for n in range(1, len(ileTrafienCech)):
                if ileTrafienCech[n] > ileTrafienCech[max]:
                    max = n
            gini = 1 - (ileTrafienCech[max] / ileUjetychWejsc)
            if gini <= minGini:
                minGini = gini
                minIndeksTymczasowyWejscia = obecnaKolumna[3]
                minKtoraWartoscWejscia = obecnaKtoraWartosc
                minCecha = max
                #print(max)
                if gini == 0:
                    break
            if minGini == 0:
                break
        #if minGini == 0:
            #break

    # po sprawdzeniu możemy wreszcie stworzyć gałąź drzewa z najlepszą wartością
    rezultat = Drzewo()
    rezultat.gini = minGini
    rezultat.nrCechy = minCecha
    rezultat.wartosc = wartosci[ktoreWejscia[minIndeksTymczasowyWejscia][0]][minKtoraWartoscWejscia]
    rezultat.nrWejscia = ktoreWejscia[minIndeksTymczasowyWejscia][0]

    # gini to 0, trzeba stworzyć tylko gałąź dla sytuacji fałszywej
    if minGini == 0 and pozostalaWysokosc > 0:
        # dodawanie fałszywej jeżeli jeszcze można
        temp = [x.copy() for x in ktoreWejscia]
        temp[minIndeksTymczasowyWejscia][1] = minKtoraWartoscWejscia + 1
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        if mozna:
            rezultat.falszywa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)
    elif pozostalaWysokosc > 0:
        # dodawanie obu jeżeli można
        #print("przed ", ktoreWejscia)
        temp = [x.copy() for x in ktoreWejscia]
        temp[minIndeksTymczasowyWejscia][2] = minKtoraWartoscWejscia
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        #print("po ", ktoreWejscia)
        if mozna:
            rezultat.prawdziwa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)

        temp = [x.copy() for x in ktoreWejscia]
        temp[minIndeksTymczasowyWejscia][1] = minKtoraWartoscWejscia + 1
        mozna = False
        for n in temp:
            if n[2] - n[1] > 1:
                mozna = True
        if mozna:
            rezultat.falszywa = budowaDrzewa(wejscie, wyjscie, wartosci, temp.copy(), pozostalaWysokosc - 1, unikalneCechy)


    return rezultat

# zwraca wynik z gałęzi dla podanego wektora wejściowego
def wynikZDrzewa(drzewo, wektor):
    if wektor[drzewo.nrWejscia] <= drzewo.wartosc:
        # jeżeli warunek został spełniony
        if drzewo.prawdziwa != None:
            # jeżeli jest dalsza gałąź zwróć wartość z jej sprawdzenia
            return wynikZDrzewa(drzewo.prawdziwa, wektor)
        else:
            return drzewo.nrCechy
    else:
        if drzewo.falszywa != None:
            # jeżeli jest dalsza gałąź zwróć wartość z jej sprawdzenia
            return wynikZDrzewa(drzewo.falszywa, wektor)
        else:
            return drzewo.nrCechy




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

    print("Budowanie drzew...")

    tablicaDrzew = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]

    #drzewo = budowaDrzewa(wejscie, wynikiNowe, wartosciWejsc, [[8, 0, len(wartosciWejsc[8]), 0],
    #                      [10, 0, len(wartosciWejsc[10]), 1]],
    #                      1, len(cechyWgIndeksow))

    drzewa  = [None for n in range(len(tablicaDrzew))]
    for n in range(len(tablicaDrzew)):
        print(n + 1, " / ", len(tablicaDrzew))
        wejscia = []
        for m in range(len(tablicaDrzew[n])):
            wejscia.append([tablicaDrzew[n][m], 0, len(wartosciWejsc[tablicaDrzew[n][m]]), m])
        drzewa[n] = budowaDrzewa(wejscie, wynikiNowe, wartosciWejsc, wejscia, 2, len(cechyWgIndeksow))

    print("Sprawdzanie celności wyjścia...")

    wynikiDrzew = [[] for n in range(len(drzewa))]

    for n in range(len(wejscie)):
        for m in range(len(drzewa)):
            #wynikiDrzew[m].append(cechyWgIndeksow[wynikZDrzewa(drzewa[m], wejscie[n])])
            wynikiDrzew[m].append(wynikZDrzewa(drzewa[m], wejscie[n]))


    #print("Celność wytrenowanego drzewa to: ", trafione / len(wejscie) * 100, "%")


    print("koniec breakpoint")
