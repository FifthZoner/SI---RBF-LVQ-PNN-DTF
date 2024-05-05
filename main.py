import pandas as pd
import matplotlib.pyplot as plt

dataRed = pd.read_csv("data/winequality-red.csv")
dataWhite = pd.read_csv("data/winequality-white.csv")

#print(dataRed.values)

inputRed = []
inputWhite = []
outputRed = []
outputWhite = []

# wczytywanie do tablic
for n in dataRed.values:
    temp = n[0].split(';')
    inputRed.append([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9]), float(temp[10])])
    outputRed.append(int(temp[11]))

for n in dataWhite.values:
    temp = n[0].split(';')
    inputWhite.append([float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9]), float(temp[10])])
    outputWhite.append(int(temp[11]))

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
plt.plot(outputWhite, 'o', markersize=3)
plt.ylabel("Wartości znormalizowane dla białego")
#plt.legend(inputLabels)
plt.show()

# Radialna, LVQ, PNN, DTF
from LVQ import runLVQ
#runLVQ(inputRed.copy(), outputRed.copy())
from RBF import runRBF
#runRBF(inputRed.copy(), outputRed.copy(), 1000, 20)
from PNN import runPNN
runPNN(inputRed.copy(), outputRed.copy(), 0.005)