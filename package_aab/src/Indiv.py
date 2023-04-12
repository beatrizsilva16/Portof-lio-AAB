from random import randint, uniform
from typing import Union


class Indiv:
    """
    # The Indiv class represents an individual in a genetic algorithm.
    It contains methods for initialization, mutation, crossover, and fitness evaluation.
    """
    def __init__(self, size, genes=[], lb=0, ub=1) -> None:
        self.lb = lb  # lower limit of gene
        self.ub = ub  # upper limit of gene
        self.genes = genes  # genome
        self.fitness = None   # fitness value
        if not self.genes:  # if there is no list of genes
            self.initRandom(size)  # create random individual

    # comparadores.
    # Permitem usar sorted, max, min

    # Comparators for sorting individuals based on fitness.
    def __eq__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    # String representation of the individual.
    def __str__(self) -> str:
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self) -> str:
        return self.__str__()

    # Set the fitness value of the individual.
    def setFitness(self, fit) -> None:
        self.fitness = fit

    # Get the fitness value of the individual.
    def getFitness(self) -> Union[int, float]:
        return self.fitness

    # Get the genes of the individual.
    def getGenes(self) -> list:
        return self.genes

    # Initialize the individual randomly.
    def initRandom(self, size: int) -> None:
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))

    # Mutate the individual by flipping a random bit.
    def mutation(self) -> None:
        s = len(self.genes)
        pos = randint(0, s-1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    # Crossover the individual with another individual.
    def crossover(self, indiv2) -> tuple:
        return self.one_pt_crossover(indiv2)

    # Perform one-point crossover with another individual.
    def one_pt_crossover(self, indiv2) -> tuple:
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
        self.lb = lb  # lower limit of gene
        self.ub = ub  # upper limit of gene
        self.genes = genes  # genome
        self.fitness = None  # fitness values
        if not self.genes:  # if there is no list of genes
            self.initRandom(size)  # create random individual

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
        s = len(self.genes)  # length of genes
        pos = randint(0, s - 1)  # random position
        self.genes[pos] = uniform(self.lb, self.ub)  # replace the position for a random value (0,1)


class IndivReal(Indiv):
    def __init__(self, size: int, genes: list = [], lb: float = 0.0, ub: float = 1.0) -> None:
        self.lb = lb  # lower limit of gene
        self.ub = ub  # upper limit of gene
        self.genes = genes  # genome
        self.fitness = None  # fitness value
        if not self.genes:  # if there is no list of genes
            self.initRandom(size)  # create random individual

    def initRandom(self, size: int) -> None:
        """
        Method that generates a list of genes of the individual with random values in the interval [lb, ub].
        :param size:
        :return:
        """
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub))

    def mutation(self) -> None:
        """
        Method for real representations that alters a single gene (mutation)
        The mutation method performs a mutation operation on one randomly selected gene in the individual.
        :return:
        """
        s = len(self.genes)  # length of genes
        pos = randint(0, s - 1)  # random position
        self.genes[pos] = uniform(self.lb, self.ub)  # replace the position for a random value (0,1)

