# -*- coding: utf-8 -*-

from package_aab.src.Indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:

    # Initializes the population with random individuals or with a list of individuals if provided
    def __init__(self, popsize, indsize, indivs=[]):
        self.popsize = popsize
        self.indsize = indsize
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    # Returns the individual at the specified index
    def getIndiv(self, index):
        return self.indivs[index]

    # Initializes the population with random individuals
    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    # Returns a list of fitness values for the population or a subset of it
    def getFitnesses(self, indivs=None):
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    # Returns the best solution (individual) in the population
    def bestSolution(self):
        return max(self.indivs)

    # Returns the fitness value of the best solution (individual) in the population
    def bestFitness(self):
        indv = self.bestSolution()
        return indv.getFitness()

    # Performs selection of n individuals using roulette wheel selection
    def selection(self, n, indivs=None):
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    # Performs roulette wheel selection given a list of fitness values
    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    # Performs linear scaling of fitness values to the range [0,1]
    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    # Performs recombination of parent individuals to generate offspring individuals
    def recombination(self, parents, noffspring):
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2)
            offsp1.mutation()
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    # Performs reinsertion of offspring individuals into the population
    def reinsertion(self, offspring):
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        # Call the constructor of the base class with the given arguments
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        # Create a new IndivInt object for each individual in the population
        for _ in range(self.popsize):
            # Set the minimum value for the genes to 0
            # Set the maximum value for the genes to ub (the upper bound)
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]):
        # Call the constructor of the base class with the given arguments
        Popul.__init__(self, popsize, indsize, indivs)
        self.lb = lb
        self.ub = ub

    def initRandomPop(self):
        self.indivs = []
        # Create a new IndivReal object for each individual in the population
        for _ in range(self.popsize):
            # Set the minimum value for the genes to lb (the lower bound)
            # Set the maximum value for the genes to ub (the upper bound)
            indiv_i = IndivReal(self.indsize, [], self.lb, self.ub)
            self.indivs.append(indiv_i)
