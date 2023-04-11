from package_aab.src.Popul import Popul

class EvolAlgorithm:

    def __init__(self, popsize: int, numits: int, noffspring: int, indsize: int):
        '''Class that implements the Evolutionary Algorithm.
                Parameters
                ----------
                popsize : int
                    size of population
                numits : int
                    number of iterations to perform
                noffspring : int
                    number of new individuals (descendants)
                indsize : int
                    size of individuals (list of genes)
                '''
        self.popsize = popsize  # population size
        self.numits = numits  # number of iterations
        self.noffspring = noffspring  # number of offspring generated per iteration
        self.indsize = indsize  # size of each individual

    def initPopul(self, indsize: int) -> None:
        """
        Method that initializes the population with a given size for individuals.
        :param indsize:  size of individuals (list of genes)
        :return:
        """
        self.popul = Popul(self.popsize, indsize)

    def evaluate(self, indivs: list) -> None:
        """
        Method that calculates the score for each individual, setting its fitness.
        :param indivs: list that represents the individuals solution.
        :return:
        """
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():
                if x == 1:
                    fit += 1.0
            ind.setFitness(fit)
        return None

    def iteration(self) -> None:
        """
        Method auxiliary of the Evolutionary Algorithm cycle (based on the number of iterations wanted).
        :return:
        """
        # Perform one iteration of the evolutionary algorithm
        parents = self.popul.selection(self.noffspring)  # select parents from the population
        offspring = self.popul.recombination(parents, self.noffspring)  # generate offspring through recombination
        self.evaluate(offspring)  # evaluate the fitness of the offspring
        self.popul.reinsertion(offspring)  # reinsert the offspring into the population

    def run(self) -> None:
        """
        Method that runs the evolutionary algorithm cycle until finding the best solution or the number of iterations is reached.
        :return:
        """
        # Run the evolutionary algorithm for the specified number of iterations
        self.initPopul(self.indsize)  # initialize the population
        self.evaluate(self.popul.indivs)  # evaluate the fitness of the initial population
        self.bestsol = self.popul.bestSolution()  # initialize the best solution found so far
        for i in range(self.numits + 1):
            self.iteration()  # perform one iteration of the algorithm
            bs = self.popul.bestSolution()  # find the best solution in the current population
            if bs > self.bestsol:  # update the best solution found so far
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def printBestSolution(self):
        # Print the best solution found by the evolutionary algorithm
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())
