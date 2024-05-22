import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.collections import PolyCollection
import math
import string
from LVQ import runLVQ
from RBF import runRBF
from PNN import runPNN
from DTF import runDTF

random.seed(a=None, version=2)

# zwraca [inputT, outputT, inputK, outputK]
def naTreningoweIKontrolne(input, output, wspKontrolnych):
    kontrolneIn = []
    kontrolneOut = []
    ile = int(len(input) * wspKontrolnych)
    for n in range(ile):
        ktory = random.randint(0, len(input) - 1)
        kontrolneIn.append(input.pop(ktory))
        kontrolneOut.append(output.pop(ktory))
    return [input, output, kontrolneIn, kontrolneOut]

dataRed = pd.read_csv("data/winequality-red.csv")
dataWhite = pd.read_csv("data/winequality-white.csv")

#print(dataRed.values)

inputRed = []
inputWhite = []
outputRed = []
outputWhite = []
outputColors = []

# wczytywanie do tablic
for n in dataRed.values:
    temp = n[0].split(';')
    inputRed.append([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9]), float(temp[10])])
    outputRed.append(int(temp[11]))
    outputColors.append(0)

for n in dataWhite.values:
    temp = n[0].split(';')
    inputWhite.append([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9]), float(temp[10])])
    outputWhite.append(int(temp[11]))
    outputColors.append(1)

# 0 - czerwony, 1 - biały
inputBoth = inputRed.copy() + inputWhite.copy()
outputBoth = outputRed.copy() + outputWhite.copy()

# normalizacja -1 : 1
for column in range(0, 11):
    max = -99999999
    min = 99999999
    for n in range(0, len(inputRed)):
        if max < inputRed[n][column]:
            max = inputRed[n][column]
        if min > inputRed[n][column]:
            min = inputRed[n][column]
    for n in range(0, len(inputRed)):
        inputRed[n][column] = (inputRed[n][column] - min) / (max - min)

for column in range(0, 11):
    max = -99999999
    min = 99999999
    for n in range(0, len(inputWhite)):
        if max < inputWhite[n][column]:
            max = inputWhite[n][column]
        if min > inputWhite[n][column]:
            min = inputWhite[n][column]
    for n in range(0, len(inputWhite)):
        inputWhite[n][column] = (inputWhite[n][column] - min) / (max - min)

inputLabels = ["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH"]

plt.plot(inputRed, 'o', markersize=1)
plt.ylabel("Wartości znormalizowane dla czerwonego")
#plt.legend(inputLabels)
plt.show()

plt.plot(inputWhite, 'o', markersize=1)
#plt.plot(outputWhite, 'o', markersize=3)
plt.ylabel("Wartości znormalizowane dla białego")
#plt.legend(inputLabels)
plt.show()

# rozdzielanie na treningowe i kontrolne
temp = naTreningoweIKontrolne(inputRed, outputRed, 0.1)
inputRedT, outputRedT, inputRedK, outputRedK = temp[0], temp[1], temp[2], temp[3]
temp = naTreningoweIKontrolne(inputWhite, outputWhite, 0.1)
inputWhiteT, outputWhiteT, inputWhiteK, outputWhiteK = temp[0], temp[1], temp[2], temp[3]
temp = naTreningoweIKontrolne(inputBoth, outputBoth, 0.1)
inputBothT, outputBothT, inputBothK, outputBothK = temp[0], temp[1], temp[2], temp[3]
temp = naTreningoweIKontrolne(inputBoth, outputColors, 0.2)
inputColorsT, outputColorsT, inputColorsK, outputColorsK = temp[0], temp[1], temp[2], temp[3]

#temp = {}
#for n in outputWhite:
    #temp[n] = 0
#for n in outputRed:
#    temp[n] = 0
#for n in outputWhite:
    #temp[n] += 1
#for n in outputRed:
    #temp[n] += 1
#print("częstości: ", temp)

# RBF, LVQ, PNN, DTF
wyniki = []
kolumny = []
kolumnyDrzew = []
#alfy = [0.00025, 0.001,  0.0025, 0.005, 0.01]
alfy = [0.0000001, 0.000001, 0.00001, 0.0001,  0.001]
bety = [0.001, 0.1, 10, 1000, 100000, 10000000, 1000000000]
ilosciNeuronow = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#iloscigalezi = [1, 2, 3, 4, 5, 6]
iloscigalezi = [1, 2, 3, 4, 5]
#iloscigalezi = [3]
iloscEpok = 750


