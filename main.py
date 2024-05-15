import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.collections import PolyCollection
import math
import string
from LVQ import runLVQ
from RBF import runRBF

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
temp = naTreningoweIKontrolne(inputRed, outputRed, 0.05)
inputRedT, outputRedT, inputRedK, outputRedK = temp[0], temp[1], temp[2], temp[3]
temp = naTreningoweIKontrolne(inputWhite, outputWhite, 0.05)
inputWhiteT, outputWhiteT, inputWhiteK, outputWhiteK = temp[0], temp[1], temp[2], temp[3]
temp = naTreningoweIKontrolne(inputBoth, outputColors, 0.1)
inputBothT, outputColorsT, inputBothK, outputColorsK = temp[0], temp[1], temp[2], temp[3]

temp = {}
for n in outputWhite:
    temp[n] = 0
#for n in outputRed:
#    temp[n] = 0
for n in outputWhite:
    temp[n] += 1
#for n in outputRed:
    #temp[n] += 1
print("częstości: ", temp)

# Radialna, LVQ, PNN, DTF
wyniki = []
#alfy = [0.00025, 0.001,  0.0025, 0.005, 0.01]
alfy = [0.00005, 0.0001, 0.0005,  0.001]
bety = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
ilosciNeuronow = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
iloscEpok = 2000


# badanie alfy
for alfa in alfy:
    #wyniki.append(runLVQ(inputRedT.copy(), outputRedT.copy(), iloscEpok, alfa, inputRedK.copy(), outputRedK.copy()))
    #wyniki.append(runLVQ(inputWhiteT.copy(), outputWhiteT.copy(), iloscEpok, alfa, inputWhiteK.copy(), outputWhiteK.copy()))
    wyniki.append(runRBF(inputRedT.copy(), outputRedT.copy(), iloscEpok, 5, alfa, 5, inputRedK.copy(), outputRedK.copy()))



#runLVQ(inputRedT.copy(), outputRedT.copy(), 100, 0.025, inputRedK.copy(), outputRedK.copy())
#runLVQ(inputWhiteT.copy(), outputWhiteT.copy(), 200, 0.001, inputWhiteK.copy(), outputWhiteK.copy())
#runLVQ(inputBothT.copy(), outputColorsT.copy(), 100, 0.001, inputBothK.copy(), outputColorsK.copy())

#runRBF(inputRedT.copy(), outputRedT.copy(), 500, 20, 0.0002, 10, inputRedK.copy(), outputRedK.copy())
#runRBF(inputWhiteT.copy(), outputWhiteT.copy(), 1000, 3, 0.001, 0.5, inputWhiteK.copy(), outputWhiteK.copy())
#runRBF(inputBothT.copy(), outputColorsT.copy(), 300, 10, 0.0005, 100, inputBothK.copy(), outputColorsK.copy())
from PNN import runPNN
#runPNN(inputRedT.copy(), outputRedT.copy(), 0.5, inputRedK.copy(), outputRedK.copy())
#runPNN(inputWhiteT.copy(), outputWhiteT.copy(), 0.5, inputWhiteK.copy(), outputWhiteK.copy())
#runPNN(inputBothT.copy(), outputColorsT.copy(), 0.5, inputBothK.copy(), outputColorsK.copy())
from DTF import runDTF
# więcej max gałęzi przy większej ilości cech?
# przy tych danych więcej gałęzi != większa szansa na trafienie
# 3 prawdopodobnie optymalne dla 4 i możliwe że w ogóle
# więcej cech nie oznacza większej celności,
# warto sprawdzić które kombinacje dają największą celność i wrzucić je jako jedyne
#drzewa = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10]]
drzewa = [[6, 7], [7, 8], [6, 7, 8], [6, 8]]
#drzewa = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
#drzewa = [[10]]
#runDTF(inputRedT.copy(), outputRedT.copy(), drzewa, 3, inputRedK.copy(), outputRedK.copy())
#runDTF(inputWhiteT.copy(), outputWhiteT.copy(), drzewa, 3, inputWhiteK.copy(), outputWhiteK.copy())
#runDTF(inputBothT.copy(), outputColorsT.copy(), drzewa, 3, inputBothK.copy(), outputColorsK.copy())


def polygon_under_graph(x, y):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (x, y) line graph. This assumes x is in ascending order.
    """
    temp2 = np.array([wyniki[y][m] for m in range(len(wyniki[y]))])
    return [(x[0], 0.), *zip(x, temp2), (x[-1], 0.)]
    # return [np.float_power(2.71828, -y * np.float_power(x, 2)), 0, 0]


ax = plt.figure().add_subplot(projection='3d')
x = np.linspace(1, iloscEpok + 1, iloscEpok)
# wybór analizy
lambdas = range(len(alfy))

# verts[i] is a list of (x, y) pairs defining polygon i.
gamma = np.vectorize(math.gamma)
verts = [polygon_under_graph(x, l)
         for l in lambdas]
facecolors = plt.colormaps['jet'](np.linspace(0, 1, len(verts)))

poly = PolyCollection(verts, facecolors=facecolors, alpha=.95)
stringizowany = []
# wybór zbioru do y
ax.add_collection3d(poly, zs=alfy, zdir='y')
ax.view_init(15, -75, 0)
# wybór wykresu
ax.set(xlim=(x[0], x[-1]), ylim=(alfy[0], alfy[-1]), zlim=(0, 1), xlabel='Epoka', ylabel='Wartość alfa', zlabel='Zgodność z danymi treningowymi')

plt.show()