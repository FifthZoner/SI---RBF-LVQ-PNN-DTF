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
            ileTrafienCech = [[0, 0] for n in range(unikalneCechy)]
            sumyTrafien = [0, 0]
            # sprawdzamy ile jest mniejszych bądź równych wartości dla danej kolumny i zliczamy które to cechy
            ileUjetychWejsc = [0, 0]
            for wiersz in range(len(wejscie)):
                # sprawdzanie czy dany wiersz może być sprawdzony
                czyLiczyc = True
                for n in range(len(ktoreWejscia)):
                    if wejscie[wiersz][obecnaKolumna[0]] < wartosci[obecnaKolumna[0]][obecnaKolumna[1]] or wejscie[wiersz][obecnaKolumna[0]] > wartosci[obecnaKolumna[0]][obecnaKolumna[2] - 1]:
                        czyLiczyc = False
                # sprawdzanie czy liczy się do trafionych
                #print(czyLiczyc)
                if czyLiczyc:

                    ileTrafienCech[wyjscie[wiersz]][1] += 1
                    if wejscie[wiersz][obecnaKolumna[0]] <= wartosci[obecnaKolumna[0]][obecnaKtoraWartosc]:
                        ileUjetychWejsc[0] += 1
                        ileTrafienCech[wyjscie[wiersz]][0] += 1
                        sumyTrafien[0] += 1
                    else:
                        ileUjetychWejsc[1] += 1
                        sumyTrafien[1] += 1

            # szukamy cechy z największą ilością trafień
            #gini = 1 - (ileTrafienCech[max] / ileUjetychWejsc)
            gini = 1
            giniPrawdziwe = 1
            giniFalszywe =1
            for n in ileTrafienCech:
                giniPrawdziwe -= math.pow(n[0] / ileUjetychWejsc[0], 2)
                if ileUjetychWejsc[1] > 0:
                    giniFalszywe -= math.pow((n[1] - n[0]) / ileUjetychWejsc[1], 2)
                else:
                    giniFalszywe = 1
            gini = ((giniPrawdziwe * sumyTrafien[0]) + (giniFalszywe * sumyTrafien[1])) / (ileUjetychWejsc[0] + ileUjetychWejsc[1])
            if gini <= minGini:
                max = 0
                for n in range(1, len(ileTrafienCech)):
                    if ileTrafienCech[n][0] / ileUjetychWejsc[0] > ileTrafienCech[max][0] / ileUjetychWejsc[0]:
                        max = n
                minGini = gini
                minIndeksTymczasowyWejscia = obecnaKolumna[3]
                minKtoraWartoscWejscia = obecnaKtoraWartosc
                minCecha = max
                #print(max)
                if gini == 0:
                    break

            if minGini == 0:
                break
        #print(minCecha)
        if minGini == 0:
            break

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
def runDTF(wejscie, wyniki, tablicaDrzew, maxWysokoscDrzewa, wejscieKontrolne, wyjscieKontrolne):
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


    #tablicaDrzew = []
    #tablicaDrzew = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [2, 4, 5], [6, 8, 3], [1, 8, 9], [2, 6, 9]]
    #tablicaDrzew = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]

    # kombinacje bez powtorzen here



    #drzewo = budowaDrzewa(wejscie, wynikiNowe, wartosciWejsc, [[8, 0, len(wartosciWejsc[8]), 0],
    #                      [10, 0, len(wartosciWejsc[10]), 1]],
    #                      1, len(cechyWgIndeksow))

    #tablicaDrzew = [[0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 1, 6], [0, 1, 7], [0, 1, 8], [0, 1, 9], [0, 1, 10],
    #                [0, 2, 3], [0, 2, 4], [0, 2, 5], [0, 2, 6], [0, 2, 7], [0, 2, 8], [0, 2, 9], [0, 2, 10], [0, 3, 4],
    #                [0, 3, 5], [0, 3, 6], [0, 3, 7], [0, 3, 8], [0, 3, 9], [0, 3, 10], [0, 4, 5], [0, 4, 6], [0, 4, 7],
    #                [0, 4, 8], [0, 4, 9], [0, 4, 10], [0, 5, 6], [0, 5, 7], [0, 5, 8], [0, 5, 9], [0, 5, 10], [0, 6, 7],
    #                [0, 6, 8], [0, 6, 9], [0, 6, 10], [0, 7, 8], [0, 7, 9], [0, 7, 10], [0, 8, 9], [0, 8, 10], [0, 9, 10]]


    drzewa  = [None for n in range(len(tablicaDrzew))]
    for n in range(len(tablicaDrzew)):
        print(n + 1, " / ", len(tablicaDrzew))
        wejscia = []
        for m in range(len(tablicaDrzew[n])):
            wejscia.append([tablicaDrzew[n][m], 0, len(wartosciWejsc[tablicaDrzew[n][m]]), m])
        drzewa[n] = budowaDrzewa(wejscie, wynikiNowe, wartosciWejsc, wejscia, maxWysokoscDrzewa, len(cechyWgIndeksow))

    print("Sprawdzanie celności wyjścia...")

    wynikiDrzew = [[] for n in range(len(drzewa))]

    for n in range(len(wejscieKontrolne)):
        for m in range(len(drzewa)):
            #wynikiDrzew[m].append(cechyWgIndeksow[wynikZDrzewa(drzewa[m], wejscie[n])])
            wynikiDrzew[m].append(wynikZDrzewa(drzewa[m], wejscieKontrolne[n]))



    #print("Celność wytrenowanego drzewa to: ", trafione / len(wejscie) * 100, "%")

    # wybieranie najpopularniejszych wyników
    wynikiWiekszosci = []
    for n in range(len(wyjscieKontrolne)):
        # pierwsze sprawdzamy które opcje są najpopularniejsze
        wybrane = [0 for n in range(len(cechyWgIndeksow))]
        for m in range(len(drzewa)):
            wybrane[wynikiDrzew[m][n]] += 1

        # szukanie wyników z największą ilością
        opcje = []
        for n in range(len(wybrane)):
            if len(opcje) == 0:
                opcje.append([n, wybrane[n]])
            else:
                if opcje[0][1] < wybrane[n]:
                    opcje.clear()
                    opcje.append([n, wybrane[n]])
                elif opcje[0][1] == wybrane[n]:
                    opcje.append([n, wybrane[n]])
        # losowanie wyniku z opcji jeżeli drzewa nie były jednomyślne
        wynikiWiekszosci.append(cechyWgIndeksow[opcje[random.randint(0, len(opcje) - 1)][0]])

    wynikiSuma = [0 for n in range(len(wynikiDrzew))]
    wynikKonsensusu = 0
    for n in range(len(wynikiDrzew)):
        for m in range(len(wynikiDrzew[n])):
            if cechyWgIndeksow[wynikiDrzew[n][m]] == wyjscieKontrolne[m]:
                wynikiSuma[n] += 1
    for n in range(len(wyjscieKontrolne)):
        if wynikiWiekszosci[n] == wyjscieKontrolne[n]:
            wynikKonsensusu += 1
    for n in range(len(wynikiSuma)):
        print("Celność wytrenowanego nr: ", n + 1, " drzewa to: ", wynikiSuma[n] / len(wyjscieKontrolne) * 100, "%")
    print("Celność lasu drzew wg większości + losowanie przy wielu to: ", wynikKonsensusu / len(wyjscieKontrolne) * 100, "%")
    print("koniec breakpoint")