# badanie alfy
#for alfa in alfy:
    #wyniki.append(runLVQ(inputRedT.copy(), outputRedT.copy(), iloscEpok, alfa, inputRedK.copy(), outputRedK.copy()))
    #wyniki.append(runLVQ(inputWhiteT.copy(), outputWhiteT.copy(), iloscEpok, alfa, inputWhiteK.copy(), outputWhiteK.copy()))
    #wyniki.append(runLVQ(inputColorsT.copy(), outputColorsT.copy(), iloscEpok, alfa, inputColorsK.copy(), outputColorsK.copy()))
    #wyniki.append(runRBF(inputRedT.copy(), outputRedT.copy(), iloscEpok, 5, alfa, 5, inputRedK.copy(), outputRedK.copy()))
    #wyniki.append(runRBF(inputColorsT.copy(), outputColorsT.copy(), iloscEpok, 5, alfa, 5, inputColorsK.copy(), outputColorsK.copy()))

# badanie bety
for beta in bety:
    #kolumny.append(runPNN(inputRedT.copy(), outputRedT.copy(), beta, inputRedK.copy(), outputRedK.copy()))
    #kolumny.append(runPNN(inputWhiteT.copy(), outputWhiteT.copy(), beta, inputWhiteK.copy(), outputWhiteK.copy()))
    #kolumny.append(runPNN(inputBothT.copy(), outputBothT.copy(), beta, inputBothK.copy(), outputBothK.copy()))
    wyniki.append(runRBF(inputColorsT.copy(), outputColorsT.copy(), iloscEpok, 3, 0.00005, beta, inputColorsK.copy(), outputColorsK.copy()))

#for ilosc in ilosciNeuronow:
#    wyniki.append(runRBF(inputColorsT.copy(), outputColorsT.copy(), iloscEpok, ilosc, 0.0005, 10, inputColorsK.copy(), outputColorsK.copy()))

#runLVQ(inputRedT.copy(), outputRedT.copy(), 500, 0.0001, inputRedK.copy(), outputRedK.copy())
#runLVQ(inputWhiteT.copy(), outputWhiteT.copy(), 500, 0.001, inputWhiteK.copy(), outputWhiteK.copy())
#runLVQ(inputBothT.copy(), outputBothT.copy(), 300, 0.001, inputBothK.copy(), outputBothK.copy())
#runLVQ(inputColorsT.copy(), outputColorsT.copy(), 100, 0.005, inputColorsK.copy(), outputColorsK.copy())

#runRBF(inputRedT.copy(), outputRedT.copy(), 500, 20, 0.0002, 10, inputRedK.copy(), outputRedK.copy())
#runRBF(inputWhiteT.copy(), outputWhiteT.copy(), 200, 6, 0.0025, 10, inputWhiteK.copy(), outputWhiteK.copy())
#runRBF(inputBothT.copy(), outputBothT.copy(), 100, 4, 0.0002, 10, inputBothK.copy(), outputBothK.copy())
#runRBF(inputColorsT.copy(), outputColorsT.copy(), 1000, 20, 0.005, 0.1, inputColorsK.copy(), outputColorsK.copy())

#runPNN(inputRedT.copy(), outputRedT.copy(), 0.5, inputRedK.copy(), outputRedK.copy())
#runPNN(inputWhiteT.copy(), outputWhiteT.copy(), 0.5, inputWhiteK.copy(), outputWhiteK.copy())
#runPNN(inputColorsT.copy(), outputColorsT.copy(), 0.5, inputColorsK.copy(), outputColorsK.copy())
# więcej max gałęzi przy większej ilości cech?
# przy tych danych więcej gałęzi != większa szansa na trafienie
# 3 prawdopodobnie optymalne dla 4 i możliwe że w ogóle
# więcej parametrów nie oznacza większej celności,
# warto sprawdzić które kombinacje dają największą celność i wrzucić je jako jedyne
#drzewa = []
#for x1 in range(0, 11):
#    for x2 in range(x1 + 1, 11):
#        drzewa.append([x1, x2])
#for x1 in range(0, 11):
#    for x2 in range(x1 + 1, 11):
#        for x3 in range(x2 + 1, 11):
#            drzewa.append([x1, x2, x3])
#print(drzewa)
#drzewa = [[0, 1], [0, 2], [0, 3], [0, 4], [0,5], [0,6], [0,7], [0,8], [0,9], [0, 10]]
#drzewa = [[4, 5], [6, 7], [9, 10]]
#drzewa = [[6, 7], [7, 8], [6, 7, 8], [6, 8]]
#drzewa = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
#drzewa = [[0, 2, 7, 8, 9, 10]]
#drzewa = [[10]]
#for ilosc in iloscigalezi:
    #kolumnyDrzew.append(runDTF(inputRedT.copy(), outputRedT.copy(), drzewa, ilosc, inputRedK.copy(), outputRedK.copy()))
    #kolumnyDrzew.append(runDTF(inputWhiteT.copy(), outputWhiteT.copy(), drzewa, ilosc, inputWhiteK.copy(), outputWhiteK.copy()))
    #kolumnyDrzew.append(runDTF(inputBothT.copy(), outputBothT.copy(), drzewa, ilosc, inputBothK.copy(), outputBothK.copy()))
    #kolumnyDrzew.append(runDTF(inputColorsT.copy(), outputColorsT.copy(), drzewa, ilosc, inputColorsK.copy(), outputColorsK.copy()))
