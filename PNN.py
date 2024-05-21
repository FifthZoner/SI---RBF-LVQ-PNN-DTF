import random
import math
import matplotlib.pyplot as plt

# obliczanie aktywacji dla danego neuronu z prototypem
def aktywacjaPNN(neuron, dane):
    neuron.wartosc = 0
    for n in range(0, len(neuron.prototyp)):
        neuron.wartosc += math.pow(2.71828, -neuron.beta * math.pow(neuron.prototyp[n] - dane[n], 2))

class neuron2:
    beta = 0
    prototyp = []
    wartosc = 0
    cecha = 0

# przekazywać 0 : 1, numery w klasach
# funkcja ogólna
def runPNN(wejscie, wyniki, beta, wejscieKontrolne, wyjscieKontrolne):

    # szukanie cech występujących w danych
    opcje = {}
    for n in wyniki:
        opcje[n] = []
    # for n in range(0, len(wyniki)):
    #    opcje[wyniki[n]].append(n)
    cechy = []
    m = 0
    for n in opcje:
        cechy.append(n)
        opcje[n] = m
        m += 1

    # przygotowywanie neuronów 2. warstwy
    neurony2 = [neuron2() for n in range(len(wejscie))]
    for n in range(0, len(wejscie)):
        neurony2[n].beta = beta
        neurony2[n].prototyp = wejscie[n]
        neurony2[n].cecha = opcje[wyniki[n]]

    # przeprowadzenie obliczeń
    liczbaTrafionych = 0

    for wiersz in range(len(wejscieKontrolne)):

        # obliczenie wartości aktywacji dla każdego neuronu dla podanej wartości
        for neuron in neurony2:
            aktywacjaPNN(neuron, wejscieKontrolne[wiersz])

        # wyliczanie średnich       TODO: suma czy średnia? raczej średnia
        sumy = [0 for n in range(len(cechy))]
        ilosci = [0 for n in range(len(cechy))]
        srednie = [0 for n in range(len(cechy))]
        for neuron in neurony2:
            sumy[neuron.cecha] += neuron.wartosc
            ilosci[neuron.cecha] += 1
        for n in range(len(srednie)):
            srednie[n] = sumy[n] / ilosci[n]
        # szukanie największej
        max = 0
        for n in range(1, len(srednie)):
            if srednie[n] > srednie[max]:
                max = n
        if cechy[max] == wyjscieKontrolne[wiersz]:
            liczbaTrafionych += 1





    print("Trafność na danych kontrolnych: ", liczbaTrafionych, " / ", len(wejscieKontrolne), " ( ", liczbaTrafionych / len(wejscieKontrolne) * 100, "% )")
    return liczbaTrafionych / len(wejscieKontrolne)