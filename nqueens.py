import numpy as np
import sys

STOP_CTR = 28
MUTATE = 0.000001
MUTATE_FLAG = True
MAX_ITER = 100000
POPULATION = None


class BoardPosition:
    def __init__(self):
        self.sequence = None
        self.fitness = None
        self.survival = None

    def setSequence(self, val):
        self.sequence = val

    def setFitness(self, fitness):
        self.fitness = fitness

    def setSurvival(self, val):
        self.survival = val

    def getAttr(self):
        return {'sequence': sequence, 'fitness': fitness, 'survival': survival}


def fitness(seq=None):
    """
    returns 28 - <number of conflicts>
    to test for conflicts, we check for
     -> row conflicts
     -> columnar conflicts
     -> diagonal conflicts

    The ideal case can yield upto 28 arrangements of non attacking pairs.
    for iteration 0 -> there are 7 non attacking queens
    for iteration 1 -> there are 6 no attacking queens ..... and so on
    Therefore max fitness = 7 + 6+ 5+4 +3 +2 +1 = 28
    hence fitness val returned will be 28 - <number of clashes>
    """

    # calculate row and column clashes
    # just subtract the unique length of array from total length of array
    # [1,1,1,2,2,2] - [1,2] => 4 clashes
    clashes = 0
    row_col_clashes = abs(8 - len(np.unique(seq)))
    clashes += row_col_clashes

    # calculate diagonal clashes
    for i in range(8):
        for j in range(8):
            if i != j:
                dx = abs(i - j)
                dy = abs(seq[i] - seq[j])
                if (dx == dy):
                    clashes += 1

    return 28 - clashes


def generateSequence():
    # randomly generates a sequence of board states.
    init_distribution = np.arange(8)
    np.random.shuffle(init_distribution)
    return init_distribution


def generatePopulation(population_size=100):
    global POPULATION

    POPULATION = population_size

    population = [BoardPosition() for i in range(population_size)]
    for i in range(population_size):
        population[i].setSequence(generateSequence())
        population[i].setFitness(fitness(population[i].sequence))

    return population


def getParent():
    globals()
    parent1, parent2 = None, None
    # parent is decided by random probability of survival.
    # since the fitness of each board position is an integer >0,
    # we need to normaliza the fitness in order to find the solution

    summation_fitness = np.sum([x.fitness for x in population])
    for each in population:
        each.survival = each.fitness / (summation_fitness * 1.0)

    while True:
        parent1_random = np.random.rand()
        parent1_rn = [x for x in population if x.survival <= parent1_random]
        try:
            parent1 = parent1_rn[0]
            break
        except:
            pass

    while True:
        parent2_random = np.random.rand()
        parent2_rn = [x for x in population if x.survival <= parent2_random]
        try:
            t = np.random.randint(len(parent2_rn))
            parent2 = parent2_rn[t]
            if parent2 != parent1:
                break
            else:
                #print("equal parents")
                continue
        except:
            print("exception")
            continue

    if parent1 is not None and parent2 is not None:
        return parent1, parent2
    else:
        sys.exit(-1)


def reproduce_crossover(parent1, parent2):
    globals()

    c = np.random.randint(8, size=1)
    child = BoardPosition()
    child.sequence = []
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    child.setFitness(fitness(child.sequence))
    return child


def mutate(child):
    """
    - according to genetic theory, a mutation will take place
    when there is an anomaly during cross over state
    - since a computer cannot determine such anomaly, we can define
    the probability of developing such a mutation
    """
    if child.survival < MUTATE:
        c = np.random.randint(8)
        child.sequence[c] = np.random.randint(8)
    return child


def GA(iteration):
    globals()
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = getParent()
        # print "Parents generated : ", parent1, parent2

        child = reproduce_crossover(parent1, parent2)

        if (MUTATE_FLAG):
            child = mutate(child)

        newpopulation.append(child)
    return newpopulation


def stop():
    globals()
    # print population[0], " printing population[0]"
    fitnessvals = [pos.fitness for pos in population]
    if STOP_CTR in fitnessvals:
        return True
    if MAX_ITER == iteration:
        return True
    return False

if __name__ =="__main__":
    population = generatePopulation(1000)

    iteration = 0;
    while not stop():
        # keep iteratin till  you find the best position
        population = GA(iteration)
        iteration += 1

    for each in population:
        if each.fitness == 28:
            print(str(each.sequence)[1:-1])
            break
    #print(fitness([4,6,0,3,1,7,5,2]))