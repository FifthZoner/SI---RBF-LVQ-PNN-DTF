import random
import math
import matplotlib.pyplot as plt
import numpy as np

# obliczanie aktywacji dla danego neuronu z prototypem
def aktywacjaRBF(prototyp, dane, beta):
    suma = 0
    for n in range(0, len(prototyp)):
        suma += math.pow(2.71828, -beta * math.pow(prototyp[n] - dane[n], 2))
    return suma

# przekazywać 0 : 1, numery w klasach
# funkcja ogólna
def runRBF(wejscie, wyniki, liczbaEpok, neuronyNaKlase, alfa, beta, wejscieKontrolne, wyjscieKontrolne):
    # wykres funkcji aktywacji
    wykresFunkcjiAktywacji = []
    for n in range(1000):
        wykresFunkcjiAktywacji.append(aktywacjaRBF([n / 1000], [0], 100))
    plt.plot(wykresFunkcjiAktywacji)
    plt.xlabel("Odległość od celu")
    plt.ylabel("Wartość funkcji aktywacji")
    plt.show()

    wykresFunkcjiAktywacji3D = [[], [] ,[], [[] for n in range(100)], [[] for n in range(100)], [[] for n in range(100)]]
    for b in range(100):
        for n in range(100):
            wykresFunkcjiAktywacji3D[0].append(n / 100)
            wykresFunkcjiAktywacji3D[1].append(b)
            wykresFunkcjiAktywacji3D[2].append(aktywacjaRBF([n / 100], [0], b))
            wykresFunkcjiAktywacji3D[3][b].append(n / 100)
            wykresFunkcjiAktywacji3D[4][b].append(b)
            wykresFunkcjiAktywacji3D[5][b].append(aktywacjaRBF([n / 100], [0], b))

    x = np.array(wykresFunkcjiAktywacji3D[0])
    y = np.array(wykresFunkcjiAktywacji3D[1])
    z = np.array(wykresFunkcjiAktywacji3D[2])
    x2 = np.array(wykresFunkcjiAktywacji3D[3])
    y2 = np.array(wykresFunkcjiAktywacji3D[4])
    z2 = np.array(wykresFunkcjiAktywacji3D[5])
    # Tworzenie wykresu 3D
    fig = plt.figure()

    # syntax for 3-D projection
    ax = plt.axes(projection='3d')
    ax.view_init(15,60, 0)

    # defining axes
    c = z
    ax.scatter(x, y, z, c=c)

    #X, Y = np.meshgrid(x, y)
    #Z = X * np.exp(X)
    #ax.plot_surface(x2, z2, z2, cmap="plasma")
    # syntax for plotting
    #ax.set_title('3d Scatter plot geeks for geeks')
    plt.show()
    # inne zmienne kontrolne
    celnosc = []

    # dzielenie danych wg klas do stworzenia neuronów
    opcje = {}
    for n in wyniki:
        opcje[n] = []
    for n in range(0, len(wyniki)):
        opcje[wyniki[n]].append(n)

    # tworzenie podanej ilości neuronów na klasę, jeżeli jest to możliwe i usuwanie z listy
    wagi = []
    bety = []
    n = 0
    for opcja in opcje:
        ile = neuronyNaKlase
        wagi.append([])
        bety.append([])
        while ile > 0 and len(opcje[opcja]) > 0:
            ktory = random.randint(0, len(opcje[opcja]) - 1)
            wagi[n].append(wejscie[ktory])
            bety[n].append(beta)
            wejscie.pop(ktory)
            wyniki.pop(ktory)
            ile -= 1
        n += 1

    opcjeTab = []
    for n in opcje:
        opcjeTab.append(n)

    # trenowanie
    for epoka in range (0, liczbaEpok):

        # zmienne statystyczne
        liczbaTrafionych = 0

        for wiersz in range(0, len(wejscie)):

            # sprawdzanie aktywacji dla każdego neuronu
            aktywacje = [[] for n in range(len(wagi))]
            for cecha in range(0, len(wagi)):
                for waga in range (0, len(wagi[cecha])):
                    aktywacje[cecha].append(aktywacjaRBF(wagi[cecha][waga], wejscie[wiersz], bety[cecha][waga]))

            # TODO: gradient prosty? (gradient descent)

            # sprawdzanie i zapisywanie która jest największa
            ktory = [0, 0]
            for cecha in range(0, len(aktywacje)):
                for waga in range(0, len(aktywacje[cecha])):
                    if aktywacje[cecha][waga] > aktywacje[ktory[0]][ktory[1]]:
                        ktory = [cecha, waga]
            #print(ktory)

            # modyfikacja modelu
            if wyniki[wiersz] == opcjeTab[ktory[0]]:
                liczbaTrafionych += 1
                for n in range(0, len(wejscie[wiersz])):
                    wagi[ktory[0]][ktory[1]][n] += alfa * (wejscie[wiersz][n] - wagi[ktory[0]][ktory[1]][n])
            else:
                for n in range(0, len(wejscie[wiersz])):
                    wagi[ktory[0]][ktory[1]][n] -= alfa * (wejscie[wiersz][n] - wagi[ktory[0]][ktory[1]][n])

        print(epoka + 1, ": ", liczbaTrafionych, " / ", len(wejscie), " ( ", liczbaTrafionych / len(wejscie) * 100, "% )")
        celnosc.append(liczbaTrafionych / len(wejscie) * 100)

    # wyswietlanie wyników
    plt.plot(celnosc)
    plt.ylabel("Procent poprawnie zaklasyfikowanych")
    plt.xlabel("Numer epoki")
    plt.show()

    liczbaTrafionych = 0
    for wiersz in range(0, len(wejscieKontrolne)):
        aktywacje = [[] for n in range(len(wagi))]
        for cecha in range(0, len(wagi)):
            for waga in range(0, len(wagi[cecha])):
                aktywacje[cecha].append(aktywacjaRBF(wagi[cecha][waga], wejscieKontrolne[wiersz], bety[cecha][waga]))

        # TODO: gradient prosty? (gradient descent)

        # sprawdzanie i zapisywanie która jest największa
        ktory = [0, 0]
        for cecha in range(0, len(aktywacje)):
            for waga in range(0, len(aktywacje[cecha])):
                if aktywacje[cecha][waga] > aktywacje[ktory[0]][ktory[1]]:
                    ktory = [cecha, waga]

        # modyfikacja modelu
        if wyjscieKontrolne[wiersz] == opcjeTab[ktory[0]]:
            liczbaTrafionych += 1
    print("Trafność na danych kontrolnych: ", liczbaTrafionych, " / ", len(wejscieKontrolne), " ( ", liczbaTrafionych / len(wejscieKontrolne) * 100, "% )")
    return celnosc