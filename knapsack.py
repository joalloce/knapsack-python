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

    #
    def printParams(self):
        print(self.weights)
        print(self.profits)
        print(self.populationSize)
        print(self.maxWeight)
        print(self.numIterations)
        print(self.population)

    def computeProfit(self, sample):
        totalProfit = 0
        for i in range(len(self.profits)):
            if sample[i] != 0:
                totalProfit += self.profits[i]

        return totalProfit

    def computeWeight(self, sample):
        totalWeight = 0
        for i in range(len(self.weights)):
            if sample[i] != 0:
                totalWeight += self.weights[i]

        return totalWeight

    def createPopulationRandomly(self):
        self.population = []
        for i in range(self.populationSize):
            sample = []
            for j in range(len(self.weights)):
                sample.append(random.randint(0, 1))
            self.population.append(sample)

    def mutation(self):
        for i in range(self.populationSize):
            for j in range(len(self.weights)):
                k = random.randint(0, 500)  # 0.2%
                if k == 1:
                    if self.population[i][j] == 1:
                        self.population[i][j] = 0
                    else:
                        self.population[i][j] = 1

    #
    def _testing(self):
        print(self.computeProfit(self.population[0]))
        print(self.computeWeight(self.population[0]))


weights = [2, 3, 1, 4]
profits = [1, 4, 2, 6]
numIterations = 4
populationSize = 6
maxWeight = 15

instance = Knapsack()
instance.setParams(weights, profits, populationSize, maxWeight, numIterations)
# instance.start()
instance.printParams()

instance.createPopulationRandomly()

instance.printParams()
instance._testing()

instance.mutation()
instance.printParams()
