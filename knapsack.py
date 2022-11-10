import random


class Knapsack():
    def __init__(self) -> None:
        self.weights = []
        self.profits = []
        self.populationSize = 0
        self.maxWeight = 1
        self.population = []
        self.populationAfterSelection = []
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
        print("populationAF", self.populationAfterSelection)
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

    # change population 1%
    def mutation(self):
        for i in range(self.populationSize):
            for j in range(len(self.weights)):
                k = random.randint(0, 100)  # 1%
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
        for i in range(self.populationSize):
            crossoverProb = random.randint(1, 100)
            if (crossoverProb < 85):
                threshold = random.randint(1, len(self.weights)-1)
                sample1 = self.populationAfterSelection[random.randint(
                    0, len(self.populationAfterSelection)-1)]
                sample2 = []
                if random.randint(0, 1) == 1:
                    randomPos = random.randint(0, self.populationSize-1)
                    sample2 = self.population[randomPos]
                else:
                    randomPos = random.randint(
                        0, len(self.populationAfterSelection)-1)
                    sample2 = self.populationAfterSelection[randomPos]
                newSample = []
                for j in range(0, threshold):
                    newSample.append(sample1[j])

                for j in range(threshold, len(self.weights)):
                    newSample.append(sample2[j])

                newPopulation.append(newSample)
            else:
                if random.randint(0, 1) == 1:
                    randomPos = random.randint(0, self.populationSize-1)
                    newPopulation.append(self.population[randomPos])
                else:
                    randomPos = random.randint(
                        0, len(self.populationAfterSelection)-1)
                    newPopulation.append(
                        self.populationAfterSelection[randomPos])
        self.population = newPopulation

    # check if 90% of the pop have the same profit
    def hasSameFitness(self):
        sameFitness = False
        profitList = {}  # store the profit values
        for i in range(self.populationSize):
            profit = self.computeProfit(self.population[i])
            if (profit not in profitList):
                profitList[profit] = 1
            else:
                profitList[profit] = profitList[profit] + 1

        for value in profitList.values():
            if (value > self.populationSize * 0.9):
                sameFitness = True

        return sameFitness

    def start(self):
        i = 0
        working = True
        while working:
            self.fitness()
            sameFitness = True
            if (not self.hasSameFitness()):
                self.selection()
                self.crossover()
                self.mutation()
                sameFitness = False

            i += 1
            # continue if 90% don't have the same fitness
            working = i < self.numIterations and not sameFitness

        if not sameFitness:
            self.fitness()

    # return the highest profit sample
    def getBestSample(self):
        self.sortPopulation()
        return self.population[0]

    def sortPopulation(self):
        self.population.sort(key=self.compare, reverse=True)

    def compare(self, sample):
        return self.computeProfit(sample)


numIterations = 800
populationSize = 60

# Example taken from https://developers.google.com/optimization/bin/knapsack
maxWeight = 850
profits = [
    360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
    78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
    87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
    312
]
weights = [
    7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
]

instance = Knapsack()
instance.setParams(weights, profits, populationSize, maxWeight, numIterations)

instance.createPopulationRandomly()
instance.start()

bestSample = instance.getBestSample()
print("Best Sample", bestSample)
print("Best Sample profit", instance.computeProfit(bestSample))
print("Best Sample weight", instance.computeWeight(bestSample))

print("weights", instance.weights)
print("profit", instance.profits)
print("maxWeight", instance.maxWeight)
print("Optimal answer", 7534)
