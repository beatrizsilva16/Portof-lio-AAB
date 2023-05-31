from random import randint, random, shuffle, uniform
from typing import Union


class Indiv:

    def __init__(self, size: int, genes: list = [], lb: int = 0, ub: int = 1) -> None:
        '''Class to implement individuals with binary and real representations, with the atributes:
        - lb/ub (lower and upper limits of the range for representing genes)
        - fitness (stores fitness value for each individual)
        :param: size :size of the list of genes
        :param: genes : list of genes (representative of genome), by default []
        :param: lower limits of the range for representing genes, by default 0
        :param: ub : upper limits of the range for representing genes, by default 1
        '''
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:  # random generation of list of genes:
            self.initRandom(size)

    # comparadores.
    # Permitem usar sorted, max, min

    def __eq__(self, solution: list) -> bool:
        '''Method auxiliary that determines if the solution is an instance of Indiv class.
        :param: solution : individual (instance of class if true)
        :returns: True if solution is instance of this class
        '''
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution: list) -> bool:
        '''Method auxiliary that determines if the current fitness is greater than the solutions' fitness.
        :param: solution :individual (instance of class if true)
        :return: True if current fitness is greater than its solution
        '''
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution: list) -> bool:
        '''Method auxiliary that determines if the current fitness is greater or equal than the solutions' fitness.
        :param: solution : individual (instance of class if true)
        :returns: True if current fitness is greater or equal than its solution
        '''
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution: list) -> bool:
        '''Method auxiliary that determines if the solution fitness is greater than the current.
        :param:solution : individual (instance of class if true)
        :returns: True if the solution fitness is greater than the curent fitness
        '''
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution: list) -> bool:
        '''Method auxiliary that determines if the solution fitness is greater or equal than the current.
        :param: solution : individual (instance of class if true)
        :returns: True if the solution fitness is greater or equal than the curent fitness
        '''
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self) -> str:
        ''' Method that writes the information about the object: the list of genes and its fitness
        :returns: String with the information of the object
        '''
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self) -> str:
        ''' Method that shows the information about the object
        :returns: String with the information of the object
        '''
        return self.__str__()

    def setFitness(self, fit: Union[int, float]) -> None:
        '''Method that sets the new fitness of the individual
        :param: fitness of the individual
        '''
        self.fitness = fit

    def getFitness(self) -> Union[int, float]:
        '''Method that shows the fitness of the individual
        :returns: fitness of the individual
        '''
        return self.fitness

    def getGenes(self) -> list:
        '''Method that shows the list of genes of the individual
        :returns: list of genes of the individual
        '''
        return self.genes

    def initRandom(self, size: int) -> None:
        '''Method that generates a list of genes of the individual (random int numbers between upper and lower bounds)
        :param: number of genes to generate
        '''
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))

    def mutation(self) -> None:
        '''Method for binary representations that alters a single gene (mutation)
        '''
        s = len(self.genes)
        pos = randint(0, s - 1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    def crossover(self, indiv2) -> tuple:
        '''Method that makes a crossover between two individuals
        :param: indiv2 : type[Indiv]
        '''
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2: list) -> tuple:
        '''Auxiliary method that makes a crossover between two individuals
        :param: indiv2 : list
            individual (instance of Indiv class)
        :returns: the new individuals with list of genes crossed-over
        '''
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0, s - 1)
        for i in range(pos):
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        res1 = self.__class__(s, offsp1, self.lb, self.ub)
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt(Indiv):

    def __init__(self, size: int, genes: list = [], lb: int = 0, ub: int = 1) -> None:
        '''Subclass to implement individuals with binary representation.
        :param: size : size of the list of genes
        :param: genes :  list of genes (representative of genome), by default []
        :param: lb : lower limits of the range for representing genes, by default 0
        :param: upper limits of the range for representing genes, by default 1
        '''
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size: int) -> None:
        '''Method that generates a list of genes of the individual (random int numbers between upper and lower bounds)
         :param: number of genes to generate
        '''
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))


class IndivReal(Indiv):

    def __init__(self, size: int, genes: list = [], lb: float = 0.0, ub: float = 1.0) -> None:
        '''Subclass to implement individuals with real representation.
        :param: size : size of the list of genes
        :param: genes : list of genes (representative of genome), by default []
        :param: lb :  lower limits of the range for representing genes, by default 0.0
        :param: ub :  upper limits of the range for representing genes, by default 1.0
        '''
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size: int) -> None:
        '''Method that generates a list of genes of the individual (random float numbers between upper and lower bounds)
        :param: number of genes to generate
        '''
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub))

    def mutation(self) -> None:
        '''Method for real representations that alters a single gene (mutation)
        '''
        s = len(self.genes)
        pos = randint(0, s - 1)
        self.genes[pos] = uniform(self.lb, self.ub)

