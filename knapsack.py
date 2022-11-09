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

    # for testing. prints variables
    def printParams(self):
        print("weights", self.weights)
        print("profit", self.profits)
        print("populationSize", self.populationSize)
        print("maxWeight", self.maxWeight)
        print("numIterations", self.numIterations)
        print("population", self.population)

    # calculate the total profit of a sample
    def computeProfit(self, sample):
        totalProfit = 0
        for i in range(len(self.profits)):
            if sample[i] != 0:
                totalProfit += self.profits[i]

        return totalProfit

    # calculate the total weight of a sample
    def computeWeight(self, sample):
        totalWeight = 0
        for i in range(len(self.weights)):
            if sample[i] != 0:
                totalWeight += self.weights[i]

        return totalWeight

    # create an inital population randomly
    def createPopulationRandomly(self):
        self.population = []
        for i in range(self.populationSize):
            sample = []
            for j in range(len(self.weights)):
                sample.append(random.randint(0, 1))
            self.population.append(sample)

    # change population 0.2%
    def mutation(self):
        for i in range(self.populationSize):
            for j in range(len(self.weights)):
                k = random.randint(0, 500)  # 0.2%
                if k == 1:
                    if self.population[i][j] == 1:
                        self.population[i][j] = 0
                    else:
                        self.population[i][j] = 1

    # check if samples are ok
    def fitness(self):
        for i in range(self.populationSize):
            sample = self.population[i]
            totalWeight = self.computeWeight(sample)
            while totalWeight > self.maxWeight:  # remove an item randomly until it fits
                k = random.randint(0, len(self.weights)-1)
                while sample[k] != 1:
                    k = random.randint(0, len(self.weights)-1)
                sample[k] = 0
                totalWeight = self.computeWeight(sample)
            self.population[i] = sample

    # Select half of the population
    def selection(self):
        newPopulation = []
        self.sortPopulation()

        # Elitism Selection. 2 selected
        self.populationAfterSelection = self.population.copy()
        best = self.populationAfterSelection[0]
        del self.populationAfterSelection[0]
        secondBest = self.populationAfterSelection[0]
        del self.populationAfterSelection[0]

        newPopulation.append(best)
        newPopulation.append(secondBest)

        # Roulette Wheel Selection
        samplesToSelect = int((len(self.population) / 2) - 2)  # half minus 2

        totalProfit = 0
        popProfits = []
        for i in range(len(self.populationAfterSelection)):
            profit = self.computeProfit(self.populationAfterSelection[i])
            totalProfit += profit
            popProfits.append(profit)

        # pick 1 sample randomly based on its profit
        for i in range(samplesToSelect):
            randomProfit = random.randint(1, totalProfit)
            j = -1
            while randomProfit > 0:
                randomProfit -= popProfits[j]
                j += 1
            newPopulation.append(self.populationAfterSelection[j])

        self.populationAfterSelection = newPopulation

    def crossover(self):
        newPopulation = []

    def sortPopulation(self):
        self.population.sort(key=self.compare, reverse=True)

    def compare(self, sample):
        return self.computeProfit(sample)

    #
    def _testing(self):
        print(self.computeProfit(self.population[0]))
        print(self.computeWeight(self.population[0]))


weights = [2, 3, 1, 4]
profits = [1, 4, 2, 6]
numIterations = 4
populationSize = 14
maxWeight = 10

instance = Knapsack()
instance.setParams(weights, profits, populationSize, maxWeight, numIterations)
# instance.start()

instance.createPopulationRandomly()
instance.printParams()

instance.selection()

instance.printParams()
