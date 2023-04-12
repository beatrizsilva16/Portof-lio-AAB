from random import randint, random, shuffle


class Indiv:
    """
    # The Indiv class represents an individual in a genetic algorithm.
    It contains methods for initialization, mutation, crossover, and fitness evaluation.
    """
    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb  # lower limit of gene
        self.ub = ub  # upper limit of gene
        self.genes = genes  # genome
        self.fitness = None   # fitness value
        if not self.genes:  # if there is no list of genes
            self.initRandom(size)  # create random individual

    # comparadores.
    # Permitem usar sorted, max, min

    # Comparators for sorting individuals based on fitness.
    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    # String representation of the individual.
    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    # Set the fitness value of the individual.
    def setFitness(self, fit):
        self.fitness = fit

    # Get the fitness value of the individual.
    def getFitness(self):
        return self.fitness

    # Get the genes of the individual.
    def getGenes(self):
        return self.genes

    # Initialize the individual randomly.
    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))

    # Mutate the individual by flipping a random bit.
    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    # Crossover the individual with another individual.
    def crossover(self, indiv2):
        return self.one_pt_crossover(indiv2)

    # Perform one-point crossover with another individual.
    def one_pt_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        # Choose a random crossover point.
        pos = randint(0, s-1)
        # Copy the genes up to the crossover point from each parent.
        for i in range(pos):
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        # Copy the genes after the crossover point from the other parent.
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        res1 = self.__class__(s, offsp1, self.lb, self.ub)
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        # Create new individuals with the offspring genes.
        return res1, res2


class IndivInt (Indiv):

    def __init__(self, size: int, genes: list = [], lb: int = 0, ub: int = 1):
        """
        Subclass to implement individuals with binary representation.
        :param size: size of the list of genes
        :param genes: list of genes (representative of genome), by default []
        :param lb: lower limits of the range for representing genes, by default 0
        :param ub: upper limits of the range for representing genes, by default 1
        """
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size: int) -> None:
        """
        Method that generates a list of genes of the individual (random int numbers between upper and lower bounds)
        :param size:  number of genes to generate
        :return:
        """
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = randint(0, self.ub)


class IndivReal(Indiv):

    def initRandom(self, size: int) -> None:
        # The initRandom method initializes the genes of the individual with random values in the interval [lb, ub].
        # In this case, the genes are initialized with random float values between lb and ub using the random function
        # and list comprehension.
        self.genes = [random() * (self.ub - self.lb) + self.lb for _ in range(size)]

    def mutation(self) -> None:
        # The mutation method performs a mutation operation on one randomly selected gene in the individual.
        s = len(self.genes)
        pos = randint(0, s - 1)
        # The mutation is performed by adding a random value in the range [lb, ub] to the selected gene.
        # The random value is generated using the random function and is scaled by the range [lb, ub].
        self.genes[pos] += (random() * (self.ub - self.lb) + self.lb) / 10
        # The new value is then constrained to the interval [lb, ub] to ensure the solution remains feasible.
        # This is done using the min and max functions.
        self.genes[pos] = max(min(self.genes[pos], self.ub), self.lb)

