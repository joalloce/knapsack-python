import random


class Knapsack():
    def __init__(self) -> None:
        self.weights = []
        self.profits = []
        self.populationSize = 0
        self.maxWeight = 1
        self.population = []
        self.populationAfterSelection = []
        self.numIterationsDone = -1
        self.numIterations = 0

    def setParams(self, weights, profits, populationSize, maxWeight, numIterations):
        self.weights = weights
        self.profits = profits
        self.populationSize = populationSize
        self.maxWeight = maxWeight
        self.numIterations = numIterations

    def printParams(self):
        print(self.weights)
        print(self.profits)
        print(self.populationSize)
        print(self.maxWeight)
        print(self.numIterations)

    def computeProfit(self, sample):
        totalProfit = 0
        for i in len(self.profits):
            if sample[i] != 0:
                totalProfit += self.profits[i]

        return totalProfit

    def computeWeight(self, sample):
        totalWeight = 0
        for i in len(self.weights):
            if sample[i] != 0:
                totalWeight += self.weights[i]

        return totalWeight


weights = [2, 3, 1, 4]
profits = [1, 4, 2, 6]
numIterations = 20
populationSize = 20
maxWeight = 15

instance = Knapsack()
instance.setParams(weights, profits, populationSize, maxWeight, numIterations)
instance.printParams()
