import random
import math
import matplotlib.pyplot as plt

# przekazywać kopie z -1 : 1
def runLVQ(wejscie, wyniki):
    # zmiana z daych -1 : 1 na 0 : 1
    for n in range (0, len(wejscie)):
        for m in range (0, 11):
            wejscie[n][m] = (wejscie[n][m] + 1) / 2
        wyniki[n] = int((wyniki[n] + 1) * 5)
    #print(wyniki)
    # przygotowywanie wagi startowej, neurony z klasami 1 : 9
    wagi = []
    #for n in range(0, 9):
    #    wagi.append([])
    #    for m in range (0, 11):
    #        wagi[n].append(random.uniform(0, 1))
    #        #print(wagi[n][m])
    for n in range(0, 9):
        wagi.append(wejscie.pop())
        wyniki.pop()

    # inne zmienne kontrolne
    alfa = 0.001
    liczbaEpok = 10000
    celnosc = []

    # trenowanie
    for epoka in range (0, liczbaEpok):
        # zmienne statystyczne
        liczbaTrafionych = 0
        for wiersz in range (0, len(wejscie)):

            # szukanie "wygranego"
            dystanse = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for kolumna in range(0, len(wejscie[wiersz])):
                for n in range(0, len(wagi)):
                    #print(wagi[n][kolumna])
                    dystanse[n] += math.pow(wejscie[wiersz][kolumna] - wagi[n][kolumna], 2)
            wygrany = 0
            for n in range(1, len(dystanse)):
                if dystanse[n] < dystanse[wygrany]:
                    wygrany = n

            # jeżeli wygrany zgadza się z wynikiem to zbliżamy go, alternatywnie oddalamy
            # +1 bo wartości są od 1 a indeksy od 0
            #print( wygrany + 1, " : ", wyniki[wiersz])
            if wygrany + 1 == wyniki[wiersz]:
                liczbaTrafionych += 1
                #print("+ ", wagi[wygrany])
                #print("with ", wejscie[wiersz])
                for n in range(0, len(wejscie[wiersz])):
                    wagi[wygrany][n] += alfa * (wejscie[wiersz][n] - wagi[wygrany][n])
                #print("+ ", wagi[wygrany])
            else:
                #print("- ", wagi[wygrany])
                #print("with ", wejscie[wiersz])
                for n in range(0, len(wejscie[wiersz])):
                    wagi[wygrany][n] -= alfa * (wejscie[wiersz][n] - wagi[wygrany][n])
                #print("- ", wagi[wygrany])

        print(epoka + 1, ": ", liczbaTrafionych, " / ", len(wejscie))
        celnosc.append(liczbaTrafionych / len(wejscie) * 100)

    # wyswietlanie wyników
    plt.plot(celnosc)
    plt.ylabel("Procent poprawnie zaklasyfikowanych")
    plt.xlabel("Numer epoki")
    plt.show()