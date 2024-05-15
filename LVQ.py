import random
import math
import matplotlib.pyplot as plt

# przekazywać kopie z 0 : 1
def runLVQ(wejscie, wyniki, liczbaEpok, alfa, wejscieKontrolne, wyjscieKontrolne):

    cechyNaIndeksy = {}
    for n in wyniki:
        cechyNaIndeksy[n] = []
    for n in range(0, len(wyniki)):
        cechyNaIndeksy[wyniki[n]].append(n)
    indeksyNaCechy = []
    m = 0
    for n in cechyNaIndeksy:
        indeksyNaCechy.append(n)
        cechyNaIndeksy[n] = m
        m += 1
    # przygotowywanie wagi startowej, neurony z klasami 1 : 9
    wagi = []
    opcje = [[] for n in range(len(indeksyNaCechy))]
    for n in range(0, len(wyniki)):
        opcje[cechyNaIndeksy[wyniki[n]]].append(n)
    for n in opcje:
        ktora = random.randint(0, len(n) - 1)
        wagi.append(wejscie[ktora])
        wejscie.pop(ktora)

    # inne zmienne kontrolne
    celnosc = []

    # trenowanie
    for epoka in range (0, liczbaEpok):
        # zmienne statystyczne
        liczbaTrafionych = 0
        for wiersz in range (0, len(wejscie)):

            # szukanie "wygranego"
            dystanse = [0 for n in range(len(indeksyNaCechy))]
            for kolumna in range(0, len(wejscie[wiersz])):
                for n in range(0, len(wagi)):
                    dystanse[n] += math.pow(wejscie[wiersz][kolumna] - wagi[n][kolumna], 2)
            wygrany = 0
            for n in range(1, len(dystanse)):
                if dystanse[n] < dystanse[wygrany]:
                    wygrany = n

            # jeżeli wygrany zgadza się z wynikiem to zbliżamy go, alternatywnie oddalamy
            if indeksyNaCechy[wygrany] == wyniki[wiersz]:
                liczbaTrafionych += 1
                for n in range(0, len(wejscie[wiersz])):
                    wagi[wygrany][n] += alfa * (wejscie[wiersz][n] - wagi[wygrany][n])
            else:
                for n in range(0, len(wejscie[wiersz])):
                    wagi[wygrany][n] -= alfa * (wejscie[wiersz][n] - wagi[wygrany][n])

        print(epoka + 1, ": ", liczbaTrafionych, " / ", len(wejscie), " ( ", liczbaTrafionych / len(wejscie) * 100, "% )")
        celnosc.append(liczbaTrafionych / len(wejscie) * 100)

    # wyswietlanie wyników
    plt.plot(celnosc)
    plt.ylabel("Procent poprawnie zaklasyfikowanych")
    plt.xlabel("Numer epoki")
    plt.show()

    # sprawdzanie z danymi kontrolnymi
    liczbaTrafionych = 0
    for wiersz in range(0, len(wejscieKontrolne)):
        dystanse = [0 for n in range(len(indeksyNaCechy))]
        for kolumna in range(0, len(wejscieKontrolne[wiersz])):
            for n in range(0, len(wagi)):
                dystanse[n] += math.pow(wejscieKontrolne[wiersz][kolumna] - wagi[n][kolumna], 2)
        wygrany = 0
        for n in range(1, len(dystanse)):
            if dystanse[n] < dystanse[wygrany]:
                wygrany = n
        if indeksyNaCechy[wygrany] == wyjscieKontrolne[wiersz]:
            liczbaTrafionych += 1
    print("Trafność na danych kontrolnych: ", liczbaTrafionych, " / ", len(wejscieKontrolne), " ( ", liczbaTrafionych / len(wejscieKontrolne) * 100, "% )")
    return celnosc