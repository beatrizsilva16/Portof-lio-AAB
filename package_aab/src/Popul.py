from package_aab.src.Indiv import Indiv, IndivInt, IndivReal
from random import random
from typing import Union


class Popul:

    def __init__(self, popsize: int, indsize: int, indivs: list = []) -> None:
        '''Class that implements the population with a given size.

        Parameters
        ----------
        :param: popsize : size of population
        :param: indsize : size of individuals (list of genes)
        :param: indivs : list of genes, by default []
        '''
        self.popsize = popsize
        self.indsize = indsize
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    def getIndiv(self, index: int) -> list:
        '''Method that returns a specific individual from the list, given its index.
        :param: index : index of the individual on the list self.indivs
        :returns: list of information about individual: list of genes and fitness (Instance of the class Indiv)
        '''
        return self.indivs[index]

    def initRandomPop(self) -> None:
        '''Method that initializes the population (creates instances of Indiv class)
        '''
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs: list = None) -> list:
        '''Method that returns the fitness information about all the individuals
        :param: list of individuals, by default None
        :returns: list of fitness of all the individuals
        '''
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self) -> list:
        '''Method that returns the best solution of all the individuals (that has the best fitness).
        :returns: the best solution
        '''
        return max(self.indivs)

    def bestFitness(self) -> Union[int, float]:
        '''Method that returns the best fitness of all the individuals
        :returns:the best fitness
        '''
        indv = self.bestSolution()
        return indv.getFitness()

    def selection(self, n: int, indivs: list = None) -> list:
        '''
        :param: n : size of selection (parents)
        :param: indivs : list that represents the individuals, by default None
        :returns: individual (selection list)
        '''
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f: list) -> int:
        '''Method that selects a specific individual based on the probability of its fitnesses
        :param: list of fitnesses
        :returns: index of individual selected
        '''
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind - 1

    def linscaling(self, fitnesses: list) -> list:
        '''Method that normalizes the fitnesses values (0,1)
        :param: list of fitnesses
        :returns: list of normalized fitnesses
        '''
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f - mn) / (mx - mn)
            res.append(val)
        return res

    def recombination(self, parents: list, noffspring: int) -> list:
        '''Method that returns the offspring after crossover between two parents and mutation.
        :param: list of individuals (parents)
        :param: number of offspring individuals to create
        :returns: list of individuals (offspring)
        '''
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds + 1]]
            offsp1, offsp2 = parent1.crossover(parent2)
            offsp1.mutation()
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring: list) -> None:
        '''Method that reinserts individuals (offspring)
        :param: list of individuals (offspring)
        '''
        tokeep = self.selection(self.popsize - len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize: int, indsize: int, ub: int, indivs: list = []) -> None:
        '''Subclass that implements a binary representation of the population with a given size.
        '''
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self) -> None:
        '''Method that initializes the population (creates instances of IndivInt class)
        '''
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):

    def __init__(self, popsize: int, indsize: int, lb: float = 0.0, ub: float = 1.0, indivs: list = []) -> None:
        '''Subclass that implements a real representation of the population with a given size.
        '''
        self.ub = ub
        self.lb = lb
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self) -> None:
        '''Method that initializes the population (creates instances of IndivReal class)
        '''
        self.indivs = []
        for _ in range(self.popsize):
            indiv_r = IndivReal(self.indsize, [], self.lb, self.ub)
            self.indivs.append(indiv_r)