#runDTF(inputRedT.copy(), outputRedT.copy(), drzewa, 6, inputRedK.copy(), outputRedK.copy())
#runDTF(inputWhiteT.copy(), outputWhiteT.copy(), drzewa, 3, inputWhiteK.copy(), outputWhiteK.copy())
#runDTF(inputBothT.copy(), outputColorsT.copy(), drzewa, 3, inputBothK.copy(), outputColorsK.copy())
if len(kolumny) != 0:
    fig = plt.figure(figsize=(10, 5))

    # Create evenly spaced x-axis values
    x_pos = np.arange(len(bety))

    # Create the bar plot with evenly spaced x-axis
    plt.bar(x_pos, kolumny, color='maroon', width=0.4)
    labels = []
    for n in bety:
        labels.append("{:.{}e}".format(n, 0))
    # Set the x-axis tick labels
    plt.xticks(x_pos, labels)

    plt.xlabel("wsp. beta")
    plt.ylabel("Celność")
    plt.show()

if len(kolumnyDrzew) != 0:
    fig = plt.figure(figsize=(10, 5))    # Create evenly spaced x-axis values
    x_pos = np.arange(len(iloscigalezi))    # Create the bar plot with evenly spaced x-axis
    plt.bar(x_pos, kolumnyDrzew, color='purple', width=0.4)
    labels = []
    for n in iloscigalezi:
        labels.append(str(n))
    # Set the x-axis tick labels
    plt.xticks(x_pos, labels)
    plt.xlabel("maksymalna wysokość drzewa")
    plt.ylabel("Celność")
    plt.show()

if len(wyniki) != 0:
    def polygon_under_graph(x, y):
        temp2 = np.array([wyniki[y][m] for m in range(len(wyniki[y]))])
        return [(x[0], 0.), *zip(x, temp2), (x[-1], 0.)]


    ax = plt.figure().add_subplot(projection='3d')
    x = np.linspace(1, iloscEpok, iloscEpok)

    # verts[i] is a list of (x, y) pairs defining polygon i.
    gamma = np.vectorize(math.gamma)
    verts = [polygon_under_graph(x, l) for l in range(len(bety))]
    facecolors = plt.colormaps['jet'](np.linspace(0, 1, len(verts)))

    # Create evenly spaced y-values
    y_values = np.linspace(bety[0], bety[-1], len(bety))

    poly = PolyCollection(verts, facecolors=facecolors, alpha=.7)
    ax.add_collection3d(poly, zs=y_values, zdir='y')
    ax.view_init(15, -75, 0)

    ax.set(xlim=(x[0], x[-1]), ylim=(bety[0], bety[-1]), zlim=(0, 1), xlabel='Epoka', zlabel='Wsp. trafień',
           #ylabel='Wsp. uczenia')
           ylabel='Wsp. beta')

    # Remove y-axis tick labels
    ax.set_yticks([])

    # Add text labels for the y-axis on the left
    for i, y in enumerate(y_values):
        # ax.text(6.1, y, -0.1, "{:.{}e}".format(alfy[i], 2), va='center', ha='right')
        # czerwony
        # ax.text(1.29 * iloscEpok, y, -0.1, "{:.{}e}".format(alfy[i], 0), va='center', ha='right')
        # biały
        ax.text(1.21 * iloscEpok, y, -0.1, "{:.{}e}".format(bety[i], 0), va='center', ha='right')

    plt.show()
